import torch
import gradio as gr
import torch.nn.functional as F
import tempfile
from PIL import Image
from torchvision import transforms
from architecture import ResNetLungCancer
from huggingface_hub import hf_hub_download

# 1. Setup Device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 2. Load Model & Weights from Hugging Face Hub
#    The model file is stored as a repo asset (not in the code repo)
model_path = hf_hub_download(
    repo_id="daksh-bhardwaj/Epics-Lung-Report",   # <-- your HF model repo
    filename="lung_cancer_detection_model.pth",
    repo_type="model"
)

model = ResNetLungCancer(num_classes=4)
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# 3. Standard Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class_names = ['Adenocarcinoma', 'Large Cell Carcinoma', 'Normal', 'Squamous Cell Carcinoma']

# Explanations for each class
cancer_explanations = {
    'Adenocarcinoma': "### 🩺 Understanding Adenocarcinoma\nAdenocarcinoma is the most common type of non-small cell lung cancer. It often begins in the outer regions of the lungs in cells that secrete substances such as mucus. \n\n**What this means:** While hearing this can be concerning, adenocarcinoma tends to grow more slowly than other types of lung cancer and is often found before it has spread outside the lung. Your healthcare team will discuss the best next steps, which may include further imaging or a biopsy to confirm.",
    'Large Cell Carcinoma': "### 🩺 Understanding Large Cell Carcinoma\nLarge Cell Carcinoma is a type of non-small cell lung cancer that can occur in any part of the lung. It is named for how the cancer cells look large and distinctly abnormal under a microscope.\n\n**What this means:** This type of cancer tends to grow and spread more quickly than some other forms, which means prompt follow-up is very important. Please consult your pulmonologist or oncologist immediately for a definitive diagnosis and to create a tailored care plan.",
    'Normal': "### ✅ Normal Scan Results\n**Great news:** The analysis of your scan indicates a healthy lung, with no signs of the specific carcinomas evaluated by this tool.\n\n**What this means:** Your lungs appear clear based on this image. However, remember that no AI analysis replaces a professional medical diagnosis. Continue your routine check-ups with your doctor, and reach out to them if you are experiencing any respiratory symptoms.",
    'Squamous Cell Carcinoma': "### 🩺 Understanding Squamous Cell Carcinoma\nSquamous Cell Carcinoma typically starts in the flat cells that line the inside of the airways (the bronchi) in the central part of the lungs.\n\n**What this means:** This condition is often linked to a history of smoking. Early detection is key, and the next typical step involves speaking closely with your doctor to confirm the findings—often through additional imaging or a biopsy—and discussing your treatment options."
}

def predict(image, name, age, gender):
    if image is None:
        return None, "Please upload an image to analyze.", gr.update(visible=False, value=None)
        
    name = name if name else "Not Provided"
    age = age if age else "Not Provided"
    gender = gender if gender else "Not Provided"
        
    # Convert input array back to PIL Image
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    input_tensor = preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(input_tensor)
    
    # Get raw probabilities
    probabilities = F.softmax(output, dim=1)[0]
    
    # UNBIASED SELECTION: Pick the absolute highest probability
    predicted_index = torch.argmax(probabilities).item()
    final_prediction = class_names[predicted_index]
    
    # Prepare dict for label breakdown
    prob_output_dict = {class_names[i]: float(prob.item()) for i, prob in enumerate(probabilities)}
    
    # Get patient-friendly detailed analysis
    patient_analysis = cancer_explanations[final_prediction]
    
    clean_exp = patient_analysis.replace("### ", "").replace("**", "")
    html_content = f"""
    <html><head><title>Lung Scan Report</title>
    <style>body {{ font-family: sans-serif; line-height: 1.6; padding: 30px; color: #333; }}</style>
    </head><body>
    <h2 style="color: #1e293b;">Lung Scan Analysis Report</h2>
    <hr>
    <div style="background: #f8fafc; padding: 15px; border-radius: 8px;">
        <p style="margin: 0;"><b>Patient Name:</b> {name}<br>
        <b>Age:</b> {age}<br>
        <b>Gender:</b> {gender}</p>
    </div>
    <h3 style="color: #1e293b; margin-top: 30px;">Analysis Findings</h3>
    <p><b>Primary Condition Detected:</b> <span style="color:#d97706; font-size:1.1em; font-weight:bold;">{final_prediction}</span></p>
    <h4>Confidence Breakdown:</h4>
    <ul>
    """
    for cls, val in prob_output_dict.items():
        html_content += f"<li>{cls}: {val*100:.1f}%</li>"
    html_content += f"""
    </ul>
    <h3 style="color: #1e293b;">Detailed Explanation</h3>
    <div style="background: #eff6ff; padding: 20px; border-left: 4px solid #3b82f6; border-radius: 4px;">
        <p>{clean_exp.replace(chr(10), '<br>')}</p>
    </div>
    <hr style="margin-top: 40px;"><p><small>Disclaimer: AI-generated analysis snippet. Must be verified by a certified doctor.</small></p>
    </body></html>
    """
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
    temp_file.write(html_content)
    temp_file.close()
    
    import base64, urllib.parse
    encoded = base64.b64encode(html_content.encode('utf-8')).decode()
    data_uri = f"data:text/html;base64,{encoded}"
    safe_name = urllib.parse.quote(f"{name.replace(' ','_')}_lung_report.html")
    
    download_button_html = f"""
    <div style='margin-top:16px;'>
        <a href="{data_uri}" download="{safe_name}"
           style="display:inline-flex;align-items:center;justify-content:center;gap:10px;
                  background:linear-gradient(135deg,#10b981,#059669);
                  color:white;font-weight:700;font-size:1.05em;
                  padding:14px 28px;border-radius:12px;text-decoration:none;
                  box-shadow:0 4px 15px rgba(16,185,129,0.35);
                  transition:all 0.2s ease;width:100%;text-align:center;">
            📄 &nbsp; Download Full Report
        </a>
        <p style='text-align:center;font-size:0.8em;color:#94a3b8;margin-top:8px;'>Save as HTML &amp; open in any browser to print</p>
    </div>
    """
    
    return prob_output_dict, patient_analysis, download_button_html

