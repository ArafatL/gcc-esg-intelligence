# Paper Package — GCC Corporate ESG Disclosure Quality

Built with Claude Fable 5 on 2026-07-07. Everything downstream runs with
Claude Code — no frontier model required.

## Contents
- paper/            arXiv-ready LaTeX (main.tex, refs.bib, auto-generated results/ + figures/)
- analysis/analysis.py   One command regenerates every figure, table, and statistic
- dataset-release/  DATASHEET.md + RELEASE_CHECKLIST.md (Zenodo DOI + arXiv steps)
- launch/           LinkedIn launch article (post after verification)

## The loop (repeat after every data update)
1. Verify rows against source PDFs (Claude Code shows evidence snippets; you confirm)
2. python analysis/analysis.py --input <verified scored CSV>
3. Compile paper on Overleaf (upload paper/ folder) — every number refreshes automatically
4. Resolve remaining \todo{} marks in main.tex (they are search targets, grep "todo{")
5. Follow dataset-release/RELEASE_CHECKLIST.md → Zenodo DOI → arXiv

## Ground rules encoded in this package
- Never hard-code a statistic in main.tex — macros only (auto_results.tex)
- Never publish a number from a row not marked verified
- TODO-VERIFY entries in refs.bib must be confirmed before arXiv submission

## Suggested first Claude Code prompt
"Copy this paper-package into the gcc-esg-intelligence repo under paper/,
commit it, then walk me through human verification of the 20 unverified
rows one company at a time, showing me each extracted value next to its
evidence snippet and source URL, and updating verification_status as I
confirm. When done, run analysis/analysis.py on the verified dataset and
show me the new macros."
