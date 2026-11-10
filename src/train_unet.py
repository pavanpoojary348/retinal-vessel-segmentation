"""
Train Standard U-Net on DRIVE dataset
=====================================
Experiment 2: ML/DL-Based Technique Baseline
"""

import os, sys, time, csv, random
import numpy as np
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import get_dataloaders
from models.unet import UNet
from models.morph_vit import DiceBCELoss
from metrics import compute_all_metrics

SEED = 42

def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def main():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[UNet Baseline] Training on device: {device}")

    proj_dir = os.path.abspath(os.path.join(SRC_DIR, ".."))
    data_root = os.path.join(proj_dir, "data", "raw")
    ckpt_dir = os.path.join(proj_dir, "outputs", "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)

    img_size = (576, 576)
    train_loader, test_loader = get_dataloaders(
        data_root=data_root, img_size=img_size, batch_size=2, num_workers=0
    )

    model = UNet(in_channels=3, out_channels=1, base_filters=16).to(device)  # 485K params for fast CPU training
    params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"U-Net Parameters: {params:,}")

    criterion = DiceBCELoss(pos_weight=4.0, dice_weight=1.0)
    optimizer = optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=15, eta_min=1e-6)

    epochs = 15
    best_dice = 0.0

    print("Beginning training (25 epochs)...")
    for epoch in range(1, epochs + 1):
        t0 = time.time()
        model.train()
        train_loss = 0.0

        for batch in train_loader:
            x = batch["input"][:, :3, :, :].to(device)  # Only 3 RGB channels!
            y = batch["label"].to(device)
            fov = batch["fov"].to(device)

            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y, fov_mask=fov)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item()

        scheduler.step()
        train_loss /= len(train_loader)

        # Validation
        model.eval()
        all_preds, all_labels, all_fovs = [], [], []
        with torch.no_grad():
            for batch in train_loader:
                x = batch["input"][:, :3, :, :].to(device)
                y = batch["label"]
                fov = batch["fov"]
                logits = model(x)
                probs = torch.sigmoid(logits).cpu().numpy()
                y_np = y.numpy()
                f_np = fov.numpy()
                for i in range(probs.shape[0]):
                    all_preds.append(probs[i, 0].ravel())
                    all_labels.append(y_np[i, 0].ravel())
                    all_fovs.append(f_np[i, 0].ravel())

        m = compute_all_metrics(
            y_true=np.concatenate(all_labels),
            y_pred_probs=np.concatenate(all_preds),
            fov_mask=np.concatenate(all_fovs),
            threshold=0.5
        )
        elapsed = time.time() - t0
        dice = m["Dice"]
        print(f"Epoch {epoch:2d}/{epochs} | Loss={train_loss:.4f} | Dice={dice:.4f} | Acc={m['Accuracy']:.4f} | Sens={m['Sensitivity']:.4f} | Spec={m['Specificity']:.4f} | {elapsed:.1f}s")

        if dice > best_dice:
            best_dice = dice
            torch.save({
                "epoch": epoch,
                "model_state": model.state_dict(),
                "best_dice": best_dice,
                "metrics": m
            }, os.path.join(ckpt_dir, "unet_best.pth"))

    print(f"\nU-Net training finished! Best Dice: {best_dice:.4f}")

if __name__ == "__main__":
    main()
