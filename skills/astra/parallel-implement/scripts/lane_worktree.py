"""Manage worker worktrees, explicit readiness, scoped commands, and cleanup."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable


LANE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
COMMIT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
CLEANUP_RECEIPT_FORMAT = 2
LANE_SCHEMA_VERSION = 1
TRANSIENT_WINDOWS_ERRORS = {5, 32}
RETRY_DELAYS = (0.25, 0.5, 1.0, 2.0)


class LaneError(RuntimeError):
    """A lane operation could not complete safely."""


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command, cwd=cwd, text=True, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            command, 124, "", "command timed out after 120s; inspect state before retrying"
        )


def command_error(result: subprocess.CompletedProcess[str]) -> str:
    return result.stderr.strip() or result.stdout.strip() or "command failed"



def git(checkout: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = run(["git", "-C", str(checkout), *args])
    if check and result.returncode != 0:
        raise LaneError(command_error(result))
    return result


def contained(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return path != root


def lexical_absolute(value: str | Path) -> Path:
    return Path(os.path.abspath(os.fspath(value)))



def path_present(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def path_identity(path: Path) -> dict[str, int] | None:
    details = path.lstat()
    if is_reparse_point(path):
        raise LaneError(f"path identity is unsafe for a reparse point: {path}")
    device = int(getattr(details, "st_dev", 0))
    inode = int(getattr(details, "st_ino", 0))
    if inode <= 0:
        return None
    return {"device": device, "inode": inode}


def repository_root(value: str) -> Path:
    requested = Path(value).resolve()
    if not requested.is_dir():
        raise LaneError(f"repository does not exist: {requested}")
    observed = Path(git(requested, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if observed != requested:
        raise LaneError(f"--repo must be the repository root: {observed}")
    return observed


def lane_root(value: str, repo: Path, *, create: bool) -> Path:
    root = Path(value).resolve()
    if root == repo or contained(root, repo):
        raise LaneError("worktree root must be outside the repository")
    if create:
        root.mkdir(parents=True, exist_ok=True)
    return root


def resolve_base(repo: Path, value: str) -> str:
    return git(repo, "rev-parse", "--verify", f"{value}^{{commit}}").stdout.strip()



def registered_worktrees(repo: Path) -> set[Path]:
    result = git(repo, "worktree", "list", "--porcelain", "-z")
    return {
        Path(line.removeprefix("worktree ")).resolve()
        for line in result.stdout.split("\0")
        if line.startswith("worktree ")
    }


def ignored_entries(checkout: Path) -> tuple[list[str] | None, str | None]:
    result = git(
        checkout,
        "ls-files",
        "--others",
        "--ignored",
        "--exclude-standard",
        "--directory",
        "-z",
        check=False,
    )
    if result.returncode != 0:
        return None, command_error(result)
    return [entry for entry in result.stdout.split("\0") if entry], None


def lane_state(root: Path, name: str) -> Path:
    container = lexical_absolute(root / ".state")
    if path_present(container) and is_reparse_point(container):
        raise LaneError(f"lane state container is a reparse point: {container}")
    state = lexical_absolute(container / name)
    if not contained(state, root):
        raise LaneError("lane state path escapes the configured root")
    if path_present(state) and is_reparse_point(state):
        raise LaneError(f"lane state is a reparse point: {state}")
    return state


def cleanup_receipt(root: Path, name: str) -> Path:
    receipt = lexical_absolute(root / ".state" / f"{name}.cleanup.json")
    if not contained(receipt, root):
        raise LaneError("cleanup receipt path escapes the configured root")
    if path_present(receipt.parent) and is_reparse_point(receipt.parent):
        raise LaneError(f"lane state container is a reparse point: {receipt.parent}")
    return receipt


def lane_manifest(root: Path, name: str) -> Path:
    manifest = (lane_state(root, name) / "lane.json").resolve()
    if not contained(manifest, root):
        raise LaneError("lane manifest path escapes the configured root")
    return manifest


def state_paths(root: Path, name: str) -> tuple[Path, Path, Path, Path, Path]:
    state = lane_state(root, name)
    state.parent.mkdir(parents=True, exist_ok=True)
    if is_reparse_point(state.parent):
        raise LaneError(f"lane state container is a reparse point: {state.parent}")
    paths = state / "tmp", state / "cache", state / "pytest", state / "pytest-cache"
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    return state, *paths


def probe_directory(path: Path) -> None:
    probe = path / f".lane-probe-{uuid.uuid4().hex}"
    try:
        probe.write_text("created", encoding="utf-8")
        if probe.read_text(encoding="utf-8") != "created":
            raise LaneError(f"lane probe read failed: {path}")
        probe.write_text("updated", encoding="utf-8")
        if probe.read_text(encoding="utf-8") != "updated":
            raise LaneError(f"lane probe update failed: {path}")
    finally:
        probe.unlink(missing_ok=True)


def manifest_payload(
    repo: Path,
    root: Path,
    worktree: Path,
    base: str,
    runtime_root: Path,
    temp_root: Path,
    cache_root: Path,
    pytest_basetemp: Path,
    pytest_cache: Path,
) -> dict[str, Any]:
    return {
        "schema_version": LANE_SCHEMA_VERSION,
        "repository": str(repo),
        "worktree": str(worktree),
        "base": base,
        "runtime_root": str(runtime_root),
        "temp_root": str(temp_root),
        "cache_root": str(cache_root),
        "pytest_basetemp": str(pytest_basetemp),
        "pytest_cache": str(pytest_cache),
        "lane_manifest": str(lane_manifest(root, worktree.name)),
        "cleanup_receipt": str(cleanup_receipt(root, worktree.name)),
    }


def write_lane_manifest(root: Path, name: str, payload: dict[str, Any]) -> Path:
    manifest = lane_manifest(root, name)
    temporary = manifest.with_name(f"{manifest.name}.tmp")
    try:
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(manifest)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest



def read_lane_manifest(
    repo: Path, root: Path, worktree: Path
) -> tuple[dict[str, Any] | None, str | None]:
    manifest = lane_manifest(root, worktree.name)
    if not path_present(manifest):
        return None, "lane manifest is missing"
    try:
        if is_reparse_point(manifest):
            return None, "lane manifest is a reparse point"
        if not manifest.is_file():
            return None, "lane manifest is not a regular file"
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "lane manifest is unreadable"
    expected_paths = {
        "repository": str(repo),
        "worktree": str(worktree),
        "runtime_root": str(lane_state(root, worktree.name)),
        "temp_root": str(lane_state(root, worktree.name) / "tmp"),
        "cache_root": str(lane_state(root, worktree.name) / "cache"),
        "pytest_basetemp": str(lane_state(root, worktree.name) / "pytest"),
        "pytest_cache": str(lane_state(root, worktree.name) / "pytest-cache"),
        "lane_manifest": str(manifest),
        "cleanup_receipt": str(cleanup_receipt(root, worktree.name)),
    }
    if not isinstance(payload, dict) or payload.get("schema_version") != LANE_SCHEMA_VERSION:
        return None, "lane manifest schema is invalid"
    if any(payload.get(key) != value for key, value in expected_paths.items()):
        return None, "lane manifest does not match the requested lane"
    if not isinstance(payload.get("base"), str) or not COMMIT_ID.fullmatch(payload["base"]):
        return None, "lane manifest has invalid base evidence"
    return payload, None



def write_cleanup_receipt(
    repo: Path,
    root: Path,
    worktree: Path,
    lane_head: str,
    authorized_at_head: str,
) -> Path:
    state = lane_state(root, worktree.name)
    if not state.is_dir():
        raise LaneError("lane state is missing")
    receipt = cleanup_receipt(root, worktree.name)
    temporary = receipt.with_name(f"{receipt.name}.tmp")
    payload = {
        "format": CLEANUP_RECEIPT_FORMAT,
        "repository": str(repo),
        "root": str(root),
        "worktree": str(worktree),
        "lane": worktree.name,
        "lane_head": lane_head,
        "authorized_at_head": authorized_at_head,
        "worktree_identity": path_identity(worktree),
        "clean": True,
        "integrated": True,
    }
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(receipt)
    finally:
        temporary.unlink(missing_ok=True)
    observed, reason = read_cleanup_receipt(repo, root, worktree)
    if observed is None:
        raise LaneError(f"cleanup receipt read-back failed: {reason}")
    if any(observed.get(key) != payload[key] for key in payload):
        raise LaneError("cleanup receipt read-back does not match the written receipt")
    return receipt



def read_cleanup_receipt(
    repo: Path, root: Path, worktree: Path
) -> tuple[dict[str, Any] | None, str | None]:
    receipt = cleanup_receipt(root, worktree.name)
    if not path_present(receipt):
        return None, "cleanup receipt is missing"
    try:
        if is_reparse_point(receipt):
            return None, "cleanup receipt is a reparse point"
        if not receipt.is_file():
            return None, "cleanup receipt is not a regular file"
        payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "cleanup receipt is unreadable"
    if not isinstance(payload, dict) or payload.get("format") != CLEANUP_RECEIPT_FORMAT:
        return None, "cleanup receipt format is invalid"
    expected = {
        "repository": str(repo),
        "root": str(root),
        "worktree": str(worktree),
        "lane": worktree.name,
        "clean": True,
        "integrated": True,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        return None, "cleanup receipt does not match the requested lane"
    if not all(
        isinstance(payload.get(key), str)
        and COMMIT_ID.fullmatch(payload[key])
        for key in ("lane_head", "authorized_at_head")
    ):
        return None, "cleanup receipt has invalid commit evidence"

    if "worktree_identity" not in payload:
        return None, "cleanup receipt is missing worktree identity"
    identity = payload["worktree_identity"]
    if identity is not None:
        if (
            not isinstance(identity, dict)
            or set(identity) != {"device", "inode"}
            or not all(isinstance(identity.get(key), int) for key in ("device", "inode"))
            or identity["inode"] <= 0
        ):
            return None, "cleanup receipt has invalid worktree identity"
    payload["worktree_identity"] = identity
    return payload, None


def is_reparse_point(path: Path) -> bool:
    details = path.lstat()
    attributes = getattr(details, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attributes & reparse_flag)


def tree_has_reparse_point(path: Path) -> bool:
    pending = [path]
    while pending:
        current = pending.pop()
        if is_reparse_point(current):
            return True
        if current.is_dir():
            pending.extend(current.iterdir())
    return False


def failure_evidence(
    phase: str, path: Path, error: OSError, retry_count: int
) -> dict[str, Any]:
    return {
        "phase": phase,
        "path": str(path),
        "error": str(error),
        "errno": error.errno,
        "winerror": getattr(error, "winerror", None),
        "retry_count": retry_count,
    }


def clear_readonly_tree(path: Path) -> None:
    if tree_has_reparse_point(path):
        raise LaneError(f"receipt-authorized path contains a reparse point: {path}")
    pending = [path]
    while pending:
        current = pending.pop()
        current.chmod(current.stat().st_mode | stat.S_IWRITE)
        if current.is_dir():
            pending.extend(current.iterdir())


def remove_with_retry(
    path: Path,
    remove: Callable[[Path], None],
    *,
    phase: str,
    receipt_authorized: bool,
) -> dict[str, Any] | None:
    for retry_count in range(len(RETRY_DELAYS) + 1):
        try:
            remove(path)
            return None
        except FileNotFoundError:
            return None
        except OSError as error:
            winerror = getattr(error, "winerror", None)
            if winerror not in TRANSIENT_WINDOWS_ERRORS or retry_count == len(RETRY_DELAYS):
                return failure_evidence(phase, path, error, retry_count)
            if receipt_authorized and winerror == 5:
                try:
                    clear_readonly_tree(path)
                except OSError as clear_error:
                    return failure_evidence(
                        f"{phase}:clear-readonly", path, clear_error, retry_count
                    )
                except LaneError as clear_error:
                    return {
                        "phase": f"{phase}:clear-readonly",
                        "path": str(path),
                        "error": str(clear_error),
                        "errno": None,
                        "winerror": None,
                        "retry_count": retry_count,
                    }
            time.sleep(RETRY_DELAYS[retry_count])
    raise AssertionError("unreachable")


def remove_tree(
    path: Path, *, phase: str, receipt_authorized: bool
) -> dict[str, Any] | None:
    return remove_with_retry(
        path,
        shutil.rmtree,
        phase=phase,
        receipt_authorized=receipt_authorized,
    )


def remove_file(
    path: Path, *, phase: str, receipt_authorized: bool
) -> dict[str, Any] | None:
    return remove_with_retry(
        path,
        lambda target: target.unlink(),
        phase=phase,
        receipt_authorized=receipt_authorized,
    )


def remove_runtime_payload(root: Path, worktree: Path) -> dict[str, Any] | None:
    state = lane_state(root, worktree.name)
    manifest = lane_manifest(root, worktree.name)
    if not state.is_dir():
        return None
    try:
        children = list(state.iterdir())
    except OSError as error:
        return failure_evidence("lane runtime enumeration", state, error, 0)
    for child in children:
        if child == manifest:
            continue
        try:
            if is_reparse_point(child):
                return {
                    "phase": "lane runtime cleanup",
                    "path": str(child),
                    "error": "runtime payload contains a reparse point",
                    "errno": None,
                    "winerror": None,
                    "retry_count": 0,
                }
        except OSError as error:
            return failure_evidence("lane runtime inspection", child, error, 0)
        if child.is_dir():
            failure = remove_tree(
                child,
                phase="lane runtime cleanup",
                receipt_authorized=True,
            )
        else:
            failure = remove_file(
                child,
                phase="lane runtime cleanup",
                receipt_authorized=True,
            )
        if failure:
            return failure
    return None


def finish_lane_cleanup(root: Path, worktree: Path) -> dict[str, Any] | None:
    state = lane_state(root, worktree.name)
    receipt = cleanup_receipt(root, worktree.name)
    if path_present(state):
        failure = remove_tree(
            state,
            phase="lane state cleanup",
            receipt_authorized=receipt.is_file(),
        )
        if failure:
            return failure
    failure = remove_file(
        receipt,
        phase="cleanup receipt removal",
        receipt_authorized=True,
    )
    if failure:
        return failure
    return None



def remove_worktree(repo: Path, worktree: Path) -> tuple[bool, dict[str, Any]]:
    result = git(repo, "worktree", "remove", str(worktree), check=False)
    try:
        registered = worktree in registered_worktrees(repo)
        present = path_present(worktree)
    except (LaneError, OSError):
        registered = None
        present = True
    evidence = {
        "phase": "worktree removal",
        "path": str(worktree),
        "error": (
            command_error(result)
            if result.returncode != 0
            else "worktree removal read-back incomplete"
        ),
        "errno": None,
        "winerror": None,
        "retry_count": 0,
        "worktree_state": (
            "registered" if registered is True else "unregistered" if registered is False else "uncertain"
        ),
        "path_state": "present" if present else "missing",
    }
    return registered is False and not present, evidence


def rollback_created_lane(
    repo: Path, root: Path, worktree: Path, base: str, name: str
) -> str | None:
    head = git(worktree, "rev-parse", "HEAD", check=False)
    status = git(worktree, "status", "--porcelain", check=False)
    ignored, ignored_error = ignored_entries(worktree)
    if head.returncode != 0 or status.returncode != 0 or ignored_error:
        return "new lane preserved because rollback state is uncertain"
    if head.stdout.strip() != base or status.stdout.strip() or ignored:
        return "new lane preserved because rollback is not exact-base and clean"

    state = lane_state(root, name)
    removed, evidence = remove_worktree(repo, worktree)
    if not removed:
        return (
            "new lane preserved because worktree removal failed: "
            f"{evidence['error']}; lane state "
            f"{'preserved' if state.exists() else 'absent'}; worktree "
            f"{evidence['worktree_state']}; path {evidence['path_state']}"
        )
    if path_present(state):
        failure = remove_tree(
            state, phase="rollback state cleanup", receipt_authorized=False
        )
        if failure:
            return (
                "new lane worktree removed but state cleanup failed: "
                f"{failure['error']}"
            )
    return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Replace helper-owned metadata without exposing a partially written document."""
    if path_present(path) and is_reparse_point(path):
        raise LaneError(f"metadata is a reparse point: {path}")
    temporary = path.with_name(f"{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def run_inventory(
    repo: Path, root: Path, name: str, *, create: bool = False
) -> tuple[Path, dict[str, Any]]:
    if not LANE_NAME.fullmatch(name):
        raise LaneError("invalid run name")
    directory = root / ".runs"
    if path_present(directory) and is_reparse_point(directory):
        raise LaneError("run inventory directory is a reparse point")
    if create:
        directory.mkdir(exist_ok=True)
    path = directory / f"{name}.json"
    expected = {"schema_version": 1, "repository": str(repo), "root": str(root), "run": name}
    if not path_present(path):
        if not create:
            raise LaneError(f"run inventory is missing: {path}")
        return path, {**expected, "lanes": {}}
    if is_reparse_point(path):
        raise LaneError("run inventory is a reparse point")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise LaneError(f"run inventory is unreadable: {path}") from error
    if (not isinstance(payload, dict)
            or any(payload.get(key) != value for key, value in expected.items())
            or not isinstance(payload.get("lanes"), dict)):
        raise LaneError("run inventory does not match this repository and run")
    for lane, item in payload["lanes"].items():
        if (not LANE_NAME.fullmatch(lane) or not isinstance(item, dict)
                or item.get("worktree") != str(root / lane)
                or not isinstance(item.get("base"), str)
                or not COMMIT_ID.fullmatch(item["base"])
                or item.get("state") not in {"preparing", "prepared", "cleaned"}):
            raise LaneError("run inventory contains invalid lane evidence")
        if item["state"] == "cleaned" and not all(
            isinstance(item.get(key), str) and COMMIT_ID.fullmatch(item[key])
            for key in ("lane_head", "integration_head")
        ):
            raise LaneError("run inventory contains invalid completion evidence")
    return path, payload


