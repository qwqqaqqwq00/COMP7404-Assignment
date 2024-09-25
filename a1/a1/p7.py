import sys, parse, grader
from typing import List

def C(x):
    if x<2:return 0
    return (x-1)*x//2

def nQueen(Q: List[List[str]]):
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
    min_cost = 0
    min_move = None
    # modify from p6, update the first min cost as "<", the last min cost as "<="
    for j in range(n):
        k = Qid[j]
        for i in range(n):
            if k==i:
                continue
            cost = row[i]+diag[n-1-i+j]+rdiag[i+j]-(row[k]+diag[n-1-k+j]+rdiag[k+j]-3)
            if cost < min_cost:
                min_cost = cost
                min_move = (i, j)
    # it is possible that current state is the best
    if min_move is not None:
        i, j = min_move
        Q[i][j] = 'q'
        k = Qid[j]
        Q[k][j] = '.'
    
    ans = ''.join(list(map(lambda x:' '.join(x)+'\n', Q))).strip()
    return ans

def better_board(problem):
    #Your p7 code here
#     solution = """. q . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . q . . . .
# q . . . q . . .
# . . . . . q . q
# . . q . . . q .
# . . . . . . . ."""
    solution = nQueen(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)