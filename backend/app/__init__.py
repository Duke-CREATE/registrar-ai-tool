# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from .config import Config  # Assuming you have a separate production configuration

def create_app(config_class=Config):  # Change to use ProductionConfig for production
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask-CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Configure and initialize caching to use Redis
    # Ensure these settings are correct for your Redis setup
    app.config['CACHE_TYPE'] = 'RedisCache'  # Change from 'simple' to 'RedisCache'
    app.config['CACHE_REDIS_URL'] = app.config.get('REDIS_URL')  # Use REDIS_URL from your config, or fallback to default

    cache = Cache(app)

    # Import and register your blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Make cache accessible through app for route-specific caching
    app.cache = cache

    return app

