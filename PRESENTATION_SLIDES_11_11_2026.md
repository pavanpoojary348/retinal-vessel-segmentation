# RETINAL BLOOD VESSEL SEGMENTATION USING MATHEMATICAL MORPHOLOGY AND VISION TRANSFORMERS (Morph-ViT)
**First Review Presentation — 11/11/2026**  
**Course:** Fundamentals of Image Processing (FIP)  
**Slide Deck:** 7 Slides (Maximum Allowed)  

---

## SLIDE 1: Title & Project Overview

### Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)
**A Comparative Study on the DRIVE Benchmark**

* **Course:** Fundamentals of Image Processing (FIP)
* **Department:** Department of Computer Science & Engineering
* **Team Members:**
  1. Krithin Kusharaj Salian (`NNM24IS110`)
  2. Niriksha (`NNM24IS141`)
  3. Pavan L Poojary (`NNM24IS149`)
* **Review Dates:** Review 1: 11/11/2026 | Final Evaluation: 24/11/2026

**Project Focus:**
Synthesizing classical image processing techniques from **Unit II (Spatial Image Enhancement)** and **Unit III (Morphological Image Processing)** with **Deep Vision Transformers (ViT)** to solve low-contrast microvascular segmentation under extreme class imbalance.

---

## SLIDE 2: Abstract & Problem Formulation

### Abstract
Automated retinal vessel segmentation provides vital diagnostic biomarkers for **Diabetic Retinopathy**, **Hypertension**, and **Glaucoma**. Manual delineation is tedious and subjective. 

### Core Image Processing Challenges:
1. **Low Contrast & Peripheral Vignetting:** Spherical fundus geometry causes non-uniform illumination and dim microcapillaries.
2. **Severe Class Imbalance:** Vessel pixels account for only $\sim 10\%$ of retinal area, while non-vessel background accounts for $\sim 90\%$.
3. **Confounding Anatomical Structures:** High-contrast optic disc margins, exudates, and drusen trigger false positives in simple edge detectors.

### Proposed Solution:
A hybrid framework (**Morph-ViT**) that integrates:
- **Green channel optical absorption physics**
- **Contrast-Limited Adaptive Histogram Equalization (CLAHE)**
- **Multi-directional Linear Top-Hat morphological filtering (12 orientations)**
- **Vision Transformer self-attention** for global vascular topological continuity
- **Connected-component morphological filtering** for artifact suppression.

---

## SLIDE 3: Dataset & Ground Truth Validation

### DRIVE Benchmark (Digital Retinal Images for Vessel Extraction)
* **Source:** Publicly available benchmark acquired with a Canon CR5 3CCD fundus camera ($45^\circ$ Field of View, $768 \times 584$ native resolution).
* **Ground-Truth Masks:** Delineated by ophthalmological experts (First Manual).
* **Field of View (FOV) Masks:** Explicit binary masks; all evaluations are conducted **strictly inside the FOV** per DRIVE protocol.
* **Standard Resolution:** Normalized to $576 \times 576$ (divisible by patch size $P=16 \implies 1,296$ tokens).

### Data Distribution:
* **Training Set:** 20 images (`21_training.tif` to `40_training.tif`) with expert ground truth.
* **Test Set:** 20 images (`01_test.tif` to `20_test.tif`) for inference and generalization testing.

---

## SLIDE 4: Proposed Methodology & Architecture

```
                                  PROPOSED Morph-ViT PIPELINE
                                  ===========================
[Input RGB Fundus] ─────────────┬────────────────────────────────────────────────────────┐
                                │                                                        │
                                ▼                                                        │
                      [Green Channel Extraction] (Peak Hemoglobin Absorption)           │
                                │                                                        │
                                ▼                                                        │
                        [CLAHE Equalization] (8x8 grid, clip=2.0)                        │
                                │                                                        │
                                ▼                                                        │
                  [Multi-Directional Top-Hat] (12 orientations 0° to 165°, length=15)    │
                                │                                                        │
                                ▼                                                        │
                     [Normalized Morph Feature]                                          │
                                │                                                        │
                                └─────────────────────────┬──────────────────────────────┘
                                                          │
                                                          ▼
                                            [4-Channel Tensor: R, G, B, Morph]
                                                          │
                                       ┌──────────────────┴──────────────────┐
                                       ▼                                     ▼
                            [CNN High-Res Stem]                     [ViT Patch Embedding]
                           (3x3 Conv -> BN -> ReLU)                  (16x16 -> 128-dim tokens)
                                       │                                     │
                                       │                                     ▼
                                       │                       [Transformer Encoder (4 layers)]
                                       │                        (MHSA, 4 heads + GELU MLP)
                                       │                                     │
                                       │                                     ▼
                                       │                         [2D Feature Reshaping]
                                       │                                     │
                                       │                        [Decoder Stages 1 & 2 (2x up)]
                                       │                                     │
                                       └──────────────────┬──────────────────┘
                                                          ▼
                                               [Decoder Stage 3 + Skip]
                                                          │
                                                          ▼
                                                  [Final 1x1 Conv]
                                                          │
                                                          ▼
                                                [Sigmoid Probability]
                                                          │
                                                          ▼
                                     [Calibrated Threshold T=0.65 + Speck Filter]
                                                          │
                                                          ▼
                                                [Final Vessel Mask]
```

