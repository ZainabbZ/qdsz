"""
pages/3_Science.py
Quantum ALS Diagnostic Engine — Science Explainer
Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Quantum ALS Diagnostic Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { background-color: #f8fafc; max-width: 1200px; padding-top: 1.5rem; }
[data-testid="stSidebar"] { background-color: #1e293b !important; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
.disclaimer-banner {
    background: #fff7ed; border-left: 5px solid #f97316;
    padding: 0.75rem 1rem; border-radius: 0 6px 6px 0;
    margin-bottom: 1rem; font-size: 13px; color: #92400e;
}
.equation-box {
    background: #f1f5f9; border-left: 3px solid #3b82f6;
    border-radius: 0 6px 6px 0; padding: 0.75rem 1rem;
    font-family: monospace; font-size: 14px; margin: 0.5rem 0;
    color: #1e293b;
}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────────
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
                   index=2, key="nav_science")
    if nav == "📋 Assessment":
        st.switch_page("pages/1_Assessment.py")
    elif nav == "📊 Clinical Report":
        st.switch_page("pages/2_Clinical_Report.py")
    st.divider()
    with st.expander("ℹ About this tool"):
        st.markdown(
            "Quantum biophysics model applying the Lindblad master equation to SOD1-ALS "
            "B-factor data. 17 mutations. Validated vs QuTiP (< 1×10⁻⁶ deviation)."
        )

# ── Disclaimer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
⚠ <strong>RESEARCH PROTOTYPE — FOR INVESTIGATIONAL USE ONLY</strong> —
This tool does not replace clinical judgment, genetic testing, or EMG evaluation.
<em>Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO | Egypt.</em>
</div>
""", unsafe_allow_html=True)

st.title("🔬 Science Explainer")
st.markdown(
    "Plain-English explanations for neurologists who want to understand the physics behind "
    "the Quantum ALS Diagnostic Engine. No equations shown by default — everything is explained "
    "with clinical analogies."
)

# ── Section 1 ────────────────────────────────────────────────────────────────────
with st.expander("📡 1 — What is quantum decoherence and why does it matter in ALS?", expanded=True):
    st.markdown("""
**Think of it like this:**

The voltage-sensing domain (VSD) of a neuronal Kv channel — the molecular switch that triggers
an action potential — behaves like a tiny quantum object. In a healthy neuron, it exists in a
*quantum superposition*: a blend of "open" and "closed" states simultaneously, like a coin
spinning in the air.

This superposition is what gives the channel exquisite sensitivity to small voltage changes.

**What SOD1 mutations do:**

SOD1 mutations increase *structural noise* — measured as B-factors in X-ray crystallography PDB files.
Think of B-factor as "how much a protein jiggles." Higher jiggling = more noise.

This noise accelerates **decoherence**: the coin stops spinning and falls to one side prematurely.
The channel loses its quantum sensitivity before the membrane is ready to fire, causing a *delay*
in action potential propagation.

**Why it matters clinically:**

The time it takes for coherence to fall below 0.5 (the functional threshold) determines the
signalling delay in motor neurons. In fast-progressing mutations like A4V, this happens nearly
10× faster than in slow mutations like H46R — directly predicting the clinical aggressiveness.
    """)

# ── Section 2 ────────────────────────────────────────────────────────────────────
with st.expander("📊 2 — What is the Quantum Decoherence Score (QDS)?"):
    st.markdown("""
**QDS is a clinical translation of protein physics.**

It maps the mutation's dephasing rate (γ_phi, derived from the protein's B-factor) onto a
**0–100% scale** with two real-world anchors:

- **0% = H46R** — the slowest known SOD1-ALS mutation (>15 year median survival)
- **96.5% = A4V** — the most aggressive known SOD1-ALS mutation (<1 year median survival)

**What QDS is NOT:**
- It is NOT a probability of having ALS.
- It is NOT a probability of dying within a certain time.
- It IS a measure of *structural instability relative to known mutations*.

**How to use it clinically:**

| QDS Range | Risk Tier | Meaning |
|---|---|---|
| 0–15% | LOW | Consistent with very slow-progressing or atypical SOD1-ALS |
| 15–40% | MODERATE | Consistent with classic SOD1-ALS (2–5 years, e.g. G93A) |
| 40–70% | HIGH | Consistent with rapidly progressive SOD1-ALS (<2 years) |
| >70% | CRITICAL | Consistent with fulminant SOD1-ALS (<1 year, e.g. A4V) |
    """)

