"""Freeze and check the Fresh Composition Epoch migration control."""

from __future__ import annotations

import argparse
import copy
import json
import posixpath
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Iterable

from scripts import campaign_artifacts, fresh_epoch_contract


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
    if _fingerprint(completed.stdout) == match.group("fingerprint"):
        return completed.stdout
    raw = subprocess.run(
        [
            "git",
            "cat-file",
            "blob",
            f"{match.group('head')}:{match.group('path')}",
        ],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if (
        raw.returncode != 0
        or _fingerprint(raw.stdout) != match.group("fingerprint")
    ):
        raise MigrationBlocked("migration recovery fingerprint mismatch")
    return raw.stdout


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


def _campaign_mapping(
    rows: list[dict[str, object]],
) -> tuple[str, str, str, list[tuple[dict[str, object], str, str, str]]]:
    if not rows:
        raise MigrationBlocked("campaign migration has no rows")
    mapped: list[tuple[dict[str, object], str, str, str]] = []
    identities: set[str] = set()
    owners: set[str] = set()
    source_roots: set[str] = set()
    target_roots: set[str] = set()
    for row in rows:
        source = row.get("source")
        target = row.get("target")
        if not isinstance(source, dict) or not isinstance(target, dict):
            raise MigrationBlocked("campaign row has no source/target mapping")
        source_key = source.get("key")
        fingerprint = source.get("fingerprint")
        identity = source.get("identity")
        target_key = target.get("path")
        owner = row.get("owner")
        if not all(
            isinstance(value, str) and value
            for value in (
                source_key,
                fingerprint,
                identity,
                target_key,
                owner,
            )
        ):
            raise MigrationBlocked("campaign row mapping is incomplete")
        if (
            row.get("artifact_class") != "campaign"
            or row.get("migration_disposition") != "move"
        ):
            raise MigrationBlocked("campaign row is not an authorized move")
        source_path = PurePosixPath(str(source_key))
        target_path = PurePosixPath(str(target_key))
        identities.add(str(identity))
        owners.add(str(owner))
        source_roots.add(source_path.parent.as_posix())
        target_roots.add(target_path.parent.as_posix())
        if source_path.name != target_path.name:
            raise MigrationBlocked("campaign target changes an artifact filename")
        mapped.append(
            (row, str(source_key), str(target_key), str(fingerprint))
        )
    if (
        len(identities) != 1
        or len(owners) != 1
        or len(source_roots) != 1
        or len(target_roots) != 1
    ):
        raise MigrationBlocked("campaign rows do not describe one exact tree")
    identity = next(iter(identities))
    if not identity.startswith("campaign:"):
        raise MigrationBlocked("campaign rows have no campaign identity")
    return (
        next(iter(source_roots)),
        next(iter(target_roots)),
        next(iter(owners)),
        mapped,
    )


def _restore_paths(snapshots: dict[Path, bytes | None]) -> None:
    removable_parents: set[Path] = set()
    for path, content in snapshots.items():
        if content is None:
            if path.is_file():
                path.unlink()
            removable_parents.update(path.parents)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_bytes(path, content)
    for parent in sorted(
        removable_parents,
        key=lambda candidate: len(candidate.parts),
        reverse=True,
    ):
        if parent.is_dir():
            try:
                parent.rmdir()
            except OSError:
                pass


def _read_compact_historical_manifest(path: Path) -> dict[str, object]:
    try:
        manifest = campaign_artifacts.read_campaign_manifest(path)
    except ValueError as reader_error:
        try:
            candidate = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise MigrationBlocked(
                f"historical campaign manifest is unreadable: {error}"
            ) from error
        schema = candidate.get("schema") if isinstance(candidate, dict) else None
        campaign = (
            candidate.get("campaign") if isinstance(candidate, dict) else None
        )
        runtime_identities = (
            candidate.get("runtime_identities")
            if isinstance(candidate, dict)
            else None
        )
        if (
            not isinstance(schema, dict)
            or schema.get("name") != "deploy-campaign-manifest"
            or schema.get("version") != 5
            or schema.get("profile") != "prompt4-accepted-v1"
            or not isinstance(campaign, dict)
            or not isinstance(campaign.get("skill"), str)
            or not isinstance(campaign.get("epoch"), str)
            or not isinstance(runtime_identities, dict)
            or runtime_identities.get("tree_algorithm")
            != "campaign-tree-v1"
        ):
            raise MigrationBlocked(
                f"historical campaign manifest is unreadable: {reader_error}"
            ) from reader_error
        manifest = candidate
    except (OSError, json.JSONDecodeError) as error:
        raise MigrationBlocked(
            f"historical campaign manifest is unreadable: {error}"
        ) from error
    schema = manifest.get("schema")
    runtime_identities = manifest.get("runtime_identities")
    if (
        not isinstance(schema, dict)
        or schema.get("name")
        not in {
            "deploy-campaign-final-manifest",
            "deploy-campaign-manifest",
        }
        or schema.get("version") != 5
        or not isinstance(runtime_identities, dict)
        or runtime_identities.get("tree_algorithm") != "campaign-tree-v1"
    ):
        raise MigrationBlocked("historical campaign meaning changed")
    return manifest


MARKDOWN_LINK = re.compile(
    r"(?P<prefix>\]\()(?P<destination>[^)\s]+)(?P<suffix>\))"
)
FULL_MARKDOWN_LINK = re.compile(
    r"!?\[(?P<label>[^\]]*)\]\((?P<destination>[^)\s]+)\)"
)


def _campaign_target_bytes(
    original: bytes,
    *,
    source_key: str,
    target_key: str,
    source_root: str,
    target_root: str,
) -> bytes:
    """Rewrite moved-root locators and preserve relative Markdown targets."""

    text = original.decode("utf-8")
    source_path = PurePosixPath(source_key)
    target_path = PurePosixPath(target_key)
    source_root_path = PurePosixPath(source_root)
    target_root_path = PurePosixPath(target_root)

    def rebase(match: re.Match[str]) -> str:
        destination = match.group("destination")
        if destination.startswith(("#", "/", "http:", "https:", "mailto:")):
            return match.group(0)
        locator, separator, fragment = destination.partition("#")
        source_destination = PurePosixPath(
            posixpath.normpath(
                posixpath.join(source_path.parent.as_posix(), locator)
            )
        )
        if source_destination.is_relative_to(source_root_path):
            relative_member = source_destination.relative_to(source_root_path)
            target_destination = target_root_path / relative_member
        else:
            target_destination = source_destination
        rebased = posixpath.relpath(
            target_destination.as_posix(),
            start=target_path.parent.as_posix(),
        )
        if separator:
            rebased = f"{rebased}#{fragment}"
        return f"{match.group('prefix')}{rebased}{match.group('suffix')}"

    rebased = MARKDOWN_LINK.sub(rebase, text)
    return rebased.replace(source_root, target_root).encode("utf-8")


def apply_campaign_migration(
    root: Path,
    rows: list[dict[str, object]],
    *,
    source_overrides: dict[str, bytes] | None = None,
) -> list[dict[str, object]]:
    """Move one historical campaign tree and reconcile its locators."""

    source_root, target_root, owner, mapped = _campaign_mapping(rows)
    owner_path = _safe_workspace_path(root, owner)
    if not owner_path.is_file():
        raise MigrationBlocked("target owner does not exist")
    source_root_path = _safe_workspace_path(root, source_root)
    target_root_path = _safe_workspace_path(root, target_root)
    source_needle = source_root.encode("utf-8")
    target_needle = target_root.encode("utf-8")
    originals: dict[str, bytes] = {}
    snapshots: dict[Path, bytes | None] = {}
    reference_contexts: dict[Path, set[str]] = {}
    exact_target_state: dict[str, bool] = {}
    target_specs: dict[Path, tuple[bytes, str, str]] = {}

    for row, source_key, target_key, fingerprint in mapped:
        original = (source_overrides or {}).get(
            source_key,
            _git_recovery_bytes(root, row),
        )
        if (
            source_key not in (source_overrides or {})
            and _fingerprint(original) != fingerprint
        ):
            raise MigrationBlocked("campaign recovery fingerprint mismatch")
        originals[source_key] = original
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        source_bytes = source_path.read_bytes() if source_path.is_file() else None
        target_bytes = target_path.read_bytes() if target_path.is_file() else None
        exact_target_state[source_key] = source_bytes is None and target_bytes is not None
        expected_target = _campaign_target_bytes(
            original,
            source_key=source_key,
            target_key=target_key,
            source_root=source_root,
            target_root=target_root,
        )
        legacy_target = original.replace(source_needle, target_needle)
        if source_bytes is None and target_bytes is None:
            raise MigrationBlocked("campaign source and target are both absent")
        if source_bytes is not None and source_bytes != original:
            raise MigrationBlocked("campaign source fingerprint mismatch")
        if target_bytes is not None and target_bytes not in {
            original,
            expected_target,
            legacy_target,
        }:
            raise MigrationBlocked("campaign target collision")
        snapshots[source_path] = source_bytes
        snapshots[target_path] = target_bytes
        target_specs[target_path] = (original, source_key, target_key)
        rewrites = row.get("reference_rewrite_set")
        if not isinstance(rewrites, list):
            raise MigrationBlocked("campaign row has no reference rewrite set")
        for raw_reference in rewrites:
            if not isinstance(raw_reference, str):
                raise MigrationBlocked("campaign reference is invalid")
            reference_key = (
                raw_reference.replace(source_root, target_root, 1)
                if raw_reference.startswith(f"{source_root}/")
                else raw_reference
            )
            reference_path = _safe_workspace_path(root, reference_key)
            reference_contexts.setdefault(reference_path, set()).add(raw_reference)

    for reference_path in reference_contexts:
        if reference_path in snapshots:
            continue
        if not reference_path.is_file():
            raise MigrationBlocked(
                "declared campaign reference is absent: "
                + reference_path.relative_to(root).as_posix()
            )
        snapshots[reference_path] = reference_path.read_bytes()

    manifest_candidates = [
        (
            _safe_workspace_path(root, source_key),
            _safe_workspace_path(root, target_key),
        )
        for _, source_key, target_key, _ in mapped
        if PurePosixPath(source_key).name == "manifest.json"
    ]
    if len(manifest_candidates) != 1:
        raise MigrationBlocked("campaign tree has no exact manifest")
    source_manifest, target_manifest = manifest_candidates[0]
    _read_compact_historical_manifest(
        source_manifest if source_manifest.is_file() else target_manifest
    )

    target_root_path.mkdir(parents=True, exist_ok=True)
    try:
        for _, source_key, target_key, _ in mapped:
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            if source_path.is_file() and not target_path.is_file():
                source_path.replace(target_path)
            elif source_path.is_file() and target_path.is_file():
                source_path.unlink()
        for target_path, (
            original,
            source_key,
            target_key,
        ) in target_specs.items():
            expected_target = _campaign_target_bytes(
                original,
                source_key=source_key,
                target_key=target_key,
                source_root=source_root,
                target_root=target_root,
            )
            if target_path.read_bytes() != expected_target:
                _atomic_write_bytes(target_path, expected_target)
        for path in sorted(reference_contexts):
            content = path.read_bytes()
            target_spec = target_specs.get(path)
            if target_spec is not None:
                original, source_key, target_key = target_spec
                rewritten = _campaign_target_bytes(
                    original,
                    source_key=source_key,
                    target_key=target_key,
                    source_root=source_root,
                    target_root=target_root,
                )
            else:
                rewritten = content.replace(source_needle, target_needle)
                for raw_reference in reference_contexts[path]:
                    original_parent = PurePosixPath(
                        raw_reference
                    ).parent.as_posix()
                    actual_key = path.relative_to(root).as_posix()
                    actual_parent = PurePosixPath(actual_key).parent.as_posix()
                    for _, source_key, target_key, _ in mapped:
                        source_locator = posixpath.relpath(
                            source_key,
                            start=original_parent,
                        )
                        target_locator = posixpath.relpath(
                            target_key,
                            start=actual_parent,
                        )
                        rewritten = rewritten.replace(
                            source_locator.encode("utf-8"),
                            target_locator.encode("utf-8"),
                        )
            if rewritten != content:
                _atomic_write_bytes(path, rewritten)
        if source_root_path.is_dir() and not any(source_root_path.iterdir()):
            source_root_path.rmdir()
    except Exception:
        _restore_paths(snapshots)
        raise

    source_tree_fingerprints = {
        PurePosixPath(source_key).name: _fingerprint(originals[source_key])
        for _, source_key, _, _ in mapped
    }
    results: list[dict[str, object]] = []
    for row, source_key, target_key, fingerprint in mapped:
        result = copy.deepcopy(row)
        target_path = _safe_workspace_path(root, target_key)
        prior = result.get("observed_result")
        rollback_proved = (
            prior.get("rollback_proved") is True
            if isinstance(prior, dict)
            else False
        )
        result["status"] = "references-reconciled"
        result["observed_result"] = {
            "passed": False,
            "campaign_identity": result["source"]["identity"],
            "source_tree_fingerprints": dict(
                sorted(source_tree_fingerprints.items())
            ),
            "moved_fingerprint": fingerprint,
            "target_fingerprint": _fingerprint(target_path.read_bytes()),
            "source_absent": True,
            "target_path": target_key,
            "exact_target_reconciled": exact_target_state[source_key],
            "rollback_proved": rollback_proved,
        }
        result["residual_risk"] = (
            "campaign compatibility and old-path proof remain pending"
        )
        results.append(result)
    return results


def rollback_campaign_migration(
    root: Path,
    rows: list[dict[str, object]],
    *,
    source_overrides: dict[str, bytes] | None = None,
) -> list[dict[str, object]]:
    """Restore one historical campaign tree and every declared locator."""

    source_root, target_root, owner, mapped = _campaign_mapping(rows)
    if not _safe_workspace_path(root, owner).is_file():
        raise MigrationBlocked("target owner does not exist")
    source_needle = source_root.encode("utf-8")
    target_needle = target_root.encode("utf-8")
    originals: dict[str, bytes] = {}
    snapshots: dict[Path, bytes | None] = {}
    reference_contexts: dict[Path, set[str]] = {}
    artifact_paths: set[Path] = set()
    for row, source_key, target_key, fingerprint in mapped:
        original = (source_overrides or {}).get(
            source_key,
            _git_recovery_bytes(root, row),
        )
        if (
            source_key not in (source_overrides or {})
            and _fingerprint(original) != fingerprint
        ):
            raise MigrationBlocked("campaign recovery fingerprint mismatch")
        originals[source_key] = original
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        source_bytes = source_path.read_bytes() if source_path.is_file() else None
        target_bytes = target_path.read_bytes() if target_path.is_file() else None
        expected_target = _campaign_target_bytes(
            original,
            source_key=source_key,
            target_key=target_key,
            source_root=source_root,
            target_root=target_root,
        )
        legacy_target = original.replace(source_needle, target_needle)
        if source_bytes is None and target_bytes is None:
            raise MigrationBlocked("campaign rollback has no source or target")
        if source_bytes is not None and source_bytes != original:
            raise MigrationBlocked("campaign rollback source collision")
        if target_bytes is not None and target_bytes not in {
            original,
            expected_target,
            legacy_target,
        }:
            raise MigrationBlocked("campaign target changed; rollback blocked")
        snapshots[source_path] = source_bytes
        snapshots[target_path] = target_bytes
        artifact_paths.update({source_path, target_path})
        rewrites = row.get("reference_rewrite_set")
        if not isinstance(rewrites, list):
            raise MigrationBlocked("campaign row has no reference rewrite set")
        for raw_reference in rewrites:
            if not isinstance(raw_reference, str):
                raise MigrationBlocked("campaign reference is invalid")
            reference_key = (
                raw_reference.replace(source_root, target_root, 1)
                if raw_reference.startswith(f"{source_root}/")
                else raw_reference
            )
            reference_path = _safe_workspace_path(root, reference_key)
            reference_contexts.setdefault(reference_path, set()).add(raw_reference)
    for path in reference_contexts:
        if path not in snapshots:
            if not path.is_file():
                raise MigrationBlocked(
                    "declared campaign reference is absent: "
                    + path.relative_to(root).as_posix()
                )
            snapshots[path] = path.read_bytes()

    try:
        for path in sorted(reference_contexts):
            if path in artifact_paths or not path.is_file():
                continue
            content = path.read_bytes()
            restored = content.replace(target_needle, source_needle)
            for raw_reference in reference_contexts[path]:
                original_parent = PurePosixPath(raw_reference).parent.as_posix()
                actual_key = path.relative_to(root).as_posix()
                actual_parent = PurePosixPath(actual_key).parent.as_posix()
                for _, source_key, target_key, _ in mapped:
                    source_locator = posixpath.relpath(
                        source_key,
                        start=original_parent,
                    )
                    target_locator = posixpath.relpath(
                        target_key,
                        start=actual_parent,
                    )
                    restored = restored.replace(
                        target_locator.encode("utf-8"),
                        source_locator.encode("utf-8"),
                    )
            if restored != content:
                _atomic_write_bytes(path, restored)
        for _, source_key, target_key, _ in mapped:
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            if not source_path.is_file():
                source_path.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write_bytes(source_path, originals[source_key])
            if target_path.is_file():
                target_path.unlink()
        target_root_path = _safe_workspace_path(root, target_root)
        if target_root_path.is_dir() and not any(target_root_path.iterdir()):
            target_root_path.rmdir()
    except Exception:
        _restore_paths(snapshots)
        raise

    results: list[dict[str, object]] = []
    for row, _, _, fingerprint in mapped:
        result = copy.deepcopy(row)
        result["status"] = "prepared"
        result["observed_result"] = {
            "passed": False,
            "rollback_proved": True,
            "restored_fingerprint": fingerprint,
        }
        result["residual_risk"] = "campaign migration remains pending after rollback"
        results.append(result)
    return results


CAMPAIGN_EXPLAINED_OLD_PATH_OWNERS = frozenset(
    {
        PUBLIC_LEDGER.as_posix(),
        "scripts/migration_ledger.py",
        "tests/test_migration_ledger.py",
    }
)
CAMPAIGN_SUPPORT_PATHS = (
    "docs/synthesis/skills/to-spec.md",
    "docs/synthesis/skills/to-tickets.md",
    "docs/validation/skills/to-spec/README.md",
    "docs/validation/skills/to-tickets/README.md",
    "scripts/campaign_artifacts.py",
)

RESEARCH_SYNTHESIS_MOVES = {
    "docs/research/2026-07-24-to-spec.md": (
        "docs/research/skills/to-spec/README.md",
        "docs/research/skills/to-spec/RP-to-spec-20260724-01.md",
        "RP-to-spec-20260724-01",
    ),
    "docs/research/convergent-pr-review-2026-07-24.md": (
        "docs/research/skills/convergent-pr-review/README.md",
        (
            "docs/research/skills/convergent-pr-review/"
            "RP-convergent-pr-review-20260724-01.md"
        ),
        "RP-convergent-pr-review-20260724-01",
    ),
    "docs/research/implement-2026-07-24.md": (
        "docs/research/skills/implement/README.md",
        "docs/research/skills/implement/RP-implement-20260724-01.md",
        "RP-implement-20260724-01",
    ),
    "docs/research/implement-2026-07-24-r2.md": (
        "docs/research/skills/implement/README.md",
        "docs/research/skills/implement/RP-implement-20260724-02.md",
        "RP-implement-20260724-02",
    ),
    "docs/research/parallel-implement-2026-07-24.md": (
        "docs/research/skills/parallel-implement/README.md",
        (
            "docs/research/skills/parallel-implement/"
            "RP-parallel-implement-20260724-01.md"
        ),
        "RP-parallel-implement-20260724-01",
    ),
    "docs/research/parallel-implement-2026-07-24-r2.md": (
        "docs/research/skills/parallel-implement/README.md",
        (
            "docs/research/skills/parallel-implement/"
            "RP-parallel-implement-20260724-02.md"
        ),
        "RP-parallel-implement-20260724-02",
    ),
    "docs/research/review-deploy-2026-07-24.md": (
        "docs/research/skills/review/README.md",
        "docs/research/skills/review/RP-review-20260724-01.md",
        "RP-review-20260724-01",
    ),
    "docs/research/to-tickets-deploy-2026-07-25.md": (
        "docs/research/skills/to-tickets/README.md",
        "docs/research/skills/to-tickets/RP-to-tickets-20260725-01.md",
        "RP-to-tickets-20260725-01",
    ),
    "docs/research/writing-great-skills-deploy-2026-07-24-7d0da40-r2.md": (
        "docs/research/skills/writing-great-skills/README.md",
        (
            "docs/research/skills/writing-great-skills/"
            "RP-writing-great-skills-20260724-01.md"
        ),
        "RP-writing-great-skills-20260724-01",
    ),
    "docs/research/skill-facets/implement/README.md": (
        "docs/research/skills/implement/README.md",
        "docs/research/skills/implement/RP-implement-20260726-01.md",
        "RP-implement-20260726-01",
    ),
    "docs/research/skill-facets/implement/SEARCH-VOCABULARY.md": (
        "docs/research/skills/implement/README.md",
        "docs/research/skills/implement/RP-implement-20260726-02.md",
        "RP-implement-20260726-02",
    ),
    "docs/research/skill-facets/to-spec/2026-07-25-deploy-research.md": (
        "docs/research/skills/to-spec/README.md",
        "docs/research/skills/to-spec/RP-to-spec-20260725-01.md",
        "RP-to-spec-20260725-01",
    ),
    "docs/research/skill-facets/to-tickets/2026-07-23-deploy-research.md": (
        "docs/research/skills/to-tickets/README.md",
        "docs/research/skills/to-tickets/RP-to-tickets-20260723-01.md",
        "RP-to-tickets-20260723-01",
    ),
    "docs/research/language/skill pack ideas/ecc-skill-pack-enhancement-candidates.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0002.md",
        "SRC-0002",
    ),
    "docs/research/language/skill pack ideas/gsd-core-skill-pack-enhancements.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0003.md",
        "SRC-0003",
    ),
    "docs/research/language/skill pack ideas/gstack-review-cso-source-packet.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0004.md",
        "SRC-0004",
    ),
    "docs/research/language/skill pack ideas/react-agent-skills-composition-note.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0005.md",
        "SRC-0005",
    ),
    "docs/research/language/skill pack ideas/skilld-skill-enhancement-candidates.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0006.md",
        "SRC-0006",
    ),
    "docs/research/language/skill pack ideas/skilld-skill-generation-vocabulary.md": (
        "docs/research/skill-pack-composition/sources/README.md",
        "docs/research/skill-pack-composition/sources/SRC-0007.md",
        "SRC-0007",
    ),
}

