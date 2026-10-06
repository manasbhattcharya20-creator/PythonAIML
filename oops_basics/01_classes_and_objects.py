"""OOP note: classes describe objects; objects are individual instances."""


# A class is like a blueprint. It describes what data and behavior its objects have.
class Dog:
    # A method is a function defined inside a class.
    def bark(self):
        # self refers to the particular Dog object using this method.
        print("Woof!")


# Create two separate objects from the same class blueprint.
first_dog = Dog()
second_dog = Dog()

first_dog.bark()
second_dog.bark()

# Each object can hold its own attributes (data).
first_dog.name = "Milo"
second_dog.name = "Luna"
print(first_dog.name, "and", second_dog.name, "are two different Dog objects.")
