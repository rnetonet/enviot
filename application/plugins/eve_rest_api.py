from eve import Eve
from logzero import logger

SETTINGS = {
    "MONGO_HOST": "localhost",
    "MONGO_PORT": 27017,
    "MONGO_DBNAME": "enviot",
    "DOMAIN": {"data": {}},
    "RESOURCE_METHODS": ["GET"],
    "ITEM_METHODS": ["GET"],
}


def main():
    logger.info("Starting Eve server...")
    app = Eve(settings=SETTINGS)
    app.run()
