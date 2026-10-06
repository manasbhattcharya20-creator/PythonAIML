"""Beginner-friendly examples of common Matplotlib plots.

Install Matplotlib with ``python -m pip install matplotlib`` before running.
"""

import matplotlib.pyplot as plt


def main():
    # Sample data used by the plots below.
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    temperatures = [18, 20, 24, 29, 33, 35]

    # Create a 2-by-2 grid so each chart is easy to compare.
    figure, axes = plt.subplots(2, 2, figsize=(11, 8))
    figure.suptitle("Matplotlib Plotting Demo", fontsize=16)

    # 1. Line plot: useful for showing change over time.
    axes[0, 0].plot(months, temperatures, marker="o", color="teal")
    axes[0, 0].set_title("Monthly temperature")
    axes[0, 0].set_xlabel("Month")
    axes[0, 0].set_ylabel("Temperature (°C)")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # 2. Bar chart: useful for comparing categories.
    subjects = ["Python", "Math", "Science", "English"]
    scores = [88, 76, 92, 81]
    axes[0, 1].bar(subjects, scores, color="cornflowerblue")
    axes[0, 1].set_title("Scores by subject")
    axes[0, 1].set_ylabel("Score")
    axes[0, 1].set_ylim(0, 100)

    # 3. Scatter plot: useful for seeing the relationship between two values.
    hours_studied = [1, 2, 2.5, 3, 4, 5, 6]
    test_scores = [52, 58, 65, 63, 75, 82, 90]
    axes[1, 0].scatter(hours_studied, test_scores, color="tomato", s=60)
    axes[1, 0].set_title("Study time and test score")
    axes[1, 0].set_xlabel("Hours studied")
    axes[1, 0].set_ylabel("Test score")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    # 4. Histogram: useful for seeing how values are distributed.
    exam_scores = [55, 62, 67, 70, 72, 74, 76, 78, 81, 83, 85, 88, 91, 94]
    axes[1, 1].hist(exam_scores, bins=5, color="mediumseagreen", edgecolor="black")
    axes[1, 1].set_title("Distribution of exam scores")
    axes[1, 1].set_xlabel("Score")
    axes[1, 1].set_ylabel("Number of students")

    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
