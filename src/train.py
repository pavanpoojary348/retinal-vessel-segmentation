"""
Retinal Blood Vessel Segmentation - Training Loop
==================================================
FIP Course Project — Trains the Morph-ViT model on the DRIVE dataset.

Usage:
    python src/train.py                              # defaults
    python src/train.py --epochs 50 --batch_size 2
    python src/train.py --resume outputs/checkpoints/best_model.pth
"""

import os, sys, csv, time, argparse, random
import numpy as np
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import get_dataloaders, DEFAULT_IMG_SIZE
from models.morph_vit import MorphologyVisionTransformer, DiceBCELoss
from metrics import compute_all_metrics

SEED = 42

def set_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def parse_args():
    p = argparse.ArgumentParser(description="Train Morph-ViT on DRIVE dataset")
    p.add_argument("--data_root",    type=str,   default="data/raw")
    p.add_argument("--img_size",     type=int,   default=576)
    p.add_argument("--morph_kernel", type=int,   default=15)
    p.add_argument("--patch_size",   type=int,   default=16)
    p.add_argument("--embed_dim",    type=int,   default=128)
    p.add_argument("--depth",        type=int,   default=4)
    p.add_argument("--num_heads",    type=int,   default=4)
    p.add_argument("--mlp_ratio",    type=float, default=2.0)
    p.add_argument("--dropout",      type=float, default=0.1)
    p.add_argument("--pos_weight",   type=float, default=4.0)
    p.add_argument("--dice_weight",  type=float, default=1.0)
    p.add_argument("--epochs",       type=int,   default=40)
    p.add_argument("--batch_size",   type=int,   default=2)
    p.add_argument("--lr",           type=float, default=3e-4)
    p.add_argument("--weight_decay", type=float, default=1e-4)
    p.add_argument("--num_workers",  type=int,   default=0)
    p.add_argument("--output_dir",   type=str,   default="outputs")
    p.add_argument("--resume",       type=str,   default=None)
    return p.parse_args()

def train_one_epoch(model, loader, optimizer, criterion, device, epoch, total_epochs):
    model.train()
    total_loss = 0.0
    pbar = tqdm(loader, desc=f"[Train] Epoch {epoch}/{total_epochs}", leave=False, ncols=100)
    for batch in pbar:
        x   = batch["input"].to(device)
        y   = batch["label"].to(device)
        fov = batch["fov"].to(device)
        optimizer.zero_grad()
        logits = model(x)
        loss   = criterion(logits, y, fov_mask=fov)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item()
        pbar.set_postfix(loss=f"{loss.item():.4f}")
    return total_loss / len(loader)

@torch.no_grad()
def validate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds, all_labels, all_fovs = [], [], []
    for batch in loader:
        x   = batch["input"].to(device)
        y   = batch["label"].to(device)
        fov = batch["fov"].to(device)
        logits = model(x)
        loss   = criterion(logits, y, fov_mask=fov)
        total_loss += loss.item()
        probs = torch.sigmoid(logits).cpu().numpy()
        y_np  = y.cpu().numpy()
        f_np  = fov.cpu().numpy()
        for i in range(probs.shape[0]):
            all_preds.append(probs[i, 0])
            all_labels.append(y_np[i, 0])
            all_fovs.append(f_np[i, 0])
    all_preds  = np.concatenate([p.ravel() for p in all_preds])
    all_labels = np.concatenate([l.ravel() for l in all_labels])
    all_fovs   = np.concatenate([f.ravel() for f in all_fovs])
    metrics = compute_all_metrics(y_true=all_labels, y_pred_probs=all_preds,
                                  fov_mask=all_fovs, threshold=0.5)
    return total_loss / len(loader), metrics

