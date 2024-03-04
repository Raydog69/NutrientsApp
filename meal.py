class Meal():
    def __init__(self, productAndAmount = [(None, None)]):
        self.productAndAmount = productAndAmount
        # self.product = [i[0] for i in productAndAmount]
        # self.amount = [i[1] for i in productAndAmount]

    def AddProduct(self, productAndAmount = (None, None)):
        self.productAndAmount.append(productAndAmount)
    
    def AddDish(self, productAndAmount = [(None, None)]):
        self.productAndAmount + productAndAmount

    def newProductAndAmount(self, new):
        self.productAndAmount = new

    def getNutritionOfMeal(self, productsDic):
        total_nutrition = {'kcal': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbs': 0.0}

        for (product, amount) in self.productAndAmount:
            nutrition = productsDic[product].nutritionInProduct(amount)
            for key in total_nutrition:
                total_nutrition[key] += nutrition[key]
        return total_nutrition
    
    def toDict(self):
        meal_dict = {}
        for product, amount in self.productAndAmount:
            if product is not None:
                meal_dict[product] = amount
        return meal_dict