def select_lanes(args: argparse.Namespace, repo: Path, root: Path, values: list[str]) -> list[Path]:
    name = getattr(args, "run", None)
    if not name:
        return validate_completed(root, values)
    _, inventory = run_inventory(repo, root, name)
    owned = [Path(item["worktree"]) for item in inventory["lanes"].values()]
    selected = validate_completed(root, values) if values else owned
    if any(lane not in owned for lane in selected):
        raise LaneError("selected lane is not owned by the named run")
    return selected


def run_ownership_blocker(args: argparse.Namespace, snapshot: dict[str, Any]) -> dict[str, str] | None:
    manifest = snapshot["manifest"]
    if manifest and manifest.get("run") != getattr(args, "run", None):
        return {"reason": "lane run ownership does not match; supply its --run"}
    return None


def mark_run_cleaned(args: argparse.Namespace, repo: Path, root: Path, lane: Path,
                     lane_head: str, integration_head: str) -> None:
    if not getattr(args, "run", None):
        return
    path, inventory = run_inventory(repo, root, args.run)
    inventory["lanes"][lane.name].update(
        state="cleaned", lane_head=lane_head, integration_head=integration_head
    )
    write_json(path, inventory)


def completed_in_run(args: argparse.Namespace, repo: Path, root: Path, lane: Path,
                     repo_head: str) -> bool:
    if not getattr(args, "run", None):
        return False
    _, inventory = run_inventory(repo, root, args.run)
    item = inventory["lanes"][lane.name]
    return (
        item["state"] == "cleaned"
        and not any(path_present(path) for path in (
            lane, lane_state(root, lane.name), cleanup_receipt(root, lane.name)
        ))
        and integration_state(repo, item["lane_head"], repo_head) is True
    )


