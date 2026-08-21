"""Deterministic HTML map for Map, subsystem Audit, and candidate Analyze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from html import escape, unescape
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

REPORT_VERSION, STATE_VERSION, RESPONSE_VERSION, MANIFEST_VERSION = 11, 3, 1, 5
_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_RUN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_SHA = re.compile(r"[0-9a-f]{64}")
_LENSES = (
    "reliability",
    "domain",
    "design",
    "simplification",
    "coding practice",
    "performance",
)
_LENS_STATES = {"complete", "evidence gap", "not applicable"}
_KINDS = {"defect", "opportunity", "gap", "retained complexity"}
_STATE = re.compile(
    r'<script id="audit-codebase-state" type="application/json" data-sha256="([0-9a-f]{64})">(.*?)</script>',
    re.S,
)
_STYLE = """:root{color-scheme:dark;--bg:#0b1020;--p:#111827;--s:#172033;--t:#e5edf8;--m:#9fb0c7;--b:#34445f;--g:#22c55e;--a:#f59e0b}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--t);font:15px/1.55 system-ui}header,main,footer{width:min(1450px,calc(100% - 32px));margin:auto}header{padding:28px 0 12px}footer{padding:18px 0 36px;color:var(--m)}section,article{background:var(--p);border:1px solid var(--b);border-radius:12px;margin:14px 0;padding:18px}.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}.muted{color:var(--m)}table{width:100%;border-collapse:collapse}th,td{padding:9px;text-align:left;vertical-align:top;border-bottom:1px solid var(--b)}dl{display:grid;grid-template-columns:minmax(140px,220px) 1fr;gap:6px 14px}dt{color:var(--m);font-weight:650}dd{margin:0}.status{border:1px solid;border-radius:999px;padding:1px 8px}.audited,.complete{color:var(--g)}.evidence-gap,.incomplete{color:var(--a)}code{overflow-wrap:anywhere}@media(max-width:700px){dl{grid-template-columns:1fr}}"""


class ReportError(ValueError):
    def __init__(self, message: str, *, stage: str = "validate") -> None:
        super().__init__(message)
        self.stage = stage


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ReportError(message, stage="arguments")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _obj(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReportError(f"{label} must be an object")
    return dict(value)


def _strict(
    value: dict[str, Any], required: set[str], optional: set[str], label: str
) -> None:
    missing, unknown = (
        sorted(required - set(value)),
        sorted(set(value) - required - optional),
    )
    if missing:
        raise ReportError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise ReportError(f"{label} has unknown fields: {', '.join(unknown)}")


def _text(value: object, label: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ReportError(f"{label} must be a non-empty string")
    return value.strip()


def _texts(value: object, label: str, *, empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not empty and not value):
        raise ReportError(f"{label} must be a list")
    result = [_text(v, f"{label} item") for v in value]
    if len(result) != len(set(result)):
        raise ReportError(f"{label} contains duplicates")
    return result


def _id(value: object, label: str) -> str:
    result = _text(value, label)
    if not _ID.fullmatch(result):
        raise ReportError(f"{label} must be lowercase kebab-case")
    return result


def _rel(value: object, label: str) -> str:
    raw = _text(value, label).replace("\\", "/")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or raw in {"", "."}:
        raise ReportError(f"{label} must be repository-relative")
    return str(path)


def _json(path: Path, label: str) -> dict[str, Any]:
    try:
        return _obj(json.loads(path.read_text(encoding="utf-8")), label)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReportError(f"cannot read {label}: {exc}") from exc


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReportError(f"git {' '.join(args)} failed") from exc


def inventory(*, repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    paths = sorted(
        p.replace("\\", "/") for p in _git(root, "ls-files", "-z").split("\0") if p
    )
    h = hashlib.sha256()
    for p in paths:
        h.update(p.encode() + b"\0" + hashlib.sha256((root / p).read_bytes()).digest())
    return {
        "response_version": RESPONSE_VERSION,
        "identity": {
            "commit": _git(root, "rev-parse", "HEAD"),
            "tree": _git(root, "show", "-s", "--format=%T", "HEAD"),
            "tracked_content_sha256": h.hexdigest(),
        },
        "tracked_paths": paths,
    }


def source_identity(*, repo_root: Path, paths: Sequence[str]) -> dict[str, Any]:
    root = repo_root.resolve()
    normalized = sorted({_rel(p, "path") for p in paths})
    if not normalized:
        raise ReportError("source-identity requires paths")
    h = hashlib.sha256()
    for p in normalized:
        if not (root / p).is_file():
            raise ReportError(f"source path does not exist: {p}")
        h.update(p.encode() + b"\0" + hashlib.sha256((root / p).read_bytes()).digest())
    return {
        "response_version": RESPONSE_VERSION,
        "paths": normalized,
        "sha256": h.hexdigest(),
    }


def _report_path(root: Path, report: Path, *, exists: bool) -> Path:
    root = root.resolve()
    path = (report if report.is_absolute() else root / report).resolve()
    try:
        parts = PurePosixPath(path.relative_to(root).as_posix()).parts
    except ValueError as exc:
        raise ReportError("report must be inside repository") from exc
    if (
        len(parts) != 4
        or parts[:2] != (".tmp", "audit-codebase")
        or not _RUN.fullmatch(parts[2])
        or parts[3] != "report.html"
    ):
        raise ReportError("report must be .tmp/audit-codebase/<run-id>/report.html")
    if exists and not path.is_file():
        raise ReportError("report does not exist")
    return path


def _dependencies(value: object, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ReportError(f"{label} must be a list")
    result = []
    for i, raw in enumerate(value):
        item = _obj(raw, f"{label}[{i}]")
        _strict(item, {"id", "evidence"}, set(), f"{label}[{i}]")
        result.append(
            {
                "id": _id(item["id"], f"{label}[{i}] id"),
                "evidence": _texts(
                    item["evidence"], f"{label}[{i}] evidence", empty=False
                ),
            }
        )
    if len({x["id"] for x in result}) != len(result):
        raise ReportError(f"{label} contains duplicates")
    return result


def _subsystem(value: object, label: str) -> dict[str, Any]:
    item = _obj(value, label)
    fields = {
        "id",
        "system_id",
        "name",
        "purpose",
        "ownership",
        "authority",
        "callers",
        "dependencies",
        "interfaces",
        "proof_seams",
        "owned_paths",
    }
    _strict(item, fields, {"exclusions"}, label)
    return {
        "id": _id(item["id"], f"{label} id"),
        "system_id": _id(item["system_id"], f"{label} system_id"),
        "name": _text(item["name"], f"{label} name"),
        "purpose": _text(item["purpose"], f"{label} purpose"),
        "ownership": _text(item["ownership"], f"{label} ownership"),
        "authority": _texts(item["authority"], f"{label} authority"),
        "callers": _texts(item["callers"], f"{label} callers"),
        "dependencies": _dependencies(item["dependencies"], f"{label} dependencies"),
        "interfaces": _texts(item["interfaces"], f"{label} interfaces"),
        "proof_seams": _texts(item["proof_seams"], f"{label} proof_seams"),
        "owned_paths": [
            _rel(p, f"{label} owned path")
            for p in _texts(item["owned_paths"], f"{label} owned_paths", empty=False)
        ],
        "exclusions": _texts(item.get("exclusions", []), f"{label} exclusions"),
        "state": "mapped",
    }


def _map(raw: dict[str, Any], root: Path) -> dict[str, Any]:
    fields = {
        "version",
        "expected_report_sha256",
        "title",
        "observation_identity",
        "systems",
        "subsystems",
        "excluded",
        "coverage",
        "evidence_limits",
    }
    _strict(raw, fields, set(), "map manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"map manifest requires version {MANIFEST_VERSION}")
    if raw["expected_report_sha256"] != "absent":
        raise ReportError("new map expects absent report")
    if not isinstance(raw["systems"], list) or not raw["systems"]:
        raise ReportError("systems must not be empty")
    systems = []
    for i, v in enumerate(raw["systems"]):
        x = _obj(v, f"systems[{i}]")
        _strict(x, {"id", "name"}, set(), f"systems[{i}]")
        systems.append(
            {"id": _id(x["id"], "system id"), "name": _text(x["name"], "system name")}
        )
    if not isinstance(raw["subsystems"], list) or not raw["subsystems"]:
        raise ReportError("subsystems must not be empty")
    subs = [_subsystem(v, f"subsystems[{i}]") for i, v in enumerate(raw["subsystems"])]
    sids = [x["id"] for x in subs]
    sysids = [x["id"] for x in systems]
    if len(sids) != len(set(sids)) or len(sysids) != len(set(sysids)):
        raise ReportError("map ids must be unique")
    for sub in subs:
        if sub["system_id"] not in sysids:
            raise ReportError(f"unknown system for {sub['id']}")
        if any(d["id"] not in sids for d in sub["dependencies"]):
            raise ReportError(f"unknown dependency for {sub['id']}")
    if not isinstance(raw["excluded"], list):
        raise ReportError("excluded must be a list")
    excluded = []
    for i, v in enumerate(raw["excluded"]):
        x = _obj(v, f"excluded[{i}]")
        _strict(x, {"path", "reason"}, set(), f"excluded[{i}]")
        excluded.append(
            {
                "path": _rel(x["path"], "excluded path"),
                "reason": _text(x["reason"], "excluded reason"),
            }
        )
    tracked = set(inventory(repo_root=root)["tracked_paths"])
    owners = {}
    for sub in subs:
        for p in sub["owned_paths"]:
            if p not in tracked:
                raise ReportError(f"{sub['id']} claims untracked path {p}")
            if p in owners:
                raise ReportError(f"{p} has multiple owners")
            owners[p] = sub["id"]
    ignored = {
        p
        for p in tracked
        for x in excluded
        if p == x["path"].rstrip("/") or p.startswith(x["path"].rstrip("/") + "/")
    }
    if set(owners) & ignored:
        raise ReportError("owned and excluded paths overlap")
    missing = sorted(tracked - set(owners) - ignored)
    if missing:
        raise ReportError(
            f"tracked paths are neither owned nor excluded: {', '.join(missing)}"
        )
    identity = _obj(raw["observation_identity"], "observation_identity")
    _strict(
        identity,
        {"commit", "tree", "tracked_content_sha256"},
        set(),
        "observation_identity",
    )
    identity = {k: _text(v, f"identity {k}") for k, v in identity.items()}
    if not _SHA.fullmatch(identity["tracked_content_sha256"]):
        raise ReportError("tracked_content_sha256 must be sha256")
    if identity != inventory(repo_root=root)["identity"]:
        raise ReportError("observation_identity does not match current repository")
    return {
        "state_version": STATE_VERSION,
        "title": _text(raw["title"], "title"),
        "observation_identity": identity,
        "systems": systems,
        "subsystems": subs,
        "excluded": excluded,
        "coverage": _text(raw["coverage"], "coverage"),
        "evidence_limits": _text(raw["evidence_limits"], "evidence_limits", empty=True),
        "systemic_findings": [],
        "history": [{"operation": "map", "selection": "repository"}],
    }


def _lenses(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ReportError("lenses must be a list")
    result = []
    for i, v in enumerate(value):
        x = _obj(v, f"lenses[{i}]")
        _strict(
            x,
            {"class", "state", "evidence", "finding_ids", "reason"},
            set(),
            f"lenses[{i}]",
        )
        name = _text(x["class"], "lens class")
        state = _text(x["state"], "lens state")
        if name not in _LENSES or state not in _LENS_STATES:
            raise ReportError("unsupported lens class or state")
        evidence = _texts(x["evidence"], "lens evidence")
        if state == "complete" and not evidence:
            raise ReportError(f"complete lens {name} requires evidence")
        result.append(
            {
                "class": name,
                "state": state,
                "evidence": evidence,
                "finding_ids": [
                    _id(y, "finding id")
                    for y in _texts(x["finding_ids"], "finding ids")
                ],
                "reason": _text(x["reason"], "lens reason"),
            }
        )
    if sorted(x["class"] for x in result) != sorted(_LENSES):
        raise ReportError("lenses must contain all six classes exactly once")
    return result


def _finding(value: object, label: str) -> dict[str, Any]:
    x = _obj(value, label)
    fields = {
        "id",
        "kind",
        "primary_class",
        "title",
        "expectation",
        "locations",
        "evidence",
        "impact",
        "causal_owner",
        "affected_scope",
        "direction",
        "proof",
        "confidence",
    }
    kind_fields = {
        "severity",
        "scenario",
        "missing_evidence",
        "boundary_reason",
        "reentry",
        "protected_constraint",
        "ceiling",
        "revisit_trigger",
    }
    _strict(x, fields, kind_fields, label)
    kind = _text(x["kind"], "kind")
    primary = _text(x["primary_class"], "primary class")
    if kind not in _KINDS or primary not in _LENSES:
        raise ReportError(f"{label} has unsupported kind or class")
    result = {
        "id": _id(x["id"], "finding id"),
        "kind": kind,
        "primary_class": primary,
        "title": _text(x["title"], "title"),
        "expectation": _text(x["expectation"], "expectation", empty=True),
        "locations": _texts(x["locations"], "locations", empty=False),
        "evidence": _texts(x["evidence"], "evidence", empty=False),
        "impact": _text(x["impact"], "impact"),
        "causal_owner": _text(x["causal_owner"], "causal owner"),
        "affected_scope": _texts(x["affected_scope"], "affected scope", empty=False),
        "direction": _text(x["direction"], "direction"),
        "proof": _texts(x["proof"], "proof", empty=False),
        "confidence": _text(x["confidence"], "confidence"),
    }
    required_by_kind = {
        "defect": ("severity", "scenario"),
        "gap": ("missing_evidence", "boundary_reason", "reentry"),
        "retained complexity": (
            "protected_constraint",
            "ceiling",
            "revisit_trigger",
        ),
        "opportunity": (),
    }
    for field in required_by_kind[kind]:
        result[field] = _text(x.get(field), field)
    unexpected = kind_fields & set(x) - set(required_by_kind[kind])
    if unexpected:
        raise ReportError(
            f"{label} has fields not valid for {kind}: {', '.join(sorted(unexpected))}"
        )
    return result


def _candidate(value: object, label: str) -> dict[str, Any]:
    x = _obj(value, label)
    fields = {
        "id",
        "title",
        "primary_class",
        "finding_ids",
        "affected_scope",
        "problem",
        "evidence",
        "direction",
        "benefit",
        "risks",
        "required_proof",
    }
    _strict(x, fields, set(), label)
    primary = _text(x["primary_class"], "primary class")
    if primary not in _LENSES:
        raise ReportError("unsupported candidate class")
    return {
        "id": _id(x["id"], "candidate id"),
        "title": _text(x["title"], "title"),
        "primary_class": primary,
        "finding_ids": [
            _id(y, "finding id")
            for y in _texts(x["finding_ids"], "finding ids", empty=False)
        ],
        "affected_scope": _texts(x["affected_scope"], "affected scope", empty=False),
        "problem": _text(x["problem"], "problem"),
        "evidence": _texts(x["evidence"], "evidence", empty=False),
        "direction": _text(x["direction"], "direction"),
        "benefit": _text(x["benefit"], "benefit"),
        "risks": _texts(x["risks"], "risks"),
        "required_proof": _texts(x["required_proof"], "required proof", empty=False),
        "state": "presented",
    }


def _audit(raw: dict[str, Any]) -> dict[str, Any]:
    fields = {
        "version",
        "expected_report_sha256",
        "subsystem_id",
        "source_identity",
        "source_trace",
        "lenses",
        "findings",
        "candidates",
        "systemic_findings",
        "coverage",
        "evidence_limits",
        "recommendation",
    }
    _strict(raw, fields, set(), "audit manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"audit manifest requires version {MANIFEST_VERSION}")
    expected = _text(raw["expected_report_sha256"], "expected report sha")
    if not _SHA.fullmatch(expected):
        raise ReportError("expected report sha must be sha256")
    trace = _obj(raw["source_trace"], "source trace")
    tf = {
        "summary",
        "entry_points",
        "callers",
        "dependencies",
        "interfaces",
        "proof_seams",
        "representative_flows",
        "history_signals",
    }
    _strict(trace, tf, set(), "source trace")
    trace = {
        k: (_text(v, k) if k == "summary" else _texts(v, k)) for k, v in trace.items()
    }
    for name in ("findings", "candidates", "systemic_findings"):
        if not isinstance(raw[name], list):
            raise ReportError(f"{name} must be a list")
    findings = [_finding(v, f"findings[{i}]") for i, v in enumerate(raw["findings"])]
    systemic = [
        _finding(v, f"systemic[{i}]") for i, v in enumerate(raw["systemic_findings"])
    ]
    candidates = [
        _candidate(v, f"candidates[{i}]") for i, v in enumerate(raw["candidates"])
    ]
    fids = [x["id"] for x in findings + systemic]
    cids = [x["id"] for x in candidates]
    if len(fids) != len(set(fids)) or len(cids) != len(set(cids)):
        raise ReportError("finding and candidate ids must be unique")
    finding_by_id = {x["id"]: x for x in findings + systemic}
    lenses = _lenses(raw["lenses"])
    for lens in lenses:
        for finding_id in lens["finding_ids"]:
            finding = finding_by_id.get(finding_id)
            if finding is None:
                raise ReportError(f"lens {lens['class']} names unknown finding")
            if finding["primary_class"] != lens["class"]:
                raise ReportError(
                    f"lens {lens['class']} names finding from {finding['primary_class']}"
                )
    listed_findings = {
        finding_id for lens in lenses for finding_id in lens["finding_ids"]
    }
    omitted_findings = set(finding_by_id) - listed_findings
    if omitted_findings:
        raise ReportError(
            f"admitted findings omitted from lens ledger: {', '.join(sorted(omitted_findings))}"
        )
    for c in candidates:
        if set(c["finding_ids"]) - set(fids):
            raise ReportError(f"candidate {c['id']} names unknown findings")
        if not any(
            finding_by_id[finding_id]["kind"] in {"defect", "opportunity"}
            for finding_id in c["finding_ids"]
        ):
            raise ReportError(
                f"candidate {c['id']} requires a defect or opportunity finding"
            )
    return {
        "expected_report_sha256": expected,
        "subsystem_id": _id(raw["subsystem_id"], "subsystem id"),
        "source_identity": _source_packet(raw["source_identity"], "source identity"),
        "source_trace": trace,
        "lenses": lenses,
        "findings": findings,
        "candidates": candidates,
        "systemic_findings": systemic,
        "coverage": _text(raw["coverage"], "coverage"),
        "evidence_limits": _text(raw["evidence_limits"], "evidence limits", empty=True),
        "recommendation": _text(raw["recommendation"], "recommendation"),
    }


def _analysis(raw: dict[str, Any]) -> dict[str, Any]:
    fields = {
        "version",
        "expected_report_sha256",
        "candidate_id",
        "state",
        "question",
        "source_identity",
        "summary",
        "cause",
        "affected_scope",
        "options",
        "recommendation",
        "tradeoffs",
        "proof",
        "evidence_limits",
    }
    _strict(raw, fields, set(), "analysis manifest")
    if raw["version"] != MANIFEST_VERSION:
        raise ReportError(f"analysis manifest requires version {MANIFEST_VERSION}")
    expected = _text(raw["expected_report_sha256"], "expected report sha")
    if not _SHA.fullmatch(expected):
        raise ReportError("expected report sha must be sha256")
    state = _text(raw["state"], "state")
    question = _text(raw["question"], "question", empty=True)
    if state not in {"analyzed", "disproved", "blocked"}:
        raise ReportError("analysis state must be analyzed, disproved, or blocked")
    if state == "blocked" and not question:
        raise ReportError("blocked analysis requires an exact question")
    if state != "blocked" and question:
        raise ReportError("only blocked analysis may contain a question")
    if not isinstance(raw["options"], list) or (
        state == "analyzed" and not raw["options"]
    ):
        raise ReportError("analyzed options must not be empty")
    options = []
    for i, v in enumerate(raw["options"]):
        x = _obj(v, f"options[{i}]")
        _strict(x, {"name", "description", "tradeoffs"}, set(), f"options[{i}]")
        options.append(
            {
                "name": _text(x["name"], "option name"),
                "description": _text(x["description"], "option description"),
                "tradeoffs": _texts(x["tradeoffs"], "option tradeoffs"),
            }
        )
    return {
        "expected_report_sha256": expected,
        "candidate_id": _id(raw["candidate_id"], "candidate id"),
        "state": state,
        "question": question,
        "source_identity": _source_packet(raw["source_identity"], "source identity"),
        "summary": _text(raw["summary"], "summary"),
        "cause": _text(raw["cause"], "cause"),
        "affected_scope": _texts(raw["affected_scope"], "affected scope", empty=False),
        "options": options,
        "recommendation": _text(
            raw["recommendation"], "recommendation", empty=state != "analyzed"
        ),
        "tradeoffs": _texts(raw["tradeoffs"], "tradeoffs"),
        "proof": _texts(raw["proof"], "proof", empty=False),
        "evidence_limits": _text(raw["evidence_limits"], "evidence limits", empty=True),
    }


def _list(values: Sequence[str], empty="None recorded") -> str:
    return (
        "<ul>" + "".join(f"<li>{escape(v)}</li>" for v in values) + "</ul>"
        if values
        else f'<span class="muted">{escape(empty)}</span>'
    )


def _source_packet(value: object, label: str) -> dict[str, Any]:
    packet = _obj(value, label)
    _strict(packet, {"paths", "sha256"}, set(), label)
    paths = [
        _rel(path, f"{label} path")
        for path in _texts(packet["paths"], f"{label} paths", empty=False)
    ]
    sha = _text(packet["sha256"], f"{label} sha256")
    if not _SHA.fullmatch(sha):
        raise ReportError(f"{label} sha256 must be sha256")
    return {"paths": sorted(paths), "sha256": sha}


def _verify_source_packet(
    root: Path, packet: dict[str, Any], required_paths: Sequence[str]
) -> None:
    if set(required_paths) - set(packet["paths"]):
        raise ReportError("source_identity omits required bound source")
    expected = source_identity(repo_root=root, paths=packet["paths"])
    actual = {"paths": packet["paths"], "sha256": packet["sha256"]}
    current = {"paths": expected["paths"], "sha256": expected["sha256"]}
    if actual != current:
        raise ReportError("source_identity does not match current bound source")


def _finding_html(x: dict[str, Any]) -> str:
    details = "".join(
        f"<dt>{escape(key.replace('_', ' ').title())}</dt><dd>{escape(x[key])}</dd>"
        for key in (
            "severity",
            "scenario",
            "missing_evidence",
            "boundary_reason",
            "reentry",
            "protected_constraint",
            "ceiling",
            "revisit_trigger",
        )
        if key in x
    )
    return f'''<article data-finding-id="{escape(x["id"])}"><h3>{escape(x["title"])}</h3><p><span class="status">{escape(x["kind"])}</span> {escape(x["primary_class"])}</p><dl><dt>Expectation</dt><dd>{escape(x["expectation"])}</dd><dt>Locations</dt><dd>{_list(x["locations"])}</dd><dt>Evidence</dt><dd>{_list(x["evidence"])}</dd><dt>Impact</dt><dd>{escape(x["impact"])}</dd><dt>Causal owner</dt><dd>{escape(x["causal_owner"])}</dd><dt>Affected scope</dt><dd>{_list(x["affected_scope"])}</dd><dt>Direction</dt><dd>{escape(x["direction"])}</dd><dt>Proof</dt><dd>{_list(x["proof"])}</dd><dt>Confidence</dt><dd>{escape(x["confidence"])}</dd>{details}</dl></article>'''


def _candidate_html(x: dict[str, Any]) -> str:
    a = x.get("analysis")
    detail = ""
    if a:
        options = "".join(
            f"""<article><h5>{escape(o["name"])}</h5><p>{escape(o["description"])}</p><strong>Trade-offs</strong>{_list(o["tradeoffs"])}</article>"""
            for o in a["options"]
        )
        detail = f"""<h4>Analysis</h4><dl><dt>Summary</dt><dd>{escape(a["summary"])}</dd><dt>Cause</dt><dd>{escape(a["cause"])}</dd><dt>Affected scope</dt><dd>{_list(a["affected_scope"])}</dd><dt>Options</dt><dd>{options}</dd><dt>Recommendation</dt><dd>{escape(a["recommendation"])}</dd><dt>Trade-offs</dt><dd>{_list(a["tradeoffs"])}</dd><dt>Question</dt><dd>{escape(a["question"]) or '<span class="muted">None</span>'}</dd><dt>Proof</dt><dd>{_list(a["proof"])}</dd><dt>Evidence limits</dt><dd>{escape(a["evidence_limits"])}</dd></dl>"""
    return f'''<article data-candidate-id="{escape(x["id"])}"><h3>{escape(x["title"])}</h3><p><span class="status {escape(x["state"])}">{escape(x["state"])}</span></p><dl><dt>Findings</dt><dd>{_list(x["finding_ids"])}</dd><dt>Affected scope</dt><dd>{_list(x["affected_scope"])}</dd><dt>Problem</dt><dd>{escape(x["problem"])}</dd><dt>Evidence</dt><dd>{_list(x["evidence"])}</dd><dt>Direction</dt><dd>{escape(x["direction"])}</dd><dt>Benefit</dt><dd>{escape(x["benefit"])}</dd><dt>Risks</dt><dd>{_list(x["risks"])}</dd><dt>Required proof</dt><dd>{_list(x["required_proof"])}</dd></dl>{detail}</article>'''


def _render(state: dict[str, Any]) -> bytes:
    identity = state["observation_identity"]
    excluded = (
        "".join(
            f"<li><code>{escape(item['path'])}</code>: {escape(item['reason'])}</li>"
            for item in state["excluded"]
        )
        or '<li class="muted">None</li>'
    )
    systems = []
    for system in state["systems"]:
        subs = []
        for x in state["subsystems"]:
            if x["system_id"] != system["id"]:
                continue
            dependencies = [
                f"""<strong>{escape(d["id"])}</strong>{_list(d["evidence"])}"""
                for d in x["dependencies"]
            ]
            subs.append(
                f'''<article data-subsystem-id="{escape(x["id"])}"><h3>{escape(x["name"])}</h3><p><span class="status {x["state"]}">{x["state"]}</span> {escape(x["purpose"])}</p><dl><dt>Ownership</dt><dd>{escape(x["ownership"])}</dd><dt>Authority</dt><dd>{_list(x["authority"])}</dd><dt>Callers</dt><dd>{_list(x["callers"])}</dd><dt>Dependencies</dt><dd>{"".join(dependencies) or '<span class="muted">None recorded</span>'}</dd><dt>Interfaces</dt><dd>{_list(x["interfaces"])}</dd><dt>Proof seams</dt><dd>{_list(x["proof_seams"])}</dd><dt>Owned paths</dt><dd>{_list(x["owned_paths"])}</dd><dt>Exclusions</dt><dd>{_list(x["exclusions"])}</dd></dl></article>'''
            )
        systems.append(
            f'''<section data-system-id="{escape(system["id"])}"><h2>System: {escape(system["name"])}</h2><div class="grid">{"".join(subs)}</div></section>'''
        )
    audits = []
    candidates = []
    for sub in state["subsystems"]:
        a = sub.get("audit")
        if not a:
            continue
        rows = "".join(
            f"<tr><td>{escape(x['class'])}</td><td class='{x['state'].replace(' ', '-')}'>{x['state']}</td><td>{_list(x['evidence'])}</td><td>{escape(x['reason'])}</td></tr>"
            for x in a["lenses"]
        )
        trace_order = (
            "summary",
            "entry_points",
            "callers",
            "dependencies",
            "interfaces",
            "proof_seams",
            "representative_flows",
            "history_signals",
        )
        audits.append(
            f"""<section><h2>Audit: {escape(sub["name"])}</h2><dl>{"".join(f"<dt>{escape(k.replace("_", " ").title())}</dt><dd>{escape(a['source_trace'][k]) if isinstance(a['source_trace'][k], str) else _list(a['source_trace'][k])}</dd>" for k in trace_order)}</dl><table><tr><th>Class</th><th>Coverage</th><th>Evidence</th><th>Reason</th></tr>{rows}</table>{"".join(_finding_html(x) for x in a["findings"])}<p><strong>Coverage:</strong> {escape(a["coverage"])}</p><p><strong>Evidence limits:</strong> {escape(a["evidence_limits"])}</p><p><strong>Recommendation:</strong> {escape(a["recommendation"])}</p></section>"""
        )
        candidates.extend(a["candidates"])
    raw = _canonical(state)
    embedded = (
        raw.decode()
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="audit-codebase-report-version" content="{REPORT_VERSION}"><title>{escape(state["title"])}</title><style>{_STYLE}</style></head><body><header><h1>{escape(state["title"])}</h1><p class="muted">Durable architecture map and subsystem audit record</p></header><main><section><h2>Repository coverage</h2><p>{escape(state["coverage"])}</p><p>{escape(state["evidence_limits"])}</p><dl><dt>Commit</dt><dd><code>{escape(identity["commit"])}</code></dd><dt>Tree</dt><dd><code>{escape(identity["tree"])}</code></dd><dt>Tracked content</dt><dd><code>{escape(identity["tracked_content_sha256"])}</code></dd><dt>Excluded paths</dt><dd><ul>{excluded}</ul></dd></dl></section><section><h2>Architecture map</h2>{"".join(systems)}</section>{"".join(audits)}<section><h2>Systemic findings</h2>{"".join(_finding_html(x) for x in state["systemic_findings"]) or '<p class="muted">None admitted.</p>'}</section><section><h2>Improvement candidates</h2>{"".join(_candidate_html(x) for x in candidates) or '<p class="muted">Audit a subsystem to produce candidates.</p>'}</section><section><h2>History</h2><ol>{"".join(f"<li>{escape(x['operation'])}: {escape(x['selection'])}</li>" for x in state["history"])}</ol></section></main><footer>Audit-codebase report format {REPORT_VERSION}</footer><script id="audit-codebase-state" type="application/json" data-sha256="{_digest(raw)}">{embedded}</script></body></html>'''
    return html.encode()


def _validate_state(state: dict[str, Any]) -> None:
    if state.get("state_version") != STATE_VERSION:
        raise ReportError(f"report state requires version {STATE_VERSION}")
    sids = [x.get("id") for x in state.get("subsystems", [])]
    fids = [x.get("id") for x in state.get("systemic_findings", [])]
    cids = []
    if len(sids) != len(set(sids)):
        raise ReportError("duplicate subsystem ids")
    for sub in state.get("subsystems", []):
        if "audit" in sub:
            if sub.get("state") != "audited":
                raise ReportError("audit requires audited state")
            _lenses(sub["audit"].get("lenses"))
            fids += [x.get("id") for x in sub["audit"].get("findings", [])]
            cids += [x.get("id") for x in sub["audit"].get("candidates", [])]
    if len(fids) != len(set(fids)) or len(cids) != len(set(cids)):
        raise ReportError("duplicate finding or candidate ids")


def _load(root: Path, report: Path) -> tuple[bytes, dict[str, Any]]:
    path = _report_path(root, report, exists=True)
    data = path.read_bytes()
    text = data.decode()
    versions = re.findall(
        r'<meta name="audit-codebase-report-version" content="([0-9]+)">', text
    )
    if versions != [str(REPORT_VERSION)]:
        raise ReportError(f"report version {REPORT_VERSION} required")
    match = _STATE.findall(text)
    if len(match) != 1:
        raise ReportError("report must contain one embedded state")
    claimed, encoded = match[0]
    try:
        state = _obj(json.loads(unescape(encoded)), "report state")
    except json.JSONDecodeError as exc:
        raise ReportError("invalid report state") from exc
    if _digest(_canonical(state)) != claimed:
        raise ReportError("report state digest mismatch")
    _validate_state(state)
    if _render(state) != data:
        raise ReportError("report is not canonical")
    return data, state


def _prepare(
    objective: str, root: Path, report: Path, manifest: Path
) -> dict[str, Any]:
    root = root.resolve()
    path = _report_path(root, report, exists=objective != "render-report")
    raw = _json(manifest, f"{objective} manifest")
    if objective == "render-report":
        if path.exists():
            raise ReportError("render-report refuses existing report")
        state = _map(raw, root)
        prior = "absent"
    else:
        data, state = _load(root, path)
        prior = _digest(data)
        packet = _audit(raw) if objective == "audit-subsystem" else _analysis(raw)
        if packet["expected_report_sha256"] != prior:
            raise ReportError("expected_report_sha256 does not match current report")
        state = json.loads(json.dumps(state))
        if objective == "audit-subsystem":
            selected = next(
                (x for x in state["subsystems"] if x["id"] == packet["subsystem_id"]),
                None,
            )
            if selected is None:
                raise ReportError(
                    f"unknown subsystem {packet['subsystem_id']}; choose one of: {', '.join(x['id'] for x in state['subsystems'])}"
                )
            _verify_source_packet(
                root, packet["source_identity"], selected["owned_paths"]
            )
            previous_audit = selected.get("audit")
            previous_systemic = [
                x
                for x in state["systemic_findings"]
                if x.get("origin_subsystem_id") == selected["id"]
            ]
            state["systemic_findings"] = [
                x
                for x in state["systemic_findings"]
                if x.get("origin_subsystem_id") != selected["id"]
            ]
            known = {x["id"] for x in state["systemic_findings"]}
            known |= {
                x["id"]
                for s in state["subsystems"]
                if s["id"] != selected["id"]
                for x in s.get("audit", {}).get("findings", [])
            }
            incoming = {
                x["id"] for x in packet["findings"] + packet["systemic_findings"]
            }
            if known & incoming:
                raise ReportError("audit reuses finding ids")
            selected["state"] = "audited"
            selected["audit"] = {
                k: v
                for k, v in packet.items()
                if k
                not in {"expected_report_sha256", "subsystem_id", "systemic_findings"}
            }
            state["systemic_findings"] += [
                {**finding, "origin_subsystem_id": selected["id"]}
                for finding in packet["systemic_findings"]
            ]
        else:
            choices = [
                x
                for s in state["subsystems"]
                for x in s.get("audit", {}).get("candidates", [])
            ]
            selected = next(
                (x for x in choices if x["id"] == packet["candidate_id"]), None
            )
            if selected is None:
                raise ReportError(
                    f"unknown candidate {packet['candidate_id']}; choose one of: {', '.join(x['id'] for x in choices) or 'none'}"
                )
            mapped_ids = {subsystem["id"] for subsystem in state["subsystems"]}
            affected_ids = set(selected["affected_scope"]) | set(
                packet["affected_scope"]
            )
            unknown_affected = affected_ids - mapped_ids
            if unknown_affected:
                raise ReportError(
                    "analysis affected_scope names unmapped subsystem: "
                    + ", ".join(sorted(unknown_affected))
                )
            affected_paths = sorted(
                {
                    path
                    for subsystem in state["subsystems"]
                    if subsystem["id"] in affected_ids
                    for path in subsystem["owned_paths"]
                }
            )
            if not affected_paths:
                raise ReportError("candidate affected_scope names no mapped subsystem")
            _verify_source_packet(root, packet["source_identity"], affected_paths)
            previous_analysis = selected.get("analysis")
            selected["state"] = packet["state"]
            selected["analysis"] = {
                k: v
                for k, v in packet.items()
                if k not in {"expected_report_sha256", "candidate_id", "state"}
            }
        history = {
            "operation": "audit" if objective == "audit-subsystem" else "analyze",
            "selection": packet["subsystem_id"]
            if objective == "audit-subsystem"
            else packet["candidate_id"],
        }
        if objective == "audit-subsystem" and previous_audit is not None:
            history["superseded"] = {
                "audit": previous_audit,
                "systemic_findings": previous_systemic,
            }
        if objective == "analyze-candidate" and previous_analysis is not None:
            history["superseded"] = {"analysis": previous_analysis}
        state["history"].append(history)
        _validate_state(state)
    rendered = _render(state)
    return {
        "path": path,
        "prior": prior,
        "rendered": rendered,
        "report_sha256": _digest(rendered),
        "state_sha256": _digest(_canonical(state)),
    }


def mutate_report(
    *,
    objective: str,
    repo_root: Path,
    report: Path,
    manifest: Path,
    validate_only: bool = False,
) -> dict[str, Any]:
    p = _prepare(objective, repo_root, report, manifest)
    result = {
        "response_version": RESPONSE_VERSION,
        "objective": objective,
        "validated": True,
        "published": False,
        "report": str(p["path"]),
        "report_sha256": p["report_sha256"],
        "state_sha256": p["state_sha256"],
    }
    if validate_only:
        return result
    path = p["path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name("report.lock")
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ReportError("another report writer is active", stage="publish") from exc
    try:
        os.close(lock_fd)
        if (p["prior"] == "absent" and path.exists()) or (
            p["prior"] != "absent"
            and (not path.is_file() or _digest(path.read_bytes()) != p["prior"])
        ):
            raise ReportError("report changed before publication", stage="publish")
        fd, temp = tempfile.mkstemp(prefix="report-", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(p["rendered"])
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
        if _digest(path.read_bytes()) != p["report_sha256"]:
            raise ReportError("published report failed read-back", stage="read-back")
        _load(repo_root.resolve(), path)
    finally:
        lock.unlink(missing_ok=True)
    result["published"] = True
    return result


def inspect_report(*, repo_root: Path, report: Path) -> dict[str, Any]:
    data, state = _load(repo_root.resolve(), report)
    return {
        "response_version": RESPONSE_VERSION,
        "report_version": REPORT_VERSION,
        "state_version": STATE_VERSION,
        "report_sha256": _digest(data),
        "state_sha256": _digest(_canonical(state)),
        "state": state,
    }


def _parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("inventory")
    p.add_argument("--repo-root", type=Path, required=True)
    p = commands.add_parser("source-identity")
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--path", action="append", dest="paths", required=True)
    p = commands.add_parser("inspect")
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    for name in ("render-report", "audit-subsystem", "analyze-candidate"):
        p = commands.add_parser(name)
        p.add_argument("--repo-root", type=Path, required=True)
        p.add_argument("--report", type=Path, required=True)
        p.add_argument("--manifest", type=Path, required=True)
        p.add_argument("--validate-only", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        a = _parser().parse_args(argv)
        if a.command == "inventory":
            result = inventory(repo_root=a.repo_root)
        elif a.command == "source-identity":
            result = source_identity(repo_root=a.repo_root, paths=a.paths)
        elif a.command == "inspect":
            result = inspect_report(repo_root=a.repo_root, report=a.report)
        else:
            result = mutate_report(
                objective=a.command,
                repo_root=a.repo_root,
                report=a.report,
                manifest=a.manifest,
                validate_only=a.validate_only,
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except ReportError as exc:
        print(
            json.dumps(
                {
                    "response_version": RESPONSE_VERSION,
                    "ok": False,
                    "stage": exc.stage,
                    "error": str(exc),
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
