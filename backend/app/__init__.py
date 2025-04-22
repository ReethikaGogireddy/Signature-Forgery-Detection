# backend/app/__init__.py

from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Application factory for the signature forgery detection backend.
    """
    app = Flask(__name__,                     # creates nes flask instance
                static_folder=None,           # since React serves the frontend
                template_folder=None)
    CORS(app)  # allow cross‐origin requests

    # import and register your routes blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
