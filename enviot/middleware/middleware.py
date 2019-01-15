import configparser
import os
import threading

import paho.mqtt.client as paho

from plugins.sonoff import SonoffRequester
from plugins.sonoff import SonoffStorage
from plugins.cloud_sync import CloudSync

# Current Work Dir
cwd = os.path.split(__file__)[0]

# Load config file
config_file = os.path.join(cwd, "middleware.ini")
config = configparser.ConfigParser()
config.read(config_file)

sonff_storage = SonoffStorage(config)
sonff_storage.start()

sonoff_requester = SonoffRequester(config)
sonoff_requester.start()

cloud_sync = CloudSync(config)
cloud_sync.start()

sonff_storage.join()
sonoff_requester.join()
cloud_sync.join()