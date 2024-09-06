import requests
import json
import time
import math

hlat = 48.4284
hlon = -123.3656
R = 6371 # radius of the earth

def deg2rad(deg):
    return deg * (math.pi/180)

def rad2deg(rad):
    return rad * (180/math.pi)

def get_iss_data(): #function to call the ISS api and assign return variables
    while True:
        try:
            response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
            data = response.json()
            lon = float(data['longitude'])
            lat = float(data['latitude'])
            alt = float(data['altitude'])
            break
        except Exception:
            print("error")
            time.sleep(5)
    return lat,lon,alt

def get_bearing(lat, lon, hlon, hlat): #function to calculate the bearing from the observer to the iss
    lat, lon, hlon, hlat = deg2rad(lat), deg2rad(lon), deg2rad(hlon), deg2rad(hlat)
    X = math.cos(lat) * math.sin(lon-hlon)
    Y = math.cos(hlat) * math.sin(lat) - math.sin(hlat) * math.cos(lat) * math.cos(lon-hlon)
    B = math.atan2(X,Y)
    B = rad2deg(B)
    Bdeg = B
    if B < 0:
        Bdeg = B % 360
    return Bdeg

def cartesian_conversion(lat, lon, alt): #convert the lattitude and longitude into cartesian quardinates to use in the trig calculation.
    lat, lon = deg2rad(lat), deg2rad(lon)
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    z = R *math.sin(lat)
    return x, y ,z



def get_angle(x, y, z, h_x, h_y, h_z): #function to get the vertical angle to the iss
    ON = math.sqrt(((x - x_h)**2) + ((y - y_h)**2) + ((z - z_h)**2))
    GA = 2 * math.asin(ON/(2 * R))
    c = math.sqrt(((alt + R)**2) + (R**2) - (2*(alt + R) * R * math.cos(GA)))
    OA = math.asin((alt + R) * (math.sin(GA)/c))
    OAD = rad2deg(OA)
    if OAD < 0:
        OAD = OAD % 360
    return OAD

    
x_h, y_h, z_h = cartesian_conversion(hlat,hlon, 0)

iteration = 0
while True:
    lat, lon, alt = get_iss_data()

    x, y, z = cartesian_conversion(lat, lon, alt)

    Bdeg = get_bearing(lat, lon, hlon, hlat)
    print(f"Bdeg: {round(Bdeg, 2)}")

    OAD = get_angle(x, y, z, x_h, y_h, z_h)
    print(f"angle to the iss: {round(OAD, 2)}")
    
    iteration += 1
    print (iteration)
    if iteration == 4:
        break
    time.sleep(5)