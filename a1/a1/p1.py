import sys, grader, parse

def start_dfs(start_state, goal_states, V, E):
    vis = V
    ans = [[], []]
    # stack based method
    s = []
    s.append((start_state, [start_state], 0))
    try:
        while len(s)>0:
            u, l, c = s.pop()
            if vis[u] == 1:
                continue
            vis[u] = 1
            if u == goal_states:
                ans[1] = l
                raise Exception("Finish")
            # record search set
            ans[0].append(u)
            if E.get(u):
                for v, cv in E[u]:
                    if vis[v] == 0:
                        s.append((v, l+[v], c+cv))
    except Exception as e:
        pass
    return ' '.join(ans[0])+'\n'+' '.join(ans[1])

# def _start_dfs(start_state, goal_states, V, E):
#     vis = V
#     ans = [[], '']
#     l = []
#     tc = 0
#     # recursive-based method
#     def dfs(u, c):
#         nonlocal tc
#         vis[u] = 1
#         l.append(u)
#         if u == goal_states:
#             # once reach the goal, return
#             ans[1] = ' '.join(l)
#             return True
#         ans[0].append(u)
#             # tc = c
#         if E.get(u):
#             #TODO: it seems like greater edge weight first, and it did pass all the test case
#             for v, cv in sorted(E[u], key=lambda x:x[1], reverse=True):
#                 if vis[v] == 0:
#                     if dfs(v, c+cv): # once reach the goal, stop iteration
#                         return True
#         l.pop()
#         vis[u] = False
#         return False
#     dfs(start_state, 0) # start
#     return ' '.join(ans[0])+'\n'+ans[1]
        

def dfs_search(problem):
    #Your p1 code here
    # solution = 'Ar D C\nAr C G'
    solution = start_dfs(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)