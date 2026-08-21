"""Prepare and safely clean up concurrent-worker Git worktrees."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


LANE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")


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
    command = ["git", "-C", str(checkout), *args]
    result = run(command)
    output = f"{result.stdout}\n{result.stderr}".lower()
    if result.returncode != 0 and (
        "dubious ownership" in output or "safe.directory" in output
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


def lane_state(root: Path, name: str) -> Path:
    state = (root / ".state" / name).resolve()
    if not contained(state, root):
        raise LaneError("lane state path escapes the configured root")
    return state


def state_paths(root: Path, name: str) -> tuple[Path, Path, Path, Path]:
    state = lane_state(root, name)
    paths = state / "tmp", state / "pytest", state / "cache"
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    return state, *paths


def remove_worktree(repo: Path, worktree: Path) -> tuple[bool, dict[str, str]]:
    result = git(repo, "worktree", "remove", str(worktree), check=False)
    if result.returncode == 0:
        return True, {}
    try:
        registered = worktree in registered_worktrees(repo)
        exists = worktree.exists()
    except (LaneError, OSError):
        registered = None
        exists = True
    evidence = {
        "error": command_error(result),
        "worktree_state": (
            "registered" if registered is True else "unregistered" if registered is False else "uncertain"
        ),
        "path_state": "present" if exists else "missing",
    }
    return registered is False and not exists, evidence


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
        return (
            "new lane preserved because worktree removal failed: "
            f"{evidence['error']}; lane state "
            f"{'preserved' if state.exists() else 'absent'}; worktree "
            f"{evidence['worktree_state']}; path {evidence['path_state']}"
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
    if worktree.parent != root:
        raise LaneError("worktree path escapes the configured root")

    registered = registered_worktrees(repo)
    reused = worktree in registered
    if worktree.exists() and not reused:
        raise LaneError(f"target exists but is not a registered worktree: {worktree}")
    if not worktree.exists() and reused:
        raise LaneError(f"registered worktree path is missing: {worktree}")
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
        _, temp_root, pytest_basetemp, pytest_cache = state_paths(root, args.name)
        return 0, {
            "ok": True,
            "worktree": str(worktree),
            "base": base,
            "reused": reused,
            "temp_root": str(temp_root),
            "pytest_basetemp": str(pytest_basetemp),
            "pytest_cache": str(pytest_cache),
        }
    except (LaneError, OSError) as error:
        if reused:
            raise
        rollback_error = rollback_created_lane(repo, root, worktree, base, args.name)
        if rollback_error:
            raise LaneError(f"{error}; {rollback_error}") from error
        raise LaneError(str(error)) from error


def recover_unregistered_lane(root: Path, worktree: Path) -> tuple[bool, str | None]:
    state = lane_state(root, worktree.name)
    if not state.is_dir():
        return False, "completed path is not a registered worktree"
    if worktree.exists():
        try:
            worktree.rmdir()
        except OSError:
            return False, "unregistered residual path preserved"
    try:
        shutil.rmtree(state)
    except OSError as error:
        return False, f"lane state cleanup failed: {error}"
    return True, None


def validate_completed(root: Path, values: list[str]) -> list[Path]:
    paths = [Path(value).resolve() for value in values]
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


def cleanup(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repo = repository_root(args.repo)
    root = lane_root(args.root, repo, create=False)
    completed = validate_completed(root, args.completed)
    if completed and not root.is_dir():
        raise LaneError(f"worktree root does not exist: {root}")

    repo_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    registered = registered_worktrees(repo)
    removed: list[str] = []
    preserved: list[dict[str, str]] = []

    for worktree in completed:
        if worktree not in registered:
            recovered, reason = recover_unregistered_lane(root, worktree)
            if recovered:
                removed.append(str(worktree))
            else:
                preserved.append({"worktree": str(worktree), "reason": str(reason)})
            continue

        status = git(worktree, "status", "--porcelain", check=False)
        head = git(worktree, "rev-parse", "HEAD", check=False)
        if status.returncode != 0 or head.returncode != 0:
            preserved.append({"worktree": str(worktree), "reason": "uncertain"})
            continue
        if status.stdout.strip():
            preserved.append({"worktree": str(worktree), "reason": "not clean"})
            continue
        integrated = git(
            repo, "merge-base", "--is-ancestor", head.stdout.strip(), repo_head, check=False
        )
        if integrated.returncode == 1:
            preserved.append({"worktree": str(worktree), "reason": "not integrated"})
            continue
        if integrated.returncode != 0:
            preserved.append({"worktree": str(worktree), "reason": "uncertain"})
            continue

        state = lane_state(root, worktree.name)
        worktree_removed, evidence = remove_worktree(repo, worktree)
        if not worktree_removed:
            preserved.append(
                {
                    "worktree": str(worktree),
                    "reason": "remove failed",
                    "lane_state": "preserved" if state.exists() else "absent",
                    **evidence,
                }
            )
            continue
        if state.exists():
            try:
                shutil.rmtree(state)
            except OSError as error:
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
                continue
        removed.append(str(worktree))

    packet = {"ok": not preserved, "removed": removed, "preserved": preserved}
    if preserved:
        packet["error"] = "cleanup incomplete"
        return 1, packet
    return 0, packet


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
