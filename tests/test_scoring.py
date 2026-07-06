import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from esgintel.scoring.model import score_row, score_dataframe, band


def full_row():
    return pd.Series({
        "scope1_emissions_tco2e": 1, "scope2_emissions_tco2e": 1,
        "scope3_emissions_tco2e": 1, "energy_consumption_mwh": 1,
        "water_consumption_m3": 1, "renewable_energy_pct": 1,
        "female_workforce_pct": 1, "board_independence_pct": 1,
        "emiratisation_pct": 1,
        "fw_gri": True, "fw_tcfd": True, "fw_issb_ifrs_s": True,
        "fw_sasb": True, "fw_cdp": True, "fw_un_sdg": True,
        "fw_net_zero_target": True, "fw_assurance": True,
    })


def test_perfect_score():
    s = score_row(full_row())
    assert s["dqs_total"] == 100.0
    assert s["dqs_band"] == "Leader"


def test_empty_score():
    s = score_row(pd.Series(dtype=object))
    assert s["dqs_total"] == 0.0
    assert s["dqs_band"] == "Minimal"


def test_bands():
    assert band(80) == "Leader"
    assert band(60) == "Advanced"
    assert band(30) == "Developing"
    assert band(10) == "Minimal"


def test_dataframe_scoring():
    df = pd.DataFrame([full_row(), pd.Series(dtype=object)])
    scored = score_dataframe(df)
    assert "dqs_total" in scored.columns
    assert len(scored) == 2
