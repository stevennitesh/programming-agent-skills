"""Freeze and check the Fresh Composition Epoch migration control."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Iterable

from scripts import fresh_epoch_contract


PUBLIC_LEDGER = Path(
    ".scratch/fresh-composition-epoch/migration-ledger.json"
)
PRIVATE_LEDGER = Path(
    ".tmp/fresh-composition-epoch/migration-ledger-private.json"
)
CLOSEOUT = Path(".scratch/fresh-composition-epoch/README.md")

PUBLIC_PREFIXES = (
    ".archive/docs/",
    "docs/adr/",
    "docs/agents/",
    "docs/plans/",
    "docs/research/",
    "docs/synthesis/",
    "docs/validation/",
    "skills/.archive/",
    "skills/custom/",
    "skills/experimental/",
    "skills/extra/",
)
PUBLIC_EXACT = frozenset(
    {
        ".gitignore",
        "AGENTS.md",
        "CONTEXT.md",
        "README.md",
        "scripts/campaign_artifacts.py",
        "scripts/install_skills.py",
        "scripts/skill_pack_contract.py",
        "scripts/validate_skills.py",
    }
)
PRIVATE_RESEARCH_ROOT = PurePosixPath("docs/research/sources")
PRIVATE_TMP_ROOT = PurePosixPath(".tmp")


def _git(root: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", *args, "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in completed.stdout.split(b"\0")
        if item
    ]


def _head(root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _is_public_path(relative: str) -> bool:
    return relative in PUBLIC_EXACT or relative.startswith(PUBLIC_PREFIXES)


def _private_logical_root(relative: str) -> str:
    path = PurePosixPath(relative)
    parts = path.parts
    if (
        path.is_relative_to(PurePosixPath(".tmp/repos"))
        and len(parts) >= 3
    ):
        return PurePosixPath(*parts[:3]).as_posix()
    if path.is_relative_to(PRIVATE_TMP_ROOT) and len(parts) >= 2:
        return PurePosixPath(*parts[:2]).as_posix()
    if path.is_relative_to(PRIVATE_RESEARCH_ROOT) and len(parts) >= 4:
        return PurePosixPath(*parts[:4]).as_posix()
    if "__pycache__" in parts:
        index = parts.index("__pycache__")
        return PurePosixPath(*parts[: index + 1]).as_posix()
    return relative


def _is_private_inventory_path(relative: str) -> bool:
    if relative.startswith(f"{PRIVATE_LEDGER.parent.as_posix()}/"):
        return False
    path = PurePosixPath(relative)
    return (
        path.is_relative_to(PRIVATE_TMP_ROOT)
        or path.is_relative_to(PRIVATE_RESEARCH_ROOT)
        or relative.startswith(PUBLIC_PREFIXES)
    )


def _empty_eval_directories(root: Path) -> list[str]:
    eval_root = root / "docs/validation/evals"
    if not eval_root.is_dir():
        return []
    result: list[str] = []
    for directory in sorted(
        (path for path in eval_root.rglob("*") if path.is_dir()),
        key=lambda path: path.relative_to(root).as_posix(),
    ):
        try:
            has_files = any(path.is_file() for path in directory.rglob("*"))
        except OSError:
            continue
        if not has_files and not any(
            parent in result
            for parent in (
                ancestor.relative_to(root).as_posix()
                for ancestor in directory.parents
                if ancestor != root and root in ancestor.parents
            )
        ):
            result.append(directory.relative_to(root).as_posix())
    return result


def discover_inventory(
    root: Path,
) -> tuple[
    list[str],
    list[str],
    list[str],
    dict[str, str],
    dict[str, str],
]:
    """Return public/private paths, reference corpus, and source states."""

    tracked = sorted(set(_git(root, "ls-files")))
    untracked = sorted(set(_git(root, "ls-files", "--others", "--exclude-standard")))
    ignored = sorted(
        set(
            _git(
                root,
                "ls-files",
                "--others",
                "--ignored",
                "--exclude-standard",
            )
        )
    )
    public_paths = sorted(
        {
            path
            for path in (*tracked, *untracked)
            if _is_public_path(path)
            and not PurePosixPath(path).is_relative_to(PRIVATE_RESEARCH_ROOT)
        }
    )
    public_states = {
        path: ("tracked" if path in tracked else "untracked")
        for path in public_paths
    }

    private_paths = {
        _private_logical_root(path)
        for path in ignored
        if _is_private_inventory_path(path)
        if path != ".tmp/.gitkeep"
    }
    private_states = {path: "private-ignored" for path in private_paths}
    for path in _empty_eval_directories(root):
        private_paths.add(path)
        private_states[path] = "local-residue"

    reference_paths = sorted(
        {
            path
            for path in (*tracked, *untracked)
            if not path.startswith((".tmp/", ".scratch/"))
        }
    )
    return (
        public_paths,
        sorted(private_paths),
        reference_paths,
        public_states,
        private_states,
    )


def build_current(
    root: Path,
    *,
    source_head: str | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    (
        public_paths,
        private_paths,
        reference_paths,
        public_states,
        private_states,
    ) = discover_inventory(root)
    return fresh_epoch_contract.build_migration_control(
        root,
        public_paths=public_paths,
        private_paths=private_paths,
        reference_paths=reference_paths,
        head=source_head or _head(root),
        public_states=public_states,
        private_states=private_states,
    )


def _serialize(payload: dict[str, object]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _read_payload(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return payload


def _state_counts(rows: Iterable[object], field: str) -> str:
    counts: Counter[str] = Counter()
    for row in rows:
        if isinstance(row, dict):
            value = row.get(field)
            counts[str(value)] += 1
    return ", ".join(f"`{key}` {counts[key]}" for key in sorted(counts))


def _closeout(public: dict[str, object], private: dict[str, object]) -> str:
    public_rows = public.get("rows")
    private_rows = private.get("rows")
    public_rows = public_rows if isinstance(public_rows, list) else []
    private_rows = private_rows if isinstance(private_rows, list) else []
    fixed_point = public.get("fixed_point")
    fixed_point = fixed_point if isinstance(fixed_point, dict) else {}
    return f"""# Fresh Composition Epoch migration control

