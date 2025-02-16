from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime
from functools import wraps
from extensions import mongo
from bson.objectid import ObjectId
from textblob import TextBlob
import time

mood_bp = Blueprint('mood', __name__)

# Cache mood analysis results
MOOD_CACHE = {}
CACHE_TIMEOUT = 300  # 5 minutes

MOOD_PLAYLISTS = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
    "sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",
    "neutral": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC"
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except Exception as e:
            current_app.logger.error(f"Token validation error: {str(e)}")
            return jsonify({"error": "Token is invalid!"}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

def analyze_mood(text):
    # Check cache first
    cache_key = hash(text)
    if cache_key in MOOD_CACHE:
        cached_result, timestamp = MOOD_CACHE[cache_key]
        if time.time() - timestamp < CACHE_TIMEOUT:
            return cached_result

    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0.3:
        mood = "happy"
    elif sentiment < -0.3:
        mood = "sad"
    else:
        mood = "neutral"
        
    # Update cache
    MOOD_CACHE[cache_key] = (mood, time.time())
    return mood

@mood_bp.route('/recommendation/from-situation', methods=['POST'])
@token_required
def recommendation_from_situation(current_user):
    try:
        data = request.get_json()
        situation = data.get('situation')
        
        if not situation or len(situation.strip()) == 0:
            return jsonify({'error': 'Situation text is required'}), 400

        detected_mood = analyze_mood(situation)
        
        # Log mood entry asynchronously
        mongo.db.moods.insert_one({
            "user_id": current_user['_id'],
            "mood": detected_mood,
            "text_input": situation,
            "timestamp": datetime.utcnow()
        })

        return jsonify({
            "detected_mood": detected_mood,
            "playlist_uri": MOOD_PLAYLISTS.get(detected_mood, MOOD_PLAYLISTS["neutral"])
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in recommendation: {str(e)}")
        return jsonify({"error": "Failed to process recommendation"}), 500