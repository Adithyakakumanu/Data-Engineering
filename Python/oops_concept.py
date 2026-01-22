#oops concepts : class-blueprint,object-instance variables,encapsulation:,inheritance:,Polymorphism,abstraction

class BankAccount: #class
    bank="BOB" #class variables
    def __init__(self, balance): #constructor
        self.balance = balance #instance variables

    def withdraw(self, amount):
        self.balance -= amount

#Encapsulation is the practice of wrapping data (attributes) and methods into a single unit (class) and restricting direct access to some of an object’s components.
class Account:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount

class ParkingSystem:
    def __init__(self, big, medium, small):
        self.spaces = {
            1: big,
            2: medium,
            3: small
        }

    def addCar(self, carType):
        if self.spaces[carType] > 0:
            self.spaces[carType] -= 1
            return True
        return False


#Inheritance:where a class acquires the properties and behaviors of another class
# Base (Parent) class
class Employee:
    def __init__(self, emp_id, name, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary

    def get_details(self):
        return f"ID: {self.emp_id}, Name: {self.name}"
# Child class 1
class FullTimeEmployee(Employee):
    def __init__(self, emp_id, name, base_salary, bonus):
        super().__init__(emp_id, name, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus
# Child class 2
class PartTimeEmployee(Employee):
    def __init__(self, emp_id, name, hourly_rate, hours_worked):
        super().__init__(emp_id, name, 0)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked
# Child class 3
class Intern(Employee):
    def __init__(self, emp_id, name, stipend):
        super().__init__(emp_id, name, stipend)

    def calculate_salary(self):
        return self.base_salary
employees = [
    FullTimeEmployee(1, "Alice", 50000, 10000),
    PartTimeEmployee(2, "Bob", 500, 40),
    Intern(3, "Charlie", 15000)
]

for emp in employees:
    print(emp.get_details())
    print("Salary:", emp.calculate_salary())
    print("-" * 30)


#Polymorphism Same method name but Different behavior

class Animal:
    def speak(self):
        print("Animal makes a sound")
class Dog(Animal):
    def speak(self):
        print("Dog barks")
class Cat(Animal):
    def speak(self):
        print("Cat meows")
animals = [Dog(), Cat(), Animal()]
for animal in animals:
    animal.speak()


#Abstraction:Abstraction means hiding implementation details and showing only essential behavior.(You know what an object does, not how it does it.)

from abc import ABC, abstractmethod
class Vehicle(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    @abstractmethod
    def start_engine(self):
        pass
    def vehicle_info(self):
        print(f"Brand: {self.brand}, Model: {self.model}")
class Car(Vehicle):
    def start_engine(self):
        print(f"{self.brand} {self.model}'s engine started with a key.")
class Bike(Vehicle):
    def start_engine(self):
        print(f"{self.brand} {self.model}'s engine started with a button.")
car = Car("Toyota", "Corolla")
bike = Bike("Honda", "CBR500R")
car.vehicle_info()
car.start_engine()
bike.vehicle_info()
bike.start_engine()
