"""Create, preflight, and clean up manual parallel-implement worktrees."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
PROJECT_MARKER_SCHEMA = 1
PROJECT_KEY_PATTERN = re.compile(r"[a-z][a-z0-9-]{1,15}-\d{3}")
PROJECT_MARKER_NAME = ".repo.json"
WORKTREE_DIR_NAME = "wt"
WINDOWS_USABLE_MAX_PATH = 259
PYTHON_PROVENANCE_MARKER = "PARALLEL_IMPLEMENT_PYTHON_PROVENANCE="
ROOT_CHECKOUT_ENV = "PARALLEL_IMPLEMENT_ROOT_CHECKOUT"
BASE_ROOT_ENV = "PARALLEL_IMPLEMENT_BASE_ROOT"
PYTHON_PROVENANCE_PROBE = r"""
import importlib
import json
import sys

roots = json.loads(sys.argv[1])
packages = json.loads(sys.argv[2])
sys.path[:0] = roots
resolved = {}
for package in packages:
    module = importlib.import_module(package)
    spec = module.__spec__
    paths = []
    origin = getattr(spec, "origin", None)
    if origin and origin not in {"built-in", "frozen"}:
        paths.append(str(origin))
    locations = getattr(spec, "submodule_search_locations", None)
    if locations:
        paths.extend(str(location) for location in locations)
    resolved[package] = list(dict.fromkeys(paths))
