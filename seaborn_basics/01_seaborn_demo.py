"""Introduction to Seaborn charts using a built-in example dataset.

Install with: python -m pip install seaborn
Run with:     python seaborn_basics/01_seaborn_demo.py
"""

import matplotlib.pyplot as plt
import seaborn as sns


def main():
    tips = sns.load_dataset("tips")
    sns.set_theme(style="whitegrid")

    figure, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    figure.suptitle("Introduction to Seaborn", fontsize=16)

    sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", ax=axes[0])
    axes[0].set(title="Bill amount and tip", xlabel="Total bill ($)", ylabel="Tip ($)")

    sns.barplot(data=tips, x="day", y="tip", hue="sex", ax=axes[1])
    axes[1].set(title="Average tip by day", xlabel="Day", ylabel="Average tip ($)")

    sns.boxplot(data=tips, x="time", y="total_bill", ax=axes[2])
    axes[2].set(title="Bill distribution by meal", xlabel="Meal", ylabel="Total bill ($)")

    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
