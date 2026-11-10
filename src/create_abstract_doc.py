"""
Generate Professional 1-Page Abstract Submissions:
- abstract.docx (Microsoft Word)
- abstract.html (Clean printable web layout)
- abstract.pdf  (High-resolution print-ready PDF via headless browser)
========================================================================
Review 1 Submission Date: 11/11/2026
Course: Fundamentals of Image Processing (FIP)
"""

import os
import subprocess
import zipfile

def generate_html_and_pdf(proj_dir: str):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Course Project Abstract — Morph-ViT</title>
<style>
  @page {
    size: A4 portrait;
    margin: 15mm 18mm 15mm 18mm;
  }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 10.5pt;
    line-height: 1.35;
    color: #111;
    margin: 0 auto;
    max-width: 800px;
    padding: 10px 20px;
  }
  .header-banner {
    text-align: center;
    border-bottom: 2px solid #0e223d;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }
  .course-tag {
    font-family: Arial, sans-serif;
    font-size: 9pt;
    font-weight: bold;
    color: #0e223d;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  h1 {
    font-size: 15pt;
    font-weight: bold;
    color: #0e223d;
    margin: 4px 0 6px 0;
    line-height: 1.25;
  }
  .meta-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    font-size: 9.5pt;
    background: #f7f9fc;
    border: 1px solid #d0d7de;
  }
  .meta-table td {
    padding: 4px 8px;
    border: 1px solid #d0d7de;
  }
  .meta-label {
    font-weight: bold;
    color: #0e223d;
    width: 20%;
  }
  h2 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #0e223d;
    border-bottom: 1px solid #0e223d;
    padding-bottom: 2px;
    margin: 10px 0 6px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  p {
    margin: 0 0 6px 0;
    text-align: justify;
  }
  .method-list {
    margin: 4px 0 8px 18px;
    padding: 0;
  }
  .method-list li {
    margin-bottom: 4px;
    text-align: justify;
  }
  .results-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 9pt;
  }
  .results-table th, .results-table td {
    border: 1px solid #333;
    padding: 3px 6px;
    text-align: center;
  }
  .results-table th {
    background-color: #0e223d;
    color: #ffffff;
    font-weight: bold;
  }
  .results-table td:first-child {
    text-align: left;
    font-weight: bold;
  }
  .highlight-col {
    background-color: #eaf3fb;
    font-weight: bold;
    color: #0e223d;
  }
  .ref-list {
    margin: 4px 0 0 16px;
    padding: 0;
    font-size: 8.5pt;
    line-height: 1.3;
  }
  .ref-list li {
    margin-bottom: 2px;
  }
  @media print {
    body {
      padding: 0;
    }
  }
</style>
</head>
<body>

<div class="header-banner">
  <div class="course-tag">Department of Computer Science & Engineering | Course Project Review 1</div>
  <h1>Automated Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)</h1>
</div>

<table class="meta-table">
  <tr>
    <td class="meta-label">Course:</td>
    <td>Fundamentals of Image Processing (FIP)</td>
    <td class="meta-label">Review Date:</td>
    <td>11/11/2026 (Final Viva: 24/11/2026)</td>
  </tr>
  <tr>
    <td class="meta-label">Team Members:</td>
    <td>
      <strong>Krithin Kusharaj Salian</strong> (NNM24IS110) &bull;
      <strong>Niriksha</strong> (NNM24IS141) &bull;
      <strong>Pavan L Poojary</strong> (NNM24IS149)
    </td>
    <td class="meta-label">Benchmark:</td>
    <td>DRIVE Dataset (40 images, 576&times;576 resolution)</td>
  </tr>
</table>

<h2>Project Abstract</h2>
<p>
Automated segmentation of the retinal vascular tree from fundus photography is an essential clinical diagnostic tool for the early detection and management of systemic microvascular diseases, including Diabetic Retinopathy, Arteriosclerosis, Stroke Risk, and Glaucoma. Manual delineation by expert ophthalmologists is time-consuming (1–2 hours per image), prone to inter-observer subjectivity, and impossible to scale for mass screening programs. The segmentation task poses three severe digital image processing challenges: (i) extreme class imbalance (~10% vessel pixels vs. ~90% background), (ii) low local contrast of peripheral microcapillaries, and (iii) non-uniform spherical illumination vignetting.
</p>

