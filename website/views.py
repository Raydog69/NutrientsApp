from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Day, Meal, User, Product
from . import db
import json
from datetime import datetime
import sqlite3
from sqlalchemy import inspect


views = Blueprint('views', __name__)

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

def scrape():
    data = loadJSON("website/foods.json")
    foods = data["foods"]

    for food in foods:
        constituents_dict = {} #Dict
        constituents_list = food["constituents"] #List


        for con in constituents_list:
            try:
                if con["unit"] == "mg":
                    quantity = con["quantity"] / 1000
                elif con["unit"] == 'µg':
                    quantity = con["quantity"] / 1000000
                else:
                    quantity = con["quantity"]
                constituents_dict[con["nutrientId"]] = quantity
            except:
                constituents_dict[con["nutrientId"]] = 0



        flerum = constituents_dict["Flerum"] #Float
        stivel = constituents_dict["Stivel"] #Float
        alko = constituents_dict["Alko"] #Float
        niacin = constituents_dict['Niacin'] #Float
        vitE = constituents_dict['Vit E'] #Float
        vitB1 = constituents_dict["Vit B1"] #Float
        vitB12 = constituents_dict['Vit B12'] #Float
        vitA = constituents_dict["Vit A"] #Float
        vitD = constituents_dict["Vit D"] #Float
        vitB2 = constituents_dict["Vit B2"] #Float
        vitB6 = constituents_dict["Vit B6"] #Float
        vitC = constituents_dict["Vit C"] #Float
        fiber = constituents_dict["Fiber"] #Float
        retinol = constituents_dict["Retinol"] #Float
        fiber = constituents_dict["Fiber"] #Float
        omega6 = constituents_dict["Omega-6"] #Float
        vann = constituents_dict['Vann'] #Float
        
        protein = constituents_dict['Protein'] #Float
        fat = constituents_dict["Fett"] #Float
        carbs = constituents_dict["Karbo"] #Float
        sukker = constituents_dict['Sukker'] #Float

        kcal = food["calories"]["quantity"] #Float
        # kj = food["energy"]["quantity"] #Float
        portions = food["portions"] #List
        name = food["foodName"] #String

        new_product = Product(name = name, kcal = kcal, protein = protein, fat = fat, carbs = carbs)
        try:
            db.session.add(new_product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")

    # print(foods[0]["constituents"])


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Product.query.delete()
    # print(Product.query.all())
    # scrape()
    # db.session.commit()

    nutrition_list = []

    if request.method == 'POST':
        mealTime = request.form.get('button')
        print(mealTime)

        return redirect(url_for('views.add_product', mealTime = mealTime))
    
    if not current_user.selected_day:
        new_day = Day(date = datetime.now().strftime('%Y-%m-%d'), user_id = current_user.id)
        db.session.add(new_day)
        db.session.commit()
        current_user.selected_day = new_day.id
    
    current_day = Day.query.get(current_user.selected_day) if current_user.selected_day else None

    existing_meals = Meal.query.filter(Meal.day_id == current_day.id).all()
    productNames = {}

    if not existing_meals:
        for i in range(3):
            new_meal = Meal(day_id = current_day.id)
            db.session.add(new_meal)
            db.session.commit()
        nutrition_list = [{"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}]
    if existing_meals: 
        for meal in existing_meals:
            if meal.products:
                for id in meal.products.keys():
                    productNames[id] = Product.query.get(id).name
                print(meal.get_nutrition())
                nutrition_list.append(meal.get_nutrition())
            else:
                nutrition_list.append({"kcal": 0, "protein": 0, "fat": 0, "carbs": 0})
    print(nutrition_list)

    return render_template("home.html", user=current_user, current_day=current_day, nutrition_list=nutrition_list, productNames = productNames)

@views.route('/add-product', methods=['GET', 'POST'])
def add_product():
    mealTime = request.args.get('mealTime')
    if request.method == "POST":
        data = dict(request.form)
        users = getproducts(data["search"])
        return render_template("add_product.html", user=current_user, mealTime=mealTime, data = users)
    else:
        return render_template("add_product.html", user=current_user, mealTime=mealTime)

@views.route("/add-meal", methods=['POST'])
def add_meal():
    mealTime = request.form.get('mealTime')
    product_id = request.form.get('product')
    amount = request.form.get('amount')
    
    selectedDayId = current_user.selected_day
    current_day = Day.query.get(selectedDayId) if selectedDayId else None
    
    if not current_day:
        flash('No current day', category='error')
    elif not all([mealTime, product_id, amount]):
        flash('Missing information', category='error')
    else:
        try:
            amount = int(amount)
            mealTime = int(mealTime)
            product_id = int(product_id)
            
            meal = Meal.query.filter_by(day_id=current_day.id).all()[mealTime]
            
            products_dict = meal.products
            if not products_dict:
                products_dict = {}

            products_dict[product_id] = products_dict.get(product_id, 0) + amount

            meal.products = products_dict
            print(products_dict)
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
        current_user.selected_day = day.id

        db.session.commit()

    else:

        print("Day added")
        new_day = Day(date=date, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_day) #adding the note to the database 
        current_user.selected_day = new_day.id
        db.session.commit()
    return jsonify({})

