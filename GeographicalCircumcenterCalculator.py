import math
from math import *
import numpy as np

#Average Earth radius in kilometers; equatorial radius: 6378.1370, polar radius: 6356.7523
r = 6371.0088

#Point A
latA = 52.5162746
longA = 13.3777041

#Point B
latB = 41.8986108
longB = 12.4768729

#Point C
latC = 48.8462218
longC = 2.3464138

#Latitude and longitude must be converted to "Earth-centered, Earth-fixed" coordinate system
def convertToECEF(lat, long):
    x = r * (math.cos(math.radians(lat)) * math.cos(math.radians(long)))
    y = r * (math.cos(math.radians(lat)) * math.sin(math.radians(long)))
    z = r * (math.sin(math.radians(lat)))
    return x, y, z

pointA = convertToECEF(latA, longA)
pointB = convertToECEF(latB, longB)
pointC = convertToECEF(latC, longC)

(xA, yA, zA) = pointA
(xB, yB, zB) = pointB
(xC, yC, zC) = pointC

pointA = np.array([xA, yA, zA])
pointB = np.array([xB, yB, zB])
pointC = np.array([xC, yC, zC])

#Vectors from point A to B and A to C
ab = pointB - pointA
ac = pointC - pointA

#The cross product of ab and ac is a vector perpendicular to both ab and ac
abXac = np.cross(ab, ac)

#Triangle in R^3
circumsphereCenter = ((np.linalg.norm(ac)**2 * np.cross(abXac, ab) + np.linalg.norm(ab)**2 * np.cross(ac, abXac))) / (2 * np.linalg.norm(abXac)**2)
circumsphereRadius = np.linalg.norm(circumsphereCenter)

#Circumcenter of the triangle in R^3
circumcenter = pointA + circumsphereCenter #Ending point B

#Directional vector from center of the sphere to circumcenter
sphereCenter = np. array([0, 0, 0]) #Starting point A
vectorSC = circumcenter - sphereCenter #Vector v

#Distance from center of the sphere to triangle circumcenter in kilometers
distanceSC = np.linalg.norm(vectorSC)

#Amount we need to move our point (as %) to reach the surface of the sphere 
amountToMove = r / distanceSC

#Circumcenter projected, from the triangle plane on to the surface of the sphere, with vector from sphere origin through triangle circumcenter
circumcenterProjected = sphereCenter + amountToMove * vectorSC

#Convert back from ECEF to latitude and longitude
latCircumcenter = math.degrees(math.asin(circumcenterProjected[2]/r))
longCircumcenter = math.degrees(math.atan2(circumcenterProjected[1], circumcenterProjected[0]))

#Calculate the distance on a great circle form one point to another
#In our case we want find the distance from each point to the circumcenter
def haversine(lat1, long1, lat2, long2):
    #Latitude and longitude must be converted to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    #Haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    d = 2 * asin(sqrt(a))
    return d * r

print("Circumcenter coordinates:", latCircumcenter,",", longCircumcenter)
print("Point A to circumcenter:", haversine(latA, longA, latCircumcenter, longCircumcenter), "kilometers")
print("Point B to circumcenter:", haversine(latB, longB, latCircumcenter, longCircumcenter), "kilometers")
print("Point C to circumcenter:", haversine(latC, longC, latCircumcenter, longCircumcenter), "kilometers")