"""A beginner-friendly demonstration of common pandas operations."""

import pandas as pd


# Create a DataFrame from a dictionary (each list becomes a column).
students = pd.DataFrame(
    {
        "Name": ["Asha", "Ravi", "Meera", "Arjun", "Sara"],
        "Subject": ["Math", "Math", "Science", "Science", "Math"],
        "Score": [92, 76, 88, 65, 95],
    }
)

print("STUDENT SCORES")
print(students)

# Inspect the data.
print("\nFirst three rows:")
print(students.head(3))
print("\nColumn names:", list(students.columns))
print("\nData types and non-empty values:")
students.info()

# Select columns and filter rows.
print("\nNames and scores:")
print(students[["Name", "Score"]])

passing_students = students[students["Score"] >= 80]
print("\nStudents scoring 80 or higher:")
print(passing_students)

# Add a calculated column, then sort by score.
students["Passed"] = students["Score"] >= 70
sorted_students = students.sort_values("Score", ascending=False)
print("\nStudents sorted by score (highest first):")
print(sorted_students)

# Group rows and calculate summary statistics.
print("\nAverage score by subject:")
print(students.groupby("Subject")["Score"].mean())

print("\nOverall score statistics:")
print(students["Score"].describe())
