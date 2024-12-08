from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    top_10_movies = db.relationship('Top_10_Movies')
    all_movies = db.relationship('All_Movies')


class Top_10_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(180), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    movie_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class All_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    movie_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
