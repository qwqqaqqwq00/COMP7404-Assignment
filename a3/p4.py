import argparse
import copy
import math
import random, grader, parse
from typing import List

class Env:
    def __init__(self, discount: float, noise: float, livingReward: float, stop_eps: float, alpha: float, grid: List[List[str]]) -> None:
        self.actions = {'N': [-1,0], 'E':[0,1], 'S':[1,0], 'W':[0,-1]}
        self.directs = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
        self.discount = discount
        self.noise = noise
        self.livingReward = livingReward
        self.stop_eps = stop_eps
        self.alpha = alpha
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
    
    def translate(self, i, j):
        if self.policy[i][j] == 'x':
            return self.grid[i][j]
        elif self.policy[i][j] == '#':
            return self.policy[i][j]
        elif self.policy[i][j] not in self.actions.keys():
            return self.policy[i][j]
        translate = {"N":"↑","E":"→","S":"↓","W":"←"}
        return translate[self.policy[i][j]]
    
    def print_pi(self):
        result = ""
        for i in range(self.n):
            linestr = ""
            for j in range(self.m):
                linestr += "|{:^7}|".format(self.translate(i, j))
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
    
    def get_action(self, i, j):
        names = []
        result = []
        for n in self.actions.keys():
            a, b = self.actions[n]
            a, b = a+i, b+j
            if 0<=a<self.n and 0<=b<self.m and [a, b] not in self.world['#']:
                result.append([a,b])
                names.append(n)
            # else:
                # result.append([i,j])
        return names, result
        
    def epsilon_greedy(self, i, j):
        if [i, j] in self.world['#']:
            return '#'
        for pos, _ in self.exit_state:
            if pos == [i, j]:
                return 'x'
        
        result = []
        for d0 in self.actions.keys():
            a, b = self.actions[d0]
            a, b = a+i, b+j
            if 0<=a<self.n and 0<=b<self.m and [a, b] not in self.world['#']:
                result.append([a,b])
            # else:
                # result.append([i,j])
        key = list(self.actions.keys())[result.index(max(result))]
        choice = random.choices(self.directs[key], [1-2*self.noise, self.noise, self.noise])[0]
        return choice
                    
    def argmax_policy(self, i, j):
        names, actions = self.get_action(i, j)
        val = [self.Q[a][b] for a, b in actions]
        return names[val.index(max(val))]
                    
    def process(self):
        result = ""
        iteration = 0
        loss = float('inf')
        # start state
        while loss > self.stop_eps:
            self.setup_agents()
            iteration += 1
            intend = ''
            Q = copy.deepcopy(self.Q)
            while intend != 'x':
                i, j = self.agents
                intend = self.epsilon_greedy(i, j)
                value = 0
                if intend == 'x':
                    value += int(self.grid[i][j])
                    Q[i][j] = value
                elif intend == '#':
                    continue
                else:
                    # off-policy
                    self.policy[i][j] = self.argmax_policy(i, j)
                    value += self.livingReward
                    neibors = self.get_neibor([i, j], intend)
                    self.agents = neibors[0]
                    for idx in range(len(neibors)):
                        a, b = neibors[idx]
                        noise = self.noise if idx > 0 else 1 - 2 * self.noise
                        value += self.discount * noise * self.Q[a][b]
                    Q[i][j] = value * self.alpha + (1 - self.alpha) * self.Q[i][j] # + self.livingReward
            prev = [x for l in self.Q for x in l if not isinstance(x, str)]
            nxt  = [x for l in Q for x in l if not isinstance(x, str)]
            loss = abs(sum(prev)-sum(nxt))
            print(f"Iteration: {iteration} | Loss: {loss}")
            self.Q = Q
        print("Result:")
        print(self.print_value())
        print(self.print_pi())
        return result
        

def p4(discount, noise, livingReward, stop_epsilon, alpha, grid_file, **kwargs):
    with open(grid_file, 'r') as f:
        grid = f.readlines()
    grid = list(map(lambda x:x.strip().split(','), grid))
    env = Env(discount, noise, livingReward, stop_epsilon, alpha, grid)
    result = env.process().rstrip('\n')
    return result

def TDLearning(args):
    result = p4(args.discount, args.noise, args.livingReward, args.stop_epsilon, args.alpha, args.grid_file)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--discount", help="discount", type=float, default=0.9)
    parser.add_argument("--noise", help="noise", type=float, default=0.2)
    parser.add_argument("--livingReward", help="livingReward", type=float, default=-0.1)
    parser.add_argument("--stop_epsilon", help="the spsilon decide when to stop", type=float, default=1e-7)
    parser.add_argument("--alpha", "alpha decide the weight of update Q table", type=float, default=0.8)
    parser.add_argument("--grid_file", help="grid world file path, sep=','", type=str, default='test_cases/p4/1.prob')
    args = parser.parse_args()
    
    TDLearning(args)