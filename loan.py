"""Predict loan approval using the Kaggle loan approval dataset."""

from pathlib import Path
import shutil

import kagglehub
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATASET_HANDLE = "architsharma01/loan-approval-prediction-dataset"
LOCAL_CSV = Path(__file__).with_name("loan.csv")
NUMERIC_FEATURES = [
    "cibil_score",
    "income_annum",
    "loan_term",
    "loan_amount",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]
CATEGORICAL_FEATURES = ["self_employed"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "loan_status"


def find_dataset_csv(dataset_dir):
    """Find the downloaded CSV that contains the expected loan columns."""
    required_columns = set(FEATURES + [TARGET])
    candidates = []

    for csv_path in Path(dataset_dir).rglob("*.csv"):
        header = pd.read_csv(csv_path, nrows=0)
        columns = {column.strip() for column in header.columns}
        if required_columns.issubset(columns):
            candidates.append(csv_path)

    if not candidates:
        raise ValueError(
            "The downloaded dataset has no CSV with the required loan columns."
        )
    if len(candidates) > 1:
        preferred = [
            path for path in candidates
            if path.name.lower() == "loan_approval_dataset.csv"
        ]
        if len(preferred) == 1:
            return preferred[0]
        raise ValueError(
            "The downloaded dataset contains multiple CSV files with loan columns."
        )
    return candidates[0]


def load_data():
    """Load the local dataset, downloading and saving it when needed."""
    if not LOCAL_CSV.exists():
        dataset_dir = kagglehub.dataset_download(DATASET_HANDLE)
        downloaded_csv = find_dataset_csv(dataset_dir)
        shutil.copyfile(downloaded_csv, LOCAL_CSV)
        print(f"Downloaded dataset saved to: {LOCAL_CSV}")

    data = pd.read_csv(LOCAL_CSV, encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    return data


def prepare_data(data):
    """Validate and clean the dataset columns used by the classifier."""
    required_columns = set(FEATURES + [TARGET])
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            f"{LOCAL_CSV.name} is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    data = data[FEATURES + [TARGET]].copy()
    for column in NUMERIC_FEATURES:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    employment_status = data["self_employed"].astype("string").str.strip().str.lower()
    unknown_employment = employment_status.notna() & ~employment_status.isin(
        ["yes", "no"]
    )
    if unknown_employment.any():
        values = sorted(employment_status[unknown_employment].unique().tolist())
        raise ValueError(f"Unknown self_employed values in dataset: {values}")
    data["self_employed"] = employment_status.map({"yes": "Yes", "no": "No"})

    loan_status = data[TARGET].astype("string").str.strip().str.lower()
    status_map = {"approved": 1, "rejected": 0}
    unknown_status = loan_status.notna() & ~loan_status.isin(status_map)
    if unknown_status.any():
        values = sorted(loan_status[unknown_status].unique().tolist())
        raise ValueError(f"Unknown loan_status values in dataset: {values}")
    data[TARGET] = loan_status.map(status_map)

    original_row_count = len(data)
    data = data.dropna(subset=FEATURES + [TARGET]).reset_index(drop=True)
    dropped_rows = original_row_count - len(data)
    if dropped_rows:
        print(f"Skipped {dropped_rows} dataset rows with missing or invalid values.")
    if data[TARGET].nunique() != 2:
        raise ValueError(
            "Training data must contain both Approved and Rejected loan statuses."
        )
    return data


def get_customer_input():
    """Prompt for customer and loan details, validating each response."""
    while True:
        try:
            cibil_score = float(input("Enter CIBIL score (300-900): "))
            income_annum = float(input("Enter annual income: "))
            employment_input = input("Is the applicant self-employed? (yes/no): ")
            loan_term = float(input("Enter loan term: "))
            loan_amount = float(input("Enter loan amount: "))
            residential_assets_value = float(input("Enter residential assets value: "))
            commercial_assets_value = float(input("Enter commercial assets value: "))
            luxury_assets_value = float(input("Enter luxury assets value: "))
            bank_asset_value = float(input("Enter bank assets value: "))
        except ValueError:
            print("Enter numeric values for scores, income, loan, and assets.")
            continue

        employment_status = employment_input.strip().lower()
        if employment_status not in ("yes", "no", "y", "n"):
            print("Enter yes or no for self-employment status.")
            continue
        if not 300 <= cibil_score <= 900:
            print("CIBIL score must be between 300 and 900.")
            continue
        if loan_term <= 0 or any(
            value < 0
            for value in (
                income_annum,
                loan_amount,
                residential_assets_value,
                commercial_assets_value,
                luxury_assets_value,
                bank_asset_value,
            )
        ):
            print("Loan term must be positive; income, loan, and assets cannot be negative.")
            continue

        return {
            "cibil_score": cibil_score,
            "income_annum": income_annum,
            "loan_term": loan_term,
            "loan_amount": loan_amount,
            "residential_assets_value": residential_assets_value,
            "commercial_assets_value": commercial_assets_value,
            "luxury_assets_value": luxury_assets_value,
            "bank_asset_value": bank_asset_value,
            "self_employed": "Yes" if employment_status in ("yes", "y") else "No",
        }


def main():
    data = prepare_data(load_data())
    preprocessor = ColumnTransformer(
        transformers=[
            ("employment", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)
        ],
        remainder="passthrough",
    )
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(n_estimators=300, random_state=42),
            ),
        ]
    )
    model.fit(data[FEATURES], data[TARGET])

    applicant = pd.DataFrame([get_customer_input()], columns=FEATURES)
    is_eligible = model.predict(applicant)[0] == 1
    print(f"\nLoan eligibility: {'Yes' if is_eligible else 'No'}")


if __name__ == "__main__":
    main()
