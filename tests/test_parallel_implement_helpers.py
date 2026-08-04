from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT / "skills/custom/parallel-implement/scripts/lane_worktree.py"
LEDGER = ROOT / "skills/custom/parallel-implement/scripts/run_ledger.py"
LEDGER_RUNTIME = runpy.run_path(str(LEDGER))
PROJECT_KEY = "repo-001"


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
    (repo / "test_smoke.py").write_text("def test_smoke():\n    assert True\n", encoding="utf-8")
    command("git", "add", "tracked.txt", "test_smoke.py", cwd=repo)
    command("git", "commit", "-m", "base", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    return repo, base


def tracker_snapshot(run: Path, parent: str, children: list[str]) -> dict[str, str | int | list[str]]:
    run.mkdir(parents=True, exist_ok=True)
    artifact = run / "tracker-snapshot.json"
    nodes = []
    for item in [parent, *children]:
        nodes.append(
            {
                "id": item,
                "title": item,
                "body": f"frozen body for {item}",
                "comments": [],
                "labels": [],
                "assignees": [],
                "state": "open",
            }
        )
    artifact.write_text(
        json.dumps(
            {
                "schema": 1,
                "tracker": "test",
                "repository": "owner/repo",
                "observed_at": "2026-08-02T00:00:00Z",
                "parent": parent,
                "children": children,
                "nodes": nodes,
                "edges": [],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return {
        "schema": 1,
        "path": str(artifact.resolve()),
        "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "repository": "owner/repo",
        "parent": parent,
        "children": children,
    }


def test_ledger_dispatch_prepares_one_final_brief_then_binds_the_spawn(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "run" / "events.jsonl"
    scope = tmp_path / "scope.json"
    snapshot = tracker_snapshot(events.parent, "parent", ["ticket-1"])
    scope.write_text(
        json.dumps(
            {
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "tracker_snapshot": snapshot,
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
        "runtime_contract": 7,
    }
    snapshot_path = Path(snapshot["path"])
    frozen_snapshot = snapshot_path.read_bytes()
    snapshot_path.write_bytes(frozen_snapshot + b"\n")
    result, drifted = helper(LEDGER, "status", "--run", str(events.parent))
    assert result.returncode == 1
    detail = json.loads(Path(drifted["detail"]).read_text(encoding="utf-8"))
    assert any("frozen tracker snapshot is missing or changed" in error for error in detail["errors"])
    snapshot_path.write_bytes(frozen_snapshot)

    packet = tmp_path / "dispatch.json"
    packet.write_text(
        json.dumps(
            {
                "kind": "prepare",
                "work_item": "ticket-1",
                "profile": "clear-worker",
                "actor_id": "worker-1",
                "attempt_id": "ticket-1-attempt-1",
                "environment": "local",
                "assignment": {
                    "mode": "implementation",
                    "ref": "ticket-1",
                },
                "write_scope": ["tracked.txt"],
                "claim": {
                    "state": "retained",
                    "work_item": "ticket-1",
                    "actor_id": "worker-1",
                    "owner": "root-agent",
                    "token": "claim-ticket-1",
                    "readback": "retained",
                },
            }
        ),
        encoding="utf-8",
    )
    result, prepared = helper(
        LEDGER,
        "dispatch",
        "--run",
        str(events.parent),
        "--in",
        str(packet),
    )
    assert result.returncode == 0, prepared
    assert prepared["receipt"]["applied"] == 3
    assert prepared["awaiting"]["action"] == "record-spawn-receipt"
    assert prepared["spawn"]["agent_type"] == "luna_max"
    revision = prepared["revision"]
    result, recovered_prepare = helper(
        LEDGER, "dispatch", "--run", str(events.parent), "--in", str(packet)
    )
    assert result.returncode == 0, recovered_prepare
    assert recovered_prepare["mode"] == "recover"
    assert recovered_prepare["revision"] == revision
    assert recovered_prepare["spawn"] == prepared["spawn"]
    brief = Path(prepared["assignment"]["path"])
    text = brief.read_text(encoding="utf-8")
    assert "Mode: `implementation`" in text
    assert "Profile: `clear-worker`" in text
    assert "Actor: `worker-1`" in text
    assert "task-1" not in text
    assert str(snapshot["path"]) in text
    assert "do not wait for a follow-up assignment" in prepared["spawn"]["message"]

    rejected_run = tmp_path / "rejected-run"
    shutil.copytree(events.parent, rejected_run)
    prepared_lane = next(
        event
        for event in map(
            json.loads,
            (rejected_run / "events.jsonl").read_text(encoding="utf-8").splitlines(),
        )
        if event["event"] == "lane-preflight"
    )
    cleanup_packet = tmp_path / "not-created-cleanup.json"
    cleanup_packet.write_text(
        json.dumps(
            {
                "kind": "events",
                "events": [
                    {
                        "event": "lane-cleanup",
                        "work_item": "ticket-1",
                        "data": {
                            "lane_id": prepared_lane["data"]["lane_id"],
                            "agent_id": "clear-worker",
                            "actor_id": "worker-1",
                            "task_id": None,
                            "state": "provider-preserved",
                            "terminal_task_state": "not-created",
                            "commit_disposition": "preserved",
                            "exact_head": base,
                            "clean": True,
                            "preservation": {"reason": "provider rejected spawn"},
                            "custody": "root integration checkout",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result, cleaned = helper(
        LEDGER, "apply", "--run", str(rejected_run), "--in", str(cleanup_packet)
    )
    assert result.returncode == 0, cleaned
    cleaned_state = LEDGER_RUNTIME["derive_state"](
        LEDGER_RUNTIME["load_events"](rejected_run / "events.jsonl"), str(repo)
    )
    assert next(iter(cleaned_state["lanes"].values()))["state"] == "provider-preserved"
    retry_packet = json.loads(packet.read_text(encoding="utf-8"))
    retry_packet.update(attempt_id="ticket-1-attempt-2", actor_id="worker-2")
    retry_packet["claim"].update(actor_id="worker-2", token="claim-ticket-1-retry")
    packet.write_text(json.dumps(retry_packet), encoding="utf-8")
    result, retried_prepare = helper(
        LEDGER, "dispatch", "--run", str(rejected_run), "--in", str(packet)
    )
    assert result.returncode == 0, retried_prepare
    assert retried_prepare["mode"] == "prepare"

    sealed = brief.read_bytes()
    brief.write_bytes(sealed + b"tampered\n")
    result, tampered = helper(LEDGER, "status", "--run", str(events.parent))
    assert result.returncode == 1
    detail = json.loads(Path(tampered["detail"]).read_text(encoding="utf-8"))
    assert any("immutable final assignment artifact" in error for error in detail["errors"])
    brief.write_bytes(sealed)

    receipt = tmp_path / "spawn-receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "kind": "receipt",
                "attempt_id": "ticket-1-attempt-1",
                "task_id": "task-1",
                "task_state": "running",
                "liveness_cursor": "cursor-1",
                "provider": "delegated-custody",
                "worktree": str(repo.resolve()),
                "environment_match": False,
                "resolved_model_status": "matched",
                "resolved_model": "gpt-5.6-luna",
                "resolved_effort_status": "matched",
                "resolved_effort": "max",
            }
        ),
        encoding="utf-8",
    )
    result, rejected_receipt = helper(
        LEDGER, "dispatch", "--run", str(events.parent), "--in", str(receipt)
    )
    assert result.returncode == 1, rejected_receipt
    result, still_authorized = helper(LEDGER, "status", "--run", str(events.parent))
    assert result.returncode == 0
    assert still_authorized["awaiting"]["action"] == "record-spawn-receipt"
    observed_receipt = json.loads(receipt.read_text(encoding="utf-8"))
    observed_receipt["environment_match"] = True
    receipt.write_text(json.dumps(observed_receipt), encoding="utf-8")
    result, activated = helper(
        LEDGER, "dispatch", "--run", str(events.parent), "--in", str(receipt)
    )
    assert result.returncode == 0, activated
    assert activated["awaiting"]["action"] == "await-worker"
    lane = next(
        event for event in map(json.loads, events.read_text(encoding="utf-8").splitlines())
        if event["event"] == "lane-preflight"
    )

    result_packet = tmp_path / "worker-result.json"
    result_packet.write_text(
        json.dumps(
            {
                "kind": "worker-result",
                "work_item": "ticket-1",
                "lane_id": lane["data"]["lane_id"],
                "agent_id": "clear-worker",
                "runtime_agent_type": "luna_max",
                "actor_id": "worker-1",
                "task_id": "task-1",
                "transport": "subagent-v2",
                "worktree": str(repo.resolve()),
                "base": base,
                "assignment_ref": "ticket-1",
                "report": {
                    "status": "done",
                    "commit": base,
                    "changed_scope_ids": ["ticket-1"],
                    "actual_changed_files": ["tracked.txt"],
                    "assignment_sha256": prepared["assignment"]["sha256"],
                    "grounding_and_scope": "ticket and repository grounded",
                    "proof": {"summary": "criterion -> focused proof passed"},
                    "risk_or_blocker": "none",
                    "required_root_action": "accept or reject",
                    "final_worktree": {"head": base, "clean": True},
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
    changed_return["report"]["final_worktree"] = {"head": base, "clean": False}
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
    mismatched["report"]["final_worktree"] = {"head": base, "clean": True}
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


def test_dispatch_reports_and_recovers_a_preserved_lane_after_failed_preflight(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    (repo / "test_smoke.py").write_text("def broken(\n", encoding="utf-8")
    command("git", "add", "test_smoke.py", cwd=repo)
    command("git", "commit", "-m", "add broken collection target", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    run = tmp_path / "run"
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "claim-parent",
                    "readback": "retained",
                },
                "tracker_snapshot": tracker_snapshot(run, "parent", ["ticket-1"]),
                "charter": {"id": "charter", "outcome": "deliver"},
            }
        ),
        encoding="utf-8",
    )
    result, started = helper(
        LEDGER, "start", "--run", str(run), "--repo", str(repo), "--in", str(scope)
    )
    assert result.returncode == 0, started
    packet = tmp_path / "dispatch.json"
    packet.write_text(
        json.dumps(
            {
                "kind": "prepare",
                "work_item": "ticket-1",
                "profile": "clear-worker",
                "actor_id": "worker-1",
                "attempt_id": "attempt-1",
                "environment": "worktree",
                "assignment": {"mode": "implementation", "ref": "ticket-1"},
                "write_scope": ["tracked.txt"],
                "claim": {
                    "state": "retained",
                    "work_item": "ticket-1",
                    "actor_id": "worker-1",
                    "owner": "root-agent",
                    "token": "claim-ticket-1",
                    "readback": "retained",
                },
                "lane": {
                    "root": str(tmp_path / "lanes"),
                },
            }
        ),
        encoding="utf-8",
    )
    result, blocked = helper(
        LEDGER, "dispatch", "--run", str(run), "--in", str(packet)
    )
    assert result.returncode == 1
    assert blocked["effect_started"] is True
    recovery = blocked["recovery"]
    assert recovery["kind"] == "isolated-lane"
    worktree = Path(recovery["worktree"])
    assert worktree.is_dir()
    assert recovery["recovery"]["action"] == "preserve-until-graph-cleanup"
    cleanup_result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        recovery["recovery"]["root"],
        "--completed",
        str(worktree),
    )
    assert cleanup_result.returncode == 0, cleanup


def test_dispatch_prepare_opens_the_configured_isolated_lane(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    lane_root = (tmp_path / "lanes" / PROJECT_KEY / "wt").resolve()
    config = repo / ".codex/config.toml"
    config.parent.mkdir()
    encoded_root = str(lane_root).replace("\\", "\\\\")
    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f'"{encoded_root}" = true\n',
        encoding="utf-8",
    )
    command("git", "add", ".codex/config.toml", cwd=repo)
    command("git", "commit", "-m", "configure lanes", cwd=repo)
    base = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    run = tmp_path / "run"
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "parent": "parent",
                "children": ["ticket-1"],
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "parent",
                    "owner": "root-agent",
                    "token": "parent-claim",
                    "readback": "retained",
                },
                "tracker_snapshot": tracker_snapshot(
                    run, "parent", ["ticket-1"]
                ),
                "charter": {"id": "charter", "outcome": "deliver"},
            }
        ),
        encoding="utf-8",
    )
    result, started = helper(
        LEDGER, "start", "--run", str(run), "--repo", str(repo), "--in", str(scope)
    )
    assert result.returncode == 0, started
    packet = tmp_path / "dispatch.json"
    packet.write_text(
        json.dumps(
            {
                "kind": "prepare",
                "work_item": "ticket-1",
                "profile": "clear-worker",
                "actor_id": "worker-1",
                "attempt_id": "attempt-1",
                "environment": "worktree",
                "assignment": {"mode": "implementation", "ref": "ticket-1"},
                "write_scope": ["tracked.txt"],
                "claim": {
                    "state": "retained",
                    "work_item": "ticket-1",
                    "actor_id": "worker-1",
                    "owner": "root-agent",
                    "token": "ticket-claim",
                    "readback": "retained",
                },
            }
        ),
        encoding="utf-8",
    )
    invalid_packet = json.loads(packet.read_text(encoding="utf-8"))
    invalid_packet["claim"]["actor_id"] = "other-worker"
    packet.write_text(json.dumps(invalid_packet), encoding="utf-8")
    result, rejected = helper(
        LEDGER, "dispatch", "--run", str(run), "--in", str(packet)
    )
    assert result.returncode == 1, rejected
    assert not lane_root.exists()
    invalid_packet["claim"]["actor_id"] = "worker-1"
    packet.write_text(json.dumps(invalid_packet), encoding="utf-8")
    result, prepared = helper(
        LEDGER, "dispatch", "--run", str(run), "--in", str(packet)
    )
    assert result.returncode == 0, prepared
    recorded = [
        json.loads(line) for line in (run / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    preflight = next(event["data"] for event in recorded if event["event"] == "lane-preflight")
    assert Path(preflight["worktree"]).is_dir()
    assert Path(preflight["worktree"]).is_relative_to(lane_root)

    cleanup_result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--completed",
        preflight["worktree"],
    )
    assert cleanup_result.returncode == 0, cleanup
    assert cleanup["removed"] == [preflight["worktree"]]


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


def test_runtime_seven_removes_the_lane_ready_compatibility_packet() -> None:
    with pytest.raises(ValueError, match="worker-result or events"):
        LEDGER_RUNTIME["packet_events"]({"kind": "lane-ready"})


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
        "dispatch",
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


def test_runtime_seven_resume_accepts_empty_exhaustive_lane_inventories(
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
                "tracker_snapshot": tracker_snapshot(
                    tmp_path / "run", "parent", ["ticket-1"]
                ),
                "dispositions": {"ticket-1": "caller-deferred"},
                "charter": {
                    "id": "charter",
                    "runtime_contract": 7,
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
    lane_path.parent.mkdir(parents=True, exist_ok=True)
    brief_path = lane_path.parent / "assignment.md"
    brief_path.write_text("frozen assignment\n", encoding="utf-8")
    assignment_sha256 = hashlib.sha256(brief_path.read_bytes()).hexdigest()
    review_brief_path = lane_path.parent / "review-assignment.md"
    review_brief_path.write_text("frozen candidate review assignment\n", encoding="utf-8")
    review_assignment_sha256 = hashlib.sha256(review_brief_path.read_bytes()).hexdigest()
    snapshot_path = lane_path.parent / "tracker-snapshot.json"
    snapshot_path.write_text(
        json.dumps(
            {
                "schema": 1,
                "tracker": "test",
                "repository": "owner/repo",
                "observed_at": "2026-08-02T00:00:00Z",
                "parent": "parent",
                "children": ["ticket-1"],
                "nodes": [
                    {
                        "id": item,
                        "title": item,
                        "body": f"frozen body for {item}",
                        "comments": [],
                        "labels": [],
                        "assignees": [],
                        "state": "open",
                    }
                    for item in ("parent", "ticket-1")
                ],
                "edges": [],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    snapshot_sha256 = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
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
        "brief_path": str(review_brief_path.resolve()),
        "assignment_sha256": review_assignment_sha256,
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
                "tracker_snapshot": {
                    "schema": 1,
                    "path": str(snapshot_path.resolve()),
                    "sha256": snapshot_sha256,
                    "repository": "owner/repo",
                    "parent": "parent",
                    "children": ["ticket-1"],
                },
                "charter": {
                    "id": "parent-charter",
                    "runtime_contract": 7,
                    "repair_generation_budget": 2,
                },
            },
        },
        {
            "event": "lane-create",
            "event_id": "lane-create",
            "work_item": "ticket-1",
            "data": {
                key: lane_receipt[key]
                for key in (
                    "lane_id",
                    "agent_id",
                    "runtime_agent_type",
                    "actor_id",
                    "transport",
                    "requested_model",
                    "requested_effort",
                    "environment",
                    "assignment_mode",
                    "assignment_ref",
                    "root_receipt",
                )
            },
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
                "attempt_id": "ticket-1-attempt-1",
                "task_name": "ticket_1",
                "prepare_sha256": "c" * 64,
                "brief_path": str(brief_path.resolve()),
                "assignment_sha256": assignment_sha256,
                "tracker_snapshot_sha256": snapshot_sha256,
                "root_receipt": root_receipt("dispatch", "ticket-1", base),
            },
        },
        {
            "event": "spawn-receipt",
            "event_id": "spawn-receipt",
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
                        "transport",
                        "requested_model",
                        "requested_effort",
                        "environment",
                        "task_state",
                        "report_transport",
                        "liveness_cursor",
                        "task_id_state",
                        "provider_acceptance",
                        "environment_match",
                        "resolved_model_status",
                        "resolved_model",
                        "resolved_effort_status",
                        "resolved_effort",
                    )
                },
                "attempt_id": "ticket-1-attempt-1",
                "assignment_sha256": assignment_sha256,
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
                "assignment_sha256": assignment_sha256,
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
                "grounding_and_scope": "bounded repository grounding",
                "proof": {"summary": "focused proof passed"},
                "required_root_action": "accept or reject",
                "final_worktree": {"head": base, "clean": True},
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


def runtime_seven_local_lane_events(
    base: str,
    checkout: Path,
    *,
    agent_id: str,
    model: str,
    effort: str,
    transport: str,
    active: bool = False,
) -> list[dict]:
    events = current_review_events(base, checkout)[:5 if active else 3]
    receipt = events[1]["data"]
    receipt.update(
        {
            "agent_id": agent_id,
            "runtime_agent_type": "luna_max" if agent_id == "clear-worker" else "default",
            "transport": transport,
            "requested_model": model,
            "requested_effort": effort,
            "environment": "local",
        }
    )
    events[2]["data"].update(receipt)
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
    if active:
        spawn = events[4]["data"]
        spawn.update(
            {
                "agent_id": agent_id,
                "runtime_agent_type": receipt["runtime_agent_type"],
                "transport": transport,
                "report_transport": transport,
                "requested_model": model,
                "requested_effort": effort,
                "resolved_model": model,
                "resolved_effort": effort,
                "environment": "local",
            }
        )
        spawn["provider_acceptance"].update(
            {
                "agent_id": agent_id,
                "runtime_agent_type": receipt["runtime_agent_type"],
                "requested_model": model,
                "requested_effort": effort,
                "environment": "local",
                "provider": "delegated-custody",
                "worktree": str(checkout),
            }
        )
    return bind_root_receipts(events)


def test_runtime_seven_routes_serial_workers_without_root_implementation(
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
        events = runtime_seven_local_lane_events(
            base,
            repo,
            agent_id=agent_id,
            model=model,
            effort=effort,
            transport=transport,
        )
        assert LEDGER_RUNTIME["derive_state"](events, str(repo))["errors"] == []

    leaked_root = runtime_seven_local_lane_events(
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

    crossed = runtime_seven_local_lane_events(
        base,
        repo,
        agent_id="clear-worker",
        model="gpt-5.6-luna",
        effort="xhigh",
        transport="codex-task",
    )
    invalid = LEDGER_RUNTIME["derive_state"](crossed, str(repo))
    assert any("requires subagent-v2 transport" in error for error in invalid["errors"])

    root_actor = runtime_seven_local_lane_events(
        base,
        repo,
        agent_id="adaptive-worker",
        model="gpt-5.6-terra",
        effort="xhigh",
        transport="subagent-v2",
    )
    root_actor[1]["data"]["actor_id"] = "root-agent"
    bind_root_receipts(root_actor)
    invalid = LEDGER_RUNTIME["derive_state"](root_actor, str(repo))
    assert any("root cannot be a worker actor" in error for error in invalid["errors"])


def test_runtime_seven_reuses_the_same_lane_for_pre_landing_correction(
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

    events = current_review_events(base, (tmp_path / "lane").resolve())[:6]
    events[0]["data"]["charter"]["runtime_contract"] = 7
    events[5]["data"]["commit"] = first
    events[5]["data"]["final_worktree"] = {"head": first, "clean": True}
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
        **events[5],
        "event_id": "handoff-corrected",
        "data": {
            **events[5]["data"],
            "assignment_ref": "feedback-1",
                "commit": successor,
                "final_worktree": {"head": successor, "clean": True},
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
        *events[:7],
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
    missing_supersession[7] = {
        **missing_supersession[7],
        "data": {
            **missing_supersession[7]["data"],
            "supersedes_commit": None,
        },
    }
    invalid = LEDGER_RUNTIME["derive_state"](missing_supersession, str(repo))
    assert any("must supersede the prior commit" in error for error in invalid["errors"])


def test_runtime_seven_serializes_local_workers_and_delegates_integration_correction(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    (repo / "tracked.txt").write_text("first serial landing\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "advance first serial worker", cwd=repo)
    advanced = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    events = runtime_seven_local_lane_events(
        base,
        repo,
        agent_id="adaptive-worker",
        model="gpt-5.6-terra",
        effort="xhigh",
        transport="subagent-v2",
        active=True,
    )
    events[0]["data"]["children"] = ["ticket-1", "ticket-2"]
    events[0]["data"]["tracker_snapshot"]["children"] = ["ticket-1", "ticket-2"]
    receipt = events[4]["data"]
    events.extend(
        [
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
                            "transport",
                        )
                    },
                    "assignment_ref": "ticket-1",
                    "worktree": str(repo),
                    "base": base,
                    "status": "done",
                    "commit": advanced,
                    "changed_scope_ids": ["ticket-1"],
                    "actual_changed_files": ["tracked.txt"],
                    "acceptance_proof": "criterion -> evidence",
                    "test_portfolio_delta": "unchanged",
                    "commands_and_results": ["focused proof passed"],
                    "skipped_checks": [],
                    "risk_or_blocker": "none",
                    "grounding_and_scope": "bounded repository grounding",
                    "proof": {"summary": "focused proof passed"},
                    "required_root_action": "accept or reject",
                    "final_worktree": {"head": advanced, "clean": True},
                    "next_need": "root acceptance",
                    "scope_notes": [],
                    "final_status": "clean",
                    "assignment_sha256": receipt["assignment_sha256"],
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

    second = runtime_seven_local_lane_events(
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
            "assignment_ref": "ticket-2",
        }
    )
    second[1]["data"].update(
        {
            "actor_id": "worker-agent-2",
            "assignment_ref": "ticket-2",
        }
    )
    events.extend(second)
    bind_root_receipts(events)
    state = LEDGER_RUNTIME["derive_state"](events, str(repo))
    assert state["errors"] == []
    assert state["lanes"]["lane-2"]["state"] == "prepared"

    stale = json.loads(json.dumps(events))
    stale[-1]["data"].update({"base": base, "observed_head": base})
    invalid = LEDGER_RUNTIME["derive_state"](stale, str(repo))
    assert any("lane base differs from current integration HEAD" in error for error in invalid["errors"])

    reused_actor = json.loads(json.dumps(events))
    reused_actor[-2]["data"]["actor_id"] = "worker-agent"
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

def test_runtime_seven_binds_review_repair_to_a_delegated_successor(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = current_review_events(base, (tmp_path / "worker-lane").resolve())
    events[0]["data"]["charter"]["runtime_contract"] = 7
    events[7]["data"].update(
        {
            "lane_head": base,
            "lane_clean": True,
            "task_state": "completed",
            "liveness_cursor": "worker-complete",
        }
    )
    events[9]["data"]["tasks"][0].update(
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
    events[11]["decision"] = "blocked"
    events[11]["data"]["findings"] = [finding]
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

    repair_lane = runtime_seven_local_lane_events(
        base,
        repo,
        agent_id="serial-integrator",
        model="gpt-5.6-sol",
        effort="medium",
        transport="subagent-v2",
        active=True,
    )[1:5]
    for event in repair_lane:
        event["work_item"] = "repair-1"
        event["event_id"] = f"repair-{event['event_id']}"
        event["data"]["lane_id"] = "repair-lane"
    repair_lane[0]["data"].update(
        {
            "actor_id": "repair-worker",
            "assignment_mode": "review-repair",
            "assignment_ref": "repair-1",
        }
    )
    repair_lane[1]["data"].update(
        {
            "actor_id": "repair-worker",
            "assignment_mode": "review-repair",
            "assignment_ref": "repair-1",
        }
    )
    repair_lane[2]["data"]["claim"].update(
        {
            "actor_id": "repair-worker",
            "work_item": "repair-1",
        }
    )
    repair_receipt = repair_lane[3]["data"]
    repair_receipt.update({"actor_id": "repair-worker", "task_id": "repair-task"})
    repair_receipt["provider_acceptance"].update(
        {"lane_id": "repair-lane", "actor_id": "repair-worker", "task_id": "repair-task"}
    )
    events.extend(repair_lane)
    events.extend(
        [
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
                    "grounding_and_scope": "bounded review repair",
                    "proof": {"summary": "F1 proof A passed"},
                    "required_root_action": "accept or reject",
                    "final_worktree": {"head": repaired, "clean": True},
                    "next_need": "root acceptance",
                    "scope_notes": [],
                    "final_status": "clean",
                    "assignment_sha256": repair_receipt["assignment_sha256"],
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

    remediation_invocation = json.loads(json.dumps(events[10]))
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

    remediation_decision = json.loads(json.dumps(events[11]))
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


def test_runtime_seven_correction_lane_becomes_truthfully_review_ready(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = current_review_events(base, (tmp_path / "worker-lane").resolve())[:8]
    events[0]["data"]["charter"]["runtime_contract"] = 7
    events[7]["data"].update(
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

    lane_events = runtime_seven_local_lane_events(
        base,
        repo,
        agent_id="serial-integrator",
        model="gpt-5.6-sol",
        effort="high",
        transport="subagent-v2",
        active=True,
    )[1:5]
    for event in lane_events:
        event["work_item"] = "correction-1"
        event["event_id"] = f"correction-{event['event_id']}"
        event["data"]["lane_id"] = "correction-lane"
    lane_events[0]["data"].update(
        {
            "actor_id": "integrator-agent",
            "assignment_mode": "integration-correction",
            "assignment_ref": "regression-1",
        }
    )
    lane_events[1]["data"].update(
        {
            "actor_id": "integrator-agent",
            "assignment_mode": "integration-correction",
            "assignment_ref": "regression-1",
        }
    )
    lane_events[2]["data"]["claim"].update(
        {"work_item": "correction-1", "actor_id": "integrator-agent"}
    )
    receipt = lane_events[3]["data"]
    receipt.update({"actor_id": "integrator-agent", "task_id": "integrator-task"})
    receipt["provider_acceptance"].update(
        {"lane_id": "correction-lane", "actor_id": "integrator-agent", "task_id": "integrator-task"}
    )
    events.extend(lane_events)
    events.extend(
        [
            {
                "event": "handoff",
                "event_id": "correction-handoff",
                "work_item": "correction-1",
                "data": {
                    **{key: receipt[key] for key in ("lane_id", "agent_id", "runtime_agent_type", "actor_id", "task_id", "transport")},
                    "assignment_ref": "regression-1",
                    "assignment_sha256": receipt["assignment_sha256"],
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
                    "grounding_and_scope": "bounded integration correction",
                    "proof": {"summary": "RED to green and loop-close passed"},
                    "required_root_action": "accept or reject",
                    "final_worktree": {"head": corrected, "clean": True},
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


def test_runtime_seven_binds_review_return_to_fresh_task(tmp_path: Path) -> None:
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


def test_runtime_seven_reselects_route_once_but_does_not_retry_incomplete_review(
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


def test_runtime_seven_requires_both_high_assurance_core_returns(
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


def test_runtime_seven_binds_root_and_automatic_repair(tmp_path: Path) -> None:
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


def test_runtime_seven_validates_route_lane_identity_and_manual_provider(
    tmp_path: Path,
) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "b" * 40
    events = current_review_events(base, (tmp_path / "lane").resolve())[:5]

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
    provisional[4] = {
        **provisional[4],
        "data": {**provisional[4]["data"], "task_id_state": "provisional"},
    }
    invalid = ledger["derive_state"](provisional)
    assert any("not active and canonical" in error for error in invalid["errors"])

    unrelated_receipt = [dict(event) for event in events]
    unrelated_receipt[4] = {
        **unrelated_receipt[4],
        "data": {
            **unrelated_receipt[4]["data"],
            "provider_acceptance": {
                **unrelated_receipt[4]["data"]["provider_acceptance"],
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

    valid = ledger["derive_state"](events)
    assert valid["errors"] == []


def test_runtime_seven_requires_cleanup_and_resume_evidence(tmp_path: Path) -> None:
    ledger = runpy.run_path(str(LEDGER))
    base = "c" * 40
    lane_path = (tmp_path / "lane").resolve()
    landed = current_review_events(base, lane_path)[:8]

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
                "tracker_snapshot": tracker_snapshot(
                    run, "parent", ["ticket-1"]
                ),
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


def test_runtime_seven_finish_records_the_supplied_root_release_receipt(
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
                    "proof": {"summary": "passed"},
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
