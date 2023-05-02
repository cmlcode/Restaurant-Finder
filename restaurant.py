class Restaurant:
    #__slots__=['name','loc','type','rating','price','reviews']
    def __init__(self,name: str, latitude: int, longitude: int, food_type: str, rating:int, price:int, reviews:int) -> None:
        self.set_name(name)
        self.set_loc(latitude, longitude)
        self.set_type(food_type)
        self.rating=rating
        self.price=price
        self.reviews=reviews

    def __repr__(self) -> str:
        return '{'+str(self.name)+', '+str(self.loc)+', '+str(self.type)+', '+str(self.rating)+', '+str(self.reviews)+'}'
    
    def set_name(self, new_name:str) -> None:
        self.name = new_name
    def set_loc(self, latitude: int, longitude: int):
        if (latitude < -90 or latitude > 90):
            raise ValueError
        if (longitude < -180 or longitude > 180):
            raise ValueError

        self.loc = (latitude, longitude)
    def set_type(self, food_type: str) -> None:
        self.food_type = food_type
    def set_rating(self, rating: int) -> None:
        if (rating < 0 or rating > 5):
            raise ValueError
        self.rating = rating
    def set_price(self, price:int) -> None:
        if (price < 0 or price > 5):
            raise ValueError
        self.price = price
    def set_reviews(self, reviews:int):
        if (reviews < 0):
            raise ValueError
        self.reviews = reviews