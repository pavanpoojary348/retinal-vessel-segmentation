# Retinal Blood Vessel Segmentation using Morphology and Vision Transformers

**FIP (Fundamental of Image Processing) Course Project**

A hybrid deep learning pipeline that combines **classical mathematical morphology** with **Vision Transformers (ViT)** for robust retinal blood vessel segmentation on the [DRIVE dataset](https://drive.grand-challenge.org/).

---

## Overview

| Component | Description |
|---|---|
| **Dataset** | DRIVE — 20 training + 20 test fundus images at 565×584px |
| **Model** | Morph-ViT: CNN stem + 4-layer ViT encoder + convolutional decoder |
| **Input** | 4 channels: RGB fundus + morphological Top-Hat feature |
| **Loss** | Combined DiceBCE (handles 10% vessel / 90% background imbalance) |
| **Metrics** | Dice, IoU, Sensitivity, Specificity, Accuracy, AUC-ROC, Precision (inside FOV) |

---

## Architecture: Morph-ViT

```
RGB Fundus (3ch)
      │
      ├─► Green Channel ─► CLAHE ─► Multi-Dir Top-Hat (12 angles) ─► Morph Feature (1ch)
      │
      └─► Normalize to [0,1]
                │
                └──────────────────────────────────────────────────────┐
                                                                        ▼
                                                        4-Channel Input (B, 4, H, W)
                                                            │           │
                                                 ┌──────────┘           │
                                                 ▼                      ▼
                                           CNN Stem                Patch Embed
                                        (3×3 Conv ×2)             (16×16 → 128d)
                                           skip feat                    │
                                                                 Positional Enc
                                                                        │
                                                              Transformer Encoder
                                                              (4× MHSA + MLP)
                                                                        │
                                                              Reshape → 2D feat
                                                                        │
                                                              Decoder Block 1 (2×up)
                                                                        │
                                                              Decoder Block 2 (2×up)
                                                                        │
                                                 ┌──────────────────────┘
                                                 ▼
                                      Decoder Block 3 (+ skip from CNN Stem)
                                                 │
                                           Final Conv (1×1)
                                                 │
                                           Sigmoid → Vessel Probability Map
```

---

## Directory Structure

```
retinal-vessel-segmentation/
├── data/raw/
│   ├── training/
│   │   ├── images/        21_training.tif … 40_training.tif
│   │   ├── 1st_manual/    21_manual1.gif  … 40_manual1.gif    (ground truth)
│   │   └── mask/          21_training_mask.gif … 40_training_mask.gif
│   └── test/
│       ├── images/        01_test.tif … 20_test.tif
│       └── mask/          01_test_mask.gif … 20_test_mask.gif
├── src/
│   ├── dataset.py         DRIVE dataset loader
│   ├── morphology.py      Morphological preprocessing (CLAHE + Top-Hat)
│   ├── metrics.py         7 evaluation metrics (FOV-masked)
│   ├── train.py           Training loop
│   ├── evaluate.py        Full evaluation + CSV report
│   ├── predict.py         Single-image inference
│   ├── ablation.py        Morphology-only vs Morph-ViT comparison
│   ├── visualise.py       Training curves, sample panels, ROC
│   └── models/
│       └── morph_vit.py   Morph-ViT model definition
├── outputs/
│   ├── checkpoints/       best_model.pth, last_model.pth
│   ├── train_log.csv      per-epoch metric history
│   ├── results/           predicted masks + evaluation_report.csv
│   ├── panels/            visualisation panel PNGs
│   └── ablation_results.csv
├── main.py                unified CLI entry point
└── requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:** `torch>=2.0`, `torchvision`, `numpy`, `scipy`, `scikit-learn`,
`scikit-image`, `opencv-python`, `pillow`, `matplotlib`, `seaborn`, `tqdm`, `einops`, `tabulate`

---

## Usage

### Train
```bash
python main.py train                              # 40 epochs, default hyperparameters
python main.py train --epochs 60 --batch_size 2 --lr 1e-4 --patch_size 8
python main.py train --resume outputs/checkpoints/last_model.pth
```

### Evaluate (requires ground truth — training split)
```bash
python main.py evaluate
python main.py evaluate --threshold 0.45
```

### Predict (single image)
```bash
python main.py predict --image data/raw/test/images/01_test.tif \
                       --fov   data/raw/test/mask/01_test_mask.gif
```

### Ablation study (morphology-only vs Morph-ViT)
```bash
python src/ablation.py
```

### Visualise training curves + sample panels
```bash
python main.py visualise
```

### Full pipeline
```bash
python main.py all
```

---

## Hyperparameters

| Parameter | Default | Description |
|---|---|---|
| `--img_size` | 576 | Resize all images to N×N (divisible by patch_size) |
| `--patch_size` | 16 | ViT patch size (8 or 16) |
| `--embed_dim` | 128 | Transformer embedding dimension |
| `--depth` | 4 | Number of Transformer encoder blocks |
| `--num_heads` | 4 | Multi-Head Self-Attention heads |
| `--mlp_ratio` | 2.0 | MLP hidden dimension ratio |
| `--dropout` | 0.1 | Dropout probability |
| `--pos_weight` | 4.0 | BCE positive class weight |
| `--dice_weight` | 1.0 | Dice loss contribution |
| `--epochs` | 40 | Training epochs |
| `--batch_size` | 2 | Batch size |
| `--lr` | 3e-4 | Initial learning rate (AdamW) |
| `--morph_kernel` | 15 | Top-Hat structuring element length |

---

## Results

**Best checkpoint: Epoch 36 (40 epochs, 576×576, patch=16, embed=128, depth=4)**

| Method | Dice | IoU | Sensitivity | Specificity | Accuracy | AUC-ROC |
|---|---|---|---|---|---|---|
| Morphology-Only baseline | ~0.72 | ~0.56 | ~0.75 | ~0.96 | ~0.93 | — |
| **Morph-ViT (ours)** | **0.7658** | **0.6212** | **0.8232** | **0.9310** | **0.9122** | **0.9494** |

> All metrics evaluated strictly inside the Field of View (FOV) mask per DRIVE benchmark protocol.

---

## Morphological Preprocessing Pipeline

1. **Green Channel Extraction** — hemoglobin absorbs green light; highest vessel contrast
2. **CLAHE** (Contrast-Limited Adaptive Histogram Equalization) — normalizes local illumination
3. **Multi-Directional Top-Hat** — 12 orientations (0°–165° in 15° steps) with linear structuring elements
4. **Max Response** — supremum across all directional Top-Hat responses

---

## Citation / References

- DRIVE Dataset: Staal et al., "Ridge-Based Vessel Segmentation," IEEE TMI 2004
- Vision Transformer: Dosovitskiy et al., "An Image is Worth 16×16 Words," ICLR 2021
- Morphological Methods: Serra, "Image Analysis and Mathematical Morphology," 1982
