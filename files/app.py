"""
app.py
Quantum ALS Diagnostic Engine — Entry Point
Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO
"""

import streamlit as st

st.set_page_config(
    page_title="Quantum ALS Diagnostic Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.main .block-container {
    background-color: #f8fafc;
    max-width: 1200px;
    padding-top: 1.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1e293b !important;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
    font-weight: 500;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    padding: 1rem;
}

/* Primary button */
.stButton > button[kind="primary"],
.stButton > button {
    background-color: #1d4ed8;
    color: #ffffff;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    transition: background-color 0.2s ease;
}
.stButton > button:hover {
    background-color: #1e40af;
}

/* Disclaimer banner */
.disclaimer-banner {
    background: #fff7ed;
    border-left: 5px solid #f97316;
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    margin-bottom: 1rem;
    font-size: 13px;
    color: #92400e;
}

/* Form labels */
label, .stSelectbox label, .stSlider label,
.stNumberInput label, .stTextInput label,
.stRadio label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

/* Hide Streamlit footer and main menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.switch_page("pages/1_Assessment.py")
