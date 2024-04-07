# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup CORS for all routes but specify the origins for security
    # You can also restrict this to specific routes
    CORS(app, resources={r"/api/*": {"origins": "https://atlas-frontend-two.vercel.app"}})

    app.config['CORS_HEADERS'] = 'Content-Type'

    # Configure caching and other app features
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = app.config.get('REDIS_URL')

    cache = Cache(app)

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.cache = cache

    return app
