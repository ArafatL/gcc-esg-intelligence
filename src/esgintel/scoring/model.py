"""Disclosure Quality Score (DQS) — transparent, rule-based scoring v0.1.

Scores each company 0-100 on the QUALITY AND COMPLETENESS of its ESG
disclosure (not its ESG performance — an important distinction that makes the
score defensible). Fully transparent weights; every point is auditable.

Pillars:
  Coverage   (45): how many core quantitative metrics are disclosed
  Frameworks (30): alignment with GRI / TCFD / ISSB / SASB / CDP / SDGs
  Rigor      (25): external assurance, net-zero target, Scope 3 disclosure
"""

from __future__ import annotations

import pandas as pd

CORE_METRICS = [
    "scope1_emissions_tco2e",
    "scope2_emissions_tco2e",
    "scope3_emissions_tco2e",
    "energy_consumption_mwh",
    "water_consumption_m3",
    "renewable_energy_pct",
    "female_workforce_pct",
    "board_independence_pct",
    "emiratisation_pct",
]

FRAMEWORK_COLS = ["fw_gri", "fw_tcfd", "fw_issb_ifrs_s", "fw_sasb", "fw_cdp", "fw_un_sdg"]

WEIGHTS = {"coverage": 45.0, "frameworks": 30.0, "rigor": 25.0}


def score_row(row: pd.Series) -> dict:
    """Compute pillar scores + total DQS for one company-year row."""
    present = sum(1 for m in CORE_METRICS if pd.notna(row.get(m)))
    coverage = WEIGHTS["coverage"] * present / len(CORE_METRICS)

    fw_hits = sum(1 for c in FRAMEWORK_COLS if bool(row.get(c)))
    frameworks = WEIGHTS["frameworks"] * fw_hits / len(FRAMEWORK_COLS)

    rigor_points = 0.0
    if bool(row.get("fw_assurance")):
        rigor_points += 10.0
    if bool(row.get("fw_net_zero_target")):
        rigor_points += 7.5
    if pd.notna(row.get("scope3_emissions_tco2e")):
        rigor_points += 7.5
    rigor = min(rigor_points, WEIGHTS["rigor"])

    total = round(coverage + frameworks + rigor, 1)
    return {
        "dqs_coverage": round(coverage, 1),
        "dqs_frameworks": round(frameworks, 1),
        "dqs_rigor": round(rigor, 1),
        "dqs_total": total,
        "dqs_band": band(total),
    }


def band(score: float) -> str:
    if score >= 75:
        return "Leader"
    if score >= 50:
        return "Advanced"
    if score >= 25:
        return "Developing"
    return "Minimal"


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Append DQS columns to a metrics dataframe."""
    scores = df.apply(score_row, axis=1, result_type="expand")
    return pd.concat([df, scores], axis=1)
