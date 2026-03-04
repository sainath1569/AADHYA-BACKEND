from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from datetime import datetime
import dotenv

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def save_log(data: dict):
    data["timestamp"] = datetime.utcnow()
    collection.insert_one(data)