"""
Retinal Blood Vessel Segmentation - Ablation Study / Baseline Comparison
=========================================================================
FIP Course Project

Compares:
  1. Classical Morphology-Only baseline (no deep learning)
  2. Trained Morph-ViT (best checkpoint)

Both are evaluated on the DRIVE training split (ground truth available)
inside the FOV mask using all 7 metrics.

Usage:
    python src/ablation.py
    python src/ablation.py --checkpoint outputs/checkpoints/best_model.pth
    python src/ablation.py --threshold 0.45
"""

import os, sys, csv, argparse
import numpy as np
import torch
from tqdm import tqdm

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import DRIVEDataset, DEFAULT_IMG_SIZE, load_image
from morphology import traditional_morphology_segmentation
from models.morph_vit import MorphologyVisionTransformer
from metrics import compute_all_metrics, format_metrics_table

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def parse_args():
    p = argparse.ArgumentParser(description="Ablation: Morphology-Only vs Morph-ViT")
    p.add_argument("--data_root",    type=str,   default="data/raw")
    p.add_argument("--checkpoint",   type=str,   default="outputs/checkpoints/best_model.pth")
    p.add_argument("--img_size",     type=int,   default=576)
    p.add_argument("--threshold",    type=float, default=0.5)
    p.add_argument("--output_dir",   type=str,   default="outputs")
    p.add_argument("--morph_kernel", type=int,   default=15)
    p.add_argument("--morph_thresh_pct", type=float, default=88.0,
                   help="Percentile threshold for morphology-only baseline")
    return p.parse_args()


# ---------------------------------------------------------------------------
# 1. Morphology-only baseline
# ---------------------------------------------------------------------------
def run_morphology_baseline(dataset, morph_kernel, morph_thresh_pct):
    """
    Runs the classical morphological segmentation baseline on all dataset images.
    Returns aggregate metrics dict.
    """
    all_preds, all_labels, all_fovs = [], [], []

    for i in tqdm(range(len(dataset)), desc="Morphology Baseline", ncols=90):
        sample = dataset[i]
        img_path = dataset.samples[i]["img_path"]
        fov_path = dataset.samples[i]["fov_path"]
        lbl_path = dataset.samples[i]["lbl_path"]

        rgb = load_image(img_path, size=(dataset.img_size[0], dataset.img_size[1]), mode="RGB")
        fov = load_image(fov_path, size=(dataset.img_size[0], dataset.img_size[1]), mode="L")
        lbl = load_image(lbl_path, size=(dataset.img_size[0], dataset.img_size[1]), mode="L") if lbl_path else None

        # Classical morphological segmentation returns binary mask
        binary = traditional_morphology_segmentation(
            rgb_image=rgb, fov_mask=fov,
            kernel_size=morph_kernel, threshold_percentile=morph_thresh_pct)

        # Use binary as probability proxy (0 or 1)
        all_preds.append(binary.astype(np.float32).ravel())
        if lbl is not None:
            all_labels.append((lbl > 0).astype(np.float32).ravel())
        else:
            all_labels.append(np.zeros(binary.size, dtype=np.float32))
        all_fovs.append((fov > 0).astype(np.float32).ravel())

    agg_pred   = np.concatenate(all_preds)
    agg_label  = np.concatenate(all_labels)
    agg_fov    = np.concatenate(all_fovs)

    return compute_all_metrics(y_true=agg_label, y_pred_probs=agg_pred,
                               fov_mask=agg_fov, threshold=0.5)