def prepare(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=True)
    if not LANE_NAME.fullmatch(args.name):
        raise LaneError("--name must contain only letters, digits, dot, dash, or underscore")
    base = resolve_base(repo, args.base)
    worktree = lexical_absolute(root / args.name)
    if worktree.parent != root:
        raise LaneError("worktree path escapes the configured root")

    registered = registered_worktrees(repo)
    reused = worktree in registered
    receipt = cleanup_receipt(root, args.name)
    state = lane_state(root, args.name)
    if path_present(receipt):
        raise LaneError(f"lane has pending cleanup: {receipt}")
    if path_present(worktree) and not reused:
        raise LaneError(f"target exists but is not a registered worktree: {worktree}")
    if path_present(worktree) and is_reparse_point(worktree):
        raise LaneError(f"worktree path is a reparse point: {worktree}")
    if not path_present(worktree) and reused:
        raise LaneError(f"registered worktree path is missing: {worktree}")
    if path_present(state) and not reused:
        raise LaneError(f"lane has residual helper state: {state}")
    if reused:
        manifest, manifest_error = read_lane_manifest(repo, root, worktree)
        if manifest is None:
            raise LaneError(f"registered lane manifest is invalid: {manifest_error}")
        if manifest["base"] != base:
            raise LaneError(
                f"registered lane base {manifest['base']} does not match requested base {base}"
            )
        if manifest.get("run") != getattr(args, "run", None):
            raise LaneError("existing lane belongs to a different run; preserve its ownership")
        for key in (
            "runtime_root",
            "temp_root",
            "cache_root",
            "pytest_basetemp",
            "pytest_cache",
        ):
            path = Path(manifest[key])
            if not path_present(path) or not path.is_dir() or is_reparse_point(path):
                raise LaneError(f"registered lane runtime is invalid: {path}")
    inventory_path = None
    if getattr(args, "run", None):
        inventory_path, inventory = run_inventory(repo, root, args.run, create=True)
        previous = inventory["lanes"].get(args.name)
        if previous and (previous["base"] != base or previous["state"] == "cleaned"):
            raise LaneError("run lane identity cannot be reused for a different candidate")
        inventory["lanes"][args.name] = {
            "worktree": str(worktree), "base": base, "state": "preparing",
        }
        write_json(inventory_path, inventory)
    if not reused:
        result = git(
            repo, "worktree", "add", "--detach", str(worktree), base, check=False
        )
        if result.returncode != 0:
            raise LaneError(f"worktree creation failed: {command_error(result)}")

    try:
        head = git(worktree, "rev-parse", "HEAD").stdout.strip()
        if head != base:
            raise LaneError(f"worktree HEAD {head} does not match requested base {base}")
        if git(worktree, "status", "--porcelain").stdout.strip():
            raise LaneError("worktree is not clean")
        runtime_root, temp_root, cache_root, pytest_basetemp, pytest_cache = (
            state_paths(root, args.name)
        )
        for path in (worktree, runtime_root, temp_root, cache_root, pytest_basetemp, pytest_cache):
            probe_directory(path)
        if git(worktree, "status", "--porcelain").stdout.strip():
            raise LaneError("worktree probe did not restore a clean checkout")
        ignored, ignored_error = ignored_entries(worktree)
        if ignored_error:
            raise LaneError(f"ignored artifact inspection failed: {ignored_error}")
        if ignored:
            raise LaneError(
                "worktree has ignored artifacts: " + ", ".join(ignored)
            )
        manifest = manifest_payload(
            repo,
            root,
            worktree,
            base,
            runtime_root,
            temp_root,
            cache_root,
            pytest_basetemp,
            pytest_cache,
        )
        if getattr(args, "run", None):
            manifest["run"] = args.run
        if not reused:
            write_lane_manifest(root, args.name, manifest)
        if inventory_path:
            inventory["lanes"][args.name]["state"] = "prepared"
            write_json(inventory_path, inventory)
        return 0, {"ok": True, "reused": reused, **manifest}
    except (LaneError, OSError) as error:
        if reused:
            raise
        rollback_error = rollback_created_lane(repo, root, worktree, base, args.name)
        if rollback_error:
            raise LaneError(f"{error}; {rollback_error}") from error
        raise LaneError(str(error)) from error



