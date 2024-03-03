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
    
    def nutritionInProduct(self, amount):
        scaledNutrients = {}
        for (nutrient, consentration) in [("kcal", self.kcal), ("protein", self.protein), ("fat", self.fat), ("carbs", self.carbs)]:
            scaledNutrients[nutrient] = amount/100 * consentration
        return scaledNutrients

    def toDict(self):
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
    
    def AlterProduct(self, name=None, kcal=None, protein=None, fat=None, carbs=None, imagePath=None, price=None):
        if kcal is not None:
            self.kcal = kcal
        if protein is not None:
            self.protein = protein
        if fat is not None:
            self.fat = fat
        if carbs is not None:
            self.carbs = carbs
        if imagePath is not None:
            self.imagePath = imagePath
        if price is not None:
            self.price = price