"""Introduction to Seaborn charts using a built-in example dataset.

Installation (PowerShell, from the project folder):
    python -m pip install seaborn

If you run this project with a specific Python interpreter, use that same
interpreter for installation, for example:
    & "C:\\Users\\Admin\\AppData\\Local\\Microsoft\\WindowsApps\\python3.12.exe" -m pip install seaborn

Run the example:
    python seaborn_basics/01_seaborn_demo.py

Seaborn depends on Matplotlib, so installing Seaborn also installs Matplotlib
when it is not already available in the selected Python environment.
"""

import seaborn as sns
import matplotlib.pyplot as plt


def main():
    # Seaborn includes small sample datasets for learning and demonstrations.
    # Loading this dataset may require an internet connection the first time.
    tips = sns.load_dataset("tips")

    # Use a clean visual style for all charts.
    sns.set_theme(style="whitegrid")
    figure, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    figure.suptitle("Introduction to Seaborn", fontsize=16)

    # Scatter plot: compare two numeric columns and color points by category.
    sns.scatterplot(
        data=tips,
        x="total_bill",
        y="tip",
        hue="time",
        ax=axes[0],
    )
    axes[0].set_title("Bill amount and tip")
    axes[0].set_xlabel("Total bill ($)")
    axes[0].set_ylabel("Tip ($)")

    # Bar plot: compare the average tip across categories.
    sns.barplot(data=tips, x="day", y="tip", hue="sex", ax=axes[1])
    axes[1].set_title("Average tip by day")
    axes[1].set_xlabel("Day")
    axes[1].set_ylabel("Average tip ($)")

    # Box plot: see the median, spread, and outliers for each meal time.
    sns.boxplot(data=tips, x="time", y="total_bill", ax=axes[2])
    axes[2].set_title("Bill distribution by meal")
    axes[2].set_xlabel("Meal")
    axes[2].set_ylabel("Total bill ($)")

    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
