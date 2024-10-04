'''
able to pass all sample test case in 11s-242s on AMD R9-7940HX
'''
from collections import deque
from functools import lru_cache
import math
import random
import sys, parse
from typing import List
import time, os, copy

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

# BEST_PERFORM = {
#     1: 164,
#     2: 2,
#     3: 0,
#     4: 1966,
#     5: 6,
#     6: 27,
#     7: 2,
#     8: 7,
#     9: 65
# }

class Actor:
    def __init__(self, name, i, j, n, m):
        self.name = name
        self.i = i
        self.j = j
        self.n = n
        self.m = m
        self.ad = {
            "E": [0, 1],
            "N": [-1, 0],
            "S": [1, 0],
            "W": [0, -1]
        }
    
    def alter_moves(self, w: List[str], ghosts = None):
        spaces = list(self.ad.keys())
        ret_space = []
        for space in spaces:
            u, v = self.ad[space]
            u, v = self.i+u, self.j+v
            if 0<=u<self.n and 0<=v<self.m and f"{u},{v}" not in w:
                ret_space.append(space)
        
        return ret_space
    
    def alter_pos(self, w: List[str], ghosts: List['Actor'] = None):
        alter_moves = self.alter_moves(w, ghosts)
        alter_moves = [self.ad[m] for m in alter_moves]
        return [[self.i+u, self.j+v] for u, v in alter_moves]
    
    def act(self, move, tick=0):
        if move:
            if isinstance(move, list):
                u, v = move
                self.i = u
                self.j = v
            else:
                u, v = self.ad[move]
                self.i+=u
                self.j+=v
        else:
            move = ""
        return f"{tick}: {self.name} moving {move}\n"
    
    def raw_pos(self):
        return [self.i, self.j]
    
    def raw_move(self, move):
        return [self.i + self.ad[move][0], self.j + self.ad[move][1]]
    
    def position(self):
        return f"{self.i},{self.j}"
    
    def __str__(self) -> str:
        return self.position()

class GhostActor(Actor):
    def __init__(self, name, i, j, n, m):
        super().__init__(name, i, j, n, m)
        
    def alter_moves(self, w: List[str], ghosts: List['GhostActor']):
        spaces = super().alter_moves(w, ghosts=ghosts)
        ghosts_pos = [g.position() for g in ghosts]
        ret_space = []
        for space in spaces:
            u, v = self.ad[space]
            u, v = self.i+u, self.j+v
            if f"{u},{v}" not in ghosts_pos:
                ret_space.append(space)
        return ret_space

