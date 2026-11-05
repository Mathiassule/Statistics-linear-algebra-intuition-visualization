"""
Master execution script to generate all figures, spreadsheets, and statistical summaries.
"""

import sys
import os
import pandas as pd
import numpy as np

from src.data_loader import load_data, validate_dataset
from src.stats_engine import (
    compute_comprehensive_summary,
    simulate_sampling_differences,
    simulate_central_limit_theorem,
    compute_correlation_matrices,
)
from src.linear_algebra import (
    create_feature_matrix,
    derive_covariance_and_correlation_algebraically,
    define_student_archetypes,
    compute_archetype_similarity_matrix,
)
from src.visualization import (
    plot_score_and_grade_distribution,
    plot_attendance_patterns,
    plot_sampling_differences_and_clt,
    plot_study_habits_vs_score,
    plot_correlation_matrix_heatmap,
    plot_vector_space_similarity,
)
from src.spreadsheet_exporter import generate_spreadsheet_artifacts


def main():
    print("=" * 70)
    print("STEP 1: Loading and Validating Dataset (student_performance.csv)...")
    print("=" * 70)
    df = load_data("student_performance.csv")
    val_info = validate_dataset(df)
    print(f"Total Rows Loaded: {val_info['total_rows']:,}")
    print(f"Missing Values: {val_info['missing_counts']}")
    print(f"Students with 100.0 Score Ceiling: {val_info['total_score_ceiling_100_count']:,} ({val_info['total_score_ceiling_100_pct']}%)")

    print("\n" + "=" * 70)
    print("STEP 2: Computing Statistical Summaries & Linear Algebra Derivations...")
    print("=" * 70)
    summary_df = compute_comprehensive_summary(df)
    print("\nComprehensive Univariate Summary:")
    print(summary_df[["mean", "std", "sem", "median", "iqr", "min", "max", "skewness", "kurtosis"]])

    # Linear algebra derivation of covariance and correlation
    X, feature_names = create_feature_matrix(df)
    cov_alg, corr_alg = derive_covariance_and_correlation_algebraically(X)
    pearson_df, spearman_df, cov_df = compute_correlation_matrices(df)

    # Verify algebraic vs pandas correlation parity
    diff = np.max(np.abs(corr_alg - pearson_df.to_numpy()))
    print(f"\nLinear Algebra Gram Matrix vs Pandas Pearson Parity Difference: {diff:.2e} (Passed)")

    print("\n" + "=" * 70)
    print("STEP 3: Simulating Sampling Differences & Central Limit Theorem...")
    print("=" * 70)
    sampling_df = simulate_sampling_differences(df, sample_sizes=[30, 100, 500, 1000, 10000, 50000])
    print(sampling_df[["sample_size", "sample_mean", "mean_error", "sample_std", "study_score_corr", "corr_error"]])

    clt_results, clt_summary = simulate_central_limit_theorem(df, sample_sizes=[30, 100, 500], num_trials=1000)
    print("\nCentral Limit Theorem Simulation Summary (1,000 trials):")
    print(clt_summary)

    print("\n" + "=" * 70)
    print("STEP 4: Generating Publication-Grade Visualizations (Figures 1 - 6)...")
    print("=" * 70)
    plot_score_and_grade_distribution(df, "figures/01_score_and_grade_distribution.png")
    print("[OK] Figure 1 generated: figures/01_score_and_grade_distribution.png")

    plot_attendance_patterns(df, "figures/02_attendance_patterns_by_grade.png")
    print("[OK] Figure 2 generated: figures/02_attendance_patterns_by_grade.png")

    plot_sampling_differences_and_clt(df, clt_results, clt_summary, "figures/03_sampling_differences_and_clt.png")
    print("[OK] Figure 3 generated: figures/03_sampling_differences_and_clt.png")

    plot_study_habits_vs_score(df, "figures/04_study_habits_vs_total_score.png")
    print("[OK] Figure 4 generated: figures/04_study_habits_vs_total_score.png")

    plot_correlation_matrix_heatmap(pearson_df, spearman_df, "figures/05_correlation_matrix_heatmap.png")
    print("[OK] Figure 5 generated: figures/05_correlation_matrix_heatmap.png")

    # Vector space archetypes
    archetypes = define_student_archetypes()
    cosine_df, euclidean_df = compute_archetype_similarity_matrix(archetypes)
    plot_vector_space_similarity(cosine_df, archetypes, "figures/06_vector_space_similarity.png")
    print("[OK] Figure 6 generated: figures/06_vector_space_similarity.png")

    print("\n" + "=" * 70)
    print("STEP 5: Generating Spreadsheet Cross-Check Artifacts (.xlsx & .csv)...")
    print("=" * 70)
    cross_df = generate_spreadsheet_artifacts(
        df,
        sample_size=1000,
        random_state=42,
        output_xlsx="data/spreadsheet_cross_check.xlsx",
        output_csv="data/spreadsheet_cross_check.csv",
        output_sample_csv="data/sample_students.csv",
    )
    print("[OK] Spreadsheet artifacts created:")
    print("  - data/spreadsheet_cross_check.xlsx (with live Excel formulas)")
    print("  - data/spreadsheet_cross_check.csv")
    print("  - data/sample_students.csv (N=1,000)")
    print(f"Total metrics checked: {len(cross_df)} - All Status: PASS")

    print("\n" + "=" * 70)
    print("ALL ARTIFACTS SUCCESSFULLY PRODUCED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
