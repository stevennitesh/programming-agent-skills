from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from decimal import localcontext
from pathlib import Path
from types import ModuleType

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "skills/extra/value-stock/scripts/valuation_gateway.py"
FIXTURES = ROOT / "tests/fixtures/value_stock_gateway"


def load_gateway() -> ModuleType:
    spec = importlib.util.spec_from_file_location("value_stock_gateway", GATEWAY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


def run_gateway(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(GATEWAY), str(path), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )


def test_equivalent_json_and_yaml_have_same_identity_without_file_mutation() -> None:
    json_path = FIXTURES / "valid_model_lock.json"
    yaml_path = FIXTURES / "valid_model_lock.yaml"
    before = {path: path.read_bytes() for path in (json_path, yaml_path)}

    json_run = run_gateway(json_path)
    yaml_run = run_gateway(yaml_path)

    assert json_run.returncode == 0, json_run.stderr
    assert yaml_run.returncode == 0, yaml_run.stderr
    json_receipt = json.loads(json_run.stdout)
    yaml_receipt = json.loads(yaml_run.stdout)
    assert json_receipt["mechanical_status"] == "pass"
    assert yaml_receipt["mechanical_status"] == "pass"
    assert json_receipt["input_identity"] == yaml_receipt["input_identity"]
    assert json_receipt["normalized_input"] == yaml_receipt["normalized_input"]
    assert json_receipt["versions"] == yaml_receipt["versions"]
    assert before == {path: path.read_bytes() for path in (json_path, yaml_path)}


def test_library_is_immutable_repeatable_and_change_sensitive() -> None:
    gateway = load_gateway()
    source = json.loads((FIXTURES / "valid_model_lock.json").read_text(encoding="utf-8"))
    before = copy.deepcopy(source)

    first = gateway.process_model_lock(source)
    repeated = gateway.process_model_lock(source)
    changed_source = copy.deepcopy(source)
    changed_source["inputs"]["revenue"]["value"] = 1201
    changed = gateway.process_model_lock(changed_source)

    assert source == before
    assert first == repeated
    assert first["input_identity"] != changed["input_identity"]
    assert first["normalized_input"]["inputs"]["revenue"]["value"] == "1200"
    assert first["contract"] == {
        "assertion_tolerance_owner": "calculator-version",
        "canonical_identity": "sha256-canonical-json-v1",
        "max_decimal_places": 12,
        "rounding": "ROUND_HALF_EVEN",
        "solver_tolerance_owner": "calculation-path-version",
        "supported_conventions": {
            "fcff": {"terminal": ["none", "perpetual_growth"]},
            "residual_income": {"terminal": ["continuing_residual_income", "none"]},
            "timing": ["explicit", "midyear", "year_end"],
        },
    }


def valid_source() -> dict[str, object]:
    return json.loads((FIXTURES / "valid_model_lock.json").read_text(encoding="utf-8"))


def invalid_source(case: str) -> dict[str, object]:
    source = valid_source()
    inputs = source["inputs"]
    assert isinstance(inputs, dict)
    revenue = inputs["revenue"]
    assert isinstance(revenue, dict)
    shares = source["diluted_shares"]
    assert isinstance(shares, dict)
    conventions = source["conventions"]
    assert isinstance(conventions, dict)
    tax_rate = inputs["tax_rate"]
    assert isinstance(tax_rate, dict)

    if case == "reference":
        revenue.pop("source_ref")
    elif case == "finite":
        revenue["value"] = float("inf")
    elif case == "precision":
        revenue["value"] = 0.1234567890123
    elif case == "unit":
        revenue.pop("unit")
    elif case == "unit_mismatch":
        tax_rate["unit"] = "currency"
    elif case == "currency":
        revenue.pop("currency")
    elif case == "currency_mismatch":
        revenue["currency"] = "EUR"
    elif case == "period":
        revenue["period"] = "FY2099"
    elif case == "scenario":
        revenue["scenario"] = "undeclared"
    elif case == "claim":
        revenue["claim_basis"] = "mystery_claim"
    elif case == "shares":
        shares["value"] = 0
    elif case == "share_claim":
        shares["claim_basis"] = "operating"
    elif case == "method":
        source["method"] = "nav"
    elif case == "terminal":
        conventions["terminal"] = "continuing_residual_income"
    elif case == "base_scenario":
        source["base_scenario"] = "undeclared"
    elif case == "date":
        source["as_of_date"] = "08/01/2026"
    else:
        raise AssertionError(f"unknown case: {case}")
    return source


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("reference", "reference"),
        ("finite", "finite"),
        ("precision", "precision"),
        ("unit", "schema"),
        ("unit_mismatch", "schema"),
        ("currency", "schema"),
        ("currency_mismatch", "currency"),
        ("period", "period"),
        ("scenario", "scenario"),
        ("claim", "schema"),
        ("shares", "positive"),
        ("share_claim", "schema"),
        ("method", "schema"),
        ("terminal", "method_convention"),
        ("base_scenario", "scenario"),
        ("date", "schema"),
    ],
)
def test_identifiable_invalid_input_returns_typed_failure(
    case: str,
    expected_code: str,
) -> None:
    gateway = load_gateway()
    source = invalid_source(case)
    before = copy.deepcopy(source)

    receipt = gateway.process_model_lock(source)

    assert source == before
    assert receipt["mechanical_status"] == "fail"
    assert receipt["run_id"] == "VAL-GATEWAY-FIXTURE-001"
    assert "input_identity" not in receipt
    assert "normalized_input" not in receipt
    assert expected_code in {failure["code"] for failure in receipt["failures"]}
    assert receipt["versions"]["gateway_contract"] == "model-lock-v1"


