class Day():
    def __init__(self, date = any, meals = [], totalNutrition = {}, productsDic = any):
        self.date = date
        self.meals = meals
        self.totalNutrition = totalNutrition
        self.totalDict = []
        self.productsDic = productsDic

    def addMeal(self, meal, ):
        self.meals.append(meal)
        self.getNutritionOfDay(self.productsDic)

    def removeMeal(self, meal):
        self.meals.remove(meal)
        self.getNutritionOfDay(self.productsDic)
    
    def toDict(self):
        for meal in self.meals:
            self.totalDict.append(meal.toDict())
        return{
            "meals" : self.totalDict,
            "totalNutrition" : self.totalNutrition
        }
    
    def getNutritionOfMeal(self, meal, productsDic):
        total_nutrition = {'kcal': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbs': 0.0}

        for (product, amount) in meal.productAndAmount:
            nutrition = productsDic[product].nutritionInProduct(amount)
            for key in total_nutrition:
                total_nutrition[key] += nutrition[key]
        return total_nutrition

    def getNutritionOfDay(self, productsDic):
        total_nutrition = {'kcal': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbs': 0.0}

        for meal in self.meals:
            nutrition = self.getNutritionOfMeal(meal, productsDic)
            for key in total_nutrition:
                total_nutrition[key] += nutrition[key]
        self.totalNutrition = total_nutrition
        return total_nutrition