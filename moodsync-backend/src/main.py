import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth import auth_bp
from src.analyser import analyze_mood
from src.songCurator import get_access_token, get_new_releases
import requests
import base64
from urllib.parse import urlencode

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
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    token = get_access_token(client_id, client_secret)
    releases = get_new_releases(token)
    return jsonify(releases)


@app.route('/login')
def login():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": os.getenv('client_id'),
        "response_type": "code",
        "redirect_uri": os.getenv('redirect_uri'),
        "scope": "user-read-private user-read-email"
    }
    return redirect(f"{auth_url}?{urlencode(params)}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{os.getenv('client_id')}:{os.getenv('client_secret')}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('redirect_uri')
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    access_token = response_data.get('access_token')
    return jsonify({"access_token": access_token})


@app.route('/profile' , methods=['GET'])
def profile():
    access_token = request.headers.get('Authorization')
    print(access_token)
    url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)