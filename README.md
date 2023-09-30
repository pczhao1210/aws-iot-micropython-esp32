## aws-iot-micropython-esp32
Using micropython to drive board sensors and dispaly to show anbient information, as well as send data to AWS IoT Core.

Work in Progress: 
- [ ] Add Cloud to Device Message function
- [ ] Add Device Shadow function

### Dev Board Introduction
This project used the [ESP32 Azure IoT Kit](https://www.espressif.com.cn/en/products/devkits/esp32-azure-kit/overview) which designed for Azure IoT when first released. 

The board is build on ESP32 chip, with bluetooth and 2.4GHz Wifi, so it's quite easy to coonect to internet or other bluetooth devices.

The board als equipped with different kind of sensors and a 128*64 OLED display, listed below:
![board](/img/board.png)
the detailed sensors are:
![sensors](/img/sensors.png)

### Quick Start
1. Flash the board with micropython with following [instruction](https://micropython.org/download/ESP32_GENERIC/), the latest firmware is v1.20, [link](https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20230426-v1.20.0.bin)
2. Install the latest [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html) version 
2. Connect the board with a Micro-USB cable, if success, you will find a CP2102 or CP210x device. Please ensure the cable can be used with DATA TRANSFER!!
3. Clone this project
4. Register your device on AWS IoT Core follow this [instruction](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)
5. Open ```config.json```, Edit the file, replace the ```<XXX>``` with your information,as below:
```
{
    "iot_core_address" : "<aws iot endpoint>",
    "device_name" : "<device id>",
    "public_topic" : "<publish topic>",
    "subscribe_topic" : "<subscribe topic>",
    "certPath" : "./cert/<cert file>",
    "keyPath" : "./cert/<key file>",
    "refresh_rate" : 10,
    "ssid" : "<Wifi SSID>",
    "password" : "<WIFI Password>"
}
```
6. Using VSCode+PYMAKR or Thonny to flash the files to board storage
7. Reboot the board using Ctrl+D in command line or plug the usb cable off and on.
8. You will see the OLED display show the temperature, humidity and IP like following photo, and the command line will show the log like:
![esp32photo](/img/esp32.png)
```
>>> Wifi is connected with the following information:
 IP address : 192.168.10.223
Subnet mask : 255.255.255.0
    Gateway : 192.168.10.1
        DNS : 192.168.10.1

Time being calibrated...
OK!

2023-9-30
16:3:23

AWS IoT Core Connected!!!
Message Sent: {"humidity": 74.7, "temp": 30.8}
The Temperature is 30.8 Celsis, The Humidity is 74.7%
Message Sent: {"humidity": 70.8, "temp": 31.0}
The Temperature is 31.0 Celsis, The Humidity is 70.8%
Message Sent: {"humidity": 70.8, "temp": 30.7}
The Temperature is 30.7 Celsis, The Humidity is 70.8%
...
```
