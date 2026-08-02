from __future__ import annotations

import argparse
import hashlib
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT / "skills/custom/parallel-implement/scripts/lane_worktree.py"
LEDGER = ROOT / "skills/custom/parallel-implement/scripts/run_ledger.py"
LEDGER_RUNTIME = runpy.run_path(str(LEDGER))
LANE_RUNTIME = runpy.run_path(str(LANE))
PROJECT_KEY = "repo-001"


def internal_lane_packet(args: tuple[str, ...]) -> tuple[subprocess.CompletedProcess[str], dict]:
    operation = args[0]
    parser = argparse.ArgumentParser()
    if operation == "create":
        parser.add_argument("--repo", required=True)
        parser.add_argument("--project-key", required=True)
        parser.add_argument("--base-root")
        parser.add_argument("--base", required=True)
        parser.add_argument("--run-id", required=True)
        parser.add_argument("--item-id", required=True)
        parser.add_argument("--branch")
        parser.add_argument("--allow-inside-repo", action="store_true")
        packet = LANE_RUNTIME["create_packet"](parser.parse_args(args[1:]))
    elif operation == "preflight":
        parser.add_argument("--repo", required=True)
        parser.add_argument("--worktree", required=True)
        parser.add_argument("--base", required=True)
        parser.add_argument("--actor-id", required=True)
        parser.add_argument("--expect-branch")
        proof = parser.add_mutually_exclusive_group()
        proof.add_argument("--proof-command-json")
        proof.add_argument("--proof-command-file")
        proof.add_argument("--skip-proof", action="store_true")
        parser.add_argument("--reason")
        provenance = parser.add_mutually_exclusive_group()
        provenance.add_argument("--python-provenance-file")
        provenance.add_argument("--skip-python-provenance", action="store_true")
        parser.add_argument("--python-provenance-reason")
        packet = LANE_RUNTIME["preflight_packet"](parser.parse_args(args[1:]))
    else:
        raise AssertionError(f"unsupported internal lane operation: {operation}")
    return subprocess.CompletedProcess([], 0 if packet["ok"] else 1), packet


def command(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def helper(
    script: Path, *args: str, env: dict[str, str] | None = None
) -> tuple[subprocess.CompletedProcess[str], dict]:
    if script == LANE and args and args[0] in {"create", "open", "cleanup"}:
        args = (args[0], "--project-key", PROJECT_KEY, *args[1:])
    if script == LANE and args and args[0] in {"create", "preflight"}:
        prior_root = os.environ.get("PARALLEL_IMPLEMENT_BASE_ROOT")
        requested_root = (
            env.get("PARALLEL_IMPLEMENT_BASE_ROOT") if env is not None else prior_root
        )
        try:
            if requested_root is None:
                os.environ.pop("PARALLEL_IMPLEMENT_BASE_ROOT", None)
            else:
                os.environ["PARALLEL_IMPLEMENT_BASE_ROOT"] = requested_root
            return internal_lane_packet(args)
        except (LANE_RUNTIME["LaneError"], OSError, json.JSONDecodeError) as error:
            packet = LANE_RUNTIME["result_packet"](
                args[0],
                False,
                state="blocked-error",
                error=str(error),
                recoverable=True,
            )
            return subprocess.CompletedProcess([], 1), packet
        finally:
            if prior_root is None:
                os.environ.pop("PARALLEL_IMPLEMENT_BASE_ROOT", None)
            else:
                os.environ["PARALLEL_IMPLEMENT_BASE_ROOT"] = prior_root
    result = subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    packet = json.loads(result.stdout)
    return result, packet


def append_event(events: Path, event: dict) -> dict:
    normalized = LEDGER_RUNTIME["normalize_event"](event)
    prior = LEDGER_RUNTIME["load_events"](events)
    LEDGER_RUNTIME["validate_events"]([*prior, normalized])
    LEDGER_RUNTIME["append_encoded"](events, [normalized])
    return normalized


def repository(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    command("git", "init", "-b", "main", cwd=repo)
    command("git", "config", "user.name", "Skill Tests", cwd=repo)
    command("git", "config", "user.email", "skills@example.test", cwd=repo)
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "base", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    return repo, base


def create_lane(repo: Path, base: str, base_root: Path, item: str = "ticket-1") -> dict:
    result, packet = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base-root",
        str(base_root),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        item,
    )
    assert result.returncode == 0, packet
    assert packet["ok"] is True
    return packet


def test_lane_open_creates_and_preflights_one_recoverable_lane(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    result, opened = helper(
        LANE,
        "open",
        "--repo",
        str(repo),
        "--base-root",
        str(tmp_path / "lanes"),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )

    assert result.returncode == 0, opened
    assert opened["state"] == "ready"
    assert opened["lane"]["ok"] is True
    assert opened["preflight"]["ok"] is True
    assert Path(opened["worktree"]).is_dir()

    cleanup_result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        opened["base_root"],
        "--worktree",
        opened["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert cleanup_result.returncode == 0, cleanup


def test_lane_open_exposes_root_inputs_read_only_without_copying(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    (repo / ".gitignore").write_text("raw/\n", encoding="utf-8")
    command("git", "add", ".gitignore", cwd=repo)
    command("git", "commit", "-m", "ignore raw inputs", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    raw = repo / "raw/source.txt"
    raw.parent.mkdir()
    raw.write_text("root-only\n", encoding="utf-8")
    proof = [
        sys.executable,
        "-c",
        (
            "import json, os, pathlib; "
            "root = pathlib.Path(os.environ['PARALLEL_IMPLEMENT_ROOT_CHECKOUT']); "
            "print(json.dumps({'cwd': str(pathlib.Path.cwd()), "
            "'root': str(root), 'raw': (root / 'raw/source.txt').read_text()}))"
        ),
    ]

    result, opened = helper(
        LANE,
        "open",
        "--repo",
        str(repo),
        "--base-root",
        str(tmp_path / "lanes"),
        "--base",
        base,
        "--run-id",
        "run-inputs",
        "--item-id",
        "ticket-inputs",
        "--actor-id",
        "worker-inputs",
        "--proof-command-json",
        json.dumps(proof),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )

    assert result.returncode == 0, opened
    observed = json.loads(opened["preflight"]["startup_proof"]["stdout"])
    assert Path(observed["cwd"]) == Path(opened["worktree"])
    assert Path(observed["root"]) == repo.resolve()
    assert observed["raw"] == "root-only\n"
    assert opened["preflight"]["root_checkout"] == {
        "path": str(repo.resolve()),
        "access": "read-only",
        "environment": "PARALLEL_IMPLEMENT_ROOT_CHECKOUT",
    }
    assert not (Path(opened["worktree"]) / "raw/source.txt").exists()

    cleanup_result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        opened["base_root"],
        "--worktree",
        opened["worktree"],
        "--run-id",
        "run-inputs",
        "--item-id",
        "ticket-inputs",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert cleanup_result.returncode == 0, cleanup
    assert raw.read_text(encoding="utf-8") == "root-only\n"


def test_lane_open_preserves_created_lane_when_preflight_fails(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    result, opened = helper(
        LANE,
        "open",
        "--repo",
        str(repo),
        "--base-root",
        str(tmp_path / "lanes"),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "raise SystemExit(7)"]),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )

    assert result.returncode == 1
    assert opened["state"] == "created-preflight-blocked"
    assert opened["recoverable"] is True
    assert Path(opened["worktree"]).is_dir()
    assert opened["next_action"]["command"] == "open"

    result, retried = helper(
        LANE,
        "open",
        "--repo",
        str(repo),
        "--base-root",
        str(tmp_path / "lanes"),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('recovered')"]),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )
    assert result.returncode == 0, retried
    assert retried["state"] == "ready"
    assert retried["lane"]["reused"] is True

    cleanup_result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        opened["base_root"],
        "--worktree",
        opened["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "preserved",
    )
    assert cleanup_result.returncode == 0, cleanup


def test_ledger_facade_starts_applies_reports_and_briefs_idempotently(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "run" / "events.jsonl"
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
                {
                    "parent": "parent",
                    "root_actor_id": "root-agent",
                    "caller_id": "caller",
                    "parent_claim": {
                        "state": "retained",
                        "work_item": "parent",
                        "owner": "root-agent",
                        "token": "claim-parent",
                        "readback": "retained",
                    },
                    "children": ["ticket-1"],
                "charter": {
                    "id": "parent-charter",
                    "outcome": "deliver the recorded child graph",
                },
            }
        ),
        encoding="utf-8",
    )

    result, started = helper(
        LEDGER,
        "start",
        "--run",
        str(events.parent),
        "--repo",
        str(repo),
        "--in",
        str(scope),
    )
    assert result.returncode == 0, started
    assert started["phase"] == "select"
    assert started["awaiting"]["action"] == "select-frontier"
    recorded_scope = json.loads(events.read_text(encoding="utf-8").splitlines()[0])
    assert recorded_scope["integration_sha"] == base
    assert recorded_scope["data"]["charter"] == {
        "id": "parent-charter",
        "outcome": "deliver the recorded child graph",
        "repair_generation_budget": 2,
        "runtime_contract": 6,
    }

    packet = tmp_path / "lane-ready.json"
    packet.write_text(
        json.dumps(
            {
                "kind": "lane-ready",
                "work_item": "ticket-1",
                "lane_id": "lane-1",
                "agent_id": "clear-worker",
                "runtime_agent_type": "luna_max",
                "actor_id": "worker-1",
                "task_id": "task-1",
                "transport": "subagent-v2",
                "requested_model": "gpt-5.6-luna",
                "requested_effort": "max",
                "environment": "worktree",
                "task_state": "ready",
                "report_transport": "subagent-v2",
                "liveness_cursor": "cursor-1",
                "assignment": {
                    "mode": "implementation",
                    "ref": "ticket-1",
                    "root_receipt": root_receipt("assign", "ticket-1", base),
                },
                "create": {
                    "state": "created",
                    "task_id_state": "canonical",
                    "provider_acceptance": {
                        "status": "accepted",
                        "lane_id": "lane-1",
                        "agent_id": "clear-worker",
                        "runtime_agent_type": "luna_max",
                        "task_id": "task-1",
                        "requested_model": "gpt-5.6-luna",
                        "requested_effort": "max",
                        "environment": "worktree",
                        "provider": "manual-helper",
                        "worktree": str(tmp_path / "lane-1"),
                    },
                    "environment_match": True,
                    "resolved_model_status": "matched",
                    "resolved_model": "gpt-5.6-luna",
                    "resolved_effort_status": "matched",
                    "resolved_effort": "max",
                },
                "preflight": {
                    "base": base,
                    "observed_head": base,
                    "status": "clean",
                    "worktree": str(tmp_path / "lane-1"),
                    "root_checkout": {
                        "path": str(repo.resolve()),
                        "access": "read-only",
                        "environment": "PARALLEL_IMPLEMENT_ROOT_CHECKOUT",
                    },
                    "provider": "manual-helper",
                    "startup_proof": {"status": "passed"},
                    "project_provenance": {"status": "verified"},
                    "temp_root": str(tmp_path / "lane-1" / ".tmp"),
                    "pytest_basetemp": str(tmp_path / "lane-1" / ".pytest"),
                    "cache_root": str(tmp_path / "lane-1" / ".cache"),
                },
            }
        ),
        encoding="utf-8",
    )
    lane_ready = json.loads(packet.read_text(encoding="utf-8"))
    lane_create = LEDGER_RUNTIME["packet_events"](lane_ready)[0]
    lane_ready["assignment"]["root_receipt"] = root_receipt(
        "assign", "ticket-1", base, lane_create["data"]
    )
    packet.write_text(json.dumps(lane_ready), encoding="utf-8")
    result, applied = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(packet),
    )
    assert result.returncode == 0, applied
    assert applied["receipt"]["applied"] == 2
    first_count = len(events.read_text(encoding="utf-8").splitlines())

    result, replayed = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(packet),
    )
    assert result.returncode == 0, replayed
    assert replayed["receipt"]["applied"] == 0
    assert replayed["receipt"]["replayed"] == 2
    assert len(events.read_text(encoding="utf-8").splitlines()) == first_count

    result, state = helper(
        LEDGER,
        "status",
        "--run",
        str(events.parent),
    )
    assert result.returncode == 0, state
    assert state["phase"] == "open"
    assert state["awaiting"]["action"] == "dispatch"
    projection = json.loads(Path(state["state"]).read_text(encoding="utf-8"))
    assert projection["items"]["ticket-1"] == "ready"

    brief = tmp_path / "WORKER.md"
    result, generated = helper(
        LEDGER,
        "brief",
        "--run",
        str(events.parent),
        "--item",
        "ticket-1",
    )
    assert result.returncode == 0, generated
    brief = Path(generated["artifact"])
    text = brief.read_text(encoding="utf-8")
    assert "Mode: `implementation`" in text
    assert "Agent: `clear-worker`" in text
    assert "Actor: `worker-1`" in text
    assert "Task: `task-1`" in text
    assert f"Root checkout: `{recorded_scope['data']['repo']}`" in text
    assert "Root checkout access: `read-only`" in text
    assert "Write boundary: `assigned worktree only`" in text
    assert "Host:" not in text
    assert "Integration correction" not in text
    assert "Do not integrate" not in text


    result_packet = tmp_path / "worker-result.json"
    result_packet.write_text(
        json.dumps(
            {
                "kind": "worker-result",
                "work_item": "ticket-1",
                "lane_id": "lane-1",
                "agent_id": "clear-worker",
                "runtime_agent_type": "luna_max",
                "actor_id": "worker-1",
                "task_id": "task-1",
                "transport": "subagent-v2",
                "worktree": str(tmp_path / "lane-1"),
                "base": base,
                "assignment_ref": "ticket-1",
                "report": {
                    "status": "done",
                    "commit": base,
                    "changed_scope_ids": ["ticket-1"],
                    "actual_changed_files": ["tracked.txt"],
                    "acceptance_proof": "criterion -> evidence",
                    "test_portfolio_delta": "unchanged",
                    "commands_and_results": ["focused proof passed"],
                    "skipped_checks": [],
                    "risk_or_blocker": "none",
                    "next_need": "root acceptance",
                    "scope_notes": "bounded",
                    "final_status": "complete",
                },
            }
        ),
        encoding="utf-8",
    )
    result, handed_off = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(result_packet),
    )
    assert result.returncode == 0, handed_off

    changed_return = json.loads(result_packet.read_text(encoding="utf-8"))
    changed_return["report"]["final_status"] = "changed retry"
    result_packet.write_text(json.dumps(changed_return), encoding="utf-8")
    result, rejected_retry = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(result_packet),
    )
    assert result.returncode == 1
    retry_detail = json.loads(
        Path(rejected_retry["detail"]).read_text(encoding="utf-8")
    )
    assert "different payload" in retry_detail["error"]

    mismatched = json.loads(result_packet.read_text(encoding="utf-8"))
    mismatched["report"]["final_status"] = "complete"
    mismatched["task_id"] = "task-other"
    result_packet.write_text(json.dumps(mismatched), encoding="utf-8")
    result, rejected = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(result_packet),
    )
    assert result.returncode == 1
    detail = json.loads(Path(rejected["detail"]).read_text(encoding="utf-8"))
    assert "mismatched task_id" in detail["error"]


