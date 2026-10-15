import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text


def get_customer_input():
    """Prompt until valid, non-negative age and income values are entered."""
    while True:
        try:
            age = float(input("Enter customer age: "))
            income = float(input("Enter customer income: "))
        except ValueError:
            print("Please enter numeric values for age and income.")
            continue

        if age < 0 or income < 0:
            print("Age and income must be non-negative.")
            continue
        return age, income


def main():
# 1. Create sample data
    data = {
        "Age": [22, 25, 28, 35, 40, 45, 50, 55],
        "Income": [20000, 25000, 30000, 35000, 45000, 50000, 60000, 70000],
        "Purchased": [0, 0, 0, 1, 1, 1, 1, 1],
    }

    df = pd.DataFrame(data)

# 2. Select input features and target
    X = df[["Age", "Income"]]
    y = df["Purchased"]

# 3. Train the decision tree
    model = DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    )
    model.fit(X, y)

    # 4. Read customer details and predict
    age, income = get_customer_input()
    new_customer = pd.DataFrame({"Age": [age], "Income": [income]})
    prediction = model.predict(new_customer)

    if prediction[0] == 1:
        print("Customer is likely to purchase")
    else:
        print("Customer is unlikely to purchase")

    # 5. Display the learned rules
    print(export_text(model, feature_names=list(X.columns)))


if __name__ == "__main__":
    main()
