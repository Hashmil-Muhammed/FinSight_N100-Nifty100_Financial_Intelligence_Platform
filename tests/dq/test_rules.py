import pytest


def check_dq_rule(rule_id, value):
    rules = {
        "DQ01": {"severity": "CRITICAL", "passes": value is not None},
        "DQ02": {"severity": "HIGH", "passes": isinstance(value, str)},
        "DQ03": {
            "severity": "MEDIUM",
            "passes": value > 0 if type(value) in (int, float) else False,
        },
    }
    return rules.get(rule_id, {"severity": "UNKNOWN", "passes": False})


@pytest.mark.parametrize(
    "rule_id, value, exp_sev, exp_pass",
    [
        ("DQ01", 100, "CRITICAL", True),
        ("DQ01", None, "CRITICAL", False),
        ("DQ02", "TCS", "HIGH", True),
        ("DQ02", 123, "HIGH", False),
        ("DQ03", 50, "MEDIUM", True),
        ("DQ03", -10, "MEDIUM", False),
        ("DQ04", 100, "UNKNOWN", False),
        ("DQ01", "Data", "CRITICAL", True),
        ("DQ01", "", "CRITICAL", True),
        ("DQ02", "ABB", "HIGH", True),
        ("DQ02", None, "HIGH", False),
        ("DQ03", 0.1, "MEDIUM", True),
        ("DQ03", 0, "MEDIUM", False),
        ("DQ03", 9999, "MEDIUM", True),
    ],
)
def test_dq_rules(rule_id, value, exp_sev, exp_pass):
    res = check_dq_rule(rule_id, value)
    assert res["severity"] == exp_sev
    assert res["passes"] == exp_pass
