import json
from app.classes import RouteData

path = []

class Edge:
    def __init__(self, weights, routes):
        self.weights = weights
        self.routes = routes


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        
        self.graph = [
            [Edge(0, 0) for column in range(vertices)] for row in range(vertices)
        ]
        self.routeArray = [
            [0 for column in range(vertices)] for row in range(vertices)
        ]

    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1
        # from the dist array,pick one which
        # has min value and is still in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    # Function to print and initlise array to store the shortest path from source to j using parent array
    def printPath(self, parent, j):
        if parent[j] == -1:
            # print(j, end=" ")
            path.clear()
            path.append(j)
            return
        self.printPath(parent, parent[j])
        # print(j, end=" ")
        path.append(j)

    # Print the constructed distance array
    def printSolution(self, src, dist, parent):
        src = src
        # print("Vertex \t\tDistance from Source\tPath")
        for i in range(0, len(dist)):
            # print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i]), end=" ")
            self.printPath(parent, i)
            # print(src, i, path)
            self.routeArray[src][i] = path.copy()
            path.clear()

    # Implements Dijkstra's single source shortest path algorithm for a graph represented using adjacency matrix representation
    def dijkstra(self, src):
        row = len(self.graph)
        col = len(self.graph[0])
        # The output array. dist[i] will hold the shortest distance from src to i
        # Initialize all distances as INFINITE
        dist = [float("Inf")] * row
        # Parent array to store shortest path tree
        parent = [-1] * row
        # Distance of source vertex from itself is always 0
        dist[src] = 0
        # Add all vertices in queue
        queue = []
        for i in range(row):
            queue.append(i)
            # Find shortest path for all vertices
        while queue:
            # Pick the minimum dist vertex from the set of vertices still in queue
            u = self.minDistance(dist, queue)
            # remove min element
            queue.remove(u)
            # Update dist value and parent index of the adjacent vertices of the picked vertex.
            # Consider only those vertices which are still in queue
            for i in range(col):
                # Update dist[i] only if it is in queue, there is an edge from u to i,
                # and total weight of path from src to i through u is smaller than current value of dist[i]
                if self.graph[u][i].weights and i in queue:
                    if dist[u] + self.graph[u][i].weights < dist[i]:
                        dist[i] = dist[u] + self.graph[u][i].weights
                        parent[i] = u
        self.printSolution(src, dist, parent)

    #Get path sequence from referenced start to end. Compute the poly line for the shortest route and returns the computed value
    def getPath(self, start, end):
        route = []
        distance = 0
        #get best route sequence
        sequence = self.routeArray[start][end]
        for i in range(len(sequence) - 1):
            #increment route distance for each point traversed
            distance += self.graph[sequence[i]][sequence[i + 1]].weights
            #extend route sequence for each point traversed
            route.extend(self.graph[sequence[i]][sequence[i + 1]].routes)
        #return computed data
        return RouteData(0, distance, route)
