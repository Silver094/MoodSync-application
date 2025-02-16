from flask import Blueprint, request, jsonify, current_app
import jwt, datetime
from functools import wraps
from app import mongo
from bson.objectid import ObjectId
from textblob import TextBlob

mood_bp = Blueprint('mood', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers.get('Authorization')
            if bearer and bearer.startswith("Bearer "):
                token = bearer.split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except Exception as e:
            return jsonify({"error": "Token is invalid!", "message": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def analyze_mood(text):
    """Analyze the situation text using sentiment polarity."""
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.3:
        return "happy"
    elif sentiment_score < -0.3:
        return "sad"
    else:
        return "neutral"

@mood_bp.route('/recommendation/from-situation', methods=['POST'])
@token_required
def recommendation_from_situation(current_user):
    data = request.get_json()
    situation = data.get('situation')
    if not situation:
        return jsonify({'error': 'Situation text is required'}), 400

    detected_mood = analyze_mood(situation)

    # Log the mood entry
    mood_data = {
        "user_id": current_user['_id'],
        "mood": detected_mood,
        "text_input": situation,
        "timestamp": datetime.datetime.utcnow()
    }
    mongo.db.moods.insert_one(mood_data)

    # Map moods to Spotify URIs (used by the Web Playback SDK)
    mood_to_playlist = {
        "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
        "sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",
        "neutral": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC"  # fallback to happy
    }
    playlist_uri = mood_to_playlist.get(detected_mood, mood_to_playlist["happy"])

    return jsonify({
        "detected_mood": detected_mood,
        "playlist_uri": playlist_uri
    }), 200
