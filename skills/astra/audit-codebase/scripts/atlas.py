"""Offline audit atlas: prepared, source-bound record updates; stdlib only."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from html import escape
from pathlib import Path, PurePosixPath


class AtlasError(ValueError):
    pass


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def relative(value):
    if not isinstance(value, str) or not value:
        raise AtlasError("path must be nonempty")
    value = value.replace("\\", "/").rstrip("/")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or ":" in value or value in {"", "."}:
        raise AtlasError("paths must be repository-relative without traversal")
    return str(p)


def inside(root, value):
    path = root / relative(value)
    if not path.resolve().is_relative_to(root):
        raise AtlasError(f"path escapes repository: {value}")
    return path


def git_paths(root, *args):
    result = subprocess.run(["git", "ls-files", "-z", *args], cwd=root,
                            capture_output=True, check=True)
    return sorted(set(x for x in result.stdout.decode("utf-8").split("\0") if x))


def inventory(root):
    return {"tracked": git_paths(root),
            "untracked": git_paths(root, "--others", "--exclude-standard")}


def expand(root, selectors, *, allow_missing=False, tracked=None):
    tracked = git_paths(root) if tracked is None else tracked
    paths = set()
    for raw in selectors:
        selector = relative(raw)
        # Exact files and directory prefixes only: no ambiguous glob ownership.
        matches = [p for p in tracked if p == selector or p.startswith(selector + "/")]
        if not matches and inside(root, selector).is_file():
            matches = [selector]  # Explicit untracked evidence is allowed.
        if not matches and not allow_missing:
            raise AtlasError(f"selector matches no files: {selector}")
        paths.update(matches)
    return sorted(paths)


def snapshot(root, selectors, *, allow_missing=False, tracked=None, cache=None):
    result = {}
    for name in expand(root, selectors, allow_missing=allow_missing, tracked=tracked):
        if cache is not None and name in cache:
            result[name] = cache[name]
            continue
        path = inside(root, name)
        if not path.exists():
            result[name] = "missing"
        elif not path.is_file():
            raise AtlasError(f"not a regular source file: {name}")
        else:
            with path.open("rb") as stream:
                result[name] = hashlib.file_digest(stream, "sha256").hexdigest()
        if cache is not None:
            cache[name] = result[name]
    return result


def freshness(root, record, *, tracked=None, cache=None):
    try:
        current = snapshot(root, record["selectors"], allow_missing=True, tracked=tracked, cache=cache)
    except AtlasError as exc:
        return {"state": "changed", "reason": str(exc)}
    previous = record["source"]
    changed = sorted(p for p in current.keys() | previous.keys()
                     if current.get(p) != previous.get(p))
    return {"state": "changed" if changed else "unchanged", "paths": changed}


def report_path(root, report):
    report = report.absolute()
    base = (root / ".tmp" / "audit-codebase").resolve()
    if not report.resolve().is_relative_to(base) or report.suffix != ".html":
        raise AtlasError("report must be an HTML file under repository .tmp/audit-codebase")
    return report


def render(state):
    # HTML order must survive loading the canonical embedded JSON.
    state = json.loads(encoded(state))
    def text(value):
        return escape(str(value), quote=True)

    def fields(record):
        parts = []
        for key, value in record["content"].items():
            if key == "lens_coverage":
                value_html = "<ul>" + "".join(
                    f'<li><strong>{text(lens)}</strong> — {text(row["status"])}: {text(row["details"])}</li>'
                    for lens, row in value.items()) + "</ul>"
            elif key == "dependencies":
                value_html = "".join(f'<li><a href="#{text(d["id"])}">{text(d["id"])}</a>: '
                                     f'{text(d["evidence"])}</li>' for d in value)
                value_html = f"<ul>{value_html}</ul>"
            else:
                value_html = text(value) if not isinstance(value, list) else "<ul>" + "".join(
                    f"<li>{text(x)}</li>" for x in value) + "</ul>"
            parts.append(f"<dt>{text(key.replace('_', ' '))}</dt><dd>{value_html}</dd>")
        return "<dl>" + "".join(parts) + "</dl>"

    records = state["records"]
    systems = sorted({r["content"]["system"] for r in records.values() if r["kind"] == "subsystem"})
    sections = []
    for system in systems:
        cards = []
        for ident, record in records.items():
            if record["kind"] != "subsystem" or record["content"]["system"] != system:
                continue
            children = sorted(((i, r) for i, r in records.items() if r.get("subsystem") == ident),
                              key=lambda pair: ({"high": 0, "medium": 1, "low": 2}.get(
                                  pair[1]["content"].get("priority"), 3), pair[0]))
            assessment = [r["content"]["coverage"] + (
                " with evidence gaps" if any(row["status"] == "gap" for row in
                    r["content"].get("lens_coverage", {}).values()) else "")
                for _, r in children if r["kind"] == "assessment"]
            badge = ", ".join(assessment) if assessment else "mapped; not audited"
            cards.append(f'<article id="{text(ident)}"><h3>{text(record["content"]["name"])}</h3>'
                         f'<p>{text(ident)} · {text(badge)} · source '
                         f'{text(state["freshness"].get(ident, {}).get("state", "unknown"))}</p>'
                         f'<details><summary>Ownership and dependencies</summary>{fields(record)}</details>'
                         + "".join(f'<details id="{text(i)}"><summary>{text(i)} — '
                                   f'{text(r["content"].get("title", "Coverage"))} '
                                   f'{text(r["content"].get("priority", ""))} · source '
                                   f'{text(state["freshness"].get(i, {}).get("state", "unknown"))}</summary>'
                                   f'{fields(r)}</details>' for i, r in children) + "</article>")
        sections.append(f"<section><h2>{text(system)}</h2>{''.join(cards)}</section>")
    nav = " · ".join(f'<a href="#{text(i)}">{text(r["content"]["name"])}</a>'
                     for i, r in records.items() if r["kind"] == "subsystem")
    payload = encoded(state).decode().replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    coverage = state["inventory"]
    return (f'<!doctype html><html lang="en"><meta charset="utf-8"><title>{text(state["title"])}</title>'
            '<style>body{font:16px/1.55 system-ui;background:#101827;color:#e5edf7;max-width:1100px;margin:32px auto;padding:0 20px}'
            'a{color:#8dd8ff}article{border:1px solid #526079;border-radius:10px;padding:18px;margin:16px 0}'
            'details{margin:12px 0}summary{cursor:pointer}dt{font-weight:bold;color:#a9bfdc}dd{margin:0 0 12px;white-space:pre-wrap;overflow-wrap:anywhere}</style>'
            f'<h1>{text(state["title"])}</h1><p>Snapshot: {text(state["observed_at"])}. '
            'Source unchanged does not mean the judgment is correct. Refresh to check current files.</p>'
            f'<nav>{nav}</nav><p>{len(coverage["owned"])} tracked paths mapped; '
            f'{len(coverage["unmapped"])} unmapped; {len(coverage["untracked"])} untracked.</p>'
            f'<details><summary>Unmapped paths and untracked evidence limits</summary><pre>{text(json.dumps(coverage, indent=2))}</pre></details>'
            + "".join(sections) + f'<details><summary>Update history ({len(state["history"])})</summary>'
            f'<pre>{text(json.dumps(state["history"], indent=2))}</pre></details>'
            f'<script type="application/json" id="astra-atlas" data-sha256="{digest(encoded(state))}">{payload}</script></html>').encode()


def load(root, report):
    report = report_path(root, report)
    raw = report.read_bytes()
    matches = re.findall(rb'<script type="application/json" id="astra-atlas" data-sha256="([a-f0-9]{64})">(.*?)</script>', raw, re.S)
    if len(matches) != 1:
        raise AtlasError("not an Astra atlas; legacy reports remain read-only")
    sha, payload = matches[0]
    state = json.loads(payload)
    if state.get("version") != 1 or sha.decode() != digest(encoded(state)) or render(state) != raw:
        raise AtlasError("invalid or hand-edited atlas")
    if state["repo"] != str(root):
        raise AtlasError("atlas belongs to a different repository")
    return state, digest(raw)


def observations(root, state):
    inv = inventory(root)
    owners = {}
    for ident, record in state["records"].items():
        if record["kind"] != "subsystem":
            continue
        try:
            paths = expand(root, record["selectors"], tracked=inv["tracked"])
        except AtlasError:
            paths = list(record["source"])
        for path in paths:
            if path in owners:
                raise AtlasError(f"overlapping ownership for {path}: {owners[path]}, {ident}")
            owners[path] = ident
    state["inventory"] = {"owned": sorted(set(inv["tracked"]) & owners.keys()),
                          "unmapped": sorted(set(inv["tracked"]) - owners.keys()),
                          "untracked": inv["untracked"]}
    cache = {}  # One observation per file per refresh; never reused across commands.
    state["freshness"] = {i: freshness(root, r, tracked=inv["tracked"], cache=cache)
                          for i, r in state["records"].items()}
    state["observed_at"] = now()


def publish(root, report, state, expected, *, evidence=None):
    report = report_path(root, report)
    report.parent.mkdir(parents=True, exist_ok=True)
    lock = report.with_suffix(".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise AtlasError("another writer is active; inspect before retrying") from exc
    os.close(fd)
    temporary = None
    try:
        actual = digest(report.read_bytes()) if report.exists() else "absent"
        if actual != expected:
            raise AtlasError("report changed; prepare a new update")
        observations(root, state)
        if evidence and snapshot(root, evidence["selectors"], allow_missing=True) != evidence["source"]:
            raise AtlasError("source changed during publication; re-examine evidence")
        data = render(state)
        # Exercise the serialization boundary before replacing a valid report.
        if render(json.loads(encoded(state))) != data:
            raise AtlasError("candidate serialization is not stable")
        fd, temporary = tempfile.mkstemp(dir=report.parent, prefix="atlas-", suffix=".tmp")
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, report)
        if report.read_bytes() != data:
            raise AtlasError("publication read-back failed")
        load(root, report)
    finally:
        if temporary and Path(temporary).exists():
            Path(temporary).unlink()
        lock.unlink()


TEMPLATES = {
    "subsystem": {"name": "", "system": "", "purpose": "", "ownership": "", "dependencies": []},
    "finding": {"title": "", "kind": "opportunity", "scenario": "", "expectation": "", "evidence": "", "consequence": "",
                "cause": "", "counterevidence": "", "direction": "", "preserve_and_verify": "",
                "priority": "", "priority_rationale": "", "confidence_and_limits": "", "status": "open"},
    "assessment": {"coverage": "focused", "examined": "", "dimensions": [], "limits": "", "recommendation": ""},
}

LENSES = ("design", "domain", "reliability", "simplification", "coding practice", "performance")


def validate(content, kind, state):
    optional = {"lens_coverage"} if kind == "assessment" else set()
    if (not isinstance(content, dict) or not set(TEMPLATES[kind]) <= set(content)
            or set(content) - set(TEMPLATES[kind]) - optional):
        raise AtlasError(f"content must have the generated {kind} fields")
    for key, value in content.items():
        if isinstance(TEMPLATES[kind].get(key), str) and not isinstance(value, str):
            raise AtlasError(f"{key} must be text")
    required = {"subsystem": ["name", "system", "purpose", "ownership"],
                "finding": ["title", "scenario", "evidence", "consequence", "confidence_and_limits"],
                "assessment": ["examined", "limits"]}[kind]
    if any(not content[k].strip() for k in required):
        raise AtlasError("fill required judgment fields: " + ", ".join(required))
    if kind == "subsystem":
        if not isinstance(content["dependencies"], list):
            raise AtlasError("dependencies must be a list")
        for item in content["dependencies"]:
            if (not isinstance(item, dict) or set(item) != {"id", "evidence"}
                    or not isinstance(item["evidence"], str) or not item["evidence"].strip()
                    or state["records"].get(item["id"], {}).get("kind") != "subsystem"):
                raise AtlasError("dependency needs existing subsystem id and evidence")
    if kind == "finding":
        if content["kind"] not in {"defect", "opportunity", "retain", "gap"}:
            raise AtlasError("invalid finding kind")
        if content["status"] not in {"open", "resolved", "disproved", "blocked"}:
            raise AtlasError("invalid finding status")
        if content["kind"] == "defect" and not content["expectation"].strip():
            raise AtlasError("defect needs an accepted expectation")
        if content["priority"] not in {"", "high", "medium", "low"}:
            raise AtlasError("priority must be high, medium, low, or empty")
        if content["kind"] in {"defect", "opportunity"} and not all(
                content[k].strip() for k in ["direction", "preserve_and_verify", "priority", "priority_rationale"]):
            raise AtlasError("actionable finding needs direction, preservation proof, and priority rationale")
    if kind == "assessment":
        if content["coverage"] not in {"focused", "comprehensive", "incomplete"}:
            raise AtlasError("invalid coverage")
        if not isinstance(content["dimensions"], list) or not all(
                isinstance(x, str) and x.strip() for x in content["dimensions"]):
            raise AtlasError("dimensions must be text entries")
        ledger = content.get("lens_coverage")
        if content["coverage"] == "comprehensive" and ledger is None:
            raise AtlasError("comprehensive coverage requires a prepared six-lens ledger")
        if ledger is not None:
            if not isinstance(ledger, dict) or set(ledger) != set(LENSES):
                raise AtlasError("lens_coverage must account for all six lenses")
            for lens, row in ledger.items():
                if (not isinstance(row, dict) or set(row) != {"status", "details"}
                        or row["status"] not in {"examined", "excluded", "gap", "pending"}
                        or not isinstance(row["details"], str)):
                    raise AtlasError(f"invalid coverage row: {lens}")
                if row["status"] == "pending":
                    if content["coverage"] == "comprehensive":
                        raise AtlasError(f"comprehensive coverage has pending lens: {lens}")
                elif not row["details"].strip():
                    raise AtlasError(f"{lens} needs examined evidence, exclusion reason, or missing evidence")


def prepare(root, report, kind, ident=None, subsystem=None, paths=(), coverage=None):
    state, revision = load(root, report)
    old = state["records"].get(ident) if ident else None
    if ident and not old:
        raise AtlasError("unknown record")
    if old and old["kind"] != kind:
        raise AtlasError("record kind cannot change")
    if not ident:
        prefix = {"subsystem": "s", "finding": "f", "assessment": "a"}[kind]
        number = 1
        used = set(state["records"]) | {item["record"] for item in state["history"]}
        while f"{prefix}{number}" in used:
            number += 1
        ident = f"{prefix}{number}"
    subsystem = subsystem if subsystem is not None else (old.get("subsystem") if old else None)
    if kind != "subsystem" and state["records"].get(subsystem, {}).get("kind") != "subsystem":
        raise AtlasError("select an existing subsystem")
    selectors = list(paths) or (old["selectors"] if old else [])
    if kind != "subsystem":
        selectors = sorted(set(selectors + state["records"][subsystem]["selectors"]))
    if not selectors:
        raise AtlasError("prepare requires --path for source ownership or evidence")
    selectors = [relative(p) for p in selectors]
    content = copy.deepcopy(old["content"] if old else TEMPLATES[kind])
    if coverage is not None:
        if kind != "assessment" or coverage not in {"focused", "comprehensive", "incomplete"}:
            raise AtlasError("--coverage applies to assessments only")
        content["coverage"] = coverage
        if coverage == "comprehensive":
            content.setdefault("lens_coverage", {lens: {"status": "pending", "details": ""} for lens in LENSES})
        elif coverage == "focused":
            content.pop("lens_coverage", None)
    return {"version": 1, "report_revision": revision, "record_id": ident,
            "kind": kind, "subsystem": subsystem, "selectors": selectors,
            "source": snapshot(root, selectors, allow_missing=bool(old)), "remove": False,
            "content": content}


def apply(root, report, draft):
    state, revision = load(root, report)
    required = {"version", "report_revision", "record_id", "kind", "subsystem", "selectors", "source", "remove", "content"}
    if not isinstance(draft, dict) or set(draft) != required or draft["version"] != 1:
        raise AtlasError("invalid prepared update")
    if draft["report_revision"] != revision:
        raise AtlasError("report changed; prepare a new update")
    if snapshot(root, draft["selectors"], allow_missing=True) != draft["source"]:
        raise AtlasError("source changed; re-examine evidence and prepare again")
    ident, kind = draft["record_id"], draft["kind"]
    if kind not in TEMPLATES or not re.fullmatch(r"[sfa][1-9][0-9]*", ident):
        raise AtlasError("invalid record identity")
    old = state["records"].get(ident)
    if old and old["kind"] != kind:
        raise AtlasError("record kind cannot change")
    if type(draft["remove"]) is not bool:
        raise AtlasError("remove must be boolean")
    if draft["remove"]:
        if not old:
            raise AtlasError("cannot remove missing record")
        if any(r.get("subsystem") == ident or any(d["id"] == ident for d in r["content"].get("dependencies", []))
               for r in state["records"].values()):
            raise AtlasError("remove dependent records or relationships first")
        del state["records"][ident]
    else:
        if kind != "subsystem" and state["records"].get(draft["subsystem"], {}).get("kind") != "subsystem":
            raise AtlasError("unknown subsystem")
        validate(draft["content"], kind, state)
        state["records"][ident] = {k: copy.deepcopy(draft[k]) for k in
                                   ["kind", "subsystem", "selectors", "source", "content"]}
    state["history"].append({"at": now(), "record": ident, "operation": "remove" if draft["remove"] else "update", "previous": old})
    publish(root, report, state, revision, evidence=draft)
    return {"record_id": ident, "report": str(report), "published": True}


def inspect(root, report, ident=None):
    state, revision = load(root, report)
    observations(root, state)
    if ident:
        if ident not in state["records"]:
            raise AtlasError("unknown record")
        ids = [i for i, r in state["records"].items() if i == ident or r.get("subsystem") == ident]
        return {"revision": revision, "records": {i: state["records"][i] for i in ids},
                "freshness": {i: state["freshness"][i] for i in ids}}
    return {"revision": revision, "inventory": {k: len(v) for k, v in state["inventory"].items()},
            "records": [{"id": i, "kind": r["kind"], "subsystem": r["subsystem"],
                         "name": r["content"].get("name", r["content"].get("title", "Coverage")),
                         "freshness": state["freshness"][i]["state"]} for i, r in state["records"].items()]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init")
    p.add_argument("--title", default="Codebase atlas")
    sub.add_parser("inventory")
    p = sub.add_parser("inspect")
    p.add_argument("--id")
    sub.add_parser("refresh")
    p = sub.add_parser("prepare")
    p.add_argument("--kind", choices=TEMPLATES, required=True)
    p.add_argument("--id")
    p.add_argument("--subsystem")
    p.add_argument("--coverage", choices=["focused", "comprehensive", "incomplete"])
    p.add_argument("--path", action="append", default=[])
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("apply")
    p.add_argument("--draft", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        root = args.repo.resolve()
        report = report_path(root, args.report)
        if args.command == "init":
            state = {"version": 1, "repo": str(root), "title": args.title, "records": {}, "history": []}
            publish(root, report, state, "absent")
            result = {"report": str(report), "created": True}
        elif args.command == "inventory":
            result = inventory(root)
        elif args.command == "inspect":
            result = inspect(root, report, args.id)
        elif args.command == "refresh":
            state, revision = load(root, report)
            publish(root, report, state, revision)
            result = inspect(root, report)
        elif args.command == "prepare":
            draft = prepare(root, report, args.kind, args.id, args.subsystem, args.path, args.coverage)
            out = args.out.absolute()
            if not out.resolve().is_relative_to((root / ".tmp" / "audit-codebase").resolve()):
                raise AtlasError("draft must be under repository .tmp/audit-codebase")
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("x", encoding="utf-8") as stream:
                json.dump(draft, stream, indent=2, ensure_ascii=False)
            result = {"draft": str(out), "record_id": draft["record_id"], "edit": "content only; remove=true for explicit deletion"}
        else:
            result = apply(root, report, json.loads(args.draft.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (AtlasError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
