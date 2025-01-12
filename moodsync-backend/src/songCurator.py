import requests
import base64
from dotenv import load_dotenv
import os
# Replace these with your Spotify API credentials
client_id = os.getenv('CLIENT_ID')
client_secret = 'your_client_secret'

# Get access token
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=headers, data=data)
    response_data = response.json()
    return response_data['access_token']

# Fetch new releases
def get_new_releases(access_token):
    url = 'https://api.spotify.com/v1/browse/new-releases'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    token = get_access_token(client_id, client_secret)
    new_releases = get_new_releases(token)
    print(new_releases)