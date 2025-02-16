from flask import Flask
from config import Config
from flask_cors import CORS
from extensions import mongo  # import the shared instance
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize MongoDB connection with app
    mongo.init_app(app)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.mood import mood_bp
    from routes.profile import profile_bp  # Newly created blueprint
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(mood_bp, url_prefix="/api")
    app.register_blueprint(profile_bp, url_prefix="/api")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
