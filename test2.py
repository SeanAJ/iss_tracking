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

iteration = 0
while True:
    response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
    data = response.json()
    #print(data)
    lon = float(data['longitude'])
    lat = float(data['latitude'])
    alt = float(data['altitude'])
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
    print(f"x: {x}, y: {y}, z:{z}")
    iteration += 1
    print (iteration)
    if iteration == 1:
        break
    time.sleep(5)