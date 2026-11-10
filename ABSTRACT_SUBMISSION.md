# PROJECT ABSTRACT SUBMISSION

**Course:** Fundamentals of Image Processing (FIP)  
**Date of Submission:** 11/11/2026  
**Department:** Department of Computer Science & Engineering  
**Project Title:** Automated Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)  
**Dataset:** DRIVE (Digital Retinal Images for Vessel Extraction) Benchmark  

**Team Members:**  
1. **KRITHIN KUSHARAJ SALIAN** (USN: `NNM24IS110`)  
2. **NIRIKSHA** (USN: `NNM24IS141`)  
3. **PAVAN L POOJARY** (USN: `NNM24IS149`)  

---

## Abstract

Automated segmentation of the retinal vascular tree from fundus photographs is a critical prerequisite for the computerized screening of ophthalmic and systemic pathologies, including Diabetic Retinopathy, Arteriosclerosis, Hypertension, and Glaucoma. The task presents severe image processing challenges: microvascular capillaries possess low local contrast, fundus images suffer from spherical illumination gradients, and vessel pixels exhibit an extreme $\sim 10:90$ class imbalance against the background retinal pigment epithelium.

In this work, we propose **Morph-ViT**, a hybrid architecture that synergistically combines classical mathematical morphology with deep Vision Transformers (ViT). The methodology proceeds through four stages:
1. **Domain-Specific Spectral & Spatial Preprocessing:** Hemoglobin exhibits peak optical absorption in the green spectrum ($\sim 540$–$580\text{ nm}$); hence, the green channel is isolated and equalized via Contrast-Limited Adaptive Histogram Equalization (CLAHE) with an $8 \times 8$ grid.
2. **Multi-Directional Linear Top-Hat Filtering:** To trace vessels of arbitrary orientation, a linear structuring element of length $l = 15$ pixels is rotated across 12 discrete angles ($\theta = 0^\circ, 15^\circ, \dots, 165^\circ$). The supremum of white Top-Hat responses is computed to isolate vascular ridges.
3. **Deep Self-Attention & Boundary Recovery:** The morphological feature is concatenated with normalized RGB channels to form a 4-channel tensor $\mathbf{X} \in \mathbb{R}^{B \times 4 \times 576 \times 576}$. A dual-convolutional CNN stem captures high-resolution edge geometry, while a 4-layer Multi-Head Self-Attention (MHSA) Vision Transformer encoder models long-range topological vessel continuity. A progressive convolutional decoder with stem skip connections reconstructs vessel boundaries.
4. **Morphological Post-Processing:** Calibrated decision thresholding ($T = 0.65$) and connected-component analysis eliminate isolated false-positive noise islands ($< 10\text{ px}$).

### Experimental Results on the DRIVE Benchmark:
Evaluated strictly inside the Field of View (FOV), the proposed Morph-ViT achieves:
- **Accuracy:** **92.35%** (vs. 89.63% for classical morphology, **+2.72%** gain)
- **AUC-ROC:** **0.9488** (vs. 0.7520 for classical morphology, **+19.68%** gain)
- **Dice Similarity Coefficient (F1):** **77.79%** (vs. 64.14% for classical morphology, **+13.65%** gain)
- **Sensitivity (Vessel Recall):** **76.54%** (vs. 53.00% for classical morphology, **+23.54%** gain)
- **Specificity:** **95.71%** | **Precision:** **79.09%** | **Model Parameters:** **247,201** ($\sim 9.98\text{ MB}$)

The results demonstrate that injecting domain-specific morphological prior knowledge into attention-based architectures substantially improves microvessel recall while maintaining a compact, real-time computational footprint.

---

## Key References

1. J. Staal, M. D. Abramoff, M. Niemeijer, M. A. Viergever, and B. van Ginneken, "Ridge-based vessel segmentation in color images of the retina," *IEEE Transactions on Medical Imaging*, vol. 23, no. 4, pp. 501–509, 2004.
2. A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," *International Conference on Learning Representations (ICLR)*, 2021.
3. O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical image segmentation," in *Proc. MICCAI*, Springer, 2015, pp. 234–241.
4. J. Serra, *Image Analysis and Mathematical Morphology*, Academic Press, London, 1982.
5. S. M. Pizer et al., "Adaptive histogram equalization and its variations," *Computer Vision, Graphics, and Image Processing*, vol. 39, no. 3, pp. 355–368, 1987.