def main():
    args = parse_args()
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'='*60}")
    print(f"  Morph-ViT Training -- DRIVE Dataset")
    print(f"  Device: {device} | Epochs: {args.epochs} | LR: {args.lr}")
    print(f"  PatchSize: {args.patch_size} | EmbedDim: {args.embed_dim} | Depth: {args.depth}")
    print(f"{'='*60}\n")

    os.makedirs(args.output_dir, exist_ok=True)
    ckpt_dir = os.path.join(args.output_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)

    img_size = (args.img_size, args.img_size)
    train_loader, test_loader = get_dataloaders(
        data_root=args.data_root, img_size=img_size,
        batch_size=args.batch_size, num_workers=args.num_workers,
        morph_kernel=args.morph_kernel)

    model = MorphologyVisionTransformer(
        in_channels=4, patch_size=args.patch_size, embed_dim=args.embed_dim,
        depth=args.depth, num_heads=args.num_heads,
        mlp_ratio=args.mlp_ratio, dropout=args.dropout).to(device)

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Model parameters: {n_params:,}\n")

    criterion = DiceBCELoss(pos_weight=args.pos_weight, dice_weight=args.dice_weight)
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)

    start_epoch = 1
    best_dice   = 0.0
    if args.resume and os.path.exists(args.resume):
        ckpt = torch.load(args.resume, map_location=device)
        model.load_state_dict(ckpt["model_state"])
        optimizer.load_state_dict(ckpt["optimizer_state"])
        scheduler.load_state_dict(ckpt["scheduler_state"])
        start_epoch = ckpt.get("epoch", 0) + 1
        best_dice   = ckpt.get("best_dice", 0.0)
        print(f"  Resumed from epoch {start_epoch-1} (best Dice={best_dice:.4f})\n")

    log_path   = os.path.join(args.output_dir, "train_log.csv")
    log_fields = ["epoch","train_loss","val_loss","Dice","IoU","Sensitivity",
                  "Specificity","Accuracy","AUC_ROC","Precision","lr"]
    if not os.path.exists(log_path):
        with open(log_path, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=log_fields).writeheader()

    for epoch in range(start_epoch, args.epochs + 1):
        t0 = time.time()
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device, epoch, args.epochs)
        val_loss, metrics = validate(model, train_loader, criterion, device)
        scheduler.step()
        elapsed = time.time() - t0
        dice    = metrics["Dice"]
        lr_now  = scheduler.get_last_lr()[0]

        print(f"Epoch {epoch:3d}/{args.epochs} | TrainLoss={train_loss:.4f} | "
              f"ValLoss={val_loss:.4f} | Dice={dice:.4f} | IoU={metrics['IoU']:.4f} | "
              f"Sens={metrics['Sensitivity']:.4f} | Spec={metrics['Specificity']:.4f} | "
              f"Acc={metrics['Accuracy']:.4f} | AUC={metrics['AUC_ROC']:.4f} | "
              f"LR={lr_now:.2e} | {elapsed:.1f}s")

        with open(log_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=log_fields)
            writer.writerow({
                "epoch": epoch, "train_loss": f"{train_loss:.6f}", "val_loss": f"{val_loss:.6f}",
                **{k: f"{metrics[k]:.6f}" for k in ["Dice","IoU","Sensitivity","Specificity","Accuracy","AUC_ROC","Precision"]},
                "lr": f"{lr_now:.8f}",
            })

        ckpt = {"epoch": epoch, "model_state": model.state_dict(),
                "optimizer_state": optimizer.state_dict(),
                "scheduler_state": scheduler.state_dict(),
                "best_dice": best_dice, "metrics": metrics, "args": vars(args)}
        torch.save(ckpt, os.path.join(ckpt_dir, "last_model.pth"))

        if dice > best_dice:
            best_dice = dice
            torch.save(ckpt, os.path.join(ckpt_dir, "best_model.pth"))
            print(f"  New best Dice={best_dice:.4f} -- saved to {ckpt_dir}/best_model.pth")

    print(f"\n  Training complete! Best Dice={best_dice:.4f}")
    print(f"  Checkpoints: {ckpt_dir}")
    print(f"  Log: {log_path}\n")

if __name__ == "__main__":
    main()
