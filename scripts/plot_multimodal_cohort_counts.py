#!/usr/bin/env python
"""
Plot intersection of modalities weighted by cohort size (Subjects).

Input:
    data/datasets_master.csv

Output:
    images/multimodal_cohort_counts.png

Interpretation:
- Mỗi dòng trong CSV = một cohort.
- Nếu cohort có Subjects = N và có cả MRI + MG + CT,
  ta xem như N patients có đủ 3 modality đó.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_master_csv(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)

    # Chuẩn hóa cột dùng
    for col in ["DatasetName", "DataTypes", "SupportingData", "Subjects"]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV.")
    df["DataTypes"] = df["DataTypes"].fillna("")
    df["SupportingData"] = df["SupportingData"].fillna("")
    # Subjects: convert to int, non-numeric -> 0
    df["Subjects"] = pd.to_numeric(df["Subjects"], errors="coerce").fillna(0).astype(int)
    return df


def add_modality_flags(df: pd.DataFrame):
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
        ["demographic", "diagnosis", "follow-up", "treatment", "measurement", "pathology detail", "classification"]
    )
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
        "has_report",
    ]

    df["n_modalities"] = df[modality_cols].sum(axis=1)

    return df, modality_cols


def aggregate_by_combination(df: pd.DataFrame, modality_cols):
    """
    Tạo combination string cho mỗi dataset, rồi cộng tổng Subjects theo combination.
    Only keeps combos với >= 2 modality.
    """
    # map column -> label đẹp
    col_to_label = {
        "has_mri": "MRI",
        "has_mg": "MG",
        "has_us": "US",
        "has_ct": "CT",
        "has_pet": "PET",
        "has_wsi": "WSI",
        "has_omics": "Omics",
        "has_clinical": "Clinical",
        "has_report": "Report",
    }

    combos = []
    for _, row in df.iterrows():
        active = [col_to_label[c] for c in modality_cols if row[c]]
        if len(active) < 2:
            continue  # chỉ quan tâm paired/multimodal
        combo_str = "+".join(sorted(active))
        combos.append((combo_str, row["Subjects"]))

    if not combos:
        return pd.DataFrame(columns=["Combination", "TotalSubjects"])

    combo_df = pd.DataFrame(combos, columns=["Combination", "Subjects"])
    agg = combo_df.groupby("Combination", as_index=False)["Subjects"].sum()
    # sort by number of subjects desc
    agg = agg.sort_values("Subjects", ascending=False)
    return agg


def plot_cohort_counts(agg: pd.DataFrame, out_path: Path):
    if agg.empty:
        print("No multimodal combinations found. Nothing to plot.")
        return

    combos = agg["Combination"].tolist()
    counts = agg["Subjects"].tolist()

    plt.figure(figsize=(max(8, 0.6 * len(combos)), 5))
    bars = plt.bar(range(len(combos)), counts)

    plt.xticks(range(len(combos)), combos, rotation=45, ha="right")
    plt.ylabel("Total subjects")
    plt.xlabel("Modality combination")
    plt.title("Cohort size per multimodal combination")

    # label value trên đầu cột
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(counts[i]),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def main():
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "data" / "datasets_master.csv"
    out_path = repo_root / "images" / "multimodal_cohort_counts.png"

    print(f"Reading: {csv_path}")
    df = load_master_csv(csv_path)
    df, modality_cols = add_modality_flags(df)

    agg = aggregate_by_combination(df, modality_cols)

    print("Multimodal combinations by total subjects:")
    print(agg.to_string(index=False))

    print(f"Saving bar plot to: {out_path}")
    plot_cohort_counts(agg, out_path)
    print("Done.")


if __name__ == "__main__":
    main()
