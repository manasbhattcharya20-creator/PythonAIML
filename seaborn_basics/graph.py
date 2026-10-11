"""Explore the Zomato market dataset with Matplotlib.

Install dependencies with:
    python -m pip install kagglehub pandas matplotlib

The first run downloads the dataset from Kaggle. A Kaggle account/token may be
required if Kaggle asks you to authenticate.
"""

from pathlib import Path

import kagglehub
import matplotlib.pyplot as plt
import pandas as pd


DATASET = "srisyra02/zomato-market-analysis"


def find_csv(dataset_path: str) -> Path:
    """Choose a CSV in the downloaded dataset directory."""
    csv_files = sorted(Path(dataset_path).rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found under {dataset_path}")
    if len(csv_files) > 1:
        print("CSV files found:")
        for index, file_path in enumerate(csv_files, start=1):
            print(f"  {index}. {file_path.name}")
        print(f"Using: {csv_files[0].name}")
    return csv_files[0]


def find_column(data: pd.DataFrame, *possible_names: str):
    """Find a column despite case, spaces, or punctuation differences."""
    normalized = {
        "".join(character for character in column.lower() if character.isalnum()): column
        for column in data.columns
    }
    for name in possible_names:
        key = "".join(character for character in name.lower() if character.isalnum())
        if key in normalized:
            return normalized[key]
    return None


def numeric_values(series: pd.Series) -> pd.Series:
    """Convert values such as '3.8/5' or '1,200' into numbers."""
    cleaned = series.astype(str).str.replace(",", "", regex=False)
    return pd.to_numeric(cleaned.str.extract(r"(-?\d+(?:\.\d+)?)")[0], errors="coerce")


def main():
    dataset_path = kagglehub.dataset_download(DATASET)
    csv_path = find_csv(dataset_path)
    data = pd.read_csv(csv_path, low_memory=False)
    data.columns = data.columns.astype(str).str.strip()

    print(f"Loaded {len(data):,} rows from {csv_path.name}")
    print("Columns:", ", ".join(data.columns))

    rating_column = find_column(data, "rate", "rating", "aggregate rating")
    cost_column = find_column(
        data, "approx_cost(for two people)", "approx cost for two", "average cost for two",
        "cost_for_two", "cost",
    )
    votes_column = find_column(data, "votes", "vote_count")
    area_column = find_column(data, "location", "locality", "listed_in(city)", "city")
    cuisine_column = find_column(data, "cuisines", "cuisine")

    # Add charts only when their source columns are available.
    charts = []

    if rating_column and cost_column:
        rating = numeric_values(data[rating_column])
        cost = numeric_values(data[cost_column])
        valid = rating.between(0, 5) & cost.gt(0)
        if valid.any():
            charts.append(("Rating vs. cost", lambda ax: ax.scatter(
                cost[valid], rating[valid], alpha=0.35, s=18, color="teal", edgecolors="none"
            ), "Average cost for two", "Rating (out of 5)"))

    if area_column:
        top_areas = data[area_column].dropna().astype(str).value_counts().head(10).sort_values()
        if not top_areas.empty:
            charts.append(("Areas with the most restaurants", lambda ax: ax.barh(
                top_areas.index, top_areas.values, color="steelblue"
            ), "Restaurant count", "Area"))

    if cuisine_column:
        cuisines = data[cuisine_column].dropna().astype(str).str.split(r",\s*").explode()
        top_cuisines = cuisines[cuisines.ne("")].value_counts().head(10).sort_values()
        if not top_cuisines.empty:
            charts.append(("Most common cuisines", lambda ax: ax.barh(
                top_cuisines.index, top_cuisines.values, color="coral"
            ), "Restaurant listings", "Cuisine"))

    if rating_column and votes_column:
        rating = numeric_values(data[rating_column])
        votes = numeric_values(data[votes_column])
        valid = rating.between(0, 5) & votes.ge(0)
        if valid.any():
            charts.append(("Ratings and customer votes", lambda ax: ax.scatter(
                votes[valid], rating[valid], alpha=0.35, s=18, color="darkorange", edgecolors="none"
            ), "Votes", "Rating (out of 5)"))

    if not charts:
        raise ValueError(
            "No supported chart columns were found. Check the printed column names "
            "and update the column-name candidates in this script."
        )

    figure, axes = plt.subplots(1, len(charts), figsize=(6 * len(charts), 5), squeeze=False)
    figure.suptitle("Zomato Market Analysis", fontsize=16)
    for ax, (title, draw, x_label, y_label) in zip(axes[0], charts):
        draw(ax)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(axis="y", alpha=0.25)

    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
