from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Day
from .models import Meal
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
    # Day.query.delete()
    # Meal.query.delete()
    try:
        selectedDayId = SelectedDayId.query.first().id
        current_day = Day.query.get(selectedDayId) if selectedDayId else None

        print(Meal.query.get(current_day.id).calculate_total_nutrition())
    except Exception as e:
        flash('Error occurred while retrieving data: {}'.format(str(e)), 'error')
        current_day = None

    return render_template("home.html", user=current_user, current_day=current_day)


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
            mealTime = int(mealTime)
            amount = int(amount)
            # meal = current_day.meals[mealTime].meal
            existing_meal = Meal.query.filter(Meal.day_id == current_day.id).first()
            print(existing_meal)
            new_meal = existing_meal.meal
            db.session.delete(existing_meal)

            if product in new_meal:
                new_meal[product] += amount
            else:
                new_meal[product] = amount

            existing_meal.meal = new_meal
            db.session.add(existing_meal)
            db.session.commit()

           
            

            flash('Meal added successfully', category='success')
        except (IndexError, ValueError) as e:
            flash('Invalid meal time or amount', category='error')
            print(e)

    return redirect(url_for('views.home'))


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    day = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = day['noteId']
    day = Day.query.get(noteId)
    if day:
        if day.user_id == current_user.id:
            db.session.delete(day)
            db.session.commit()

    return jsonify({})


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

    return jsonify({})

