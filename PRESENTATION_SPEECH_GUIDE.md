# PRESENTATION SPEECH GUIDE (REVIEW 1 — 11/11/2026)
## Project: Retinal Blood Vessel Segmentation (Morph-ViT)
### Deck: `presentation_simple.pptx` (7 Slides)

This guide provides a simple, conversational 30-to-45-second speaking script for each slide, plus likely faculty questions and straightforward answers.

---

### SLIDE 1: Title & Team Credentials
* **Slide Contents:** Project Title, Course (FIP), Department, Team Names & USNs.
* **What to Say (30 Seconds):**
  > *"Good morning Mam/Sir. Today our team is presenting our Course Project for Fundamentals of Image Processing, titled **'Retinal Blood Vessel Segmentation Using Mathematical Morphology and Vision Transformers'**.*  
  > *Our team members are Krithin Kusharaj Salian, Niriksha, and Pavan L Poojary from the Department of Computer Science & Engineering.*  
  > *In this project, we combine syllabus concepts from Units II and III with modern Vision Transformers to automate eye vessel extraction."*

---

### SLIDE 2: Why This Project? (Clinical Need & Problem)
* **Slide Contents:** The Clinical Need, The Bottleneck (1-2 hours manual tracing), Our Goal, Core Image Challenges.
* **What to Say (45 Seconds):**
  > *"To explain the clinical motivation:*  
  > *Retinal blood vessels are the only blood vessels in the human body that can be seen directly without surgery.*  
  > *Doctors examine them to detect major diseases early—including Diabetic Retinopathy (which is a leading cause of adult blindness), High Blood Pressure, and Stroke risk.*  
  > *Right now, eye specialists have to trace these tiny vessels by hand, which takes 1 to 2 hours per photograph and causes eye fatigue.*  
  > *Our goal is to automate this process in seconds.*  
  > *The main image processing challenge is that blood vessels occupy only 10% of the image, while 90% is background, and thin peripheral capillaries are very faint."*

---

### SLIDE 3: The Dataset & Evaluation Standard
* **Slide Contents:** DRIVE Dataset (40 images), Doctor Ground Truth, Strict Field of View (FOV) Rule.
* **What to Say (35 Seconds):**
  > *"For our benchmark, we used the DRIVE dataset, which is a standard, publicly available medical benchmark containing 40 retinal fundus photographs.*  
  > *We split the data evenly: 20 images for training and 20 images strictly for testing.*  
  > *Every image comes with expert ground truth masks drawn and verified by ophthalmologists.*  
  > *Very importantly, as per the guidelines, we evaluate our model **strictly inside the circular retinal mask (Field of View)**.*  
  > *We exclude the outer black border so that our accuracy metrics are 100% fair and clinically honest."*

---

### SLIDE 4: Our Methodology (3 Simple Steps)
* **Slide Contents:** Step 1: Preprocessing (Green Channel, CLAHE, Top-Hat), Step 2: Morph-ViT Model (CNN + ViT), Step 3: Speck Cleaning.
* **What to Say (50 Seconds):**
  > *"Our proposed framework, called **Morph-ViT**, works in three simple steps:*  
  > * **Step 1 is Classical Image Processing from Units II and III:**  
  >   First, we extract the Green Channel because blood absorbs green light best, giving maximum vessel contrast.  
  >   Second, we apply CLAHE to fix uneven lighting across the round eye surface.  
  >   Third, we apply a 12-direction linear White Top-Hat filter to highlight vessels in every orientation.*  
  > * **Step 2 is Deep Learning with Vision Transformers:**  
  >   We combine the original image with our morphological map into a 4-channel input.  
  >   A CNN stem captures sharp vessel edges, while a 4-layer Vision Transformer uses self-attention to connect long vessel branches.*  
  > * **Step 3 is Post-Processing:**  
  >   A simple connected-component filter automatically discards tiny isolated noise specks smaller than 10 pixels."*

---

