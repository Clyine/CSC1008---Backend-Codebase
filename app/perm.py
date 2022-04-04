import sys

#NEW ROUTE TO BE AT INDEX 0,1 REST OF THE ROUTES IN INDEX 2 AND BEYOND. EVEN INDEX = START, ODD INDEX = DESTINATION


class Permuation():
    def __init__(self, size, matrix):
        #Initialise tripList
        self.list = []
        #Assign index 0,1 to be new Trip coordinates
        self.list.append([0,1])
        #Populate rest of the list based index
        for i in range(size):
            self.list.append([2*i+2,2*i+3])
        #Initialise distance matrix
        self.dist = matrix
        
        #Initialise and populate list of permuations and sequences
        self.perms = []
        self.sequence = []
        self.setSequence(self.list)
        
        self.Mat = None
        
    def printGraph(self):
        print(self.perms)
        
    def setSequence(self, set):
        #Append all possible permuations of User-Driver Trip
        for i in range(len(set)-1):
            self.perms.append([set[0],set[i+1]])
            
        #For each permutation set, generate all logical sequence of points
        for i in range(len(set)-1):
            set = self.perms[i]
            self.sequence.append([set[1][0],set[0][0],set[1][1],set[0][1]])
            self.sequence.append([set[1][0],set[0][0],set[0][1],set[1][1]])
            self.sequence.append([set[1][0],set[1][1],set[0][0],set[0][1]])

    def bruteForce(self):
        #Initialise shortest distaance variable
        shortest = sys.maxsize
        #initialise index of the shortest route
        index = 0
        #For each sequence in list of sequence, compute the total distance
        for i in range(len(self.sequence)):
            route = self.sequence[i]
            currDist = 0
            for j in range(3):
                currDist += self.dist[route[j]][route[j+1]]
            #if distance is less than shortest, set index as current index and shortest as current distance
            if (currDist < shortest):
                shortest = currDist
                index = i
        #returns sequence with the shortest total distance
        return self.sequence[index]