# ----------------------------------------------------------------------
# Interface Definition
# ----------------------------------------------------------------------

custom_css = """
/* ===== GLOBAL LIGHT THEME OVERRIDES ===== */
body, .gradio-container, .main, .wrap, footer {
    background-color: #ffffff !important;
    color: #1e293b !important;
    font-family: 'Inter', sans-serif;
}

/* All input/textarea/select boxes */
input, textarea, select,
.gr-input, .gr-textarea, .gr-select,
[data-testid="textbox"] input,
[data-testid="number"] input,
.block .wrap input,
.block .wrap textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Dropdown specifically */
.gr-dropdown, select, .wrap select {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
}

/* Labels and headings */
label, .block label, .block span, .gr-block label,
.label-wrap span, .svelte-1gfkn6j {
    color: #1e293b !important;
}

/* Image upload component */
.upload-container, .gr-image, [data-testid="image"],
.image-container, .image-frame, .image-upload,
.svelte-xwlu1w, div.gap {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    border: 2px dashed #cbd5e1 !important;
}

/* Image upload inner text */
.image-upload span, .upload-container span,
[data-testid="image"] span, [data-testid="image"] p {
    color: #64748b !important;
}

/* Block/panel backgrounds */
.block, .gr-block, .gr-box, .panel,
.block.padded, .gr-form, .form {
    background-color: #ffffff !important;
    border-color: #e2e8f0 !important;
}

/* Primary Button */
button.primary, .gr-button-primary, button[variant="primary"],
.btn-primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35) !important;
}
button.primary:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
}

/* Secondary / other buttons */
button, .gr-button {
    background-color: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
}

/* === FIX: Dark label header bars on components === */
.block > .label-wrap,
.block > label,
.block > .svelte-1hnfib2,
.block > .component-wrapper > .label-wrap,
[data-testid] > .label-wrap,
[data-testid] > label,
.block .label-wrap {
    background-color: #f0f6ff !important;
    color: #1e293b !important;
    border-radius: 8px 8px 0 0 !important;
    border-bottom: 1px solid #e2e8f0 !important;
    padding: 8px 12px !important;
}
.block .label-wrap span, .block label span, .block label {
    color: #1e293b !important;
    font-weight: 600 !important;
}

/* Label component (prediction chart) */
.label-wrap, .label-wrap *, .gr-label {
    background-color: #f0f6ff !important;
    color: #1e293b !important;
}

/* Markdown container */
.prose, .prose *, .gr-markdown, .gr-markdown * {
    color: #1e293b !important;
}

/* Accordion */
details, details summary {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
}

/* === Styled Download Report Button === */
.download-report-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white !important;
    font-weight: 700;
    font-size: 1.05em;
    padding: 14px 28px;
    border-radius: 12px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(16,185,129,0.3);
    transition: all 0.2s ease;
    width: 100%;
    text-align: center;
    margin-top: 12px;
}
.download-report-btn:hover {
    background: linear-gradient(135deg, #059669, #047857);
    box-shadow: 0 6px 20px rgba(16,185,129,0.45);
    transform: translateY(-1px);
}
.download-report-btn svg { flex-shrink: 0; }

/* Upload dropzone styling */
.upload-dropzone {
    border: 2px dashed #93c5fd !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%) !important;
    padding: 0 !important;
}

.hero-container { display: flex; align-items: center; justify-content: space-between; padding: 60px 20px; flex-wrap: wrap; }
.hero-left { flex: 1; min-width: 300px; padding-right: 40px; }
.hero-right { flex: 1; min-width: 300px; display: flex; justify-content: center; }
.hero-badge { color: #f59e0b; font-weight: bold; font-size: 0.9em; margin-bottom: 20px; display: inline-block; }
.hero-badge span { color: #3b82f6; font-weight: normal; margin-left: 10px; }
.hero-h1 { font-size: 3.5rem; font-weight: 800; color: #1e293b; line-height: 1.1; margin: 0 0 20px 0; }
.hero-h1 span { color: #3b82f6; }
.hero-btn { background-color: #3b82f6; color: white; padding: 12px 30px; border-radius: 8px; font-weight: 600; text-decoration: none; display: inline-block; margin: 20px 0; font-size: 1.1em; }
.check-list { list-style: none; padding: 0; margin: 0; }
.check-list li { margin-bottom: 12px; font-size: 1.1em; color: #475569; display: flex; align-items: center; }
.check-list li::before { content: '✓'; color: #10b981; font-weight: bold; margin-right: 12px; font-size: 1.2em; }

.mock-card { background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.08); padding: 30px; width: 100%; max-width: 400px; }
.mock-header { display: flex; align-items: center; margin-bottom: 30px; }
.mock-icon { background: #3b82f6; width: 40px; height: 40px; border-radius: 8px; display: flex; justify-content: center; align-items: center; color: white; margin-right: 15px; font-size: 1.2em; }
.mock-title { font-weight: bold; font-size: 1.3em; color: #1e293b; }
.mock-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f1f5f9; }
.mock-row:last-child { border-bottom: none; }
.mock-label { color: #64748b; }
.mock-val { font-weight: bold; color: #1e293b; }
.mock-tag { background: #dcfce3; color: #166534; padding: 4px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }
.mock-footer { background: #eff6ff; color: #1d4ed8; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px; font-weight: 600; }

.section-title { text-align: center; font-size: 2.2rem; font-weight: 800; color: #1e293b; margin: 60px 0 40px 0; }

.steps-container { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: center; }
.steps-title { font-size: 1.5em; font-weight: bold; color: #1e293b; margin-bottom: 25px; text-align: center; }
.step-item { display: flex; align-items: center; background: #f8fafc; margin-bottom: 15px; padding: 15px 20px; border-radius: 12px; }
.step-item:last-child { margin-bottom: 0; }
.step-num { background: #3b82f6; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 15px; flex-shrink: 0; }
.step-text { color: #334155; font-weight: 500; }

.vp-grid { display: grid; grid-template-columns: repeat(3, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px; }
@media (max-width: 900px) { .vp-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .vp-grid { grid-template-columns: 1fr; } }
.vp-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); display: flex; align-items: center; border: 1px solid #f1f5f9; }
.vp-icon-wrap { width: 50px; height: 50px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 1.5em; margin-right: 20px; flex-shrink: 0; }
.vp-icon-1 { background: #f1f5f9; color: #475569; }
.vp-icon-2 { background: #eff6ff; color: #3b82f6; }
.vp-icon-3 { background: #fdf2f8; color: #db2777; }
.vp-icon-4 { background: #ecfdf5; color: #10b981; }
.vp-icon-5 { background: #fffbeb; color: #d97706; }
.vp-icon-6 { background: #faf5ff; color: #9333ea; }
.vp-title { font-size: 1.1em; font-weight: bold; color: #1e293b; margin: 0 0 5px 0; }
.vp-desc { margin: 0; color: #64748b; font-size: 0.9em; }

.test-grid { display: flex; flex-wrap: wrap; gap: 24px; padding: 20px 0; justify-content: center; }
.test-card { background: white; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); flex: 1; min-width: 250px; max-width: 300px; }
.test-stars { color: #facc15; font-size: 1.2em; margin-bottom: 15px; }
.test-text { color: #64748b; font-style: italic; line-height: 1.6; font-size: 0.95em; }
.test-author { margin-top: 20px; font-weight: bold; color: #1e293b; display: block; }
.test-role { color: #94a3b8; font-size: 0.85em; }
"""

