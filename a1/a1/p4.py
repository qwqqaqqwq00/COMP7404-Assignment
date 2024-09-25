from heapq import heappop, heappush
import sys, parse, grader

def greedy(start_state, goal_states, V, E):
    vis = {v: False for v in V.keys()}
    q = []
    ans = [[], []]
    # minimize next vertex weight during pathfinding
    heappush(q, (V[start_state], start_state, [start_state]))
    while len(q)>0:
        uw, u, l = heappop(q)
        vis[u] = True
        if u == goal_states:
            ans[1] = l
            break
        ans[0].append(u)
        if E.get(u):
            for v, _ in E[u]:
                if not vis[v]:
                    heappush(q, (V[v], v, l+[v]))
    return ' '.join(ans[0])+"\n"+' '.join(ans[1])
def greedy_search(problem):
    #Your p4 code here
    # solution = 'S B D C\nS C G'
    solution = greedy(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)