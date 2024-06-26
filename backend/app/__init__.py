# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure CORS with specific options
    CORS(app, resources={
        r"/process_message": {
            "origins": [
                "https://atlas-frontend-two.vercel.app",
                "https://atlas-frontend-git-main-daniels-projects-a44d4a0e.vercel.app",
                "https://atlas-frontend-faav82vd0-daniels-projects-a44d4a0e.vercel.app"
            ]
        }
    }, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Configure and initialize caching to use Redis
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = app.config.get('REDIS_URL')

    cache = Cache(app)

    # Import and register your blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.cache = cache

    return app
