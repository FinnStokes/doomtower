import heapq

class Node:
    def __init__(self, index):
        self.index = index
    
    def __cmp__(self, other):
        return other.index - self.index
    
    def __hash__(self):
        return hash(self.index)

class Edge:
    def __init__(self, src, dest, cost):
        self.src = src
        self.dest = dest
        self.cost = cost
    
    def __cmp__(self, other):
        if self.src < other.src:
            return -1
        elif self.src > other.src:
            return 1
        else:
            if self.dest < other.dest:
                return -1
            elif self.dest > other.dest:
                return 1
            else:
                return 0
    
    def __hash__(self):
        return hash(self.src) ^ hash(self.dest)

class Graph:    
    def __init__(self):
        self.edges = set()
        self.nodes = set()

    def addEdge(self, src, dest, cost):
        if Node(src) in self.nodes and Node(dest) in self.nodes:
            self.edges.add(Edge(src, dest, cost))

    def addNode(self, index):
         self.nodes.add(Node(index))

    def getEdge(self, src, dest):
        e = Edge(src, dest, 0)
        if e in self.edges:
            edge = set([e]) & self.edges
            return edge.pop()
    
    def getNode(self, index):
        n = Node(index)
        if n in self.nodes:
            node = set([n]) & self.nodes
            return node.pop()

    def getPath(self, src, dest):
        spt = [None] * (len(self.nodes) + 1) # Shortest Path Tree
        sf = [None] * (len(self.edges) + 1) # Search Frontier
        costs = [0] * (len(self.edges) + 1)
        pq = [] # Priority Queue
        heapq.heappush(pq, (0, src))
        while pq:
            nextCost, nextNode = heapq.heappop(pq)
            spt[nextNode] = sf[nextNode]
            
            if nextNode == dest:
                # return path
                path = [dest]
                while True:
                    path.insert(0, spt[path[0]])
                    if path[0] == src:
                        return path
            
            # relax the edges
            for e in self.edges:
                if e.src == nextNode:
                    newCost = costs[nextNode] + e.cost
                    if sf[e.dest] == None:
                        costs[e.dest] = newCost
                        heapq.heappush(pq, (newCost, e.dest))
                        sf[e.dest] = nextNode
                    elif newCost < costs[e.dest]:
                        costs[e.dest] = newCost
                        heapq.heappush(pq, (newCost, e.dest))
                        sf[e.dest] = nextNode

    def removeNode(self, index):
        self.nodes.remove(Node(index))

    def removeEdge(self, src, dest):
        self.edges.remove(Edge(src, dest, 0))
