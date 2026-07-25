"""Verify frozen deploy-campaign fixtures, payloads, and artifact trees."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from scripts.skill_pack_contract import tree_entries


TREE_ALGORITHM = (
    "campaign-tree-v1: SHA-256 of UTF-8 lines sorted by ordinal UTF-8 "
    "POSIX path; path<TAB>byte_count<TAB>file_sha256<LF>"
)
CURRENT_FIXTURE_SCHEMA_VERSION = 2
REQUIRED_CASE_FIELDS = (
    "task",
    "authority",
    "initial_state",
    "tools_operations",
    "mutation_boundary",
    "requested_output",
)
DECISION_STATE_VALUES = {
    "target_resolution": frozenset({"resolved", "unresolved", "not-applicable"}),
    "evidence_availability": frozenset(
        {"inspectable", "unavailable", "not-applicable"}
    ),
    "mutation_permission": frozenset({"allowed", "forbidden", "not-applicable"}),
}
CASE_CONTEXT_FIELDS = REQUIRED_CASE_FIELDS + ("decision_state",)
SOURCE_FIELDS = ("facts", "source_facts")
ISOLATION_FALSE_FIELDS = (
    "candidate_terms_present",
    "prior_outputs_present",
    "conclusions_present",
)
FORBIDDEN_DISPATCH_KEYS = frozenset(
    {
        "candidate_hint",
        "candidate_language",
        "candidate_terms",
        "conclusions",
        "expected_weakness",
        "expected_weaknesses",
        "hypothesis",
        "prior_outputs",
        "rubric",
        "rubrics_or_scores",
        "scores",
        "scoring",
    }
)


def _nonempty(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, bytes, list, tuple, dict, set)):
        return bool(value)
    return True


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def _canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_decision_state(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} decision_state must be an object")
    missing = sorted(set(DECISION_STATE_VALUES).difference(value))
    unexpected = sorted(set(value).difference(DECISION_STATE_VALUES))
    invalid = sorted(
        field
        for field, allowed in DECISION_STATE_VALUES.items()
        if field in value and value[field] not in allowed
    )
    failures: list[str] = []
    if missing:
        failures.append("missing " + ", ".join(missing))
    if unexpected:
        failures.append("unexpected " + ", ".join(unexpected))
    if invalid:
        failures.append("invalid " + ", ".join(invalid))
    if failures:
        raise ValueError(f"{label} decision_state is invalid: {'; '.join(failures)}")


def campaign_tree_hash(directory: Path) -> dict[str, object]:
    entries = tree_entries(directory)
    files = [
        (name, content)
        for name, (kind, content) in entries.items()
        if kind == "file"
    ]
    digest = hashlib.sha256()
    for name, content in sorted(files, key=lambda item: item[0].encode("utf-8")):
        if "\t" in name or "\r" in name or "\n" in name:
            raise ValueError(f"Campaign artifact path is not hash-safe: {name!r}")
        file_sha256 = hashlib.sha256(content).hexdigest()
        digest.update(f"{name}\t{len(content)}\t{file_sha256}\n".encode("utf-8"))
    return {
        "algorithm": TREE_ALGORITHM,
        "file_count": len(files),
        "sha256": digest.hexdigest(),
    }


def _case_nodes(
    value: object,
    inherited: dict[str, object] | None = None,
) -> list[tuple[str, dict[str, object]]]:
    context = dict(inherited or {})
    cases: list[tuple[str, dict[str, object]]] = []
    if isinstance(value, dict):
        for field in CASE_CONTEXT_FIELDS:
            if field in value:
                context[field] = value[field]
        if "id" in value and any(field in value for field in SOURCE_FIELDS):
            case = dict(context)
            case.update(value)
            cases.append((str(value["id"]), case))
        for child in value.values():
            cases.extend(_case_nodes(child, context))
    elif isinstance(value, list):
        for child in value:
            cases.extend(_case_nodes(child, context))
    return cases


def lint_worker_fixture(path: Path) -> dict[str, object]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Worker fixture must be a JSON object")
    schema_version = payload.get("schema_version", 1)
    if schema_version not in (1, CURRENT_FIXTURE_SCHEMA_VERSION):
        raise ValueError(
            "Worker fixture schema_version must be 1 or "
            f"{CURRENT_FIXTURE_SCHEMA_VERSION}"
        )
    requires_decision_state = schema_version >= CURRENT_FIXTURE_SCHEMA_VERSION

    isolation = payload.get("isolation")
    if not isinstance(isolation, dict):
        raise ValueError("Worker fixture must define an isolation object")
    if isolation.get("arm_delta") != "runtime package only":
        raise ValueError("Worker fixture isolation.arm_delta must be runtime package only")
    leaked_or_unstated = [
        key
        for key in ISOLATION_FALSE_FIELDS
        if isolation.get(key) is not False
    ]
    leaked_or_unstated.extend(
        key
        for key, value in isolation.items()
        if key.endswith("_present")
        and value is not False
        and key not in leaked_or_unstated
    )
    if leaked_or_unstated:
        raise ValueError(
            "Worker fixture isolation must explicitly exclude: "
            + ", ".join(sorted(leaked_or_unstated))
        )

    inherited = payload.get("fixed_execution")
    if inherited is not None and not isinstance(inherited, dict):
        raise ValueError("Worker fixture fixed_execution must be an object")
    cases = _case_nodes(payload, inherited)
    if not cases:
        raise ValueError("Worker fixture must contain at least one sourced case")
    case_ids = [case_id for case_id, _case in cases]
    duplicate_ids = sorted(
        case_id for case_id in set(case_ids) if case_ids.count(case_id) > 1
    )
    if duplicate_ids:
        raise ValueError(
            "Worker fixture contains duplicate case IDs: "
            + ", ".join(duplicate_ids)
        )

    failures: list[str] = []
    for case_id, case in cases:
        missing = [
            field for field in REQUIRED_CASE_FIELDS if not _nonempty(case.get(field))
        ]
        if requires_decision_state and not _nonempty(case.get("decision_state")):
            missing.append("decision_state")
        if not any(_nonempty(case.get(field)) for field in SOURCE_FIELDS):
            missing.append("facts|source_facts")
        if missing:
            failures.append(f"{case_id}: {', '.join(missing)}")
    if failures:
        raise ValueError("Worker fixture cases are incomplete: " + "; ".join(failures))
    for case_id, case in cases:
        if "decision_state" in case:
            _validate_decision_state(case["decision_state"], f"Case {case_id}")

    return {
        "status": "ok",
        "schema_version": schema_version,
        "case_count": len(cases),
    }


def _fixture_case(path: Path, case_id: str) -> dict[str, object]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Worker fixture must be a JSON object")
    inherited = payload.get("fixed_execution")
    cases = {
        candidate_id: case
        for candidate_id, case in _case_nodes(
            payload,
            inherited if isinstance(inherited, dict) else None,
        )
    }
    if case_id not in cases:
        raise ValueError(f"Worker fixture case is missing: {case_id}")
    return cases[case_id]


def _remove_json_pointer(payload: object, pointer: str) -> object:
    if not pointer.startswith("/") or pointer == "/":
        raise ValueError(f"Runtime pointer must name one nested value: {pointer!r}")
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.removeprefix("/").split("/")
    ]
    parent = payload
    for part in parts[:-1]:
        if isinstance(parent, dict) and part in parent:
            parent = parent[part]
        elif isinstance(parent, list) and part.isdigit() and int(part) < len(parent):
            parent = parent[int(part)]
        else:
            raise ValueError(f"Runtime pointer is missing: {pointer}")
    leaf = parts[-1]
    if isinstance(parent, dict) and leaf in parent:
        return parent.pop(leaf)
    elif isinstance(parent, list) and leaf.isdigit() and int(leaf) < len(parent):
        return parent.pop(int(leaf))
    else:
        raise ValueError(f"Runtime pointer is missing: {pointer}")


def _forbidden_dispatch_keys(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        found.update(FORBIDDEN_DISPATCH_KEYS.intersection(value))
        for child in value.values():
            found.update(_forbidden_dispatch_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_forbidden_dispatch_keys(child))
    return found


def _lint_dispatch_payload(
    payload: object,
    label: str,
    *,
    require_decision_state: bool,
) -> None:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} dispatch payload must be a JSON object")
    missing = [
        field for field in REQUIRED_CASE_FIELDS if not _nonempty(payload.get(field))
    ]
    if require_decision_state and not _nonempty(payload.get("decision_state")):
        missing.append("decision_state")
    if not any(_nonempty(payload.get(field)) for field in SOURCE_FIELDS):
        missing.append("facts|source_facts")
    if missing:
        raise ValueError(f"{label} dispatch payload is incomplete: {', '.join(missing)}")
    if "decision_state" in payload:
        _validate_decision_state(
            payload["decision_state"],
            f"{label} dispatch payload",
        )
    forbidden = _forbidden_dispatch_keys(payload)
    if forbidden:
        raise ValueError(
            f"{label} dispatch payload contains root-only fields: "
            + ", ".join(sorted(forbidden))
        )


def _verify_fixture_fidelity(
    payload: dict[str, object],
    fixture_case: dict[str, object],
    label: str,
) -> None:
    fields = list(REQUIRED_CASE_FIELDS)
    if "decision_state" in fixture_case:
        fields.append("decision_state")
    fields.extend(field for field in SOURCE_FIELDS if field in fixture_case)
    mismatched = [
        field
        for field in fields
        if payload.get(field) != fixture_case.get(field)
    ]
    if mismatched:
        raise ValueError(
            f"{label} dispatch payload disagrees with its worker fixture case: "
            + ", ".join(mismatched)
        )


def lint_dispatch_payload(
    fixture_path: Path,
    case_id: str,
    payload_path: Path,
    runtime_pointer: str = "/runtime",
) -> dict[str, object]:
    fixture_result = lint_worker_fixture(fixture_path)
    fixture_case = _fixture_case(fixture_path, case_id)
    payload = _read_json(payload_path)
    _lint_dispatch_payload(
        payload,
        "Resolved",
        require_decision_state=(
            fixture_result["schema_version"] >= CURRENT_FIXTURE_SCHEMA_VERSION
        ),
    )
    _verify_fixture_fidelity(payload, fixture_case, "Resolved")

    runtime_check = copy.deepcopy(payload)
    runtime = _remove_json_pointer(runtime_check, runtime_pointer)
    if not _nonempty(runtime):
        raise ValueError("Resolved dispatch payload must name a nonempty runtime")
    return {
        "status": "ok",
        "case_id": case_id,
        "runtime_pointer": runtime_pointer,
        "dispatch_payload_sha256": _canonical_json_sha256(payload),
    }


def compare_payloads(
    fixture_path: Path,
    case_id: str,
    control_path: Path,
    candidate_path: Path,
    runtime_pointer: str = "/runtime",
) -> dict[str, object]:
    fixture_result = lint_worker_fixture(fixture_path)
    fixture_case = _fixture_case(fixture_path, case_id)
    control = _read_json(control_path)
    candidate = _read_json(candidate_path)
    require_decision_state = (
        fixture_result["schema_version"] >= CURRENT_FIXTURE_SCHEMA_VERSION
    )
    _lint_dispatch_payload(
        control,
        "Control",
        require_decision_state=require_decision_state,
    )
    _lint_dispatch_payload(
        candidate,
        "Candidate",
        require_decision_state=require_decision_state,
    )
    _verify_fixture_fidelity(control, fixture_case, "Control")
    _verify_fixture_fidelity(candidate, fixture_case, "Candidate")

    normalized_control = copy.deepcopy(control)
    normalized_candidate = copy.deepcopy(candidate)
    control_runtime = _remove_json_pointer(normalized_control, runtime_pointer)
    candidate_runtime = _remove_json_pointer(normalized_candidate, runtime_pointer)
    if not _nonempty(control_runtime) or not _nonempty(candidate_runtime):
        raise ValueError("Both dispatch payloads must name a nonempty runtime")
    if control_runtime == candidate_runtime:
        raise ValueError("Control and candidate dispatch runtimes must differ")
    if normalized_control != normalized_candidate:
        raise ValueError(
            "Control and candidate dispatch payloads differ outside the runtime slot"
        )

    return {
        "status": "ok",
        "runtime_pointer": runtime_pointer,
        "shared_payload_sha256": _canonical_json_sha256(normalized_control),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify deploy-campaign artifact identities and isolation."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    hash_tree = commands.add_parser("hash-tree")
    hash_tree.add_argument("path", type=Path)

    lint_fixture = commands.add_parser("lint-fixture")
    lint_fixture.add_argument("path", type=Path)

    lint_payload = commands.add_parser("lint-payload")
    lint_payload.add_argument("fixture", type=Path)
    lint_payload.add_argument("case_id")
    lint_payload.add_argument("payload", type=Path)
    lint_payload.add_argument("--runtime-pointer", default="/runtime")

    compare = commands.add_parser("compare-payloads")
    compare.add_argument("fixture", type=Path)
    compare.add_argument("case_id")
    compare.add_argument("control", type=Path)
    compare.add_argument("candidate", type=Path)
    compare.add_argument("--runtime-pointer", default="/runtime")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "hash-tree":
            result = campaign_tree_hash(args.path)
        elif args.command == "lint-fixture":
            result = lint_worker_fixture(args.path)
        elif args.command == "lint-payload":
            result = lint_dispatch_payload(
                args.fixture,
                args.case_id,
                args.payload,
                args.runtime_pointer,
            )
        else:
            result = compare_payloads(
                args.fixture,
                args.case_id,
                args.control,
                args.candidate,
                args.runtime_pointer,
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
