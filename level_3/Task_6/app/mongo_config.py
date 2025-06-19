from pymongo.collection import Collection
from dotenv import load_dotenv
import os
from pymongo import AsyncMongoClient

# load .env
load_dotenv()

# Create async client
client = AsyncMongoClient(os.getenv("MONGODB_URI"))

# Reference to the database
Database = client["AuthDB"]

# Reference to the users collection
UserCollection: Collection = Database["users"]

async def get_user_collection():
    client = AsyncMongoClient(os.getenv("MONGODB_URI"))
    db = client["AuthDB"]
    collection = db["users"]
    try:
        yield collection
    finally:
        client.close()
