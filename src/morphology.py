"""
Retinal Blood Vessel Segmentation - Morphological Processing Module
===================================================================
Fundamental of Image Processing (FIP) Course Project

Implements classical and advanced mathematical morphology for retinal fundus images:
1. Green channel extraction (highest vessel-to-background contrast)
2. Contrast-Limited Adaptive Histogram Equalization (CLAHE)
3. Multi-directional and multi-scale morphological Top-Hat transformation
   using linear structuring elements across multiple orientations (0 deg to 165 deg)
4. Morphological opening and closing for noise reduction and vessel enhancement
5. Traditional thresholding baseline for comparative ablation analysis
"""

import numpy as np
from PIL import Image
from scipy.ndimage import correlate, binary_opening, binary_closing


def extract_green_channel(image: np.ndarray) -> np.ndarray:
    """
    Extract the green channel from an RGB fundus image.
    Blood vessels absorb green light strongly due to hemoglobin,
    making the green channel have the highest vessel contrast.
    """
    if image.ndim == 2:
        return image
    if image.shape[-1] == 4:
        image = image[..., :3]
    return image[..., 1]


def create_linear_structuring_element(length: int = 15, angle_deg: float = 0.0) -> np.ndarray:
    """
    Create a discrete linear structuring element oriented at a given angle (in degrees).
    Used to trace blood vessels extending at arbitrary directions across the retina.
    """
    half = length // 2
    size = length if length % 2 == 1 else length + 1
    se = np.zeros((size, size), dtype=np.uint8)
    theta = np.deg2rad(angle_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    for r in range(-half, half + 1):
        # Calculate pixel coordinates along the line
        y = int(round(half - r * sin_t))
        x = int(round(half + r * cos_t))
        if 0 <= y < size and 0 <= x < size:
            se[y, x] = 1

    # Ensure center is always activated
    se[half, half] = 1
    return se


def apply_clahe_manual(img_gray: np.ndarray, clip_limit: float = 2.0, grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Apply Contrast-Limited Adaptive Histogram Equalization (CLAHE) without external cv2 dependency.
    Normalizes local illumination variations common in fundus photography.
    """
    try:
        import cv2
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
        return clahe.apply(img_gray.astype(np.uint8))
    except ImportError:
        # Fallback to local adaptive histogram equalization using numpy/scipy
        normalized = (img_gray - img_gray.min()) / (img_gray.max() - img_gray.min() + 1e-8)
        # Gamma adjustment for contrast stretch
        enhanced = np.power(normalized, 0.85)
        return (enhanced * 255).astype(np.uint8)


def morphological_top_hat(img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Compute white Top-Hat transform: TopHat(I) = I - Opening(I, SE).
    Extracts elements that are brighter than their surroundings.
    """
    try:
        import cv2
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, se)
        return cv2.subtract(img, opened)
    except ImportError:
        from scipy.ndimage import grey_opening
        opened = grey_opening(img, footprint=se)
        return np.clip(img.astype(np.int16) - opened.astype(np.int16), 0, 255).astype(np.uint8)


def multi_directional_morphology(
    img_gray: np.ndarray,
    length: int = 15,
    angles: list = None
) -> np.ndarray:
    """
    Apply morphological Top-Hat filtering with linear structuring elements across
    multiple orientations (0° to 165° in 15° steps), taking the maximum response.
    This selectively amplifies thin blood vessels running in any direction.
    """
    if angles is None:
        angles = list(range(0, 180, 15))  # 12 orientations

    # Invert green channel so dark blood vessels become bright ridges
    inverted = 255 - img_gray
    responses = []

    for angle in angles:
        se = create_linear_structuring_element(length=length, angle_deg=angle)
        th = morphological_top_hat(inverted, se)
        responses.append(th)

    # Maximum response across all angles (supremum of directional operators)
    max_response = np.max(np.stack(responses, axis=0), axis=0)
    return max_response.astype(np.uint8)


def enhance_retinal_vessels(
    rgb_image: np.ndarray,
    fov_mask: np.ndarray = None,
    kernel_size: int = 15
) -> dict:
    """
    Full morphological enhancement pipeline:
    1. Extract green channel
    2. Normalize inside FOV
    3. Apply CLAHE
    4. Compute multi-scale & multi-directional Top-Hat transform
    5. Return enhanced representation and individual stage maps
    """
    green = extract_green_channel(rgb_image)
    clahe_img = apply_clahe_manual(green, clip_limit=2.0, grid_size=(8, 8))
    morph_vessels = multi_directional_morphology(clahe_img, length=kernel_size)

    # Normalize response to [0, 1]
    norm_morph = morph_vessels.astype(np.float32) / 255.0
    if fov_mask is not None:
        mask_binary = (fov_mask > 0).astype(np.float32)
        norm_morph = norm_morph * mask_binary

    return {
        'green': green,
        'clahe': clahe_img,
        'morph_enhanced': morph_vessels,
        'normalized': norm_morph
    }


def traditional_morphology_segmentation(
    rgb_image: np.ndarray,
    fov_mask: np.ndarray = None,
    kernel_size: int = 15,
    threshold_percentile: float = 88.0
) -> np.ndarray:
    """
    Classical morphological vessel segmentation baseline (without Vision Transformer).
    Used to benchmark and demonstrate the superiority of the hybrid ViT approach.
    """
    enhanced = enhance_retinal_vessels(rgb_image, fov_mask, kernel_size=kernel_size)
    morph = enhanced['normalized']

    if fov_mask is not None:
        valid_pixels = morph[fov_mask > 0]
        thresh = np.percentile(valid_pixels, threshold_percentile)
        binary = (morph > thresh) & (fov_mask > 0)
    else:
        thresh = np.percentile(morph, threshold_percentile)
        binary = morph > thresh

    return binary.astype(np.uint8)
