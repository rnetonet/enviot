import configparser
import os
import time

import paho.mqtt.client as paho

import plugins_support

this_module_path = os.path.split(__file__)[0]
config_file = os.path.join(this_module_path, "middleware.ini")

config = configparser.ConfigParser()
config.read(config_file)

plugins = plugins_support.get_plugins()


def on_message(client, userdata, message):
    payload_decoded = message.payload.decode("utf8")
    for plugin in plugins:
        plugin.handle(payload_decoded)


client = paho.Client()
client.on_message = on_message

client.connect(config["middleware"]["broker_host"])
client.subscribe("enviot/#")
client.loop_forever()
