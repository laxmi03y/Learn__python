class Car:
    def __init__(self,model,color,year):
        self.color=color
        self.year=year
        self.model=model
    def sound(self):
        return f"fat fat"
    def info(self):
        return f" {self.model} is {self.color}make in {self.year} "
my_car=Car("BMW",2005,"BLACK")
print(my_car.info())
print(my_car.sound())
