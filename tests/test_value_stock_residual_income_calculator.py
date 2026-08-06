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
MODEL_LOCK = ROOT / "skills/extra/value-stock/examples/residual-income-model-lock.json"


def load_gateway() -> ModuleType:
    spec = importlib.util.spec_from_file_location("value_stock_valuation_gateway", GATEWAY)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load valuation gateway")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture() -> dict[str, object]:
    return json.loads(MODEL_LOCK.read_text(encoding="utf-8"))


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
    assert receipt["versions"]["calculation_path"] == "residual-income-contract-v2"
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
        "terminal_clean_surplus_assumption": "no_direct_equity_adjustment",
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


def test_terminal_exposes_implied_clean_surplus_economics_without_judgment() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["residual_income"].pop("claim_bridge")
    source["residual_income"].pop("award_treatment")

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    terminal = receipt["calculation"]["terminal"]
    assert terminal["next_period_net_income"] == "145.2"
    assert terminal["next_period_book_value_growth"] == "36.3"
    assert terminal["next_period_ending_book_value"] == "1246.3"
    assert terminal["implied_distribution"] == "108.9"
    assert terminal["implied_payout_ratio"] == "0.75"
    assert terminal["direct_equity_adjustment"] == "0"
    assert terminal["direct_equity_adjustment_assumption"] == (
        "none_supplied_clean_surplus_assumes_zero"
    )
    assert "warnings" not in terminal

    undefined = copy.deepcopy(source)
    undefined["inputs"]["terminal_roe"]["value"] = 0
    failed = gateway.calculate_model_lock(undefined)
    assert failed["mechanical_status"] == "fail"
    assert "terminal_payout_undefined" in {
        failure["code"] for failure in failed["failures"]
    }


def test_residual_income_target_security_bridge_and_award_convention_are_exclusive() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["inputs"]["existing_awards"] = {
        "value": 3,
        "unit": "currency",
        "value_kind": "monetary",
        "currency": "USD",
        "date": "2025-12-31",
        "evidence_class": "estimated",
        "claim_basis": "target_security",
        "scenario": "base",
        "source_ref": "model-lock:existing-awards",
    }
    source["inputs"]["target_adjustment"] = {
        "value": 1,
        "unit": "currency",
        "value_kind": "monetary",
        "currency": "USD",
        "date": "2025-12-31",
        "evidence_class": "estimated",
        "claim_basis": "target_security",
        "scenario": "base",
        "source_ref": "model-lock:target-adjustment",
    }
    source["residual_income"]["claim_bridge"] = {
        "existing_awards": ["existing_awards"],
        "target_claim_adjustments": [
            {"effect": "subtract", "input": "target_adjustment"}
        ],
    }
    source["residual_income"]["award_treatment"] = {
        "existing_awards": "claim_bridge"
    }

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["calculation"]["common_equity_before_target_adjustments"] == (
        "1358.77213695"
    )
    assert receipt["calculation"]["claim_bridge"] == {
        "existing_awards": "3",
        "target_claim_adjustments": "-1",
        "target_common_equity": "1354.77213695",
    }
    assert receipt["calculation"]["per_share_value"] == "13.54772137"

    added = copy.deepcopy(source)
    added["residual_income"]["claim_bridge"]["target_claim_adjustments"][0][
        "effect"
    ] = "add"
    added_receipt = gateway.calculate_model_lock(added)
    assert added_receipt["mechanical_status"] == "pass"
    assert added_receipt["calculation"]["claim_bridge"][
        "target_claim_adjustments"
    ] == "1"
    assert added_receipt["calculation"]["per_share_value"] == "13.56772137"

    double_counted = copy.deepcopy(source)
    double_counted["residual_income"]["award_treatment"]["existing_awards"] = (
        "diluted_shares"
    )
    failed = gateway.calculate_model_lock(double_counted)
    assert failed["mechanical_status"] == "fail"
    assert "award_double_count" in {
        failure["code"] for failure in failed["failures"]
    }

    unreferenced = copy.deepcopy(source)
    unreferenced["residual_income"]["claim_bridge"][
        "target_claim_adjustments"
    ] = []
    incomplete = gateway.calculate_model_lock(unreferenced)
    assert incomplete["mechanical_status"] == "fail"
    assert "bridge_incomplete" in {
        failure["code"] for failure in incomplete["failures"]
    }
