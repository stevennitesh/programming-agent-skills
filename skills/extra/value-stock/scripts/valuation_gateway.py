from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from datetime import date
from decimal import (
    MAX_EMAX,
    MIN_EMIN,
    ROUND_HALF_EVEN,
    Context,
    Decimal,
    DivisionByZero,
    InvalidOperation,
    Overflow,
    localcontext,
)
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker, validators


CALCULATOR_VERSION = "1.0.0"
GATEWAY_CONTRACT_VERSION = "model-lock-v1"
PATH_VERSIONS = {
    "fcff": "fcff-contract-v1",
    "residual_income": "residual-income-contract-v1",
}
CONTRACT = {
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
FCFF_ASSERTION_TOLERANCE = Decimal("0.00000001")
FCFF_OUTPUT_QUANTUM = Decimal("0.00000001")
FCFF_CONTEXT_PRECISION = 50
FCFF_DERIVED_FORMULA_REF = (
    "fcff-v1:nopat-plus-da-minus-capex-minus-working-capital-change"
)
FCFF_TERMINAL_FORMULA_REF = "fcff-v1:last-fcff-times-one-plus-growth"
FCFF_PATH_CONTRACT = {
    "arithmetic_precision_digits": FCFF_CONTEXT_PRECISION,
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
    "day_count": "actual_365",
    "forecast_rate_basis": "valuation_origin_spot",
    "derived_fcff_formula": FCFF_DERIVED_FORMULA_REF,
    "output_decimal_places": 8,
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
    "terminal_formula": FCFF_TERMINAL_FORMULA_REF,
}
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references/model-lock-v1.schema.json"
MODEL_LOCK_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _is_number(_checker: Any, instance: Any) -> bool:
    return isinstance(instance, (Decimal, int, float)) and not isinstance(instance, bool)


DecimalValidator = validators.extend(
    Draft202012Validator,
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine("number", _is_number),
)
MODEL_LOCK_VALIDATOR = DecimalValidator(
    MODEL_LOCK_SCHEMA,
    format_checker=FormatChecker(),
)


class DecimalSafeLoader(yaml.SafeLoader):
    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate key: {key}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _decimal_from_yaml(loader: DecimalSafeLoader, node: yaml.Node) -> Decimal:
    return Decimal(loader.construct_scalar(node).replace("_", ""))


DecimalSafeLoader.add_constructor(
    "tag:yaml.org,2002:int",
    _decimal_from_yaml,
)
DecimalSafeLoader.add_constructor(
    "tag:yaml.org,2002:float",
    _decimal_from_yaml,
)
DecimalSafeLoader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    lambda loader, node: loader.construct_scalar(node),
)


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_source(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(
            text,
            parse_int=Decimal,
            parse_float=Decimal,
            parse_constant=_reject_json_constant,
            object_pairs_hook=_unique_json_object,
        )
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.load(text, Loader=DecimalSafeLoader)
    raise ValueError(f"unsupported source format: {path.suffix or '<none>'}")


def _canonical_decimal(value: Decimal) -> str:
    if value == 0:
        return "0"
    rendered = format(value, "f")
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def normalize(value: Any) -> Any:
    if isinstance(value, Decimal):
        return _canonical_decimal(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return _canonical_decimal(Decimal(value))
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite number")
        return _canonical_decimal(Decimal(str(value)))
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _failure(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _path(parts: Any) -> str:
    return ".".join(str(part) for part in parts) or "$"


def _value_records(source: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    shares = source.get("diluted_shares")
    if isinstance(shares, dict):
        records.append(("diluted_shares", shares))
    inputs = source.get("inputs")
    if isinstance(inputs, dict):
        records.extend(
            (f"inputs.{name}", record)
            for name, record in inputs.items()
            if isinstance(record, dict)
        )
    return records


def _as_decimal(value: Any) -> Decimal | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    return None


def validate_model_lock(source: dict[str, Any]) -> list[dict[str, str]]:
    failures = [
        _failure("schema", _path(error.absolute_path), error.message)
        for error in sorted(
            MODEL_LOCK_VALIDATOR.iter_errors(source),
            key=lambda item: (_path(item.absolute_path), item.message),
        )
    ]

    scenarios_raw = source.get("scenarios")
    scenarios = {
        value for value in scenarios_raw if isinstance(value, str)
    } if isinstance(scenarios_raw, list) else set()
    if isinstance(scenarios_raw, list) and len(scenarios) != len(scenarios_raw):
        failures.append(_failure("scenario", "scenarios", "scenario ids must be unique strings"))
    base_scenario = source.get("base_scenario")
    if isinstance(base_scenario, str) and base_scenario not in scenarios:
        failures.append(_failure("scenario", "base_scenario", "base scenario is not declared"))

    periods_raw = source.get("periods")
    period_ids = {
        period.get("id")
        for period in periods_raw
        if isinstance(period, dict) and isinstance(period.get("id"), str)
    } if isinstance(periods_raw, list) else set()
    if isinstance(periods_raw, list) and len(period_ids) != len(periods_raw):
        failures.append(_failure("period", "periods", "period ids must be unique strings"))

    reporting_currency = source.get("reporting_currency")
    for record_path, record in _value_records(source):
        has_source = isinstance(record.get("source_ref"), str) and bool(record.get("source_ref"))
        has_formula = isinstance(record.get("formula_ref"), str) and bool(record.get("formula_ref"))
        if has_source == has_formula:
            failures.append(
                _failure(
                    "reference",
                    record_path,
                    "exactly one source_ref or formula_ref is required",
                )
            )

        number = _as_decimal(record.get("value"))
        if number is not None:
            if not number.is_finite():
                failures.append(_failure("finite", f"{record_path}.value", "value must be finite"))
            elif max(0, -number.as_tuple().exponent) > CONTRACT["max_decimal_places"]:
                failures.append(
                    _failure(
                        "precision",
                        f"{record_path}.value",
                        f"value exceeds {CONTRACT['max_decimal_places']} decimal places",
                    )
                )

        scenario = record.get("scenario")
        if isinstance(scenario, str) and scenario not in scenarios:
            failures.append(_failure("scenario", f"{record_path}.scenario", "scenario is not declared"))
        period = record.get("period")
        if isinstance(period, str) and period not in period_ids:
            failures.append(_failure("period", f"{record_path}.period", "period is not declared"))
        if (
            record.get("value_kind") == "monetary"
            and isinstance(record.get("currency"), str)
            and isinstance(reporting_currency, str)
            and record["currency"] != reporting_currency
        ):
            failures.append(
                _failure(
                    "currency",
                    f"{record_path}.currency",
                    "currency must match reporting_currency in gateway v1",
                )
            )

    shares = source.get("diluted_shares")
    if isinstance(shares, dict):
        shares_value = _as_decimal(shares.get("value"))
        if shares_value is not None and shares_value.is_finite() and shares_value <= 0:
            failures.append(
                _failure("positive", "diluted_shares.value", "diluted shares must be positive")
            )

    method = source.get("method")
    conventions = source.get("conventions")
    terminal = conventions.get("terminal") if isinstance(conventions, dict) else None
    allowed_terminals = (
        CONTRACT["supported_conventions"].get(method, {}).get("terminal", [])
        if isinstance(method, str)
        else []
    )
    if isinstance(method, str) and method in PATH_VERSIONS and terminal not in allowed_terminals:
        failures.append(
            _failure(
                "method_convention",
                "conventions.terminal",
                f"terminal convention is not supported for {method}",
            )
        )

    unique = {
        (failure["code"], failure["path"], failure["message"]): failure
        for failure in failures
    }
    return [unique[key] for key in sorted(unique)]


def _versions(method: Any) -> dict[str, Any]:
    return {
        "calculator": CALCULATOR_VERSION,
        "gateway_contract": GATEWAY_CONTRACT_VERSION,
        "calculation_path": PATH_VERSIONS.get(method) if isinstance(method, str) else None,
    }


def _failure_receipt(source: dict[str, Any], failures: list[dict[str, str]]) -> dict[str, Any]:
    method = source.get("method")
    return {
        "mechanical_status": "fail",
        "run_id": source["run_id"],
        "method": method if isinstance(method, str) else None,
        "versions": _versions(method),
        "contract": copy.deepcopy(CONTRACT),
        "failures": failures,
        "assertions": [{"id": "model_lock_valid", "status": "fail"}],
        "warnings": [],
    }


def validate_normalized_model_lock(source: dict[str, Any]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for record_path, record in _value_records(source):
        value = record.get("value")
        try:
            decimal_value = Decimal(value) if isinstance(value, str) else None
        except ArithmeticError:
            decimal_value = None
        if (
            decimal_value is None
            or not decimal_value.is_finite()
            or _canonical_decimal(decimal_value) != value
        ):
            failures.append(
                _failure(
                    "normalized_numeric",
                    f"{record_path}.value",
                    "normalized value must be a finite canonical decimal string",
                )
            )
    return failures


def build_receipt(source: Any) -> dict[str, Any]:
    normalized = normalize(source)
    normalized_failures = validate_normalized_model_lock(normalized)
    if normalized_failures:
        return _failure_receipt(source, normalized_failures)
    method = normalized["method"]
    identity = hashlib.sha256(canonical_json(normalized).encode("utf-8")).hexdigest()
    return {
        "mechanical_status": "pass",
        "run_id": normalized["run_id"],
        "method": method,
        "input_identity": f"sha256:{identity}",
        "versions": _versions(method),
        "contract": copy.deepcopy(CONTRACT),
        "normalized_input": normalized,
        "assertions": [
            {"id": "model_lock_source_valid", "status": "pass"},
            {"id": "model_lock_normalized_valid", "status": "pass"},
        ],
        "warnings": [],
    }


def process_model_lock(source: Any) -> dict[str, Any]:
    if not isinstance(source, dict) or not isinstance(source.get("run_id"), str) or not source["run_id"]:
        raise ValueError("input has no stable run_id")
    failures = validate_model_lock(source)
    if failures:
        return _failure_receipt(source, failures)
    return build_receipt(source)


def _input_decimal(source: dict[str, Any], input_id: str) -> Decimal:
    return Decimal(source["inputs"][input_id]["value"])


def _fcff_decimal_context(precision: int = FCFF_CONTEXT_PRECISION) -> Context:
    context = Context(
        prec=precision,
        rounding=ROUND_HALF_EVEN,
        Emin=MIN_EMIN,
        Emax=MAX_EMAX,
        capitals=1,
        clamp=0,
    )
    context.clear_traps()
    for signal in (InvalidOperation, DivisionByZero, Overflow):
        context.traps[signal] = True
    return context


def _receipt_decimal(value: Decimal) -> str:
    integer_digits = max(1, value.adjusted() + 1) if value else 1
    with localcontext(
        _fcff_decimal_context(
            max(
            FCFF_CONTEXT_PRECISION,
            integer_digits + abs(FCFF_OUTPUT_QUANTUM.as_tuple().exponent) + 5,
            )
        )
    ):
        rounded = value.quantize(FCFF_OUTPUT_QUANTUM)
    return _canonical_decimal(rounded)


def _sum_inputs(source: dict[str, Any], input_ids: list[str]) -> Decimal:
    return sum((_input_decimal(source, input_id) for input_id in input_ids), Decimal(0))


def _calculation_failure_receipt(
    receipt: dict[str, Any],
    failures: list[dict[str, str]],
) -> dict[str, Any]:
    result = copy.deepcopy(receipt)
    result["mechanical_status"] = "fail"
    unique = {
        (failure["code"], failure["path"], failure["message"]): failure
        for failure in failures
    }
    result["failures"] = [unique[key] for key in sorted(unique)]
    result["assertions"].append({"id": "fcff_calculation_valid", "status": "fail"})
    result.pop("calculation", None)
    return result


def _fcff_input(
    source: dict[str, Any],
    input_id: Any,
    path: str,
    failures: list[dict[str, str]],
    *,
    unit: str,
    claim_basis: str,
    period: str | None = None,
    record_date: str | None = None,
    nonnegative: bool = False,
) -> dict[str, Any] | None:
    inputs = source["inputs"]
    if not isinstance(input_id, str) or input_id not in inputs:
        failures.append(_failure("input_reference", path, "referenced input does not exist"))
        return None
    record = inputs[input_id]
    if record.get("unit") != unit:
        failures.append(_failure("method_unit", path, f"input must use unit {unit}"))
    if record.get("claim_basis") != claim_basis:
        failures.append(
            _failure("claim_basis", path, f"input must use claim basis {claim_basis}")
        )
    if unit == "currency":
        if (
            record.get("value_kind") != "monetary"
            or record.get("currency") != source["reporting_currency"]
        ):
            failures.append(
                _failure(
                    "method_currency",
                    path,
                    "monetary input must use the reporting currency",
                )
            )
    elif record.get("value_kind") != "non_monetary" or record.get("currency") is not None:
        failures.append(
            _failure("method_unit", path, "ratio input must be non-monetary")
        )
    if record.get("scenario") != source["base_scenario"]:
        failures.append(_failure("scenario", path, "input must belong to the base scenario"))
    if period is not None and record.get("period") != period:
        failures.append(_failure("fcff_period", path, f"input must belong to {period}"))
    if record_date is not None and record.get("date") != record_date:
        failures.append(_failure("claim_timing", path, f"input date must be {record_date}"))
    if nonnegative and Decimal(record["value"]) < 0:
        failures.append(_failure("claim_sign", path, "claim-bridge amounts must be nonnegative"))
    if len(Decimal(record["value"]).as_tuple().digits) > FCFF_CONTEXT_PRECISION:
        failures.append(
            _failure(
                "calculation_precision",
                path,
                f"input exceeds {FCFF_CONTEXT_PRECISION} significant digits",
            )
        )
    return record


def _next_year(value: date) -> date:
    try:
        return value.replace(year=value.year + 1)
    except ValueError:
        return value.replace(year=value.year + 1, day=28)


def validate_fcff_calculation(source: dict[str, Any]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    config = source.get("fcff")
    if not isinstance(config, dict):
        return [_failure("fcff_required", "fcff", "FCFF calculation data is required")]

    as_of = date.fromisoformat(source["as_of_date"])
    period_rows = {
        row["id"]: row
        for row in source["periods"]
        if isinstance(row, dict) and row.get("kind") == "forecast"
    }
    forecast_periods = config["forecast_periods"]
    configured_ids = [row["period"] for row in forecast_periods]
    if len(set(configured_ids)) != len(configured_ids) or set(configured_ids) != set(period_rows):
        failures.append(
            _failure(
                "forecast_coverage",
                "fcff.forecast_periods",
                "every declared forecast period must be modeled exactly once",
            )
        )

    timing = source["conventions"]["timing"]
    prior_realization: date | None = None
    first_prior_period_end = config["discounting"].get(
        "midyear_first_prior_period_end"
    )
    prior_period_end: date | None = None
    if timing == "midyear":
        if isinstance(first_prior_period_end, str):
            prior_period_end = date.fromisoformat(first_prior_period_end)
            if prior_period_end > as_of:
                failures.append(
                    _failure(
                        "timing_convention",
                        "fcff.discounting.midyear_first_prior_period_end",
                        "the preceding period end cannot follow the valuation date",
                    )
                )
        else:
            failures.append(
                _failure(
                    "timing_convention",
                    "fcff.discounting.midyear_first_prior_period_end",
                    "midyear timing requires the preceding period end",
                )
            )
    elif first_prior_period_end is not None:
        failures.append(
            _failure(
                "timing_convention",
                "fcff.discounting.midyear_first_prior_period_end",
                "the preceding period end is only used for midyear timing",
            )
        )
    calculated_fcff: list[Decimal | None] = []
    for index, row in enumerate(forecast_periods):
        row_path = f"fcff.forecast_periods.{index}"
        period_id = row["period"]
        realization = date.fromisoformat(row["realization_date"])
        if realization <= as_of:
            failures.append(
                _failure("timing_elapsed", f"{row_path}.realization_date", "cash flow has elapsed")
            )
        if prior_realization is not None and realization <= prior_realization:
            failures.append(
                _failure(
                    "timing_convention",
                    f"{row_path}.realization_date",
                    "forecast realization dates must increase",
                )
            )
        prior_realization = realization
        period_row = period_rows.get(period_id)
        if (
            timing == "year_end"
            and period_row is not None
            and row["realization_date"] != period_row["date"]
        ):
            failures.append(
                _failure(
                    "timing_convention",
                    f"{row_path}.realization_date",
                    "year-end cash flow must use the declared period end date",
                )
            )
        if timing == "midyear" and period_row is not None and prior_period_end is not None:
            period_end = date.fromisoformat(period_row["date"])
            if period_end <= prior_period_end:
                failures.append(
                    _failure(
                        "timing_convention",
                        f"{row_path}.period",
                        "midyear period ends must increase",
                    )
                )
            else:
                midpoint = prior_period_end + (period_end - prior_period_end) // 2
                if realization != midpoint:
                    failures.append(
                        _failure(
                            "timing_convention",
                            f"{row_path}.realization_date",
                            "midyear cash flow must use the midpoint between period ends",
                        )
                    )
            prior_period_end = period_end

        output = _fcff_input(
            source,
            row["output_input"],
            f"{row_path}.output_input",
            failures,
            unit="currency",
            claim_basis="enterprise",
            period=period_id,
        )
        rate = _fcff_input(
            source,
            row["discount_rate_input"],
            f"{row_path}.discount_rate_input",
            failures,
            unit="ratio",
            claim_basis="enterprise",
            period=period_id,
        )
        if rate is not None and Decimal(rate["value"]) <= -1:
            failures.append(
                _failure("discount_rate", f"{row_path}.discount_rate_input", "rate must exceed -1")
            )

        computed: Decimal | None = None
        if row["branch"] == "derived":
            components = row["components"]
            component_ids = list(components.values())
            if len(component_ids) != len(set(component_ids)):
                failures.append(
                    _failure(
                        "derived_component_duplicate",
                        f"{row_path}.components",
                        "derived FCFF component inputs must be distinct",
                    )
                )
            component_specs = {
                "ebit": ("currency", "operating"),
                "tax_rate": ("ratio", "operating"),
                "depreciation_amortization": ("currency", "operating"),
                "capital_expenditures": ("currency", "operating"),
                "working_capital_change": ("currency", "operating"),
            }
            records = {
                role: _fcff_input(
                    source,
                    components[role],
                    f"{row_path}.components.{role}",
                    failures,
                    unit=spec[0],
                    claim_basis=spec[1],
                    period=period_id,
                )
                for role, spec in component_specs.items()
            }
            if output is not None and output.get("formula_ref") != FCFF_DERIVED_FORMULA_REF:
                failures.append(
                    _failure(
                        "fcff_formula",
                        f"{row_path}.output_input",
                        "derived FCFF must retain the registered formula reference",
                    )
                )
            if all(record is not None for record in records.values()):
                computed = (
                    Decimal(records["ebit"]["value"])
                    * (Decimal(1) - Decimal(records["tax_rate"]["value"]))
                    + Decimal(records["depreciation_amortization"]["value"])
                    - Decimal(records["capital_expenditures"]["value"])
                    - Decimal(records["working_capital_change"]["value"])
                )
                if (
                    output is not None
                    and abs(computed - Decimal(output["value"])) > FCFF_ASSERTION_TOLERANCE
                ):
                    failures.append(
                        _failure(
                            "fcff_identity",
                            f"{row_path}.output_input",
                            "derived FCFF does not match the registered identity",
                        )
                    )
        elif output is not None:
            computed = Decimal(output["value"])
            if "source_ref" not in output:
                failures.append(
                    _failure(
                        "fcff_formula",
                        f"{row_path}.output_input",
                        "direct FCFF must retain source lineage",
                    )
                )
        calculated_fcff.append(computed)

    terminal = config["terminal"]
    convention = source["conventions"]["terminal"]
    if convention == "none" and terminal is not None:
        failures.append(_failure("terminal_convention", "fcff.terminal", "terminal must be null"))
    if convention == "perpetual_growth" and terminal is None:
        failures.append(
            _failure("terminal_convention", "fcff.terminal", "perpetual terminal is required")
        )
    if terminal is not None:
        terminal_date = date.fromisoformat(terminal["terminal_date"])
        next_period_date = date.fromisoformat(terminal["next_period_date"])
        if terminal_date <= as_of:
            failures.append(
                _failure(
                    "terminal_timing",
                    "fcff.terminal.terminal_date",
                    "terminal date must follow the valuation date",
                )
            )
        if prior_realization is not None and terminal_date < prior_realization:
            failures.append(
                _failure(
                    "terminal_timing",
                    "fcff.terminal.terminal_date",
                    "terminal date must not precede the final forecast realization",
                )
            )
        last_period = period_rows.get(forecast_periods[-1]["period"])
        if last_period is None or terminal["terminal_date"] != last_period["date"]:
            failures.append(
                _failure(
                    "terminal_timing",
                    "fcff.terminal.terminal_date",
                    "terminal date must equal the final forecast period end",
                )
            )
        if next_period_date != _next_year(terminal_date):
            failures.append(
                _failure(
                    "terminal_timing",
                    "fcff.terminal.next_period_date",
                    "terminal numerator must be dated one interval after terminal date",
                )
            )
        next_fcff = _fcff_input(
            source,
            terminal["next_period_fcff_input"],
            "fcff.terminal.next_period_fcff_input",
            failures,
            unit="currency",
            claim_basis="enterprise",
            record_date=terminal["next_period_date"],
        )
        terminal_wacc = _fcff_input(
            source,
            terminal["discount_rate_input"],
            "fcff.terminal.discount_rate_input",
            failures,
            unit="ratio",
            claim_basis="enterprise",
            record_date=terminal["terminal_date"],
        )
        growth = _fcff_input(
            source,
            terminal["growth_rate_input"],
            "fcff.terminal.growth_rate_input",
            failures,
            unit="ratio",
            claim_basis="enterprise",
            record_date=terminal["terminal_date"],
        )
        if terminal_wacc is not None and growth is not None:
            wacc_value = Decimal(terminal_wacc["value"])
            growth_value = Decimal(growth["value"])
            if wacc_value <= growth_value:
                failures.append(
                    _failure(
                        "terminal_spread",
                        "fcff.terminal",
                        "terminal WACC must exceed growth",
                    )
                )
            if wacc_value <= -1:
                failures.append(
                    _failure("discount_rate", "fcff.terminal", "terminal WACC must exceed -1")
                )
            if (
                next_fcff is not None
                and calculated_fcff
                and calculated_fcff[-1] is not None
                and abs(
                    Decimal(next_fcff["value"])
                    - calculated_fcff[-1] * (Decimal(1) + growth_value)
                )
                > FCFF_ASSERTION_TOLERANCE
            ):
                failures.append(
                    _failure(
                        "terminal_fcff_identity",
                        "fcff.terminal.next_period_fcff_input",
                        "terminal FCFF does not match last FCFF grown one interval",
                    )
                )
        if next_fcff is not None and next_fcff.get("formula_ref") != FCFF_TERMINAL_FORMULA_REF:
            failures.append(
                _failure(
                    "fcff_formula",
                    "fcff.terminal.next_period_fcff_input",
                    "terminal FCFF must retain the registered formula reference",
                )
            )

    bridge = config["claim_bridge"]
    bridge_claims = {
        "excess_cash": "common_equity",
        "non_operating_assets": "common_equity",
        "debt": "debt",
        "preferred_stock": "preferred",
        "noncontrolling_interests": "noncontrolling_interest",
        "other_senior_claims": "other",
        "existing_awards": "target_security",
    }
    seen_bridge_inputs: set[str] = set()
    for category, claim_basis in bridge_claims.items():
        for position, input_id in enumerate(bridge[category]):
            if input_id in seen_bridge_inputs:
                failures.append(
                    _failure(
                        "bridge_duplicate",
                        f"fcff.claim_bridge.{category}.{position}",
                        "claim-bridge input is counted more than once",
                    )
                )
            seen_bridge_inputs.add(input_id)
            _fcff_input(
                source,
                input_id,
                f"fcff.claim_bridge.{category}.{position}",
                failures,
                unit="currency",
                claim_basis=claim_basis,
                record_date=source["as_of_date"],
                nonnegative=True,
            )
    target_adjustment_effects: dict[str, str] = {}
    for position, item in enumerate(bridge["target_claim_adjustments"]):
        input_id = item["input"]
        target_adjustment_effects[input_id] = item["effect"]
        if input_id in seen_bridge_inputs:
            failures.append(
                _failure(
                    "bridge_duplicate",
                    f"fcff.claim_bridge.target_claim_adjustments.{position}",
                    "claim-bridge input is counted more than once",
                )
            )
        seen_bridge_inputs.add(input_id)
        _fcff_input(
            source,
            input_id,
            f"fcff.claim_bridge.target_claim_adjustments.{position}.input",
            failures,
            unit="currency",
            claim_basis="target_security",
            record_date=source["as_of_date"],
            nonnegative=True,
        )

    bridge_claim_bases = set(bridge_claims.values())
    for input_id, record in source["inputs"].items():
        is_material_bridge_input = (
            record.get("unit") == "currency"
            and record.get("value_kind") == "monetary"
            and record.get("currency") == source["reporting_currency"]
            and record.get("date") == source["as_of_date"]
            and record.get("scenario") == source["base_scenario"]
            and record.get("claim_basis") in bridge_claim_bases
            and Decimal(record["value"]) != 0
        )
        if is_material_bridge_input and input_id not in seen_bridge_inputs:
            failures.append(
                _failure(
                    "bridge_incomplete",
                    "fcff.claim_bridge",
                    f"material claim-bridge input {input_id} is not applied",
                )
            )

    award_treatment = config["award_treatment"]
    existing_awards = bridge["existing_awards"]
    if (
        (award_treatment["existing_awards"] == "claim_bridge" and not existing_awards)
        or (award_treatment["existing_awards"] != "claim_bridge" and existing_awards)
    ):
        failures.append(
            _failure(
                "award_double_count",
                "fcff.award_treatment.existing_awards",
                "existing awards must use exactly one declared treatment",
            )
        )
    future_grants = award_treatment["future_grants"]
    future_claim = award_treatment["future_grants_claim_adjustment"]
    if (
        future_grants == "future_dilution"
        and (
            not isinstance(future_claim, str)
            or target_adjustment_effects.get(future_claim) != "subtract"
        )
    ) or (future_grants != "future_dilution" and future_claim is not None):
        failures.append(
            _failure(
                "future_grants_claim",
                "fcff.award_treatment.future_grants_claim_adjustment",
                "future dilution must map exactly once to a target-claim adjustment",
            )
        )

    shares = source["diluted_shares"]
    if shares.get("scenario") != source["base_scenario"]:
        failures.append(
            _failure(
                "share_scenario",
                "diluted_shares.scenario",
                "diluted shares must belong to the base scenario",
            )
        )
    if shares.get("date") != source["as_of_date"]:
        failures.append(
            _failure(
                "share_timing",
                "diluted_shares.date",
                "diluted shares must be point-in-time at the valuation date",
            )
        )
    if len(Decimal(shares["value"]).as_tuple().digits) > FCFF_CONTEXT_PRECISION:
        failures.append(
            _failure(
                "calculation_precision",
                "diluted_shares.value",
                f"input exceeds {FCFF_CONTEXT_PRECISION} significant digits",
            )
        )
    unique = {
        (failure["code"], failure["path"], failure["message"]): failure
        for failure in failures
    }
    return [unique[key] for key in sorted(unique)]


def _calculate_fcff(source: dict[str, Any]) -> dict[str, Any]:
    config = source["fcff"]
    as_of = date.fromisoformat(source["as_of_date"])
    forecast_results: list[dict[str, str]] = []
    forecast_present_values: list[Decimal] = []

    with localcontext(_fcff_decimal_context()):
        last_fcff: Decimal | None = None
        for period in config["forecast_periods"]:
            output_record = source["inputs"][period["output_input"]]
            output_value = _input_decimal(source, period["output_input"])
            if period["branch"] == "derived":
                components = period["components"]
                ebit = _input_decimal(source, components["ebit"])
                tax_rate = _input_decimal(source, components["tax_rate"])
                depreciation = _input_decimal(
                    source,
                    components["depreciation_amortization"],
                )
                capital_expenditures = _input_decimal(
                    source,
                    components["capital_expenditures"],
                )
                working_capital_change = _input_decimal(
                    source,
                    components["working_capital_change"],
                )
                fcff = (
                    ebit * (Decimal(1) - tax_rate)
                    + depreciation
                    - capital_expenditures
                    - working_capital_change
                )
            else:
                fcff = output_value
            last_fcff = fcff

            realization_date = date.fromisoformat(period["realization_date"])
            exponent = Decimal((realization_date - as_of).days) / Decimal(365)
            discount_rate = _input_decimal(source, period["discount_rate_input"])
            discount_factor = Decimal(1) / ((Decimal(1) + discount_rate) ** exponent)
            present_value = fcff * discount_factor
            forecast_present_values.append(present_value)
            forecast_results.append(
                {
                    "period": period["period"],
                    "realization_date": period["realization_date"],
                    "branch": period["branch"],
                    "output_input": period["output_input"],
                    "lineage": {
                        "kind": "formula" if "formula_ref" in output_record else "source",
                        "ref": output_record.get("formula_ref", output_record.get("source_ref")),
                    },
                    "fcff": _receipt_decimal(fcff),
                    "discount_rate_input": period["discount_rate_input"],
                    "discount_rate": _receipt_decimal(discount_rate),
                    "discount_exponent": _receipt_decimal(exponent),
                    "discount_factor": _receipt_decimal(discount_factor),
                    "present_value": _receipt_decimal(present_value),
                }
            )

        terminal_result: dict[str, str] | None = None
        terminal_present_value = Decimal(0)
        terminal = config["terminal"]
        if terminal is not None:
            next_period_record = source["inputs"][terminal["next_period_fcff_input"]]
            terminal_wacc = _input_decimal(source, terminal["discount_rate_input"])
            growth_rate = _input_decimal(source, terminal["growth_rate_input"])
            assert last_fcff is not None
            next_period_fcff = last_fcff * (Decimal(1) + growth_rate)
            terminal_value = next_period_fcff / (terminal_wacc - growth_rate)
            terminal_date = date.fromisoformat(terminal["terminal_date"])
            terminal_exponent = Decimal((terminal_date - as_of).days) / Decimal(365)
            terminal_discount_factor = Decimal(1) / (
                (Decimal(1) + terminal_wacc) ** terminal_exponent
            )
            terminal_present_value = terminal_value * terminal_discount_factor
            terminal_result = {
                "terminal_date": terminal["terminal_date"],
                "next_period_date": terminal["next_period_date"],
                "next_period_fcff_input": terminal["next_period_fcff_input"],
                "formula_ref": next_period_record["formula_ref"],
                "next_period_fcff": _receipt_decimal(next_period_fcff),
                "discount_rate_input": terminal["discount_rate_input"],
                "growth_rate_input": terminal["growth_rate_input"],
                "wacc": _receipt_decimal(terminal_wacc),
                "growth_rate": _receipt_decimal(growth_rate),
                "terminal_value": _receipt_decimal(terminal_value),
                "discount_exponent": _receipt_decimal(terminal_exponent),
                "discount_factor": _receipt_decimal(terminal_discount_factor),
                "present_value": _receipt_decimal(terminal_present_value),
            }

        enterprise_value = sum(forecast_present_values, Decimal(0)) + terminal_present_value
        bridge = config["claim_bridge"]
        bridge_categories = {
            category: _sum_inputs(source, bridge[category])
            for category in (
                "excess_cash",
                "non_operating_assets",
                "debt",
                "preferred_stock",
                "noncontrolling_interests",
                "other_senior_claims",
                "existing_awards",
            )
        }
        additive_assets = (
            bridge_categories["excess_cash"] + bridge_categories["non_operating_assets"]
        )
        senior_claims = (
            bridge_categories["debt"]
            + bridge_categories["preferred_stock"]
            + bridge_categories["noncontrolling_interests"]
            + bridge_categories["other_senior_claims"]
        )
        common_equity_pool = enterprise_value + additive_assets - senior_claims
        existing_awards = bridge_categories["existing_awards"]
        target_adjustments = sum(
            (
                _input_decimal(source, item["input"])
                if item["effect"] == "add"
                else -_input_decimal(source, item["input"])
                for item in bridge["target_claim_adjustments"]
            ),
            Decimal(0),
        )
        target_common_equity = common_equity_pool - existing_awards + target_adjustments
        diluted_shares = Decimal(source["diluted_shares"]["value"])
        per_share_value = target_common_equity / diluted_shares

    return {
        "forecast_periods": forecast_results,
        "terminal": terminal_result,
        "enterprise_value": _receipt_decimal(enterprise_value),
        "claim_bridge": {
            "categories": {
                category: _receipt_decimal(value)
                for category, value in bridge_categories.items()
            },
            "excess_cash_and_non_operating_assets": _receipt_decimal(additive_assets),
            "senior_and_excluded_claims": _receipt_decimal(senior_claims),
            "common_equity_pool": _receipt_decimal(common_equity_pool),
            "existing_awards": _receipt_decimal(existing_awards),
            "target_claim_adjustments": _receipt_decimal(target_adjustments),
            "target_common_equity": _receipt_decimal(target_common_equity),
        },
        "diluted_shares": _receipt_decimal(diluted_shares),
        "per_share_value": _receipt_decimal(per_share_value),
    }


def calculate_model_lock(source: Any) -> dict[str, Any]:
    receipt = process_model_lock(source)
    if receipt["mechanical_status"] == "fail":
        return receipt
    if receipt["method"] != "fcff":
        return _calculation_failure_receipt(
            receipt,
            [_failure("unsupported_method", "method", "calculation path is not implemented")],
        )
    receipt["path_contract"] = copy.deepcopy(FCFF_PATH_CONTRACT)
    with localcontext(_fcff_decimal_context()):
        failures = validate_fcff_calculation(receipt["normalized_input"])
        if failures:
            return _calculation_failure_receipt(receipt, failures)
        result = copy.deepcopy(receipt)
        result["calculation"] = _calculate_fcff(result["normalized_input"])
    result["assertions"].append({"id": "fcff_calculation_valid", "status": "pass"})
    return result


def render_receipt_json(receipt: dict[str, Any]) -> str:
    return json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def render_receipt_markdown(receipt: dict[str, Any]) -> str:
    return (
        "# Calculation Receipt\n\n"
        f"- mechanical_status: `{receipt['mechanical_status']}`\n"
        f"- run_id: `{receipt['run_id']}`\n"
        f"- method: `{receipt.get('method')}`\n\n"
        "```json\n"
        f"{render_receipt_json(receipt).rstrip()}\n"
        "```\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a valuation Model Lock.")
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output-format",
        choices=("json", "markdown"),
        default="json",
    )
    parser.add_argument(
        "--calculate",
        action="store_true",
        help="execute the selected supported calculation path after validation",
    )
    args = parser.parse_args(argv)
    try:
        source = load_source(args.input)
        receipt = calculate_model_lock(source) if args.calculate else process_model_lock(source)
    except (OSError, ValueError, ArithmeticError, yaml.YAMLError) as error:
        sys.stderr.write(f"model-lock input error: {error}\n")
        return 3
    renderer = render_receipt_json if args.output_format == "json" else render_receipt_markdown
    sys.stdout.write(renderer(receipt))
    return 0 if receipt["mechanical_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
