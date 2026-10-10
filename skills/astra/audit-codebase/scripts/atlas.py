"""Offline visual codebase workbench for Map, subsystem Audit, and candidate Analyze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import textwrap
from datetime import datetime, timezone
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

REPORT_VERSION, STATE_VERSION = 4, 4
RESPONSE_VERSION, MANIFEST_VERSION = 2, 1
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
.content{min-width:0;width:min(1500px,100%);padding:32px clamp(20px,4vw,54px) 64px}.hero{display:flex;gap:24px;align-items:flex-start;justify-content:space-between;margin-bottom:24px}.hero h1{font-size:clamp(28px,4vw,44px);line-height:1.05;margin:0 0 8px;letter-spacing:-.035em}.hero p{margin:0;color:var(--muted);max-width:780px}.hero-meta{text-align:right;font-size:12px;color:var(--muted)}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:22px 0 28px}.metric{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--border);border-radius:12px;padding:14px}.metric strong{display:block;font-size:24px;line-height:1.1}.metric span{color:var(--muted);font-size:12px}
.section{margin:34px 0}.section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:14px}.section h2{font-size:21px;margin:0}.section-head p{margin:0;color:var(--muted)}.panel{background:rgba(13,24,36,.9);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);padding:18px}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px}.toolbar input,.toolbar select{background:#07131f;color:var(--text);border:1px solid var(--border);border-radius:9px;padding:9px 11px}.toolbar input{min-width:260px;flex:1}
.architecture{overflow:auto;padding:10px}.architecture svg{display:block;min-width:760px}.architecture .sys-label{fill:#8ea8bd;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.architecture .edge{stroke:#3a5a73;stroke-width:1.5;fill:none;opacity:.85}.architecture .node rect{fill:#102235;stroke:#31516a;stroke-width:1.4;rx:12}.architecture .node.audited rect{stroke:#2f9e7b}.architecture .node.changed rect{stroke:#c17a2b;stroke-width:2}.architecture .node text.name{fill:#edf7ff;font-size:14px;font-weight:750}.architecture .node text.meta{fill:#93a8ba;font-size:11px}.architecture .node:hover rect{stroke:#67e8f9}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:10px}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}.dot.mapped{background:#60a5fa}.dot.audited{background:#34d399}.dot.changed{background:#fbbf24}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(310px,100%),1fr))}.card{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--border);border-radius:13px;padding:16px;min-width:0;overflow-wrap:anywhere}.card h3{margin:0 0 5px;font-size:17px}.card h4{margin:18px 0 8px;font-size:14px}.card p{margin:7px 0}.muted{color:var(--muted)}
.badges{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 12px}.badge{display:inline-flex;align-items:center;border:1px solid var(--border);border-radius:999px;padding:2px 8px;font-size:11px;font-weight:700}.badge.audited,.badge.complete,.badge.strong,.badge.analyzed,.badge.fresh{color:var(--green);border-color:#216c58}.badge.changed,.badge.evidence-gap,.badge.blocked,.badge.worth-exploring{color:var(--amber);border-color:#805e1b}.badge.defect,.badge.p1,.badge.p0{color:var(--red);border-color:#7d3040}.badge.mapped,.badge.opportunity,.badge.speculative,.badge.presented{color:var(--blue);border-color:#315b8c}.badge.retained-complexity,.badge.not-applicable,.badge.disproved{color:var(--muted)}
.kv{display:grid;grid-template-columns:140px minmax(0,1fr);gap:6px 12px;margin:12px 0}.kv dt{color:var(--muted);font-weight:650}.kv dd{margin:0;overflow-wrap:anywhere}ul.compact{margin:6px 0;padding-left:18px}
.command{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}.copy{border:1px solid #2b6370;color:#b9f5ff;background:#0a2a31;border-radius:8px;padding:7px 9px}.copy:hover{background:#0e3741}
.coverage-row{display:grid;grid-template-columns:140px minmax(0,1fr) 72px;gap:10px;align-items:center;margin:9px 0}.bar{display:flex;height:8px;background:#132535;border-radius:999px;overflow:hidden}.bar>span{display:block;height:100%}.bar .complete{background:#34d399}.bar .not-applicable{background:#93a8ba}.bar .evidence-gap{background:#fbbf24}.bar .changed{background:#fb7185}.bar .not-audited{background:#284158}.coverage-detail{color:var(--muted);font-size:12px;margin-top:5px}.stale-warning{padding:10px;border-left:3px solid var(--amber);background:#332711}.comparison{margin:18px 0}.comparison figcaption{font-weight:650}.diagram{overflow:auto}.diagram svg{display:block;max-width:none}.diagram rect{fill:#102235;stroke:#31516a}.diagram text{fill:#e8f0f7;font-size:12px}
.table-scroll{overflow:auto}.lens-table{width:100%;border-collapse:collapse}.lens-table th,.lens-table td{padding:8px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border)}.lens-table th{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
.finding{border-left:3px solid #31516a}.finding.defect{border-left-color:var(--red)}.finding.opportunity{border-left-color:var(--blue)}.finding.gap{border-left-color:var(--amber)}.finding.retained-complexity{border-left-color:#64748b}
.candidate{position:relative}.strength{position:absolute;top:14px;right:14px}.compare{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:12px 0}.compare>div{min-width:0;background:#0a1622;border:1px solid var(--border);border-radius:10px;padding:12px}.compare h4{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}.option-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));gap:10px}.option{background:#0a1622;border:1px solid var(--border);border-radius:10px;padding:12px}.option h5{margin:0 0 6px;font-size:14px}
details{border-top:1px solid var(--border);margin-top:12px;padding-top:10px}summary{cursor:pointer;color:#bfd1df;font-weight:650}.evidence{font-size:12px;color:#c5d3de}.history{margin:0;padding-left:20px}.history li{margin:5px 0;color:var(--muted)}.history-record{white-space:pre-wrap;overflow-wrap:anywhere;max-height:32em;overflow:auto}.badge.verified,.badge.committed,.badge.deployed{color:var(--green);border-color:#216c58}.hidden{display:none!important}footer{margin-top:42px;padding-top:20px;border-top:1px solid var(--border);color:var(--muted);font-size:12px}
@media(max-width:1050px){.shell{grid-template-columns:1fr}.sidebar{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--border)}.sidebar nav{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}.metrics{grid-template-columns:repeat(3,1fr)}}@media(max-width:650px){.content{padding:22px 14px 50px}.hero{display:block}.hero-meta{text-align:left;margin-top:10px}.metrics{grid-template-columns:repeat(2,1fr)}.compare{grid-template-columns:1fr}.coverage-row{grid-template-columns:minmax(0,1fr) auto;gap:6px;margin:14px 0}.coverage-row>div{grid-column:1/-1;grid-row:2}.coverage-row>span:last-child{grid-column:2;grid-row:1}.kv{grid-template-columns:1fr}.strength{position:static;margin-bottom:8px}}
"""
_SCRIPT = r"""
(function(){
  const q=document.getElementById('search'), state=document.getElementById('state-filter');
  const apply=()=>{const needle=(q&&q.value||'').toLowerCase().trim(), wanted=state&&state.value||'all';
    document.querySelectorAll('[data-filter-card]').forEach(el=>{const hay=(el.getAttribute('data-search')||'').toLowerCase(), st=el.getAttribute('data-state')||'', work=el.getAttribute('data-work-status')||'';
      el.classList.toggle('hidden',(!!needle&&!hay.includes(needle))||(wanted!=='all'&&(wanted==='changed'?el.getAttribute('data-freshness')!=='changed':wanted==='outstanding'?el.getAttribute('data-outstanding')!=='true':['verified','deferred','implemented'].includes(wanted)?work!==wanted:st!==wanted)));});};
  if(q)q.addEventListener('input',apply);if(state)state.addEventListener('change',apply);
  document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{
    const target=document.getElementById((link.getAttribute('href')||'').slice(1));
    if(target&&target.matches('[data-filter-card]')&&target.classList.contains('hidden')){
      if(q)q.value='';if(state)state.value='all';apply();}}));
  document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{const value=button.getAttribute('data-copy')||'';
    try{if(navigator.clipboard&&navigator.clipboard.writeText)await navigator.clipboard.writeText(value);else{const t=document.createElement('textarea');t.value=value;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();let copied=false;try{copied=document.execCommand('copy');}finally{t.remove();}if(!copied)throw new Error('Clipboard unavailable');}
      const old=button.textContent;button.textContent='Copied';setTimeout(()=>button.textContent=old,1200);}catch(_){window.prompt('Copy this command',value);}}));
  let saved;
  document.querySelectorAll('[data-history-index]').forEach(detail=>detail.addEventListener('toggle',()=>{
    if(!detail.open||detail.dataset.loaded)return;
    if(!saved)saved=JSON.parse(document.getElementById('audit-codebase-state').textContent);
    detail.querySelector('pre').textContent=JSON.stringify(saved.history[Number(detail.dataset.historyIndex)],null,2);
    detail.dataset.loaded='true';
  }));
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


def _index_entries(root: Path, paths: Sequence[str] = ()) -> dict[str, dict[str, str]]:
    entries = {}
    for record in _git(root, "--literal-pathspecs", "ls-files", "--stage", "-z", "--", *paths).split("\0"):
        if not record:
            continue
        metadata, path = record.split("\t", 1)
        mode, object_id, stage = metadata.split()
        if stage != "0":
            raise ReportError(f"source index has an unresolved entry: {path}")
        entries[path.replace("\\", "/")] = {"mode": mode, "object_id": object_id}
    return entries


def _source_digest(root: Path, path: str, entries: dict[str, dict[str, str]]) -> bytes:
    target = root / path
    entry = entries.get(path)
    mode = entry["mode"] if entry else "untracked"
    if entry and entry["mode"] == "160000":
        resolved = target.resolve()
        if resolved == root or not resolved.is_relative_to(root):
            raise ReportError(f"gitlink checkout is outside repository: {path}")
        if target.is_symlink() or getattr(target, "is_junction", lambda: False)():
            raise ReportError(f"gitlink checkout is redirected: {path}")
        checkout = None
        if (target / ".git").exists():
            if Path(_git(target, "rev-parse", "--show-toplevel")).resolve() != resolved:
                raise ReportError(f"gitlink checkout does not own its worktree: {path}")
            checkout = inventory(repo_root=target)["identity"]
        elif target.is_dir():
            try:
                if any(target.iterdir()):
                    raise ReportError(f"gitlink directory is not a checkout: {path}")
            except OSError as exc:
                raise ReportError(f"cannot inspect gitlink directory: {path}: {exc}") from exc
        payload = {
            "mode": mode, "kind": "gitlink",
            "materialization": "directory" if target.is_dir() else "file" if target.is_file() else "missing",
            "checkout": checkout,
        }
        if payload["materialization"] == "file":
            try:
                payload["content_sha256"] = _digest(target.read_bytes())
                payload["executable_bits"] = target.stat().st_mode & 0o111
            except OSError as exc:
                raise ReportError(f"cannot read gitlink file: {path}: {exc}") from exc
    else:
        try:
            is_link = target.is_symlink()
            content = os.fsencode(os.readlink(target)) if is_link else target.read_bytes()
            payload = {"mode": mode, "kind": "symlink" if is_link else "file", "content_sha256": _digest(content)}
            if not is_link:
                payload["executable_bits"] = target.stat().st_mode & 0o111
        except FileNotFoundError as exc:
            if not entry:
                raise ReportError(f"source path does not exist: {path}") from exc
            payload = {"mode": mode, "kind": "missing"}
        except OSError as exc:
            raise ReportError(f"cannot read source path: {path}: {exc}") from exc
    if entry:
        payload["object_id"] = entry["object_id"]
    return hashlib.sha256(_canonical(payload)).digest()


def inventory(*, repo_root: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    entries = _index_entries(root)
    paths = sorted(entries)
    h = hashlib.sha256()
    fingerprints = {}
    for p in paths:
        fingerprint = _source_digest(root, p, entries)
        fingerprints[p] = fingerprint.hex()
        h.update(p.encode() + b"\0" + fingerprint)
    return {
        "response_version": RESPONSE_VERSION,
        "identity": {
            "commit": _git(root, "rev-parse", "HEAD"),
            "tree": _git(root, "show", "-s", "--format=%T", "HEAD"),
            "tracked_content_sha256": h.hexdigest(),
        },
        "tracked_paths": paths,
        "tracked_entries": entries,
        "fingerprints": fingerprints,
    }


def source_identity(*, repo_root: Path, paths: Sequence[str]) -> dict[str, Any]:
    root = repo_root.resolve()
    normalized = sorted({_rel(p, "path") for p in paths})
    if not normalized:
        raise ReportError("source-identity requires paths")
    entries = _index_entries(root, normalized)
    h = hashlib.sha256()
    fingerprints = {}
    for p in normalized:
        fingerprint = _source_digest(root, p, entries)
        fingerprints[p] = fingerprint.hex()
        h.update(p.encode() + b"\0" + fingerprint)
    return {
        "response_version": RESPONSE_VERSION,
        "paths": normalized,
        "sha256": h.hexdigest(),
        "fingerprints": fingerprints,
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


def _exclusions(value: object) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ReportError("excluded must be a list")
    excluded = []
    for i, raw in enumerate(value):
        item = _obj(raw, f"excluded[{i}]")
        _strict(item, {"path", "reason"}, set(), f"excluded[{i}]")
        excluded.append({"path": _rel(item["path"], "excluded path"),
                         "reason": _text(item["reason"], "excluded reason")})
    return excluded


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
    _strict(raw, fields - {"coverage"}, {"coverage"}, "map manifest")
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
    excluded = _exclusions(raw["excluded"])
    observed = inventory(repo_root=root)
    tracked = set(observed["tracked_paths"])
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
    if identity != observed["identity"]:
        raise ReportError("observation_identity does not match current repository")
    for sub in subs:
        packet = source_identity(repo_root=root, paths=sub["owned_paths"])
        sub["map_source"] = {k: packet[k] for k in ("paths", "sha256", "fingerprints")}
    state = {
        "state_version": STATE_VERSION,
        "title": _text(raw["title"], "title"),
        "observation_identity": identity,
        "systems": systems,
        "subsystems": subs,
        "excluded": excluded,
        "coverage": _text(raw.get("coverage", ""), "coverage", empty=True),
        "evidence_limits": _text(raw["evidence_limits"], "evidence limits", empty=True),
        "systemic_findings": [],
        "history": [{"operation": "map", "selection": "repository"}],
        "run_id": "",
        "observed_at": "",
        "freshness": {},
        "retired_subsystems": [],
        "outcomes": [],
        "delivery_requirements": [],
        "preview": [],
        "map_inventory": {"paths": observed["tracked_paths"], "fingerprints": observed["fingerprints"]},
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


def _diagram(value: object, label: str) -> dict[str, Any]:
    diagram = _obj(value, label)
    _strict(diagram, {"nodes", "edges"}, set(), label)
    if not isinstance(diagram["nodes"], list) or not diagram["nodes"]:
        raise ReportError(f"{label} needs at least one node")
    nodes = []
    for raw in diagram["nodes"]:
        node = _obj(raw, f"{label} node")
        _strict(node, {"id", "label"}, set(), f"{label} node")
        nodes.append({"id": _id(node["id"], "node id"), "label": _text(node["label"], "node label")})
    ids = [node["id"] for node in nodes]
    if len(ids) != len(set(ids)):
        raise ReportError(f"{label} has duplicate node ids")
    if not isinstance(diagram["edges"], list):
        raise ReportError(f"{label} edges must be a list")
    edges = []
    for raw in diagram["edges"]:
        edge = _obj(raw, f"{label} edge")
        _strict(edge, {"from", "to", "label"}, set(), f"{label} edge")
        if edge["from"] not in ids or edge["to"] not in ids:
            raise ReportError(f"{label} edge names unknown node")
        edges.append({"from": edge["from"], "to": edge["to"], "label": _text(edge["label"], "edge label", empty=True)})
    return {"nodes": nodes, "edges": edges}


def _comparison(value: object) -> dict[str, Any]:
    comparison = _obj(value, "comparison")
    _strict(comparison, {"caption", "before", "after"}, set(), "comparison")
    return {
        "caption": _text(comparison["caption"], "comparison caption"),
        "before": _diagram(comparison["before"], "before diagram"),
        "after": _diagram(comparison["after"], "after diagram"),
    }


def _candidate(value: object, label: str) -> dict[str, Any]:
    x = _obj(value, label)
    fields = {
        "id", "title", "primary_class", "strength", "finding_ids", "affected_scope",
        "problem", "evidence", "direction", "benefit", "risks", "required_proof",
    }
    _strict(x, fields, {"comparison"}, label)
    primary = _text(x["primary_class"], "primary class")
    strength = _text(x["strength"], "candidate strength")
    if primary not in _LENSES:
        raise ReportError("unsupported candidate class")
    if strength not in {"strong", "worth exploring", "speculative"}:
        raise ReportError("candidate strength must be strong, worth exploring, or speculative")
    result = {
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
    if "comparison" in x:
        result["comparison"] = _comparison(x["comparison"])
    return result


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
    _strict(raw, fields - {"coverage"}, {"coverage"}, "audit manifest")
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
        "coverage": _text(raw.get("coverage", ""), "coverage", empty=True),
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
    _strict(raw, fields, {"comparison"}, "analysis manifest")
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
    result = {
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
    if "comparison" in raw:
        result["comparison"] = _comparison(raw["comparison"])
    return result


def _source_packet(value: object, label: str) -> dict[str, Any]:
    packet = _obj(value, label)
    _strict(packet, {"paths", "sha256", "fingerprints"}, set(), label)
    paths = [
        _rel(path, f"{label} path")
        for path in _texts(packet["paths"], f"{label} paths", empty=False)
    ]
    sha = _text(packet["sha256"], f"{label} sha256")
    if not _SHA.fullmatch(sha):
        raise ReportError(f"{label} sha256 must be sha256")
    result = {"paths": sorted(paths), "sha256": sha}
    fingerprints = _obj(packet["fingerprints"], f"{label} fingerprints")
    if set(fingerprints) != set(paths) or any(not isinstance(value, str) or not _SHA.fullmatch(value) for value in fingerprints.values()):
        raise ReportError(f"{label} fingerprints must cover its paths with sha256 values")
    result["fingerprints"] = fingerprints
    return result


def _verify_source_packet(
    root: Path, packet: dict[str, Any], required_paths: Sequence[str]
) -> dict[str, Any]:
    if set(required_paths) - set(packet["paths"]):
        raise ReportError("source_identity omits required bound source")
    expected = source_identity(repo_root=root, paths=packet["paths"])
    actual = {"paths": packet["paths"], "sha256": packet["sha256"]}
    current = {"paths": expected["paths"], "sha256": expected["sha256"]}
    if actual != current:
        raise ReportError("source_identity does not match current bound source")
    if packet["fingerprints"] != expected["fingerprints"]:
        raise ReportError("source fingerprints do not match current bound source")
    return {k: expected[k] for k in ("paths", "sha256", "fingerprints")}


def _packet_observation(root: Path, packet: dict[str, Any]) -> dict[str, Any]:
    result = {"freshness": "fresh", "changed_paths": []}
    try:
        current = source_identity(repo_root=root, paths=packet["paths"])
        result["freshness"] = "fresh" if current["sha256"] == packet["sha256"] else "changed"
        result["changed_paths"] = sorted(path for path in packet["paths"] if current["fingerprints"][path] != packet["fingerprints"][path])
    except ReportError as exc:
        result["freshness"] = "changed"
        result["error"] = str(exc)
        for path in packet["paths"]:
            try:
                actual = source_identity(repo_root=root, paths=[path])["fingerprints"][path]
            except ReportError:
                actual = None
            if actual != packet["fingerprints"][path]:
                result["changed_paths"].append(path)
    return result


def _map_drift(state: dict[str, Any], root: Path) -> dict[str, Any]:
    tracked = {path.replace("\\", "/") for path in _git(root, "ls-files", "-z", "--").split("\0") if path}
    owned = {path for sub in state["subsystems"] for path in sub["owned_paths"]}
    excluded = {path for path in tracked for item in state["excluded"] if path == item["path"].rstrip("/") or path.startswith(item["path"].rstrip("/") + "/")}
    previous = set(state["map_inventory"]["paths"])
    unowned, missing = sorted(tracked - owned - excluded), sorted(owned - tracked)
    return {
        "added_paths": sorted(tracked - previous),
        "removed_paths": sorted(previous - tracked),
        "unowned_paths": unowned,
        "missing_owned_paths": missing,
        "needs_reconcile": bool(unowned or missing),
    }


def _catalog(state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    candidates, findings = {}, {}
    audit_indices, prior_audit_indices, analysis_indices = {}, {}, {}
    for index, event in enumerate(state["history"]):
        if event["operation"] == "audit":
            prior_audit_indices[index] = audit_indices.get(event["selection"], -1)
            audit_indices[event["selection"]] = index
        elif event["operation"] == "analyze":
            analysis_indices.setdefault(event["selection"], []).append(index)

    def add(audit: dict[str, Any], origin: str, historical: bool, systemic: Sequence[dict[str, Any]], audit_index: int, cutoff: int) -> None:
        for item in audit.get("candidates", []):
            analyses = [index for index in analysis_indices.get(item["id"], []) if index < cutoff]
            analysis_index = analyses[-1] if "analysis" in item and analyses else audit_index
            candidates.setdefault(item["id"], {"record": item, "origin": origin, "historical": historical, "audit_source": audit["source_identity"], "audit_index": audit_index, "analysis_index": analysis_index})
        for item in audit.get("findings", []) + list(systemic):
            findings.setdefault(item["id"], {"record": item, "origin": origin, "historical": historical, "audit_source": audit["source_identity"], "audit_index": audit_index})

    active = {sub["id"] for sub in state["subsystems"]}
    for sub in state["subsystems"] + state.get("retired_subsystems", []):
        if "audit" in sub:
            systemic = [item for item in state["systemic_findings"] if item["origin_subsystem_id"] == sub["id"]]
            add(sub["audit"], sub["id"], sub["id"] not in active, systemic, audit_indices.get(sub["id"], -1), len(state["history"]))
    for index, event in reversed(list(enumerate(state["history"]))):
        superseded = event.get("superseded", {})
        if "audit" in superseded:
            add(superseded["audit"], event["selection"], True, superseded.get("systemic_findings", []), prior_audit_indices.get(index, -1), index)
    return candidates, findings


def _target(value: object, state: dict[str, Any]) -> dict[str, str]:
    target = _obj(value, "outcome target")
    _strict(target, {"kind", "id"}, set(), "outcome target")
    kind = _text(target["kind"], "target kind")
    if kind not in {"candidate", "finding"}:
        raise ReportError("target kind must be candidate or finding")
    identifier = _id(target["id"], "target id")
    catalog = _catalog(state)[0 if kind == "candidate" else 1]
    if identifier not in catalog:
        raise ReportError(f"unknown {target['kind']} {identifier}")
    return {"kind": kind, "id": identifier}


def _outcome(value: object, state: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    raw = _obj(value, "outcome")
    optional = {"source_identity", "reference", "destination"} | ({"recorded_at", "finding_ids"} if root is None else set())
    _strict(raw, {"id", "target", "type", "summary", "evidence"}, optional, "outcome")
    kind = _text(raw["type"], "outcome type")
    if kind not in {"implemented", "verified", "deferred", "committed", "deployed", "reopened"}:
        raise ReportError("unsupported outcome type")
    result = {
        "id": _id(raw["id"], "outcome id"), "target": _target(raw["target"], state), "type": kind,
        "summary": _text(raw["summary"], "outcome summary"),
        "evidence": _texts(raw["evidence"], "outcome evidence", empty=False),
    }
    if kind in {"implemented", "verified"} and "source_identity" not in raw:
        raise ReportError(f"{kind} outcome requires its observed source identity")
    if result["target"]["kind"] == "candidate":
        ids = _catalog(state)[0][result["target"]["id"]]["record"]["finding_ids"] if root is not None else raw.get("finding_ids")
        result["finding_ids"] = _texts(ids, "outcome finding ids", empty=False)
        if set(result["finding_ids"]) - set(_catalog(state)[1]):
            raise ReportError("outcome names an unknown finding")
    elif "finding_ids" in raw:
        raise ReportError("only candidate outcomes bind a finding group")
    if "source_identity" in raw:
        packet = _source_packet(raw["source_identity"], "outcome source")
        result["source_identity"] = _verify_source_packet(root, packet, _outcome_required_paths(state, result)) if root is not None else packet
    if kind == "committed":
        reference = _text(raw.get("reference"), "commit reference")
        if not re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", reference):
            raise ReportError("committed outcome requires a full Git commit ID")
        result["reference"] = reference
    elif kind == "deployed":
        result["reference"] = _text(raw.get("reference"), "deployed version or evidence reference")
        result["destination"] = _text(raw.get("destination"), "deployment destination")
    if kind not in {"committed", "deployed"} and ({"reference", "destination"} & set(raw)):
        raise ReportError("delivery references require a committed or deployed outcome")
    if kind == "committed" and "destination" in raw:
        raise ReportError("commit outcome cannot name a deployment destination")
    result["recorded_at"] = _text(raw.get("recorded_at"), "outcome time") if root is None else _now()
    return result


def _delivery(value: object, state: dict[str, Any]) -> dict[str, Any]:
    raw = _obj(value, "delivery requirement")
    _strict(raw, {"target", "commit", "deployments", "reason"}, set(), "delivery requirement")
    if not isinstance(raw["commit"], bool):
        raise ReportError("delivery commit requirement must be boolean")
    return {"target": _target(raw["target"], state), "commit": raw["commit"],
            "deployments": _texts(raw["deployments"], "deployment destinations"), "reason": _text(raw["reason"], "delivery authority or reason")}


def _target_events(state: dict[str, Any], target: dict[str, str]) -> list[tuple[int, dict[str, Any]]]:
    return [(index, event) for index, event in enumerate(state["outcomes"])
            if event["target"] == target or (target["kind"] == "finding" and event["target"]["kind"] == "candidate" and target["id"] in event["finding_ids"])]


def _work_status(state: dict[str, Any], target: dict[str, str]) -> dict[str, Any]:
    candidates, findings = _catalog(state)
    item = (candidates if target["kind"] == "candidate" else findings)[target["id"]]
    own_events = _target_events(state, target)
    relevant = dict(own_events)
    linked = []
    if target["kind"] == "candidate":
        for fid in item["record"]["finding_ids"]:
            relevant.update(_target_events(state, {"kind": "finding", "id": fid}))
            linked.append(_work_status(state, {"kind": "finding", "id": fid})["status"])
    epoch = max((index for index, event in relevant.items() if event["type"] in {"implemented", "reopened"}), default=-1)
    current = [event for index, event in own_events if index >= epoch]
    decisions = [event for event in current if event["type"] in {"implemented", "verified", "deferred", "reopened"}]
    status = "historical" if item["historical"] else "open"
    if target["kind"] == "finding" and item["record"]["kind"] not in {"defect", "opportunity"}:
        status = item["record"]["kind"]
    if target["kind"] == "candidate" and item["record"]["state"] == "disproved":
        status = "disproved"
    group_changed = False
    if decisions:
        decision = decisions[-1]
        status = "open" if decision["type"] == "reopened" else decision["type"]
        if status == "verified" and state.get("outcome_freshness", {}).get(decision["id"]) != "fresh":
            status = "verification changed"
        if decision["type"] == "verified" and target["kind"] == "candidate":
            group_changed = set(decision["finding_ids"]) != set(item["record"]["finding_ids"])
            if group_changed:
                status = "verification changed"
    if target["kind"] == "candidate" and (not decisions or status in {"open", "implemented", "verified", "deferred", "verification changed"}) and not group_changed:
        if linked and all(value == "verified" for value in linked):
            status = "verified"
            verified_paths = set()
            for fid in item["record"]["finding_ids"]:
                decisions_for_finding = [event for _, event in _target_events(state, {"kind": "finding", "id": fid}) if event["type"] in {"implemented", "verified", "deferred", "reopened"}]
                verified_paths.update(decisions_for_finding[-1]["source_identity"]["paths"])
            if set(_required_paths(state, item["record"])) - verified_paths:
                status = "verification changed"
        elif linked and all(value == "deferred" for value in linked):
            status = "deferred"
        elif relevant:
            status = next((value for value in ("open", "verification changed", "implemented") if value in linked), "open")
    requirement = next((row for row in state.get("delivery_requirements", []) if row["target"] == target), None)
    commits = [event["reference"] for event in current if event["type"] == "committed"]
    deployments = [event["destination"] for event in current if event["type"] == "deployed"]
    return {"status": status, "commit_pending": bool(requirement and requirement["commit"] and not commits),
            "deployment_pending": sorted(set(requirement["deployments"]) - set(deployments)) if requirement else [],
            "commits": commits, "deployments": deployments, "outcome_ids": [relevant[index]["id"] for index in sorted(relevant)]}


def _current_scope(state: dict[str, Any], ids: Sequence[str]) -> set[str]:
    active = {sub["id"] for sub in state["subsystems"]}
    retired = {sub["id"]: sub for sub in state.get("retired_subsystems", [])}

    def resolve(sid: str, visited: set[str]) -> set[str]:
        if sid in active:
            return {sid}
        if sid not in retired or sid in visited:
            raise ReportError(f"unknown or cyclic retired subsystem: {sid}")
        result = set()
        for replacement in retired[sid]["retirement"]["replacement_ids"]:
            result |= resolve(replacement, visited | {sid})
        return result

    return set().union(*(resolve(sid, set()) for sid in ids))


def _required_paths(state: dict[str, Any], record: dict[str, Any]) -> list[str]:
    scope = set(record["affected_scope"]) | set(record.get("analysis", {}).get("affected_scope", []))
    owners = _current_scope(state, sorted(scope))
    return sorted({path for sub in state["subsystems"] if sub["id"] in owners for path in sub["owned_paths"]})


def _outcome_required_paths(state: dict[str, Any], event: dict[str, Any]) -> list[str]:
    candidates, findings = _catalog(state)
    target = event["target"]
    item = (candidates if target["kind"] == "candidate" else findings)[target["id"]]
    paths = set(_required_paths(state, item["record"]))
    for fid in event.get("finding_ids", []):
        paths.update(_required_paths(state, findings[fid]["record"]))
    return sorted(paths)


def _scope_observation(observation: dict[str, Any], packet: dict[str, Any], required_paths: Sequence[str]) -> dict[str, Any]:
    missing = set(required_paths) - set(packet["paths"])
    if not missing:
        return observation
    return {**observation, "freshness": "changed", "scope_changed": True,
            "changed_paths": sorted(set(observation["changed_paths"]) | missing)}


def _structure_observation(observation: dict[str, Any], owners: Sequence[str], since: int,
                           revisions: dict[int, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    later = sorted(index for index in revisions if index > since)
    if not later:
        return observation
    before, after = revisions[later[0]][0], revisions[later[-1]][1]
    changes = {}
    for sid in owners:
        prior, current = before.get(sid, {}), after.get(sid, {})
        fields = (set(prior) | set(current)) - {"id", "name", "state"}
        changed = sorted(field for field in fields if
                         (sorted(prior.get(field, [])) != sorted(current.get(field, [])) if field == "owned_paths"
                          else prior.get(field) != current.get(field)))
        if changed:
            changes[sid] = changed
    return {**observation, "freshness": "changed", "structure_changed": True, "structure_changes": changes} if changes else observation


def _candidate_observations(state: dict[str, Any], item: dict[str, Any], root: Path,
                            revisions: dict[int, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    if not item["historical"]:
        return state["candidate_source_changes"][item["record"]["id"]]
    packet = item["record"].get("analysis", {}).get("source_identity") or item["audit_source"]
    scoped = _scope_observation(_packet_observation(root, packet), packet, _required_paths(state, item["record"]))
    scope = set(item["record"]["affected_scope"]) | set(item["record"].get("analysis", {}).get("affected_scope", [])) | {item["origin"]}
    scoped = _structure_observation(scoped, sorted(scope | _current_scope(state, sorted(scope))), item["analysis_index"], revisions)
    audit = _structure_observation(_packet_observation(root, item["audit_source"]), [item["origin"]], item["audit_index"], revisions)
    return {"audit": audit, "analysis": scoped if "analysis" in item["record"] else None, "scope": scoped}


def _finding_scope_observation(state: dict[str, Any], item: dict[str, Any], observed: dict[str, Any],
                               revisions: dict[int, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    packet = item["audit_source"]
    scoped = _scope_observation(observed, packet, _required_paths(state, item["record"]))
    scope = set(item["record"]["affected_scope"]) | {item["origin"]}
    owners = scope | _current_scope(state, sorted(scope))
    return _structure_observation(scoped, sorted(owners), item["audit_index"], revisions)


def _finding_observations(state: dict[str, Any], item: dict[str, Any], root: Path,
                          revisions: dict[int, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    observed = state["source_changes"][item["origin"]] if not item["historical"] else _packet_observation(root, item["audit_source"])
    return {"audit": observed, "scope": _finding_scope_observation(state, item, observed, revisions)}


def _refresh_observation(state: dict[str, Any], root: Path) -> None:
    cache = {}
    revisions = _reconciliation_revisions(state)
    audit_indices = {item["selection"]: index for index, item in enumerate(state["history"]) if item["operation"] == "audit"}
    analysis_indices = {item["selection"]: index for index, item in enumerate(state["history"]) if item["operation"] == "analyze"}

    def observe(packet: dict[str, Any]) -> dict[str, Any]:
        key = _canonical(packet)
        if key not in cache:
            cache[key] = _packet_observation(root, packet)
        return cache[key]

    state["source_changes"] = {sub["id"]: observe(sub.get("audit", {}).get("source_identity") or sub["map_source"]) for sub in state["subsystems"]}
    for sub in state["subsystems"]:
        if "audit" in sub:
            state["source_changes"][sub["id"]] = _structure_observation(state["source_changes"][sub["id"]], [sub["id"]], audit_indices.get(sub["id"], -1), revisions)
            scope_change = sorted(set(sub["owned_paths"]) ^ set(sub["audit_scope"]))
            if scope_change:
                change = dict(state["source_changes"][sub["id"]])
                change.update(freshness="changed", scope_changed=True, changed_paths=sorted(set(change["changed_paths"]) | set(scope_change)))
                state["source_changes"][sub["id"]] = change
    state["freshness"] = {
        sub["id"]: state["source_changes"][sub["id"]]["freshness"]
        for sub in state["subsystems"]
    }
    state["candidate_source_changes"], state["candidate_freshness"] = {}, {}
    for sub in state["subsystems"]:
        for candidate in sub.get("audit", {}).get("candidates", []):
            packet = candidate.get("analysis", {}).get("source_identity") or sub["audit"]["source_identity"]
            scoped = _scope_observation(observe(packet), packet, _required_paths(state, candidate))
            scope = set(candidate["affected_scope"]) | set(candidate.get("analysis", {}).get("affected_scope", []))
            owners = scope | _current_scope(state, sorted(scope))
            since = analysis_indices.get(candidate["id"], -1) if "analysis" in candidate else audit_indices.get(sub["id"], -1)
            scoped = _structure_observation(scoped, sorted(owners), since, revisions)
            audit = state["source_changes"][sub["id"]]
            state["candidate_source_changes"][candidate["id"]] = {"audit": audit, "analysis": scoped if "analysis" in candidate else None, "scope": scoped}
            state["candidate_freshness"][candidate["id"]] = "changed" if audit["freshness"] == "changed" else scoped["freshness"]
    state["outcome_source_changes"] = {}
    for event in state["outcomes"]:
        if "source_identity" not in event:
            continue
        packet = event["source_identity"]
        state["outcome_source_changes"][event["id"]] = _scope_observation(observe(packet), packet, _outcome_required_paths(state, event))
    state["outcome_freshness"] = {eid: observation["freshness"] for eid, observation in state["outcome_source_changes"].items()}
    state["map_drift"] = _map_drift(state, root)
    state["observed_at"] = _now()


def _list(values: Sequence[str], empty: str = "None recorded") -> str:
    return "<ul class=\"compact\">" + "".join(f"<li>{escape(v)}</li>" for v in values) + "</ul>" if values else f'<span class="muted">{escape(empty)}</span>'


def _badge(value: str, label: str | None = None) -> str:
    cls = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return f'<span class="badge {escape(cls)}">{escape(label or value)}</span>'


def _live_systemic_findings(state: dict[str, Any]) -> list[dict[str, Any]]:
    active = {sub["id"] for sub in state["subsystems"]}
    return [finding for finding in state["systemic_findings"] if finding["origin_subsystem_id"] in active]


def _systemic_counts(state: dict[str, Any]) -> dict[str, int]:
    counts = {sub["id"]: 0 for sub in state["subsystems"]}
    for finding in _live_systemic_findings(state):
        for sid in _current_scope(state, finding["affected_scope"]):
            counts[sid] += 1
    return counts


def _architecture_svg(state: dict[str, Any]) -> str:
    systemic_counts = _systemic_counts(state)
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
            systemic_count = systemic_counts[sub["id"]]
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


def _finding_html(x: dict[str, Any], run_id: str, work: dict[str, Any] | None = None, observation: dict[str, Any] | None = None) -> str:
    extras = "".join(
        f"<dt>{escape(k.replace('_',' ').title())}</dt><dd>{escape(x[k])}</dd>"
        for k in ("severity","scenario","missing_evidence","boundary_reason","reentry","protected_constraint","ceiling","revisit_trigger")
        if k in x
    )
    search = " ".join([x["title"], x["kind"], x["primary_class"], x["impact"], x["direction"], *x["affected_scope"]])
    freshness = observation["freshness"] if observation else "fresh"
    command = f"$audit-codebase inspect finding {x['id']} in atlas run {run_id}"
    warning = '<p class="stale-warning">Finding evidence or affected ownership changed. Inspect changed inputs before reusing this judgment.</p>' if freshness == "changed" else ""
    return f'''<article class="card finding {escape(x["kind"].replace(" ","-"))}" data-filter-card data-state="{escape(x["kind"])}" data-freshness="{escape(freshness)}" data-work-status="{escape(work['status']) if work else ''}" data-outstanding="{str(_outstanding(work)).lower() if work else 'false'}" data-search="{escape(search,quote=True)}" id="finding-{escape(x["id"])}"><h3>{escape(x["title"])}</h3><div class="badges">{_badge(x["kind"])}{_badge(x["primary_class"])}{_badge(freshness, 'Finding inputs ' + freshness)}{_work_badges(work) if work else ""}</div>{warning}<p>{escape(x["impact"])}</p><dl class="kv"><dt>Causal owner</dt><dd>{escape(x["causal_owner"])}</dd><dt>Affected</dt><dd>{escape(", ".join(x["affected_scope"]))}</dd><dt>Direction</dt><dd>{escape(x["direction"])}</dd><dt>Confidence</dt><dd>{escape(x["confidence"])}</dd></dl><details class="evidence"><summary>Evidence and proof</summary><dl class="kv"><dt>Expectation</dt><dd>{escape(x["expectation"]) or '<span class="muted">None</span>'}</dd><dt>Locations</dt><dd>{_list(x["locations"])}</dd><dt>Evidence</dt><dd>{_list(x["evidence"])}</dd><dt>Proof</dt><dd>{_list(x["proof"])}</dd>{extras}</dl></details><div class="command"><button class="copy" data-copy="{escape(command, quote=True)}">Copy inspect command</button></div></article>'''


def _diagram_svg(diagram: dict[str, Any], label: str, marker: str) -> str:
    labels = {node["id"]: textwrap.wrap(node["label"], width=22) for node in diagram["nodes"]}
    edge_labels = [textwrap.wrap(edge["label"], width=28) for edge in diagram["edges"]]
    lanes = []
    cursor = 20
    for lines in edge_labels:
        lanes.append(cursor)
        cursor += max(28, 16 * len(lines) + 12)
    node_y = max(74, cursor + 24)
    node_height = max(60, 24 + 18 * max(len(lines) for lines in labels.values()))
    width = max(340, 30 + 210 * len(diagram["nodes"]))
    height = node_y + node_height + 26
    positions = {node["id"]: 30 + index * 210 for index, node in enumerate(diagram["nodes"])}
    parts = []
    for edge, lines, lane in zip(diagram["edges"], edge_labels, lanes):
        start, end = positions[edge["from"]] + 90, positions[edge["to"]] + 90
        if start == end:
            start, end = start - 35, end + 35
        middle = (start + end) // 2
        peak = lane + max(0, len(lines) - 1) * 16 + 8
        control_y = round((peak - node_y * .25) / .75)
        parts.append(
            f'<path d="M{start},{node_y} C{start},{control_y} {end},{control_y} {end},{node_y}" fill="none" '
            f'stroke="#67e8f9" marker-end="url(#{marker})"><title>{escape(edge["label"])}</title></path>'
        )
        for row, line in enumerate(lines):
            parts.append(f'<text x="{middle}" y="{lane+row*16}" text-anchor="middle">{escape(line)}</text>')
    for node in diagram["nodes"]:
        x = positions[node["id"]]
        parts.append(f'<rect x="{x}" y="{node_y}" width="180" height="{node_height}" rx="10"/>')
        for row, line in enumerate(labels[node["id"]]):
            parts.append(f'<text x="{x+90}" y="{node_y+24+row*18}" text-anchor="middle">{escape(line)}</text>')
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{escape(label, quote=True)}">'
        f'<title>{escape(label)}</title><defs><marker id="{marker}" markerWidth="8" markerHeight="8" '
        'refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#67e8f9"/></marker></defs>'
        + "".join(parts) + '</svg>'
    )


def _comparison_html(comparison: dict[str, Any], candidate_id: str) -> str:
    caption = comparison["caption"]
    before = _diagram_svg(comparison["before"], f'Before: {caption}', f'{candidate_id}-before-arrow')
    after = _diagram_svg(comparison["after"], f'Proposed: {caption}', f'{candidate_id}-after-arrow')
    return (
        f'<figure class="comparison"><figcaption>{escape(caption)}</figcaption><div class="compare">'
        f'<div><h4>Before</h4><div class="diagram">{before}</div></div>'
        f'<div><h4>Proposed</h4><div class="diagram">{after}</div></div></div></figure>'
    )


def _work_badges(work: dict[str, Any]) -> str:
    labels = {"open": "Work open", "implemented": "Implemented; verification pending", "verified": "Fix verified", "deferred": "Deferred",
              "verification changed": "Verification inputs changed", "historical": "Historical; outcome unrecorded", "disproved": "Proposal disproved"}
    badges = _badge(work["status"], labels.get(work["status"], work["status"]))
    if work["commits"]:
        badges += _badge("committed", "Committed")
    if work["commit_pending"]:
        badges += _badge("changed", "Commit pending")
    if work["deployments"]:
        badges += _badge("deployed", "Deployed: " + ", ".join(work["deployments"]))
    if work["deployment_pending"]:
        badges += _badge("changed", "Deployment pending: " + ", ".join(work["deployment_pending"]))
    return badges


def _candidate_commands(x: dict[str, Any], run_id: str, freshness: str, work: dict[str, Any]) -> tuple[str, str]:
    changed = freshness == "changed"
    command = (
        f"$audit-codebase inspect candidate {x['id']} in atlas run {run_id}"
        if changed or work["status"] in {"implemented", "verification changed", "verified", "deferred", "historical", "disproved"}
        else f"$audit-codebase analyze candidate {x['id']} in atlas run {run_id}"
    )
    next_action = ""
    if not changed and x["state"] == "analyzed" and work["status"] == "open":
        next_action = (
            f"Use analyzed audit candidate {x['id']} from atlas run {run_id}. "
            "Help me choose the appropriate next owner among direct implementation, "
            "$codebase-design, $prototype, or $to-tickets. Do not start the next workflow yet."
        )
    elif not changed and x["state"] == "blocked" and work["status"] == "open":
        next_action = (
            f"Use blocked audit candidate {x['id']} from atlas run {run_id}. "
            "Help me resolve the exact blocker without starting implementation."
        )
    return command, next_action


def _candidate_html(x: dict[str, Any], run_id: str, freshness: str, audit_id: str, audit_freshness: str, work: dict[str, Any]) -> str:
    analysis = x.get("analysis")
    changed = freshness == "changed"
    audit_changed = audit_freshness == "changed"
    freshness_cause = "audit" if audit_changed else "analysis" if changed else "none"
    search = " ".join([x["title"], x["primary_class"], x["strength"], x["problem"], x["direction"], *x["affected_scope"]])
    analysis_html = ""
    if analysis:
        options = "".join(
            f'<article class="option"><h5>{escape(o["name"])}</h5><p>{escape(o["description"])}</p>'
            f'<strong>Trade-offs</strong>{_list(o["tradeoffs"])}</article>' for o in analysis["options"]
        )
        heading = "Prior analysis: source changed" if changed else "Analysis"
        analysis_html = f'''<div class="panel" style="margin-top:12px"><h4>{heading}</h4>
<p>{escape(analysis["summary"])}</p><dl class="kv"><dt>Cause</dt><dd>{escape(analysis["cause"])}</dd>
<dt>Recommendation</dt><dd>{escape(analysis["recommendation"]) or '<span class="muted">None</span>'}</dd>
<dt>Trade-offs</dt><dd>{_list(analysis["tradeoffs"])}</dd><dt>Proof</dt><dd>{_list(analysis["proof"])}</dd>
<dt>Evidence limits</dt><dd>{escape(analysis["evidence_limits"]) or '<span class="muted">None</span>'}</dd>
<dt>Blocking question</dt><dd>{escape(analysis["question"]) or '<span class="muted">None</span>'}</dd>
</dl><div class="option-grid">{options}</div></div>'''
    command, next_action = _candidate_commands(x, run_id, freshness, work)
    command_label = "Copy inspect command" if " inspect candidate " in command else "Copy analyze command"
    next_button = (
        f'<button class="copy" data-copy="{escape(next_action, quote=True)}">Copy next-action handoff</button>'
        if next_action else ""
    )
    evidence_owner = "Audit" if audit_changed or not analysis else "Analysis"
    freshness_badge = _badge(freshness, f'{evidence_owner} source {freshness}')
    warning = ""
    if audit_changed:
        warning = '<p class="stale-warning">Originating audit evidence or ownership changed. Inspect changed paths and recorded outcomes to choose the necessary reassessment. Prior evidence is retained.</p>'
    elif changed:
        warning = '<p class="stale-warning">Analysis evidence changed. Inspect changed paths and recorded outcomes before reusing this recommendation. Prior evidence is retained.</p>'
    comparison = (analysis or {}).get("comparison") or x.get("comparison")
    visual = _comparison_html(comparison, x["id"]) if comparison else ""
    state_badge = _badge("changed", f'{x["state"]} (prior)') if changed else _badge(x["state"])
    return f'''<article class="card candidate" data-filter-card data-state="{escape(x["state"])}"
data-freshness="{freshness}" data-freshness-cause="{freshness_cause}" data-work-status="{escape(work['status'])}" data-outstanding="{str(_outstanding(work)).lower()}" data-search="{escape(search, quote=True)}" id="candidate-{escape(x["id"])}">
<div class="strength">{_badge(x["strength"], x["strength"].title())}</div><h3>{escape(x["title"])}</h3>
<div class="badges">{state_badge}{_badge(x["primary_class"])}{freshness_badge}{_work_badges(work)}</div>{warning}
<div class="compare"><div><h4>Current problem</h4><p>{escape(x["problem"])}</p></div>
<div><h4>Direction</h4><p>{escape(x["direction"])}</p><p class="muted">{escape(x["benefit"])}</p></div></div>
{visual}<dl class="kv"><dt>Affects</dt><dd>{escape(", ".join(x["affected_scope"]))}</dd>
<dt>Findings</dt><dd>{escape(", ".join(x["finding_ids"]))}</dd><dt>Risks</dt><dd>{_list(x["risks"])}</dd>
<dt>Required proof</dt><dd>{_list(x["required_proof"])}</dd></dl>
<details class="evidence"><summary>Evidence</summary>{_list(x["evidence"])}</details>{analysis_html}
<div class="command"><button class="copy" data-copy="{escape(command, quote=True)}">{command_label}</button>{next_button}</div></article>'''


def _coverage_counts(state: dict[str, Any]) -> dict[str, dict[str, int]]:
    coverage = {}
    for lens in _LENSES:
        counts = {name: 0 for name in ("complete", "not applicable", "evidence gap", "changed", "not audited")}
        for sub in state["subsystems"]:
            if "audit" not in sub:
                status = "not audited"
            elif state["freshness"][sub["id"]] == "changed":
                status = "changed"
            else:
                status = next(row["state"] for row in sub["audit"]["lenses"] if row["class"] == lens)
            counts[status] += 1
        coverage[lens] = counts
    return coverage


def _coverage_rows(state: dict[str, Any]) -> list[str]:
    rows = []
    total = len(state["subsystems"])
    for lens, counts in _coverage_counts(state).items():
        resolved = counts["complete"] + counts["not applicable"]
        detail = " · ".join(f'{count} {name}' for name, count in counts.items())
        segments = "".join(
            f'<span class="{name.replace(" ", "-")}" style="width:{count*100/total if total else 0:.2f}%" '
            f'title="{count} {name}"></span>' for name, count in counts.items()
        )
        attributes = " ".join(f'data-{name.replace(" ", "-")}="{count}"' for name, count in counts.items())
        rows.append(
            f'<div class="coverage-row" data-lens="{lens}" data-total="{total}" {attributes}>'
            f'<span>{escape(lens.title())}</span><div><div class="bar" role="img" '
            f'aria-label="{escape(detail, quote=True)}">{segments}</div>'
            f'<div class="coverage-detail">{escape(detail)}</div></div>'
            f'<span title="Current complete or not applicable / all mapped subsystems">{resolved}/{total}</span></div>'
        )
    return rows


def _maintenance_html(state: dict[str, Any]) -> str:
    def changed_inputs(observation: dict[str, Any]) -> str:
        metadata = [f"{sid}: {', '.join(fields)} changed" for sid, fields in sorted(observation.get("structure_changes", {}).items())]
        return _list(observation["changed_paths"] + metadata)

    candidates, findings = _catalog(state)
    revisions = _reconciliation_revisions(state)
    drift = state["map_drift"]
    warnings = []
    if drift["needs_reconcile"]:
        warnings.append(f'<div class="panel stale-warning"><strong>Ownership reconciliation needed</strong><p>{len(drift["unowned_paths"])} unowned tracked paths; {len(drift["missing_owned_paths"])} removed owned paths.</p>{_list((drift["unowned_paths"] + drift["missing_owned_paths"])[:20])}</div>')
    changes = []
    for sid, observation in state["source_changes"].items():
        if observation["freshness"] == "changed":
            changes.append(f'<li><a href="#subsystem-{escape(sid)}">{escape(sid)}</a>: changed inputs{changed_inputs(observation)}{escape(observation.get("error", ""))}</li>')
    for cid, observations in state["candidate_source_changes"].items():
        scoped = observations["scope"]
        if scoped["freshness"] == "changed":
            changes.append(f'<li><a href="#candidate-{escape(cid)}">{escape(cid)}</a>: candidate inputs or affected scope changed{changed_inputs(scoped)}{escape(scoped.get("error", ""))}</li>')
    for eid, observation in state["outcome_source_changes"].items():
        if observation["freshness"] == "changed":
            changes.append(f'<li><a href="#outcome-{escape(eid)}">{escape(eid)}</a>: outcome inputs or affected scope changed{_list(observation["changed_paths"])}{escape(observation.get("error", ""))}</li>')
    for fid, item in findings.items():
        if item["historical"]:
            continue
        observation = _finding_scope_observation(state, item, state["source_changes"][item["origin"]], revisions)
        if observation["freshness"] == "changed":
            changes.append(f'<li><a href="#finding-{escape(fid)}">{escape(fid)}</a>: finding inputs or affected scope changed{changed_inputs(observation)}{escape(observation.get("error", ""))}</li>')
    if changes:
        warnings.append('<details class="panel"><summary>Changed inputs and ownership</summary><ul class="compact">' + "".join(changes) + '</ul></details>')
    targets = {(_event["target"]["kind"], _event["target"]["id"]) for _event in state["outcomes"] + state["delivery_requirements"]}
    cards = []
    for kind, identifier in sorted(targets):
        target = {"kind": kind, "id": identifier}
        work = _work_status(state, target)
        entry = (candidates if kind == "candidate" else findings)[identifier]
        events = []
        applicable_ids = set(work["outcome_ids"])
        for event in state["outcomes"]:
            if event["id"] not in applicable_ids:
                continue
            basis = event.get("source_identity", {}).get("sha256", "")
            reference = event.get("reference", "")
            anchor = f' id="outcome-{escape(event["id"])}"' if event["target"] == target else ""
            origin = "" if anchor else f'<p class="muted"><a href="#outcome-{escape(event["id"])}">Recorded for {escape(event["target"]["kind"])} <code>{escape(event["target"]["id"])}</code></a></p>'
            events.append(f'<li{anchor}><strong>{escape(event["type"])}</strong>: {escape(event["summary"])}{origin}{_list(event["evidence"])}<code>{escape(reference)}</code>' + (f'<p class="muted">Observed source <code>{escape(basis)}</code> · {escape(state["outcome_freshness"][event["id"]])}</p>' if basis else "") + '</li>')
        cards.append(f'<article class="card" id="work-{kind}-{escape(identifier)}" data-filter-card data-state="outcome" data-work-status="{escape(work["status"])}" data-outstanding="{str(_outstanding(work)).lower()}" data-search="{escape(identifier + " " + entry["record"]["title"], quote=True)}"><h3>{escape(entry["record"]["title"])}</h3><p>{kind} <code>{escape(identifier)}</code></p><div class="badges">{_work_badges(work)}</div><details><summary>Outcome evidence</summary><ul class="compact">{"".join(events)}</ul></details></article>')
    preview = "".join(f'<li>{escape(record["environment"])} / {escape(record["capability"])}: {escape(record["state"])} — {escape(record["reason"])}' + (f'<p>Visually checked report revision <code>{escape(record["report_sha256"])}</code></p>' if record["state"] == "verified" else "") + '</li>' for record in state["preview"])
    archived = []
    for kind, catalog in (("candidate", candidates), ("finding", findings)):
        for identifier, entry in sorted(catalog.items()):
            if not entry["historical"]:
                continue
            work = _work_status(state, {"kind": kind, "id": identifier})
            command = f"$audit-codebase inspect {kind} {identifier} in atlas run {state['run_id']}"
            archived.append(f'<article class="card" id="{kind}-{escape(identifier)}" data-filter-card data-state="historical" data-work-status="{escape(work["status"])}" data-outstanding="{str(_outstanding(work)).lower()}" data-search="{escape(identifier + " " + entry["record"]["title"], quote=True)}"><h3>{escape(entry["record"]["title"])}</h3><p>Historical {kind} <code>{escape(identifier)}</code> · Original owner <code>{escape(entry["origin"])}</code></p>{_work_badges(work)}<div class="command"><button class="copy" data-copy="{escape(command, quote=True)}">Copy inspect command</button></div></article>')
    history = '<details class="panel"><summary>Historical candidates and findings</summary><div class="grid">' + "".join(archived) + '</div></details>' if archived else ""
    return '<section class="section" id="outcomes"><div class="section-head"><div><h2>Work outcomes and delivery</h2><p>Audit evidence, fix verification, and delivery are separate records. Source changes call for inspection of affected conclusions.</p></div></div>' + "".join(warnings) + '<div class="grid">' + ("".join(cards) or '<div class="panel muted">No work outcomes recorded.</div>') + '</div>' + history + '<details class="panel"><summary>Preview capability and visual verification</summary>' + (_list([]) if not preview else '<ul class="compact">' + preview + '</ul>') + '<p>Static report checks do not establish visual verification.</p></details></section>'


def _render(state: dict[str, Any]) -> bytes:
    identity, subsystems = state["observation_identity"], state["subsystems"]
    audited = [x for x in subsystems if x["state"] == "audited"]
    changed = [x for x in subsystems if state["freshness"].get(x["id"]) == "changed"]
    systemic = _live_systemic_findings(state)
    systemic_counts = _systemic_counts(state)
    findings = [x for sub in audited for x in sub["audit"]["findings"]] + systemic
    finding_catalog = _catalog(state)[1]
    revisions = _reconciliation_revisions(state)
    candidates = [x for sub in audited for x in sub["audit"]["candidates"]]
    candidate_owners = {x["id"]: sub["id"] for sub in audited for x in sub["audit"]["candidates"]}
    gap_count = sum(1 for sub in audited if state["freshness"][sub["id"]] == "fresh" for lens in sub["audit"]["lenses"] if lens["state"] == "evidence gap")
    current_audits = sum(state["freshness"][sub["id"]] == "fresh" for sub in audited)
    changed_candidates = sum(value == "changed" for value in state["candidate_freshness"].values())
    metrics = [("Subsystems",len(subsystems)),("Current audits",current_audits),("Not audited",len(subsystems)-len(audited)),("Changed subsystems",len(changed)),("Findings",len(findings)),("Candidates",len(candidates)),("Changed candidates",changed_candidates)]
    summary = _summary(state)
    metrics += [("Previously audited", len(audited)), ("Outstanding candidates", summary["outstanding_candidates"]), ("Fixes verified", summary["verified_candidates"]), ("Deferred candidates", summary["deferred_candidates"]), ("Delivery pending", summary["delivery_pending"])]
    metric_html = "".join(f'<div class="metric"><strong>{v}</strong><span>{escape(k)}</span></div>' for k,v in metrics)
    lens_rows = _coverage_rows(state)
    cards={}
    audits=[]
    for sub in subsystems:
        audit=sub.get("audit")
        systemic_count=systemic_counts[sub["id"]]
        fc=(len(audit["findings"]) if audit else 0)+systemic_count
        cc=len(audit["candidates"]) if audit else 0
        fresh=state["freshness"].get(sub["id"],"fresh"); deps=[d["id"] for d in sub["dependencies"]]
        search=" ".join([sub["name"],sub["purpose"],sub["ownership"],sub["system_id"],*deps])
        command=f"$audit-codebase audit subsystem {sub['id']} in atlas run {state['run_id']}"
        dep_detail="".join(f'<li><a href="#subsystem-{escape(d["id"])}">{escape(d["id"])}</a>: {escape("; ".join(d["evidence"]))}</li>' for d in sub["dependencies"]) or '<li class="muted">None recorded</li>'
        cards[sub["id"]]=f'''<article class="card" id="subsystem-{escape(sub["id"])}" data-filter-card data-state="{escape(sub["state"])}" data-freshness="{fresh}" data-search="{escape(search,quote=True)}"><h3>{escape(sub["name"])}</h3><div class="badges">{_badge(sub["state"])}{_badge("changed" if fresh=="changed" else "fresh","Source changed" if fresh=="changed" else "Source fresh")}{_badge(sub["system_id"])}</div><p>{escape(sub["purpose"])}</p><dl class="kv"><dt>Ownership</dt><dd>{escape(sub["ownership"])}</dd><dt>Dependencies</dt><dd>{escape(", ".join(deps)) if deps else '<span class="muted">None</span>'}</dd><dt>Audit result</dt><dd>{fc} findings · {cc} candidates</dd></dl><details class="evidence"><summary>Architecture evidence</summary><dl class="kv"><dt>Authority</dt><dd>{_list(sub["authority"])}</dd><dt>Callers</dt><dd>{_list(sub["callers"])}</dd><dt>Dependencies</dt><dd><ul class="compact">{dep_detail}</ul></dd><dt>Interfaces</dt><dd>{_list(sub["interfaces"])}</dd><dt>Proof seams</dt><dd>{_list(sub["proof_seams"])}</dd><dt>Owned paths</dt><dd>{_list(sub["owned_paths"])}</dd><dt>Exclusions</dt><dd>{_list(sub["exclusions"])}</dd></dl></details><div class="command"><button class="copy" data-copy="{escape(command,quote=True)}">Copy audit command</button></div></article>'''
        if audit:
            trace=audit["source_trace"]
            lens_html="".join(f'<tr><td>{escape(row["class"])}</td><td>{_badge(row["state"])}</td><td>{escape(row["reason"])}</td><td>{_list(row["evidence"])}</td></tr>' for row in audit["lenses"])
            audits.append(f'''<article class="panel" id="audit-{escape(sub["id"])}"><div class="section-head"><div><h2>{escape(sub["name"])}</h2><p>{escape(trace["summary"])}</p></div><div class="badges">{_badge("audited", "Previously audited")}{_badge(fresh,"Audit source "+fresh)}{_badge("evidence-gap",f"{sum(1 for x in audit['lenses'] if x['state']=='evidence gap')} gaps")}</div></div><div class="table-scroll"><table class="lens-table"><thead><tr><th>Lens</th><th>Coverage</th><th>Reason</th><th>Evidence</th></tr></thead><tbody>{lens_html}</tbody></table></div><details class="evidence"><summary>Source trace</summary><dl class="kv"><dt>Entry points</dt><dd>{_list(trace["entry_points"])}</dd><dt>Callers</dt><dd>{_list(trace["callers"])}</dd><dt>Dependencies</dt><dd>{_list(trace["dependencies"])}</dd><dt>Interfaces</dt><dd>{_list(trace["interfaces"])}</dd><dt>Proof seams</dt><dd>{_list(trace["proof_seams"])}</dd><dt>Representative flows</dt><dd>{_list(trace["representative_flows"])}</dd><dt>History signals</dt><dd>{_list(trace["history_signals"])}</dd><dt>Evidence limits</dt><dd>{escape(audit["evidence_limits"]) or '<span class="muted">None</span>'}</dd></dl></details><p><strong>Audit recommendation:</strong> {escape(audit["recommendation"])}</p></article>''')
    systems_index="".join(f'<section id="system-{escape(system["id"])}"><h3>{escape(system["name"])}</h3><div class="grid">{"".join(cards[sub["id"]] for sub in subsystems if sub["system_id"]==system["id"])}</div></section>' for system in state["systems"])
    candidates=sorted(candidates,key=lambda x:({"strong":0,"worth exploring":1,"speculative":2}[x["strength"]],x["title"]))
    candidate_html="".join(
        _candidate_html(x, state["run_id"], state["candidate_freshness"][x["id"]], candidate_owners[x["id"]], state["freshness"][candidate_owners[x["id"]]], _work_status(state, {"kind": "candidate", "id": x["id"]}))
        for x in candidates
    )
    finding_html="".join(_finding_html(x, state["run_id"], _work_status(state, {"kind": "finding", "id": x["id"]}),
                                     _finding_scope_observation(state, finding_catalog[x["id"]], state["source_changes"][finding_catalog[x["id"]]["origin"]], revisions)) for x in findings)
    excluded="".join(f'<li><code>{escape(x["path"])}</code>: {escape(x["reason"])}</li>' for x in state["excluded"]) or '<li class="muted">None</li>'
    history="".join(f'<li>{escape(x["operation"])} · {escape(x["selection"])}<details data-history-index="{index}"><summary>Stored record</summary><pre class="history-record"></pre></details></li>' for index, x in enumerate(state["history"]))
    maintenance = _maintenance_html(state)
    nav_systems="".join(f'<a href="#system-{escape(s["id"])}">{escape(s["name"])}</a>' for s in state["systems"])
    raw=_canonical(state); embedded=raw.decode().replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="audit-codebase-report-version" content="{REPORT_VERSION}"><title>{escape(state["title"])}</title><style>{_STYLE}</style></head><body><div class="shell"><aside class="sidebar"><div class="brand">Audit atlas</div><nav><a href="#overview">Overview</a><a href="#architecture">Architecture</a><a href="#subsystems">Subsystems</a><a href="#audits">Audits</a><a href="#findings">Findings</a><a href="#candidates">Candidates</a><a href="#outcomes">Outcomes</a><a href="#evidence">Evidence</a><a href="#history">History</a>{nav_systems}</nav><div class="minor">Run <code>{escape(state["run_id"])}</code><br>Observed {escape(state["observed_at"])}</div></aside><main class="content"><header class="hero" id="overview"><div><h1>{escape(state["title"])}</h1><p>Visual architecture map and evidence-backed improvement workbench. Select a subsystem to audit, then a candidate to analyze.</p></div><div class="hero-meta">Commit <code>{escape(identity["commit"][:12])}</code><br>Tree <code>{escape(identity["tree"][:12])}</code></div></header><div class="metrics">{metric_html}</div><section class="section"><div class="section-head"><div><h2>Audit coverage</h2><p>All mapped subsystems; current complete and non-applicable assessments count as resolved.</p></div><div class="badges">{_badge("evidence-gap",f"{gap_count} evidence gaps")}</div></div><div class="panel">{"".join(lens_rows)}</div></section><section class="section" id="architecture"><div class="section-head"><div><h2>Architecture map</h2><p>Dependencies are directional. Click a subsystem to inspect it.</p></div></div><div class="panel architecture">{_architecture_svg(state)}<div class="legend"><span><i class="dot mapped"></i>mapped</span><span><i class="dot audited"></i>audited</span><span><i class="dot changed"></i>source changed</span></div></div></section><section class="section" id="subsystems"><div class="section-head"><div><h2>Subsystem explorer</h2><p>Search the map, then copy the exact drill-down command.</p></div></div><div class="toolbar"><input id="search" type="search" placeholder="Search subsystems, findings, candidates..."><select id="state-filter"><option value="all">All states</option><option value="mapped">Mapped</option><option value="audited">Audited</option><option value="presented">Candidate: presented</option><option value="analyzed">Candidate: analyzed</option><option value="blocked">Candidate: blocked</option><option value="disproved">Candidate: disproved</option><option value="changed">Source changed</option><option value="outstanding">Outstanding work</option><option value="verified">Fix verified</option><option value="deferred">Deferred</option><option value="implemented">Implemented</option></select></div>{systems_index}</section><section class="section" id="audits"><div class="section-head"><div><h2>Audit records</h2><p>Meaning first; source trace and evidence stay expandable.</p></div></div>{"".join(audits) or '<div class="panel muted">Audit a mapped subsystem to populate this section.</div>'}</section><section class="section" id="findings"><div class="section-head"><div><h2>Findings</h2><p>Defects, opportunities, retained complexity, and explicit evidence gaps.</p></div></div><div class="grid">{finding_html or '<div class="panel muted">No admitted findings yet.</div>'}</div></section><section class="section" id="candidates"><div class="section-head"><div><h2>Improvement candidates</h2><p>Qualitative strength, not a numeric architecture score. Select one to analyze.</p></div></div><div class="grid">{candidate_html or '<div class="panel muted">Audit a subsystem to produce selectable candidates.</div>'}</div></section>{maintenance}<section class="section" id="evidence"><div class="section-head"><div><h2>Evidence and provenance</h2><p>Forensic detail is preserved without dominating the decision view.</p></div></div><div class="panel"><dl class="kv"><dt>Tracked content</dt><dd><code>{escape(identity["tracked_content_sha256"])}</code></dd><dt>Evidence limits</dt><dd>{escape(state["evidence_limits"]) or '<span class="muted">None</span>'}</dd><dt>Excluded paths</dt><dd><ul class="compact">{excluded}</ul></dd></dl></div></section><section class="section" id="history"><div class="section-head"><div><h2>History</h2><p>Mapping, audit, analysis, and work records. Historical evidence is available on demand.</p></div></div><div class="panel"><ol class="history">{history}</ol></div></section><footer>Audit-codebase workbench format {REPORT_VERSION}. Read-only HTML; copy commands return control to the agent.</footer></main></div><script id="audit-codebase-state" type="application/json" data-sha256="{_digest(raw)}">{embedded}</script><script>{_SCRIPT}</script></body></html>'''
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
        if sub.get("state") != ("audited" if "audit" in sub else "mapped"):
            raise ReportError("subsystem state does not match its audit record")
        if state["freshness"][sub["id"]] not in {"fresh","changed"}: raise ReportError("invalid subsystem freshness")
        if "audit" in sub:
            if sub.get("state")!="audited": raise ReportError("audit requires audited state")
            scope = _texts(sub.get("audit_scope"), "original audit ownership", empty=False)
            if set(scope) - set(sub["audit"]["source_identity"]["paths"]):
                raise ReportError("audit source omits its recorded ownership scope")
            _lenses(sub["audit"].get("lenses"))
            fids += [x.get("id") for x in sub["audit"].get("findings",[])]
            cids += [x.get("id") for x in sub["audit"].get("candidates",[])]
            for candidate in sub["audit"].get("candidates", []):
                if "comparison" in candidate:
                    _comparison(candidate["comparison"])
                if "analysis" in candidate:
                    _source_packet(candidate["analysis"].get("source_identity"), "analysis source")
                    if "comparison" in candidate["analysis"]:
                        _comparison(candidate["analysis"]["comparison"])
    if len(fids)!=len(set(fids)) or len(cids)!=len(set(cids)): raise ReportError("duplicate finding or candidate ids")
    candidate_freshness = _obj(state.get("candidate_freshness"), "candidate freshness")
    if set(candidate_freshness) != set(cids):
        raise ReportError("freshness must cover every candidate")
    if any(value not in {"fresh", "changed"} for value in candidate_freshness.values()):
        raise ReportError("invalid candidate freshness")
    required = {"retired_subsystems", "outcomes", "delivery_requirements", "preview", "map_inventory", "map_drift", "source_changes", "candidate_source_changes", "outcome_freshness", "outcome_source_changes"}
    if required - set(state):
        raise ReportError("report is missing maintained workbench records")
    for name in ("retired_subsystems", "outcomes", "delivery_requirements", "preview", "history"):
        if not isinstance(state[name], list):
            raise ReportError(f"report {name} must be a list")
    _reconciliation_revisions(state)
    retired_ids = [sub["id"] for sub in state["retired_subsystems"]]
    if len(retired_ids) != len(set(retired_ids)) or set(retired_ids) & set(sids):
        raise ReportError("retired subsystem ids must remain unique and separate")
    known = set(sids + retired_ids)
    system_ids = [system["id"] for system in state["systems"]]
    if len(system_ids) != len(set(system_ids)):
        raise ReportError("duplicate system ids")
    owned = []
    for sub in state["subsystems"] + state["retired_subsystems"]:
        specification = {key: value for key, value in sub.items() if key not in {"audit", "state", "map_source", "retirement", "audit_scope"}}
        _subsystem(specification, "stored subsystem")
        if sub["id"] in sids:
            if sub["system_id"] not in system_ids or any(dep["id"] not in sids for dep in sub["dependencies"]):
                raise ReportError("current subsystem has an unknown system or dependency")
            owned += sub["owned_paths"]
        else:
            retirement = _obj(sub.get("retirement"), "retirement")
            _strict(retirement, {"replacement_ids", "reason"}, set(), "retirement")
            _text(retirement["reason"], "retirement reason")
            replacements = _texts(retirement["replacement_ids"], "retirement replacements")
            if set(replacements) - known:
                raise ReportError("retirement names an unknown replacement")
            _current_scope(state, [sub["id"]])
        if "audit" in sub:
            audit = sub["audit"]
            packet = {key: audit[key] for key in ("source_identity", "source_trace", "lenses", "findings", "coverage", "evidence_limits", "recommendation")}
            packet.update(version=MANIFEST_VERSION, expected_report_sha256="0" * 64, subsystem_id=sub["id"], systemic_findings=[{key: value for key, value in item.items() if key != "origin_subsystem_id"} for item in state["systemic_findings"] if item["origin_subsystem_id"] == sub["id"]])
            packet["candidates"] = [{key: value for key, value in candidate.items() if key not in {"analysis", "state"}} for candidate in audit["candidates"]]
            _audit(packet)
            _source_packet(audit["source_identity"], "stored audit source")
            if any(set(finding["affected_scope"]) - known for finding in audit["findings"]):
                raise ReportError("finding names an unknown affected subsystem")
            for candidate in audit["candidates"]:
                if candidate.get("state") not in {"presented", "analyzed", "blocked", "disproved"} or (candidate["state"] != "presented") != ("analysis" in candidate):
                    raise ReportError("candidate state does not match its analysis record")
                if set(candidate["affected_scope"]) - known:
                    raise ReportError("candidate names an unknown affected subsystem")
                if "analysis" in candidate:
                    analysis = dict(candidate["analysis"])
                    analysis.update(version=MANIFEST_VERSION, expected_report_sha256="0" * 64, candidate_id=candidate["id"], state=candidate["state"])
                    _analysis(analysis)
                    if set(analysis["affected_scope"]) - known:
                        raise ReportError("analysis names an unknown affected subsystem")
    if len(owned) != len(set(owned)):
        raise ReportError("stored paths have multiple owners")
    for item in state["systemic_findings"]:
        if item["origin_subsystem_id"] not in known or set(item["affected_scope"]) - known:
            raise ReportError("systemic finding names an unknown subsystem")
    ids = []
    for event in state["outcomes"]:
        _outcome(event, state)
        ids.append(event["id"])
    if len(ids) != len(set(ids)):
        raise ReportError("duplicate outcome ids")
    bound_outcomes = {event["id"] for event in state["outcomes"] if "source_identity" in event}
    if set(state["outcome_source_changes"]) != bound_outcomes or set(state["outcome_freshness"]) != bound_outcomes:
        raise ReportError("source observations must cover all bound outcomes")
    targets = []
    for requirement in state["delivery_requirements"]:
        targets.append(_canonical(_delivery(requirement, state)["target"]))
    if len(targets) != len(set(targets)):
        raise ReportError("duplicate delivery requirements")
    for record in state["preview"]:
        _preview_record(record, stored=True)
    preview_keys = [(record["environment"], record["capability"]) for record in state["preview"]]
    if len(preview_keys) != len(set(preview_keys)):
        raise ReportError("duplicate preview capability records")
    baseline = _obj(state["map_inventory"], "map inventory")
    _strict(baseline, {"paths", "fingerprints"}, set(), "map inventory")
    baseline_paths = [_rel(path, "inventory path") for path in _texts(baseline["paths"], "inventory paths")]
    fingerprints = _obj(baseline["fingerprints"], "inventory fingerprints")
    if set(fingerprints) != set(baseline_paths) or any(not isinstance(value, str) or not _SHA.fullmatch(value) for value in fingerprints.values()):
        raise ReportError("map inventory fingerprints must cover all paths")
    exclusions = []
    for item in state["excluded"]:
        item = _obj(item, "stored exclusion")
        _strict(item, {"path", "reason"}, set(), "stored exclusion")
        exclusions.append(_rel(item["path"], "excluded path").rstrip("/"))
        _text(item["reason"], "exclusion reason")
    excluded_paths = {path for path in baseline_paths for prefix in exclusions if path == prefix or path.startswith(prefix + "/")}
    if set(owned) & excluded_paths or set(owned) | excluded_paths != set(baseline_paths):
        raise ReportError("stored ownership does not cover its map inventory exactly once")


def _preview_record(value: object, *, stored: bool = False) -> dict[str, Any]:
    raw = _obj(value, "preview record")
    _strict(raw, {"environment", "capability", "state", "reason", "evidence"}, {"report_sha256"} | ({"recorded_at"} if stored else set()), "preview record")
    preview_state = _text(raw["state"], "preview state")
    if preview_state not in {"unavailable", "verified"}:
        raise ReportError("preview state must be unavailable or verified")
    result = {key: _text(raw[key], f"preview {key}") for key in ("environment", "capability", "state", "reason")}
    result["evidence"] = _texts(raw["evidence"], "preview evidence", empty=False)
    if preview_state == "verified":
        digest = _text(raw.get("report_sha256"), "visually checked report digest")
        if not _SHA.fullmatch(digest):
            raise ReportError("visual verification requires the checked report digest")
        result["report_sha256"] = digest
    elif "report_sha256" in raw:
        raise ReportError("environment limitations do not claim report verification")
    result["recorded_at"] = _text(raw.get("recorded_at"), "preview time") if stored else _now()
    return result


def _reconcile(raw: dict[str, Any], state: dict[str, Any], root: Path) -> dict[str, Any]:
    _strict(raw, {"version", "expected_report_sha256", "observation_identity"}, {"title", "systems", "subsystems", "ownership_changes", "excluded", "retirements", "coverage", "evidence_limits"}, "reconciliation manifest")
    for name in ("subsystems", "ownership_changes", "retirements"):
        if name in raw and not isinstance(raw[name], list):
            raise ReportError(f"reconciliation {name} must be a list")
    structural_keys = {"id", "system_id", "name", "purpose", "ownership", "authority", "callers", "dependencies", "interfaces", "proof_seams", "owned_paths", "exclusions"}
    definitions = {sub["id"]: {key: value for key, value in sub.items() if key in structural_keys} for sub in state["subsystems"]}
    previous_ids = set(definitions)
    retired_ids = {sub["id"] for sub in state["retired_subsystems"]}
    patched = set()
    for patch in raw.get("subsystems", []):
        patch = _obj(patch, "subsystem patch")
        _strict(patch, {"id"}, structural_keys - {"id"}, "subsystem patch")
        sid = _id(patch["id"], "subsystem patch id")
        if sid in patched:
            raise ReportError("subsystem patches repeat an id")
        patched.add(sid)
        if sid in retired_ids:
            raise ReportError("retired subsystem ids cannot be reused")
        definitions[sid] = {**definitions.get(sid, {}), **patch}
    retirements = {}
    for value in raw.get("retirements", []):
        value = _obj(value, "retirement")
        _strict(value, {"id", "replacement_ids", "reason"}, set(), "retirement")
        sid = _id(value["id"], "retired subsystem id")
        if sid not in previous_ids or sid in retirements:
            raise ReportError("retirements must name distinct current subsystems")
        retirements[sid] = {"replacement_ids": _texts(value["replacement_ids"], "replacement ids"), "reason": _text(value["reason"], "retirement reason")}
        definitions.pop(sid, None)
    excluded = _exclusions(raw.get("excluded", state["excluded"]))
    for sid, definition in definitions.items():
        definition["owned_paths"] = [_rel(path, f"{sid} owned path") for path in
                                     _texts(definition.get("owned_paths", []), f"{sid} owned_paths")]
    tracked = set(inventory(repo_root=root)["tracked_paths"])
    changes = []
    changed_paths = set()
    for value in raw.get("ownership_changes", []):
        change = _obj(value, "ownership change")
        _strict(change, {"path", "owner", "reason"}, set(), "ownership change")
        path, reason = _rel(change["path"], "ownership path"), _text(change["reason"], "ownership reason")
        if path in changed_paths:
            raise ReportError("ownership changes repeat a path")
        changed_paths.add(path)
        owner = _id(change["owner"], "new owner id") if change["owner"] is not None else None
        if owner is not None and owner not in definitions:
            raise ReportError("ownership change names an unknown current subsystem")
        for definition in definitions.values():
            definition["owned_paths"] = [item for item in definition.get("owned_paths", []) if item != path]
        if owner is not None:
            definitions[owner].setdefault("owned_paths", []).append(path)
            excluded = [item for item in excluded if item["path"] != path]
        elif path in tracked and not any(path == item["path"] or path.startswith(item["path"].rstrip("/") + "/") for item in excluded):
            excluded.append({"path": path, "reason": reason})
        changes.append({"path": path, "owner": owner, "reason": reason})
    mapped = _map({"version": MANIFEST_VERSION, "expected_report_sha256": "absent", "title": raw.get("title", state["title"]),
                   "observation_identity": raw["observation_identity"], "systems": raw.get("systems", state["systems"]),
                   "subsystems": list(definitions.values()), "excluded": excluded, "coverage": raw.get("coverage", state["coverage"]),
                   "evidence_limits": raw.get("evidence_limits", state["evidence_limits"])}, root)
    old = {sub["id"]: sub for sub in state["subsystems"]}
    for sub in mapped["subsystems"]:
        if "audit" in old.get(sub["id"], {}):
            sub["audit"] = old[sub["id"]]["audit"]
            sub["state"] = "audited"
            sub["audit_scope"] = old[sub["id"]]["audit_scope"]
    history = {"operation": "reconcile", "selection": "repository", "ownership_changes": changes, "retirements": retirements,
               "superseded": {"map": {key: state[key] for key in ("observation_identity", "systems", "excluded", "map_inventory")}}}
    history["superseded"]["map"]["subsystems"] = [{key: value for key, value in sub.items() if key != "audit"} for sub in state["subsystems"]]
    for sid, retirement in retirements.items():
        state["retired_subsystems"].append({**old[sid], "retirement": retirement})
    for key in ("title", "observation_identity", "systems", "subsystems", "excluded", "coverage", "evidence_limits", "map_inventory"):
        state[key] = mapped[key]
    state["history"].append(history)
    return state


def _record_outcomes(raw: dict[str, Any], state: dict[str, Any], root: Path) -> dict[str, Any]:
    _strict(raw, {"version", "expected_report_sha256"}, {"events", "delivery_requirements"}, "outcome manifest")
    events, requirements = raw.get("events", []), raw.get("delivery_requirements", [])
    if not isinstance(events, list) or not isinstance(requirements, list) or not (events or requirements):
        raise ReportError("record-outcome requires events or delivery requirements")
    normalized = [_outcome(value, state, root) for value in events]
    existing = {event["id"] for event in state["outcomes"]}
    ids = [event["id"] for event in normalized]
    if existing & set(ids) or len(ids) != len(set(ids)):
        raise ReportError("outcome ids must be new and unique")
    normalized_requirements = [_delivery(value, state) for value in requirements]
    targets = [_canonical(row["target"]) for row in normalized_requirements]
    if len(targets) != len(set(targets)):
        raise ReportError("delivery requirements repeat a target")
    previous = [row for row in state["delivery_requirements"] if _canonical(row["target"]) in targets]
    state["delivery_requirements"] = [row for row in state["delivery_requirements"] if _canonical(row["target"]) not in targets] + normalized_requirements
    state["outcomes"] += normalized
    state["history"].append({"operation": "outcome", "selection": ", ".join(f"{event['target']['kind']}:{event['target']['id']}" for event in normalized) or "delivery requirements",
                             "outcome_ids": ids, "delivery_requirements": normalized_requirements,
                             "superseded": {"delivery_requirements": previous}})
    return state


def _load(root: Path, report: Path) -> tuple[bytes, dict[str, Any]]:
    path = _report_path(root, report, exists=True)
    data = path.read_bytes()
    text = data.decode()
    versions = re.findall(
        r'<meta name="audit-codebase-report-version" content="([0-9]+)">', text
    )
    if versions != [str(REPORT_VERSION)]:
        raise ReportError(f"report version {REPORT_VERSION} required; create a new current-format map")
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
    elif objective in {"reconcile-map", "record-outcome", "record-preview"}:
        data, state = _load(root, path)
        prior = _digest(data)
        if raw.get("version") != MANIFEST_VERSION or raw.get("expected_report_sha256") != prior:
            raise ReportError("manifest version or expected_report_sha256 does not match current report")
        state = json.loads(json.dumps(state))
        if objective == "reconcile-map":
            state = _reconcile(raw, state, root)
        elif objective == "record-outcome":
            state = _record_outcomes(raw, state, root)
        else:
            _strict(raw, {"version", "expected_report_sha256", "preview"}, set(), "preview manifest")
            record = _preview_record(raw["preview"])
            if record["state"] == "verified" and record["report_sha256"] != prior:
                raise ReportError("visual verification does not name the current report revision")
            key = (record["environment"], record["capability"])
            previous = next((item for item in state["preview"] if (item["environment"], item["capability"]) == key), None)
            if previous and {k: v for k, v in previous.items() if k != "recorded_at"} == {k: v for k, v in record.items() if k != "recorded_at"}:
                return {"path": path, "prior": prior, "rendered": data, "report_sha256": prior, "state_sha256": _digest(_canonical(state)), "unchanged": True}
            state["preview"] = [item for item in state["preview"] if (item["environment"], item["capability"]) != key] + [record]
            state["history"].append({"operation": "preview", "selection": record["environment"], "superseded": {"preview": previous}})
        _refresh_observation(state, root)
        _validate_state(state)
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
            packet["source_identity"] = _verify_source_packet(
                root, packet["source_identity"], selected["owned_paths"]
            )
            historical_candidates, historical_findings = _catalog(state)
            if any(item["id"] in historical_candidates and historical_candidates[item["id"]]["origin"] != selected["id"] for item in packet["candidates"]):
                raise ReportError("audit reuses a candidate id from another owner")
            if any(item["id"] in historical_findings and historical_findings[item["id"]]["origin"] != selected["id"] for item in packet["findings"] + packet["systemic_findings"]):
                raise ReportError("audit reuses a finding id from another owner")
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
            selected["audit_scope"] = list(selected["owned_paths"])
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
            affected_ids = _current_scope(state, list(set(selected["affected_scope"]) | set(packet["affected_scope"])))
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
            packet["source_identity"] = _verify_source_packet(root, packet["source_identity"], affected_paths)
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
    result = {
        "path": path,
        "prior": prior,
        "rendered": rendered,
        "report_sha256": _digest(rendered),
        "state_sha256": _digest(_canonical(state)),
    }
    return result


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
    if p.get("unchanged"):
        result["unchanged"] = True
    if validate_only or p.get("unchanged"):
        return result
    _publish_prepared(p, repo_root)
    result["published"] = True
    return result


def _publish_prepared(p: dict[str, Any], repo_root: Path) -> None:
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


def refresh_report(*, repo_root: Path, report: Path) -> dict[str, Any]:
    root = repo_root.resolve()
    data, state = _load(root, report)
    _refresh_observation(state, root)
    _validate_state(state)
    rendered = _render(state)
    path = _report_path(root, report, exists=True)
    _publish_prepared({"path": path, "prior": _digest(data), "rendered": rendered, "report_sha256": _digest(rendered)}, root)
    return {"response_version": RESPONSE_VERSION, "refreshed": True, "report": str(path), "report_sha256": _digest(rendered), "state_sha256": _digest(_canonical(state)), "freshness": state["freshness"], "map_drift": state["map_drift"]}


def _outstanding(work: dict[str, Any]) -> bool:
    return work["status"] in {"open", "implemented", "verification changed"} or work["commit_pending"] or bool(work["deployment_pending"])


def _summary(state: dict[str, Any]) -> dict[str, Any]:
    candidates, findings = _catalog(state)
    works = [_work_status(state, {"kind": "candidate", "id": cid}) for cid in candidates]
    finding_works = [_work_status(state, {"kind": "finding", "id": fid}) for fid in findings]
    deliveries = [_work_status(state, row["target"]) for row in state["delivery_requirements"]]
    return {
        "mapped_subsystems": len(state["subsystems"]), "retired_subsystems": len(state["retired_subsystems"]),
        "previously_audited": sum("audit" in sub for sub in state["subsystems"]),
        "current_audits": sum("audit" in sub and state["freshness"][sub["id"]] == "fresh" for sub in state["subsystems"]),
        "changed_subsystems": sum(value == "changed" for value in state["freshness"].values()),
        "candidate_ids": len(candidates), "historical_candidates": sum(item["historical"] for item in candidates.values()),
        "outstanding_candidates": sum(_outstanding(work) for work in works),
        "verified_candidates": sum(work["status"] == "verified" for work in works),
        "deferred_candidates": sum(work["status"] == "deferred" for work in works),
        "outstanding_findings": sum(_outstanding(work) for work in finding_works),
        "verified_findings": sum(work["status"] == "verified" for work in finding_works),
        "delivery_pending": sum(work["commit_pending"] or bool(work["deployment_pending"]) for work in deliveries),
        "coverage": _coverage_counts(state),
    }


def _reconciliation_revisions(state: dict[str, Any]) -> dict[int, tuple[dict[str, Any], dict[str, Any]]]:
    def definitions(values: object) -> dict[str, Any]:
        if not isinstance(values, list):
            raise ReportError("retained map subsystems must be a list")
        records = [_subsystem({key: value for key, value in _obj(record, "retained subsystem").items()
                               if key not in {"state", "audit", "map_source", "audit_scope"}}, "retained subsystem") for record in values]
        result = {record["id"]: record for record in records}
        if len(result) != len(records):
            raise ReportError("retained map has duplicate subsystem ids")
        return result

    after = definitions(state["subsystems"])
    revisions = {}
    # Every reconciliation retains the complete map immediately before its change.
    # The next retained map (or current map for the last change) is its result.
    for index in range(len(state["history"]) - 1, -1, -1):
        stored = _obj(state["history"][index], "history record")
        _text(stored.get("operation"), "history operation")
        _text(stored.get("selection"), "history selection")
        if stored["operation"] != "reconcile":
            continue
        prior = _obj(stored.get("superseded"), "retained reconciliation")
        before = definitions(_obj(prior.get("map"), "retained map").get("subsystems"))
        if not isinstance(stored.get("ownership_changes"), list):
            raise ReportError("retained ownership changes must be a list")
        for change in stored["ownership_changes"]:
            change = _obj(change, "retained ownership change")
            _strict(change, {"path", "owner", "reason"}, set(), "retained ownership change")
            _rel(change["path"], "retained ownership path")
            _text(change["reason"], "retained ownership reason")
            if change["owner"] is not None:
                _id(change["owner"], "retained owner")
        for sid, retirement in _obj(stored.get("retirements"), "retained retirements").items():
            _id(sid, "retained retirement id")
            retirement = _obj(retirement, "retained retirement")
            _strict(retirement, {"replacement_ids", "reason"}, set(), "retained retirement")
            _texts(retirement["replacement_ids"], "retained replacements")
            _text(retirement["reason"], "retained retirement reason")
        revisions[index] = (before, after)
        after = before
    return revisions


def _inspection_history(state: dict[str, Any], rows: list[dict[str, Any]], *, subsystem: str | None,
                        candidate: str | None, finding: str | None, paths: Sequence[str],
                        outstanding: bool, detail: bool, matched_subsystems: Sequence[str] = ()) -> list[dict[str, Any]]:
    candidates, findings = _catalog(state)
    targets = {(row["target"]["kind"], row["target"]["id"]) for row in rows}
    if candidate:
        targets.add(("candidate", candidate))
    if finding:
        targets.add(("finding", finding))
    for kind, identifier in list(targets):
        if kind == "candidate":
            targets.update(("finding", fid) for fid in candidates[identifier]["record"]["finding_ids"])
    owners = set(matched_subsystems) | ({subsystem} if subsystem else set())
    bound_paths = set()
    for kind, identifier in targets:
        item = (candidates if kind == "candidate" else findings)[identifier]
        owners.add(item["origin"])
        owners.update(item["record"]["affected_scope"])
        owners.update(item["record"].get("analysis", {}).get("affected_scope", []))
        bound_paths.update(item["audit_source"]["paths"])
        bound_paths.update(_required_paths(state, item["record"]))
    # Keep every retired boundary in a selected target's replacement chain relevant.
    retired = {sub["id"]: sub["retirement"]["replacement_ids"] for sub in state["retired_subsystems"]}
    pending = list(owners)
    while pending:
        for replacement in retired.get(pending.pop(), []):
            if replacement not in owners:
                owners.add(replacement)
                pending.append(replacement)
    identifiers = {identifier for _, identifier in targets}
    identifiers.update(matched_subsystems)
    if subsystem:
        identifiers.add(subsystem)
    filtered = bool(subsystem or candidate or finding or paths or outstanding)

    def path_matches(path: str) -> bool:
        return path in bound_paths or any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in paths)

    def owner_matches(record: dict[str, Any]) -> bool:
        return record["id"] in owners or any(path_matches(path) for path in record.get("owned_paths", []))

    map_revisions = _reconciliation_revisions(state)
    entries = []
    for index, stored in enumerate(state["history"]):
        prior = stored.get("superseded", {})
        old_findings = prior.get("audit", {}).get("findings", []) + prior.get("systemic_findings", [])
        revisions = prior.get("audit", {}).get("candidates", []) + old_findings
        related = {item["id"] for item in revisions}
        for event in state["outcomes"]:
            if event["id"] in stored.get("outcome_ids", []):
                related.add(event["target"]["id"])
                related.update(event.get("finding_ids", []))
        requirements = stored.get("delivery_requirements", []) + prior.get("delivery_requirements", [])
        related.update(row["target"]["id"] for row in requirements)
        affected_owners = set()
        if index in map_revisions:
            before, after = map_revisions[index]
            affected_owners = {sid for sid in before.keys() | after.keys() if before.get(sid) != after.get(sid)}
        reconciliation = stored["operation"] == "reconcile" and (
            bool(affected_owners & owners) or any(path_matches(change["path"]) for change in stored["ownership_changes"]))
        if filtered and stored["selection"] not in identifiers and not related & identifiers and not reconciliation:
            continue
        entry = dict(stored)
        if filtered and detail:
            entry.pop("superseded", None)
            revision = next((item for item in prior.get("audit", {}).get("candidates", []) if item["id"] == candidate), None)
            if revision is not None:
                entry["candidate_revision"] = revision
            if "analysis" in prior:
                entry["prior_analysis"] = prior["analysis"]
            relevant_findings = [item for item in old_findings if ("finding", item["id"]) in targets]
            if relevant_findings:
                entry["finding_revisions"] = relevant_findings
                entry["audit_source_identity"] = prior["audit"]["source_identity"]
            if requirements:
                entry["delivery_requirements"] = [row for row in stored.get("delivery_requirements", []) if (row["target"]["kind"], row["target"]["id"]) in targets]
                entry["prior_delivery_requirements"] = [row for row in prior.get("delivery_requirements", []) if (row["target"]["kind"], row["target"]["id"]) in targets]
            if stored["operation"] == "reconcile":
                entry["affected_subsystems"] = sorted(affected_owners & owners)
                entry["subsystems"] = [record for sid, record in after.items() if sid in affected_owners and owner_matches(record)]
                entry["prior_subsystems"] = [record for record in before.values() if owner_matches(record)]
                entry["ownership_changes"] = [change for change in stored["ownership_changes"] if change["owner"] in owners or path_matches(change["path"])]
                entry["retirements"] = {sid: record for sid, record in stored["retirements"].items() if sid in owners}
        elif not detail:
            entry.pop("superseded", None)
        entries.append(entry)
    return entries


def _subsystem_inspection(state: dict[str, Any], sub: dict[str, Any], root: Path, paths: Sequence[str], limit: int,
                          revisions: dict[int, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any] | None:
    packet = sub.get("audit", {}).get("source_identity") or sub["map_source"]
    bound = set(packet["paths"]) | set(sub["owned_paths"])
    matching = sorted(path for path in bound if not paths or any(path == prefix or path.startswith(prefix.rstrip("/") + "/") for prefix in paths))
    if paths and not matching:
        return None
    historical = sub["id"] not in state["source_changes"]
    observed = state["source_changes"].get(sub["id"])
    if observed is None:
        since = max((index for index, item in enumerate(state["history"]) if item["operation"] == "audit" and item["selection"] == sub["id"]), default=-1)
        owners = {sub["id"]} | _current_scope(state, [sub["id"]])
        observed = _structure_observation(_packet_observation(root, packet), sorted(owners), since, revisions)
    changed = observed["changed_paths"]
    return {"subsystem_id": sub["id"], "name": sub["name"], "state": sub["state"], "historical": historical,
            "source_sha256": packet["sha256"], "matching_paths": matching[:limit], "matching_paths_total": len(matching), "matching_paths_has_more": len(matching) > limit,
            "source_changes": {**observed, "changed_paths": changed[:limit], "changed_paths_total": len(changed), "changed_paths_has_more": len(changed) > limit}}


def inspect_report(*, repo_root: Path, report: Path, full: bool = False,
                   subsystem: str | None = None, candidate: str | None = None, finding: str | None = None,
                   changed_paths: Sequence[str] = (), outstanding: bool = False, history: bool = False,
                   limit: int = 20, offset: int = 0, detail: bool = True) -> dict[str, Any]:
    data, state = _load(repo_root.resolve(), report)
    result = {
        "response_version": RESPONSE_VERSION,
        "report_version": REPORT_VERSION,
        "state_version": STATE_VERSION,
        "report_sha256": _digest(data),
        "state_sha256": _digest(_canonical(state)),
    }
    selected = bool(subsystem or candidate or finding or changed_paths or outstanding or history)
    if full:
        if selected:
            raise ReportError("--full cannot be combined with selection filters")
        result["state"] = state
        return result
    if limit < 1 or limit > 100 or offset < 0:
        raise ReportError("inspection limit must be 1..100 and offset nonnegative")
    root = repo_root.resolve()
    _refresh_observation(state, root)
    candidates, findings = _catalog(state)
    revisions = _reconciliation_revisions(state)
    subs = {sub["id"]: sub for sub in state["subsystems"] + state["retired_subsystems"]}
    if subsystem is not None and subsystem not in subs:
        raise ReportError(f"unknown subsystem {subsystem}")
    if candidate is not None and candidate not in candidates:
        raise ReportError(f"unknown candidate {candidate}")
    if finding is not None and finding not in findings:
        raise ReportError(f"unknown finding {finding}")
    paths = [_rel(path, "changed path") for path in changed_paths]
    rows = []
    for kind, catalog in (("candidate", candidates), ("finding", findings)):
        for identifier, item in sorted(catalog.items()):
            if candidate is not None and (kind != "candidate" or identifier != candidate):
                continue
            if finding is not None and (kind != "finding" or identifier != finding):
                continue
            scope = set(item["record"]["affected_scope"]) | set(item["record"].get("analysis", {}).get("affected_scope", []))
            if subsystem is not None and item["origin"] != subsystem and subsystem not in scope | _current_scope(state, sorted(scope)):
                continue
            if item["historical"] and not (history or candidate or finding or subsystem or outstanding):
                continue
            bound = set(item.get("audit_source", {}).get("paths", []))
            bound |= set(item["record"].get("analysis", {}).get("source_identity", {}).get("paths", []))
            bound |= set(_required_paths(state, item["record"]))
            if item["origin"] in subs:
                bound |= set(subs[item["origin"]]["owned_paths"])
            target = {"kind": kind, "id": identifier}
            work = _work_status(state, target)
            applicable_outcomes = [event for event in reversed(state["outcomes"]) if event["id"] in work["outcome_ids"]]
            bound |= {path for event in applicable_outcomes for path in event.get("source_identity", {}).get("paths", [])}
            if paths and not any(bound_path == path or bound_path.startswith(path.rstrip("/") + "/") for path in paths for bound_path in bound):
                continue
            if outstanding and not _outstanding(work):
                continue
            row = {"target": target, "title": item["record"]["title"], "subsystem_id": item["origin"], "historical": item["historical"], "work": work}
            observed_outcomes = [event for event in applicable_outcomes if event["id"] in state["outcome_source_changes"] and (not paths or any(bound_path == path or bound_path.startswith(path.rstrip("/") + "/") for path in paths for bound_path in set(event["source_identity"]["paths"]) | set(state["outcome_source_changes"][event["id"]]["changed_paths"])))]
            row["outcome_source_changes"] = {event["id"]: state["outcome_source_changes"][event["id"]] for event in observed_outcomes[:limit]}
            row.update(outcome_observations_total=len(observed_outcomes), outcome_observations_has_more=len(observed_outcomes) > limit)
            if kind == "candidate":
                row.update(analysis_state=item["record"]["state"], source_changes=state["candidate_source_changes"].get(identifier))
                if row["source_changes"] is None:
                    row["source_changes"] = _candidate_observations(state, item, root, revisions)
            else:
                packet = item["audit_source"]
                row["source_changes"] = _finding_observations(state, item, root, revisions)
                if detail and (finding or subsystem):
                    row["audit_source_identity"] = packet
            if detail and (candidate or finding or subsystem):
                row["record"] = item["record"]
                row.update(outcomes=applicable_outcomes[:limit], outcomes_total=len(applicable_outcomes), outcomes_has_more=len(applicable_outcomes) > limit)
                if kind == "candidate":
                    row["findings"] = [findings[fid]["record"] for fid in item["record"]["finding_ids"]]
            rows.append(row)
    subsystem_rows = []
    if paths or subsystem is not None:
        selected_owners = None
        if candidate or finding:
            item = (candidates if candidate else findings)[candidate or finding]
            scope = set(item["record"]["affected_scope"]) | set(item["record"].get("analysis", {}).get("affected_scope", [])) | {item["origin"]}
            selected_owners = scope | _current_scope(state, sorted(scope))
        for sid, sub in sorted(subs.items()):
            if subsystem is not None and sid != subsystem:
                continue
            if sid not in state["source_changes"] and not (history or subsystem is not None):
                continue
            if selected_owners is not None and sid not in selected_owners:
                continue
            observed_subsystem = _subsystem_inspection(state, sub, root, paths, limit, revisions)
            if observed_subsystem is not None:
                subsystem_rows.append(observed_subsystem)
    result.update(summary=_summary(state), observed_at=state["observed_at"], rows=rows[offset:offset + limit], total=len(rows), offset=offset, limit=limit, has_more=offset + limit < len(rows),
                  subsystems=subsystem_rows[offset:offset + limit], subsystems_total=len(subsystem_rows), subsystems_has_more=offset + limit < len(subsystem_rows))
    result["map_drift"] = {key: value[:limit] if isinstance(value, list) else value for key, value in state["map_drift"].items()}
    result["map_drift"]["totals"] = {key: len(value) for key, value in state["map_drift"].items() if isinstance(value, list)}
    result["preview"] = state["preview"]
    if subsystem and detail:
        result["subsystem"] = subs[subsystem]
        selected_subsystem = _subsystem_inspection(state, subs[subsystem], root, [], limit, revisions)
        result["source_changes"] = selected_subsystem["source_changes"]
    if history:
        entries = _inspection_history(state, rows, subsystem=subsystem, candidate=candidate, finding=finding,
                                      paths=paths, outstanding=outstanding, detail=detail, matched_subsystems=[sub["subsystem_id"] for sub in subsystem_rows])
        result.update(history=entries[offset:offset + limit], history_total=len(entries), history_has_more=offset + limit < len(entries))
    return result


def status_report(*, repo_root: Path, report: Path, **filters: Any) -> dict[str, Any]:
    return inspect_report(repo_root=repo_root, report=report, full=False, detail=False, **filters)


def check_report(*, repo_root: Path, report: Path) -> dict[str, Any]:
    data, state = _load(repo_root.resolve(), report)
    ids, references, commands = [], [], []

    class Surface(HTMLParser):
        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            attributes = dict(attrs)
            if attributes.get("id"):
                ids.append(attributes["id"])
            if attributes.get("href", "").startswith("#"):
                references.append(attributes["href"][1:])
            for value in attributes.values():
                if value:
                    references.extend(re.findall(r"url\(#([^)]*)\)", value))
            if attributes.get("data-copy"):
                commands.append(attributes["data-copy"])

    Surface().feed(data.decode("utf-8"))
    if len(ids) != len(set(ids)) or set(references) - set(ids):
        raise ReportError("report has duplicate ids or unresolved anchors", stage="check-report")
    candidates, findings = _catalog(state)
    navigation = {"overview", "architecture", "subsystems", "audits", "findings", "candidates", "outcomes", "evidence", "history"}
    navigation |= {f"system-{system['id']}" for system in state["systems"]}
    navigation |= {f"subsystem-{sub['id']}" for sub in state["subsystems"]}
    required_ids = navigation | {"search", "state-filter", "audit-codebase-state", "arrow"}
    required_ids |= {f"audit-{sub['id']}" for sub in state["subsystems"] if "audit" in sub}
    required_ids |= {f"candidate-{cid}" for cid in candidates} | {f"finding-{fid}" for fid in findings}
    required_ids |= {f"work-{item['target']['kind']}-{item['target']['id']}" for item in state["outcomes"] + state["delivery_requirements"]}
    required_ids |= {f"outcome-{event['id']}" for event in state["outcomes"]}
    navigation |= {f"candidate-{cid}" for cid, change in state["candidate_source_changes"].items() if change["scope"]["freshness"] == "changed"}
    navigation |= {f"outcome-{eid}" for eid, change in state["outcome_source_changes"].items() if change["freshness"] == "changed"}
    revisions = _reconciliation_revisions(state)
    navigation |= {f"finding-{fid}" for fid, item in findings.items() if not item["historical"] and
                   _finding_scope_observation(state, item, state["source_changes"][item["origin"]], revisions)["freshness"] == "changed"}
    for cid, item in candidates.items():
        comparison = item["record"].get("analysis", {}).get("comparison") or item["record"].get("comparison")
        if comparison and not item["historical"]:
            for side in ("before", "after"):
                marker = f"{cid}-{side}-arrow"
                required_ids.add(marker)
                if comparison[side]["edges"]:
                    navigation.add(marker)
    if required_ids - set(ids) or navigation - set(references):
        raise ReportError("report is missing required anchors or navigation references", stage="check-report")
    required = {f"$audit-codebase audit subsystem {sub['id']} in atlas run {state['run_id']}" for sub in state["subsystems"]}
    required |= {f"$audit-codebase inspect finding {fid} in atlas run {state['run_id']}" for fid in findings}
    for cid, item in candidates.items():
        if item["historical"]:
            required.add(f"$audit-codebase inspect candidate {cid} in atlas run {state['run_id']}")
        else:
            command, next_action = _candidate_commands(item["record"], state["run_id"], state["candidate_freshness"][cid],
                                                      _work_status(state, {"kind": "candidate", "id": cid}))
            required.add(command)
            if next_action:
                required.add(next_action)
    if set(commands) - required:
        raise ReportError("report has an invalid selection command", stage="check-report")
    if required - set(commands):
        raise ReportError("report is missing a required selection command", stage="check-report")
    _refresh_observation(state, repo_root.resolve())
    revisions = _reconciliation_revisions(state)
    candidate_changes = {cid: _candidate_observations(state, item, repo_root.resolve(), revisions) for cid, item in candidates.items()}
    candidate_freshness = {cid: "changed" if change["audit"]["freshness"] == "changed" else change["scope"]["freshness"] for cid, change in candidate_changes.items()}
    finding_changes = {fid: _finding_observations(state, item, repo_root.resolve(), revisions) for fid, item in findings.items()}
    drift = state["map_drift"]
    return {"response_version": RESPONSE_VERSION, "valid": True, "report_sha256": _digest(data),
            "checks": {"canonical_state": True, "relationships": True, "anchors": True, "ids": True, "selection_commands": True},
            "ownership_current": not drift["needs_reconcile"], "map_drift": drift,
            "freshness": state["freshness"], "candidate_freshness": candidate_freshness,
            "outcome_freshness": state["outcome_freshness"], "finding_freshness": {fid: change["scope"]["freshness"] for fid, change in finding_changes.items()},
            "source_changes": {sid: change for sid, change in state["source_changes"].items() if change["freshness"] == "changed"},
            "candidate_source_changes": {cid: change for cid, change in candidate_changes.items() if candidate_freshness[cid] == "changed"},
            "outcome_source_changes": {eid: change for eid, change in state["outcome_source_changes"].items() if change["freshness"] == "changed"},
            "finding_source_changes": {fid: change for fid, change in finding_changes.items() if change["scope"]["freshness"] == "changed"},
            "visual_verification": {"performed_by_check_report": False, "records": state["preview"]}}


def _parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("inventory")
    p.add_argument("--repo-root", type=Path, required=True)
    p = commands.add_parser("source-identity")
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--path", action="append", dest="paths", required=True)
    for name in ("inspect", "status"):
        p = commands.add_parser(name)
        p.add_argument("--repo-root", type=Path, required=True)
        p.add_argument("--report", type=Path, required=True)
        p.add_argument("--subsystem")
        p.add_argument("--candidate")
        p.add_argument("--finding")
        p.add_argument("--changed-path", action="append", default=[], dest="changed_paths")
        p.add_argument("--outstanding", action="store_true")
        p.add_argument("--history", action="store_true")
        p.add_argument("--limit", type=int, default=20)
        p.add_argument("--offset", type=int, default=0)
        if name == "inspect":
            p.add_argument("--full", action="store_true")
    p = commands.add_parser("check-report")
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p = commands.add_parser("refresh")
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    for name in ("render-report", "audit-subsystem", "analyze-candidate", "reconcile-map", "record-outcome", "record-preview"):
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
        elif a.command in {"inspect", "status"}:
            result = inspect_report(repo_root=a.repo_root, report=a.report, full=getattr(a, "full", False), detail=a.command == "inspect",
                                    subsystem=a.subsystem, candidate=a.candidate, finding=a.finding, changed_paths=a.changed_paths,
                                    outstanding=a.outstanding, history=a.history, limit=a.limit, offset=a.offset)
        elif a.command == "check-report":
            result = check_report(repo_root=a.repo_root, report=a.report)
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
