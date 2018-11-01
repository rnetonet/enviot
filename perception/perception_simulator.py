import datetime
import random
import time

import paho.mqtt.client as paho
import pandas as pd

_DELAY = 30
_DATAFILE = "data.csv"
_BROKER = "localhost"

df = pd.read_csv(_DATAFILE)
df["reading_time"] =  pd.to_datetime(df["reading_time"], yearfirst=True)
df.index = df["reading_time"]

client = paho.Client()
client.connect(_BROKER)

while True:
    current_hour = datetime.datetime.now().hour
    hour_start = f"{current_hour:02}:00"
    hour_end = f"{current_hour:02}:59"
    data = df.between_time(hour_start, hour_end)
    
    payload = data.sample().to_json()

    client.publish(f"enviot/notify", payload)
    time.sleep(_DELAY)

client.disconnect()
