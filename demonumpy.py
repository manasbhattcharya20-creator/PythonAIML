"""Demonstrate summation and multiplication with NumPy arrays."""

import numpy as np

first_array = np.array([1, 2, 3, 4])
second_array = np.array([5, 6, 7, 8])

print("First array:", first_array)
print("Second array:", second_array)

# Add corresponding elements and calculate the total sum.
print("Element-wise addition:", np.add(first_array, second_array))
print("Sum of first array:", np.sum(first_array))

# Sum all values in a two-dimensional array.
two_dimensional_array = np.array([[1, 2, 3], [4, 5, 6]])
print("\nTwo-dimensional array:")
print(two_dimensional_array)
print("Sum of all values in the 2D array:", np.sum(two_dimensional_array))

# Multiply corresponding elements and calculate the total product.
print("Element-wise multiplication:", np.multiply(first_array, second_array))
print("Product of first array:", np.prod(first_array))

# Add two numbers entered by the user without using a NumPy array.
first_number = int(input("\nEnter the first number: "))
second_number = int(input("Enter the second number: "))
print("Sum without using an array:", first_number + second_number)
