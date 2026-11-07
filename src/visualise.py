"""
Retinal Blood Vessel Segmentation - Visualisation Utilities
============================================================
FIP Course Project

Provides plotting functions for training curves, sample panels, ROC curves,
and morphological stage visualisations.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_sample_panel(rgb, fov, label, morph, pred_prob=None, pred_binary=None,
                      title="", save_path=None):
    """2x3 panel: original, FOV, GT | morph, prob, binary."""
    nrows = 2
    fig, axes = plt.subplots(nrows, 3, figsize=(12, 8))

    axes[0][0].imshow(rgb);                    axes[0][0].set_title("RGB Fundus"); axes[0][0].axis("off")
    axes[0][1].imshow(fov, cmap="gray");       axes[0][1].set_title("FOV Mask");   axes[0][1].axis("off")
    axes[0][2].imshow(label, cmap="gray");     axes[0][2].set_title("GT Vessels"); axes[0][2].axis("off")
    axes[1][0].imshow(morph, cmap="hot");      axes[1][0].set_title("Morph Feature"); axes[1][0].axis("off")

    if pred_prob is not None:
        im = axes[1][1].imshow(pred_prob, cmap="hot", vmin=0, vmax=1)
        axes[1][1].set_title("Pred Probability"); axes[1][1].axis("off")
        plt.colorbar(im, ax=axes[1][1], fraction=0.046, pad=0.04)
    else:
        axes[1][1].axis("off")

    if pred_binary is not None:
        axes[1][2].imshow(pred_binary, cmap="gray")
        axes[1][2].set_title("Binary Pred (thr=0.5)"); axes[1][2].axis("off")
    else:
        axes[1][2].axis("off")

    if title:
        fig.suptitle(title, fontsize=13, fontweight="bold")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight"); plt.close(fig)
    else:
        plt.show()


def plot_training_curves(log_csv, save_path=None):
    """Plot loss, Dice/AUC, Sensitivity/Specificity from train_log.csv."""
    import csv
    epochs, train_losses, val_losses = [], [], []
    dices, aucs, sensitivities, specificities = [], [], [], []
    with open(log_csv) as f:
        for row in csv.DictReader(f):
            epochs.append(int(row["epoch"]))
            train_losses.append(float(row["train_loss"]))
            val_losses.append(float(row["val_loss"]))
            dices.append(float(row["Dice"]))
            aucs.append(float(row["AUC_ROC"]))
            sensitivities.append(float(row["Sensitivity"]))
            specificities.append(float(row["Specificity"]))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(epochs, train_losses, label="Train", color="steelblue")
    axes[0].plot(epochs, val_losses,   label="Val",   color="orange", ls="--")
    axes[0].set_title("Loss Curves"); axes[0].set_xlabel("Epoch"); axes[0].legend(); axes[0].grid(alpha=0.3)

    axes[1].plot(epochs, dices, label="Dice (F1)", color="green")
    axes[1].plot(epochs, aucs,  label="AUC-ROC",   color="purple", ls="--")
    axes[1].set_title("Dice & AUC-ROC"); axes[1].set_ylim(0,1); axes[1].legend(); axes[1].grid(alpha=0.3)

    axes[2].plot(epochs, sensitivities, label="Sensitivity", color="tomato")
    axes[2].plot(epochs, specificities, label="Specificity", color="teal", ls="--")
    axes[2].set_title("Sensitivity & Specificity"); axes[2].set_ylim(0,1); axes[2].legend(); axes[2].grid(alpha=0.3)

    fig.suptitle("Morph-ViT Training History -- DRIVE", fontsize=13, fontweight="bold")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight"); plt.close(fig)
        print(f"  Training curves saved: {save_path}")
    else:
        plt.show()


def plot_per_image_metrics(metrics_list, metric_key="Dice", save_path=None):
    """Bar chart of a chosen metric for each evaluation image."""
    image_ids = [m["image_id"] for m in metrics_list if m["image_id"] != "AGGREGATE"]
    values    = [m[metric_key] for m in metrics_list if m["image_id"] != "AGGREGATE"]
    colors    = ["steelblue" if v >= np.mean(values) else "salmon" for v in values]

    fig, ax = plt.subplots(figsize=(max(10, len(image_ids) * 0.6), 5))
    ax.bar(image_ids, values, color=colors)
    ax.axhline(np.mean(values), color="black", ls="--", lw=1.5, label=f"Mean={np.mean(values):.4f}")
    ax.set_xticklabels(image_ids, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel(metric_key); ax.set_ylim(0,1); ax.legend(); ax.grid(axis="y", alpha=0.3)
    ax.set_title(f"Per-Image {metric_key} -- DRIVE")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight"); plt.close(fig)
    else:
        plt.show()


def plot_roc_curve(y_true, y_score, auc_val=None, save_path=None):
    """Plot ROC curve."""
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(y_true.ravel(), y_score.ravel())
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(fpr, tpr, color="steelblue", lw=2,
            label=f"ROC (AUC={auc_val:.4f})" if auc_val else "ROC")
    ax.plot([0,1],[0,1], "k--", lw=1, label="Random")
    ax.set_xlabel("FPR"); ax.set_ylabel("TPR (Sensitivity)")
    ax.set_title("ROC Curve -- Morph-ViT DRIVE"); ax.legend(loc="lower right"); ax.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight"); plt.close(fig)
    else:
        plt.show()


def plot_morphology_stages(morph_dict, image_id="", save_path=None):
    """Show 4 morphological preprocessing stages."""
    stages = [
        ("Green Channel",    morph_dict.get("green"),           "gray"),
        ("After CLAHE",      morph_dict.get("clahe"),           "gray"),
        ("Morph Top-Hat",    morph_dict.get("morph_enhanced"),  "hot"),
        ("Normalized [0,1]", morph_dict.get("normalized"),      "hot"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, (title, img, cmap) in zip(axes, stages):
        if img is not None: ax.imshow(img, cmap=cmap)
        ax.set_title(title); ax.axis("off")
    suptitle = "Morphological Preprocessing Pipeline"
    if image_id: suptitle += f" -- {image_id}"
    fig.suptitle(suptitle, fontsize=12, fontweight="bold"); plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight"); plt.close(fig)
    else:
        plt.show()


if __name__ == "__main__":
    log_csv = os.path.join("outputs", "train_log.csv")
    if os.path.exists(log_csv):
        plot_training_curves(log_csv, save_path=os.path.join("outputs", "training_curves.png"))
    else:
        print("No training log found. Run training first.")
