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

class ProductDic():
    def __init__(self, products_path = "products.json"):
        self.products_path = products_path
        self.products = loadJSON(self.products_path)
        
        #Add new product to products JSON file
    def addNewProduct(self, name = None, kcal = None, protein = None, fat = None, carbs = None, imagePath = None, price = None):
        product = Product(name, kcal, protein, fat, carbs, imagePath, price)

        self.products[product.returnName()] = product.returnDict()

        writeJSON(self.products_path, self.products)


    #Return dictionary containing quatities of all nutrients in a certain amount of a given product
    def nutritionInProduct(self, product, amount):
        scaledNutrients = {}
        for (nutrient, consentration) in self.products[product]["nutrition"].items():
            scaledNutrients[nutrient] = amount/100 * consentration
        return scaledNutrients
    
    def returnProductDic(self):
        return self.products
    

class MealDic():
    def __init__(self, userLog_Path = "userLog.json"):
        self.userLog_Path = userLog_Path
        self.userLog = loadJSON(self.userLog_Path)
    
    def additionalMealInDay(self, date):
        self.userLog[date][f'Meal {len(self.userLog[date]) + 1}'] = {}
        writeJSON(self.userLog_Path, self.userLog)

    #Manually add a product to a meal of a day
    def addProductToMeal(self, date, meal, product, amount):
        try:
            self.userLog[date][meal][product] += amount
        except:
            self.userLog[date][meal][product] = amount

        writeJSON(self.userLog_Path, self.userLog)
        NutritionDic().setUserTotalNutritionLog(date)

    def returnUserLog(self):
        return self.userLog
    

class NutritionDic():
    def __init__(self, userTotalNutritionLog_Path = "userTotalNutritionLog.json"):
        self.userTotalNutritionLog_Path = userTotalNutritionLog_Path
        self.userTotalNutritionLog = loadJSON(self.userTotalNutritionLog_Path)

    def nutritionOfDay(self, date):
        dayNutritionDict = {}
        for key in Product().returnNutrientTypes():
            dayNutritionDict[key] = 0

        for mealDics in MealDic().returnUserLog()[date].values():
            for (product, amount) in mealDics.items():
                temp = ProductDic().nutritionInProduct(product, amount)
                for nutrient in Product.returnNutrientTypes():
                    dayNutritionDict[nutrient] += temp[nutrient]
        return dayNutritionDict
    

    def returnUserTotalNutritionLog(self):
        return self.userTotalNutritionLog

    def setUserTotalNutritionLog(self, date):
        self.returnUserTotalNutritionLog()[date] = self.nutritionOfDay(date)
        writeJSON(self.userTotalNutritionLog_Path, self.returnUserTotalNutritionLog())

        
#MealDic().addProductToMeal(date = "2024-1-03", meal = "Meal 3", product = "Pasta", amount = 157)
#MealDic().additionalMealInDay("2024-1-03")

ProductDic().addNewProduct(name= "Laks", kcal=205, protein=20, fat=16, carbs = 1, price= 55/4 )

# print(nutritionOfDay(date = "2024-1-03"))

