import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from esgintel.extraction.metrics import extract_metrics

SAMPLE = """
Sustainability Report 2025. Our Scope 1 emissions were 42,000 tCO2e this year,
while Scope 2 emissions totalled 118,500 tCO2e. Total energy consumption
reached 310,200 MWh. Renewable energy sources accounted for 8.5% of our mix.
Women represent 31% of our workforce. Independent directors comprise 55% of
the board. This report is prepared in accordance with GRI Standards and the
TCFD recommendations. We remain committed to our net-zero pathway. Limited
assurance was provided by an independent third party.
"""


def test_scope1():
    r = extract_metrics(SAMPLE)
    assert r.metrics["scope1_emissions_tco2e"] == 42000


def test_scope2():
    r = extract_metrics(SAMPLE)
    assert r.metrics["scope2_emissions_tco2e"] == 118500


def test_energy():
    r = extract_metrics(SAMPLE)
    assert r.metrics["energy_consumption_mwh"] == 310200


def test_percentages():
    r = extract_metrics(SAMPLE)
    assert r.metrics["renewable_energy_pct"] == 8.5
    assert r.metrics["female_workforce_pct"] == 31
    assert r.metrics["board_independence_pct"] == 55


def test_frameworks():
    r = extract_metrics(SAMPLE)
    assert r.frameworks["gri"] and r.frameworks["tcfd"]
    assert r.frameworks["net_zero_target"] and r.frameworks["assurance"]
    assert not r.frameworks["sasb"]


def test_evidence_traceability():
    r = extract_metrics(SAMPLE)
    assert "42,000" in r.evidence["scope1_emissions_tco2e"]


# Regression test: real table-style layout from Emirates NBD ESG Data Pack 2024
REAL_TABLE_SAMPLE = """
Summary of GHG Emissions - Emission Category in tCO2e Emirates NBD Group
Scope 1 757.78
Scope 2 36,271.17
Scope 3 199,795.04
Total Emissions 236,823.99
Energy Consumption: Electricity consumption from non-renewable sources (kWh) 83,631,577.73
Water Consumption: Water consumption (liters) 221,633,952.53
Gender Diversity: Share of women in total workforce as a % 41%
Emiratisation: % of nationalisation among total workforce 36%
KPMG Lower Gulf Limited were engaged to perform an independent limited assurance opinion.
"""


def test_real_table_scope_emissions():
    r = extract_metrics(REAL_TABLE_SAMPLE)
    assert r.metrics["scope1_emissions_tco2e"] == 757.78
    assert r.metrics["scope2_emissions_tco2e"] == 36271.17
    assert r.metrics["scope3_emissions_tco2e"] == 199795.04


def test_real_table_unit_conversion():
    r = extract_metrics(REAL_TABLE_SAMPLE)
    assert abs(r.metrics["energy_consumption_mwh"] - 83631.578) < 0.01   # kWh -> MWh
    assert abs(r.metrics["water_consumption_m3"] - 221633.953) < 0.01   # liters -> m3


def test_real_table_percentages_and_assurance():
    r = extract_metrics(REAL_TABLE_SAMPLE)
    assert r.metrics["female_workforce_pct"] == 41
    assert r.metrics["emiratisation_pct"] == 36
    assert r.frameworks["assurance"]
