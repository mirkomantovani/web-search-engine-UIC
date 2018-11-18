# Mirko Mantovani

"""
A weighted undirected graph
"""


class UndirectedGraph:
    def __init__(self):
        self.graph = {}

    def __repr__(self):
        return 'Graph:'+ str(self.graph)

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, i, j, weight):
        if i not in self.graph:
            self.add_node(i)
        if j not in self.graph:
            self.add_node(j)
        self.graph[i][j] = weight
        self.graph[j][i] = weight

    def get_edge(self, i, j):
        if i in self.graph:
            if j in self.graph[i]:
                return self.graph[i][j]
        return -1


"""
An unweighted directed graph
"""


class DirectedGraph:
    def __init__(self):
        self.graph = {}

    def __repr__(self):
        return 'Graph:' + str(self.graph)

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, i, j):
        if i not in self.graph:
            self.add_node(i)
        self.graph[i][j] = 1

    def get_edge(self, i, j):
        if i in self.graph:
            if j in self.graph[i]:
                return self.graph[i][j]
        return -1


"""
A directed graph optimized to run fast pagerank algorithm
"""


class OptimizedDirectedGraph:
    def __init__(self):
        self.graph = {}
        # inverted is like an inverted index for graph nodes, it provides fast access to all the nodes pointing to
        # the specified pointed whose key is specified
        self.inverted = {}

    def __repr__(self):
        return 'Graph:' + str(self.graph)

    def get_len(self):
        return len(self.graph)

    # get all the nodes pointing to pointed
    def get_pointing_to(self, pointed):
        if pointed in self.inverted:
            return self.inverted[pointed]
        else:
            return set()

    def get_out_degree(self, node):
        return len(self.graph[node])

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, i, j):
        if i not in self.graph:
            self.add_node(i)
        self.graph[i][j] = 1
        self.add_inverted(j, i)

    def get_edge(self, i, j):
        if i in self.graph:
            if j in self.graph[i]:
                return self.graph[i][j]
        return -1

    def add_inverted(self, pointed, pointing):
        if pointed != pointing:
            if pointed not in self.inverted:
                self.inverted[pointed] = set()
            self.inverted[pointed].add(pointing)
