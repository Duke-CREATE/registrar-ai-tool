# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS globally for all domains and routes
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # Configure and initialize caching to use Redis
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = app.config.get('REDIS_URL')

    cache = Cache(app)

    # Import and register your blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.cache = cache

    return app
