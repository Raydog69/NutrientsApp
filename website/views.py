from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Day
from .models import Meal
from .models import User
from .models import SelectedDayId
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # User.query.delete()
    # Day.query.delete()
    # Meal.query.delete()
    try:
        selectedDayId = SelectedDayId.query.first().id
        current_day = Day.query.get(selectedDayId) if selectedDayId else None
        nutrition_list = []

        existing_meals = Meal.query.filter(Meal.day_id == current_day.id).all()
        if not existing_meals:
            for i in range(3):
                new_meal = Meal(day_id = current_day.id)
                db.session.add(new_meal)
                db.session.commit()
            nutrition_list = [{"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}]
        if existing_meals: 
            for meal in existing_meals:
                nutrition_list.append(meal.calculate_total_nutrition())
        print(nutrition_list)
    except Exception as e:
        flash('Error occurred while retrieving data: {}'.format(str(e)), 'error')
        current_day = None

    return render_template("home.html", user=current_user, current_day=current_day, nutrition_list=nutrition_list)

@views.route('/add-product', methods=['GET', 'POST'])
def sign_up():
   
    return render_template("add_product.html", user=current_user)

@views.route("/add-meal", methods=['POST'])
def add_meal():
    mealTime = request.form.get('mealTime')
    product = request.form.get('product')
    amount = request.form.get('amount')
    
    selectedDayId = SelectedDayId.query.first().id
    current_day = Day.query.get(selectedDayId) if selectedDayId else None
    
    if not current_day:
        flash('No current day', category='error')
    elif not all([mealTime, product, amount]):
        flash('Missing information', category='error')
    else:
        try:
            amount = int(amount)
            mealTime = int(mealTime)
            
            existing_meals = Meal.query.filter(Meal.day_id == current_day.id).all()
            new_meal_data = existing_meals[mealTime].meal
            db.session.delete(existing_meals[mealTime])

            if product in new_meal_data:
                new_meal_data[product] += amount
            else:
                new_meal_data[product] = amount

            existing_meals[mealTime].meal = new_meal_data
            db.session.add(existing_meals[mealTime])
            db.session.commit()
            

            flash('Meal added successfully', category='success')
        except (IndexError, ValueError) as e:
            flash('Invalid meal time or amount', category='error')
            print(e)

    return redirect(url_for('views.home'))



@views.route('/add-day', methods=['POST'])
def add_day():
    dateDic = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    year = dateDic["year"]
    month = dateDic['month']
    day = dateDic['date']
    date = f'{year}-{month}-{day}'
    day = Day.query.filter(Day.date == date, Day.user_id == current_user.id).first()

    if day:
        selectedDayId = SelectedDayId.query.first()
        if not selectedDayId:
            selectedDayId = selectedDayId(id = day.id)
            db.session.add(selectedDayId)
            db.session.commit()

        else:
            selectedDayId.id = day.id

            db.session.commit()

    else:

        print("Day added")
        new_day = Day(date=date, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_day) #adding the note to the database 
        db.session.commit()
        
        selectedDayId = SelectedDayId.query.first()
        if not selectedDayId:
            selectedDayId = selectedDayId(id = new_day.id)
            db.session.add(selectedDayId)
            db.session.commit()

        else:
            selectedDayId.id = new_day.id

            db.session.commit()

    return jsonify({})

