import os
from dotenv import load_dotenv

# Load environment variables only in development
if os.getenv('FLASK_ENV') != 'production':
    load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    MONGO_URI = os.getenv("MONGO_URI")
    SPOTIFY_CONFIG = {
        'client_id': os.getenv("SPOTIFY_CLIENT_ID"),
        'client_secret': os.getenv("SPOTIFY_CLIENT_SECRET"),
        'redirect_uri': os.getenv("SPOTIFY_REDIRECT_URI"),
    }
    REACT_APP_URL = os.getenv("REACT_APP_URL", "http://localhost:3000")
    
    # Added configuration for better performance
    MONGO_CONNECT_TIMEOUT_MS = 5000
    MONGO_SOCKET_TIMEOUT_MS = 5000
    MONGO_MAX_POOL_SIZE = 50