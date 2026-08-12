"""Deterministic JSON-state renderer for the audit-codebase HTML atlas."""

from __future__ import annotations

import argparse
import hashlib
from html import escape, unescape
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from typing import Any, NoReturn, Sequence


REPORT_VERSION = 10
STATE_VERSION = 2
RESPONSE_VERSION = 1
MANIFEST_VERSION = 4

_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_GIT_ID = re.compile(r"[0-9a-f]{40,64}")
_MAP_STATES = {"complete", "incomplete"}
_SUBSYSTEM_STATES = {"mapped", "incomplete", "audited"}
_CANDIDATE_STATES = (
    "presented",
    "decision pending",
    "analyzed",
    "implemented",
    "disproved",
    "blocked",
)
_FINDING_STATES = ("active", "resolved", "disproved")
_FINDING_KINDS = {"defect", "opportunity", "gap", "retained complexity"}
_LENSES = (
    "reliability",
    "domain",
    "design",
    "simplification",
    "coding practice",
    "performance",
)
_STRENGTHS = {"Strong", "Worth exploring", "Speculative"}
_TRACKER_STATES = {
    "not-applicable",
    "authority-required",
    "ready-graph",
    "reused",
    "recovery",
}

_STYLE = """
:root {
  color-scheme: dark;
  --bg: #0b1020;
  --panel: #111827;
  --panel-2: #172033;
  --text: #e5edf8;
  --muted: #9fb0c7;
  --border: #34445f;
  --link: #7dd3fc;
  --mapped: #64748b;
  --incomplete: #f59e0b;
  --audited: #22c55e;
  --presented: #38bdf8;
  --decision: #f59e0b;
  --analyzed: #a78bfa;
  --implemented: #22c55e;
  --disproved: #94a3b8;
  --blocked: #f87171;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.55 ui-sans-serif, system-ui, sans-serif;
}
a { color: var(--link); }
code { white-space: pre-wrap; overflow-wrap: anywhere; }
header, main, footer { width: min(1500px, calc(100% - 32px)); margin: 0 auto; }
header { padding: 28px 0 16px; }
footer { padding: 22px 0 40px; color: var(--muted); }
section, article, .panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin: 14px 0;
  padding: 18px;
}
h1, h2, h3, h4 { line-height: 1.2; }
.muted { color: var(--muted); }
.systems, .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.map-wrap, .table-wrap { overflow-x: auto; }
svg { min-width: 900px; width: 100%; }
.edge { stroke: #70829f; stroke-width: 1.5; }
.node rect { fill: var(--panel-2); stroke-width: 3; rx: 12; }
.node text { fill: var(--text); text-anchor: middle; }
.state-mapped { stroke: var(--mapped); }
.state-incomplete { stroke: var(--incomplete); }
.state-audited { stroke: var(--audited); }
.status { border: 1px solid currentColor; border-radius: 999px; padding: 1px 8px; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid var(--border); padding: 9px; text-align: left; vertical-align: top; }
dl { display: grid; grid-template-columns: minmax(140px, 220px) 1fr; gap: 6px 14px; }
dt { color: var(--muted); font-weight: 650; }
dd { margin: 0; }
[data-candidate-id], [data-finding-id] { border-left: 4px solid var(--border); }
[data-state="presented"] { border-left-color: var(--presented); }
[data-state="decision pending"] { border-left-color: var(--decision); }
[data-state="analyzed"] { border-left-color: var(--analyzed); }
[data-state="implemented"] { border-left-color: var(--implemented); }
[data-state="disproved"] { border-left-color: var(--disproved); }
[data-state="blocked"] { border-left-color: var(--blocked); }
@media (max-width: 700px) {
  dl { grid-template-columns: 1fr; }
  header, main, footer { width: min(100% - 20px, 1500px); }
}
""".strip()

_STATE_PATTERN = re.compile(
    r'<script id="audit-codebase-state" type="application/json" '
    r'data-sha256="([0-9a-f]{64})">(.*?)</script>',
    re.DOTALL,
)


