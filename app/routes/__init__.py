from flask import Flask
from .api_routes import api_bp
from .frontend_routes import front_end_bp

def register_blueprints(app:Flask):
    app.register_blueprint(api_bp)
    app.register_blueprint(front_end_bp)