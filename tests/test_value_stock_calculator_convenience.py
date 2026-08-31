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
    / "skills/extra/value-stock/examples/residual-income-model-lock.json"
)
SKILL = ROOT / "skills/extra/value-stock/SKILL.md"
RUNBOOK = ROOT / "skills/extra/value-stock/references/analyst-runbook.md"
METHODS = ROOT / "skills/extra/value-stock/references/valuation-methods.md"
COMPACT_REPORT = ROOT / "skills/extra/value-stock/references/compact-report.md"
FULL_REPORT = ROOT / "skills/extra/value-stock/references/report-contract.md"
MARKET_CONTEXT = ROOT / "skills/extra/value-stock/references/market-context.md"
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
    residual_income_run = run_gateway("calculate", RI_FIXTURE)

    assert help_run.returncode == 0
    assert "validate INPUT" in help_run.stdout
    assert "calculate INPUT" in help_run.stdout
    assert (
        "python skills/extra/value-stock/scripts/valuation_gateway.py calculate "
        "skills/extra/value-stock/examples/fcff-model-lock.json" in help_run.stdout
    )
    assert validate_run.returncode == 0, validate_run.stderr
    assert "calculation" not in json.loads(validate_run.stdout)
    assert calculate_run.returncode == 0, calculate_run.stderr
    assert json.loads(calculate_run.stdout)["calculation"]["per_share_value"]
    assert residual_income_run.returncode == 0, residual_income_run.stderr
    assert json.loads(residual_income_run.stdout)["method"] == "residual_income"


def test_skill_routes_operations_to_conditional_references_and_calculators() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    methods = METHODS.read_text(encoding="utf-8")
    normalized_skill = " ".join(skill.split())
    normalized_runbook = " ".join(runbook.split())
    normalized_runbook_lower = normalized_runbook.lower()

    assert skill.count("[analyst-runbook.md](references/analyst-runbook.md)") == 1
    assert skill.count("[market-context.md](references/market-context.md)") == 1
    assert "completely at the start of every valuation run" not in skill
    assert (
        "Do not preload the whole runbook or a branch-only reference"
        in normalized_skill
    )
    assert (
        "Resolve capability for the requested calculator operation" in normalized_skill
    )
    assert (
        "caller-owned path takes precedence over the bundled fallback"
        in normalized_skill
    )
    assert runbook.count("## 3. Forecast, Freeze, And Calculate") == 1
    assert "[FCFF example](../examples/fcff-model-lock.json)" in runbook
    assert (
        "[residual-income example](../examples/residual-income-model-lock.json)"
        in runbook
    )
    assert "[valuation-methods.md](valuation-methods.md)" in runbook
    assert runbook.count("### Conditional Research Resolution") == 1
    assert normalized_runbook.count("caller declares a valuation research catalog") == 1
    assert (
        "a catalog row cannot satisfy a model lock requirement"
        in normalized_runbook_lower
    )
    assert "### Independent Review" in runbook
    assert "### Run Feedback" in runbook
    assert "If a caller-owned path exists, use only it" in normalized_runbook
    assert "Never use both paths for one material result" in normalized_runbook
    assert (
        "do not invent a command or manual parallel calculation" in normalized_runbook
    )
    assert "[bundled valuation gateway](../scripts/valuation_gateway.py)" in runbook
    assert "[compact-report.md](compact-report.md) for Compact" in normalized_runbook
    assert "[report-contract.md](report-contract.md) for Full" in normalized_runbook
    assert "`mechanical_status: fail` excludes the affected result" in skill
    assert "capability gap with an exact unlock condition" in normalized_runbook
    normalized_methods = " ".join(methods.split())
    assert (
        "receipt supplies the deterministic arithmetic and assertions represented "
        "by the selected typed calculation path" in normalized_methods
    )

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


