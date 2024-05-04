
# --------------------------------   DATABASE MODELS    ------------------------------------------------
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDetails(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"