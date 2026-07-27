import pytest
from src.analytics.ratios import ProfitabilityEngine


@pytest.fixture
def ratio_engine():
    return ProfitabilityEngine(
        db_path=":memory:"
    )  # Dummy DB path for testing functions


def test_debt_to_equity_bank_carve_out(ratio_engine):
    # 'HDFCBANK' should return None for D/E
    row = {
        "company_id": "HDFCBANK",
        "borrowings": 5000,
        "equity_capital": 100,
        "reserves": 900,
    }
    assert ratio_engine.calc_debt_to_equity(row) is None


def test_debt_to_normal(ratio_engine):
    # Standard company ('TCS') D/E calculation
    row = {
        "company_id": "TCS",
        "borrowings": 500,
        "equity_capital": 100,
        "reserves": 900,
    }  # Equity = 1000
    assert ratio_engine.calc_debt_to_equity(row) == 0.50


def test_icr_debt_free_substitution(ratio_engine):
    # Zero interest should return 999.0
    row = {"profit_before_tax": 1000, "interest": 0}
    assert ratio_engine.calc_icr(row) == 999.0


def test_icr_normal_calculation(ratio_engine):
    # Normal ICR calculation
    row = {"profit_before_tax": 1000, "interest": 100}
    assert ratio_engine.calc_icr(row) == 10.0


def test_asset_turnover(ratio_engine):
    row = {"sales": 2000, "equity_capital": 500, "reserves": 300, "borrowings": 200}
    assert ratio_engine.calc_asset_turnover(row) == 2.0
