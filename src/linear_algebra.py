"""
Linear Algebra Intuition Module: Vectors, Matrices, and Similarity.

Develops applied intuition for:
- Data as row vectors in R^d and design matrices X in R^(n x d)
- Centering, Gram matrices, and deriving covariance/correlation via matrix multiplication
- Vector dot products, Euclidean norms, and Cosine similarity
- Feature scale sensitivity and standardization
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


FEATURE_COLS = [
    "weekly_self_study_hours",
    "attendance_percentage",
    "class_participation",
    "total_score",
]


def create_feature_matrix(
    df: pd.DataFrame, columns: List[str] = None
) -> Tuple[np.ndarray, List[str]]:
    """Extract the numeric design matrix X in R^(n x d)."""
    if columns is None:
        columns = FEATURE_COLS
    return df[columns].to_numpy(dtype=float), columns


def derive_covariance_and_correlation_algebraically(
    X: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Derive sample covariance and Pearson correlation purely using matrix algebra.

    Mathematics:
        1. Mean vector: mu = (1/n) * X^T * 1
        2. Centered matrix: X_tilde = X - 1 * mu^T
        3. Covariance matrix: S = (1 / (n - 1)) * X_tilde^T * X_tilde
        4. Standardized matrix: Z = X_tilde * D^(-1), where D_jj = sqrt(S_jj)
        5. Correlation matrix: R = (1 / (n - 1)) * Z^T * Z
    """
    n, d = X.shape

    # 1. Mean vector
    mu = np.mean(X, axis=0)

    # 2. Centered matrix
    X_tilde = X - mu

    # 3. Covariance matrix via matrix inner product
    cov_matrix = (X_tilde.T @ X_tilde) / (n - 1)

    # 4. Standard deviations and diagonal scaling matrix D^(-1)
    std_devs = np.sqrt(np.diag(cov_matrix))
    D_inv = np.diag(1.0 / std_devs)

    # 5. Standardized matrix Z
    Z = X_tilde @ D_inv

    # 6. Correlation matrix via Gram matrix of standardized features
    corr_matrix = (Z.T @ Z) / (n - 1)

    return cov_matrix, corr_matrix


def compute_vector_metrics(
    u: np.ndarray, v: np.ndarray
) -> Dict[str, float]:
    """Compute vector dot product, Euclidean distance, L2 norms, and Cosine similarity.

    Formula:
        Cosine_Similarity(u, v) = (u . v) / (||u||_2 * ||v||_2)
    """
    dot_product = float(np.dot(u, v))
    norm_u = float(np.linalg.norm(u))
    norm_v = float(np.linalg.norm(v))
    euclidean_dist = float(np.linalg.norm(u - v))

    if norm_u == 0.0 or norm_v == 0.0:
        cosine_sim = 0.0
    else:
        cosine_sim = float(dot_product / (norm_u * norm_v))

    # Angle in radians and degrees
    clamped_cos = max(-1.0, min(1.0, cosine_sim))
    angle_rad = float(np.arccos(clamped_cos))
    angle_deg = float(np.degrees(angle_rad))

    return {
        "dot_product": round(dot_product, 4),
        "norm_u": round(norm_u, 4),
        "norm_v": round(norm_v, 4),
        "euclidean_distance": round(euclidean_dist, 4),
        "cosine_similarity": round(cosine_sim, 4),
        "angle_degrees": round(angle_deg, 2),
    }


def define_student_archetypes() -> Dict[str, np.ndarray]:
    """Define canonical student behavioral vectors in R^4.

    Features: [weekly_self_study_hours, attendance_percentage, class_participation, total_score]
    """
    archetypes = {
        "High Study / High Score (A-Student)": np.array([25.0, 95.0, 8.5, 98.0]),
        "Average Effort / Mid Score (B/C-Student)": np.array([12.0, 85.0, 6.0, 75.0]),
        "Low Effort / Low Score (D/F-Student)": np.array([3.0, 65.0, 3.0, 42.0]),
        "High Attendance / Low Study (Passive)": np.array([3.0, 98.0, 7.5, 45.0]),
        "Independent High Studier (Low Attend)": np.array([26.0, 55.0, 4.0, 97.0]),
    }
    return archetypes


def compute_archetype_similarity_matrix(
    archetypes: Dict[str, np.ndarray], standardize_with: Tuple[np.ndarray, np.ndarray] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute pairwise Cosine Similarity and Euclidean Distance matrices across archetypes.

    Optionally standardizes vectors first using (mean, std) from the population.
    """
    names = list(archetypes.keys())
    k = len(names)
    matrix = np.array([archetypes[n] for n in names])

    if standardize_with is not None:
        mean_vec, std_vec = standardize_with
        matrix = (matrix - mean_vec) / std_vec

    cosine_mat = np.zeros((k, k))
    euclidean_mat = np.zeros((k, k))

    for i in range(k):
        for j in range(k):
            u = matrix[i]
            v = matrix[j]
            metrics = compute_vector_metrics(u, v)
            cosine_mat[i, j] = metrics["cosine_similarity"]
            euclidean_mat[i, j] = metrics["euclidean_distance"]

    df_cosine = pd.DataFrame(cosine_mat, index=names, columns=names).round(4)
    df_euclidean = pd.DataFrame(euclidean_mat, index=names, columns=names).round(4)

    return df_cosine, df_euclidean
