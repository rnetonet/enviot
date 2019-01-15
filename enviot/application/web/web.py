import configparser
import csv
import datetime
import logging
import os.path
from io import StringIO

import pytz
import tzlocal
from bson.objectid import ObjectId
from bson.son import SON
from flask import Flask, render_template, make_response
from loguru import logger
from pymongo import MongoClient


def main():
    # Load config file
    cwd = os.path.split(__file__)[0]

    config_file = os.path.join(cwd, "web.ini")
    config = configparser.ConfigParser()
    config.read(config_file)

    if "web" not in config:
        logger.error(f"web not in config")
        return

    app = Flask(__name__)

    # Flask: only log errors
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    client = MongoClient(config["web"]["host"], int(config["web"]["port"]))
    db = getattr(client, config["web"]["database"])
    table = getattr(db, config["web"]["table"])

    def _to_local_time(utctime):
        local_timezone = tzlocal.get_localzone()
        local_time = utctime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        return local_time

    @app.template_filter("datetime")
    def _datetime(t):
        local_time = _to_local_time(t)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    @app.template_filter("hour")
    def hour(doc):
        local_time = _to_local_time(doc["_id"].generation_time)
        return local_time.strftime("%H")

    @app.route("/")
    def index():
        latest = table.find().sort([("_id", -1)]).limit(1)[0]

        dummy_id = ObjectId.from_datetime(
            datetime.datetime.today() - datetime.timedelta(days=60)
        )
        last_thirty_days = table.aggregate(
            [
                {"$match": {"_id": {"$gte": dummy_id}}},
                {
                    "$group": {
                        "_id": {
                            "$toDate": {
                                "$dateToString": {
                                    "format": "%Y-%m-%dT%H:00:00+00:00",
                                    "date": "$_id",
                                }
                            }
                        },
                        "temperatureSensor": {
                            "$avg": {"$ifNull": ["$temperatureSensor", 0]}
                        },
                        "humiditySensor": {"$avg": {"$ifNull": ["$humiditySensor", 0]}},
                        "soundSensor": {"$avg": {"$ifNull": ["$soundSensor", 0]}},
                        "luminositySensor": {
                            "$avg": {"$ifNull": ["$luminositySensor", 0]}
                        },
                        "dustSensor": {"$avg": {"$ifNull": ["$dustSensor", 0]}},
                    }
                },
                {"$sort": SON([("_id", 1)])},
            ]
        )

        return render_template("index.html", **locals())

    @app.route("/download")
    def download():
        _out = StringIO()
        _csv = csv.writer(_out)

        # headers
        _csv.writerow(["timestamp", "temperatureSensor", "soundSensor", "luminositySensor", "humiditySensor", "dustSensor", "client_id"])

        dummy_id = ObjectId.from_datetime(
            datetime.datetime.today() - datetime.timedelta(days=60)
        )
        query = table.find({"_id": {"$gte": dummy_id}}).sort([("_id", 1)])

        # rows
        for doc in query:
            try:
                _csv.writerow(
                    [
                        _to_local_time(doc["_id"].generation_time),
                        doc["temperatureSensor"],
                        doc["soundSensor"],
                        doc["luminositySensor"],
                        doc["humiditySensor"],
                        doc["dustSensor"],
                        doc["client_id"]
                    ]
                )
            except:
                logger.error(f"Can´t dump {doc} to csv")

        output = make_response(_out.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=dump.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    app.run(
        host=config["web"]["service_host"],
        port=int(config["web"]["service_port"]),
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    logger.info("Loaded")
    main()
