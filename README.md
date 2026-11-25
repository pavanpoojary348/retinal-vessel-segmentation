# Automated Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Benchmark: DRIVE](https://img.shields.io/badge/Dataset-DRIVE-green.svg)](https://drive.grand-challenge.org/)

**Course:** Fundamentals of Image Processing (FIP)  
**Institution:** NMAM Institute of Technology, Nitte (Nitte Deemed to be University, Karnataka, India)  
**Department:** Information Science & Engineering  

**Team Members:**  
1. **Krithin Kusharaj Salian** (USN: `NNM24IS110`)  
2. **Niriksha** (USN: `NNM24IS141`)  
3. **Pavan L Poojary** (USN: `NNM24IS149`)  

---

## 📌 Project Overview

This repository contains the complete implementation of **Morph-ViT**, a hybrid medical image segmentation framework that combines **classical mathematical morphology (Units II & III syllabus)** with a **deep Vision Transformer (ViT)** to segment blood vessels from retinal fundus photographs on the public **DRIVE benchmark**.

Eye clinicians examine retinal blood vessels non-invasively to detect **Diabetic Retinopathy** (the leading cause of adult blindness), **Hypertension**, and **Glaucoma**. Manual tracing takes **1 to 2 hours per scan**. Our automated system accomplishes this in **1.09 seconds** per image with state-of-the-art accuracy.

```
Raw RGB Fundus ──► Green Channel ──► CLAHE ──► 12-Directional Top-Hat (15 px)
       │                                                    │
       └─────────────────────────┬──────────────────────────┘
                                 ▼
                     4-Channel Input [R, G, B, Morph]
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
             CNN Stem                     Patch Tokenizer (16x16)
          (Fine Capillaries)                     │
                 │                        4-Layer ViT Encoder
                 │                      (Self-Attention Continuity)
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                       Skip-Decoder Network
                                 │
                  Connected-Component Speck Filter (<= 10 px)
                                 ▼
              Clean Binary Vessel Mask & Green Doctor Overlay
```

---

## 🏆 Benchmark Comparative Results (DRIVE Dataset)

All metrics are evaluated **strictly inside the circular Field of View (FOV) mask** per international medical benchmark standards:

| Evaluation Metric | Traditional Image Processing (Top-Hat + CLAHE) | Standard ML/DL Baseline (U-Net, 2015) | Proposed Hybrid Technique (Morph-ViT) |
|---|:---:|:---:|:---:|
| **Accuracy** | 89.63% | 88.60% | **92.35% (Highest)** |
| **Dice Score (F1)** | 64.14% | 72.38% | **77.79% (+13.65% over Trad)** |
| **IoU (Jaccard Index)** | 47.21% | 56.71% | **63.66% (Highest)** |
| **Precision** | **81.19%** | 62.81% | 79.09% |
| **Recall (Sensitivity)** | 53.00% | **85.38%** | 76.54% (+23.54% over Trad) |
| **Specificity** | **97.40%** | 89.28% | 95.71% |
| **AUC-ROC** | 75.20% | 94.45% | **94.94% (Highest)** |
| **Inference Time** | **177.4 ms** | 671.7 ms | 1,099 ms (CPU) |
| **Model Size** | **0.00 MB** (Algorithmic) | 1.88 MB | 3.29 MB (Compact) |
| **Parameters** | **0** | 482,737 | 862,049 |

---

## 🚀 Quick Start Guide (Run on Any PC)

Follow these simple steps to set up and run this project on Windows, macOS, or Linux.

### 1. Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Bash) and clone the repo:
```bash
git clone https://github.com/pavanpoojary348/retinal-vessel-segmentation.git
cd retinal-vessel-segmentation
```

### 2. Set Up a Python Virtual Environment
We recommend **Python 3.10, 3.11, or 3.12**:

* **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install all required libraries with a single command:
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Code

### 1. Test a Single Retinal Image (Takes 2 Seconds)
Run inference on any image using our pre-trained model:
```bash
python src/predict.py --image data/raw/training/images/21_training.tif
```
**Outputs generated in `outputs/predictions/`:**
* `21_training_morph.png` $\to$ 12-directional Top-Hat morphological prior map
* `21_training_prob.png` $\to$ AI probability heatmap (continuous confidence 0% to 100%)
* `21_training_binary.png` $\to$ Final clean black-and-white vessel mask ($T=0.65$, specks removed)
* `21_training_overlay.png` $\to$ Clinical green vessel overlay on top of the patient's eye

---

### 2. Run the 3-Way Comparative Benchmark Table
Reproduce the mandatory course results table comparing Traditional, U-Net, and Morph-ViT:
```bash
python src/evaluate_all_three.py
```
This prints the comparison table to the terminal and exports `outputs/comparative_results_table.csv`.

---

### 3. Generate 4-Color Diagnostic Error Maps
Generate visual error panels showing True Positives (Green), False Negatives (Red), and False Positives (Blue):
```bash
python src/visualise_error_maps.py
```
Open `outputs/error_maps/21_training_error_panel.png` to inspect the visual breakdown.

---

### 4. Run the Ablation Study
Measure the isolated contribution of each component:
```bash
python src/ablation.py
```

---

### 5. Launch the Interactive Jupyter Demo
Step through the entire pipeline interactively:
```bash
jupyter notebook demo.ipynb
```

---

### 6. Train Models from Scratch (Optional)
To retrain the models:
* **Train Morph-ViT:**
  ```bash
  python src/train.py --epochs 15 --batch_size 2
  ```
* **Train U-Net Baseline:**
  ```bash
  python src/train_unet.py --epochs 15 --batch_size 2
  ```

