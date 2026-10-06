"""Introduction to Python's built-in data types."""

# Integers and floats store whole numbers and decimal numbers.
age = 20
height = 1.72

# Strings store text. Use quotes around text values.
name = "Asha"

# Booleans represent either True or False.
is_student = True

# None represents the absence of a value.
middle_name = None

print("Integer:", age, "| type:", type(age).__name__)
print("Float:", height, "| type:", type(height).__name__)
print("String:", name, "| type:", type(name).__name__)
print("Boolean:", is_student, "| type:", type(is_student).__name__)
print("None value:", middle_name, "| type:", type(middle_name).__name__)

# Convert between compatible types when needed.
age_as_text = str(age)
height_as_integer = int(height)  # int() removes the decimal part.
print("Age as text:", age_as_text)
print("Height converted to integer:", height_as_integer)
