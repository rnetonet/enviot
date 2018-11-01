import configparser
import os
import time

import paho.mqtt.client as paho

this_module_path = os.path.split(__file__)[0]
config_file = os.path.join(this_module_path, "middleware.ini")

config = configparser.ConfigParser()
config.read(config_file)


def on_message(client, userdata, message):
    print("------------------------------")
    print("topic: %s" % message.topic)
    print(message.payload.decode("utf8"))
    print("qos: %d" % message.qos)
    print("------------------------------")


client = paho.Client()
client.on_message = on_message

client.connect(config["middleware"]["broker_host"])
client.subscribe("enviot/#")
client.loop_forever()
