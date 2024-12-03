from . import db

class Top_10_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(180), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False)


class All_Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False) 

    
