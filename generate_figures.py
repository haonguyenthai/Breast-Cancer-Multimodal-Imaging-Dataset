#!/usr/bin/env python
"""
Generate histogram and pie chart for Breast-Cancer-Multimodal-Imaging-Datasets.

- Reads:  data/datasets_master.csv
- Writes: images/histogram_with_values.png
          images/piechart.png
"""

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    if "ModalityGroup" not in df.columns:
        raise ValueError("Column 'ModalityGroup' not found in CSV.")
    return df


def plot_histogram(counts: pd.Series, out_path: Path) -> None:
    """
    Bar plot: number of datasets per modality, with value labels.
    """
    modalities = counts.index.tolist()
    values = counts.values.tolist()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(modalities, values)

    plt.xlabel("Modality group")
    plt.ylabel("Number of datasets")
    plt.title("Number of datasets per modality")
    plt.xticks(rotation=30, ha="right")

    # Add value labels on top of bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(val),
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def plot_pie(counts: pd.Series, out_path: Path) -> None:
    """
    Pie chart: distribution of datasets by modality.
    """
    labels = counts.index.tolist()
    sizes = counts.values.tolist()

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )

    plt.title("Distribution of datasets by modality")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "data" / "datasets_master.csv"

    print(f"Reading CSV from: {csv_path}")
    df = load_data(csv_path)

    # Group by ModalityGroup
    counts = (
        df["ModalityGroup"]
        .fillna("Unknown")
        .value_counts()
        .sort_index()
    )
    print("Dataset counts by modality:")
    print(counts)

    images_dir = repo_root / "images"
    hist_path = images_dir / "histogram_with_values.png"
    pie_path = images_dir / "piechart.png"

    print(f"Saving histogram to: {hist_path}")
    plot_histogram(counts, hist_path)

    print(f"Saving pie chart to: {pie_path}")
    plot_pie(counts, pie_path)

    print("Done.")


if __name__ == "__main__":
    main()