---

## 📂 Repository File Structure

```
retinal-vessel-segmentation/
│
├── data/raw/                             --> DRIVE Dataset Benchmark
│   ├── training/                         --> 20 Training fundus images + 1st_manual + masks
│   └── test/                             --> 20 Test fundus images + masks
│
├── src/                                  --> Core Source Code
│   ├── morphology.py                     --> Green channel, CLAHE & 12-Angle Top-Hat (Units II & III)
│   ├── dataset.py                        --> DRIVE data loader & 4-channel tensor preparation
│   ├── metrics.py                        --> Accuracy, Dice, IoU, Recall, Precision inside FOV
│   ├── postprocess.py                    --> Connected-component speck filter (<= 10 px)
│   ├── train.py                          --> Training loop for Morph-ViT (DiceBCE Loss)
│   ├── train_unet.py                     --> Training loop for U-Net baseline
│   ├── evaluate.py                       --> Evaluation of Morph-ViT
│   ├── evaluate_all_three.py             --> Mandatory 3-way comparative benchmark table
│   ├── ablation.py                       --> Component isolation & ablation study
│   ├── predict.py                        --> Single-image clinical inference engine
│   ├── visualise.py                      --> Diagnostic training curve plotting
│   ├── visualise_error_maps.py           --> 4-color error map generator
│   │
│   └── models/                           --> Neural Network Architectures
│       ├── morph_vit.py                  --> Proposed Morph-ViT (CNN Stem + ViT + Skip Decoder)
│       └── unet.py                       --> Standard Biomedical U-Net Baseline
│
├── outputs/                              --> Generated Outputs & Checkpoints
│   ├── checkpoints/                      --> Trained weights (best_model.pth, unet_best.pth)
│   ├── comparative_results_table.csv     --> Final evaluation numbers
│   ├── training_curves.png               --> Loss, Dice, and AUC convergence graphs
│   ├── error_maps/                       --> Visual 4-color error map panels
│   └── predictions/                      --> Segmented masks and green clinical overlays
│
├── presentation_simple.pptx              --> Simple 7-slide oral presentation deck
├── PRESENTATION_SPEECH_GUIDE.md          --> 30-second speaking script for every slide
├── abstract.pdf / abstract.docx          --> 1-page paper abstract with team credentials
├── REPORT_DATA_AND_CLAUDE_PROMPT.pdf     --> Report data pack with <20% AI detection prompt
├── main.py                               --> Unified CLI entry point
└── requirements.txt                      --> Python package dependencies
```

---

## 🔬 Scientific Methodology

### 1. Classical Morphology (Units II & III Syllabus)
* **Spectral Green Channel:** Hemoglobin absorption peaks at $540\text{–}580\text{ nm}$, providing maximum contrast against the choroid.
* **CLAHE:** Equalizes spherical illumination with an $8 \times 8$ tile grid and clip limit $\beta = 2.0$.
* **12-Directional Linear Top-Hat:** Uses a straight-line structuring element ($l = 15\text{ px}$) rotated across 12 angles $\theta \in \{0^\circ, 15^\circ, \dots, 165^\circ\}$:
  $$\text{WTH}_\theta(I_{\text{inv}}) = I_{\text{inv}} - (I_{\text{inv}} \circ L_{\theta, l})$$
  $$M(x, y) = \max_{\theta} \left[ \text{WTH}_\theta(I_{\text{inv}})(x, y) \right]$$

### 2. Morph-ViT Neural Architecture
* **4-Channel Input:** $\mathbf{X} \in \mathbb{R}^{B \times 4 \times 576 \times 576} = [R, G, B, M]$
* **CNN High-Resolution Stem:** Two $3 \times 3$ Conv layers preserve fine microcapillary edge gradients.
* **Vision Transformer Encoder:** 4 layers of Multi-Head Self-Attention ($4$ heads, $128$ embedding dimensions, $1,296$ tokens) model long-range vascular tree continuity.
* **Progressive Skip-Decoder:** Upsamples features back to full resolution and fuses them with CNN stem features.

### 3. Connected-Component Speck Filter
* Discards isolated false-positive noise islands smaller than $10\text{ pixels}$, boosting final precision to **$79.09\%$**.

---

## 📚 Key Literature References

1. **J. Staal, M. D. Abramoff, M. Niemeijer, M. A. Viergever, and B. van Ginneken**, *"Ridge-based vessel segmentation in color images of the retina,"* IEEE Transactions on Medical Imaging, vol. 23, no. 4, pp. 501–509, 2004.
2. **A. Dosovitskiy et al.**, *"An image is worth 16x16 words: Transformers for image recognition at scale,"* International Conference on Learning Representations (ICLR), 2021.
3. **O. Ronneberger, P. Fischer, and T. Brox**, *"U-Net: Convolutional networks for biomedical image segmentation,"* in Proc. MICCAI, Springer, 2015, pp. 234–241.
4. **J. Serra**, *Image Analysis and Mathematical Morphology*, Academic Press, London, 1982.
5. **S. M. Pizer et al.**, *"Adaptive histogram equalization and its variations,"* Computer Vision, Graphics, and Image Processing, vol. 39, no. 3, pp. 355–368, 1987.
6. **M. M. Fraz et al.**, *"Blood vessel segmentation methodologies in retinal images – A survey,"* Computer Methods and Programs in Biomedicine, vol. 108, no. 1, pp. 407–433, 2012.

---

## 📄 License
This project is developed for academic evaluation under the B.Tech program at **NMAM Institute of Technology, Nitte**. Code is open for research and educational purposes.
