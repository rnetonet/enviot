import time

import paho.mqtt.client as paho

_BROKER = "localhost"


def on_message(client, userdata, message):
    print("------------------------------")
    print(f"client: {client.}")
    print("topic: %s" % message.topic)
    print(message.payload.decode("utf8"))
    print("qos: %d" % message.qos)
    print("------------------------------")


client = paho.Client()
client.on_message = on_message

client.connect(_BROKER)
client.subscribe("enviot/#")
client.loop_forever()
