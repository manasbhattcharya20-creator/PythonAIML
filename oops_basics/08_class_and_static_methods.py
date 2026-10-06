"""OOP note: class methods work with the class; static methods are utilities."""


class Temperature:
    unit = "Celsius"  # Class attribute shared by Temperature objects.

    def __init__(self, degrees):
        self.degrees = degrees  # Instance attribute unique to each object.

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        # cls refers to the class. This alternate constructor returns an object.
        celsius = (fahrenheit - 32) * 5 / 9
        return cls(celsius)

    @staticmethod
    def is_freezing(degrees):
        # A static method needs neither self nor cls; it groups a helper with
        # the class because the helper is conceptually related to Temperature.
        return degrees <= 0


today = Temperature.from_fahrenheit(68)
print(f"Temperature: {today.degrees:.1f} {Temperature.unit}")
print("Is it freezing?", Temperature.is_freezing(today.degrees))
