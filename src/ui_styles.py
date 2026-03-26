CUSTOM_CSS = r"""
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

/* Clickable layer fix: We hide Gradio's text/icons but keep the container clickable */
.upload-dropzone [data-testid="image"] span,
.upload-dropzone .upload-button svg,
.upload-dropzone .icon-container {
    display: none !important;
}

/* Style the empty state which is usually the clickable area */
.upload-dropzone .empty-state {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100% !important;
    min-height: 250px !important;
    cursor: pointer !important;
}

/* Inject custom icon and text INTO the clickable empty state */
.upload-dropzone .empty-state::before {
    content: "" !important;
    display: block !important;
    width: 100px !important;
    height: 100px !important;
    background-image: url('file/assets/lung_icon.png') !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    margin-bottom: 20px !important;
}

.upload-dropzone .empty-state::after {
    content: "Drop your CT scan or X-Ray image here\A(Supported formats: PNG, JPG, JPEG)";
    white-space: pre-wrap !important; 
    color: #3b82f6 !important;
    font-weight: 700 !important;
    font-size: 1.25em !important;
    display: block !important;
    text-align: center !important;
    line-height: 1.6 !important;
}

/* Ensure the background and border apply correctly */
.upload-dropzone, .upload-dropzone .image-container {
    background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%) !important;
    border: 2px dashed #93c5fd !important;
    border-radius: 16px !important;
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
