"""
pages/2_Clinical_Report.py
Quantum ALS Diagnostic Engine — Clinical Report Page
Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum_engine import (
    REFERENCE_PANEL,
    TAU_ACT_WT, V_HALF_WT, G_MAX_WT,
    COHERENCE_THRESHOLD,
    generate_full_report_text,
)

st.set_page_config(
    page_title="Quantum ALS Diagnostic Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──────────────────────────────────────────────────────────────────
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
.risk-card { border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 0.5rem; color: #fff; }
.rec-card {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 0.75rem 1rem; margin-bottom: 0.5rem;
}
.fda-badge { background:#dcfce7; color:#166534; border-radius:4px; padding:1px 6px; font-size:11px; font-weight:600; }
.exp-badge { background:#fef3c7; color:#92400e; border-radius:4px; padding:1px 6px; font-size:11px; font-weight:600; }
.off-badge { background:#e0f2fe; color:#075985; border-radius:4px; padding:1px 6px; font-size:11px; font-weight:600; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────────
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
                   index=1, key="nav_report")
    if nav == "📋 Assessment":
        st.switch_page("pages/1_Assessment.py")
    elif nav == "🔬 Science":
        st.switch_page("pages/3_Science.py")
    st.divider()
    with st.expander("ℹ About this tool"):
        st.markdown(
            "Quantum biophysics model applying the Lindblad master equation to SOD1-ALS "
            "B-factor data. 17 mutations. Validated vs QuTiP (< 1×10⁻⁶ deviation)."
        )

# ── Disclaimer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
⚠ <strong>RESEARCH PROTOTYPE — FOR INVESTIGATIONAL USE ONLY</strong> —
This tool does not replace clinical judgment, genetic testing, or EMG evaluation.
<em>Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO | Egypt.</em>
</div>
""", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────────
if "qr" not in st.session_state:
    st.warning("⚠ No analysis found. Please complete the patient assessment first.")
    if st.button("← Go to Assessment"):
        st.switch_page("pages/1_Assessment.py")
    st.stop()

qr      = st.session_state["qr"]
recs    = st.session_state["recs"]
pp      = st.session_state["patient_profile"]
now     = datetime.now()
date_str = now.strftime("%Y-%m-%d %H:%M:%S")

# ── Report Header ────────────────────────────────────────────────────────────────
st.title("📊 Clinical Report")

conf_color = {"HIGH": "#22c55e", "MODERATE": "#eab308", "LOW": "#ef4444"}.get(qr["confidence"], "#6b7280")
source_label = "Reference Panel (Genetic)" if qr["source"] == "reference_panel" else "Clinical Estimation"

col_h1, col_h2, col_h3, col_h4 = st.columns(4)
with col_h1:
    st.markdown(f"**Patient ID:** `{pp.get('patient_id','N/A')}`")
    st.markdown(f"**Generated:** {date_str}")
with col_h2:
    st.markdown(f"**Source:** {source_label}")
    st.markdown(f"**Mutation:** `{qr['mutation_key']}`")
with col_h3:
    st.markdown(f"**PDB Structure:** `{qr['pdb_id']}`")
    if qr.get("proxy"):
        st.markdown("⚠ *Structural proxy used*")
with col_h4:
    st.markdown(
        f"**Confidence:** <span style='background:{conf_color};color:#fff;"
        f"border-radius:4px;padding:2px 8px;font-weight:600'>{qr['confidence']}</span>",
        unsafe_allow_html=True,
    )

st.divider()

# ── Row 1: Four Metric Cards ──────────────────────────────────────────────────────
st.subheader("🔑 Key Metrics")
risk_color = qr["risk_color"]
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""<div style="background:{risk_color};border-radius:8px;padding:1rem 1.5rem;color:#fff;">
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;opacity:0.85;">RISK TIER</div>
        <div style="font-size:32px;font-weight:700;">{qr['risk_tier']}</div>
        <div style="font-size:13px;opacity:0.9;">QDS: {qr['qds_pct']:.1f}%</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c2:
    st.metric(
        label="Decoherence Rate vs WT",
        value=f"{qr['rate_increase_pct']:.0f}% faster",
        delta=f"{qr['rate_ratio']:.2f}× WT decoherence rate",
        help="G93A reference benchmark: ~300% (4.00×)",
    )
    st.caption("G93A reference benchmark: ~300% (4.00×)")

with c3:
    st.metric(
        label="Ion Channel Signal Delay",
        value=f"+{qr['delta_tau_ms']*1000:.1f} μs",
        delta=f"vs healthy baseline {TAU_ACT_WT*1000:.0f} ms",
    )
    st.caption("G93A reference: 297–320 μs (0.30–0.32 ms)")

with c4:
    survival_val = qr["survival_est"]
    st.metric(
        label="Estimated Survival",
        value=f"~{survival_val} years",
        delta=" ".join(qr["risk_label"].split()[:5]),
    )
    st.caption("Population median — individual outcomes vary")

st.divider()

# ── Row 2: Electrophysiology Table ────────────────────────────────────────────────
st.subheader("⚡ Electrophysiology Predictions")

