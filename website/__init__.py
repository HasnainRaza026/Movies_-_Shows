import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from utilities.logger import logger

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
DB_NAME = "movies_and_shows.db"

# Loading API key with fallback
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    logger.error("API_KEY environment variable not set. The application may not function as expected.")



def create_app(config_class='config.Config'):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)

    # Bind Flask-Migrate to the app and SQLAlchemy, used for db migrations
    migrate = Migrate(app, db)

    # Register blueprints
    from .views import views
    from .auth import auth
    from .error import error
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(error, url_prefix='/')

    # Import models and create the database
    from .models import User, Top_10_Movies, All_Movies
    create_database(app)

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Redirect unauthorized (anonymous) users to the login page
    login_manager.init_app(app)

    # Load a user by their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Import socket event handlers to ensure they are registered
    with app.app_context():
        from . import sockets

    logger.info("Flask app created and configured successfully.")
    return app



def create_database(app):
    """Create the database and tables if they don't already exist."""
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database initialized (tables created if not present).")
    except Exception as error:
        logger.error(f"Failed to initialize the database: {error}")
        raise
