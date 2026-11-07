"""
Retinal Blood Vessel Segmentation - Single-Image Prediction
============================================================
FIP Course Project

Usage:
    python src/predict.py --image data/raw/test/images/01_test.tif
    python src/predict.py --image my_fundus.tif --fov my_mask.gif
    python src/predict.py --image my_fundus.tif --checkpoint outputs/checkpoints/best_model.pth
"""

import os, sys, argparse
import numpy as np
import torch
from PIL import Image

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from dataset import DEFAULT_IMG_SIZE, load_image
from morphology import enhance_retinal_vessels
from models.morph_vit import MorphologyVisionTransformer
from postprocess import clean_isolated_specks

def parse_args():
    p = argparse.ArgumentParser(description="Predict vessel mask for a single retinal image")
    p.add_argument("--image",        type=str, required=True)
    p.add_argument("--fov",          type=str, default=None)
    p.add_argument("--checkpoint",   type=str, default="outputs/checkpoints/best_model.pth")
    p.add_argument("--img_size",     type=int, default=576)
    p.add_argument("--morph_kernel", type=int, default=15)
    p.add_argument("--threshold",    type=float, default=0.65)
    p.add_argument("--min_speck",    type=int, default=10)
    p.add_argument("--output_dir",   type=str, default="outputs/predictions")
    return p.parse_args()

def load_model(checkpoint_path, device):
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    ckpt  = torch.load(checkpoint_path, map_location=device)
    saved = ckpt.get("args", {})
    model = MorphologyVisionTransformer(
        in_channels=4, patch_size=saved.get("patch_size",16),
        embed_dim=saved.get("embed_dim",128), depth=saved.get("depth",4),
        num_heads=saved.get("num_heads",4), mlp_ratio=saved.get("mlp_ratio",2.0), dropout=0.0).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    print(f"  Loaded checkpoint: epoch={ckpt.get('epoch','?')}")
    return model

def make_overlay(rgb, prob_map, alpha=0.5):
    overlay = rgb.copy().astype(np.float32)
    heat    = np.zeros_like(rgb, dtype=np.float32)
    heat[..., 1] = prob_map * 255
    blended = (1 - alpha) * overlay + alpha * heat
    return np.clip(blended, 0, 255).astype(np.uint8)

@torch.no_grad()
def predict(args):
    device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img_size  = (args.img_size, args.img_size)
    base_name = os.path.splitext(os.path.basename(args.image))[0]
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\n  Morph-ViT Single-Image Prediction")
    print(f"  Image: {args.image} | Threshold: {args.threshold} | Device: {device}\n")

    rgb = load_image(args.image, size=img_size, mode="RGB")
    if args.fov and os.path.exists(args.fov):
        fov = load_image(args.fov, size=img_size, mode="L")
    else:
        fov = np.ones((img_size[0], img_size[1]), dtype=np.uint8) * 255

    morph_dict = enhance_retinal_vessels(rgb, fov_mask=fov, kernel_size=args.morph_kernel)
    morph_ch   = morph_dict["normalized"].astype(np.float32)

    rgb_norm   = rgb.astype(np.float32) / 255.0
    rgb_t      = torch.from_numpy(rgb_norm).permute(2, 0, 1)
    morph_t    = torch.from_numpy(morph_ch).unsqueeze(0)
    x          = torch.cat([rgb_t, morph_t], dim=0).unsqueeze(0).to(device)

    model  = load_model(args.checkpoint, device)
    logits = model(x)
    prob   = torch.sigmoid(logits).squeeze().cpu().numpy()
    fov_bin = (fov > 0).astype(np.float32)
    prob   = prob * fov_bin

    # Morphological speck removal
    min_spk = getattr(args, "min_speck", 10)
    binary = (prob >= args.threshold).astype(np.uint8)
    binary = clean_isolated_specks(binary, min_size=min_spk, fov_mask=fov) * 255

    Image.fromarray((prob * 255).astype(np.uint8)).save(
        os.path.join(args.output_dir, f"{base_name}_prob.png"))
    Image.fromarray(binary).save(
        os.path.join(args.output_dir, f"{base_name}_binary.png"))
    Image.fromarray(make_overlay(rgb, prob)).save(
        os.path.join(args.output_dir, f"{base_name}_overlay.png"))
    Image.fromarray(morph_dict["morph_enhanced"]).save(
        os.path.join(args.output_dir, f"{base_name}_morph.png"))

    print(f"  Outputs saved to: {args.output_dir}/")
    print(f"    {base_name}_prob.png, _binary.png, _overlay.png, _morph.png")
    vessel_pct = binary.sum() / (binary.size * 255) * 100
    print(f"  Vessel coverage: {vessel_pct:.2f}% | Max prob: {prob.max():.4f}\n")

if __name__ == "__main__":
    predict(parse_args())
