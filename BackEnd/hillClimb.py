import requests
import random
import math
from requests.api import get


def climb(latitude, longitude):
    # Hill climbing algorithm finds the local maximum points
    # First generate 100 lat lon points within 30mile radius
    points = []
    for i in range(0, 100):
        ang = random.uniform(0, 1) * 2 * math.pi
        hyp = math.sqrt(random.uniform(0, 1)) * 0.5
        adj = math.cos(ang) * hyp
        opp = math.sin(ang) * hyp
        points.append([latitude + adj, longitude + opp, 0])

    for point in points:
        latitude = point[0]
        longitude = point[1]
        elevation = requests.get(
            f"http://gethighelevation.com:5000/v1/etopo1?locations={latitude},{longitude}")
        elevation = elevation.json()
        elevation = elevation["results"][0]["elevation"]
        point[2] = elevation
        print(f'\n{point}')

    # Hill climb algorithm for each point
    tenHighestPoints = []
    for point in points:
        # expand coordinate .0005 lat and lon in every direction
        pointOne = [point[0]+.0005, point[1]+.0005]
        pointTwo = [point[0]-.0005, point[1]-.0005]
        pointThree = [point[0]+.0005, point[1]-.0005]
        pointFour = [point[0]-.0005, point[1]+.0005]

        # Query API for elevation of each point
        pointOneElevation = requests.get(
            f"http://gethighelevation.com:5000/v1/etopo1?locations={pointOne[0]},{pointOne[1]}")
        pointOneElevation = pointOneElevation.json()
        pointOneElevation = pointOneElevation["results"][0]["elevation"]

        pointTwoElevation = requests.get(
            f"http://gethighelevation.com:5000/v1/etopo1?locations={pointTwo[0]},{pointTwo[1]}")
        pointTwoElevation = pointTwoElevation.json()
        pointTwoElevation = pointTwoElevation["results"][0]["elevation"]

        pointThreeElevation = requests.get(
            f"http://gethighelevation.com:5000/v1/etopo1?locations={pointThree[0]},{pointThree[1]}")
        pointThreeElevation = pointThreeElevation.json()
        pointThreeElevation = pointThreeElevation["results"][0]["elevation"]

        pointFourElevation = requests.get(
            f"http://gethighelevation.com:5000/v1/etopo1?locations={pointFour[0]},{pointFour[1]}")
        pointFourElevation = pointFourElevation.json()
        pointFourElevation = pointFourElevation["results"][0]["elevation"]

        # Replace point with highest of five total points
        highestPointLocal = []
        maxElevationLocal = max(pointOneElevation, pointTwoElevation,
                                pointThreeElevation, pointFourElevation, point[2])

        if maxElevationLocal == pointOneElevation:
            highestPointLocal = [pointOne[0], pointOne[1], pointOneElevation]
        elif maxElevationLocal == pointTwoElevation:
            highestPointLocal = [pointTwo[0], pointTwo[1], pointTwoElevation]
        elif maxElevationLocal == pointThreeElevation:
            highestPointLocal = [pointThree[0],
                                 pointThree[1], pointThreeElevation]
        elif maxElevationLocal == pointFourElevation:
            highestPointLocal = [pointFour[0],
                                 pointFour[1], pointFourElevation]
        elif maxElevationLocal == point[2]:
            highestPointLocal = point

        print(f'local high point = {highestPointLocal}')

        # Sort and filter tenHighestPoints
        if len(tenHighestPoints) < 10:
            tenHighestPoints.append(highestPointLocal)
        for element in tenHighestPoints:
            if highestPointLocal[2] > element[2]:
                tenHighestPoints.remove(element)
                tenHighestPoints.append(highestPointLocal)
                break

    for p in tenHighestPoints:
        print(p)

    def metersToFeet(meters):
        feet = meters * 3.2808
        feet = round(feet)
        return feet

    highestPointsResponse = {
        "points": {
            "one": {
                "lat": tenHighestPoints[0][0],
                "lng": tenHighestPoints[0][1],
                "elevation": metersToFeet(tenHighestPoints[0][2])
            },
            "two": {
                "lat": tenHighestPoints[1][0],
                "lng": tenHighestPoints[1][1],
                "elevation": metersToFeet(tenHighestPoints[1][2])
            },
            "three": {
                "lat": tenHighestPoints[2][0],
                "lng": tenHighestPoints[2][1],
                "elevation": metersToFeet(tenHighestPoints[2][2])
            },
            "four": {
                "lat": tenHighestPoints[3][0],
                "lng": tenHighestPoints[3][1],
                "elevation": metersToFeet(tenHighestPoints[3][2])
            },
            "five": {
                "lat": tenHighestPoints[4][0],
                "lng": tenHighestPoints[4][1],
                "elevation": metersToFeet(tenHighestPoints[4][2])
            },
            "six": {
                "lat": tenHighestPoints[5][0],
                "lng": tenHighestPoints[5][1],
                "elevation": metersToFeet(tenHighestPoints[5][2])
            },
            "seven": {
                "lat": tenHighestPoints[6][0],
                "lng": tenHighestPoints[6][1],
                "elevation": metersToFeet(tenHighestPoints[6][2])
            },
            "eight": {
                "lat": tenHighestPoints[7][0],
                "lng": tenHighestPoints[7][1],
                "elevation": metersToFeet(tenHighestPoints[7][2])
            },
            "nine": {
                "lat": tenHighestPoints[8][0],
                "lng": tenHighestPoints[8][1],
                "elevation": metersToFeet(tenHighestPoints[8][2])
            },
            "ten": {
                "lat": tenHighestPoints[9][0],
                "lng": tenHighestPoints[9][1],
                "elevation": metersToFeet(tenHighestPoints[9][2])
            },
        }
    }

    return highestPointsResponse