from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth import auth_bp
from src.analyser import analyze_mood
from src.songCurator import get_access_token, get_new_releases
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return "Welcome to MoodSync!"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    mood = analyze_mood(text)
    return jsonify({"mood": mood})

@app.route('/new-releases', methods=['GET'])
def new_releases():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    token = get_access_token(client_id, client_secret)
    releases = get_new_releases(token)
    return jsonify(releases)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)