from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Day
from .models import Meal
from . import db
import json

views = Blueprint('views', __name__)

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        day = request.form.get('note')#Gets the note from the HTML 

        if len(day) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_day = Day(data=day, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_day) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


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
        print("Aldready Exits")
        for meal in day.meals:
            print(meal.meal)
            print(meal.calculate_total_nutrition())

    else:
        new_day = Day(date=date, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_day) #adding the note to the database 
        db.session.commit()

        new_meal_data = {"Potato": 200}
        new_meal = Meal(meal=new_meal_data, day_id = new_day.id) 
        db.session.add(new_meal)
        db.session.commit()
    return jsonify({})