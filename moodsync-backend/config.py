import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-development-secret-key")
    MONGO_URI = os.environ.get("MONGO_URI")