# ── Section 3 ────────────────────────────────────────────────────────────────────
with st.expander("✅ 3 — How was G93A validated?"):
    st.markdown("""
**The core validation finding (Block 8B):**

G93A is the most studied ALS mutation in the world (mouse model since 1994).
The model's calibration is anchored on this mutation:

- Wild-Type (healthy) γ_phi = **0.080**
- G93A γ_phi = **0.320** = exactly **4.00 × Wild-Type**

This 4× ratio matches the `ALS_PATHOLOGY_MULTIPLIER` derived from comparing B-factors
in PDB structures 2NNX (G93A) vs 1HL5 (WT).

**What this means in practice:**

Running the Lindblad solver for both WT and G93A and fitting the early-time exponential decay
gives γ_eff(ALS) / γ_eff(WT) ≈ **4.00** — a **300% increase in decoherence rate**.

This was independently verified against QuTiP's `mesolve` function with a maximum deviation
of < 1×10⁻⁶ across all 500 time points.

**G93A electrophysiology prediction:**
The model predicts an action potential latency of **0.2974 ms** (range 0.30–0.32 ms),
consistent with the Block 12 coupling equations applied to G93A's 37.1% QDS.
    """)

# ── Section 4 ────────────────────────────────────────────────────────────────────
with st.expander("⚙ 4 — How do the coupling equations work?"):
    st.markdown(
        "The three coupling equations translate the quantum result (ΔC — coherence loss) "
        "into measurable electrophysiology parameters:"
    )
    st.markdown("""
<div class="equation-box">
τ_ALS = τ_WT × (1 + K_TAU × ΔC) = 0.85 × (1 + 1.25 × ΔC)
</div>

<div class="equation-box">
V½_ALS = V½_WT + K_V × ΔC = −28.5 + 6.0 × ΔC
</div>

<div class="equation-box">
G_max_ALS = G_max_WT × exp(−K_G × ΔC) = 45.3 × exp(−0.35 × ΔC)
</div>
""", unsafe_allow_html=True)
    st.markdown("""
**Clinical interpretation:**

- **τ_ALS** — How long it takes the channel to open after a voltage step.
  Higher ΔC → slower activation → delayed action potentials. Measured in milliseconds.

- **V½_ALS** — The voltage at which half the channels are open. A more positive (depolarized)
  V½ means the neuron needs more stimulation to fire — consistent with motor neuron hypoexcitability
  seen in ALS EMG studies.

- **G_max_ALS** — The peak ion current the channel can carry. Reduced G_max contributes to the
  characteristic reduction in CMAP amplitude seen on nerve conduction studies.

The coupling constants (K_TAU = 1.25, K_V = 6.0, K_G = 0.35) are phenomenological parameters
calibrated from Bhatt et al. (2010) and Tegmark (2000).
    """)

# ── Section 5 ────────────────────────────────────────────────────────────────────
with st.expander("⚠ 5 — What are the model's limitations?"):
    st.markdown("""
**This model is a research prototype. Its current limitations are:**

1. **No wet-lab validation yet.** All calibrations are derived from PDB B-factors and
   published clinical survival data. No direct patient electrophysiology or fluorescence
   measurements have been made.

2. **SOD1-specific.** The model is calibrated on the 17 SOD1 mutations in the reference panel.
   For C9orf72, TDP-43, FUS, and sporadic (non-SOD1) ALS, the tool falls back to
   clinical estimation mode — results carry significantly higher uncertainty.

3. **Synthetic population basis.** The 204-case clinical big-data set used for the
   machine learning components was generated synthetically based on published population
   statistics, not from actual patient records.

4. **Phenomenological coupling constants.** K_TAU, K_V, and K_G are estimated from
   existing biophysics literature, not derived from first-principles quantum mechanics.

5. **Individual variation.** ALS has wide phenotypic heterogeneity. Even within a single
   mutation (e.g. I113T), survival ranges from 1 to 15+ years. Population medians in the
   model should never be applied to individual prognosis without clinical context.

6. **Proxy structures.** G37R and I113T use structural proxies (PDB structures from other
   mutations with similar scaffolds) — predictions for these carry higher uncertainty.
    """)

# ── Section 6: Key Findings Table ────────────────────────────────────────────────
with st.expander("📋 6 — Key findings at a glance"):
    import pandas as pd
    findings = {
        "Finding": [
            "G93A decoherence vs WT",
            "Predicted action potential latency (G93A)",
            "Total coherence loss (ΔC)",
            "Time to coherence threshold (G93A)",
            "Mutations modeled",
            "Clinical Big Data set",
            "QuTiP validation agreement",
            "Pearson r (quantum ↔ biology)",
            "r (decoherence ↔ signal latency)",
        ],
        "Value": [
            "300% faster (4.00×)",
            "0.2974 ms (range 0.30–0.32 ms)",
            "29.99% (~30%)",
            "t = 0.0626 simulation units",
            "17 SOD1 variants",
            "204 synthetic cases",
            "< 1×10⁻⁶ maximum deviation",
            "r = 0.5058, p < 0.0001",
            "r > 0.98",
        ],
    }
    st.dataframe(pd.DataFrame(findings), use_container_width=True, hide_index=True)
