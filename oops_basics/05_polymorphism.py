"""OOP note: polymorphism lets different objects respond to the same operation."""


class Cat:
    def speak(self):
        return "Meow"


class Dog:
    def speak(self):
        return "Woof"


class Parrot:
    def speak(self):
        return "Hello"


# Each object has a speak() method, so the same loop works with all of them.
# The objects do not need to share a parent class for this Python style to work.
animals = [Cat(), Dog(), Parrot()]
for animal in animals:
    print(animal.speak())

# The caller asks each object to speak without needing to check its exact type.
