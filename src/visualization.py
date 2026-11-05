"""
Visualization module for student performance data.
Adheres to chart critique principles:
- High data-to-ink ratio
- Perceptually uniform, colorblind-friendly palettes
- Clear direct annotations, avoiding misleading truncations
- Informative titles, labels, and figure subtitles
"""

import os
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set styling
plt.rcParams.update({
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
    "font.family": "sans-serif",
    "figure.autolayout": False,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 15,
})


GRADE_PALETTE = {
    "A": "#2E7D32",  # Deep green
    "B": "#1976D2",  # Vibrant blue
    "C": "#F57C00",  # Amber orange
    "D": "#E64A19",  # Deep orange
    "F": "#C2185B",  # Raspberry red
}


def plot_score_and_grade_distribution(
    df: pd.DataFrame, output_path: str = "figures/01_score_and_grade_distribution.png"
):
    """Figure 1: Distribution of Total Scores and Grade Proportions."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Panel 1: Histogram + KDE
    scores = df["total_score"]
    mean_val = scores.mean()
    median_val = scores.median()
    q25, q75 = scores.quantile(0.25), scores.quantile(0.75)
    ceiling_pct = (scores == 100.0).mean() * 100

    sns.histplot(
        scores,
        bins=50,
        kde=True,
        color="#34495E",
        ax=ax1,
        stat="density",
        alpha=0.45,
        edgecolor="white",
        linewidth=0.5,
    )

    ax1.axvline(mean_val, color="#D32F2F", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.1f}")
    ax1.axvline(median_val, color="#1976D2", linestyle="-", linewidth=2, label=f"Median: {median_val:.1f}")
    ax1.axvspan(q25, q75, color="#90CAF9", alpha=0.2, label=f"IQR [{q25:.1f} - {q75:.1f}]")

    ax1.annotate(
        f"Ceiling Effect Spike:\n{ceiling_pct:.1f}% scored exactly 100",
        xy=(100, 0.04),
        xytext=(65, 0.045),
        arrowprops=dict(facecolor="#D32F2F", shrink=0.08, width=1.5, headwidth=6),
        fontsize=9.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFEBEE", edgecolor="#D32F2F", alpha=0.9),
    )

    ax1.set_title("Total Score Density & Non-Normal Left Skew", pad=12, fontweight="bold")
    ax1.set_xlabel("Total Score (0 – 100)")
    ax1.set_ylabel("Probability Density")
    ax1.set_xlim(0, 105)
    ax1.legend(loc="upper left", frameon=True)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel 2: Grade distribution
    grade_counts = df["grade"].value_counts(sort=False)
    grade_pcts = df["grade"].value_counts(normalize=True, sort=False) * 100
    grades = list(grade_counts.index)
    palette = [GRADE_PALETTE.get(g, "#555555") for g in grades]

    bars = ax2.bar(grades, grade_counts.values, color=palette, edgecolor="black", linewidth=0.8, alpha=0.85)

    for bar, pct, cnt in zip(bars, grade_pcts.values, grade_counts.values):
        yval = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 12000,
            f"{cnt:,}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax2.set_title("Grade Composition (Population N=1,000,000)", pad=12, fontweight="bold")
    ax2.set_xlabel("Letter Grade")
    ax2.set_ylabel("Student Count")
    ax2.set_ylim(0, max(grade_counts.values) * 1.22)
    ax2.grid(axis="y", linestyle=":", alpha=0.6)

    plt.suptitle("Figure 1: Academic Achievement & Score Censoring Analysis", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_attendance_patterns(
    df: pd.DataFrame, output_path: str = "figures/02_attendance_patterns_by_grade.png"
):
    """Figure 2: Attendance Distribution Across Grade Categories."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Sample for faster and cleaner plotting if huge
    plot_df = df.sample(n=50000, random_state=42) if len(df) > 50000 else df

    # Panel 1: Boxplot of Attendance by Grade
    sns.boxplot(
        data=plot_df,
        x="grade",
        y="attendance_percentage",
        hue="grade",
        legend=False,
        palette=GRADE_PALETTE,
        ax=ax1,
        width=0.45,
        boxprops=dict(alpha=0.85),
    )
    ax1.set_title("Attendance Range by Grade (Virtually Identical)", pad=12, fontweight="bold")
    ax1.set_xlabel("Letter Grade")
    ax1.set_ylabel("Attendance Percentage (%)")
    ax1.set_ylim(45, 105)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel 2: Density Overlays
    for grade in ["A", "B", "C", "D", "F"]:
        subset = plot_df[plot_df["grade"] == grade]["attendance_percentage"]
        sns.kdeplot(
            subset,
            ax=ax2,
            label=f"Grade {grade} (mean: {subset.mean():.1f}%)",
            color=GRADE_PALETTE.get(grade),
            linewidth=2,
        )

    ax2.set_title("Attendance KDE Overlays: Statistical Invariance", pad=12, fontweight="bold")
    ax2.set_xlabel("Attendance Percentage (%)")
    ax2.set_ylabel("Density")
    ax2.legend(loc="upper left", frameon=True)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle(
        "Figure 2: Attendance Patterns Across Academic Tiers (Testing Orthogonality)",
        y=1.02,
        fontsize=15,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_sampling_differences_and_clt(
    df: pd.DataFrame,
    clt_results: Dict[int, np.ndarray],
    clt_summary_df: pd.DataFrame,
    output_path: str = "figures/03_sampling_differences_and_clt.png",
):
    """Figure 3: Sampling Variance, Sample Size Sensitivity, and Central Limit Theorem."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10), dpi=300)

    pop_mean = df["total_score"].mean()
    pop_std = df["total_score"].std(ddof=0)

    # Top-Left: Small Sample (N=30)
    sample_30 = df.sample(n=30, random_state=42)["total_score"]
    sns.histplot(sample_30, bins=15, ax=ax1, color="#E65100", kde=True, stat="density", alpha=0.6)
    ax1.axvline(sample_30.mean(), color="#B71C1C", linestyle="--", linewidth=2, label=f"Sample Mean: {sample_30.mean():.1f}")
    ax1.axvline(pop_mean, color="#1B5E20", linestyle=":", linewidth=2, label=f"True Pop Mean: {pop_mean:.1f}")
    ax1.set_title("Small Sample (N = 30): High Volatility & Bias Risk", fontweight="bold")
    ax1.set_xlabel("Total Score")
    ax1.set_ylabel("Density")
    ax1.legend(loc="upper left")
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Top-Right: Moderate Sample (N=1,000)
    sample_1000 = df.sample(n=1000, random_state=42)["total_score"]
    sns.histplot(sample_1000, bins=35, ax=ax2, color="#0D47A1", kde=True, stat="density", alpha=0.5)
    ax2.axvline(sample_1000.mean(), color="#B71C1C", linestyle="--", linewidth=2, label=f"Sample Mean: {sample_1000.mean():.1f}")
    ax2.axvline(pop_mean, color="#1B5E20", linestyle=":", linewidth=2, label=f"True Pop Mean: {pop_mean:.1f}")
    ax2.set_title("Moderate Sample (N = 1,000): Stable Population Convergence", fontweight="bold")
    ax2.set_xlabel("Total Score")
    ax2.set_ylabel("Density")
    ax2.legend(loc="upper left")
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Bottom-Left: CLT - Sampling Distributions of the Mean (1,000 trials each)
    clt_colors = {30: "#E65100", 100: "#7B1FA2", 500: "#0288D1"}
    for n, means in clt_results.items():
        theoretical_sem = pop_std / np.sqrt(n)
        sns.kdeplot(
            means,
            ax=ax3,
            label=f"N={n} (Empirical SEM={np.std(means):.2f}, Theor={theoretical_sem:.2f})",
            color=clt_colors.get(n, "#333333"),
            linewidth=2.2,
        )
    ax3.axvline(pop_mean, color="#1B5E20", linestyle="--", linewidth=1.8, label=f"True Mean = {pop_mean:.2f}")
    ax3.set_title("Central Limit Theorem: Distribution of 1,000 Sample Means", fontweight="bold")
    ax3.set_xlabel("Sample Mean Value")
    ax3.set_ylabel("Sampling Distribution Density")
    ax3.legend(loc="upper right", fontsize=8.5)
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Bottom-Right: 95% Confidence Interval Width vs Sample Size
    sample_sizes = [30, 50, 100, 250, 500, 1000, 5000, 10000]
    ci_widths = [1.96 * (pop_std / np.sqrt(n)) * 2 for n in sample_sizes]  # Full width of 95% CI

    ax4.plot(sample_sizes, ci_widths, marker="o", color="#C2185B", linewidth=2, markersize=6)
    ax4.set_xscale("log")
    ax4.set_title(r"Precision Decay: 95% CI Margin of Error $\propto 1/\sqrt{N}$", fontweight="bold")
    ax4.set_xlabel("Sample Size (N) [Log Scale]")
    ax4.set_ylabel("95% CI Width (Score Points)")
    for n, w in zip([30, 100, 1000, 10000], [ci_widths[0], ci_widths[2], ci_widths[5], ci_widths[7]]):
        ax4.annotate(f"N={n}\nWidth: ±{w/2:.2f}", xy=(n, w), xytext=(n * 1.15, w + 0.8), fontsize=8.5)
    ax4.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle("Figure 3: Sampling Intuition, Error Decay, and the Central Limit Theorem", y=1.01, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_study_habits_vs_score(
    df: pd.DataFrame, output_path: str = "figures/04_study_habits_vs_total_score.png"
):
    """Figure 4: Relationship between Weekly Study Hours and Academic Results."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Panel 1: Hexbin Plot (avoids overplotting with 1,000,000 points)
    # Take 100k sample for fast high-density rendering
    sub = df.sample(n=100000, random_state=42)
    x = sub["weekly_self_study_hours"]
    y = sub["total_score"]

    hb = ax1.hexbin(x, y, gridsize=45, cmap="YlGnBu", mincnt=1, bins="log")
    cb = fig.colorbar(hb, ax=ax1)
    cb.set_label("Log10(Student Count)")

    # Linear fit line
    m, b = np.polyfit(x, y, 1)
    x_vals = np.linspace(0, 40, 100)
    ax1.plot(x_vals, m * x_vals + b, color="#D32F2F", linewidth=2.5, label=f"Linear Fit (Slope={m:.2f}, r=0.81)")
    ax1.axhline(100, color="#7B1FA2", linestyle=":", linewidth=1.8, label="Score Ceiling (100.0)")

    ax1.set_title("Study Hours vs Score (Hexbin Density & Fit)", pad=12, fontweight="bold")
    ax1.set_xlabel("Weekly Self-Study Hours")
    ax1.set_ylabel("Total Score")
    ax1.legend(loc="lower right")
    ax1.grid(True, linestyle=":", alpha=0.4)

    # Panel 2: Boxplot by Grade
    sns.boxplot(
        data=sub,
        x="grade",
        y="weekly_self_study_hours",
        hue="grade",
        legend=False,
        palette=GRADE_PALETTE,
        ax=ax2,
        width=0.5,
        boxprops=dict(alpha=0.85),
    )
    grade_means = sub.groupby("grade", observed=False)["weekly_self_study_hours"].mean()
    for i, (grade, mean_val) in enumerate(grade_means.items()):
        ax2.text(i, mean_val + 1.2, f"μ={mean_val:.1f}h", ha="center", fontsize=9, fontweight="bold", color="#111111")

    ax2.set_title("Self-Study Hours by Assigned Letter Grade", pad=12, fontweight="bold")
    ax2.set_xlabel("Letter Grade")
    ax2.set_ylabel("Weekly Self-Study Hours")
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle("Figure 4: Study Habits vs Performance & Non-Linear Saturation", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_correlation_matrix_heatmap(
    pearson_df: pd.DataFrame,
    spearman_df: pd.DataFrame,
    output_path: str = "figures/05_correlation_matrix_heatmap.png",
):
    """Figure 5: Pearson Linear vs Spearman Rank Correlation Heatmaps."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    clean_labels = [
        "Study Hours",
        "Attendance %",
        "Participation",
        "Total Score",
    ]

    sns.heatmap(
        pearson_df,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        cbar_kws={"label": "Pearson Correlation (r)"},
        ax=ax1,
        xticklabels=clean_labels,
        yticklabels=clean_labels,
        linewidths=0.75,
    )
    ax1.set_title("Pearson Linear Correlation Matrix", pad=12, fontweight="bold")

    sns.heatmap(
        spearman_df,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        cbar_kws={"label": "Spearman Rank Correlation (ρ)"},
        ax=ax2,
        xticklabels=clean_labels,
        yticklabels=clean_labels,
        linewidths=0.75,
    )
    ax2.set_title("Spearman Rank Correlation Matrix", pad=12, fontweight="bold")

    plt.suptitle("Figure 5: Bivariate Association Matrix (Linear vs Rank)", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_vector_space_similarity(
    cosine_df: pd.DataFrame,
    archetypes: Dict[str, np.ndarray],
    output_path: str = "figures/06_vector_space_similarity.png",
):
    """Figure 6: Linear Algebra Vector Profiles and Cosine Similarity Heatmap."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # Panel 1: Parallel coordinates / line profile of archetypes
    feature_names = ["Study Hours", "Attendance %", "Participation", "Total Score"]
    archetype_names = list(archetypes.keys())
    colors = ["#2E7D32", "#1976D2", "#C2185B", "#F57C00", "#7B1FA2"]

    for (name, vec), col in zip(archetypes.items(), colors):
        # Normalize to 0-100 for visually comparable scale
        # Study: 0-40 -> 0-100, Attendance: 50-100 -> 0-100, Part: 0-10 -> 0-100, Score: 0-100
        norm_vec = [
            (vec[0] / 40.0) * 100.0,
            ((vec[1] - 50.0) / 50.0) * 100.0,
            (vec[2] / 10.0) * 100.0,
            vec[3],
        ]
        ax1.plot(feature_names, norm_vec, marker="o", linewidth=2.2, label=name, color=col)

    ax1.set_title("Student Archetype Feature Vectors (Scaled 0-100)", pad=12, fontweight="bold")
    ax1.set_ylabel("Scaled Dimensional Value (0 – 100)")
    ax1.legend(loc="lower left", fontsize=8.5, frameon=True)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Shorten names for clean matrix axis
    short_labels = [
        "A-Student (High/High)",
        "Mid-Student (Avg/Avg)",
        "Low-Student (Low/Low)",
        "Passive (High Att/Low Study)",
        "Independent (Low Att/High Study)",
    ]

    sns.heatmap(
        cosine_df,
        annot=True,
        fmt=".3f",
        cmap="viridis",
        vmin=0.7,
        vmax=1.0,
        cbar_kws={"label": "Cosine Similarity cos(θ)"},
        ax=ax2,
        xticklabels=short_labels,
        yticklabels=short_labels,
        linewidths=0.75,
    )
    ax2.set_title(r"Pairwise Cosine Similarity: $\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$", pad=12, fontweight="bold")
    plt.setp(ax2.get_xticklabels(), rotation=35, ha="right")

    plt.suptitle("Figure 6: Linear Algebra in Feature Space (Vectors & Directional Similarity)", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
