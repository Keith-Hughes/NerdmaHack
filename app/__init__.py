from flask import Flask
from config import config
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app.config.from_object(config[config_name])

    # Initialize other components like database, etc.
    # from .models import db
    # db.init_app(app)

    # Register routes blueprints
    from .routes import register_blueprints
    register_blueprints(app)


    return app