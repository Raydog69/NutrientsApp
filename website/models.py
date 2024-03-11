from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime
import json

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _meal = db.Column('meal', db.String(255))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))

    @property
    def meal(self):
        return json.loads(self._meal) if self._meal else {}

    @meal.setter
    def meal(self, value):
        self._meal = json.dumps(value) if value else None

        
    def calculate_total_nutrition(self):
        if not self._meal:
            return None  # No meal data, return None or appropriate default value
        products_dic = loadJSON("products.json")
        total_nutrition = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
        for (product, amount) in self.meal.items():
            if product in products_dic:
                concentration = products_dic[product]["nutrition"]
                for nutrient, concentration_value in concentration.items():
                    total_nutrition[nutrient] += (amount / 100) * concentration_value
        return total_nutrition

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), unique=True)
    meals = db.relationship('Meal')
    # water = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Day')

