from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    # id = email address of user
    id = db.Column(db.String(120), unique=True, primary_key=True)
    name = db.Column(db.String(60), unique=False)
    points = db.Column(db.Integer, default=0)
    last_answer = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=0)
    non_competitive = db.Column(db.Boolean, unique=False)
    banned = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(60))
    hint = db.Column(db.String(200))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(60))
    level = db.Column(db.Integer)
    user_email = db.Column(db.String(120))
    time = db.Column(db.Integer)
    ip = db.Column(db.String(120))
    username = db.Column(db.String(60), unique=False)
