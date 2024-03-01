import json
import numpy as np

def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

def writeJSON(file_path, loaded_Json):
    with open(file_path, "w") as json_file:
            json.dump(loaded_Json, json_file, indent=4)

class Product():
    def __init__(self, 
                 name = None,
                 kcal = None,
                 protein = None,
                 fat = None,
                 carbs = None,
                 imagePath = None,
                 price = None
                 ):
        
        self.name = name
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs  = carbs
        self.imagePath = imagePath
        self.price = price
    
    def returnName(self):
        return self.name

    def returnDict(self):
        return {
        "name" : self.name,
        "nutrition" : 
        {
            "kcal" : self.kcal,
            "protein" : self.protein,
            "fat" : self.fat,
            "carbs" : self.carbs
        },
        "imagePath" : self.imagePath,
        "price" : self.price
        }
    
    def returnNutrientTypes():
        return ["kcal", "protein", "fat", "carbs"]


#Load products
products_path = "products.json"
products = loadJSON(products_path)

#Load userlog
userLog_Path = "userLog.json"
userLog = loadJSON(userLog_Path)

#Add new product to products JSON file
def addNewProduct(name = None, kcal = None, protein = None, fat = None, carbs = None, imagePath = None, price = None):
    product = Product(name, kcal, protein, fat, carbs, imagePath, price)

    products[product.returnName()] = product.returnDict()

    writeJSON(products_path, products)

#Return dictionary containing quatities of all nutrients in a certain amount of a given product
def nutritionInProduct(product, amount):
    scaledNutrients = {}
    for (nutrient, consentration) in products[product]["nutrition"].items():
        scaledNutrients[nutrient] = amount/100 * consentration
    return scaledNutrients

#Return a dictionary containing quantities of all nutrients eaten within a certain date
def nutritionOfDay(date):
    dayNutritionDict = {}
    for mealDics in userLog[date].values():
        for (product, amount) in mealDics.items():
            for nutrient in Product.returnNutrientTypes():
                try:
                    dayNutritionDict[nutrient] += nutritionInProduct(product, amount)[nutrient]
                except:
                    dayNutritionDict[nutrient] = nutritionInProduct(product, amount)[nutrient]
    return dayNutritionDict


# Manually add new product
addNewProduct(name= "Potato", kcal=250, protein=5)


print(nutritionOfDay(date = "2024-1-03"))