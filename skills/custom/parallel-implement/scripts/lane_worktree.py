"""Prepare and safely clean up concurrent-worker Git worktrees."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


LANE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")


class LaneError(RuntimeError):
    """A lane operation could not complete safely."""


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def command_error(result: subprocess.CompletedProcess[str]) -> str:
    return result.stderr.strip() or result.stdout.strip() or "command failed"


def git(
    checkout: Path, *args: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", str(checkout), *args]
    result = run(command)
    trust_error = f"{result.stdout}\n{result.stderr}".lower()
    if result.returncode != 0 and (
        "dubious ownership" in trust_error or "safe.directory" in trust_error
    ):
        result = run(
            [
                "git",
                "-c",
                f"safe.directory={checkout}",
                "-C",
                str(checkout),
                *args,
            ]
        )
    if check and result.returncode != 0:
        raise LaneError(command_error(result))
    return result


def contained(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return path != root


def repository_root(path: str) -> Path:
    requested = Path(path).resolve()
    if not requested.is_dir():
        raise LaneError(f"repository does not exist: {requested}")
    observed = Path(
        git(requested, "rev-parse", "--show-toplevel").stdout.strip()
    ).resolve()
    if observed != requested:
        raise LaneError(f"--repo must be the repository root: {observed}")
    return observed


def lane_root(path: str, repo: Path, *, create: bool) -> Path:
    root = Path(path).resolve()
    if root == repo or contained(root, repo):
        raise LaneError("worktree root must be outside the repository")
    if create:
        root.mkdir(parents=True, exist_ok=True)
    return root


def resolve_base(repo: Path, value: str) -> str:
    result = git(repo, "rev-parse", "--verify", f"{value}^{{commit}}")
    return result.stdout.strip()


def registered_worktrees(repo: Path) -> list[Path]:
    result = git(repo, "worktree", "list", "--porcelain")
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            paths.append(Path(line.removeprefix("worktree ")).resolve())
    return paths


def lane_state(root: Path, name: str) -> Path:
    state = (root / ".state" / name).resolve()
    if not contained(state, root):
        raise LaneError("lane state path escapes the configured root")
    return state


def state_paths(root: Path, name: str) -> tuple[Path, Path, Path, Path]:
    state = lane_state(root, name)
    temp_root = state / "tmp"
    pytest_basetemp = state / "pytest"
    pytest_cache = state / "cache"
    for path in (temp_root, pytest_basetemp, pytest_cache):
        path.mkdir(parents=True, exist_ok=True)
    return state, temp_root, pytest_basetemp, pytest_cache


def pytest_configured(worktree: Path) -> bool:
    pytest_ini = worktree / "pytest.ini"
    if pytest_ini.is_file():
        return True
    for relative, marker in (
        ("pyproject.toml", "[tool.pytest.ini_options]"),
        ("setup.cfg", "[tool:pytest]"),
        ("tox.ini", "[pytest]"),
    ):
        path = worktree / relative
        if path.is_file() and marker in path.read_text(encoding="utf-8", errors="replace"):
            return True
    tracked = git(worktree, "ls-files", "--", "*.py").stdout.splitlines()
    return any(
        Path(relative).name.startswith("test_")
        or Path(relative).name.endswith("_test.py")
        for relative in tracked
    )


def pytest_smoke(
    worktree: Path,
    temp_root: Path,
    pytest_basetemp: Path,
    pytest_cache: Path,
) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "TMP": str(temp_root),
            "TEMP": str(temp_root),
            "TMPDIR": str(temp_root),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-o",
        "addopts=",
        "--collect-only",
        "-q",
        f"--basetemp={pytest_basetemp}",
        "-o",
        f"cache_dir={pytest_cache}",
    ]
    result = run(command, cwd=worktree, env=environment)
    if result.returncode != 0:
        detail = command_error(result)
        if len(detail) > 1200:
            detail = detail[-1200:]
        raise LaneError(f"pytest collection failed: {detail}")


def rollback_created_lane(
    repo: Path, root: Path, worktree: Path, base: str, name: str
) -> str | None:
    head = git(worktree, "rev-parse", "HEAD", check=False)
    status = git(worktree, "status", "--porcelain", check=False)
    if head.returncode != 0 or status.returncode != 0:
        return "new lane preserved because rollback state is uncertain"
    if head.stdout.strip() != base or status.stdout.strip():
        return "new lane preserved because rollback is not exact-base and clean"

    state = lane_state(root, name)
    removed, evidence = remove_worktree(repo, worktree)
    if not removed:
        lane_state_status = "preserved" if state.exists() else "absent"
        return (
            "new lane preserved because worktree removal failed: "
            f"{evidence['error']}; lane state {lane_state_status}; "
            f"worktree {evidence['worktree_state']}; path {evidence['path_state']}"
        )
    if state.exists():
        try:
            shutil.rmtree(state)
        except OSError as error:
            return f"new lane worktree removed but state cleanup failed: {error}"
    return None


def prepare(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=True)
    if not LANE_NAME.fullmatch(args.name):
        raise LaneError("--name must contain only letters, digits, dot, dash, or underscore")
    base = resolve_base(repo, args.base)
    worktree = (root / args.name).resolve()
    if not contained(worktree, root):
        raise LaneError("worktree path escapes the configured root")

    registered = registered_worktrees(repo)
    reused = worktree in registered
    if worktree.exists() and not reused:
        raise LaneError(f"target exists but is not a registered worktree: {worktree}")
    if not worktree.exists() and reused:
        raise LaneError(f"registered worktree path is missing: {worktree}")
    if not reused:
        result = git(
            repo,
            "worktree",
            "add",
            "--detach",
            str(worktree),
            base,
            check=False,
        )
        if result.returncode != 0:
            raise LaneError(f"worktree creation failed: {command_error(result)}")

    try:
        head = git(worktree, "rev-parse", "HEAD").stdout.strip()
        if head != base:
            raise LaneError(f"worktree HEAD {head} does not match requested base {base}")
        status = git(worktree, "status", "--porcelain").stdout.strip()
        if status:
            raise LaneError("worktree is not clean")

        _, temp_root, pytest_basetemp, pytest_cache = state_paths(root, args.name)
        pytest_status = "not-applicable"
        if pytest_configured(worktree):
            pytest_smoke(worktree, temp_root, pytest_basetemp, pytest_cache)
            pytest_status = "passed"
        if git(worktree, "status", "--porcelain").stdout.strip():
            raise LaneError("preflight left the worktree dirty")

        return 0, {
            "ok": True,
            "worktree": str(worktree),
            "base": base,
            "reused": reused,
            "temp_root": str(temp_root),
            "pytest_basetemp": str(pytest_basetemp),
            "pytest_cache": str(pytest_cache),
            "pytest": pytest_status,
        }
    except (LaneError, OSError) as error:
        if reused:
            raise
        rollback_error = rollback_created_lane(repo, root, worktree, base, args.name)
        if rollback_error:
            raise LaneError(f"{error}; {rollback_error}") from error
        raise LaneError(str(error)) from error


def worktree_age(worktree: Path) -> tuple[int, str]:
    try:
        age = worktree.stat().st_mtime_ns
    except OSError:
        age = 2**63 - 1
    return age, str(worktree).casefold()


def remove_worktree(repo: Path, worktree: Path) -> tuple[bool, dict[str, str]]:
    result = git(repo, "worktree", "remove", str(worktree), check=False)
    if result.returncode == 0:
        return True, {}

    try:
        still_registered = worktree in set(registered_worktrees(repo))
        path_exists = worktree.exists()
    except (LaneError, OSError):
        still_registered = None
        path_exists = True
    worktree_state = (
        "registered"
        if still_registered is True
        else "unregistered"
        if still_registered is False
        else "uncertain"
    )
    evidence = {
        "error": command_error(result),
        "worktree_state": worktree_state,
        "path_state": "present" if path_exists else "missing",
    }
    return still_registered is False and not path_exists, evidence


def recover_unregistered_lane(root: Path, worktree: Path) -> tuple[bool, dict[str, str]]:
    state = lane_state(root, worktree.name)
    if worktree.exists():
        try:
            worktree.rmdir()
        except OSError as error:
            return False, {
                "worktree": str(worktree),
                "reason": "unregistered residual path preserved",
                "error": str(error),
                "lane_state": "preserved",
                "worktree_state": "unregistered",
                "path_state": "present",
            }
    try:
        shutil.rmtree(state)
    except OSError as error:
        return False, {
            "worktree": str(worktree),
            "reason": "lane state cleanup failed",
            "error": str(error),
            "lane_state": "preserved",
            "worktree_state": "unregistered",
            "path_state": "missing",
        }
    return True, {}


def cleanup(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    completed_paths = [Path(path).resolve() for path in args.completed]
    if len(completed_paths) != len(set(completed_paths)):
        raise LaneError("--completed contains a duplicate worktree")
    for worktree in completed_paths:
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
    if completed_paths and not root.is_dir():
        raise LaneError(f"worktree root does not exist: {root}")
    completed = set(completed_paths)
    registered = set(registered_worktrees(repo))
    recovery_paths: list[Path] = []
    for worktree in completed_paths:
        if worktree not in registered:
            state = lane_state(root, worktree.name)
            if not state.is_dir():
                raise LaneError(f"completed path is not a registered worktree: {worktree}")
            if args.oldest:
                raise LaneError(
                    "unregistered residual recovery requires cleanup without --oldest: "
                    f"{worktree}"
                )
            recovery_paths.append(worktree)
    repo_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    candidates = sorted(
        (
            path
            for path in registered
            if path != repo and path.parent == root
        ),
        key=worktree_age,
    )

    safe: list[Path] = []
    preserved: list[dict[str, str]] = []
    for worktree in candidates:
        if worktree not in completed:
            preserved.append({"worktree": str(worktree), "reason": "not completed"})
            continue
        status = git(worktree, "status", "--porcelain", check=False)
        if status.returncode != 0:
            preserved.append({"worktree": str(worktree), "reason": "uncertain"})
            continue
        if status.stdout.strip():
            preserved.append({"worktree": str(worktree), "reason": "not clean"})
            continue
        head = git(worktree, "rev-parse", "HEAD", check=False)
        if head.returncode != 0:
            preserved.append({"worktree": str(worktree), "reason": "uncertain"})
            continue
        integrated = git(
            repo,
            "merge-base",
            "--is-ancestor",
            head.stdout.strip(),
            repo_head,
            check=False,
        )
        if integrated.returncode == 1:
            preserved.append({"worktree": str(worktree), "reason": "not integrated"})
            continue
        if integrated.returncode != 0:
            preserved.append({"worktree": str(worktree), "reason": "uncertain"})
            continue
        safe.append(worktree)

    removed: list[str] = []
    remove_failed = False
    capacity_released = False
    for worktree in recovery_paths:
        recovered, evidence = recover_unregistered_lane(root, worktree)
        if recovered:
            removed.append(str(worktree))
        else:
            remove_failed = True
            preserved.append(evidence)
    for index, worktree in enumerate(safe):
        state = lane_state(root, worktree.name)
        worktree_removed, evidence = remove_worktree(repo, worktree)
        if not worktree_removed:
            remove_failed = True
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": (
                        "remove failed"
                        if evidence["worktree_state"] != "unregistered"
                        else "remove incomplete"
                    ),
                    "lane_state": "preserved" if state.exists() else "absent",
                    **evidence,
                }
            )
            continue
        capacity_released = True
        if state.exists():
            try:
                shutil.rmtree(state)
            except OSError as error:
                remove_failed = True
                preserved.append(
                    {
                        "worktree": str(worktree),
                        "reason": "lane state cleanup failed",
                        "error": str(error),
                        "lane_state": "preserved",
                        "worktree_state": "unregistered",
                        "path_state": "missing",
                    }
                )
                if args.oldest:
                    break
                continue
        removed.append(str(worktree))
        if args.oldest:
            preserved.extend(
                {"worktree": str(remaining), "reason": "capacity retained"}
                for remaining in safe[index + 1 :]
            )
            break

    if args.oldest and not removed:
        if remove_failed:
            return 1, {
                "ok": False,
                "error": (
                    "capacity cleanup incomplete"
                    if capacity_released
                    else "capacity cleanup failed"
                ),
                "removed": [],
                "preserved": preserved,
            }
        return 2, {
            "ok": False,
            "error": "capacity blocked: no safe completed worktree",
            "removed": [],
            "preserved": preserved,
        }
    if remove_failed and not args.oldest:
        return 1, {
            "ok": False,
            "error": "cleanup incomplete",
            "removed": removed,
            "preserved": preserved,
        }
    return 0, {"ok": True, "removed": removed, "preserved": preserved}


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
    cleanup_parser.add_argument("--oldest", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        code, packet = prepare(args) if args.operation == "prepare" else cleanup(args)
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