RESEARCH_SYNTHESIS_SUPPORT_PATHS = (
    "docs/research/skills/README.md",
    "docs/research/skills/convergent-pr-review/README.md",
    "docs/research/skills/implement/README.md",
    "docs/research/skills/parallel-implement/README.md",
    "docs/research/skills/review/README.md",
    "docs/research/skills/to-spec/README.md",
    "docs/research/skills/to-tickets/README.md",
    "docs/research/skills/writing-great-skills/README.md",
    "docs/research/skill-pack-composition/sources/README.md",
)

RESEARCH_SYNTHESIS_EXPLAINED_OLD_PATH_OWNERS = frozenset(
    {
        PUBLIC_LEDGER.as_posix(),
        "scripts/fresh_epoch_contract.py",
        "scripts/migration_ledger.py",
        "tests/test_migration_ledger.py",
    }
)


def _is_research_synthesis_row(row: dict[str, object]) -> bool:
    source = row.get("source")
    source_key = source.get("key") if isinstance(source, dict) else None
    return (
        row.get("artifact_class") in {"research", "synthesis"}
        and source_key != CATALOG_SOURCE
    )


def _settled_research_synthesis_owner(source_key: str) -> str:
    if source_key == "docs/research/README.md":
        return source_key
    if source_key.startswith("docs/research/backlog/"):
        return "docs/research/backlog/README.md"
    if source_key.startswith("docs/research/language/skill pack ideas/"):
        return "docs/research/language/skill pack ideas/README.md"
    if source_key.startswith("docs/research/language/"):
        return "docs/research/language/README.md"
    if source_key == "docs/research/skill-facets/README.md":
        return source_key
    if source_key.startswith(
        "docs/research/skill-pack-composition/cards/"
    ):
        return "docs/research/skill-pack-composition/cards/README.md"
    if source_key.startswith(
        "docs/research/skill-pack-composition/sources/"
    ):
        return "docs/research/skill-pack-composition/sources/README.md"
    if source_key.startswith("docs/research/skill-pack-composition/"):
        return "docs/research/skill-pack-composition/README.md"
    if source_key.startswith("docs/research/skills/"):
        return "docs/research/skills/README.md"
    if source_key == "docs/synthesis/README.md":
        return source_key
    if source_key == "docs/synthesis/methods/README.md":
        return source_key
    if source_key.startswith("docs/synthesis/methods/prompts/"):
        return "docs/synthesis/methods/prompts/README.md"
    if source_key.startswith("docs/synthesis/methods/"):
        return source_key
    if source_key.startswith("docs/synthesis/skills/"):
        return source_key
    if source_key in {
        "docs/synthesis/skill-context-relationships.md",
        "docs/synthesis/skill-pack.md",
    }:
        return source_key
    raise MigrationBlocked(
        f"research/synthesis owner remains unsettled: {source_key}"
    )


