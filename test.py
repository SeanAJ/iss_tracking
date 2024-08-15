import requests
import json
import time
import geopandas as gpd
import shapely.geometry

iteration = 0
while True:
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    print(data)
    long = float(data['iss_position']['longitude'])
    lat = float(data['iss_position']['latitude'])
    print(long)
    print(lat)
    iteration += 1
    print (iteration)
    if iteration == 4:
        break
    time.sleep(5)