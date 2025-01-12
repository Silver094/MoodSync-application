from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

# Sample data
moods = [
    {"id": 1, "mood": "happy"},
    {"id": 2, "mood": "sad"},
    {"id": 3, "mood": "excited"}
]

@app.route('/')
def home():
    return "Welcome to MoodSync!"

@app.route('/moods', methods=['POST'])
def get_moods():
    request_data = request.get_json()
    print(request_data)
    return jsonify(request_data)

# @app.route('/moods/<int:mood_id>', methods=['GET'])
# def get_mood(mood_id):
#     mood = next((mood for mood in moods if mood["id"] == mood_id), None)
#     if mood is None:
#         return jsonify({"error": "Mood not found"}), 404
#     return jsonify(mood)

# @app.route('/moods', methods=['POST'])
# def add_mood():
#     new_mood = request.get_json()
#     new_mood["id"] = len(moods) + 1
#     moods.append(new_mood)
#     return jsonify(new_mood), 201

# @app.route('/moods/<int:mood_id>', methods=['PUT'])
# def update_mood(mood_id):
#     mood = next((mood for mood in moods if mood["id"] == mood_id), None)
#     if mood is None:
#         return jsonify({"error": "Mood not found"}), 404
#     updated_data = request.get_json()
#     mood.update(updated_data)
#     return jsonify(mood)

# @app.route('/moods/<int:mood_id>', methods=['DELETE'])
# def delete_mood(mood_id):
#     global moods
#     moods = [mood for mood in moods if mood["id"] != mood_id]
#     return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug=True)