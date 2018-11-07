import json

from logzero import logger
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

_CONNECTION_TIMEOUT_MS = 30000

client = MongoClient(serverSelectionTimeoutMS=_CONNECTION_TIMEOUT_MS)

try:
    client.server_info()
    connected = True
except ServerSelectionTimeoutError:
    connected = False

if connected:

    def handle(payload_decoded):
        doc_json = json.loads(payload_decoded)[0]
        doc = client.enviot.data.insert_one(doc_json)
        logger.info(f"Saved new doc on mongodb: {doc.inserted_id}")


else:

    def handle(payload_decoded):
        logger.error(f"Can´t connect to mongodb")
