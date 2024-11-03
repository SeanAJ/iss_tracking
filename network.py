import network
import time
import machine

ssid = ""
password = ""

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        time.sleep(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


try:
    connect()
except KeyboardInterrupt:
    machine.reset()