Status: frozen inventory; no migration authorized or performed.

This durable `.scratch/` control implements issue #41 and remains temporary
cross-ticket execution state. It is not research, synthesis, validation, or
runtime authority. The complete private inventory remains only in the ignored
sidecar at `{PRIVATE_LEDGER.as_posix()}`; this tracked closeout deliberately
publishes no private source locators.

## Fixed point

- Source Git HEAD: `{fixed_point.get("source_head")}`
- Public inventory fingerprint: `{fixed_point.get("public_inventory_fingerprint")}`
- Private inventory fingerprint: `{fixed_point.get("private_inventory_fingerprint")}`
- Public rows: {len(public_rows)}
- Private/local rows: {len(private_rows)}
- Public migration dispositions: {_state_counts(public_rows, "migration_disposition")}
- Private/local source states: {_state_counts(
        (
            row.get("source")
            for row in private_rows
            if isinstance(row, dict)
        ),
        "state",
    )}

## Contract

Each inventoried artifact has one `MIG-NNNN` row across the tracked ledger and
ignored sidecar. Epoch, Catalog-query, proof-reuse, and migration dispositions
are separate fields. A move or removal requires a recovery pointer and Lock.
No row is `verified`; owner gaps remain explicit. Hash/access failure is
`blocked` and never receives an inferred identity.

Run:

```text
python -m scripts.migration_ledger check
```

The check re-enumerates tracked, untracked, ignored, private, and empty local
residue; recomputes hashes and inbound tracked references; and fails on fixed
point drift, missing/duplicate/stale rows, privacy leakage, or premature proof.
Any new in-scope artifact stales this control before migration.

Source: issues #32, #34, #38, #39, and #41; ADR-0008 and ADR-0009.
"""


def freeze(root: Path) -> int:
    public, private, observed = build_current(root)
    failures = fresh_epoch_contract.validate_migration_control(
        public,
        private,
        observed,
    )
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    public_path = root / PUBLIC_LEDGER
    private_path = root / PRIVATE_LEDGER
    closeout_path = root / CLOSEOUT
    public_path.parent.mkdir(parents=True, exist_ok=True)
    private_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.write_bytes(_serialize(public).encode("utf-8"))
    private_path.write_bytes(_serialize(private).encode("utf-8"))
    closeout_path.write_bytes(_closeout(public, private).encode("utf-8"))
    print(f"Frozen migration control: {len(public['rows'])} public rows.")
    print("Private inventory remains in the ignored sidecar.")
    return 0


def check(root: Path) -> int:
    try:
        public = _read_payload(root / PUBLIC_LEDGER)
        private = _read_payload(root / PRIVATE_LEDGER)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: Cannot read migration control: {error}")
        return 1
    fixed_point = public.get("fixed_point")
    source_head = (
        fixed_point.get("source_head")
        if isinstance(fixed_point, dict)
        else None
    )
    if not isinstance(source_head, str):
        print("FAIL: Migration control has no source HEAD.")
        return 1
    expected_public, expected_private, observed = build_current(
        root,
        source_head=source_head,
    )
    failures = fresh_epoch_contract.validate_migration_control(
        public,
        private,
        observed,
    )
    if public != expected_public:
        failures.append("Tracked migration ledger differs from current fixed point.")
    if private != expected_private:
        failures.append("Private migration sidecar differs from current fixed point.")
    if failures:
        for failure in sorted(set(failures)):
            print(f"FAIL: {failure}")
        return 1
    print(f"Migration control complete: {len(public['rows'])} public rows.")
    print("Private inventory matched without publishing source locators.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("freeze", "check"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    if arguments.action == "freeze":
        return freeze(root)
    return check(root)


if __name__ == "__main__":
    raise SystemExit(main())
