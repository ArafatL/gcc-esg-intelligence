"""Download sustainability / annual report PDFs listed in the registry.

Run on your own machine (network access required):

    python scripts/run_pipeline.py --download
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path

import requests

from esgintel.utils.io import RAW_DIR

log = logging.getLogger("esgintel.downloader")

HEADERS = {
    "User-Agent": "ESGIntel/0.1 (open-source research; contact: arafatilakhani@gmail.com)"
}


def _safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text).strip("_")


def download_report(ticker: str, url: str, dest_dir: Path | None = None,
                    timeout: int = 60, polite_delay: float = 1.0) -> Path | None:
    """Download a single PDF report. Returns local path or None on failure."""
    dest_dir = dest_dir or RAW_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"{_safe_name(ticker)}.pdf"
    if out.exists():
        log.info("%s already downloaded, skipping", ticker)
        return out
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type and not url.lower().endswith(".pdf"):
            log.warning("%s: URL did not return a PDF (%s)", ticker, content_type)
            return None
        out.write_bytes(resp.content)
        log.info("Downloaded %s (%.1f KB)", ticker, len(resp.content) / 1024)
        time.sleep(polite_delay)  # be a polite scraper
        return out
    except requests.RequestException as exc:
        log.error("%s: download failed — %s", ticker, exc)
        return None


def download_all(registry_df, dest_dir: Path | None = None) -> dict[str, Path]:
    """Download every report_url present in the registry dataframe."""
    results: dict[str, Path] = {}
    rows = registry_df.dropna(subset=["report_url"])
    for row in rows.itertuples():
        path = download_report(row.ticker, row.report_url, dest_dir)
        if path:
            results[row.ticker] = path
    log.info("Downloaded %d/%d reports", len(results), len(rows))
    return results
