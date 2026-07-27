"""Freeze and check the Fresh Composition Epoch migration control."""

from __future__ import annotations

import argparse
import copy
import json
import re
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
CATALOG_SOURCE = (
    "docs/research/skill-pack-composition/catalog-contract-research.md"
)
CATALOG_TARGET = "docs/research/skill-pack-composition/sources/SRC-0001.md"
CATALOG_OWNER = "docs/research/skill-pack-composition/sources/README.md"
EXPLAINED_OLD_PATH_OWNERS = frozenset(
    {
        PUBLIC_LEDGER.as_posix(),
        "scripts/fresh_epoch_contract.py",
        "scripts/migration_ledger.py",
        "tests/test_migration_ledger.py",
    }
)


class MigrationBlocked(RuntimeError):
    """A migration precondition or proof boundary was not satisfied."""


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


def _head_paths(root: Path, head: str) -> set[str]:
    paths = set(_git(root, "ls-tree", "-r", "--name-only", head))
    changed = set(_git(root, "diff", "--name-only", head))
    return paths.difference(changed)


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
    selected_head = source_head or _head(root)
    return fresh_epoch_contract.build_migration_control(
        root,
        public_paths=public_paths,
        private_paths=private_paths,
        reference_paths=reference_paths,
        head=selected_head,
        head_paths=_head_paths(root, selected_head),
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


def _safe_workspace_path(root: Path, relative: object) -> Path:
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or PurePosixPath(relative).is_absolute()
        or any(part in {"", ".", ".."} for part in PurePosixPath(relative).parts)
    ):
        raise MigrationBlocked(f"unsafe migration path: {relative!r}")
    resolved_root = root.resolve()
    candidate = (resolved_root / Path(*PurePosixPath(relative).parts)).resolve()
    if not candidate.is_relative_to(resolved_root):
        raise MigrationBlocked(f"migration path escapes root: {relative}")
    return candidate


def _fingerprint(content: bytes) -> str:
    return fresh_epoch_contract.exact_content_fingerprint(content)


def _require_mapping(
    row: dict[str, object],
) -> tuple[str, str, str, str]:
    source = row.get("source")
    target = row.get("target")
    if not isinstance(source, dict) or not isinstance(target, dict):
        raise MigrationBlocked("migration row has no source/target mapping")
    source_key = source.get("key")
    source_fingerprint = source.get("fingerprint")
    target_path = target.get("path")
    target_identity = target.get("semantic_id")
    if not all(
        isinstance(value, str) and value
        for value in (
            source_key,
            source_fingerprint,
            target_path,
            target_identity,
        )
    ):
        raise MigrationBlocked("migration row mapping is incomplete")
    if row.get("migration_disposition") != "move":
        raise MigrationBlocked("migration row is not an authorized move")
    return (
        str(source_key),
        str(source_fingerprint),
        str(target_path),
        str(target_identity),
    )


def prepare_migration(row: dict[str, object]) -> dict[str, object]:
    """Apply the source-authorized concrete plan to the catalog tracer row."""

    prepared = copy.deepcopy(row)
    prior_result = prepared.get("observed_result")
    rollback_proved = (
        prior_result.get("rollback_proved") is True
        if isinstance(prior_result, dict)
        else False
    )
    source = prepared.get("source")
    if not isinstance(source, dict) or source.get("key") != CATALOG_SOURCE:
        raise MigrationBlocked("selected row is not the catalog migration tracer")
    prepared.update(
        {
            "owner": CATALOG_OWNER,
            "owner_gap": None,
            "migration_disposition": "move",
            "target": {
                "semantic_id": "SRC-0001",
                "path": CATALOG_TARGET,
            },
            "basis": ["issue-34-current-to-target-mapping"],
            "reference_rewrite_set": [CATALOG_SOURCE],
            "required_proof": [
                "target-read-back",
                "reference-reconciliation",
                "owner-routing",
                "validator-proof",
                "old-path-disposition",
                "rollback",
            ],
            "status": "prepared",
            "observed_result": (
                {"passed": False, "rollback_proved": True}
                if rollback_proved
                else None
            ),
            "residual_risk": "migration and proof remain pending",
        }
    )
    recovery = prepared.get("recovery")
    if not isinstance(recovery, dict) or not recovery.get("pointer"):
        raise MigrationBlocked("catalog migration has no recovery pointer")
    recovery["applicable_lock"] = "FCE-pack-lock"
    return prepared


