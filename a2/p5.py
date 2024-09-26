import math
import random
import sys, parse
from typing import List
import time, os, copy

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

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
    
    def collision(self, node: List[Actor]):
        return node[0].position() in [x.position() for x in node[1:]]
    

    def add_score(self, node: List[GhostActor]):
        """minimax k state score evaluate function.

        Args:
            node (List[GhostActor]): list of actor
            turn (int, optional): who is active. Defaults to 0.

        Returns:
            float: the score value for minimax
        """
        # it is a difficult task to design the score evalution function
        i, j = node[0].raw_pos()
        uvlist = [[n.i, n.j] for n in node[1:]]
        # too close to GHOST!!! pacman deserve punishment
        score = PACMAN_EATEN_SCORE if min(abs(i-u)+abs(j-v) for u, v in uvlist) < 2 else 0
        xylist = [list(map(int, f.split(','))) for f in self.foods]
        fd = [abs(i-u)+abs(j-v) for u, v in xylist]
        fd = [v for v in fd if v < 2]
        # how many foods surround pacman
        score += EAT_FOOD_SCORE * len(fd)
        return score

    def minimax_score(self, node: List[GhostActor], k: int, begin: int, turn: int, a: float=float('-inf'), b: float=float('inf')):
        """score calculate node in k moves

        Args:
            node (List[GhostActor]): list of actor
            k (int): k depth
            begin (int): entry actor
            turn (int): who is current actor

        Returns:
            float: expecti max score
        """
        # terminate
        if k <= 0:
            return self.add_score(node, turn)

        elif turn == 0:
            # pacman maximize
            k -= 1
            score = float('-inf')
            moves = node[turn].alter_pos(self.wall, node[1:])
            if len(moves) == 0:
                return score
            org = node[turn].raw_pos()
            for move in moves:
                node[turn].act(move)
                if node[turn].position() in [n.position() for n in node[1:]]:
                    return PACMAN_EATEN_SCORE
                score = 0
                borrow = False
                if f"{move[0]},{move[1]}" in self.foods:
                    if len(self.foods) == 1:
                        return PACMAN_WIN_SCORE
                    self.foods.remove(f"{move[0]},{move[1]}")
                    borrow = True
                score += max(score, self.minimax_score(node, k, begin, (turn+1) % len(node), a, b))
                if borrow:
                    self.foods.append(f"{move[0]},{move[1]}")
                a = max(a, score)
                if b <= a:
                    break
            node[turn].act(org)
            return score
        else:
            # ghost minimize
            score = float('inf')
            moves = node[turn].alter_pos(self.wall, node[1:])
            if len(moves) == 0:
                return score
            org = node[turn].raw_pos()
            for move in moves:
                node[turn].act(move)
                if node[turn].position() == node[0].position():
                    return PACMAN_EATEN_SCORE
                score = min(score, self.minimax_score(node, k, begin, (turn+1) % len(node), a, b))
                b = min(b, score)
                if b <= a:
                    break
            node[turn].act(org)
            return score
    
    def minimax_move(self, k, begin: int=0):
        # start moving
        if begin == 0:
            moves = self.pacman.alter_moves(self.wall, self.ghosts)
        else:
            moves = self.ghosts[begin-1].alter_moves(self.wall, self.ghosts)
        
        
        if len(moves) == 0:
            return None
        sim_actors = [self.pacman, *self.ghosts]
        org = sim_actors[begin].raw_pos()
        scores = []
        # scores in each direction
        for move in moves:
            sim_actors[begin].act(move)
            scores.append(self.minimax_score(sim_actors, k, begin, begin))
        sim_actors[begin].act(org)
        if begin == 0:
            ms = max(scores)
        else:
            ms = min(scores)
        best = [i for i in range(len(scores)) if scores[i] == ms]
        return random.choice([moves[i] for i in best])
        
    
    def process(self, tick=0, k=10):
        result = []
        try:
        # for i in [0]:
            while True:
                move = self.minimax_move(k)
                self.pacman.act(move, tick)
                if self.pacman.position() in [g.position() for g in self.ghosts]:
                    raise Exception("Ghost Win!")
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