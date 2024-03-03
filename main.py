import json
import numpy as np
from product import Product
from meal import Meal
from day import Day
import datetime

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

def writeJSON(file_path, loaded_Json):
    with open(file_path, "w") as json_file:
            json.dump(loaded_Json, json_file, indent=4)

def InitializeAllProducts(products_path = "products.json"):
    productsData = loadJSON(products_path)
    productsDic = {}
    for product in productsData:
        productsDic[product] = Product(name=product, 
                                kcal=productsData[product]["nutrition"]["kcal"],
                                protein=productsData[product]["nutrition"]["protein"],
                                fat=productsData[product]["nutrition"]["fat"],
                                carbs=productsData[product]["nutrition"]["carbs"]
                                )
    return productsDic

def InitializeAllDays(file_path = "userLog.json"):
    daysData = loadJSON(file_path)
    daysDicDicDic = {}
    for (date, dic) in daysData.items():
        meals = []
        for mealDic in dic["meals"]:
            products = []
            for tup in mealDic.items():
                products.append(tup)
            meals.append(Meal(products))

        daysDic[date] = Day(date, meals, dic["totalNutrition"])
    return daysDic

productsDic = InitializeAllProducts()
daysDic = InitializeAllDays()

def makeDays(numdays):
    base = datetime.datetime.now()
    datetimeList = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_list = [f'{t.year}-{t.month}-{t.day}' for t in datetimeList]
    for date in date_list:
        try:
            daysDic[date]
        except:
            daysDic[date] = Day(date)

def writeAllProductsToJson(file_path = "products.json"):
    products_data = {}
    for (key, product) in productsDic.items():
        products_data[key] = product.toDict()
    writeJSON(file_path, products_data)

def writeAllDaysToJson(file_path = "userLog.json"):
    userLog_data = {}
    for (key, day) in daysDic.items():
        userLog_data[key] = day.toDict()
    writeJSON(file_path, userLog_data)

def addNewProduct(name = None, kcal = None, protein = None, fat = None, carbs = None, imagePath = None, price = None):
    product = Product(name, kcal, protein, fat, carbs, imagePath, price)
    productsDic[name] = product
    writeAllProductsToJson()  #Updates products.json
addNewProduct(name="Sild", kcal=210, protein=9.5, fat=3.4, carbs=17, price=35)

def removeProduct(product):
    productsDic.pop(product, None)
    writeAllProductsToJson()  #Updates products.json


SildOgSkeva = Meal([("Sild", 55)])
daysDic['2024-3-3'].addMeal(SildOgSkeva)


writeAllDaysToJson()  