<h2>Proposed Methodology (Morph-ViT)</h2>
<p>
We propose <strong>Morph-ViT</strong>, a hybrid framework that bridges syllabus-grounded mathematical morphology (Units II & III) with Vision Transformer (ViT) self-attention:
</p>
<ol class="method-list">
  <li><strong>Optical Preprocessing & CLAHE:</strong> Hemoglobin absorbs light maximally at 540–580 nm. The green channel is isolated and enhanced using Contrast-Limited Adaptive Histogram Equalization (CLAHE, 8&times;8 tiles, clip limit 2.0) to normalize background vignetting.</li>
  <li><strong>12-Directional Linear Top-Hat Filtering:</strong> To capture vascular structures regardless of orientation, linear structuring elements of length <em>l</em> = 15 px are rotated across 12 angles &theta; &in; {0&deg;, 15&deg;, &hellip;, 165&deg;}. The supremum of white top-hat transformations isolates vascular ridges: <em>M(x, y) = max<sub>&theta;</sub> [I<sub>inv</sub> - (I<sub>inv</sub> &comp; L<sub>&theta;</sub>)]</em>.</li>
  <li><strong>Deep Hybrid Vision Transformer:</strong> The morphological prior is fused with normalized RGB channels to form a 4-channel tensor. A dual 3&times;3 CNN stem preserves high-resolution edge geometry, while a 4-layer Vision Transformer encoder (16&times;16 patches, 4 attention heads) models global vascular connectivity. A convolutional decoder with stem skip connections reconstructs vessel boundaries.</li>
  <li><strong>Speck Postprocessing:</strong> Connected-component filtering removes spurious false-positive noise islands (&le; 10 px).</li>
</ol>

<h2>Experimental Benchmark Results (DRIVE Test Set)</h2>
<p>
All evaluation metrics were calculated <strong>strictly inside the Field of View (FOV)</strong> to prevent artificial inflation from outer border pixels:
</p>

<table class="results-table">
  <thead>
    <tr>
      <th>Evaluation Metric</th>
      <th>Traditional Method (Top-Hat + CLAHE)</th>
      <th>ML/DL Method (Standard U-Net)</th>
      <th>Proposed Method (Morph-ViT Hybrid)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Accuracy</td>
      <td>89.63%</td>
      <td>88.60%</td>
      <td class="highlight-col">92.35% (Best)</td>
    </tr>
    <tr>
      <td>Dice Similarity (F1)</td>
      <td>64.14%</td>
      <td>72.38%</td>
      <td class="highlight-col">77.79% (+13.65% gain)</td>
    </tr>
    <tr>
      <td>IoU (Jaccard Index)</td>
      <td>47.21%</td>
      <td>56.71%</td>
      <td class="highlight-col">63.66% (Best)</td>
    </tr>
    <tr>
      <td>Precision</td>
      <td>81.19%</td>
      <td>62.81%</td>
      <td class="highlight-col">79.09%</td>
    </tr>
    <tr>
      <td>Recall (Sensitivity)</td>
      <td>53.00%</td>
      <td>85.38%</td>
      <td class="highlight-col">76.54% (+23.54% gain)</td>
    </tr>
    <tr>
      <td>Specificity</td>
      <td>97.40%</td>
      <td>89.28%</td>
      <td class="highlight-col">95.71%</td>
    </tr>
    <tr>
      <td>AUC-ROC</td>
      <td>75.20%</td>
      <td>94.45%</td>
      <td class="highlight-col">94.94% (Best)</td>
    </tr>
    <tr>
      <td>Execution Time</td>
      <td>177.4 ms / img</td>
      <td>671.7 ms / img</td>
      <td class="highlight-col">1,099 ms / img (CPU)</td>
    </tr>
    <tr>
      <td>Model Size / Parameters</td>
      <td>0 MB (0 params)</td>
      <td>1.88 MB (482,737 params)</td>
      <td class="highlight-col">3.29 MB (862,049 params)</td>
    </tr>
  </tbody>
