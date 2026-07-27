import pytest


# Mock KPI logic for standalone testing
def calc_roe(net_profit, equity):
    if equity is None or equity <= 0:
        return None
    return round((net_profit / equity) * 100, 2)


def calc_de(debt, equity):
    if debt == 0:
        return 0.0
    if equity is None or equity <= 0:
        return None
    return round(debt / equity, 2)


def calc_icr(op_profit, interest):
    if interest is None or interest == 0:
        return None
    return round(op_profit / interest, 2)


def check_turnaround(old_val, new_val):
    if old_val < 0 and new_val > 0:
        return 1
    return 0


@pytest.mark.parametrize(
    "np, eq, exp",
    [
        (100, 1000, 10.0),
        (-50, 1000, -5.0),
        (100, -500, None),
        (100, 0, None),
        (0, 1000, 0.0),
    ],
)
def test_roe_logic(np, eq, exp):
    assert calc_roe(np, eq) == exp


@pytest.mark.parametrize(
    "debt, eq, exp",
    [
        (0, 1000, 0.0),
        (500, 1000, 0.5),
        (1000, 500, 2.0),
        (500, -100, None),
        (0, -100, 0.0),
    ],
)
def test_de_logic(debt, eq, exp):
    assert calc_de(debt, eq) == exp


@pytest.mark.parametrize(
    "op, int_exp, exp",
    [
        (1000, 100, 10.0),
        (1000, 0, None),
        (-500, 100, -5.0),
        (1000, None, None),
        (0, 100, 0.0),
    ],
)
def test_icr_logic(op, int_exp, exp):
    assert calc_icr(op, int_exp) == exp


@pytest.mark.parametrize(
    "old, new, exp",
    [(-10, 50, 1), (10, 50, 0), (-10, -5, 0), (50, -10, 0), (-100, 1, 1)],
)
def test_turnaround_flag(old, new, exp):
    assert check_turnaround(old, new) == exp
