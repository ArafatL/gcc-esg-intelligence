# Datasheet: GCC Corporate ESG Disclosure Quality Dataset (v0.1)

Following *Datasheets for Datasets* (Gebru et al., 2021).

## Motivation
**Purpose.** No open, company-level ESG disclosure dataset exists for GCC
capital markets; commercial ratings are opaque and diverge. This dataset
provides a verified, evidence-linked baseline of what GCC-listed companies
disclosed for FY2024, to support investor analysis, regulatory baselining,
and research.
**Creator.** Arafat Lakhani (independent researcher, Dubai, UAE).
**Funding.** None.

## Composition
**Instances.** One row per company (v0.1: 21 companies; DFM, ADX, Tadawul,
QSE, Boursa Kuwait). Planned v1.0: company-year panel 2020–2025.
**Fields.** Identity (ticker, name, exchange, sector, country, report_year);
9 quantitative metrics (Scope 1/2/3 tCO2e, energy MWh, water m3, renewable %,
female workforce %, board independence %, nationalisation %); 8 credibility
signals (GRI/TCFD/ISSB/SASB/CDP/SDG references, net-zero target, external
assurance); DQS pillar and total scores; source_url; verification_status;
evidence page references.
**Missing data.** Missingness is signal, not noise: an empty metric means the
company did not disclose it (verified), and feeds the Coverage pillar.
**Confidentiality.** None — all values derive from public corporate reports.

## Collection Process
Source PDFs identified from issuer investor-relations sites and exchange
disclosure feeds; every URL verified live and recorded. Values extracted by
an open pattern-based pipeline (table-aware, unit-converting, evidence
snippet retained per value; see repository), optionally LLM-assisted, then
human-verified against source PDFs with page numbers logged. Extraction
pattern evolution is documented in docs/EXTRACTION_LOG.md.

## Preprocessing
Unit normalisation only (kWh→MWh, litres→m³). No imputation. Group-level
figures preferred over parent-entity where both are reported; scope noted.

## Uses
**Intended.** Disclosure-quality benchmarking, regulatory baselining,
disclosure-trend research, extraction-method evaluation.
**Not intended.** As a measure of ESG *performance*; as investment advice;
as a complete census of GCC markets (sample selects on size and report
availability — see paper §Limitations).

## Distribution & Maintenance
MIT licence. GitHub (living) + Zenodo (versioned, DOI). Maintained by the
author; corrections via GitHub issues; versioned releases on each
verification pass or coverage expansion.
