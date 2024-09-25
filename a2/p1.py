import sys, random, grader, parse
from typing import List

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
        u, v = self.ad[move]
        self.i+=u
        self.j+=v
        return f"{tick}: {self.name} moving {move}\n"
    
    def position(self):
        return f"{self.i},{self.j}"
    
    def __str__(self) -> str:
        return self.position()


class Scheduler:
    def __init__(self, state: List[List[str]], pacman: Actor, ghosts: List[Actor], foods: List[str], wall: List[str]) -> None:
        self.state = state
        self.pacman = pacman
        self.ghosts = ghosts
        self.foods = foods
        self.wall = wall
        
    def figure(self, before_position: str, after_position: str, flag: str):
        i, j = list(map(int, before_position.split(",")))
        u, v = list(map(int, after_position.split(",")))
        # to be notified: ghost can walk on to pacman's food
        self.state[i][j] = ' ' if before_position not in self.foods else '.'
        self.state[u][v] = flag
        return ["".join(x)+"\n" for x in self.state]
    
    def process(self, tick=0):
        board = 0
        tick = tick
        result = []
        try:
            while True:
                move = random.choice(self.pacman.alter_moves(self.wall))
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
                    move = random.choice(ghost.alter_moves(self.wall))
                    before = ghost.position()
                    tick += 1
                    result.append(ghost.act(move, tick))
                    result.extend(self.figure(before, ghost.position(), ghost.name))
                    if ghost.position() == self.pacman.position():
                        board += PACMAN_EATEN_SCORE
                        raise Exception("Bad terminate")
                    result.append(f"score: {board}\n")
        except Exception as e:
            # bad terminate
            if len(self.foods)>0:
                result.append(f"score: {board}\n")
                result.append("WIN: Ghost")
            else:
                # food clear
                result.append(f"score: {board}\n")
                result.append("WIN: Pacman")
                
        return result
        

def p1(seed, state):
    random.seed(seed)
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
                g.append(Actor(state[i][j], i,j,n,m))
    assert(p is not None)
    s = Scheduler(state, p, g, f, w)
    result.extend(s.process(tick))
    return "".join(result)

def random_play_single_ghost(problem):
    #Your p1 code here
    solution = p1(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)