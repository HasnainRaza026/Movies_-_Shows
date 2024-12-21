import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'vgyft768uctxes445er67t8ybvgyctf5s676t8guhu')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join('tmp', 'movies_and_shows.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
