"""Clean the monthly marketing data and fit a linear regression model.

The model predicts Sales Revenue from Advertising Spend. The linked sheet's
Sales Units column is deliberately excluded because it is derived from revenue
in this small example and would make the prediction misleading.

Dependencies: pandas, scikit-learn, matplotlib
"""

from pathlib import Path
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1MFB85ojEhLyMHvU8snzYX4HVgIcCea_IPDXk6czjDTc/export?format=csv"
)
LOCAL_CSV = Path(__file__).with_name("marketing_data.csv")
FEATURE = "Advertising Spend (₹)"
TARGET = "Sales Revenue (₹)"


def number_from_text(value):
    """Convert values such as '₹10,000' and '5%' to numbers."""
    if pd.isna(value):
        return float("nan")
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    return float(cleaned) if cleaned else float("nan")


def load_data():
    """Read a local CSV if present; otherwise read the Google Sheet export."""
    source = LOCAL_CSV if LOCAL_CSV.exists() else SHEET_CSV_URL
    return pd.read_csv(source, encoding="utf-8-sig")


def clean_data(data):
    """Normalize column labels and values, then drop unusable/duplicate rows."""
    data = data.copy()
    data.columns = data.columns.str.strip()

    required = {FEATURE, TARGET}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Spreadsheet is missing required columns: {sorted(missing)}")

    for column in (FEATURE, TARGET):
        data[column] = data[column].map(number_from_text)

    # Clean other numeric-looking columns too, keeping them available for later use.
    for column in ("Sales Units", "Website Visitors", "Discount (%)"):
        if column in data.columns:
            data[column] = data[column].map(number_from_text)

    data = data.drop_duplicates()
    data = data.dropna(subset=[FEATURE, TARGET])
    data = data[(data[FEATURE] >= 0) & (data[TARGET] >= 0)]
    return data.reset_index(drop=True)


def fit_linear_regression(x, y):
    """Fit y = intercept + slope*x using the ordinary least squares formula."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.var(x) == 0:
        raise ValueError("Linear regression needs at least two distinct feature values.")
    slope = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    intercept = y.mean() - slope * x.mean()
    return intercept, slope


def predict(intercept, slope, x):
    return intercept + slope * np.asarray(x, dtype=float)


def main():
    raw_data = load_data()
    data = clean_data(raw_data)
    if len(data) < 4:
        raise ValueError("At least four valid rows are needed for a train/test split.")

    print(f"Rows before cleaning: {len(raw_data)}")
    print(f"Rows after cleaning:  {len(data)}")
    print("\nCleaned data:")
    print(data.to_string(index=False))

    x = data[FEATURE].to_numpy()
    y = data[TARGET].to_numpy()
    rng = np.random.default_rng(42)
    row_order = rng.permutation(len(data))
    test_count = max(1, int(np.ceil(len(data) * 0.25)))
    test_rows = row_order[:test_count]
    train_rows = row_order[test_count:]

    intercept, slope = fit_linear_regression(x[train_rows], y[train_rows])
    predictions = predict(intercept, slope, x[test_rows])
    actual = y[test_rows]
    residuals = actual - predictions
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((actual - actual.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot else float("nan")
    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals ** 2))

    print("\nLinear regression results (test set):")
    print(f"Intercept:          ₹{intercept:,.2f}")
    print(f"Revenue per ₹1 ad:   ₹{slope:,.2f}")
    print(f"R²:                 {r_squared:.3f}")
    print(f"MAE:                ₹{mae:,.2f}")
    print(f"RMSE:               ₹{rmse:,.2f}")

    # Fit a display line to all cleaned observations after evaluating the holdout.
    display_intercept, display_slope = fit_linear_regression(x, y)
    ordered_x = np.sort(x)
    plt.scatter(x, y, color="steelblue", label="Observed months")
    plt.plot(
        ordered_x, predict(display_intercept, display_slope, ordered_x),
        color="darkorange", label="Linear regression",
    )
    plt.xlabel("Advertising Spend (₹)")
    plt.ylabel("Sales Revenue (₹)")
    plt.title("Advertising Spend vs Sales Revenue")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
