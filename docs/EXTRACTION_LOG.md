# Extraction Tuning Log

## Session 2 — 2026-07-06 (Fable-assisted): full-registry URL validation

**Goal:** verified report URLs for the 16 remaining registry companies
(Session 1 covered DEWA, Emirates NBD, e&, FAB, ADIB).

**Result: all 21/21 registry companies now have verified URLs.** Every URL
below was HTTP-verified (status 200/206, `application/pdf` content type,
`%PDF-` signature) before being added to the registry:

| Ticker | Document | Size |
|---|---|---|
| EMAAR | Integrated Annual Report 2024 (properties.emaar.com) | 19.7 MB |
| DIB | Sustainability Report 2024 (dib.ae) | ~8 MB |
| SALIK | Integrated Annual Report 2024 (ar2024.salik.ae) | 15.6 MB |
| ADNOCDIST | ESG Report 2024 (adnocdistribution.ae) | 10.8 MB |
| ALDAR | Sustainability Report 2024 (Mubasher mirror) | 29.5 MB |
| MASDAR (TAQA) | Integrated Report 2024 (Mubasher mirror) | 15.4 MB |
| ARAMCO | Sustainability Report 2024 (Argaam S3 mirror) | 15.5 MB |
| SABIC | Integrated Annual Report 2024 (sabic.com) | 13.1 MB |
| STC | Sustainability Report 2024 (stc.com) | 8.2 MB |
| ALRAJHI | Integrated Annual Report 2024 (alrajhibank.com.sa/ir24) | 12.7 MB |
| MAADEN | Sustainability Report 2024 (Oracle Cloud storage) | 16.9 MB |
| QNB | Sustainability Performance Data pack (qnb.com) | — |
| IQCD | Sustainability Report **2021** — latest published | 9.5 MB |
| ORDS | ESG Report 2024 (ooredoo.com) | 11.1 MB |
| KFH | Sustainability Report 2024 (kfh.com) | 2.6 MB |
| ZAIN | Sustainability Report 2024 (zain.com/SR2024) | 23.3 MB |

**Sourcing notes:**
1. Mirror strategy confirmed: `static.mubasher.info` and `argaamplus S3`
   (both flagged in Session 1) serve PDFs that the corporate origin blocks
   or throttles — cdn.aldar.com returns 503 to non-browser agents and
   aramco.com times out on direct fetches.
2. Al Rajhi publishes its report as an HTML microsite (`/ir24/`); the full
   PDF lives at the non-obvious path `/ir24/services/pdf/`.
3. QNB's main sustainability report page (qnb.com) is bot-protected (403);
   the machine-readable Sustainability Performance Data pack under
   `/document/en/enSustainabilityPerformanceData` is directly fetchable
   and is table-formatted — well suited to our extraction patterns.
4. Industries Qatar has not published a sustainability report since 2021;
   registry keeps the 2021 report with a staleness caveat.
5. Salik's Sustainability Report 2024 is HTML-only (sr2024.salik.ae); the
   Integrated Annual Report 2024 PDF is used instead (contains the
   sustainability + DFM ESG metrics sections).
6. cdn.emiratesnbd.com now 403s the ESGIntel research User-Agent (worked
   in Session 1) — download requires a browser UA fallback.

**Next:** human spot-check of extracted values against source PDFs, then
promote rows from `extracted_pending_human_check`, and start the
multi-year series (e& SR2021/SR2020 URLs already located in Session 1).

## Session 1 — 2026-07-06 (Fable-assisted)

**Document:** Emirates NBD Group ESG Data Pack 2024 (cdn.emiratesnbd.com/assets/pdf/esg_data_pack_2024.pdf)

**Findings from real GCC disclosure text:**
1. Metrics appear predominantly in TABLE layouts ("Scope 1    757.78") with units
   in column headers, not adjacent to values → added table-style patterns (v0.2).
2. Units vary: kWh (not MWh), liters (not m3) → added per-pattern multipliers.
3. Scope 3 reported with category breakdowns ("Scope 3 – Category 6") → pattern
   must not capture category numbers; negative lookahead added.
4. Assurance statements name the auditor (KPMG Lower Gulf, ISAE 3000/3410) →
   rigor pillar validated against real language.
5. Emiratisation reported as "% of nationalisation among total workforce" →
   pattern added.

**Verified extraction (Group-level, FY2024, KPMG limited assurance on S1/S2/S3-Cat6):**
Scope 1: 757.78 tCO2e | Scope 2: 36,271.17 | Scope 3 (8 categories): 199,795.04
Energy: 83,631.58 MWh (from kWh) | Water: 221,633.95 m3 (from liters)
Women in workforce: 41% | Emiratisation: 36%

**Verified report URLs added to registry:** DEWA (2022 integrated, via DFM feeds),
Emirates NBD (2024 data pack), e& (SR2023; SR2021/SR2020 also located for time
series), FAB (2024 ESG report), ADIB (2024, new registry addition).

**Source patterns discovered:** feeds.dfm.ae (DFM disclosures),
candidocs.nasdaqdubai.com (Nasdaq Dubai), argaamplus S3 (Argaam mirrors),
fabannualreport2024.com (FAB microsite). These are repeatable URL sources.
