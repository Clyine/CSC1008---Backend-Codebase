import json


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        self.routeArray = [[0 for column in range(vertices)] for row in range(vertices)]
    
    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def printPath(self, parent, j):
        
        if parent[j] == -1:
            #print(j, end=" ")
            path.clear()
            path.append(j)
            return
        self.printPath(parent, parent[j])
        #print(j, end=" ")
        path.append(j)

    def printSolution(self, src, dist, parent):
        src = src
        #print("Vertex \t\tDistance from Source\tPath")
        for i in range(1, len(dist)):
            #print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i]), end=" ")
            self.printPath(parent, i)
            #print(src, i, path)
            self.routeArray[src][i] = path.copy()
            path.clear()

    def dijkstra(self, src):
        row = len(self.graph)
        col = len(self.graph[0])
        dist = [float("Inf")] * row
        parent = [-1] * row
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
        while queue:
            u = self.minDistance(dist, queue)
            queue.remove(u)
            for i in range(col):
                if self.graph[u][i] and i in queue:
                    if dist[u] + self.graph[u][i] < dist[i]:
                        dist[i] = dist[u] + self.graph[u][i]
                        parent[i] = u
        self.printSolution(src, dist, parent)



file = open("output.json")
data = json.load(file)

path = []

G = Graph(79)

for item in data["listing"]:
    i = item["from"]
    j = item["to"]
    G.graph[i][j] = item["dist"]
    
# Print the solution

for i in range(79):
    G.dijkstra(i)
#print("\n")

print(G.routeArray)