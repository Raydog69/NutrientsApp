from main import Product
from main import ProductDic
from main import MealDic
from main import NutritionDic


class Dish():
    def __init__(self, productAndAmountDic, recipe = "", shelf_life_in_freezer = "120 dagar formatert##"):
        self.productAndAmountDic = productAndAmountDic
        
    def getNutrition(self):
        nutrientDic = {}
        for key in Product().returnNutrientTypes():
            nutrientDic[key] = 0

        for (product, amount) in self.productAndAmountDic.items():
                temp = ProductDic().nutritionInProduct(product, amount)
                for nutrient in Product().returnNutrientTypes():
                    ProductDic().dayNutritionDict[nutrient] += temp[nutrient]
        for (product, amount) in self.productAndAmountDic.items():
            ProductDic().nutritionInProduct(product, amount) 
        return nutrientDic


spaggettiMedVann = Dish(productAndAmountDic = {"Pasta": 200, "Vann": 2000}, recipe = "Kokes i vannet i 15 minutter. :)")
dishes = [spaggettiMedVann]
print(dishes[0].getNutrition())
