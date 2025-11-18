# app.py
import streamlit as st
import numpy as np
from pathlib import Path
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Hazard Risk Ratio — Dialysis",
    page_icon="🩺",
    layout="centered"
)

# Coefficients
B_GENDER = 0.452
B_AGE = 0.017
B_COMORBID = -0.138

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main-container {
    max-width: 620px;
    margin: 0 auto;
    padding: 0;
}

.title-area {
    text-align: center;
    margin-bottom: 4px;
}
h1 {
    font-weight: 700;
    font-size: 1.9rem;
    margin-bottom: 0.3rem;
}
.subtext {
    color: #6b7280;
    font-size: 0.92rem;
    margin-top: -8px;
    text-align: center;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
}
.center-btn {
    display: flex;
    justify-content: center;
    margin-top: 14px;
}
.download-center {
    text-align: center;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- MAIN CONTAINER ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------- HEADER WITH LOGO ----------
logo_path = Path("logo.png")
if logo_path.exists():
    st.image(Image.open(logo_path), width=64)
else:
    st.write("<div style='text-align:center;font-size:42px'>🩺</div>", unsafe_allow_html=True)

st.markdown("""
<div class="title-area">
<h1>Hazard Risk Ratio Calculator for Dialysis Patients</h1>
</div>
<div class="subtext">Dialysis patient risk estimate (Cox model)</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- INPUT CARD ----------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    age = st.number_input("Age at start of dialysis (years)", 0, 120, 50, 1)

    comorb_options = [
        "Diabetic Nephropathy",
        "Hypertensive Nephrosclerosis",
        "Chronic Glomerulonephritis",
        "Gouty Nephropathy",
        "Others (e.g. Uropatic Nephropathy)"
    ]
    comorbidity = st.selectbox("Primary comorbidity", comorb_options)

    # Centered button
    center = st.columns([1,1,1])
    with center[1]:
        calculate = st.button("🔍 Calculate Hazard Ratio", use_container_width=True)

    if calculate:
        g = 1 if gender.lower() == "male" else 0
        c = comorb_options.index(comorbidity)
        hr = np.exp(B_GENDER*g + B_AGE*float(age) + B_COMORBID*c)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;'>Hazard Risk Ratio: {hr:.3f}</h3>", unsafe_allow_html=True)
        st.write(f"<div style='text-align:center;'>The patient's mortality hazard risk is<b>{hr:.2f}×</b> times higher than the baseline hazard.</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Compact metrics

        # CSV download centered
        csv_str = f"gender,age,comorb_idx,hr\n{g},{age},{c},{hr:.6f}\n"
        st.markdown('<div class="download-center">', unsafe_allow_html=True)
    

        st.download_button("Download CSV result", csv_str, "hazard_ratio.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)



st.markdown("</div>", unsafe_allow_html=True)
