import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from utilities.logger import logger

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")  # Initialize SocketIO without app
DB_NAME = "movies_and_shows.db"

API_KEY = os.getenv('API_KEY')

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    socketio.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')  # Register routes blueprint

    from .models import Top_10_Movies, All_Movies
    create_database(app)

    # Ensure sockets.py handlers are imported
    with app.app_context():
        from . import sockets  # Import sockets to register event handlers

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        logger.info("Database initialized (tables created if not present).")
