import sys, grader, parse, collections

def bfs(start_state, goal_states, V, E):
    # using queue to implement the bfs
    q = collections.deque()
    q.append((start_state, [start_state], 0))
    vis = V
    ans = [[], []]
    try:
        while len(q)>0:
            u, l, c = q.popleft()
            if vis[u] == 1:
                continue
            vis[u] = 1
            # record search set
            ans[0].append(u)
            if E.get(u):
                for v, cv in E[u]:
                    if vis[v] == 0:
                        if v == goal_states:
                            # once reach the goal, stop iteration
                            ans[1] = l+[v]
                            raise Exception("Finish")
                        q.append((v, l+[v], c+cv))
    except Exception as e:
        # record the search set
        while len(q)>0:
            u, l, c = q.popleft()
            # if watched, skip
            if vis[u] == 1:
                continue
            vis[u] = 1
            # if reached, break
            if u == goal_states:
                break
            ans[0].append(u)
        
    return ' '.join(ans[0])+'\n'+' '.join(ans[1])

def bfs_search(problem):
    #Your p2 code here
    # solution = 'Ar B C D\nAr C G'
    solution = bfs(**problem)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)