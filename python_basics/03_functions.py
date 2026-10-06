"""Introduction to defining and using Python functions."""


# A function is a named, reusable block of code.
def greet(name):
    """Return a greeting for the supplied name."""
    return f"Hello, {name}!"


# Parameters receive values; a default makes the parameter optional.
def multiply(number, factor=2):
    """Multiply a number by a factor (2 by default)."""
    return number * factor


print(greet("Asha"))
print("5 doubled:", multiply(5))
print("5 multiplied by 3:", multiply(5, 3))

# Functions can return multiple values, which can be unpacked into variables.
def get_min_and_max(numbers):
    """Return the smallest and largest values in a non-empty list."""
    return min(numbers), max(numbers)


low, high = get_min_and_max([8, 3, 12, 5])
print("Smallest:", low)
print("Largest:", high)
