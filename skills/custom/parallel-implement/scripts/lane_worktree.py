"""Prepare, inspect, clean up, and verify concurrent-worker Git worktrees."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any


LANE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
COMMIT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
CLEANUP_RECEIPT_FORMAT = 2
LANE_SCHEMA_VERSION = 1
TRANSIENT_WINDOWS_ERRORS = {5, 32}
RETRY_DELAYS = (0.25, 0.5, 1.0, 2.0)


class LaneError(RuntimeError):
    """A lane operation could not complete safely."""


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
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
    result = git(repo, "worktree", "list", "--porcelain")
    return {
        Path(line.removeprefix("worktree ")).resolve()
        for line in result.stdout.splitlines()
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


def remove_tree(
    path: Path, *, phase: str, receipt_authorized: bool
) -> dict[str, Any] | None:
    for retry_count in range(len(RETRY_DELAYS) + 1):
        try:
            shutil.rmtree(path)
            return None
        except OSError as error:
            winerror = getattr(error, "winerror", None)
            if winerror not in TRANSIENT_WINDOWS_ERRORS or retry_count == len(RETRY_DELAYS):
                return failure_evidence(phase, path, error, retry_count)
            if receipt_authorized and winerror == 5:
                try:
                    clear_readonly_tree(path)
                except (LaneError, OSError) as clear_error:
                    if isinstance(clear_error, OSError):
                        return failure_evidence(
                            f"{phase}:clear-readonly", path, clear_error, retry_count
                        )
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


def remove_file(
    path: Path, *, phase: str, receipt_authorized: bool
) -> dict[str, Any] | None:
    for retry_count in range(len(RETRY_DELAYS) + 1):
        try:
            path.unlink()
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
                except (LaneError, OSError) as clear_error:
                    if isinstance(clear_error, OSError):
                        return failure_evidence(
                            f"{phase}:clear-readonly", path, clear_error, retry_count
                        )
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
        if not reused:
            write_lane_manifest(root, args.name, manifest)
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
    repo: Path, root: Path, worktree: Path, repo_head: str
) -> tuple[bool, str | None]:
    snapshot = observe_lane(
        repo,
        root,
        worktree,
        repo_head,
        registered=False,
    )
    if snapshot["receipt"] is None:
        return False, snapshot["receipt_error"]
    if snapshot["integrated"] is False:
        return False, "cleanup receipt commit is no longer integrated"
    if snapshot["integrated"] is not True:
        return False, "cleanup receipt integration is uncertain"
    if not snapshot["residual_identity_ok"]:
        return False, snapshot["residual_identity_error"]

    if snapshot["present"] is True:
        failure = remove_tree(
            worktree,
            phase="unregistered residual path cleanup",
            receipt_authorized=True,
        )
        if failure:
            return False, json.dumps(failure, sort_keys=True)

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
    return {
        "registered": registered,
        "present": present,
        "path_error": path_error,
        "manifest": manifest,
        "manifest_error": manifest_error,
        "receipt": receipt,
        "receipt_error": receipt_error,
        "receipt_state": receipt_state,
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
        ),
        "cleanup_eligible": (
            (mechanically_clean and manifest is not None and integrated is True)
            or (
                not registered
                and receipt is not None
                and integrated is True
                and residual_identity_ok
            )
        ),
    }


def cleanup_blocker(snapshot: dict[str, Any]) -> dict[str, Any] | None:
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
        },
    }
    return (0 if ok else 1), packet


def cleanup(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    completed = validate_completed(root, args.completed)
    if completed and not root.is_dir():
        raise LaneError(f"worktree root does not exist: {root}")

    repo_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    registered = registered_worktrees(repo)
    removed: list[str] = []
    preserved: list[dict[str, Any]] = []

    for worktree in completed:
        if worktree not in registered:
            recovered, reason = recover_unregistered_lane(repo, root, worktree, repo_head)
            if recovered:
                removed.append(str(worktree))
            else:
                preserved.append({"worktree": str(worktree), "reason": str(reason)})
            continue

        snapshot = observe_lane(
            repo, root, worktree, repo_head, registered=True
        )
        blocker = cleanup_blocker(snapshot)
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
    if not args.lane:
        raise LaneError("verify-cleanup requires at least one --lane")
    lanes = validate_completed(root, args.lane)
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

        action = "none" if finish_clean else "preserve-and-report"
        reason: str | None = None
        if not finish_clean and not head_matches:
            reason = "repository HEAD does not match the proved integration HEAD"
        elif not finish_clean and snapshot["registered"]:
            blocker = cleanup_blocker(snapshot)
            if blocker is None:
                action = "cleanup"
                cleanup_paths.append(str(worktree))
            elif blocker["reason"] == "ignored artifacts present":
                reason = "registered lane has ignored artifacts"
            else:
                reason = blocker.get("error") or blocker["reason"]
        elif not finish_clean:
            if snapshot["cleanup_eligible"]:
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


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    operations = value.add_subparsers(dest="operation", required=True)

    prepare_parser = operations.add_parser("prepare")
    prepare_parser.add_argument("--repo", required=True)
    prepare_parser.add_argument("--root", required=True)
    prepare_parser.add_argument("--base", required=True)
    prepare_parser.add_argument("--name", required=True)

    cleanup_parser = operations.add_parser("cleanup")
    cleanup_parser.add_argument("--repo", required=True)
    cleanup_parser.add_argument("--root", required=True)
    cleanup_parser.add_argument("--completed", action="append", default=[])

    inspect_parser = operations.add_parser("inspect")
    inspect_parser.add_argument("--repo", required=True)
    inspect_parser.add_argument("--root", required=True)
    inspect_parser.add_argument("--lane", required=True)

    verify_parser = operations.add_parser("verify-cleanup")
    verify_parser.add_argument("--repo", required=True)
    verify_parser.add_argument("--root", required=True)
    verify_parser.add_argument("--integration-head", required=True)
    verify_parser.add_argument("--lane", action="append", default=[])
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
