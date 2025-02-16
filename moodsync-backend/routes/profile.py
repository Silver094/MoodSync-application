from flask import Blueprint, jsonify, current_app, request
from app import mongo
from bson.objectid import ObjectId
import jwt
from functools import wraps

profile_bp = Blueprint('profile', __name__)

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers:
      bearer = request.headers.get('Authorization')
      if bearer and bearer.startswith("Bearer "):
        token = bearer.split(" ")[1]
    if not token:
      return jsonify({"error": "Token is missing"}), 401
    try:
      data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
      current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
      if not current_user:
        return jsonify({"error": "User not found"}), 401
    except Exception as e:
      return jsonify({"error": "Token is invalid", "message": str(e)}), 401
    return f(current_user, *args, **kwargs)
  return decorated

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
  # Return unified profile data (created via Spotify login)
  user_profile = {
      "username": current_user.get("username"),
      "email": current_user.get("email"),
      "spotify_id": current_user.get("spotify_id"),
      "created_at": current_user.get("created_at")
  }
  return jsonify(user_profile), 200
