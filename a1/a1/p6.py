import sys, parse, grader
from typing import List

def C(x):
    if x<2:return 0
    return (x-1)*x//2

def ntk(Q: List[List[str]]):
    n = len(Q)
    row = [0] * n
    col = [0] * n
    diag = [0] * (2*n-1)
    rdiag = [0] * (2*n-1)
    Qid = [-1] * n
    for i in range(n):
        for j in range(n):
            if Q[i][j] == 'q':
                row[i]+=1
                col[j]+=1
                diag[n-1-i+j]+=1
                rdiag[i+j]+=1
                Qid[j] = i
    # calculate the total cost of current state
    tot = 0
    for c in col+row+diag+rdiag:
        tot += C(c)
    ans = [[tot for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            k = Qid[j]
            if k != i:
                # move Q[i] to Q[i][j]
                ans[i][j] += row[i]+diag[n-1-i+j]+rdiag[i+j]
                ans[i][j] -= row[k]+diag[n-1-k+j]+rdiag[k+j]-3
    
    # the format seems like center align and the last one is right align
    ans = [f"{x[0]:^3}{x[1]:^3}{x[2]:^3}{x[3]:^3}{x[4]:^3}{x[5]:^3}{x[6]:^3}{x[7]:>2}\n" for x in ans]
    ans = ''.join(ans)[:-1]
    return ans

def number_of_attacks(problem):
    #Your p6 code here
#     solution = """18 12 14 13 13 12 14 14
# 14 16 13 15 12 14 12 16
# 14 12 18 13 15 12 14 14
# 15 14 14 17 13 16 13 16
# 17 14 17 15 17 14 16 16
# 17 17 16 18 15 17 15 17
# 18 14 17 15 15 14 17 16
# 14 14 13 17 12 14 12 18"""
    solution = ntk(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)