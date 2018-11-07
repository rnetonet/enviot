from pymongo import MongoClient
client = MongoClient()
db = client.enviot

def handle(payload_decoded):
    doc = db.data.insert_one(payload_decoded)
    print(f"mongo: Ok! {doc.inserted_id}")