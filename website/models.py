from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Day(db.Model):
    date = 0
    meals = []
    water = 0
    data = "nigga" + str(meals) + str(water)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Day')