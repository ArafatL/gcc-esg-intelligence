"""Heuristic ESG metric extraction from disclosure text.

v0.2 — tuned against real GCC disclosures (Emirates NBD ESG Data Pack 2024).
Key lesson from real documents: metrics usually appear in TABLE layouts
("Scope 1    757.78") where the unit lives in a header, not next to the
number. Patterns therefore come in two flavours: sentence-style (unit after
number) and table-style (label immediately followed by number). Each pattern
carries a multiplier for unit conversion (kWh->MWh, litres->m3).
Every extracted value keeps an evidence snippet for human verification.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

NUM = r"([0-9]{1,3}(?:[, ][0-9]{3})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)"

# (pattern, multiplier) — first match wins, so order = priority
METRIC_PATTERNS: dict[str, list[tuple[str, float]]] = {
    "scope1_emissions_tco2e": [
        (rf"scope\s*1[^0-9%]{{0,80}}{NUM}\s*(?:t\s?co2e?|tonnes|tons|mt)", 1),
        (rf"scope\s*1\s*\(?\s*t\s?co2e?\s*\)?[^0-9%]{{0,60}}{NUM}", 1),   # table: unit before number
        (rf"scope\s*1(?:\s+emissions)?\s+{NUM}(?!\s*%)", 1),               # bare table row
    ],
    "scope2_emissions_tco2e": [
        (rf"scope\s*2[^0-9%]{{0,80}}{NUM}\s*(?:t\s?co2e?|tonnes|tons|mt)", 1),
        (rf"scope\s*2\s*\(?\s*t\s?co2e?\s*\)?[^0-9%]{{0,60}}{NUM}", 1),
        (rf"scope\s*2(?:\s+emissions)?\s+{NUM}(?!\s*%)", 1),
    ],
    "scope3_emissions_tco2e": [
        (rf"scope\s*3[^0-9%]{{0,80}}{NUM}\s*(?:t\s?co2e?|tonnes|tons|mt)", 1),
        (rf"scope\s*3\s*(?!\s*[-–]\s*category)\(?\s*t?\s?co2e?\s*\)?[^0-9%]{{0,20}}{NUM}", 1),
        (rf"scope\s*3\s+{NUM}(?!\s*%)", 1),
    ],
    "energy_consumption_mwh": [
        (rf"(?:total\s+)?energy\s+consum\w*[^0-9%]{{0,60}}{NUM}\s*mwh", 1),
        (rf"(?:total\s+)?energy\s+consum\w*[^0-9%]{{0,60}}{NUM}\s*gwh", 1000),
        (rf"electricity\s+consumption[^0-9%]{{0,120}}\(?\s*kwh\s*\)?[^0-9%]{{0,20}}{NUM}", 0.001),
        (rf"(?:total\s+)?energy\s+consum\w*[^0-9%]{{0,60}}{NUM}\s*kwh", 0.001),
    ],
    "water_consumption_m3": [
        (rf"water\s+(?:consum|withdraw)\w*[^0-9%]{{0,60}}{NUM}\s*(?:m3|m\u00b3|cubic)", 1),
        (rf"water\s+consumption\s*\(?\s*lit(?:er|re)s?\s*\)?[^0-9%]{{0,60}}{NUM}", 0.001),
        (rf"water\s+(?:consum|withdraw)\w*[^0-9%]{{0,60}}{NUM}\s*lit(?:er|re)s", 0.001),
    ],
    "renewable_energy_pct": [
        (rf"renewable\s+(?:energy|electricity|sources?)[^0-9]{{0,60}}{NUM}\s*%", 1),
        (rf"clean\s+energy\s+accounted\s+for\s+{NUM}\s*%", 1),
    ],
    "female_workforce_pct": [
        (rf"(?:female|women)[^0-9]{{0,60}}{NUM}\s*%\s*(?:of\s+(?:the\s+)?(?:total\s+)?workforce|of\s+employees)", 1),
        (rf"share\s+of\s+women\s+in\s+total\s+workforce[^0-9]{{0,20}}{NUM}\s*%", 1),
        (rf"women\s+represent\s+{NUM}\s*%", 1),
    ],
    "board_independence_pct": [
        (rf"independent\s+(?:board\s+)?(?:members|directors)[^0-9]{{0,60}}{NUM}\s*%", 1),
        (rf"board\s+independence[^0-9]{{0,30}}{NUM}\s*%", 1),
    ],
    "emiratisation_pct": [
        (rf"emiratis(?:ation|ed)?[^0-9]{{0,60}}{NUM}\s*%", 1),
        (rf"%\s+of\s+nationalisation\s+among\s+total\s+workforce[^0-9]{{0,20}}{NUM}\s*%", 1),
        (rf"national(?:isation|s)\s+rate[^0-9]{{0,40}}{NUM}\s*%", 1),
    ],
}

FRAMEWORK_KEYWORDS = {
    "gri": r"\bGRI\b|Global Reporting Initiative",
    "tcfd": r"\bTCFD\b|Task\s*Force on Climate",
    "issb_ifrs_s": r"\bISSB\b|IFRS\s*S[12]\b",
    "sasb": r"\bSASB\b",
    "cdp": r"\bCDP\b|Carbon Disclosure Project",
    "un_sdg": r"\bSDGs?\b|Sustainable Development Goals",
    "net_zero_target": r"net[\s-]?zero",
    "assurance": r"(?:independent|external|limited|reasonable)\s+assurance",
}


@dataclass
class ExtractionResult:
    metrics: dict[str, float] = field(default_factory=dict)
    evidence: dict[str, str] = field(default_factory=dict)
    frameworks: dict[str, bool] = field(default_factory=dict)

    def as_row(self) -> dict:
        row: dict = dict(self.metrics)
        row.update({f"fw_{k}": v for k, v in self.frameworks.items()})
        return row


def _to_float(raw: str) -> float:
    return float(raw.replace(",", "").replace(" ", ""))


def extract_metrics(text: str) -> ExtractionResult:
    """Run all metric + framework patterns over document text."""
    result = ExtractionResult()
    lowered = text.lower()
    for metric, patterns in METRIC_PATTERNS.items():
        for pat, multiplier in patterns:
            m = re.search(pat, lowered, flags=re.IGNORECASE)
            if m:
                try:
                    result.metrics[metric] = round(_to_float(m.group(1)) * multiplier, 3)
                    start = max(m.start() - 40, 0)
                    result.evidence[metric] = text[start:m.end() + 40].replace("\n", " ")
                except ValueError:
                    continue
                break
    for fw, pat in FRAMEWORK_KEYWORDS.items():
        result.frameworks[fw] = bool(re.search(pat, text, flags=re.IGNORECASE))
    return result
