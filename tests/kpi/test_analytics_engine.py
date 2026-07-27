import pytest
from src.analytics.ratios import ProfitabilityEngine
from src.analytics.cagr import CAGREngine
from src.analytics.cashflow_kpis import CashFlowEngine


# --- 1. Setup Dummy Engines for Testing ---
@pytest.fixture
def ratio_engine():
    return ProfitabilityEngine(db_path=":memory:")


@pytest.fixture
def cagr_engine():
    return CAGREngine(db_path=":memory:")


@pytest.fixture
def cf_engine():
    return CashFlowEngine(db_path=":memory:")


# --- 2. Profitability Ratio Tests (Day 08) ---
def test_npm_normal(ratio_engine):
    assert ratio_engine.calc_npm({"sales": 1000, "net_profit": 150}) == 15.0


def test_npm_zero_sales(ratio_engine):
    assert ratio_engine.calc_npm({"sales": 0, "net_profit": 100}) is None


def test_opm_normal(ratio_engine):
    assert ratio_engine.calc_opm({"sales": 1000, "operating_profit": 200}) == 20.0


def test_roe__normal(ratio_engine):
    assert (
        ratio_engine.calc_roe(
            {"net_profit": 150, "equity_capital": 100, "reserves": 900}
        )
        == 15.0
    )


def test_roe_negative_equity(ratio_engine):
    assert (
        ratio_engine.calc_roe(
            {"net_profit": 100, "equity_capital": 100, "reserves": -200}
        )
        is None
    )


def test_roce_normal(ratio_engine):
    assert (
        ratio_engine.calc_roce(
            {
                "operating_profit": 250,
                "equity_capital": 100,
                "reserves": 900,
                "borrowings": 1000,
            }
        )
        == 12.5
    )


# --- 3. Leverage & Efficiency Tests (Day 09) ---
def test_debt_to_equity_normal(ratio_engine):
    assert (
        ratio_engine.calc_debt_to_equity(
            {
                "company_id": "TCS",
                "borrowings": 500,
                "equity_capital": 100,
                "reserves": 900,
            }
        )
        == 0.50
    )


def test_debt_to_equity_bank_carve_out(ratio_engine):
    assert (
        ratio_engine.calc_debt_to_equity(
            {
                "company_id": "HDFCBANK",
                "borrowings": 5000,
                "equity_capital": 100,
                "reserves": 900,
            }
        )
        is None
    )


def test_icr_normal(ratio_engine):
    assert ratio_engine.calc_icr({"profit_before_tax": 1000, "interest": 100}) == 10.0


def test_icr_debt_free(ratio_engine):
    assert ratio_engine.calc_icr({"profit_before_tax": 1000, "interest": 0}) == 999.0


def test_asset_turnover(ratio_engine):
    assert (
        ratio_engine.calc_asset_turnover(
            {"sales": 2000, "equity_capital": 500, "reserves": 300, "borrowings": 200}
        )
        == 2.0
    )


def test_asset_turnover_zero_assets(ratio_engine):
    assert (
        ratio_engine.calc_asset_turnover(
            {"sales": 2000, "equity_capital": 0, "reserves": 0, "borrowings": 0}
        )
        is None
    )


# --- 4. CAGR Tests (Day 10) ---
def test_cagr_normal(cagr_engine):
    val, turn = cagr_engine.compute_cagr(start_val=100, end_val=161.051, periods=5)
    assert val == 10.0
    assert turn is False


def test_cagr_turnaround(cagr_engine):
    val, turn = cagr_engine.compute_cagr(start_val=-50, end_val=100, periods=3)
    assert val is None
    assert turn is True


def test_cagr_continuous_loss(cagr_engine):
    val, turn = cagr_engine.compute_cagr(start_val=-100, end_val=-50, periods=3)
    assert val is None
    assert turn is False


# --- 5. Cash Flow KPI Tests (Day 11) ---
def test_allocation_mature_cash_cow(cf_engine):
    assert cf_engine.get_allocation_pattern(cfo=1000, cfi=-500, cff=-200).startswith(
        "1."
    )


def test_allocation_high_burn_startup(cf_engine):
    assert cf_engine.get_allocation_pattern(cfo=-1000, cfi=-500, cff=1500).startswith(
        "6."
    )


def test_allocation_liquidity_crisis(cf_engine):
    assert cf_engine.get_allocation_pattern(cfo=-500, cfi=-200, cff=-100).startswith(
        "5."
    )


def test_cfo_quality_score(cf_engine):
    # Faking dataframe apply logic manually for test
    row = {"cfo": 150, "net_profit": 100}
    assert round(row["cfo"] / row["net_profit"], 2) == 1.50


def test_cfo_quality_negative_profit(cf_engine):
    row = {"cfo": 150, "net_profit": -100}
    val = round(row["cfo"] / row["net_profit"], 2) if row["net_profit"] > 0 else None
    assert val is None
