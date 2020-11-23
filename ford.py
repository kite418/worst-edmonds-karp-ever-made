import math

class Vertice():
    def __init__(self, name):
        self.edges = []
        self.pred = None
        self.name = name
        
    def get_edge(self, dest):
        for edge in self.edges:
            if (edge[0] == dest):
                return edge

def path_to_edges(path):
    edge_path = []
    min_cap = math.inf
    for i in range(len(path) - 1, 0, -1):
        v = path[i]
        e = v.get_edge(path[i - 1].name)

        edge_path.append((v, e))

        min_cap = min(min_cap, e[1]) 

    return (edge_path, min_cap)

def to_adj_list(d_iterator, N, M):
    V = []
    for i in range(M):
        V.append(Vertice(i + 1))

    line = next(d_iterator, None)
    while (line != None):
        line = line.split(" ")
        source = line[0]
        dest = line[1]
        cap = line[2]   

        # (dest, capacity, flow)
        V[int(source) - 1].edges.append([int(dest), int(cap), 0]) 

        line = next(d_iterator, None)
    
    return V
    
def build_residual(adj_lst):
    gf = []
    for i in range(len(adj_lst)):
        gf.append(Vertice(i + 1))
    
    for i in range(len(adj_lst)):
        v = adj_lst[i]

        for edge in v.edges:
            forward_c = edge[1] - edge[2]
            backward_c = edge[2]

            if (forward_c > 0):
                forward = [edge[0], forward_c]
                v_r = gf[i]
                v_r.edges.append(forward)
            
            if (backward_c > 0):
                backward = [i + 1, backward_c]
                v_r2 = gf[edge[0] - 1]
                v_r2.edges.append(backward)

    return gf

def bfs(adj_lst):
    frontier =[adj_lst[0]]
    explored =[]

    for v in adj_lst:
        v.pred = None

    while (len(frontier) > 0):
        v = frontier.pop()
        for edge in v.edges:
            dest_v = adj_lst[edge[0] - 1]
            if (dest_v not in frontier and dest_v not in explored):
                frontier.append(dest_v)
                dest_v.pred = v

                if (dest_v == adj_lst[-1]):
                    current = dest_v
                    path = []
                    while (current != adj_lst[0]):
  
                        path.append(current)
                        current = current.pred

                    path.append(current)

                    return path

        explored.append(v)

    return None

def ford(data):
    iterator = iter(data.splitlines())
    l1 = next(iterator).split(" ")
    N = int(l1[0])
    M = int(l1[1])

    adj_lst = to_adj_list(iterator, N, M)

    gf = build_residual(adj_lst)
    path = bfs(gf)


    while (path != None):
        edge_path, cap = path_to_edges(path)

        for thing in edge_path:
            v = thing[0]
            i = v.name - 1

            v1 = adj_lst[i]
            e = v1.get_edge(thing[1][0])

            e[2] += cap
    
        gf = build_residual(adj_lst)
        path = bfs(gf)



    flow = 0
    for e in adj_lst[0].edges:
        flow += e[2]

    return flow



# THIS IS THE FUNCTION
# OUTPUT IS LIST OF MAX FLOWS CORRESPONDING TO INPUT CASES
# OUTPUT[0] = MAX FLOW FOR CASE 1, OUTPUT[1] = MAX FLOW FOR CASE 2 ETC
def ford_multiple_cases(case_lst):
    output = []
    i = 0
    for case in case_lst:
        output.append(ford(case))
    
    return output
    

test_cases = ["""9 6
1 2 16
1 3 13
2 4 12
3 2 4
3 5 14
4 3 9
4 6 20
5 4 7
5 6 4
""",
"""5 4
1 2 40
1 4 20 
2 4 20
2 3 30 
3 4 10
""",
"""8 6
1 2 11
1 3 12
2 4 12
3 2 1
3 5 11
4 6 19
5 4 7
5 6 4
""",
"""13 8
1 2 13
1 3 10
1 4 10
2 5 24
3 2 5
3 4 15
4 7 15
3 7 7
5 6 1
5 8 9
6 8 13
6 7 6
7 8 16
"""]


print(ford_multiple_cases(test_cases))