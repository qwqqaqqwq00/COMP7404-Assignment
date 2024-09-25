from heapq import heappush, heappop
import sys, parse, grader

def ucs(start_state, goal_states, V, E):
    # heap based method
    q = []
    # minimize total edge weight of the path
    heappush(q, (0, start_state, [start_state]))
    vis = V
    ans = [[], []]
    try:
        while len(q)>0:
            c, u, l = heappop(q)
            if vis[u] == 1:
                continue
            vis[u] = 1
            if u == goal_states:
                ans[1] = l
                raise Exception("Finish")
            ans[0].append(u)
            if E.get(u):
                for v, cv in E[u]:
                    if vis[v] == 0:
                        heappush(q, (c+cv, v, l+[v]))
    except Exception as e:
        while len(q)>0:
            c, u, l = heappop(q)
            if vis[u] == 1:
                continue
            vis[u] = 1
            if u == goal_states:
                break
            ans[0].append(u)
        
    return ' '.join(ans[0])+'\n'+' '.join(ans[1])

def ucs_search(problem):
    #Your p3 code here
    # solution = 'S D B C\nS C G'
    solution = ucs(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)