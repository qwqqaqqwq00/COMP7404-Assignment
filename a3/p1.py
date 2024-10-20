import copy
from decimal import Decimal
import sys, random, grader, parse
from typing import List

class Env:
    def __init__(self, noise: float, livingReward: float, grid: List[List[str]], policy: List[List[str]]) -> None:
        self.actions = {'N': [-1,0], 'E':[0,1], 'S':[1,0], 'W':[0,-1]}
        self.noise = noise
        self.livingReward = Decimal("{:f}".format(livingReward))
        self.grid = grid
        self.n = len(grid)
        self.m = len(grid[0])
        self.policy = policy
        self.world: dict[str, list[list[int]]] = {'S':[], '#':[]}
        self.exit_state: List[List[int]] = []
        self.cumulativeReward = Decimal("0.0")
        self.agents = None
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 'S':
                    self.world['S'] = [i,j]
                    # self.agents = self.world['S']
                    self.grid[i][j] = 'S'
                elif self.grid[i][j] != '_' and self.policy[i][j] != 'exit':
                    # if not self.world.get(self.grid[i][j]):
                        # self.world[self.grid[i][j]] = []
                    self.world[self.grid[i][j]].append([i,j])
                elif self.policy[i][j] == 'exit':
                    score = int(self.grid[i][j])
                    self.exit_state.append([[i,j],score])
                    
        self.agents = self.world['S']
        
    def print_state(self, exit=False):
        grid_world = copy.deepcopy(self.grid)
        i,j = self.agents
        if not exit:
            grid_world[i][j] = 'P'
        result = ""
        for gl in grid_world:
            linestr = ''
            for x in gl:
                linestr += "{:>5}".format(x)
            result+=f"{linestr}\n"
        return result
            
    def valid_position(self, i, j):
        return 0<=i<self.n and 0<=j<self.m and [i, j] not in self.world['#']
    
    def not_collision(self, i, j):
        return [i, j] not in self.world['#']
    
    def take_action(self, agent: List[int]):
        a, b = agent
        intend = self.policy[a][b]
        if intend == 'exit':
            return intend, intend
        direct = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
        # act = list(self.actions.keys())
        # aw = {a:self.noise for a in act}
        # aw[intend] = 1 - 3 * self.noise
        # weights = {k:aw[k] for k,v in self.actions.items() if self.not_collision(v[0]+agent[0], v[1]+agent[1])}
        action = random.choices(direct[intend], [1-self.noise*2, self.noise, self.noise])
        return action[0], intend
    
    def get_reward(self, agent):
        x, y = agent
        for state, score in self.exit_state:
            if state == [x, y]:
                return score
        return self.livingReward
    
    def act(self, agent, action):
        x, y = agent
        if action != 'exit':
            a, b = self.actions[action]
            x, y = agent[0]+a, agent[1]+b
            if not self.valid_position(x, y):
                x, y = agent
        return [x, y]
    
    def decimal_str(self, dec):
        if isinstance(dec, int):
            return str(dec)+".0"
        dec = str(dec)
        integer, decimal = dec.split('.')
        decimal = decimal.rstrip('0')
        decimal = '0' if len(decimal)<1 else decimal
        return integer+"."+decimal
            
    def process(self):
        result = ""
        # start state
        result += "Start state:\n"
        result += self.print_state()
        result += f"Cumulative reward sum: {self.cumulativeReward}\n"
        while True:
            result += "-------------------------------------------- \n"
            action, intend = self.take_action(self.agents)
            result += f"Taking action: {action} (intended: {intend})\n"
            reward = self.get_reward(self.agents)
            self.agents = self.act(self.agents, action)
            result += f"Reward received: {self.decimal_str(reward)}\n"
            result += "New state:\n"
            result += self.print_state(action == 'exit')
            self.cumulativeReward += reward
            result += f"Cumulative reward sum: {self.decimal_str(self.cumulativeReward)}\n"
            if action == 'exit':
                break
        return result
        

def p1(seed, noise, livingReward, grid, policy):
    if seed != -1:
        random.seed(seed, version=1)
    env = Env(noise, livingReward, grid, policy)
    result = env.process().rstrip('\n')
    return result

def play_episode(problem):
    experience = p1(**problem)
    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)