class Scheduler:
    def __init__(self, state: List[List[str]], pacman: GhostActor, ghosts: List[GhostActor], foods: List[str], wall: List[str]) -> None:
        self.state = state
        self.pacman = pacman
        self.ghosts = ghosts
        self.foods = foods
        self.wall = wall
        self.start = self.pacman.raw_pos()
        self.q = deque()
        self.vis = set()
    
    @lru_cache(maxsize=32)
    def q_append(self, u, v, d):
        for a, b in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            a,b = u+a,v+b
            if f"{a},{b}" not in self.vis and f"{a},{b}" not in self.wall:
                self.q.append([a,b, d+1])

    def bfs(self, i, j):
        self.q.clear()
        self.vis.clear()
        self.q.append([i, j, 0])
        closest_ghost = 0
        gs = set(g.position() for g in self.ghosts)
        fd = 0
        while len(self.q)>0:
            u, v, d = self.q.popleft()
            self.vis.add(f"{u},{v}")
            if d > 3:break
            if f"{u},{v}" in gs:
                closest_ghost = d * 50
                break
            # add food score
            # food score = eat food - walk cost
            if f"{u},{v}" in self.foods:
                fd += -d
            self.q_append(u, v, d)
        return closest_ghost + fd

    # @lru_cache(maxsize=8)
    def add_score(self, i, j):
        """minimax k state score evaluate function.

        Args:
            node (List[GhostActor]): list of actor
            turn (int, optional): who is active. Defaults to 0.

        Returns:
            float: the score value for minimax
        """
        # it is a difficult task to design the score evalution function
        return self.bfs(i, j)

    @lru_cache(maxsize=32)
    def minimax_score(self, k: int, begin: int, turn: int, a: float=float('-inf'), b: float=float('inf')):
        # minimax tree
        
        # terminate, minimax tree node
        if k <= 0:
            i, j = self.pacman.raw_pos()
            return self.add_score(i, j)

        elif turn == 0:
            # pacman maximize
            k -= 1
            score = float('-inf')
            moves = self.pacman.alter_pos(self.wall, self.ghosts)
            # skip do action
            if len(moves) == 0:
                return score
            org = self.pacman.raw_pos()
            gs = [n.position() for n in self.ghosts]
            for move in moves:
                self.pacman.act(move)
                # failed on pacman was eaten
                # if this state near to ghost, then it would be eaten by ghost next moment
                if self.pacman.position() in gs:
                    return PACMAN_EATEN_SCORE
                # alpha-beta pruning
                score += max(score, self.minimax_score(k, begin, (turn+1) % (len(self.ghosts)+1), a, b))
                a = max(a, score)
                if b <= a:
                    break
            # reset pacman state
            self.pacman.act(org)
            return score
        else:
            # ghost minimize
            score = float('inf')
            moves = self.ghosts[turn-1].alter_pos(self.wall, self.ghosts)
            # skip do action
            if len(moves) == 0:
                return score
            org = self.ghosts[turn-1].raw_pos()
            for move in moves:
                self.ghosts[turn-1].act(move)
                # if ghost win, stop (min)
                if self.ghosts[turn-1].position() == self.pacman.position():
                    return PACMAN_EATEN_SCORE
                # alpha-beta pruning
                score = min(score, self.minimax_score(k, begin, (turn+1) % (len(self.ghosts)+1), a, b))
                b = min(b, score)
                if b <= a:
                    break
            # reset ghost state
            self.ghosts[turn-1].act(org)
            return score
    
    def minimax_move(self, k, begin: int=0):
        # root of minimax
        # start moving
        if begin == 0:
            moves = self.pacman.alter_moves(self.wall, self.ghosts)
            p = self.pacman
        else:
            moves = self.ghosts[begin-1].alter_moves(self.wall, self.ghosts)
            p = self.ghosts[begin-1]
        
        if len(moves) == 0:
            return None
        # sim_actors = [self.pacman, *self.ghosts]
        org = p.raw_pos()
        scores = []
        # scores in each direction
        for move in moves:
            p.act(move)
            scores.append(self.minimax_score(k, begin, begin))
        p.act(org)
        if begin == 0:
            ms = max(scores)
        else:
            ms = min(scores)
        best = [i for i in range(len(scores)) if scores[i] == ms]
        try:
            move = random.choice([moves[i] for i in best])
            return move
        except:
            return None
        
    
    def process(self, tick=0, k=10):
        result = []
        try:
            while True:
                move = self.minimax_move(k)
                self.pacman.act(move, tick)
                if self.pacman.position() in self.foods:
                    self.foods.remove(self.pacman.position())
                    if len(self.foods) == 0:
                        raise Exception("Pacman Win!")
                for i, ghost in enumerate(self.ghosts):
                    move = self.minimax_move(k, i+1)
                    ghost.act(move, tick)
                    if ghost.position() == self.pacman.position():
                        raise Exception("Ghost Win!")
        except Exception as e:
            # print(e)
            # bad terminate
            if len(self.foods)>0:
                result.append("WIN: Ghost")
            else:
                # food clear
                result.append("WIN: Pacman")
        return result
        

def p5(k, seed, state):
    # random.seed(seed)
    tick = 0
    result = [f"seed: {seed}\n", f"{tick}\n"]
    n, m = len(state), len(state[0])
    p = None
    g = []
    f = []
    w = []
    for i in range(n):
        for j in range(m):
            if state[i][j] == 'P':
                p = Actor("P", i, j, n, m)
            elif state[i][j] == '.':
                f.append(f"{i},{j}")
            elif state[i][j] == '%':
                w.append(f"{i},{j}")
            elif state[i][j] == ' ':
                continue
            else:
                g.append(GhostActor(state[i][j], i,j,n,m))
    assert(p is not None)
    g.sort(key=lambda x: x.name)
    s = Scheduler(state, p, g, f, w)
    result.extend(s.process(tick, k))
    return "".join(result)

def min_max_multiple_ghosts(problem, k):
    #Your p5 code here
    solution = p5(k, **problem)
    winner = solution.split(' ')[-1]
    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    # problem['seed'] = BEST_PERFORM[test_case_id]
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)