def residual_identity_check(
    worktree: Path, receipt: dict[str, Any]
) -> tuple[bool, str | None]:
    if not path_present(worktree):
        return True, None
    try:
        if tree_has_reparse_point(worktree):
            return False, "unregistered residual path contains a reparse point"
        expected = receipt.get("worktree_identity")
        if expected is None:
            return False, "cleanup receipt lacks worktree identity for residual path"
        observed = path_identity(worktree)
        if observed is None:
            return False, "residual path identity is unavailable"
        if observed != expected:
            return False, "cleanup receipt worktree identity does not match residual path"
    except OSError as error:
        return False, f"unregistered residual path inspection failed: {error}"
    return True, None


def recover_unregistered_lane(
    repo: Path, root: Path, worktree: Path, repo_head: str,
    args: argparse.Namespace | None = None,
) -> tuple[bool, str | None]:
    snapshot = observe_lane(
        repo,
        root,
        worktree,
        repo_head,
        registered=False,
    )
    if snapshot["command_active"]:
        return False, "lane command active or interrupted; establish process quiescence"
    if args is not None and (blocker := run_ownership_blocker(args, snapshot)):
        return False, blocker["reason"]
    if snapshot["receipt"] is None:
        return False, snapshot["receipt_error"]
    if snapshot["integrated"] is False:
        return False, "cleanup receipt commit is no longer integrated"
    if snapshot["integrated"] is not True:
        return False, "cleanup receipt integration is uncertain"
    if not snapshot["residual_identity_ok"]:
        return False, snapshot["residual_identity_error"]
    if git(repo, "rev-parse", "HEAD").stdout.strip() != repo_head:
        return False, "repository HEAD changed before residual cleanup"

    if snapshot["present"] is True:
        failure = remove_tree(
            worktree,
            phase="unregistered residual path cleanup",
            receipt_authorized=True,
        )
        if failure:
            return False, json.dumps(failure, sort_keys=True)

    if args is not None:
        mark_run_cleaned(args, repo, root, worktree, snapshot["receipt"]["lane_head"], repo_head)
    failure = finish_lane_cleanup(root, worktree)
    if failure:
        return False, json.dumps(failure, sort_keys=True)
    return True, None


def validate_completed(root: Path, values: list[str]) -> list[Path]:
    paths = [lexical_absolute(value) for value in values]
    if len(paths) != len(set(paths)):
        raise LaneError("--completed contains a duplicate worktree")
    for worktree in paths:
        if not contained(worktree, root):
            raise LaneError(f"completed worktree is outside the configured root: {worktree}")
        if worktree.parent != root:
            raise LaneError(
                f"completed worktree is not a direct child of the configured root: {worktree}"
            )
        if not LANE_NAME.fullmatch(worktree.name):
            raise LaneError(
                f"completed worktree name does not match prepare lane naming: {worktree}"
            )
    return paths


def validate_lane(root: Path, value: str) -> Path:
    lanes = validate_completed(root, [value])
    return lanes[0]



def integration_state(repo: Path, commit: str | None, repo_head: str) -> bool | None:
    if not commit:
        return None
    result = git(
        repo,
        "merge-base",
        "--is-ancestor",
        commit,
        repo_head,
        check=False,
    )
    return True if result.returncode == 0 else False if result.returncode == 1 else None


def directory_inventory(path: Path) -> dict[str, Any]:
    try:
        exists = path_present(path)
        reparse = exists and is_reparse_point(path)
        return {
            "path": str(path),
            "exists": exists,
            "directory": exists and path.is_dir() and not reparse,
            "error": "runtime path is a reparse point" if reparse else None,
        }
    except OSError as error:
        return {
            "path": str(path),
            "exists": None,
            "directory": None,
            "error": str(error),
        }


def runtime_inventory(manifest: dict[str, Any] | None) -> tuple[dict[str, Any], bool]:
    if manifest is None:
        return {}, False
    runtime = {
        key: directory_inventory(Path(manifest[key]))
        for key in (
            "runtime_root",
            "temp_root",
            "cache_root",
            "pytest_basetemp",
            "pytest_cache",
        )
    }
    valid = all(
        item["exists"] and item["directory"] and item["error"] is None
        for item in runtime.values()
    )
    return runtime, valid


def observe_lane(
    repo: Path,
    root: Path,
    worktree: Path,
    repo_head: str,
    *,
    registered: bool | None = None,
) -> dict[str, Any]:
    if registered is None:
        registered = worktree in registered_worktrees(repo)

    manifest, manifest_error = read_lane_manifest(repo, root, worktree)
    receipt, receipt_error = read_cleanup_receipt(repo, root, worktree)
    runtime, runtime_valid = runtime_inventory(manifest)

    try:
        present = path_present(worktree)
        path_error = None
    except OSError as error:
        present = None
        path_error = str(error)

    if present and path_error is None:
        try:
            if is_reparse_point(worktree):
                path_error = "worktree path is a reparse point"
        except OSError as error:
            path_error = str(error)

    lane_head: str | None = None
    clean: bool | None = None
    status_error: str | None = None
    ignored: list[str] | None = None
    ignored_error: str | None = None
    if registered and present and path_error is None:
        head = git(worktree, "rev-parse", "HEAD", check=False)
        status = git(worktree, "status", "--porcelain", check=False)
        if head.returncode == 0 and status.returncode == 0:
            lane_head = head.stdout.strip()
            clean = not status.stdout.strip()
        else:
            status_error = command_error(head if head.returncode else status)
        ignored, ignored_error = ignored_entries(worktree)

    integrated = integration_state(repo, lane_head, repo_head)
    residual_identity_ok = False
    residual_identity_error: str | None = None
    if not registered and receipt is not None:
        integrated = integration_state(repo, receipt["lane_head"], repo_head)
        residual_identity_ok, residual_identity_error = residual_identity_check(
            worktree, receipt
        )

    mechanically_clean = (
        registered
        and present is True
        and clean is True
        and path_error is None
        and status_error is None
        and ignored_error is None
        and ignored == []
    )
    receipt_state = (
        "valid"
        if receipt is not None
        else "absent"
        if receipt_error == "cleanup receipt is missing"
        else "invalid"
    )
    command_active = path_present(lane_state(root, worktree.name) / "active-command.json")
    snapshot = {
        "registered": registered,
        "present": present,
        "path_error": path_error,
        "manifest": manifest,
        "manifest_error": manifest_error,
        "receipt": receipt,
        "receipt_error": receipt_error,
        "receipt_state": receipt_state,
        "command_active": command_active,
        "lane_head": lane_head,
        "clean": clean,
        "status_error": status_error,
        "ignored_entries": ignored,
        "ignored_error": ignored_error,
        "integrated": integrated,
        "runtime": runtime,
        "runtime_valid": runtime_valid,
        "residual_identity_ok": residual_identity_ok,
        "residual_identity_error": residual_identity_error,
        "resume_or_land_eligible": (
            mechanically_clean
            and manifest is not None
            and receipt_state == "absent"
            and runtime_valid
            and not command_active
        ),
    }
    snapshot["cleanup_eligible"] = (
        cleanup_blocker(snapshot) is None if registered else (
            receipt is not None and integrated is True and residual_identity_ok
            and not command_active
        )
    )
    return snapshot