def test_cli_identifiable_failure_emits_receipt_and_nonzero_exit(tmp_path: Path) -> None:
    source = invalid_source("reference")
    path = tmp_path / "invalid-model-lock.json"
    path.write_text(json.dumps(source), encoding="utf-8")

    completed = run_gateway(path)

    assert completed.returncode == 2
    assert completed.stderr == ""
    receipt = json.loads(completed.stdout)
    assert receipt["mechanical_status"] == "fail"
    assert receipt["run_id"] == "VAL-GATEWAY-FIXTURE-001"
    assert "input_identity" not in receipt
    assert "reference" in {failure["code"] for failure in receipt["failures"]}


@pytest.mark.parametrize("method", [[], {}, 7])
def test_identifiable_non_string_method_returns_failure_receipt(method: object) -> None:
    gateway = load_gateway()
    source = valid_source()
    source["method"] = method

    receipt = gateway.process_model_lock(source)

    assert receipt["mechanical_status"] == "fail"
    assert receipt["run_id"] == "VAL-GATEWAY-FIXTURE-001"
    assert "schema" in {failure["code"] for failure in receipt["failures"]}


@pytest.mark.parametrize("suffix", [".json", ".yaml"])
@pytest.mark.parametrize("method", [[], {}, 7])
def test_cli_non_string_method_has_typed_failure_without_traceback(
    tmp_path: Path,
    suffix: str,
    method: object,
) -> None:
    source = valid_source()
    source["method"] = method
    path = tmp_path / f"invalid-method{suffix}"
    if suffix == ".json":
        path.write_text(json.dumps(source), encoding="utf-8")
    else:
        path.write_text(yaml.safe_dump(source), encoding="utf-8")

    completed = run_gateway(path)

    assert completed.returncode == 2
    assert completed.stderr == ""
    receipt = json.loads(completed.stdout)
    assert receipt["mechanical_status"] == "fail"
    assert "schema" in {failure["code"] for failure in receipt["failures"]}


