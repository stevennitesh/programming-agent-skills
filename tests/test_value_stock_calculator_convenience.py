from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
from decimal import Decimal, Inexact, Rounded, localcontext
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "skills/extra/value-stock/scripts/valuation_gateway.py"
FCFF_FIXTURE = ROOT / "skills/extra/value-stock/examples/fcff-model-lock.json"
RI_FIXTURE = (
    ROOT
    / "tests/fixtures/value_stock_residual_income/residual_income_model_lock.json"
)
SKILL = ROOT / "skills/extra/value-stock/SKILL.md"
METHODS = ROOT / "skills/extra/value-stock/references/valuation-methods.md"
WORKFLOW_PROOF = ROOT / "docs/validation/skills/value-stock"


def load_gateway() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "value_stock_calculator_convenience", GATEWAY
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


def load_fixture(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def use_scenario(source: dict[str, object], scenario: str) -> None:
    source["run_id"] = f"{source['run_id']}-{scenario}"
    source["base_scenario"] = scenario
    source["scenarios"] = [scenario]
    source["diluted_shares"]["scenario"] = scenario
    for record in source["inputs"].values():
        record["scenario"] = scenario


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


def test_cli_has_obvious_validate_and_calculate_routes_with_copyable_help() -> None:
    help_run = subprocess.run(
        [sys.executable, str(GATEWAY), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    validate_run = run_gateway("validate", FCFF_FIXTURE)
    calculate_run = run_gateway("calculate", FCFF_FIXTURE)

    assert help_run.returncode == 0
    assert "validate INPUT" in help_run.stdout
    assert "calculate INPUT" in help_run.stdout
    assert (
        "python scripts/valuation_gateway.py calculate "
        "examples/fcff-model-lock.json" in help_run.stdout
    )
    assert validate_run.returncode == 0, validate_run.stderr
    assert "calculation" not in json.loads(validate_run.stdout)
    assert calculate_run.returncode == 0, calculate_run.stderr
    assert json.loads(calculate_run.stdout)["calculation"]["per_share_value"]


def test_skill_has_one_calculator_route_to_the_tested_example_and_method_owner() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    methods = METHODS.read_text(encoding="utf-8")

    assert skill.count("## Run The Calculator") == 1
    assert "[canonical Model Lock](examples/fcff-model-lock.json)" in skill
    assert "[valuation-methods.md](references/valuation-methods.md)" in skill
    assert "python scripts/valuation_gateway.py validate examples/fcff-model-lock.json" in skill
    assert "python scripts/valuation_gateway.py calculate examples/fcff-model-lock.json" in skill
    assert "`mechanical_status: fail` excludes the affected result" in skill
    assert "explicit capability gap" in skill
    assert "receipt supplies all material arithmetic and assertions" in methods

    canonical_path = "skills/extra/value-stock/examples/fcff-model-lock.json"
    oracle = json.loads(
        (ROOT / "tests/fixtures/value_stock_fcff/fcff_oracle_v1.json").read_text(
            encoding="utf-8"
        )
    )
    negatives = json.loads(
        (ROOT / "tests/fixtures/value_stock_fcff/fcff_negative_cases.json").read_text(
            encoding="utf-8"
        )
    )
    assert oracle["source_fixture"] == canonical_path
    assert negatives["base_fixture"] == canonical_path


@pytest.mark.parametrize("stem", ["real-fcff", "real-residual-income"])
def test_real_workflow_report_consumes_its_authoritative_receipt(stem: str) -> None:
    gateway = load_gateway()
    model_lock = load_fixture(WORKFLOW_PROOF / f"{stem}-model-lock.json")
    persisted_receipt = json.loads(
        (WORKFLOW_PROOF / f"{stem}-receipt.json").read_text(encoding="utf-8")
    )
    report = (WORKFLOW_PROOF / f"{stem}-report.md").read_text(encoding="utf-8")

    assert persisted_receipt == gateway.calculate_model_lock(model_lock)
    assert persisted_receipt["mechanical_status"] == "pass"
    assert persisted_receipt["input_identity"] in report
    assert persisted_receipt["versions"]["calculation_path"] in report
    assert persisted_receipt["calculation"]["per_share_value"] in report
    assert "Material arithmetic: receipt only; not manually reproduced." in report


def test_complete_cases_stay_separate_immutable_and_repeatable() -> None:
    gateway = load_gateway()
    base = load_fixture(FCFF_FIXTURE)
    alternate = copy.deepcopy(base)
    use_scenario(alternate, "alternate")
    before = copy.deepcopy([base, alternate])

    first = gateway.calculate_model_locks([base, alternate])
    repeated = gateway.calculate_model_locks([base, alternate])

    assert [base, alternate] == before
    assert repeated == first
    assert [receipt["normalized_input"]["base_scenario"] for receipt in first] == [
        "base",
        "alternate",
    ]
    assert first[0]["input_identity"] != first[1]["input_identity"]
    assert all(receipt["mechanical_status"] == "pass" for receipt in first)


@pytest.mark.parametrize(
    ("fixture", "input_id", "target", "lower", "upper", "solved"),
    [
        (FCFF_FIXTURE, "fcff_fy2027", "9.04636364", "60", "80", "70"),
        (RI_FIXTURE, "net_income_fy2026", "13.58772137", "130", "150", "140"),
    ],
)
def test_reverse_solve_reuses_each_method_without_mutating_the_model_lock(
    fixture: Path,
    input_id: str,
    target: str,
    lower: str,
    upper: str,
    solved: str,
) -> None:
    gateway = load_gateway()
    source = load_fixture(fixture)
    source["inputs"][input_id]["value"] = Decimal(lower)
    before = copy.deepcopy(source)
    base_receipt = gateway.calculate_model_lock(source)

    receipt = gateway.reverse_solve_model_lock(
        source,
        input_id=input_id,
        target_per_share=Decimal(target),
        lower_bound=Decimal(lower),
        upper_bound=Decimal(upper),
    )

    assert source == before
    assert receipt["mechanical_status"] == "pass"
    assert receipt["calculation"]["per_share_value"] == target
    base_input = copy.deepcopy(base_receipt["normalized_input"])
    solved_input = copy.deepcopy(receipt["normalized_input"])
    assert solved_input["inputs"][input_id]["value"] == solved
    solved_input["inputs"][input_id]["value"] = base_input["inputs"][input_id][
        "value"
    ]
    assert solved_input == base_input
    assert receipt["reverse_solve"] == {
        "status": "solved",
        "input_id": input_id,
        "target_output": "per_share_value",
        "target_value": target,
        "lower_bound": lower,
        "upper_bound": upper,
        "tolerance": "0.00000001",
        "solved_input_value": solved,
        "achieved_value": target,
        "iterations": 1,
        "residual_error": "0",
    }
    assert receipt["assertions"][-1]["status"] == "pass"


def test_reverse_solve_reports_an_unbracketed_target_as_failure() -> None:
    gateway = load_gateway()
    source = load_fixture(FCFF_FIXTURE)
    before = copy.deepcopy(source)

    receipt = gateway.reverse_solve_model_lock(
        source,
        input_id="fcff_fy2027",
        target_per_share=Decimal("100"),
        lower_bound=Decimal("60"),
        upper_bound=Decimal("80"),
    )

    assert source == before
    assert receipt["mechanical_status"] == "fail"
    assert "reverse_solve_no_solution" in {
        failure["code"] for failure in receipt["failures"]
    }
    assert receipt["reverse_solve"]["target_value"] == "100"
    assert receipt["reverse_solve"]["iterations"] == 0
    assert Decimal(receipt["reverse_solve"]["residual_error"]) != 0


def test_reverse_solve_is_independent_of_ambient_decimal_context() -> None:
    gateway = load_gateway()
    source = load_fixture(FCFF_FIXTURE)
    arguments = {
        "input_id": "fcff_fy2027",
        "target_per_share": Decimal("9.04636364"),
        "lower_bound": Decimal("60"),
        "upper_bound": Decimal("80"),
    }

    expected = gateway.reverse_solve_model_lock(source, **arguments)
    with localcontext() as context:
        context.prec = 6
        context.traps[Inexact] = True
        context.traps[Rounded] = True
        actual = gateway.reverse_solve_model_lock(source, **arguments)

    assert actual == expected


def test_objective_diagnostics_are_cross_method_and_repeatable() -> None:
    gateway = load_gateway()

    fcff = gateway.calculate_model_lock(load_fixture(FCFF_FIXTURE))
    residual_income = gateway.calculate_model_lock(load_fixture(RI_FIXTURE))

    assert fcff["diagnostics"] == {
        "discount_rate_growth_spread": "0.07",
        "oldest_dated_input_age_days": 0,
        "terminal_value_share": "0.88336192",
    }
    assert residual_income["diagnostics"] == {
        "discount_rate_growth_spread": "0.07",
        "oldest_dated_input_age_days": 0,
        "terminal_value_share": "0.21027388",
    }
    assert gateway.calculate_model_lock(load_fixture(FCFF_FIXTURE)) == fcff
    assert gateway.calculate_model_lock(load_fixture(RI_FIXTURE)) == residual_income


def test_cli_reverse_solve_emits_authoritative_json() -> None:
    completed = run_gateway(
        "calculate",
        FCFF_FIXTURE,
        "--reverse-input",
        "fcff_fy2027",
        "--target-per-share",
        "9.04636364",
        "--lower-bound",
        "60",
        "--upper-bound",
        "80",
    )

    assert completed.returncode == 0, completed.stderr
    receipt = json.loads(completed.stdout)
    assert receipt["mechanical_status"] == "pass"
    assert receipt["reverse_solve"]["status"] == "solved"
    assert receipt["calculation"]["per_share_value"] == "9.04636364"