def test_market_context_package_routes_three_request_shapes_without_manual_arithmetic() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    methods = METHODS.read_text(encoding="utf-8")
    compact = COMPACT_REPORT.read_text(encoding="utf-8")
    full = FULL_REPORT.read_text(encoding="utf-8")
    market = MARKET_CONTEXT.read_text(encoding="utf-8")
    normalized_market = " ".join(market.split())

    assert "| Price-dependent intrinsic valuation | `required` |" in market
    assert "| Explicit relative valuation | `required` |" in market
    assert "| Intrinsic valuation without price | `not_requested` |" in market
    assert "market_context_scope" in runbook
    assert "not_requested" in runbook
    assert "do not collect it" in skill

    selection_position = market.index("seal_selection_evidence_pack()")
    outcome_position = market.index("seal_market_context_evidence_pack()")
    calculation_position = market.index("Send the frozen lock through the public")
    assert selection_position < outcome_position < calculation_position

    lanes = (
        "own_history",
        "competitive_peers",
        "economic_peers",
        "industry",
        "broad_market",
    )
    for lane in lanes:
        assert f"`{lane}`" in market
        assert f"`{lane}`" in skill
    assert "forward P/E =" not in methods
    assert "PEG =" not in methods
    assert "Do not calculate it in the report" in full
    assert "Do not calculate or infer a missing value" in compact

    for report_contract in (compact, full):
        assert "QualityVsPriceAssessment" in report_contract
        assert "up to three supported thesis breakers" in report_contract
        assert "market-context.md" in report_contract

    assert "does not reduce a supported intrinsic result" in normalized_market
    assert "user requested it" in normalized_market
    assert "declared it load-bearing" in normalized_market


def test_interactive_verdict_stops_before_publication_and_redundant_audit() -> None:
    skill = " ".join(SKILL.read_text(encoding="utf-8").split())
    runbook = " ".join(RUNBOOK.read_text(encoding="utf-8").split())

    assert "Use verdict mode by default" in skill
    assert "Do not persist, construct a manifest, audit" in skill
    assert "Enter publication mode only when the user asks" in skill
    assert "Runtime availability alone is not a reason to run it" in skill
    assert "Present the report in verdict mode and stop" in runbook
    assert "`persist_run()` already performs the staged audit" in runbook
    assert "The checklist does not require persistence" in runbook


def test_runbook_resolves_capability_before_dependent_work_and_preserves_catalog_states() -> None:
    runbook = RUNBOOK.read_text(encoding="utf-8")
    method_position = runbook.index("### Method Disposition")
    capability_position = runbook.index("### Operation Capability Resolution")
    evidence_position = runbook.index("### Selected Evidence And Gates")

    assert method_position < capability_position < evidence_position
    capability = runbook[capability_position:evidence_position]
    for field in (
        "caller owner",
        "selected method",
        "exact requested operation",
        "public interface",
        "contract and version",
        "capability state",
        "unlock condition",
    ):
        assert field in capability
    assert "Capability does not choose method fit" in capability

    research = runbook[
        runbook.index("### Conditional Research Resolution") : runbook.index(
            "### Forward P/E Or PEG"
        )
    ]
    rows = {
        columns[0]: columns[1]
        for line in research.splitlines()
        if line.startswith("| `")
        and len(columns := [part.strip() for part in line.strip("|").split("|")]) == 2
    }
    assert set(rows) == {"`no_match`", "`blocked`", "`stale`", "`conflict`", "`ambiguous`"}
    assert "$research" in rows["`no_match`"]
    assert all("$research" not in action for state, action in rows.items() if state != "`no_match`")


def test_return_contracts_scope_reverse_as_an_adjunct_and_reuse_selected_sections() -> None:
    for path in (COMPACT_REPORT, FULL_REPORT):
        contract = " ".join(path.read_text(encoding="utf-8").split())
        assert "only when the selected intrinsic spine declares a compatible operation" in contract
        assert "separate adjunct capability gap" in contract
        assert "does not downgrade an otherwise complete intrinsic result" in contract
        assert "Apply only the source and method sections already selected by the runbook" in contract
        assert "Do not reload either whole reference" in contract


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
