"""Offline visual codebase workbench for Map, subsystem Audit, and candidate Analyze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

REPORT_VERSION, STATE_VERSION, RESPONSE_VERSION, MANIFEST_VERSION = 1, 1, 1, 1
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
_STYLE = r"""
:root{color-scheme:dark;--bg:#071019;--panel:#0d1824;--panel2:#111f2e;--text:#e8f0f7;--muted:#93a8ba;--border:#284158;--accent:#67e8f9;--green:#34d399;--amber:#fbbf24;--red:#fb7185;--blue:#60a5fa;--shadow:0 16px 45px rgba(0,0,0,.24)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:linear-gradient(180deg,#071019,#09131e 42%,#071019);color:var(--text);font:14px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}button,input,select{font:inherit}button{cursor:pointer}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;overflow-wrap:anywhere}
.shell{display:grid;grid-template-columns:248px minmax(0,1fr);min-height:100vh}.sidebar{position:sticky;top:0;height:100vh;padding:24px 18px;border-right:1px solid var(--border);background:rgba(7,16,25,.96);overflow:auto}.brand{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:800;margin-bottom:22px}.sidebar nav{display:grid;gap:6px}.sidebar nav a{display:block;padding:8px 10px;border-radius:8px;color:var(--muted)}.sidebar nav a:hover{background:var(--panel2);color:var(--text);text-decoration:none}.sidebar .minor{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);font-size:12px;color:var(--muted)}
.content{width:min(1500px,100%);padding:32px clamp(20px,4vw,54px) 64px}.hero{display:flex;gap:24px;align-items:flex-start;justify-content:space-between;margin-bottom:24px}.hero h1{font-size:clamp(28px,4vw,44px);line-height:1.05;margin:0 0 8px;letter-spacing:-.035em}.hero p{margin:0;color:var(--muted);max-width:780px}.hero-meta{text-align:right;font-size:12px;color:var(--muted)}
.metrics{display:grid;grid-template-columns:repeat(6,minmax(110px,1fr));gap:10px;margin:22px 0 28px}.metric{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--border);border-radius:12px;padding:14px}.metric strong{display:block;font-size:24px;line-height:1.1}.metric span{color:var(--muted);font-size:12px}
.section{margin:34px 0}.section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:14px}.section h2{font-size:21px;margin:0}.section-head p{margin:0;color:var(--muted)}.panel{background:rgba(13,24,36,.9);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);padding:18px}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px}.toolbar input,.toolbar select{background:#07131f;color:var(--text);border:1px solid var(--border);border-radius:9px;padding:9px 11px}.toolbar input{min-width:260px;flex:1}
.architecture{overflow:auto;padding:10px}.architecture svg{display:block;min-width:760px}.architecture .sys-label{fill:#8ea8bd;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.architecture .edge{stroke:#3a5a73;stroke-width:1.5;fill:none;opacity:.85}.architecture .node rect{fill:#102235;stroke:#31516a;stroke-width:1.4;rx:12}.architecture .node.audited rect{stroke:#2f9e7b}.architecture .node.changed rect{stroke:#c17a2b;stroke-width:2}.architecture .node text.name{fill:#edf7ff;font-size:14px;font-weight:750}.architecture .node text.meta{fill:#93a8ba;font-size:11px}.architecture .node:hover rect{stroke:#67e8f9}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:10px}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}.dot.mapped{background:#60a5fa}.dot.audited{background:#34d399}.dot.changed{background:#fbbf24}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}.card{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--border);border-radius:13px;padding:16px;min-width:0}.card h3{margin:0 0 5px;font-size:17px}.card h4{margin:18px 0 8px;font-size:14px}.card p{margin:7px 0}.muted{color:var(--muted)}
.badges{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 12px}.badge{display:inline-flex;align-items:center;border:1px solid var(--border);border-radius:999px;padding:2px 8px;font-size:11px;font-weight:700}.badge.audited,.badge.complete,.badge.strong,.badge.analyzed,.badge.fresh{color:var(--green);border-color:#216c58}.badge.changed,.badge.evidence-gap,.badge.blocked,.badge.worth-exploring{color:var(--amber);border-color:#805e1b}.badge.defect,.badge.p1,.badge.p0{color:var(--red);border-color:#7d3040}.badge.mapped,.badge.opportunity,.badge.speculative,.badge.presented{color:var(--blue);border-color:#315b8c}.badge.retained-complexity,.badge.not-applicable,.badge.disproved{color:var(--muted)}
.kv{display:grid;grid-template-columns:110px minmax(0,1fr);gap:6px 12px;margin:12px 0}.kv dt{color:var(--muted);font-weight:650}.kv dd{margin:0;overflow-wrap:anywhere}ul.compact{margin:6px 0;padding-left:18px}
.command{display:flex;gap:8px;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}.copy{border:1px solid #2b6370;color:#b9f5ff;background:#0a2a31;border-radius:8px;padding:7px 9px}.copy:hover{background:#0e3741}
.coverage-row{display:grid;grid-template-columns:140px 1fr 72px;gap:10px;align-items:center;margin:9px 0}.bar{height:8px;background:#132535;border-radius:999px;overflow:hidden}.bar>span{display:block;height:100%;background:linear-gradient(90deg,#34d399,#67e8f9)}
.lens-table{width:100%;border-collapse:collapse}.lens-table th,.lens-table td{padding:8px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border)}.lens-table th{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
.finding{border-left:3px solid #31516a}.finding.defect{border-left-color:var(--red)}.finding.opportunity{border-left-color:var(--blue)}.finding.gap{border-left-color:var(--amber)}.finding.retained-complexity{border-left-color:#64748b}
.candidate{position:relative}.strength{position:absolute;top:14px;right:14px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}.compare>div{background:#0a1622;border:1px solid var(--border);border-radius:10px;padding:12px}.compare h4{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.option-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.option{background:#0a1622;border:1px solid var(--border);border-radius:10px;padding:12px}.option h5{margin:0 0 6px;font-size:14px}
details{border-top:1px solid var(--border);margin-top:12px;padding-top:10px}summary{cursor:pointer;color:#bfd1df;font-weight:650}.evidence{font-size:12px;color:#c5d3de}.history{margin:0;padding-left:20px}.history li{margin:5px 0;color:var(--muted)}.hidden{display:none!important}footer{margin-top:42px;padding-top:20px;border-top:1px solid var(--border);color:var(--muted);font-size:12px}
@media(max-width:1050px){.shell{grid-template-columns:1fr}.sidebar{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--border)}.sidebar nav{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}.metrics{grid-template-columns:repeat(3,1fr)}}@media(max-width:650px){.content{padding:22px 14px 50px}.hero{display:block}.hero-meta{text-align:left;margin-top:10px}.metrics{grid-template-columns:repeat(2,1fr)}.compare{grid-template-columns:1fr}.coverage-row{grid-template-columns:110px 1fr 55px}.kv{grid-template-columns:1fr}.strength{position:static;margin-bottom:8px}}
"""
_SCRIPT = r"""
(function(){
  const q=document.getElementById('search'), state=document.getElementById('state-filter');
  const apply=()=>{const needle=(q&&q.value||'').toLowerCase().trim(), wanted=state&&state.value||'all';
    document.querySelectorAll('[data-filter-card]').forEach(el=>{const hay=(el.getAttribute('data-search')||'').toLowerCase(), st=el.getAttribute('data-state')||'';
      el.classList.toggle('hidden',(!!needle&&!hay.includes(needle))||(wanted!=='all'&&st!==wanted));});};
  if(q)q.addEventListener('input',apply);if(state)state.addEventListener('change',apply);
  document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{const value=button.getAttribute('data-copy')||'';
    try{if(navigator.clipboard&&navigator.clipboard.writeText)await navigator.clipboard.writeText(value);else{const t=document.createElement('textarea');t.value=value;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();}
      const old=button.textContent;button.textContent='Copied';setTimeout(()=>button.textContent=old,1200);}catch(_){window.prompt('Copy this command',value);}}));
})();
"""


class ReportError(ValueError):
    def __init__(self, message: str, *, stage: str = "validate") -> None:
        super().__init__(message)
        self.stage = stage


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ReportError(message, stage="arguments")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    _strict(identity, {"commit", "tree", "tracked_content_sha256"}, set(), "observation_identity")
    identity = {k: _text(v, f"identity {k}") for k, v in identity.items()}
    if not _SHA.fullmatch(identity["tracked_content_sha256"]):
        raise ReportError("tracked_content_sha256 must be sha256")
    if identity != inventory(repo_root=root)["identity"]:
        raise ReportError("observation_identity does not match current repository")
    for sub in subs:
        sub["map_source"] = {
            "paths": list(sub["owned_paths"]),
            "sha256": source_identity(repo_root=root, paths=sub["owned_paths"])["sha256"],
        }
    state = {
        "state_version": STATE_VERSION,
        "title": _text(raw["title"], "title"),
        "observation_identity": identity,
        "systems": systems,
        "subsystems": subs,
        "excluded": excluded,
        "coverage": _text(raw["coverage"], "coverage"),
        "evidence_limits": _text(raw["evidence_limits"], "evidence limits", empty=True),
        "systemic_findings": [],
        "history": [{"operation": "map", "selection": "repository"}],
        "run_id": "",
        "observed_at": "",
        "freshness": {},
    }
    _refresh_observation(state, root)
    return state


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
        "id", "title", "primary_class", "strength", "finding_ids", "affected_scope",
        "problem", "evidence", "direction", "benefit", "risks", "required_proof",
    }
    _strict(x, fields, set(), label)
    primary = _text(x["primary_class"], "primary class")
    strength = _text(x["strength"], "candidate strength")
    if primary not in _LENSES:
        raise ReportError("unsupported candidate class")
    if strength not in {"strong", "worth exploring", "speculative"}:
        raise ReportError("candidate strength must be strong, worth exploring, or speculative")
    return {
        "id": _id(x["id"], "candidate id"),
        "title": _text(x["title"], "title"),
        "primary_class": primary,
        "strength": strength,
        "finding_ids": [_id(y, "finding id") for y in _texts(x["finding_ids"], "finding ids", empty=False)],
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


def _source_freshness(root: Path, packet: dict[str, Any]) -> str:
    try:
        current = source_identity(repo_root=root, paths=packet["paths"])
    except ReportError:
        return "changed"
    return "fresh" if current["sha256"] == packet["sha256"] else "changed"


def _refresh_observation(state: dict[str, Any], root: Path) -> None:
    state["freshness"] = {
        sub["id"]: _source_freshness(
            root, sub.get("audit", {}).get("source_identity") or sub["map_source"]
        )
        for sub in state["subsystems"]
    }
    state["observed_at"] = _now()


def _list(values: Sequence[str], empty: str = "None recorded") -> str:
    return "<ul class=\"compact\">" + "".join(f"<li>{escape(v)}</li>" for v in values) + "</ul>" if values else f'<span class="muted">{escape(empty)}</span>'


def _badge(value: str, label: str | None = None) -> str:
    cls = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return f'<span class="badge {escape(cls)}">{escape(label or value)}</span>'


def _architecture_svg(state: dict[str, Any]) -> str:
    grouped = {s["id"]: [x for x in state["subsystems"] if x["system_id"] == s["id"]] for s in state["systems"]}
    width = max(860, 210 + max((len(v) for v in grouped.values()), default=1) * 230)
    height = max(220, 55 + len(state["systems"]) * 150)
    positions, parts = {}, []
    for row, system in enumerate(state["systems"]):
        y = 45 + row * 150
        parts.append(f'<text class="sys-label" x="20" y="{y+30}">{escape(system["name"])}</text>')
        for col, sub in enumerate(grouped[system["id"]]):
            x = 175 + col * 230
            positions[sub["id"]] = (x, y)
            audit = sub.get("audit")
            systemic_count = sum(
                1 for finding in state["systemic_findings"]
                if sub["id"] in finding["affected_scope"]
            )
            local_count = len(audit["findings"]) if audit else 0
            candidate_count = len(audit["candidates"]) if audit else 0
            meta = (
                f'audited · {local_count + systemic_count} findings · {candidate_count} candidates'
                if audit else
                (f'mapped · {systemic_count} systemic findings' if systemic_count else "mapped · not audited")
            )
            fresh = state["freshness"].get(sub["id"], "fresh")
            cls = "changed" if fresh == "changed" else sub["state"]
            parts.append(f'<a href="#subsystem-{escape(sub["id"])}"><g class="node {escape(cls)}"><rect x="{x}" y="{y}" width="195" height="82"></rect><text class="name" x="{x+14}" y="{y+28}">{escape(sub["name"])}</text><text class="meta" x="{x+14}" y="{y+50}">{escape(meta)}</text><text class="meta" x="{x+14}" y="{y+67}">{escape(fresh)}</text></g></a>')
    edges = []
    for sub in state["subsystems"]:
        sx, sy = positions[sub["id"]]
        for dep in sub["dependencies"]:
            if dep["id"] not in positions:
                continue
            dx, dy = positions[dep["id"]]
            x1, y1, x2, y2 = sx + 195, sy + 41, dx, dy + 41
            if x2 < x1:
                x1, y1, x2, y2 = sx + 98, sy + 82, dx + 98, dy
            mid = (x1 + x2) // 2
            edges.append(f'<path class="edge" d="M{x1},{y1} C{mid},{y1} {mid},{y2} {x2},{y2}" marker-end="url(#arrow)"></path>')
    return f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Subsystem dependency map"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3a5a73"></path></marker></defs>{"".join(edges)}{"".join(parts)}</svg>'


def _finding_html(x: dict[str, Any]) -> str:
    extras = "".join(
        f"<dt>{escape(k.replace('_',' ').title())}</dt><dd>{escape(x[k])}</dd>"
        for k in ("severity","scenario","missing_evidence","boundary_reason","reentry","protected_constraint","ceiling","revisit_trigger")
        if k in x
    )
    search = " ".join([x["title"], x["kind"], x["primary_class"], x["impact"], x["direction"], *x["affected_scope"]])
    return f'''<article class="card finding {escape(x["kind"].replace(" ","-"))}" data-filter-card data-state="{escape(x["kind"])}" data-search="{escape(search,quote=True)}" id="finding-{escape(x["id"])}"><h3>{escape(x["title"])}</h3><div class="badges">{_badge(x["kind"])}{_badge(x["primary_class"])}</div><p>{escape(x["impact"])}</p><dl class="kv"><dt>Causal owner</dt><dd>{escape(x["causal_owner"])}</dd><dt>Affected</dt><dd>{escape(", ".join(x["affected_scope"]))}</dd><dt>Direction</dt><dd>{escape(x["direction"])}</dd><dt>Confidence</dt><dd>{escape(x["confidence"])}</dd></dl><details class="evidence"><summary>Evidence and proof</summary><dl class="kv"><dt>Expectation</dt><dd>{escape(x["expectation"]) or '<span class="muted">None</span>'}</dd><dt>Locations</dt><dd>{_list(x["locations"])}</dd><dt>Evidence</dt><dd>{_list(x["evidence"])}</dd><dt>Proof</dt><dd>{_list(x["proof"])}</dd>{extras}</dl></details></article>'''


def _candidate_html(x: dict[str, Any], run_id: str) -> str:
    analysis = x.get("analysis")
    search = " ".join([x["title"], x["primary_class"], x["strength"], x["problem"], x["direction"], *x["affected_scope"]])
    analysis_html = ""
    if analysis:
        options = "".join(f'<article class="option"><h5>{escape(o["name"])}</h5><p>{escape(o["description"])}</p><strong>Trade-offs</strong>{_list(o["tradeoffs"])}</article>' for o in analysis["options"])
        analysis_html = f'''<div class="panel" style="margin-top:12px"><h4>Analysis</h4><p>{escape(analysis["summary"])}</p><dl class="kv"><dt>Cause</dt><dd>{escape(analysis["cause"])}</dd><dt>Recommendation</dt><dd>{escape(analysis["recommendation"]) or '<span class="muted">None</span>'}</dd><dt>Trade-offs</dt><dd>{_list(analysis["tradeoffs"])}</dd><dt>Proof</dt><dd>{_list(analysis["proof"])}</dd><dt>Evidence limits</dt><dd>{escape(analysis["evidence_limits"]) or '<span class="muted">None</span>'}</dd><dt>Blocking question</dt><dd>{escape(analysis["question"]) or '<span class="muted">None</span>'}</dd></dl><div class="option-grid">{options}</div></div>'''
    command = f"$audit-codebase analyze candidate {x['id']} in atlas run {run_id}"
    next_action = (
        f"Use analyzed audit candidate {x['id']} from atlas run {run_id}. "
        "Help me choose the appropriate next owner among direct implementation, "
        "$codebase-design, $prototype, or $to-tickets. Do not start the next workflow yet."
        if x["state"] == "analyzed"
        else (
            f"Use blocked audit candidate {x['id']} from atlas run {run_id}. "
            "Help me resolve the exact blocker without starting implementation."
            if x["state"] == "blocked" else ""
        )
    )
    next_button = (
        f'<button class="copy" data-copy="{escape(next_action,quote=True)}">Copy next-action handoff</button>'
        if next_action else ""
    )
    return f'''<article class="card candidate" data-filter-card data-state="{escape(x["state"])}" data-search="{escape(search,quote=True)}" id="candidate-{escape(x["id"])}"><div class="strength">{_badge(x["strength"],x["strength"].title())}</div><h3>{escape(x["title"])}</h3><div class="badges">{_badge(x["state"])}{_badge(x["primary_class"])}</div><div class="compare"><div><h4>Current problem</h4><p>{escape(x["problem"])}</p></div><div><h4>Direction</h4><p>{escape(x["direction"])}</p><p class="muted">{escape(x["benefit"])}</p></div></div><dl class="kv"><dt>Affects</dt><dd>{escape(", ".join(x["affected_scope"]))}</dd><dt>Findings</dt><dd>{escape(", ".join(x["finding_ids"]))}</dd><dt>Risks</dt><dd>{_list(x["risks"])}</dd><dt>Required proof</dt><dd>{_list(x["required_proof"])}</dd></dl><details class="evidence"><summary>Evidence</summary>{_list(x["evidence"])}</details>{analysis_html}<div class="command"><button class="copy" data-copy="{escape(command,quote=True)}">Copy analyze command</button>{next_button}</div></article>'''


def _render(state: dict[str, Any]) -> bytes:
    identity, subsystems = state["observation_identity"], state["subsystems"]
    audited = [x for x in subsystems if x["state"] == "audited"]
    changed = [x for x in subsystems if state["freshness"].get(x["id"]) == "changed"]
    findings = [x for sub in audited for x in sub["audit"]["findings"]] + state["systemic_findings"]
    candidates = [x for sub in audited for x in sub["audit"]["candidates"]]
    gap_count = sum(1 for sub in audited for lens in sub["audit"]["lenses"] if lens["state"] == "evidence gap")
    metrics = [("Subsystems",len(subsystems)),("Audited",len(audited)),("Mapped",len(subsystems)-len(audited)),("Source changed",len(changed)),("Findings",len(findings)),("Candidates",len(candidates))]
    metric_html = "".join(f'<div class="metric"><strong>{v}</strong><span>{escape(k)}</span></div>' for k,v in metrics)
    lens_rows = []
    for lens in _LENSES:
        done = sum(1 for sub in audited for row in sub["audit"]["lenses"] if row["class"]==lens and row["state"]=="complete")
        total=len(audited); pct=int(round(done*100/total)) if total else 0
        lens_rows.append(f'<div class="coverage-row"><span>{escape(lens.title())}</span><div class="bar"><span style="width:{pct}%"></span></div><span>{done}/{total}</span></div>')
    cards={}
    audits=[]
    for sub in subsystems:
        audit=sub.get("audit")
        systemic_count=sum(1 for finding in state["systemic_findings"] if sub["id"] in finding["affected_scope"])
        fc=(len(audit["findings"]) if audit else 0)+systemic_count
        cc=len(audit["candidates"]) if audit else 0
        fresh=state["freshness"].get(sub["id"],"fresh"); deps=[d["id"] for d in sub["dependencies"]]
        search=" ".join([sub["name"],sub["purpose"],sub["ownership"],sub["system_id"],*deps])
        command=f"$audit-codebase audit subsystem {sub['id']} in atlas run {state['run_id']}"
        dep_detail="".join(f'<li><a href="#subsystem-{escape(d["id"])}">{escape(d["id"])}</a>: {escape("; ".join(d["evidence"]))}</li>' for d in sub["dependencies"]) or '<li class="muted">None recorded</li>'
        cards[sub["id"]]=f'''<article class="card" id="subsystem-{escape(sub["id"])}" data-filter-card data-state="{escape(sub["state"])}" data-search="{escape(search,quote=True)}"><h3>{escape(sub["name"])}</h3><div class="badges">{_badge(sub["state"])}{_badge("changed" if fresh=="changed" else "fresh","Source changed" if fresh=="changed" else "Source fresh")}{_badge(sub["system_id"])}</div><p>{escape(sub["purpose"])}</p><dl class="kv"><dt>Ownership</dt><dd>{escape(sub["ownership"])}</dd><dt>Dependencies</dt><dd>{escape(", ".join(deps)) if deps else '<span class="muted">None</span>'}</dd><dt>Audit result</dt><dd>{fc} findings · {cc} candidates</dd></dl><details class="evidence"><summary>Architecture evidence</summary><dl class="kv"><dt>Authority</dt><dd>{_list(sub["authority"])}</dd><dt>Callers</dt><dd>{_list(sub["callers"])}</dd><dt>Dependencies</dt><dd><ul class="compact">{dep_detail}</ul></dd><dt>Interfaces</dt><dd>{_list(sub["interfaces"])}</dd><dt>Proof seams</dt><dd>{_list(sub["proof_seams"])}</dd><dt>Owned paths</dt><dd>{_list(sub["owned_paths"])}</dd><dt>Exclusions</dt><dd>{_list(sub["exclusions"])}</dd></dl></details><div class="command"><button class="copy" data-copy="{escape(command,quote=True)}">Copy audit command</button></div></article>'''
        if audit:
            trace=audit["source_trace"]
            lens_html="".join(f'<tr><td>{escape(row["class"])}</td><td>{_badge(row["state"])}</td><td>{escape(row["reason"])}</td><td>{_list(row["evidence"])}</td></tr>' for row in audit["lenses"])
            audits.append(f'''<article class="panel" id="audit-{escape(sub["id"])}"><div class="section-head"><div><h2>{escape(sub["name"])}</h2><p>{escape(trace["summary"])}</p></div><div class="badges">{_badge(audit["coverage"])}{_badge("evidence-gap",f"{sum(1 for x in audit['lenses'] if x['state']=='evidence gap')} gaps")}</div></div><table class="lens-table"><thead><tr><th>Lens</th><th>Coverage</th><th>Reason</th><th>Evidence</th></tr></thead><tbody>{lens_html}</tbody></table><details class="evidence"><summary>Source trace</summary><dl class="kv"><dt>Entry points</dt><dd>{_list(trace["entry_points"])}</dd><dt>Callers</dt><dd>{_list(trace["callers"])}</dd><dt>Dependencies</dt><dd>{_list(trace["dependencies"])}</dd><dt>Interfaces</dt><dd>{_list(trace["interfaces"])}</dd><dt>Proof seams</dt><dd>{_list(trace["proof_seams"])}</dd><dt>Representative flows</dt><dd>{_list(trace["representative_flows"])}</dd><dt>History signals</dt><dd>{_list(trace["history_signals"])}</dd><dt>Evidence limits</dt><dd>{escape(audit["evidence_limits"]) or '<span class="muted">None</span>'}</dd></dl></details><p><strong>Audit recommendation:</strong> {escape(audit["recommendation"])}</p></article>''')
    systems_index="".join(f'<section id="system-{escape(system["id"])}"><h3>{escape(system["name"])}</h3><div class="grid">{"".join(cards[sub["id"]] for sub in subsystems if sub["system_id"]==system["id"])}</div></section>' for system in state["systems"])
    candidates=sorted(candidates,key=lambda x:({"strong":0,"worth exploring":1,"speculative":2}[x["strength"]],x["title"]))
    candidate_html="".join(_candidate_html(x,state["run_id"]) for x in candidates)
    finding_html="".join(_finding_html(x) for x in findings)
    excluded="".join(f'<li><code>{escape(x["path"])}</code>: {escape(x["reason"])}</li>' for x in state["excluded"]) or '<li class="muted">None</li>'
    history="".join(f'<li>{escape(x["operation"])} · {escape(x["selection"])}</li>' for x in state["history"])
    nav_systems="".join(f'<a href="#system-{escape(s["id"])}">{escape(s["name"])}</a>' for s in state["systems"])
    raw=_canonical(state); embedded=raw.decode().replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="audit-codebase-report-version" content="{REPORT_VERSION}"><title>{escape(state["title"])}</title><style>{_STYLE}</style></head><body><div class="shell"><aside class="sidebar"><div class="brand">Audit atlas</div><nav><a href="#overview">Overview</a><a href="#architecture">Architecture</a><a href="#subsystems">Subsystems</a><a href="#audits">Audits</a><a href="#findings">Findings</a><a href="#candidates">Candidates</a><a href="#evidence">Evidence</a><a href="#history">History</a>{nav_systems}</nav><div class="minor">Run <code>{escape(state["run_id"])}</code><br>Observed {escape(state["observed_at"])}</div></aside><main class="content"><header class="hero" id="overview"><div><h1>{escape(state["title"])}</h1><p>Visual architecture map and evidence-backed improvement workbench. Select a subsystem to audit, then a candidate to analyze.</p></div><div class="hero-meta">Commit <code>{escape(identity["commit"][:12])}</code><br>Tree <code>{escape(identity["tree"][:12])}</code></div></header><div class="metrics">{metric_html}</div><section class="section"><div class="section-head"><div><h2>Coverage</h2><p>{escape(state["coverage"])}</p></div><div class="badges">{_badge("evidence-gap",f"{gap_count} evidence gaps")}</div></div><div class="panel">{"".join(lens_rows)}</div></section><section class="section" id="architecture"><div class="section-head"><div><h2>Architecture map</h2><p>Dependencies are directional. Click a subsystem to inspect it.</p></div></div><div class="panel architecture">{_architecture_svg(state)}<div class="legend"><span><i class="dot mapped"></i>mapped</span><span><i class="dot audited"></i>audited</span><span><i class="dot changed"></i>source changed</span></div></div></section><section class="section" id="subsystems"><div class="section-head"><div><h2>Subsystem explorer</h2><p>Search the map, then copy the exact drill-down command.</p></div></div><div class="toolbar"><input id="search" type="search" placeholder="Search subsystems, findings, candidates..."><select id="state-filter"><option value="all">All states</option><option value="mapped">Mapped</option><option value="audited">Audited</option><option value="presented">Candidate: presented</option><option value="analyzed">Candidate: analyzed</option><option value="blocked">Candidate: blocked</option></select></div>{systems_index}</section><section class="section" id="audits"><div class="section-head"><div><h2>Audited subsystems</h2><p>Meaning first; source trace and evidence stay expandable.</p></div></div>{"".join(audits) or '<div class="panel muted">Audit a mapped subsystem to populate this section.</div>'}</section><section class="section" id="findings"><div class="section-head"><div><h2>Findings</h2><p>Defects, opportunities, retained complexity, and explicit evidence gaps.</p></div></div><div class="grid">{finding_html or '<div class="panel muted">No admitted findings yet.</div>'}</div></section><section class="section" id="candidates"><div class="section-head"><div><h2>Improvement candidates</h2><p>Qualitative strength, not a numeric architecture score. Select one to analyze.</p></div></div><div class="grid">{candidate_html or '<div class="panel muted">Audit a subsystem to produce selectable candidates.</div>'}</div></section><section class="section" id="evidence"><div class="section-head"><div><h2>Evidence and provenance</h2><p>Forensic detail is preserved without dominating the decision view.</p></div></div><div class="panel"><dl class="kv"><dt>Tracked content</dt><dd><code>{escape(identity["tracked_content_sha256"])}</code></dd><dt>Evidence limits</dt><dd>{escape(state["evidence_limits"]) or '<span class="muted">None</span>'}</dd><dt>Excluded paths</dt><dd><ul class="compact">{excluded}</ul></dd></dl></div></section><section class="section" id="history"><div class="section-head"><div><h2>History</h2><p>Map, audit, and analysis updates.</p></div></div><div class="panel"><ol class="history">{history}</ol></div></section><footer>Audit-codebase workbench format {REPORT_VERSION}. Read-only HTML; copy commands return control to ChatGPT.</footer></main></div><script id="audit-codebase-state" type="application/json" data-sha256="{_digest(raw)}">{embedded}</script><script>{_SCRIPT}</script></body></html>'''
    return html.encode()


def _validate_state(state: dict[str, Any]) -> None:
    if state.get("state_version") != STATE_VERSION:
        raise ReportError(f"report state requires version {STATE_VERSION}")
    if not isinstance(state.get("run_id"), str) or not _RUN.fullmatch(state["run_id"]):
        raise ReportError("report state has invalid run id")
    if not isinstance(state.get("observed_at"), str) or not state["observed_at"]:
        raise ReportError("report state has no observation time")
    sids=[x.get("id") for x in state.get("subsystems",[])]
    fids=[x.get("id") for x in state.get("systemic_findings",[])]
    cids=[]
    if len(sids)!=len(set(sids)): raise ReportError("duplicate subsystem ids")
    if set(state.get("freshness",{}))!=set(sids): raise ReportError("freshness must cover every subsystem")
    for sub in state.get("subsystems",[]):
        _source_packet(sub.get("map_source"), f"{sub.get('id')} map source")
        if state["freshness"][sub["id"]] not in {"fresh","changed"}: raise ReportError("invalid subsystem freshness")
        if "audit" in sub:
            if sub.get("state")!="audited": raise ReportError("audit requires audited state")
            _lenses(sub["audit"].get("lenses"))
            fids += [x.get("id") for x in sub["audit"].get("findings",[])]
            cids += [x.get("id") for x in sub["audit"].get("candidates",[])]
    if len(fids)!=len(set(fids)) or len(cids)!=len(set(cids)): raise ReportError("duplicate finding or candidate ids")


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
        state["run_id"] = path.parent.name
        _refresh_observation(state, root)
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
        _refresh_observation(state, root)
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


def refresh_report(*, repo_root: Path, report: Path) -> dict[str, Any]:
    root=repo_root.resolve()
    data,state=_load(root,report)
    prior=_digest(data)
    state=json.loads(json.dumps(state))
    _refresh_observation(state,root)
    rendered=_render(state)
    path=_report_path(root,report,exists=True)
    lock=path.with_name("report.lock")
    try: lock_fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError as exc: raise ReportError("another report writer is active",stage="publish") from exc
    try:
        os.close(lock_fd)
        if _digest(path.read_bytes())!=prior: raise ReportError("report changed before refresh",stage="publish")
        fd,temp=tempfile.mkstemp(prefix="report-",suffix=".tmp",dir=path.parent)
        try:
            with os.fdopen(fd,"wb") as stream:
                stream.write(rendered);stream.flush();os.fsync(stream.fileno())
            os.replace(temp,path)
        finally:
            if os.path.exists(temp): os.unlink(temp)
        _load(root,path)
    finally: lock.unlink(missing_ok=True)
    return {"response_version":RESPONSE_VERSION,"refreshed":True,"report":str(path),"report_sha256":_digest(rendered),"state_sha256":_digest(_canonical(state)),"freshness":state["freshness"]}


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
    p = commands.add_parser("refresh")
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
        elif a.command == "refresh":
            result = refresh_report(repo_root=a.repo_root, report=a.report)
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
