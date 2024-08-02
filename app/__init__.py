from flask import Flask
from config import config
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from .models import db


#load environment variables
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app.config.from_object(config[config_name])
    migrate = Migrate(app, db)

    # Initialize other components like database, etc.
    # from .models import db
    db.init_app(app)

    # Register routes blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()


    return app