# ---------------------------------------------------------------------------
# 2. Morph-ViT inference
# ---------------------------------------------------------------------------
@torch.no_grad()
def run_morph_vit(dataset, checkpoint_path, device, threshold):
    """Runs the trained Morph-ViT and returns aggregate metrics dict."""
    if not os.path.exists(checkpoint_path):
        print(f"[WARN] Checkpoint not found: {checkpoint_path}")
        return None

    ckpt = torch.load(checkpoint_path, map_location=device)
    a    = ckpt.get("args", {})
    model = MorphologyVisionTransformer(
        in_channels=4, patch_size=a.get("patch_size", 16),
        embed_dim=a.get("embed_dim", 128), depth=a.get("depth", 4),
        num_heads=a.get("num_heads", 4), mlp_ratio=a.get("mlp_ratio", 2.0), dropout=0.0).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    epoch = ckpt.get("epoch", "?")
    print(f"  Loaded Morph-ViT checkpoint: epoch={epoch}, best_dice={ckpt.get('best_dice','?'):.4f}")

    all_preds, all_labels, all_fovs = [], [], []

    for i in tqdm(range(len(dataset)), desc="Morph-ViT", ncols=90):
        sample = dataset[i]
        x      = sample["input"].unsqueeze(0).to(device)
        label  = sample["label"].numpy()[0]
        fov    = sample["fov"].numpy()[0]

        logits = model(x)
        prob   = torch.sigmoid(logits).squeeze().cpu().numpy()

        all_preds.append(prob.ravel())
        all_labels.append(label.ravel())
        all_fovs.append(fov.ravel())

    agg_pred   = np.concatenate(all_preds)
    agg_label  = np.concatenate(all_labels)
    agg_fov    = np.concatenate(all_fovs)

    return compute_all_metrics(y_true=agg_label, y_pred_probs=agg_pred,
                               fov_mask=agg_fov, threshold=threshold)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args   = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'='*70}")
    print(f"  Ablation Study: Morphology-Only vs Morph-ViT")
    print(f"  DRIVE Dataset — Training Split (20 images)")
    print(f"  Device: {device} | Threshold: {args.threshold}")
    print(f"{'='*70}\n")

    img_size = (args.img_size, args.img_size)
    dataset  = DRIVEDataset(root_dir=args.data_root, split="training",
                            img_size=img_size, augment=False, morph_kernel=args.morph_kernel)

    # --- Run baselines ---
    print("Running Morphology-Only baseline...")
    morph_metrics = run_morphology_baseline(dataset, args.morph_kernel, args.morph_thresh_pct)
    morph_metrics["model"] = "Morphology-Only"

    print("\nRunning Morph-ViT...")
    vit_metrics = run_morph_vit(dataset, args.checkpoint, device, args.threshold)
    if vit_metrics:
        vit_metrics["model"] = "Morph-ViT (ours)"

    # --- Display comparison table ---
    metric_keys = ["Dice", "IoU", "Sensitivity", "Specificity", "Accuracy", "AUC_ROC", "Precision"]
    models = [morph_metrics]
    if vit_metrics:
        models.append(vit_metrics)

    rows    = [[m["model"]] + [f"{m[k]:.4f}" for k in metric_keys] for m in models]
    headers = ["Method"] + metric_keys

    print(f"\n{'='*90}")
    print(f"  ABLATION RESULTS — DRIVE Training Split (All Metrics Inside FOV)")
    print(f"{'='*90}")
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="github"))
    else:
        print(" | ".join(f"{h:<22}" for h in headers))
        print("-" * (24 * len(headers)))
        for row in rows:
            print(" | ".join(f"{c:<22}" for c in row))
    print(f"{'='*90}\n")

    if vit_metrics:
        print("  Improvement of Morph-ViT over Morphology-Only baseline:")
        for k in metric_keys:
            delta = vit_metrics[k] - morph_metrics[k]
            sign  = "+" if delta >= 0 else ""
            print(f"    {k:<15}: {sign}{delta:.4f}")
        print()

    # Save CSV
    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = os.path.join(args.output_dir, "ablation_results.csv")
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["model"] + metric_keys
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in models:
            writer.writerow({k: m.get(k, "") for k in fieldnames})
    print(f"  Ablation results saved: {csv_path}\n")


if __name__ == "__main__":
    main()
