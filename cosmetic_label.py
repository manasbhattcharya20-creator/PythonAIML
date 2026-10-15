"""Predict a cosmetics product label from selected ingredients.

The ingredient picker is searchable and supports selecting multiple ingredients.
Predictions are based on ingredient/category frequencies in the linked dataset;
they are statistical matches, not medical or product-safety advice.

Dependencies: pandas
"""

from collections import Counter
import math
import re
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1DhfxQuchPjk06UM5Tvwd3T56xNDNksjdEYpZzC8m-vc/export?format=csv"
)
LABEL_COLUMN = "Label"
INGREDIENT_COLUMN_PATTERN = re.compile(r"^Ingredient \d+$")


def load_data():
    """Read product labels and ingredient columns from the linked Google Sheet."""
    data = pd.read_csv(SHEET_CSV_URL, encoding="utf-8-sig")
    data.columns = data.columns.map(lambda name: str(name).strip())
    ingredient_columns = [
        column for column in data.columns
        if INGREDIENT_COLUMN_PATTERN.fullmatch(column)
    ]
    if LABEL_COLUMN not in data.columns:
        raise ValueError(f"The spreadsheet must contain a '{LABEL_COLUMN}' column.")
    if not ingredient_columns:
        raise ValueError("The spreadsheet contains no numbered ingredient columns.")

    data = data.dropna(subset=[LABEL_COLUMN]).copy()
    data[LABEL_COLUMN] = data[LABEL_COLUMN].astype(str).str.strip()
    data = data[data[LABEL_COLUMN] != ""].reset_index(drop=True)
    if data.empty:
        raise ValueError("The spreadsheet contains no product labels.")
    return data, ingredient_columns


def build_model(data, ingredient_columns):
    """Build per-label product counts and ingredient occurrence counts."""
    label_counts = Counter()
    ingredient_label_counts = {}
    ingredient_names = {}

    for _, row in data[[LABEL_COLUMN, *ingredient_columns]].iterrows():
        label = str(row[LABEL_COLUMN]).strip()
        label_counts[label] += 1
        product_ingredients = set()
        for value in row[ingredient_columns]:
            if pd.notna(value):
                ingredient = str(value).strip()
                if ingredient:
                    ingredient_key = ingredient.casefold()
                    product_ingredients.add(ingredient_key)
                    ingredient_names.setdefault(ingredient_key, ingredient)

        for ingredient_key in product_ingredients:
            counts = ingredient_label_counts.setdefault(
                ingredient_key, Counter()
            )
            counts[label] += 1

    return label_counts, ingredient_label_counts, ingredient_names


def predict_label(label_counts, ingredient_label_counts, selected_ingredients):
    """Return the highest-scoring label and normalized scores for the selection."""
    if not selected_ingredients:
        raise ValueError("Select at least one ingredient.")

    labels = sorted(label_counts)
    total_products = sum(label_counts.values())
    log_scores = {}
    for label in labels:
        # Laplace smoothing keeps rare or unseen ingredients usable.
        score = math.log((label_counts[label] + 1) / (total_products + len(labels)))
        for ingredient in selected_ingredients:
            ingredient_key = ingredient.casefold()
            present_count = ingredient_label_counts.get(
                ingredient_key, Counter()
            ).get(label, 0)
            score += math.log(
                (present_count + 1) / (label_counts[label] + 2)
            )
        log_scores[label] = score

    largest_score = max(log_scores.values())
    exponentials = {
        label: math.exp(score - largest_score)
        for label, score in log_scores.items()
    }
    total_score = sum(exponentials.values())
    probabilities = {
        label: score / total_score
        for label, score in exponentials.items()
    }
    predicted_label = max(probabilities, key=probabilities.get)
    return predicted_label, probabilities


def create_app(data, ingredient_columns):
    """Open the searchable ingredient selector and label prediction results."""
    label_counts, ingredient_label_counts, ingredient_names = build_model(
        data, ingredient_columns
    )
    all_ingredients = sorted(ingredient_names.values(), key=str.casefold)
    selected_ingredients = set()
    visible_ingredients = []

    root = tk.Tk()
    root.title("Cosmetics Label Predictor")
    root.geometry("850x650")

    ttk.Label(
        root,
        text="Search and select one or more ingredients to predict a product label.",
    ).pack(anchor="w", padx=12, pady=(12, 4))
    ttk.Label(
        root,
        text=f"{len(all_ingredients):,} ingredients available from the spreadsheet.",
    ).pack(anchor="w", padx=12, pady=(0, 8))

    search_text = tk.StringVar()
    search_entry = ttk.Entry(root, textvariable=search_text)
    search_entry.pack(fill="x", padx=12, pady=(0, 8))

    list_frame = ttk.Frame(root)
    list_frame.pack(fill="both", expand=True, padx=12)
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    ingredient_list = tk.Listbox(
        list_frame,
        selectmode=tk.EXTENDED,
        yscrollcommand=scrollbar.set,
        exportselection=False,
    )
    scrollbar.config(command=ingredient_list.yview)
    ingredient_list.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    selection_summary = tk.StringVar(value="No ingredients selected.")
    ttk.Label(root, textvariable=selection_summary).pack(
        anchor="w", padx=12, pady=(8, 4)
    )
    result_text = tk.StringVar(value="Your predicted label will appear here.")
    ttk.Label(
        root,
        textvariable=result_text,
        justify="left",
        wraplength=820,
    ).pack(anchor="w", padx=12, pady=(4, 12))

    def sync_visible_selection():
        visible_selected = {
            ingredient_list.get(index)
            for index in ingredient_list.curselection()
        }
        selected_ingredients.difference_update(visible_ingredients)
        selected_ingredients.update(visible_selected)
        count = len(selected_ingredients)
        selection_summary.set(
            f"{count} ingredient{'s' if count != 1 else ''} selected."
        )

    def refresh_ingredients(*_):
        sync_visible_selection()
        query = search_text.get().strip().casefold()
        filtered = [
            ingredient
            for ingredient in all_ingredients
            if query in ingredient.casefold()
        ]
        ingredient_list.delete(0, tk.END)
        ingredient_list.insert(tk.END, *filtered)
        visible_ingredients[:] = filtered
        for index, ingredient in enumerate(filtered):
            if ingredient in selected_ingredients:
                ingredient_list.selection_set(index)

    def selection_changed(_event=None):
        sync_visible_selection()

    def show_prediction():
        sync_visible_selection()
        if not selected_ingredients:
            messagebox.showwarning(
                "Select ingredients", "Select at least one ingredient first."
            )
            return

        predicted_label, probabilities = predict_label(
            label_counts,
            ingredient_label_counts,
            selected_ingredients,
        )
        ranked_labels = sorted(
            probabilities.items(), key=lambda item: item[1], reverse=True
        )
        details = "\n".join(
            f"{label}: {probability:.1%}"
            for label, probability in ranked_labels
        )
        result_text.set(
            f"Predicted label: {predicted_label}\n\n"
            f"Label scores based on the spreadsheet:\n{details}"
        )

    ingredient_list.bind("<<ListboxSelect>>", selection_changed)
    search_text.trace_add("write", refresh_ingredients)
    ttk.Button(
        root, text="Predict label", command=show_prediction
    ).pack(anchor="e", padx=12, pady=(0, 12))

    refresh_ingredients()
    search_entry.focus_set()
    root.mainloop()


def main():
    data, ingredient_columns = load_data()
    create_app(data, ingredient_columns)


if __name__ == "__main__":
    main()
