"""
Retinal Blood Vessel Segmentation - DRIVE Dataset Loader
=========================================================
Fundamental of Image Processing (FIP) Course Project

Loads and preprocesses the DRIVE (Digital Retinal Images for Vessel Extraction) dataset:
- 20 training images (21-40) with ground-truth vessel masks and FOV masks
- 20 test images  (01-20) with FOV masks (no ground-truth masks released for public)

Each sample returns:
  - input_tensor : (4, H, W) float32 -- 3 RGB channels + 1 morphological channel
  - label_tensor : (1, H, W) float32 -- binary vessel mask
  - fov_tensor   : (1, H, W) float32 -- field-of-view mask (1 = valid retinal pixel)
  - image_id     : str -- e.g. "21_training"
"""

import os
import glob
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader

import sys
sys.path.insert(0, os.path.dirname(__file__))
from morphology import enhance_retinal_vessels

DEFAULT_IMG_SIZE = (576, 576)   # divisible by 16 and 8 patch sizes


def load_image(path, size=None, mode="RGB"):
    """Load an image file (TIF/GIF/PNG/JPG) and return a uint8 numpy array."""
    img = Image.open(path).convert(mode)
    if size is not None:
        img = img.resize((size[1], size[0]), Image.BILINEAR)
    return np.array(img, dtype=np.uint8)


class DRIVEDataset(Dataset):
    """
    PyTorch Dataset for the DRIVE retinal vessel segmentation benchmark.

    Directory structure expected (standard DRIVE layout):
        data/raw/
            training/
                images/        21_training.tif ... 40_training.tif
                1st_manual/    21_manual1.gif  ... 40_manual1.gif
                mask/          21_training_mask.gif ... 40_training_mask.gif
            test/
                images/        01_test.tif ... 20_test.tif
                mask/          01_test_mask.gif ... 20_test_mask.gif
    """

    def __init__(self, root_dir, split="training", img_size=DEFAULT_IMG_SIZE,
                 augment=False, morph_kernel=15):
        assert split in ("training", "test"), f"split must be training or test, got {split}"
        self.split = split
        self.img_size = img_size
        self.augment = augment
        self.morph_kernel = morph_kernel

        split_dir = os.path.join(root_dir, split)
        img_dir   = os.path.join(split_dir, "images")
        mask_dir  = os.path.join(split_dir, "mask")
        label_dir = os.path.join(split_dir, "1st_manual") if split == "training" else None

        img_paths = sorted(glob.glob(os.path.join(img_dir, "*.tif")))
        if not img_paths:
            raise FileNotFoundError(f"No .tif images found in {img_dir}")

        self.samples = []
        for img_path in img_paths:
            base = os.path.splitext(os.path.basename(img_path))[0]
            num  = base.split("_")[0]

            fov_name = f"{num}_training_mask.gif" if split == "training" else f"{num}_test_mask.gif"
            fov_path = os.path.join(mask_dir, fov_name)
            if not os.path.exists(fov_path):
                print(f"[WARN] FOV mask not found: {fov_path}")
                continue

            lbl_path = None
            if label_dir is not None:
                lbl_name = f"{num}_manual1.gif"
                lbl_path = os.path.join(label_dir, lbl_name)
                if not os.path.exists(lbl_path):
                    print(f"[WARN] Label not found: {lbl_path}")
                    continue

            self.samples.append({
                "image_id": base,
                "img_path": img_path,
                "fov_path": fov_path,
                "lbl_path": lbl_path,
            })

        if not self.samples:
            raise RuntimeError(f"Dataset is empty for split={split!r} in {root_dir}")

        print(f"[DRIVEDataset] Split={split!r} | {len(self.samples)} samples | img_size={img_size}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        H, W   = self.img_size

        rgb = load_image(sample["img_path"], size=self.img_size, mode="RGB")
        fov = load_image(sample["fov_path"], size=self.img_size, mode="L")

        morph_dict = enhance_retinal_vessels(rgb, fov_mask=fov, kernel_size=self.morph_kernel)
        morph_ch   = morph_dict["normalized"].astype(np.float32)

        rgb_norm   = rgb.astype(np.float32) / 255.0
        rgb_t      = torch.from_numpy(rgb_norm).permute(2, 0, 1)
        morph_t    = torch.from_numpy(morph_ch).unsqueeze(0)
        input_tensor = torch.cat([rgb_t, morph_t], dim=0)

        if sample["lbl_path"] is not None:
            lbl   = load_image(sample["lbl_path"], size=self.img_size, mode="L")
            lbl_bin = (lbl > 0).astype(np.float32)
        else:
            lbl_bin = np.zeros((H, W), dtype=np.float32)
        label_tensor = torch.from_numpy(lbl_bin).unsqueeze(0)

        fov_bin    = (fov > 0).astype(np.float32)
        fov_tensor = torch.from_numpy(fov_bin).unsqueeze(0)

        if self.augment:
            input_tensor, label_tensor, fov_tensor = self._augment(input_tensor, label_tensor, fov_tensor)

        return {
            "input":    input_tensor,
            "label":    label_tensor,
            "fov":      fov_tensor,
            "image_id": sample["image_id"],
        }

    def _augment(self, x, y, fov):
        import random
        if random.random() > 0.5:
            x   = torch.flip(x,   dims=[2])
            y   = torch.flip(y,   dims=[2])
            fov = torch.flip(fov, dims=[2])
        if random.random() > 0.5:
            x   = torch.flip(x,   dims=[1])
            y   = torch.flip(y,   dims=[1])
            fov = torch.flip(fov, dims=[1])
        return x, y, fov


def get_dataloaders(data_root, img_size=DEFAULT_IMG_SIZE, batch_size=2,
                    num_workers=0, morph_kernel=15):
    """Build training and test DataLoaders."""
    train_ds = DRIVEDataset(root_dir=data_root, split="training",
                            img_size=img_size, augment=True, morph_kernel=morph_kernel)
    test_ds  = DRIVEDataset(root_dir=data_root, split="test",
                            img_size=img_size, augment=False, morph_kernel=morph_kernel)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, pin_memory=torch.cuda.is_available(),
                              drop_last=False)
    test_loader  = DataLoader(test_ds, batch_size=1, shuffle=False,
                              num_workers=num_workers, pin_memory=torch.cuda.is_available())
    return train_loader, test_loader


if __name__ == "__main__":
    import sys
    root   = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    ds     = DRIVEDataset(root_dir=root, split="training", img_size=(576, 576), augment=True)
    sample = ds[0]
    print(f"image_id: {sample['image_id']}")
    print(f"input   : {sample['input'].shape}  min={sample['input'].min():.3f}  max={sample['input'].max():.3f}")
    print(f"label   : {sample['label'].shape}  vessel%={sample['label'].mean()*100:.2f}%")
    print(f"fov     : {sample['fov'].shape}   valid%={sample['fov'].mean()*100:.2f}%")