def _git_recovery_bytes(root: Path, row: dict[str, object]) -> bytes:
    recovery = row.get("recovery")
    pointer = recovery.get("pointer") if isinstance(recovery, dict) else None
    match = (
        re.fullmatch(
            r"git:(?P<head>[0-9a-f]{40}):(?P<path>.+)@"
            r"(?P<fingerprint>sha256-v1:[0-9a-f]{64})",
            pointer,
        )
        if isinstance(pointer, str)
        else None
    )
    if match is None:
        raise MigrationBlocked("migration recovery is not Git-addressed")
    completed = subprocess.run(
        [
            "git",
            "cat-file",
            "--filters",
            f"--path={match.group('path')}",
            f"{match.group('head')}:{match.group('path')}",
        ],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise MigrationBlocked("cannot read migration recovery bytes")
    if _fingerprint(completed.stdout) != match.group("fingerprint"):
        raise MigrationBlocked("migration recovery fingerprint mismatch")
    return completed.stdout


def _normalized_target_bytes(
    original: bytes,
    *,
    source_key: str,
    target_key: str,
    target_identity: str,
) -> bytes:
    rewritten = original.replace(
        source_key.encode("utf-8"),
        target_key.encode("utf-8"),
    )
    return (
        f"---\nartifact_id: {target_identity}\n---\n\n".encode("utf-8")
        + rewritten
    )


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    temporary = path.with_name(f".{path.name}.migration-new")
    try:
        temporary.write_bytes(content)
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_migration(
    root: Path,
    row: dict[str, object],
) -> dict[str, object]:
    """Apply or resume one recoverable move and its declared path rewrites."""

    applied = copy.deepcopy(row)
    (
        source_key,
        source_fingerprint,
        target_key,
        target_identity,
    ) = _require_mapping(applied)
    source_path = _safe_workspace_path(root, source_key)
    target_path = _safe_workspace_path(root, target_key)
    owner_path = _safe_workspace_path(root, applied.get("owner"))
    if not owner_path.is_file():
        raise MigrationBlocked("target owner does not exist")
    source_exists = source_path.is_file()
    target_exists = target_path.is_file()
    if not source_exists and not target_exists:
        raise MigrationBlocked("source and target are both absent")
    original = _git_recovery_bytes(root, applied)
    if _fingerprint(original) != source_fingerprint:
        raise MigrationBlocked("recovery bytes do not match frozen source")
    if source_exists and source_path.read_bytes() != original:
        raise MigrationBlocked("source fingerprint mismatch")
    rewritten = original.replace(
        source_key.encode("utf-8"),
        target_key.encode("utf-8"),
    )
    normalized = _normalized_target_bytes(
        original,
        source_key=source_key,
        target_key=target_key,
        target_identity=target_identity,
    )
    allowed_target_bytes = {original, rewritten, normalized}
    if target_exists and target_path.read_bytes() not in allowed_target_bytes:
        raise MigrationBlocked("target collision: mismatched bytes")

    rewrites = applied.get("reference_rewrite_set")
    if not isinstance(rewrites, list) or not rewrites:
        raise MigrationBlocked("migration row has no reference rewrite set")

    moved_now = source_exists and not target_exists
    duplicate_source = source_exists and target_exists
    if not target_path.parent.is_dir():
        raise MigrationBlocked("target owner directory does not exist")
    if moved_now:
        source_path.replace(target_path)
    original_reference_bytes: dict[Path, bytes] = {}
    try:
        for raw_reference in rewrites:
            reference_key = (
                target_key if raw_reference == source_key else raw_reference
            )
            reference_path = _safe_workspace_path(root, reference_key)
            if not reference_path.is_file():
                raise MigrationBlocked(
                    f"declared reference is absent: {raw_reference}"
                )
            reference_bytes = reference_path.read_bytes()
            original_reference_bytes[reference_path] = reference_bytes
            replacement = (
                normalized
                if raw_reference == source_key
                else reference_bytes.replace(
                    source_key.encode("utf-8"),
                    target_key.encode("utf-8"),
                )
            )
            if (
                raw_reference != source_key
                and replacement == reference_bytes
                and target_key.encode("utf-8") not in reference_bytes
            ):
                raise MigrationBlocked(
                    f"declared reference has neither locator: {raw_reference}"
                )
            if replacement != reference_bytes:
                _atomic_write_bytes(reference_path, replacement)
        if duplicate_source:
            source_path.unlink()
    except Exception:
        for reference_path, reference_bytes in original_reference_bytes.items():
            _atomic_write_bytes(reference_path, reference_bytes)
        if moved_now and target_path.exists() and not source_path.exists():
            target_path.replace(source_path)
        raise

    target_bytes = target_path.read_bytes()
    prior = applied.get("observed_result")
    rollback_proved = (
        prior.get("rollback_proved") is True
        if isinstance(prior, dict)
        else False
    )
    applied["status"] = "references-reconciled"
    applied["observed_result"] = {
        "passed": False,
        "moved_fingerprint": source_fingerprint,
        "target_fingerprint": _fingerprint(target_bytes),
        "source_absent": not source_path.exists(),
        "target_path": target_key,
        "reference_rewrites": sorted(str(item) for item in rewrites),
        "exact_target_reconciled": target_exists,
        "rollback_proved": rollback_proved,
    }
    applied["residual_risk"] = "final target and old-path proof remain pending"
    return applied


def rollback_migration(
    root: Path,
    row: dict[str, object],
) -> dict[str, object]:
    """Restore original bytes and locators before semantic normalization."""

    rolled_back = copy.deepcopy(row)
    (
        source_key,
        source_fingerprint,
        target_key,
        target_identity,
    ) = _require_mapping(rolled_back)
    source_path = _safe_workspace_path(root, source_key)
    target_path = _safe_workspace_path(root, target_key)
    original = _git_recovery_bytes(root, rolled_back)
    if _fingerprint(original) != source_fingerprint:
        raise MigrationBlocked("recovery bytes do not match frozen source")
    if source_path.exists() and source_path.read_bytes() != original:
        raise MigrationBlocked("rollback source collision")
    normalized = _normalized_target_bytes(
        original,
        source_key=source_key,
        target_key=target_key,
        target_identity=target_identity,
    )
    allowed_target_bytes = {
        original,
        original.replace(
            source_key.encode("utf-8"),
            target_key.encode("utf-8"),
        ),
        normalized,
    }
    if target_path.exists() and (
        not target_path.is_file()
        or target_path.read_bytes() not in allowed_target_bytes
    ):
        raise MigrationBlocked("target changed after migration; rollback blocked")
    if not source_path.exists() and not target_path.exists():
        raise MigrationBlocked("rollback source and target are both absent")

    rewrites = rolled_back.get("reference_rewrite_set")
    if not isinstance(rewrites, list):
        raise MigrationBlocked("migration row has no reference rewrite set")
    for raw_reference in rewrites:
        if raw_reference == source_key:
            continue
        reference_path = _safe_workspace_path(root, raw_reference)
        if not reference_path.is_file():
            raise MigrationBlocked(
                f"declared reference is absent: {raw_reference}"
            )
        content = reference_path.read_bytes()
        restored = content.replace(
            target_key.encode("utf-8"),
            source_key.encode("utf-8"),
        )
        if restored != content:
            _atomic_write_bytes(reference_path, restored)
    if not source_path.exists():
        _atomic_write_bytes(source_path, original)
    if target_path.exists():
        target_path.unlink()
    rolled_back["status"] = "prepared"
    rolled_back["observed_result"] = {
        "passed": False,
        "rollback_proved": True,
        "restored_fingerprint": source_fingerprint,
    }
    rolled_back["residual_risk"] = "migration remains pending after rollback"
    return rolled_back


def _text_inventory(root: Path) -> list[str]:
    paths = set(_git(root, "ls-files"))
    paths.update(_git(root, "ls-files", "--others", "--exclude-standard"))
    return sorted(paths)


def verify_migration(
    root: Path,
    row: dict[str, object],
) -> dict[str, object]:
    """Verify target identity, routing, disposition, and old-path closure."""

    verified = copy.deepcopy(row)
    source_key, source_fingerprint, target_key, target_identity = _require_mapping(
        verified
    )
    source_path = _safe_workspace_path(root, source_key)
    target_path = _safe_workspace_path(root, target_key)
    owner_path = _safe_workspace_path(root, verified.get("owner"))
    if source_path.exists() or not target_path.is_file():
        raise MigrationBlocked("migration target/source disposition is incomplete")
    if not owner_path.is_file():
        raise MigrationBlocked("target owner does not exist")
    original = _git_recovery_bytes(root, verified)
    expected_target = _normalized_target_bytes(
        original,
        source_key=source_key,
        target_key=target_key,
        target_identity=target_identity,
    )
    try:
        target_bytes = target_path.read_bytes()
    except OSError as error:
        raise MigrationBlocked(f"cannot read migration target: {error}") from error
    if target_bytes != expected_target:
        raise MigrationBlocked("target differs from allowed source normalization")
    observed_identity = fresh_epoch_contract._artifact_identity(target_path)
    if observed_identity != target_identity:
        raise MigrationBlocked("target semantic identity mismatch")

    explained: list[str] = []
    unexplained: list[str] = []
    needle = source_key.encode("utf-8")
    for relative in _text_inventory(root):
        path = _safe_workspace_path(root, relative)
        if not path.is_file():
            continue
        try:
            content = path.read_bytes()
        except OSError as error:
            raise MigrationBlocked(
                f"cannot complete old-path scan: {relative}: {error}"
            ) from error
        if needle not in content:
            continue
        if relative in EXPLAINED_OLD_PATH_OWNERS:
            explained.append(relative)
        else:
            unexplained.append(relative)
    if unexplained:
        raise MigrationBlocked(
            "unexplained old-path reference: " + ", ".join(unexplained)
        )

    prior = verified.get("observed_result")
    prior = prior if isinstance(prior, dict) else {}
    verified["status"] = "verified"
    verified["observed_result"] = {
        **prior,
        "passed": True,
        "moved_fingerprint": source_fingerprint,
        "source_absent": True,
        "target_fingerprint": _fingerprint(target_bytes),
        "target_identity": observed_identity,
        "target_path": target_key,
        "owner": str(verified["owner"]),
        "unexplained_old_path_references": [],
        "explained_historical_references": sorted(explained),
    }
    verified["residual_risk"] = (
        "semantic admission and proof reuse remain explicitly unassessed"
    )
    return verified


def _write_control_state(
    root: Path,
    public: dict[str, object],
    private: dict[str, object],
) -> None:
    outputs = {
        root / PUBLIC_LEDGER: _serialize(public).encode("utf-8"),
        root / CLOSEOUT: _closeout(public, private).encode("utf-8"),
    }
    originals = {path: path.read_bytes() for path in outputs}
    temporaries = {
        path: path.with_name(f".{path.name}.new") for path in outputs
    }
    try:
        for path, content in outputs.items():
            temporaries[path].write_bytes(content)
        for path in outputs:
            temporaries[path].replace(path)
    except OSError:
        for path, content in originals.items():
            _atomic_write_bytes(path, content)
        raise
    finally:
        for temporary in temporaries.values():
            if temporary.exists():
                temporary.unlink()


def operate(root: Path, *, action: str, migration_id: str) -> int:
    """Run one selected migration transition and persist its row."""

    ledger_path = root / PUBLIC_LEDGER
    try:
        public = _read_payload(ledger_path)
        private = _read_payload(root / PRIVATE_LEDGER)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: Cannot read migration control: {error}")
        return 1
    rows = public.get("rows")
    if not isinstance(rows, list):
        print("FAIL: Public migration control has no rows.")
        return 1
    selected_index = next(
        (
            index
            for index, row in enumerate(rows)
            if isinstance(row, dict)
            and row.get("migration_id") == migration_id
        ),
        None,
    )
    if selected_index is None:
        print(f"FAIL: Unknown migration row: {migration_id}")
        return 1
    selected = rows[selected_index]
    assert isinstance(selected, dict)
    try:
        if action == "migrate":
            prepared = prepare_migration(selected)
            result = apply_migration(root, prepared)
        elif action == "rollback":
            result = rollback_migration(root, prepare_migration(selected))
        elif action == "verify":
            result = verify_migration(root, selected)
        else:
            raise MigrationBlocked(f"unsupported migration action: {action}")
        rows[selected_index] = result
        try:
            _write_control_state(root, public, private)
        except OSError:
            if action == "migrate":
                rollback_migration(root, result)
            elif action == "rollback":
                apply_migration(root, result)
            raise
    except (MigrationBlocked, OSError) as error:
        print(f"FAIL: {error}")
        return 1
    print(f"Migration {migration_id}: {result['status']}.")
    return 0


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
    verified_rows = [
        row
        for row in public_rows
        if isinstance(row, dict) and row.get("status") == "verified"
    ]
    fixed_point = public.get("fixed_point")
    fixed_point = fixed_point if isinstance(fixed_point, dict) else {}
    status = (
        f"active control; {len(verified_rows)} migration row(s) verified"
        if verified_rows
        else "frozen inventory; no migration authorized or performed"
    )
    verified_summary = (
        "\n".join(
            f"- `{row.get('migration_id')}` -> "
            f"`{row.get('target', {}).get('path')}`"
            for row in verified_rows
            if isinstance(row.get("target"), dict)
        )
        or "- None."
    )
    verification_contract = (
        "Only the listed rows are `verified`; every other row remains pending."
        if verified_rows
        else "No row is `verified`; owner gaps remain explicit."
    )
    return f"""# Fresh Composition Epoch migration control

Status: {status}.

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

## Verified migrations

{verified_summary}

## Contract

Each inventoried artifact has one `MIG-NNNN` row across the tracked ledger and
ignored sidecar. Epoch, Catalog-query, proof-reuse, and migration dispositions
are separate fields. A move or removal requires a recovery pointer and Lock.
{verification_contract} Hash/access failure is `blocked` and never receives
an inferred identity.

Run:

```text
python -m scripts.migration_ledger check
```

The check re-enumerates tracked, untracked, ignored, private, and empty local
residue; verifies unchanged public content and each applied target; and fails
on unexplained path/content drift, missing/duplicate/stale rows, privacy
leakage, or premature proof.

Source: issues #32, #34, #38, #39, #41, and #46; ADR-0008 and ADR-0009.
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


def _check_applied(
    root: Path,
    public: dict[str, object],
    private: dict[str, object],
) -> list[str]:
    failures: list[str] = []
    public_rows = public.get("rows")
    private_rows = private.get("rows")
    if not isinstance(public_rows, list) or not isinstance(private_rows, list):
        return ["Migration control rows are incomplete."]
    fixed_point = public.get("fixed_point")
    fixed_point = fixed_point if isinstance(fixed_point, dict) else {}
    synthetic_observed = {
        "public_inventory_fingerprint": fixed_point.get(
            "public_inventory_fingerprint"
        ),
        "private_inventory_fingerprint": fixed_point.get(
            "private_inventory_fingerprint"
        ),
        "public_source_keys": [
            row.get("source", {}).get("key")
            for row in public_rows
            if isinstance(row, dict) and isinstance(row.get("source"), dict)
        ],
        "private_source_keys": [
            row.get("source", {}).get("key")
            for row in private_rows
            if isinstance(row, dict) and isinstance(row.get("source"), dict)
        ],
    }
    failures.extend(
        fresh_epoch_contract.validate_migration_control(
            public,
            private,
            synthetic_observed,
        )
    )

    (
        current_public,
        current_private,
        _,
        _,
        _,
    ) = discover_inventory(root)
    expected_public: set[str] = set()
    support_changes: dict[str, dict[str, object]] = {}
    for row in public_rows:
        if not isinstance(row, dict) or not isinstance(row.get("source"), dict):
            continue
        source = row["source"]
        source_key = source.get("key")
        if not isinstance(source_key, str):
            continue
        if row.get("status") == "verified" and row.get(
            "migration_disposition"
        ) == "move":
            target = row.get("target")
            target_key = target.get("path") if isinstance(target, dict) else None
            if isinstance(target_key, str):
                expected_public.add(target_key)
            try:
                reverified = verify_migration(root, row)
            except MigrationBlocked as error:
                failures.append(str(error))
            else:
                if reverified.get("observed_result") != row.get("observed_result"):
                    failures.append(
                        f"Verified migration proof drift: {row.get('migration_id')}"
                    )
            observed_result = row.get("observed_result")
            if isinstance(observed_result, dict):
                raw_support = observed_result.get("support_fingerprints")
                if isinstance(raw_support, dict):
                    support_changes.update(
                        {
                            str(key): value
                            for key, value in raw_support.items()
                            if isinstance(value, dict)
                        }
                    )
            continue
        expected_public.add(source_key)

    actual_public = {
        relative
        for relative in current_public
        if fresh_epoch_contract._path_fingerprint(
            _safe_workspace_path(root, relative)
        )
        is not None
    }
    for missing in sorted(expected_public - actual_public):
        failures.append(f"Missing migration-controlled path: {missing}")
    for extra in sorted(actual_public - expected_public):
        failures.append(f"Uninventoried migration-controlled path: {extra}")

    row_by_source = {
        row["source"]["key"]: row
        for row in public_rows
        if isinstance(row, dict)
        and isinstance(row.get("source"), dict)
        and isinstance(row["source"].get("key"), str)
    }
    for relative in sorted(actual_public):
        row = row_by_source.get(relative)
        if row is None:
            continue
        expected_fingerprint = row["source"].get("fingerprint")
        support = support_changes.get(relative)
        if support is not None:
            if support.get("before") != expected_fingerprint:
                failures.append(f"Support baseline mismatch: {relative}")
            expected_fingerprint = support.get("after")
        observed_fingerprint = fresh_epoch_contract._path_fingerprint(
            _safe_workspace_path(root, relative)
        )
        if observed_fingerprint != expected_fingerprint:
            failures.append(f"Migration-controlled content drift: {relative}")

    expected_private = {
        row["source"]["key"]
        for row in private_rows
        if isinstance(row, dict)
        and isinstance(row.get("source"), dict)
        and isinstance(row["source"].get("key"), str)
    }
    if set(current_private) != expected_private:
        failures.append("Private migration inventory paths changed.")
    private_sidecar = public.get("private_sidecar")
    expected_sidecar_fingerprint = (
        private_sidecar.get("fingerprint")
        if isinstance(private_sidecar, dict)
        else None
    )
    actual_sidecar_fingerprint = fresh_epoch_contract.exact_content_fingerprint(
        _serialize(private).encode("utf-8")
    )
    if actual_sidecar_fingerprint != expected_sidecar_fingerprint:
        failures.append("Private migration sidecar identity changed.")
    return failures


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
    rows = public.get("rows")
    has_applied = isinstance(rows, list) and any(
        isinstance(row, dict)
        and row.get("status")
        in {"moved", "references-reconciled", "verified"}
        for row in rows
    )
    if has_applied:
        failures = _check_applied(root, public, private)
    else:
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
            failures.append(
                "Tracked migration ledger differs from current fixed point."
            )
        if private != expected_private:
            failures.append(
                "Private migration sidecar differs from current fixed point."
            )
    try:
        closeout = (root / CLOSEOUT).read_bytes()
    except OSError as error:
        failures.append(f"Cannot read migration closeout: {error}")
    else:
        expected_closeout = _closeout(public, private).encode("utf-8")
        if closeout != expected_closeout:
            failures.append("Migration closeout differs from public ledger.")
    if failures:
        for failure in sorted(set(failures)):
            print(f"FAIL: {failure}")
        return 1
    print(f"Migration control complete: {len(public['rows'])} public rows.")
    print("Private inventory matched without publishing source locators.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=("freeze", "check", "migrate", "rollback", "verify"),
    )
    parser.add_argument("migration_id", nargs="?")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    if arguments.action == "freeze":
        return freeze(root)
    if arguments.action == "check":
        return check(root)
    if arguments.migration_id is None:
        parser.error(f"{arguments.action} requires a migration ID")
    return operate(
        root,
        action=arguments.action,
        migration_id=arguments.migration_id,
    )


if __name__ == "__main__":
    raise SystemExit(main())
