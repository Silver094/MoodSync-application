import os
from datetime import datetime, timedelta
from urllib.parse import urlencode
import jwt
import requests
from flask import Blueprint, request, redirect, current_app, jsonify
from extensions import mongo
from bson.objectid import ObjectId
import time

auth_bp = Blueprint('auth', __name__)

# Constants
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_EXPIRY = timedelta(hours=24)

# Cache Spotify config for 1 hour
_config_cache = {}
_cache_timestamp = 0
_CACHE_DURATION = 3600  # 1 hour in seconds

def get_spotify_config():
    global _cache_timestamp, _config_cache
    current_time = time.time()
    
    # Check if cache is expired
    if not _config_cache or (current_time - _cache_timestamp) > _CACHE_DURATION:
        _config_cache = current_app.config['SPOTIFY_CONFIG']
        _cache_timestamp = current_time
    
    return _config_cache

@auth_bp.route('/auth/spotify')
def auth_spotify():
    try:
        config = get_spotify_config()
        scopes = "user-read-email user-read-private streaming user-modify-playback-state user-read-playback-state"
        auth_url = f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={config['client_id']}&scope={scopes.replace(' ', '%20')}&redirect_uri={config['redirect_uri']}&show_dialog=true"
        return redirect(auth_url)
    except Exception as e:
        current_app.logger.error(f"Error in auth_spotify: {str(e)}")
        return jsonify({"error": "Authentication failed"}), 500

@auth_bp.route('/auth/spotify/callback')
def spotify_callback():
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        current_app.logger.error(f"Spotify auth error: {error}")
        return redirect(f"{current_app.config['REACT_APP_URL']}/error?message={error}")

    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    try:
        # Get Spotify tokens
        tokens = get_spotify_tokens(code)
        if not tokens:
            raise Exception("Failed to get Spotify tokens")

        access_token = tokens["access_token"]
        refresh_token = tokens.get("refresh_token")
        
        # Get user profile and create/update user
        user = handle_spotify_user(access_token, refresh_token)
        if not user:
            raise Exception("Failed to handle user profile")
        
        # Generate MoodSync token
        moodsync_token = generate_jwt_token(user["_id"])
        
        # Redirect to frontend with tokens using urlencode
        redirect_params = {
            'token': moodsync_token,
            'spotifyToken': access_token
        }
        redirect_url = f"{current_app.config['REACT_APP_URL']}/spotify/callback?{urlencode(redirect_params)}"
        return redirect(redirect_url)
    
    except Exception as e:
        current_app.logger.error(f"Spotify callback error: {str(e)}")
        return redirect(f"{current_app.config['REACT_APP_URL']}/error?message=Authentication failed")
    
def get_spotify_tokens(code):
    config = get_spotify_config()
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config['redirect_uri'],
            "client_id": config['client_id'],
            "client_secret": config['client_secret']
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code != 200:
        raise Exception("Failed to get Spotify tokens")
    return response.json()

def handle_spotify_user(access_token, refresh_token):
    profile = requests.get(
        f"{SPOTIFY_API_URL}/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user_data = {
        "username": profile.get("display_name") or profile["id"],
        "email": profile.get("email"),
        "spotify_id": profile["id"],
        "spotify_access_token": access_token,
        "spotify_refresh_token": refresh_token,
        "updated_at": datetime.utcnow()
    }

    user = mongo.db.users.find_one_and_update(
        {"spotify_id": profile["id"]},
        {
            "$set": user_data,
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True,
        return_document=True
    )
    return user

def generate_jwt_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")