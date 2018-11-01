import configparser
import datetime
import os
import random
import time

import paho.mqtt.client as paho
import pandas as pd

this_module_path = os.path.split(__file__)[0]
config_file = os.path.join(this_module_path, "perception.ini")

config = configparser.ConfigParser()
config.read(config_file)

data_file = os.path.join(this_module_path, config["perception"]["data_file"])

df = pd.read_csv(data_file)
df["reading_time"] = pd.to_datetime(df["reading_time"], yearfirst=True)
df.index = df["reading_time"]

client = paho.Client()
client.connect(config["perception"]["broker_host"])

while True:
    current_hour = datetime.datetime.now().hour
    hour_start = f"{current_hour:02}:00"
    hour_end = f"{current_hour:02}:59"
    data = df.between_time(hour_start, hour_end)

    payload = data.sample().to_json(orient="records")
    
    client.publish(f"enviot/notify", payload)

    time.sleep(config.getint("perception", "interval", fallback=30))

client.disconnect()
