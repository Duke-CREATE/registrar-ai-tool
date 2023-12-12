# __init.py__
from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig, Config

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask-CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Import and register your blueprints or routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Additional initialization can go here

    return app
