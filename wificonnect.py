# wifiConnect.py
from network import WLAN
from network import STA_IF
from time import time
from time import sleep_ms
from gc import mem_free
from machine import Pin
import json

config_file = json.loads(open("config.json","r").read())

ssid = config_file["ssid"]
password  = config_file["password"]

WIFI_LED=Pin(32,Pin.OUT)
WIFI_LED.value(0)

def wifi_connect():
    print("\nAvailable memory: %s Byte" % str(mem_free()))
    print("\nSSID to be connected is: %s" % ssid)
    wlan = WLAN(STA_IF)
    wlan.active(True)
    start_time = time()

    if not wlan.isconnected():
        print("\nThe current device is not networked and is connecting ....")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            sleep_ms(500)
            if time() - start_time > 10:
                print("\nFail !!!")
                break

    if wlan.isconnected():
        wlan = WLAN(STA_IF)
        WIFI_LED.value(1)
        global IP, Subnet, Gateway, DNS
        IP_info = wlan.ifconfig()
        IP = IP_info[0]
        Subnet = IP_info[1]
        Gateway = IP_info[2]
        DNS = IP_info[3]
        print("Wifi is connected with the following information:")
        print(" IP address : " + IP)
        print("Subnet mask : " + Subnet)
        print("    Gateway : " + Gateway)
        print("        DNS : " + DNS)
        
def wlaninfo():
    wlaninfo = {
        "IP":IP,
        "Subnet":Subnet,
        "Gateway":Gateway,
        "DNS":DNS
    }
    return wlaninfo