delta_tau_mV  = qr["v_half_ALS"] - V_HALF_WT
delta_g       = qr["g_max_ALS"] - G_MAX_WT

electro_data = {
    "Parameter": [
        "Activation Time Constant (τ_act)",
        "Half-Activation Voltage (V½)",
        "Max Conductance (G_max)",
        "Quantum Coherence Loss (ΔC)",
        "Coherence < 0.5 at time",
    ],
    "Wild-Type (Healthy)": [
        f"{TAU_ACT_WT:.3f} ms",
        f"{V_HALF_WT:.1f} mV",
        f"{G_MAX_WT:.1f} nS",
        "0.00%",
        "t=∞ (never)",
    ],
    "This Patient (ALS)": [
        f"{qr['tau_ALS_ms']:.3f} ms",
        f"{qr['v_half_ALS']:.2f} mV",
        f"{qr['g_max_ALS']:.2f} nS",
        f"{qr['delta_C']*100:.2f}%",
        f"t={qr['t_thresh_patient']:.4f} (sim units)",
    ],
    "Change": [
        f"+{qr['delta_tau_ms']*1000:.1f} μs ⬆",
        f"{delta_tau_mV:+.2f} mV ⬆ DEPOLARIZED",
        f"{delta_g:+.2f} nS ⬇ REDUCED",
        "—",
        "—",
    ],
}

import pandas as pd
st.dataframe(pd.DataFrame(electro_data), use_container_width=True, hide_index=True)

st.divider()

# ── Row 3: Three Plotly Charts ─────────────────────────────────────────────────────
st.subheader("📈 Quantum Dynamics")
ch1, ch2, ch3 = st.columns(3)

# ── Chart A: Coherence Decay ────────────────────────────────────────────────────
with ch1:
    t_eval        = qr["t_eval"]
    coh_wt        = qr["coherence_wt"]
    coh_pat       = qr["coherence_patient"]
    t_thresh_wt   = qr["t_thresh_wt"]
    t_thresh_pat  = qr["t_thresh_patient"]
    mutation_key  = qr["mutation_key"]

    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(
        x=t_eval, y=coh_wt, mode="lines", name="Wild-Type WT",
        line=dict(color="#3b82f6", width=2),
    ))
    fig_a.add_trace(go.Scatter(
        x=t_eval, y=coh_pat, mode="lines", name=f"Patient — {mutation_key}",
        line=dict(color="#ef4444", width=2),
    ))
    # Horizontal threshold
    fig_a.add_hline(
        y=COHERENCE_THRESHOLD, line_dash="dash", line_color="#f59e0b",
        annotation_text=f"Functional threshold ({COHERENCE_THRESHOLD})",
        annotation_position="top right",
    )
    # Vertical threshold lines
    fig_a.add_vline(x=t_thresh_wt, line_dash="dot", line_color="#3b82f6",
                    annotation_text=f"WT t={t_thresh_wt:.2f}", annotation_position="top right")
    fig_a.add_vline(x=t_thresh_pat, line_dash="dot", line_color="#ef4444",
                    annotation_text=f"Pt t={t_thresh_pat:.2f}", annotation_position="bottom right")

    fig_a.update_layout(
        title="Quantum Coherence Dynamics — Lindblad Master Equation",
        xaxis_title="Simulation time",
        yaxis_title="Coherence |ρ₀₁(t)|",
        legend=dict(x=0.6, y=0.95),
        margin=dict(l=40, r=20, t=60, b=40),
        height=360,
        template="plotly_white",
    )
    st.plotly_chart(fig_a, use_container_width=True)

# ── Chart B: Mutation Risk Spectrum ─────────────────────────────────────────────
with ch2:
    panel_items = [
        (name, data) for name, data in REFERENCE_PANEL.items() if name != "WT (Healthy)"
    ]
    panel_items.sort(key=lambda x: x[1]["gamma_phi"])

    def bar_color(qds_val):
        if qds_val < 0.15:   return "#22c55e"
        elif qds_val < 0.40: return "#eab308"
        elif qds_val < 0.70: return "#f97316"
        else:                return "#ef4444"

    from quantum_engine import GAMMA_MIN, GAMMA_MAX
    names   = [n for n, _ in panel_items]
    qds_vals = [
        float(np.clip((d["gamma_phi"] - GAMMA_MIN) / (GAMMA_MAX - GAMMA_MIN), 0, 1)) * 100
        for _, d in panel_items
    ]
    colors  = [bar_color(q/100) for q in qds_vals]
    progs   = [d["prognosis"] for _, d in panel_items]

    # Highlight current patient
    bar_widths = [0.8 if n != mutation_key else 0.95 for n in names]

    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(
        y=names, x=qds_vals, orientation="h",
        marker_color=colors,
        text=[f"{q:.1f}%  {p}" for q, p in zip(qds_vals, progs)],
        textposition="inside",
        insidetextanchor="start",
    ))
    # Star on current mutation
    if mutation_key in names:
        idx   = names.index(mutation_key)
        fig_b.add_trace(go.Scatter(
            x=[qds_vals[idx] + 2], y=[mutation_key],
            mode="markers+text",
            marker=dict(symbol="star", size=14, color="#1d4ed8"),
            text=["◀ THIS PATIENT"], textposition="middle right",
            showlegend=False,
        ))

    fig_b.update_layout(
        title="SOD1 Mutation Risk Spectrum — QDS",
        xaxis_title="Quantum Decoherence Score (%)",
        xaxis=dict(range=[0, 110]),
        margin=dict(l=70, r=20, t=60, b=40),
        height=360,
        template="plotly_white",
        showlegend=False,
    )
    st.plotly_chart(fig_b, use_container_width=True)

