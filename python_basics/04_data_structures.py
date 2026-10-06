"""Introduction to lists, tuples, dictionaries, and sets."""

# A list is ordered and changeable. Indexes start at zero.
fruits = ["apple", "banana", "mango"]
fruits.append("orange")
print("List:", fruits)
print("First fruit:", fruits[0])

# A tuple is ordered but cannot be changed after it is created.
point = (4, 7)
print("Tuple coordinate:", point)
print("X coordinate:", point[0])

# A dictionary stores values under keys for easy lookup.
student = {"name": "Ravi", "score": 86}
student["grade"] = "B"  # Add a new key and value.
print("Dictionary:", student)
print("Student name:", student["name"])

# A set stores unique values; duplicates are removed automatically.
unique_numbers = {1, 2, 2, 3, 3, 3}
unique_numbers.add(4)
print("Set of unique numbers:", unique_numbers)

# Loop through dictionary key-value pairs.
print("Student details:")
for key, value in student.items():
    print(f"{key}: {value}")
