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
    
    def alter_moves(self, w: List[str]):
        spaces = list(self.ad.keys())
        ret_space = []
        for space in spaces:
            u, v = self.ad[space]
            u, v = self.i+u, self.j+v
            if 0<=u<self.n and 0<=v<self.m and f"{u},{v}" not in w:
                ret_space.append(space)
        
        return ret_space
    
    def act(self, move, tick):
        if move:
            u, v = self.ad[move]
            self.i+=u
            self.j+=v
        else:
            move = ""
        return f"{tick}: {self.name} moving {move}\n"
    
    def position(self):
        return f"{self.i},{self.j}"
    
    def __str__(self) -> str:
        return self.position()

class GhostActor(Actor):
    def __init__(self, name, i, j, n, m):
        super().__init__(name, i, j, n, m)
        
    def alter_moves(self, w: List[str], ghosts: List['GhostActor']):
        spaces = super().alter_moves(w)
        ghosts_pos = [g.position() for g in ghosts]
        ret_space = []
        for space in spaces:
            u, v = self.ad[space]
            u, v = self.i+u, self.j+v
            if f"{u},{v}" not in ghosts_pos:
                ret_space.append(space)
        return ret_space


class Scheduler:
    def __init__(self, state: List[List[str]], pacman: Actor, ghosts: List[GhostActor], foods: List[str], wall: List[str]) -> None:
        self.state = state
        self.pacman = pacman
        self.ghosts = ghosts
        self.foods = foods
        self.wall = wall
        
    def figure(self, before_position: str, after_position: str, flag: str):
        i, j = list(map(int, before_position.split(",")))
        u, v = list(map(int, after_position.split(",")))
        self.state[i][j] = ' ' if before_position not in self.foods else '.'
        self.state[u][v] = flag
        return ["".join(x)+"\n" for x in self.state]
    
    def manhattan_score(self, move):
        i, j = self.pacman.i, self.pacman.j
        i, j = i + self.pacman.ad[move][0], j + self.pacman.ad[move][1]
        closest_ghost = min([abs(x.i-i) + abs(x.j-j) for x in self.ghosts])        
        closest_food = min([abs(int(f.split(',')[0])-i)+abs(int(f.split(',')[1])-j) for f in self.foods])
        # lower is better
        return closest_food - closest_ghost
    
    def argmin(self, moves):
        scores = [self.manhattan_score(move) for move in moves]
        idx = scores.index(min(scores))
        ret_move = moves[idx]
        return ret_move
            
    
    def process(self, tick=0):
        board = 0
        tick = tick
        result = []
        try:
        # for i in [0]:
            while True:
                move = self.argmin(self.pacman.alter_moves(self.wall))
                before = self.pacman.position()
                tick += 1
                result.append(self.pacman.act(move, tick))
                board += PACMAN_MOVING_SCORE
                ghost_pos = [w.position() for w in self.ghosts]
                current = self.pacman.position()
                if current in ghost_pos:
                    u, v = list(map(int, current.split(',')))
                    result.extend(self.figure(before, current, self.state[u][v]))
                    board += PACMAN_EATEN_SCORE
                    raise Exception("Bad terminate")
                result.extend(self.figure(before, current, self.pacman.name))
                if self.pacman.position() in self.foods:
                    self.foods.remove(self.pacman.position())
                    board += EAT_FOOD_SCORE
                    if len(self.foods) == 0:
                        board += PACMAN_WIN_SCORE
                        raise Exception("Pacman Win!")
                result.append(f"score: {board}\n")
                for ghost in self.ghosts:
                    moves = ghost.alter_moves(self.wall, self.ghosts)
                    move = None
                    if len(moves) > 0:
                        move = random.choice(moves)
                    before = ghost.position()
                    tick += 1
                    result.append(ghost.act(move, tick))
                    result.extend(self.figure(before, ghost.position(), ghost.name))
                    if ghost.position() == self.pacman.position():
                        board += PACMAN_EATEN_SCORE
                        raise Exception("Bad terminate")
                    result.append(f"score: {board}\n")
        except Exception as e:
            # print(e)
            # bad terminate
            if len(self.foods)>0:
                result.append(f"score: {board}\n")
                result.append("WIN: Ghost")
            else:
                # food clear
                result.append(f"score: {board}\n")
                result.append("WIN: Pacman")
                
        return result
        

def p4(seed, state):
    # random.seed(seed)
    tick = 0
    result = [f"seed: {seed}\n", f"{tick}\n"]
    result.extend(["".join(x)+"\n" for x in state])
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
    result.extend(s.process(tick))
    return "".join(result)

def better_play_multiple_ghosts(problem):
    #Your p4 code here
    solution = p4(**problem)
    winner = solution.split(' ')[-1]
    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)