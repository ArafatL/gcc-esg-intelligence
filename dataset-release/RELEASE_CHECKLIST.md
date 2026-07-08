# Dataset + Preprint Release Checklist

## A. Finalise dataset (with Claude Code)
- [ ] Complete human verification of all 21 rows (log page numbers)
- [ ] Move verified CSV to data/releases/v0.1/gcc_esg_disclosures_v0.1.csv (un-gitignored) + commit
- [ ] Re-run: python analysis/analysis.py --input data/releases/v0.1/gcc_esg_disclosures_v0.1.csv
- [ ] Check every \todo{} left in main.tex is resolved

## B. Zenodo (DOI)
- [ ] Create account at zenodo.org (sign in with GitHub)
- [ ] Either enable GitHub–Zenodo integration and cut a GitHub release v0.1
      (auto-DOI), or upload CSV + DATASHEET.md manually
- [ ] Metadata: title, author + ORCID (create at orcid.org — 5 min), MIT,
      keywords: ESG, disclosure, GCC, sustainability reporting, dataset
- [ ] Paste DOI into paper (Data Availability) and repo README

## C. arXiv
- [ ] Compile on Overleaf (upload paper/ folder; pdflatex + bibtex) — free
- [ ] Fix TODO-VERIFY bib entries (exact ESGReveal/ESG-KG/ESGAgent citations)
- [ ] Category: q-fin.GN (primary), cs.CY (cross-list)
- [ ] Endorsement: if prompted, request via MITx network / a publishing contact
- [ ] Upload .tex source + figures (arXiv compiles from source)

## D. Optional venue targets (after arXiv)
- [ ] ClimateNLP / FinNLP workshop (dataset & resource track)
- [ ] Journal of Sustainable Finance & Investment (data/methods note)
