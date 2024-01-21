import os
from pymongo import MongoClient


def inject_mongo_client() -> MongoClient:
    return MongoClient(os.environ["MONGO_CONNECTION_STRING"])