# ── Chart C: Purity Decay ───────────────────────────────────────────────────────
with ch3:
    purity = qr["purity_patient"]
    fig_c = go.Figure()
    fig_c.add_trace(go.Scatter(
        x=t_eval, y=purity, mode="lines", name="Purity",
        line=dict(color="#ef4444", width=2),
        fill="tozeroy",
        fillcolor="rgba(239,68,68,0.08)",
    ))
    fig_c.add_hline(y=1.0, line_dash="dash", line_color="#6b7280",
                    annotation_text="Pure quantum state", annotation_position="top right")
    fig_c.add_hline(y=0.5, line_dash="dash", line_color="#f97316",
                    annotation_text="Mixed state", annotation_position="bottom right")
    fig_c.update_layout(
        title="Quantum State Purity Over Time",
        xaxis_title="Simulation time",
        yaxis_title="Purity Tr(ρ²)",
        margin=dict(l=40, r=20, t=60, b=40),
        height=360,
        template="plotly_white",
    )
    st.plotly_chart(fig_c, use_container_width=True)

st.divider()

# ── Row 4: Recommendations ────────────────────────────────────────────────────────
st.subheader("📋 Clinical Recommendations")

tab_pharma, tab_monitor, tab_referral, tab_warnings = st.tabs([
    "💊 Pharmacological", "📅 Monitoring Protocol", "👥 Specialist Referrals", "⚠ Warnings & Limitations"
])

# ── Tab 1: Pharma ──────────────────────────────────────────────────────────────
with tab_pharma:
    has_tofersen = any("Tofersen" in rec["drug"] for rec in recs["pharma"])
    for rec in recs["pharma"]:
        badge_class = "fda-badge"
        cl = rec.get("class", "")
        if "Experimental" in cl:
            badge_class = "exp-badge"
        elif "Off-Label" in cl:
            badge_class = "off-badge"

        st.markdown(
            f"""<div class="rec-card">
            <span class="{badge_class}">{cl}</span>
            <strong style="margin-left:8px;">{rec['drug']}</strong><br>
            <span style="font-size:13px;color:#374151;">{rec['detail']}</span>
            </div>""",
            unsafe_allow_html=True,
        )

    if has_tofersen:
        st.info(
            "📅 **Tofersen Dosing Calendar:** Loading: Day 1 → Day 15 → Day 29, "
            "then maintenance every 28 days. Monitor NfL monthly for first 3 months."
        )

# ── Tab 2: Monitoring ─────────────────────────────────────────────────────────────
with tab_monitor:
    for item in recs["monitoring"]:
        st.markdown(f"• {item}")
    st.markdown("---")
    st.markdown("**Monitoring Frequency Summary:**")

    monitor_table = {
        "Interval": ["Weekly", "Monthly", "Every 3 months", "Every 6 months"],
        "Tests": [
            "NfL if on Tofersen (first 3 months)",
            "ALSFRS-R, weight, respiratory symptoms",
            "FVC, LFTs, CMP, neurofilament",
            "EMG/NCS, cognitive screen",
        ],
    }
    st.dataframe(pd.DataFrame(monitor_table), use_container_width=True, hide_index=True)

# ── Tab 3: Referrals ──────────────────────────────────────────────────────────────
with tab_referral:
    for item in recs["referrals"]:
        st.markdown(
            f"""<div class="rec-card"><span style="font-size:13px;color:#374151;">👤 {item}</span></div>""",
            unsafe_allow_html=True,
        )

# ── Tab 4: Warnings ───────────────────────────────────────────────────────────────
with tab_warnings:
    for w in recs["warnings"]:
        st.warning(w)
    st.success(
        "✅ Model validated: QuTiP mesolve agreement < 1×10⁻⁶. "
        f"Research basis: SOD1-G93A decoherence 300% (4.00×) faster than Wild-Type. "
        f"G93A benchmark: {qr['rate_increase_g93a_pct']:.0f}% ({qr['rate_ratio_g93a']:.2f}×)."
    )

st.divider()

# ── Row 5: Downloads ──────────────────────────────────────────────────────────────
st.subheader("📥 Export")
col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    report_text = generate_full_report_text(pp, qr, recs, date_str)
    filename    = f"QAD_Report_{pp.get('patient_id','UNKNOWN')}_{now.strftime('%Y%m%d')}.txt"
    st.download_button(
        label="📄 Download Full Clinical Report (TXT)",
        data=report_text,
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )

with col_dl2:
    if st.button("🔬 View Science Explainer", use_container_width=True):
        st.switch_page("pages/3_Science.py")