def cleanup_blocker(snapshot: dict[str, Any]) -> dict[str, Any] | None:
    if snapshot.get("command_active"):
        return {"reason": "lane command active or interrupted; establish process quiescence"}
    if snapshot["receipt_state"] == "invalid":
        return {
            "reason": "cleanup receipt invalid",
            "error": snapshot["receipt_error"],
        }
    if (
        snapshot["present"] is not True
        or snapshot["path_error"]
        or snapshot["status_error"]
        or snapshot["ignored_error"]
        or snapshot["lane_head"] is None
        or snapshot["clean"] is None
    ):
        return {
            "reason": "uncertain",
            "error": (
                snapshot["path_error"]
                or snapshot["status_error"]
                or snapshot["ignored_error"]
            ),
        }
    if snapshot["clean"] is not True:
        return {"reason": "not clean"}
    if snapshot["ignored_entries"]:
        return {
            "reason": "ignored artifacts present",
            "ignored_entries": snapshot["ignored_entries"],
        }
    if snapshot["integrated"] is False:
        return {"reason": "not integrated"}
    if snapshot["integrated"] is not True:
        return {"reason": "uncertain"}
    if snapshot["manifest"] is None:
        return {
            "reason": "lane manifest invalid",
            "error": str(snapshot["manifest_error"]),
        }
    return None


def inspect_lane(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    if not root.is_dir():
        raise LaneError(f"worktree root does not exist: {root}")
    worktree = validate_lane(root, args.lane)
    repo_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    snapshot = observe_lane(repo, root, worktree, repo_head)

    ok = (
        snapshot["manifest"] is not None
        and snapshot["path_error"] is None
        and snapshot["status_error"] is None
        and (not snapshot["registered"] or snapshot["ignored_error"] is None)
    )
    packet = {
        "ok": ok,
        "worktree": str(worktree),
        "repository_head": repo_head,
        "manifest": {
            "valid": snapshot["manifest"] is not None,
            "schema_version": (
                snapshot["manifest"].get("schema_version")
                if snapshot["manifest"]
                else None
            ),
            "error": snapshot["manifest_error"],
        },
        "registered": snapshot["registered"],
        "path_state": (
            "present"
            if snapshot["present"] is True
            else "missing"
            if snapshot["present"] is False
            else "uncertain"
        ),
        "lane_head": snapshot["lane_head"],
        "clean": snapshot["clean"],
        "integrated": snapshot["integrated"],
        "status_error": snapshot["status_error"],
        "path_error": snapshot["path_error"],
        "ignored_entries": snapshot["ignored_entries"] or [],
        "ignored_error": snapshot["ignored_error"],
        "runtime": snapshot["runtime"],
        "readiness": readiness_record(root, worktree),
        "cleanup_receipt": {
            "state": snapshot["receipt_state"],
            "error": snapshot["receipt_error"],
        },
        "residual_identity": {
            "matches": snapshot["residual_identity_ok"],
            "error": snapshot["residual_identity_error"],
        },
        "mechanical": {
            "resume_or_land_eligible": snapshot["resume_or_land_eligible"],
            "cleanup_eligible": snapshot["cleanup_eligible"],
            "actor_quiescence_unverified": True,
            "command_active_or_interrupted": snapshot["command_active"],
        },
    }
    return (0 if ok else 1), packet


def cleanup(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    completed = select_lanes(args, repo, root, args.completed)
    if completed and not root.is_dir():
        raise LaneError(f"worktree root does not exist: {root}")

    repo_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    expected_head = getattr(args, "integration_head", None)
    if not expected_head or not COMMIT_ID.fullmatch(expected_head):
        raise LaneError("cleanup requires --integration-head with the proved full commit ID")
    if repo_head != expected_head:
        raise LaneError("repository HEAD does not match the proved integration HEAD")
    registered = registered_worktrees(repo)
    removed: list[str] = []
    preserved: list[dict[str, Any]] = []

    for worktree in completed:
        if git(repo, "rev-parse", "HEAD").stdout.strip() != expected_head:
            preserved.append({"worktree": str(worktree), "reason": "integration HEAD changed"})
            continue
        if worktree not in registered and completed_in_run(args, repo, root, worktree, repo_head):
            removed.append(str(worktree))
            continue
        if worktree not in registered:
            recovered, reason = recover_unregistered_lane(repo, root, worktree, repo_head, args)
            if recovered:
                removed.append(str(worktree))
            else:
                preserved.append({"worktree": str(worktree), "reason": str(reason)})
            continue

        snapshot = observe_lane(
            repo, root, worktree, repo_head, registered=True
        )
        blocker = cleanup_blocker(snapshot)
        blocker = blocker or run_ownership_blocker(args, snapshot)
        if blocker:
            preserved.append({"worktree": str(worktree), **blocker})
            continue

        state = lane_state(root, worktree.name)
        try:
            write_cleanup_receipt(
                repo,
                root,
                worktree,
                snapshot["lane_head"],
                repo_head,
            )
            receipt, receipt_error = read_cleanup_receipt(repo, root, worktree)
            if receipt is None:
                raise LaneError(str(receipt_error))
        except (LaneError, OSError) as error:
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "cleanup receipt failed",
                    "error": str(error),
                }
            )
            continue

        if git(repo, "rev-parse", "HEAD").stdout.strip() != expected_head:
            preserved.append({"worktree": str(worktree), "reason": "cleanup identity changed"})
            continue
        payload_failure = remove_runtime_payload(root, worktree)
        if payload_failure:
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "runtime cleanup incomplete",
                    "lane_state": "preserved" if path_present(state) else "absent",
                    "worktree_state": "registered",
                    "path_state": "present",
                    **payload_failure,
                }
            )
            continue

        current_head_result = git(repo, "rev-parse", "HEAD", check=False)
        current_head = (
            current_head_result.stdout.strip()
            if current_head_result.returncode == 0
            else None
        )
        current_registered = worktree in registered_worktrees(repo)
        current = (
            observe_lane(
                repo,
                root,
                worktree,
                current_head or repo_head,
                registered=current_registered,
            )
            if current_head
            else None
        )
        try:
            identity_matches = (
                current is not None
                and current["present"] is True
                and path_identity(worktree) == receipt["worktree_identity"]
            )
        except (LaneError, OSError):
            identity_matches = False

        if (
            current_head != repo_head
            or current is None
            or cleanup_blocker(current) is not None
            or current["registered"] is not True
            or current["lane_head"] != snapshot["lane_head"]
            or not identity_matches
        ):
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "cleanup identity changed",
                    "lane_state": "preserved" if path_present(state) else "absent",
                    "worktree_state": (
                        "registered" if current_registered else "unregistered"
                    ),
                    "path_state": (
                        "present"
                        if current and current["present"] is True
                        else "missing"
                        if current and current["present"] is False
                        else "uncertain"
                    ),
                }
            )
            continue

        worktree_removed, evidence = remove_worktree(repo, worktree)
        if not worktree_removed:
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "remove failed",
                    "lane_state": "preserved" if path_present(state) else "absent",
                    **evidence,
                }
            )
            continue

        mark_run_cleaned(args, repo, root, worktree, snapshot["lane_head"], repo_head)
        failure = finish_lane_cleanup(root, worktree)
        if failure:
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "cleanup incomplete",
                    "lane_state": "preserved" if path_present(state) else "absent",
                    "worktree_state": "unregistered",
                    "path_state": "missing",
                    **failure,
                }
            )
            continue
        removed.append(str(worktree))

    packet = {"ok": not preserved, "removed": removed, "preserved": preserved}
    if preserved:
        packet["error"] = "cleanup incomplete"
        return 1, packet
    return 0, packet


