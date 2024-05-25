from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import json

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    kcal = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float) 

    def get_nutrition(self):
        return {"kcal": self.kcal, "protein": self.protein, "fat": self.fat, "carbs": self.carbs}


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    products = db.Column(db.PickleType)
    mealTime = db.Column(db.Integer)

    def get_nutrition(self):
        nutrition = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
        for (id, amount) in self.products.items():
            for (key, item) in Product.query.get(id).get_nutrition().items():
                nutrition[key] += int(item * amount / 100)
        return nutrition
    

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255))
    meals = db.relationship('Meal')
    weight = db.Column(db.Float)
    # water = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    days = db.relationship('Day')
    selected_day = db.Column(db.Integer)
