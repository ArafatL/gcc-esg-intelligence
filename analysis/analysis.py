"""Full statistical analysis for the GCC ESG Disclosure Quality paper.

Reads the scored dataset, produces every figure, table, and statistic the
manuscript needs, and writes them into paper/results/ and paper/figures/ so
the LaTeX compiles with fresh numbers. Run after each verification pass:

    python analysis/analysis.py --input data/processed/scored_disclosures.csv

Requires: pandas, numpy, scipy, matplotlib.
"""

from __future__ import annotations

import argparse
from itertools import permutations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent / "paper"
FIGS = PAPER / "figures"
RES = PAPER / "results"

CORE_METRICS = ["scope1_emissions_tco2e", "scope2_emissions_tco2e",
                "scope3_emissions_tco2e", "energy_consumption_mwh",
                "water_consumption_m3", "renewable_energy_pct",
                "female_workforce_pct", "board_independence_pct",
                "emiratisation_pct"]
FW_COLS = ["fw_gri", "fw_tcfd", "fw_issb_ifrs_s", "fw_sasb", "fw_cdp", "fw_un_sdg"]
BAND_COLORS = {"Leader": "#1a9850", "Advanced": "#66bd63",
               "Developing": "#fdae61", "Minimal": "#d73027"}
BASE_W = {"coverage": 45.0, "frameworks": 30.0, "rigor": 25.0}

METRIC_LABELS = {
    "scope1_emissions_tco2e": "Scope 1 emissions",
    "scope2_emissions_tco2e": "Scope 2 emissions",
    "scope3_emissions_tco2e": "Scope 3 emissions",
    "energy_consumption_mwh": "Energy consumption",
    "water_consumption_m3": "Water consumption",
    "renewable_energy_pct": "Renewable share",
    "female_workforce_pct": "Female workforce %",
    "board_independence_pct": "Board independence %",
    "emiratisation_pct": "Nationalisation %",
    "fw_assurance": "External assurance",
    "fw_net_zero_target": "Net-zero target",
}


def truthy(s: pd.Series) -> pd.Series:
    return s.fillna(False).astype(str).str.lower().isin(["true", "1", "1.0", "yes"])


def score_with_weights(df: pd.DataFrame, w: dict) -> pd.Series:
    cov = w["coverage"] * df[CORE_METRICS].notna().sum(axis=1) / len(CORE_METRICS)
    fw = w["frameworks"] * sum(truthy(df[c]) for c in FW_COLS) / len(FW_COLS)
    rig_raw = (10 * truthy(df["fw_assurance"])
               + 7.5 * truthy(df["fw_net_zero_target"])
               + 7.5 * df["scope3_emissions_tco2e"].notna())
    rig = np.minimum(rig_raw * (w["rigor"] / 25.0), w["rigor"])
    return (cov + fw + rig).round(1)


