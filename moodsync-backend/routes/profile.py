from flask import Blueprint, jsonify
from functools import wraps
from app import mongo
from routes.mood import token_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        "username": current_user.get("username"),
        "email": current_user.get("email"),
        "spotify_id": current_user.get("spotify_id"),
        "created_at": current_user.get("created_at"),
        "updated_at": current_user.get("updated_at")
    }), 200