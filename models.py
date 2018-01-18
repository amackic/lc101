from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Make(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    short_name = db.Column(db.String(80))

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, text, owner_id):
        self.text = text
        self.owner_id = owner_id


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    comments = db.relationship('Comment', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
