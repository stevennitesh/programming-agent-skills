from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "skills/extra/value-stock/scripts/valuation_gateway.py"
FIXTURES = ROOT / "tests/fixtures/value_stock_residual_income"


def load_gateway() -> ModuleType:
    spec = importlib.util.spec_from_file_location("value_stock_valuation_gateway", GATEWAY)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load valuation gateway")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture() -> dict[str, object]:
    return json.loads(
        (FIXTURES / "residual_income_model_lock.json").read_text(encoding="utf-8")
    )


NEGATIVE_CASES = json.loads(
    (FIXTURES / "residual_income_negative_cases.json").read_text(encoding="utf-8")
)["cases"]


def apply_mutation(source: dict[str, object], case: dict[str, Any]) -> None:
    target: Any = source
    for part in case["path"][:-1]:
        target = target[part]
    leaf = case["path"][-1]
    if case["operation"] == "set":
        target[leaf] = copy.deepcopy(case["value"])
    else:
        raise AssertionError(f"unknown mutation operation: {case['operation']}")


def test_frozen_residual_income_case_matches_independent_oracle_without_mutation() -> None:
    gateway = load_gateway()
    source = load_fixture()
    before = copy.deepcopy(source)
    oracle = json.loads(
        (FIXTURES / "residual_income_oracle_v1.json").read_text(encoding="utf-8")
    )

    receipt = gateway.calculate_model_lock(source)

    assert source == before
    assert "beginning_book_value_input" not in source["residual_income"][
        "forecast_periods"
    ][1]
    assert receipt["mechanical_status"] == "pass"
    assert receipt["method"] == "residual_income"
    assert receipt["versions"]["calculation_path"] == "residual-income-contract-v1"
    assert receipt["path_contract"] == {
        "arithmetic_precision_digits": 50,
        "compounding": "annual",
        "day_count": "actual_365",
        "ending_book_value_formula": (
            "residual-income-v1:beginning-book-plus-net-income-minus-dividends-plus-adjustments"
        ),
        "forecast_rate_basis": "valuation_origin_spot",
        "net_income_formula": "residual-income-v1:roe-times-beginning-book-value",
        "output_decimal_places": 8,
        "residual_income_formula": "residual-income-v1:net-income-minus-equity-charge",
        "reverse_solve_tolerance": "0.00000001",
        "rounding": "ROUND_HALF_EVEN",
        "terminal_formula": (
            "residual-income-v1:next-residual-income-over-ke-minus-growth"
        ),
        "timing_conventions": {
            "explicit": "caller_declared_realization_date",
            "year_end": "declared_period_end_date",
        },
    }
    assert receipt["calculation"] == oracle["expected"]
    assert receipt["assertions"][-1] == {
        "id": "residual_income_calculation_valid",
        "status": "pass",
    }


@pytest.mark.parametrize("case", NEGATIVE_CASES, ids=lambda case: case["id"])
def test_residual_income_negative_control_passes_fails_and_restores(
    case: dict[str, Any],
) -> None:
    gateway = load_gateway()
    conforming = load_fixture()
    baseline = gateway.calculate_model_lock(conforming)
    mutated = copy.deepcopy(conforming)
    apply_mutation(mutated, case)

    failed = gateway.calculate_model_lock(mutated)
    restored = gateway.calculate_model_lock(conforming)

    assert baseline["mechanical_status"] == "pass"
    assert failed["mechanical_status"] == "fail"
    assert case["expected_code"] in {failure["code"] for failure in failed["failures"]}
    assert restored == baseline


def test_residual_income_without_terminal_uses_forecast_residual_income_only() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["conventions"]["terminal"] = "none"
    source["residual_income"]["terminal"] = None

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["calculation"]["terminal"] is None
    assert receipt["calculation"]["target_common_equity"] == "1073.05785124"
    assert receipt["calculation"]["per_share_value"] == "10.73057851"
