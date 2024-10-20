import re

def get_lines(file_path):
    with open(file_path, 'r') as f:
        l = f.read()
    pats = re.findall(r'([a-zA-Z]+):(.*?)(?=\n[a-zA-Z]+:|\n$|\Z)', l, re.DOTALL)
    ret = {}
    for k, v in pats:
        ret[k]=v
    return ret

def cast_empty(m):
    ret = []
    for v in m:
        if v == '':
            continue
        ret.append(v)
    return ret if len(ret)>0 else None
        
def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    problem = get_lines(file_path)
    problem['seed'] = int(problem['seed'])
    problem['noise'] = float(problem['noise'])
    problem['livingReward'] = float(problem['livingReward'])
    problem['grid'] = list(map(
        lambda x: cast_empty(x.strip().split(' ')),
        problem['grid'].splitlines()[1:]
        ))
    problem['policy'] = list(map(lambda x: cast_empty(x.strip().split(' ')),problem['policy'].splitlines()[1:]))
    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = get_lines(file_path)
    problem['discount'] = float(problem['discount'])
    problem['noise'] = float(problem['noise'])
    problem['livingReward'] = float(problem['livingReward'])
    problem['iterations'] = int(problem['iterations'])
    problem['grid'] = list(map(lambda x: cast_empty(x.strip().split(' ')),problem['grid'].splitlines()[1:]))
    problem['policy'] = list(map(lambda x: cast_empty(x.strip().split(' ')),problem['policy'].splitlines()[1:]))
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = get_lines(file_path)
    problem['discount'] = float(problem['discount'])
    problem['noise'] = float(problem['noise'])
    problem['livingReward'] = float(problem['livingReward'])
    problem['iterations'] = int(problem['iterations'])
    problem['grid'] = list(map(lambda x: cast_empty(x.strip().split(' ')),problem['grid'].splitlines()[1:]))
    return problem