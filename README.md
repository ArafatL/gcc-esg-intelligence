# 🌍 ESGIntel — GCC ESG Disclosure Intelligence Platform

**Open-source pipeline for ingesting, extracting, and scoring corporate sustainability disclosures across GCC markets** (DFM · ADX · Tadawul · QSE · Boursa Kuwait · Bahrain Bourse).

> The GCC has no open, comparable ESG disclosure dataset. As ISSB/IFRS S1–S2 adoption and UAE climate law reporting requirements accelerate, investors, regulators, and researchers need a transparent way to see *who discloses what*. ESGIntel is that missing layer.

## What it does

```
Company Registry ──▶ Report Downloader ──▶ PDF Text Extraction
                                                  │
        Streamlit Dashboard ◀── DQS Scoring ◀── Metric Extraction
                                                (regex + optional LLM)
```

1. **Ingest** — curated registry of GCC-listed companies + polite PDF downloader for their sustainability/annual reports
2. **Extract** — auditable regex extraction of 9 core quantitative metrics (Scope 1/2/3 emissions, energy, water, renewables %, female workforce %, board independence %, nationalisation %) plus framework-alignment signals (GRI, TCFD, ISSB, SASB, CDP, SDGs, net-zero targets, external assurance). Every value is traceable to its source sentence. Optional LLM-assisted extraction via the Anthropic API for hard documents.
3. **Score** — a fully transparent **Disclosure Quality Score (DQS, 0–100)**: Coverage (45) + Frameworks (30) + Rigor (25). DQS measures disclosure quality, *not* ESG performance — a deliberate, defensible design choice.
4. **Serve** — interactive Streamlit dashboard: market rankings, sector analysis, country distributions, per-company deep-dives, and full methodology.

## Quickstart

```bash
git clone https://github.com/ArafatL/gcc-esg-intelligence
cd gcc-esg-intelligence
pip install -r requirements.txt

# Run the pipeline on the bundled sample dataset
python scripts/run_pipeline.py

# Launch the dashboard
streamlit run app/dashboard.py

# Run tests
pytest tests/ -v
```

To score **real reports**: add `report_url` values to `data/sample/companies.csv` (or your own registry CSV), then:

```bash
python scripts/run_pipeline.py --download
```

> ⚠️ The bundled `sample_disclosures.csv` contains **synthetic demonstration values** so the dashboard works out of the box. Real figures come from running the pipeline on actual reports.

## DQS Methodology (v0.1)

| Pillar | Weight | Measures |
|---|---|---|
| **Coverage** | 45 | Share of 9 core quantitative metrics disclosed |
| **Frameworks** | 30 | GRI / TCFD / ISSB / SASB / CDP / SDG alignment |
| **Rigor** | 25 | External assurance · net-zero target · Scope 3 disclosure |

Bands: **Leader** ≥ 75 · **Advanced** ≥ 50 · **Developing** ≥ 25 · **Minimal** < 25

## Roadmap

- [x] Verified report URLs for all 21 registry companies (see `docs/EXTRACTION_LOG.md`)
- [ ] Expand registry to 100+ GCC companies with verified report URLs
- [ ] Multi-year time series (2020–2025) for disclosure-trend analysis
- [ ] Arabic-language report support
- [ ] ML disclosure-gap prediction (which companies will disclose Scope 3 next?)
- [ ] Public hosted dashboard + downloadable dataset releases

## Author

**Arafat Lakhani** — Data & AI Analyst (Dubai, UAE) · AI × Sustainability × Finance
[LinkedIn](https://www.linkedin.com/in/arafat-lakhani/) · arafatilakhani@gmail.com

MIT License — contributions and issue reports welcome.
