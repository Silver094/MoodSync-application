from flask import Flask
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)

with app.app_context():
    try:
        # Try to access the database and list collections
        collections = mongo.db.list_collection_names()
        print("Collections:", collections)
    except Exception as e:
        print("Error accessing MongoDB:", e)
