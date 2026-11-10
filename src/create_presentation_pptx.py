"""
Re-generate presentation.pptx with the EXACT benchmark numbers from evaluate_all_three.py
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(proj_dir: str):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    NAVY = RGBColor(16, 37, 66)
    TEAL = RGBColor(0, 150, 166)
    DARK_GRAY = RGBColor(40, 40, 40)
    LIGHT_BG = RGBColor(248, 249, 250)
    WHITE = RGBColor(255, 255, 255)

    def add_header(slide, title_text, category="FUNDAMENTALS OF IMAGE PROCESSING (FIP) COURSE PROJECT"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.15)

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    # SLIDE 1
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.33), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "COURSE PROJECT REVIEW — 11/11/2026"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = TEAL

    p1 = tf1.add_paragraph()
    p1.text = "Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers (Morph-ViT)"
    p1.font.size = Pt(27)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(16)

    p2 = tf1.add_paragraph()
    p2.text = "A Comparative Study on the DRIVE Benchmark Meeting All Course Mandates"
    p2.font.size = Pt(18)
    p2.font.italic = True
    p2.font.color.rgb = RGBColor(200, 225, 235)
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "\nCourse: Fundamentals of Image Processing (FIP)\nTeam Members: [Insert Student Names & USN / Roll Numbers]\nEvaluation Date: 11/11/2026 (First Review) | Final Viva: 24/11/2026"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(220, 220, 220)
    p3.space_before = Pt(24)

    # SLIDE 2
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Slide 1/7: Abstract & Clinical Problem Formulation")
    tb2_left = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.5))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    p = tf2_l.paragraphs[0]; p.text = "Clinical Motivation:"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY
    for b in [
        "The retina provides the human body's ONLY non-invasive, direct in vivo view of the microvascular circulatory system.",
        "Early vascular alterations are direct clinical biomarkers for:",
        "  • Diabetic Retinopathy (leading cause of adult blindness)",
        "  • Arteriosclerosis & Stroke Risk",
        "  • Hypertensive Retinopathy & Glaucoma",
        "Manual tracing by ophthalmologists is labor-intensive, subjective, and clinically unscalable."
    ]:
        p = tf2_l.add_paragraph(); p.text = b; p.font.size = Pt(13); p.space_before = Pt(6)

    tb2_right = s2.shapes.add_textbox(Inches(6.8), Inches(1.4), Inches(5.8), Inches(5.5))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True
    p = tf2_r.paragraphs[0]; p.text = "Core Image Processing Challenges:"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY
    for b in [
        "1. Extreme Class Imbalance: Vessel pixels comprise only ~10% of the retinal area, while background comprises ~90%.",
        "2. Low Local Contrast: Fine terminal microcapillaries have intensity profiles near sensor noise floor.",
        "3. Non-Uniform Illumination: Spherical eyeball geometry induces peripheral vignetting.",
        "4. Confounding Pathologies: Optic disc rim, exudates, and hemorrhages create sharp false-positive edges.",
        "Proposed Solution: Morph-ViT harmonizes physics-driven morphological filtering (Units II & III) with deep self-attention."
    ]:
        p = tf2_r.add_paragraph(); p.text = b; p.font.size = Pt(13); p.space_before = Pt(6)

    # SLIDE 3
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Slide 2/7: Dataset Specification & Validation Protocols")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    for heading, items in [
        ("Public Benchmark: DRIVE (Digital Retinal Images for Vessel Extraction)",
         ["Acquired with a Canon CR5 3CCD camera at 45° Field of View (FOV).",
          "Native resolution: 768 x 584 pixels, 8 bits per color channel.",
          "Standard normalized resolution: 576 x 576 pixels (divisible by patch size P=16 -> 1,296 tokens)."]),
        ("Ground-Truth & FOV Mask Standards (Mandatory Instruction 4):",
         ["Ground-Truth Annotations: Independent manual tracings produced by expert ophthalmologists (1st Manual).",
          "Field of View (FOV) Masks: Exact circular binary masks delineating the valid retinal boundary.",
          "Strict Clinical Protocol: All evaluation metrics are computed STRICTLY INSIDE the FOV mask, avoiding artificial accuracy inflation."]),
        ("Dataset Split Architecture:",
         ["Training Split: 20 fundus images (21_training to 40_training) with expert ground-truth masks.",
          "Test Split: 20 fundus images (01_test to 20_test) for clinical generalization assessment."])
    ]:
        p = tf3.add_paragraph() if tf3.paragraphs[0].text else tf3.paragraphs[0]
        p.text = heading; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY; p.space_before = Pt(12)
        for it in items:
            p_it = tf3.add_paragraph(); p_it.text = "• " + it; p_it.font.size = Pt(12.5); p_it.space_before = Pt(4)

    # SLIDE 4
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Slide 3/7: Proposed Methodology & Morph-ViT Architecture")
    tb4_left = s4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.8), Inches(5.7))
    tf4_l = tb4_left.text_frame
    tf4_l.word_wrap = True
    p = tf4_l.paragraphs[0]; p.text = "Mathematical Image Processing Pipeline:"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY
    for s in [
        "1. Green Channel Isolation: Hemoglobin absorbs peak light at 540-580 nm, providing maximum vessel contrast.",
        "2. CLAHE (8x8 tiles, clip=2.0): Normalizes illumination without amplifying sensor noise.",
        "3. Multi-Directional Top-Hat Filter (Units II & III):",
        "   - Linear structuring elements L of length l=15 px.",
        "   - Rotated across 12 discrete angles (0° to 165° in 15° steps).",
        "   - White Top-Hat: WTH(I) = I - (I ∘ L)",
        "   - Supremum Operator: M(x, y) = max_θ [WTH_θ(I_inv)]",
        "4. Connected-Component Post-Processing: Filters out isolated non-vessel noise specks (< 10 px)."
    ]:
        p = tf4_l.add_paragraph(); p.text = s; p.font.size = Pt(12); p.space_before = Pt(4)

    tb4_right = s4.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.8), Inches(5.7))
    tf4_r = tb4_right.text_frame
    tf4_r.word_wrap = True
    p = tf4_r.paragraphs[0]; p.text = "Deep Vision Transformer (Morph-ViT):"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY
    for s in [
        "• 4-Channel Input: Fuses [R, G, B, Morphological Top-Hat].",
        "• High-Resolution CNN Stem: Dual 3x3 Conv layers preserve fine edge boundaries.",
        "• ViT Patch Embedding: 16x16 patches projected to 128-dimensional token vectors (1,296 tokens).",
        "• 4-Layer Transformer Encoder: Multi-Head Self-Attention (4 heads) models global vascular tree continuity.",
        "• Convolutional Decoder: Progressive bilinear 2x upsampling stages with skip connections from CNN stem.",
        "• Imbalance-Aware Loss: DiceBCELoss with positive weighting w_pos = 4.0 to penalize missed capillary pixels."
    ]:
        p = tf4_r.add_paragraph(); p.text = s; p.font.size = Pt(12); p.space_before = Pt(5)

    # SLIDE 5
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Slide 4/7: Six Mandatory Comparative Experiments")
    rows_data = [
        ["Exp 1", "Traditional Image-Processing Technique", "Multi-directional Top-Hat with linear structuring elements + CLAHE (Units II & III)", "Establish syllabus-aligned baseline."],
        ["Exp 2", "ML/DL-Based Technique", "Standard U-Net architecture (Ronneberger et al., 2015) on 3-channel RGB fundus", "Evaluate gain from pure deep learning."],
        ["Exp 3", "Proposed Hybrid Technique", "Morph-ViT (Top-Hat morphology + CNN stem + ViT Self-Attention)", "Demonstrate hybrid synergy of physics + attention."],
        ["Exp 4", "Hyperparameter Tuning", "Systematic sweep: Thresholds (T=0.30 to 0.70), Structuring Length (l=9, 15, 21), Min-Speck (<=10px)", "Identify optimal operating parameters."],
        ["Exp 5", "Ablation Study", "Modular isolation: Pure Morphology vs. Pure ViT vs. Morph-ViT Raw vs. Full Optimized", "Quantify contribution of each component."],
        ["Exp 6", "Performance Comparison", "Accuracy, Dice, IoU, Precision, Recall, Specificity, AUC, Execution Time, and Model Size (MB)", "Provide full clinical & computational audit."]
    ]
    t5_shape = s5.shapes.add_table(7, 4, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.4))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(1.1); t5.columns[1].width = Inches(3.2); t5.columns[2].width = Inches(4.7); t5.columns[3].width = Inches(2.73)
    for j, h in enumerate(["Exp #", "Method to be Implemented", "Exact Pipeline / Model", "Core Academic Purpose"]):
        cell = t5.cell(0, j); cell.text = h; cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs: p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = WHITE
    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j); cell.text = val; cell.fill.solid(); cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            for p in cell.text_frame.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_GRAY

    # SLIDE 6
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Slide 5/7: Visual Comparison & Color-Coded Error Map Analysis")
    err_panel_path = os.path.join(proj_dir, "outputs", "error_maps", "21_training_error_panel.png")
    if os.path.exists(err_panel_path):
        s6.shapes.add_picture(err_panel_path, Inches(0.8), Inches(1.3), Inches(7.5), Inches(5.8))
    tb6 = s6.shapes.add_textbox(Inches(8.5), Inches(1.3), Inches(4.3), Inches(5.8))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]; p.text = "Color-Coded Error Map Key:"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY
    for e in [
        "🟩 Green (True Positive): Correctly segmented vessel lumens.",
        "🟥 Red (False Negative): Missed microvessels. Traditional morphology misses 47% of capillaries. Morph-ViT dramatically reduces missed vessels to only 23.4%!",
        "🟦 Blue (False Positive): False alarms near disc rim. Effectively suppressed by connected-component filtering.",
        "⬛ Black (True Negative): Background properly identified inside the Field of View.",
        "\nClinical Interpretation:\nMorph-ViT maintains vessel continuity through crossings and bifurcations where traditional filtering fractures."
    ]:
        p = tf6.add_paragraph(); p.text = e; p.font.size = Pt(12); p.space_before = Pt(6)

    # SLIDE 7: Common Results Table with ACTUAL NUMBERS
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Slide 6/7: Mandatory Common Results Table & Key References")

    table_data_7 = [
        ["Accuracy", "89.63%", "88.60%", "92.35% (Best)"],
        ["Dice Score (F1-score)", "64.14%", "72.38%", "77.79% (+13.65%)"],
        ["IoU (Jaccard Index)", "47.21%", "56.71%", "63.66% (Best)"],
        ["Precision", "81.19%", "62.81%", "79.09%"],
        ["Recall (Sensitivity)", "53.00%", "85.38%", "76.54%"],
        ["Specificity", "97.40%", "89.28%", "95.71%"],
        ["AUC-ROC", "75.20%", "94.45%", "94.94% (Best)"],
        ["Execution Time (ms)", "177.4 ms", "671.7 ms", "1,099 ms (CPU)"],
        ["Model Size (MB)", "0.00 MB (Algorithmic)", "1.88 MB", "3.29 MB"],
        ["Trainable Parameters", "0", "482,737", "862,049"]
    ]

    t7_shape = s7.shapes.add_table(11, 4, Inches(0.8), Inches(1.3), Inches(6.8), Inches(5.8))
    t7 = t7_shape.table
    t7.columns[0].width = Inches(2.3); t7.columns[1].width = Inches(1.5); t7.columns[2].width = Inches(1.5); t7.columns[3].width = Inches(1.5)
    headers7 = ["Evaluation Metric", "Traditional Method\n(Morphology)", "ML/DL Method\n(Standard U-Net)", "Proposed Method\n(Morph-ViT)"]
    for j, h in enumerate(headers7):
        cell = t7.cell(0, j); cell.text = h; cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs: p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = WHITE

    for i, row in enumerate(table_data_7):
        for j, val in enumerate(row):
            cell = t7.cell(i + 1, j); cell.text = val; cell.fill.solid(); cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            for p in cell.text_frame.paragraphs: p.font.size = Pt(9.5); p.font.color.rgb = DARK_GRAY

    tb7_ref = s7.shapes.add_textbox(Inches(7.8), Inches(1.3), Inches(4.7), Inches(5.8))
    tf7_r = tb7_ref.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]; p.text = "Key Takeaways & Academic References:"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY
    for r in [
        "1. Morph-ViT achieves the highest Accuracy (92.35%) and Dice score (77.79%), matching expert human agreement (78-80%).",
        "2. Traditional morphology misses thin capillaries (Recall only 53.00%), while Morph-ViT boosts recall to 76.54%.",
        "3. U-Net suffers from lower precision (62.81%), whereas Morph-ViT achieves 79.09% precision thanks to morphological priors.",
        "\nLiterature References:",
        "[1] J. Staal et al., 'Ridge-based vessel segmentation in color images of the retina,' IEEE TMI, 2004.",
        "[2] A. Dosovitskiy et al., 'An image is worth 16x16 words: Transformers for image recognition at scale,' ICLR, 2021.",
        "[3] O. Ronneberger et al., 'U-Net: Convolutional networks for biomedical image segmentation,' MICCAI, 2015.",
        "[4] J. Serra, 'Image Analysis and Mathematical Morphology', Academic Press, 1982."
    ]:
        p = tf7_r.add_paragraph(); p.text = r; p.font.size = Pt(11); p.space_before = Pt(3)

    out_file = os.path.join(proj_dir, "presentation.pptx")
    prs.save(out_file)
    print(f"Presentation saved successfully to: {out_file}")

if __name__ == "__main__":
    docs_dir = None
    for d in os.listdir(r"C:\Users\pooja\OneDrive"):
        if "li" in d.lower():
            docs_dir = os.path.join(r"C:\Users\pooja\OneDrive", d)
            break
    proj = os.path.join(docs_dir, "retinal-vessel-segmentation")
    create_deck(proj)
