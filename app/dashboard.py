"""ESGIntel Dashboard — GCC ESG Disclosure Intelligence.

Run:  streamlit run app/dashboard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from esgintel.scoring.model import score_dataframe, CORE_METRICS  # noqa: E402

st.set_page_config(page_title="ESGIntel — GCC ESG Intelligence",
                   page_icon="🌍", layout="wide")

BAND_COLORS = {"Leader": "#1a9850", "Advanced": "#66bd63",
               "Developing": "#fdae61", "Minimal": "#d73027"}


@st.cache_data
def load_data() -> pd.DataFrame:
    processed = ROOT / "data" / "processed" / "scored_disclosures.csv"
    if processed.exists():
        return pd.read_csv(processed)
    raw = pd.read_csv(ROOT / "data" / "sample" / "sample_disclosures.csv")
    return score_dataframe(raw)


df = load_data()

st.title("🌍 ESGIntel — GCC ESG Disclosure Intelligence")
st.caption(
    "Open-source disclosure-quality scoring for GCC-listed companies. "
    "Demo values are synthetic — run the pipeline on real reports to replace them. "
    "Built by Arafat Lakhani."
)

# ── Sidebar filters ─────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    countries = st.multiselect("Country", sorted(df["country"].unique()),
                               default=sorted(df["country"].unique()))
    sectors = st.multiselect("Sector", sorted(df["sector"].unique()),
                             default=sorted(df["sector"].unique()))
    min_score = st.slider("Minimum DQS", 0, 100, 0)

view = df[df["country"].isin(countries)
          & df["sector"].isin(sectors)
          & (df["dqs_total"] >= min_score)]

# ── Headline metrics ────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Companies", len(view))
c2.metric("Avg DQS", f"{view['dqs_total'].mean():.1f}" if len(view) else "—")
c3.metric("Leaders", int((view["dqs_band"] == "Leader").sum()))
c4.metric("Scope 3 disclosed",
          f"{view['scope3_emissions_tco2e'].notna().mean() * 100:.0f}%" if len(view) else "—")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🏆 Rankings", "📊 Sector Analysis", "🔍 Company Deep-Dive", "📋 Methodology"])

with tab1:
    ranked = view.sort_values("dqs_total", ascending=False)
    fig = px.bar(ranked, x="dqs_total", y="name", orientation="h",
                 color="dqs_band", color_discrete_map=BAND_COLORS,
                 labels={"dqs_total": "Disclosure Quality Score", "name": ""},
                 height=max(400, 28 * len(ranked)))
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      legend_title_text="Band")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    left, right = st.columns(2)
    with left:
        sector_avg = view.groupby("sector")["dqs_total"].mean().reset_index()
        fig = px.bar(sector_avg.sort_values("dqs_total"), x="dqs_total", y="sector",
                     orientation="h", labels={"dqs_total": "Avg DQS", "sector": ""},
                     title="Average disclosure quality by sector")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.box(view, x="country", y="dqs_total", points="all",
                     hover_name="name",
                     labels={"dqs_total": "DQS", "country": ""},
                     title="Score distribution by country")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Metric coverage across the market")
    coverage = (view[CORE_METRICS].notna().mean() * 100).sort_values()
    fig = px.bar(coverage, orientation="h",
                 labels={"value": "% of companies disclosing", "index": ""})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    company = st.selectbox("Select a company", view["name"].tolist())
    row = view[view["name"] == company].iloc[0]
    a, b, c = st.columns(3)
    a.metric("Total DQS", row["dqs_total"], row["dqs_band"])
    b.metric("Coverage", f"{row['dqs_coverage']}/45")
    c.metric("Frameworks", f"{row['dqs_frameworks']}/30")

    pillar_df = pd.DataFrame({
        "Pillar": ["Coverage", "Frameworks", "Rigor"],
        "Score": [row["dqs_coverage"], row["dqs_frameworks"], row["dqs_rigor"]],
        "Max": [45, 30, 25],
    })
    fig = px.bar(pillar_df, x="Pillar", y=["Score", "Max"], barmode="overlay",
                 opacity=0.85, title=f"{company} — pillar breakdown")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Disclosed metrics")
    disclosed = {m: row[m] for m in CORE_METRICS if pd.notna(row.get(m))}
    if disclosed:
        st.dataframe(pd.DataFrame(disclosed.items(),
                                  columns=["Metric", "Value"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No quantitative metrics disclosed.")

with tab4:
    st.markdown("""
### Disclosure Quality Score (DQS) methodology — v0.1

DQS measures the **quality and completeness of ESG disclosure**, not ESG
performance. A high score means an investor can actually find the data —
it does not mean the company is "green".

| Pillar | Weight | What it measures |
|---|---|---|
| Coverage | 45 | Share of 9 core quantitative metrics disclosed (Scope 1/2/3, energy, water, renewables %, female workforce %, board independence %, nationalisation %) |
| Frameworks | 30 | Alignment mentions: GRI, TCFD, ISSB/IFRS S1-S2, SASB, CDP, UN SDGs |
| Rigor | 25 | External assurance (10), net-zero target (7.5), Scope 3 disclosure (7.5) |

**Bands:** Leader ≥ 75 · Advanced ≥ 50 · Developing ≥ 25 · Minimal < 25

Every extracted value is traceable to a source sentence (see
`ExtractionResult.evidence`). Weights are deliberately transparent and open
to challenge — open an issue on GitHub.
""")
