from . import db

class Top_10_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(180), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False)
    movie_id = db.Column(db.Integer, unique=True, nullable=False)


class All_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False)
    movie_id = db.Column(db.Integer, unique=True, nullable=False)
