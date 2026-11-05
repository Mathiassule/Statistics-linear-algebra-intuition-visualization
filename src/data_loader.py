"""
Data loading and validation module for the Student Performance dataset.
"""

import os
from typing import Optional, Tuple
import pandas as pd
import numpy as np


FEATURE_COLUMNS = [
    "weekly_self_study_hours",
    "attendance_percentage",
    "class_participation",
    "total_score",
]

ALL_COLUMNS = ["student_id"] + FEATURE_COLUMNS + ["grade"]

GRADE_ORDER = ["A", "B", "C", "D", "F"]


def load_data(
    filepath: str = "student_performance.csv",
    nrows: Optional[int] = None,
) -> pd.DataFrame:
    """Load the student performance dataset from CSV.

    Args:
        filepath: Path to the student_performance.csv file.
        nrows: Optional number of rows to load (useful for quick previews/tests).

    Returns:
        pd.DataFrame containing the student records.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")

    df = pd.read_csv(filepath, nrows=nrows)
    # Ensure correct categorical ordering for grade
    if "grade" in df.columns:
        df["grade"] = pd.Categorical(df["grade"], categories=GRADE_ORDER, ordered=True)

    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """Perform data quality, schema, and boundary validation on the dataset.

    Returns:
        A dictionary with validation summary results.
    """
    missing_counts = df.isnull().sum().to_dict()
    total_rows = len(df)
    duplicates = df["student_id"].duplicated().sum() if "student_id" in df.columns else 0

    ranges = {}
    for col in FEATURE_COLUMNS:
        if col in df.columns:
            ranges[col] = {
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "mean": float(df[col].mean()),
            }

    ceiling_count = int((df["total_score"] == 100.0).sum()) if "total_score" in df.columns else 0
    ceiling_pct = float(ceiling_count / total_rows * 100.0) if total_rows > 0 else 0.0

    return {
        "total_rows": total_rows,
        "columns": list(df.columns),
        "missing_counts": missing_counts,
        "duplicate_ids": duplicates,
        "feature_ranges": ranges,
        "total_score_ceiling_100_count": ceiling_count,
        "total_score_ceiling_100_pct": round(ceiling_pct, 2),
    }


def get_stratified_or_random_sample(
    df: pd.DataFrame, n: int = 1000, random_state: int = 42
) -> pd.DataFrame:
    """Return a reproducible random sample from the dataset.

    Args:
        df: Input DataFrame.
        n: Sample size.
        random_state: Seed for reproducibility.

    Returns:
        Sampled pd.DataFrame.
    """
    if len(df) <= n:
        return df.copy()
    return df.sample(n=n, random_state=random_state).sort_values("student_id").reset_index(drop=True)