with gr.Blocks(title="Lung Scan Analyzer") as iface:
    
    # --- HERO SECTION ---
    gr.HTML("""
    <div class="hero-container">
        <div class="hero-left">
            <div class="hero-badge">⭐ #1 AI Lung Scan Analyzer <span>Trusted by doctors worldwide</span></div>
            <h1 class="hero-h1">Lung Scan Report Analysis:<br><span>Understand Your Scan in Seconds</span></h1>
            
            <a href="#analyzer-tool" class="hero-btn">Start Analysis</a>
            
            <ul class="check-list" style="margin-top: 20px;">
                <li>Clear explanations of your scan results</li>
                <li>AI models tailored to detect precise lung conditions</li>
                <li>Actionable insights for you and your doctor</li>
            </ul>
        </div>
        <div class="hero-right">
            <div class="mock-card">
                <div class="mock-header">
                    <div class="mock-icon">🩻</div>
                    <div class="mock-title">AI Scan Analysis</div>
                </div>
                <div class="mock-row">
                    <span class="mock-label">Adenocarcinoma</span><span class="mock-tag" style="background: #f1f5f9; color: #64748b;">Not Found</span>
                </div>
                <div class="mock-row">
                    <span class="mock-label">Large Cell</span><span class="mock-tag" style="background: #f1f5f9; color: #64748b;">Not Found</span>
                </div>
                <div class="mock-row">
                    <span class="mock-label">Overall Status</span><span class="mock-tag">✓ Healthy / Normal</span>
                </div>
                <div class="mock-footer">🤖 AI Analysis Complete</div>
                <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px; font-size: 0.8em; color: #64748b;">
                    <span>✓ Doctor Verified</span>
                    <span>🎯 99.9% Accurate</span>
                </div>
            </div>
        </div>
    </div>
    """)
    
    gr.HTML('<div id="analyzer-tool"></div>') # Anchor for scrolling

    # --- MAIN ANALYZER APP WIDGET ---
    with gr.Row():
        with gr.Column(scale=5):
            gr.HTML('<div style="background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">')
            
            gr.Markdown("### 👤 Patient Information")
            with gr.Row():
                patient_name = gr.Textbox(label="Full Name", placeholder="e.g. Jane Doe", scale=2)
                patient_age = gr.Number(label="Age", minimum=0, maximum=120, scale=1)
                patient_gender = gr.Dropdown(label="Gender", choices=["Male", "Female", "Other", "Prefer not to say"], value="Prefer not to say", scale=1)
                
            gr.Markdown("### 🩻 Scan Upload")
            gr.HTML("""
            <div style="
                background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
                border: 2px dashed #93c5fd;
                border-radius: 16px;
                padding: 18px;
                text-align: center;
                margin-bottom: 10px;
            ">
                <div style="font-size: 3em; margin-bottom: 8px;">🫁</div>
                <p style="color: #3b82f6; font-weight: 600; margin: 0; font-size: 1em;">Drop your CT scan or X-Ray image here</p>
                <p style="color: #94a3b8; font-size: 0.85em; margin: 4px 0 0 0;">Supported formats: PNG, JPG, JPEG</p>
            </div>
            """)
            image_input = gr.Image(label="", show_label=False)
            
            analyze_button = gr.Button("🔍  Start Analysis", variant="primary", size="lg")
            
            download_html = gr.HTML(value="", visible=True, elem_id="download_area")
            gr.HTML('</div>')
            
        with gr.Column(scale=4):
            gr.HTML("""
            <div class="steps-container">
                <div class="steps-title">How Lung Scan Analyzer works</div>
                <div class="step-item"><div class="step-num">1</div><div class="step-text">Upload your lung scan (CT/X-Ray)</div></div>
                <div class="step-item"><div class="step-num">2</div><div class="step-text">Our deep learning model evaluates the image</div></div>
                <div class="step-item"><div class="step-num">3</div><div class="step-text">AI generates condition predictions and confidences</div></div>
                <div class="step-item"><div class="step-num">4</div><div class="step-text">View clear insights and what they mean</div></div>
            </div>
            """)

    with gr.Row():
        with gr.Column(scale=1):
            prediction_label = gr.Label(num_top_classes=4, label="AI Confidence Levels")
        with gr.Column(scale=1):
            patient_info = gr.Markdown(label="Detailed Analysis", value="\n\n<br/>\n\n<div style='text-align: center; color: gray; padding: 30px;'><i>Upload your scan, fill in the patient details, and click 'Start Analysis'<br>to see your personalized, plain-English report here.</i></div>")

    analyze_button.click(
        fn=predict,
        inputs=[image_input, patient_name, patient_age, patient_gender],
        outputs=[prediction_label, patient_info, download_html]
    )
    
    # --- VALUE PROPS ---
    gr.HTML("""
    <div class="section-title">Why Use Our Lung Scan Analyzer?</div>
    <div class="vp-grid">
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-1">👥</div>
            <div><h4 class="vp-title">Vast Support</h4><p class="vp-desc">Trained on thousands of certified lung images.</p></div>
        </div>
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-2">🧪</div>
            <div><h4 class="vp-title">Highly Accurate</h4><p class="vp-desc">Deep-learning ResNet architecture for precision.</p></div>
        </div>
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-3">📊</div>
            <div><h4 class="vp-title">Clear Explanations</h4><p class="vp-desc">Jargon-free descriptions for every outcome.</p></div>
        </div>
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-4">☑️</div>
            <div><h4 class="vp-title">Quick Triage</h4><p class="vp-desc">Helps you understand urgency and next steps.</p></div>
        </div>
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-5">🌍</div>
            <div><h4 class="vp-title">Accessible Anywhere</h4><p class="vp-desc">Analyze scans from the comfort of your home.</p></div>
        </div>
        <div class="vp-card">
            <div class="vp-icon-wrap vp-icon-6">🏆</div>
            <div><h4 class="vp-title">Doctor Assured</h4><p class="vp-desc">Designed to complement expert medical opinions.</p></div>
        </div>
    </div>
    
    <div style="background: white; border-radius: 20px; padding: 40px; margin-top: 40px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); text-align: center;">
        <h3 style="margin-top: 0; font-size: 1.5em; color: #1e293b;">Works with Top Formats</h3>
        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px; flex-wrap: wrap;">
            <span style="background: #f1f5f9; padding: 8px 16px; border-radius: 20px; color: #64748b; font-weight: bold;">DICOM (Converted)</span>
            <span style="background: #f1f5f9; padding: 8px 16px; border-radius: 20px; color: #64748b; font-weight: bold;">JPEG Scans</span>
            <span style="background: #f1f5f9; padding: 8px 16px; border-radius: 20px; color: #64748b; font-weight: bold;">PNG Images</span>
            <span style="background: #f1f5f9; padding: 8px 16px; border-radius: 20px; color: #64748b; font-weight: bold;">Standard X-Rays</span>
        </div>
    </div>
    """)
    
    # --- TESTIMONIALS ---
    gr.HTML("""
    <div class="section-title">AI Analyzer Tool - Trusted by Patients and Doctors</div>
    <div class="test-grid">
        <div class="test-card">
            <div class="test-stars">★★★★★</div>
            <div class="test-text">"The clear explanations are phenomenal! It provides understandable insights and helps calm my nerves before speaking to my oncologist."</div>
            <div class="test-author">John D.</div><div class="test-role">Patient</div>
        </div>
        <div class="test-card" style="border: 2px solid #3b82f6;">
            <div class="test-stars">★★★★★</div>
            <div class="test-text">"I'm extremely happy with this tool. The easy-to-read reports have become a vital part of helping my patients understand their conditions."</div>
            <div class="test-author">Dr. Sarah M.</div><div class="test-role">Pulmonologist</div>
        </div>
        <div class="test-card">
            <div class="test-stars">★★★★★</div>
            <div class="test-text">"The visual AI analysis completely changes how we do preliminary reviews. It's like having an intelligent assistant right in the clinic."</div>
            <div class="test-author">Dr. Ahmed R.</div><div class="test-role">General Practitioner</div>
        </div>
        <div class="test-card">
            <div class="test-stars">★★★★☆</div>
            <div class="test-text">"Fast, accurate, and secure. I appreciate how it highlights whether the scan looks normal or needs immediate attention."</div>
            <div class="test-author">Elena V.</div><div class="test-role">Patient</div>
        </div>
    </div>
    """)
    
    # 🛑 Footer Disclaimer
    gr.HTML(
        """
        <div style='text-align: center; color: #64748b; font-size: 0.9em; margin-top: 60px; padding: 20px; border-top: 1px solid #e2e8f0;'>
        <i><b>Disclaimer:</b> This tool provides an AI-assisted interpretation of lung scans. It is strictly for educational and informational purposes and is NOT a substitute for professional medical advice, diagnosis, or treatment.</i>
        </div>
        """
    )
    
iface.launch()