def latex_escape(s: str) -> str:
    return str(s).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def write_group_table(df, by, path, caption, label):
    g = (df.groupby(by)
           .agg(n=("dqs_total", "size"), mean_dqs=("dqs_total", "mean"),
                scope3=("scope3_emissions_tco2e", lambda s: 100 * s.notna().mean()),
                assured=("fw_assurance", lambda s: 100 * truthy(s).mean()))
           .sort_values("mean_dqs", ascending=False).round(1))
    rows = "\n".join(
        f"{latex_escape(idx)} & {int(r.n)} & {r.mean_dqs:.1f} & {r.scope3:.0f}\\% & {r.assured:.0f}\\% \\\\"
        for idx, r in g.iterrows())
    path.write_text(
"""\\begin{table}[t]\\centering
\\caption{%s}\\label{%s}
\\begin{tabular}{lrrrr}\\toprule
%s & $n$ & Mean \\dqs{} & Scope~3 & Assured \\\\ \\midrule
%s
\\bottomrule\\end{tabular}\\end{table}
""" % (caption, label, by.capitalize(), rows))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True,
                    help="scored dataset CSV (must contain dqs_total or raw metrics)")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    for col in FW_COLS + ["fw_assurance", "fw_net_zero_target"]:
        if col not in df:
            df[col] = False
    if "dqs_total" not in df.columns:
        df["dqs_total"] = score_with_weights(df, BASE_W)
    if "dqs_band" not in df.columns:
        df["dqs_band"] = pd.cut(df["dqs_total"], [-1, 24.99, 49.99, 74.99, 200],
                                labels=["Minimal", "Developing", "Advanced", "Leader"])
    FIGS.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)

    # ---------- Figure 1: ranking ----------
    ranked = df.sort_values("dqs_total")
    fig, ax = plt.subplots(figsize=(8, max(4, 0.3 * len(ranked))))
    ax.barh(ranked["name"], ranked["dqs_total"],
            color=[BAND_COLORS.get(str(b), "#888") for b in ranked["dqs_band"]])
    for thr in (25, 50, 75):
        ax.axvline(thr, color="grey", lw=0.6, ls="--")
    ax.set_xlabel("Disclosure Quality Score (0–100)"); ax.set_xlim(0, 100)
    fig.tight_layout(); fig.savefig(FIGS / "fig1_ranking.pdf"); plt.close(fig)

    # ---------- Figure 2: coverage anatomy ----------
    cov = {METRIC_LABELS[m]: 100 * df[m].notna().mean() for m in CORE_METRICS}
    cov[METRIC_LABELS["fw_assurance"]] = 100 * truthy(df["fw_assurance"]).mean()
    cov[METRIC_LABELS["fw_net_zero_target"]] = 100 * truthy(df["fw_net_zero_target"]).mean()
    cs = pd.Series(cov).sort_values()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(cs.index, cs.values, color="#4575b4")
    ax.set_xlabel("% of companies disclosing"); ax.set_xlim(0, 100)
    fig.tight_layout(); fig.savefig(FIGS / "fig2_coverage.pdf"); plt.close(fig)

    # ---------- Figure 3 + stat: weight sensitivity ----------
    base = score_with_weights(df, BASE_W)
    rhos = []
    for a, b in permutations(BASE_W, 2):
        w = dict(BASE_W); w[a] += 10; w[b] -= 10
        rhos.append(spearmanr(base, score_with_weights(df, w)).statistic)
    w_eq = {k: 100 / 3 for k in BASE_W}
    rhos.append(spearmanr(base, score_with_weights(df, w_eq)).statistic)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.boxplot([rhos], vert=False, widths=0.5)
    ax.scatter(rhos, np.ones(len(rhos)), color="#d73027", zorder=3)
    ax.set_xlabel("Spearman rank correlation with baseline ranking")
    ax.set_yticks([]); ax.set_xlim(min(0.8, min(rhos) - 0.02), 1.001)
    fig.tight_layout(); fig.savefig(FIGS / "fig3_sensitivity.pdf"); plt.close(fig)

    # ---------- Tables ----------
    write_group_table(df, "sector", RES / "table_by_sector.tex",
                      "Disclosure quality by sector.", "tab:sector")
    write_group_table(df, "country", RES / "table_by_country.tex",
                      "Disclosure quality by market.", "tab:country")
    defs = "\n".join(f"{latex_escape(v)} & \\texttt{{{latex_escape(k)}}} \\\\"
                     for k, v in METRIC_LABELS.items())
    (RES / "table_definitions.tex").write_text(
        "\\begin{tabular}{ll}\\toprule Item & Dataset column \\\\ \\midrule\n"
        + defs + "\n\\bottomrule\\end{tabular}\n")

    # ---------- Macros ----------
    pct = lambda s: f"{100 * s:.0f}\\%"
    macros = {
        "NComp": len(df), "NExch": df["exchange"].nunique(),
        "NCountry": df["country"].nunique(),
        "AvgDQS": f"{df.dqs_total.mean():.1f}", "MedDQS": f"{df.dqs_total.median():.1f}",
        "SdDQS": f"{df.dqs_total.std():.1f}", "MaxDQS": f"{df.dqs_total.max():.1f}",
        "MinDQS": f"{df.dqs_total.min():.1f}",
        "ScopeThreePct": pct(df.scope3_emissions_tco2e.notna().mean()),
        "AssurancePct": pct(truthy(df.fw_assurance).mean()),
        "NetZeroPct": pct(truthy(df.fw_net_zero_target).mean()),
        "GriPct": pct(truthy(df.fw_gri).mean()),
        "TcfdPct": pct(truthy(df.fw_tcfd).mean()),
        "IssbPct": pct(truthy(df.fw_issb_ifrs_s).mean()),
        "MinSpearman": f"{min(rhos):.3f}",
    }
    lines = ["% AUTO-GENERATED by analysis/analysis.py — do not edit by hand"]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items()]
    (RES / "auto_results.tex").write_text("\n".join(lines) + "\n")

    print("Wrote 3 figures, 3 tables, and macros:")
    for k, v in macros.items():
        print(f"  \\{k} = {v}")


if __name__ == "__main__":
    main()
