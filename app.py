# app.py
import streamlit as st
import numpy as np
from pathlib import Path
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Hazard Risk Ratio — Dialysis",
    page_icon="🩺",
    layout="centered"
)

# ---------- COEFFICIENTS ----------
B_GENDER = 0.452
B_AGE = 0.017
B_COMORBID = -0.138

# ---------- RISK THRESHOLDS & COLORS ----------
RISK_THRESHOLDS = {
    "Low Risk": 2.5,
    "Medium Risk": 4.0,
    "High Risk": 6.0,
    "Very High Risk": float('inf')
}

RISK_COLORS = {
    "Low Risk": "#2E8B57",      # Green
    "Medium Risk": "#FF8C00",   # Orange
    "High Risk": "#C0392B",     # Red
    "Very High Risk": "#7B0000" # Dark Red
}

# ---------- TREATMENTS ----------
TREATMENT_RECOMMENDATIONS = {
    "Diabetic Nephropathy": {
        "Low Risk": "• Standard diabetes management\n• Target HbA1c <7.0%\n• Quarterly renal function monitoring\n• Lifestyle counseling",
        "Medium Risk": "• Enhanced glycemic control\n• Consider SGLT2 inhibitors\n• Bi-monthly clinical assessment\n• Cardiovascular risk screening",
        "High Risk": "• Intensive diabetes management\n• SGLT2 inhibitors + GLP-1 agonists\n• Monthly multidisciplinary review\n• Cardiac function assessment",
        "Very High Risk": "• Aggressive glycemic control\n• Multiple drug therapy\n• Weekly symptom monitoring\n• Palliative care integration"
    },
    "Hypertensive Nephrosclerosis": {
        "Low Risk": "• Standard BP control (Target <140/90)\n• RAAS inhibitors\n• Lifestyle modification\n• Annual cardiac assessment",
        "Medium Risk": "• Tight BP control (Target <130/80)\n• Multiple antihypertensives\n• Volume management\n• Semi-annual echocardiogram",
        "High Risk": "• Intensive BP management\n• Triple drug therapy\n• Monthly lab monitoring\n• Fluid status optimization",
        "Very High Risk": "• Aggressive BP control\n• Specialist hypertension management\n• Frequent clinical assessment\n• Advanced care planning"
    },
    "Chronic Glomerulonephritis": {
        "Low Risk": "• Standard immunosuppression\n• Regular urine protein monitoring\n• Infection prophylaxis\n• Annual immunological workup",
        "Medium Risk": "• Optimized immunosuppression\n• Monthly proteinuria assessment\n• Cardiovascular protection\n• Specialist nephrology follow-up",
        "High Risk": "• Intensive immunosuppression\n• Bi-weekly clinical assessment\n• Infection risk management\n• Multidisciplinary care coordination",
        "Very High Risk": "• Aggressive immunomodulation\n• Weekly monitoring\n• Comprehensive infection control\n• Transplantation evaluation"
    },
    "Gouty Nephropathy": {
        "Low Risk": "• Uric acid control (Target <6.0 mg/dL)\n• Allopurinol/febuxostat\n• Hydration emphasis\n• Annual joint assessment",
        "Medium Risk": "• Intensive urate lowering\n• Combination therapy\n• Renal function protection\n• Quarterly uric acid monitoring",
        "High Risk": "• Aggressive uric acid management\n• Monthly lab surveillance\n• Tophi management\n• Dietary strict compliance",
        "Very High Risk": "• Maximum urate-lowering therapy\n• Frequent clinical assessment\n• Joint preservation strategies\n• Advanced renal protection"
    }
}

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-container { max-width: 620px; margin: 0 auto; padding: 0; }
.title-area { text-align: center; margin-bottom: 4px; }
h1 { font-weight: 700; font-size: 1.9rem; margin-bottom: 0.3rem; }
.subtext { color: #6b7280; font-size: 0.92rem; margin-top: -8px; text-align: center; }
.center-btn { display: flex; justify-content: center; margin-top: 14px; }
.download-center { text-align: center; margin-top: 12px; }
.result-box { background-color: #f3f4f6; padding: 10px; border-radius: 6px; margin-top: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------- MAIN CONTAINER ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------- HEADER ----------
logo_path = Path("logo.png")
if logo_path.exists():
    st.image(Image.open(logo_path), width=64)
else:
    st.write("<div style='text-align:center;font-size:42px'>🩺</div>", unsafe_allow_html=True)

st.markdown("""
<div class="title-area">
<h1>Hazard Risk Ratio Calculator for Dialysis Patients</h1>
</div>
<div class="subtext">Cox regression-based mortality risk assessment</div>
""", unsafe_allow_html=True)

# ---------- INPUTS ----------
st.write("")
gender = st.selectbox("Gender", ["Male", "Female"], index=0)
age = st.number_input("Age at start of dialysis (years)", 0, 120, 50, 1)
comorb_options = list(TREATMENT_RECOMMENDATIONS.keys())
comorbidity = st.selectbox("Primary comorbidity", comorb_options)

# ---------- CALCULATION ----------
if st.button("🔍 Calculate Hazard Ratio"):
    g_val = 1 if gender.lower() == "male" else 0
    c_val = comorb_options.index(comorbidity)
    hr = np.exp(B_GENDER*g_val + B_AGE*float(age) + B_COMORBID*c_val)

    # Determine risk level
    for level, threshold in RISK_THRESHOLDS.items():
        if hr < threshold:
            risk_level = level
            break
    risk_color = RISK_COLORS[risk_level]

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>Hazard Risk Ratio: {hr:.3f}</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:center;'>Patient mortality hazard risk is <b>{hr:.2f}×</b> higher than baseline.<br>"
        f"Risk Level: <b style='color:{risk_color}'>{risk_level}</b></div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Treatment recommendation
    treatment_text = TREATMENT_RECOMMENDATIONS[comorbidity][risk_level]
    st.subheader("Clinical Treatment Recommendations")
    st.text_area("", treatment_text, height=200)

    # ---------- DOWNLOAD CSV ----------
    csv_str = f"gender,age,comorb_idx,hr,risk_level\n{gender},{age},{c_val},{hr:.6f},{risk_level}\n"
    st.markdown('<div class="download-center">', unsafe_allow_html=True)
    st.download_button("Download CSV result", csv_str, "hazard_ratio.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- DOWNLOAD PDF ----------
    def create_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, "Dialysis Mortality Risk Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, height-90, f"Patient: {gender}, {int(age)} years old")
        c.drawString(50, height-110, f"Primary Comorbidity: {comorbidity}")
        c.drawString(50, height-130, f"Hazard Risk Ratio: {hr:.3f}")
        c.drawString(50, height-150, f"Risk Level: {risk_level}")
        c.drawString(50, height-180, "Clinical Treatment Recommendations:")
        text = c.beginText(50, height-200)
        text.setFont("Helvetica", 11)
        for line in treatment_text.split("\n"):
            text.textLine(line)
        c.drawText(text)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf()
    st.download_button(
        "Download PDF report",
        data=pdf_buffer,
        file_name="hazard_risk_report.pdf",
        mime="application/pdf"
    )

st.markdown("</div>", unsafe_allow_html=True)




st.markdown("</div>", unsafe_allow_html=True)
