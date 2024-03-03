import random
class Meal():
    def __init__(self, productAndAmount = [(None, None)]):
        self.productAndAmount = productAndAmount
        # self.product = [i[0] for i in productAndAmount]
        # self.amount = [i[1] for i in productAndAmount]

    def AddProduct(self, productAndAmount = (None, None)):
        self.productAndAmount.append(productAndAmount)
    
    def AddDish(self, productAndAmount = [(None, None)]):
        self.productAndAmount + productAndAmount

    def getProductAndAmount(self):
        return self.productAndAmount
    
    def toDict(self):
        meal_dict = {}
        for product, amount in self.productAndAmount:
            if product is not None:
                meal_dict[product] = amount
        return meal_dict