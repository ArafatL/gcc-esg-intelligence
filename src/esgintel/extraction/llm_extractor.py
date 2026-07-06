"""Optional LLM-assisted extraction via the Anthropic API.

Used for documents where regex extraction is insufficient (scanned layouts,
tables, narrative-buried figures). Requires ANTHROPIC_API_KEY in env.
Designed to run with a cheap fast model — the schema does the heavy lifting.
"""

from __future__ import annotations

import json
import logging
import os

log = logging.getLogger("esgintel.llm")

EXTRACTION_PROMPT = """You are an ESG data extraction engine. From the report text below,
extract these metrics if explicitly stated (do NOT infer or estimate):
scope1_emissions_tco2e, scope2_emissions_tco2e, scope3_emissions_tco2e,
energy_consumption_mwh, water_consumption_m3, renewable_energy_pct,
female_workforce_pct, board_independence_pct, emiratisation_pct.

Respond ONLY with a JSON object. Use null for metrics not found. For each
found metric also include "<metric>_evidence": the exact sentence it came from.

REPORT TEXT:
{text}
"""


def llm_extract(text: str, model: str = "claude-haiku-4-5-20251001",
                max_chars: int = 150_000) -> dict:
    """Extract metrics with an LLM. Returns {} if API key missing or call fails."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.info("ANTHROPIC_API_KEY not set — skipping LLM extraction")
        return {}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": EXTRACTION_PROMPT.format(text=text[:max_chars]),
            }],
        )
        raw = msg.content[0].text.strip()
        raw = raw.removeprefix("```json").removesuffix("```").strip()
        return json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        log.error("LLM extraction failed: %s", exc)
        return {}
