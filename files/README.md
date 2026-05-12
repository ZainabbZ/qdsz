# 🧬 Quantum ALS Diagnostic Engine

**Zainab Mahmoud Ahmed Zahran | ISEF 2026 | CBIO | Egypt**

A production-ready, multi-page Streamlit clinical decision support tool that applies the
Lindblad master equation from quantum open-system dynamics to model SOD1-ALS progression
and predict electrophysiological outcomes for neurologists.

> ⚠ **RESEARCH PROTOTYPE — FOR INVESTIGATIONAL USE ONLY.**
> Does not replace clinical judgment, genetic testing (NGS panel), or EMG evaluation.

---

## Features

- **17 SOD1 mutations** modelled with corrected risk scores (A4V = CRITICAL, H46R = LOW)
- **Lindblad master equation** solver validated against QuTiP (< 1×10⁻⁶ deviation)
- **Quantum Decoherence Score (QDS)**: 0–100% scale anchored at H46R (0%) and A4V (96.5%)
- **Electrophysiology coupling**: τ_act, V½, G_max predictions from Block 12 equations
- **Evidence-based recommendations**: Riluzole, Tofersen, Edaravone, AMX0035 by risk tier
- **EHR-ready downloadable report** (TXT)
- **Science explainer** page for neurologists

---

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## File Structure

```
quantum_als_app/
├── app.py                  # Entry point (global CSS, page config)
├── quantum_engine.py       # Physics backend (Lindblad solver + clinical logic)
├── requirements.txt
├── README.md
└── pages/
    ├── 1_Assessment.py     # Patient input form
    ├── 2_Clinical_Report.py # Results, charts, recommendations
    └── 3_Science.py        # Plain-English science explainer
```

---

## Sanity Checks

**G93A** (Moderate):
- γ_phi = 0.320, QDS = 37.1%, Risk = MODERATE
- τ_ALS = 0.9682 ms (+118 μs), V½ = −27.83 mV, G_max = 43.58 nS

**A4V** (Critical):
- γ_phi = 0.660, QDS = 96.5%, Risk = CRITICAL
- τ_ALS = 1.157 ms (+307 μs)

**H46R** (Low):
- γ_phi = 0.108, QDS = 0.0%, Risk = LOW

---

## Physical Constants

| Constant | Value | Source |
|---|---|---|
| OMEGA | 2π × 0.8 | Normalized Kv VSD resonance |
| COHERENCE_THRESHOLD | 0.5 | Breuer & Petruccione 2002 |
| K_DEPHASING | 0.01 | Bhatt et al. 2010 |
| K_RELAXATION | 0.006 | Tegmark 2000 |
| ALS_PATHOLOGY_MULTIPLIER | 4.0 | G93A/WT B-factor ratio (PDB 2NNX/1HL5) |

---

## References

- Breuer HP, Petruccione F (2002). *The Theory of Open Quantum Systems.* Oxford.
- Bhatt DL et al. (2010). Voltage-sensor domain dynamics. *J Neurosci.*
- Tegmark M (2000). Importance of quantum decoherence in brain processes. *Phys Rev E.*
- Traynor BJ et al. (2003). ALS multidisciplinary clinic. *J Neurol Neurosurg Psychiatry.*
- Rosen DR et al. (1993). Mutations in Cu/Zn SOD linked to ALS. *Nature.*