def test_runtime_profile_resolver_emits_exact_collaboration_arguments() -> None:
    result, clear = helper(LEDGER, "profile", "--id", "clear-worker")
    assert result.returncode == 0
    assert clear["spawn"] == {"agent_type": "luna_max"}
    assert (clear["model"], clear["reasoning"]) == ("gpt-5.6-luna", "max")

    result, adaptive = helper(LEDGER, "profile", "--id", "adaptive-worker")
    assert result.returncode == 0
    assert adaptive["spawn"] == {
        "agent_type": "default",
        "model": "gpt-5.6-terra",
        "reasoning_effort": "xhigh",
    }

    result, missing = helper(LEDGER, "profile", "--id", "unknown-worker")
    assert result.returncode == 1
    assert missing["code"] == "UNKNOWN_PROFILE"


def test_runtime_six_rejects_lane_ready_without_task_receipt(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    events = tmp_path / "run" / "events.jsonl"
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "parent": "parent",
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "children": ["ticket-1"],
                "charter": {"id": "parent-charter", "outcome": "deliver"},
            }
        ),
        encoding="utf-8",
    )
    result, started = helper(
        LEDGER,
        "start",
        "--run",
        str(events.parent),
        "--repo",
        str(repo),
        "--in",
        str(scope),
    )
    assert result.returncode == 0, started

    packet = tmp_path / "lane-ready.json"
    packet.write_text(
        json.dumps(
            {
                "kind": "lane-ready",
                "work_item": "ticket-1",
                "lane_id": "lane-1",
                "actor_id": "worker-1",
                "assignment": {
                    "mode": "implementation",
                    "ref": "ticket-1",
                    "root_receipt": root_receipt("assign", "ticket-1", ""),
                },
            }
        ),
        encoding="utf-8",
    )
    result, rejected = helper(
        LEDGER,
        "apply",
        "--run",
        str(events.parent),
        "--in",
        str(packet),
    )
    assert result.returncode == 1
    detail = json.loads(Path(rejected["detail"]).read_text(encoding="utf-8"))
    assert "task receipt" in detail["error"]


@pytest.mark.skipif(os.name != "nt", reason="Windows manual-lane default")
def test_lane_helper_defaults_to_the_repository_drive_project_worktree_root() -> None:
    lane = runpy.run_path(str(LANE))
    repository_root = Path("C:/repo")
    expected_base = Path("C:/pi").resolve()
    project_root, root = lane["project_paths"](expected_base, PROJECT_KEY)

    assert lane["default_base_root"](repository_root) == expected_base
    assert project_root == expected_base / PROJECT_KEY
    assert root == expected_base / PROJECT_KEY / "wt"


@pytest.mark.skipif(os.name != "nt", reason="Windows path-budget default")
def test_lane_helper_uses_the_259_character_windows_path_limit(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    lane = runpy.run_path(str(LANE))

    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    worktree = Path(f"{repo.drive}/pi/lane")
    budget = lane["path_budget"](worktree, repo, base)

    assert budget["limit"] == 259
    assert budget["checkout_projection"] == len(str(worktree)) + 1 + len("tracked.txt")


def test_lane_path_budget_uses_the_selected_base_not_the_current_index(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    base_path = Path("base") / ("b" * 48)
    (repo / base_path).parent.mkdir()
    (repo / base_path).write_text("base\n", encoding="utf-8")
    command("git", "add", str(base_path), cwd=repo)
    command("git", "commit", "-m", "add base path", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()

    (repo / base_path).unlink()
    index_path = Path("index") / ("i" * 80)
    (repo / index_path).parent.mkdir()
    (repo / index_path).write_text("index\n", encoding="utf-8")
    command("git", "add", "-A", cwd=repo)

    lane = runpy.run_path(str(LANE))
    worktree = tmp_path / "lane"
    budget = lane["path_budget"](worktree, repo, base)

    assert budget["longest_tracked_relative_path"] == len(base_path.as_posix())
    assert budget["longest_tracked_relative_path"] != len(index_path.as_posix())
    assert budget["checkout_projection"] == len(str(worktree)) + 1 + len(
        base_path.as_posix()
    )
    assert "reserve" not in budget


def test_lane_helper_creates_preflights_and_removes_a_detached_worktree(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    created = create_lane(repo, base, tmp_path / "lanes")
    worktree = Path(created["worktree"])

    result, preflight = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        str(worktree),
        "--base",
        base,
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )
    assert result.returncode == 0, preflight
    assert preflight["detached"] is True
    assert preflight["status"] == "clean"
    assert set(preflight["probes"].values()) == {"passed"}
    assert preflight["startup_proof"]["returncode"] == 0
    assert preflight["git_trust"] in {"normal", "command-scoped-safe-directory"}
    assert Path(preflight["temp_root"]).is_dir()
    assert Path(preflight["pytest_basetemp"]).is_dir()
    assert Path(preflight["cache_root"]).is_dir()

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        str(worktree),
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup
    assert cleanup["state"] == "removed"
    assert cleanup["registered_after"] is False
    assert cleanup["directory_exists"] is False


def test_lane_preflight_accepts_a_utf8_argv_file_with_provenance(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    created = create_lane(repo, base, tmp_path / "lanes")
    proof_file = tmp_path / "proof-command.json"
    proof_bytes = json.dumps(
        [sys.executable, "-c", "print('file-started')"]
    ).encode("utf-8")
    proof_file.write_bytes(proof_bytes)

    result, preflight = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-file",
        "--proof-command-file",
        str(proof_file),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )
    assert result.returncode == 0, preflight
    proof = preflight["startup_proof"]
    assert proof["returncode"] == 0
    assert proof["command_file"] == str(proof_file.resolve())
    assert proof["command_file_sha256"] == hashlib.sha256(proof_bytes).hexdigest()

    bom_proof_file = tmp_path / "proof-command-bom.json"
    bom_proof_bytes = b"\xef\xbb\xbf" + proof_bytes
    bom_proof_file.write_bytes(bom_proof_bytes)
    result, bom_preflight = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-file-bom",
        "--proof-command-file",
        str(bom_proof_file),
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )
    assert result.returncode == 0, bom_preflight
    bom_proof = bom_preflight["startup_proof"]
    assert bom_proof["returncode"] == 0
    assert bom_proof["command_file_sha256"] == hashlib.sha256(
        bom_proof_bytes
    ).hexdigest()

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_preflight_verifies_declared_python_packages_resolve_beneath_lane(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    package = repo / "src/example_package"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    namespace = repo / "src/example_namespace"
    namespace.mkdir(parents=True)
    (namespace / "module.py").write_text("VALUE = 2\n", encoding="utf-8")
    command(
        "git",
        "add",
        "src/example_package/__init__.py",
        "src/example_namespace/module.py",
        cwd=repo,
    )
    command("git", "commit", "-m", "add example package", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    created = create_lane(repo, base, tmp_path / "lanes")
    provenance_file = tmp_path / "python-provenance.json"
    provenance_bytes = json.dumps(
        {
            "executable": sys.executable,
            "import_roots": ["src"],
            "packages": ["example_package", "example_namespace"],
        }
    ).encode("utf-8")
    provenance_file.write_bytes(provenance_bytes)

    result, preflight = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-python",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
        "--python-provenance-file",
        str(provenance_file),
    )

    assert result.returncode == 0, preflight
    provenance = preflight["project_provenance"]
    assert provenance["configuration_file"] == str(provenance_file.resolve())
    assert provenance["configuration_sha256"] == hashlib.sha256(
        provenance_bytes
    ).hexdigest()
    assert provenance["packages"] == ["example_package", "example_namespace"]
    assert provenance["import_roots"] == [
        str((Path(created["worktree"]) / "src").resolve())
    ]
    resolved = provenance["resolved_packages"]["example_package"]
    assert resolved
    assert all(Path(path).is_relative_to(Path(created["worktree"])) for path in resolved)
    namespace_paths = provenance["resolved_packages"]["example_namespace"]
    assert namespace_paths == [
        str((Path(created["worktree"]) / "src/example_namespace").resolve())
    ]


def test_lane_preflight_rejects_python_provenance_outside_the_lane(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    created = create_lane(repo, base, tmp_path / "lanes")
    provenance_file = tmp_path / "python-provenance.json"
    provenance_file.write_text(
        json.dumps(
            {
                "executable": sys.executable,
                "import_roots": ["../outside"],
                "packages": ["example_package"],
            }
        ),
        encoding="utf-8",
    )

    result, blocked = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-python",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
        "--python-provenance-file",
        str(provenance_file),
    )

    assert result.returncode == 1
    assert "import root escapes the lane" in blocked["error"]


def test_lane_base_root_precedence_uses_explicit_then_environment_then_default(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    environment_root = tmp_path / "environment-lanes"
    explicit_root = tmp_path / "explicit-lanes"
    env = {**os.environ, "PARALLEL_IMPLEMENT_BASE_ROOT": str(environment_root)}

    result, created = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base-root",
        str(explicit_root),
        "--base",
        base,
        "--run-id",
        "run-explicit",
        "--item-id",
        "ticket-explicit",
        env=env,
    )
    assert result.returncode == 0, created
    assert Path(created["base_root"]) == explicit_root.resolve()
    assert Path(created["root"]) == explicit_root.resolve() / PROJECT_KEY / "wt"
    assert created["base_root_source"] == "explicit"
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-explicit",
        "--item-id",
        "ticket-explicit",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup

    result, created = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base",
        base,
        "--run-id",
        "run-environment",
        "--item-id",
        "ticket-environment",
        env=env,
    )
    assert result.returncode == 0, created
    assert Path(created["base_root"]) == environment_root.resolve()
    assert Path(created["root"]) == environment_root.resolve() / PROJECT_KEY / "wt"
    assert created["base_root_source"] == "environment"
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-environment",
        "--item-id",
        "ticket-environment",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_project_key_owns_one_repository_and_short_worktree_root(
    tmp_path: Path,
) -> None:
    first_parent = tmp_path / "first"
    second_parent = tmp_path / "second"
    first_parent.mkdir()
    second_parent.mkdir()
    first_repo, first_base = repository(first_parent)
    second_repo, second_base = repository(second_parent)
    command(
        "git",
        "remote",
        "add",
        "origin",
        "https://example.test/first.git",
        cwd=first_repo,
    )
    command(
        "git",
        "remote",
        "add",
        "origin",
        "https://example.test/second.git",
        cwd=second_repo,
    )
    base_root = tmp_path / "pi"

    created = create_lane(first_repo, first_base, base_root)
    assert Path(created["project_root"]) == base_root / PROJECT_KEY
    assert Path(created["root"]) == base_root / PROJECT_KEY / "wt"
    assert Path(created["worktree"]).parent == Path(created["root"])
    assert first_repo.name not in Path(created["worktree"]).name

    result, blocked = helper(
        LANE,
        "create",
        "--repo",
        str(second_repo),
        "--base-root",
        str(base_root),
        "--base",
        second_base,
        "--run-id",
        "run-2",
        "--item-id",
        "ticket-2",
    )
    assert result.returncode == 1
    assert "belongs to another repository" in blocked["error"]

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(first_repo),
        "--base-root",
        str(base_root),
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        first_base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_preflight_requires_proof_or_an_explicit_skip(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    created = create_lane(repo, base, tmp_path / "lanes")

    result, blocked = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-1",
    )
    assert result.returncode == 1
    assert blocked["state"] == "blocked-proof"
    assert blocked["recoverable"] is True
    assert blocked["next_action"]

    result, provenance_blocked = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
    )
    assert result.returncode == 1
    assert provenance_blocked["state"] == "blocked-provenance"

    result, skipped = helper(
        LANE,
        "preflight",
        "--repo",
        str(repo),
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-1",
        "--skip-proof",
        "--reason",
        "repository has no startup proof command",
        "--skip-python-provenance",
        "--python-provenance-reason",
        "test repository has no importable project package",
    )
    assert result.returncode == 0, skipped
    assert skipped["startup_proof"]["skipped"] is True
    assert skipped["startup_proof"]["reason"]

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base[:8],
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup
    assert cleanup["expected_head"] == base


def test_lane_creation_stops_on_failure_and_rejects_unsafe_roots(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"

    result, failed = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base-root",
        str(lane_root),
        "--base",
        "missing-base",
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
    )
    assert result.returncode == 1
    assert failed["operation"] == "create"
    assert failed["ok"] is False
    assert not Path(failed["worktree"]).exists()

    result, nested = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base-root",
        str(repo / "nested"),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-2",
    )
    assert result.returncode == 1
    assert "inside the active checkout" in nested["error"]

    lane = runpy.run_path(str(LANE))
    limit = lane["WINDOWS_USABLE_MAX_PATH"] if os.name == "nt" else 4096
    with pytest.raises(lane["LaneError"], match="checkout path limit exceeded"):
        lane["path_budget"](Path("x" * limit), repo, base)

    created = create_lane(repo, base, lane_root, item="ticket-with-a-long-name")
    assert created["path_budget"]["checkout_projection"] == (
        len(created["worktree"]) + 1 + len("tracked.txt")
    )
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-with-a-long-name",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_cleanup_records_and_purges_an_unregistered_residual(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    created = create_lane(repo, base, lane_root)
    worktree = Path(created["worktree"])
    command("git", "worktree", "remove", str(worktree), cwd=repo)
    worktree.mkdir(parents=True)
    (worktree / "residual.txt").write_text("residual\n", encoding="utf-8")

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        str(lane_root),
        "--worktree",
        str(worktree),
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 1
    assert cleanup["state"] == "unregistered-residual-directory"

    result, purged = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        str(lane_root),
        "--worktree",
        str(worktree),
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
        "--confirm-unregistered-residual",
    )
    assert result.returncode == 0, purged
    assert purged["state"] == "removed"
    assert not worktree.exists()


