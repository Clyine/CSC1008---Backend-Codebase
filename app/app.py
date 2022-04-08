
import json
from flask import Flask, jsonify,request
from flask_cors import CORS
from app.graph import Graph, Edge

from app.helper import getLongLat, getRoute, getMatrix
from app.classes import Trip

#This is the backend code powered by flask for our CSC1008 project.
#The code is currently built and run on heroku at "https://csc1008-ride-testing-app.herokuapp.com/"
#Our frontend codebase currently performs HTTP request at "https://csc1008-ride-testing-app.herokuapp.com/"

#initialise flask server object
app = Flask(__name__)
CORS(app)

#Opens output.json, which contains details on our precomputed trips.
#The data is loaded and converted into a List of "Trip" objects.
#Each "Trip" Object contains the Start and End Coordinates as well as the polyline route data it's currently on
file = open("/app/app/output.json")
data = json.load(file)
file.close()

tripList = []
for i in range((int)(len(data["tripList"]))):
    tripList.append(Trip(data["tripList"][i]["from"],data["tripList"][i]["to"],data["tripList"][i]["route"]))
    
del data

#Opens DjisktraOutput.json, which contains details on our defined vertex, edgelist
#A graph of size 79 is initialised as we have defined only 79 vertices.
#Data from our egdelist is converted into Edge Objects and inserted into our graph, forming a adjacency matrix
G = Graph(79)
file = open("/app/app/DjisktraOutput.json")
data = json.load(file)
file.close()

for item in data["listing"]:
    i = item["from"]
    j = item["to"]
    G.graph[i][j] = Edge(item["dist"], item["route"])
    
#Djisktra algorithm is run to find the shorted path from source node "i" to all other node in graph.
#Results is stored in G.routeArray
for i in range(79):
    G.dijkstra(i)


#Simple user authentication methods.
#Currently one 1 account
#Username = Cat
#Password = 123
# ----------------------------  Login ----------------------------
@app.route('/api/login/login', methods = ['POST'])
def login():
    content = request.get_json(silent=True)
    if content["username"] == "Cat" and content["password"] == "123":
        return jsonify(
            httpStatus = "201",
            success = True,
            message = "Correct information entered!"
        ), 201

    else:
        return jsonify(
            httpStatus = "201",
            success = False,
            message = "Incorrect information entered!"
        ), 201

@app.route('/api/login/isloggedin', methods = ['GET'])
def loggedIn():
    return jsonify(
            httpStatus = "201",
            success = True,
            message = "Correct information entered!"
        ), 201

@app.route('/api/login/logout', methods = ['POST'])
def logout():
    content = request.get_json(silent=True)
    print(content["meow"])
    return jsonify(), 201

# ----------------------------  API control ----------------------------
#Get best shared route if possible given a start postal code and end postal code
@app.route('/api/postal', methods=['POST', 'GET'])
def findroute():
    content = request.get_json(silent=True)
    
    #Converts postal code to LatLong coordinates using OneMap API
    start = getLongLat(content['params']['pickup']) 
    end = getLongLat(content['params']['destination'])
    
    #get data for optimal route in index format
    results = getMatrix(start, end)
    routeSeq = results.arrayRoute
    compList = results.compRoute
    prevRoute = results.prevRoute
    
    #compute Route and distance if there is no sharing of vehicles
    oRouteResponse = getRoute(start, end)
    oDist = oRouteResponse.totalDistance
    
    #initialise route polyline list and distance
    route = []
    dist = 0;
    
    #for each element in the optimal sequence, get directions from point to point with API calls, append polyline data to route list.
    for i in range(0,len(routeSeq)-1):
        routeResponse = getRoute(routeSeq[i],routeSeq[i+1])
        route.append(routeResponse.rawRoute)
        #Sum total distance
        dist += routeResponse.totalDistance
        
    #if shared total distance is more than 2 times of the original, set the standalone route as results
    if oDist/dist > 2:
        route = oRouteResponse.rawRoute
        prevRoute = []
    
    startLatLong = [start[1],start[0]]
    endLatLong =[end[1], end[0]] 
    taxiDist = dist #taxiRouteResponse.totalDistance
    
    #returns geodata to web app via HTTP
    return jsonify(
        pickup=startLatLong,
        destination=endLatLong,
        taxiDist = taxiDist,
        newRoute=route,
        prevRoute=prevRoute,
        comproute=compList), 201


#Returns all precomputed trips for simulation purposes for plotting onto map
@app.route('/api/postal/test/all', methods=['GET'])
def getAll():
    mylist = []
    for item in tripList:
        mylist.append(item.route)
    return jsonify(mylist), 201

#Return route generated from our djisktra implementation
@app.route('/api/routing/test', methods=['POST', 'GET'])
def getShortestRoute():
    content = request.get_json(silent=True)
    start = int(content['params']['start'])-1
    end = int(content['params']['end'])-1
    ans = G.getPath(start, end)
    
    return jsonify(
        distance = ans.totalDistance,
        route = ans.rawRoute
    )
    
#Returns all information on our Graph for plotting into the map
@app.route('/api/routing/all', methods=['GET'])
def getAllVertex():
    return jsonify(data)
        

# ----------------------------  User  ----------------------------

if __name__ == '__main__':
    app.run()