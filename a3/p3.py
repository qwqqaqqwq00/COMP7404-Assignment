import copy
from decimal import Decimal
import sys, random, grader, parse
from typing import List

class Env:
    def __init__(self, discount: float, noise: float, livingReward: float, iterations: int, grid: List[List[str]]) -> None:
        self.actions = {'N': [-1,0], 'E':[0,1], 'S':[1,0], 'W':[0,-1]}
        self.directs = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
        self.discount = discount
        self.noise = noise
        self.livingReward = livingReward
        self.iterations = iterations
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])
        self.Q = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.policy = [['' for _ in range(self.m)] for _ in range(self.n)]
        self.world: dict[str, list[list[int]]] = {'S':[], '#':[]}
        self.exit_state = []
        self.agents = None
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 'S':
                    self.world['S'] = [i,j]
                    self.grid[i][j] = 'S'
                elif self.grid[i][j] == '#':
                    self.world[self.grid[i][j]].append([i,j])
                    self.Q[i][j] = ' #####'
                    self.policy[i][j] = '#'
                elif self.grid[i][j] != '_':
                    score = int(self.grid[i][j])
                    self.exit_state.append([[i,j],score])
                    self.policy[i][j] = 'x'
        self.setup_agents()
    
    def setup_agents(self):
        self.agents = self.world['S']
        
    def print_value(self):
        result = ""
        for gl in self.Q:
            linestr = ''
            for x in gl:
                if not isinstance(x, str):
                    linestr += "|{:7.2f}|".format(x)
                else:
                    linestr += "|{:7}|".format(x)
            result+=f"{linestr}\n"
        return result
    
    def print_pi(self):
        result = ""
        for i in range(self.n):
            linestr = ""
            for j in range(self.m):
                linestr += "| {} |".format(self.policy[i][j])
            result+=f"{linestr}\n"
        return result
    
    def get_neibor(self, agent, action):
        result = []
        i, j = agent
        for n in self.directs[action]:
            a, b = self.actions[n]
            a, b = a+i, b+j
            if 0<=a<self.n and 0<=b<self.m and [a, b] not in self.world['#']:
                result.append([a,b])
            else:
                result.append([i,j])
        return result
    
    def argmax(self, i, j):
        if [i, j] in self.world['#']:
            return '#'
        for pos, _ in self.exit_state:
            if pos == [i, j]:
                return 'x'
        
        ret, val = 'N', float('-inf')
        # act = [self.get_neibor([i,j],n)[0] for n in self.directs.keys()]
        # act = [self.Q[a][b] for a,b in act]
        # ret = list(self.directs.keys())[act.index(max(act))]
        for d0 in self.actions.keys():
            tmpval = 0
            neibors = self.get_neibor([i, j], d0)
            for idx in range(len(neibors)):
                a, b = neibors[idx]
                noise = self.noise if idx > 0 else 1 - 2 * self.noise
                tmpval += noise * self.Q[a][b]
            if tmpval>val:
                ret = d0
                val = tmpval
        return ret
            
    def process(self):
        result = ""
        iteration = 0
        # start state
        result += f'V_k={iteration}\n'
        result += self.print_value()
        while iteration < self.iterations - 1:
            self.setup_agents()
            iteration += 1
            Q = copy.deepcopy(self.Q)
            for i in range(self.n):
                for j in range(self.m):
                    # off-policy
                    intend = self.argmax(i, j)
                    value = 0
                    if intend == 'x':
                        value += int(self.grid[i][j])
                    elif intend == '#':
                        continue
                    else:
                        self.policy[i][j] = intend
                        value += self.livingReward
                        neibors = self.get_neibor([i, j], intend)
                        for idx in range(len(neibors)):
                            a, b = neibors[idx]
                            noise = self.noise if idx > 0 else 1 - 2 * self.noise
                            value += self.discount * noise * self.Q[a][b]
                    Q[i][j] = value
            self.Q = Q
            result += f'V_k={iteration}\n'
            result += self.print_value()
            result += f"pi_k={iteration}\n"
            result += self.print_pi()
        return result
        

def p2(discount, noise, livingReward, iterations, grid):
    env = Env(discount, noise, livingReward, iterations, grid)
    result = env.process().rstrip('\n')
    return result

def value_iteration(problem):
    result = p2(**problem)
    return result

if __name__ == "__main__":
    # test_case_id = int(sys.argv[1])
    test_case_id = 3
    problem_id = 3
    # for test_case_id in range(5):
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)