def verify_cleanup(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    if not args.lane and not getattr(args, "run", None):
        raise LaneError("verify-cleanup requires at least one --lane")
    if args.lane and getattr(args, "run", None):
        raise LaneError("verify-cleanup --run verifies the entire inventory; omit --lane")
    lanes = select_lanes(args, repo, root, args.lane)
    if not lanes:
        raise LaneError("run inventory contains no lanes")
    if not COMMIT_ID.fullmatch(args.integration_head):
        raise LaneError("--integration-head must be a full commit ID")

    expected_head = resolve_base(repo, args.integration_head)
    initial_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    head_matches = initial_head == expected_head
    registered = registered_worktrees(repo)
    lane_results: list[dict[str, Any]] = []
    cleanup_paths: list[str] = []
    retry_paths: list[str] = []

    for worktree in lanes:
        state_exists = path_present(lane_state(root, worktree.name))
        receipt_exists = path_present(cleanup_receipt(root, worktree.name))
        snapshot = observe_lane(
            repo,
            root,
            worktree,
            initial_head,
            registered=worktree in registered,
        )
        finish_clean = (
            not snapshot["registered"]
            and snapshot["present"] is False
            and not state_exists
            and not receipt_exists
        )
        if finish_clean and getattr(args, "run", None):
            finish_clean = completed_in_run(args, repo, root, worktree, initial_head)

        action = "none" if finish_clean else "preserve-and-report"
        reason: str | None = None
        if not finish_clean and not head_matches:
            reason = "repository HEAD does not match the proved integration HEAD"
        elif not finish_clean and snapshot["registered"]:
            blocker = cleanup_blocker(snapshot) or run_ownership_blocker(args, snapshot)
            if blocker is None:
                action = "cleanup"
                cleanup_paths.append(str(worktree))
            elif blocker["reason"] == "ignored artifacts present":
                reason = "registered lane has ignored artifacts"
            else:
                reason = blocker.get("error") or blocker["reason"]
        elif not finish_clean:
            if snapshot["cleanup_eligible"] and not run_ownership_blocker(args, snapshot):
                action = "retry-cleanup"
                retry_paths.append(str(worktree))
            else:
                reason = (
                    snapshot["receipt_error"]
                    or snapshot["residual_identity_error"]
                    or "residual lane is not cleanup eligible"
                )

        lane_results.append(
            {
                "worktree": str(worktree),
                "registered": snapshot["registered"],
                "path_state": (
                    "present"
                    if snapshot["present"] is True
                    else "missing"
                    if snapshot["present"] is False
                    else "uncertain"
                ),
                "lane_state": "present" if state_exists else "absent",
                "cleanup_receipt": "present" if receipt_exists else "absent",
                "required_action": action,
                "finish_clean": finish_clean,
                "reason": reason,
            }
        )

    final_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    head_matches = head_matches and final_head == expected_head
    if not head_matches:
        cleanup_paths.clear()
        retry_paths.clear()
        for item in lane_results:
            if not item["finish_clean"]:
                item["required_action"] = "preserve-and-report"
                item["reason"] = (
                    "repository HEAD does not match the proved integration HEAD"
                )

    finish_clean = head_matches and all(item["finish_clean"] for item in lane_results)
    packet = {
        "ok": finish_clean,
        "finish_clean": finish_clean,
        "repository_head": final_head,
        "repository_head_initial": initial_head,
        "integration_head": expected_head,
        "head_matches": head_matches,
        "lanes": lane_results,
        "cleanup": cleanup_paths,
        "retry_cleanup": retry_paths,
    }
    if not finish_clean:
        packet["error"] = "cleanup verification failed"
    return (0 if finish_clean else 1), packet


def status_run(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    path, inventory = run_inventory(repo, root, args.run)
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    registered = registered_worktrees(repo)
    results = []
    for item in inventory["lanes"].values():
        lane = Path(item["worktree"])
        try:
            snapshot = observe_lane(repo, root, lane, head, registered=lane in registered)
            ownership_error = run_ownership_blocker(args, snapshot)
            if ownership_error:
                results.append({**item, "error": ownership_error["reason"]})
                continue
            results.append({
                **item, "registered": snapshot["registered"], "present": snapshot["present"],
                "lane_head": snapshot["lane_head"], "clean": snapshot["clean"],
                "integrated": snapshot["integrated"],
                "resume_or_land_eligible": snapshot["resume_or_land_eligible"],
                "cleanup_eligible": snapshot["cleanup_eligible"],
                "command_active_or_interrupted": snapshot["command_active"],
                "finish_clean": lane not in registered and completed_in_run(args, repo, root, lane, head),
                "readiness": readiness_record(root, lane),
            })
        except (LaneError, OSError) as error:
            results.append({**item, "error": str(error)})
    final_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    ok = final_head == head and not any("error" in item for item in results)
    return (0 if ok else 1), {
        "ok": ok, "run": args.run, "inventory": str(path), "lanes": results,
        "repository_head": final_head, "head_changed": final_head != head,
        "actor_quiescence_unverified": True,
    }


def readiness_record(root: Path, lane: Path) -> dict[str, Any]:
    path = lane_state(root, lane.name) / "readiness.json"
    try:
        if not path_present(path):
            return {"state": "not-recorded"}
        if is_reparse_point(path):
            return {"state": "unreadable"}
        result = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(result, dict):
            return {"state": "unreadable"}
        return {"state": "recorded", "last_result": result, "freshness_unverified": True}
    except (OSError, ValueError):
        return {"state": "unreadable"}


def execution_lane(args: argparse.Namespace) -> tuple[Path, Path, Path, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    lane = validate_lane(root, args.lane)
    snapshot = observe_lane(repo, root, lane, git(repo, "rev-parse", "HEAD").stdout.strip())
    if (not snapshot["registered"] or snapshot["present"] is not True
            or snapshot["path_error"] or snapshot["status_error"]
            or snapshot["manifest"] is None or not snapshot["runtime_valid"]
            or snapshot["receipt_state"] != "absent" or snapshot["command_active"]):
        raise LaneError("lane cannot execute commands: inspect its lifecycle/runtime state first")
    return repo, root, lane, snapshot["manifest"]


def assignments(values: list[str]) -> dict[str, str]:
    result = {}
    for value in values:
        key, separator, content = value.partition("=")
        if os.name == "nt":
            key = key.upper()
        if not separator or key in result:
            raise LaneError("expected distinct KEY=value assignments")
        result[key] = content
    return result


def expand_argument(value: str, manifest: dict[str, Any]) -> str:
    for key in ("worktree", "runtime_root", "temp_root", "cache_root", "pytest_basetemp", "pytest_cache"):
        value = value.replace(f"@{key}@", manifest[key])
    return value


def execution_profile(args: argparse.Namespace, manifest: dict[str, Any]) -> dict[str, Any]:
    profile: dict[str, Any] = {}
    if args.profile:
        try:
            profile = json.loads(Path(args.profile).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as error:
            raise LaneError(f"cannot read execution profile: {error}") from error
    allowed = {"env", "inputs", "outputs", "setup", "checks", "timeout"}
    if not isinstance(profile, dict) or set(profile) - allowed:
        raise LaneError("execution profile has unknown fields or is not an object")
    for field in ("env", "inputs", "outputs"):
        values = profile.get(field, {})
        if not isinstance(values, dict):
            raise LaneError(f"profile {field} must be a KEY=value object")
        if os.name == "nt":
            values = {key.upper(): value for key, value in values.items()}
        values = {**values, **assignments(getattr(args, field))}
        if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key)
               or not isinstance(value, str) or "\0" in value for key, value in values.items()):
            raise LaneError(f"invalid profile {field} assignment")
        profile[field] = values
    names = [key.upper() for field in ("env", "inputs", "outputs") for key in profile[field]]
    if len(names) != len(set(names)) or {"LANE_WORKTREE", "LANE_RUNTIME"} & set(names):
        raise LaneError("profile environment keys overlap or replace lane identity")
    for field in ("setup", "checks"):
        commands = profile.get(field, [])
        if not isinstance(commands, list):
            raise LaneError(f"profile {field} must be a list of argument arrays")
        try:
            commands = commands + [json.loads(value) for value in getattr(args, field, [])]
        except ValueError as error:
            raise LaneError(f"invalid {field} command JSON") from error
        if any(not isinstance(command, list) or not command
               or any(not isinstance(value, str) or "\0" in value for value in command)
               for command in commands):
            raise LaneError(f"profile {field} commands must be nonempty string arrays")
        profile[field] = commands
    timeout = args.timeout if args.timeout is not None else profile.get("timeout", 300)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise LaneError("timeout must be a finite positive number of seconds")
    profile["timeout"] = timeout

    for field in ("env", "inputs", "outputs"):
        profile[field] = {key: expand_argument(value, manifest) for key, value in profile[field].items()}
    for field in ("setup", "checks"):
        profile[field] = [[expand_argument(value, manifest) for value in command] for command in profile[field]]
    return profile


def runtime_path(path: Path, runtime: Path) -> Path:
    path = lexical_absolute(path)
    if not contained(path, runtime):
        raise LaneError(f"output must be inside this lane's disposable runtime: {path}")
    if path.relative_to(runtime).parts[0].lower() in {
        "lane.json", "active-command.json", "last-command.json", "readiness.json",
    }:
        raise LaneError("output overlaps helper metadata")
    current = path
    while current != runtime:
        if path_present(current) and is_reparse_point(current):
            raise LaneError(f"output path is redirected: {current}")
        current = current.parent
    return path


def execution_environment(manifest: dict[str, Any], profile: dict[str, Any]) -> dict[str, str]:
    lane = Path(manifest["worktree"])
    runtime = Path(manifest["runtime_root"])
    env = dict(os.environ)
    env.update({
        "TMP": manifest["temp_root"], "TEMP": manifest["temp_root"], "TMPDIR": manifest["temp_root"],
        "XDG_CACHE_HOME": manifest["cache_root"], "UV_CACHE_DIR": str(runtime / "cache" / "uv"),
        "PYTHONPYCACHEPREFIX": str(runtime / "cache" / "pycache"),
        "LANE_WORKTREE": str(lane), "LANE_RUNTIME": str(runtime),
    })
    inputs = {}
    for key, value in profile["inputs"].items():
        path = (lane / value).resolve()
        if path == runtime or contained(path, runtime) or contained(runtime, path):
            raise LaneError(f"shared input overlaps disposable runtime: {path}")
        if path.is_file():
            with path.open("rb") as handle:
                handle.read(1)
        elif path.is_dir():
            with os.scandir(path) as entries:
                next(entries, None)
        else:
            raise LaneError(f"input is not an accessible file or directory: {path}")
        inputs[key] = str(path)
    outputs = {}
    for key, value in profile["outputs"].items():
        path = runtime_path(runtime / value, runtime)
        if any(path == Path(item) or contained(path, Path(item)) or contained(Path(item), path)
               for item in inputs.values()):
            raise LaneError("shared inputs and writable outputs overlap")
        path.mkdir(parents=True, exist_ok=True)
        probe_directory(path)
        outputs[key] = str(path)
    env.update(profile["env"])
    env.update(inputs)
    env.update(outputs)
    return {key.upper(): value for key, value in env.items()} if os.name == "nt" else env


class WindowsJob:
    """Own the launched command tree without process discovery or PID-based killing."""

    def __init__(self) -> None:
        import ctypes
        from ctypes import wintypes

        class BasicLimits(ctypes.Structure):
            _fields_ = [
                ("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                ("flags", wintypes.DWORD), ("minimum_working_set", ctypes.c_size_t),
                ("maximum_working_set", ctypes.c_size_t), ("active_process_limit", wintypes.DWORD),
                ("affinity", ctypes.c_size_t), ("priority_class", wintypes.DWORD),
                ("scheduling_class", wintypes.DWORD),
            ]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [("basic", BasicLimits), ("io_counters", ctypes.c_ulonglong * 6),
                        ("memory_limits", ctypes.c_size_t * 4)]

        self.ctypes = ctypes
        self.api = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, wintypes.LPCWSTR], wintypes.HANDLE),
            "SetInformationJobObject": ([wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD], wintypes.BOOL),
            "AssignProcessToJobObject": ([wintypes.HANDLE, wintypes.HANDLE], wintypes.BOOL),
            "TerminateJobObject": ([wintypes.HANDLE, wintypes.UINT], wintypes.BOOL),
            "CloseHandle": ([wintypes.HANDLE], wintypes.BOOL),
        }
        for name, (arguments, result) in signatures.items():
            method = getattr(self.api, name)
            method.argtypes, method.restype = arguments, result
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process: subprocess.Popen[bytes]) -> None:
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise self.ctypes.WinError(self.ctypes.get_last_error())

    def terminate(self) -> None:
        if not self.api.TerminateJobObject(self.handle, 124):
            raise self.ctypes.WinError(self.ctypes.get_last_error())

    def close(self) -> None:
        if self.handle:
            if not self.api.CloseHandle(self.handle):
                raise self.ctypes.WinError(self.ctypes.get_last_error())
            self.handle = None


