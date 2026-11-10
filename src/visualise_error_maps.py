"""
Visual Comparison & Error Map Generator
=======================================
Requirement 6: "Students must provide visual comparisons of input images,
ground-truth images, predicted results and error maps wherever applicable."

Color scheme:
- Green [0, 255, 0]  : True Positive (TP) - correctly segmented vessel
- Red   [255, 0, 0]  : False Negative (FN) - missed capillary
- Blue  [0, 150, 255]: False Positive (FP) - false detection
- Black [0, 0, 0]    : True Negative (TN) - correct background
"""

import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import load_image
from morphology import traditional_morphology_segmentation


def make_error_map(pred_bin: np.ndarray, gt_bin: np.ndarray, fov_bin: np.ndarray) -> np.ndarray:
    """
    Generate an RGB error map:
    - Green: TP (correct vessel)
    - Red: FN (missed vessel)
    - Blue: FP (false alarm)
    - Black: TN (background inside FOV)
    - Dark gray: outside FOV
    """
    H, W = pred_bin.shape
    error_rgb = np.zeros((H, W, 3), dtype=np.uint8)

    # Outside FOV: Dark gray
    error_rgb[fov_bin == 0] = [35, 35, 35]

    # Inside FOV masks
    in_fov = (fov_bin > 0)
    tp = in_fov & (pred_bin == 1) & (gt_bin == 1)
    fn = in_fov & (pred_bin == 0) & (gt_bin == 1)
    fp = in_fov & (pred_bin == 1) & (gt_bin == 0)
    tn = in_fov & (pred_bin == 0) & (gt_bin == 0)

    error_rgb[tp] = [0, 230, 0]       # Green: TP
    error_rgb[fn] = [230, 30, 30]     # Red: FN (missed)
    error_rgb[fp] = [30, 140, 255]    # Cyan/Blue: FP (false alarm)
    error_rgb[tn] = [10, 10, 10]      # Black: TN

    return error_rgb


def generate_error_panels(proj_dir: str):
    data_root = os.path.join(proj_dir, "data", "raw", "training")
    results_dir = os.path.join(proj_dir, "outputs", "results")
    out_dir = os.path.join(proj_dir, "outputs", "error_maps")
    os.makedirs(out_dir, exist_ok=True)

    img_ids = ["21_training", "22_training", "23_training", "24_training", "25_training"]
    img_size = (576, 576)

    print(f"Generating visual comparison & error panels for {len(img_ids)} samples...")

    for img_id in img_ids:
        num = img_id.split("_")[0]
        img_path = os.path.join(data_root, "images", f"{num}_training.tif")
        fov_path = os.path.join(data_root, "mask", f"{num}_training_mask.gif")
        lbl_path = os.path.join(data_root, "1st_manual", f"{num}_manual1.gif")
        pred_bin_path = os.path.join(results_dir, f"{img_id}_pred_binary.png")

        if not os.path.exists(pred_bin_path):
            continue

        rgb = load_image(img_path, size=img_size, mode="RGB")
        fov = load_image(fov_path, size=img_size, mode="L")
        lbl = load_image(lbl_path, size=img_size, mode="L")
        pred_img = Image.open(pred_bin_path).convert("L")
        pred_bin = (np.array(pred_img) > 127).astype(np.uint8)

        gt_bin = (lbl > 0).astype(np.uint8)
        fov_bin = (fov > 0).astype(np.uint8)

        # Traditional morphology prediction for comparison
        morph_bin = traditional_morphology_segmentation(rgb, fov, kernel_size=15, threshold_percentile=88.0)

        # Generate error maps
        err_morph = make_error_map(morph_bin, gt_bin, fov_bin)
        err_vit = make_error_map(pred_bin, gt_bin, fov_bin)

        # Create 2x3 Figure:
        # Row 1: Input RGB | Ground Truth | Proposed Morph-ViT Prediction
        # Row 2: Traditional Morphology | Morph Error Map | Morph-ViT Error Map
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))

        axes[0, 0].imshow(rgb)
        axes[0, 0].set_title("(a) Input RGB Fundus", fontsize=12, fontweight="bold")
        axes[0, 0].axis("off")

        axes[0, 1].imshow(gt_bin, cmap="gray")
        axes[0, 1].set_title("(b) Ground Truth (Expert)", fontsize=12, fontweight="bold")
        axes[0, 1].axis("off")

        axes[0, 2].imshow(pred_bin, cmap="gray")
        axes[0, 2].set_title("(c) Proposed Morph-ViT Prediction", fontsize=12, fontweight="bold")
        axes[0, 2].axis("off")

        axes[1, 0].imshow(morph_bin, cmap="gray")
        axes[1, 0].set_title("(d) Traditional Morphology (Exp 1)", fontsize=12, fontweight="bold")
        axes[1, 0].axis("off")

        axes[1, 1].imshow(err_morph)
        axes[1, 1].set_title("(e) Traditional Error Map\n(Red=Missed, Green=Correct)", fontsize=11, fontweight="bold")
        axes[1, 1].axis("off")

        axes[1, 2].imshow(err_vit)
        axes[1, 2].set_title("(f) Proposed Morph-ViT Error Map\n(High Green = High Recall)", fontsize=11, fontweight="bold")
        axes[1, 2].axis("off")

        plt.suptitle(f"Retinal Vessel Segmentation Error Map Analysis — {img_id}", fontsize=14, fontweight="bold", y=0.98)
        plt.tight_layout()

        save_path = os.path.join(out_dir, f"{img_id}_error_panel.png")
        plt.savefig(save_path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        print(f"  ✓ Saved: {save_path}")

    print("All error panels generated successfully in outputs/error_maps/!")


if __name__ == "__main__":
    docs_dir = None
    for d in os.listdir(r"C:\Users\pooja\OneDrive"):
        if "li" in d.lower():
            docs_dir = os.path.join(r"C:\Users\pooja\OneDrive", d)
            break
    proj = os.path.join(docs_dir, "retinal-vessel-segmentation")
    generate_error_panels(proj)
