from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('database_url')

if not uri:
    raise ValueError("No database URL found in environment variables")

try:
    client = MongoClient(uri)
    db = client['Authentication']
    collection = db['Users']
except errors.ConnectionError as e:
    print(f"Could not connect to MongoDB: {e}")
    raise