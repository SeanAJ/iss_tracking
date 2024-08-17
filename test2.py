import requests
import json
import time
import numpy as np
#import geopandas as gpd
#import geodatasets
#import shapely.geometry
#import matplotlib.pyplot as plt

#worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

hlon = 48.4284
hlat = -123.3656

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

    iteration += 1
    print (iteration)
    if iteration == 1:
        break
    time.sleep(5)