import json
import time
import traceback
from pathlib import Path
from threading import Thread

from loguru import logger
from pymongo import MongoClient

module_name = Path(__file__).name.replace(".py", "")


class CloudSync(Thread):
    def __init__(self, config):
        Thread.__init__(self)

        self.config = config

        self.from_client = MongoClient(
            self.config[module_name]["from_host"],
            int(self.config[module_name]["from_port"]),
        )
        self.to_client = MongoClient(
            self.config[module_name]["to_host"],
            int(self.config[module_name]["to_port"]),
        )

        # Test connection to servers
        self.from_client.server_info()
        self.to_client.server_info()

        self.from_db = getattr(
            self.from_client, self.config[module_name]["from_database"]
        )
        self.from_table = getattr(self.from_db, self.config[module_name]["from_table"])

        self.to_db = getattr(self.to_client, self.config[module_name]["to_database"])
        self.to_table = getattr(self.to_db, self.config[module_name]["to_table"])

        logger.info("CloudSync started")

    def run(self):
        while True:
            try:
                docs_to_migrate = self.from_table.find().sort("_id", 1)
                n_docs_to_migrate = docs_to_migrate.count()

                for doc in docs_to_migrate:
                    self.to_table.insert_one(doc)
                    self.from_table.delete_one(doc)

                logger.debug(f"{n_docs_to_migrate} migrated to cloud")
            except:
                logger.error("An unexpected error happened: ")
                traceback.print_exc()

            time.sleep(int(self.config[module_name]["interval_secs"]))
