import requests
import generate
import app
from vincenty import vincenty
from app.perm import Permuation
from app.classes import RouteData, matrixData
from app.timSort import timSort

#returns latLong of given postal code (OneMap API)
def getLongLat(postalCode):
    params = {
        'searchVal': postalCode,
        'returnGeom': 'Y',
        'getAddrDetails': 'N',
        'pageNum': "1"
    }
    api_result = requests.get('https://developers.onemap.sg/commonapi/search', params, timeout=0.3)
    api_response = api_result.json()
    latLong = []
    latLong.append(float(api_response["results"][0]["LATITUDE"]))
    latLong.append(float(api_response["results"][0]["LONGITUDE"]))

    return latLong

#returns route from Source to Destination, Takes in Long,Lat (openrouteservice)
def getRoute(Start, Destination): 
    params = {
        'api_key': '5b3ce3597851110001cf6248e696f02158f640bca49e3e46a2a54122',
        'start': str(Start[0])+','+str(Start[1]),
        'end': str(Destination[0])+','+str(Destination[1]),
    }
    api_result = requests.get('https://api.openrouteservice.org/v2/directions/driving-car', params)
    api_response = api_result.json()
    
    time = api_response["features"][0]["properties"]["segments"][0]["duration"]
    distance = api_response["features"][0]["properties"]["segments"][0]["distance"]
    route = api_response["features"][0]["geometry"]["coordinates"]
    
    #Flip returned coordinates as required format for plotting is LatLong, API returns LongLat
    for i in range(0, len(route)):
        route[i][0], route[i][1] = route[i][1], route[i][0]
           
    #Create and return GeoData Struct
    ans = RouteData(time, distance, route)
    return ans

def getMatrix(start, end):  # Matrix Service
    
    #Create deep copy of master list of trips
    tempTripList = app.tripList.copy()
    #Sort list based on proximity to new pickup point
    temp = list(map(lambda x:getDistance(x,start),tempTripList))
    timSort(temp,tempTripList)
    
    #Initialise list of trips and Routes used for comparison
    compList = []
    compRoutes = []
    
    #Set index 0,1 of list to be coordinates of new trip
    compList.append(start)
    compList.append(end)
    
    #Populate rest of the list with the top 10 closest trips, taking a deep copy of the coord whenever its relevant
    for i in range(20):
        compList.append(tempTripList[i].start.copy())
        compList.append(tempTripList[i].end.copy())
        compRoutes.append(tempTripList[i].route)

    #Flips coordinates to LongLat format for API. Currently in LatLong format
    for coord in compList:
        coord[0], coord[1] = coord[1], coord[0]
     
    #Calls API for distance matrix between given points. 22x22 matrix.
    body = {
        "locations": compList,
        "metrics": ["distance"]
    }
    headers = {
        'Authorization': '5b3ce3597851110001cf6248e696f02158f640bca49e3e46a2a54122',
    }
    api_result = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
    api_response = api_result.json()
    
    #Get API response
    arrayMatrix = api_response["distances"]
    
    #Set trips in the list. (Currently hardcoded as a total of 11 trips, inclusive of new trips. Can be changed in line 63 up to a max of 58 (29 Trips))
    size = (int)(len(compList)/2)
    
    #Create Permuation of "m" trips. where m = size - 1.
    perm = Permuation(size-1, arrayMatrix)
    
    #returns the sequence of index for the shortest possible path
    bestpath = perm.bruteForce()
    print(bestpath)
    
    #Get the index of the trip that will be will be picking up the new trip
    prevRoute = (int)(bestpath[0]/2)-1
    
    #Create and return the index of the cordinates of the optimal route sequence
    route = []
    route.append(compList[bestpath[0]])
    route.append(compList[bestpath[1]])
    route.append(compList[bestpath[2]])
    route.append(compList[bestpath[3]])

    ans = matrixData(route, prevRoute, compRoutes)
    
    return ans


def getDistance(trip,start):
    #Straight line distance from current position to new pick
    a = vincenty((trip.start[0],trip.start[1]), (start[0],start[1]))
    #Shortest straight line distance from current position to current destination to new pickup
    b = vincenty((trip.start[0],trip.start[1]), (trip.end[0],trip.end[1])) + vincenty((trip.end[0],trip.end[1]), (start[0],start[1]))
    return min(a,b)
