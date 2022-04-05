
import json
from random import Random, random, randrange
from time import sleep
from flask import Flask, jsonify,request
from flask_cors import CORS

from app.helper import getLongLat, getRoute, getMatrix
from app.classes import Trip
import app.generate
import threading
import gunicorn

app = Flask(__name__)
CORS(app)

file = open("/app/app/output.json")
data = json.load(file)
file.close()

tripList = []
for i in range((int)(len(data))):
    tripList.append(Trip(data["start"],data["end"],data["route"]))
    
del data

# ----------------------------  Loops  ---------------------------

# def move(tripList):
#     while (True):
#         sleep(10)       
#         for trip in tripList:
#             trip.move()
#         print("Moved Vehicles ID:", randrange(0,100))
 
        
# t = threading.Thread(target=move, args=(tripList,))
# t.daemon = True
# t.start()

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
@app.route('/api/postal', methods=['POST', 'GET'])
def findroute():
    content = request.get_json(silent=True)
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
    
    #returns geodata to web app via HTTP
    return jsonify(
        newRoute=route,
        prevRoute=prevRoute,
        comproute=compList), 201


@app.route('/api/postal/test/all', methods=['GET'])
def getAll():
    return jsonify(data), 201
        

# ----------------------------  User  ----------------------------

if __name__ == '__main__':
    app.run()