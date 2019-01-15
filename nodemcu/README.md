# NodeMCU and DHT11

# Setup NodeMCU

* Install `esptool`:

```shell
sudo pip install -U esptool
```

* Plug NodeMCU into USB

* Erase:

```shell
esptool.py --port /dev/ttyUSB0 erase_flash
```

* Download the firmware:

```shell
wget -c "http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin"
```

* Write:

```shell
$ sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.binesptool.py v2.5.1

Serial port /dev/ttyUSB0
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: 2c:3a:e8:37:d8:a3
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0040
Compressed 604872 bytes to 394893...
Wrote 604872 bytes (394893 compressed) at 0x00000000 in 9.0 seconds (effective 538.9 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

* Install `picocom` to access shell:

```
sudo apt-get install picocom
```

* Acess REPL:

```shell
sudo picocom /dev/ttyUSB0 -b115200
```

* In REPL, setup the access point name and passwor (`nodemcu`, `_n0d3mcu`):

```shell
>>> import network
>>> ap_if = network.WLAN(network.AP_IF)
>>> ap_if.config(essid="nodemcu", authmode=network.AUTH_WPA_WPA2_PSK, password="_n0d3mcu")
```

* Setup an Wi-fi connection:

```shell
>>> import network
>>> sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
>>> sta_if.connect("UFBA-Visitante")
>>> sta_if.isconnected()
True
```

* Configure `WebREPL` 

```shell
>>> import webrepl_setup
WebREPL daemon auto-start status: disabled

Would you like to (E)nable or (D)isable it running on boot?
(Empty line to quit)
> E
Would you like to change WebREPL password? (y/n) y
New password (4-9 chars): _n0d3mcu
Confirm password: _n0d3mcu
Changes will be activated after reboot
Would you like to reboot now? (y/n) 
```

* Restart `WebREPL` to get the ip in Wi-fi network:

```shell
>>> import webrepl
>>> webrepl.stop()
>>> webrepl.start()
WebREPL daemon started on ws://192.168.4.1:8266
WebREPL daemon started on ws://172.20.19.237:8266
Started webrepl in normal mode
>>> 
```

* Download `WebREPL` interface. MicroPython provides only a websocket interface:

```shell
wget -c "https://github.com/micropython/webrepl/archive/master.zip"
mv master.zip webrepl.zip
unzip webrepl.zip
rm webrepl.zip
mv webrepl-master/ webrepl
xdg-open webrepl/webrepl.html
```

> If you can´t connect through Wi-fi, connect to `nodemcu` AP.

## Setup DHT11


## Reading DHT11 data

```python
>>> import dht
>>> import machine
>>> d = dht.DHT11(machine.Pin(14))
>>> d.measure()
>>> d.temperature()
>>> d.humidity()
``` 

### A simple script to periodic collect

```python
import dht
import machine

def collect(*args, **kwargs):
    d = dht.DHT11(machine.Pin(14))
    d.measure()
    print()
    print("***")
    print("Temperature (celsius): {}".format(d.temperature()))
    print("Humidity: {}".format(d.humidity()))
    print("***")
    print()

from machine import Timer
tim = Timer(-1)
tim.init(period=5000, mode=Timer.PERIODIC, callback=collect)
```
