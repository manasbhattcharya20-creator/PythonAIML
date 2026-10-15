"""Predict airline passenger satisfaction with logistic regression.

The sheet's numeric columns are model inputs. The Boolean ``satisfaction``
column is the target. NumPy implements the model, so scikit-learn is not needed.

Dependencies: pandas, numpy
"""

from pathlib import Path

import numpy as np
import pandas as pd


SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1z8ztPiBB0pyMuRiRhEuEi5YIoO5IWgZq4P7swMOAWV4/export?format=csv"
)
LOCAL_CSV = Path(__file__).with_name("passenger_satisfaction.csv")
CLEANED_CSV = Path(__file__).with_name("passenger_satisfaction_cleaned.csv")
TARGET = "satisfaction"


def load_and_clean_data():
    """Keep complete numeric input rows and convert satisfaction to 0/1."""
    source = LOCAL_CSV if LOCAL_CSV.exists() else SHEET_CSV_URL
    raw = pd.read_csv(source, encoding="utf-8-sig")
    raw.columns = raw.columns.map(lambda name: str(name).strip())

    target_column = next(
        (column for column in raw.columns if column.casefold() == TARGET), None
    )
    if target_column is None:
        raise ValueError(f"The spreadsheet must contain a '{TARGET}' column.")

    labels = raw[target_column].astype(str).str.strip().str.casefold().map(
        {"true": 1, "false": 0, "1": 1, "0": 0, "satisfied": 1, "dissatisfied": 0}
    )
    features = raw.drop(columns=[target_column]).apply(pd.to_numeric, errors="coerce")
    clean = features.copy()
    clean[target_column] = labels
    clean = clean.replace([np.inf, -np.inf], np.nan).dropna().drop_duplicates()
    clean[target_column] = clean[target_column].astype(int)

    if clean.empty:
        raise ValueError("No complete rows with numeric inputs and valid labels were found.")
    if clean[target_column].nunique() != 2:
        raise ValueError("The cleaned data must contain both TRUE and FALSE labels.")
    return clean.reset_index(drop=True), list(features.columns), len(raw)


def sigmoid(values):
    """Numerically stable logistic function."""
    values = np.clip(values, -40, 40)
    return 1.0 / (1.0 + np.exp(-values))


def fit_logistic_regression(x, y, learning_rate=0.1, iterations=8000, l2=0.01):
    """Train a binary logistic-regression model with gradient descent."""
    means = x.mean(axis=0)
    scales = x.std(axis=0)
    scales[scales == 0] = 1.0
    x_scaled = (x - means) / scales
    design = np.column_stack((np.ones(len(x_scaled)), x_scaled))
    weights = np.zeros(design.shape[1], dtype=float)

    for _ in range(iterations):
        probabilities = sigmoid(design @ weights)
        gradient = design.T @ (probabilities - y) / len(y)
        gradient[1:] += l2 * weights[1:]
        weights -= learning_rate * gradient

    return weights, means, scales


def probabilities_for(x, weights, means, scales):
    x_scaled = (x - means) / scales
    design = np.column_stack((np.ones(len(x_scaled)), x_scaled))
    return sigmoid(design @ weights)


def raw_input_equation(weights, means, scales, feature_names):
    """Rewrite the standardized model equation in the original input units."""
    raw_coefficients = weights[1:] / scales
    raw_intercept = weights[0] - np.sum(raw_coefficients * means)
    equation = f"z = {raw_intercept:.6f}"
    for coefficient, feature in zip(raw_coefficients, feature_names):
        sign = "+" if coefficient >= 0 else "-"
        equation += f" {sign} {abs(coefficient):.6f} * {feature}"
    equation += "\nP(satisfied=True) = 1 / (1 + exp(-z))"
    return equation, raw_intercept, raw_coefficients


def stratified_split(y, test_fraction=0.2, seed=42):
    """Make a reproducible train/test split while keeping both labels represented."""
    rng = np.random.default_rng(seed)
    train_parts = []
    test_parts = []
    for label in (0, 1):
        rows = np.flatnonzero(y == label)
        rng.shuffle(rows)
        test_count = max(1, int(round(len(rows) * test_fraction)))
        if len(rows) - test_count < 1:
            raise ValueError("Each satisfaction class needs at least two rows.")
        test_parts.extend(rows[:test_count])
        train_parts.extend(rows[test_count:])
    rng.shuffle(train_parts)
    rng.shuffle(test_parts)
    return np.array(train_parts), np.array(test_parts)


def predict_from_user_input(feature_names, intercept, coefficients):
    """Prompt for each passenger feature separately and print the prediction."""
    print("\nEnter one passenger's information, one value at a time.")
    print("Press Enter at any prompt to exit without making a prediction.")
    while True:
        entered_values = []
        for name in feature_names:
            while True:
                answer = input(f"{name}: ").strip()
                if not answer:
                    return
                try:
                    value = float(answer)
                    if not np.isfinite(value):
                        raise ValueError
                    entered_values.append(value)
                    break
                except ValueError:
                    print("Please enter a finite number.")

        values = np.asarray(entered_values, dtype=float)
        probability = float(sigmoid(intercept + values @ coefficients))
        prediction = probability >= 0.5
        print(f"Satisfied: {prediction} (probability: {probability:.1%})")


def main():
    data, feature_names, original_count = load_and_clean_data()
    x = data[feature_names].to_numpy(dtype=float)
    y = data[TARGET].to_numpy(dtype=float)
    train_rows, test_rows = stratified_split(y)

    weights, means, scales = fit_logistic_regression(x[train_rows], y[train_rows])
    test_probabilities = probabilities_for(
        x[test_rows], weights, means, scales
    )
    test_predictions = (test_probabilities >= 0.5).astype(int)
    accuracy = float(np.mean(test_predictions == y[test_rows]))

    # Fit on all cleaned rows for the interactive predictions and displayed equation.
    final_weights, final_means, final_scales = fit_logistic_regression(x, y)
    equation, intercept, coefficients = raw_input_equation(
        final_weights, final_means, final_scales, feature_names
    )

    data.to_csv(CLEANED_CSV, index=False)
    print(f"Rows before cleaning: {original_count}")
    print(f"Rows after cleaning:  {len(data)}")
    print(f"Cleaned numeric data saved to: {CLEANED_CSV}")
    print(f"\nHoldout accuracy: {accuracy:.1%}")
    print("\nModel equation:")
    print(equation)
    predict_from_user_input(feature_names, intercept, coefficients)


if __name__ == "__main__":
    main()
