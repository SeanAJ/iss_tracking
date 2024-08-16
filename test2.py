import requests
import json
import time
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
    print(data)
    long = float(data['longitude'])
    lat = float(data['latitude'])
    alt = float(data['altitude'])
    print(long)
    print(lat)
    print(alt)
    iteration += 1
    print (iteration)
    if iteration == 4:
        break
    time.sleep(5)