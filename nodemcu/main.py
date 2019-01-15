# main.py
import dht
import machine
import network
import ujson
from machine import Timer
from umqtt.simple import MQTTClient

_SSID_WIFI = "UFBA-Visitante"
_PASS_WIFI = ""

_MIDDLEWARE_IP = "45.79.210.176"
_MIDDLEWARE_PORT = "80"

_CLIENT_ID = "lab148"

# Connect to wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(_SSID_WIFI, _PASS_WIFI)

# Function called from time to time
def collect(*args, **kwargs):
    d = dht.DHT11(machine.Pin(14))
    d.measure()

    data = {
        "client_id": _CLIENT_ID,
        "temperature": d.temperature(),
        "humidity": d.humidity(),
    }
    payload = ujson.dumps(data)

    c = MQTTClient(_CLIENT_ID, _MIDDLEWARE_IP, int(_MIDDLEWARE_PORT))
    c.connect()
    c.publish(b"enviot/notify", bytes(payload, "ascii"))
    c.disconnect()


tim = Timer(-1)
tim.init(period=30000, mode=Timer.PERIODIC, callback=collect)
