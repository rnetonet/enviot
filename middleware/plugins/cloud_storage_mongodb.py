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

    if not hasattr(handle, "counter"):
        handle.counter = 0

    handle.counter += 1

    if handle.counter == int(config[file_name]["batch_size"]):
        try:
            from_client = MongoClient(
                config[file_name]["from_host"], int(config[file_name]["from_port"])
            )
            to_client = MongoClient(
                config[file_name]["to_host"], int(config[file_name]["to_port"])
            )

            # Test connection to servers
            from_client.server_info()
            to_client.server_info()

            from_db = getattr(from_client, config[file_name]["from_database"])
            from_table = getattr(from_db, config[file_name]["from_table"])

            to_db = getattr(to_client, config[file_name]["to_database"])
            to_table = getattr(to_db, config[file_name]["to_table"])

            # Migrate all in the fog
            docs_to_migrate = from_table.find().sort("_id", 1)
            n_docs_to_migrate = docs_to_migrate.count()

            for doc in docs_to_migrate:
                to_table.insert_one(doc)
                from_table.delete_one(doc)
            
            logger.info(f"{n_docs_to_migrate} migrated to cloud")
            handle.counter = 0
        except:
            logger.error("An unexpected error happened: ")
            traceback.print_exc()
            handle.counter = 0

logger.debug("Loaded")