def prepare_research_synthesis_migrations(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Settle every research/synthesis row without semantic admission."""

    prepared_rows: list[dict[str, object]] = []
    for original_row in rows:
        prepared = copy.deepcopy(original_row)
        if not _is_research_synthesis_row(prepared):
            prepared_rows.append(prepared)
            continue
        if prepared.get("status") == "verified":
            prepared_rows.append(prepared)
            continue
        source = prepared.get("source")
        if not isinstance(source, dict):
            raise MigrationBlocked("research/synthesis source is incomplete")
        source_key = source.get("key")
        fingerprint = source.get("fingerprint")
        if not isinstance(source_key, str) or not isinstance(fingerprint, str):
            raise MigrationBlocked("research/synthesis source is unreadable")
        move = RESEARCH_SYNTHESIS_MOVES.get(source_key)
        if move is None:
            prepared.update(
                {
                    "owner": (
                        _settled_research_synthesis_owner(source_key)
                    ),
                    "owner_gap": None,
                    "migration_disposition": "preserve-in-place",
                    "target": {"semantic_id": None, "path": None},
                    "basis": ["issue-48-settled-existing-owner"],
                    "reference_rewrite_set": [],
                    "required_proof": [
                        "fixed-point-identity",
                        "owner-routing",
                    ],
                    "status": "prepared",
                    "observed_result": None,
                    "residual_risk": (
                        "semantic admission and proof reuse remain unassessed"
                    ),
                }
            )
        else:
            owner, target_path, semantic_id = move
            prepared.update(
                {
                    "owner": owner,
                    "owner_gap": None,
                    "migration_disposition": "move",
                    "target": {
                        "semantic_id": semantic_id,
                        "path": target_path,
                    },
                    "basis": ["issue-48-research-synthesis-owner-mapping"],
                    "reference_rewrite_set": sorted(
                        set(
                            str(item)
                            for item in prepared.get(
                                "inbound_references",
                                [],
                            )
                            if isinstance(item, str)
                        )
                    ),
                    "required_proof": [
                        "target-read-back",
                        "reference-reconciliation",
                        "owner-routing",
                        "old-path-disposition",
                        "rollback",
                    ],
                    "status": "prepared",
                    "observed_result": None,
                    "residual_risk": "migration and proof remain pending",
                }
            )
            recovery = prepared.get("recovery")
            if not isinstance(recovery, dict) or not recovery.get("pointer"):
                raise MigrationBlocked("research/synthesis row has no recovery")
            recovery["applicable_lock"] = "FCE-pack-lock"
        prepared_rows.append(prepared)
    return prepared_rows


def _research_synthesis_mapping(
    rows: list[dict[str, object]],
) -> list[tuple[dict[str, object], str, str, str, str]]:
    mapped: list[tuple[dict[str, object], str, str, str, str]] = []
    for row in rows:
        if not _is_research_synthesis_row(row):
            continue
        if row.get("migration_disposition") != "move":
            continue
        source = row.get("source")
        target = row.get("target")
        if not isinstance(source, dict) or not isinstance(target, dict):
            raise MigrationBlocked("research/synthesis mapping is incomplete")
        values = (
            source.get("key"),
            source.get("fingerprint"),
            target.get("path"),
            target.get("semantic_id"),
        )
        if not all(isinstance(value, str) and value for value in values):
            raise MigrationBlocked("research/synthesis mapping is incomplete")
        mapped.append((row, *[str(value) for value in values]))
    return mapped


def _verified_target_map(
    rows: list[dict[str, object]],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in rows:
        if (
            row.get("status") != "verified"
            or row.get("migration_disposition") != "move"
        ):
            continue
        source = row.get("source")
        target = row.get("target")
        source_key = source.get("key") if isinstance(source, dict) else None
        target_key = target.get("path") if isinstance(target, dict) else None
        if isinstance(source_key, str) and isinstance(target_key, str):
            result[source_key] = target_key
    return result


def _research_target_bytes(
    root: Path,
    original: bytes,
    *,
    source_key: str,
    target_key: str,
    target_identity: str,
    moved_targets: dict[str, str],
    rewrite_plain_paths: bool = True,
    local_only_links: dict[str, str] | None = None,
) -> bytes:
    text = original.decode("utf-8")
    source_path = PurePosixPath(source_key)
    target_path = PurePosixPath(target_key)

    def replace_local_only(match: re.Match[str]) -> str:
        destination = match.group("destination")
        if destination.startswith(("#", "/", "http:", "https:", "mailto:")):
            return match.group(0)
        locator = destination.partition("#")[0]
        note = (local_only_links or {}).get(locator)
        label = (
            "`pre-prune residue`"
            if locator.startswith("../evals/")
            else match.group("label")
        )
        return (
            f"{label} ({note})"
            if note is not None
            else match.group(0)
        )

    if local_only_links:
        text = FULL_MARKDOWN_LINK.sub(replace_local_only, text)

    def rebase(match: re.Match[str]) -> str:
        destination = match.group("destination")
        if destination.startswith(("#", "/", "http:", "https:", "mailto:")):
            return match.group(0)
        locator, separator, fragment = destination.partition("#")
        source_destination = PurePosixPath(
            posixpath.normpath(
                posixpath.join(source_path.parent.as_posix(), locator)
            )
        )
        mapped_destination = _mapped_destination(
            source_destination.as_posix(), moved_targets
        )
        if mapped_destination is not None:
            source_destination = PurePosixPath(mapped_destination)
        elif not _safe_workspace_path(
            root,
            source_destination.as_posix(),
        ).exists():
            remaining = PurePosixPath(locator)
            while remaining.parts and remaining.parts[0] == "..":
                remaining = PurePosixPath(*remaining.parts[1:])
            candidates = (
                remaining,
                PurePosixPath("docs") / remaining,
            )
            existing = [
                candidate
                for candidate in candidates
                if _safe_workspace_path(root, candidate.as_posix()).exists()
            ]
            if len(existing) == 1:
                source_destination = existing[0]
        rebased = posixpath.relpath(
            source_destination.as_posix(),
            start=target_path.parent.as_posix(),
        )
        if separator:
            rebased = f"{rebased}#{fragment}"
        return f"{match.group('prefix')}{rebased}{match.group('suffix')}"

    rebased = MARKDOWN_LINK.sub(rebase, text)
    if rewrite_plain_paths:
        rebased = rebased.replace(source_key, target_key)
    return (
        f"---\nartifact_id: {target_identity}\n---\n\n".encode("utf-8")
        + rebased.encode("utf-8")
    )


def _mapped_destination(
    source: str,
    moved_targets: dict[str, str],
) -> str | None:
    exact = moved_targets.get(source)
    if exact is not None:
        return exact
    source_path = PurePosixPath(source)
    candidates: set[str] = set()
    for old, new in moved_targets.items():
        try:
            remainder = PurePosixPath(old).relative_to(source_path)
        except ValueError:
            continue
        candidate = PurePosixPath(new)
        for _ in remainder.parts:
            candidate = candidate.parent
        candidates.add(candidate.as_posix())
    return next(iter(candidates)) if len(candidates) == 1 else None


def _mapped_prefixes(
    mapped: list[tuple[dict[str, object], str, str, str, str]],
) -> dict[str, str]:
    candidates: dict[str, set[str]] = {}
    legacy_roots = {
        PurePosixPath("docs/validation/evals"),
        PurePosixPath("docs/validation/transcripts"),
    }
    for _, source_key, _, target_key, _ in mapped:
        source = PurePosixPath(source_key).parent
        target = PurePosixPath(target_key).parent
        while source.parts and target.parts and source not in legacy_roots:
            candidates.setdefault(source.as_posix(), set()).add(
                target.as_posix()
            )
            source = source.parent
            target = target.parent
    return {
        source: next(iter(targets))
        for source, targets in candidates.items()
        if len(targets) == 1
    }


def _rewrite_group_reference(
    content: bytes,
    *,
    original_reference: str,
    actual_reference: str,
    mapped: list[tuple[dict[str, object], str, str, str, str]],
    forward: bool,
    rewrite_plain_paths: bool = True,
    rewrite_directory_paths: bool = False,
) -> bytes:
    rewritten = content.decode("utf-8")
    actual_parent = PurePosixPath(actual_reference).parent.as_posix()
    ordered = sorted(mapped, key=lambda item: len(item[1]), reverse=True)
    if rewrite_plain_paths and rewrite_directory_paths:
        prefixes = _mapped_prefixes(mapped)
        for source_prefix in sorted(prefixes, key=len, reverse=True):
            target_prefix = prefixes[source_prefix]
            before_prefix, after_prefix = (
                (source_prefix, target_prefix)
                if forward
                else (target_prefix, source_prefix)
            )
            rewritten = rewritten.replace(before_prefix, after_prefix)
    for _, source_key, _, target_key, _ in ordered:
        source_locator_at_actual = posixpath.relpath(
            source_key,
            start=actual_parent,
        )
        target_locator = posixpath.relpath(target_key, start=actual_parent)
        before_key, after_key = (
            (source_key, target_key) if forward else (target_key, source_key)
        )
        before_locator, after_locator = (
            (source_locator_at_actual, target_locator)
            if forward
            else (target_locator, source_locator_at_actual)
        )
        if rewrite_plain_paths:
            rewritten = rewritten.replace(before_key, after_key)

        def replace_link(match: re.Match[str]) -> str:
            destination = match.group("destination")
            locator, separator, fragment = destination.partition("#")
            if locator != before_locator:
                return match.group(0)
            replacement = after_locator
            if separator:
                replacement = f"{replacement}#{fragment}"
            return (
                f"{match.group('prefix')}{replacement}"
                f"{match.group('suffix')}"
            )

        rewritten = MARKDOWN_LINK.sub(replace_link, rewritten)
    return rewritten.encode("utf-8")


def _reference_baseline_bytes(
    root: Path,
    rows: list[dict[str, object]],
    *,
    raw_reference: str,
    actual_reference: str,
) -> bytes:
    source_row = next(
        (
            row
            for row in rows
            if isinstance(row.get("source"), dict)
            and row["source"].get("key") == raw_reference
            and row.get("migration_disposition") != "move"
        ),
        None,
    )
    if source_row is not None:
        return _git_recovery_bytes(root, source_row)

    target_row = next(
        (
            row
            for row in rows
            if isinstance(row.get("target"), dict)
            and row["target"].get("path") == actual_reference
            and row.get("migration_disposition") == "move"
        ),
        None,
    )
    if target_row is not None:
        if target_row.get("artifact_class") == "campaign":
            source = target_row.get("source")
            identity = (
                source.get("identity") if isinstance(source, dict) else None
            )
            campaign_rows = [
                row
                for row in rows
                if row.get("artifact_class") == "campaign"
                and isinstance(row.get("source"), dict)
                and row["source"].get("identity") == identity
            ]
            source_root, target_root, _, mapped = _campaign_mapping(
                campaign_rows
            )
            campaign_member = next(
                item
                for item in mapped
                if item[2] == actual_reference
            )
            row, source_key, target_key, _ = campaign_member
            return _campaign_target_bytes(
                _git_recovery_bytes(root, row),
                source_key=source_key,
                target_key=target_key,
                source_root=source_root,
                target_root=target_root,
            )
        source = target_row.get("source")
        target = target_row.get("target")
        source_key = source.get("key") if isinstance(source, dict) else None
        target_key = target.get("path") if isinstance(target, dict) else None
        identity = (
            target.get("semantic_id") if isinstance(target, dict) else None
        )
        if all(
            isinstance(value, str) and value
            for value in (source_key, target_key, identity)
        ):
            return _research_target_bytes(
                root,
                _git_recovery_bytes(root, target_row),
                source_key=str(source_key),
                target_key=str(target_key),
                target_identity=str(identity),
                moved_targets={str(source_key): str(target_key)},
            )

    fallback_row = next(
        (
            row
            for row in rows
            if isinstance(row.get("source"), dict)
            and row["source"].get("key") == raw_reference
        ),
        None,
    )
    if fallback_row is not None:
        return _git_recovery_bytes(root, fallback_row)
    raise MigrationBlocked(
        f"declared reference has no recoverable baseline: {raw_reference}"
    )


def _reference_expected_bytes(
    root: Path,
    rows: list[dict[str, object]],
    mapped: list[tuple[dict[str, object], str, str, str, str]],
    *,
    raw_reference: str,
    actual_reference: str,
) -> tuple[bytes, bytes]:
    baseline = _reference_baseline_bytes(
        root,
        rows,
        raw_reference=raw_reference,
        actual_reference=actual_reference,
    )
    expected = _rewrite_group_reference(
        baseline,
        original_reference=raw_reference,
        actual_reference=actual_reference,
        mapped=mapped,
        forward=True,
    )
    return baseline, expected


def _research_synthesis_support_fingerprints(
    root: Path,
    rows: list[dict[str, object]],
) -> dict[str, dict[str, str | None]]:
    recovery = next(
        (
            row.get("recovery")
            for row in rows
            if _is_research_synthesis_row(row)
            and isinstance(row.get("recovery"), dict)
        ),
        None,
    )
    pointer = recovery.get("pointer") if isinstance(recovery, dict) else None
    match = re.fullmatch(
        r"git:(?P<head>[0-9a-f]{40}):.+@sha256-v1:[0-9a-f]{64}",
        pointer or "",
    )
    if match is None:
        raise MigrationBlocked("research/synthesis support has no fixed point")
    result: dict[str, dict[str, str | None]] = {}
    for row in rows:
        observed = row.get("observed_result")
        inherited = (
            observed.get("support_fingerprints")
            if isinstance(observed, dict)
            else None
        )
        if isinstance(inherited, dict):
            result.update(
                {
                    str(key): value
                    for key, value in inherited.items()
                    if isinstance(value, dict)
                }
            )
    reference_paths = {
        str(reference)
        for row in rows
        for reference in row.get("reference_rewrite_set", [])
        if isinstance(reference, str)
    }
    verified_targets = _verified_target_map(rows)
    reference_paths = {
        verified_targets.get(relative, relative)
        for relative in reference_paths
    }
    current_targets = {
        target_key
        for _, _, _, target_key, _ in _research_synthesis_mapping(rows)
    }
    reference_paths.difference_update(current_targets)
    for relative in sorted(
        set(RESEARCH_SYNTHESIS_SUPPORT_PATHS) | reference_paths
    ):
        path = _safe_workspace_path(root, relative)
        if not path.is_file():
            continue
        completed = subprocess.run(
            [
                "git",
                "cat-file",
                "--filters",
                f"--path={relative}",
                f"{match.group('head')}:{relative}",
            ],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        result[relative] = {
            "before": (
                _fingerprint(completed.stdout)
                if completed.returncode == 0
                else None
            ),
            "after": fresh_epoch_contract._path_fingerprint(path),
        }
    return result


def apply_research_synthesis_migrations(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Move the settled research/synthesis lane as one recoverable group."""

    mapped = _research_synthesis_mapping(rows)
    target_by_source = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    target_by_source.update(_verified_target_map(rows))
    research_targets = {
        target_key for _, _, _, target_key, _ in mapped
    }
    snapshots: dict[Path, bytes | None] = {}
    reference_contexts: dict[tuple[str, str], Path] = {}
    reference_states: dict[tuple[str, str], tuple[bytes, bytes]] = {}
    for row, source_key, fingerprint, target_key, identity in mapped:
        owner = _safe_workspace_path(root, row.get("owner"))
        if not owner.is_file():
            raise MigrationBlocked(f"target owner does not exist: {row.get('owner')}")
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        original = _git_recovery_bytes(root, row)
        if _fingerprint(original) != fingerprint:
            raise MigrationBlocked("research/synthesis recovery mismatch")
        if source_path.is_file() and source_path.read_bytes() != original:
            raise MigrationBlocked(f"source fingerprint mismatch: {source_key}")
        expected = _research_target_bytes(
            root,
            original,
            source_key=source_key,
            target_key=target_key,
            target_identity=identity,
            moved_targets=target_by_source,
        )
        expected = _rewrite_group_reference(
            expected,
            original_reference=source_key,
            actual_reference=target_key,
            mapped=mapped,
            forward=True,
        )
        if target_path.is_file() and target_path.read_bytes() != expected:
            raise MigrationBlocked(f"target collision: {target_key}")
        if not source_path.is_file() and not target_path.is_file():
            raise MigrationBlocked(f"source and target absent: {source_key}")
        snapshots[source_path] = (
            source_path.read_bytes() if source_path.is_file() else None
        )
        snapshots[target_path] = (
            target_path.read_bytes() if target_path.is_file() else None
        )
        for raw_reference in row.get("reference_rewrite_set", []):
            if not isinstance(raw_reference, str):
                continue
            actual_reference = target_by_source.get(
                raw_reference,
                raw_reference,
            )
            if actual_reference in research_targets:
                continue
            reference_path = _safe_workspace_path(root, actual_reference)
            reference_contexts[(raw_reference, actual_reference)] = reference_path
            baseline, expected_reference = _reference_expected_bytes(
                root,
                rows,
                mapped,
                raw_reference=raw_reference,
                actual_reference=actual_reference,
            )
            reference_states[(raw_reference, actual_reference)] = (
                baseline,
                expected_reference,
            )
            if (
                not reference_path.is_file()
                or reference_path.read_bytes()
                not in {baseline, expected_reference}
            ):
                raise MigrationBlocked(
                    "declared reference content mismatch: "
                    f"{actual_reference}"
                )
            if reference_path not in snapshots:
                snapshots[reference_path] = (
                    reference_path.read_bytes()
                    if reference_path.is_file()
                    else None
                )

    try:
        for _, source_key, _, target_key, identity in mapped:
            row = next(item for item in rows if item.get("source", {}).get("key") == source_key)
            original = _git_recovery_bytes(root, row)
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_bytes = _research_target_bytes(
                root,
                original,
                source_key=source_key,
                target_key=target_key,
                target_identity=identity,
                moved_targets=target_by_source,
            )
            target_bytes = _rewrite_group_reference(
                target_bytes,
                original_reference=source_key,
                actual_reference=target_key,
                mapped=mapped,
                forward=True,
            )
            _atomic_write_bytes(target_path, target_bytes)
            if source_path.is_file():
                source_path.unlink()
        for (raw_reference, actual_reference), path in reference_contexts.items():
            _, expected_reference = reference_states[
                (raw_reference, actual_reference)
            ]
            if path.read_bytes() != expected_reference:
                _atomic_write_bytes(path, expected_reference)
    except Exception:
        _restore_paths(snapshots)
        raise

    results: list[dict[str, object]] = []
    for row in rows:
        result = copy.deepcopy(row)
        if _is_research_synthesis_row(result):
            result["status"] = (
                "references-reconciled"
                if result.get("migration_disposition") == "move"
                else "prepared"
            )
            result["observed_result"] = {
                "passed": False,
                "rollback_proved": False,
            }
        results.append(result)
    return results


def rollback_research_synthesis_migrations(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Restore the research/synthesis lane to frozen source bytes."""

    mapped = _research_synthesis_mapping(rows)
    target_by_source = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    target_by_source.update(_verified_target_map(rows))
    research_targets = {
        target_key for _, _, _, target_key, _ in mapped
    }
    snapshots: dict[Path, bytes | None] = {}
    reference_contexts: dict[tuple[str, str], Path] = {}
    reference_states: dict[tuple[str, str], tuple[bytes, bytes]] = {}
    for row, source_key, fingerprint, target_key, identity in mapped:
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        original = _git_recovery_bytes(root, row)
        expected_target = _research_target_bytes(
            root,
            original,
            source_key=source_key,
            target_key=target_key,
            target_identity=identity,
            moved_targets=target_by_source,
        )
        expected_target = _rewrite_group_reference(
            expected_target,
            original_reference=source_key,
            actual_reference=target_key,
            mapped=mapped,
            forward=True,
        )
        if source_path.is_file() and source_path.read_bytes() != original:
            raise MigrationBlocked(
                f"rollback source collision: {source_key}"
            )
        if target_path.is_file() and target_path.read_bytes() != expected_target:
            raise MigrationBlocked(
                f"rollback target collision: {target_key}"
            )
        if not source_path.is_file() and not target_path.is_file():
            raise MigrationBlocked(
                f"rollback source and target are absent: {source_key}"
            )
        snapshots[source_path] = (
            source_path.read_bytes() if source_path.is_file() else None
        )
        snapshots[target_path] = (
            target_path.read_bytes() if target_path.is_file() else None
        )
        for raw_reference in row.get("reference_rewrite_set", []):
            if isinstance(raw_reference, str):
                actual_reference = target_by_source.get(
                    raw_reference,
                    raw_reference,
                )
                path = _safe_workspace_path(root, actual_reference)
                reference_contexts[(raw_reference, actual_reference)] = path
                if actual_reference not in research_targets:
                    baseline, expected_reference = _reference_expected_bytes(
                        root,
                        rows,
                        mapped,
                        raw_reference=raw_reference,
                        actual_reference=actual_reference,
                    )
                    reference_states[(raw_reference, actual_reference)] = (
                        baseline,
                        expected_reference,
                    )
                    if (
                        not path.is_file()
                        or path.read_bytes()
                        not in {baseline, expected_reference}
                    ):
                        raise MigrationBlocked(
                            "declared reference content mismatch: "
                            f"{actual_reference}"
                        )
                if path not in snapshots:
                    snapshots[path] = path.read_bytes() if path.is_file() else None
    try:
        for (raw_reference, actual_reference), path in reference_contexts.items():
            if path.is_file() and actual_reference not in research_targets:
                baseline, _ = reference_states[
                    (raw_reference, actual_reference)
                ]
                if path.read_bytes() != baseline:
                    _atomic_write_bytes(path, baseline)
        for row, source_key, fingerprint, target_key, _ in mapped:
            original = _git_recovery_bytes(root, row)
            if _fingerprint(original) != fingerprint:
                raise MigrationBlocked("research/synthesis recovery mismatch")
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            source_path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_bytes(source_path, original)
            if target_path.is_file():
                target_path.unlink()
    except Exception:
        _restore_paths(snapshots)
        raise
    results: list[dict[str, object]] = []
    for row in rows:
        result = copy.deepcopy(row)
        if _is_research_synthesis_row(result):
            result["status"] = "prepared"
            result["observed_result"] = {
                "passed": False,
                "rollback_proved": True,
            }
        results.append(result)
    return results


def _verify_markdown_links(
    root: Path,
    path: Path,
    relative: str,
    *,
    forbidden_paths: set[str] | None = None,
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise MigrationBlocked(
            f"cannot read moved Markdown links: {relative}: {error}"
        ) from error
    for match in MARKDOWN_LINK.finditer(text):
        destination = match.group("destination").strip("<>")
        if destination.startswith(
            ("#", "/", "http:", "https:", "mailto:")
        ):
            continue
        locator = destination.partition("#")[0]
        resolved_relative = PurePosixPath(
            posixpath.normpath(
                posixpath.join(
                    PurePosixPath(relative).parent.as_posix(),
                    locator,
                )
            )
        ).as_posix()
        if forbidden_paths and any(
            forbidden == resolved_relative
            or forbidden.startswith(resolved_relative.rstrip("/") + "/")
            for forbidden in forbidden_paths
        ):
            raise MigrationBlocked(
                "moved Markdown link targets legacy residue: "
                f"{relative} -> {destination}"
            )
        resolved = _safe_workspace_path(
            root,
            resolved_relative,
        )
        if not resolved.exists():
            raise MigrationBlocked(
                "moved Markdown link is unresolved: "
                f"{relative} -> {destination}"
            )


def verify_research_synthesis_migrations(
    root: Path,
    rows: list[dict[str, object]],
    *,
    allowed_support: dict[str, dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Prove every research/synthesis move or settled in-place owner."""

    mapped = _research_synthesis_mapping(rows)
    target_by_source = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    target_by_source.update(_verified_target_map(rows))
    research_targets = {
        target_key for _, _, _, target_key, _ in mapped
    }
    reference_contexts: set[tuple[str, str]] = set()
    for row, _, _, _, _ in mapped:
        for raw_reference in row.get("reference_rewrite_set", []):
            if not isinstance(raw_reference, str):
                continue
            actual_reference = target_by_source.get(
                raw_reference,
                raw_reference,
            )
            if actual_reference not in research_targets:
                reference_contexts.add((raw_reference, actual_reference))
    for raw_reference, actual_reference in sorted(reference_contexts):
        _, expected_reference = _reference_expected_bytes(
            root,
            rows,
            mapped,
            raw_reference=raw_reference,
            actual_reference=actual_reference,
        )
        path = _safe_workspace_path(root, actual_reference)
        current_bytes = path.read_bytes() if path.is_file() else None
        supported = (
            current_bytes is not None
            and isinstance(allowed_support, dict)
            and isinstance(allowed_support.get(actual_reference), dict)
            and allowed_support[actual_reference].get("after")
            == _fingerprint(current_bytes)
        )
        if current_bytes != expected_reference and not supported:
            raise MigrationBlocked(
                "declared reference content mismatch: "
                f"{actual_reference}"
            )
    support = _research_synthesis_support_fingerprints(root, rows)
    results: list[dict[str, object]] = []
    for row in rows:
        verified = copy.deepcopy(row)
        if not _is_research_synthesis_row(verified):
            results.append(verified)
            continue
        source = verified.get("source")
        if not isinstance(source, dict):
            raise MigrationBlocked("research/synthesis source is incomplete")
        source_key = source.get("key")
        fingerprint = source.get("fingerprint")
        if not isinstance(source_key, str) or not isinstance(fingerprint, str):
            raise MigrationBlocked("research/synthesis source is unreadable")
        owner = _safe_workspace_path(root, verified.get("owner"))
        if not owner.is_file():
            raise MigrationBlocked(f"settled owner is absent: {verified.get('owner')}")
        observed: dict[str, object]
        if verified.get("migration_disposition") == "move":
            target = verified.get("target")
            if not isinstance(target, dict):
                raise MigrationBlocked("research/synthesis target is incomplete")
            target_key = target.get("path")
            identity = target.get("semantic_id")
            if not isinstance(target_key, str) or not isinstance(identity, str):
                raise MigrationBlocked("research/synthesis target is incomplete")
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            if source_path.exists() or not target_path.is_file():
                raise MigrationBlocked("research/synthesis move is incomplete")
            original = _git_recovery_bytes(root, verified)
            expected = _research_target_bytes(
                root,
                original,
                source_key=source_key,
                target_key=target_key,
                target_identity=identity,
                moved_targets={
                    source: target
                    for _, source, _, target, _ in mapped
                },
            )
            expected = _rewrite_group_reference(
                expected,
                original_reference=source_key,
                actual_reference=target_key,
                mapped=mapped,
                forward=True,
            )
            target_bytes = target_path.read_bytes()
            supported = (
                isinstance(allowed_support, dict)
                and isinstance(allowed_support.get(target_key), dict)
                and allowed_support[target_key].get("after")
                == _fingerprint(target_bytes)
            )
            if target_bytes != expected and not supported:
                raise MigrationBlocked(f"target content mismatch: {target_key}")
            if fresh_epoch_contract._artifact_identity(target_path) != identity:
                raise MigrationBlocked(f"target identity mismatch: {target_key}")
            owner_text = owner.read_text(encoding="utf-8")
            if (
                identity not in owner_text
                or PurePosixPath(target_key).name not in owner_text
            ):
                raise MigrationBlocked(
                    f"target owner does not index packet: {target_key}"
                )
            if target_path.suffix.casefold() == ".md":
                _verify_markdown_links(root, target_path, target_key)
            observed = {
                "passed": True,
                "source_absent": True,
                "target_path": target_key,
                "target_identity": identity,
                "target_fingerprint": _fingerprint(target_bytes),
                "owner": str(verified["owner"]),
                "unexplained_old_path_references": [],
                "support_fingerprints": support,
            }
        else:
            source_path = _safe_workspace_path(root, source_key)
            original = _git_recovery_bytes(root, verified)
            expected = _rewrite_group_reference(
                original,
                original_reference=source_key,
                actual_reference=source_key,
                mapped=mapped,
                forward=True,
            )
            if not source_path.is_file():
                raise MigrationBlocked(f"preserved source drift: {source_key}")
            current = source_path.read_bytes()
            current_fingerprint = _fingerprint(current)
            support_entry = support.get(source_key)
            intentional_support_change = (
                isinstance(support_entry, dict)
                and support_entry.get("before") == fingerprint
                and support_entry.get("after") == current_fingerprint
            )
            later_supported = (
                isinstance(allowed_support, dict)
                and isinstance(allowed_support.get(source_key), dict)
                and allowed_support[source_key].get("after")
                == current_fingerprint
            )
            if (
                current != expected
                and not intentional_support_change
                and not later_supported
            ):
                raise MigrationBlocked(f"preserved source drift: {source_key}")
            observed = {
                "passed": True,
                "preserved_fingerprint": current_fingerprint,
                "owner": str(verified["owner"]),
            }
        verified["status"] = "verified"
        verified["observed_result"] = observed
        verified["residual_risk"] = (
            "semantic admission and proof reuse remain explicitly unassessed"
        )
        results.append(verified)

    for relative, fingerprints in support.items():
        if (
            not relative.casefold().endswith(".md")
            or fingerprints.get("before") == fingerprints.get("after")
        ):
            continue
        path = _safe_workspace_path(root, relative)
        if path.is_file():
            _verify_markdown_links(root, path, relative)

    needles = {
        source_key: source_key.encode("utf-8")
        for _, source_key, _, _, _ in mapped
    }
    unexplained: list[str] = []
    for relative in _text_inventory(root):
        path = _safe_workspace_path(root, relative)
        if not path.is_file():
            continue
        content = path.read_bytes()
        for source_key, needle in needles.items():
            if (
                needle in content
                and relative not in RESEARCH_SYNTHESIS_EXPLAINED_OLD_PATH_OWNERS
            ):
                unexplained.append(f"{source_key} in {relative}")
    if unexplained:
        raise MigrationBlocked(
            "unexplained research/synthesis old-path reference: "
            + ", ".join(sorted(unexplained))
        )
    return results


VALIDATION_EVAL_GROUPS = {
    "2026-07-24-writing-great-skills-incumbent-reconciliation.md": (
        "writing-great-skills",
        "EV-writing-great-skills-incumbent-reconciliation-20260724-01",
    ),
    "convergent-pr-review-2026-07-24": (
        "convergent-pr-review",
        "EV-convergent-pr-review-prompt4-20260724-01",
    ),
    "implement-prompt4": (
        "implement",
        "EV-implement-prompt4-20260724-01",
    ),
    "parallel-implement-prompt4-r2": (
        "parallel-implement",
        "EV-parallel-implement-prompt4-r2-20260724-01",
    ),
    "prototype-prompt4": (
        "prototype",
        "EV-prototype-prompt4-20260721-01",
    ),
    "review-2026-07-24-prompt4": (
        "review",
        "EV-review-prompt4-20260724-01",
    ),
    "simplify-code-b0-d0": (
        "simplify-code",
        "EV-simplify-code-b0-d0-20260723-01",
    ),
    "simplify-code-prompt4": (
        "simplify-code",
        "EV-simplify-code-prompt4-20260723-01",
    ),
    "tdd-pruning-results": (
        "tdd",
        "EV-tdd-pruning-20260722-01",
    ),
    "to-spec-2026-07-24": (
        "to-spec",
        "EV-to-spec-prompt4-20260724-01",
    ),
    "to-spec-2026-07-25": (
        "to-spec",
        "EV-to-spec-prompt4-20260725-01",
    ),
    "to-tickets-2026-07-23": (
        "to-tickets",
        "EV-to-tickets-prompt4-20260723-01",
    ),
    "to-tickets-2026-07-25": (
        "to-tickets",
        "EV-to-tickets-prompt4-20260725-01",
    ),
    "writing-great-skills-2026-07-24-7d0da40-r2-prompt5": (
        "writing-great-skills",
        "EV-writing-great-skills-prompt5-r2-20260724-01",
    ),
}

VALIDATION_TRANSCRIPT_SKILLS = (
    "writing-great-skills",
    "convergent-pr-review",
    "parallel-implement",
    "improve-codebase",
    "to-questionnaire",
    "domain-modeling",
    "grill-with-docs",
    "simplify-code",
    "audit-codebase",
    "to-tickets",
    "prototype",
    "implement",
    "research",
    "grilling",
    "to-spec",
    "review",
    "tdd",
)

VALIDATION_TRANSCRIPT_OVERRIDES = {
    "2026-07-18-audit-implement-handoff-eval.md": "audit-codebase",
    "2026-07-18-audit-pruning-equivalence-eval.md": "audit-codebase",
    "2026-07-18-coordinated-v2-behavior-eval.md": "audit-codebase",
    "2026-07-18-parallel-checkpoint-correction-eval.md": "parallel-implement",
    "2026-07-18-root-only-orchestration-eval.md": "convergent-pr-review",
}

PACK_VALIDATION_OWNER_GAPS = frozenset(
    {
        "docs/validation/evals/core-workflows.md",
        (
            "docs/validation/transcripts/"
            "2026-07-12-cohesion-followup-evals.md"
        ),
        (
            "docs/validation/transcripts/"
            "2026-07-13-cohesion-boundary-evals.md"
        ),
        (
            "docs/validation/transcripts/"
            "2026-07-13-whole-pack-workflow-traces.md"
        ),
        (
            "docs/validation/transcripts/"
            "2026-07-21-behavior-evaluation-cost-reduction.md"
        ),
    }
)

VALIDATION_REFERENCE_GAPS = {
    (
        "docs/validation/transcripts/"
        "2026-07-22-prototype-b0-c1-construction-evidence.md"
    ): (
        "docs/validation/skills/prototype/README.md",
        "Historical inactive Prototype runtime locator is no longer present.",
    )
}

VALIDATION_REFERENCE_REPAIRS = {
    "docs/synthesis/skill-context-relationships.md": {
        (
            "../validation/transcripts/"
            "2026-07-23-to-questionnaire-pruning.md"
        ): (
            "../validation/skills/to-questionnaire/evals/"
            "EV-to-questionnaire-pruning-equivalence-eval-20260721-01/"
            "evidence/"
            "2026-07-21-to-questionnaire-pruning-equivalence-eval.md"
        ),
        "2026-07-23-to-questionnaire-pruning.md": (
            "2026-07-21-to-questionnaire-pruning-equivalence-eval.md"
        ),
    }
}

VALIDATION_LOCAL_ONLY_LINKS = {
    (
        "docs/validation/evals/parallel-implement-prompt4-r2/results.md"
    ): {
        "raw/": "retained as unverifiable local residue; not tracked proof"
    },
    (
        "docs/validation/transcripts/"
        "2026-07-21-research-extraction-pruning-evidence.md"
    ): {
        "../evals/research-pruning-pre-prune/": (
            "retained as unverifiable local residue; not tracked proof"
        )
    },
    (
        "docs/validation/transcripts/"
        "2026-07-21-writing-great-skills-post-candidate-behavior-eval.md"
    ): {
        "../evals/writing-great-skills-pruning-pre-prune/": (
            "retained as unverifiable local residue; not tracked proof"
        )
    },
}

VALIDATION_STRUCTURED_REFERENCE_REPAIRS = {
    (
        "docs/validation/evals/"
        "parallel-implement-prompt4-r2/protocol-manifest.json"
    ): {
        "docs/validation/evals/parallel-implement-prompt4/**": (
            "docs/validation/skills/parallel-implement/evals/"
            "EV-parallel-implement-prompt4-r2-20260724-01/**"
        )
    }
}

VALIDATION_STRUCTURED_REFERENCE_GAPS = {
    (
        "docs/validation/evals/"
        "parallel-implement-prompt4-r2/protocol-manifest.json"
    ): {
        "prompt3_construction_transcript": (
            "blocked-reference-gap; "
            "docs/validation/transcripts/"
            "2026-07-24-parallel-implement-prompt3-construction-r2.md "
            "was absent at the migration fixed point; no target fabricated"
        )
    }
}


def _validation_preserved_owner(source_key: str) -> str | None:
    if source_key == "docs/validation/README.md":
        return source_key
    if source_key == "docs/validation/evals/README.md":
        return source_key
    if source_key == "docs/validation/transcripts/README.md":
        return source_key
    if source_key == "docs/validation/shared/README.md":
        return source_key
    if source_key.startswith("docs/validation/shared/schemas/"):
        return "docs/validation/shared/schemas/README.md"
    if source_key.startswith("docs/validation/shared/fixtures/"):
        return "docs/validation/shared/fixtures/README.md"
    if source_key.startswith("docs/validation/shared/protocols/"):
        return "docs/validation/shared/protocols/README.md"
    if source_key.startswith("docs/validation/skill-pack/"):
        return "docs/validation/skill-pack/README.md"
    if source_key == "docs/validation/skills/README.md":
        return source_key
    if source_key.startswith("docs/validation/skills/"):
        parts = PurePosixPath(source_key).parts
        if len(parts) >= 4:
            return (
                PurePosixPath(*parts[:4]) / "README.md"
            ).as_posix()
    return None


def _validation_eval_mapping(
    source_key: str,
) -> tuple[str, str, str] | None:
    prefix = "docs/validation/evals/"
    if not source_key.startswith(prefix):
        return None
    relative = PurePosixPath(source_key).relative_to(prefix)
    group = relative.parts[0]
    mapping = VALIDATION_EVAL_GROUPS.get(group)
    if mapping is None:
        return None
    skill, eval_id = mapping
    if len(relative.parts) == 1:
        member = f"results{PurePosixPath(group).suffix}"
    else:
        member = PurePosixPath(*relative.parts[1:]).as_posix()
    target = (
        PurePosixPath("docs/validation/skills")
        / skill
        / "evals"
        / eval_id
        / member
    ).as_posix()
    return skill, eval_id, target


def _validation_transcript_mapping(
    source_key: str,
) -> tuple[str, str, str] | None:
    prefix = "docs/validation/transcripts/"
    if not source_key.startswith(prefix) or source_key.endswith("/README.md"):
        return None
    filename = PurePosixPath(source_key).name
    skill = VALIDATION_TRANSCRIPT_OVERRIDES.get(filename)
    stem = PurePosixPath(filename).stem
    match = re.fullmatch(
        r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<purpose>.+)",
        stem,
    )
    if match is None:
        return None
    purpose = match.group("purpose")
    if skill is None:
        skill = next(
            (
                candidate
                for candidate in VALIDATION_TRANSCRIPT_SKILLS
                if candidate in purpose
            ),
            None,
        )
    if skill is None:
        return None
    normalized_purpose = purpose.replace(skill, "").strip("-")
    if not normalized_purpose:
        normalized_purpose = "historical-evidence"
    date = match.group("date").replace("-", "")
    eval_id = f"EV-{skill}-{normalized_purpose}-{date}-01"
    target = (
        PurePosixPath("docs/validation/skills")
        / skill
        / "evals"
        / eval_id
        / "evidence"
        / filename
    ).as_posix()
    return skill, eval_id, target


def prepare_validation_migrations(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Assign every remaining validation row to an owner or explicit gap."""

    prepared_rows: list[dict[str, object]] = []
    for original in rows:
        prepared = copy.deepcopy(original)
        source = prepared.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        if (
            not isinstance(source_key, str)
            or not source_key.startswith("docs/validation/")
            or prepared.get("artifact_class") == "campaign"
            or prepared.get("status") == "verified"
        ):
            prepared_rows.append(prepared)
            continue
        if source_key in PACK_VALIDATION_OWNER_GAPS:
            prepared.update(
                {
                    "owner": "docs/validation/skill-pack/README.md",
                    "owner_gap": (
                        "Historical pack-result identity is ambiguous; "
                        "preserved without fabricating a composition epoch."
                    ),
                    "migration_disposition": "owner-gap",
                    "target": {"semantic_id": None, "path": None},
                    "basis": ["issue-49-explicit-pack-owner-gap"],
                    "reference_rewrite_set": [],
                    "required_proof": ["fixed-point-identity"],
                    "status": "blocked",
                    "observed_result": {
                        "passed": False,
                        "preserved_fingerprint": source.get("fingerprint"),
                    },
                    "residual_risk": (
                        "pack-level historical identity remains unresolved"
                    ),
                }
            )
            prepared_rows.append(prepared)
            continue
        reference_gap = VALIDATION_REFERENCE_GAPS.get(source_key)
        if reference_gap is not None:
            owner, gap = reference_gap
            prepared.update(
                {
                    "owner": owner,
                    "owner_gap": None,
                    "migration_disposition": "preserve-in-place",
                    "target": {"semantic_id": None, "path": None},
                    "basis": ["issue-49-reference-gap"],
                    "reference_rewrite_set": [],
                    "required_proof": [
                        "fixed-point-identity",
                        "reference-reconciliation",
                    ],
                    "status": "blocked",
                    "observed_result": {
                        "passed": False,
                        "preserved_fingerprint": source.get("fingerprint"),
                    },
                    "residual_risk": gap,
                }
            )
            prepared_rows.append(prepared)
            continue
        mapping = (
            _validation_eval_mapping(source_key)
            or _validation_transcript_mapping(source_key)
        )
        if mapping is not None:
            skill, eval_id, target_path = mapping
            prior_result = prepared.get("observed_result")
            rollback_proved = (
                isinstance(prior_result, dict)
                and prior_result.get("rollback_proved") is True
            )
            prepared.update(
                {
                    "owner": (
                        f"docs/validation/skills/{skill}/README.md"
                    ),
                    "owner_gap": None,
                    "migration_disposition": "move",
                    "target": {
                        "semantic_id": eval_id,
                        "path": target_path,
                    },
                    "basis": ["issue-49-validation-owner-mapping"],
                    "reference_rewrite_set": sorted(
                        {
                            str(item)
                            for item in prepared.get(
                                "inbound_references", []
                            )
                            if isinstance(item, str)
                        }
                    ),
                    "required_proof": [
                        "target-read-back",
                        "reference-reconciliation",
                        "owner-routing",
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
                raise MigrationBlocked("validation row has no recovery pointer")
            recovery["applicable_lock"] = "FCE-pack-lock"
            prepared_rows.append(prepared)
            continue
        owner = _validation_preserved_owner(source_key)
        if owner is None:
            prepared.update(
                {
                    "owner": "docs/validation/skill-pack/README.md",
                    "owner_gap": "Validation owner could not be proved.",
                    "migration_disposition": "owner-gap",
                    "target": {"semantic_id": None, "path": None},
                    "basis": ["issue-49-explicit-owner-gap"],
                    "reference_rewrite_set": [],
                    "required_proof": ["fixed-point-identity"],
                    "status": "blocked",
                    "observed_result": {
                        "passed": False,
                        "preserved_fingerprint": source.get("fingerprint"),
                    },
                    "residual_risk": "validation owner remains unresolved",
                }
            )
        else:
            prepared.update(
                {
                    "owner": owner,
                    "owner_gap": None,
                    "migration_disposition": "preserve-in-place",
                    "target": {"semantic_id": None, "path": None},
                    "basis": ["issue-49-settled-existing-owner"],
                    "reference_rewrite_set": [],
                    "required_proof": [
                        "fixed-point-identity",
                        "owner-routing",
                    ],
                    "status": "prepared",
                    "observed_result": None,
                    "residual_risk": (
                        "semantic admission and proof reuse remain unassessed"
                    ),
                }
            )
        prepared_rows.append(prepared)
    return prepared_rows


def _validation_mapping(
    rows: list[dict[str, object]],
) -> list[tuple[dict[str, object], str, str, str, str]]:
    mapped: list[tuple[dict[str, object], str, str, str, str]] = []
    targets: set[str] = set()
    for row in rows:
        if row.get("migration_disposition") != "move":
            continue
        source = row.get("source")
        target = row.get("target")
        source_key = source.get("key") if isinstance(source, dict) else None
        fingerprint = (
            source.get("fingerprint") if isinstance(source, dict) else None
        )
        target_key = target.get("path") if isinstance(target, dict) else None
        identity = (
            target.get("semantic_id") if isinstance(target, dict) else None
        )
        if (
            row.get("artifact_class")
            not in {"evaluation", "validation-transcript"}
            or not all(
                isinstance(value, str) and value
                for value in (
                    source_key,
                    fingerprint,
                    target_key,
                    identity,
                )
            )
        ):
            continue
        if str(target_key) in targets:
            raise MigrationBlocked(
                f"duplicate validation target: {target_key}"
            )
        targets.add(str(target_key))
        mapped.append(
            (
                row,
                str(source_key),
                str(fingerprint),
                str(target_key),
                str(identity),
            )
        )
    return mapped


def _validation_prior_mapping(
    rows: list[dict[str, object]],
) -> list[tuple[dict[str, object], str, str, str, str]]:
    mapped: list[tuple[dict[str, object], str, str, str, str]] = []
    for row in rows:
        if (
            row.get("migration_disposition") != "move"
            or row.get("status")
            not in {"references-reconciled", "verified"}
            or row.get("artifact_class")
            in {"evaluation", "validation-transcript"}
        ):
            continue
        source = row.get("source")
        target = row.get("target")
        source_key = source.get("key") if isinstance(source, dict) else None
        fingerprint = (
            source.get("fingerprint") if isinstance(source, dict) else None
        )
        target_key = target.get("path") if isinstance(target, dict) else None
        identity = (
            target.get("semantic_id") if isinstance(target, dict) else None
        )
        if all(
            isinstance(value, str) and value
            for value in (source_key, fingerprint, target_key)
        ):
            mapped.append(
                (
                    row,
                    str(source_key),
                    str(fingerprint),
                    str(target_key),
                    str(identity or source.get("identity") or "path-only"),
                )
            )
    return mapped


def _validation_recovery_bytes(
    root: Path,
    row: dict[str, object],
    rows: list[dict[str, object]],
) -> bytes:
    original = _git_recovery_bytes(root, row)
    source = row.get("source")
    source_key = source.get("key") if isinstance(source, dict) else None
    if not isinstance(source_key, str):
        raise MigrationBlocked("validation source is incomplete")
    research_mapping = _research_synthesis_mapping(rows)
    replayed = _rewrite_group_reference(
        original,
        original_reference=source_key,
        actual_reference=source_key,
        mapped=research_mapping,
        forward=True,
    )
    if replayed == original:
        return original
    support_entry = next(
        (
            observed.get("support_fingerprints", {}).get(source_key)
            for candidate in rows
            for observed in [candidate.get("observed_result")]
            if isinstance(observed, dict)
            and isinstance(observed.get("support_fingerprints"), dict)
            and isinstance(
                observed["support_fingerprints"].get(source_key), dict
            )
        ),
        None,
    )
    if (
        not isinstance(support_entry, dict)
        or support_entry.get("before") != _fingerprint(original)
        or support_entry.get("after") != _fingerprint(replayed)
    ):
        raise MigrationBlocked(
            f"validation prior-migration baseline is unproved: {source_key}"
        )
    return replayed


def _validation_target_bytes(
    root: Path,
    original: bytes,
    *,
    source_key: str,
    target_key: str,
    target_identity: str,
    moved_targets: dict[str, str],
    mapped: list[tuple[dict[str, object], str, str, str, str]],
    prior_mapped: list[
        tuple[dict[str, object], str, str, str, str]
    ] | None = None,
) -> bytes:
    prefix = (
        f"---\nartifact_id: {target_identity}\n---\n\n".encode("utf-8")
    )
    normalized = _research_target_bytes(
        root,
        original,
        source_key=source_key,
        target_key=target_key,
        target_identity=target_identity,
        moved_targets=moved_targets,
        rewrite_plain_paths=PurePosixPath(target_key).suffix.casefold()
        != ".md",
        local_only_links=VALIDATION_LOCAL_ONLY_LINKS.get(source_key),
    )
    if not normalized.startswith(prefix):
        raise MigrationBlocked("validation normalization prefix mismatch")
    rewritten = _rewrite_group_reference(
        normalized[len(prefix) :],
        original_reference=source_key,
        actual_reference=target_key,
        mapped=[*(prior_mapped or []), *mapped],
        forward=True,
        rewrite_plain_paths=PurePosixPath(target_key).suffix.casefold()
        != ".md",
        rewrite_directory_paths=(
            PurePosixPath(target_key).suffix.casefold() != ".md"
        ),
    )
    campaign_roots = {
        (
            PurePosixPath(source_key).parent.as_posix(),
            PurePosixPath(target_key).parent.as_posix(),
        )
        for row, source_key, _, target_key, _ in (prior_mapped or [])
        if row.get("artifact_class") == "campaign"
    }
    if PurePosixPath(target_key).suffix.casefold() != ".md":
        for source_root, target_root in sorted(
            campaign_roots,
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            rewritten = rewritten.replace(
                source_root.encode("utf-8"),
                target_root.encode("utf-8"),
            )
    for before, after in VALIDATION_STRUCTURED_REFERENCE_REPAIRS.get(
        source_key, {}
    ).items():
        rewritten = rewritten.replace(
            before.encode("utf-8"),
            after.encode("utf-8"),
        )
    gap_dispositions = VALIDATION_STRUCTURED_REFERENCE_GAPS.get(source_key)
    if gap_dispositions:
        try:
            payload = json.loads(rewritten.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise MigrationBlocked(
                f"validation structured reference gap is unreadable: {source_key}"
            ) from error
        evidence_dispositions = payload.get("evidence_dispositions")
        if not isinstance(evidence_dispositions, dict):
            raise MigrationBlocked(
                f"validation evidence dispositions are absent: {source_key}"
            )
        evidence_dispositions.update(gap_dispositions)
        rewritten = (
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        ).encode("utf-8")
    return rewritten


def _validation_source_head(rows: list[dict[str, object]]) -> str:
    for row in rows:
        recovery = row.get("recovery")
        pointer = (
            recovery.get("pointer") if isinstance(recovery, dict) else None
        )
        match = re.fullmatch(
            r"git:(?P<head>[0-9a-f]{40}):.+@sha256-v1:[0-9a-f]{64}",
            pointer or "",
        )
        if match is not None:
            return match.group("head")
    raise MigrationBlocked("validation migration has no fixed point")


def _git_path_bytes(root: Path, head: str, relative: str) -> bytes | None:
    completed = subprocess.run(
        [
            "git",
            "cat-file",
            "blob",
            f"{head}:{relative}",
        ],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout if completed.returncode == 0 else None


def _validation_reference_states(
    root: Path,
    rows: list[dict[str, object]],
    mapped: list[tuple[dict[str, object], str, str, str, str]],
) -> dict[str, tuple[bytes, bytes]]:
    head = _validation_source_head(rows)
    moved_targets = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    moved_targets.update(_verified_target_map(rows))
    prior_mapping = _validation_prior_mapping(rows)
    moved_targets.update(
        {
            source_key: target_key
            for _, source_key, _, target_key, _ in prior_mapping
        }
    )
    validation_sources = {
        source_key for _, source_key, _, _, _ in mapped
    }
    states: dict[str, tuple[bytes, bytes]] = {}
    for row, _, _, _, _ in mapped:
        for raw_reference in row.get("reference_rewrite_set", []):
            if not isinstance(raw_reference, str):
                raise MigrationBlocked("validation reference is invalid")
            actual_reference = moved_targets.get(
                raw_reference, raw_reference
            )
            if raw_reference in validation_sources:
                continue
            path = _safe_workspace_path(root, actual_reference)
            baseline = _git_path_bytes(root, head, raw_reference)
            if baseline is None:
                if not path.is_file():
                    raise MigrationBlocked(
                        "declared validation reference is absent: "
                        + actual_reference
                    )
                baseline = path.read_bytes()
            prior_target_row = next(
                (
                    candidate
                    for candidate in rows
                    if isinstance(candidate.get("target"), dict)
                    and candidate["target"].get("path")
                    == actual_reference
                    and candidate.get("migration_disposition") == "move"
                ),
                None,
            )
            if (
                prior_target_row is not None
                and prior_target_row.get("artifact_class") == "campaign"
            ):
                source = prior_target_row.get("source")
                identity = (
                    source.get("identity")
                    if isinstance(source, dict)
                    else None
                )
                campaign_rows = [
                    candidate
                    for candidate in rows
                    if candidate.get("artifact_class") == "campaign"
                    and isinstance(candidate.get("source"), dict)
                    and candidate["source"].get("identity") == identity
                ]
                source_root, target_root, _, campaign_mapping = (
                    _campaign_mapping(campaign_rows)
                )
                member = next(
                    item
                    for item in campaign_mapping
                    if item[2] == actual_reference
                )
                campaign_row, source_key, target_key, _ = member
                overrides = _campaign_source_overrides(
                    root, rows, campaign_rows
                )
                rollback_baseline = _campaign_target_bytes(
                    overrides.get(
                        source_key,
                        _git_recovery_bytes(root, campaign_row),
                    ),
                    source_key=source_key,
                    target_key=target_key,
                    source_root=source_root,
                    target_root=target_root,
                )
            elif prior_target_row is not None:
                head_bytes = _git_path_bytes(
                    root, _head(root), actual_reference
                )
                rollback_baseline = (
                    head_bytes
                    if head_bytes is not None
                    else _reference_baseline_bytes(
                        root,
                        rows,
                        raw_reference=raw_reference,
                        actual_reference=actual_reference,
                    )
                )
            else:
                rollback_baseline = _rewrite_group_reference(
                    baseline,
                    original_reference=raw_reference,
                    actual_reference=actual_reference,
                    mapped=prior_mapping,
                    forward=True,
                )
                if path.is_file():
                    checkout_bytes = path.read_bytes()
                    if checkout_bytes.replace(b"\r\n", b"\n") == (
                        rollback_baseline.replace(b"\r\n", b"\n")
                    ):
                        rollback_baseline = checkout_bytes
            expected = _rewrite_group_reference(
                rollback_baseline,
                original_reference=raw_reference,
                actual_reference=actual_reference,
                mapped=mapped,
                forward=True,
            )
            for before, after in VALIDATION_REFERENCE_REPAIRS.get(
                actual_reference, {}
            ).items():
                expected = expected.replace(
                    before.encode("utf-8"),
                    after.encode("utf-8"),
                )
            if path.is_file():
                checkout_bytes = path.read_bytes()
                if checkout_bytes.replace(b"\r\n", b"\n") == (
                    expected.replace(b"\r\n", b"\n")
                ):
                    if b"\r\n" in checkout_bytes:
                        rollback_baseline = rollback_baseline.replace(
                            b"\r\n", b"\n"
                        ).replace(b"\n", b"\r\n")
                    else:
                        rollback_baseline = rollback_baseline.replace(
                            b"\r\n", b"\n"
                        )
                    expected = checkout_bytes
            prior = states.get(actual_reference)
            if prior is not None and prior != (rollback_baseline, expected):
                raise MigrationBlocked(
                    "validation reference has conflicting baselines: "
                    + actual_reference
                )
            states[actual_reference] = (rollback_baseline, expected)
    return states


def _validation_support_fingerprints(
    root: Path,
    rows: list[dict[str, object]],
    references: Iterable[str],
) -> dict[str, dict[str, str | None]]:
    head = _validation_source_head(rows)
    paths = {
        str(row.get("owner"))
        for row in rows
        if isinstance(row.get("owner"), str)
        and str(row.get("owner")).startswith("docs/validation/")
    }
    paths.update(references)
    paths.add("docs/validation/skills/README.md")
    for row in rows:
        if row.get("migration_disposition") != "move":
            continue
        source = row.get("source")
        target = row.get("target")
        source_key = source.get("key") if isinstance(source, dict) else None
        target_key = target.get("path") if isinstance(target, dict) else None
        if (
            row.get("artifact_class")
            in {"evaluation", "validation-transcript"}
            and isinstance(source_key, str)
            and isinstance(target_key, str)
        ):
            paths.update({source_key, target_key})
    result: dict[str, dict[str, str | None]] = {}
    source_fingerprints = {
        row["source"]["key"]: row["source"].get("fingerprint")
        for row in rows
        if isinstance(row.get("source"), dict)
        and isinstance(row["source"].get("key"), str)
    }
    for relative in sorted(paths):
        path = _safe_workspace_path(root, relative)
        before = _git_path_bytes(root, head, relative)
        result[relative] = {
            "before": (
                source_fingerprints.get(relative)
                if relative in source_fingerprints
                else _fingerprint(before) if before is not None else None
            ),
            "after": (
                fresh_epoch_contract._path_fingerprint(path)
                if path.is_file()
                else None
            ),
        }
    return result


def _validation_row_support(
    row: dict[str, object],
    support: dict[str, dict[str, str | None]],
    moved_targets: dict[str, str],
) -> dict[str, dict[str, str | None]]:
    source = row.get("source")
    target = row.get("target")
    paths = {
        "docs/validation/skills/README.md",
        str(row.get("owner")),
        str(source.get("key")) if isinstance(source, dict) else "",
        str(target.get("path")) if isinstance(target, dict) else "",
    }
    paths.update(
        moved_targets.get(reference, reference)
        for reference in row.get("reference_rewrite_set", [])
        if isinstance(reference, str)
    )
    return {
        path: support[path]
        for path in sorted(paths)
        if path in support
    }


def apply_validation_migrations(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Move every settled validation eval as one recoverable transaction."""

    mapped = _validation_mapping(rows)
    if not mapped:
        raise MigrationBlocked("validation migration has no settled moves")
    moved_targets = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    moved_targets.update(_verified_target_map(rows))
    prior_mapping = _validation_prior_mapping(rows)
    moved_targets.update(
        {
            source_key: target_key
            for _, source_key, _, target_key, _ in prior_mapping
        }
    )
    references = _validation_reference_states(root, rows, mapped)
    snapshots: dict[Path, bytes | None] = {}
    expected_targets: dict[str, bytes] = {}
    for row, source_key, fingerprint, target_key, identity in mapped:
        owner = _safe_workspace_path(root, row.get("owner"))
        if not owner.is_file():
            raise MigrationBlocked(
                f"validation owner does not exist: {row.get('owner')}"
            )
        original = _validation_recovery_bytes(root, row, rows)
        if (
            _fingerprint(original) != fingerprint
            and _fingerprint(_git_recovery_bytes(root, row)) != fingerprint
        ):
            raise MigrationBlocked("validation recovery fingerprint mismatch")
        expected = _validation_target_bytes(
            root,
            original,
            source_key=source_key,
            target_key=target_key,
            target_identity=identity,
            moved_targets=moved_targets,
            mapped=mapped,
            prior_mapped=prior_mapping,
        )
        expected_targets[target_key] = expected
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        source_bytes = (
            source_path.read_bytes() if source_path.is_file() else None
        )
        target_bytes = (
            target_path.read_bytes() if target_path.is_file() else None
        )
        prior_result = row.get("observed_result")
        prior_target_fingerprint = (
            prior_result.get("target_fingerprint")
            if isinstance(prior_result, dict)
            else None
        )
        if source_bytes is None and target_bytes is None:
            raise MigrationBlocked(
                f"validation source and target are absent: {source_key}"
            )
        if source_bytes is not None and source_bytes != original:
            raise MigrationBlocked(
                f"validation source fingerprint mismatch: {source_key}"
            )
        if (
            target_bytes is not None
            and target_bytes != expected
            and _fingerprint(target_bytes) != prior_target_fingerprint
        ):
            raise MigrationBlocked(
                f"validation target collision: {target_key}"
            )
        snapshots[source_path] = source_bytes
        snapshots[target_path] = target_bytes
    for relative, (baseline, expected) in references.items():
        path = _safe_workspace_path(root, relative)
        if not path.is_file() or path.read_bytes() not in {baseline, expected}:
            raise MigrationBlocked(
                "declared validation reference content mismatch: "
                f"{relative}; current="
                f"{_fingerprint(path.read_bytes()) if path.is_file() else None}; "
                f"baseline={_fingerprint(baseline)}; "
                f"expected={_fingerprint(expected)}"
            )
        snapshots.setdefault(path, path.read_bytes())

    try:
        for _, source_key, _, target_key, _ in mapped:
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if (
                not target_path.is_file()
                or target_path.read_bytes() != expected_targets[target_key]
            ):
                _atomic_write_bytes(
                    target_path, expected_targets[target_key]
                )
            if source_path.is_file():
                source_path.unlink()
        source_parents = {
            _safe_workspace_path(root, source_key).parent
            for _, source_key, _, _, _ in mapped
        }
        stop_roots = {
            root / "docs/validation/evals",
            root / "docs/validation/transcripts",
        }
        for parent in sorted(
            {
                ancestor
                for start in source_parents
                for ancestor in (start, *start.parents)
                if any(
                    ancestor == stop or stop in ancestor.parents
                    for stop in stop_roots
                )
            },
            key=lambda candidate: len(candidate.parts),
            reverse=True,
        ):
            if parent in stop_roots:
                continue
            if parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
        for relative, (_, expected) in references.items():
            path = _safe_workspace_path(root, relative)
            if path.read_bytes() != expected:
                _atomic_write_bytes(path, expected)
    except Exception:
        _restore_paths(snapshots)
        raise

    support = _validation_support_fingerprints(
        root, rows, references.keys()
    )
    results: list[dict[str, object]] = []
    moved_keys = {source_key for _, source_key, _, _, _ in mapped}
    for row in rows:
        result = copy.deepcopy(row)
        source = result.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        if source_key in moved_keys:
            target = result.get("target")
            target_key = (
                target.get("path") if isinstance(target, dict) else None
            )
            prior = result.get("observed_result")
            rollback_proved = (
                prior.get("rollback_proved") is True
                if isinstance(prior, dict)
                else False
            )
            result["status"] = "references-reconciled"
            result["observed_result"] = {
                "passed": False,
                "rollback_proved": rollback_proved,
                "source_absent": True,
                "target_path": target_key,
                "support_fingerprints": _validation_row_support(
                    result, support, moved_targets
                ),
            }
            result["residual_risk"] = (
                "validation identity and old-path proof remain pending"
            )
        results.append(result)
    return results


def rollback_validation_migrations(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Restore validation sources and exact fixed-point references."""

    mapped = _validation_mapping(rows)
    if not mapped:
        raise MigrationBlocked("validation migration has no settled moves")
    moved_targets = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    moved_targets.update(_verified_target_map(rows))
    prior_mapping = _validation_prior_mapping(rows)
    moved_targets.update(
        {
            source_key: target_key
            for _, source_key, _, target_key, _ in prior_mapping
        }
    )
    references = _validation_reference_states(root, rows, mapped)
    snapshots: dict[Path, bytes | None] = {}
    originals: dict[str, bytes] = {}
    for row, source_key, fingerprint, target_key, identity in mapped:
        original = _validation_recovery_bytes(root, row, rows)
        originals[source_key] = original
        expected = _validation_target_bytes(
            root,
            original,
            source_key=source_key,
            target_key=target_key,
            target_identity=identity,
            moved_targets=moved_targets,
            mapped=mapped,
            prior_mapped=prior_mapping,
        )
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        source_bytes = (
            source_path.read_bytes() if source_path.is_file() else None
        )
        target_bytes = (
            target_path.read_bytes() if target_path.is_file() else None
        )
        prior_result = row.get("observed_result")
        prior_target_fingerprint = (
            prior_result.get("target_fingerprint")
            if isinstance(prior_result, dict)
            else None
        )
        if source_bytes is not None and source_bytes != original:
            raise MigrationBlocked(
                f"validation rollback source collision: {source_key}"
            )
        if (
            target_bytes is not None
            and target_bytes != expected
            and _fingerprint(target_bytes) != prior_target_fingerprint
        ):
            raise MigrationBlocked(
                f"validation rollback target collision: {target_key}"
            )
        if source_bytes is None and target_bytes is None:
            raise MigrationBlocked(
                f"validation rollback source and target absent: {source_key}"
            )
        snapshots[source_path] = source_bytes
        snapshots[target_path] = target_bytes
    for relative, (baseline, expected) in references.items():
        path = _safe_workspace_path(root, relative)
        if not path.is_file() or path.read_bytes() not in {baseline, expected}:
            raise MigrationBlocked(
                f"declared validation reference content mismatch: {relative}"
            )
        snapshots.setdefault(path, path.read_bytes())
    try:
        for relative, (baseline, _) in references.items():
            path = _safe_workspace_path(root, relative)
            if path.read_bytes() != baseline:
                _atomic_write_bytes(path, baseline)
        for _, source_key, _, target_key, _ in mapped:
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            source_path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_bytes(source_path, originals[source_key])
            if target_path.is_file():
                target_path.unlink()
    except Exception:
        _restore_paths(snapshots)
        raise

    results: list[dict[str, object]] = []
    moved_keys = {source_key for _, source_key, _, _, _ in mapped}
    for row in rows:
        result = copy.deepcopy(row)
        source = result.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        if source_key in moved_keys:
            result["status"] = "prepared"
            result["observed_result"] = {
                "passed": False,
                "rollback_proved": True,
            }
            result["residual_risk"] = (
                "validation migration remains pending after rollback"
            )
        results.append(result)
    return results


def verify_validation_migrations(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Prove validation ownership, identity, references, and recovery."""

    mapped = _validation_mapping(rows)
    if not mapped:
        raise MigrationBlocked("validation migration has no settled moves")
    moved_targets = {
        source_key: target_key
        for _, source_key, _, target_key, _ in mapped
    }
    moved_targets.update(_verified_target_map(rows))
    prior_mapping = _validation_prior_mapping(rows)
    moved_targets.update(
        {
            source_key: target_key
            for _, source_key, _, target_key, _ in prior_mapping
        }
    )
    references = _validation_reference_states(root, rows, mapped)
    for relative, (_, expected) in references.items():
        path = _safe_workspace_path(root, relative)
        if not path.is_file() or path.read_bytes() != expected:
            raise MigrationBlocked(
                f"declared validation reference content mismatch: {relative}"
            )
    support = _validation_support_fingerprints(
        root, rows, references.keys()
    )
    moved_by_source = {
        source_key: (row, fingerprint, target_key, identity)
        for row, source_key, fingerprint, target_key, identity in mapped
    }
    results: list[dict[str, object]] = []
    for row in rows:
        verified = copy.deepcopy(row)
        source = verified.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        move = moved_by_source.get(str(source_key))
        if move is not None:
            _, fingerprint, target_key, identity = move
            source_path = _safe_workspace_path(root, source_key)
            target_path = _safe_workspace_path(root, target_key)
            owner = _safe_workspace_path(root, verified.get("owner"))
            if source_path.exists() or not target_path.is_file():
                raise MigrationBlocked(
                    f"validation move is incomplete: {source_key}"
                )
            if not owner.is_file() or "EV-" not in owner.read_text("utf-8"):
                raise MigrationBlocked(
                    f"validation owner does not route eval identities: {owner}"
                )
            expected = _validation_target_bytes(
                root,
                _validation_recovery_bytes(root, verified, rows),
                source_key=str(source_key),
                target_key=target_key,
                target_identity=identity,
                moved_targets=moved_targets,
                mapped=mapped,
                prior_mapped=prior_mapping,
            )
            target_bytes = target_path.read_bytes()
            if target_bytes != expected:
                raise MigrationBlocked(
                    f"validation target content mismatch: {target_key}"
                )
            if identity not in PurePosixPath(target_key).parts:
                raise MigrationBlocked(
                    f"validation target identity mismatch: {target_key}"
                )
            if target_path.suffix.casefold() == ".md":
                _verify_markdown_links(
                    root,
                    target_path,
                    target_key,
                    forbidden_paths=set(moved_by_source),
                )
            prior = verified.get("observed_result")
            rollback_proved = (
                prior.get("rollback_proved") is True
                if isinstance(prior, dict)
                else False
            )
            verified["status"] = "verified"
            verified["observed_result"] = {
                "passed": True,
                "rollback_proved": rollback_proved,
                "source_absent": True,
                "moved_fingerprint": fingerprint,
                "target_path": target_key,
                "target_identity": identity,
                "target_fingerprint": _fingerprint(target_bytes),
                "owner": str(verified["owner"]),
                "support_fingerprints": _validation_row_support(
                    verified, support, moved_targets
                ),
            }
            verified["residual_risk"] = (
                "semantic admission and proof reuse remain unassessed"
            )
        elif (
            isinstance(source_key, str)
            and source_key.startswith("docs/validation/")
            and verified.get("migration_disposition") == "preserve-in-place"
            and verified.get("status") != "blocked"
        ):
            path = _safe_workspace_path(root, source_key)
            owner = _safe_workspace_path(root, verified.get("owner"))
            if not path.is_file() or not owner.is_file():
                raise MigrationBlocked(
                    f"preserved validation owner is absent: {source_key}"
                )
            expected_fingerprint = source.get("fingerprint")
            current_fingerprint = fresh_epoch_contract._path_fingerprint(path)
            support_entry = support.get(source_key)
            allowed = {
                expected_fingerprint,
                (
                    support_entry.get("after")
                    if isinstance(support_entry, dict)
                    else None
                ),
            }
            if current_fingerprint not in allowed:
                raise MigrationBlocked(
                    f"preserved validation drift: {source_key}"
                )
            verified["status"] = "verified"
            verified["observed_result"] = {
                "passed": True,
                "preserved_fingerprint": current_fingerprint,
                "owner": str(verified["owner"]),
                "support_fingerprints": _validation_row_support(
                    verified, support, moved_targets
                ),
            }
        results.append(verified)

    explained_owners = {
        PUBLIC_LEDGER.as_posix(),
        "scripts/migration_ledger.py",
        "tests/test_migration_ledger.py",
        *{
            target_key
            for _, _, _, target_key, _ in mapped
            if PurePosixPath(target_key).suffix.casefold() == ".md"
        },
    }
    unexplained: list[str] = []
    for relative in _text_inventory(root):
        path = _safe_workspace_path(root, relative)
        if not path.is_file():
            continue
        content = path.read_bytes()
        for _, source_key, _, _, _ in mapped:
            if (
                source_key.encode("utf-8") in content
                and relative not in explained_owners
            ):
                unexplained.append(f"{source_key} in {relative}")
    if unexplained:
        raise MigrationBlocked(
            "unexplained validation old-path reference: "
            + ", ".join(sorted(unexplained))
        )
    return results


def _campaign_support_fingerprints(
    root: Path,
    mapped: list[tuple[dict[str, object], str, str, str]],
) -> dict[str, dict[str, str | None]]:
    recovery = mapped[0][0].get("recovery")
    pointer = recovery.get("pointer") if isinstance(recovery, dict) else None
    match = re.fullmatch(
        r"git:(?P<head>[0-9a-f]{40}):.+@sha256-v1:[0-9a-f]{64}",
        pointer or "",
    )
    if match is None:
        raise MigrationBlocked("campaign support has no recovery fixed point")
    result: dict[str, dict[str, str | None]] = {}
    controlled_paths = set(CAMPAIGN_SUPPORT_PATHS)
    controlled_paths.update(
        source_key
        for _, source_key, _, _ in mapped
    )
    controlled_paths.update(
        target_key
        for _, _, target_key, _ in mapped
    )
    for relative in sorted(controlled_paths):
        baseline = _git_path_bytes(root, match.group("head"), relative)
        before = _fingerprint(baseline) if baseline is not None else None
        path = _safe_workspace_path(root, relative)
        after = (
            fresh_epoch_contract._path_fingerprint(path)
            if path.exists()
            else None
        )
        result[relative] = {"before": before, "after": after}
    return result


def verify_campaign_migration(
    root: Path,
    rows: list[dict[str, object]],
    allowed_support: dict[str, dict[str, object]] | None = None,
    *,
    source_overrides: dict[str, bytes] | None = None,
) -> list[dict[str, object]]:
    """Prove one moved campaign tree, v1 meaning, and locator closure."""

    source_root, target_root, owner, mapped = _campaign_mapping(rows)
    if not _safe_workspace_path(root, owner).is_file():
        raise MigrationBlocked("target owner does not exist")
    source_needle = source_root.encode("utf-8")
    target_needle = target_root.encode("utf-8")
    source_tree_fingerprints: dict[str, str] = {}
    target_fingerprints: dict[str, str] = {}
    for row, source_key, target_key, fingerprint in mapped:
        source_path = _safe_workspace_path(root, source_key)
        target_path = _safe_workspace_path(root, target_key)
        if source_path.exists() or not target_path.is_file():
            raise MigrationBlocked("campaign target/source disposition is incomplete")
        original = (source_overrides or {}).get(
            source_key,
            _git_recovery_bytes(root, row),
        )
        expected = _campaign_target_bytes(
            original,
            source_key=source_key,
            target_key=target_key,
            source_root=source_root,
            target_root=target_root,
        )
        try:
            target_bytes = target_path.read_bytes()
        except OSError as error:
            raise MigrationBlocked(
                f"cannot read campaign migration target: {error}"
            ) from error
        supported = (
            isinstance(allowed_support, dict)
            and isinstance(allowed_support.get(target_key), dict)
            and allowed_support[target_key].get("after")
            == _fingerprint(target_bytes)
        )
        if target_bytes != expected and not supported:
            raise MigrationBlocked("campaign target differs from locator-only rewrite")
        source_tree_fingerprints[PurePosixPath(source_key).name] = (
            _fingerprint(original)
        )
        target_fingerprints[PurePosixPath(target_key).name] = _fingerprint(
            target_bytes
        )

    manifest_path = _safe_workspace_path(
        root,
        f"{target_root}/manifest.json",
    )
    _read_compact_historical_manifest(manifest_path)

    explained: list[str] = []
    unexplained: list[str] = []
    old_needles = {
        source_needle,
        f"validation/campaigns/{PurePosixPath(source_root).name}".encode("utf-8"),
    }
    for relative in _text_inventory(root):
        path = _safe_workspace_path(root, relative)
        if not path.is_file():
            continue
        try:
            content = path.read_bytes()
        except OSError as error:
            raise MigrationBlocked(
                f"cannot complete campaign old-path scan: {relative}: {error}"
            ) from error
        if not any(needle in content for needle in old_needles):
            continue
        if relative in CAMPAIGN_EXPLAINED_OLD_PATH_OWNERS:
            explained.append(relative)
        else:
            unexplained.append(relative)
    if unexplained:
        raise MigrationBlocked(
            "unexplained campaign old-path reference: "
            + ", ".join(unexplained)
        )

    support_fingerprints = _campaign_support_fingerprints(root, mapped)
    results: list[dict[str, object]] = []
    for row, source_key, target_key, fingerprint in mapped:
        result = copy.deepcopy(row)
        prior = result.get("observed_result")
        prior = prior if isinstance(prior, dict) else {}
        result["status"] = "verified"
        result["observed_result"] = {
            **prior,
            "passed": True,
            "campaign_identity": result["source"]["identity"],
            "source_tree_fingerprints": dict(
                sorted(source_tree_fingerprints.items())
            ),
            "target_tree_fingerprints": dict(
                sorted(target_fingerprints.items())
            ),
            "moved_fingerprint": fingerprint,
            "source_absent": True,
            "target_path": target_key,
            "manifest_schema": "deploy-campaign-final-manifest:5",
            "runtime_tree_algorithm": "campaign-tree-v1",
            "owner": owner,
            "support_fingerprints": support_fingerprints,
            "unexplained_old_path_references": [],
            "explained_historical_references": sorted(explained),
        }
        result["residual_risk"] = (
            "semantic admission and proof reuse remain explicitly unassessed"
        )
        results.append(result)
    return results


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


def terminalize_private_rows(
    root: Path,
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Prove preserved private evidence or block Lock-gated residue."""

    results: list[dict[str, object]] = []
    for row in rows:
        result = copy.deepcopy(row)
        source = result.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        state = source.get("state") if isinstance(source, dict) else None
        fingerprint = (
            source.get("fingerprint") if isinstance(source, dict) else None
        )
        if not isinstance(source_key, str):
            raise MigrationBlocked("private migration source is incomplete")
        current = fresh_epoch_contract._path_fingerprint(
            _safe_workspace_path(root, source_key)
        )
        if state == "private-ignored":
            if current == fingerprint and isinstance(fingerprint, str):
                result.update(
                    {
                        "owner_gap": None,
                        "status": "verified",
                        "observed_result": {
                            "passed": True,
                            "preserved_fingerprint": current,
                        },
                        "residual_risk": (
                            "epoch admission and proof reuse remain unassessed"
                        ),
                    }
                )
            else:
                result.update(
                    {
                        "owner_gap": (
                            "Private evidence fingerprint could not be proved."
                        ),
                        "status": "blocked",
                        "observed_result": {"passed": False},
                        "residual_risk": (
                            "private evidence identity is not currently proved"
                        ),
                    }
                )
            basis = list(result.get("basis", []))
            if "issue-49-private-terminal-disposition" not in basis:
                basis.append("issue-49-private-terminal-disposition")
            result["basis"] = basis
        elif state == "local-residue":
            result.update(
                {
                    "owner_gap": (
                        "Cleanup is Lock-gated; local residue is not a "
                        "Git artifact."
                    ),
                    "status": "blocked",
                    "observed_result": {
                        "passed": False,
                        "preserved_fingerprint": fingerprint,
                    },
                    "residual_risk": (
                        "local residue remains until separately authorized "
                        "cleanup"
                    ),
                }
            )
            basis = list(result.get("basis", []))
            if "issue-49-lock-gated-residue" not in basis:
                basis.append("issue-49-lock-gated-residue")
            result["basis"] = basis
            result["required_proof"] = [
                "authorized-cleanup-lock",
                "old-path-disposition",
            ]
        results.append(result)
    return results


def _verify_private_terminal_rows(
    root: Path,
    rows: list[dict[str, object]],
) -> list[str]:
    failures: list[str] = []
    for row in rows:
        source = row.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        state = source.get("state") if isinstance(source, dict) else None
        migration_id = str(row.get("migration_id"))
        recovery = row.get("recovery")
        applicable_lock = (
            recovery.get("applicable_lock")
            if isinstance(recovery, dict)
            else None
        )
        if not isinstance(source_key, str):
            failures.append(
                f"Private migration source is incomplete: {migration_id}"
            )
            continue
        if state == "private-ignored":
            if row.get("status") == "verified":
                current = fresh_epoch_contract._path_fingerprint(
                    _safe_workspace_path(root, source_key)
                )
                if current != source.get("fingerprint"):
                    failures.append(
                        f"Private migration proof drift: {migration_id}"
                    )
            elif row.get("status") != "blocked" or not row.get("owner_gap"):
                failures.append(
                    f"Private migration is non-terminal: {migration_id}"
                )
        elif state == "local-residue":
            if (
                row.get("status") != "blocked"
                or not row.get("owner_gap")
                or applicable_lock != "authorized-cleanup-lock"
            ):
                failures.append(
                    f"Private residue is non-terminal: {migration_id}"
                )
                continue
            observed = row.get("observed_result")
            preserved = (
                observed.get("preserved_fingerprint")
                if isinstance(observed, dict)
                else None
            )
            current = fresh_epoch_contract._path_fingerprint(
                _safe_workspace_path(root, source_key)
            )
            if (
                not isinstance(preserved, str)
                or preserved != source.get("fingerprint")
                or current != preserved
            ):
                failures.append(
                    f"Private residue proof drift: {migration_id}"
                )
    return failures


def _write_control_state(
    root: Path,
    public: dict[str, object],
    private: dict[str, object],
) -> None:
    private_bytes = _serialize(private).encode("utf-8")
    private_sidecar = public.get("private_sidecar")
    if not isinstance(private_sidecar, dict):
        private_sidecar = {"path": PRIVATE_LEDGER.as_posix()}
        public["private_sidecar"] = private_sidecar
    private_sidecar["fingerprint"] = _fingerprint(private_bytes)
    outputs = {
        root / PUBLIC_LEDGER: _serialize(public).encode("utf-8"),
        root / PRIVATE_LEDGER: private_bytes,
        root / CLOSEOUT: _closeout(public, private).encode("utf-8"),
    }
    originals = {
        path: path.read_bytes() if path.is_file() else None
        for path in outputs
    }
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
            if content is None:
                if path.is_file():
                    path.unlink()
            else:
                _atomic_write_bytes(path, content)
        raise
    finally:
        for temporary in temporaries.values():
            if temporary.exists():
                temporary.unlink()


def _campaign_source_overrides(
    root: Path,
    all_rows: list[dict[str, object]],
    campaign_rows: list[dict[str, object]],
) -> dict[str, bytes]:
    """Replay prior verified path-only migrations into campaign baselines."""

    research_mapping = _research_synthesis_mapping(all_rows)
    support: dict[str, list[dict[str, object]]] = {}
    for row in all_rows:
        observed = row.get("observed_result")
        raw_support = (
            observed.get("support_fingerprints")
            if isinstance(observed, dict)
            else None
        )
        if isinstance(raw_support, dict):
            for key, value in raw_support.items():
                if isinstance(value, dict):
                    support.setdefault(str(key), []).append(value)
    overrides: dict[str, bytes] = {}
    source_root, target_root, _, campaign_mapping = _campaign_mapping(
        campaign_rows
    )
    target_by_source = {
        source_key: target_key
        for _, source_key, target_key, _ in campaign_mapping
    }
    for row in campaign_rows:
        source = row.get("source")
        source_key = source.get("key") if isinstance(source, dict) else None
        if not isinstance(source_key, str):
            raise MigrationBlocked("campaign source is incomplete")
        original = _git_recovery_bytes(root, row)
        replayed = _rewrite_group_reference(
            original,
            original_reference=source_key,
            actual_reference=source_key,
            mapped=research_mapping,
            forward=True,
        )
        if replayed == original:
            continue
        support_entries = support.get(source_key, [])
        direct_proof = any(
            entry.get("before") == _fingerprint(original)
            and entry.get("after") == _fingerprint(replayed)
            for entry in support_entries
        )
        target_key = target_by_source[source_key]
        target_proof = any(
            entry.get("after")
            == _fingerprint(
                _campaign_target_bytes(
                    replayed,
                    source_key=source_key,
                    target_key=target_key,
                    source_root=source_root,
                    target_root=target_root,
                )
            )
            for entry in support.get(target_key, [])
        )
        if not direct_proof and not target_proof:
            raise MigrationBlocked(
                f"campaign prior-migration baseline is unproved: {source_key}"
            )
        overrides[source_key] = replayed
    return overrides


def _latest_support_fingerprints(
    rows: Iterable[dict[str, object]],
) -> dict[str, dict[str, object]]:
    support: dict[str, dict[str, object]] = {}
    for row in rows:
        observed = row.get("observed_result")
        raw_support = (
            observed.get("support_fingerprints")
            if isinstance(observed, dict)
            else None
        )
        if isinstance(raw_support, dict):
            support.update(
                {
                    str(key): value
                    for key, value in raw_support.items()
                    if isinstance(value, dict)
                }
            )
    return support


def _row_local_proof(observed: object) -> object:
    """Exclude the aggregate support snapshot from one row's stable proof."""
    if not isinstance(observed, dict):
        return observed
    return {
        key: value
        for key, value in observed.items()
        if key != "support_fingerprints"
    }


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
    selected_source = selected.get("source")
    selected_identity = (
        selected_source.get("identity")
        if isinstance(selected_source, dict)
        else None
    )
    campaign_indexes = [
        index
        for index, row in enumerate(rows)
        if isinstance(row, dict)
        and isinstance(row.get("source"), dict)
        and row["source"].get("identity") == selected_identity
        and row.get("artifact_class") == "campaign"
    ]
    is_campaign = (
        isinstance(selected_identity, str)
        and selected_identity.startswith("campaign:")
        and bool(campaign_indexes)
    )
    research_synthesis_indexes = [
        index
        for index, row in enumerate(rows)
        if isinstance(row, dict) and _is_research_synthesis_row(row)
    ]
    is_research_synthesis = (
        _is_research_synthesis_row(selected)
        and bool(research_synthesis_indexes)
    )
    selected_source_key = (
        selected.get("source", {}).get("key")
        if isinstance(selected.get("source"), dict)
        else None
    )
    validation_indexes = [
        index
        for index, row in enumerate(rows)
        if isinstance(row, dict)
        and isinstance(row.get("source"), dict)
        and str(row["source"].get("key", "")).startswith(
            "docs/validation/"
        )
        and row.get("artifact_class") != "campaign"
    ]
    is_validation = (
        isinstance(selected_source_key, str)
        and selected_source_key.startswith("docs/validation/")
        and selected.get("artifact_class") != "campaign"
        and bool(validation_indexes)
    )
    try:
        if is_campaign:
            campaign_rows = [rows[index] for index in campaign_indexes]
            assert all(isinstance(row, dict) for row in campaign_rows)
            typed_campaign_rows = [
                row for row in campaign_rows if isinstance(row, dict)
            ]
            typed_all_rows = [
                row for row in rows if isinstance(row, dict)
            ]
            campaign_overrides = _campaign_source_overrides(
                root,
                typed_all_rows,
                typed_campaign_rows,
            )
            if action == "migrate":
                campaign_result = apply_campaign_migration(
                    root,
                    typed_campaign_rows,
                    source_overrides=campaign_overrides,
                )
            elif action == "rollback":
                campaign_result = rollback_campaign_migration(
                    root,
                    typed_campaign_rows,
                    source_overrides=campaign_overrides,
                )
            elif action == "verify":
                campaign_result = verify_campaign_migration(
                    root,
                    typed_campaign_rows,
                    allowed_support=_latest_support_fingerprints(
                        typed_all_rows
                    ),
                    source_overrides=campaign_overrides,
                )
            else:
                raise MigrationBlocked(
                    f"unsupported migration action: {action}"
                )
            for index, result_row in zip(
                campaign_indexes,
                campaign_result,
                strict=True,
            ):
                rows[index] = result_row
            result_status = campaign_result[0]["status"]
        elif is_research_synthesis:
            typed_rows = [
                row for row in rows if isinstance(row, dict)
            ]
            prepared_rows = prepare_research_synthesis_migrations(typed_rows)
            if action == "migrate":
                group_result = apply_research_synthesis_migrations(
                    root,
                    prepared_rows,
                )
            elif action == "rollback":
                group_result = rollback_research_synthesis_migrations(
                    root,
                    prepared_rows,
                )
            elif action == "verify":
                group_result = verify_research_synthesis_migrations(
                    root,
                    prepared_rows,
                )
            else:
                raise MigrationBlocked(
                    f"unsupported migration action: {action}"
                )
            rows[:] = group_result
            result_status = rows[selected_index]["status"]
        elif is_validation:
            typed_rows = [
                row for row in rows if isinstance(row, dict)
            ]
            prepared_rows = prepare_validation_migrations(typed_rows)
            if action == "migrate":
                group_result = apply_validation_migrations(
                    root,
                    prepared_rows,
                )
            elif action == "rollback":
                group_result = rollback_validation_migrations(
                    root,
                    prepared_rows,
                )
            elif action == "verify":
                group_result = verify_validation_migrations(
                    root,
                    prepared_rows,
                )
                private_rows = private.get("rows")
                if not isinstance(private_rows, list):
                    raise MigrationBlocked(
                        "private migration control has no rows"
                    )
                private["rows"] = terminalize_private_rows(
                    root,
                    [
                        row
                        for row in private_rows
                        if isinstance(row, dict)
                    ],
                )
            else:
                raise MigrationBlocked(
                    f"unsupported migration action: {action}"
                )
            rows[:] = group_result
            result_status = rows[selected_index]["status"]
        else:
            if action == "migrate":
                prepared = prepare_migration(selected)
                result = apply_migration(root, prepared)
            elif action == "rollback":
                result = rollback_migration(root, prepare_migration(selected))
            elif action == "verify":
                result = verify_migration(root, selected)
            else:
                raise MigrationBlocked(
                    f"unsupported migration action: {action}"
                )
            rows[selected_index] = result
            result_status = result["status"]
        try:
            _write_control_state(root, public, private)
        except OSError:
            if is_campaign:
                if action == "migrate":
                    rollback_campaign_migration(
                        root,
                        campaign_result,
                        source_overrides=campaign_overrides,
                    )
                elif action == "rollback":
                    apply_campaign_migration(
                        root,
                        campaign_result,
                        source_overrides=campaign_overrides,
                    )
            elif is_research_synthesis:
                if action == "migrate":
                    rollback_research_synthesis_migrations(
                        root,
                        group_result,
                    )
                elif action == "rollback":
                    apply_research_synthesis_migrations(
                        root,
                        group_result,
                    )
            elif is_validation:
                if action == "migrate":
                    rollback_validation_migrations(root, group_result)
                elif action == "rollback":
                    apply_validation_migrations(root, group_result)
            else:
                if action == "migrate":
                    rollback_migration(root, result)
                elif action == "rollback":
                    apply_migration(root, result)
            raise
    except (MigrationBlocked, OSError) as error:
        print(f"FAIL: {error}")
        return 1
    print(f"Migration {migration_id}: {result_status}.")
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
        "Only the listed public rows are `verified`; every other public row "
        "remains pending. Private rows retain terminal status only in the "
        "ignored sidecar, without publishing their source locators."
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
- Private/local terminal statuses: {_state_counts(private_rows, "status")}

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
        current_private_states,
    ) = discover_inventory(root)
    expected_public: set[str] = set()
    support_changes: dict[str, dict[str, object]] = {}
    verified_campaigns: dict[str, list[dict[str, object]]] = {}
    verified_research_synthesis: list[dict[str, object]] = []
    verified_validation: list[dict[str, object]] = []
    for row in public_rows:
        if not isinstance(row, dict) or not isinstance(row.get("source"), dict):
            continue
        source = row["source"]
        source_key = source.get("key")
        if not isinstance(source_key, str):
            continue
        observed_result = row.get("observed_result")
        if row.get("status") == "verified" and isinstance(
            observed_result, dict
        ):
            raw_support = observed_result.get("support_fingerprints")
            if isinstance(raw_support, dict):
                support_changes.update(
                    {
                        str(key): value
                        for key, value in raw_support.items()
                        if isinstance(value, dict)
                    }
                )
        if (
            row.get("status") == "verified"
            and _is_research_synthesis_row(row)
        ):
            verified_research_synthesis.append(row)
            target = row.get("target")
            target_key = (
                target.get("path") if isinstance(target, dict) else None
            )
            expected_public.add(
                target_key
                if row.get("migration_disposition") == "move"
                and isinstance(target_key, str)
                else source_key
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
        if row.get("status") == "verified" and row.get(
            "migration_disposition"
        ) == "move":
            target = row.get("target")
            target_key = target.get("path") if isinstance(target, dict) else None
            if isinstance(target_key, str):
                expected_public.add(target_key)
            source_identity = source.get("identity")
            if (
                row.get("artifact_class") == "campaign"
                and isinstance(source_identity, str)
                and source_identity.startswith("campaign:")
            ):
                verified_campaigns.setdefault(source_identity, []).append(row)
            elif row.get("artifact_class") in {
                "evaluation",
                "validation-transcript",
            }:
                verified_validation.append(row)
            elif (
                isinstance(target_key, str)
                and target_key in support_changes
            ):
                pass
            else:
                try:
                    reverified = verify_migration(root, row)
                except MigrationBlocked as error:
                    failures.append(str(error))
                else:
                    if reverified.get("observed_result") != row.get(
                        "observed_result"
                    ):
                        failures.append(
                            "Verified migration proof drift: "
                            + str(row.get("migration_id"))
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

    for campaign_rows in verified_campaigns.values():
        try:
            campaign_overrides = _campaign_source_overrides(
                root,
                [
                    row
                    for row in public_rows
                    if isinstance(row, dict)
                ],
                campaign_rows,
            )
            reverified_rows = verify_campaign_migration(
                root,
                campaign_rows,
                allowed_support=support_changes,
                source_overrides=campaign_overrides,
            )
        except MigrationBlocked as error:
            failures.append(str(error))
            continue
        observed_by_id = {
            row.get("migration_id"): row.get("observed_result")
            for row in reverified_rows
        }
        campaign_has_supported_change = any(
            isinstance(row.get("target"), dict)
            and row["target"].get("path") in support_changes
            for row in campaign_rows
        )
        for row in campaign_rows:
            target = row.get("target")
            target_key = (
                target.get("path") if isinstance(target, dict) else None
            )
            if campaign_has_supported_change or (
                isinstance(target_key, str)
                and target_key in support_changes
            ):
                continue
            if observed_by_id.get(row.get("migration_id")) != row.get(
                "observed_result"
            ):
                failures.append(
                    f"Verified migration proof drift: {row.get('migration_id')}"
                )

    if verified_research_synthesis:
        try:
            reverified_rows = verify_research_synthesis_migrations(
                root,
                [
                    row
                    for row in public_rows
                    if isinstance(row, dict)
                ],
                allowed_support=support_changes,
            )
        except MigrationBlocked as error:
            failures.append(str(error))
        else:
            observed_by_id = {
                row.get("migration_id"): row.get("observed_result")
                for row in reverified_rows
            }
            for row in verified_research_synthesis:
                target = row.get("target")
                target_key = (
                    target.get("path")
                    if isinstance(target, dict)
                    else None
                )
                source = row.get("source")
                source_key = (
                    source.get("key")
                    if isinstance(source, dict)
                    else None
                )
                if (
                    target_key in support_changes
                    or source_key in support_changes
                ):
                    continue
                if _row_local_proof(
                    observed_by_id.get(row.get("migration_id"))
                ) != _row_local_proof(row.get("observed_result")):
                    failures.append(
                        "Verified migration proof drift: "
                        + str(row.get("migration_id"))
                    )

    if verified_validation:
        try:
            reverified_rows = verify_validation_migrations(
                root,
                [
                    row
                    for row in public_rows
                    if isinstance(row, dict)
                ],
            )
        except MigrationBlocked as error:
            failures.append(str(error))
        else:
            observed_by_id = {
                row.get("migration_id"): row.get("observed_result")
                for row in reverified_rows
            }
            for row in verified_validation:
                if _row_local_proof(
                    observed_by_id.get(row.get("migration_id"))
                ) != _row_local_proof(row.get("observed_result")):
                    failures.append(
                        "Verified migration proof drift: "
                        + str(row.get("migration_id"))
                    )

    for relative, support in support_changes.items():
        if support.get("after") is not None:
            expected_public.add(relative)
        else:
            expected_public.discard(relative)

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
            support = support_changes.get(relative)
            if support is not None:
                observed_fingerprint = fresh_epoch_contract._path_fingerprint(
                    _safe_workspace_path(root, relative)
                )
                if observed_fingerprint != support.get("after"):
                    failures.append(
                        f"Migration support content drift: {relative}"
                    )
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
        and row["source"].get("state") != "local-residue"
    }
    current_stable_private = {
        relative
        for relative in current_private
        if current_private_states.get(relative) != "local-residue"
    }
    failures.extend(
        _verify_private_terminal_rows(
            root,
            [
                row
                for row in private_rows
                if isinstance(row, dict)
            ],
        )
    )
    if current_stable_private != expected_private:
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
