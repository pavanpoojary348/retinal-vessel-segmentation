"""
Generate Professional 7-Slide PowerPoint Presentation (presentation.pptx)
========================================================================
- Large, high-visibility typography across ALL slides (13-32pt) for crystal-clear readability.
- Slide 1: High-contrast bright gold/white/cyan typography inside structured card.
- Slides 2-7: Boosted section headings (20-22pt), large bullet text (15.5-16.5pt), large table cells (13-14.5pt).
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

    # Professional High-Contrast Color Palette
    NAVY = RGBColor(14, 34, 61)
    TEAL = RGBColor(0, 160, 175)
    GOLD = RGBColor(255, 210, 63)
    CYAN = RGBColor(160, 230, 245)
    DARK_TEXT = RGBColor(20, 25, 35)
    LIGHT_BG = RGBColor(245, 247, 250)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(25, 50, 85)

    def add_header(slide, title_text, category="FUNDAMENTALS OF IMAGE PROCESSING (FIP) — COURSE PROJECT"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(1.25))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.12)

        p_cat = tf.paragraphs[0]
        r_cat = p_cat.add_run()
        r_cat.text = category.upper()
        r_cat.font.size = Pt(13)
        r_cat.font.bold = True
        r_cat.font.color.rgb = GOLD

        p_title = tf.add_paragraph()
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.size = Pt(26)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: Title Slide (Large Typography & High Contrast)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.75), Inches(11.53), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.color.rgb = GOLD

    tb1 = s1.shapes.add_textbox(Inches(0.9), Inches(0.95), Inches(11.53), Inches(3.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "COURSE PROJECT FIRST REVIEW — 11/11/2026"
    r0.font.size = Pt(17)
    r0.font.bold = True
    r0.font.color.rgb = GOLD

    p1 = tf1.add_paragraph()
    r1 = p1.add_run()
    r1.text = "Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)"
    r1.font.size = Pt(32)
    r1.font.bold = True
    r1.font.color.rgb = WHITE
    p1.space_before = Pt(14)

    p2 = tf1.add_paragraph()
    r2 = p2.add_run()
    r2.text = "A Hybrid Classical-Deep Learning Comparative Study on the DRIVE Benchmark"
    r2.font.size = Pt(21)
    r2.font.italic = True
    r2.font.color.rgb = CYAN
    p2.space_before = Pt(8)

    # Info card for Team & Course details
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.35), Inches(11.53), Inches(2.65))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = TEAL
    card1.line.width = Pt(1.5)

    tf_c = card1.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_top = Inches(0.2)

    p0 = tf_c.paragraphs[0]
    r_l0 = p0.add_run(); r_l0.text = "Course: "; r_l0.font.size = Pt(16); r_l0.font.bold = True; r_l0.font.color.rgb = GOLD
    r_v0 = p0.add_run(); r_v0.text = "Fundamentals of Image Processing (FIP)   |   Dept. of Computer Science & Engineering"; r_v0.font.size = Pt(16); r_v0.font.bold = True; r_v0.font.color.rgb = WHITE

    p1 = tf_c.add_paragraph()
    p1.space_before = Pt(6)
    r_l1 = p1.add_run(); r_l1.text = "Team Members:"; r_l1.font.size = Pt(16); r_l1.font.bold = True; r_l1.font.color.rgb = GOLD

    team_members = [
        ("Krithin Kusharaj Salian", "NNM24IS110"),
        ("Niriksha", "NNM24IS141"),
        ("Pavan L Poojary", "NNM24IS149")
    ]
    p_team = tf_c.add_paragraph()
    p_team.space_before = Pt(4)
    for i, (name, usn) in enumerate(team_members):
        if i > 0:
            r_sep = p_team.add_run(); r_sep.text = "     •     "; r_sep.font.size = Pt(16); r_sep.font.bold = True; r_sep.font.color.rgb = TEAL
        r_name = p_team.add_run(); r_name.text = f"{name} "; r_name.font.size = Pt(16); r_name.font.bold = True; r_name.font.color.rgb = WHITE
        r_usn = p_team.add_run(); r_usn.text = f"({usn})"; r_usn.font.size = Pt(15.5); r_usn.font.bold = True; r_usn.font.color.rgb = CYAN

    p_rev = tf_c.add_paragraph()
    p_rev.space_before = Pt(7)
    r_l2 = p_rev.add_run(); r_l2.text = "Review Dates: "; r_l2.font.size = Pt(15); r_l2.font.bold = True; r_l2.font.color.rgb = TEAL
    r_v2 = p_rev.add_run(); r_v2.text = "Review 1: 11/11/2026   |   Final Project Viva & Evaluation: 24/11/2026"; r_v2.font.size = Pt(15); r_v2.font.bold = True; r_v2.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 2: Abstract & Problem Formulation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Slide 1/7: Abstract & Clinical Problem Formulation")

    # Left Card: Clinical Motivation
    c2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c2_l.fill.solid()
    c2_l.fill.fore_color.rgb = LIGHT_BG
    c2_l.line.color.rgb = TEAL
    c2_l.line.width = Pt(1.5)

    tf2_l = c2_l.text_frame
    tf2_l.word_wrap = True
    tf2_l.margin_left = Inches(0.4)
    tf2_l.margin_top = Inches(0.3)
    tf2_l.margin_right = Inches(0.4)

    p = tf2_l.paragraphs[0]
    r = p.add_run()
    r.text = "Clinical Motivation:"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = NAVY

    bullets_l = [
        ("Direct In Vivo Biomarker:", " Retinal fundus images provide the body's only non-invasive window into microvascular circulation."),
        ("Key Disease Indicator:", " Vital for screening Diabetic Retinopathy (leading adult blindness cause), Stroke, Hypertension, and Glaucoma."),
        ("Clinical Screening Bottleneck:", " Manual tracing takes 1–2 hours per image, is operator-dependent, and cannot scale to mass healthcare.")
    ]
    for bold_prefix, rest in bullets_l:
        p = tf2_l.add_paragraph()
        p.space_before = Pt(14)
        r_b = p.add_run()
        r_b.text = "• " + bold_prefix
        r_b.font.size = Pt(16.5)
        r_b.font.bold = True
        r_b.font.color.rgb = NAVY

        r_t = p.add_run()
        r_t.text = rest
        r_t.font.size = Pt(16)
        r_t.font.color.rgb = DARK_TEXT

    # Right Card: Image Processing Challenges
    c2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c2_r.fill.solid()
    c2_r.fill.fore_color.rgb = LIGHT_BG
    c2_r.line.color.rgb = NAVY
    c2_r.line.width = Pt(1.5)

    tf2_r = c2_r.text_frame
    tf2_r.word_wrap = True
    tf2_r.margin_left = Inches(0.4)
    tf2_r.margin_top = Inches(0.3)
    tf2_r.margin_right = Inches(0.4)

    p = tf2_r.paragraphs[0]
    r = p.add_run()
    r.text = "Core Challenges & Proposed Solution:"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = NAVY

    bullets_r = [
        ("Extreme Class Imbalance:", " Vessel pixels occupy only ~10% of retinal area; 90% is non-vessel background."),
        ("Thin Peripheral Capillaries:", " Fine terminal microvessels have intensity profiles near sensor noise floor."),
        ("Illumination Vignetting:", " Spherical eye curvature causes severe lighting drop-off at periphery."),
        ("Proposed Morph-ViT Solution:", " Unites physical mathematical morphology (Units II & III) with Vision Transformer self-attention.")
    ]
    for bold_prefix, rest in bullets_r:
        p = tf2_r.add_paragraph()
        p.space_before = Pt(12)
        r_b = p.add_run()
        r_b.text = "• " + bold_prefix
        r_b.font.size = Pt(16.5)
        r_b.font.bold = True
        r_b.font.color.rgb = NAVY if "Proposed" not in bold_prefix else RGBColor(0, 130, 80)

        r_t = p.add_run()
        r_t.text = rest
        r_t.font.size = Pt(16)
        r_t.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 3: Dataset Specification & Validation Protocols
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Slide 2/7: Dataset Specification & Validation Protocols")

    c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.73), Inches(5.5))
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
        ("Public Benchmark: DRIVE Dataset",
         [("Native Specs: ", "Canon CR5 3CCD camera, 768 × 584 resolution, 45° FOV, 8 bits/channel."),
          ("Standard Splits: ", "20 Training images (21–40) & 20 Test images (01–20) for rigorous evaluation.")]),
        ("Ground-Truth & Strict FOV Protocol (Mandatory Instruction 4):",
         [("Certified Ground Truth: ", "Independent manual delineations by expert ophthalmologists."),
          ("Field of View (FOV) Masks: ", "Exact circular binary masks delineating true retinal diagnostic area."),
          ("Strict Benchmark Rule: ", "ALL evaluation metrics are calculated EXCLUSIVELY INSIDE THE FOV mask, preventing artificial metric inflation from outside black background pixels.")]),
        ("Input Processing Resolution:",
         [("Normalized 576 × 576: ", "Maintains anatomical aspect ratio, perfectly divisible by ViT patch size P=16 (1,296 patch tokens).")])
    ]

    first = True
    for heading, items in sections_3:
        p = tf3.paragraphs[0] if first else tf3.add_paragraph()
        first = False
        p.space_before = Pt(12) if not first else Pt(0)
        r = p.add_run()
        r.text = heading
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.color.rgb = NAVY

        for lbl, it in items:
            p_it = tf3.add_paragraph()
            p_it.space_before = Pt(5)
            r_l = p_it.add_run()
            r_l.text = "  • " + lbl
            r_l.font.size = Pt(16.5)
            r_l.font.bold = True
            r_l.font.color.rgb = NAVY if "EXCLUSIVELY" not in it else RGBColor(180, 20, 20)

            r_it = p_it.add_run()
            r_it.text = it
            r_it.font.size = Pt(16)
            r_it.font.color.rgb = DARK_TEXT if "EXCLUSIVELY" not in it else RGBColor(180, 20, 20)
            if "EXCLUSIVELY" in it:
                r_it.font.bold = True

    # =========================================================================
    # SLIDE 4: Proposed Methodology & Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Slide 3/7: Proposed Methodology & Morph-ViT Architecture")

    # Left Column: Mathematical Morphology Pipeline
    c4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c4_l.fill.solid()
    c4_l.fill.fore_color.rgb = LIGHT_BG
    c4_l.line.color.rgb = TEAL
    c4_l.line.width = Pt(1.5)

    tf4_l = c4_l.text_frame
    tf4_l.word_wrap = True
    tf4_l.margin_left = Inches(0.4)
    tf4_l.margin_top = Inches(0.3)
    tf4_l.margin_right = Inches(0.4)

    p = tf4_l.paragraphs[0]
    r = p.add_run()
    r.text = "Mathematical Morphology (Units II & III):"
    r.font.size = Pt(21)
    r.font.bold = True
    r.font.color.rgb = NAVY

    morph_points = [
        ("1. Green Channel Selection:", " Hemoglobin absorption peak (540–580 nm) yields optimal vessel-to-background contrast."),
        ("2. CLAHE Normalization:", " (8×8 grid, clip=2.0) smooths vignetting without blowing out noise."),
        ("3. 12-Directional Linear Top-Hat:", " Linear structuring elements (length l=15 px) across θ ∈ {0°, 15°, ..., 165°}:"),
        ("   WTH_θ(I) = I - (I ∘ L_θ) ; M(x, y) = max_θ [WTH_θ(I_inv)]", ""),
        ("4. Connected-Component Filter:", " Discards small isolated false-positive noise specks (< 10 px).")
    ]
    for lbl, desc in morph_points:
        p = tf4_l.add_paragraph()
        p.space_before = Pt(8)
        r_lbl = p.add_run()
        r_lbl.text = lbl
        r_lbl.font.size = Pt(15.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = NAVY if "WTH" not in lbl else RGBColor(0, 100, 150)

        if desc:
            r_desc = p.add_run()
            r_desc.text = desc
            r_desc.font.size = Pt(15)
            r_desc.font.color.rgb = DARK_TEXT

    # Right Column: Deep Vision Transformer
    c4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c4_r.fill.solid()
    c4_r.fill.fore_color.rgb = LIGHT_BG
    c4_r.line.color.rgb = NAVY
    c4_r.line.width = Pt(1.5)

    tf4_r = c4_r.text_frame
    tf4_r.word_wrap = True
    tf4_r.margin_left = Inches(0.4)
    tf4_r.margin_top = Inches(0.3)
    tf4_r.margin_right = Inches(0.4)

    p = tf4_r.paragraphs[0]
    r = p.add_run()
    r.text = "Deep Vision Transformer (Morph-ViT):"
    r.font.size = Pt(21)
    r.font.bold = True
    r.font.color.rgb = NAVY

    vit_points = [
        ("• 4-Channel Fusion Input:", " Direct concatenation [R, G, B + Morphological Top-Hat Prior]."),
        ("• High-Res CNN Stem:", " Dual 3×3 convolutions retain fine vessel boundary gradients."),
        ("• ViT Tokenizer:", " 16×16 non-overlapping patches projected to 128-dim tokens (1,296 tokens)."),
        ("• 4-Layer Self-Attention:", " Multi-Head Attention captures global vascular tree connectivity."),
        ("• Skip-Decoder:", " Bilinear upsampling fused with CNN stem skip features."),
        ("• Weighted DiceBCELoss:", " Positive class weighting (w_pos = 4.0) heavily penalizes missed vessels.")
    ]
    for lbl, desc in vit_points:
        p = tf4_r.add_paragraph()
        p.space_before = Pt(8)
        r_lbl = p.add_run()
        r_lbl.text = lbl
        r_lbl.font.size = Pt(15.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = NAVY

        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.size = Pt(15)
        r_desc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5: Six Mandatory Comparative Experiments
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Slide 4/7: Six Mandatory Comparative Experiments")

    rows_5 = [
        ["Exp 1", "Traditional Technique", "Multi-directional Top-Hat with linear structuring elements + CLAHE (Units II & III)", "Establish syllabus baseline."],
        ["Exp 2", "ML/DL-Based Technique", "Standard U-Net architecture (Ronneberger et al., 2015) on 3-channel RGB", "Evaluate deep learning gains."],
        ["Exp 3", "Proposed Hybrid Technique", "Morph-ViT (Morphological Top-Hat + CNN stem + ViT Self-Attention)", "Demonstrate hybrid physics+attention synergy."],
        ["Exp 4", "Hyperparameter Tuning", "Sweep: Decision Thresholds (T=0.30 to 0.70), Kernel Length (l=9, 15, 21), Speck (<10 px)", "Identify optimal parameters."],
        ["Exp 5", "Ablation Study", "Modular isolation: Pure Morphology vs. Pure ViT vs. Morph-ViT Raw vs. Full Optimized", "Quantify component gains."],
        ["Exp 6", "Performance Comparison", "Accuracy, Dice, IoU, Precision, Recall, Specificity, AUC, Execution Time & Model Size", "Comprehensive clinical audit."]
    ]

    t5_shape = s5.shapes.add_table(7, 4, Inches(0.8), Inches(1.45), Inches(11.73), Inches(5.5))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(1.2)
    t5.columns[1].width = Inches(3.0)
    t5.columns[2].width = Inches(4.7)
    t5.columns[3].width = Inches(2.83)

    headers5 = ["Exp #", "Method to be Implemented", "Exact Pipeline / Model", "Core Academic Purpose"]
    for j, h in enumerate(headers5):
        cell = t5.cell(0, j)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.margin_left = Inches(0.1)
        cell.margin_right = Inches(0.1)
        cell.margin_top = Inches(0.08)
        cell.margin_bottom = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for i, row in enumerate(rows_5):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            cell.margin_left = Inches(0.1)
            cell.margin_right = Inches(0.1)
            cell.margin_top = Inches(0.06)
            cell.margin_bottom = Inches(0.06)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(13.5)
            r.font.color.rgb = DARK_TEXT
            if j == 0:
                r.font.bold = True
                r.font.size = Pt(14)
                r.font.color.rgb = NAVY
            elif j == 1:
                r.font.bold = True

    # =========================================================================
    # SLIDE 6: Visual Comparison & Error Map Analysis
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Slide 5/7: Visual Comparison & Color-Coded Error Map Analysis")

    err_panel_path = os.path.join(proj_dir, "outputs", "error_maps", "21_training_error_panel.png")
    if os.path.exists(err_panel_path):
        s6.shapes.add_picture(err_panel_path, Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.6))

    tb6 = s6.shapes.add_textbox(Inches(8.4), Inches(1.4), Inches(4.5), Inches(5.6))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    tf6.margin_left = Inches(0.2)
    tf6.margin_right = Inches(0.2)
    p = tf6.paragraphs[0]
    r = p.add_run()
    r.text = "Color-Coded Error Map Key:"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = NAVY

    err_items = [
        ("🟩 Green (True Positive):", " Correctly segmented vessel lumens.", RGBColor(0, 150, 0)),
        ("🟥 Red (False Negative):", " Missed microvessels. Morphology misses 47% of capillaries. Morph-ViT cuts missed vessels to only 23.4%!", RGBColor(200, 0, 0)),
        ("🟦 Blue (False Positive):", " Noise near optic disc. Suppressed by morphological speck filtering.", RGBColor(0, 100, 220)),
        ("⬛ Black (True Negative):", " Correct non-vessel background inside FOV.", DARK_TEXT),
        ("\nClinical Significance:\n", "Morph-ViT preserves thin vessel connectivity across complex bifurcations without fragmentation.", NAVY)
    ]
    for lbl, desc, col in err_items:
        p = tf6.add_paragraph()
        p.space_before = Pt(10)
        r_lbl = p.add_run()
        r_lbl.text = lbl
        r_lbl.font.size = Pt(16)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = col

        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.size = Pt(15.5)
        r_desc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 7: Common Results Table with ACTUAL NUMBERS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Slide 6/7: Mandatory Common Results Table & Key References")

    table_data_7 = [
        ["Accuracy", "89.63%", "88.60%", "92.35% (Best)"],
        ["Dice Score (F1)", "64.14%", "72.38%", "77.79% (+13.65%)"],
        ["IoU (Jaccard)", "47.21%", "56.71%", "63.66% (Best)"],
        ["Precision", "81.19%", "62.81%", "79.09%"],
        ["Recall (Sens.)", "53.00%", "85.38%", "76.54% (+23.54%)"],
        ["Specificity", "97.40%", "89.28%", "95.71%"],
        ["AUC-ROC", "75.20%", "94.45%", "94.94% (Best)"],
        ["Exec. Time (ms)", "177.4 ms", "671.7 ms", "1,099 ms (CPU)"],
        ["Model Size (MB)", "0.00 MB", "1.88 MB", "3.29 MB"],
        ["Parameters", "0", "482,737", "862,049"]
    ]

    t7_shape = s7.shapes.add_table(11, 4, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.6))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(2.2)
    t7.columns[1].width = Inches(1.6)
    t7.columns[2].width = Inches(1.6)
    t7.columns[3].width = Inches(1.8)

    headers7 = ["Evaluation Metric", "Traditional Method\n(Morphology)", "ML/DL Method\n(Standard U-Net)", "Proposed Method\n(Morph-ViT)"]
    for j, h in enumerate(headers7):
        cell = t7.cell(0, j)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.margin_left = Inches(0.08)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for i, row in enumerate(table_data_7):
        for j, val in enumerate(row):
            cell = t7.cell(i + 1, j)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(12.5)
            r.font.color.rgb = DARK_TEXT
            if j == 0:
                r.font.bold = True
            elif j == 3:  # Highlight proposed method
                r.font.bold = True
                r.font.color.rgb = NAVY
                r.font.size = Pt(13)

    # References on right
    tb7_ref = s7.shapes.add_textbox(Inches(8.2), Inches(1.4), Inches(4.7), Inches(5.6))
    tf7_r = tb7_ref.text_frame
    tf7_r.word_wrap = True
    tf7_r.margin_left = Inches(0.2)
    tf7_r.margin_right = Inches(0.2)
    p = tf7_r.paragraphs[0]
    r = p.add_run()
    r.text = "Key Findings & Literature:"
    r.font.size = Pt(21)
    r.font.bold = True
    r.font.color.rgb = NAVY

    ref_bullets = [
        ("Highest Accuracy & Dice:", " Morph-ViT achieves 92.35% Acc and 77.79% Dice, matching ophthalmologist agreement (78–80%)."),
        ("Overcoming Capillary Dropout:", " Morphology misses thin capillaries (Recall 53.0%), boosted to 76.54% by Morph-ViT."),
        ("High Precision (79.09%):", " Morphological priors eliminate U-Net's high false-positive rate (Precision 62.81%)."),
        ("\nLiterature References:", ""),
        ("[1] J. Staal et al., ", "IEEE TMI, 2004 (DRIVE benchmark)."),
        ("[2] A. Dosovitskiy et al., ", "ICLR, 2021 (Vision Transformers)."),
        ("[3] O. Ronneberger et al., ", "MICCAI, 2015 (U-Net)."),
        ("[4] J. Serra, ", "Academic Press, 1982 (Mathematical Morphology).")
    ]
    for lbl, desc in ref_bullets:
        p = tf7_r.add_paragraph()
        p.space_before = Pt(4)
        r_lbl = p.add_run()
        r_lbl.text = lbl
        if "\n" in lbl:
            r_lbl.font.size = Pt(15.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = NAVY
        elif "[" in lbl:
            r_lbl.font.size = Pt(13)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = NAVY
        else:
            r_lbl.font.size = Pt(14.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = NAVY

        if desc:
            r_desc = p.add_run()
            r_desc.text = desc
            r_desc.font.size = Pt(13 if "[" in lbl else 14)
            r_desc.font.color.rgb = DARK_TEXT

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
