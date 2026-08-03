from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from datetime import date
from decimal import Decimal
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
    args = parser.parse_args(argv)
    try:
        source = load_source(args.input)
        receipt = process_model_lock(source)
    except (OSError, ValueError, ArithmeticError, yaml.YAMLError) as error:
        sys.stderr.write(f"model-lock input error: {error}\n")
        return 3
    renderer = render_receipt_json if args.output_format == "json" else render_receipt_markdown
    sys.stdout.write(renderer(receipt))
    return 0 if receipt["mechanical_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