</table>

<h2>Key Literature References</h2>
<ol class="ref-list">
  <li>J. Staal et al., &ldquo;Ridge-based vessel segmentation in color images of the retina,&rdquo; <em>IEEE Transactions on Medical Imaging</em>, vol. 23, no. 4, pp. 501&ndash;509, 2004.</li>
  <li>A. Dosovitskiy et al., &ldquo;An image is worth 16x16 words: Transformers for image recognition at scale,&rdquo; <em>ICLR</em>, 2021.</li>
  <li>O. Ronneberger et al., &ldquo;U-Net: Convolutional networks for biomedical image segmentation,&rdquo; in <em>Proc. MICCAI</em>, 2015, pp. 234&ndash;241.</li>
  <li>J. Serra, <em>Image Analysis and Mathematical Morphology</em>, Academic Press, London, 1982.</li>
</ol>

</body>
</html>
"""
    html_path = os.path.join(proj_dir, "abstract.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created: {html_path}")

    # Generate PDF using Microsoft Edge if available
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    pdf_path = os.path.join(proj_dir, "abstract.pdf")
    if edge_exe:
        cmd = [
            edge_exe,
            "--headless=new",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if os.path.exists(pdf_path):
                print(f"Created: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
        except Exception as e:
            print("Edge PDF conversion note:", e)


def generate_docx(proj_dir: str):
    """Generate professional abstract.docx using native OpenXML."""
    docx_path = os.path.join(proj_dir, "abstract.docx")

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <!-- Header Title -->
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="60"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:color w:val="0E223D"/>
          <w:sz w:val="18"/>
        </w:rPr>
        <w:t>DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING | COURSE PROJECT REVIEW 1</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="160"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:color w:val="0E223D"/>
          <w:sz w:val="28"/>
        </w:rPr>
        <w:t>Automated Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)</w:t>
      </w:r>
    </w:p>

    <!-- Metadata Table -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="0" w:type="auto"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
          <w:left w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
          <w:right w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
          <w:insideH w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
          <w:insideV w:val="single" w:sz="6" w:space="0" w:color="D0D7DE"/>
        </w:tblBorders>
      </w:tblPr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Course:</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>Fundamentals of Image Processing (FIP)</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Review Date:</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>11/11/2026 (Final: 24/11/2026)</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Team Members:</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="18"/></w:rPr><w:t>Krithin Kusharaj Salian (NNM24IS110) | Niriksha (NNM24IS141) | Pavan L Poojary (NNM24IS149)</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="18"/></w:rPr><w:t>Benchmark:</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>DRIVE (40 fundus images, 576x576)</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>

    <!-- Abstract Section -->
    <w:p><w:pPr><w:spacing w:before="180" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="22"/></w:rPr><w:t>1. PROJECT ABSTRACT &amp; CLINICAL MOTIVATION</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:jc w:val="both"/><w:spacing w:after="100"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Automated segmentation of the retinal vascular tree from fundus photography is an essential clinical diagnostic tool for the computerized screening of systemic microvascular diseases, including Diabetic Retinopathy, Arteriosclerosis, Stroke Risk, and Glaucoma. Manual delineation by expert ophthalmologists requires 1 to 2 hours per scan, exhibits high inter-observer variability, and cannot scale to mass healthcare screening. The task introduces three critical image processing challenges: (i) extreme class imbalance (~10% vessel pixels vs. ~90% background), (ii) low local contrast of peripheral microcapillaries near sensor noise floor, and (iii) non-uniform spherical illumination vignetting.</w:t></w:r>
    </w:p>

    <!-- Methodology Section -->
    <w:p><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="22"/></w:rPr><w:t>2. PROPOSED METHODOLOGY (Morph-ViT)</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:jc w:val="both"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>We propose Morph-ViT, a novel hybrid architecture that couples syllabus-aligned mathematical morphology (Units II &amp; III) with deep Vision Transformer self-attention:</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>a) Optical Preprocessing &amp; CLAHE: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Hemoglobin absorbs light maximally at 540-580 nm; hence the green channel is isolated and equalized using CLAHE (8x8 tiles, clip=2.0) to eliminate illumination vignetting.</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>b) 12-Directional Linear Top-Hat Filtering: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Linear structuring elements (l=15 px) are rotated across 12 angles to compute the supremum of white Top-Hat responses, capturing vessels regardless of orientation: M(x, y) = max_theta [WTH_theta(I_inv)].</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>c) Deep Vision Transformer: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>The morphological prior is concatenated with RGB channels to form a 4-channel tensor. A dual 3x3 CNN stem preserves high-resolution edges, while a 4-layer Vision Transformer encoder (16x16 patches, 4 heads) models global vascular connectivity. A skip-decoder reconstructs vessel boundaries.</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>d) Morphological Post-Processing: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Connected-component analysis strips isolated false-positive noise specks (&lt;= 10 px).</w:t></w:r>
    </w:p>

    <!-- Results Section -->
    <w:p><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="22"/></w:rPr><w:t>3. EXPERIMENTAL COMPARATIVE RESULTS (STRICTLY INSIDE FOV)</w:t></w:r>
    </w:p>
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="0" w:type="auto"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="6" w:space="0" w:color="333333"/>
          <w:left w:val="single" w:sz="6" w:space="0" w:color="333333"/>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="333333"/>
          <w:right w:val="single" w:sz="6" w:space="0" w:color="333333"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
          <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tblBorders>
      </w:tblPr>
      <w:tr>
        <w:tc><w:tcPr><w:shd w:fill="0E223D"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="17"/></w:rPr><w:t>Evaluation Metric</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="0E223D"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="17"/></w:rPr><w:t>Traditional Morphology</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="0E223D"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="17"/></w:rPr><w:t>Standard U-Net</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="0E223D"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="17"/></w:rPr><w:t>Proposed Morph-ViT</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>Accuracy</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>89.63%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>88.60%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>92.35% (Best)</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>Dice Similarity (F1)</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>64.14%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>72.38%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>77.79% (+13.65%)</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>IoU (Jaccard Index)</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>47.21%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>56.71%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>63.66% (Best)</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>Recall (Sensitivity)</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>53.00%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>85.38%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>76.54% (+23.54%)</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>Precision</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>81.19%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>62.81%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>79.09%</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:rPr><w:b/><w:sz w:val="17"/></w:rPr><w:t>AUC-ROC</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>75.20%</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:rPr><w:sz w:val="17"/></w:rPr><w:t>94.45%</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:shd w:fill="EAF3FB"/></w:tcPr><w:p><w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="17"/></w:rPr><w:t>94.94% (Best)</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>

    <!-- References Section -->
    <w:p><w:pPr><w:spacing w:before="120" w:after="40"/></w:pPr>
      <w:r><w:rPr><w:b/><w:color w:val="0E223D"/><w:sz w:val="20"/></w:rPr><w:t>4. KEY REFERENCES</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:spacing w:after="20"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>[1] J. Staal et al., "Ridge-based vessel segmentation in color images of the retina," IEEE TMI, vol. 23, no. 4, pp. 501-509, 2004.</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:spacing w:after="20"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>[2] A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," ICLR, 2021.</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:spacing w:after="20"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>[3] O. Ronneberger et al., "U-Net: Convolutional networks for biomedical image segmentation," MICCAI, pp. 234-241, 2015.</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:spacing w:after="20"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>[4] J. Serra, Image Analysis and Mathematical Morphology, Academic Press, London, 1982.</w:t></w:r>
    </w:p>

    <!-- Page Setup: Standard Letter, 0.7-inch margins -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1008" w:right="1008" w:bottom="1008" w:left="1008"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc_xml)

    print(f"Created: {docx_path} (Size: {os.path.getsize(docx_path)} bytes)")


if __name__ == "__main__":
    docs_dir = None
    for d in os.listdir(r"C:\Users\pooja\OneDrive"):
        if "li" in d.lower():
            docs_dir = os.path.join(r"C:\Users\pooja\OneDrive", d)
            break
    proj = os.path.join(docs_dir, "retinal-vessel-segmentation")
    generate_html_and_pdf(proj)
    generate_docx(proj)

