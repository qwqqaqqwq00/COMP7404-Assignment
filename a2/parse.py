import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as f:
        l = f.readlines()
    problem = {}
    problem["seed"] = int(l[0].strip().split(":")[-1].strip())
    problem['state'] = [
        list(x.strip()) for x in l[1:]
    ]
    # problem = ''
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')