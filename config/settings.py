import os
from dotenv import load_dotenv

load_dotenv()

class TwitterConfig:
    EMAIL = os.getenv('TWITTER_EMAIL')
    PASSWORD = os.getenv('TWITTER_PASSWORD')

class ProxyConfig:
    AUTH = os.getenv('PROXYMESH_AUTH')

class MongoConfig:
    URI = os.getenv('MONGODB_URI')
    DATABASE = 'twitter_trends'
    COLLECTION = 'trends'
