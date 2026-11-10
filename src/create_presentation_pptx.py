"""
Generate Professional 7-Slide PowerPoint Presentation (presentation.pptx)
========================================================================
- Increased font sizes across all slides for high readability on projector screens.
- Fixed first slide text visibility: high-contrast bright white/gold/cyan on dark navy card.
- Standard widescreen 16:9 format (13.33 x 7.5 inches).
- Modifies and overwrites presentation.pptx directly in place.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(proj_dir: str):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    NAVY = RGBColor(14, 34, 61)
    TEAL = RGBColor(0, 160, 175)
    GOLD = RGBColor(255, 210, 63)
    CYAN = RGBColor(160, 230, 245)
    DARK_TEXT = RGBColor(25, 25, 25)
    LIGHT_BG = RGBColor(245, 247, 250)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(25, 50, 85)

    def add_header(slide, title_text, category="FUNDAMENTALS OF IMAGE PROCESSING (FIP) — COURSE PROJECT"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(1.2))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.15)

        p_cat = tf.paragraphs[0]
        r_cat = p_cat.add_run()
        r_cat.text = category.upper()
        r_cat.font.size = Pt(12)
        r_cat.font.bold = True
        r_cat.font.color.rgb = GOLD

        p_title = tf.add_paragraph()
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.size = Pt(24)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: Title Slide (Pristine High Contrast & Large Fonts)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.8), Inches(11.53), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.color.rgb = GOLD

    tb1 = s1.shapes.add_textbox(Inches(0.9), Inches(1.0), Inches(11.53), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "COURSE PROJECT FIRST REVIEW — 11/11/2026"
    r0.font.size = Pt(16)
    r0.font.bold = True
    r0.font.color.rgb = GOLD

    p1 = tf1.add_paragraph()
    r1 = p1.add_run()
    r1.text = "Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)"
    r1.font.size = Pt(30)
    r1.font.bold = True
    r1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

    p2 = tf1.add_paragraph()
    r2 = p2.add_run()
    r2.text = "A Hybrid Classical-Deep Learning Comparative Study on the DRIVE Benchmark"
    r2.font.size = Pt(20)
    r2.font.italic = True
    r2.font.color.rgb = CYAN
    p2.space_before = Pt(8)

    # Info card for Team & Course details (prevents any dark text)
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.5), Inches(11.53), Inches(2.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = TEAL
    card1.line.width = Pt(1.5)

    tf_c = card1.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_top = Inches(0.25)

    info_lines = [
        ("Course:", " Fundamentals of Image Processing (FIP)", GOLD, WHITE, 16),
        ("Team Members:", " [Insert Student Names & USN / Roll Numbers]", GOLD, WHITE, 16),
        ("Department:", " Department of Computer Science & Engineering", GOLD, WHITE, 15),
        ("Review Dates:", " Review 1: 11/11/2026  |  Final Viva & Evaluation: 24/11/2026", TEAL, CYAN, 14.5)
    ]

    for idx, (label, val, c_lbl, c_val, sz) in enumerate(info_lines):
        p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
        if idx > 0:
            p.space_before = Pt(6)
        r_lbl = p.add_run()
        r_lbl.text = label
        r_lbl.font.size = Pt(sz)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = c_lbl

        r_val = p.add_run()
        r_val.text = val
        r_val.font.size = Pt(sz)
        r_val.font.bold = True
        r_val.font.color.rgb = c_val

    # =========================================================================
    # SLIDE 2: Abstract & Problem Formulation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Slide 1/7: Abstract & Clinical Problem Formulation")

    # Left Card
    c2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(5.7), Inches(5.6))
    c2_l.fill.solid()
    c2_l.fill.fore_color.rgb = LIGHT_BG
    c2_l.line.color.rgb = TEAL
    c2_l.line.width = Pt(1.5)

    tf2_l = c2_l.text_frame
    tf2_l.word_wrap = True
    tf2_l.margin_left = Inches(0.35)
    tf2_l.margin_top = Inches(0.25)
    tf2_l.margin_right = Inches(0.35)

    p = tf2_l.paragraphs[0]
    r = p.add_run()
    r.text = "Clinical Motivation:"
    r.font.size = Pt(19)
    r.font.bold = True
    r.font.color.rgb = NAVY

    bullets_l = [
        "Direct In Vivo Biomarker: Retinal vessels provide the body's only non-invasive microcirculation view.",
        "Diagnostic Indicator for Major Systemic Diseases:",
        "  • Diabetic Retinopathy (leading cause of adult blindness)",
        "  • Arteriosclerosis, Stroke Risk & Hypertension",
        "  • Glaucoma & Macular Degeneration",
        "Clinical Bottleneck: Manual tracing by eye specialists takes 1-2 hours per image, is highly subjective, and cannot scale to mass population screening."
    ]
    for b in bullets_l:
        p = tf2_l.add_paragraph()
        p.space_before = Pt(8)
        r = p.add_run()
        r.text = "• " + b if not b.startswith("  •") else b
        r.font.size = Pt(14.5)
        r.font.color.rgb = DARK_TEXT
        if "Diabetic Retinopathy" in b or "Direct In Vivo" in b:
            r.font.bold = True

    # Right Card
    c2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.6))
    c2_r.fill.solid()
    c2_r.fill.fore_color.rgb = LIGHT_BG
    c2_r.line.color.rgb = NAVY
    c2_r.line.width = Pt(1.5)

    tf2_r = c2_r.text_frame
    tf2_r.word_wrap = True
    tf2_r.margin_left = Inches(0.35)
    tf2_r.margin_top = Inches(0.25)
    tf2_r.margin_right = Inches(0.35)

    p = tf2_r.paragraphs[0]
    r = p.add_run()
    r.text = "Key Image Processing Challenges:"
    r.font.size = Pt(19)
    r.font.bold = True
    r.font.color.rgb = NAVY

    bullets_r = [
        "1. Extreme Class Imbalance: Vessel pixels comprise only ~10% of retinal pixels, while background is ~90%.",
        "2. Dim Peripheral Capillaries: Terminal microvessels have intensity profiles near sensor noise floor.",
        "3. Non-Uniform Illumination: Spherical retina creates severe illumination vignetting at outer edges.",
        "4. Confounding Structures: Optic disc margins and exudates trigger high false-alarm rates.",
        "Proposed Hybrid Solution: Morph-ViT unites classical mathematical morphology (Units II & III) with Vision Transformer self-attention."
    ]
    for b in bullets_r:
        p = tf2_r.add_paragraph()
        p.space_before = Pt(8)
        r = p.add_run()
        r.text = b
        r.font.size = Pt(14.5)
        r.font.color.rgb = DARK_TEXT
        if b.startswith("Proposed"):
            r.font.bold = True
            r.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 3: Dataset Specification & Validation Protocols
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Slide 2/7: Dataset Specification & Validation Protocols")

    c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.73), Inches(5.6))
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = NAVY
    c3.line.width = Pt(1.5)

    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.5)
    tf3.margin_top = Inches(0.3)
    tf3.margin_right = Inches(0.5)

    sections_3 = [
        ("Public Benchmark: DRIVE Dataset (Canon CR5 non-mydriatic 3CCD camera)",
         ["Native resolution: 768 x 584 pixels, 45° Field of View (FOV), 8 bits per color channel.",
          "Standard normalized processing resolution: 576 x 576 pixels (perfectly divisible by patch size P=16 -> 1,296 tokens)."]),
        ("Ground-Truth & Strict FOV Protocols (Mandatory Instruction 4):",
         ["Independent Expert Ground Truth: Gold-standard manual delineations created by ophthalmologists (1st Manual).",
          "Field of View (FOV) Masks: Exact circular binary masks delineating the true retinal diagnostic area.",
          "Strict Clinical Benchmark Protocol: All evaluation metrics are calculated EXCLUSIVELY INSIDE THE FOV, preventing artificial metric inflation from outside non-retinal black borders."]),
        ("Dataset Split Architecture:",
         ["Training Split: 20 fundus images (21_training to 40_training) with expert manual vessel segmentations.",
          "Test Split: 20 fundus images (01_test to 20_test) for clinical generalization and inference testing."])
    ]

    first = True
    for heading, items in sections_3:
        p = tf3.paragraphs[0] if first else tf3.add_paragraph()
        first = False
        p.space_before = Pt(10) if not first else Pt(0)
        r = p.add_run()
        r.text = heading
        r.font.size = Pt(17)
        r.font.bold = True
        r.font.color.rgb = NAVY

        for it in items:
            p_it = tf3.add_paragraph()
            p_it.space_before = Pt(4)
            r_it = p_it.add_run()
            r_it.text = "• " + it
            r_it.font.size = Pt(14)
            r_it.font.color.rgb = DARK_TEXT
            if "EXCLUSIVELY INSIDE THE FOV" in it:
                r_it.font.bold = True
                r_it.font.color.rgb = RGBColor(180, 20, 20)

    # =========================================================================
    # SLIDE 4: Proposed Methodology & Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Slide 3/7: Proposed Methodology & Morph-ViT Architecture")

    # Left Column: Mathematical Morphology Pipeline
    c4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.7))
    c4_l.fill.solid()
    c4_l.fill.fore_color.rgb = LIGHT_BG
    c4_l.line.color.rgb = TEAL
    c4_l.line.width = Pt(1.5)

    tf4_l = c4_l.text_frame
    tf4_l.word_wrap = True
    tf4_l.margin_left = Inches(0.35)
    tf4_l.margin_top = Inches(0.25)
    tf4_l.margin_right = Inches(0.35)

    p = tf4_l.paragraphs[0]
    r = p.add_run()
    r.text = "Mathematical Morphology Pipeline:"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = NAVY

    morph_points = [
        "1. Green Channel Selection: Hemoglobin absorbs light peak at 540-580 nm, providing maximum vessel-to-choroid contrast.",
        "2. CLAHE (8x8 grid, clip=2.0): Normalizes spherical illumination vignetting without amplifying sensor noise.",
        "3. Multi-Directional Linear Top-Hat (Units II & III):",
        "   - Linear structuring elements L of length l=15 px.",
        "   - Rotated across 12 angles: θ ∈ {0°, 15°, 30°, ..., 165°}.",
        "   - White Top-Hat: WTH_θ(I) = I - (I ∘ L_θ)",
        "   - Directional Supremum: M(x, y) = max_θ [WTH_θ(I_inv)]",
        "4. Connected-Component Post-Processing: Removes isolated false-positive noise islands (< 10 px)."
    ]
    for pt in morph_points:
        p = tf4_l.add_paragraph()
        p.space_before = Pt(5)
        r = p.add_run()
        r.text = pt
        r.font.size = Pt(13.5)
        r.font.color.rgb = DARK_TEXT
        if "Directional Supremum" in pt or "White Top-Hat" in pt:
            r.font.bold = True

    # Right Column: Deep Vision Transformer
    c4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.7))
    c4_r.fill.solid()
    c4_r.fill.fore_color.rgb = LIGHT_BG
    c4_r.line.color.rgb = NAVY
    c4_r.line.width = Pt(1.5)

    tf4_r = c4_r.text_frame
    tf4_r.word_wrap = True
    tf4_r.margin_left = Inches(0.35)
    tf4_r.margin_top = Inches(0.25)
    tf4_r.margin_right = Inches(0.35)

    p = tf4_r.paragraphs[0]
    r = p.add_run()
    r.text = "Deep Vision Transformer (Morph-ViT):"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = NAVY

    vit_points = [
        "• 4-Channel Fusion Input: Concatenates [R, G, B, Morphological Top-Hat Channel].",
        "• High-Resolution CNN Stem: Dual 3x3 Conv layers preserve fine microcapillary edge boundaries.",
        "• ViT Patch Embedding: 16x16 non-overlapping patches projected to 128-dim token vectors (1,296 tokens).",
        "• 4-Layer Transformer Encoder: Multi-Head Self-Attention (4 heads) models global vascular tree continuity.",
        "• Convolutional Decoder: Progressive bilinear 2x upsampling with skip connections from CNN stem.",
        "• Imbalance-Aware Loss: DiceBCELoss with positive class weighting w_pos = 4.0 to strongly penalize missed vessels."
    ]
    for pt in vit_points:
        p = tf4_r.add_paragraph()
        p.space_before = Pt(7)
        r = p.add_run()
        r.text = pt
        r.font.size = Pt(13.5)
        r.font.color.rgb = DARK_TEXT
        if "4-Channel Fusion" in pt or "Multi-Head Self-Attention" in pt:
            r.font.bold = True

    # =========================================================================
    # SLIDE 5: Six Mandatory Comparative Experiments
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Slide 4/7: Six Mandatory Comparative Experiments")

    rows_5 = [
        ["Exp 1", "Traditional Technique", "Multi-directional Top-Hat with linear structuring elements + CLAHE (Units II & III)", "Establish syllabus-aligned baseline."],
        ["Exp 2", "ML/DL-Based Technique", "Standard U-Net architecture (Ronneberger et al., 2015) on 3-channel RGB", "Evaluate gain from pure deep learning."],
        ["Exp 3", "Proposed Hybrid Technique", "Morph-ViT (Morphological Top-Hat + CNN stem + ViT Self-Attention)", "Demonstrate hybrid synergy of physics + attention."],
        ["Exp 4", "Hyperparameter Tuning", "Systematic sweep: Thresholds (T=0.30 to 0.70), Kernel Length (l=9, 15, 21), Min-Speck (<=10px)", "Identify optimal operating parameters."],
        ["Exp 5", "Ablation Study", "Modular isolation: Pure Morphology vs. Pure ViT vs. Morph-ViT Raw vs. Full Optimized", "Quantify contribution of each component."],
        ["Exp 6", "Performance Comparison", "Accuracy, Dice, IoU, Precision, Recall, Specificity, AUC, Execution Time, and Model Size (MB)", "Provide full clinical & computational audit."]
    ]

    t5_shape = s5.shapes.add_table(7, 4, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.6))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(1.1)
    t5.columns[1].width = Inches(3.1)
    t5.columns[2].width = Inches(4.7)
    t5.columns[3].width = Inches(2.83)

    headers5 = ["Exp #", "Method to be Implemented", "Exact Pipeline / Model", "Core Academic Purpose"]
    for j, h in enumerate(headers5):
        cell = t5.cell(0, j)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for i, row in enumerate(rows_5):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(12)
            r.font.color.rgb = DARK_TEXT
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 6: Visual Comparison & Error Map Analysis
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Slide 5/7: Visual Comparison & Color-Coded Error Map Analysis")

    err_panel_path = os.path.join(proj_dir, "outputs", "error_maps", "21_training_error_panel.png")
    if os.path.exists(err_panel_path):
        s6.shapes.add_picture(err_panel_path, Inches(0.8), Inches(1.35), Inches(7.6), Inches(5.8))

    tb6 = s6.shapes.add_textbox(Inches(8.6), Inches(1.35), Inches(4.3), Inches(5.8))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]
    r = p.add_run()
    r.text = "Color-Coded Error Map Key:"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = NAVY

    err_items = [
        ("🟩 Green (True Positive):", " Correctly segmented vessel lumens.", RGBColor(0, 150, 0)),
        ("🟥 Red (False Negative):", " Missed microvessels. Traditional morphology misses 47% of capillaries. Morph-ViT reduces missed vessels to only 23.4%!", RGBColor(200, 0, 0)),
        ("🟦 Blue (False Positive):", " False alarms near disc rim. Effectively suppressed by connected-component filtering.", RGBColor(0, 100, 220)),
        ("⬛ Black (True Negative):", " Background properly identified inside Field of View.", DARK_TEXT),
        ("\nClinical Significance:\n", "Morph-ViT maintains vascular continuity across complex crossings where traditional filters fragment.", NAVY)
    ]
    for lbl, desc, col in err_items:
        p = tf6.add_paragraph()
        p.space_before = Pt(8)
        r_lbl = p.add_run()
        r_lbl.text = lbl
        r_lbl.font.size = Pt(14)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = col

        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.size = Pt(13)
        r_desc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 7: Common Results Table with ACTUAL NUMBERS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Slide 6/7: Mandatory Common Results Table & Key References")

    table_data_7 = [
        ["Accuracy", "89.63%", "88.60%", "92.35% (Best)"],
        ["Dice Score (F1-score)", "64.14%", "72.38%", "77.79% (+13.65%)"],
        ["IoU (Jaccard Index)", "47.21%", "56.71%", "63.66% (Best)"],
        ["Precision", "81.19%", "62.81%", "79.09%"],
        ["Recall (Sensitivity)", "53.00%", "85.38%", "76.54% (+23.54%)"],
        ["Specificity", "97.40%", "89.28%", "95.71%"],
        ["AUC-ROC", "75.20%", "94.45%", "94.94% (Best)"],
        ["Execution Time (ms)", "177.4 ms", "671.7 ms", "1,099 ms (CPU)"],
        ["Model Size (MB)", "0.00 MB (Algorithmic)", "1.88 MB", "3.29 MB"],
        ["Trainable Parameters", "0", "482,737", "862,049"]
    ]

    t7_shape = s7.shapes.add_table(11, 4, Inches(0.8), Inches(1.35), Inches(7.0), Inches(5.8))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(2.3)
    t7.columns[1].width = Inches(1.55)
    t7.columns[2].width = Inches(1.55)
    t7.columns[3].width = Inches(1.6)

    headers7 = ["Evaluation Metric", "Traditional Method\n(Morphology)", "ML/DL Method\n(Standard U-Net)", "Proposed Method\n(Morph-ViT)"]
    for j, h in enumerate(headers7):
        cell = t7.cell(0, j)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for i, row in enumerate(table_data_7):
        for j, val in enumerate(row):
            cell = t7.cell(i + 1, j)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(11)
            r.font.color.rgb = DARK_TEXT
            if j == 3:  # Highlight proposed method
                r.font.bold = True
                r.font.color.rgb = NAVY

    # References on right
    tb7_ref = s7.shapes.add_textbox(Inches(8.0), Inches(1.35), Inches(4.7), Inches(5.8))
    tf7_r = tb7_ref.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]
    r = p.add_run()
    r.text = "Key Takeaways & Academic References:"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY

    ref_bullets = [
        "1. Morph-ViT achieves highest Accuracy (92.35%) and Dice score (77.79%), matching expert human agreement (78-80%).",
        "2. Traditional morphology misses thin capillaries (Recall only 53.00%), while Morph-ViT boosts recall to 76.54%.",
        "3. U-Net suffers from lower precision (62.81%), whereas Morph-ViT achieves 79.09% precision thanks to morphological priors.",
        "\nLiterature References:",
        "[1] J. Staal et al., 'Ridge-based vessel segmentation in color images of the retina,' IEEE TMI, 2004.",
        "[2] A. Dosovitskiy et al., 'An image is worth 16x16 words: Transformers for image recognition at scale,' ICLR, 2021.",
        "[3] O. Ronneberger et al., 'U-Net: Convolutional networks for biomedical image segmentation,' MICCAI, 2015.",
        "[4] J. Serra, 'Image Analysis and Mathematical Morphology', Academic Press, 1982."
    ]
    for rb in ref_bullets:
        p = tf7_r.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = rb
        r.font.size = Pt(11.5)
        r.font.color.rgb = DARK_TEXT
        if "highest Accuracy" in rb:
            r.font.bold = True

    out_file = os.path.join(proj_dir, "presentation.pptx")
    prs.save(out_file)
    print(f"Updated presentation.pptx saved directly to: {out_file}")


if __name__ == "__main__":
    docs_dir = None
    for d in os.listdir(r"C:\Users\pooja\OneDrive"):
        if "li" in d.lower():
            docs_dir = os.path.join(r"C:\Users\pooja\OneDrive", d)
            break
    proj = os.path.join(docs_dir, "retinal-vessel-segmentation")
    create_deck(proj)
