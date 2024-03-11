class Day():
    def __init__(self, date = any, meals = [], water = 0, totalNutrition = {}, productsDic = any):
        self.date = date
        self.meals = meals
        self.water = water
        self.totalNutrition = totalNutrition
        self.totalDict = []
        self.productsDic = productsDic

    def addMeal(self, meal):
        self.meals.append(meal)
        self.getNutritionOfDay(self.productsDic)

    def removeMeal(self, meal):
        self.meals.remove(meal)
        self.getNutritionOfDay(self.productsDic)

    def getWater(self):
        return self.water
    
    def alterWater(self, newWater):
        self.water = newWater

    def getNutritionOfDay(self, productsDic):
        total_nutrition = {'kcal': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbs': 0.0}

        for meal in self.meals:
            nutrition = meal.getNutritionOfMeal(productsDic)
            for key in total_nutrition:
                total_nutrition[key] += nutrition[key]
        self.totalNutrition = total_nutrition
        return total_nutrition
    
    def toDict(self):
        for meal in self.meals:
            self.totalDict.append(meal.toDict())
        return{
            "meals" : self.totalDict,
            "totalNutrition" : self.totalNutrition,
            "water": self.water
        }