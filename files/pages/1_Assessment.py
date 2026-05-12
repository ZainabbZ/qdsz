"""
pages/1_Assessment.py
Quantum ALS Diagnostic Engine — Patient Assessment Page
Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_engine import (
    map_clinical_to_quantum,
    get_clinical_recommendations,
    REFERENCE_PANEL,
)

st.set_page_config(
    page_title="Quantum ALS Diagnostic Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { background-color: #f8fafc; max-width: 1200px; padding-top: 1.5rem; }
[data-testid="stSidebar"] { background-color: #1e293b !important; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="metric-container"] {
    background-color: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.07); padding: 1rem;
}
.stButton > button {
    background-color: #1d4ed8; color: #ffffff; font-weight: 600;
    border: none; border-radius: 6px;
}
.stButton > button:hover { background-color: #1e40af; }
.disclaimer-banner {
    background: #fff7ed; border-left: 5px solid #f97316;
    padding: 0.75rem 1rem; border-radius: 0 6px 6px 0;
    margin-bottom: 1rem; font-size: 13px; color: #92400e;
}
label, .stSelectbox label, .stSlider label, .stNumberInput label,
.stTextInput label, .stRadio label {
    font-size: 13px !important; font-weight: 500 !important; color: #374151 !important;
}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem 0;">
        <div style="font-size:18px;font-weight:700;color:#f1f5f9;">🧬 Quantum ALS</div>
        <div style="font-size:12px;color:#94a3b8;">Diagnostic Engine</div>
        <div style="font-size:11px;color:#64748b;margin-top:2px;">ISEF 2026 | CBIO</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    nav = st.radio("Navigation", ["📋 Assessment", "📊 Clinical Report", "🔬 Science"],
                   index=0, key="nav_assessment")
    if nav == "📊 Clinical Report":
        st.switch_page("pages/2_Clinical_Report.py")
    elif nav == "🔬 Science":
        st.switch_page("pages/3_Science.py")

    st.divider()
    with st.expander("ℹ About this tool"):
        st.markdown(
            "A research-grade quantum biophysics model that applies the Lindblad master equation "
            "to SOD1-ALS structural data to predict electrophysiological outcomes. "
            "17 mutations modelled. Validated against QuTiP (< 1×10⁻⁶ deviation)."
        )

# ── Disclaimer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
⚠ <strong>RESEARCH PROTOTYPE — FOR INVESTIGATIONAL USE ONLY</strong><br>
This tool does not replace clinical judgment, genetic testing, or EMG evaluation.<br>
All outputs require clinical correlation and expert review.<br>
<em>Built by Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO | Egypt.</em>
</div>
""", unsafe_allow_html=True)

# ── Page title ──────────────────────────────────────────────────────────────────
st.title("🧬 Patient Assessment")
st.markdown("Enter patient demographics, clinical presentation, and genetic information below.")

# ── Form ────────────────────────────────────────────────────────────────────────
with st.form("assessment_form"):
    col_left, col_right = st.columns(2)

    # ── Left: Demographics ──────────────────────────────────────────────────────
    with col_left:
        st.subheader("👤 Patient Demographics")
        patient_id = st.text_input("Patient ID", placeholder="e.g. ALS-2026-001")
        age = st.number_input("Age at symptom onset", min_value=18, max_value=90, value=55, step=1)
        sex = st.selectbox("Biological sex", ["Male", "Female", "Not specified"])
        family_history = st.radio("Family history of ALS", ["Yes", "No", "Unknown"], horizontal=True)
        months_diag = st.number_input(
            "Months from first symptom to diagnosis",
            min_value=1, max_value=60, value=12, step=1,
        )

    # ── Right: Clinical Presentation ────────────────────────────────────────────
    with col_right:
        st.subheader("🏥 Clinical Presentation")
        onset_region = st.selectbox(
            "Onset region",
            ["Limb (Lower)", "Limb (Upper)", "Bulbar", "Respiratory", "Generalized / Multi-focal"],
        )
        alsfrs_score = st.slider("Current ALSFRS-R score", min_value=0, max_value=48, value=36)
        alsfrs_3m = st.number_input(
            "ALSFRS-R change over last 3 months",
            min_value=0.0, max_value=20.0, step=0.5, value=4.0,
            help="Points lost — enter positive number",
        )
        fvc_percent = st.slider("FVC % predicted", min_value=10, max_value=100, value=80)
        progression_rate = st.selectbox(
            "Progression rate assessment",
            [
                "Slow (<0.3 pts/month decline)",
                "Moderate (0.3–0.5 pts/month)",
                "Rapid (0.5–1.0 pts/month)",
                "Very rapid (>1.0 pts/month)",
            ],
        )

    # ── Genetics ────────────────────────────────────────────────────────────────
    st.subheader("🔬 Genetic Information")
    mutation_known_radio = st.radio(
        "Mutation known?",
        ["Yes — confirmed by genetic testing", "No — genetics pending or not done"],
        key="mutation_known_radio",
    )

    mutation_known = mutation_known_radio.startswith("Yes")
    mutation_selected = None

    if mutation_known:
        mutation_options = [
            "H46R", "D90A", "G41D", "G37R (structural proxy)", "I113T (structural proxy)",
            "V148G", "G85R", "G93A", "T54R", "L38V", "S134N", "E21K", "I104F",
            "E100G", "C111Y", "A4V",
            "Other SOD1 mutation", "Non-SOD1 (C9orf72/TDP-43/FUS/other)",
        ]
        mutation_selected = st.selectbox("Known SOD1 mutation", mutation_options)
        if "Non-SOD1" in mutation_selected:
            st.info(
                "ℹ Non-SOD1 mutations use clinical estimation mode only — "
                "predictions have limited precision."
            )
    else:
        st.info(
            "ℹ Quantum estimation mode active — gamma_phi will be estimated from clinical features."
        )

    # ── Submit ───────────────────────────────────────────────────────────────────
    submitted = st.form_submit_button("🧬 Run Quantum Analysis", use_container_width=True)

# ── On Submit ───────────────────────────────────────────────────────────────────
if submitted:
    if not patient_id.strip():
        st.error("⚠ Please enter a Patient ID before running the analysis.")
        st.stop()

    # Clean mutation key
    mutation_str = ""
    if mutation_known and mutation_selected:
        # Strip proxy annotations, take first token
        mutation_str = mutation_selected.split(" ")[0].upper()
        if "NON-SOD1" in mutation_str or "OTHER" in mutation_str:
            mutation_str = ""
            mutation_known = False

    patient_profile = {
        "patient_id":               patient_id.strip(),
        "age":                      age,
        "sex":                      sex,
        "family_history":           family_history,
        "onset_region":             onset_region,
        "months_onset_to_diagnosis": months_diag,
        "alsfrs_score":             alsfrs_score,
        "alsfrs_3month_change":     alsfrs_3m,
        "fvc_percent":              fvc_percent,
        "progression_rate":         progression_rate,
        "mutation_known":           mutation_known,
        "mutation":                 mutation_str,
    }

    with st.spinner("🔬 Running quantum simulation (Lindblad master equation)..."):
        qr   = map_clinical_to_quantum(patient_profile)
        recs = get_clinical_recommendations(qr, patient_profile)

    st.session_state["qr"]              = qr
    st.session_state["recs"]            = recs
    st.session_state["patient_profile"] = patient_profile

    st.success("✅ Analysis complete — navigating to clinical report...")
    st.switch_page("pages/2_Clinical_Report.py")
