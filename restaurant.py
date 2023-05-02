class Restaurant:
    #__slots__=['name','loc','type','rating','price','reviews']
    def __init__(self,name,loc,type,rating,price,reviews):
        self.name=name
        self.loc=loc
        self.type=type
        self.rating=rating
        self.price=price
        self.reviews=reviews
    def __repr__(self):
        return '{'+str(self.name)+', '+str(self.loc)+', '+str(self.type)+', '+str(self.rating)+', '+str(self.reviews)+'}'