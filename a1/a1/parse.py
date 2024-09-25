import os, sys
def read_graph_search_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = list(map(lambda l: l.strip(), lines))
    # problem as a dict
    problem = {}
    start, end = lines[0].split(":"), lines[1].split(":")
    problem[start[0].strip()] = start[1].strip()
    problem[end[0].strip()] = end[1].strip()
    problem['V'] = {}
    problem['E'] = {}
    for l in lines[2:]:
        l = l.split(' ')
        if len(l) == 2:
            # vertex weight
            problem['V'][l[0]] = int(l[1])
        else:
            # edge weight
            if not problem['E'].get(l[0]):
                problem['E'][l[0]] = []
            problem['E'][l[0]].append([l[1], float(l[2])])
    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    problem = {'Q': []}
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = list(map(lambda x: x.strip().split(' '), lines))
    problem['Q'] = lines
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')