### SLIDE 5: The 6 Mandatory Experiments
* **Slide Contents:** Experiment Table comparing Traditional, ML/DL Baseline, Proposed Hybrid, Hyperparameter Tuning, Ablation, and Performance.
* **What to Say (35 Seconds):**
  > *"As required by the course guidelines, we conducted all 6 mandatory comparative experiments:*  
  > * **Exp 1:** Traditional baseline using Top-Hat morphology and CLAHE.  
  > * **Exp 2:** Deep learning baseline using the standard U-Net architecture.  
  > * **Exp 3:** Our proposed hybrid model, Morph-ViT.  
  > * **Exp 4:** Hyperparameter tuning across decision thresholds from 0.3 to 0.7.  
  > * **Exp 5:** An ablation study testing the model with and without the morphological input.  
  > * **Exp 6:** A comprehensive performance comparison measuring Accuracy, Dice score, Speed, and Model Size."*

---

### SLIDE 6: Visual Results & Error Maps
* **Slide Contents:** Embedded output error panel with Color-Coded Key (Green=Correct, Red=Missed, Blue=Noise, Black=Background).
* **What to Say (40 Seconds):**
  > *"Here you can see the visual outputs and our color-coded error map:*  
  > * **Green** shows correctly detected vessels.  
  > * **Red** shows missed vessels. Notice that traditional morphology misses 47% of thin capillaries, but our Morph-ViT cuts missed vessels down to only 23%!  
  > * **Blue** shows false noise dots, which are suppressed by our morphological speck filter.  
  > * **Black** is correctly identified background.*  
  > *The key takeaway is that Morph-ViT keeps vessels continuous and connected without breaking at junctions."*

---

### SLIDE 7: Final Results & Key Conclusions
* **Slide Contents:** Results Table (Accuracy 92.35%, Dice 77.79%, Recall 76.54%, Precision 79.09%) and 3 Key Takeaways.
* **What to Say (45 Seconds):**
  > *"Looking at our final numerical results:*  
  > * **Traditional morphology** is fast (177 ms) and has high specificity (97.4%), but it misses thin vessels, giving a low recall of only 53%.  
  > * **Standard U-Net** catches more vessels (85.4% recall), but gives many false alarms, resulting in a low precision of 62.8%.  
  > * **Our Proposed Morph-ViT** achieves the best balance:  
  >   It reaches the highest overall **Accuracy of 92.35%**, the highest **Dice score of 77.79%** (a +13.6% improvement over morphology), and matches human expert agreement levels.*  
  > *In conclusion, combining classical morphology with Vision Transformers solves both capillary dropout and false alarms.*  
  > *Thank you Mam/Sir, we are now ready for your questions."*

---

### Potential Faculty Questions & Quick Answers:

1. **Q: Why did you pick the Green channel instead of grayscale or Red?**  
   * **A:** *"Hemoglobin in blood absorbs light maximally in the green wavelength (around 540–580 nm). The red channel is over-saturated and the blue channel is noisy, so the green channel provides the highest contrast between blood vessels and the retinal background."*

2. **Q: Why use Top-Hat morphology with 12 angles?**  
   * **A:** *"Blood vessels run in all directions (horizontal, vertical, diagonal). A single linear structuring element only catches vessels at one angle. By rotating the line structuring element across 12 angles from 0° to 165° and taking the maximum response, we capture vessels in every direction."*

3. **Q: Why use a Vision Transformer (ViT) instead of just regular U-Net?**  
   * **A:** *"Standard CNNs only look at small local neighborhoods of pixels (typically 3×3). Vision Transformers use self-attention across the whole image, allowing the network to understand that two broken vessel segments belong to the same continuous vessel branch."*

4. **Q: Why is your evaluation strictly inside the FOV?**  
   * **A:** *"Because fundus photos are circular with large black borders outside the eye. If you include the black borders, any model that simply predicts 'background' gets artificially inflated 95%+ accuracy. Evaluating strictly inside the FOV measures real clinical vessel detection."*
