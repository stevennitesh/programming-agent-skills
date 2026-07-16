"""Create, preflight, and clean up manual parallel-implement worktrees."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


class LaneError(RuntimeError):
    """A safe lane lifecycle operation could not complete."""


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise LaneError(f"{' '.join(args)}: {detail}")
    return result


def git_repo_with_trust(
    repo: Path, args: list[str], *, check: bool = True
) -> tuple[subprocess.CompletedProcess[str], str]:
    command = ["git", "-C", str(repo), *args]
    result = run(command, check=False)
    trust = "normal"
    trust_error = f"{result.stdout}\n{result.stderr}".lower()
    if result.returncode != 0 and (
        "dubious ownership" in trust_error or "safe.directory" in trust_error
    ):
        trust = "command-scoped-safe-directory"
        command = [
            "git",
            "-c",
            f"safe.directory={repo}",
            "-C",
            str(repo),
            *args,
        ]
        result = run(command, check=False)
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise LaneError(detail)
    return result, trust


def git_root(repo: Path) -> tuple[Path, str]:
    result, trust = git_repo_with_trust(repo, ["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip()).resolve(), trust


def git_with_trust(
    worktree: Path, args: list[str], *, check: bool = True
) -> tuple[subprocess.CompletedProcess[str], str]:
    command = ["git", "-C", str(worktree), *args]
    result = run(command, check=False)
    trust = "normal"
    trust_error = f"{result.stdout}\n{result.stderr}".lower()
    if result.returncode != 0 and (
        "dubious ownership" in trust_error or "safe.directory" in trust_error
    ):
        trust = "command-scoped-safe-directory"
        command = [
            "git",
            "-c",
            f"safe.directory={worktree}",
            "-C",
            str(worktree),
            *args,
        ]
        result = run(command, check=False)
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise LaneError(detail)
    return result, trust


def slug(value: str, *, limit: int = 28) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (normalized or "lane")[:limit].rstrip("-")


def contains(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return target != root


def registered_worktrees(repo: Path) -> dict[Path, dict[str, str]]:
    result, _ = git_repo_with_trust(repo, ["worktree", "list", "--porcelain"])
    records: dict[Path, dict[str, str]] = {}
    current: dict[str, str] = {}
    for line in [*result.stdout.splitlines(), ""]:
        if not line:
            if "worktree" in current:
                records[Path(current["worktree"]).resolve()] = current
            current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return records


def longest_tracked_path(repo: Path) -> int:
    result, _ = git_repo_with_trust(repo, ["ls-files", "-z"])
    return max((len(path) for path in result.stdout.split("\0") if path), default=0)


def path_budget(worktree: Path, repo: Path, configured: int | None) -> dict[str, int]:
    limit = configured if configured is not None else (240 if os.name == "nt" else 4096)
    longest = longest_tracked_path(repo)
    reserve = 32
    predicted = len(str(worktree)) + 1 + longest + reserve
    if predicted > limit:
        raise LaneError(
            f"path budget exceeded: predicted {predicted}, limit {limit}; choose a shorter root"
        )
    return {
        "limit": limit,
        "longest_tracked_relative_path": longest,
        "reserve": reserve,
        "predicted_maximum": predicted,
    }


def emit(operation: str, ok: bool, **data: Any) -> int:
    packet = {
        "schema": SCHEMA_VERSION,
        "operation": operation,
        "ok": ok,
        **data,
    }
    print(json.dumps(packet, sort_keys=True))
    return 0 if ok else 1


def create(args: argparse.Namespace) -> int:
    repo, repo_trust = git_root(Path(args.repo).resolve())
    root = (
        Path(args.root).resolve()
        if args.root
        else (repo.parent / "worktrees" / "parallel-implement").resolve()
    )
    worktree = (root / f"{slug(repo.name)}-{slug(args.run_id)}" / slug(args.item_id)).resolve()
    if contains(repo, worktree) and not args.allow_inside_repo:
        raise LaneError("worktree path is inside the active checkout")
    if not contains(root, worktree):
        raise LaneError("worktree path escaped the selected root")
    if worktree.exists():
        raise LaneError(f"worktree path already exists: {worktree}")
    budget = path_budget(worktree, repo, args.max_path)
    root.mkdir(parents=True, exist_ok=True)

    command = ["git", "worktree", "add"]
    if args.branch:
        command.extend(["-b", args.branch])
    else:
        command.append("--detach")
    command.extend([str(worktree), args.base])
    result, create_trust = git_repo_with_trust(repo, command[1:], check=False)
    if result.returncode != 0:
        return emit(
            "create",
            False,
            provider="manual-git",
            repo=str(repo),
            root=str(root),
            worktree=str(worktree),
            git_trust=create_trust,
            error=result.stderr.strip() or result.stdout.strip(),
        )

    records = registered_worktrees(repo)
    record = records.get(worktree)
    if record is None:
        raise LaneError("git reported success but did not register the worktree")
    expected_result, expected_trust = git_repo_with_trust(repo, ["rev-parse", args.base])
    expected = expected_result.stdout.strip()
    actual = record.get("HEAD") or record.get("head")
    if actual != expected:
        raise LaneError(f"registered worktree HEAD {actual} does not match {expected}")
    return emit(
        "create",
        True,
        provider="manual-git",
        repo=str(repo),
        root=str(root),
        worktree=str(worktree),
        base=expected,
        branch=args.branch,
        detached=not bool(args.branch),
        git_trust=(
            "command-scoped-safe-directory"
            if "command-scoped-safe-directory"
            in {repo_trust, create_trust, expected_trust}
            else "normal"
        ),
        path_budget=budget,
        cleanup_route="lane_worktree.py cleanup",
    )


def reversible_probe(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write("parallel-implement preflight\n")
        handle.flush()
        os.fsync(handle.fileno())
    path.unlink()


def resolve_git_path(worktree: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (worktree / path).resolve()


def preflight(args: argparse.Namespace) -> int:
    worktree = Path(args.worktree).resolve()
    root_result, trust = git_with_trust(worktree, ["rev-parse", "--show-toplevel"])
    root = Path(root_result.stdout.strip()).resolve()
    if root != worktree:
        raise LaneError(f"worktree root mismatch: expected {worktree}, got {root}")

    head_result, trust = git_with_trust(worktree, ["rev-parse", "HEAD"])
    head = head_result.stdout.strip()
    base_result, trust = git_with_trust(worktree, ["rev-parse", args.base])
    base = base_result.stdout.strip()
    if head != base:
        raise LaneError(f"worktree HEAD {head} does not match base {base}")

    status_result, trust = git_with_trust(worktree, ["status", "--porcelain=v1"])
    status = status_result.stdout
    if status:
        raise LaneError(f"worktree is not clean: {status.strip()}")

    branch_result, trust = git_with_trust(
        worktree, ["symbolic-ref", "-q", "--short", "HEAD"], check=False
    )
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    if args.expect_branch and branch != args.expect_branch:
        raise LaneError(f"expected branch {args.expect_branch}, got {branch or 'detached'}")
    if not args.expect_branch and branch is not None:
        raise LaneError(f"expected detached HEAD, got branch {branch}")

    token = uuid.uuid4().hex
    lane_tmp = worktree / ".tmp"
    lane_tmp_existed = lane_tmp.exists()
    reversible_probe(lane_tmp / f"parallel-implement-{token}.probe")
    if not lane_tmp_existed and lane_tmp.exists() and not any(lane_tmp.iterdir()):
        lane_tmp.rmdir()

    index_result, trust = git_with_trust(worktree, ["rev-parse", "--git-path", "index"])
    index_path = resolve_git_path(worktree, index_result.stdout.strip())
    reversible_probe(index_path.with_name(f"{index_path.name}.{token}.lock-probe"))

    common_result, trust = git_with_trust(worktree, ["rev-parse", "--git-common-dir"])
    common_dir = resolve_git_path(worktree, common_result.stdout.strip())
    reversible_probe(common_dir / "objects" / "info" / f"parallel-implement-{token}.probe")

    proof: dict[str, Any] = {"command": None, "returncode": None}
    if args.proof_command_json:
        command = json.loads(args.proof_command_json)
        if not isinstance(command, list) or not command or not all(
            isinstance(part, str) and part for part in command
        ):
            raise LaneError("proof command must be a non-empty JSON string array")
        result = run(command, cwd=worktree, check=False)
        proof = {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
        }
        if result.returncode != 0:
            raise LaneError(f"proof startup failed: {result.stderr.strip()}")

    return emit(
        "preflight",
        True,
        provider="manual-git",
        worktree=str(worktree),
        repo_root=str(root),
        base=base,
        head=head,
        branch=branch,
        detached=branch is None,
        status="clean",
        git_trust=trust,
        effective_identity=os.environ.get("USERNAME") or os.environ.get("USER"),
        probes={"checkout": "passed", "index_lock": "passed", "git_objects": "passed"},
        proof_startup=proof,
        cleanup_route="lane_worktree.py cleanup",
    )


def cleanup(args: argparse.Namespace) -> int:
    repo, repo_trust = git_root(Path(args.repo).resolve())
    worktree = Path(args.worktree).resolve()
    registered_before = worktree in registered_worktrees(repo)
    if not registered_before:
        state = "unregistered-residual-directory" if worktree.exists() else "removed"
        return emit(
            "cleanup",
            state == "removed",
            repo=str(repo),
            worktree=str(worktree),
            state=state,
            registered_before=False,
            registered_after=False,
            directory_exists=worktree.exists(),
        )

    head_result, _ = git_with_trust(worktree, ["rev-parse", "HEAD"])
    head = head_result.stdout.strip()
    if head != args.expected_head:
        raise LaneError(f"worktree HEAD {head} does not match recorded {args.expected_head}")
    status_result, _ = git_with_trust(worktree, ["status", "--porcelain=v1"])
    if status_result.stdout:
        return emit(
            "cleanup",
            False,
            repo=str(repo),
            worktree=str(worktree),
            state="blocked-dirty",
            head=head,
            status=status_result.stdout,
        )
    if args.disposition not in {"integrated", "preserved"}:
        return emit(
            "cleanup",
            False,
            repo=str(repo),
            worktree=str(worktree),
            state="blocked-unpreserved",
            head=head,
        )

    result, remove_trust = git_repo_with_trust(
        repo, ["worktree", "remove", str(worktree)], check=False
    )
    registered_after = worktree in registered_worktrees(repo)
    directory_exists = worktree.exists()
    if not registered_after and not directory_exists:
        state = "removed"
    elif not registered_after and directory_exists:
        state = "unregistered-residual-directory"
    else:
        state = "registered-preserved"
    return emit(
        "cleanup",
        state == "removed",
        repo=str(repo),
        worktree=str(worktree),
        state=state,
        head=head,
        disposition=args.disposition,
        git_trust=(
            "command-scoped-safe-directory"
            if "command-scoped-safe-directory" in {repo_trust, remove_trust}
            else "normal"
        ),
        registered_before=registered_before,
        registered_after=registered_after,
        directory_exists=directory_exists,
        git_returncode=result.returncode,
        git_error=result.stderr.strip(),
    )


def extended_path(path: Path) -> str:
    value = str(path)
    if os.name != "nt" or value.startswith("\\\\?\\"):
        return value
    if value.startswith("\\\\"):
        return "\\\\?\\UNC\\" + value.lstrip("\\")
    return "\\\\?\\" + value


def purge_residual(args: argparse.Namespace) -> int:
    repo, _ = git_root(Path(args.repo).resolve())
    root = Path(args.root).resolve()
    worktree = Path(args.worktree).resolve()
    if not args.confirm_unregistered_residual:
        raise LaneError("explicit residual-cleanup confirmation is required")
    if not contains(root, worktree):
        raise LaneError("residual path is outside the recorded worktree root")
    if worktree in registered_worktrees(repo):
        raise LaneError("residual path is still registered as a Git worktree")
    if worktree.exists():
        shutil.rmtree(extended_path(worktree))
    return emit(
        "purge-residual",
        not worktree.exists(),
        repo=str(repo),
        root=str(root),
        worktree=str(worktree),
        state="removed" if not worktree.exists() else "unregistered-residual-directory",
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    create_parser = commands.add_parser("create")
    create_parser.add_argument("--repo", required=True)
    create_parser.add_argument("--root")
    create_parser.add_argument("--base", required=True)
    create_parser.add_argument("--run-id", required=True)
    create_parser.add_argument("--item-id", required=True)
    create_parser.add_argument("--branch")
    create_parser.add_argument("--max-path", type=int)
    create_parser.add_argument("--allow-inside-repo", action="store_true")
    create_parser.set_defaults(handler=create)

    preflight_parser = commands.add_parser("preflight")
    preflight_parser.add_argument("--worktree", required=True)
    preflight_parser.add_argument("--base", required=True)
    preflight_parser.add_argument("--expect-branch")
    preflight_parser.add_argument("--proof-command-json")
    preflight_parser.set_defaults(handler=preflight)

    cleanup_parser = commands.add_parser("cleanup")
    cleanup_parser.add_argument("--repo", required=True)
    cleanup_parser.add_argument("--worktree", required=True)
    cleanup_parser.add_argument("--expected-head", required=True)
    cleanup_parser.add_argument("--disposition", required=True)
    cleanup_parser.set_defaults(handler=cleanup)

    purge_parser = commands.add_parser("purge-residual")
    purge_parser.add_argument("--repo", required=True)
    purge_parser.add_argument("--root", required=True)
    purge_parser.add_argument("--worktree", required=True)
    purge_parser.add_argument("--confirm-unregistered-residual", action="store_true")
    purge_parser.set_defaults(handler=purge_residual)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (LaneError, OSError, json.JSONDecodeError) as error:
        return emit(args.command, False, error=str(error))


if __name__ == "__main__":
    raise SystemExit(main())
