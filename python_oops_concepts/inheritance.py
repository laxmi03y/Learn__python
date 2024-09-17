

# single inheritance
class College:
    def __init__(self,name,branch):
        self.name=name
        self.branch=branch
    def attendance(self):
        return "varrey to performance"
class student(College):
    def attendance(self):
        return f" full attendence of {self.name} & which branch is {self.branch}"
stu=student("laxmi","CSE")
print(stu.attendance())

# multilevel inheritance
# multiple--------------------------------------------------------------
class Engine:
    def start(self):
        return "Engine starting"

class Radio:
    def play_music(self):
        return "Playing music"

class Car(Engine, Radio):
    def drive(self):
        return "Car driving"

car = Car()
print(car.start())
print(car.play_music())
print(car.drive())

# HEIRARICAL __________________________________

class College:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def attendance(self):
        return "varrey to performance"
class student(College):
    def attendance(self):
        return f" full attendence of {self.name} &  {self.age} year old"
class teacher(College):
    def attendance(self):
        return f" full attendence of {self.name} &  {self.age} year old"
stu=student("laxmi",22)
madam=teacher("tanu",45)
print(stu.attendance())
print(madam.attendance())