"""OOP note: abstraction describes required behavior and hides implementation."""

from abc import ABC, abstractmethod


class Shape(ABC):
    # ABC makes this an abstract base class.
    @abstractmethod
    def area(self):
        # Child classes must provide their own area calculation.
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# Rectangle is usable because it implements the required area() method.
rectangle = Rectangle(5, 3)
print("Rectangle area:", rectangle.area())

# Shape() itself cannot be created while area() is abstract. This helps ensure
# every concrete shape provides the behavior promised by the base class.
