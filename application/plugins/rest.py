import builtins
import logging
from pathlib import Path

from bson import json_util
from flask import Flask, request
from logzero import logger
from pymongo import MongoClient

#
# Sample URLs:
# http://localhost:5000/?luminosity:int=313&sound:int=494
# http://localhost:5000/?sound:int=494
# http://localhost:5000/?count:int=10
#

file_name = Path(__file__).name.replace(".py", "")


def main(config):
    if file_name not in config:
        logger.error(f"{file_name} not in config")
        return

    app = Flask(__name__)

    # Flask log only errors
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    client = MongoClient(config[file_name]["host"], int(config[file_name]["port"]))
    db = getattr(client, config[file_name]["database"])
    table = getattr(db, config[file_name]["table"])

    @app.route("/")
    def main():
        query = {}

        for arg in request.args.keys():
            if ":" in arg:
                name, _type = arg.split(":")
                query[name] = request.args.get(arg, type=getattr(builtins, _type))

        data = [doc for doc in table.find(query)]
        return json_util.dumps(data)

    app.run()


logger.info("Loaded")
