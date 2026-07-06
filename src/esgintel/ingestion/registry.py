"""Company registry for GCC-listed firms.

The registry is a curated CSV (data/sample/companies.csv to start) holding
ticker, name, exchange, sector, and the investor-relations / sustainability
report URL. Growing this registry IS the dataset-building work: each row you
add expands platform coverage.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from esgintel.utils.io import SAMPLE_DIR

EXCHANGES = {
    "DFM": "Dubai Financial Market",
    "ADX": "Abu Dhabi Securities Exchange",
    "TADAWUL": "Saudi Exchange",
    "QSE": "Qatar Stock Exchange",
    "BK": "Boursa Kuwait",
    "BHB": "Bahrain Bourse",
    "MSX": "Muscat Stock Exchange",
}


@dataclass
class Company:
    ticker: str
    name: str
    exchange: str
    sector: str
    country: str
    report_url: str | None = None

    @property
    def exchange_full(self) -> str:
        return EXCHANGES.get(self.exchange, self.exchange)


def load_registry(path: str | Path | None = None) -> pd.DataFrame:
    """Load the company registry CSV."""
    csv_path = Path(path) if path else SAMPLE_DIR / "companies.csv"
    df = pd.read_csv(csv_path)
    required = {"ticker", "name", "exchange", "sector", "country"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Registry missing columns: {missing}")
    return df


def companies(path: str | Path | None = None) -> list[Company]:
    df = load_registry(path)
    return [
        Company(
            ticker=r.ticker,
            name=r.name,
            exchange=r.exchange,
            sector=r.sector,
            country=r.country,
            report_url=getattr(r, "report_url", None),
        )
        for r in df.itertuples()
    ]
