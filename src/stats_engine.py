"""
Statistical engine for distributions, sampling analysis, and Central Limit Theorem intuition.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def compute_comprehensive_summary(
    df: pd.DataFrame, columns: List[str] = None
) -> pd.DataFrame:
    """Compute rich univariate summary statistics for numerical columns.

    Includes measures of central tendency, dispersion, shape (skewness, kurtosis),
    and standard error of the mean (SEM).
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if "student_id" in columns:
            columns.remove("student_id")

    summary_rows = []
    n = len(df)

    for col in columns:
        series = df[col].dropna()
        q25 = float(series.quantile(0.25))
        q75 = float(series.quantile(0.75))
        iqr = q75 - q25
        mean_val = float(series.mean())
        std_val = float(series.std(ddof=1))
        sem_val = float(std_val / np.sqrt(len(series))) if len(series) > 0 else 0.0

        summary_rows.append({
            "feature": col,
            "count": int(len(series)),
            "mean": round(mean_val, 4),
            "std": round(std_val, 4),
            "variance": round(float(series.var(ddof=1)), 4),
            "sem": round(sem_val, 4),
            "min": round(float(series.min()), 4),
            "25%": round(q25, 4),
            "median": round(float(series.median()), 4),
            "75%": round(q75, 4),
            "max": round(float(series.max()), 4),
            "iqr": round(iqr, 4),
            "skewness": round(float(series.skew()), 4),
            "kurtosis": round(float(series.kurtosis()), 4),
        })

    return pd.DataFrame(summary_rows).set_index("feature")


def simulate_sampling_differences(
    df: pd.DataFrame,
    feature: str = "total_score",
    sample_sizes: List[int] = None,
    random_state: int = 42,
) -> pd.DataFrame:
    """Demonstrate how sample size dictates estimation precision and sampling error.

    Compares sample statistics against the true population parameter (N=1,000,000).
    """
    if sample_sizes is None:
        sample_sizes = [30, 100, 500, 1000, 10000, 50000]

    pop_mean = float(df[feature].mean())
    pop_std = float(df[feature].std(ddof=0))
    pop_corr = float(df["weekly_self_study_hours"].corr(df["total_score"]))

    records = [{
        "sample_size": f"Population (N={len(df):,})",
        "sample_mean": round(pop_mean, 4),
        "mean_error": 0.0000,
        "sample_std": round(pop_std, 4),
        "ci_95_lower": round(pop_mean, 4),
        "ci_95_upper": round(pop_mean, 4),
        "study_score_corr": round(pop_corr, 4),
        "corr_error": 0.0000,
    }]

    rng = np.random.RandomState(random_state)
    for n in sample_sizes:
        indices = rng.choice(len(df), size=n, replace=False)
        sample = df.iloc[indices]
        s_mean = float(sample[feature].mean())
        s_std = float(sample[feature].std(ddof=1))
        sem = s_std / np.sqrt(n)

        # 95% Confidence Interval using t-distribution
        t_crit = stats.t.ppf(0.975, df=n - 1)
        ci_lower = s_mean - t_crit * sem
        ci_upper = s_mean + t_crit * sem

        s_corr = float(sample["weekly_self_study_hours"].corr(sample["total_score"]))

        records.append({
            "sample_size": f"N = {n:,}",
            "sample_mean": round(s_mean, 4),
            "mean_error": round(abs(s_mean - pop_mean), 4),
            "sample_std": round(s_std, 4),
            "ci_95_lower": round(ci_lower, 4),
            "ci_95_upper": round(ci_upper, 4),
            "study_score_corr": round(s_corr, 4),
            "corr_error": round(abs(s_corr - pop_corr), 4),
        })

    return pd.DataFrame(records)


def simulate_central_limit_theorem(
    df: pd.DataFrame,
    feature: str = "total_score",
    sample_sizes: List[int] = None,
    num_trials: int = 1000,
    random_state: int = 42,
) -> Tuple[Dict[int, np.ndarray], pd.DataFrame]:
    """Simulate repeated sampling to demonstrate the Central Limit Theorem.

    Shows that the distribution of sample means converges to Normal(mu, sigma^2 / N),
    even when the underlying population exhibits skewness and censoring.
    """
    if sample_sizes is None:
        sample_sizes = [30, 100, 500]

    pop_mean = float(df[feature].mean())
    pop_std = float(df[feature].std(ddof=0))
    rng = np.random.RandomState(random_state)

    values = df[feature].to_numpy()
    results = {}
    clt_summary = []

    for n in sample_sizes:
        # Draw num_trials samples of size n
        sample_indices = rng.choice(len(values), size=(num_trials, n), replace=True)
        sample_means = values[sample_indices].mean(axis=1)
        results[n] = sample_means

        empirical_sem = float(np.std(sample_means, ddof=1))
        theoretical_sem = float(pop_std / np.sqrt(n))
        skew = float(stats.skew(sample_means))
        kurt = float(stats.kurtosis(sample_means))

        clt_summary.append({
            "sample_size": n,
            "pop_mean": round(pop_mean, 4),
            "mean_of_sample_means": round(float(np.mean(sample_means)), 4),
            "empirical_sem": round(empirical_sem, 4),
            "theoretical_sem": round(theoretical_sem, 4),
            "sem_difference": round(abs(empirical_sem - theoretical_sem), 4),
            "sampling_dist_skew": round(skew, 4),
            "sampling_dist_kurt": round(kurt, 4),
        })

    return results, pd.DataFrame(clt_summary)


def compute_correlation_matrices(
    df: pd.DataFrame, columns: List[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compute Pearson correlation, Spearman rank correlation, and sample covariance matrices."""
    if columns is None:
        columns = [
            "weekly_self_study_hours",
            "attendance_percentage",
            "class_participation",
            "total_score",
        ]

    subset = df[columns]
    pearson = subset.corr(method="pearson").round(4)
    spearman = subset.corr(method="spearman").round(4)
    covariance = subset.cov().round(4)

    return pearson, spearman, covariance
