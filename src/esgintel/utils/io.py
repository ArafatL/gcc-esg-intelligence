"""Shared IO helpers: paths, config loading, safe file handling."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import yaml

log = logging.getLogger("esgintel")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"


def load_config(path: str | Path | None = None) -> dict:
    """Load the YAML config; fall back to repo-root config.yaml."""
    cfg_path = Path(path) if path else PROJECT_ROOT / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def save_df(df: pd.DataFrame, name: str, processed: bool = True) -> Path:
    """Persist a dataframe as CSV into processed (or raw) data dir."""
    target_dir = PROCESSED_DIR if processed else RAW_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    out = target_dir / f"{name}.csv"
    df.to_csv(out, index=False)
    log.info("Saved %s rows -> %s", len(df), out)
    return out


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
