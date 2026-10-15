"""Clean cosmetics data and publish it to a Google spreadsheet.

The cleaned data is also saved as a local CSV copy.

Dependencies: pandas, gspread, google-auth-oauthlib
"""

from pathlib import Path

import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1Z5o8WumDB06CIGrxUMK3sLaEtc1juIbwRsBYbCODnkA/export?format=csv"
)
DESTINATION_SPREADSHEET_ID = "1I8gAiDHDqZkUKAkMRfeiQkHlij1HdvAYIAjVPAPB8v4"
DESTINATION_WORKSHEET = "Cleaned Data"
GOOGLE_SHEETS_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
LOCAL_CSV = Path(__file__).with_name("cosmetics.csv")
CLEANED_CSV = Path(__file__).with_name("cosmetics_cleaned.csv")
OAUTH_CLIENT_FILE = Path(__file__).with_name("google_oauth_client.json")
OAUTH_TOKEN_FILE = Path(__file__).with_name("google_oauth_token.json")

TEXT_COLUMNS = ("Label", "Brand", "Name", "Ingredients")
NUMERIC_COLUMNS = ("Price", "Rank")
SKIN_TYPE_COLUMNS = ("Combination", "Dry", "Normal", "Oily", "Sensitive")
REQUIRED_COLUMNS = TEXT_COLUMNS + NUMERIC_COLUMNS + SKIN_TYPE_COLUMNS


def load_data():
    """Read a local cosmetics CSV if present; otherwise read the Google Sheet."""
    source = LOCAL_CSV if LOCAL_CSV.exists() else SHEET_CSV_URL
    return pd.read_csv(source, encoding="utf-8-sig")


def clean_data(data):
    """Normalize cosmetics data, remove incomplete/duplicate rows, and validate it."""
    data = data.copy()
    data.columns = data.columns.map(lambda name: str(name).strip())

    missing_columns = sorted(set(REQUIRED_COLUMNS).difference(data.columns))
    if missing_columns:
        raise ValueError(
            f"Spreadsheet is missing required columns: {missing_columns}"
        )

    for column in TEXT_COLUMNS:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace("", pd.NA)

    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    binary_values = {
        "1": 1,
        "1.0": 1,
        "true": 1,
        "yes": 1,
        "0": 0,
        "0.0": 0,
        "false": 0,
        "no": 0,
    }
    for column in SKIN_TYPE_COLUMNS:
        values = data[column].astype("string").str.strip().str.casefold()
        normalized = values.map(binary_values)
        invalid_values = values[values.notna() & normalized.isna()].unique()
        if len(invalid_values):
            raise ValueError(
                f"Column '{column}' contains invalid skin-type flags: "
                f"{invalid_values.tolist()}"
            )
        data[column] = normalized

    data[list(NUMERIC_COLUMNS)] = data[list(NUMERIC_COLUMNS)].replace(
        [float("inf"), float("-inf")], pd.NA
    )
    data = data.dropna(subset=list(REQUIRED_COLUMNS))
    data = data.drop_duplicates().reset_index(drop=True)

    if data.empty:
        raise ValueError("No complete cosmetics product rows were found.")

    for column in SKIN_TYPE_COLUMNS:
        data[column] = data[column].astype(int)

    return data


def split_ingredients(data):
    """Add one column per ingredient while retaining the original ingredient list."""
    ingredient_rows = [
        [ingredient.strip() for ingredient in ingredients.split(",") if ingredient.strip()]
        for ingredients in data["Ingredients"]
    ]
    ingredient_columns = pd.DataFrame(ingredient_rows, index=data.index)
    ingredient_columns.columns = [
        f"Ingredient {number}" for number in range(1, len(ingredient_columns.columns) + 1)
    ]
    return pd.concat([data, ingredient_columns], axis=1)


def authorize_google_sheets():
    """Authorize access using a local Google OAuth Desktop client."""
    if not OAUTH_CLIENT_FILE.exists():
        raise FileNotFoundError(
            f"Google OAuth client file not found: {OAUTH_CLIENT_FILE}\n"
            "Create a Google Cloud OAuth client ID for a Desktop app, download "
            "its JSON file, and save it beside cosmetics.py as "
            "'google_oauth_client.json'. Enable the Google Sheets API and use "
            "an account that can edit the destination spreadsheet."
        )

    credentials = None
    if OAUTH_TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            OAUTH_TOKEN_FILE, GOOGLE_SHEETS_SCOPE
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            OAUTH_CLIENT_FILE, GOOGLE_SHEETS_SCOPE
        )
        credentials = flow.run_local_server(port=0)

    OAUTH_TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")
    return gspread.authorize(credentials)


def write_to_google_sheet(data):
    """Write cleaned rows to the destination spreadsheet's dedicated worksheet."""
    client = authorize_google_sheets()
    spreadsheet = client.open_by_key(DESTINATION_SPREADSHEET_ID)
    try:
        worksheet = spreadsheet.worksheet(DESTINATION_WORKSHEET)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=DESTINATION_WORKSHEET,
            rows=max(len(data) + 1, 100),
            cols=len(data.columns),
        )

    values = [data.columns.tolist()] + data.astype(object).values.tolist()
    worksheet.resize(
        rows=max(len(values), worksheet.row_count),
        cols=max(len(data.columns), worksheet.col_count),
    )
    worksheet.clear()
    worksheet.update(
        values=values,
        range_name="A1",
        value_input_option="RAW",
    )
    return spreadsheet.url


def main():
    raw_data = load_data()
    cleaned_data = split_ingredients(clean_data(raw_data))
    cleaned_data.to_csv(CLEANED_CSV, index=False, encoding="utf-8")
    spreadsheet_url = write_to_google_sheet(cleaned_data)

    removed_rows = len(raw_data) - len(cleaned_data)
    print(f"Rows before cleaning: {len(raw_data)}")
    print(f"Rows after cleaning:  {len(cleaned_data)}")
    print(f"Rows removed:         {removed_rows}")
    print(f"Local CSV saved to:    {CLEANED_CSV}")
    print(f"Google Sheet updated:  {spreadsheet_url}")


if __name__ == "__main__":
    main()
