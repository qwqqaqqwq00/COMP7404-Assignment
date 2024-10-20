import copy
import sys, grader, parse
from decimal import Decimal
import sys, random, grader, parse
from typing import List

class Env:
    def __init__(self, discount: float, noise: float, livingReward: float, iterations: int, grid: List[List[str]], policy: List[List[str]]) -> None:
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
        self.policy = policy
        self.world: dict[str, list[list[int]]] = {'S':[], '#':[]}
        self.exit_state = []
        self.cumulativeReward = 0.0
        self.agents = None
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 'S':
                    self.world['S'] = [i,j]
                    self.grid[i][j] = 'S'
                elif self.grid[i][j] == '#':
                    self.world[self.grid[i][j]].append([i,j])
                    self.Q[i][j] = ' #####'
                elif self.policy[i][j] == 'exit':
                    score = int(self.grid[i][j])
                    self.exit_state.append([[i,j],score])
        self.setup_agents()
    
    def setup_agents(self):
        self.agents = self.world['S']
        
    def print_state(self):
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
            
    def process(self):
        result = ""
        iteration = 0
        # start state
        result += f'V^pi_k={iteration}\n'
        result += self.print_state()
        while iteration < self.iterations - 1:
            self.setup_agents()
            iteration += 1
            Q = copy.deepcopy(self.Q)
            for i in range(self.n):
                for j in range(self.m):
                    intend = self.policy[i][j]
                    value = 0
                    if intend == 'exit':
                        value += int(self.grid[i][j])
                    elif intend == '#':
                        continue
                    else:
                        value += self.livingReward
                        neibors = self.get_neibor([i, j], intend)
                        for idx in range(len(neibors)):
                            a, b = neibors[idx]
                            noise = self.noise if idx > 0 else 1 - 2 * self.noise
                            value += self.discount * noise * self.Q[a][b]
                    Q[i][j] = value
            self.Q = Q
            result += f'V^pi_k={iteration}\n'
            result += self.print_state()
        return result
        

def p2(discount, noise, livingReward, iterations, grid, policy):
    env = Env(discount, noise, livingReward, iterations, grid, policy)
    result = env.process().rstrip('\n')
    return result

def policy_evaluation(problem):
    return_value = p2(**problem)
    return return_value

if __name__ == "__main__":
    # test_case_id = 7
    test_case_id = int(sys.argv[1])
    problem_id = 2
    # for test_case_id in range(8):
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)