"""
Retinal Blood Vessel Segmentation - Morphological Post-Processing Module
========================================================================
Fundamental of Image Processing (FIP) Course Project

Applies connected-component morphological filtering to remove isolated false-positive
noise specks while preserving continuous vascular trees.
"""

import numpy as np
from scipy.ndimage import label


def clean_isolated_specks(binary_mask: np.ndarray, min_size: int = 10, fov_mask: np.ndarray = None) -> np.ndarray:
    """
    Remove isolated connected components smaller than min_size pixels.
    Enforces FOV boundary constraints.
    """
    clean = (binary_mask > 0).astype(np.uint8)

    if min_size > 0:
        labeled, num_features = label(clean)
        if num_features > 0:
            sizes = np.bincount(labeled.ravel())
            small_mask = sizes < min_size
            clean[small_mask[labeled]] = 0

    if fov_mask is not None:
        clean = clean * (fov_mask > 0).astype(np.uint8)

    return clean