def stop_command(process: subprocess.Popen[bytes], job: WindowsJob | None) -> None:
    """Stop only the process group/tree launched by this invocation."""
    if job is not None:
        job.terminate()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()
    process.wait(timeout=15)


def execute_command(manifest: dict[str, Any], command: list[str], env: dict[str, str],
                    timeout: float) -> dict[str, Any]:
    runtime = Path(manifest["runtime_root"])
    marker = runtime / "active-command.json"
    record = {"command": command, "cwd": manifest["worktree"], "state": "starting", "started_at": time.time()}
    # Exclusive creation rejects overlapping commands and preserves interrupted custody.
    with marker.open("x", encoding="utf-8") as handle:
        json.dump(record, handle)
    started = time.monotonic()
    process = None
    job = None
    reader = None
    tail = bytearray()
    total = 0
    timed_out = False
    stopped = True
    error = None
    try:
        launch = command
        if os.name == "nt":
            job = WindowsJob()
            # The wrapper waits for input, so no user command can start before job assignment.
            wrapper = "import json,subprocess,sys; args=json.loads(sys.stdin.buffer.readline()); sys.exit(subprocess.call(args,stdin=subprocess.DEVNULL))"
            launch = [sys.executable, "-c", wrapper]
        process = subprocess.Popen(
            launch, cwd=manifest["worktree"], env=env, stdin=subprocess.PIPE if job else subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            start_new_session=os.name != "nt",
            creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW) if os.name == "nt" else 0,
        )
        write_json(marker, {**record, "state": "running", "pid": process.pid})
        if job:
            job.assign(process)
            assert process.stdin is not None
            process.stdin.write(json.dumps(command).encode("utf-8") + b"\n")
            process.stdin.close()

        def drain() -> None:
            nonlocal total
            assert process is not None and process.stdout is not None
            while chunk := process.stdout.read(4096):
                total += len(chunk)
                tail.extend(chunk)
                del tail[:-16384]

        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            stop_command(process, job)
    except (OSError, subprocess.SubprocessError, KeyboardInterrupt) as failure:
        error = str(failure) or type(failure).__name__
    finally:
        if process is not None and process.poll() is None:
            try:
                stop_command(process, job)
            except (OSError, subprocess.SubprocessError) as failure:
                error = str(failure)
                stopped = False
        if job:
            try:
                job.close()
            except OSError as failure:
                error = str(failure)
                stopped = False
        if reader is not None:
            reader.join(timeout=2)
            stopped = stopped and not reader.is_alive()
        if process is not None and process.stdout is not None and stopped:
            process.stdout.close()
    result = {
        **record, "state": "finished" if stopped else "uncertain", "pid": process.pid if process else None,
        "ok": process is not None and process.returncode == 0 and not timed_out and not error and stopped,
        "returncode": process.returncode if process else None, "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic() - started, 3), "error": error,
        "output_tail": bytes(tail).decode("utf-8", errors="replace"), "output_truncated": total > 16384,
        "actor_quiescence_unverified": True,
    }
    write_json(runtime / "last-command.json", result)
    if stopped:
        marker.unlink()
    return result