@pytest.mark.parametrize("payload", ["{}", "{not-json"])
def test_cli_unidentifiable_input_does_not_fabricate_receipt(
    tmp_path: Path,
    payload: str,
) -> None:
    path = tmp_path / "unidentifiable.json"
    path.write_text(payload, encoding="utf-8")

    completed = run_gateway(path)

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert completed.stderr.startswith("model-lock input error:")


def test_cli_missing_input_does_not_fabricate_receipt(tmp_path: Path) -> None:
    completed = run_gateway(tmp_path / "missing.json")

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert completed.stderr.startswith("model-lock input error:")


@pytest.mark.parametrize(
    ("suffix", "payload"),
    [
        (".json", '{"run_id":"first","run_id":"second"}'),
        (".yaml", "run_id: first\nrun_id: second\n"),
    ],
)
def test_cli_rejects_duplicate_keys_without_choosing_a_value(
    tmp_path: Path,
    suffix: str,
    payload: str,
) -> None:
    path = tmp_path / f"duplicate{suffix}"
    path.write_text(payload, encoding="utf-8")

    completed = run_gateway(path)

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert "duplicate key" in completed.stderr


def test_cli_rejects_unsupported_yaml_number_without_a_traceback(tmp_path: Path) -> None:
    payload = (FIXTURES / "valid_model_lock.yaml").read_text(encoding="utf-8")
    path = tmp_path / "unsupported-number.yaml"
    path.write_text(payload.replace("value: 1200", "value: 0x10"), encoding="utf-8")

    completed = run_gateway(path)

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert completed.stderr.startswith("model-lock input error:")
    assert "Traceback" not in completed.stderr


def test_markdown_is_a_compact_navigation_summary() -> None:
    path = FIXTURES / "valid_model_lock.json"
    markdown_run = run_gateway(path, "--output-format", "markdown")

    assert markdown_run.returncode == 0, markdown_run.stderr
    assert markdown_run.stdout.startswith("# Calculation Receipt\n")
    assert "mechanical_status: `pass`" in markdown_run.stdout
    assert "input_identity:" in markdown_run.stdout
    assert "```json" not in markdown_run.stdout
    assert "normalized_input" not in markdown_run.stdout


def test_normalized_contract_is_revalidated_and_identity_is_independently_checkable() -> None:
    gateway = load_gateway()
    receipt = gateway.process_model_lock(valid_source())
    normalized = receipt["normalized_input"]
    canonical = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )

    assert receipt["input_identity"] == (
        "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    )
    assert receipt["assertions"] == [
        {"id": "model_lock_source_valid", "status": "pass"},
        {"id": "model_lock_normalized_valid", "status": "pass"},
    ]

    corrupted = copy.deepcopy(normalized)
    corrupted["inputs"]["revenue"]["value"] = "1200.00"
    failures = gateway.validate_normalized_model_lock(corrupted)
    assert "normalized_numeric" in {failure["code"] for failure in failures}


def test_mutating_a_receipt_cannot_change_the_gateway_contract() -> None:
    gateway = load_gateway()
    first = gateway.process_model_lock(valid_source())

    first["contract"]["rounding"] = "CORRUPTED"
    second = gateway.process_model_lock(valid_source())

    assert second["contract"]["rounding"] == "ROUND_HALF_EVEN"


def test_high_significance_integers_preserve_value_and_identity() -> None:
    gateway = load_gateway()
    first_source = valid_source()
    second_source = valid_source()
    first_value = 123456789012345678901234567890
    second_value = 123456789012345678901234567891
    first_source["inputs"]["revenue"]["value"] = first_value
    second_source["inputs"]["revenue"]["value"] = second_value

    with localcontext() as context:
        context.prec = 6
        first = gateway.process_model_lock(first_source)
        second = gateway.process_model_lock(second_source)

    assert first["normalized_input"]["inputs"]["revenue"]["value"] == str(first_value)
    assert second["normalized_input"]["inputs"]["revenue"]["value"] == str(second_value)
    assert first["input_identity"] != second["input_identity"]
