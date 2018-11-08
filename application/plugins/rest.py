import builtins

from bson import json_util
from flask import Flask, request
from logzero import logger
from pymongo import MongoClient

# Sample URL: http://localhost:5000/?luminosity:int=313&sound:int=494

def main(config):
    from flask import Flask

    app = Flask(__name__)

    client = MongoClient()

    @app.route("/")
    def main():
        query = {}

        for arg in request.args.keys():
            if ":" in arg:
                name, _type = arg.split(":")
                query[name] = request.args.get(arg, type=getattr(builtins, _type))

        data = [doc for doc in client.enviot.data.find(query)]
        print(request.args, query, data)
        return json_util.dumps(data)

    app.run(debug=True)
