from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your MongoDB connection string
uri = os.getenv('database_url')

if not uri:
    print(uri)
    raise ValueError("No database URL found in environment variables")

try:
    # Connect to MongoDB
    client = MongoClient(uri)
    # Access the database
    db = client['Authentication']
    # Access a collection
    collection = db['Users']
except errors.ConnectionError as e:
    print(f"Could not connect to MongoDB: {e}")
    raise

# Example: Insert a document
user = {
    "name": "John Doe",
    "email": "john@example.com",
    "preferences": {
        "mood": "happy",
        "genre": "pop"
    }
}

try:
    result = collection.insert_one(user)
    print(f"User inserted with ID: {result.inserted_id}")
except errors.PyMongoError as e:
    print(f"An error occurred while inserting the document: {e}")