def test_lane_cleanup_rejects_an_unrelated_contained_directory(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    created = create_lane(repo, base, lane_root)
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        created["base_root"],
        "--worktree",
        created["worktree"],
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup
    unrelated = Path(created["root"]) / "unrelated"
    unrelated.mkdir(parents=True)
    marker = unrelated / "keep.txt"
    marker.write_text("keep\n", encoding="utf-8")

    result, blocked = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        str(lane_root),
        "--worktree",
        str(unrelated),
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "preserved",
        "--confirm-unregistered-residual",
    )

    assert result.returncode == 1
    assert "does not match the helper-created lane identity" in blocked["error"]
    assert marker.read_text(encoding="utf-8") == "keep\n"


def test_lane_cleanup_requires_the_existing_project_binding(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    base_root = tmp_path / "missing-lanes"
    worktree = (
        base_root
        / PROJECT_KEY
        / "wt"
        / LANE_RUNTIME["lane_name"](PROJECT_KEY, "run-1", "ticket-1")
    )

    result, blocked = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--base-root",
        str(base_root),
        "--worktree",
        str(worktree),
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--expected-head",
        base,
        "--disposition",
        "preserved",
    )

    assert result.returncode == 1
    assert "has no identity marker" in blocked["error"]
    assert not base_root.exists()


@pytest.mark.parametrize("removal_fails", [False, True])
def test_lane_cleanup_reports_verified_residual_recovery_in_the_same_call(
    tmp_path: Path, monkeypatch, capsys, removal_fails: bool
) -> None:
    namespace = runpy.run_path(str(LANE))
    cleanup = namespace["cleanup"]
    globals_ = cleanup.__globals__
    repo = tmp_path / "repo"
    base_root = tmp_path / "lanes"
    root = base_root / PROJECT_KEY / "wt"
    run_id = "run-1"
    item_id = "ticket-1"
    worktree = root / namespace["lane_name"](PROJECT_KEY, run_id, item_id)
    worktree.mkdir(parents=True)
    (worktree / "generated-path.txt").write_text("residual\n", encoding="utf-8")
    head = "a" * 40
    registrations = iter(({worktree.resolve(): {"HEAD": head}}, {}))

    monkeypatch.setitem(globals_, "git_root", lambda path: (repo.resolve(), "normal"))
    monkeypatch.setitem(
        globals_, "ensure_project_marker", lambda *args, **kwargs: {}
    )
    monkeypatch.setitem(globals_, "registered_worktrees", lambda path: next(registrations))

    def fake_worktree_git(path, args, *, check=True):
        stdout = "" if args[0] == "status" else f"{head}\n"
        return subprocess.CompletedProcess(args, 0, stdout, ""), "normal"

    monkeypatch.setitem(globals_, "git_with_trust", fake_worktree_git)
    monkeypatch.setitem(
        globals_,
        "git_repo_with_trust",
        lambda path, args, check=False: (
            subprocess.CompletedProcess(args, 1, "", "Filename too long"),
            "normal",
        ),
    )
    if removal_fails:
        def fail_removal(path):
            raise OSError("extended path cleanup failed")

        monkeypatch.setattr(globals_["shutil"], "rmtree", fail_removal)

    result = cleanup(
        argparse.Namespace(
            repo=str(repo),
            project_key=PROJECT_KEY,
            base_root=str(base_root),
            worktree=str(worktree),
            run_id=run_id,
            item_id=item_id,
            expected_head=head[:8],
            disposition="integrated",
        )
    )
    packet = json.loads(capsys.readouterr().out)
    if removal_fails:
        assert result == 1
        assert packet["state"] == "unregistered-residual-directory"
        assert packet["recoverable"] is True
        assert packet["next_action"]["command"] == "inspect-residual"
        assert worktree.exists()
    else:
        assert result == 0, packet
        assert packet["state"] == "removed"
        assert packet["registered_after"] is False
        assert packet["residual_removed"] is True
        assert packet["cleanup_method"] == "extended-path-fallback"
        assert packet["git_remove"] == "failed"
        assert packet["fallback"] == "succeeded"
        assert packet["git_error"] == "Filename too long"
        assert not worktree.exists()


def test_lane_helper_never_mutates_global_safe_directory() -> None:
    source = LANE.read_text(encoding="utf-8")
    assert "safe.directory=" in source
    assert "--global" not in source


def test_lane_helper_exposes_only_open_and_cleanup() -> None:
    parser = LANE_RUNTIME["parser"]()
    subparsers = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    assert set(subparsers.choices) == {"open", "cleanup"}


def test_run_ledger_exposes_the_profile_resolver_and_five_campaign_commands() -> None:
    parser = LEDGER_RUNTIME["parser"]()
    subparsers = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    assert set(subparsers.choices) == {
        "profile",
        "start",
        "status",
        "apply",
        "brief",
        "finish",
    }


def test_events_packet_cannot_bypass_the_lane_ready_gate() -> None:
    with pytest.raises(ValueError, match="lane-create must use its dedicated facade"):
        LEDGER_RUNTIME["packet_events"](
            {
                "kind": "events",
                "events": [
                    {"event": "lane-create", "work_item": "ticket-1"},
                    {"event": "lane-preflight", "work_item": "ticket-1"},
                    {"event": "dispatch", "work_item": "ticket-1"},
                ],
            }
        )


