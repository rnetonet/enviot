import json
import time
import traceback
from pathlib import Path
from threading import Thread

import paho.mqtt.client as paho
from loguru import logger
from pymongo import MongoClient

module_name = Path(__file__).name.replace(".py", "")


class SonoffStorage(Thread):
    def __init__(self, config):
        Thread.__init__(self)

        self.config = config
        self.config_sensor_list = (
            self.config[module_name]["sensor_list"].strip().split(",")
        )

        self.mqtt = paho.Client()
        self.mqtt.connect(
            self.config["middleware"]["broker_host"],
            int(self.config["middleware"]["broker_port"]),
        )
        self.mqtt.subscribe("#")
        self.mqtt.on_message = self.handle

        self.current_doc = {}

        self.mongo = MongoClient(
            self.config[module_name]["mongodb_host"],
            int(self.config[module_name]["mongodb_port"]),
        )
        self.mongo_db = getattr(
            self.mongo, self.config[module_name]["mongodb_database"]
        )
        self.mongo_table = getattr(
            self.mongo_db, self.config[module_name]["mongodb_table"]
        )

        logger.info("SonoffStorage started")

    def handle(self, client, userdata, message):
        raw_payload = message.payload.decode("utf8")

        payload = json.loads(raw_payload)
        body = payload.get("BODY")
        sensor = list(body.keys())[0]
        value = body.get(sensor)

        self.current_doc[sensor] = value

        # If complete, add client_id and save
        if not set(self.config_sensor_list).difference(set(self.current_doc.keys())):
            self.current_doc["client_id"] = self.config[module_name]["client_id"]
            self.save()

    def save(self):
        try:
            self.mongo.server_info()
            doc = self.mongo_table.insert_one(self.current_doc)
            logger.debug(f"Saved new doc on MongoDB: {doc.inserted_id}")
            logger.debug(self.current_doc)
        except:
            logger.error("Can´t connect to MongoDB")
            traceback.print_exc()

        self.current_doc = {}

    def run(self):
        self.mqtt.loop_forever()


class SonoffRequester(Thread):
    def __init__(self, config):
        Thread.__init__(self)

        self.config = config
        self.config_sensor_list = (
            self.config[module_name]["sensor_list"].strip().split(",")
        )

        self.mqtt = paho.Client()
        self.mqtt.connect(
            self.config["middleware"]["broker_host"],
            int(self.config["middleware"]["broker_port"]),
        )

        logger.info("SonoffRequester started")

    def request(self):
        for sensor in self.config_sensor_list:
            self.mqtt.publish(
                self.config[module_name]["mqtt_topic"], f"GET VALUE {sensor}"
            )

    def run(self):
        while True:
            self.request()
            time.sleep(int(self.config[module_name]["interval_secs"]))
