from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # store a hash, not plaintext
    profile = db.Column(db.String(255))
