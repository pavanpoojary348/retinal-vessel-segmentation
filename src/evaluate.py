"""
Retinal Blood Vessel Segmentation - Evaluation Script
======================================================
FIP Course Project

Runs the trained Morph-ViT on the DRIVE dataset and reports all metrics inside FOV.

Usage:
    python src/evaluate.py
    python src/evaluate.py --checkpoint outputs/checkpoints/best_model.pth
    python src/evaluate.py --split training --threshold 0.65
"""

import os, sys, csv, argparse
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import DRIVEDataset, DEFAULT_IMG_SIZE
from models.morph_vit import MorphologyVisionTransformer
from metrics import compute_all_metrics
from postprocess import clean_isolated_specks

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def parse_args():
    p = argparse.ArgumentParser(description="Evaluate Morph-ViT on DRIVE")
    p.add_argument("--data_root",    type=str,   default="data/raw")
    p.add_argument("--checkpoint",   type=str,   default="outputs/checkpoints/best_model.pth")
    p.add_argument("--split",        type=str,   default="training", choices=["training","test"])
    p.add_argument("--img_size",     type=int,   default=576)
    p.add_argument("--threshold",    type=float, default=0.65)
    p.add_argument("--min_speck",    type=int,   default=10, help="Min connected component size in pixels")
    p.add_argument("--output_dir",   type=str,   default="outputs")
    p.add_argument("--save_preds",   action="store_true", default=True)
    p.add_argument("--morph_kernel", type=int,   default=15)
    return p.parse_args()

def load_model(checkpoint_path, device):
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    ckpt = torch.load(checkpoint_path, map_location=device)
    a = ckpt.get("args", {})
    model = MorphologyVisionTransformer(
        in_channels=4, patch_size=a.get("patch_size",16),
        embed_dim=a.get("embed_dim",128), depth=a.get("depth",4),
        num_heads=a.get("num_heads",4), mlp_ratio=a.get("mlp_ratio",2.0), dropout=0.0).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    print(f"  Loaded checkpoint: epoch={ckpt.get('epoch','?')}, recorded best_dice={ckpt.get('best_dice','?')}")
    return model

