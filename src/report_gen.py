import base64
import urllib.parse
from string import Template

def generate_report_html(patient_data, prediction, breakdown, explanation):
    """Generate the HTML report content."""
    clean_exp = explanation.replace("### ", "").replace("**", "")
    
    breakdown_list = ""
    for cls, val in breakdown.items():
        breakdown_list += f"<li>{cls}: {val*100:.1f}%</li>"
    
    html_template = f"""
    <html><head><title>Lung Scan Report</title>
    <style>body {{ font-family: sans-serif; line-height: 1.6; padding: 30px; color: #333; }}</style>
    </head><body>
    <h2 style="color: #1e293b;">Lung Scan Analysis Report</h2>
    <hr>
    <div style="background: #f8fafc; padding: 15px; border-radius: 8px;">
        <p style="margin: 0;"><b>Patient Name:</b> {patient_data['name']}<br>
        <b>Age:</b> {patient_data['age']}<br>
        <b>Gender:</b> {patient_data['gender']}</p>
    </div>
    <h3 style="color: #1e293b; margin-top: 30px;">Analysis Findings</h3>
    <p><b>Primary Condition Detected:</b> <span style="color:#d97706; font-size:1.1em; font-weight:bold;">{prediction}</span></p>
    <h4>Confidence Breakdown:</h4>
    <ul>
        {breakdown_list}
    </ul>
    <h3 style="color: #1e293b;">Detailed Explanation</h3>
    <div style="background: #eff6ff; padding: 20px; border-left: 4px solid #3b82f6; border-radius: 4px;">
        <p>{clean_exp.replace(chr(10), '<br>')}</p>
    </div>
    <hr style="margin-top: 40px;"><p><small>Disclaimer: AI-generated analysis snippet. Must be verified by a certified doctor.</small></p>
    </body></html>
    """
    return html_template

def generate_download_button_html(html_content, patient_name):
    """Generate the download button HTML for the Gradio UI."""
    encoded = base64.b64encode(html_content.encode('utf-8')).decode()
    data_uri = f"data:text/html;base64,{encoded}"
    
    # Safe filename formatting
    safe_name = urllib.parse.quote(f"{patient_name.replace(' ','_')}_lung_report.html")
    
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
    return download_button_html
