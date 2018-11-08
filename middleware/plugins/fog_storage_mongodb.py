import json
import traceback
from pathlib import Path

from logzero import logger
from pymongo import MongoClient

file_name = Path(__file__).name.replace(".py", "")


def handle(payload_decoded, config):
    if file_name not in config:
        logger.error(f"{file_name} not in config")
        return

    try:
        if not hasattr("handle", "client"):
            handle.client = MongoClient(
                config[file_name]["host"], int(config[file_name]["port"])
            )

        # Check connection
        handle.client.server_info()

        db = getattr(handle.client, config[file_name]["database"])
        table = getattr(db, config[file_name]["table"])

        doc_json = json.loads(payload_decoded)[0]
        doc = table.insert_one(doc_json)
        logger.info(f"Saved new doc on mongodb: {doc.inserted_id}")
    except:
        logger.error("An unexpected error happened: ")
        traceback.print_exc()
        handle.client = None


logger.debug("Loaded")
