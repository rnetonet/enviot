import configparser
import datetime
import os
import time

import paho.mqtt.client as paho
import pandas as pd
from logzero import logger

# Current module path
curr_mod_path = os.path.split(__file__)[0]

# Full path to configuration file
config_file = os.path.join(curr_mod_path, "perception.ini")

# Reading configuration
config = configparser.ConfigParser()
config.read(config_file)

# Data file, where events are collected
data_file = os.path.join(curr_mod_path, config["perception"]["data_file"])

# Load into DataFrame
df = pd.read_csv(data_file)

# Convert "reading_time" to proper datetime and make it the DataFrame index
df["reading_time"] = pd.to_datetime(df["reading_time"], yearfirst=True)
df.index = df["reading_time"]

# Paho setup
client = paho.Client()
client.connect(config["perception"]["broker_host"], int(config["perception"]["broker_port"]))

while True:
    # Define time limits
    current_hour = datetime.datetime.now().hour
    hour_start = f"{current_hour:02}:00"
    hour_end = f"{current_hour:02}:59"

    # Get a sample from data contained in time limits
    data = df.between_time(hour_start, hour_end)
    payload = data.sample()

    # Add client_id, convet to json and publish using paho
    payload["client_id"] = config["perception"]["client_id"]
    payload = payload.to_json(orient="records")
    client.publish(f"enviot/notify", payload)

    logger.info(f"Sent: {payload}")

    time.sleep(config.getint("perception", "interval", fallback=30))

client.disconnect()