### Key Mathematical Formulations:
1. **White Top-Hat Transform:** $\text{WTH}_\theta(I_{\text{inv}}) = I_{\text{inv}} - (I_{\text{inv}} \circ L_{\theta, l})$
2. **Directional Supremum:** $M(x, y) = \max_{\theta \in \{0^\circ, \dots, 165^\circ\}} \text{WTH}_\theta(I_{\text{inv}})$
3. **Imbalance-Aware Loss:** $\mathcal{L} = \mathcal{L}_{\text{BCE}}(w_{\text{pos}} = 4.0) + \mathcal{L}_{\text{Dice}}$

---

## SLIDE 5: Six Mandatory Comparative Experiments

Our project addresses all 6 experiments mandated by the course guidelines:

1. **Experiment 1 (Traditional Image Processing):**
   * Multi-directional Top-Hat filtering with linear structuring elements + CLAHE + Percentile Thresholding (Syllabus: Units II & III).
2. **Experiment 2 (ML/DL-Based Technique):**
   * Standard U-Net (Ronneberger et al., 2015) trained on 3-channel RGB.
3. **Experiment 3 (Proposed Hybrid Advanced Technique):**
   * Morph-ViT combining physics-based Top-Hat, CNN stem, and Vision Transformer self-attention.
4. **Experiment 4 (Hyperparameter Tuning):**
   * Systematic sweep across Decision Thresholds ($T \in [0.30, 0.70]$), Structuring Element Length ($l \in \{9, 15, 21\}$), and Min-Speck Area ($\le 10\text{ px}$).
5. **Experiment 5 (Ablation Study):**
   * Evaluating pure morphology vs. pure ViT vs. uncalibrated Morph-ViT vs. full post-processed Morph-ViT.
6. **Experiment 6 (Performance Comparison):**
   * Execution time (ms/image), model storage footprint (MB), parameter count, and all clinical classification metrics.

---

## SLIDE 6: Visual Comparison & Error Map Analysis

*(Include screenshots of `outputs/error_maps/21_training_error_panel.png` and `outputs/predictions/01_test_overlay.png`)*

### Qualitative Visual Grid:
* **(a) Input RGB Fundus Image:** Real patient retina from DRIVE dataset.
* **(b) Ground Truth (Expert 1st Manual):** Ophthalmologist manual tracing.
* **(c) Traditional Morphology Result:** Clear main vessels, but thin capillaries are broken.
* **(d) Proposed Morph-ViT Result:** Continuous, unbroken microvascular network.
* **(e) Color-Coded Error Map (Ground Truth vs. Prediction):**
  - 🟩 **Green (True Positive):** Correctly detected vessel segments.
  - 🟥 **Red (False Negative):** Missed vessels (drastically reduced from $47.0\%$ in traditional to only $23.4\%$ in Morph-ViT).
  - 🟦 **Blue (False Positive):** False alarms (suppressed via connected-component filtering).
  - ⬛ **Black (True Negative):** Background properly excluded inside FOV.

---

## SLIDE 7: Common Results Table & References

### Mandatory Reporting Format Table (Evaluated strictly inside FOV on DRIVE):

| Evaluation Metric | Traditional Method (Morphology) | ML/DL Method (Standard U-Net) | Proposed Method (Morph-ViT) |
|:---|:---:|:---:|:---:|
| **Accuracy** | 89.63% | 90.45% | **92.35%** |
| **Dice Score (F1)** | 64.14% | 72.80% | **77.79%** |
| **IoU (Jaccard Index)** | 47.21% | 57.23% | **63.65%** |
| **Precision** | **81.19%** | 73.15% | **79.09%** |
| **Recall (Sensitivity)** | 53.00% | 72.46% | **76.54%** |
| **Specificity** | **97.40%** | 94.10% | **95.71%** |
| **AUC-ROC** | 75.20% | 91.80% | **94.88%** |
| **Execution Time** | **38 ms/image** | 58 ms/image | **42 ms/image** |
| **Model Size** | **0.0 MB (algorithmic)** | 7.35 MB (1.92M params) | **0.95 MB (247K params)** |

### Key Conclusion:
* Morph-ViT outperforms both the traditional baseline (+13.65% Dice) and standard U-Net (+4.99% Dice) while having **8× fewer parameters** than U-Net.
* Demonstrates that classical morphological priors dramatically accelerate and enhance Transformer attention.

### Key References:
1. J. Staal et al., "Ridge-based vessel segmentation in color images of the retina," *IEEE TMI*, 23(4):501-509, 2004.
2. A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," *ICLR*, 2021.
3. O. Ronneberger et al., "U-Net: Convolutional networks for biomedical image segmentation," *MICCAI*, pp. 234-241, 2015.
4. J. Serra, *Image Analysis and Mathematical Morphology*, Academic Press, 1982.

