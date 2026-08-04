from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
from decimal import Inexact, Rounded, localcontext
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "skills/extra/value-stock/scripts/valuation_gateway.py"
FIXTURES = ROOT / "tests/fixtures/value_stock_fcff"
MODEL_LOCK = ROOT / "skills/extra/value-stock/examples/fcff-model-lock.json"


def load_gateway() -> ModuleType:
    spec = importlib.util.spec_from_file_location("value_stock_fcff_gateway", GATEWAY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


def load_fixture() -> dict[str, object]:
    return json.loads(MODEL_LOCK.read_text(encoding="utf-8"))


def run_gateway(command: str, path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(GATEWAY), command, str(path), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )


NEGATIVE_CASES = json.loads(
    (FIXTURES / "fcff_negative_cases.json").read_text(encoding="utf-8")
)["cases"]


def apply_mutation(source: dict[str, object], case: dict[str, Any]) -> None:
    target: Any = source
    for part in case["path"][:-1]:
        target = target[part]
    leaf = case["path"][-1]
    if case["operation"] == "set":
        target[leaf] = copy.deepcopy(case["value"])
    elif case["operation"] == "delete":
        del target[leaf]
    elif case["operation"] == "append":
        target[leaf].append(copy.deepcopy(case["value"]))
    else:
        raise AssertionError(f"unknown mutation operation: {case['operation']}")


def test_frozen_fcff_case_matches_independent_oracle_without_input_mutation() -> None:
    gateway = load_gateway()
    source = load_fixture()
    before = copy.deepcopy(source)
    oracle = json.loads((FIXTURES / "fcff_oracle_v1.json").read_text(encoding="utf-8"))

    receipt = gateway.calculate_model_lock(source)

    assert source == before
    assert receipt["mechanical_status"] == "pass"
    assert receipt["method"] == "fcff"
    assert receipt["versions"]["calculation_path"] == "fcff-contract-v1"
    assert receipt["path_contract"] == {
        "arithmetic_precision_digits": 50,
        "assertion_absolute_tolerance": "0.00000001",
        "claim_bridge_signs": {
            "add": ["excess_cash", "non_operating_assets"],
            "subtract": [
                "debt",
                "preferred_stock",
                "noncontrolling_interests",
                "other_senior_claims",
                "existing_awards",
            ],
            "declared": ["target_claim_adjustments"],
        },
        "compounding": "annual",
        "day_count": "actual_365",
        "forecast_rate_basis": "valuation_origin_spot",
        "derived_fcff_formula": (
            "fcff-v1:nopat-plus-da-minus-capex-minus-working-capital-change"
        ),
        "output_decimal_places": 8,
        "reverse_solve_tolerance": "0.00000001",
        "rounding": "ROUND_HALF_EVEN",
        "terminal_wacc_roles": [
            "valuation_origin_spot_discount_rate",
            "perpetual_growth_denominator_rate",
        ],
        "timing_conventions": {
            "explicit": "caller_declared_realization_date",
            "midyear": "floor_midpoint_from_declared_first_prior_period_end",
            "year_end": "declared_period_end_date",
        },
        "terminal_formula": "fcff-v1:last-fcff-times-one-plus-growth",
    }
    assert receipt["calculation"] == oracle["expected"]
    assert receipt["assertions"][-1] == {"id": "fcff_calculation_valid", "status": "pass"}


def test_calculator_owns_derived_fcff_terminal_values_and_fixed_conventions() -> None:
    gateway = load_gateway()
    source = load_fixture()
    assert "fcff_fy2026" not in source["inputs"]
    assert "terminal_fcff" not in source["inputs"]
    assert "discounting" not in source["fcff"]
    assert "output_input" not in source["fcff"]["forecast_periods"][0]
    terminal_input = source["fcff"]["terminal"]
    assert "next_period_date" not in terminal_input
    assert "interval_years" not in terminal_input
    assert "next_period_fcff_input" not in terminal_input

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["path_contract"]["day_count"] == "actual_365"
    assert receipt["path_contract"]["compounding"] == "annual"
    assert receipt["path_contract"]["forecast_rate_basis"] == "valuation_origin_spot"
    assert "fcff_fy2026" not in receipt["normalized_input"]["inputs"]
    assert "terminal_fcff" not in receipt["normalized_input"]["inputs"]
    derived = receipt["calculation"]["forecast_periods"][0]
    assert "output_input" not in derived
    assert derived["lineage"] == {
        "kind": "formula",
        "ref": "fcff-v1:nopat-plus-da-minus-capex-minus-working-capital-change",
    }
    terminal_result = receipt["calculation"]["terminal"]
    assert terminal_result["next_period_date"] == "2028-12-31"
    assert "next_period_fcff_input" not in terminal_result
    assert terminal_result["formula_ref"] == "fcff-v1:last-fcff-times-one-plus-growth"
    assert terminal_result["next_period_fcff"] == "72.1"


@pytest.mark.parametrize("case", NEGATIVE_CASES, ids=lambda case: case["id"])
def test_fcff_negative_control_passes_fails_and_restores(case: dict[str, Any]) -> None:
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


def test_fcff_without_terminal_values_only_explicit_cash_flows() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["conventions"]["terminal"] = "none"
    source["fcff"]["terminal"] = None

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["calculation"]["terminal"] is None
    assert receipt["calculation"]["enterprise_value"] == "112.39669421"
    assert receipt["calculation"]["per_share_value"] == "0.53396694"


def test_cli_calculate_dispatches_json_and_compact_markdown_receipt() -> None:
    path = MODEL_LOCK

    json_run = run_gateway("calculate", path)
    markdown_run = run_gateway("calculate", path, "--output-format", "markdown")

    assert json_run.returncode == 0, json_run.stderr
    assert markdown_run.returncode == 0, markdown_run.stderr
    json_receipt = json.loads(json_run.stdout)
    assert json_receipt["calculation"]["per_share_value"] == "9.04636364"
    assert "## Results" in markdown_run.stdout
    assert "per_share_value: `9.04636364`" in markdown_run.stdout
    assert "## Diagnostics" in markdown_run.stdout
    assert "```json" not in markdown_run.stdout
    assert "normalized_input" not in markdown_run.stdout


def test_cli_calculation_failure_is_machine_readable_and_nonzero(tmp_path: Path) -> None:
    source = load_fixture()
    source["inputs"]["terminal_wacc"]["value"] = 0.03
    path = tmp_path / "invalid-fcff.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    completed = run_gateway("calculate", path)

    assert completed.returncode == 2
    assert completed.stderr == ""
    receipt = json.loads(completed.stdout)
    assert receipt["mechanical_status"] == "fail"
    assert "input_identity" in receipt
    assert "terminal_spread" in {failure["code"] for failure in receipt["failures"]}


def test_json_and_yaml_fcff_runs_have_identical_inputs_and_calculations(
    tmp_path: Path,
) -> None:
    json_path = MODEL_LOCK
    yaml_path = tmp_path / "fcff_model_lock.yaml"
    yaml_path.write_text(yaml.safe_dump(load_fixture(), sort_keys=False), encoding="utf-8")

    json_run = run_gateway("calculate", json_path)
    yaml_run = run_gateway("calculate", yaml_path)

    assert json_run.returncode == 0, json_run.stderr
    assert yaml_run.returncode == 0, yaml_run.stderr
    json_receipt = json.loads(json_run.stdout)
    yaml_receipt = json.loads(yaml_run.stdout)
    assert yaml_receipt["input_identity"] == json_receipt["input_identity"]
    assert yaml_receipt["normalized_input"] == json_receipt["normalized_input"]
    assert yaml_receipt["calculation"] == json_receipt["calculation"]


def test_fcff_result_is_independent_of_ambient_decimal_traps_and_bounds() -> None:
    gateway = load_gateway()
    source = load_fixture()
    oracle = json.loads((FIXTURES / "fcff_oracle_v1.json").read_text(encoding="utf-8"))

    with localcontext() as context:
        context.prec = 6
        context.Emax = 9
        context.Emin = -9
        context.traps[Inexact] = True
        context.traps[Rounded] = True
        receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["calculation"] == oracle["expected"]


def test_terminal_timing_must_follow_valuation_and_final_realization() -> None:
    gateway = load_gateway()
    valid_explicit = load_fixture()
    valid_explicit["conventions"]["timing"] = "explicit"
    valid_explicit["fcff"]["forecast_periods"][0]["realization_date"] = "2026-06-30"
    valid_explicit["fcff"]["forecast_periods"][1]["realization_date"] = "2027-09-30"

    elapsed_terminal = copy.deepcopy(valid_explicit)
    elapsed_terminal["periods"][1]["date"] = "2025-12-31"
    elapsed_terminal["fcff"]["terminal"]["terminal_date"] = "2025-12-31"
    elapsed_terminal["inputs"]["terminal_wacc"]["date"] = "2025-12-31"
    elapsed_terminal["inputs"]["terminal_growth"]["date"] = "2025-12-31"

    pre_forecast_terminal = copy.deepcopy(valid_explicit)
    pre_forecast_terminal["fcff"]["forecast_periods"][1]["realization_date"] = "2028-06-30"

    valid_receipt = gateway.calculate_model_lock(valid_explicit)
    elapsed_receipt = gateway.calculate_model_lock(elapsed_terminal)
    pre_forecast_receipt = gateway.calculate_model_lock(pre_forecast_terminal)

    assert valid_receipt["mechanical_status"] == "pass"
    for receipt in (elapsed_receipt, pre_forecast_receipt):
        assert receipt["mechanical_status"] == "fail"
        assert "terminal_timing" in {failure["code"] for failure in receipt["failures"]}


def test_diluted_shares_must_belong_to_base_scenario() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["scenarios"].append("diluted")
    source["diluted_shares"]["scenario"] = "diluted"

    failed = gateway.calculate_model_lock(source)

    assert failed["mechanical_status"] == "fail"
    assert "share_scenario" in {failure["code"] for failure in failed["failures"]}


def test_future_dilution_adjustment_must_subtract_from_equity() -> None:
    gateway = load_gateway()
    valid = load_fixture()
    valid["fcff"]["award_treatment"]["future_grants"] = "future_dilution"
    valid["fcff"]["award_treatment"]["future_grants_claim_adjustment"] = (
        "target_adjustment"
    )
    wrong_sign = copy.deepcopy(valid)
    wrong_sign["fcff"]["claim_bridge"]["target_claim_adjustments"][0]["effect"] = "add"

    valid_receipt = gateway.calculate_model_lock(valid)
    failed = gateway.calculate_model_lock(wrong_sign)
    restored = gateway.calculate_model_lock(valid)

    assert valid_receipt["mechanical_status"] == "pass"
    assert failed["mechanical_status"] == "fail"
    assert "future_grants_claim" in {failure["code"] for failure in failed["failures"]}
    assert restored == valid_receipt


def test_irregular_dates_match_independent_actual_365_oracle_and_one_day_change() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["conventions"]["timing"] = "explicit"
    source["fcff"]["forecast_periods"][0]["realization_date"] = "2026-06-30"
    source["fcff"]["forecast_periods"][1]["realization_date"] = "2027-06-30"
    source["periods"][1]["date"] = "2027-09-30"
    source["fcff"]["terminal"]["terminal_date"] = "2027-09-30"
    source["inputs"]["terminal_wacc"]["date"] = "2027-09-30"
    source["inputs"]["terminal_growth"]["date"] = "2027-09-30"
    oracle = json.loads((FIXTURES / "fcff_oracle_v1.json").read_text(encoding="utf-8"))[
        "irregular_actual_365_expected"
    ]

    receipt = gateway.calculate_model_lock(source)
    later = copy.deepcopy(source)
    later["fcff"]["forecast_periods"][0]["realization_date"] = "2026-07-01"
    later_receipt = gateway.calculate_model_lock(later)

    assert receipt["mechanical_status"] == "pass"
    for position, expected in enumerate(oracle["forecast_periods"]):
        actual = receipt["calculation"]["forecast_periods"][position]
        assert actual["discount_exponent"] == expected["discount_exponent"]
        assert actual["discount_factor"] == expected["discount_factor"]
        assert actual["present_value"] == expected["present_value"]
    terminal = receipt["calculation"]["terminal"]
    assert terminal["discount_exponent"] == oracle["terminal"]["discount_exponent"]
    assert terminal["discount_factor"] == oracle["terminal"]["discount_factor"]
    assert terminal["present_value"] == oracle["terminal"]["present_value"]
    assert receipt["calculation"]["enterprise_value"] == oracle["enterprise_value"]
    assert receipt["calculation"]["per_share_value"] == oracle["per_share_value"]
    assert later_receipt["calculation"]["forecast_periods"][0]["present_value"] == (
        oracle["first_cash_flow_one_day_later_present_value"]
    )


def test_midyear_timing_matches_independent_oracle_and_rejects_mistiming() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["as_of_date"] = "2026-03-31"
    source["diluted_shares"]["date"] = source["as_of_date"]
    for record in source["inputs"].values():
        if record.get("date") == "2025-12-31":
            record["date"] = source["as_of_date"]
    source["conventions"]["timing"] = "midyear"
    source["fcff"]["midyear_first_prior_period_end"] = "2025-12-31"
    source["fcff"]["forecast_periods"][0]["realization_date"] = "2026-07-01"
    source["fcff"]["forecast_periods"][1]["realization_date"] = "2027-07-01"
    oracle = json.loads((FIXTURES / "fcff_oracle_v1.json").read_text(encoding="utf-8"))[
        "midyear_expected"
    ]

    receipt = gateway.calculate_model_lock(source)
    mistimed = copy.deepcopy(source)
    mistimed["fcff"]["forecast_periods"][0]["realization_date"] = "2026-06-30"
    failed = gateway.calculate_model_lock(mistimed)
    reversed_periods = copy.deepcopy(source)
    reversed_periods["conventions"]["terminal"] = "none"
    reversed_periods["fcff"]["terminal"] = None
    reversed_periods["periods"][1]["date"] = "2026-06-30"
    reversed_receipt = gateway.calculate_model_lock(reversed_periods)
    future_prior_end = copy.deepcopy(source)
    future_prior_end["fcff"]["midyear_first_prior_period_end"] = "2026-04-01"
    future_prior_end["fcff"]["forecast_periods"][0][
        "realization_date"
    ] = "2026-08-16"
    future_prior_receipt = gateway.calculate_model_lock(future_prior_end)
    restored = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    for position, expected in enumerate(oracle["forecast_periods"]):
        actual = receipt["calculation"]["forecast_periods"][position]
        assert actual["realization_date"] == expected["realization_date"]
        assert actual["discount_exponent"] == expected["discount_exponent"]
        assert actual["discount_factor"] == expected["discount_factor"]
        assert actual["present_value"] == expected["present_value"]
    terminal = receipt["calculation"]["terminal"]
    assert terminal["discount_exponent"] == oracle["terminal"]["discount_exponent"]
    assert terminal["discount_factor"] == oracle["terminal"]["discount_factor"]
    assert terminal["present_value"] == oracle["terminal"]["present_value"]
    assert receipt["calculation"]["enterprise_value"] == oracle["enterprise_value"]
    assert receipt["calculation"]["per_share_value"] == oracle["per_share_value"]
    assert failed["mechanical_status"] == "fail"
    assert "timing_convention" in {failure["code"] for failure in failed["failures"]}
    assert reversed_receipt["mechanical_status"] == "fail"
    assert "timing_convention" in {
        failure["code"] for failure in reversed_receipt["failures"]
    }
    assert future_prior_receipt["mechanical_status"] == "fail"
    assert "timing_convention" in {
        failure["code"] for failure in future_prior_receipt["failures"]
    }
    assert restored == receipt


def test_unequal_valuation_origin_spot_rates_match_independent_oracle() -> None:
    gateway = load_gateway()
    source = load_fixture()
    source["conventions"]["timing"] = "explicit"
    source["fcff"]["forecast_periods"][0]["realization_date"] = "2026-06-30"
    source["fcff"]["forecast_periods"][1]["realization_date"] = "2027-06-30"
    source["periods"][1]["date"] = "2027-09-30"
    source["fcff"]["terminal"]["terminal_date"] = "2027-09-30"
    source["inputs"]["terminal_wacc"]["date"] = "2027-09-30"
    source["inputs"]["terminal_growth"]["date"] = "2027-09-30"
    source["inputs"]["wacc_fy2026"]["value"] = 0.08
    source["inputs"]["wacc_fy2027"]["value"] = 0.12
    oracle = json.loads((FIXTURES / "fcff_oracle_v1.json").read_text(encoding="utf-8"))[
        "unequal_spot_rate_expected"
    ]

    receipt = gateway.calculate_model_lock(source)

    assert receipt["mechanical_status"] == "pass"
    assert receipt["path_contract"]["forecast_rate_basis"] == oracle["rate_basis"]
    for position, expected in enumerate(oracle["forecast_periods"]):
        actual = receipt["calculation"]["forecast_periods"][position]
        assert actual["discount_rate"] == expected["discount_rate"]
        assert actual["discount_exponent"] == expected["discount_exponent"]
        assert actual["discount_factor"] == expected["discount_factor"]
        assert actual["present_value"] == expected["present_value"]
    terminal = receipt["calculation"]["terminal"]
    assert terminal["wacc"] == oracle["terminal"]["discount_rate"]
    assert terminal["discount_exponent"] == oracle["terminal"]["discount_exponent"]
    assert terminal["discount_factor"] == oracle["terminal"]["discount_factor"]
    assert terminal["present_value"] == oracle["terminal"]["present_value"]
    assert receipt["calculation"]["enterprise_value"] == oracle["enterprise_value"]
    assert receipt["calculation"]["per_share_value"] == oracle["per_share_value"]


def test_fixed_discount_conventions_are_owned_by_the_path_contract() -> None:
    gateway = load_gateway()
    conforming = load_fixture()
    caller_override = copy.deepcopy(conforming)
    caller_override["fcff"]["discounting"] = {
        "day_count": "actual_365",
        "compounding": "annual",
        "forecast_rate_basis": "valuation_origin_spot",
    }

    baseline = gateway.calculate_model_lock(conforming)
    failed = gateway.calculate_model_lock(caller_override)
    restored = gateway.calculate_model_lock(conforming)

    assert baseline["mechanical_status"] == "pass"
    assert baseline["path_contract"]["day_count"] == "actual_365"
    assert baseline["path_contract"]["compounding"] == "annual"
    assert baseline["path_contract"]["forecast_rate_basis"] == "valuation_origin_spot"
    assert failed["mechanical_status"] == "fail"
    assert "schema" in {failure["code"] for failure in failed["failures"]}
    assert restored == baseline


def test_fcff_receipt_is_repeatable_and_changes_with_load_bearing_input() -> None:
    gateway = load_gateway()
    source = load_fixture()

    first = gateway.calculate_model_lock(source)
    repeated = gateway.calculate_model_lock(source)
    changed_source = copy.deepcopy(source)
    changed_source["inputs"]["fcff_fy2027"]["value"] = 71
    changed = gateway.calculate_model_lock(changed_source)

    assert repeated == first
    assert changed["mechanical_status"] == "pass"
    assert changed["input_identity"] != first["input_identity"]
    assert changed["calculation"]["per_share_value"] != first["calculation"]["per_share_value"]


def test_declared_award_treatments_account_for_claims_once() -> None:
    gateway = load_gateway()
    future_dilution = load_fixture()
    future_dilution["fcff"]["award_treatment"]["future_grants"] = "future_dilution"
    future_dilution["fcff"]["award_treatment"][
        "future_grants_claim_adjustment"
    ] = "target_adjustment"
    awards_in_shares = load_fixture()
    awards_in_shares["fcff"]["award_treatment"]["existing_awards"] = "diluted_shares"
    awards_in_shares["fcff"]["claim_bridge"]["existing_awards"] = []
    del awards_in_shares["inputs"]["existing_awards"]

    future_receipt = gateway.calculate_model_lock(future_dilution)
    shares_receipt = gateway.calculate_model_lock(awards_in_shares)

    assert future_receipt["mechanical_status"] == "pass"
    assert shares_receipt["mechanical_status"] == "pass"
    assert shares_receipt["calculation"]["claim_bridge"]["existing_awards"] == "0"
    assert shares_receipt["calculation"]["per_share_value"] == "9.07636364"


def test_target_claim_adjustment_signs_are_applied_once_and_reported() -> None:
    gateway = load_gateway()
    subtract = load_fixture()
    add = copy.deepcopy(subtract)
    add["fcff"]["claim_bridge"]["target_claim_adjustments"][0]["effect"] = "add"

    subtract_receipt = gateway.calculate_model_lock(subtract)
    add_receipt = gateway.calculate_model_lock(add)

    assert subtract_receipt["mechanical_status"] == "pass"
    assert add_receipt["mechanical_status"] == "pass"
    assert subtract_receipt["calculation"]["claim_bridge"][
        "target_claim_adjustments"
    ] == "-1"
    assert add_receipt["calculation"]["claim_bridge"]["target_claim_adjustments"] == "1"
    assert subtract_receipt["calculation"]["per_share_value"] == "9.04636364"
    assert add_receipt["calculation"]["per_share_value"] == "9.06636364"
