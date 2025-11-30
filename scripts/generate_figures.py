#!/usr/bin/env python
"""
Generate figures for Breast-Cancer-Multimodal-Imaging-Datasets.

Reads:
    data/datasets_master.csv

Writes:
    images/histogram_with_values.png    # số dataset theo ModalityGroup
    images/piechart.png                 # % dataset theo ModalityGroup
    images/modality_subjects_bar.png    # tổng số SUBJECTS theo ModalityGroup
    images/datasets_by_datatype.png     # số dataset theo từng loại data (MRI, MG, US, CT, PET, WSI, Omics, Clinical+Report)
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------- IO ---------------------- #

def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)

    if "ModalityGroup" not in df.columns:
        raise ValueError("Column 'ModalityGroup' not found in CSV.")

    # chuẩn hóa Subjects -> numeric (patient count)
    if "Subjects" in df.columns:
        df["Subjects"] = pd.to_numeric(df["Subjects"], errors="coerce").fillna(0).astype(int)
    else:
        df["Subjects"] = 0

    # chuẩn hóa DataTypes + SupportingData cho phần detect modality
    if "DataTypes" not in df.columns:
        df["DataTypes"] = ""
    df["DataTypes"] = df["DataTypes"].fillna("")

    if "SupportingData" not in df.columns:
        df["SupportingData"] = ""
    df["SupportingData"] = df["SupportingData"].fillna("")

    return df


# ----------------- Plot helpers ----------------- #

def plot_histogram(counts: pd.Series, out_path: Path) -> None:
    """Bar plot: number of datasets per modality group."""
    modalities = counts.index.tolist()
    values = counts.values.tolist()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(modalities, values)

    plt.xlabel("Modality group")
    plt.ylabel("Number of datasets")
    plt.title("Number of datasets per modality")
    plt.xticks(rotation=30, ha="right")

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
    """Pie chart: distribution of datasets by modality group."""
    labels = counts.index.tolist()
    sizes = counts.values.tolist()

    plt.figure(figsize=(6, 6))
    plt.pie(
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


def plot_subjects_bar(subject_counts: pd.Series, out_path: Path) -> None:
    """Bar plot: total number of subjects per modality group."""
    modalities = subject_counts.index.tolist()
    values = subject_counts.values.tolist()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(modalities, values)

    plt.xlabel("Modality group")
    plt.ylabel("Total number of subjects")
    plt.title("Total subjects per modality group")
    plt.xticks(rotation=30, ha="right")

    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(val),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def plot_datatype_bar(counts: dict, out_path: Path) -> None:
    """
    Bar plot: number of datasets that contain each data type:
    MRI, MG/DBT, US, CT, PET, Histopathology/WSI, Omics, Clinical+Report.
    """
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, values)

    plt.xlabel("Data type")
    plt.ylabel("Number of datasets")
    plt.title("Number of datasets per data type")
    plt.xticks(rotation=30, ha="right")

    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(val),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()

def plot_datatype_pie(counts: dict, out_path: Path) -> None:
    """
    Pie chart: distribution of data types across all datasets.
    Lưu ý: một dataset có thể đóng góp vào nhiều lát (MRI + WSI + Omics, ...),
    nên tổng % là trên tổng số "lần xuất hiện" của data type, không phải số dataset.
    """
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Distribution of data types across datasets")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()
# --------------- Datatype detection --------------- #

def compute_datatype_counts(df: pd.DataFrame) -> dict:
    """
    Dùng DataTypes + SupportingData để detect từng loại data,
    rồi trả về dict: {label: số dataset có loại đó}.
    """
    dt = (df["DataTypes"].astype(str) + " " + df["SupportingData"].astype(str)).str.lower()

    def has_any(keywords):
        return dt.apply(lambda s: any(k.lower() in s for k in keywords))

    has_mri = has_any(["mr"])
    has_mg = has_any(["mg"])  # mammography / DBT
    has_us = has_any(["us", "ultrasound"])
    has_ct = has_any(["ct"])
    has_pet = has_any(["pt"])
    has_wsi = has_any(["histopathology", "whole slide image"])
    has_omics = has_any(["genomics", "proteomics", "molecular test"])
    has_clinical = has_any(
        [
            "demographic",
            "diagnosis",
            "follow-up",
            "treatment",
            "measurement",
            "pathology detail",
            "classification",
        ]
    )
    has_report = has_any(["report"])

    # clinical + report gộp chung
    has_clinical_or_report = has_clinical | has_report

    counts = {
        "MRI": int(has_mri.sum()),
        "Mammography/DBT": int(has_mg.sum()),
        "Ultrasound": int(has_us.sum()),
        "CT": int(has_ct.sum()),
        "PET": int(has_pet.sum()),
        "Histopathology/WSI": int(has_wsi.sum()),
        "Omics": int(has_omics.sum()),
        "Clinical/Report": int(has_clinical_or_report.sum()),
    }
    return counts


# ---------------------- main ---------------------- #

def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "data" / "datasets_master.csv"
    images_dir = repo_root / "images"

    print(f"Reading CSV from: {csv_path}")
    df = load_data(csv_path)

    # --------- 1) dataset-level counts theo ModalityGroup --------- #
    dataset_counts = (
        df["ModalityGroup"]
        .fillna("Unknown")
        .value_counts()
        .sort_index()
    )
    print("Dataset counts by ModalityGroup:")
    print(dataset_counts)

    hist_path = images_dir / "histogram_with_values.png"
    pie_path = images_dir / "piechart.png"

    print(f"Saving histogram to: {hist_path}")
    plot_histogram(dataset_counts, hist_path)

    print(f"Saving pie chart to: {pie_path}")
    plot_pie(dataset_counts, pie_path)

    # --------- 2) subject-level counts theo ModalityGroup --------- #
    subject_counts = (
        df.groupby(df["ModalityGroup"].fillna("Unknown"))["Subjects"]
        .sum()
        .sort_index()
    )
    print("Total subjects by ModalityGroup:")
    print(subject_counts)

    subj_path = images_dir / "modality_subjects_bar.png"
    print(f"Saving total-subjects bar plot to: {subj_path}")
    plot_subjects_bar(subject_counts, subj_path)

    # --------- 3) dataset-level counts theo DataTypes (radiology, WSI, omics, clinical) --------- #
    datatype_counts = compute_datatype_counts(df)
    print("Dataset counts by data type (from DataTypes + SupportingData):")
    for k, v in datatype_counts.items():
        print(f"{k}: {v}")

    dt_bar_path = images_dir / "datasets_by_datatype.png"
    print(f"Saving data-type bar plot to: {dt_bar_path}")
    plot_datatype_bar(datatype_counts, dt_bar_path)

    dt_pie_path = images_dir / "datatype_pie.png"
    print(f"Saving data-type pie chart to: {dt_pie_path}")
    plot_datatype_pie(datatype_counts, dt_pie_path)

    print("Done.")


if __name__ == "__main__":
    main()