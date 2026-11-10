"""
Generate Simple, Easy-to-Explain 7-Slide PowerPoint Presentation (presentation_simple.pptx)
========================================================================================
- Designed specifically for effortless Review 1 oral presentation.
- Punchy, high-impact bullet points in plain English (no dense jargon).
- Extra-large typography (16-32pt) for maximum legibility.
- Slide 1: High-contrast title & student credentials card.
- Slide 6: Visual results with color-coded guide.
- Slide 7: Clean comparative results table & 3 conversational takeaways.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_simple_deck(proj_dir: str):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Clean Navy, Vibrant Gold, Medical Teal, Slate
    NAVY = RGBColor(14, 34, 61)
    TEAL = RGBColor(0, 150, 165)
    GOLD = RGBColor(255, 205, 50)
    CYAN = RGBColor(160, 230, 245)
    DARK = RGBColor(25, 30, 40)
    LIGHT_BG = RGBColor(246, 248, 252)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(22, 45, 78)
    GREEN = RGBColor(0, 145, 60)
    RED = RGBColor(210, 30, 30)
    BLUE = RGBColor(20, 110, 220)

    def add_banner(slide, slide_num, title_text):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(1.2))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.12)

        p_cat = tf.paragraphs[0]
        r_cat = p_cat.add_run()
        r_cat.text = f"FUNDAMENTALS OF IMAGE PROCESSING (FIP)  •  SLIDE {slide_num}/7"
        r_cat.font.size = Pt(12.5)
        r_cat.font.bold = True
        r_cat.font.color.rgb = GOLD

        p_title = tf.add_paragraph()
        r_title = p_title.add_run()
        r_title.text = title_text
        r_title.font.size = Pt(26)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: Simple & Bold Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.7), Inches(11.53), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.color.rgb = GOLD

    tb1 = s1.shapes.add_textbox(Inches(0.9), Inches(0.9), Inches(11.53), Inches(3.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "COURSE PROJECT FIRST REVIEW  •  11/11/2026"
    r0.font.size = Pt(17)
    r0.font.bold = True
    r0.font.color.rgb = GOLD

    p1 = tf1.add_paragraph()
    p1.space_before = Pt(12)
    r1 = p1.add_run()
    r1.text = "Retinal Blood Vessel Segmentation"
    r1.font.size = Pt(36)
    r1.font.bold = True
    r1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = "Combining Mathematical Morphology (Units II & III) with Vision Transformers"
    r2.font.size = Pt(22)
    r2.font.italic = True
    r2.font.color.rgb = CYAN

    # Credential Card
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.35), Inches(11.53), Inches(2.65))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = TEAL
    card1.line.width = Pt(1.5)

    tf_c = card1.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_top = Inches(0.2)

    p_c0 = tf_c.paragraphs[0]
    r = p_c0.add_run(); r.text = "Course: "; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = GOLD
    r = p_c0.add_run(); r.text = "Fundamentals of Image Processing (FIP)   |   Dept: Computer Science & Engineering"; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = WHITE

    p_c1 = tf_c.add_paragraph()
    p_c1.space_before = Pt(6)
    r = p_c1.add_run(); r.text = "Team Members:"; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = GOLD

    team = [
        ("Krithin Kusharaj Salian", "NNM24IS110"),
        ("Niriksha", "NNM24IS141"),
        ("Pavan L Poojary", "NNM24IS149")
    ]
    p_team = tf_c.add_paragraph()
    p_team.space_before = Pt(4)
    for i, (name, usn) in enumerate(team):
        if i > 0:
            r = p_team.add_run(); r.text = "     •     "; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = TEAL
        r = p_team.add_run(); r.text = f"{name} "; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = WHITE
        r = p_team.add_run(); r.text = f"({usn})"; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = CYAN

    p_rev = tf_c.add_paragraph()
    p_rev.space_before = Pt(8)
    r = p_rev.add_run(); r.text = "Key Dates: "; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = TEAL
    r = p_rev.add_run(); r.text = "Review 1: 11/11/2026   |   Final Project Viva & Demo: 24/11/2026"; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 2: Why This Project? (The Problem & Goal)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_banner(s2, 1, "Why This Project? Clinical Problem & Our Goal")

    # Left Card: Clinical Need
    c2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c2_l.fill.solid()
    c2_l.fill.fore_color.rgb = LIGHT_BG
    c2_l.line.color.rgb = TEAL
    c2_l.line.width = Pt(1.5)

    tf2_l = c2_l.text_frame
    tf2_l.word_wrap = True
    tf2_l.margin_left = Inches(0.4); tf2_l.margin_top = Inches(0.3); tf2_l.margin_right = Inches(0.4)

    p = tf2_l.paragraphs[0]
    r = p.add_run(); r.text = "The Clinical Need:"; r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY

    pts_2l = [
        ("Eye as a Diagnostic Window:", " Retinal blood vessels are the only blood vessels in the human body visible non-invasively."),
        ("Early Disease Detection:", " Critical for early screening of Diabetic Retinopathy, High Blood Pressure, Stroke risk, and Glaucoma."),
        ("The Current Bottleneck:", " Eye doctors must manually trace vessels by hand. It takes 1 to 2 hours per image and is prone to human error.")
    ]
    for b_lbl, b_txt in pts_2l:
        p = tf2_l.add_paragraph()
        p.space_before = Pt(14)
        r = p.add_run(); r.text = "• " + b_lbl; r.font.size = Pt(17); r.font.bold = True; r.font.color.rgb = NAVY
        r = p.add_run(); r.text = b_txt; r.font.size = Pt(16.5); r.font.color.rgb = DARK

    # Right Card: Our Solution & Challenges
    c2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c2_r.fill.solid()
    c2_r.fill.fore_color.rgb = LIGHT_BG
    c2_r.line.color.rgb = NAVY
    c2_r.line.width = Pt(1.5)

    tf2_r = c2_r.text_frame
    tf2_r.word_wrap = True
    tf2_r.margin_left = Inches(0.4); tf2_r.margin_top = Inches(0.3); tf2_r.margin_right = Inches(0.4)

    p = tf2_r.paragraphs[0]
    r = p.add_run(); r.text = "Our Goal & Image Challenges:"; r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY

    pts_2r = [
        ("Our Project Goal:", " Build an automated AI system that extracts blood vessels accurately in seconds."),
        ("Challenge 1 - Severe Imbalance:", " Blood vessels occupy only ~10% of retinal pixels; 90% is background."),
        ("Challenge 2 - Thin Capillaries:", " Tiny peripheral vessels are faint and blend into sensor noise."),
        ("Our Solution (Morph-ViT):", " Combines classical morphology to highlight edges + Vision Transformers to connect vessel branches.")
    ]
    for b_lbl, b_txt in pts_2r:
        p = tf2_r.add_paragraph()
        p.space_before = Pt(12)
        r = p.add_run(); r.text = "• " + b_lbl; r.font.size = Pt(17); r.font.bold = True
        r.font.color.rgb = GREEN if "Solution" in b_lbl else NAVY
        r = p.add_run(); r.text = b_txt; r.font.size = Pt(16.5); r.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 3: The Dataset & Evaluation Rules
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_banner(s3, 2, "The Dataset: DRIVE Benchmark & Evaluation Standard")

    c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.73), Inches(5.5))
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = NAVY
    c3.line.width = Pt(1.5)

    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.5); tf3.margin_top = Inches(0.35); tf3.margin_right = Inches(0.5)

    secs_3 = [
        ("1. Public DRIVE Benchmark Dataset",
         [("Standard Medical Benchmark: ", "40 high-resolution retinal fundus photographs from clinical practice."),
          ("Clean 50/50 Split: ", "20 images used strictly for training, and 20 separate images used for final evaluation.")]),
        ("2. Certified Doctor Ground Truth (Mandatory Requirement)",
         [("Expert Verification: ", "Every single vessel has been manually traced and verified by ophthalmologists."),
          ("No Guesswork: ", "Ensures accurate mathematical measurement of True Positives and False Positives.")]),
        ("3. Strict Field of View (FOV) Rule",
         [("Fair Evaluation: ", "All metrics (Accuracy, Dice, Recall) are computed EXCLUSIVELY inside the circular retina mask."),
          ("Zero Inflation: ", "Prevents artificially boosting accuracy numbers using the easy outer black borders.")])
    ]

    for s_idx, (heading, bullets) in enumerate(secs_3):
        p = tf3.paragraphs[0] if s_idx == 0 else tf3.add_paragraph()
        p.space_before = Pt(12) if s_idx > 0 else Pt(0)
        r = p.add_run(); r.text = heading; r.font.size = Pt(21); r.font.bold = True; r.font.color.rgb = NAVY

        for b_lbl, b_txt in bullets:
            p_b = tf3.add_paragraph()
            p_b.space_before = Pt(4)
            r = p_b.add_run(); r.text = "   • " + b_lbl; r.font.size = Pt(17); r.font.bold = True
            r.font.color.rgb = RED if "EXCLUSIVELY" in b_txt else NAVY
            r = p_b.add_run(); r.text = b_txt; r.font.size = Pt(16.5); r.font.color.rgb = DARK
            if "EXCLUSIVELY" in b_txt:
                r.font.bold = True

    # =========================================================================
    # SLIDE 4: Our Approach in 3 Simple Steps
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_banner(s4, 3, "Our Methodology: 3 Simple Pipeline Steps")

    # Left Box: Classical Image Processing
    c4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c4_l.fill.solid()
    c4_l.fill.fore_color.rgb = LIGHT_BG
    c4_l.line.color.rgb = TEAL
    c4_l.line.width = Pt(1.5)

    tf4_l = c4_l.text_frame
    tf4_l.word_wrap = True
    tf4_l.margin_left = Inches(0.4); tf4_l.margin_top = Inches(0.3); tf4_l.margin_right = Inches(0.4)

    p = tf4_l.paragraphs[0]
    r = p.add_run(); r.text = "Step 1: Classical Morphology (Units II & III)"; r.font.size = Pt(21); r.font.bold = True; r.font.color.rgb = NAVY

    m_steps = [
        ("Green Channel Extraction:", " Hemoglobin absorbs green light best, giving maximum vessel contrast over red/blue."),
        ("CLAHE (Histogram Equalization):", " Evens out uneven spherical lighting so dark edges become visible."),
        ("12-Direction Linear Top-Hat:", " Rotates a line structuring element across 12 angles (0° to 165°) to catch vessels in every orientation."),
        ("Output Feature:", " Produces a crisp vessel probability map based on physical optics.")
    ]
    for b_lbl, b_txt in m_steps:
        p = tf4_l.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run(); r.text = "• " + b_lbl; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = NAVY
        r = p.add_run(); r.text = b_txt; r.font.size = Pt(16); r.font.color.rgb = DARK

    # Right Box: Deep Learning & Cleaning
    c4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5))
    c4_r.fill.solid()
    c4_r.fill.fore_color.rgb = LIGHT_BG
    c4_r.line.color.rgb = NAVY
    c4_r.line.width = Pt(1.5)

    tf4_r = c4_r.text_frame
    tf4_r.word_wrap = True
    tf4_r.margin_left = Inches(0.4); tf4_r.margin_top = Inches(0.3); tf4_r.margin_right = Inches(0.4)

    p = tf4_r.paragraphs[0]
    r = p.add_run(); r.text = "Steps 2 & 3: Deep AI & Speck Cleaning"; r.font.size = Pt(21); r.font.bold = True; r.font.color.rgb = NAVY

    d_steps = [
        ("4-Channel Fusion Input:", " Combines raw [R, G, B] with our classical Morphological map."),
        ("CNN Edge Stem:", " Preserves sharp boundaries of tiny capillary vessels."),
        ("Vision Transformer (ViT):", " Uses self-attention to track full blood vessel branches without breaking at junctions."),
        ("Step 3 - Noise Cleaning:", " Simple connected-component filter automatically discards tiny isolated noise dots (<10 px).")
    ]
    for b_lbl, b_txt in d_steps:
        p = tf4_r.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run(); r.text = "• " + b_lbl; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = NAVY
        r = p.add_run(); r.text = b_txt; r.font.size = Pt(16); r.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 5: The 6 Mandatory Experiments
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_banner(s5, 4, "The 6 Mandatory Course Comparative Experiments")

    rows_5 = [
        ["Exp 1", "Traditional Image Processing", "Top-Hat Filtering + CLAHE (Units II & III)", "Establish syllabus baseline"],
        ["Exp 2", "Standard Deep Learning (ML/DL)", "Standard U-Net Architecture (Ronneberger 2015)", "Measure pure deep learning gain"],
        ["Exp 3", "Proposed Hybrid Method", "Morph-ViT (Morphology + Vision Transformer)", "Show benefit of combining physics + AI"],
        ["Exp 4", "Hyperparameter Tuning", "Sweep decision thresholds (0.3 to 0.7) & filter sizes", "Find optimal operating balance"],
        ["Exp 5", "Ablation Study", "Test model with vs. without morphological input", "Prove individual module value"],
        ["Exp 6", "Performance Comparison", "Accuracy, Dice, Recall, Precision, Speed & Size", "Complete clinical & speed audit"]
    ]

    t5_shape = s5.shapes.add_table(7, 4, Inches(0.8), Inches(1.45), Inches(11.73), Inches(5.5))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(1.2)
    t5.columns[1].width = Inches(3.2)
    t5.columns[2].width = Inches(4.5)
    t5.columns[3].width = Inches(2.83)

    headers5 = ["Exp #", "Technique Evaluated", "Methodology Implemented", "Core Academic Purpose"]
    for j, h in enumerate(headers5):
        cell = t5.cell(0, j)
        cell.text = ""; cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.1)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run(); r.text = h; r.font.size = Pt(15.5); r.font.bold = True; r.font.color.rgb = WHITE

    for i, row in enumerate(rows_5):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j)
            cell.text = ""; cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.1)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run(); r.text = val; r.font.size = Pt(14); r.font.color.rgb = DARK
            if j == 0:
                r.font.bold = True; r.font.color.rgb = NAVY
            elif j == 1:
                r.font.bold = True

    # =========================================================================
    # SLIDE 6: Visual Results & Error Map Analysis
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_banner(s6, 5, "Visual Comparison: Predicted Results & Error Maps")

    err_panel_path = os.path.join(proj_dir, "outputs", "error_maps", "21_training_error_panel.png")
    if os.path.exists(err_panel_path):
        s6.shapes.add_picture(err_panel_path, Inches(0.8), Inches(1.4), Inches(7.3), Inches(5.6))

    tb6 = s6.shapes.add_textbox(Inches(8.3), Inches(1.4), Inches(4.6), Inches(5.6))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    tf6.margin_left = Inches(0.2); tf6.margin_right = Inches(0.2)
    p = tf6.paragraphs[0]
    r = p.add_run(); r.text = "How to Read the Error Map:"; r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY

    err_items = [
        ("🟩 Green (True Positive):", " Correctly detected blood vessels.", GREEN),
        ("🟥 Red (False Negative):", " Missed blood vessels. Traditional morphology misses 47% of capillaries. Morph-ViT cuts missed vessels to only 23%!", RED),
        ("🟦 Blue (False Positive):", " Noise dots. Almost completely eliminated by our speck filter.", BLUE),
        ("⬛ Black (True Negative):", " Non-vessel background tissue.", DARK),
        ("\nMain Takeaway:\n", "Morph-ViT keeps vessels connected across intersections, avoiding the broken fragments seen in traditional filters.", NAVY)
    ]
    for lbl, desc, col in err_items:
        p = tf6.add_paragraph()
        p.space_before = Pt(8)
        r = p.add_run(); r.text = lbl; r.font.size = Pt(16.5); r.font.bold = True; r.font.color.rgb = col
        r = p.add_run(); r.text = desc; r.font.size = Pt(15.5); r.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 7: Final Results & Clear Takeaways
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_banner(s7, 6, "Final Comparative Results & Key Conclusions")

    table_data_7 = [
        ["Accuracy", "89.63%", "88.60%", "92.35% (Highest)"],
        ["Dice Score (F1)", "64.14%", "72.38%", "77.79% (+13.6% gain)"],
        ["IoU (Overlap)", "47.21%", "56.71%", "63.66% (Highest)"],
        ["Precision", "81.19%", "62.81%", "79.09%"],
        ["Recall (Sensitivity)", "53.00%", "85.38%", "76.54% (+23.5% gain)"],
        ["Specificity", "97.40%", "89.28%", "95.71%"],
        ["AUC-ROC", "75.20%", "94.45%", "94.94% (Highest)"],
        ["Processing Speed", "177 ms", "672 ms", "1,099 ms (CPU)"],
        ["Model Parameters", "0 (Algorithmic)", "482,737", "862,049"]
    ]

    t7_shape = s7.shapes.add_table(10, 4, Inches(0.8), Inches(1.4), Inches(7.3), Inches(5.6))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(2.2)
    t7.columns[1].width = Inches(1.6)
    t7.columns[2].width = Inches(1.6)
    t7.columns[3].width = Inches(1.9)

    headers7 = ["Evaluation Metric", "Traditional\n(Morphology)", "ML/DL Method\n(Standard U-Net)", "Proposed Method\n(Morph-ViT)"]
    for j, h in enumerate(headers7):
        cell = t7.cell(0, j)
        cell.text = ""; cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        r = p.add_run(); r.text = h; r.font.size = Pt(13.5); r.font.bold = True; r.font.color.rgb = WHITE

    for i, row in enumerate(table_data_7):
        for j, val in enumerate(row):
            cell = t7.cell(i + 1, j)
            cell.text = ""; cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.08)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run(); r.text = val; r.font.size = Pt(13); r.font.color.rgb = DARK
            if j == 0:
                r.font.bold = True
            elif j == 3:
                r.font.bold = True; r.font.color.rgb = NAVY; r.font.size = Pt(13.5)

    # Right Card: 3 Clear Takeaways
    tb7 = s7.shapes.add_textbox(Inches(8.3), Inches(1.4), Inches(4.6), Inches(5.6))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    tf7.margin_left = Inches(0.2); tf7.margin_right = Inches(0.2)
    p = tf7.paragraphs[0]
    r = p.add_run(); r.text = "3 Key Conclusions to Explain:"; r.font.size = Pt(21); r.font.bold = True; r.font.color.rgb = NAVY

    conclusions = [
        ("1. Best Accuracy & Dice:", " Morph-ViT achieves highest accuracy (92.35%) and Dice (77.79%), matching human expert agreement (~78-80%)."),
        ("2. Catches Thin Vessels:", " Traditional morphology missed thin capillaries (Recall only 53%). Morph-ViT boosts recall to 76.54%."),
        ("3. Eliminates False Alarms:", " Standard U-Net has low precision (62.81%). Morph-ViT's morphological prior raises precision to 79.09%."),
        ("\nLiterature References:", ""),
        ("[1] J. Staal et al., ", "IEEE TMI, 2004 (DRIVE benchmark)."),
        ("[2] A. Dosovitskiy et al., ", "ICLR, 2021 (Vision Transformers)."),
        ("[3] O. Ronneberger et al., ", "MICCAI, 2015 (U-Net).")
    ]
    for lbl, desc in conclusions:
        p = tf7.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run(); r.text = lbl
        if "\n" in lbl:
            r.font.size = Pt(15.5); r.font.bold = True; r.font.color.rgb = NAVY
        elif "[" in lbl:
            r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = NAVY
        else:
            r.font.size = Pt(14.5); r.font.bold = True; r.font.color.rgb = NAVY

        if desc:
            r = p.add_run(); r.text = desc
            r.font.size = Pt(13 if "[" in lbl else 14); r.font.color.rgb = DARK

    out_file = os.path.join(proj_dir, "presentation_simple.pptx")
    prs.save(out_file)
    print(f"Simple presentation saved directly to: {out_file}")

if __name__ == "__main__":
    docs_dir = None
    for d in os.listdir(r"C:\Users\pooja\OneDrive"):
        if "li" in d.lower():
            docs_dir = os.path.join(r"C:\Users\pooja\OneDrive", d)
            break
    proj = os.path.join(docs_dir, "retinal-vessel-segmentation")
    create_simple_deck(proj)
