# Extraction Tuning Log

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
