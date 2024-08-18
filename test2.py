import requests
import json
import time
import numpy as np
import math
#import geopandas as gpd
#import geodatasets
#import shapely.geometry
#import matplotlib.pyplot as plt

#worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

hlat = 48.4284
hlon = -123.3656

#convert home location
hlat, hlon = np.deg2rad(hlat), np.deg2rad(hlon)
R = 6371 # radius of the earth
x_h = R * np.cos(hlat) * np.cos(hlon)
y_h = R * np.cos(hlat) * np.sin(hlon)
z_h = R *np.sin(hlat)
x_h = round(x_h,2)
y_h = round(y_h,2)
z_h = round(z_h,2)
print(f"home x: {x_h}, home y: {y_h}, home z: {z_h}")

iteration = 0
while True:
    response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
    data = response.json()
    #print(data)
    lon = float(data['longitude'])
    lat = float(data['latitude'])
    alt = float(data['altitude'])
    #lon = float(input("longitude:"))
    #lat = float(input("latitude: "))
    #alt = 0
    print(f"longitude: {lon}")
    print(f"latitude: {lat}")
    print(f"altitude: {alt}")

    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371 + alt # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    x = round(x,2)
    y = round(y,2)
    z = round(z,2)
    print(f"x: {x}")
    print(f"y: {y}")
    print(f"z: {z}")

    X = np.cos(lat) * np.sin(lon-hlon)
    Y = np.cos(hlat) * np.sin(lat) - np.sin(hlat) * np.cos(lat) * np.cos(lon-hlon)
    B = math.atan2(X,Y)
    B = np.rad2deg(B)

    print(f"B: {B}")
    #Calculate the distance from the observer to the nadir of the iss
    ON = np.sqrt(((x - x_h)**2) + ((y- y_h)**2) + ((z - z_h)**2))
    print(f"nadir: {ON}")
    # Calculate the geocentric angle
    GA = 2 * math.asin(ON/(2 * R))
    print(f"Geocentric angle: {GA}")
    #calculate the distance from the observer up to the ISS
    c = np.sqrt(((alt + R)**2) + (R**2) - (2*(alt + R) * R * np.cos(GA)))
    print(f"Distance from observer to the iss: {c}")
    #calculate the angle from the observer to the iss
    OA = math.asin((alt + R) * (np.sin(GA)/c))
    OAD = np.rad2deg(OA)
    print(f"angle  from observer to iss: {OAD}")
    

    iteration += 1
    print (iteration)
    if iteration == 1:
        break
    time.sleep(5)