def test_run_ledger_syntax_failures_are_compact_json() -> None:
    result = subprocess.run(
        [sys.executable, str(LEDGER), "status"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    packet = json.loads(result.stdout)
    assert result.returncode == 1
    assert packet["code"] == "INPUT_INVALID"
    assert packet["changed"] is False
    assert result.stderr == ""


def test_run_ledger_does_not_report_malformed_existing_stream_as_its_mutation(
    tmp_path: Path,
) -> None:
    run = tmp_path / "malformed"
    run.mkdir()
    (run / "events.jsonl").write_text("not-json\n", encoding="utf-8")

    result, packet = helper(LEDGER, "status", "--run", str(run))

    assert result.returncode == 1
    assert packet["effect_started"] is False
    assert packet["changed"] is False


def test_brief_artifact_names_are_collision_safe() -> None:
    artifact_name = LEDGER_RUNTIME["artifact_name"]
    unsafe = "unsafe/name"
    encoded = artifact_name(unsafe)

    assert artifact_name(encoded) != encoded


def test_runtime_six_resume_accepts_empty_exhaustive_lane_inventories(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = [
        {
            "schema": 1,
            "event_id": "scope",
            "timestamp": "2026-01-01T00:00:00+00:00",
            "event": "scope",
            "work_item": "parent",
            "worker_sha": None,
            "integration_sha": base,
            "validation": None,
            "decision": None,
            "risk": None,
            "data": {
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "children": ["ticket-1"],
                "dispositions": {"ticket-1": "caller-deferred"},
                "charter": {
                    "id": "charter",
                    "runtime_contract": 6,
                    "repair_generation_budget": 2,
                },
            },
        },
        {
            "schema": 1,
            "event_id": "checkpoint",
            "timestamp": "2026-01-01T00:00:01+00:00",
            "event": "checkpoint",
            "work_item": "parent",
            "worker_sha": None,
            "integration_sha": base,
            "validation": None,
            "decision": "partial",
            "risk": None,
            "data": {
                "reason": "bounded stop",
                "continuation": "resume",
                "current_head": base,
                "actors": "idle",
                "integration_state": "clean",
                "next_frontier": [],
                "blockers": [],
                "claims_complete": True,
                    "claims": [
                        {
                            "work_item": "parent",
                            "state": "retained",
                            "owner": "root-agent",
                            "token": "claim-parent",
                            "claimed_at": "2026-01-01T00:00:00+00:00",
                            "recovery_owner": "root-agent",
                            "readback": "retained",
                        }
                    ],
                    "tracker": "unchanged",
                    "root_receipt": root_receipt("checkpoint", "parent", base),
                },
        },
        {
            "schema": 1,
            "event_id": "resume",
            "timestamp": "2026-01-01T00:00:02+00:00",
            "event": "resume",
            "work_item": "parent",
            "worker_sha": None,
            "integration_sha": None,
            "validation": None,
            "decision": None,
            "risk": None,
            "data": {},
        },
        {
            "schema": 1,
            "event_id": "reconcile",
            "timestamp": "2026-01-01T00:00:03+00:00",
            "event": "reconcile",
            "work_item": "parent",
            "worker_sha": None,
            "integration_sha": None,
            "validation": None,
            "decision": None,
            "risk": None,
            "data": {
                "git": {
                    "head": base,
                    "status": "clean",
                    "observed_at": "2026-01-01T00:00:03+00:00",
                },
                "worktrees": [],
                "tasks": [],
                "claims": [
                    {
                        "lane_id": None,
                        "work_item": "parent",
                        "actor_id": "root-agent",
                        "state": "retained",
                        "owner": "root-agent",
                        "token": "claim-parent",
                        "observed_at": "2026-01-01T00:00:03+00:00",
                    }
                ],
                "tracker": {"observed_at": "2026-01-01T00:00:03+00:00"},
            },
        },
    ]
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["resume_pending"] is False

    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    dirty = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert any(
        "Git evidence must match clean live integration HEAD" in error
        for error in dirty["errors"]
    )


def root_receipt(
    action: str,
    subject: str,
    head: str,
    data: dict | None = None,
) -> dict[str, str]:
    return {
        "actor_id": "root-agent",
        "action": action,
        "subject": subject,
        "head": head,
        "receipt_id": f"root-{action}-{subject}",
        "decision_sha256": LEDGER_RUNTIME["root_decision_digest"](
            action, subject, head, data or {}
        ),
    }


def bind_root_receipts(events: list[dict]) -> list[dict]:
    for event in events:
        data = event.get("data")
        receipt = data.get("root_receipt") if isinstance(data, dict) else None
        if isinstance(receipt, dict):
            data["root_receipt"] = root_receipt(
                receipt["action"],
                event["work_item"],
                receipt["head"],
                data,
            )
    return events


def current_review_events(base: str, lane_path: Path) -> list[dict]:
    root_checkout = (lane_path.parent / "repo").resolve()
    review_path = (lane_path.parent / "integration-checkout").resolve()
    lane_receipt = {
        "lane_id": "lane-1",
        "agent_id": "clear-worker",
        "runtime_agent_type": "luna_max",
        "actor_id": "worker-agent",
        "task_id": "worker-task",
        "host_id": "worker-host",
        "transport": "subagent-v2",
        "requested_model": "gpt-5.6-luna",
        "requested_effort": "max",
        "environment": "worktree",
        "task_state": "ready",
        "report_transport": "subagent-v2",
        "liveness_cursor": "worker-cursor",
        "assignment_mode": "implementation",
        "assignment_ref": "ticket-1",
        "root_receipt": root_receipt("assign", "ticket-1", base),
        "task_id_state": "canonical",
        "provider_acceptance": {
            "status": "accepted",
            "lane_id": "lane-1",
            "agent_id": "clear-worker",
            "runtime_agent_type": "luna_max",
            "task_id": "worker-task",
            "host_id": "worker-host",
            "requested_model": "gpt-5.6-luna",
            "requested_effort": "max",
            "environment": "worktree",
            "provider": "manual-helper",
            "worktree": str(lane_path),
        },
        "environment_match": True,
        "resolved_model_status": "matched",
        "resolved_model": "gpt-5.6-luna",
        "resolved_effort_status": "matched",
        "resolved_effort": "max",
    }
    review_receipt = {
        "agent_id": "ordinary-reviewer",
        "runtime_agent_type": "default",
        "lane_id": "review-lane",
        "actor_id": "review-agent",
        "task_id": "review-task",
        "host_id": "review-host",
        "transport": "subagent-v2",
        "requested_model": "gpt-5.6-sol",
        "requested_effort": "high",
        "resolved_model_status": "matched",
        "resolved_model": "gpt-5.6-sol",
        "resolved_effort_status": "matched",
        "resolved_effort": "high",
        "telemetry_unavailable_reason": None,
        "environment": "local",
        "worktree": str(review_path),
        "provider": "delegated-custody",
    }
    events = [
        {
            "event": "scope",
            "event_id": "scope",
            "work_item": "parent",
            "integration_sha": base,
            "data": {
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "children": ["ticket-1"],
                "charter": {
                    "id": "parent-charter",
                    "runtime_contract": 6,
                    "repair_generation_budget": 2,
                },
            },
        },
        {
            "event": "lane-create",
            "event_id": "lane-create",
            "work_item": "ticket-1",
            "data": lane_receipt,
        },
        {
            "event": "lane-preflight",
            "event_id": "lane-preflight",
            "work_item": "ticket-1",
            "data": {
                "lane_id": "lane-1",
                "worktree": str(lane_path),
                "root_checkout": {
                    "path": str(root_checkout),
                    "access": "read-only",
                    "environment": "PARALLEL_IMPLEMENT_ROOT_CHECKOUT",
                },
                "base": base,
                "observed_head": base,
                "provider": "manual-helper",
                "status": "clean",
                "startup_proof": {"status": "passed"},
                "project_provenance": {"status": "verified"},
                "temp_root": str(lane_path / ".tmp"),
                "pytest_basetemp": str(lane_path / ".pytest"),
                "cache_root": str(lane_path / ".cache"),
            },
        },
        {
            "event": "dispatch",
            "event_id": "dispatch",
            "work_item": "ticket-1",
            "data": {
                "lane_id": "lane-1",
                "claim": {
                    "state": "retained",
                    "work_item": "ticket-1",
                    "actor_id": "worker-agent",
                    "owner": "root-agent",
                    "token": "claim-ticket-1",
                    "readback": "claim retained",
                },
                "assignment_sha256": "a" * 64,
                "root_receipt": root_receipt("dispatch", "ticket-1", base),
            },
        },
        {
            "event": "handoff",
            "event_id": "handoff",
            "work_item": "ticket-1",
            "data": {
                **{
                    key: lane_receipt[key]
                    for key in (
                        "lane_id",
                        "agent_id",
                        "runtime_agent_type",
                        "actor_id",
                        "task_id",
                        "host_id",
                        "transport",
                    )
                },
                "assignment_ref": "ticket-1",
                "assignment_sha256": "a" * 64,
                "worktree": str(lane_path),
                "base": base,
                "status": "done",
                "commit": base,
                "changed_scope_ids": ["ticket-1"],
                "actual_changed_files": ["tracked.txt"],
                "acceptance_proof": "criterion -> evidence",
                "test_portfolio_delta": "unchanged",
                "commands_and_results": ["focused proof passed"],
                "skipped_checks": [],
                "risk_or_blocker": "none",
                "next_need": "root acceptance",
                "scope_notes": "bounded",
                "final_status": "complete",
            },
        },
        {
            "event": "accept",
            "event_id": "accept",
            "work_item": "ticket-1",
            "worker_sha": base,
            "data": {
                "root_receipt": root_receipt(
                    "accept-worker-return", "ticket-1", base
                )
            },
        },
        {
            "event": "land",
            "event_id": "land",
            "work_item": "ticket-1",
            "worker_sha": base,
            "integration_sha": base,
            "data": {
                "prior_integration_sha": base,
                "observed_head": base,
                "clean": True,
                "lane_head": base,
                "lane_clean": True,
                "task_state": "completed",
                "liveness_cursor": "worker-complete",
                "root_receipt": root_receipt("land", "ticket-1", base),
            },
        },
        {
            "event": "graph-drained",
            "event_id": "graph-drained",
            "work_item": "parent",
            "integration_sha": base,
            "data": {
                "root_receipt": root_receipt("graph-drained", "parent", base)
            },
        },
        {
            "event": "review-ready",
            "event_id": "review-ready",
            "work_item": "parent",
            "integration_sha": base,
            "data": {
                "tasks": [
                    {
                        "lane_id": "lane-1",
                        "actor_id": "worker-agent",
                        "task_id": "worker-task",
                        "state": "completed",
                        "head": base,
                        "clean": True,
                        "liveness_cursor": "worker-complete",
                    }
                ],
                "integration": {"head": base, "clean": True},
                "final_proof": {
                    "head": base,
                    "status": "passed",
                    "receipt": "final-proof-1",
                },
                "root_receipt": root_receipt("review-ready", "parent", base),
            },
        },
        {
            "event": "review-invocation",
            "event_id": "review-invocation",
            "work_item": "parent",
            "integration_sha": base,
            "data": {
                "mode": "initial",
                "route": "change-review",
                "route_evidence": {
                    "candidate": base,
                    "basis": "ordinary",
                    "source": "recorded candidate risk classification",
                },
                "task_state": "ready",
                "liveness_cursor": "review-cursor",
                "task_id_state": "canonical",
                "provider_acceptance": {
                    "status": "accepted",
                    "lane_id": "review-lane",
                    "agent_id": "ordinary-reviewer",
                    "runtime_agent_type": "default",
                    "task_id": "review-task",
                    "host_id": "review-host",
                    "requested_model": "gpt-5.6-sol",
                    "requested_effort": "high",
                    "environment": "local",
                    "provider": "delegated-custody",
                    "worktree": str(review_path),
                },
                "environment_match": True,
                "resolved_model_status": "matched",
                "resolved_model": "gpt-5.6-sol",
                "resolved_effort_status": "matched",
                "resolved_effort": "high",
                "observed_head": base,
                "status": "clean",
                "startup_proof": {"status": "passed"},
                "project_provenance": {"status": "verified"},
                "temp_root": str((review_path / ".tmp").resolve()),
                "pytest_basetemp": str((review_path / ".pytest").resolve()),
                "cache_root": str((review_path / ".cache").resolve()),
                "root_receipt": root_receipt("select-review", "parent", base),
                **review_receipt,
            },
        },
        {
            "event": "review-decision",
            "event_id": "review-decision",
            "work_item": "parent",
            "integration_sha": base,
            "decision": "pass",
            "data": {
                "review_invocation_id": "review-invocation",
                "mode": "initial",
                "route": "change-review",
                "findings": [],
                "terminal_task_state": "completed",
                "liveness_cursor": "review-final-cursor",
                "reviewed_head": base,
                "clean": True,
                "lane_state": "provider-preserved",
                "custody": "Codex provider retains cleanup custody",
                **review_receipt,
            },
        },
    ]
    return bind_root_receipts(events)


def runtime_six_local_lane_events(
    base: str,
    checkout: Path,
    *,
    agent_id: str,
    model: str,
    effort: str,
    transport: str,
) -> list[dict]:
    events = current_review_events(base, checkout)[:3]
    receipt = events[1]["data"]
    receipt.update(
        {
            "agent_id": agent_id,
            "runtime_agent_type": "luna_max" if agent_id == "clear-worker" else "default",
            "transport": transport,
            "report_transport": transport,
            "requested_model": model,
            "requested_effort": effort,
            "resolved_model": model,
            "resolved_effort": effort,
            "environment": "local",
        }
    )
    receipt["provider_acceptance"].update(
        {
            "agent_id": agent_id,
            "runtime_agent_type": "luna_max" if agent_id == "clear-worker" else "default",
            "requested_model": model,
            "requested_effort": effort,
            "environment": "local",
            "provider": "delegated-custody",
            "worktree": str(checkout),
        }
    )
    events[2]["data"].update(
        {
            "worktree": str(checkout),
            "provider": "delegated-custody",
            "temp_root": str(checkout / ".tmp"),
            "pytest_basetemp": str(checkout / ".pytest"),
            "cache_root": str(checkout / ".cache"),
        }
    )
    events[2]["data"].pop("root_checkout")
    return bind_root_receipts(events)


def test_runtime_six_routes_serial_workers_without_root_implementation(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    cases = (
        ("clear-worker", "gpt-5.6-luna", "max", "subagent-v2"),
        ("adaptive-worker", "gpt-5.6-terra", "xhigh", "subagent-v2"),
        ("fast-adaptive-worker", "gpt-5.6-sol", "medium", "subagent-v2"),
        ("demanding-worker", "gpt-5.6-sol", "high", "subagent-v2"),
    )
    for agent_id, model, effort, transport in cases:
        events = runtime_six_local_lane_events(
            base,
            repo,
            agent_id=agent_id,
            model=model,
            effort=effort,
            transport=transport,
        )
        assert LEDGER_RUNTIME["derive_state"](events, str(repo))["errors"] == []

    leaked_root = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="clear-worker",
        model="gpt-5.6-luna",
        effort="max",
        transport="subagent-v2",
    )
    leaked_root[2]["data"]["root_checkout"] = {
        "path": str(repo),
        "access": "read-only",
        "environment": "PARALLEL_IMPLEMENT_ROOT_CHECKOUT",
    }
    invalid = LEDGER_RUNTIME["derive_state"](leaked_root, str(repo))
    assert any(
        "local lane cannot include a root checkout binding" in error
        for error in invalid["errors"]
    )

    crossed = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="clear-worker",
        model="gpt-5.6-luna",
        effort="xhigh",
        transport="codex-task",
    )
    invalid = LEDGER_RUNTIME["derive_state"](crossed, str(repo))
    assert any("requires subagent-v2 transport" in error for error in invalid["errors"])

    root_actor = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="adaptive-worker",
        model="gpt-5.6-terra",
        effort="xhigh",
        transport="subagent-v2",
    )
    root_actor[1]["data"]["actor_id"] = "root-agent"
    root_actor[1]["data"]["provider_acceptance"]["actor_id"] = "root-agent"
    bind_root_receipts(root_actor)
    invalid = LEDGER_RUNTIME["derive_state"](root_actor, str(repo))
    assert any("root cannot be a worker actor" in error for error in invalid["errors"])


def test_runtime_six_reuses_the_same_lane_for_pre_landing_correction(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    (repo / "tracked.txt").write_text("first return\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "first return", cwd=repo)
    first = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    (repo / "tracked.txt").write_text("corrected return\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "--amend", "-m", "correct returned commit", cwd=repo)
    successor = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()

    events = current_review_events(base, (tmp_path / "lane").resolve())[:5]
    events[0]["data"]["charter"]["runtime_contract"] = 6
    events[3]["data"]["assignment_sha256"] = "a" * 64
    events[4]["data"]["assignment_sha256"] = "a" * 64
    events[4]["data"]["commit"] = first
    feedback_data = {"root_receipt": root_receipt("route-correction", "ticket-1", first)}
    events.append(
        {
            "event": "reject",
            "event_id": "feedback-1",
            "work_item": "ticket-1",
            "worker_sha": first,
            "decision": {
                "return_event_id": "handoff",
                "feedback": "fix the verified local defect",
                "required_proof": "focused proof passes",
            },
            "data": feedback_data,
        }
    )
    corrected_return = {
        **events[4],
        "event_id": "handoff-corrected",
        "data": {
            **events[4]["data"],
            "assignment_ref": "feedback-1",
            "commit": successor,
            "supersedes_commit": first,
        },
    }
    events.extend(
        [
            corrected_return,
            {
                "event": "accept",
                "event_id": "accept-corrected",
                "work_item": "ticket-1",
                "worker_sha": successor,
                "data": {
                    "root_receipt": root_receipt(
                        "accept-worker-return", "ticket-1", successor
                    )
                },
            },
            {
                "event": "land",
                "event_id": "land-corrected",
                "work_item": "ticket-1",
                "worker_sha": successor,
                "integration_sha": successor,
                "data": {
                    "prior_integration_sha": base,
                    "observed_head": successor,
                    "clean": True,
                    "lane_head": successor,
                    "lane_clean": True,
                    "task_state": "idle",
                    "liveness_cursor": "corrected-return",
                    "root_receipt": root_receipt("land", "ticket-1", successor),
                },
            },
        ]
    )
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["items"]["ticket-1"]["accepted"] == successor
    assert state["items"]["ticket-1"]["landed"] == successor

    stale_accept = [
        *events[:6],
        {
            "event": "accept",
            "event_id": "accept-stale-return",
            "work_item": "ticket-1",
            "worker_sha": first,
            "data": {
                "root_receipt": root_receipt(
                    "accept-worker-return", "ticket-1", first
                )
            },
        },
    ]
    bind_root_receipts(stale_accept)
    invalid = LEDGER_RUNTIME["derive_state"](stale_accept, str(repo))
    assert any("feedback requires a corrected successor Return" in error for error in invalid["errors"])

    missing_supersession = [dict(event) for event in events]
    missing_supersession[6] = {
        **missing_supersession[6],
        "data": {
            **missing_supersession[6]["data"],
            "supersedes_commit": None,
        },
    }
    invalid = LEDGER_RUNTIME["derive_state"](missing_supersession, str(repo))
    assert any("must supersede the prior commit" in error for error in invalid["errors"])


def test_runtime_six_serializes_local_workers_and_delegates_integration_correction(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    (repo / "tracked.txt").write_text("first serial landing\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "advance first serial worker", cwd=repo)
    advanced = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    events = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="adaptive-worker",
        model="gpt-5.6-terra",
        effort="xhigh",
        transport="subagent-v2",
    )
    events[0]["data"]["children"] = ["ticket-1", "ticket-2"]
    receipt = events[1]["data"]
    events.extend(
        [
            {
                "event": "dispatch",
                "event_id": "dispatch-1",
                "work_item": "ticket-1",
                "data": {
                    "lane_id": "lane-1",
                    "claim": {
                        "state": "retained",
                        "work_item": "ticket-1",
                        "actor_id": "worker-agent",
                        "owner": "root-agent",
                        "token": "claim-ticket-1",
                        "readback": "retained",
                    },
                    "root_receipt": root_receipt("dispatch", "ticket-1", base),
                    "assignment_sha256": "a" * 64,
                },
            },
            {
                "event": "handoff",
                "event_id": "handoff-1",
                "work_item": "ticket-1",
                "data": {
                    **{
                        key: receipt[key]
                        for key in (
                            "lane_id",
                            "agent_id",
                            "runtime_agent_type",
                            "actor_id",
                            "task_id",
                            "host_id",
                            "transport",
                        )
                    },
                    "assignment_ref": "ticket-1",
                    "worktree": str(repo),
                    "base": base,
                    "status": "done",
                    "commit": advanced,
                    "changed_scope_ids": ["ticket-1"],
                    "actual_changed_files": [],
                    "acceptance_proof": "criterion -> evidence",
                    "test_portfolio_delta": "unchanged",
                    "commands_and_results": ["focused proof passed"],
                    "skipped_checks": [],
                    "risk_or_blocker": "none",
                    "next_need": "root acceptance",
                    "scope_notes": [],
                    "final_status": "clean",
                    "assignment_sha256": "a" * 64,
                },
            },
            {
                "event": "accept",
                "event_id": "accept-1",
                "work_item": "ticket-1",
                "worker_sha": advanced,
                "data": {
                    "root_receipt": root_receipt(
                        "accept-worker-return", "ticket-1", advanced
                    )
                },
            },
            {
                "event": "land",
                "event_id": "land-1",
                "work_item": "ticket-1",
                "worker_sha": advanced,
                "integration_sha": advanced,
                "data": {
                    "prior_integration_sha": base,
                    "observed_head": advanced,
                    "clean": True,
                    "lane_head": advanced,
                    "lane_clean": True,
                    "task_state": "idle",
                    "liveness_cursor": "worker-1-idle",
                    "root_receipt": root_receipt("land", "ticket-1", advanced),
                },
            },
        ]
    )

    second = runtime_six_local_lane_events(
        advanced,
        repo,
        agent_id="demanding-worker",
        model="gpt-5.6-sol",
        effort="high",
        transport="subagent-v2",
    )[1:3]
    for event in second:
        event["work_item"] = "ticket-2"
        event["event_id"] = f"{event['event_id']}-2"
        event["data"]["lane_id"] = "lane-2"
    second[0]["data"].update(
        {
            "actor_id": "worker-agent-2",
            "task_id": "worker-task-2",
            "host_id": "worker-host-2",
            "assignment_ref": "ticket-2",
        }
    )
    second[0]["data"]["provider_acceptance"].update(
        {
            "lane_id": "lane-2",
            "actor_id": "worker-agent-2",
            "task_id": "worker-task-2",
            "host_id": "worker-host-2",
        }
    )
    second[1]["data"].update(
        {
            "actor_id": "worker-agent-2",
            "task_id": "worker-task-2",
            "host_id": "worker-host-2",
        }
    )
    events.extend(second)
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["lanes"]["lane-2"]["state"] == "ready"

    stale = json.loads(json.dumps(events))
    stale[-1]["data"].update({"base": base, "observed_head": base})
    invalid = LEDGER_RUNTIME["derive_state"](stale, str(repo))
    assert any("lane base differs from current integration HEAD" in error for error in invalid["errors"])

    reused_actor = json.loads(json.dumps(events))
    reused_actor[-2]["data"]["actor_id"] = "worker-agent"
    reused_actor[-2]["data"]["provider_acceptance"]["actor_id"] = "worker-agent"
    bind_root_receipts(reused_actor)
    invalid = LEDGER_RUNTIME["derive_state"](reused_actor, str(repo))
    assert any("reuses a worker actor identity" in error for error in invalid["errors"])

    correction_data = {
        "red": "cross-worker loop-close regression",
        "route": "serial-integrator",
        "owner": "integrator-agent",
        "write_scope": ["integration-scope"],
        "required_proof": "loop-close proof passes",
        "root_receipt": root_receipt("route-correction", "parent", advanced),
    }
    routed = [
        *events,
        {
            "event": "integration-regression",
            "event_id": "regression-1",
            "work_item": "parent",
            "integration_sha": advanced,
            "data": correction_data,
        },
    ]
    bind_root_receipts(routed)
    assert LEDGER_RUNTIME["derive_state"](routed, str(repo))["errors"] == []

def test_runtime_six_binds_review_repair_to_a_delegated_successor(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = current_review_events(base, (tmp_path / "worker-lane").resolve())
    events[0]["data"]["charter"]["runtime_contract"] = 6
    events[3]["data"]["assignment_sha256"] = "a" * 64
    events[4]["data"]["assignment_sha256"] = "a" * 64
    events[6]["data"].update(
        {
            "lane_head": base,
            "lane_clean": True,
            "task_state": "completed",
            "liveness_cursor": "worker-complete",
        }
    )
    events[8]["data"]["tasks"][0].update(
        {"head": base, "clean": True, "liveness_cursor": "worker-complete"}
    )
    finding = {
        "id": "F1",
        "blocking": True,
        "remediation": "automatic-in-scope",
        "anchor": "acceptance A",
        "evidence": "failing proof A",
        "required_proof": "proof A passes",
    }
    events[10]["decision"] = "blocked"
    events[10]["data"]["findings"] = [finding]
    events.append(
        {
            "event": "repair-plan",
            "event_id": "repair-plan-1",
            "work_item": "parent",
            "data": {
                "charter_id": "parent-charter",
                "generation": 1,
                "review_decision_id": "review-decision",
                "review_target": base,
                "finding_ids": ["F1"],
            },
        }
    )

    (repo / "tracked.txt").write_text("review repaired\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "repair review finding", cwd=repo)
    repaired = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()

    repair_lane = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="serial-integrator",
        model="gpt-5.6-sol",
        effort="medium",
        transport="subagent-v2",
    )[1:3]
    for event in repair_lane:
        event["work_item"] = "repair-1"
        event["event_id"] = f"repair-{event['event_id']}"
        event["data"]["lane_id"] = "repair-lane"
    repair_receipt = repair_lane[0]["data"]
    repair_receipt.update(
        {
            "actor_id": "repair-worker",
            "task_id": "repair-task",
            "host_id": "repair-host",
            "assignment_mode": "review-repair",
            "assignment_ref": "repair-1",
        }
    )
    repair_receipt["provider_acceptance"].update(
        {
            "lane_id": "repair-lane",
            "actor_id": "repair-worker",
            "task_id": "repair-task",
            "host_id": "repair-host",
        }
    )
    repair_lane[1]["data"].update(
        {
            "actor_id": "repair-worker",
            "task_id": "repair-task",
            "host_id": "repair-host",
        }
    )
    events.extend(repair_lane)
    events.extend(
        [
            {
                "event": "dispatch",
                "event_id": "repair-dispatch",
                "work_item": "repair-1",
                "data": {
                    "lane_id": "repair-lane",
                    "claim": {
                        "state": "retained",
                        "work_item": "repair-1",
                        "actor_id": "repair-worker",
                        "owner": "root-agent",
                        "token": "claim-repair-1",
                        "readback": "retained",
                    },
                    "root_receipt": root_receipt("dispatch", "repair-1", base),
                    "assignment_sha256": "b" * 64,
                },
            },
            {
                "event": "handoff",
                "event_id": "repair-handoff",
                "work_item": "repair-1",
                "data": {
                    **{
                        key: repair_receipt[key]
                        for key in (
                            "lane_id",
                            "agent_id",
                            "runtime_agent_type",
                            "actor_id",
                            "task_id",
                            "host_id",
                            "transport",
                        )
                    },
                    "assignment_ref": "repair-1",
                    "worktree": str(repo),
                    "base": base,
                    "status": "done",
                    "commit": repaired,
                    "changed_scope_ids": ["F1"],
                    "actual_changed_files": ["tracked.txt"],
                    "acceptance_proof": "F1 -> repaired proof",
                    "test_portfolio_delta": "unchanged",
                    "commands_and_results": ["proof A passed"],
                    "skipped_checks": [],
                    "risk_or_blocker": "none",
                    "next_need": "root acceptance",
                    "scope_notes": [],
                    "final_status": "clean",
                    "assignment_sha256": "b" * 64,
                },
            },
            {
                "event": "accept",
                "event_id": "repair-accept",
                "work_item": "repair-1",
                "worker_sha": repaired,
                "data": {
                    "root_receipt": root_receipt(
                        "accept-worker-return", "repair-1", repaired
                    )
                },
            },
            {
                "event": "land",
                "event_id": "repair-land",
                "work_item": "repair-1",
                "worker_sha": repaired,
                "integration_sha": repaired,
                "data": {
                    "prior_integration_sha": base,
                    "observed_head": repaired,
                    "clean": True,
                    "lane_head": repaired,
                    "lane_clean": True,
                    "task_state": "idle",
                    "liveness_cursor": "repair-idle",
                    "root_receipt": root_receipt("land", "repair-1", repaired),
                },
            },
            {
                "event": "repair-complete",
                "event_id": "repair-complete-1",
                "work_item": "parent",
                "integration_sha": repaired,
                "validation": "F1 proof and regression passed",
                "data": {
                    "generation": 1,
                    "finding_ids": ["F1"],
                    "lane_id": "repair-lane",
                    "actor_id": "repair-worker",
                    "task_id": "repair-task",
                    "worker_sha": repaired,
                    "prior_integration_sha": base,
                    "supersedes_candidate": base,
                    "landing_method": "direct",
                    "root_receipt": root_receipt(
                        "complete-repair", "parent", repaired
                    ),
                },
            },
            {
                "event": "review-ready",
                "event_id": "repair-review-ready",
                "work_item": "parent",
                "integration_sha": repaired,
                "data": {
                    "tasks": [
                        {
                            "lane_id": "lane-1",
                            "actor_id": "worker-agent",
                            "task_id": "worker-task",
                            "state": "completed",
                            "head": base,
                            "clean": True,
                            "liveness_cursor": "worker-complete",
                        },
                        {
                            "lane_id": "repair-lane",
                            "actor_id": "repair-worker",
                            "task_id": "repair-task",
                            "state": "idle",
                            "head": repaired,
                            "clean": True,
                            "liveness_cursor": "repair-idle",
                        },
                    ],
                    "integration": {"head": repaired, "clean": True},
                    "final_proof": {
                        "head": repaired,
                        "status": "passed",
                        "receipt": "repair-final-proof",
                    },
                    "root_receipt": root_receipt(
                        "review-ready", "parent", repaired
                    ),
                },
            },
        ]
    )
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["repair_completed_generation"] == 1
    assert state["integration_head"] == repaired
    assert "review has not passed" in LEDGER_RUNTIME["intent_errors"](state, "lock")

    remediation_invocation = json.loads(json.dumps(events[9]))
    remediation_invocation.update(
        {
            "event_id": "remediation-review-invocation",
            "integration_sha": repaired,
        }
    )
    remediation_data = remediation_invocation["data"]
    remediation_data.update(
        {
            "mode": "remediation",
            "actor_id": "remediation-reviewer",
            "task_id": "remediation-review-task",
            "host_id": "remediation-review-host",
            "lane_id": "remediation-review-lane",
            "observed_head": repaired,
            "route_evidence": {
                "candidate": repaired,
                "basis": "ordinary",
                "source": "repaired candidate risk classification",
            },
        }
    )
    remediation_data["provider_acceptance"].update(
        {
            "actor_id": "remediation-reviewer",
            "task_id": "remediation-review-task",
            "host_id": "remediation-review-host",
            "lane_id": "remediation-review-lane",
        }
    )
    remediation_data["root_receipt"] = root_receipt(
        "select-review", "parent", repaired, remediation_data
    )

    remediation_decision = json.loads(json.dumps(events[10]))
    remediation_decision.update(
        {
            "event_id": "remediation-review-decision",
            "integration_sha": repaired,
            "decision": "pass",
        }
    )
    remediation_decision["data"].update(
        {
            "review_invocation_id": "remediation-review-invocation",
            "mode": "remediation",
            "actor_id": "remediation-reviewer",
            "task_id": "remediation-review-task",
            "host_id": "remediation-review-host",
            "lane_id": "remediation-review-lane",
            "reviewed_head": repaired,
            "findings": [],
        }
    )
    reviewed = [*events, remediation_invocation, remediation_decision]
    bind_root_receipts(reviewed)
    reviewed_state = LEDGER_RUNTIME["derive_state"](reviewed, str(repo))
    assert reviewed_state["errors"] == []
    assert LEDGER_RUNTIME["intent_errors"](reviewed_state, "lock") == []

    missing_provenance = [dict(event) for event in events]
    missing_provenance[-2] = {
        **missing_provenance[-2],
        "data": {**missing_provenance[-2]["data"], "actor_id": "root-agent"},
    }
    bind_root_receipts(missing_provenance)
    invalid = LEDGER_RUNTIME["derive_state"](missing_provenance, str(repo))
    assert any("Repair worker provenance differs" in error for error in invalid["errors"])


def test_runtime_six_correction_lane_becomes_truthfully_review_ready(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = current_review_events(base, (tmp_path / "worker-lane").resolve())[:7]
    events[0]["data"]["charter"]["runtime_contract"] = 6
    events[3]["data"]["assignment_sha256"] = "a" * 64
    events[4]["data"]["assignment_sha256"] = "a" * 64
    events[6]["data"].update(
        {
            "lane_head": base,
            "lane_clean": True,
            "task_state": "completed",
            "liveness_cursor": "worker-complete",
        }
    )
    regression = {
        "event": "integration-regression",
        "event_id": "regression-1",
        "work_item": "parent",
        "integration_sha": base,
        "data": {
            "red": "cross-worker regression",
            "route": "serial-integrator",
            "owner": "integrator-agent",
            "write_scope": ["integration-scope"],
            "required_proof": "loop-close passes",
            "root_receipt": root_receipt("route-correction", "parent", base),
        },
    }
    events.append(regression)

    (repo / "tracked.txt").write_text("integrated correction\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "correct integration", cwd=repo)
    corrected = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()

    lane_events = runtime_six_local_lane_events(
        base,
        repo,
        agent_id="serial-integrator",
        model="gpt-5.6-sol",
        effort="high",
        transport="subagent-v2",
    )[1:3]
    for event in lane_events:
        event["work_item"] = "correction-1"
        event["event_id"] = f"correction-{event['event_id']}"
        event["data"]["lane_id"] = "correction-lane"
    receipt = lane_events[0]["data"]
    receipt.update(
        {
            "actor_id": "integrator-agent",
            "task_id": "integrator-task",
            "host_id": "integrator-host",
            "assignment_mode": "integration-correction",
            "assignment_ref": "regression-1",
        }
    )
    receipt["provider_acceptance"].update(
        {
            "lane_id": "correction-lane",
            "actor_id": "integrator-agent",
            "task_id": "integrator-task",
            "host_id": "integrator-host",
        }
    )
    lane_events[1]["data"].update(
        {"actor_id": "integrator-agent", "task_id": "integrator-task", "host_id": "integrator-host"}
    )
    events.extend(lane_events)
    events.extend(
        [
            {
                "event": "dispatch",
                "event_id": "correction-dispatch",
                "work_item": "correction-1",
                "data": {
                    "lane_id": "correction-lane",
                    "claim": {
                        "state": "retained",
                        "work_item": "correction-1",
                        "actor_id": "integrator-agent",
                        "owner": "root-agent",
                        "token": "claim-correction",
                        "readback": "retained",
                    },
                    "assignment_sha256": "c" * 64,
                    "root_receipt": root_receipt("dispatch", "correction-1", base),
                },
            },
            {
                "event": "handoff",
                "event_id": "correction-handoff",
                "work_item": "correction-1",
                "data": {
                    **{key: receipt[key] for key in ("lane_id", "agent_id", "runtime_agent_type", "actor_id", "task_id", "host_id", "transport")},
                    "assignment_ref": "regression-1",
                    "assignment_sha256": "c" * 64,
                    "worktree": str(repo),
                    "base": base,
                    "status": "done",
                    "commit": corrected,
                    "changed_scope_ids": ["integration-scope"],
                    "actual_changed_files": ["tracked.txt"],
                    "acceptance_proof": "RED -> green",
                    "test_portfolio_delta": "unchanged",
                    "commands_and_results": ["loop-close passed"],
                    "skipped_checks": [],
                    "risk_or_blocker": "none",
                    "next_need": "root acceptance",
                    "scope_notes": [],
                    "final_status": "clean",
                },
            },
            {
                "event": "accept",
                "event_id": "correction-accept",
                "work_item": "correction-1",
                "worker_sha": corrected,
                "data": {"root_receipt": root_receipt("accept-worker-return", "correction-1", corrected)},
            },
            {
                "event": "integration-correction",
                "event_id": "correction-land",
                "work_item": "parent",
                "integration_sha": corrected,
                "validation": "loop-close passed",
                "data": {
                    "regression_event_id": "regression-1",
                    "prior_integration_sha": base,
                    "correction_commit": corrected,
                    "route": "serial-integrator",
                    "actor_id": "integrator-agent",
                    "changed_scope": ["integration-scope"],
                    "lane_id": "correction-lane",
                    "worker_sha": corrected,
                    "landing_method": "direct",
                    "lane_head": corrected,
                    "lane_clean": True,
                    "task_state": "idle",
                    "liveness_cursor": "integrator-idle",
                    "root_receipt": root_receipt("land-correction", "parent", corrected),
                },
            },
            {
                "event": "graph-drained",
                "event_id": "corrected-drain",
                "work_item": "parent",
                "integration_sha": corrected,
                "data": {"root_receipt": root_receipt("graph-drained", "parent", corrected)},
            },
            {
                "event": "review-ready",
                "event_id": "corrected-review-ready",
                "work_item": "parent",
                "integration_sha": corrected,
                "data": {
                    "tasks": [
                        {"lane_id": "lane-1", "actor_id": "worker-agent", "task_id": "worker-task", "state": "completed", "head": base, "clean": True, "liveness_cursor": "worker-complete"},
                        {"lane_id": "correction-lane", "actor_id": "integrator-agent", "task_id": "integrator-task", "state": "idle", "head": corrected, "clean": True, "liveness_cursor": "integrator-idle"},
                    ],
                    "integration": {"head": corrected, "clean": True},
                    "final_proof": {"head": corrected, "status": "passed", "receipt": "corrected-proof"},
                    "root_receipt": root_receipt("review-ready", "parent", corrected),
                },
            },
        ]
    )
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["lanes"]["correction-lane"]["state"] == "landed"
    assert state["lanes"]["correction-lane"]["worker_sha"] == corrected


def test_runtime_six_binds_review_return_to_fresh_task(tmp_path: Path) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "a" * 40
    events = current_review_events(base, (tmp_path / "lane").resolve())

    valid = ledger["derive_state"](events)
    assert valid["errors"] == []

    wrong_return = [dict(event) for event in events]
    wrong_return[-1] = {
        **wrong_return[-1],
        "data": {**wrong_return[-1]["data"], "task_id": "other-review-task"},
    }
    invalid = ledger["derive_state"](wrong_return)
    assert any("review Return has mismatched task_id" in error for error in invalid["errors"])

    overlapping = [dict(event) for event in events]
    overlapping[-2] = {
        **overlapping[-2],
        "data": {**overlapping[-2]["data"], "task_id": "worker-task"},
    }
    invalid = ledger["derive_state"](overlapping)
    assert any("review task is an implementation task" in error for error in invalid["errors"])


def test_runtime_six_reselects_route_once_but_does_not_retry_incomplete_review(
    tmp_path: Path,
) -> None:
    _, base = repository(tmp_path)
    original = current_review_events(base, (tmp_path / "worker-lane").resolve())

    def successor_invocation(route: str) -> dict:
        event = json.loads(json.dumps(original[-2]))
        event["event_id"] = "review-invocation-2"
        data = event["data"]
        data.update(
            {
                "route": route,
                "agent_id": (
                    "assurance-coordinator"
                    if route == "high-assurance-review"
                    else "ordinary-reviewer"
                ),
                "actor_id": "review-agent-2",
                "task_id": "review-task-2",
                "host_id": "review-host-2",
                "lane_id": "review-lane-2",
            }
        )
        data["route_evidence"] = {
            "candidate": base,
            "basis": "release" if route == "high-assurance-review" else "ordinary",
            "source": "recorded candidate risk classification",
        }
        data["provider_acceptance"].update(
            {
                "agent_id": data["agent_id"],
                "task_id": data["task_id"],
                "host_id": data["host_id"],
                "lane_id": data["lane_id"],
            }
        )
        data["root_receipt"] = root_receipt("select-review", "parent", base, data)
        return event

    mismatch = json.loads(json.dumps(original))
    mismatch[-1]["decision"] = "scope-mismatch"
    mismatch[-1]["data"]["findings"] = []
    mismatch[-1]["data"]["residual_risks"] = []
    alternate = successor_invocation("high-assurance-review")
    allowed = LEDGER_RUNTIME["derive_state"]([*mismatch, alternate])
    assert allowed["errors"] == []
    assert allowed["review_route"] == "high-assurance-review"

    incomplete = json.loads(json.dumps(original))
    incomplete[-1]["decision"] = "incomplete"
    incomplete_state = LEDGER_RUNTIME["derive_state"](incomplete)
    assert "incomplete review requires a partial checkpoint" in LEDGER_RUNTIME[
        "intent_errors"
    ](incomplete_state, "review")
    retry = successor_invocation("change-review")
    rejected = LEDGER_RUNTIME["derive_state"]([*incomplete, retry])
    assert any(
        "initial mode is only valid for the first invocation" in error
        for error in rejected["errors"]
    )


def test_runtime_six_requires_both_high_assurance_core_returns(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = current_review_events(base, (tmp_path / "worker-lane").resolve())
    invocation = events[-2]["data"]
    invocation["route"] = "high-assurance-review"
    invocation["agent_id"] = "assurance-coordinator"
    invocation["route_evidence"]["basis"] = "release"
    invocation["provider_acceptance"]["agent_id"] = "assurance-coordinator"
    decision = events[-1]["data"]
    decision["route"] = "high-assurance-review"
    decision["agent_id"] = "assurance-coordinator"
    decision["assurance_returns"] = [
        {
            "agent_id": "har-spec-reviewer",
            "runtime_agent_type": "default",
            "actor_id": "spec-reviewer",
            "task_id": "spec-review-task",
            "lane_id": "spec-review-lane",
            "host_id": "spec-review-host",
            "transport": "subagent-v2",
            "task_id_state": "canonical",
            "requested_model": "gpt-5.6-sol",
            "requested_effort": "xhigh",
            "environment": "local",
            "worktree": str(repo),
            "resolved_model_status": "matched",
            "resolved_model": "gpt-5.6-sol",
            "resolved_effort_status": "matched",
            "resolved_effort": "xhigh",
            "provider_acceptance": {
                "status": "accepted",
                "lane_id": "spec-review-lane",
                "agent_id": "har-spec-reviewer",
                "runtime_agent_type": "default",
                "task_id": "spec-review-task",
                "host_id": "spec-review-host",
                "requested_model": "gpt-5.6-sol",
                "requested_effort": "xhigh",
                "environment": "local",
                "provider": "delegated-custody",
                "worktree": str(repo),
            },
            "status": "complete",
            "reviewed_head": base,
        },
        {
            "agent_id": "har-standards-reviewer",
            "runtime_agent_type": "default",
            "actor_id": "standards-reviewer",
            "task_id": "standards-review-task",
            "lane_id": "standards-review-lane",
            "host_id": "standards-review-host",
            "transport": "subagent-v2",
            "task_id_state": "canonical",
            "requested_model": "gpt-5.6-sol",
            "requested_effort": "xhigh",
            "environment": "local",
            "worktree": str(repo),
            "resolved_model_status": "matched",
            "resolved_model": "gpt-5.6-sol",
            "resolved_effort_status": "matched",
            "resolved_effort": "xhigh",
            "provider_acceptance": {
                "status": "accepted",
                "lane_id": "standards-review-lane",
                "agent_id": "har-standards-reviewer",
                "runtime_agent_type": "default",
                "task_id": "standards-review-task",
                "host_id": "standards-review-host",
                "requested_model": "gpt-5.6-sol",
                "requested_effort": "xhigh",
                "environment": "local",
                "provider": "delegated-custody",
                "worktree": str(repo),
            },
            "status": "complete",
            "reviewed_head": base,
        },
    ]
    bind_root_receipts(events)

    accepted = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert accepted["errors"] == []

    wrong_binding = json.loads(json.dumps(events))
    wrong_binding[-1]["data"]["assurance_returns"][0][
        "requested_effort"
    ] = "high"
    invalid_binding = LEDGER_RUNTIME["derive_state"](wrong_binding, str(repo))
    assert any(
        "assurance reviewer binding does not match har-spec-reviewer" in error
        for error in invalid_binding["errors"]
    )

    missing_receipt = json.loads(json.dumps(events))
    del missing_receipt[-1]["data"]["assurance_returns"][0]["provider_acceptance"]
    invalid_receipt = LEDGER_RUNTIME["derive_state"](missing_receipt, str(repo))
    assert any(
        "assurance reviewer har-spec-reviewer requires a task-bound provider receipt"
        in error
        for error in invalid_receipt["errors"]
    )

    contradictory_telemetry = json.loads(json.dumps(events))
    spec_return = contradictory_telemetry[-1]["data"]["assurance_returns"][0]
    spec_return["resolved_model_status"] = "unavailable"
    spec_return["telemetry_unavailable_reason"] = "runtime did not expose it"
    invalid_telemetry = LEDGER_RUNTIME["derive_state"](
        contradictory_telemetry, str(repo)
    )
    assert any(
        "unavailable review telemetry cannot include resolved_model" in error
        for error in invalid_telemetry["errors"]
    )

    partial = json.loads(json.dumps(events))
    partial[-1]["decision"] = "incomplete"
    partial[-1]["data"]["assurance_returns"] = partial[-1]["data"][
        "assurance_returns"
    ][:1]
    partial_state = LEDGER_RUNTIME["derive_state"](partial, str(repo))
    assert partial_state["errors"] == []
    assert "spec-reviewer" in partial_state["review_actor_ids_used"]
    assert "spec-review-task" in partial_state["review_task_ids_used"]

    incomplete = json.loads(json.dumps(events))
    incomplete[-1]["data"]["assurance_returns"] = incomplete[-1]["data"][
        "assurance_returns"
    ][:1]
    rejected = LEDGER_RUNTIME["derive_state"](incomplete, str(repo))
    assert any(
        "requires two core assurance returns" in error
        for error in rejected["errors"]
    )


def test_runtime_six_binds_root_and_automatic_repair(tmp_path: Path) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "a" * 40
    events = current_review_events(base, (tmp_path / "lane").resolve())

    missing_root = [dict(event) for event in events[:2]]
    missing_root[-1] = {
        **missing_root[-1],
        "data": {
            key: value
            for key, value in missing_root[-1]["data"].items()
            if key != "root_receipt"
        },
    }
    invalid = ledger["derive_state"](missing_root)
    assert any("root-owned assign receipt" in error for error in invalid["errors"])

    blocker = {
        "id": "F1",
        "blocking": True,
        "remediation": "automatic-in-scope",
        "anchor": "code.py:1",
        "evidence": "observed",
        "required_proof": "focused proof",
    }
    blocked = [dict(event) for event in events]
    blocked[-1] = {
        **blocked[-1],
        "decision": "blocked",
        "data": {**blocked[-1]["data"], "findings": [blocker]},
    }
    repair = {
        "event": "repair-plan",
        "event_id": "repair-plan",
        "work_item": "parent",
        "integration_sha": base,
        "data": {
            "charter_id": "parent-charter",
            "generation": 1,
            "review_decision_id": "review-decision",
            "review_target": base,
            "finding_ids": ["F1"],
        },
    }
    valid = ledger["derive_state"]([*blocked, repair])
    assert valid["errors"] == []

    decision_required = json.loads(json.dumps(blocked))
    decision_required[-1]["data"]["findings"][0]["remediation"] = "decision-required"
    invalid = ledger["derive_state"]([*decision_required, repair])
    assert any("decision-required blocker" in error for error in invalid["errors"])


def test_runtime_six_validates_route_lane_identity_and_manual_provider(
    tmp_path: Path,
) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "b" * 40
    events = current_review_events(base, (tmp_path / "lane").resolve())[:3]

    missing_root_checkout = json.loads(json.dumps(events))
    missing_root_checkout[2]["data"].pop("root_checkout")
    invalid = ledger["derive_state"](missing_root_checkout)
    assert any(
        "requires the read-only root checkout binding" in error
        for error in invalid["errors"]
    )

    wrong_route = [dict(event) for event in events]
    wrong_route[1] = {
        **wrong_route[1],
        "data": {**wrong_route[1]["data"], "requested_model": "gpt-5.6-terra"},
    }
    invalid = ledger["derive_state"](wrong_route)
    assert any("agent binding does not match" in error for error in invalid["errors"])

    provisional = [dict(event) for event in events]
    provisional[1] = {
        **provisional[1],
        "data": {**provisional[1]["data"], "task_id_state": "provisional"},
    }
    invalid = ledger["derive_state"](provisional)
    assert any("task ID is not canonical" in error for error in invalid["errors"])

    unrelated_receipt = [dict(event) for event in events]
    unrelated_receipt[1] = {
        **unrelated_receipt[1],
        "data": {
            **unrelated_receipt[1]["data"],
            "provider_acceptance": {
                **unrelated_receipt[1]["data"]["provider_acceptance"],
                "task_id": "other-task",
            },
        },
    }
    invalid = ledger["derive_state"](unrelated_receipt)
    assert any("task-bound provider acceptance" in error for error in invalid["errors"])

    wrong_head = [dict(event) for event in events]
    wrong_head[2] = {
        **wrong_head[2],
        "data": {**wrong_head[2]["data"], "observed_head": "d" * 40},
    }
    invalid = ledger["derive_state"](wrong_head)
    assert any("observed HEAD differs" in error for error in invalid["errors"])

    reused_lane = events + [
        {
            **events[1],
            "event_id": "lane-create-reused",
            "work_item": "ticket-2",
        }
    ]
    invalid = ledger["derive_state"](reused_lane)
    assert any("reuses a lane ID" in error for error in invalid["errors"])

    manual = [dict(event) for event in events]
    manual[1] = {
        **manual[1],
        "data": {
            **manual[1]["data"],
                "transport": "subagent-v2",
                "report_transport": "subagent-v2",
            "provider_acceptance": {
                **manual[1]["data"]["provider_acceptance"],
                "provider": "manual-helper",
            },
        },
    }
    manual[2] = {
        **manual[2],
        "data": {**manual[2]["data"], "provider": "manual-helper"},
    }
    bind_root_receipts(manual)
    valid = ledger["derive_state"](manual)
    assert valid["errors"] == []


def test_runtime_six_requires_cleanup_and_resume_evidence(tmp_path: Path) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "c" * 40
    lane_path = (tmp_path / "lane").resolve()
    landed = current_review_events(base, lane_path)[:7]

    shallow_cleanup = landed + [
        {
            "event": "lane-cleanup",
            "event_id": "cleanup",
            "work_item": "ticket-1",
            "data": {"lane_id": "lane-1", "state": "provider-preserved"},
        }
    ]
    invalid = ledger["derive_state"](shallow_cleanup)
    assert any("requires terminal task state" in error for error in invalid["errors"])

    wrong_head_cleanup = [
        *landed,
        {
            **shallow_cleanup[-1],
            "data": {
                **shallow_cleanup[-1]["data"],
                "agent_id": "clear-worker",
                "actor_id": "worker-agent",
                "task_id": "worker-task",
                "host_id": "worker-host",
                "terminal_task_state": "completed",
                "commit_disposition": "integrated",
                "exact_head": "d" * 40,
                "clean": True,
                "custody": "provider custody",
            },
        },
    ]
    invalid = ledger["derive_state"](wrong_head_cleanup)
    assert any("cleanup HEAD differs" in error for error in invalid["errors"])

    cleanup = {
        "event": "lane-cleanup",
        "event_id": "cleanup",
        "work_item": "ticket-1",
        "data": {
            "lane_id": "lane-1",
            "state": "removed",
            "agent_id": "clear-worker",
            "actor_id": "worker-agent",
            "task_id": "worker-task",
            "host_id": "worker-host",
            "terminal_task_state": "completed",
            "commit_disposition": "integrated",
            "exact_head": base,
            "clean": True,
            "registered_after": False,
            "directory_exists": False,
        },
    }
    valid = ledger["derive_state"](landed + [cleanup])
    assert valid["errors"] == []

    checkpoint_data = {
        "reason": "bounded stop",
        "continuation": "resume",
        "current_head": base,
        "actors": "idle",
        "integration_state": "clean",
        "next_frontier": [],
        "blockers": [],
        "claims_complete": True,
        "claims": [],
        "tracker": "unchanged",
    }
    checkpoint = {
        "event": "checkpoint",
        "event_id": "checkpoint-missing-landed-claim",
        "work_item": "parent",
        "integration_sha": base,
        "decision": "partial",
        "data": checkpoint_data,
    }
    checkpoint_data["root_receipt"] = root_receipt(
        "checkpoint", "parent", base, checkpoint_data
    )
    invalid = ledger["derive_state"]([*landed, cleanup, checkpoint])
    assert any("omits retained custody" in error for error in invalid["errors"])

    retained_checkpoint_data = {
        **checkpoint_data,
        "claims": [
            {
                "work_item": "ticket-1",
                "state": "retained",
                "owner": "root-agent",
                "token": "claim-ticket-1",
                "claimed_at": "2026-01-01T00:00:00+00:00",
                "recovery_owner": "root-agent",
                "readback": "retained",
            },
            {
                "work_item": "parent",
                "state": "retained",
                "owner": "root-agent",
                "token": "claim-parent",
                "claimed_at": "2026-01-01T00:00:00+00:00",
                "recovery_owner": "root-agent",
                "readback": "retained",
            },
        ],
    }
    retained_checkpoint_data["root_receipt"] = root_receipt(
        "checkpoint", "parent", base, retained_checkpoint_data
    )
    resumed_landed = [
        *landed,
        cleanup,
        {**checkpoint, "data": retained_checkpoint_data},
        {
            "event": "resume",
            "event_id": "resume-landed",
            "work_item": "parent",
            "timestamp": "2026-01-01T00:00:10+00:00",
            "data": {},
        },
        {
            "event": "reconcile",
            "event_id": "reconcile-landed",
            "work_item": "parent",
            "data": {
                "git": {
                    "head": base,
                    "status": "clean",
                    "observed_at": "2026-01-01T00:00:11+00:00",
                },
                "worktrees": [
                    {
                            "lane_id": "lane-1",
                            "provider": "manual-helper",
                        "state": "removed",
                        "worktree": str(lane_path),
                        "observed_at": "2026-01-01T00:00:11+00:00",
                    }
                ],
                "tasks": [
                    {
                        "lane_id": "lane-1",
                        "agent_id": "clear-worker",
                        "actor_id": "worker-agent",
                        "task_id": "worker-task",
                        "host_id": "worker-host",
                        "task_state": "completed",
                        "liveness_cursor": "worker-reconciled",
                        "observation_id": "worker-observation-2",
                        "observed_at": "2026-01-01T00:00:11+00:00",
                        "worktree": str(lane_path),
                        "head": base,
                        "status": "clean",
                        "processes": [],
                        "claim_state": "retained",
                    }
                ],
                "claims": [
                    {
                        "lane_id": "lane-1",
                        "work_item": "ticket-1",
                        "actor_id": "worker-agent",
                        "state": "retained",
                        "owner": "root-agent",
                        "token": "claim-ticket-1",
                        "observed_at": "2026-01-01T00:00:11+00:00",
                    },
                    {
                        "lane_id": None,
                        "work_item": "parent",
                        "actor_id": "root-agent",
                        "state": "retained",
                        "owner": "root-agent",
                        "token": "claim-parent",
                        "observed_at": "2026-01-01T00:00:11+00:00",
                    },
                ],
                "tracker": {"observed_at": "2026-01-01T00:00:11+00:00"},
            },
        },
    ]
    valid = ledger["derive_state"](resumed_landed)
    assert valid["errors"] == []

    missing_preserved_lane = json.loads(json.dumps(resumed_landed))
    missing_preserved_lane[-1]["data"]["worktrees"] = []
    missing_preserved_lane[-1]["data"]["tasks"] = []
    invalid = ledger["derive_state"](missing_preserved_lane)
    assert any("worktree inventory is not exhaustive" in error for error in invalid["errors"])
    assert any("task inventory is not exhaustive" in error for error in invalid["errors"])

    mismatched_git = json.loads(json.dumps(resumed_landed))
    mismatched_git[-1]["data"]["git"]["head"] = "f" * 40
    invalid = ledger["derive_state"](mismatched_git)
    assert any("Git evidence must match clean live integration HEAD" in error for error in invalid["errors"])

    resumed = landed + [
        {
            "event": "resume",
            "event_id": "resume",
            "work_item": "parent",
            "timestamp": "2026-01-01T00:00:10+00:00",
            "data": {},
        },
        {
            "event": "reconcile",
            "event_id": "reconcile",
            "work_item": "parent",
            "data": {
                "git": {},
                "worktrees": {},
                "tasks": None,
                "claims": {},
                "tracker": {},
                "remote": {},
            },
        },
    ]
    invalid = ledger["derive_state"](resumed)
    assert any("empty reconciliation evidence: tasks" in error for error in invalid["errors"])

    stale = [
        *landed,
        resumed[-2],
        {
            "event": "reconcile",
            "event_id": "reconcile-stale",
            "work_item": "parent",
            "data": {
                "git": {"observed_at": "2026-01-01T00:00:05+00:00"},
                "worktrees": [{"lane_id": "lane-1"}],
                "tasks": [
                    {
                        "task_id": "worker-task",
                        "host_id": "worker-host",
                        "task_state": "completed",
                        "liveness_cursor": "worker-final-cursor",
                        "observation_id": "observation-1",
                        "observed_at": "2026-01-01T00:00:05+00:00",
                        "worktree": str(lane_path),
                        "head": base,
                        "status": "clean",
                        "processes": [],
                        "claim_state": "retained",
                    }
                ],
                "claims": [{"work_item": "ticket-1", "state": "retained"}],
                "tracker": {"observed_at": "2026-01-01T00:00:05+00:00"},
                "remote": {"observed_at": "2026-01-01T00:00:05+00:00"},
            },
        },
    ]
    invalid = ledger["derive_state"](stale)
    assert any("evidence is not post-resume" in error for error in invalid["errors"])
    assert any("worktree observation is stale or mismatched" in error for error in invalid["errors"])
    assert any("claim observation is stale or mismatched" in error for error in invalid["errors"])
    assert any("requires one observation for task" in error for error in invalid["errors"])
    assert any("task inventory is not exhaustive and unique" in error for error in invalid["errors"])


def test_finish_is_nonmutating_when_the_run_is_incomplete(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    run = tmp_path / "incomplete"
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "parent": "parent",
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "children": ["ticket-1"],
                "charter": {"id": "parent-charter", "outcome": "deliver"},
            }
        ),
        encoding="utf-8",
    )
    result, started = helper(
        LEDGER,
        "start",
        "--run",
        str(run),
        "--repo",
        str(repo),
        "--in",
        str(scope),
    )
    assert result.returncode == 0, started
    before = (run / "events.jsonl").read_bytes()

    result, blocked = helper(LEDGER, "finish", "--run", str(run))

    assert result.returncode == 1, blocked
    assert blocked["code"] == "INCOMPLETE"
    assert blocked["effect_started"] is False
    assert blocked["changed"] is False
    assert (run / "events.jsonl").read_bytes() == before
    assert Path(blocked["detail"]).is_file()


def test_runtime_six_finish_records_the_supplied_root_release_receipt(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    run = tmp_path / "runtime-six-finish"
    events_path = run / "events.jsonl"
    events = current_review_events(base, (tmp_path / "lane").resolve())
    events[0]["data"]["repo"] = str(repo.resolve())
    events.extend(
        [
            {
                "event": "closeout-head",
                "event_id": "closeout-head",
                "work_item": "parent",
                "integration_sha": base,
                "data": {"root_receipt": root_receipt("lock", "parent", base)},
            },
            {
                "event": "child-closeout",
                "event_id": "child-closeout",
                "work_item": "ticket-1",
                "integration_sha": base,
                "data": {
                    "state": "verified",
                    "delivered": "ticket implementation",
                    "acceptance_evidence": "accepted",
                    "proof": "passed",
                    "review": "passed",
                    "reviewed_head": base,
                    "landed_head": base,
                    "residual_risk": "none",
                    "intended_mutation": "recorded",
                    "posted_comment": "recorded",
                    "mutation_readback": "verified",
                    "claim_release": {
                        "state": "released",
                        "token": "claim-ticket-1",
                        "readback": "absent",
                    },
                    "affected_frontier_readback": {"receipt": "frontier-1"},
                    "root_receipt": root_receipt("close-child", "ticket-1", base),
                },
            },
            {
                "event": "parent-closeout",
                "event_id": "parent-closeout",
                "work_item": "parent",
                "integration_sha": base,
                "data": {
                    "state": "verified",
                    "claim_release": {
                        "state": "released",
                        "work_item": "parent",
                        "token": "claim-parent",
                        "readback": "absent",
                    },
                    "root_receipt": root_receipt("close-parent", "parent", base),
                },
            },
            {
                "event": "lane-cleanup",
                "event_id": "lane-cleanup",
                "work_item": "ticket-1",
                "data": {
                    "lane_id": "lane-1",
                    "agent_id": "clear-worker",
                    "actor_id": "worker-agent",
                    "task_id": "worker-task",
                    "host_id": "worker-host",
                    "state": "removed",
                    "terminal_task_state": "completed",
                    "commit_disposition": "integrated",
                    "exact_head": base,
                    "clean": True,
                    "registered_after": False,
                    "directory_exists": False,
                },
            },
            {
                "event": "tracker-lock",
                "event_id": "tracker-lock",
                "work_item": "parent",
                "integration_sha": base,
                "data": {
                    "root_receipt": root_receipt("tracker-lock", "parent", base)
                },
            },
        ]
    )
    bind_root_receipts(events)
    for event in events:
        append_event(events_path, event)
    completion = tmp_path / "completion.json"
    release_receipt = root_receipt("release", "parent", base)
    completion.write_text(
        json.dumps({"root_receipt": release_receipt}), encoding="utf-8"
    )

    result, finished = helper(
        LEDGER,
        "finish",
        "--run",
        str(run),
        "--in",
        str(completion),
    )

    assert result.returncode == 0, finished
    recorded = LEDGER_RUNTIME["load_events"](events_path)
    assert recorded[-1]["event"] == "release"
    assert recorded[-1]["data"]["root_receipt"] == release_receipt
