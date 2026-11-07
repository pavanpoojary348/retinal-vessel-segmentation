"""
Retinal Blood Vessel Segmentation - Evaluation Metrics Module
============================================================
Fundamental of Image Processing (FIP) Course Project

Implements all required performance metrics:
1. Dice Coefficient (F1-score)
2. IoU (Intersection over Union / Jaccard Index)
3. Sensitivity / Recall (True Positive Rate)
4. Specificity (True Negative Rate)
5. Accuracy
6. AUC-ROC (Area Under the Receiver Operating Characteristic Curve)
7. Precision (Positive Predictive Value)

All metrics are evaluated strictly INSIDE the Field of View (FOV) mask,
adhering to DRIVE benchmark standards.
"""

import numpy as np
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc


def compute_all_metrics(
    y_true: np.ndarray,
    y_pred_probs: np.ndarray,
    fov_mask: np.ndarray = None,
    threshold: float = 0.5
) -> dict:
    """
    Compute comprehensive segmentation evaluation metrics.

    Parameters:
    - y_true: Ground truth binary mask (0 or 1, or 0 to 255)
    - y_pred_probs: Predicted probability map [0.0, 1.0]
    - fov_mask: Field of view mask (evaluates only valid retinal pixels)
    - threshold: Binary classification threshold (default 0.5)

    Returns:
    - Dictionary containing Dice, IoU, Sensitivity, Specificity, Accuracy, AUC, Precision, Recall
    """
    # Flatten arrays
    y_t = (y_true > 0).astype(np.uint8).ravel()
    y_p = y_pred_probs.ravel()

    # Filter to only FOV pixels if FOV mask is provided
    if fov_mask is not None:
        valid_indices = (fov_mask.ravel() > 0)
        y_t = y_t[valid_indices]
        y_p = y_p[valid_indices]

    # Binary prediction at specified threshold
    y_pred_bin = (y_p >= threshold).astype(np.uint8)

    # Confusion matrix components
    tp = np.sum((y_pred_bin == 1) & (y_t == 1))
    tn = np.sum((y_pred_bin == 0) & (y_t == 0))
    fp = np.sum((y_pred_bin == 1) & (y_t == 0))
    fn = np.sum((y_pred_bin == 0) & (y_t == 1))

    eps = 1e-7

    # Metric calculations
    sensitivity = tp / (tp + fn + eps)      # Recall
    recall = sensitivity
    specificity = tn / (tn + fp + eps)
    precision = tp / (tp + fp + eps)
    accuracy = (tp + tn) / (tp + tn + fp + fn + eps)
    dice = (2.0 * tp) / (2.0 * tp + fp + fn + eps)   # F1-Score
    iou = tp / (tp + fp + fn + eps)                  # Jaccard

    # Area Under ROC Curve
    try:
        if len(np.unique(y_t)) > 1:
            roc_auc = float(roc_auc_score(y_t, y_p))
        else:
            roc_auc = 0.5
    except Exception:
        roc_auc = 0.5

    # Area Under Precision-Recall Curve
    try:
        p_vals, r_vals, _ = precision_recall_curve(y_t, y_p)
        pr_auc = float(auc(r_vals, p_vals))
    except Exception:
        pr_auc = 0.0

    return {
        'Dice': float(dice),
        'IoU': float(iou),
        'Sensitivity': float(sensitivity),
        'Recall': float(recall),
        'Specificity': float(specificity),
        'Accuracy': float(accuracy),
        'AUC_ROC': float(roc_auc),
        'AUC_PR': float(pr_auc),
        'Precision': float(precision),
        'TP': int(tp),
        'TN': int(tn),
        'FP': int(fp),
        'FN': int(fn)
    }


def format_metrics_table(metrics_dict: dict, model_name: str = 'Model') -> str:
    """Format metrics dictionary into a clean markdown table."""
    headers = ['Model', 'Dice (F1)', 'IoU', 'Sensitivity (Recall)', 'Specificity', 'Accuracy', 'AUC-ROC', 'Precision']
    row = [
        model_name,
        f"{metrics_dict.get('Dice', 0):.4f}",
        f"{metrics_dict.get('IoU', 0):.4f}",
        f"{metrics_dict.get('Sensitivity', 0):.4f}",
        f"{metrics_dict.get('Specificity', 0):.4f}",
        f"{metrics_dict.get('Accuracy', 0):.4f}",
        f"{metrics_dict.get('AUC_ROC', 0):.4f}",
        f"{metrics_dict.get('Precision', 0):.4f}"
    ]
    header_str = '| ' + ' | '.join(headers) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
    row_str = '| ' + ' | '.join(row) + ' |'
    return f"{header_str}\n{separator}\n{row_str}"
