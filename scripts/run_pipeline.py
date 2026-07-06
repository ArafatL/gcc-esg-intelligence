"""End-to-end pipeline: registry -> (download) -> extract -> score -> CSV.

Usage:
  python scripts/run_pipeline.py                  # score sample dataset
  python scripts/run_pipeline.py --download       # also fetch PDFs (needs network)
  python scripts/run_pipeline.py --pdf-dir data/raw   # extract from local PDFs
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd

from esgintel.utils.io import SAMPLE_DIR, RAW_DIR, save_df, setup_logging
from esgintel.ingestion.registry import load_registry
from esgintel.extraction.pdf_text import extract_text
from esgintel.extraction.metrics import extract_metrics
from esgintel.scoring.model import score_dataframe


def extract_from_pdfs(registry: pd.DataFrame, pdf_dir: Path) -> pd.DataFrame:
    rows = []
    for company in registry.itertuples():
        pdf_path = pdf_dir / f"{company.ticker}.pdf"
        if not pdf_path.exists():
            continue
        text = extract_text(pdf_path)
        result = extract_metrics(text)
        row = {"ticker": company.ticker, "name": company.name,
               "exchange": company.exchange, "sector": company.sector,
               "country": company.country}
        row.update(result.as_row())
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(description="ESGIntel pipeline")
    parser.add_argument("--download", action="store_true", help="download report PDFs")
    parser.add_argument("--pdf-dir", type=Path, default=RAW_DIR)
    args = parser.parse_args()

    registry = load_registry()

    if args.download:
        from esgintel.ingestion.downloader import download_all
        download_all(registry, args.pdf_dir)

    extracted = extract_from_pdfs(registry, args.pdf_dir)
    if extracted.empty:
        print("No local PDFs found — scoring the bundled sample dataset instead.")
        extracted = pd.read_csv(SAMPLE_DIR / "sample_disclosures.csv")

    scored = score_dataframe(extracted)
    out = save_df(scored, "scored_disclosures")
    print(f"\nScored {len(scored)} companies -> {out}")
    cols = ["ticker", "name", "dqs_total", "dqs_band"]
    print(scored[cols].sort_values("dqs_total", ascending=False).to_string(index=False))


if __name__ == "__main__":
    main()
