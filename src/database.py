from pymongo import MongoClient
from config.settings import MongoConfig
import logging

class MongoDBClient:
    def __init__(self):
        self.config = MongoConfig()
        self.client = MongoClient(self.config.URI)
        self.db = self.client[self.config.DATABASE]
        self.collection = self.db[self.config.COLLECTION]

    def insert_trend(self, trend_data):
        try:
            result = self.collection.insert_one(trend_data)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Database insertion error: {str(e)}")
            raise

    def get_latest_trend(self):
        try:
            return self.collection.find_one(sort=[('timestamp', -1)])
        except Exception as e:
            logging.error(f"Database retrieval error: {str(e)}")
            raise