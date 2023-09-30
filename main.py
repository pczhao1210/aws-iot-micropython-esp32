import json
import time

from machine import Pin, SoftI2C
from umqtt.robust import MQTTClient

from wificonnect import wifi_connect
from wificonnect import wlaninfo

from settime import set_time
from settime import date_now
from settime import time_now

import HTS221
import SSD1306

#Set WIFI & IoT Connected LED to OFF status
AWS_IoT_LED=Pin(33,Pin.OUT)
AWS_IoT_LED.value(0)
WIFI_LED=Pin(32,Pin.OUT)
WIFI_LED.value(0)

#Read local config file for configurations
config = json.loads(open("config.json","r").read())

#Set LED refresh rate & I2C Connection & IoT Reporting rate
refresh_rate = config["refresh_rate"]
print("Refresh Rate is: %s" % refresh_rate)
i2c = SoftI2C(scl=Pin(26), sda=Pin(25), freq=100000)

#AWS IoT Related Settings
aws_iot_endpoint = config["iot_core_address"]
print("AWS IoT Endpoint is: %s" % aws_iot_endpoint)
client_id = config["device_name"]
print("AWS IoT Deivce ID is: %s" % client_id)
publish_topic = config["public_topic"]
print("AWS IoT Publish Topic is: %s" % publish_topic)
subcribe_topic = config["subscribe_topic"]
print("AWS IoT Publish Topic is: %s" % subcribe_topic)
certPath = config["certPath"]
with open(certPath, 'r') as f:
    cert = f.read()
keyPath = config["keyPath"]
with open(keyPath, 'r') as f:
    key = f.read()
SSL_PARAMS = {'key': key,'cert': cert, 'server_side': False}

def sub_cb(topic, msg):
    global MQTT_CLIENT
    MQTT_CLIENT.set_callback(sub_cb)
    print('Device received a Message: ')
    print((topic, msg))  #print incoming message, waits for loop below

if __name__ == '__main__':
    #WIFI Connection
    wifi_connect()
    set_time()
    date_now();time_now()
    ip = wlaninfo()["IP"]

    #OLED Config
    oled_width = 128
    oled_height = 64
    oled = SSD1306.SSD1306_I2C(oled_width, oled_height, i2c)

    #HTS221
    hts = HTS221.HTS221(i2c)

    #IoT Connection
    MQTT_Client = MQTTClient(client_id=client_id, server=aws_iot_endpoint, port=8883, keepalive=1200, ssl=True, ssl_params = SSL_PARAMS)
    MQTT_Client.DEBUG = True
    MQTT_Client.connect()
    AWS_IoT_LED.value(1)
    print("AWS IoT Core Connected!!!")
    MQTT_Client.set_callback(sub_cb)

    while True:
        temperature = hts.temperature()
        humidity = hts.humidity()
        #ht = hts.get()

        #Build IoT Message
        msg_raw = {
        "temp":20,
        "humidity":50
        }
        msg = json.dumps(msg_raw)
                
        #Build LED texts
        temp_txt = "{temperature} Celsis".format(temperature=temperature)
        humidity_txt = "{humidity} %".format(humidity=humidity)
        
        oled.fill(0)
        oled.text('Realtime T & H', 0, 0)
        oled.text("Temperature:", 0, 16)
        oled.text(temp_txt, 0, 26)
        oled.text("Humidity:", 0, 36)
        oled.text(humidity_txt, 0, 46)
        oled.text(ip,0,56)
        oled.show()

        MQTT_Client.publish(publish_topic, msg)
        print("Message Sent: " + msg)
        
        log_output = "The Temperature is {temperature} Celsis, The Humidity is {humidity}%"
        print((log_output).format(temperature=temperature, humidity=humidity))
        
        time.sleep(refresh_rate)

