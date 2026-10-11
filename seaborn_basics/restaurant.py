"""Restaurant price and rating market analysis using Seaborn.

Install dependencies with:
    python -m pip install "kagglehub[pandas-datasets]" seaborn

Run from the project folder with:
    python seaborn_basics/restaurant.py
"""

from pathlib import Path
import re

import kagglehub
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATASET_HANDLE = "srisyra02/zomato-market-analysis"


def find_csv(dataset_dir: str) -> Path:
    """Find a CSV inside the downloaded Kaggle dataset."""
    csv_files = sorted(Path(dataset_dir).rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in Kaggle dataset folder: {dataset_dir}")
    if len(csv_files) > 1:
        print("CSV files found:")
        for candidate in csv_files:
            print(f"  {candidate.name}")
        print(f"Using {csv_files[0].name}")
    return csv_files[0]


def find_column(data: pd.DataFrame, candidates: tuple[str, ...]) -> str | None:
    """Match a column name while ignoring capitalization and punctuation."""
    normalize = lambda value: re.sub(r"[^a-z0-9]", "", value.lower())
    columns = {normalize(str(column)): str(column) for column in data.columns}
    for candidate in candidates:
        match = columns.get(normalize(candidate))
        if match:
            return match
    return None


def to_number(values: pd.Series) -> pd.Series:
    """Parse numeric prices/ratings, including strings like '3.8/5' and '1,200'."""
    cleaned = values.astype(str).str.replace(",", "", regex=False)
    extracted = cleaned.str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
    return pd.to_numeric(extracted, errors="coerce")


def main() -> None:
    # Download once so the script can discover the dataset's CSV filename.
    dataset_dir = kagglehub.dataset_download(DATASET_HANDLE)
    csv_path = find_csv(dataset_dir)

    # Load the discovered dataset file with KaggleHub's Pandas adapter.
    data = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        DATASET_HANDLE,
        csv_path.name,
    )
    data.columns = data.columns.astype(str).str.strip()

    print(f"Loaded {len(data):,} restaurant records from {csv_path.name}")
    print("Dataset columns:", ", ".join(data.columns))

    price_column = find_column(data, (
        "approx_cost(for two people)", "approx cost for two", "average cost for two",
        "cost_for_two", "average_cost", "price", "cost",
    ))
    rating_column = find_column(data, (
        "rate", "rating", "aggregate rating", "aggregate_rating",
    ))
    name_column = find_column(data, ("name", "restaurant name", "restaurant_name"))

    if not price_column or not rating_column:
        raise ValueError(
            "Could not identify both restaurant price and rating columns. "
            f"Found price={price_column!r}, rating={rating_column!r}. "
            "See the printed column names and add their names to the candidate lists."
        )

    analysis = pd.DataFrame({
        "price": to_number(data[price_column]),
        "rating": to_number(data[rating_column]),
    })
    if name_column:
        analysis["restaurant"] = data[name_column].astype(str)

    # Keep plausible values and remove incomplete rows before computing summaries.
    analysis = analysis.dropna(subset=["price", "rating"])
    analysis = analysis[(analysis["price"] > 0) & analysis["rating"].between(0, 5)].copy()
    if analysis.empty:
        raise ValueError("No rows have usable positive prices and ratings between 0 and 5.")

    # Group prices into four market tiers for easy comparison.
    try:
        analysis["price_tier"] = pd.qcut(
            analysis["price"], q=4,
            labels=["Budget", "Mid-range", "Premium", "Luxury"],
            duplicates="drop",
        )
    except ValueError:
        analysis["price_tier"] = pd.cut(analysis["price"], bins=4)

    summary = analysis.groupby("price_tier", observed=True).agg(
        restaurants=("rating", "size"),
        average_price=("price", "mean"),
        median_price=("price", "median"),
        average_rating=("rating", "mean"),
        median_rating=("rating", "median"),
    ).round(2)

    print("\nMarket summary by price tier:")
    print(summary.to_string())
    correlation = analysis["price"].corr(analysis["rating"])
    print(f"\nPrice-rating correlation: {correlation:.2f}")
    if correlation > 0.2:
        print("Higher-priced restaurants tend to have higher ratings in this dataset.")
    elif correlation < -0.2:
        print("Higher-priced restaurants tend to have lower ratings in this dataset.")
    else:
        print("Price and rating have a weak linear relationship in this dataset.")

    sns.set_theme(style="whitegrid", palette="deep")
    figure, axes = plt.subplots(1, 3, figsize=(18, 5))
    figure.suptitle("Restaurant Market Analysis: Price and Rating", fontsize=16)

    # Limit the scatter to the 99th price percentile so outliers do not hide the market pattern.
    scatter_data = analysis[analysis["price"] <= analysis["price"].quantile(0.99)]
    sns.scatterplot(
        data=scatter_data, x="price", y="rating", alpha=0.35,
        s=24, color="teal", ax=axes[0],
    )
    sns.regplot(
        data=scatter_data, x="price", y="rating", scatter=False,
        color="darkorange", line_kws={"linewidth": 2}, ax=axes[0],
    )
    axes[0].set_title("Price vs. rating (up to 99th percentile)")
    axes[0].set_xlabel("Price / cost value in dataset")
    axes[0].set_ylabel("Rating (out of 5)")

    sns.barplot(
        data=analysis, x="price_tier", y="rating", errorbar=None,
        order=analysis["price_tier"].dropna().unique(), ax=axes[1],
    )
    axes[1].set_title("Average rating by price tier")
    axes[1].set_xlabel("Price tier")
    axes[1].set_ylabel("Average rating")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].set_ylim(0, 5)

    tier_counts = analysis["price_tier"].value_counts().reindex(
        analysis["price_tier"].dropna().unique()
    )
    sns.barplot(x=tier_counts.index.astype(str), y=tier_counts.values, ax=axes[2])
    axes[2].set_title("Restaurant count by price tier")
    axes[2].set_xlabel("Price tier")
    axes[2].set_ylabel("Number of restaurants")
    axes[2].tick_params(axis="x", rotation=20)

    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
