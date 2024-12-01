from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from utilities.logger import logger

db = SQLAlchemy()

DB_NAME = "movies_and_shows.db"

def create_app(config_class='config.Config'):
    app = Flask (__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    from .views import views
    app.register_blueprint (views, url_prefix='/')

    from .models import Top_10_Movies, All_Movies
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        logger.info("Database initialized (tables created if not present).")

