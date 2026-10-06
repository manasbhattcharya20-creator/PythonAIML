# ============================================================
# NUMPY AND PANDAS DEMONSTRATION
# Run this file in Visual Studio Code
# ============================================================

import numpy as np
import pandas as pd

print("=" * 60)
print("NUMPY DEMONSTRATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. Creating NumPy arrays
# ------------------------------------------------------------

numbers = np.array([10, 20, 30, 40, 50])

print("\n1. NumPy Array:")
print(numbers)

# ------------------------------------------------------------
# 2. Two-dimensional array
# ------------------------------------------------------------

sales = np.array([
    [100, 200, 300],
    [150, 250, 350],
    [200, 300, 400]
])

print("\n2. 2D NumPy Array:")
print(sales)

# ------------------------------------------------------------
# 3. Array properties
# ------------------------------------------------------------

print("\n3. Array Properties:")
print("Shape:", sales.shape)
print("Number of dimensions:", sales.ndim)
print("Size:", sales.size)
print("Data type:", sales.dtype)

# ------------------------------------------------------------
# 4. Mathematical operations
# ------------------------------------------------------------

print("\n4. Mathematical Operations:")

print("Original:", numbers)
print("Add 10:", numbers + 10)
print("Multiply by 2:", numbers * 2)
print("Square:", numbers ** 2)

# ------------------------------------------------------------
# 5. NumPy aggregation functions
# ------------------------------------------------------------

print("\n5. Aggregation Functions:")

print("Sum:", np.sum(numbers))
print("Mean:", np.mean(numbers))
print("Minimum:", np.min(numbers))
print("Maximum:", np.max(numbers))
print("Standard Deviation:", np.std(numbers))

# ------------------------------------------------------------
# 6. Indexing
# ------------------------------------------------------------

print("\n6. Indexing:")

print("First element:", numbers[0])
print("Third element:", numbers[2])
print("Last element:", numbers[-1])

# ------------------------------------------------------------
# 7. Slicing
# ------------------------------------------------------------

print("\n7. Slicing:")

print("First three:", numbers[:3])
print("Last two:", numbers[-2:])
print("Elements 2 to 4:", numbers[1:4])

# ------------------------------------------------------------
# 8. Filtering
# ------------------------------------------------------------

print("\n8. Filtering:")

high_values = numbers[numbers > 25]

print("Values greater than 25:")
print(high_values)


# ============================================================
# PANDAS DEMONSTRATION
# ============================================================

print("\n")
print("=" * 60)
print("PANDAS DEMONSTRATION")
print("=" * 60)

# ------------------------------------------------------------
# 9. Creating a Pandas Series
# ------------------------------------------------------------

scores = pd.Series([85, 90, 78, 92, 88])

print("\n9. Pandas Series:")
print(scores)

# ------------------------------------------------------------
# 10. Creating a DataFrame
# ------------------------------------------------------------

data = {
    "Customer_ID": [101, 102, 103, 104, 105],
    "Name": ["Rahul", "Priya", "Amit", "Sneha", "John"],
    "City": ["Bangalore", "Pune", "Delhi", "Hyderabad", "Bangalore"],
    "Age": [28, 32, 25, 35, 30],
    "Sales": [50000, 75000, 45000, 90000, 65000]
}

df = pd.DataFrame(data)

print("\n10. Pandas DataFrame:")
print(df)

# ------------------------------------------------------------
# 11. Display first and last records
# ------------------------------------------------------------

print("\n11. First 3 records:")
print(df.head(3))

print("\nLast 2 records:")
print(df.tail(2))

# ------------------------------------------------------------
# 12. DataFrame information
# ------------------------------------------------------------

print("\n12. DataFrame Information:")
print(df.info())

# ------------------------------------------------------------
# 13. Statistical summary
# ------------------------------------------------------------

print("\n13. Statistical Summary:")
print(df.describe())

# ------------------------------------------------------------
# 14. Selecting columns
# ------------------------------------------------------------

print("\n14. Select Sales Column:")
print(df["Sales"])

print("\nSelect Name and Sales:")
print(df[["Name", "Sales"]])

# ------------------------------------------------------------
# 15. Filtering data
# ------------------------------------------------------------

print("\n15. Customers with Sales > 60000:")
high_sales = df[df["Sales"] > 60000]
print(high_sales)

# ------------------------------------------------------------
# 16. Multiple conditions
# ------------------------------------------------------------

print("\n16. Bangalore Customers:")
bangalore = df[df["City"] == "Bangalore"]
print(bangalore)

print("\nCustomers Age > 30 and Sales > 60000:")

result = df[
    (df["Age"] > 30) &
    (df["Sales"] > 60000)
]

print(result)

# ------------------------------------------------------------
# 17. Sorting
# ------------------------------------------------------------

print("\n17. Sort by Sales:")
sorted_df = df.sort_values("Sales", ascending=False)
print(sorted_df)

# ------------------------------------------------------------
# 18. Adding a new column
# ------------------------------------------------------------

df["Bonus"] = df["Sales"] * 0.10

print("\n18. New Bonus Column:")
print(df)

# ------------------------------------------------------------
# 19. Creating a calculated column
# ------------------------------------------------------------

df["Final_Sales"] = df["Sales"] + df["Bonus"]

print("\n19. Final Sales:")
print(df)

# ------------------------------------------------------------
# 20. Group By
# ------------------------------------------------------------

print("\n20. Sales by City:")

city_sales = df.groupby("City")["Sales"].sum()

print(city_sales)

# ------------------------------------------------------------
# 21. Average sales by city
# ------------------------------------------------------------

print("\n21. Average Sales by City:")

average_sales = df.groupby("City")["Sales"].mean()

print(average_sales)

# ------------------------------------------------------------
# 22. Multiple aggregations
# ------------------------------------------------------------

print("\n22. Multiple Aggregations:")

summary = df.groupby("City")["Sales"].agg(
    ["sum", "mean", "min", "max", "count"]
)

print(summary)

# ------------------------------------------------------------
# 23. Missing values
# ------------------------------------------------------------

print("\n23. Missing Value Demonstration:")

df.loc[2, "Sales"] = np.nan

print(df)

print("\nNumber of missing values:")
print(df.isnull().sum())

# ------------------------------------------------------------
# 24. Fill missing values
# ------------------------------------------------------------

df["Sales"] = df["Sales"].fillna(df["Sales"].mean())

print("\n24. After Filling Missing Sales:")
print(df)

# ------------------------------------------------------------
# 25. Remove duplicate records
# ------------------------------------------------------------

print("\n25. Duplicate Check:")

print("Number of duplicate rows:",
      df.duplicated().sum())

# ------------------------------------------------------------
# 26. Final DataFrame
# ------------------------------------------------------------

print("\n26. Final DataFrame:")
print(df)

print("\n")
print("=" * 60)
print("NUMPY AND PANDAS DEMONSTRATION COMPLETED")
print("=" * 60)