class ReportError(ValueError):
    def __init__(
        self,
        message: str,
        *,
        stage: str = "validate",
        mutation_started: bool = False,
        report_unchanged: bool = True,
        report_state: str = "unchanged",
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.mutation_started = mutation_started
        self.report_unchanged = report_unchanged
        self.report_state = report_state


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ReportError(message, stage="arguments")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _strict(record: dict[str, Any], required: set[str], optional: set[str], label: str) -> None:
    missing = sorted(required - set(record))
    unknown = sorted(set(record) - required - optional)
    if missing:
        raise ReportError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise ReportError(f"{label} has unknown fields: {', '.join(unknown)}")


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReportError(f"{label} must be an object")
    return dict(value)


def _text(value: object, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ReportError(f"{label} must be a non-empty string")
    return value.strip()


def _identifier(value: object, label: str) -> str:
    result = _text(value, label)
    if _ID.fullmatch(result) is None:
        raise ReportError(f"{label} is not a safe identifier")
    return result


def _text_list(value: object, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ReportError(f"{label} must be a list")
    result = [_text(item, f"{label} item") for item in value]
    if len(result) != len(set(result)):
        raise ReportError(f"{label} contains duplicates")
    return result


def _relative_path(value: object, label: str) -> str:
    raw = _text(value, label).replace("\\", "/")
    path = PurePosixPath(raw)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ReportError(f"{label} must be a contained relative path")
    return path.as_posix()


def _sha(value: object, label: str, *, absent: bool = False) -> str:
    result = _text(value, label)
    if absent and result == "absent":
        return result
    if _SHA256.fullmatch(result) is None:
        raise ReportError(f"{label} must be a lowercase SHA-256")
    return result


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = path.resolve(strict=True).read_bytes()
        value = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReportError(f"{label} is not readable UTF-8 JSON: {exc}") from exc
    return _object(value, label)


def _report_path(repo_root: Path, report: Path, *, must_exist: bool) -> tuple[Path, Path]:
    try:
        root = repo_root.resolve(strict=True)
    except OSError as exc:
        raise ReportError(f"repository root cannot resolve: {exc}") from exc
    candidate = report.resolve(strict=must_exist)
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ReportError("report is outside repository root") from exc
    parts = relative.parts
    if (
        len(parts) != 4
        or parts[0] != ".scratch"
        or parts[1] != "audit-codebase"
        or not _RUN_ID.fullmatch(parts[2])
        or parts[3] != "report.html"
    ):
        raise ReportError(
            "report must be .scratch/audit-codebase/<run-id>/report.html"
        )
    return root, candidate


def _normalize_dependencies(value: object, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ReportError(f"{label} must be a list")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        item = _object(raw, f"{label}[{index}]")
        _strict(item, {"id", "evidence"}, set(), f"{label}[{index}]")
        identifier = _identifier(item["id"], f"{label}[{index}].id")
        if identifier in seen:
            raise ReportError(f"{label} repeats dependency {identifier!r}")
        seen.add(identifier)
        result.append(
            {
                "id": identifier,
                "evidence": _text_list(
                    item["evidence"],
                    f"{label}[{index}].evidence",
                    allow_empty=False,
                ),
            }
        )
    return sorted(result, key=lambda item: item["id"])


def _normalize_subsystem(value: object, label: str) -> dict[str, Any]:
    item = _object(value, label)
    required = {
        "id",
        "system_id",
        "name",
        "source_identity",
        "purpose",
        "authority",
        "callers",
        "responsibility",
        "dependencies",
        "interfaces",
        "proof_seams",
        "owned_paths",
    }
    _strict(item, required, set(), label)
    return {
        "id": _identifier(item["id"], f"{label}.id"),
        "system_id": _identifier(item["system_id"], f"{label}.system_id"),
        "name": _text(item["name"], f"{label}.name"),
        "state": "mapped",
        "source_identity": _text(item["source_identity"], f"{label}.source_identity"),
        "purpose": _text(item["purpose"], f"{label}.purpose"),
        "authority": _text_list(item["authority"], f"{label}.authority"),
        "callers": _text_list(item["callers"], f"{label}.callers"),
        "responsibility": _text(item["responsibility"], f"{label}.responsibility"),
        "dependencies": _normalize_dependencies(
            item["dependencies"], f"{label}.dependencies"
        ),
        "interfaces": _text_list(item["interfaces"], f"{label}.interfaces"),
        "proof_seams": _text_list(item["proof_seams"], f"{label}.proof_seams"),
        "owned_paths": sorted(
            _relative_path(path, f"{label}.owned_paths item")
            for path in _text_list(item["owned_paths"], f"{label}.owned_paths")
        ),
    }


def _normalize_map_manifest(raw: dict[str, Any], root: Path, report: Path) -> dict[str, Any]:
    required = {
        "version",
        "expected_report_sha256",
        "map_state",
        "title",
        "observation_identity",
        "systems",
        "subsystems",
        "excluded",
        "coverage",
        "evidence_limits",
        "next_selection",
    }
    _strict(raw, required, set(), "Map manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"Map manifest requires version {MANIFEST_VERSION}")
    map_state = _text(raw["map_state"], "Map manifest map_state")
    if map_state not in _MAP_STATES:
        raise ReportError("Map manifest has unsupported map_state")
    if not isinstance(raw["systems"], list) or not raw["systems"]:
        raise ReportError("Map manifest systems must be a non-empty list")
    systems: list[dict[str, str]] = []
    system_ids: set[str] = set()
    for index, value in enumerate(raw["systems"]):
        item = _object(value, f"system[{index}]")
        _strict(item, {"id", "name"}, set(), f"system[{index}]")
        identifier = _identifier(item["id"], f"system[{index}].id")
        if identifier in system_ids:
            raise ReportError(f"duplicate system ID: {identifier}")
        system_ids.add(identifier)
        systems.append({"id": identifier, "name": _text(item["name"], f"system[{index}].name")})
    if not isinstance(raw["subsystems"], list) or not raw["subsystems"]:
        raise ReportError("Map manifest subsystems must be a non-empty list")
    subsystems = [
        _normalize_subsystem(value, f"subsystem[{index}]")
        for index, value in enumerate(raw["subsystems"])
    ]
    subsystem_ids = [item["id"] for item in subsystems]
    if len(subsystem_ids) != len(set(subsystem_ids)):
        raise ReportError("Map manifest has duplicate subsystem IDs")
    for subsystem in subsystems:
        if subsystem["system_id"] not in system_ids:
            raise ReportError(
                f"subsystem {subsystem['id']!r} references unknown system"
            )
        for dependency in subsystem["dependencies"]:
            if dependency["id"] not in subsystem_ids:
                raise ReportError(
                    f"subsystem {subsystem['id']!r} references unknown dependency "
                    f"{dependency['id']!r}"
                )
            if dependency["id"] == subsystem["id"]:
                raise ReportError("a subsystem may not depend on itself")
    owned: dict[str, str] = {}
    for subsystem in subsystems:
        for path in subsystem["owned_paths"]:
            if path in owned:
                raise ReportError(
                    f"path {path!r} is owned by both {owned[path]!r} and "
                    f"{subsystem['id']!r}"
                )
            owned[path] = subsystem["id"]
    if not isinstance(raw["excluded"], list):
        raise ReportError("Map manifest excluded must be a list")
    excluded: list[dict[str, str]] = []
    excluded_paths: set[str] = set()
    for index, value in enumerate(raw["excluded"]):
        item = _object(value, f"excluded[{index}]")
        _strict(item, {"path", "reason"}, set(), f"excluded[{index}]")
        path = _relative_path(item["path"], f"excluded[{index}].path")
        if path in excluded_paths or path in owned:
            raise ReportError(f"path {path!r} has duplicate ownership or exclusion")
        excluded_paths.add(path)
        excluded.append({"path": path, "reason": _text(item["reason"], f"excluded[{index}].reason")})
    all_claims = sorted(set(owned) | excluded_paths)
    for index, path in enumerate(all_claims):
        parts = PurePosixPath(path).parts
        for other in all_claims[index + 1 :]:
            other_parts = PurePosixPath(other).parts
            if parts == other_parts[: len(parts)]:
                raise ReportError(f"Map paths overlap by ancestor scope: {path!r} and {other!r}")
    for path in owned:
        candidate = (root / Path(*PurePosixPath(path).parts)).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ReportError(f"owned path escapes repository: {path}") from exc
        if not candidate.is_file():
            raise ReportError(f"owned path is not a current file: {path}")
    tracked_paths, tracked_identity = _tracked_inventory(root)
    if raw["observation_identity"] != tracked_identity:
        raise ReportError("Map observation_identity does not match the current tracked inventory")
    uncovered = [
        path
        for path in tracked_paths
        if path not in owned
        and not any(
            PurePosixPath(excluded).parts == PurePosixPath(path).parts[: len(PurePosixPath(excluded).parts)]
            for excluded in excluded_paths
        )
    ]
    if map_state == "complete" and uncovered:
        raise ReportError("complete Map leaves tracked paths unowned or unexcluded: " + ", ".join(uncovered))
    state = {
        "state_version": STATE_VERSION,
        "repository_root": str(root),
        "run_id": report.parent.name,
        "title": _text(raw["title"], "Map manifest title"),
        "map_state": map_state,
        "observation_identity": tracked_identity,
        "systems": sorted(systems, key=lambda item: item["id"]),
        "subsystems": sorted(subsystems, key=lambda item: item["id"]),
        "excluded": sorted(excluded, key=lambda item: item["path"]),
        "coverage": _text(raw["coverage"], "Map manifest coverage"),
        "evidence_limits": _text(
            raw["evidence_limits"], "Map manifest evidence_limits", allow_empty=True
        ),
        "next_selection": _text(
            raw["next_selection"], "Map manifest next_selection", allow_empty=True
        ),
        "findings": [],
        "candidates": [],
        "history": [],
    }
    _validate_state(state)
    return state


def _normalize_lenses(value: object, subsystem_state: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ReportError("Audit manifest lenses must be a list")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        item = _object(raw, f"lens[{index}]")
        _strict(
            item,
            {
                "class",
                "applicability",
                "coverage",
                "evidence",
                "item_ids",
                "detailed_owner_loaded",
                "reason",
            },
            set(),
            f"lens[{index}]",
        )
        lens = _text(item["class"], f"lens[{index}].class")
        if lens not in _LENSES or lens in seen:
            raise ReportError(f"lens[{index}] has unknown or duplicate class")
        seen.add(lens)
        applicability = _text(item["applicability"], f"lens[{index}].applicability")
        coverage = _text(item["coverage"], f"lens[{index}].coverage")
        if applicability not in {"applicable", "not applicable"}:
            raise ReportError(f"lens[{index}] has unsupported applicability")
        if coverage not in {"complete", "incomplete"}:
            raise ReportError(f"lens[{index}] has unsupported coverage")
        loaded = item["detailed_owner_loaded"]
        if not isinstance(loaded, bool):
            raise ReportError(f"lens[{index}].detailed_owner_loaded must be boolean")
        if lens == "reliability" and not loaded:
            raise ReportError("Reliability detailed owner must always be loaded")
        result.append(
            {
                "class": lens,
                "applicability": applicability,
                "coverage": coverage,
                "evidence": _text_list(item["evidence"], f"lens[{index}].evidence"),
                "item_ids": _text_list(item["item_ids"], f"lens[{index}].item_ids"),
                "detailed_owner_loaded": loaded,
                "reason": _text(item["reason"], f"lens[{index}].reason"),
            }
        )
    if seen != set(_LENSES):
        raise ReportError("Audit manifest requires exactly the six lens classes")
    if subsystem_state == "audited" and any(item["coverage"] != "complete" for item in result):
        raise ReportError("an audited subsystem requires complete coverage for every lens")
    return sorted(result, key=lambda item: _LENSES.index(item["class"]))


def _normalize_source_trace(value: object) -> dict[str, Any]:
    item = _object(value, "source_trace")
    required = {
        "summary",
        "authority",
        "entry_points",
        "callers",
        "responsibility",
        "dependencies",
        "interfaces",
        "proof_seams",
        "scenarios",
    }
    _strict(item, required, set(), "source_trace")
    return {
        "summary": _text(item["summary"], "source_trace.summary"),
        "authority": _text_list(item["authority"], "source_trace.authority"),
        "entry_points": _text_list(item["entry_points"], "source_trace.entry_points"),
        "callers": _text_list(item["callers"], "source_trace.callers"),
        "responsibility": _text(item["responsibility"], "source_trace.responsibility"),
        "dependencies": _text_list(item["dependencies"], "source_trace.dependencies"),
        "interfaces": _text_list(item["interfaces"], "source_trace.interfaces"),
        "proof_seams": _text_list(item["proof_seams"], "source_trace.proof_seams"),
        "scenarios": _text_list(item["scenarios"], "source_trace.scenarios"),
    }


def _normalize_finding(value: object, subsystem_id: str, label: str) -> dict[str, Any]:
    item = _object(value, label)
    required = {
        "id",
        "kind",
        "primary_class",
        "title",
        "state",
        "location",
        "evidence",
        "impact",
        "direction",
        "proof",
        "confidence",
    }
    _strict(item, required, {"severity", "expectation"}, label)
    kind = _text(item["kind"], f"{label}.kind")
    state = _text(item["state"], f"{label}.state")
    if kind not in _FINDING_KINDS or state not in _FINDING_STATES:
        raise ReportError(f"{label} has unsupported kind or state")
    primary = _text(item["primary_class"], f"{label}.primary_class")
    if primary not in _LENSES and not primary.startswith("declared:"):
        raise ReportError(f"{label} has unsupported primary class")
    severity = item.get("severity")
    if severity is not None and severity not in {"P0", "P1", "P2", "P3"}:
        raise ReportError(f"{label}.severity is unsupported")
    if kind == "defect" and severity is None:
        raise ReportError(f"{label} defect requires severity")
    return {
        "id": _identifier(item["id"], f"{label}.id"),
        "subsystem_id": subsystem_id,
        "kind": kind,
        "primary_class": primary,
        "title": _text(item["title"], f"{label}.title"),
        "state": state,
        "severity": severity,
        "expectation": _text(item.get("expectation", ""), f"{label}.expectation", allow_empty=True),
        "location": _text_list(item["location"], f"{label}.location", allow_empty=False),
        "evidence": _text_list(item["evidence"], f"{label}.evidence", allow_empty=False),
        "impact": _text(item["impact"], f"{label}.impact"),
        "direction": _text(item["direction"], f"{label}.direction", allow_empty=True),
        "proof": _text_list(item["proof"], f"{label}.proof", allow_empty=False),
        "confidence": _text(item["confidence"], f"{label}.confidence"),
        "history": [],
    }


def _skill_links(value: object) -> dict[str, str]:
    item = _object(value, "skill_links")
    _strict(item, {"audit_codebase", "to_tickets", "implement"}, set(), "skill_links")
    result: dict[str, str] = {}
    for name in ("audit_codebase", "to_tickets", "implement"):
        path = Path(_text(item[name], f"skill_links.{name}"))
        if not path.is_absolute():
            raise ReportError(f"skill_links.{name} must be absolute")
        result[name] = path.as_posix()
    return result


def _analyze_pickup(candidate_id: str, report: Path, links: dict[str, str]) -> str:
    return (
        f"[$audit-codebase]({links['audit_codebase']}) Analyze candidate "
        f"{candidate_id} from {report.as_posix()}. If implementation-ready, invoke "
        f"[$to-tickets]({links['to_tickets']}) for that exact analyzed candidate "
        "and record its returned tracker state in this Analyze publication."
    )


def _candidate_bundle_sha256(state: dict[str, Any], candidate: dict[str, Any]) -> str:
    immutable_fields = (
        "id",
        "subsystem_id",
        "title",
        "primary_class",
        "member_ids",
        "files_modules",
        "supported_behavior",
        "problem",
        "evidence",
        "direction",
        "benefit",
        "safety_floors",
        "required_proof",
        "decision_questions",
        "strength",
        "strength_reason",
    )
    return _digest(
        _canonical_json(
            {
                "run_id": state["run_id"],
                "candidate": {name: candidate[name] for name in immutable_fields},
            }
        )
    )


def _normalize_candidate(
    value: object,
    subsystem_id: str,
    report: Path,
    links: dict[str, str],
    label: str,
) -> dict[str, Any]:
    item = _object(value, label)
    required = {
        "id",
        "title",
        "primary_class",
        "member_ids",
        "files_modules",
        "supported_behavior",
        "problem",
        "evidence",
        "direction",
        "benefit",
        "safety_floors",
        "required_proof",
        "decision_questions",
        "strength",
        "strength_reason",
    }
    _strict(item, required, set(), label)
    identifier = _identifier(item["id"], f"{label}.id")
    strength = _text(item["strength"], f"{label}.strength")
    if strength not in _STRENGTHS:
        raise ReportError(f"{label}.strength is unsupported")
    primary = _text(item["primary_class"], f"{label}.primary_class")
    if primary not in _LENSES and primary != "mixed" and not primary.startswith("declared:"):
        raise ReportError(f"{label}.primary_class is unsupported")
    return {
        "id": identifier,
        "subsystem_id": subsystem_id,
        "title": _text(item["title"], f"{label}.title"),
        "primary_class": primary,
        "member_ids": _text_list(item["member_ids"], f"{label}.member_ids", allow_empty=False),
        "files_modules": _text_list(item["files_modules"], f"{label}.files_modules", allow_empty=False),
        "supported_behavior": _text(item["supported_behavior"], f"{label}.supported_behavior"),
        "problem": _text(item["problem"], f"{label}.problem"),
        "evidence": _text_list(item["evidence"], f"{label}.evidence", allow_empty=False),
        "direction": _text(item["direction"], f"{label}.direction"),
        "benefit": _text(item["benefit"], f"{label}.benefit"),
        "safety_floors": _text_list(item["safety_floors"], f"{label}.safety_floors"),
        "required_proof": _text_list(item["required_proof"], f"{label}.required_proof", allow_empty=False),
        "decision_questions": _text_list(item["decision_questions"], f"{label}.decision_questions"),
        "strength": strength,
        "strength_reason": _text(item["strength_reason"], f"{label}.strength_reason"),
        "state": "presented",
        "current_source_validity": "unexamined",
        "last_verified_identity": "",
        "source_trace": [],
        "analysis": {},
        "tracker": {"status": "not-applicable", "issue_urls": [], "ready_issue_url": ""},
        "pickup": _analyze_pickup(identifier, report, links),
        "history": [],
    }


def _normalize_audit_manifest(raw: dict[str, Any], report: Path) -> dict[str, Any]:
    required = {
        "version",
        "expected_report_sha256",
        "subsystem_id",
        "state",
        "source_identity",
        "source_trace",
        "lenses",
        "findings",
        "candidates",
        "coverage",
        "evidence_limits",
        "recommendation",
        "skill_links",
    }
    _strict(raw, required, set(), "Audit manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"Audit manifest requires version {MANIFEST_VERSION}")
    state = _text(raw["state"], "Audit manifest state")
    if state not in {"audited", "incomplete"}:
        raise ReportError("Audit manifest state must be audited or incomplete")
    subsystem_id = _identifier(raw["subsystem_id"], "Audit manifest subsystem_id")
    if not isinstance(raw["findings"], list) or not isinstance(raw["candidates"], list):
        raise ReportError("Audit findings and candidates must be lists")
    links = _skill_links(raw["skill_links"])
    findings = [
        _normalize_finding(value, subsystem_id, f"finding[{index}]")
        for index, value in enumerate(raw["findings"])
    ]
    candidates = [
        _normalize_candidate(value, subsystem_id, report, links, f"candidate[{index}]")
        for index, value in enumerate(raw["candidates"])
    ]
    finding_ids = [item["id"] for item in findings]
    candidate_ids = [item["id"] for item in candidates]
    if len(finding_ids) != len(set(finding_ids)) or len(candidate_ids) != len(set(candidate_ids)):
        raise ReportError("Audit manifest repeats a finding or candidate ID")
    admitted = {item["id"]: item for item in findings}
    for candidate in candidates:
        for member in candidate["member_ids"]:
            if member not in admitted:
                raise ReportError(
                    f"candidate {candidate['id']!r} references a finding not in its Audit packet"
                )
        if not any(admitted[item]["kind"] in {"defect", "opportunity"} for item in candidate["member_ids"]):
            raise ReportError(f"candidate {candidate['id']!r} is gap/retain-only")
    lenses = _normalize_lenses(raw["lenses"], state)
    known_item_ids = set(finding_ids)
    for lens in lenses:
        unknown_items = sorted(set(lens["item_ids"]) - known_item_ids)
        if unknown_items:
            raise ReportError(
                f"lens {lens['class']!r} references unknown item IDs: "
                + ", ".join(unknown_items)
            )
    return {
        "version": MANIFEST_VERSION,
        "expected_report_sha256": _sha(
            raw["expected_report_sha256"], "Audit manifest expected_report_sha256"
        ),
        "subsystem_id": subsystem_id,
        "state": state,
        "source_identity": _text(raw["source_identity"], "Audit manifest source_identity"),
        "source_trace": _normalize_source_trace(raw["source_trace"]),
        "lenses": lenses,
        "findings": sorted(findings, key=lambda item: item["id"]),
        "candidates": sorted(candidates, key=lambda item: item["id"]),
        "coverage": _text(raw["coverage"], "Audit manifest coverage"),
        "evidence_limits": _text(raw["evidence_limits"], "Audit manifest evidence_limits", allow_empty=True),
        "recommendation": _text(raw["recommendation"], "Audit manifest recommendation", allow_empty=True),
        "skill_links": links,
    }


def _normalize_analysis(value: object) -> dict[str, Any]:
    item = _object(value, "analysis")
    required = {
        "validity_reason",
        "changed_evidence_members",
        "current_shape_cost",
        "keep",
        "smallest_sufficient_change",
        "structural_change",
        "replacement",
        "recommended_direction",
        "rejected_alternatives",
        "contracts_decisions",
        "responsibilities_interfaces_seams",
        "compatibility_migration",
        "proof_plan",
        "residual_risk",
        "decision_status",
    }
    _strict(item, required, set(), "analysis")
    decision = _text(item["decision_status"], "analysis.decision_status")
    if decision not in {"none", "pending", "settled", "evidence gap", "blocked"}:
        raise ReportError("analysis.decision_status is unsupported")
    result: dict[str, Any] = {"decision_status": decision}
    list_fields = {
        "changed_evidence_members",
        "rejected_alternatives",
        "contracts_decisions",
        "responsibilities_interfaces_seams",
        "proof_plan",
    }
    for name in required - {"decision_status"}:
        result[name] = (
            _text_list(item[name], f"analysis.{name}")
            if name in list_fields
            else _text(item[name], f"analysis.{name}", allow_empty=True)
        )
    return result


def _normalize_tracker(
    value: object,
    *,
    require_local_graph: bool = False,
) -> dict[str, Any]:
    item = _object(value, "tracker")
    required = {"status", "issue_urls", "ready_issue_url"}
    common_optional = {
        "candidate_bundle_sha256",
        "mutation_identity",
        "read_back",
        "observed_issue_state",
    }
    local_optional = {
        "provider",
        "parent_ref",
        "issue_refs",
        "ready_issue_ref",
        "readiness",
        "blockers",
        "claim_state",
        "frontier",
        "graph_sha256",
    }
    _strict(item, required, common_optional | local_optional, "tracker")
    status = _text(item["status"], "tracker.status")
    if status not in _TRACKER_STATES:
        raise ReportError("tracker has unsupported status")
    urls = _text_list(item["issue_urls"], "tracker.issue_urls")
    ready = _text(item["ready_issue_url"], "tracker.ready_issue_url", allow_empty=True)
    if any(re.fullmatch(r"https://[^\s]+", url) is None for url in urls):
        raise ReportError("tracker issue_urls must be absolute HTTPS URLs")
    if ready and re.fullmatch(r"https://[^\s]+", ready) is None:
        raise ReportError("tracker ready_issue_url must be an absolute HTTPS URL")
    supplied_optional = set(item) - required
    local = item.get("provider") == "local-markdown"
    if "provider" in item and not local:
        raise ReportError("tracker provider is unsupported")
    if local and status not in {"ready-graph", "reused"}:
        raise ReportError("Local Markdown provider requires a ready tracker state")
    if status in {"ready-graph", "reused"}:
        expected = {"candidate_bundle_sha256", "mutation_identity", "read_back"}
        if local:
            expected |= local_optional - {"graph_sha256"}
            allowed = {frozenset(expected), frozenset(expected | {"graph_sha256"})}
            if frozenset(supplied_optional) not in allowed:
                raise ReportError("Local Markdown tracker state has missing or foreign fields")
            if require_local_graph and "graph_sha256" not in supplied_optional:
                raise ReportError("Local Markdown tracker state requires graph_sha256")
            if urls or ready:
                raise ReportError("Local Markdown tracker state forbids hosted issue URLs")
        elif supplied_optional != expected:
            raise ReportError("ready tracker state has missing or foreign fields")
        if not local and (not urls or ready not in urls):
            raise ReportError("ready tracker state requires one returned frontier issue")
        _sha(item["candidate_bundle_sha256"], "tracker.candidate_bundle_sha256")
        _text(item["mutation_identity"], "tracker.mutation_identity")
        if item["read_back"] is not True:
            raise ReportError("ready tracker state requires verified read-back")
        if local:
            parent_ref = _text(item["parent_ref"], "tracker.parent_ref")
            issue_refs = _text_list(item["issue_refs"], "tracker.issue_refs", allow_empty=False)
            ready_issue_ref = _text(item["ready_issue_ref"], "tracker.ready_issue_ref")
            frontier = _text_list(item["frontier"], "tracker.frontier", allow_empty=False)
            blockers = _text_list(item["blockers"], "tracker.blockers")
            readiness = _text(item["readiness"], "tracker.readiness")
            claim_state = _text(item["claim_state"], "tracker.claim_state")
            if readiness != "ready-for-agent" or blockers or claim_state != "unclaimed":
                raise ReportError(
                    "Local Markdown ready tracker requires ready, unblocked, unclaimed state"
                )
            if ready_issue_ref not in issue_refs or frontier[0] != ready_issue_ref:
                raise ReportError("Local Markdown ready issue must lead the verified frontier")
            local_result = {
                "provider": "local-markdown",
                "parent_ref": parent_ref,
                "issue_refs": issue_refs,
                "ready_issue_ref": ready_issue_ref,
                "readiness": readiness,
                "blockers": blockers,
                "claim_state": claim_state,
                "frontier": frontier,
            }
            if "graph_sha256" in item:
                local_result["graph_sha256"] = _sha(
                    item["graph_sha256"], "tracker.graph_sha256"
                )
    elif status == "recovery":
        expected = {
            "candidate_bundle_sha256",
            "mutation_identity",
            "observed_issue_state",
        }
        if supplied_optional != expected:
            raise ReportError("tracker recovery has missing or foreign fields")
        _sha(item["candidate_bundle_sha256"], "tracker.candidate_bundle_sha256")
        _text(item["mutation_identity"], "tracker.mutation_identity")
        _text(item["observed_issue_state"], "tracker.observed_issue_state")
    elif status == "authority-required":
        if supplied_optional or urls or ready:
            raise ReportError(
                "authority-required tracker state forbids tracker mutation fields or issues"
            )
    elif supplied_optional or urls or ready:
        raise ReportError(
            "not-applicable tracker state forbids tracker mutation fields or issues"
        )
    result: dict[str, Any] = {
        "status": status,
        "issue_urls": urls,
        "ready_issue_url": ready,
    }
    for name in ("candidate_bundle_sha256", "mutation_identity", "read_back", "observed_issue_state"):
        if name in item:
            result[name] = item[name]
    if local:
        result |= local_result
    return result


def _contained_local_markdown_ref(root: Path, ref: str, label: str) -> Path:
    pure = PurePosixPath(ref)
    if (
        pure.is_absolute()
        or pure.as_posix() != ref
        or not pure.parts
        or pure.parts[0] != ".scratch"
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise ReportError(f"{label} must be one contained .scratch relative path")
    path = root
    for part in pure.parts:
        path /= part
        if path.is_symlink():
            raise ReportError(f"{label} may not traverse a symlink")
    try:
        path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as exc:
        raise ReportError(f"{label} is missing or escapes the repository") from exc
    if not path.is_file():
        raise ReportError(f"{label} must identify one file")
    return path


def _markdown_field(source: str, field: str, *, required: bool = True) -> str:
    matches = re.findall(rf"(?m)^{re.escape(field)}:\s*(.*?)\s*$", source)
    if len(matches) > 1 or (required and len(matches) != 1):
        raise ReportError(f"Local Markdown issue requires one {field} field")
    return matches[0] if matches else ""


def _verify_local_markdown_graph(
    root: Path,
    tracker: dict[str, Any],
    candidate_id: str,
    candidate_digest: str,
    *,
    phase: str,
) -> str:
    parent_ref = tracker["parent_ref"]
    issue_refs = tracker["issue_refs"]
    parent_parts = PurePosixPath(parent_ref).parts
    if len(parent_parts) != 3 or parent_parts[-1] != "SPEC.md":
        raise ReportError("Local Markdown parent must be .scratch/<feature>/SPEC.md")
    expected_issue_parent = PurePosixPath(*parent_parts[:-1], "issues")
    if any(
        len(PurePosixPath(ref).parts) != 4
        or PurePosixPath(ref).parent != expected_issue_parent
        or PurePosixPath(ref).suffix != ".md"
        for ref in issue_refs
    ):
        raise ReportError("Local Markdown issues must share the configured parent issue directory")
    parent_path = _contained_local_markdown_ref(root, parent_ref, "tracker.parent_ref")
    issue_paths = [
        _contained_local_markdown_ref(root, ref, f"tracker.issue_refs[{index}]")
        for index, ref in enumerate(issue_refs)
    ]
    parent_source = parent_path.read_text(encoding="utf-8")
    if (
        f"- Candidate: `{candidate_id}`" not in parent_source
        or f"- Candidate bundle SHA-256: `{candidate_digest}`" not in parent_source
    ):
        raise ReportError("Local Markdown parent does not match the selected candidate")
    parent_links = re.findall(r"\]\((issues/[^)\s]+\.md)\)", parent_source)
    expected_links = [f"issues/{PurePosixPath(ref).name}" for ref in issue_refs]
    if parent_links != expected_links:
        raise ReportError("Local Markdown parent child order does not match issue_refs")

    issues: dict[str, dict[str, object]] = {}
    for ref, path in zip(issue_refs, issue_paths, strict=True):
        source = path.read_text(encoding="utf-8")
        match = re.fullmatch(r"(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name)
        if match is None:
            raise ReportError("Local Markdown issue filename requires a numeric stable identity")
        if match.group(1) in issues:
            raise ReportError("Local Markdown graph has duplicate numeric stable identity")
        if _markdown_field(source, "Parent") != "../SPEC.md":
            raise ReportError("Local Markdown issue parent identity does not match")
        if f"`{candidate_id}`" not in source or f"`{candidate_digest}`" not in source:
            raise ReportError("Local Markdown issue does not match the selected candidate")
        blocked = _markdown_field(source, "Blocked by")
        blockers = [] if blocked.lower() == "none" else [item.strip() for item in blocked.split(",")]
        claim = _markdown_field(source, "Claimed by", required=False)
        issues[match.group(1)] = {
            "ref": ref,
            "status": _markdown_field(source, "Status"),
            "blockers": blockers,
            "claimed": bool(claim),
            "source": source,
        }
    if phase == "ready":
        frontier = [
            str(issue["ref"])
            for issue in issues.values()
            if issue["status"] == "ready-for-agent"
            and not issue["claimed"]
            and not any(
                blocker not in issues or issues[blocker]["status"] != "implemented"
                for blocker in issue["blockers"]
            )
        ]
        if frontier != tracker["frontier"]:
            raise ReportError("Local Markdown frontier does not match read-back")
        ready_ref = tracker["ready_issue_ref"]
        ready = next(issue for issue in issues.values() if issue["ref"] == ready_ref)
        if ready["status"] != tracker["readiness"] or ready["blockers"] != tracker["blockers"]:
            raise ReportError("Local Markdown ready issue state does not match read-back")
        if bool(ready["claimed"]) != (tracker["claim_state"] != "unclaimed"):
            raise ReportError("Local Markdown ready issue claim state does not match read-back")
    elif phase == "completed":
        if any(issue["status"] != "implemented" for issue in issues.values()):
            raise ReportError("Local Markdown tracker graph is not implemented")
        if any(issue["claimed"] for issue in issues.values()):
            raise ReportError("Local Markdown implemented issue remains claimed")
        if any(
            blocker not in issues or issues[blocker]["status"] != "implemented"
            for issue in issues.values()
            for blocker in issue["blockers"]
        ):
            raise ReportError("Local Markdown implemented graph has an unresolved blocker")
        if any(
            not str(issue["source"]).partition("\n## Implementation Notes\n")[2].strip()
            for issue in issues.values()
        ):
            raise ReportError("Local Markdown implemented issue has incomplete closeout")
    else:
        raise ReportError("Local Markdown verification phase is unsupported")
    digest = hashlib.sha256()
    for ref, path in [(parent_ref, parent_path), *zip(issue_refs, issue_paths, strict=True)]:
        digest.update(ref.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _verify_local_markdown_commit(
    root: Path,
    tracker: dict[str, Any],
    candidate_id: str,
    candidate_digest: str,
    commit: str,
) -> str:
    completion_digest = _verify_local_markdown_graph(
        root,
        tracker,
        candidate_id,
        candidate_digest,
        phase="completed",
    )
    for ref in [tracker["parent_ref"], *tracker["issue_refs"]]:
        path = _contained_local_markdown_ref(root, ref, "Local Markdown completion ref")
        committed = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "rev-parse", f"{commit}:{ref}"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        observed = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={root}",
                "hash-object",
                f"--path={ref}",
                str(path),
            ],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if (
            committed.returncode != 0
            or observed.returncode != 0
            or committed.stdout.strip() != observed.stdout.strip()
        ):
            raise ReportError("Local Markdown completion is not exact in the implementation commit")
    return completion_digest


def _https_only_local_markdown_frontier(tracker: dict[str, Any]) -> str | None:
    if (
        tracker.get("status") != "recovery"
        or tracker.get("issue_urls")
        or tracker.get("ready_issue_url")
    ):
        return None
    observed = str(tracker.get("observed_issue_state", "")).lower()
    required = (
        "publication recovery: local markdown graph",
        "one unclaimed ready-for-agent child",
        "no blockers",
        "requires an absolute https ready_issue_url",
        "supplies only local repository paths",
        "no truthful hosted url exists",
        "cannot be recorded as ready-graph",
    )
    match = re.search(r"\bfrontier\s+(\d+)\b", observed)
    if match is None or any(fragment not in observed for fragment in required):
        return None
    return match.group(1)


def _recover_local_markdown_tracker(
    root: Path,
    candidate_id: str,
    candidate_digest: str,
    tracker: dict[str, Any],
    commit: str,
) -> tuple[dict[str, Any], str]:
    frontier_id = _https_only_local_markdown_frontier(tracker)
    if frontier_id is None:
        raise ReportError("tracker recovery is not the Local Markdown HTTPS-only mismatch")
    scratch = root / ".scratch"
    matches: list[tuple[str, list[str]]] = []
    if scratch.is_dir() and not scratch.is_symlink():
        for parent in sorted(scratch.glob("*/SPEC.md")):
            try:
                parent_ref = parent.relative_to(root).as_posix()
                checked = _contained_local_markdown_ref(
                    root, parent_ref, "Local Markdown recovery parent"
                )
            except (ReportError, ValueError):
                continue
            source = checked.read_text(encoding="utf-8")
            if (
                f"- Candidate: `{candidate_id}`" not in source
                or f"- Candidate bundle SHA-256: `{candidate_digest}`" not in source
            ):
                continue
            links = re.findall(r"\]\((issues/[^)\s]+\.md)\)", source)
            issue_refs = [
                (PurePosixPath(parent_ref).parent / link).as_posix() for link in links
            ]
            if len(issue_refs) == 1:
                matches.append((parent_ref, issue_refs))
    if len(matches) != 1:
        raise ReportError("Local Markdown recovery requires one uniquely matching graph")
    parent_ref, issue_refs = matches[0]
    ready_matches = [
        ref
        for ref in issue_refs
        if re.match(rf"{re.escape(frontier_id)}-", PurePosixPath(ref).name)
    ]
    if len(ready_matches) != 1:
        raise ReportError("Local Markdown recovery frontier identity does not match")
    ready_ref = ready_matches[0]
    ready_source = _contained_local_markdown_ref(
        root, ready_ref, "Local Markdown recovery ready issue"
    ).read_text(encoding="utf-8")
    if (
        "- Ready state after publication verification: `ready-for-agent`." not in ready_source
        or _markdown_field(ready_source, "Blocked by").lower() != "none"
        or _markdown_field(ready_source, "Claimed by", required=False)
    ):
        raise ReportError("Local Markdown recovery cannot revalidate the original ready frontier")
    recovered = {
        "status": "ready-graph",
        "issue_urls": [],
        "ready_issue_url": "",
        "provider": "local-markdown",
        "parent_ref": parent_ref,
        "issue_refs": issue_refs,
        "ready_issue_ref": ready_ref,
        "readiness": "ready-for-agent",
        "blockers": [],
        "claim_state": "unclaimed",
        "frontier": [ready_ref],
        "candidate_bundle_sha256": candidate_digest,
        "mutation_identity": tracker["mutation_identity"],
        "read_back": True,
    }
    completion_digest = _verify_local_markdown_commit(
        root,
        recovered,
        candidate_id,
        candidate_digest,
        commit,
    )
    recovered["graph_sha256"] = completion_digest
    return recovered, completion_digest


def _normalize_finding_transitions(value: object, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ReportError(f"{label} must be a list")
    transitions: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        item_label = f"{label}[{index}]"
        item = _object(raw, item_label)
        _strict(item, {"finding_id", "state", "reason"}, set(), item_label)
        finding_id = _identifier(item["finding_id"], f"{item_label}.finding_id")
        state = _text(item["state"], f"{item_label}.state")
        if finding_id in seen or state not in _FINDING_STATES:
            raise ReportError(f"{label} has duplicate or unsupported transition")
        seen.add(finding_id)
        transitions.append(
            {
                "finding_id": finding_id,
                "state": state,
                "reason": _text(item["reason"], f"{item_label}.reason"),
            }
        )
    return sorted(transitions, key=lambda item: item["finding_id"])


def _normalize_analyze_manifest(raw: dict[str, Any]) -> dict[str, Any]:
    required = {
        "version",
        "expected_report_sha256",
        "candidate_id",
        "current_source_validity",
        "last_verified_identity",
        "source_trace",
        "state",
        "analysis",
        "tracker",
        "next_owner",
        "member_ids",
        "finding_transitions",
    }
    _strict(raw, required, set(), "Analyze manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"Analyze manifest requires version {MANIFEST_VERSION}")
    validity = _text(raw["current_source_validity"], "Analyze current_source_validity")
    state = _text(raw["state"], "Analyze state")
    if validity not in {"confirmed", "changed", "disproved", "blocked"}:
        raise ReportError("Analyze manifest has unsupported validity")
    if state not in {"analyzed", "decision pending", "disproved", "blocked"}:
        raise ReportError("Analyze manifest has unsupported state")
    valid_pairs = {
        "confirmed": {"analyzed", "decision pending", "blocked"},
        "changed": {"analyzed", "decision pending", "blocked"},
        "disproved": {"disproved"},
        "blocked": {"blocked"},
    }
    if state not in valid_pairs[validity]:
        raise ReportError("Analyze validity and state disagree")
    tracker = _normalize_tracker(raw["tracker"])
    if _https_only_local_markdown_frontier(tracker) is not None:
        raise ReportError(
            "Fresh Analyze must record Local Markdown directly, not as HTTPS-only recovery"
        )
    ready = tracker["status"] != "not-applicable"
    if ready and state != "analyzed":
        raise ReportError("only analyzed candidates may be implementation-ready")
    if ready and validity != "confirmed":
        raise ReportError("implementation readiness requires confirmed current source")
    next_owner = _object(raw["next_owner"], "next_owner")
    _strict(next_owner, {"skill", "reason", "prerequisite", "invocation"}, set(), "next_owner")
    normalized_owner = {
        name: _text(next_owner[name], f"next_owner.{name}", allow_empty=True)
        for name in ("skill", "reason", "prerequisite", "invocation")
    }
    if normalized_owner["skill"]:
        if not normalized_owner["reason"] or not normalized_owner["invocation"]:
            raise ReportError("a next owner requires its reason and invocation")
    elif any(normalized_owner[name] for name in ("reason", "prerequisite", "invocation")):
        raise ReportError("next-owner details require one named skill")
    transitions = _normalize_finding_transitions(
        raw["finding_transitions"], "Analyze finding_transitions"
    )
    analysis = _normalize_analysis(raw["analysis"])
    readiness_fields = (
        "validity_reason",
        "current_shape_cost",
        "keep",
        "smallest_sufficient_change",
        "structural_change",
        "replacement",
        "recommended_direction",
        "compatibility_migration",
        "residual_risk",
    )
    if ready and (
        analysis["decision_status"] != "settled"
        or not analysis["proof_plan"]
        or any(not analysis[name] for name in readiness_fields)
    ):
        raise ReportError("implementation readiness requires a settled comparison and proof plan")
    return {
        "version": MANIFEST_VERSION,
        "expected_report_sha256": _sha(
            raw["expected_report_sha256"], "Analyze expected_report_sha256"
        ),
        "candidate_id": _identifier(raw["candidate_id"], "Analyze candidate_id"),
        "current_source_validity": validity,
        "last_verified_identity": _text(
            raw["last_verified_identity"], "Analyze last_verified_identity"
        ),
        "source_trace": _text_list(raw["source_trace"], "Analyze source_trace", allow_empty=False),
        "state": state,
        "analysis": analysis,
        "tracker": tracker,
        "next_owner": normalized_owner,
        "member_ids": _text_list(raw["member_ids"], "Analyze member_ids", allow_empty=False),
        "finding_transitions": transitions,
    }


def _normalize_close_manifest(raw: dict[str, Any]) -> dict[str, Any]:
    required = {
        "version",
        "expected_report_sha256",
        "completion_route",
        "implementation_outcome",
        "report",
        "run_id",
        "subsystem_id",
        "candidate_id",
        "commit_identity",
        "commit_tree_identity",
        "current_source_result",
        "accepted_proof",
        "skipped_checks",
        "changed_scope",
        "change_closure",
        "residual_risk",
        "last_verified_identity",
        "candidate_bundle_sha256",
        "finding_transitions",
    }
    route_fields = {
        "tracker_mutation_identity",
        "ready_issue_url",
        "tracker_provider",
        "parent_ref",
        "issue_refs",
        "ready_issue_ref",
        "tracker_completion_sha256",
        "direct_implementation_authority",
    }
    review_fields = {"formal_review_decision", "formal_review_provenance"}
    legacy_fields = {"repair_generations_used"}
    _strict(raw, required, route_fields | review_fields | legacy_fields, "Close manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"Close manifest requires version {MANIFEST_VERSION}")
    route = _text(raw["completion_route"], "Close completion_route")
    supplied_route_fields = set(raw) & route_fields
    if route in {"tracker-frontier", "local-markdown-recovery"}:
        hosted_fields = {"tracker_mutation_identity", "ready_issue_url"}
        local_fields = {
            "tracker_mutation_identity",
            "tracker_provider",
            "parent_ref",
            "issue_refs",
            "ready_issue_ref",
            "tracker_completion_sha256",
        }
        if route == "tracker-frontier" and supplied_route_fields == hosted_fields:
            ready_issue_url = _text(raw["ready_issue_url"], "Close ready_issue_url")
            if re.fullmatch(r"https://[^\s]+", ready_issue_url) is None:
                raise ReportError("Close ready_issue_url must be an absolute HTTPS URL")
            route_packet = {
                "tracker_mutation_identity": _text(
                    raw["tracker_mutation_identity"], "Close tracker_mutation_identity"
                ),
                "ready_issue_url": ready_issue_url,
            }
        elif supplied_route_fields == local_fields:
            if raw["tracker_provider"] != "local-markdown":
                raise ReportError("Local Markdown Close requires tracker_provider local-markdown")
            route_packet = {
                "tracker_mutation_identity": _text(
                    raw["tracker_mutation_identity"], "Close tracker_mutation_identity"
                ),
                "tracker_provider": "local-markdown",
                "parent_ref": _text(raw["parent_ref"], "Close parent_ref"),
                "issue_refs": _text_list(
                    raw["issue_refs"], "Close issue_refs", allow_empty=False
                ),
                "ready_issue_ref": _text(
                    raw["ready_issue_ref"], "Close ready_issue_ref"
                ),
                "tracker_completion_sha256": _sha(
                    raw["tracker_completion_sha256"],
                    "Close tracker_completion_sha256",
                ),
            }
        else:
            raise ReportError(
                f"{route} Close has mixed or incomplete tracker identity fields"
            )
    elif route == "authorized-direct-recovery":
        if supplied_route_fields != {"direct_implementation_authority"}:
            raise ReportError(
                "authorized-direct-recovery Close requires direct authority and forbids tracker fields"
            )
        route_packet = {
            "direct_implementation_authority": _text(
                raw["direct_implementation_authority"],
                "Close direct_implementation_authority",
            )
        }
    else:
        raise ReportError("Close completion_route is unsupported")
    if raw["implementation_outcome"] != "complete":
        raise ReportError("Close requires implementation_outcome complete")
    if raw["change_closure"] != "complete":
        raise ReportError("Close requires complete Change Closure")
    supplied_review_fields = set(raw) & review_fields
    if supplied_review_fields and supplied_review_fields != review_fields:
        raise ReportError("Close review decision and provenance must be supplied together")
    review_packet: dict[str, str] = {}
    if supplied_review_fields:
        if raw["formal_review_decision"] != "accepted":
            raise ReportError("Close supplied review must be accepted")
        review_packet = {
            "formal_review_decision": "accepted",
            "formal_review_provenance": _text(
                raw["formal_review_provenance"], "Close formal_review_provenance"
            ),
        }
    if "repair_generations_used" in raw:
        repairs = raw["repair_generations_used"]
        if not isinstance(repairs, int) or isinstance(repairs, bool) or repairs < 0:
            raise ReportError(
                "Close legacy repair_generations_used must be a non-negative integer"
            )
    transitions = _normalize_finding_transitions(
        raw["finding_transitions"], "Close finding_transitions"
    )
    commit = _text(raw["commit_identity"], "Close commit_identity")
    tree = _text(raw["commit_tree_identity"], "Close commit_tree_identity")
    if _GIT_ID.fullmatch(commit) is None or _GIT_ID.fullmatch(tree) is None:
        raise ReportError("Close has invalid commit or tree identity")
    current = _text(raw["current_source_result"], "Close current_source_result")
    if current not in {"current", "reachable"}:
        raise ReportError("Close current_source_result is unsupported")
    return {
        "version": MANIFEST_VERSION,
        "expected_report_sha256": _sha(raw["expected_report_sha256"], "Close expected_report_sha256"),
        "completion_route": route,
        "implementation_outcome": "complete",
        "report": _text(raw["report"], "Close report"),
        "run_id": _text(raw["run_id"], "Close run_id"),
        "subsystem_id": _identifier(raw["subsystem_id"], "Close subsystem_id"),
        "candidate_id": _identifier(raw["candidate_id"], "Close candidate_id"),
        "commit_identity": commit,
        "commit_tree_identity": tree,
        "current_source_result": current,
        "accepted_proof": _text(raw["accepted_proof"], "Close accepted_proof"),
        "skipped_checks": _text(raw["skipped_checks"], "Close skipped_checks"),
        "changed_scope": _text(raw["changed_scope"], "Close changed_scope"),
        "change_closure": "complete",
        "residual_risk": _text(raw["residual_risk"], "Close residual_risk"),
        "last_verified_identity": _text(raw["last_verified_identity"], "Close last_verified_identity"),
        "candidate_bundle_sha256": _sha(
            raw["candidate_bundle_sha256"], "Close candidate_bundle_sha256"
        ),
        "finding_transitions": transitions,
    } | review_packet | route_packet


def _validate_state(state: dict[str, Any]) -> None:
    required = {
        "state_version",
        "repository_root",
        "run_id",
        "title",
        "map_state",
        "observation_identity",
        "systems",
        "subsystems",
        "excluded",
        "coverage",
        "evidence_limits",
        "next_selection",
        "findings",
        "candidates",
        "history",
    }
    _strict(state, required, set(), "report state")
    if state["state_version"] != STATE_VERSION:
        raise ReportError(f"report state requires version {STATE_VERSION}")
    if state["map_state"] not in _MAP_STATES or _RUN_ID.fullmatch(state["run_id"]) is None:
        raise ReportError("report state has invalid map or run state")
    for field in ("systems", "subsystems", "excluded", "findings", "candidates", "history"):
        if not isinstance(state[field], list):
            raise ReportError(f"report state {field} must be a list")
    for index, system in enumerate(state["systems"]):
        item = _object(system, f"report system[{index}]")
        _strict(item, {"id", "name"}, set(), f"report system[{index}]")
    subsystem_fields = {
        "id",
        "system_id",
        "name",
        "state",
        "source_identity",
        "purpose",
        "authority",
        "callers",
        "responsibility",
        "dependencies",
        "interfaces",
        "proof_seams",
        "owned_paths",
    }
    for index, subsystem in enumerate(state["subsystems"]):
        item = _object(subsystem, f"report subsystem[{index}]")
        _strict(item, subsystem_fields, {"audit"}, f"report subsystem[{index}]")
        if item["state"] not in _SUBSYSTEM_STATES:
            raise ReportError("report state has unsupported subsystem state")
        if not isinstance(item["dependencies"], list):
            raise ReportError("report state subsystem dependencies must be a list")
        for dep_index, dependency in enumerate(item["dependencies"]):
            _strict(
                _object(dependency, f"report dependency[{dep_index}]"),
                {"id", "evidence"},
                set(),
                f"report dependency[{dep_index}]",
            )
        if "audit" not in item:
            if item["state"] != "mapped":
                raise ReportError("incomplete or audited subsystem requires Audit facts")
            continue
        if item["state"] == "mapped":
            raise ReportError("mapped subsystem forbids Audit facts")
        audit = _object(item["audit"], f"report subsystem[{index}].audit")
        _strict(
            audit,
            {
                "source_trace",
                "lenses",
                "coverage",
                "evidence_limits",
                "recommendation",
                "history",
                "skill_links",
            },
            set(),
            f"report subsystem[{index}].audit",
        )
        if _normalize_source_trace(audit["source_trace"]) != audit["source_trace"]:
            raise ReportError("report state has noncanonical Source Trace")
        if _normalize_lenses(audit["lenses"], item["state"]) != audit["lenses"]:
            raise ReportError("report state has noncanonical lens coverage")
        if _skill_links(audit["skill_links"]) != audit["skill_links"]:
            raise ReportError("report state has noncanonical skill links")
        if not isinstance(audit["history"], list):
            raise ReportError("report state Audit history must be a list")
    for index, excluded_item in enumerate(state["excluded"]):
        _strict(
            _object(excluded_item, f"report exclusion[{index}]"),
            {"path", "reason"},
            set(),
            f"report exclusion[{index}]",
        )
    for index, finding in enumerate(state["findings"]):
        item = _object(finding, f"report finding[{index}]")
        if "subsystem_id" not in item or not isinstance(item.get("history"), list):
            raise ReportError("report state finding requires subsystem ownership and history")
        current = {
            key: value
            for key, value in item.items()
            if key not in {"subsystem_id", "history"}
        }
        normalized = _normalize_finding(
            current,
            item["subsystem_id"],
            f"report finding[{index}]",
        )
        normalized["history"] = item["history"]
        if normalized != item:
            raise ReportError("report state has noncanonical finding facts")
    candidate_fields = {
        "id",
        "subsystem_id",
        "title",
        "primary_class",
        "member_ids",
        "files_modules",
        "supported_behavior",
        "problem",
        "evidence",
        "direction",
        "benefit",
        "safety_floors",
        "required_proof",
        "decision_questions",
        "strength",
        "strength_reason",
        "state",
        "current_source_validity",
        "last_verified_identity",
        "source_trace",
        "analysis",
        "tracker",
        "pickup",
        "history",
    }
    implementation_fields = {
        "commit_identity",
        "commit_tree_identity",
        "current_source_result",
        "accepted_proof",
        "skipped_checks",
        "changed_scope",
        "residual_risk",
        "last_verified_identity",
    }
    review_fields = {"formal_review_decision", "formal_review_provenance"}
    legacy_fields = {"repair_generations_used"}
    for index, candidate in enumerate(state["candidates"]):
        item = _object(candidate, f"report candidate[{index}]")
        _strict(
            item,
            candidate_fields,
            {"next_owner", "implementation"},
            f"report candidate[{index}]",
        )
        if not isinstance(item["history"], list):
            raise ReportError("report state candidate history must be a list")
        if _normalize_tracker(item["tracker"], require_local_graph=True) != item["tracker"]:
            raise ReportError("report state has noncanonical tracker facts")
        if item["analysis"]:
            if _normalize_analysis(item["analysis"]) != item["analysis"]:
                raise ReportError("report state has noncanonical candidate analysis")
        elif item["state"] != "presented":
            raise ReportError("non-presented candidate requires analysis")
        if "next_owner" in item:
            _strict(
                _object(item["next_owner"], f"report candidate[{index}].next_owner"),
                {"skill", "reason", "prerequisite", "invocation"},
                set(),
                f"report candidate[{index}].next_owner",
            )
        elif item["state"] != "presented":
            raise ReportError("non-presented candidate requires next-owner facts")
        if "implementation" in item:
            implementation = _object(
                item["implementation"], f"report candidate[{index}].implementation"
            )
            _strict(
                implementation,
                implementation_fields,
                {
                    "direct_implementation_authority",
                    "tracker_completion_sha256",
                }
                | review_fields
                | legacy_fields,
                f"report candidate[{index}].implementation",
            )
            if item["state"] != "implemented" or item["pickup"]:
                raise ReportError("implementation facts require a closed candidate")
            tracker_status = item["tracker"]["status"]
            has_direct_authority = "direct_implementation_authority" in implementation
            has_tracker_completion = "tracker_completion_sha256" in implementation
            if tracker_status in {"ready-graph", "reused"}:
                if has_direct_authority:
                    raise ReportError("tracker-frontier implementation forbids direct authority")
                local = item["tracker"].get("provider") == "local-markdown"
                if local != has_tracker_completion:
                    raise ReportError(
                        "Local Markdown implementation requires exact tracker completion identity"
                    )
                if local:
                    _sha(
                        implementation["tracker_completion_sha256"],
                        "report tracker_completion_sha256",
                    )
            elif tracker_status in {"authority-required", "not-applicable"}:
                if not has_direct_authority or has_tracker_completion:
                    raise ReportError("direct implementation requires explicit authority")
                _text(
                    implementation["direct_implementation_authority"],
                    "report direct_implementation_authority",
                )
            else:
                raise ReportError("implemented candidate has no valid completion route")
            commit = _text(implementation["commit_identity"], "report commit_identity")
            tree = _text(
                implementation["commit_tree_identity"], "report commit_tree_identity"
            )
            if _GIT_ID.fullmatch(commit) is None or _GIT_ID.fullmatch(tree) is None:
                raise ReportError("report implementation has invalid commit or tree identity")
            source_result = _text(
                implementation["current_source_result"],
                "report implementation.current_source_result",
            )
            if source_result not in {"current", "reachable"}:
                raise ReportError("report implementation has invalid current-source result")
            supplied_review_fields = set(implementation) & review_fields
            if supplied_review_fields and supplied_review_fields != review_fields:
                raise ReportError(
                    "report implementation review decision and provenance must be supplied together"
                )
            if supplied_review_fields:
                if implementation["formal_review_decision"] != "accepted":
                    raise ReportError("report implementation supplied review must be accepted")
                _text(
                    implementation["formal_review_provenance"],
                    "report implementation.formal_review_provenance",
                )
            if "repair_generations_used" in implementation:
                repairs = implementation["repair_generations_used"]
                if not isinstance(repairs, int) or isinstance(repairs, bool) or repairs < 0:
                    raise ReportError(
                        "report implementation has invalid legacy repair count"
                    )
            for field in (
                "accepted_proof",
                "skipped_checks",
                "changed_scope",
                "residual_risk",
                "last_verified_identity",
            ):
                _text(implementation[field], f"report implementation.{field}")
            if implementation["last_verified_identity"] != item["last_verified_identity"]:
                raise ReportError("report implementation last verified identity does not match")
        elif item["state"] == "implemented":
            raise ReportError("implemented candidate requires implementation facts")
    system_ids = {item["id"] for item in state["systems"]}
    subsystem_ids = {item["id"] for item in state["subsystems"]}
    if len(system_ids) != len(state["systems"]) or len(subsystem_ids) != len(state["subsystems"]):
        raise ReportError("report state repeats system or subsystem IDs")
    owned: set[str] = set()
    for subsystem in state["subsystems"]:
        if subsystem["system_id"] not in system_ids:
            raise ReportError("report state subsystem has unknown system")
        for dependency in subsystem["dependencies"]:
            if dependency["id"] not in subsystem_ids:
                raise ReportError("report state has unknown dependency")
            if dependency["id"] == subsystem["id"]:
                raise ReportError("report state has a self-dependency")
        for path in subsystem["owned_paths"]:
            if path in owned:
                raise ReportError("report state has duplicate path ownership")
            owned.add(path)
    excluded = {item["path"] for item in state["excluded"]}
    if len(excluded) != len(state["excluded"]) or owned & excluded:
        raise ReportError("report state has duplicate or overlapping exclusions")
    findings = {item["id"]: item for item in state["findings"]}
    candidates = {item["id"]: item for item in state["candidates"]}
    if len(findings) != len(state["findings"]) or len(candidates) != len(state["candidates"]):
        raise ReportError("report state repeats finding or candidate IDs")
    for finding in findings.values():
        if finding["subsystem_id"] not in subsystem_ids or finding["state"] not in _FINDING_STATES:
            raise ReportError("report state has invalid finding ownership or state")
    for candidate in candidates.values():
        if candidate["subsystem_id"] not in subsystem_ids or candidate["state"] not in _CANDIDATE_STATES:
            raise ReportError("report state has invalid candidate ownership or state")
        for member in candidate["member_ids"]:
            if member not in findings or findings[member]["subsystem_id"] != candidate["subsystem_id"]:
                raise ReportError("candidate references an unknown or foreign finding")


def _state_json_for_html(state: dict[str, Any]) -> tuple[str, str]:
    data = _canonical_json(state)
    digest = _digest(data)
    safe = data.decode("utf-8").replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    return safe, digest


def _list_html(values: Sequence[str], *, empty: str = "None recorded") -> str:
    if not values:
        return f'<p class="muted">{escape(empty)}</p>'
    return "<ul>" + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ul>"


def _dl(fields: Sequence[tuple[str, object]]) -> str:
    parts: list[str] = []
    for label, value in fields:
        if isinstance(value, list):
            rendered = _list_html([str(item) for item in value])
        elif isinstance(value, bool):
            rendered = "yes" if value else "no"
        else:
            rendered = escape(
                "None recorded" if value is None or value == "" else str(value)
            )
        parts.append(f"<dt>{escape(label)}</dt><dd>{rendered}</dd>")
    return "<dl>" + "".join(parts) + "</dl>"


def _map_svg(subsystems: list[dict[str, Any]]) -> str:
    ordered = sorted(subsystems, key=lambda item: item["id"])
    width = max(960, 310 * max(1, min(4, len(ordered))))
    rows = (len(ordered) + 3) // 4
    height = max(190, rows * 165)
    positions: dict[str, tuple[int, int]] = {}
    nodes: list[str] = []
    for index, subsystem in enumerate(ordered):
        column = index % 4
        row = index // 4
        x = 30 + column * 300
        y = 35 + row * 165
        positions[subsystem["id"]] = (x, y)
    edges: list[str] = []
    for subsystem in ordered:
        x1, y1 = positions[subsystem["id"]]
        for dependency in subsystem["dependencies"]:
            x2, y2 = positions[dependency["id"]]
            edges.append(
                f'<line class="edge" x1="{x1 + 120}" y1="{y1 + 55}" '
                f'x2="{x2 + 120}" y2="{y2 + 55}"><title>'
                f"{escape(subsystem['name'])} depends on "
                f"{escape(next(item['name'] for item in ordered if item['id'] == dependency['id']))}"
                f": {escape('; '.join(dependency['evidence']))}</title></line>"
            )
    for subsystem in ordered:
        x, y = positions[subsystem["id"]]
        count = len(subsystem["owned_paths"])
        nodes.append(
            f'<a class="node" id="map-node-{subsystem["id"]}" '
            f'href="#subsystem-{subsystem["id"]}" '
            f'data-subsystem-id="{subsystem["id"]}" data-state="{subsystem["state"]}" '
            f'aria-label="{escape(subsystem["name"], quote=True)}; {subsystem["state"]}">'
            f'<rect class="state-{subsystem["state"]}" x="{x}" y="{y}" width="240" height="110"/>'
            f'<text x="{x + 120}" y="{y + 45}"><tspan x="{x + 120}">{escape(subsystem["name"])}</tspan>'
            f'<tspan x="{x + 120}" dy="28">{subsystem["state"]} · {count} '
            f'{"file" if count == 1 else "files"}</tspan></text></a>'
        )
    return (
        f'<div class="map-wrap"><svg viewBox="0 0 {width} {height}" '
        'role="img" aria-label="Repository relationship map">'
        + "".join(edges)
        + "".join(nodes)
        + "</svg></div>"
    )


def _dependency_table(subsystems: list[dict[str, Any]]) -> str:
    names = {item["id"]: item["name"] for item in subsystems}
    rows = [
        "<tr>"
        f"<td>{escape(subsystem['name'])}</td>"
        f"<td>{escape(names[dependency['id']])}</td>"
        f"<td>{escape('; '.join(dependency['evidence']))}</td></tr>"
        for subsystem in sorted(subsystems, key=lambda item: item["id"])
        for dependency in subsystem["dependencies"]
    ]
    if not rows:
        return '<p class="muted">No dependency edges recorded.</p>'
    return (
        '<div class="table-wrap"><table><caption>Dependency evidence</caption>'
        '<thead><tr><th>Source</th><th>Depends on</th><th>Evidence</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def _finding_html(finding: dict[str, Any]) -> str:
    return (
        f'<article id="finding-{finding["id"]}" data-finding-id="{finding["id"]}" '
        f'data-subsystem-id="{finding["subsystem_id"]}" data-state="{finding["state"]}">'
        f'<h4>{escape(finding["title"])} <span class="status">{escape(finding["state"])}</span></h4>'
        + _dl(
            (
                ("Kind", finding["kind"]),
                ("Primary class", finding["primary_class"]),
                ("Severity", finding["severity"]),
                ("Location", finding["location"]),
                ("Expectation", finding["expectation"]),
                ("Evidence", finding["evidence"]),
                ("Impact or cost", finding["impact"]),
                ("Direction", finding["direction"]),
                ("Proof", finding["proof"]),
                ("Confidence", finding["confidence"]),
            )
        )
        + ("<h5>History</h5>" + _list_html([json.dumps(item, ensure_ascii=False, sort_keys=True) for item in finding["history"]]) if finding["history"] else "")
        + "</article>"
    )


def _candidate_html(candidate: dict[str, Any]) -> str:
    tracker = candidate["tracker"]
    pickup = candidate.get("pickup", "")
    fields: list[tuple[str, object]] = [
        ("Primary class", candidate["primary_class"]),
        ("Strength", candidate["strength"]),
        ("State", candidate["state"]),
        ("Members", candidate["member_ids"]),
        ("Files and modules", candidate["files_modules"]),
        ("Supported behavior", candidate["supported_behavior"]),
        ("Problem", candidate["problem"]),
        ("Evidence", candidate["evidence"]),
        ("Direction", candidate["direction"]),
        ("Benefit", candidate["benefit"]),
        ("Safety floors", candidate["safety_floors"]),
        ("Required proof", candidate["required_proof"]),
        ("Decision questions", candidate["decision_questions"]),
        ("Current-source validity", candidate["current_source_validity"]),
        ("Last verified", candidate["last_verified_identity"]),
        ("Tracker", tracker["status"]),
        ("Issues", tracker["issue_urls"]),
    ]
    if tracker.get("provider") == "local-markdown":
        fields.extend(
            (
                ("Tracker Provider", tracker["provider"]),
                ("Tracker Parent", tracker["parent_ref"]),
                ("Tracker Items", tracker["issue_refs"]),
                ("Ready Tracker Item", tracker["ready_issue_ref"]),
                ("Tracker Frontier", tracker["frontier"]),
            )
        )
    if candidate["analysis"]:
        for name, value in sorted(candidate["analysis"].items()):
            fields.append((name.replace("_", " ").title(), value))
    if candidate.get("implementation"):
        if "direct_implementation_authority" in candidate["implementation"]:
            fields.append(("Completion Route", "authorized-direct-recovery"))
        for name, value in sorted(candidate["implementation"].items()):
            fields.append((name.replace("_", " ").title(), value))
    return (
        f'<article id="candidate-{candidate["id"]}" data-candidate-id="{candidate["id"]}" '
        f'data-subsystem-id="{candidate["subsystem_id"]}" data-state="{candidate["state"]}" '
        f'data-strength="{escape(candidate["strength"], quote=True)}">'
        f'<h4>{escape(candidate["title"])} <span class="status">{escape(candidate["state"])}</span></h4>'
        + _dl(fields)
        + (f"<h5>Next pickup</h5><code>{escape(pickup)}</code>" if pickup else "")
        + ("<h5>History</h5>" + _list_html([json.dumps(item, ensure_ascii=False, sort_keys=True) for item in candidate["history"]]) if candidate["history"] else "")
        + "</article>"
    )


def _render_html(state: dict[str, Any]) -> bytes:
    _validate_state(state)
    embedded, state_digest = _state_json_for_html(state)
    subsystems = sorted(state["subsystems"], key=lambda item: item["id"])
    systems = []
    for system in sorted(state["systems"], key=lambda item: item["id"]):
        members = [item for item in subsystems if item["system_id"] == system["id"]]
        systems.append(
            f'<section id="system-{system["id"]}"><h2>{escape(system["name"])}</h2>'
            + _list_html(
                [
                    f"{item['name']} — {item['state']} — {len(item['owned_paths'])} files"
                    for item in members
                ]
            )
            + "</section>"
        )
    findings_by_subsystem = {
        identifier: [item for item in state["findings"] if item["subsystem_id"] == identifier]
        for identifier in (item["id"] for item in subsystems)
    }
    candidates_by_subsystem = {
        identifier: [item for item in state["candidates"] if item["subsystem_id"] == identifier]
        for identifier in (item["id"] for item in subsystems)
    }
    details: list[str] = []
    for subsystem in subsystems:
        audit = subsystem.get("audit")
        narrative = ""
        if audit:
            trace = audit["source_trace"]
            lens_rows = "".join(
                "<tr>"
                f"<td>{escape(item['class'])}</td>"
                f"<td>{escape(item['applicability'])}</td>"
                f"<td>{escape(item['coverage'])}</td>"
                f"<td>{escape('; '.join(item['evidence']))}</td>"
                f"<td>{escape('; '.join(item['item_ids']) or 'none')}</td>"
                f"<td>{'yes' if item['detailed_owner_loaded'] else 'no'}</td>"
                f"<td>{escape(item['reason'])}</td></tr>"
                for item in audit["lenses"]
            )
            narrative = (
                "<h3>Current Source Trace</h3>"
                + _dl(
                    (
                        ("Summary", trace["summary"]),
                        ("Authority", trace["authority"]),
                        ("Entry points", trace["entry_points"]),
                        ("Callers", trace["callers"]),
                        ("Responsibility", trace["responsibility"]),
                        ("Dependencies", trace["dependencies"]),
                        ("Interfaces", trace["interfaces"]),
                        ("Proof seams", trace["proof_seams"]),
                        ("Scenarios", trace["scenarios"]),
                        ("Coverage", audit["coverage"]),
                        ("Evidence limits", audit["evidence_limits"]),
                        ("Recommendation", audit["recommendation"]),
                    )
                )
                + '<div class="table-wrap"><table><caption>Six-lens coverage</caption>'
                "<thead><tr><th>Class</th><th>Applicability</th><th>Coverage</th>"
                "<th>Evidence</th><th>Items</th><th>Owner loaded</th><th>Reason</th></tr></thead>"
                f"<tbody>{lens_rows}</tbody></table></div>"
            )
        finding_cards = "".join(
            _finding_html(item) for item in sorted(findings_by_subsystem[subsystem["id"]], key=lambda item: item["id"])
        )
        candidate_cards = "".join(
            _candidate_html(item) for item in sorted(candidates_by_subsystem[subsystem["id"]], key=lambda item: item["id"])
        )
        details.append(
            f'<section id="subsystem-{subsystem["id"]}" data-subsystem-id="{subsystem["id"]}" '
            f'data-state="{subsystem["state"]}" data-source-identity="{escape(subsystem["source_identity"], quote=True)}">'
            f'<h2>{escape(subsystem["name"])} <span class="status">{subsystem["state"]}</span></h2>'
            + _dl(
                (
                    ("Purpose", subsystem["purpose"]),
                    ("Authority", subsystem["authority"]),
                    ("Callers", subsystem["callers"]),
                    ("Responsibility", subsystem["responsibility"]),
                    ("Dependencies", [item["id"] for item in subsystem["dependencies"]]),
                    ("Interfaces", subsystem["interfaces"]),
                    ("Proof seams", subsystem["proof_seams"]),
                    ("Owned paths", subsystem["owned_paths"]),
                )
            )
            + narrative
            + "<h3>Findings</h3>"
            + (finding_cards or '<p class="muted">None recorded.</p>')
            + "<h3>Candidates</h3>"
            + (candidate_cards or '<p class="muted">None recorded.</p>')
            + "</section>"
        )
    candidate_counts = {item: 0 for item in _CANDIDATE_STATES}
    finding_counts = {item: 0 for item in _FINDING_STATES}
    for candidate in state["candidates"]:
        candidate_counts[candidate["state"]] += 1
    for finding in state["findings"]:
        finding_counts[finding["state"]] += 1
    progress = (
        "Candidates: "
        + ", ".join(f"{key} {value}" for key, value in candidate_counts.items())
        + ". Findings: "
        + ", ".join(f"{key} {value}" for key, value in finding_counts.items())
        + "."
    )
    html = f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="audit-codebase-report-version" content="{REPORT_VERSION}">
<title>{escape(state["title"])}</title>
<style>{_STYLE}</style>
</head>
<body>
<header id="report-header" data-repository-root="{escape(state["repository_root"], quote=True)}"
 data-run-id="{escape(state["run_id"], quote=True)}" data-map-state="{state["map_state"]}">
<h1>{escape(state["title"])}</h1>
<p class="muted">Map {state["map_state"]} · observation {escape(state["observation_identity"])}</p>
</header>
<main>
<section id="summary-map"><h2>Repository map</h2>{_map_svg(subsystems)}{_dependency_table(subsystems)}
<p>{escape(state["coverage"])}</p><p class="muted">{escape(state["evidence_limits"])}</p></section>
<div class="systems">{"".join(systems)}</div>
{"".join(details)}
<section id="summary-progress"><h2>Progress</h2><p>{escape(progress)}</p>
<p><strong>Next user selection:</strong> {escape(state["next_selection"] or "none")}</p></section>
</main>
<footer id="report-footer">{escape(progress)} Release decision: none; product mutation authority: none;
downstream execution: none; next selection authority: user.</footer>
<script id="audit-codebase-state" type="application/json" data-sha256="{state_digest}">{embedded}</script>
</body>
</html>
"""
    return html.encode("utf-8")


def _load_report(repo_root: Path, report: Path) -> tuple[Path, Path, bytes, dict[str, Any]]:
    root, canonical = _report_path(repo_root, report, must_exist=True)
    try:
        data = canonical.read_bytes()
        source = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ReportError(f"report is not readable UTF-8: {exc}") from exc
    version = re.findall(
        r'<meta name="audit-codebase-report-version" content="([^"]+)">', source
    )
    if version != [str(REPORT_VERSION)]:
        raise ReportError(
            f"report structural version is unsupported; version {REPORT_VERSION} is required"
        )
    matches = list(_STATE_PATTERN.finditer(source))
    if len(matches) != 1:
        raise ReportError("report requires one canonical JSON state block")
    try:
        state_data = unescape(matches[0].group(2)).encode("utf-8")
        state = _object(json.loads(state_data.decode("utf-8")), "embedded report state")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReportError(f"embedded report state is invalid: {exc}") from exc
    if _digest(_canonical_json(state)) != matches[0].group(1):
        raise ReportError("embedded report state digest does not match")
    _validate_state(state)
    if state["repository_root"] != str(root) or state["run_id"] != canonical.parent.name:
        raise ReportError("embedded repository or run identity does not match")
    if _render_html(state) != data:
        raise ReportError("report is not the canonical projection of its JSON state")
    return root, canonical, data, state


def _upsert(records: list[dict[str, Any]], incoming: list[dict[str, Any]], label: str) -> None:
    positions = {item["id"]: index for index, item in enumerate(records)}
    for item in incoming:
        if item["id"] in positions:
            prior = records[positions[item["id"]]]
            if prior["subsystem_id"] != item["subsystem_id"]:
                raise ReportError(f"{label} {item['id']!r} cannot change subsystem")
            item["history"] = _prior_record_history(prior)
            records[positions[item["id"]]] = item
        else:
            records.append(item)
    records.sort(key=lambda item: item["id"])


def _prior_record_history(record: dict[str, Any]) -> list[dict[str, Any]]:
    return list(record["history"]) + [
        {key: value for key, value in record.items() if key != "history"}
    ]


def _reduce_audit(state: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    subsystem = next(
        (item for item in state["subsystems"] if item["id"] == packet["subsystem_id"]),
        None,
    )
    if subsystem is None:
        raise ReportError(f"subsystem not found: {packet['subsystem_id']}")
    if any(
        candidate["subsystem_id"] == packet["subsystem_id"]
        and candidate["state"] == "analyzed"
        for candidate in state["candidates"]
    ):
        raise ReportError("Audit may not rewrite a subsystem with an analyzed candidate")
    audit_history = list(subsystem["audit"]["history"]) if "audit" in subsystem else []
    previous = {
        "state": subsystem["state"],
        "source_identity": subsystem["source_identity"],
        "audit": (
            {
                key: value
                for key, value in subsystem["audit"].items()
                if key != "history"
            }
            if "audit" in subsystem
            else None
        ),
    }
    audit_history.append(previous)
    subsystem["state"] = packet["state"]
    subsystem["source_identity"] = packet["source_identity"]
    subsystem["audit"] = {
        "source_trace": packet["source_trace"],
        "lenses": packet["lenses"],
        "coverage": packet["coverage"],
        "evidence_limits": packet["evidence_limits"],
        "recommendation": packet["recommendation"],
        "history": audit_history,
        "skill_links": packet["skill_links"],
    }
    existing_findings = {item["id"]: item for item in state["findings"]}
    lifecycle_changes = sorted(
        item["id"]
        for item in packet["findings"]
        if item["id"] in existing_findings
        and item["state"] != existing_findings[item["id"]]["state"]
    )
    if lifecycle_changes:
        raise ReportError(
            "Audit may not change existing finding lifecycle states: "
            + ", ".join(lifecycle_changes)
        )
    _upsert(state["findings"], packet["findings"], "finding")
    known_findings = {item["id"]: item for item in state["findings"]}
    for candidate in packet["candidates"]:
        for member in candidate["member_ids"]:
            if member not in known_findings:
                raise ReportError(f"candidate {candidate['id']!r} references unknown finding")
    existing_candidate_ids = {item["id"] for item in state["candidates"]}
    repeated_candidates = sorted(
        item["id"] for item in packet["candidates"] if item["id"] in existing_candidate_ids
    )
    if repeated_candidates:
        raise ReportError(
            "Audit may only present new candidate IDs; Analyze owns existing candidates: "
            + ", ".join(repeated_candidates)
        )
    state["candidates"].extend(packet["candidates"])
    state["candidates"].sort(key=lambda item: item["id"])
    state["next_selection"] = (
        "Select one presented candidate to Analyze."
        if packet["candidates"]
        else "Select another mapped subsystem to Audit."
    )
    state["history"].append(
        {
            "operation": "audit",
            "subsystem_id": packet["subsystem_id"],
            "source_identity": packet["source_identity"],
        }
    )
    _validate_state(state)
    return state


def _reduce_analyze(
    state: dict[str, Any],
    packet: dict[str, Any],
    report: Path,
    root: Path,
) -> dict[str, Any]:
    candidate = next(
        (item for item in state["candidates"] if item["id"] == packet["candidate_id"]),
        None,
    )
    if candidate is None:
        raise ReportError(f"candidate not found: {packet['candidate_id']}")
    subsystem = next(item for item in state["subsystems"] if item["id"] == candidate["subsystem_id"])
    if subsystem["state"] != "audited":
        raise ReportError("Analyze requires a candidate in an audited subsystem")
    if candidate["state"] in {"implemented", "disproved"}:
        raise ReportError("terminal candidate may not be analyzed")
    candidate_digest = _candidate_bundle_sha256(state, candidate)
    findings = {item["id"]: item for item in state["findings"]}
    for member in packet["member_ids"]:
        if member not in findings or findings[member]["subsystem_id"] != candidate["subsystem_id"]:
            raise ReportError("Analyze member_ids contain an unknown or foreign finding")
    if not any(findings[member]["kind"] in {"defect", "opportunity"} for member in packet["member_ids"]):
        raise ReportError("Analyze candidate may not become gap/retain-only")
    prior_members = set(candidate["member_ids"])
    if packet["current_source_validity"] == "confirmed" and packet["member_ids"] != candidate["member_ids"]:
        raise ReportError("confirmed Analyze must preserve the exact candidate boundary")
    tracker = packet["tracker"]
    tracker_published = tracker["status"] != "not-applicable"
    if packet["current_source_validity"] == "changed" and tracker_published:
        raise ReportError("changed candidate evidence requires a new Analyze selection before publication")
    if tracker["status"] in {"ready-graph", "reused", "recovery"}:
        if tracker["candidate_bundle_sha256"] != candidate_digest:
            raise ReportError("tracker candidate bundle does not match the selected candidate")
    if tracker.get("provider") == "local-markdown":
        tracker["graph_sha256"] = _verify_local_markdown_graph(
            root,
            tracker,
            candidate["id"],
            candidate_digest,
            phase="ready",
        )
    transitions = {item["finding_id"]: item for item in packet["finding_transitions"]}
    if not set(transitions) <= prior_members | set(packet["member_ids"]):
        raise ReportError("Analyze finding transition is outside the old or current candidate members")
    for identifier, transition in transitions.items():
        finding = findings[identifier]
        finding["history"].append(
            {"state": finding["state"], "reason": transition["reason"]}
        )
        finding["state"] = transition["state"]
    candidate["history"] = _prior_record_history(candidate)
    candidate["member_ids"] = packet["member_ids"]
    candidate["current_source_validity"] = packet["current_source_validity"]
    candidate["last_verified_identity"] = packet["last_verified_identity"]
    candidate["source_trace"] = packet["source_trace"]
    candidate["state"] = packet["state"]
    candidate["analysis"] = packet["analysis"]
    candidate["tracker"] = packet["tracker"]
    if packet["state"] in {"disproved"}:
        candidate["pickup"] = ""
    elif tracker["status"] in {"ready-graph", "reused"}:
        links = subsystem["audit"]["skill_links"]
        ready_identity = tracker.get("ready_issue_ref", tracker["ready_issue_url"])
        candidate["pickup"] = (
            f"[$implement]({links['implement']}) tracker item {ready_identity} "
            f"for audit candidate {candidate['id']} from {report.as_posix()}. Return, but do not "
            f"invoke, [$audit-codebase]({links['audit_codebase']}) Close with matching report, "
            "run, subsystem, and candidate identities; "
            "implementation outcome; candidate-bundle digest; tracker mutation identity and Ready "
            "tracker item identity; commit and tree identities; current-source result; accepted proof and "
            "skipped checks; formal-review decision and provenance when activated; "
            "changed scope; Change Closure; residual risk; last verified identity; and one proposed "
            "state-and-reason transition for every active member finding."
        )
    elif tracker["status"] in {"recovery", "authority-required"}:
        links = subsystem["audit"]["skill_links"]
        candidate["pickup"] = _analyze_pickup(candidate["id"], report, links)
    elif packet["state"] in {"blocked", "decision pending"}:
        links = subsystem["audit"]["skill_links"]
        candidate["pickup"] = _analyze_pickup(candidate["id"], report, links)
    else:
        candidate["pickup"] = packet["next_owner"]["invocation"]
    candidate["next_owner"] = packet["next_owner"]
    state["next_selection"] = (
        candidate["pickup"] if candidate["pickup"] else "Select another report item."
    )
    state["history"].append(
        {
            "operation": "analyze",
            "candidate_id": candidate["id"],
            "source_identity": packet["last_verified_identity"],
        }
    )
    _validate_state(state)
    return state


def _verify_commit(root: Path, commit: str, tree: str, source_result: str) -> None:
    try:
        actual_tree = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "show", "-s", "--format=%T", commit],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        head = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        reachable = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=root,
            capture_output=True,
        ).returncode == 0
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReportError(f"Close cannot verify implementation commit: {exc}") from exc
    if actual_tree != tree:
        raise ReportError("Close commit tree identity does not match Git")
    if source_result == "current" and commit != head:
        raise ReportError("Close claimed current commit but HEAD differs")
    if source_result == "reachable" and not reachable:
        raise ReportError("Close claimed reachable commit but Git disagrees")


def _reduce_close(
    state: dict[str, Any],
    packet: dict[str, Any],
    report: Path,
    root: Path,
) -> dict[str, Any]:
    if Path(packet["report"]).resolve() != report or packet["run_id"] != state["run_id"]:
        raise ReportError("Close report or run identity does not match")
    candidate = next(
        (item for item in state["candidates"] if item["id"] == packet["candidate_id"]),
        None,
    )
    if candidate is None or candidate["subsystem_id"] != packet["subsystem_id"]:
        raise ReportError("Close candidate or subsystem identity does not match")
    if candidate["state"] != "analyzed":
        raise ReportError("Close requires an analyzed candidate")
    tracker = candidate["tracker"]
    candidate_digest = _candidate_bundle_sha256(state, candidate)
    if packet["candidate_bundle_sha256"] != candidate_digest:
        raise ReportError("Close candidate bundle identity does not match")
    local_tracker = False
    recovered_tracker: dict[str, Any] | None = None
    if packet["completion_route"] == "tracker-frontier":
        if (
            tracker["status"] not in {"ready-graph", "reused"}
            or tracker["read_back"] is not True
        ):
            raise ReportError(
                "tracker-frontier Close requires a read-back-verified tracker frontier"
            )
        if tracker["candidate_bundle_sha256"] != candidate_digest:
            raise ReportError("Close tracker candidate bundle identity does not match")
        if packet["tracker_mutation_identity"] != tracker["mutation_identity"]:
            raise ReportError("Close tracker mutation identity does not match")
        local_tracker = tracker.get("provider") == "local-markdown"
        if local_tracker:
            if packet.get("tracker_provider") != "local-markdown":
                raise ReportError("Local Markdown Close requires the local tracker packet")
            for field in ("parent_ref", "issue_refs", "ready_issue_ref"):
                if packet[field] != tracker[field]:
                    raise ReportError(f"Close Local Markdown {field} identity does not match")
        elif packet.get("ready_issue_url") != tracker["ready_issue_url"]:
            raise ReportError("Close Ready issue identity does not match")
    elif packet["completion_route"] == "local-markdown-recovery":
        if _https_only_local_markdown_frontier(tracker) is None:
            raise ReportError(
                "local-markdown-recovery Close requires the exact HTTPS-only recovery state"
            )
        if packet["tracker_mutation_identity"] != tracker["mutation_identity"]:
            raise ReportError("Close tracker mutation identity does not match")
        if packet.get("tracker_provider") != "local-markdown":
            raise ReportError("Local Markdown recovery requires the local tracker packet")
        local_tracker = True
    elif packet["completion_route"] == "authorized-direct-recovery":
        if tracker["status"] not in {"authority-required", "not-applicable"}:
            raise ReportError(
                "authorized-direct-recovery Close requires authority-required or not-applicable tracker state"
            )
    else:
        raise ReportError("Close completion route is unsupported")
    if packet["last_verified_identity"] != candidate["last_verified_identity"]:
        raise ReportError("Close last verified identity does not match Analyze")
    _verify_commit(
        root,
        packet["commit_identity"],
        packet["commit_tree_identity"],
        packet["current_source_result"],
    )
    if packet["completion_route"] == "local-markdown-recovery":
        recovered_tracker, completion_digest = _recover_local_markdown_tracker(
            root,
            candidate["id"],
            candidate_digest,
            tracker,
            packet["commit_identity"],
        )
        for field in ("parent_ref", "issue_refs", "ready_issue_ref"):
            if packet[field] != recovered_tracker[field]:
                raise ReportError(f"Close Local Markdown {field} identity does not match")
        if packet["tracker_completion_sha256"] != completion_digest:
            raise ReportError("Close Local Markdown completion identity does not match")
    elif local_tracker:
        completion_digest = _verify_local_markdown_commit(
            root,
            tracker,
            candidate["id"],
            candidate_digest,
            packet["commit_identity"],
        )
        if packet["tracker_completion_sha256"] != completion_digest:
            raise ReportError("Close Local Markdown completion identity does not match")
    findings = {item["id"]: item for item in state["findings"]}
    active_members = {
        identifier
        for identifier in candidate["member_ids"]
        if findings[identifier]["state"] == "active"
    }
    transitions = {item["finding_id"]: item for item in packet["finding_transitions"]}
    if set(transitions) != active_members:
        raise ReportError("Close transitions must cover every active candidate finding")
    for identifier, transition in transitions.items():
        finding = findings[identifier]
        finding["history"].append(
            {"state": finding["state"], "reason": transition["reason"]}
        )
        finding["state"] = transition["state"]
    candidate["history"] = _prior_record_history(candidate)
    if recovered_tracker is not None:
        candidate["tracker"] = recovered_tracker
    candidate["state"] = "implemented"
    candidate["pickup"] = ""
    candidate["implementation"] = {
        key: packet[key]
        for key in (
            "commit_identity",
            "commit_tree_identity",
            "current_source_result",
            "accepted_proof",
            "skipped_checks",
            "changed_scope",
            "residual_risk",
            "last_verified_identity",
        )
    }
    for key in ("formal_review_decision", "formal_review_provenance"):
        if key in packet:
            candidate["implementation"][key] = packet[key]
    if packet["completion_route"] == "authorized-direct-recovery":
        candidate["implementation"]["direct_implementation_authority"] = packet[
            "direct_implementation_authority"
        ]
    elif local_tracker:
        candidate["implementation"]["tracker_completion_sha256"] = packet[
            "tracker_completion_sha256"
        ]
    state["next_selection"] = "Select another report item."
    state["history"].append(
        {
            "operation": "close",
            "candidate_id": candidate["id"],
            "commit_identity": packet["commit_identity"],
        }
    )
    _validate_state(state)
    return state


def _prepare(
    *,
    command: str,
    repo_root: Path,
    report: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    raw = _load_json(manifest_path, f"{command} manifest")
    root, canonical = _report_path(
        repo_root,
        report,
        must_exist=command != "render-report" or report.exists(),
    )
    if command == "render-report":
        expected = _sha(raw.get("expected_report_sha256"), "Map expected_report_sha256", absent=True)
        if canonical.exists():
            _, _, current_bytes, current_state = _load_report(root, canonical)
            if current_state["findings"] or current_state["candidates"] or any(
                item.get("audit") for item in current_state["subsystems"]
            ):
                raise ReportError("Map render may not replace audit or candidate history")
            if expected != _digest(current_bytes):
                raise ReportError("report collision")
        elif expected != "absent":
            raise ReportError("new Map report requires expected_report_sha256 absent")
        source_bytes = current_bytes if canonical.exists() else None
        state = _normalize_map_manifest(raw, root, canonical)
        normalized = {"expected_report_sha256": expected}
    else:
        root, canonical, source_bytes, state = _load_report(root, canonical)
        if command == "audit-subsystem":
            normalized = _normalize_audit_manifest(raw, canonical)
        elif command == "analyze-candidate":
            normalized = _normalize_analyze_manifest(raw)
        elif command == "close-candidate":
            normalized = _normalize_close_manifest(raw)
        else:
            raise ReportError(f"unsupported mutation command: {command}")
        if normalized["expected_report_sha256"] != _digest(source_bytes):
            raise ReportError("report collision")
        state = json.loads(json.dumps(state))
        if command == "audit-subsystem":
            state = _reduce_audit(state, normalized)
        elif command == "analyze-candidate":
            state = _reduce_analyze(state, normalized, canonical, root)
        else:
            state = _reduce_close(state, normalized, canonical, root)
    output = _render_html(state)
    output_digest = _digest(output)
    state_digest = _digest(_canonical_json(state))
    source_digest = _digest(source_bytes) if source_bytes is not None else "absent"
    bundle = _digest(
        command.encode()
        + b"\0"
        + str(canonical).encode("utf-8")
        + b"\0"
        + source_digest.encode("ascii")
        + b"\0"
        + output_digest.encode("ascii")
        + b"\0"
        + state_digest.encode("ascii")
        + b"\0"
        + _canonical_json(normalized)
    )
    return {
        "_report": canonical,
        "_source": source_bytes,
        "_output": output,
        "response_version": RESPONSE_VERSION,
        "command": command,
        "ok": True,
        "report": str(canonical),
        "report_sha256": output_digest,
        "bundle_sha256": bundle,
        "state_sha256": state_digest,
        "stage": "validate",
        "mutation_started": False,
        "report_unchanged": True,
        "effect": "none",
        "report_state": "unchanged",
    }


def _publish(prepared: dict[str, Any]) -> dict[str, Any]:
    report: Path = prepared["_report"]
    source: bytes | None = prepared["_source"]
    output: bytes = prepared["_output"]
    try:
        report.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ReportError(f"cannot create report directory: {exc}", stage="render") from exc
    sibling: Path | None = None
    lock = report.with_name(report.name + ".lock")
    lock_fd: int | None = None
    try:
        try:
            lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(lock_fd, _canonical_json({"pid": os.getpid(), "report": str(report)}))
            os.fsync(lock_fd)
        except FileExistsError as exc:
            raise ReportError(
                "another report publisher holds the transaction lock",
                stage="collision-check",
                report_unchanged=False,
                report_state="unknown",
            ) from exc
        except OSError as exc:
            raise ReportError(f"cannot acquire report transaction lock: {exc}", stage="collision-check") from exc
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=report.parent,
                prefix=".report-",
                suffix=".tmp",
                delete=False,
            ) as handle:
                sibling = Path(handle.name)
                handle.write(output)
                handle.flush()
                os.fsync(handle.fileno())
            if sibling.read_bytes() != output:
                raise ReportError("atomic sibling read-back mismatch", stage="render")
        except OSError as exc:
            raise ReportError(f"cannot render atomic sibling: {exc}", stage="render") from exc
        if source is None:
            if report.exists():
                raise ReportError(
                    "report appeared concurrently",
                    stage="collision-check",
                    report_unchanged=False,
                    report_state="unknown",
                )
        else:
            try:
                current = report.read_bytes()
            except OSError as exc:
                raise ReportError(f"cannot recheck report: {exc}", stage="collision-check") from exc
            if current != source:
                raise ReportError(
                    "report changed concurrently",
                    stage="collision-check",
                    report_unchanged=False,
                    report_state="unknown",
                )
        try:
            os.replace(sibling, report)
            sibling = None
        except OSError as exc:
            unchanged = report.exists() and (source is None or report.read_bytes() == source)
            raise ReportError(
                f"atomic replacement failed: {exc}",
                stage="replace",
                mutation_started=True,
                report_unchanged=unchanged,
                report_state="unchanged" if unchanged else "unknown",
            ) from exc
        try:
            published = report.read_bytes()
        except OSError as exc:
            raise ReportError(
                f"published report read-back failed: {exc}",
                stage="read-back",
                mutation_started=True,
                report_unchanged=False,
                report_state="unknown",
            ) from exc
        if published != output:
            raise ReportError(
                "published report read-back mismatch",
                stage="read-back",
                mutation_started=True,
                report_unchanged=False,
                report_state="unknown",
            )
    finally:
        if lock_fd is not None:
            try:
                os.close(lock_fd)
            except OSError:
                pass
            try:
                lock.unlink(missing_ok=True)
            except OSError:
                pass
        if sibling is not None:
            try:
                sibling.unlink(missing_ok=True)
            except OSError:
                pass
    return {
        key: value for key, value in prepared.items() if not key.startswith("_")
    } | {
        "stage": "read-back",
        "mutation_started": True,
        "report_unchanged": False,
        "effect": "created" if source is None else "replaced",
        "report_state": "updated",
    }


def mutate_report(
    *,
    command: str,
    repo_root: Path,
    report: Path,
    manifest_path: Path,
    validate_only: bool,
    expected_bundle_sha256: str | None,
) -> dict[str, Any]:
    prepared = _prepare(
        command=command,
        repo_root=repo_root,
        report=report,
        manifest_path=manifest_path,
    )
    if validate_only:
        return {key: value for key, value in prepared.items() if not key.startswith("_")}
    if expected_bundle_sha256 is None:
        raise ReportError("publication requires --expected-bundle-sha256")
    if expected_bundle_sha256 != prepared["bundle_sha256"]:
        raise ReportError("publication bundle collision")
    return _publish(prepared)


def inspect_report(
    *,
    repo_root: Path,
    report: Path,
    objective: str,
    subsystem_id: str | None = None,
    candidate_id: str | None = None,
) -> dict[str, Any]:
    _, canonical, data, state = _load_report(repo_root, report)
    result: dict[str, Any] = {
        "response_version": RESPONSE_VERSION,
        "command": "inspect",
        "ok": True,
        "report": str(canonical),
        "report_version": REPORT_VERSION,
        "state_version": STATE_VERSION,
        "sha256": _digest(data),
        "run_id": state["run_id"],
        "map_state": state["map_state"],
        "objective": objective,
    }
    if objective == "map":
        if subsystem_id or candidate_id:
            raise ReportError("Map inspection accepts no selected ID")
        result["state"] = state
    elif objective == "audit":
        if not subsystem_id or candidate_id:
            raise ReportError("Audit inspection requires one subsystem ID")
        subsystem = next((item for item in state["subsystems"] if item["id"] == subsystem_id), None)
        if subsystem is None:
            raise ReportError(f"subsystem not found: {subsystem_id}")
        if state["map_state"] != "complete" or subsystem["state"] not in {"mapped", "incomplete", "audited"}:
            raise ReportError("subsystem is not admissible for Audit")
        result["subsystem"] = subsystem
        result["findings"] = [item for item in state["findings"] if item["subsystem_id"] == subsystem_id]
        result["candidates"] = [item for item in state["candidates"] if item["subsystem_id"] == subsystem_id]
    elif objective in {"analyze", "close"}:
        if not candidate_id or subsystem_id:
            raise ReportError(f"{objective.capitalize()} inspection requires one candidate ID")
        candidate = next((item for item in state["candidates"] if item["id"] == candidate_id), None)
        if candidate is None:
            raise ReportError(f"candidate not found: {candidate_id}")
        allowed = (
            {"presented", "decision pending", "analyzed", "blocked"}
            if objective == "analyze"
            else {"analyzed"}
        )
        if candidate["state"] not in allowed:
            raise ReportError(f"candidate state {candidate['state']!r} is not admissible for {objective}")
        candidate_digest = _candidate_bundle_sha256(state, candidate)
        if objective == "close":
            tracker = candidate["tracker"]
            tracker_status = tracker["status"]
            if tracker_status in {"ready-graph", "reused"}:
                if tracker.get("provider") == "local-markdown":
                    result["tracker_completion_sha256"] = _verify_local_markdown_commit(
                        Path(state["repository_root"]),
                        tracker,
                        candidate["id"],
                        candidate_digest,
                        "HEAD",
                    )
                result["completion_route"] = "tracker-frontier"
            elif _https_only_local_markdown_frontier(tracker) is not None:
                recovered, completion_digest = _recover_local_markdown_tracker(
                    Path(state["repository_root"]),
                    candidate["id"],
                    candidate_digest,
                    tracker,
                    "HEAD",
                )
                result["completion_route"] = "local-markdown-recovery"
                result["tracker_completion_sha256"] = completion_digest
                result["recovered_tracker"] = recovered
            elif tracker_status in {"authority-required", "not-applicable"}:
                result["completion_route"] = "authorized-direct-recovery"
            else:
                raise ReportError("candidate has no admissible Close completion route")
        result["candidate"] = candidate
        result["candidate_bundle_sha256"] = candidate_digest
        result["member_findings"] = [
            item for item in state["findings"] if item["id"] in candidate["member_ids"]
        ]
        result["subsystem"] = next(
            item for item in state["subsystems"] if item["id"] == candidate["subsystem_id"]
        )
    else:
        raise ReportError(f"unsupported objective: {objective}")
    def without_history(value: object) -> object:
        if isinstance(value, dict):
            return {
                key: without_history(item)
                for key, item in value.items()
                if key != "history"
            }
        if isinstance(value, list):
            return [without_history(item) for item in value]
        return value

    return without_history(result)  # type: ignore[return-value]


def _tracked_inventory(root: Path) -> tuple[list[str], str]:
    try:
        process = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReportError(f"cannot enumerate tracked repository files: {exc}") from exc
    paths = sorted(
        _relative_path(raw.decode("utf-8"), "tracked inventory path")
        for raw in process.stdout.split(b"\0")
        if raw
    )
    digest = hashlib.sha256(b"audit-codebase-inventory-v1\0")
    for path in paths:
        candidate = root / Path(*PurePosixPath(path).parts)
        if not candidate.is_file():
            raise ReportError(f"tracked inventory path is not a current file: {path}")
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_digest(candidate.read_bytes()).encode("ascii"))
        digest.update(b"\0")
    return paths, digest.hexdigest()


def inventory(*, repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve(strict=True)
    paths, identity = _tracked_inventory(root)
    return {
        "response_version": RESPONSE_VERSION,
        "command": "inventory",
        "ok": True,
        "mode": "tracked-live-worktree",
        "paths": paths,
        "count": len(paths),
        "identity": identity,
    }


def source_identity(
    *,
    repo_root: Path,
    path_list: Path,
) -> dict[str, Any]:
    root = repo_root.resolve(strict=True)
    try:
        lines = path_list.resolve(strict=True).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ReportError(f"path list is unreadable: {exc}") from exc
    paths = sorted({_relative_path(line, "path list item") for line in lines if line.strip()})
    if not paths:
        raise ReportError("path list is empty")
    digest = hashlib.sha256(b"audit-codebase-source-v1\0")
    for path in paths:
        candidate = (root / Path(*PurePosixPath(path).parts)).resolve(strict=True)
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ReportError(f"path escapes repository: {path}") from exc
        data = candidate.read_bytes()
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_digest(data).encode("ascii"))
        digest.update(b"\0")
    return {
        "response_version": RESPONSE_VERSION,
        "command": "source-identity",
        "ok": True,
        "mode": "live-worktree",
        "paths": paths,
        "identity": digest.hexdigest(),
    }


def _schema(
    objective: str,
    completion_route: str | None = None,
    tracker_provider: str | None = None,
    reviewed: bool = False,
) -> dict[str, Any]:
    if objective != "close" and completion_route is not None:
        raise ReportError("completion_route applies only to Close schema")
    if objective not in {"analyze", "close"} and tracker_provider is not None:
        raise ReportError("tracker_provider applies only to Analyze or Close schema")
    if objective != "close" and reviewed:
        raise ReportError("reviewed applies only to Close schema")
    common = {"version": MANIFEST_VERSION, "expected_report_sha256": "<sha256>"}
    if objective == "map":
        template = common | {
            "expected_report_sha256": "absent",
            "map_state": "complete",
            "title": "",
            "observation_identity": "",
            "systems": [{"id": "", "name": ""}],
            "subsystems": [
                {
                    "id": "",
                    "system_id": "",
                    "name": "",
                    "source_identity": "",
                    "purpose": "",
                    "authority": [],
                    "callers": [],
                    "responsibility": "",
                    "dependencies": [{"id": "", "evidence": [""]}],
                    "interfaces": [],
                    "proof_seams": [],
                    "owned_paths": [],
                }
            ],
            "excluded": [{"path": "", "reason": ""}],
            "coverage": "",
            "evidence_limits": "",
            "next_selection": "",
        }
    elif objective == "audit":
        template = common | {
            "subsystem_id": "",
            "state": "audited",
            "source_identity": "",
            "source_trace": {
                "summary": "",
                "authority": [],
                "entry_points": [],
                "callers": [],
                "responsibility": "",
                "dependencies": [],
                "interfaces": [],
                "proof_seams": [],
                "scenarios": [],
            },
            "lenses": [
                {
                    "class": name,
                    "applicability": "applicable",
                    "coverage": "complete",
                    "evidence": [],
                    "item_ids": [],
                    "detailed_owner_loaded": name == "reliability",
                    "reason": "",
                }
                for name in _LENSES
            ],
            "findings": [],
            "candidates": [],
            "coverage": "",
            "evidence_limits": "",
            "recommendation": "",
            "skill_links": {
                "audit_codebase": "",
                "to_tickets": "",
                "implement": "",
            },
        }
    elif objective == "analyze":
        if tracker_provider not in {None, "local-markdown"}:
            raise ReportError("Analyze schema tracker provider is unsupported")
        template = common | {
            "candidate_id": "",
            "member_ids": [],
            "finding_transitions": [],
            "current_source_validity": "confirmed",
            "last_verified_identity": "",
            "source_trace": [],
            "state": "analyzed",
            "analysis": {
                "validity_reason": "",
                "changed_evidence_members": [],
                "current_shape_cost": "",
                "keep": "",
                "smallest_sufficient_change": "",
                "structural_change": "",
                "replacement": "",
                "recommended_direction": "",
                "rejected_alternatives": [],
                "contracts_decisions": [],
                "responsibilities_interfaces_seams": [],
                "compatibility_migration": "",
                "proof_plan": [],
                "residual_risk": "",
                "decision_status": "none",
            },
            "tracker": (
                {
                    "status": "ready-graph",
                    "issue_urls": [],
                    "ready_issue_url": "",
                    "provider": "local-markdown",
                    "parent_ref": "",
                    "issue_refs": [],
                    "ready_issue_ref": "",
                    "readiness": "ready-for-agent",
                    "blockers": [],
                    "claim_state": "unclaimed",
                    "frontier": [],
                    "candidate_bundle_sha256": "",
                    "mutation_identity": "",
                    "read_back": True,
                }
                if tracker_provider == "local-markdown"
                else {
                    "status": "not-applicable",
                    "issue_urls": [],
                    "ready_issue_url": "",
                }
            ),
            "next_owner": {"skill": "", "reason": "", "prerequisite": "", "invocation": ""},
        }
    elif objective == "close":
        if completion_route not in {
            "tracker-frontier",
            "local-markdown-recovery",
            "authorized-direct-recovery",
        }:
            raise ReportError("Close schema requires one completion_route")
        template = common | {
            "completion_route": completion_route,
            "implementation_outcome": "complete",
            "report": "",
            "run_id": "",
            "subsystem_id": "",
            "candidate_id": "",
            "commit_identity": "",
            "commit_tree_identity": "",
            "current_source_result": "current",
            "accepted_proof": "",
            "skipped_checks": "none",
            "changed_scope": "",
            "change_closure": "complete",
            "residual_risk": "",
            "last_verified_identity": "",
            "candidate_bundle_sha256": "",
            "finding_transitions": [],
        }
        if reviewed:
            template |= {
                "formal_review_decision": "accepted",
                "formal_review_provenance": "",
            }
        if completion_route == "tracker-frontier":
            if tracker_provider not in {None, "local-markdown"}:
                raise ReportError("tracker-frontier schema provider is unsupported")
            if tracker_provider == "local-markdown":
                template |= {
                    "tracker_mutation_identity": "",
                    "tracker_provider": "local-markdown",
                    "parent_ref": "",
                    "issue_refs": [],
                    "ready_issue_ref": "",
                    "tracker_completion_sha256": "",
                }
            else:
                template |= {
                    "tracker_mutation_identity": "",
                    "ready_issue_url": "",
                }
        elif completion_route == "local-markdown-recovery":
            if tracker_provider is not None:
                raise ReportError(
                    "local-markdown-recovery schema fixes its tracker provider"
                )
            template |= {
                "tracker_mutation_identity": "",
                "tracker_provider": "local-markdown",
                "parent_ref": "",
                "issue_refs": [],
                "ready_issue_ref": "",
                "tracker_completion_sha256": "",
            }
        else:
            if tracker_provider is not None:
                raise ReportError(
                    "authorized-direct-recovery schema forbids a tracker provider"
                )
            template["direct_implementation_authority"] = ""
    else:
        raise ReportError(f"unsupported schema objective: {objective}")
    return {
        "response_version": RESPONSE_VERSION,
        "command": "schema",
        "ok": True,
        "objective": objective,
        "template": template,
    }


def _parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__, add_help=True)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)

    schema = commands.add_parser("schema")
    schema.add_argument("--objective", choices=("map", "audit", "analyze", "close"), required=True)
    schema.add_argument(
        "--completion-route",
        choices=(
            "tracker-frontier",
            "local-markdown-recovery",
            "authorized-direct-recovery",
        ),
    )
    schema.add_argument("--tracker-provider", choices=("local-markdown",))
    schema.add_argument("--reviewed", action="store_true")

    def report_args(command: argparse.ArgumentParser) -> None:
        command.add_argument("--repo-root", type=Path, required=True)
        command.add_argument("--report", type=Path, required=True)

    inspect = commands.add_parser("inspect")
    report_args(inspect)
    inspect.add_argument("--objective", choices=("map", "audit", "analyze", "close"), required=True)
    inspect.add_argument("--subsystem-id")
    inspect.add_argument("--candidate-id")

    identity = commands.add_parser("source-identity")
    identity.add_argument("--repo-root", type=Path, required=True)
    identity.add_argument("--path-list", type=Path, required=True)

    inventory_command = commands.add_parser("inventory")
    inventory_command.add_argument("--repo-root", type=Path, required=True)

    for name in ("render-report", "audit-subsystem", "analyze-candidate", "close-candidate"):
        command = commands.add_parser(name)
        report_args(command)
        command.add_argument("--manifest", type=Path, required=True)
        command.add_argument("--validate-only", action="store_true")
        command.add_argument("--expected-bundle-sha256")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(argv if argv is not None else sys.argv[1:])
    command = arguments[0] if arguments else "arguments"
    try:
        args = _parser().parse_args(arguments)
        command = args.command
        if command == "schema":
            result = _schema(
                args.objective,
                args.completion_route,
                args.tracker_provider,
                args.reviewed,
            )
        elif command == "inspect":
            result = inspect_report(
                repo_root=args.repo_root,
                report=args.report,
                objective=args.objective,
                subsystem_id=args.subsystem_id,
                candidate_id=args.candidate_id,
            )
        elif command == "source-identity":
            result = source_identity(
                repo_root=args.repo_root,
                path_list=args.path_list,
            )
        elif command == "inventory":
            result = inventory(repo_root=args.repo_root)
        else:
            result = mutate_report(
                command=command,
                repo_root=args.repo_root,
                report=args.report,
                manifest_path=args.manifest,
                validate_only=args.validate_only,
                expected_bundle_sha256=args.expected_bundle_sha256,
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except ReportError as exc:
        print(
            json.dumps(
                {
                    "response_version": RESPONSE_VERSION,
                    "command": command,
                    "ok": False,
                    "error": str(exc),
                    "stage": exc.stage,
                    "mutation_started": exc.mutation_started,
                    "report_unchanged": exc.report_unchanged,
                    "report_state": exc.report_state,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    except Exception as exc:  # defensive JSON-only CLI boundary
        publication_attempt = command in {
            "render-report",
            "audit-subsystem",
            "analyze-candidate",
            "close-candidate",
        } and "--validate-only" not in arguments
        print(
            json.dumps(
                {
                    "response_version": RESPONSE_VERSION,
                    "command": command,
                    "ok": False,
                    "error": f"unexpected helper failure: {exc}",
                    "stage": "internal",
                    "mutation_started": publication_attempt,
                    "report_unchanged": not publication_attempt,
                    "report_state": "unknown" if publication_attempt else "unchanged",
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