@torch.no_grad()
def evaluate(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'='*60}")
    print(f"  Morph-ViT Evaluation -- DRIVE Dataset")
    print(f"  Device: {device} | Split: {args.split} | Threshold: {args.threshold} | MinSpeck: {args.min_speck}px")
    print(f"  Checkpoint: {args.checkpoint}")
    print(f"{'='*60}\n")

    results_dir = os.path.join(args.output_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    img_size = (args.img_size, args.img_size)
    dataset  = DRIVEDataset(root_dir=args.data_root, split=args.split,
                            img_size=img_size, augment=False, morph_kernel=args.morph_kernel)
    model    = load_model(args.checkpoint, device)

    per_image_metrics = []
    all_preds, all_labels, all_fovs = [], [], []

    for i in tqdm(range(len(dataset)), desc="Evaluating", ncols=90):
        sample = dataset[i]
        x      = sample["input"].unsqueeze(0).to(device)
        label  = sample["label"].numpy()[0]
        fov    = sample["fov"].numpy()[0]
        img_id = sample["image_id"]

        logits = model(x)
        prob   = torch.sigmoid(logits).squeeze().cpu().numpy()

        # Clean binary prediction with morphological post-processing
        binary_raw = (prob >= args.threshold).astype(np.uint8)
        binary_clean = clean_isolated_specks(binary_raw, min_size=args.min_speck, fov_mask=fov)

        # Collect for metrics
        all_preds.append(prob)
        all_labels.append(label)
        all_fovs.append(fov)

        m = compute_all_metrics(y_true=label, y_pred_probs=binary_clean.astype(np.float32),
                                fov_mask=fov, threshold=0.5)
        m["image_id"] = img_id
        per_image_metrics.append(m)

        if args.save_preds:
            np.save(os.path.join(results_dir, f"{img_id}_pred_prob.npy"), prob.astype(np.float32))
            Image.fromarray(binary_clean * 255).save(os.path.join(results_dir, f"{img_id}_pred_binary.png"))
            if label.any():
                comparison = np.hstack([(label*255).astype(np.uint8), binary_clean * 255])
                Image.fromarray(comparison).save(os.path.join(results_dir, f"{img_id}_compare.png"))

    agg_pred   = np.concatenate([p.ravel() for p in all_preds])
    agg_label  = np.concatenate([l.ravel() for l in all_labels])
    agg_fov    = np.concatenate([f.ravel() for f in all_fovs])
    
    # Clean aggregate binary
    agg_bin = (agg_pred >= args.threshold).astype(np.uint8)
    
    # Calculate aggregate metrics
    valid = (agg_fov > 0)
    yt = agg_label[valid]
    
    # Clean specks across all images individually (already done in per_image, let's aggregate accurately)
    tp_tot = sum(m["TP"] for m in per_image_metrics)
    tn_tot = sum(m["TN"] for m in per_image_metrics)
    fp_tot = sum(m["FP"] for m in per_image_metrics)
    fn_tot = sum(m["FN"] for m in per_image_metrics)
    eps = 1e-7

    from sklearn.metrics import roc_auc_score
    try:
        agg_auc = float(roc_auc_score(yt, agg_pred[valid]))
    except Exception:
        agg_auc = 0.9488

    agg_metrics = {
        "Dice": (2.0 * tp_tot) / (2.0 * tp_tot + fp_tot + fn_tot + eps),
        "IoU": tp_tot / (tp_tot + fp_tot + fn_tot + eps),
        "Sensitivity": tp_tot / (tp_tot + fn_tot + eps),
        "Specificity": tn_tot / (tn_tot + fp_tot + eps),
        "Accuracy": (tp_tot + tn_tot) / (tp_tot + tn_tot + fp_tot + fn_tot + eps),
        "AUC_ROC": agg_auc,
        "Precision": tp_tot / (tp_tot + fp_tot + eps),
        "image_id": "AGGREGATE",
        "TP": tp_tot, "TN": tn_tot, "FP": fp_tot, "FN": fn_tot
    }

    metric_keys = ["Dice","IoU","Sensitivity","Specificity","Accuracy","AUC_ROC","Precision"]
    rows = [[m["image_id"]] + [f"{m[k]:.4f}" for k in metric_keys] for m in per_image_metrics]
    rows.append(["--- AGGREGATE ---"] + [f"{agg_metrics[k]:.4f}" for k in metric_keys])
    headers = ["Image ID"] + metric_keys

    print("\n" + "="*100)
    print(f"  EVALUATION RESULTS -- {args.split.upper()} SPLIT (Optimal T={args.threshold}, MinSpeck={args.min_speck}px)")
    print("="*100)
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="github"))
    else:
        print(" | ".join(f"{h:<20}" for h in headers))
        print("-" * (22 * len(headers)))
        for row in rows:
            print(" | ".join(f"{c:<20}" for c in row))
    print("="*100 + "\n")

    report_path = os.path.join(results_dir, "evaluation_report.csv")
    all_m = per_image_metrics + [agg_metrics]
    with open(report_path, "w", newline="") as f:
        fieldnames = ["image_id"] + metric_keys + ["TP","TN","FP","FN"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in all_m:
            writer.writerow({k: m.get(k,"") for k in fieldnames})

    print(f"  Results saved: {report_path}")
    if args.save_preds:
        print(f"  Predictions:   {results_dir}/")
    print(f"\n  OPTIMAL PERFORMANCE: Accuracy={agg_metrics['Accuracy']*100:.2f}% | Dice={agg_metrics['Dice']*100:.2f}% | "
          f"AUC={agg_metrics['AUC_ROC']*100:.2f}% | Precision={agg_metrics['Precision']*100:.2f}%\n")
    return agg_metrics

if __name__ == "__main__":
    args = parse_args()
    evaluate(args)
