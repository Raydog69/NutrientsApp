from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Day, Meal, User, Product
from . import db
import json
from datetime import datetime
import sqlite3
from sqlalchemy import inspect
import calendar


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

def getproducts(search):
    results = Product.query.filter(Product.name.like(f'%{search}%')).all()
    return results

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

        return redirect(url_for('views.search', mealTime = mealTime))
    
    if not current_user.selected_day:
        m = int(datetime.now().strftime('%m'))
        new_day = Day(date = datetime.now().strftime(f'%Y-{m}-%d'), user_id = current_user.id)
        db.session.add(new_day)
        db.session.commit()
        current_user.selected_day = new_day.id
        db.session.commit()

    if current_user.selected_day:
        current_day = Day.query.get(current_user.selected_day) 
    else:
        current_day = None

    existing_meals = Meal.query.filter(Meal.day_id == current_day.id).all()
    productNames = {}

    if not existing_meals:
        for i in range(3):
            new_meal = Meal(day_id = current_day.id, mealTime = i)
            db.session.add(new_meal)
            db.session.commit()
        existing_meals = Meal.query.filter(Meal.day_id == current_day.id).all()
        nutrition_list = [{"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}]
    if existing_meals:
        existing_meals = sorted(existing_meals, key=lambda x: x.mealTime)
        for meal in existing_meals:
            if meal.products:
                for id in meal.products.keys():
                    productNames[id] = Product.query.get(id).name
                nutrition_list.append(meal.get_nutrition())
            else:
                nutrition_list.append({"kcal": 0, "protein": 0, "fat": 0, "carbs": 0})
    total_nutrition = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
    for nutrition in nutrition_list:
        for key, value in nutrition.items():
            total_nutrition[key] += value
    return render_template("home.html", existing_meals=existing_meals, user=current_user, current_day=current_day, nutrition_list=nutrition_list, total_nutrition=total_nutrition, productNames = productNames)

@views.route('/profile-page', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_date = request.form.get('date')
        weight = request.form.get('weight')
        current_date = f'{current_date[:4]}-{int(current_date[5:7])}-{int(current_date[8:10])}'
        if weight != "":
            weight = float(weight)
            print(current_date, "what")
            day = Day.query.filter(Day.user_id==current_user.id, Day.date == current_date).first()
            if not day:
                new_day = Day(date=current_date, user_id=current_user.id, weight=weight)
                db.session.add(new_day)
                db.session.commit()
            else:
                day.weight = weight
                db.session.commit()

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_date = f'{current_date[:4]}-{int(current_date[5:7])}-{int(current_date[8:10])}'
    print(current_date)
    year, month, _ = map(int, current_date.split('-'))
    num_days = calendar.monthrange(year, month)[1]

    # Generate labels for the days throughout the month
    labels = [str(day) for day in range(1, num_days + 1)]
    
    data = []
    for day in range(1, num_days + 1):
        current_date = datetime.now().strftime(f'%Y-%m-{day}')
        current_date = f'{current_date[:4]}-{int(current_date[5:7])}-{int(current_date[8:10])}'
        current_day = Day.query.filter(Day.user_id==current_user.id, Day.date == current_date).first()
        if current_day:
            data.append(current_day.weight)
        else:
            data.append(None)


    graph_data = {
        "labels": labels,
        "datasets": [{
            "label": "My First dataset",
            "backgroundColor": "rgba(75, 192, 192, 0.2)",
            "borderColor": "rgba(75, 192, 192, 1)",
            "data": data
        }]
    }
    
    return render_template("profile_page.html", user=current_user, graph_data=json.dumps(graph_data))


@views.route('/search', methods=['GET', 'POST'])
def search():
    mealTime = request.args.get('mealTime')
    if request.method == "POST":
        data = dict(request.form)
        search = data["search"]
        products = getproducts(search)

        return render_template("search.html", user=current_user, data = products, mealTime=mealTime)
    else:
        return render_template("search.html", user=current_user, data = None, mealTime=mealTime)

@views.route('/add-product', methods=['GET', 'POST'])
def add_product():
    mealTime = int(request.args.get('mealTime'))
    product = int(request.args.get('product'))
    
    return render_template("add_product.html", user=current_user, mealTime=mealTime, product=product, productName=Product.query.get(product).name)

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
            
            meal = Meal.query.filter_by(day_id=current_day.id, mealTime = mealTime).first()
            
            products_dict = meal.products or {}
            products_dict[product_id] = products_dict.get(product_id, 0) + amount
            

            db.session.delete(meal)
            meal = Meal(day_id=current_day.id, products = products_dict, mealTime = mealTime) 
            db.session.add(meal)

            db.session.commit()
 
            print(meal.products, "PRINT 2")

            
            flash('Meal added successfully', category='success')
        except (IndexError, ValueError) as e:
            flash('Invalid meal time or amount', category='error')
            print(e)

    return redirect(url_for('views.home'))

@views.route("/delete-meal", methods=['POST'])
def delete_meal():
    dateDic = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    mealTime = dateDic["mealTime"]
    product_id = dateDic['product']

    selectedDayId = current_user.selected_day
    current_day = Day.query.get(selectedDayId) if selectedDayId else None
    print(mealTime, product_id, current_day, selectedDayId)

    meal = Meal.query.filter_by(day_id=current_day.id, mealTime = mealTime).first()
            
    products_dict = meal.products
    if meal.products:
        products_dict.pop(product_id)

        db.session.delete(meal)
        meal = Meal(day_id=current_day.id, products = products_dict, mealTime = mealTime) 
        db.session.add(meal)

        db.session.commit()

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
        new_day = Day(date=date, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_day) #adding the note to the database 
        db.session.commit()
        current_user.selected_day = new_day.id
        db.session.commit()
    return jsonify({})

