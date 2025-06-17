from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# Create async client
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))

# Reference to the database
Database = client["AuthDB"]

# Reference to the users collection
UserCollection: Collection = Database["users"]
