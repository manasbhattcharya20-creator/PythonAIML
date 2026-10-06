import pandas as pd

data = pd.DataFrame(
    {
        "Name": ["Asha", "Ravi", "Meera"],
        "Score": [92, 76, 88],
    }
)

print("All students:")
print(data)

print("\nScores above 80:")
print(data[data["Score"] > 80])

print("\nAverage score:", data["Score"].mean())
