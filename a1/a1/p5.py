from heapq import heappop, heappush
import sys, parse, grader

def astar(start_state, goal_states, V, E):
    vis = {v: False for v in V.keys()}
    q = []
    ans = [[], []]
    # minimize total edge weight (g(x)) plus next vertex weight (h(x)) of the path (f(x)=g(x)+h(x))
    heappush(q, (V[start_state], start_state, [start_state]))
    while len(q)>0:
        uw, u, l = heappop(q)
        uw -= V[u]
        if vis[u]:
            continue
        vis[u] = True
        if u == goal_states:
            ans[1] = l
            break
        ans[0].append(u)
        if E.get(u):
            for v, cv in E[u]:
                if not vis[v]:
                    heappush(q, (V[v]+uw+cv, v, l+[v]))
    return ' '.join(ans[0])+"\n"+' '.join(ans[1])

def astar_search(problem):
    #Your p5 code here
    # solution = 'S D C B\nS C G'
    solution = astar(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)