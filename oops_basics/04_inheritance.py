"""OOP note: inheritance lets a specialized class reuse a parent class."""


class Vehicle:
    def __init__(self, brand):
        # Shared data and behavior can live in the parent (base) class.
        self.brand = brand

    def describe(self):
        print(f"This vehicle is made by {self.brand}.")


class Car(Vehicle):
    # Car inherits Vehicle's initializer and describe method.
    def __init__(self, brand, doors):
        # super() calls the parent class implementation.
        super().__init__(brand)
        self.doors = doors

    def show_doors(self):
        print(f"This car has {self.doors} doors.")


my_car = Car("Toyota", 4)
my_car.describe()  # Inherited from Vehicle.
my_car.show_doors()  # Defined specifically on Car.