print("PARALLEL_IMPLEMENT_PYTHON_PROVENANCE=" + json.dumps(resolved, sort_keys=True))
"""


class LaneError(RuntimeError):
    """A safe lane lifecycle operation could not complete."""


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
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


def slug(value: str, *, limit: int = 16) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (normalized or "lane")[:limit].rstrip("-")


def project_key(value: str) -> str:
    if not PROJECT_KEY_PATTERN.fullmatch(value):
        raise LaneError(
            "project key must be a short lowercase name followed by a three-digit ID"
        )
    return value


def lane_name(project: str, run_id: str, item_id: str) -> str:
    identity = f"{project}\0{run_id}\0{item_id}"
    suffix = hashlib.sha256(identity.encode()).hexdigest()[:8]
    return f"{slug(run_id, limit=10)}-{slug(item_id, limit=10)}-{suffix}"


def project_paths(base_root: Path, project: str) -> tuple[Path, Path]:
    project_root = (base_root / project).resolve()
    return project_root, (project_root / WORKTREE_DIR_NAME).resolve()


def default_base_root(repo: Path) -> Path:
    if os.name == "nt":
        if not re.fullmatch(r"[A-Za-z]:", repo.drive):
            raise LaneError("repository root has no Windows drive")
        return (Path(f"{repo.drive}/") / "pi").resolve()
    return (repo.parent / "worktrees").resolve()


def contains(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return target != root


def require_lane_identity(
    project: str,
    root: Path,
    worktree: Path,
    run_id: str,
    item_id: str,
) -> None:
    expected = (root / lane_name(project, run_id, item_id)).resolve()
    if worktree != expected:
        raise LaneError(
            f"worktree path does not match the helper-created lane identity: "
            f"expected {expected}"
        )


def repository_identity(repo: Path) -> tuple[str, str]:
    origin, _ = git_repo_with_trust(
        repo, ["config", "--get", "remote.origin.url"], check=False
    )
    if origin.returncode == 0 and origin.stdout.strip():
        source = "origin"
        value = origin.stdout.strip()
    else:
        roots, _ = git_repo_with_trust(
            repo, ["rev-list", "--max-parents=0", "HEAD"]
        )
        source = "root-commits"
        value = "\n".join(sorted(roots.stdout.splitlines()))
    digest = hashlib.sha256(f"{source}\0{value}".encode()).hexdigest()
    return digest, source


def ensure_project_marker(
    repo: Path, project_root: Path, project: str, *, create: bool = False
) -> dict[str, str | int]:
    identity, identity_source = repository_identity(repo)
    marker = project_root / PROJECT_MARKER_NAME
    expected: dict[str, str | int] = {
        "schema": PROJECT_MARKER_SCHEMA,
        "project_key": project,
        "repository_identity": identity,
        "identity_source": identity_source,
    }
    if marker.exists():
        try:
            observed = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise LaneError(f"invalid project identity marker: {marker}") from error
        if observed != expected:
            raise LaneError(f"project key {project} belongs to another repository")
        return expected
    if not create:
        raise LaneError(f"project root has no identity marker: {project_root}")
    project_root.mkdir(parents=True, exist_ok=True)
    if any(project_root.iterdir()):
        raise LaneError(f"project root has no identity marker: {project_root}")
    try:
        with marker.open("x", encoding="utf-8") as handle:
            json.dump(expected, handle, sort_keys=True)
            handle.write("\n")
    except FileExistsError:
        observed = json.loads(marker.read_text(encoding="utf-8"))
        if observed != expected:
            raise LaneError(f"project key {project} belongs to another repository")
    return expected


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


def longest_tracked_path_at_base(repo: Path, base: str) -> int:
    result, _ = git_repo_with_trust(
        repo, ["ls-tree", "-r", "--name-only", "-z", base]
    )
    return max((len(path) for path in result.stdout.split("\0") if path), default=0)


def path_budget(worktree: Path, repo: Path, base: str) -> dict[str, int]:
    limit = WINDOWS_USABLE_MAX_PATH if os.name == "nt" else 4096
    longest = longest_tracked_path_at_base(repo, base)
    predicted = len(str(worktree)) + 1 + longest
    if predicted > limit:
        raise LaneError(
            f"checkout path limit exceeded: predicted {predicted}, limit {limit}; "
            "choose a shorter base root or project key"
        )
    return {
        "limit": limit,
        "longest_tracked_relative_path": longest,
        "checkout_projection": predicted,
    }


def result_packet(operation: str, ok: bool, **data: Any) -> dict[str, Any]:
    return {
        "schema": SCHEMA_VERSION,
        "operation": operation,
        "ok": ok,
        **data,
    }


def emit_packet(packet: dict[str, Any]) -> int:
    print(json.dumps(packet, sort_keys=True))
    return 0 if packet["ok"] else 1


def emit(operation: str, ok: bool, **data: Any) -> int:
    return emit_packet(result_packet(operation, ok, **data))


def blocked_packet(
    operation: str,
    *,
    state: str,
    error: str,
    recoverable: bool,
    next_action: dict[str, Any],
    **data: Any,
) -> dict[str, Any]:
    return result_packet(
        operation,
        False,
        state=state,
        error=error,
        recoverable=recoverable,
        next_action=next_action,
        **data,
    )


def blocked(
    operation: str,
    *,
    state: str,
    error: str,
    recoverable: bool,
    next_action: dict[str, Any],
    **data: Any,
) -> int:
    return emit_packet(
        blocked_packet(
            operation,
            state=state,
            error=error,
            recoverable=recoverable,
            next_action=next_action,
            **data,
        )
    )


def create_packet(args: argparse.Namespace) -> dict[str, Any]:
    repo, repo_trust = git_root(Path(args.repo).resolve())
    project = project_key(args.project_key)
    environment_root = os.environ.get(BASE_ROOT_ENV, "").strip()
    if args.base_root:
        base_root = Path(args.base_root).resolve()
        base_root_source = "explicit"
    elif environment_root:
        base_root = Path(environment_root).resolve()
        base_root_source = "environment"
    else:
        base_root = default_base_root(repo)
        base_root_source = (
            "windows-repo-drive-default" if os.name == "nt" else "repo-parent-default"
        )
    project_root, root = project_paths(base_root, project)
    worktree = (root / lane_name(project, args.run_id, args.item_id)).resolve()
    if contains(repo, worktree) and not args.allow_inside_repo:
        raise LaneError("worktree path is inside the active checkout")
    if not contains(root, worktree):
        raise LaneError("worktree path escaped the selected root")
    reused = worktree.exists()
    if reused and not getattr(args, "reuse_existing", False):
        raise LaneError(f"worktree path already exists: {worktree}")
    try:
        budget = path_budget(worktree, repo, args.base)
    except LaneError as error:
        return blocked_packet(
            "create",
            state="blocked-path-budget",
            error=str(error),
            recoverable=True,
            next_action={
                "command": "create",
                "repair": "choose a shorter base root or project key",
            },
            provider="manual-helper",
            repo=str(repo),
            project_key=project,
            base_root=str(base_root),
            base_root_source=base_root_source,
            project_root=str(project_root),
            root=str(root),
            worktree=str(worktree),
        )
    marker = ensure_project_marker(repo, project_root, project, create=True)
    root.mkdir(exist_ok=True)

    create_trust = repo_trust
    if not reused:
        command = ["git", "worktree", "add"]
        if args.branch:
            command.extend(["-b", args.branch])
        else:
            command.append("--detach")
        command.extend([str(worktree), args.base])
        result, create_trust = git_repo_with_trust(repo, command[1:], check=False)
        if result.returncode != 0:
            return blocked_packet(
                "create",
                state="blocked-create",
                error=result.stderr.strip() or result.stdout.strip(),
                recoverable=True,
                next_action={
                    "command": "open",
                    "repair": "change the base, root, trust, permission, capability, or conflicting path",
                },
                provider="manual-helper",
                repo=str(repo),
                project_key=project,
                base_root=str(base_root),
                base_root_source=base_root_source,
                project_root=str(project_root),
                root=str(root),
                worktree=str(worktree),
                git_trust=create_trust,
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
    return result_packet(
        "create",
        True,
        provider="manual-helper",
        repo=str(repo),
        project_key=project,
        base_root=str(base_root),
        base_root_source=base_root_source,
        project_root=str(project_root),
        project_marker=marker,
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
        reused=reused,
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


def proof_command(args: argparse.Namespace) -> tuple[list[str] | None, dict[str, str]]:
    if args.proof_command_file:
        path = Path(args.proof_command_file).resolve()
        raw = path.read_bytes()
        try:
            value = json.loads(raw.decode("utf-8-sig"))
        except UnicodeDecodeError as error:
            raise LaneError("proof command file must be UTF-8") from error
        provenance = {
            "command_file": str(path),
            "command_file_sha256": hashlib.sha256(raw).hexdigest(),
        }
    elif args.proof_command_json:
        value = json.loads(args.proof_command_json)
        provenance = {"command_source": "inline-json"}
    else:
        return None, {}
    if not isinstance(value, list) or not value or not all(
        isinstance(part, str) and part for part in value
    ):
        raise LaneError("proof command must be a non-empty JSON string array")
    return value, provenance


def python_provenance(args: argparse.Namespace, worktree: Path) -> dict[str, Any]:
    path = Path(args.python_provenance_file).resolve()
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except UnicodeDecodeError as error:
        raise LaneError("Python provenance file must be UTF-8") from error
    if not isinstance(value, dict):
        raise LaneError("Python provenance file must contain one JSON object")

    executable_value = value.get("executable")
    roots_value = value.get("import_roots")
    packages = value.get("packages")
    if not isinstance(executable_value, str) or not executable_value:
        raise LaneError("Python provenance requires an explicit executable")
    executable_path = Path(executable_value)
    if not executable_path.is_absolute():
        raise LaneError("Python provenance executable must be an existing absolute file")
    executable = executable_path.resolve()
    if not executable.is_file():
        raise LaneError("Python provenance executable must be an existing absolute file")
    if not isinstance(roots_value, list) or not roots_value or not all(
        isinstance(root, str) and root for root in roots_value
    ):
        raise LaneError("Python provenance import_roots must be a non-empty string list")
    if not isinstance(packages, list) or not packages or not all(
        isinstance(package, str)
        and re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", package)
        for package in packages
    ):
        raise LaneError("Python provenance packages must be a non-empty import-name list")

    import_roots: list[Path] = []
    for root_value in roots_value:
        candidate = Path(root_value)
        resolved = (
            candidate.resolve()
            if candidate.is_absolute()
            else (worktree / candidate).resolve()
        )
        if resolved != worktree and not contains(worktree, resolved):
            raise LaneError(f"Python provenance import root escapes the lane: {root_value}")
        if not resolved.is_dir():
            raise LaneError(f"Python provenance import root is not a directory: {root_value}")
        import_roots.append(resolved)

    result = run(
        [
            str(executable),
            "-I",
            "-B",
            "-c",
            PYTHON_PROVENANCE_PROBE,
            json.dumps([str(root) for root in import_roots]),
            json.dumps(packages),
        ],
        cwd=worktree,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "probe failed"
        raise LaneError(f"Python provenance probe failed: {detail}")
    encoded = next(
        (
            line[len(PYTHON_PROVENANCE_MARKER) :]
            for line in reversed(result.stdout.splitlines())
            if line.startswith(PYTHON_PROVENANCE_MARKER)
        ),
        None,
    )
    if encoded is None:
        raise LaneError("Python provenance probe returned no structured result")
    resolved_value = json.loads(encoded)
    if not isinstance(resolved_value, dict):
        raise LaneError("Python provenance probe returned an invalid result")

    resolved_packages: dict[str, list[str]] = {}
    for package in packages:
        package_paths = resolved_value.get(package)
        if not isinstance(package_paths, list) or not package_paths or not all(
            isinstance(package_path, str) and package_path
            for package_path in package_paths
        ):
            raise LaneError(f"Python package resolved no project paths: {package}")
        verified: list[str] = []
        for package_path in package_paths:
            resolved_path = Path(package_path).resolve()
            if resolved_path != worktree and not contains(worktree, resolved_path):
                raise LaneError(
                    f"Python package resolves outside the lane: {package} -> {resolved_path}"
                )
            verified.append(str(resolved_path))
        resolved_packages[package] = verified

    return {
        "status": "verified",
        "configuration_file": str(path),
        "configuration_sha256": hashlib.sha256(raw).hexdigest(),
        "executable": str(executable),
        "import_roots": [str(root) for root in import_roots],
        "packages": packages,
        "resolved_packages": resolved_packages,
    }


def preflight_packet(args: argparse.Namespace) -> dict[str, Any]:
    worktree = Path(args.worktree).resolve()
    root_checkout = Path(args.repo).resolve()
    command, command_provenance = proof_command(args)
    if args.skip_proof and not args.reason:
        return blocked_packet(
            "preflight",
            state="blocked-proof",
            error="--skip-proof requires --reason",
            recoverable=True,
            next_action={"command": "preflight", "required": ["--reason"]},
            worktree=str(worktree),
        )
    if not args.python_provenance_file and not args.skip_python_provenance:
        return blocked_packet(
            "preflight",
            state="blocked-provenance",
            error="Python provenance is required unless explicitly skipped",
            recoverable=True,
            next_action={
                "command": "preflight",
                "required": [
                    "--python-provenance-file",
                    "or --skip-python-provenance --python-provenance-reason",
                ],
            },
            worktree=str(worktree),
        )
    if args.skip_python_provenance and not args.python_provenance_reason:
        return blocked_packet(
            "preflight",
            state="blocked-provenance",
            error="--skip-python-provenance requires --python-provenance-reason",
            recoverable=True,
            next_action={
                "command": "preflight",
                "required": ["--python-provenance-reason"],
            },
            worktree=str(worktree),
        )

    trusts: set[str] = set()
    source_result, trust = git_with_trust(
        root_checkout, ["rev-parse", "--show-toplevel"]
    )
    trusts.add(trust)
    if Path(source_result.stdout.strip()).resolve() != root_checkout:
        raise LaneError("root checkout does not resolve to its recorded Git root")
    if root_checkout == worktree:
        raise LaneError("isolated worktree must differ from the root checkout")

    root_result, trust = git_with_trust(worktree, ["rev-parse", "--show-toplevel"])
    trusts.add(trust)
    root = Path(root_result.stdout.strip()).resolve()
    if root != worktree:
        raise LaneError(f"worktree root mismatch: expected {worktree}, got {root}")

    head_result, trust = git_with_trust(worktree, ["rev-parse", "HEAD"])
    trusts.add(trust)
    head = head_result.stdout.strip()
    base_result, trust = git_with_trust(worktree, ["rev-parse", args.base])
    trusts.add(trust)
    base = base_result.stdout.strip()
    if head != base:
        raise LaneError(f"worktree HEAD {head} does not match base {base}")

    status_result, trust = git_with_trust(worktree, ["status", "--porcelain=v1"])
    trusts.add(trust)
    status = status_result.stdout
    if status:
        raise LaneError(f"worktree is not clean: {status.strip()}")

    branch_result, trust = git_with_trust(
        worktree, ["symbolic-ref", "-q", "--short", "HEAD"], check=False
    )
    trusts.add(trust)
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    if args.expect_branch and branch != args.expect_branch:
        raise LaneError(f"expected branch {args.expect_branch}, got {branch or 'detached'}")
    if not args.expect_branch and branch is not None:
        raise LaneError(f"expected detached HEAD, got branch {branch}")

    token = uuid.uuid4().hex
    lane_tmp = worktree / ".tmp"
    reversible_probe(lane_tmp / f"parallel-implement-{token}.probe")
    actor_root = lane_tmp / "pi" / slug(args.actor_id, limit=20)
    pytest_basetemp = actor_root / "pytest"
    cache_root = actor_root / "cache"
    pytest_basetemp.mkdir(parents=True, exist_ok=True)
    cache_root.mkdir(parents=True, exist_ok=True)

    index_result, trust = git_with_trust(worktree, ["rev-parse", "--git-path", "index"])
    trusts.add(trust)
    index_path = resolve_git_path(worktree, index_result.stdout.strip())
    reversible_probe(index_path.with_name(f"{index_path.name}.{token}.lock-probe"))

    common_result, trust = git_with_trust(worktree, ["rev-parse", "--git-common-dir"])
    trusts.add(trust)
    common_dir = resolve_git_path(worktree, common_result.stdout.strip())
    reversible_probe(common_dir / "objects" / "info" / f"parallel-implement-{token}.probe")

    proof: dict[str, Any]
    if command is not None:
        proof_env = {**os.environ, ROOT_CHECKOUT_ENV: str(root_checkout)}
        result = run(command, cwd=worktree, check=False, env=proof_env)
        proof = {
            "status": "passed",
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
            **command_provenance,
        }
        if result.returncode != 0:
            raise LaneError(f"proof startup failed: {result.stderr.strip()}")
    elif args.skip_proof:
        proof = {"status": "skipped", "skipped": True, "reason": args.reason}
    else:
        proof = {
            "status": "passed",
            "kind": "builtin-viability",
            "checks": ["checkout", "index-lock", "git-objects"],
        }

    provenance = (
        python_provenance(args, worktree)
        if args.python_provenance_file
        else {
            "status": "not-applicable",
            "skipped": True,
            "reason": args.python_provenance_reason,
        }
    )

    final_head_result, trust = git_with_trust(worktree, ["rev-parse", "HEAD"])
    trusts.add(trust)
    final_head = final_head_result.stdout.strip()
    if final_head != base:
        raise LaneError(
            f"worktree HEAD changed during preflight: expected {base}, got {final_head}"
        )
    final_status_result, trust = git_with_trust(
        worktree, ["status", "--porcelain=v1"]
    )
    trusts.add(trust)
    if final_status_result.stdout:
        raise LaneError(
            f"worktree changed during preflight: {final_status_result.stdout.strip()}"
        )
    final_branch_result, trust = git_with_trust(
        worktree, ["symbolic-ref", "-q", "--short", "HEAD"], check=False
    )
    trusts.add(trust)
    final_branch = (
        final_branch_result.stdout.strip()
        if final_branch_result.returncode == 0
        else None
    )
    if final_branch != branch:
        raise LaneError(
            f"worktree branch changed during preflight: expected {branch or 'detached'}, "
            f"got {final_branch or 'detached'}"
        )

    return result_packet(
        "preflight",
        True,
        provider="manual-helper",
        worktree=str(worktree),
        root_checkout={
            "path": str(root_checkout),
            "access": "read-only",
            "environment": ROOT_CHECKOUT_ENV,
        },
        repo_root=str(root),
        base=base,
        observed_head=final_head,
        branch=final_branch,
        detached=final_branch is None,
        status="clean",
        git_trust=(
            "command-scoped-safe-directory"
            if "command-scoped-safe-directory" in trusts
            else "normal"
        ),
        effective_identity=os.environ.get("USERNAME") or os.environ.get("USER"),
        probes={"checkout": "passed", "index_lock": "passed", "git_objects": "passed"},
        startup_proof=proof,
        project_provenance=provenance,
        actor_id=args.actor_id,
        temp_root=str(actor_root),
        pytest_basetemp=str(pytest_basetemp),
        cache_root=str(cache_root),
        cleanup_route="lane_worktree.py cleanup",
    )


def open_lane(args: argparse.Namespace) -> int:
    """Create and preflight one lane while preserving it on startup failure."""
    try:
        lane = create_packet(
            argparse.Namespace(
                repo=args.repo,
                project_key=args.project_key,
                base_root=args.base_root,
                base=args.base,
                run_id=args.run_id,
                item_id=args.item_id,
                branch=args.branch,
                allow_inside_repo=args.allow_inside_repo,
                reuse_existing=True,
            )
        )
    except (LaneError, OSError, json.JSONDecodeError) as error:
        lane = blocked_packet(
            "create",
            state="blocked-error",
            error=str(error),
            recoverable=True,
            next_action={"command": "open", "repair": "correct the creation input"},
        )
    if not lane.get("ok"):
        return emit(
            "open",
            False,
            state=lane.get("state", "blocked-create"),
            recoverable=lane.get("recoverable", True),
            lane=lane,
            error=lane.get("error", "lane creation failed"),
            next_action=lane.get("next_action"),
        )

    try:
        preflight = preflight_packet(
            argparse.Namespace(
                worktree=str(lane["worktree"]),
                repo=str(lane["repo"]),
                base=args.base,
                actor_id=args.actor_id,
                expect_branch=args.branch,
                proof_command_json=args.proof_command_json,
                proof_command_file=args.proof_command_file,
                skip_proof=args.skip_proof,
                reason=args.reason,
                python_provenance_file=args.python_provenance_file,
                skip_python_provenance=args.skip_python_provenance,
                python_provenance_reason=args.python_provenance_reason,
            )
        )
    except (LaneError, OSError, json.JSONDecodeError) as error:
        preflight = blocked_packet(
            "preflight",
            state="blocked-error",
            error=str(error),
            recoverable=True,
            next_action={"command": "open", "repair": "correct the startup input"},
            worktree=str(lane["worktree"]),
        )
    if not preflight.get("ok"):
        return emit(
            "open",
            False,
            state="created-preflight-blocked",
            recoverable=True,
            repo=lane.get("repo"),
            project_key=lane.get("project_key"),
            base_root=lane.get("base_root"),
            root=lane.get("root"),
            worktree=lane.get("worktree"),
            lane=lane,
            preflight=preflight,
            error=preflight.get("error", "lane preflight failed"),
            next_action={
                "command": "open",
                "worktree": lane.get("worktree"),
                "repair": "fix the startup cause and retry open; the lane was preserved",
            },
        )
    return emit(
        "open",
        True,
        state="ready",
        repo=lane.get("repo"),
        project_key=lane.get("project_key"),
        base_root=lane.get("base_root"),
        root=lane.get("root"),
        worktree=lane.get("worktree"),
        lane=lane,
        preflight=preflight,
        next_action={
            "command": "run_ledger.py dispatch",
            "packet": "prepare",
        },
    )


def cleanup(args: argparse.Namespace) -> int:
    repo, repo_trust = git_root(Path(args.repo).resolve())
    project = project_key(args.project_key)
    base_root = Path(args.base_root).resolve()
    project_root, root = project_paths(base_root, project)
    ensure_project_marker(repo, project_root, project)
    worktree = Path(args.worktree).resolve()
    if not contains(root, worktree):
        raise LaneError("worktree path is outside the recorded root")
    require_lane_identity(project, root, worktree, args.run_id, args.item_id)
    registered_before = worktree in registered_worktrees(repo)
    if not registered_before:
        state = "unregistered-residual-directory" if worktree.exists() else "removed"
        if state == "removed":
            return emit(
                "cleanup",
                True,
                repo=str(repo),
                project_key=project,
                base_root=str(base_root),
                root=str(root),
                worktree=str(worktree),
                state=state,
                registered_before=False,
                registered_after=False,
                directory_exists=False,
            )
        if getattr(args, "confirm_unregistered_residual", False):
            return emit_packet(purge_residual_packet(args))
        return blocked(
            "cleanup",
            state=state,
            error="worktree is already unregistered, so its HEAD and cleanliness cannot be reverified",
            recoverable=True,
            next_action={
                "command": "cleanup",
                "project_key": project,
                "base_root": str(base_root),
                "root": str(root),
                "worktree": str(worktree),
                "requires": "--confirm-unregistered-residual",
            },
            repo=str(repo),
            project_key=project,
            base_root=str(base_root),
            root=str(root),
            worktree=str(worktree),
            registered_before=False,
            registered_after=False,
            directory_exists=True,
        )

    head_result, _ = git_with_trust(worktree, ["rev-parse", "HEAD"])
    head = head_result.stdout.strip()
    expected_result, _ = git_with_trust(worktree, ["rev-parse", args.expected_head])
    expected_head = expected_result.stdout.strip()
    if head != expected_head:
        raise LaneError(f"worktree HEAD {head} does not match recorded {expected_head}")
    status_result, _ = git_with_trust(worktree, ["status", "--porcelain=v1"])
    if status_result.stdout:
        return blocked(
            "cleanup",
            state="blocked-dirty",
            error="worktree is dirty",
            recoverable=True,
            next_action={"command": "inspect", "repair": "preserve or reconcile dirty state"},
            repo=str(repo),
            root=str(root),
            worktree=str(worktree),
            head=head,
            status=status_result.stdout,
        )
    if args.disposition not in {"integrated", "preserved"}:
        return blocked(
            "cleanup",
            state="blocked-unpreserved",
            error="commit disposition is neither integrated nor preserved",
            recoverable=True,
            next_action={"command": "cleanup", "repair": "record integrated or preserved disposition"},
            repo=str(repo),
            root=str(root),
            worktree=str(worktree),
            head=head,
        )

    result, remove_trust = git_repo_with_trust(
        repo, ["worktree", "remove", str(worktree)], check=False
    )
    registered_after = worktree in registered_worktrees(repo)
    directory_exists = worktree.exists()
    residual_removed = False
    cleanup_method = "git-worktree-remove"
    fallback = "not-needed"
    if not registered_after and directory_exists:
        cleanup_method = "extended-path-fallback"
        try:
            shutil.rmtree(extended_path(worktree))
        except OSError as error:
            return blocked(
                "cleanup",
                state="unregistered-residual-directory",
                error=str(error),
                recoverable=True,
                next_action={
                    "command": "inspect-residual",
                    "root": str(root),
                    "worktree": str(worktree),
                    "requires": "manual recovery after verified cleanup failure",
                },
                repo=str(repo),
                root=str(root),
                worktree=str(worktree),
                head=head,
                expected_head=expected_head,
                disposition=args.disposition,
                registered_before=registered_before,
                registered_after=False,
                directory_exists=True,
                cleanup_method=cleanup_method,
                git_remove="succeeded" if result.returncode == 0 else "failed",
                fallback="failed",
                git_returncode=result.returncode,
                git_error=result.stderr.strip(),
            )
        directory_exists = worktree.exists()
        residual_removed = not directory_exists
        fallback = "succeeded" if residual_removed else "failed"
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
        project_key=project,
        base_root=str(base_root),
        root=str(root),
        worktree=str(worktree),
        state=state,
        head=head,
        expected_head=expected_head,
        disposition=args.disposition,
        git_trust=(
            "command-scoped-safe-directory"
            if "command-scoped-safe-directory" in {repo_trust, remove_trust}
            else "normal"
        ),
        registered_before=registered_before,
        registered_after=registered_after,
        directory_exists=directory_exists,
        residual_removed=residual_removed,
        cleanup_method=cleanup_method,
        git_remove="succeeded" if result.returncode == 0 else "failed",
        fallback=fallback,
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


def purge_residual_packet(args: argparse.Namespace) -> dict[str, Any]:
    repo, _ = git_root(Path(args.repo).resolve())
    project = project_key(args.project_key)
    base_root = Path(args.base_root).resolve()
    project_root, root = project_paths(base_root, project)
    ensure_project_marker(repo, project_root, project)
    worktree = Path(args.worktree).resolve()
    if not args.confirm_unregistered_residual:
        raise LaneError("explicit residual-cleanup confirmation is required")
    if not contains(root, worktree):
        raise LaneError("residual path is outside the recorded worktree root")
    require_lane_identity(project, root, worktree, args.run_id, args.item_id)
    if worktree in registered_worktrees(repo):
        raise LaneError("residual path is still registered as a Git worktree")
    if worktree.exists():
        shutil.rmtree(extended_path(worktree))
    return result_packet(
        "cleanup",
        not worktree.exists(),
        repo=str(repo),
        project_key=project,
        base_root=str(base_root),
        root=str(root),
        worktree=str(worktree),
        state="removed" if not worktree.exists() else "unregistered-residual-directory",
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    open_parser = commands.add_parser("open")
    open_parser.add_argument("--repo", required=True)
    open_parser.add_argument("--project-key", required=True)
    open_parser.add_argument("--base-root")
    open_parser.add_argument("--base", required=True)
    open_parser.add_argument("--run-id", required=True)
    open_parser.add_argument("--item-id", required=True)
    open_parser.add_argument("--actor-id", required=True)
    open_parser.add_argument("--branch")
    open_parser.add_argument("--allow-inside-repo", action="store_true")
    open_proof = open_parser.add_mutually_exclusive_group()
    open_proof.add_argument("--proof-command-json")
    open_proof.add_argument("--proof-command-file")
    open_proof.add_argument("--skip-proof", action="store_true")
    open_parser.add_argument("--reason")
    open_provenance = open_parser.add_mutually_exclusive_group()
    open_provenance.add_argument("--python-provenance-file")
    open_provenance.add_argument("--skip-python-provenance", action="store_true")
    open_parser.add_argument("--python-provenance-reason")
    open_parser.set_defaults(handler=open_lane)

    cleanup_parser = commands.add_parser("cleanup")
    cleanup_parser.add_argument("--repo", required=True)
    cleanup_parser.add_argument("--project-key", required=True)
    cleanup_parser.add_argument("--base-root", required=True)
    cleanup_parser.add_argument("--worktree", required=True)
    cleanup_parser.add_argument("--run-id", required=True)
    cleanup_parser.add_argument("--item-id", required=True)
    cleanup_parser.add_argument("--expected-head", required=True)
    cleanup_parser.add_argument("--disposition", required=True)
    cleanup_parser.add_argument("--confirm-unregistered-residual", action="store_true")
    cleanup_parser.set_defaults(handler=cleanup)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (LaneError, OSError, json.JSONDecodeError) as error:
        return blocked(
            args.command,
            state="blocked-error",
            error=str(error),
            recoverable=True,
            next_action={"command": args.command, "repair": "inspect the returned error and retry only after its cause changes"},
        )


if __name__ == "__main__":
    raise SystemExit(main())
