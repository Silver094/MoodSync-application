import os
from flask import Flask
from config import Config
from flask_cors import CORS
from extensions import mongo
from logging.config import dictConfig

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                os.getenv("REACT_APP_URL"),
                "https://moodsync-frontend.onrender.com",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    mongo.init_app(app)

    # Basic health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    with app.app_context():
        # Register blueprints
        from routes.auth import auth_bp
        from routes.mood import mood_bp
        from routes.profile import profile_bp

        app.register_blueprint(auth_bp, url_prefix="/api")
        app.register_blueprint(mood_bp, url_prefix="/api")
        app.register_blueprint(profile_bp, url_prefix="/api")

    return app
app = create_app() 

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)