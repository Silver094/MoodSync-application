import os
import datetime
import jwt
import requests
from flask import Blueprint, request, redirect, current_app
from werkzeug.security import generate_password_hash
from app import mongo
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)

# Environment variables (make sure these are set)
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
REACT_APP_URL = os.environ.get("REACT_APP_URL")
print("hello")
print(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI,REACT_APP_URL)

@auth_bp.route('/auth/spotify')
def auth_spotify():
    scopes = "user-read-email user-read-private streaming user-modify-playback-state user-read-playback-state"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={SPOTIFY_CLIENT_ID}"
        f"&scope={scopes.replace(' ', '%20')}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        "&show_dialog=true"
    )
    return redirect(auth_url)

@auth_bp.route('/auth/spotify/callback')
def spotify_callback():
    code = request.args.get('code')
    if not code:
        return "Missing code parameter", 400

    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,  # Ensure this matches your Spotify Developer Dashboard
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(token_url, data=data, headers=headers)

    try:
        token_data = token_response.json()
    except Exception as e:
        current_app.logger.error(f"Error parsing token response: {e}. Response text: {token_response.text}")
        return "Error retrieving Spotify tokens", 400

    if "access_token" not in token_data:
        current_app.logger.error(f"Spotify token response error: {token_response.text}")
        return "Error retrieving Spotify tokens", 400

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")

    # Use the access token to fetch the Spotify user profile
    profile_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    try:
        spotify_user = profile_response.json()
    except Exception as e:
        current_app.logger.error(f"Error parsing Spotify profile response: {e}. Response text: {profile_response.text}")
        return "Error retrieving Spotify profile", 400

    spotify_id = spotify_user.get("id")
    email = spotify_user.get("email")
    display_name = spotify_user.get("display_name") or spotify_id

    # Create or update the MoodSync user based on Spotify ID
    user = mongo.db.users.find_one({"spotify_id": spotify_id})
    if not user:
        user_data = {
            "username": display_name,
            "email": email,
            "spotify_id": spotify_id,
            "spotify_access_token": access_token,
            "spotify_refresh_token": refresh_token,
            "created_at": datetime.datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user_data)
        user = mongo.db.users.find_one({"_id": result.inserted_id})
    else:
        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "spotify_access_token": access_token,
                "spotify_refresh_token": refresh_token
            }}
        )

    # Issue your MoodSync JWT token
    jwt_payload = {
        "user_id": str(user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    moodsync_token = jwt.encode(jwt_payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    # Redirect to the frontend with both tokens
    ...
# Redirect to the frontend with both tokens
    return redirect(f"{REACT_APP_URL}/spotify/callback?token={moodsync_token}&spotifyToken={access_token}")
...
