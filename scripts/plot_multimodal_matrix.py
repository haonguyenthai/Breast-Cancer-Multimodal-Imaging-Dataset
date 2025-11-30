#!/usr/bin/env python
"""
Plot multimodal intersection matrix for breast cancer datasets.

Input:
    data/datasets_master.csv

Output:
    images/multimodal_matrix.png

Ý tưởng:
- Parse DataTypes + SupportingData để detect loại data:
  MRI, Mammography, Ultrasound, CT, PET, WSI, Omics, Clinical
- Chỉ giữ các dataset có >= 2 loại (paired / multimodal)
- Vẽ heatmap: rows = dataset, cols = loại dữ liệu, ô 1 = có, 0 = không

Lưu ý:
- Đây là intersection theo "dataset", KHÔNG phải theo số bệnh nhân.
  (số bệnh nhân dùng trong script plot_multimodal_cohort_counts.py)
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_master_csv(csv_path: Path) -> pd.DataFrame:
    """Load master CSV and chuẩn hóa các cột cần thiết."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)

    if "DatasetName" not in df.columns or "DataTypes" not in df.columns:
        raise ValueError("CSV must contain at least 'DatasetName' and 'DataTypes' columns.")

    df["DataTypes"] = df["DataTypes"].fillna("")

    if "SupportingData" in df.columns:
        df["SupportingData"] = df["SupportingData"].fillna("")
    else:
        df["SupportingData"] = ""

    return df


def add_modality_flags(df: pd.DataFrame):
    """
    Thêm các cột boolean has_mri, has_mg, ... và n_modalities.
    Bỏ cột Report khỏi danh sách modality để vẽ (coi như clinical metadata).
    """
    # Ghép DataTypes + SupportingData và đưa về lowercase
    dt = (df["DataTypes"].astype(str) + " " + df["SupportingData"].astype(str)).str.lower()

    def has_any(keywords):
        return dt.apply(lambda s: any(k.lower() in s for k in keywords))

    df["has_mri"] = has_any(["mr"])
    df["has_mg"] = has_any(["mg"])  # mammography / DBT
    df["has_us"] = has_any(["us", "ultrasound"])
    df["has_ct"] = has_any(["ct"])
    df["has_pet"] = has_any(["pt"])
    df["has_wsi"] = has_any(["histopathology", "whole slide image"])
    df["has_omics"] = has_any(["genomics", "proteomics", "molecular test"])
    df["has_clinical"] = has_any(
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
    # vẫn detect report nhưng KHÔNG đưa vào matrix
    df["has_report"] = has_any(["report"])

    modality_cols = [
        "has_mri",
        "has_mg",
        "has_us",
        "has_ct",
        "has_pet",
        "has_wsi",
        "has_omics",
        "has_clinical",
        # "has_report",  # không dùng trong heatmap
    ]

    df["n_modalities"] = df[modality_cols].sum(axis=1)

    return df, modality_cols


def plot_multimodal_matrix(df: pd.DataFrame, modality_cols, out_path: Path) -> None:
    """Vẽ heatmap intersection cho các dataset có >= 2 modality."""
    # Chỉ giữ datasets paired / multimodal
    multi_df = df[df["n_modalities"] >= 2].copy()

    if multi_df.empty:
        print("No multimodal datasets (n_modalities >= 2) found. Nothing to plot.")
        return

    # Sort: dataset nào nhiều modality thì lên trên
    multi_df = multi_df.sort_values(by="n_modalities", ascending=False)

    # Build matrix
    matrix = multi_df[modality_cols].astype(int).values

    # Pretty labels cho cột
    col_labels = [
        "MRI",
        "Mammography",
        "Ultrasound",
        "CT",
        "PET",
        "WSI",
        "Omics",
        "Clinical",
    ]
    row_labels = multi_df["DatasetName"].tolist()

    # Chiều cao figure phụ thuộc số dataset
    plt.figure(figsize=(10, max(4, 0.4 * len(row_labels))))

    im = plt.imshow(matrix, aspect="auto")

    # Ticks & labels
    plt.xticks(range(len(col_labels)), col_labels, rotation=45, ha="right")
    plt.yticks(range(len(row_labels)), row_labels)

    plt.xlabel("Data type")
    plt.ylabel("Dataset")
    plt.title("Multimodal intersections (datasets with ≥ 2 data types)")

    # Colorbar để đọc 0/1
    cbar = plt.colorbar(im)
    cbar.set_label("Has data type (1 = yes, 0 = no)")

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "data" / "datasets_master.csv"
    out_path = repo_root / "images" / "multimodal_matrix.png"

    print(f"Reading: {csv_path}")
    df = load_master_csv(csv_path)
    df, modality_cols = add_modality_flags(df)

    print("Example of modality flags:")
    print(df[["DatasetName", "n_modalities"] + modality_cols].head())

    print(f"Saving multimodal matrix to: {out_path}")
    plot_multimodal_matrix(df, modality_cols, out_path)
    print("Done.")


if __name__ == "__main__":
    main()