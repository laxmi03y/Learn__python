
class Animal:
    def speak(self):
        return "Some generic animal sound"

# Derived class Dog
class Dog(Animal):
    def speak(self):
        return "bow bow"

# Derived class Cat
class Cat(Animal):
    def speak(self):
        return "mew mew"


my_dog = Dog()
my_cat = Cat()


print(my_dog.speak())
print(my_cat.speak())
