import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import requests
import json
import time
import math
import stepper
from servo import Servo

ssid = ''
password = ''

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
    
hlat = 48.4284
hlon = -123.3656
R = 6371 # radius of the earth
IN1 = 2
IN2 = 3
IN3 = 4
IN4 = 5
my_servo = Servo(pin_id=6)

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

def cartesian_conversion(lat, lon, alt, R): #convert the lattitude and longitude into cartesian quardinates to use in the trig calculation.
    lat, lon = deg2rad(lat), deg2rad(lon)
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    z = R *math.sin(lat)
    return x, y ,z



def get_angle(x, y, z, h_x, h_y, h_z, R): #function to get the vertical angle to the iss
    ON = math.sqrt(((x - x_h)**2) + ((y - y_h)**2) + ((z - z_h)**2))
    GA = 2 * math.asin(ON/(2 * R))
    c = math.sqrt(((alt + R)**2) + (R**2) - (2*(alt + R) * R * math.cos(GA)))
    OA = math.asin((alt + R) * (math.sin(GA)/c))
    OAD = rad2deg(OA)
    if OAD < 0:
        OAD = OAD % 360
    if OAD > 180:
        OAD = 360 - OAD
    return OAD

    
x_h, y_h, z_h = cartesian_conversion(hlat,hlon, 0, R)

iteration = 0
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
stepper_motor = stepper.HalfStepMotor.frompins(IN1, IN2, IN3, IN4)
stepper_motor.reset()
while True:
    lat, lon, alt = get_iss_data()

    x, y, z = cartesian_conversion(lat, lon, alt, R)

    Bdeg = get_bearing(lat, lon, hlon, hlat)
    print(f"Bdeg: {round(Bdeg, 2)}")

    OAD = get_angle(x, y, z, x_h, y_h, z_h, R)
    print(f"angle to the iss: {round(OAD, 2)}")
    
    stepper_motor.step_until_angle(Bdeg)
    my_servo.write(OAD)


    
    #iteration += 1
    #print (iteration)
    #if iteration == 4:
    #    break
    time.sleep(1)