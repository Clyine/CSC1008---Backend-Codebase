class RouteData: #define object to hold geo data
    def __init__(self, time, distance, rawRoute):
        self.timeRequired = time
        self.totalDistance = distance
        self.rawRoute = rawRoute

class matrixData: 
    def __init__(self, arrayRoute, prevRoute, compRoute):
        self.arrayRoute = arrayRoute
        self.prevRoute = prevRoute
        self.compRoute = compRoute
        
class Trip:
    def __init__(self,start,end,route):
        self.start = start
        self.end = end
        self.route = route
            