def lane_command(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    _, _, lane, manifest = execution_lane(args)
    ready = args.operation == "ready"
    record = Path(manifest["runtime_root"]) / "readiness.json"
    result: dict[str, Any] = {"ok": False, "worktree": str(lane), "state": "checking", "commands": []}
    if ready:
        write_json(record, result)
    try:
        profile = execution_profile(args, manifest)
        if ready and not profile["checks"]:
            raise LaneError("ready requires at least one explicit health check (--check or profile checks)")
        command = getattr(args, "command", [])
        if command[:1] == ["--"]:
            command = command[1:]
        if not ready and not command:
            raise LaneError("exec requires a command after --")
        command = [expand_argument(value, manifest) for value in command]
        env = execution_environment(manifest, profile)
        result.update(
            head=git(lane, "rev-parse", "HEAD").stdout.strip(),
            profile_digest=hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest(),
            environment_keys=sorted(set(profile["env"]) | set(profile["inputs"]) | set(profile["outputs"])),
            inputs={key: env[key] for key in profile["inputs"]},
            outputs={key: env[key] for key in profile["outputs"]},
        )
        commands = (([] if args.checks_only else profile["setup"]) + profile["checks"]) if ready else [command]
        for command in commands:
            evidence = execute_command(manifest, command, env, profile["timeout"])
            result["commands"].append(evidence)
            if not evidence["ok"]:
                break
        result["ok"] = all(item["ok"] for item in result["commands"])
    except (LaneError, OSError) as error:
        result["error"] = str(error)
    result.update(state="passed" if result["ok"] else "failed", observed_at=time.time())
    if ready:
        write_json(record, result)
    return (0 if result["ok"] else 1), result


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    operations = value.add_subparsers(dest="operation", required=True)

    prepare_parser = operations.add_parser("prepare")
    prepare_parser.add_argument("--repo", required=True)
    prepare_parser.add_argument("--root", required=True)
    prepare_parser.add_argument("--base", required=True)
    prepare_parser.add_argument("--name", required=True)
    prepare_parser.add_argument("--run", help="optional named inventory for this delivery")

    cleanup_parser = operations.add_parser("cleanup")
    cleanup_parser.add_argument("--repo", required=True)
    cleanup_parser.add_argument("--root", required=True)
    cleanup_parser.add_argument("--completed", action="append", default=[])
    cleanup_parser.add_argument("--integration-head", required=True, help="proved full commit ID")
    cleanup_parser.add_argument("--run", help="select owned run lanes when --completed is omitted")

    inspect_parser = operations.add_parser("inspect")
    inspect_parser.add_argument("--repo", required=True)
    inspect_parser.add_argument("--root", required=True)
    inspect_parser.add_argument("--lane", required=True)

    verify_parser = operations.add_parser("verify-cleanup")
    verify_parser.add_argument("--repo", required=True)
    verify_parser.add_argument("--root", required=True)
    verify_parser.add_argument("--integration-head", required=True)
    verify_parser.add_argument("--lane", action="append", default=[])
    verify_parser.add_argument("--run", help="verify the complete named inventory")

    status_parser = operations.add_parser("status", help="inspect every lane in a named run")
    status_parser.add_argument("--repo", required=True)
    status_parser.add_argument("--root", required=True)
    status_parser.add_argument("--run", required=True)
    for operation in ("ready", "exec"):
        command_parser = operations.add_parser(operation, help="run explicit setup/checks" if operation == "ready" else "run a command in the lane environment")
        command_parser.add_argument("--repo", required=True)
        command_parser.add_argument("--root", required=True)
        command_parser.add_argument("--lane", required=True)
        command_parser.add_argument("--profile", help="optional JSON execution profile; never auto-discovered")
        command_parser.add_argument("--env", dest="env", action="append", default=[], metavar="KEY=value")
        command_parser.add_argument("--input", dest="inputs", action="append", default=[], metavar="KEY=path")
        command_parser.add_argument("--output", dest="outputs", action="append", default=[], metavar="KEY=runtime-relative-path")
        command_parser.add_argument("--timeout", type=float, help="per-command seconds (default 300)")
        if operation == "ready":
            command_parser.add_argument("--checks-only", action="store_true", help="reuse established setup and rerun health checks")
            command_parser.add_argument("--setup", dest="setup", action="append", default=[], help="JSON argument array; repeatable")
            command_parser.add_argument("--check", dest="checks", action="append", default=[], help="JSON argument array; repeatable")
        else:
            command_parser.add_argument("command", nargs=argparse.REMAINDER)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "prepare":
            code, packet = prepare(args)
        elif args.operation == "inspect":
            code, packet = inspect_lane(args)
        elif args.operation == "verify-cleanup":
            code, packet = verify_cleanup(args)
        elif args.operation == "status":
            code, packet = status_run(args)
        elif args.operation in {"ready", "exec"}:
            code, packet = lane_command(args)
        else:
            code, packet = cleanup(args)
    except (LaneError, OSError) as error:
        packet = {"ok": False, "error": str(error)}
        if args.operation == "prepare" and hasattr(args, "root") and hasattr(args, "name"):
            candidate = (Path(args.root).resolve() / args.name).resolve()
            if candidate.exists():
                packet["worktree"] = str(candidate)
        code = 1
    print(json.dumps(packet, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
