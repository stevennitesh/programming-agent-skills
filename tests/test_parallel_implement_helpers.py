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
    result = subprocess.run(
        [sys.executable, str(LEDGER), "append", "--events", str(events), "--stdin"],
        input=json.dumps(event),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    packet = json.loads(result.stdout)
    assert result.returncode == 0, packet
    return packet["event"]


def append_receipt(
    events: Path,
    event: dict,
    *,
    intent: str,
    event_id: str,
    repo: Path | None = None,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    args = [
        sys.executable,
        str(LEDGER),
        "append-receipt",
        "--events",
        str(events),
        "--intent",
        intent,
        "--event-id",
        event_id,
        "--stdin",
    ]
    if repo is not None:
        args.extend(["--repo", str(repo)])
    result = subprocess.run(
        args,
        input=json.dumps(event),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result, json.loads(result.stdout)


def validate_state(
    events: Path, intent: str, *, repo: Path | None = None
) -> tuple[subprocess.CompletedProcess[str], dict]:
    args = [
        sys.executable,
        str(LEDGER),
        "validate-state",
        "--events",
        str(events),
        "--intent",
        intent,
    ]
    if repo is not None:
        args.extend(["--repo", str(repo)])
    result = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result, json.loads(result.stdout)


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


def create_lane(repo: Path, base: str, lane_root: Path, item: str = "ticket-1") -> dict:
    result, packet = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        item,
        "--max-path",
        "1000",
    )
    assert result.returncode == 0, packet
    assert packet["ok"] is True
    return packet


def test_lane_helper_defaults_to_the_repo_parent_worktree_namespace(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    result, created = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--max-path",
        "1000",
    )
    assert result.returncode == 0, created
    expected_root = (repo.parent / "worktrees" / "parallel-implement").resolve()
    assert Path(created["root"]) == expected_root
    assert created["root_source"] == "repo-parent-default"
    assert Path(created["worktree"]).is_relative_to(expected_root)

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_helper_creates_preflights_and_removes_a_detached_worktree(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    created = create_lane(repo, base, tmp_path / "lanes")
    worktree = Path(created["worktree"])

    result, preflight = helper(
        LANE,
        "preflight",
        "--worktree",
        str(worktree),
        "--base",
        base,
        "--actor-id",
        "worker-1",
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
    )
    assert result.returncode == 0, preflight
    assert preflight["detached"] is True
    assert preflight["status"] == "clean"
    assert set(preflight["probes"].values()) == {"passed"}
    assert preflight["proof_startup"]["returncode"] == 0
    assert preflight["git_trust"] in {"normal", "command-scoped-safe-directory"}
    assert Path(preflight["temp_root"]).is_dir()
    assert Path(preflight["pytest_basetemp"]).is_dir()
    assert Path(preflight["cache_root"]).is_dir()

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        str(worktree),
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
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-file",
        "--proof-command-file",
        str(proof_file),
    )
    assert result.returncode == 0, preflight
    proof = preflight["proof_startup"]
    assert proof["returncode"] == 0
    assert proof["command_file"] == str(proof_file.resolve())
    assert proof["command_file_sha256"] == hashlib.sha256(proof_bytes).hexdigest()

    bom_proof_file = tmp_path / "proof-command-bom.json"
    bom_proof_bytes = b"\xef\xbb\xbf" + proof_bytes
    bom_proof_file.write_bytes(bom_proof_bytes)
    result, bom_preflight = helper(
        LANE,
        "preflight",
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-file-bom",
        "--proof-command-file",
        str(bom_proof_file),
    )
    assert result.returncode == 0, bom_preflight
    bom_proof = bom_preflight["proof_startup"]
    assert bom_proof["returncode"] == 0
    assert bom_proof["command_file_sha256"] == hashlib.sha256(
        bom_proof_bytes
    ).hexdigest()

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 0, cleanup


def test_lane_root_precedence_uses_explicit_then_environment_then_default(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    environment_root = tmp_path / "environment-lanes"
    explicit_root = tmp_path / "explicit-lanes"
    env = {**os.environ, "PARALLEL_IMPLEMENT_WORKTREE_ROOT": str(environment_root)}

    result, created = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--root",
        str(explicit_root),
        "--base",
        base,
        "--run-id",
        "run-explicit",
        "--item-id",
        "ticket-explicit",
        "--max-path",
        "1000",
        env=env,
    )
    assert result.returncode == 0, created
    assert Path(created["root"]) == explicit_root.resolve()
    assert created["root_source"] == "explicit"
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
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
        "--max-path",
        "1000",
        env=env,
    )
    assert result.returncode == 0, created
    assert Path(created["root"]) == environment_root.resolve()
    assert created["root_source"] == "environment"
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
        "--expected-head",
        base,
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

    result, skipped = helper(
        LANE,
        "preflight",
        "--worktree",
        created["worktree"],
        "--base",
        base,
        "--actor-id",
        "worker-1",
        "--skip-proof",
        "--reason",
        "repository has no startup proof command",
    )
    assert result.returncode == 0, skipped
    assert skipped["proof_startup"]["skipped"] is True
    assert skipped["proof_startup"]["reason"]

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
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
        "--root",
        str(lane_root),
        "--base",
        "missing-base",
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-1",
        "--max-path",
        "1000",
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
        "--root",
        str(repo / "nested"),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-2",
        "--max-path",
        "1000",
    )
    assert result.returncode == 1
    assert "inside the active checkout" in nested["error"]

    short_budget_root = tmp_path / "short-budget-lanes"
    result, budget = helper(
        LANE,
        "create",
        "--repo",
        str(repo),
        "--root",
        str(short_budget_root),
        "--base",
        base,
        "--run-id",
        "run-1",
        "--item-id",
        "ticket-3",
        "--max-path",
        "10",
    )
    assert result.returncode == 1
    assert "path budget exceeded" in budget["error"]
    assert budget["state"] == "blocked-path-budget"
    assert not short_budget_root.exists()

    created = create_lane(repo, base, lane_root, item="ticket-with-a-long-name")
    if sys.platform == "win32":
        assert created["path_budget"]["reserve"] >= 96
    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        created["root"],
        "--worktree",
        created["worktree"],
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
        "--root",
        str(lane_root),
        "--worktree",
        str(worktree),
        "--expected-head",
        base,
        "--disposition",
        "integrated",
    )
    assert result.returncode == 1
    assert cleanup["state"] == "unregistered-residual-directory"

    result, purged = helper(
        LANE,
        "purge-residual",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--worktree",
        str(worktree),
        "--confirm-unregistered-residual",
    )
    assert result.returncode == 0, purged
    assert purged["state"] == "removed"
    assert not worktree.exists()


@pytest.mark.parametrize("removal_fails", [False, True])
def test_lane_cleanup_reports_verified_residual_recovery_in_the_same_call(
    tmp_path: Path, monkeypatch, capsys, removal_fails: bool
) -> None:
    namespace = runpy.run_path(str(LANE))
    cleanup = namespace["cleanup"]
    globals_ = cleanup.__globals__
    repo = tmp_path / "repo"
    root = tmp_path / "lanes"
    worktree = root / "lane"
    worktree.mkdir(parents=True)
    (worktree / "generated-path.txt").write_text("residual\n", encoding="utf-8")
    head = "a" * 40
    registrations = iter(({worktree.resolve(): {"HEAD": head}}, {}))

    monkeypatch.setitem(globals_, "git_root", lambda path: (repo.resolve(), "normal"))
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
            root=str(root),
            worktree=str(worktree),
            expected_head=head[:8],
            disposition="integrated",
        )
    )
    packet = json.loads(capsys.readouterr().out)
    if removal_fails:
        assert result == 1
        assert packet["state"] == "unregistered-residual-directory"
        assert packet["recoverable"] is True
        assert packet["next_action"]["command"] == "purge-residual"
        assert worktree.exists()
    else:
        assert result == 0, packet
        assert packet["state"] == "removed"
        assert packet["registered_after"] is False
        assert packet["residual_removed"] is True
        assert not worktree.exists()


def test_lane_helper_never_mutates_global_safe_directory() -> None:
    source = LANE.read_text(encoding="utf-8")
    assert "safe.directory=" in source
    assert "--global" not in source


def test_run_ledger_is_the_validated_append_only_event_owner(tmp_path: Path) -> None:
    events = tmp_path / "run" / "events.jsonl"
    lifecycle = (
        ("one", "lane-create"),
        ("two", "lane-preflight"),
        ("three", "lane-cleanup"),
    )
    for event_id, event in lifecycle:
        result, packet = helper(
            LEDGER,
            "append",
            "--events",
            str(events),
            "--event",
            event,
            "--event-id",
            event_id,
            "--work-item",
            "ticket-1",
            "--data-json",
            json.dumps({"packet": f"{event}.json"}),
        )
        assert result.returncode == 0, packet

    result, validated = helper(LEDGER, "validate", "--events", str(events))
    assert result.returncode == 0, validated
    assert validated["count"] == 3

    result, listed = helper(LEDGER, "list", "--events", str(events))
    assert result.returncode == 0, listed
    assert [item["event"] for item in listed["items"]] == [
        event for _, event in lifecycle
    ]

    result, duplicate = helper(
        LEDGER,
        "append",
        "--events",
        str(events),
        "--event",
        "land",
        "--event-id",
        "three",
        "--work-item",
        "ticket-1",
    )
    assert result.returncode == 1
    assert "duplicates event_id" in duplicate["error"]
    assert len(events.read_text(encoding="utf-8").splitlines()) == 3


def test_append_receipt_is_idempotent_and_separates_commit_from_authority(
    tmp_path: Path,
) -> None:
    events = tmp_path / "receipt.jsonl"
    scope = {
        "event": "scope",
        "work_item": "parent",
        "data": {
            "children": ["ticket-1"],
            "charter": {
                "id": "charter-1",
                "repair_generation_budget": 2,
                "review_invocation_budget": 3,
                "review_invocations_required": 1,
            },
        },
    }

    result, first = append_receipt(
        events, scope, intent="dispatch", event_id="scope-1"
    )
    assert result.returncode == 0, first
    assert first["committed"] is True
    assert first["event_id"] == "scope-1"
    assert first["event_number"] == 1
    assert first["requested_intent"] == {"name": "dispatch", "allowed": False}
    assert "dispatch" not in first["authorized_intents"]
    assert first["counters"] == {
        "repairs_used": 0,
        "repairs_remaining": 2,
        "reviews_used": 0,
        "reviews_remaining": 3,
        "reviews_required_remaining": 1,
    }

    result, replay = append_receipt(
        events, scope, intent="dispatch", event_id="scope-1"
    )
    assert result.returncode == 0, replay
    assert replay == first
    assert len(events.read_text(encoding="utf-8").splitlines()) == 1

    conflicting = {**scope, "data": {**scope["data"], "children": ["ticket-2"]}}
    result, rejected = append_receipt(
        events, conflicting, intent="dispatch", event_id="scope-1"
    )
    assert result.returncode == 1
    assert rejected["committed"] is False
    assert "different payload" in rejected["error"]
    assert len(events.read_text(encoding="utf-8").splitlines()) == 1


def test_append_receipt_replay_rechecks_authority_after_the_stream_advances(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "stale-receipt.jsonl"
    prefix = canonical_review_prefix(base)
    for event in prefix[:-1]:
        append_event(events, event)

    decision = prefix[-1]
    result, first = append_receipt(
        events,
        decision,
        intent="lock",
        event_id="review-1-decision",
        repo=repo,
    )
    assert result.returncode == 0, first
    assert first["requested_intent"] == {"name": "lock", "allowed": True}
    assert first["receipt_fresh"] is True

    append_event(events, {"event": "resume", "work_item": "parent"})
    result, replay = append_receipt(
        events,
        decision,
        intent="lock",
        event_id="review-1-decision",
        repo=repo,
    )
    assert result.returncode == 0, replay
    assert replay["committed"] is True
    assert replay["event_number"] == first["event_number"]
    assert replay["state_event_count"] == first["state_event_count"] + 1
    assert replay["receipt_fresh"] is False
    assert replay["requested_intent"] == {"name": "lock", "allowed": False}
    assert "lock" not in replay["authorized_intents"]


def test_canonical_review_invocations_require_a_nonempty_reason(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    for reason in (None, ""):
        events = tmp_path / f"missing-reason-{reason is None}.jsonl"
        prefix = canonical_review_prefix(base)
        invocation = prefix[-2]
        invocation["data"] = {"mode": "initial"}
        if reason is not None:
            invocation["data"]["reason"] = reason
        for event in prefix:
            append_event(events, event)
        result, invalid = validate_state(events, "lock", repo=repo)
        assert result.returncode == 1
        assert any("requires a reason" in error for error in invalid["errors"])

def test_append_receipt_rejects_semantically_invalid_state_without_writing(
    tmp_path: Path,
) -> None:
    events = tmp_path / "invalid-receipt.jsonl"
    result, rejected = append_receipt(
        events,
        {
            "event": "accept",
            "work_item": "ticket-1",
            "worker_sha": "abc",
        },
        intent="land",
        event_id="invalid-accept",
    )
    assert result.returncode == 1
    assert rejected["committed"] is False
    assert "semantically invalid" in rejected["error"]
    assert not events.exists() or events.read_text(encoding="utf-8") == ""

def test_ledger_state_machine_rejects_illegal_campaign_transitions(
    tmp_path: Path,
) -> None:
    events = tmp_path / "invalid.jsonl"
    append_event(events, {"event": "accept", "work_item": "ticket-1", "worker_sha": "abc"})
    result, packet = validate_state(events, "land")
    assert result.returncode == 1
    assert packet["allowed"] is False
    assert any("accept requires dispatch" in error for error in packet["errors"])

    events = tmp_path / "land-without-accept.jsonl"
    append_event(
        events,
        {"event": "lane-create", "work_item": "ticket-1", "data": {"lane_id": "one"}},
    )
    append_event(
        events,
        {"event": "lane-preflight", "work_item": "ticket-1", "data": {"lane_id": "one"}},
    )
    append_event(
        events,
        {"event": "dispatch", "work_item": "ticket-1", "data": {"lane_id": "one"}},
    )
    append_event(
        events,
        {
            "event": "land",
            "work_item": "ticket-1",
            "worker_sha": "abc",
            "integration_sha": "def",
        },
    )
    result, packet = validate_state(events, "review")
    assert result.returncode == 1
    assert any("land requires acceptance" in error for error in packet["errors"])


def test_resume_requires_external_reconciliation_before_redispatch(
    tmp_path: Path,
) -> None:
    events = tmp_path / "resume.jsonl"
    for event in (
        {"event": "scope", "work_item": "parent", "data": {"children": ["ticket-1"]}},
        {"event": "lane-create", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "lane-preflight", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "resume", "work_item": "parent"},
    ):
        append_event(events, event)

    result, blocked = validate_state(events, "dispatch")
    assert result.returncode == 1
    assert any("resume requires reconciled" in error for error in blocked["errors"])

    append_event(
        events,
        {
            "event": "reconcile",
            "work_item": "parent",
            "data": {
                "git": "clean",
                "worktrees": "verified",
                "agents": "none active",
                "tracker": "claim verified",
                "remote": "unchanged",
            },
        },
    )
    result, allowed = validate_state(events, "dispatch")
    assert result.returncode == 0, allowed
    assert allowed["allowed"] is True


def valid_campaign_events(base: str) -> list[dict]:
    closeout = {
        "state": "verified",
        "delivered": "ticket implementation",
        "acceptance_evidence": "criterion -> proof",
        "proof": "focused and integration proof passed",
        "review": "pass",
        "reviewed_head": base,
        "residual_risk": "none",
        "intended_mutation": "implemented and closed",
        "posted_comment": "comment-1",
        "mutation_readback": "closed and claim released",
    }
    return [
        {
            "event": "scope",
            "work_item": "parent",
            "data": {
                "children": ["ticket-1"],
                "push_required": True,
                "charter": {"id": "parent-charter", "repair_budget": 2},
            },
        },
        {"event": "lane-create", "work_item": "ticket-1", "data": {"lane_id": "lane-1", "state": "created"}},
        {"event": "lane-preflight", "work_item": "ticket-1", "data": {"lane_id": "lane-1", "state": "ready"}},
        {"event": "dispatch", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "accept", "work_item": "ticket-1", "worker_sha": base},
        {"event": "land", "work_item": "ticket-1", "worker_sha": base, "integration_sha": base},
        {"event": "graph-drained", "work_item": "parent", "integration_sha": base},
        {"event": "review-ready", "work_item": "parent", "integration_sha": base},
        {"event": "review-target", "work_item": "parent", "integration_sha": base},
        {"event": "review-decision", "work_item": "parent", "integration_sha": base, "decision": "pass"},
        {"event": "closeout-head", "work_item": "parent", "integration_sha": base},
        {"event": "child-closeout", "work_item": "ticket-1", "integration_sha": base, "data": closeout},
        {"event": "parent-closeout", "work_item": "parent", "integration_sha": base, "data": {"state": "verified"}},
        {"event": "tracker-lock", "work_item": "parent", "integration_sha": base},
        {"event": "push", "work_item": "parent", "integration_sha": base},
        {"event": "lane-cleanup", "work_item": "ticket-1", "data": {"lane_id": "lane-1", "state": "removed", "registered_after": False, "directory_exists": False}},
        {"event": "release", "work_item": "parent", "integration_sha": base, "decision": "complete"},
    ]


def blocked_review_events(base: str, findings: list[dict], *, budget: int = 2) -> list[dict]:
    return [
        {
            "event": "scope",
            "work_item": "parent",
            "data": {
                "children": ["ticket-1"],
                "charter": {"id": "parent-charter", "repair_budget": budget},
            },
        },
        {"event": "lane-create", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "lane-preflight", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "dispatch", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "accept", "work_item": "ticket-1", "worker_sha": base},
        {"event": "land", "work_item": "ticket-1", "worker_sha": base, "integration_sha": base},
        {"event": "graph-drained", "work_item": "parent", "integration_sha": base},
        {"event": "review-ready", "work_item": "parent", "integration_sha": base},
        {"event": "review-target", "work_item": "parent", "integration_sha": base},
        {
            "event": "review-decision",
            "event_id": "review-1",
            "work_item": "parent",
            "integration_sha": base,
            "decision": "blocked",
            "data": {"mode": "initial", "findings": findings},
        },
    ]


def canonical_review_prefix(
    base: str,
    *,
    review_budget: int = 3,
    reviews_required: int = 1,
    decision: str = "pass",
    findings: list[dict] | None = None,
) -> list[dict]:
    return [
        {
            "event": "scope",
            "work_item": "parent",
            "data": {
                "children": ["ticket-1"],
                "charter": {
                    "id": "parent-charter",
                    "runtime_contract": 2,
                    "repair_generation_budget": 2,
                    "review_invocation_budget": review_budget,
                    "review_invocations_required": reviews_required,
                },
            },
        },
        {"event": "lane-create", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "lane-preflight", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "dispatch", "work_item": "ticket-1", "data": {"lane_id": "lane-1"}},
        {"event": "accept", "work_item": "ticket-1", "worker_sha": base},
        {"event": "land", "work_item": "ticket-1", "worker_sha": base, "integration_sha": base},
        {"event": "graph-drained", "work_item": "parent", "integration_sha": base},
        {"event": "review-ready", "work_item": "parent", "integration_sha": base},
        {
            "event": "review-invocation",
            "event_id": "review-1",
            "work_item": "parent",
            "integration_sha": base,
            "data": {"mode": "initial", "reason": "first integrated candidate"},
        },
        {
            "event": "review-decision",
            "event_id": "review-1-decision",
            "work_item": "parent",
            "integration_sha": base,
            "decision": decision,
            "data": {
                "review_invocation_id": "review-1",
                "mode": "initial",
                "findings": findings or [],
            },
        },
    ]


def test_ledger_authorizes_one_complete_bounded_repair_generation(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "repair.jsonl"
    findings = [
        {
            "id": "F1",
            "blocking": True,
            "remediation": "automatic-in-scope",
            "anchor": "acceptance A",
            "evidence": "failing proof A",
            "required_proof": "proof A passes",
        },
        {
            "id": "F2",
            "blocking": True,
            "remediation": "automatic-in-scope",
            "anchor": "acceptance B",
            "evidence": "failing proof B",
            "required_proof": "proof B passes",
        },
    ]
    for event in blocked_review_events(base, findings):
        append_event(events, event)
    append_event(
        events,
        {
            "event": "repair-plan",
            "work_item": "parent",
            "data": {
                "charter_id": "parent-charter",
                "generation": 1,
                "review_decision_id": "review-1",
                "review_target": base,
                "finding_ids": ["F1", "F2"],
            },
        },
    )

    result, authorized = validate_state(events, "repair", repo=repo)
    assert result.returncode == 0, authorized
    assert authorized["allowed"] is True

    (repo / "tracked.txt").write_text("repaired\n", encoding="utf-8")
    command("git", "add", "tracked.txt", cwd=repo)
    command("git", "commit", "-m", "repair findings", cwd=repo)
    repaired = command("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    for event in (
        {"event": "lane-create", "work_item": "repair-1", "data": {"lane_id": "repair-lane"}},
        {"event": "lane-preflight", "work_item": "repair-1", "data": {"lane_id": "repair-lane"}},
        {"event": "dispatch", "work_item": "repair-1", "data": {"lane_id": "repair-lane"}},
        {"event": "accept", "work_item": "repair-1", "worker_sha": repaired},
        {"event": "land", "work_item": "repair-1", "worker_sha": repaired, "integration_sha": repaired},
        {
            "event": "repair-complete",
            "work_item": "parent",
            "integration_sha": repaired,
            "validation": "F1 and F2 proof plus regression passed",
            "data": {"generation": 1, "finding_ids": ["F1", "F2"]},
        },
    ):
        append_event(events, event)

    result, review = validate_state(events, "review", repo=repo)
    assert result.returncode == 0, review
    append_event(events, {"event": "review-ready", "work_item": "parent", "integration_sha": repaired})
    append_event(
        events,
        {
            "event": "review-invocation",
            "event_id": "review-2",
            "work_item": "parent",
            "integration_sha": repaired,
            "data": {"mode": "remediation", "reason": "verify repaired successor"},
        },
    )
    append_event(
        events,
        {
            "event": "review-decision",
            "work_item": "parent",
            "integration_sha": repaired,
            "decision": "pass",
            "data": {
                "review_invocation_id": "review-2",
                "mode": "remediation",
                "findings": [],
            },
        },
    )
    result, lock = validate_state(events, "lock", repo=repo)
    assert result.returncode == 0, lock


def test_review_invocations_support_assurance_and_caller_budget_changes(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "assurance.jsonl"
    for event in canonical_review_prefix(base):
        append_event(events, event)

    append_event(
        events,
        {
            "event": "scope-change",
            "work_item": "parent",
            "data": {
                "charter": {
                    "id": "parent-charter",
                    "runtime_contract": 2,
                    "repair_generation_budget": 2,
                    "review_invocation_budget": 4,
                    "review_invocations_required": 4,
                },
                "budget_change": {
                    "source": "caller requested three additional assurance reviews",
                    "reason": "increase confidence before closeout",
                    "prior": {
                        "repair_generation_budget": 2,
                        "review_invocation_budget": 3,
                        "review_invocations_required": 1,
                    },
                },
            },
        },
    )
    for number in range(2, 5):
        append_event(
            events,
            {
                "event": "review-invocation",
                "event_id": f"review-{number}",
                "work_item": "parent",
                "integration_sha": base,
                "data": {
                    "mode": "assurance",
                    "reason": f"caller-required confidence pass {number - 1}",
                },
            },
        )
        append_event(
            events,
            {
                "event": "review-decision",
                "work_item": "parent",
                "integration_sha": base,
                "decision": "pass with residual risk",
                "data": {
                    "review_invocation_id": f"review-{number}",
                    "mode": "assurance",
                    "findings": [],
                },
            },
        )

    result, lock = validate_state(events, "lock", repo=repo)
    assert result.returncode == 0, lock
    assert lock["review_invocations_used"] == 4
    assert lock["review_invocations_completed"] == 4
    assert lock["review_invocations_required"] == 4


def test_budget_scope_change_requires_exact_prior_values_and_caller_evidence(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "unauthorized-budget-change.jsonl"
    for event in canonical_review_prefix(base):
        append_event(events, event)
    append_event(
        events,
        {
            "event": "scope-change",
            "work_item": "parent",
            "data": {
                "charter": {
                    "id": "parent-charter",
                    "runtime_contract": 2,
                    "repair_generation_budget": 4,
                    "review_invocation_budget": 5,
                    "review_invocations_required": 2,
                }
            },
        },
    )
    result, blocked = validate_state(events, "lock", repo=repo)
    assert result.returncode == 1
    assert any("budget changes require data.budget_change" in error for error in blocked["errors"])


def test_incomplete_review_may_retry_the_same_target_and_mode(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "retry.jsonl"
    for event in canonical_review_prefix(base, decision="incomplete"):
        append_event(events, event)
    append_event(
        events,
        {
            "event": "review-invocation",
            "event_id": "review-2",
            "work_item": "parent",
            "integration_sha": base,
            "data": {"mode": "initial", "reason": "retry incomplete invocation"},
        },
    )
    append_event(
        events,
        {
            "event": "review-decision",
            "work_item": "parent",
            "integration_sha": base,
            "decision": "pass",
            "data": {
                "review_invocation_id": "review-2",
                "mode": "initial",
                "findings": [],
            },
        },
    )
    result, lock = validate_state(events, "lock", repo=repo)
    assert result.returncode == 0, lock
    assert lock["review_invocations_used"] == 2
    assert lock["review_invocations_completed"] == 1


def test_repair_requires_a_remaining_successor_review_invocation(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "no-successor-review.jsonl"
    finding = {
        "id": "F1",
        "blocking": True,
        "remediation": "automatic-in-scope",
        "anchor": "acceptance",
        "evidence": "failure",
        "required_proof": "proof",
    }
    for event in canonical_review_prefix(
        base, review_budget=1, decision="blocked", findings=[finding]
    ):
        append_event(events, event)
    append_event(
        events,
        {
            "event": "repair-plan",
            "work_item": "parent",
            "data": {
                "charter_id": "parent-charter",
                "generation": 1,
                "review_decision_id": "review-1-decision",
                "review_target": base,
                "finding_ids": ["F1"],
            },
        },
    )
    result, repair = validate_state(events, "repair", repo=repo)
    assert result.returncode == 1
    assert any("successor review invocation" in error for error in repair["errors"])


@pytest.mark.parametrize(
    ("findings", "finding_ids", "budget", "expected"),
    [
        (
            [
                {
                    "id": "F1",
                    "blocking": True,
                    "remediation": "decision-required",
                    "anchor": "public contract",
                    "evidence": "contract change required",
                    "required_proof": "caller decision",
                }
            ],
            ["F1"],
            2,
            "decision-required",
        ),
        (
            [
                {
                    "id": "F1",
                    "blocking": True,
                    "remediation": "automatic-in-scope",
                    "anchor": "acceptance",
                    "evidence": "failure",
                    "required_proof": "proof",
                },
                {
                    "id": "F2",
                    "blocking": True,
                    "remediation": "automatic-in-scope",
                    "anchor": "acceptance",
                    "evidence": "failure",
                    "required_proof": "proof",
                },
            ],
            ["F1"],
            2,
            "every blocking finding ID",
        ),
        (
            [
                {
                    "id": "F1",
                    "blocking": True,
                    "remediation": "automatic-in-scope",
                    "anchor": "acceptance",
                    "evidence": "failure",
                    "required_proof": "proof",
                }
            ],
            ["F1"],
            0,
            "Repair Generation Budget",
        ),
    ],
)
def test_ledger_rejects_unauthorized_or_partial_repair_plans(
    tmp_path: Path,
    findings: list[dict],
    finding_ids: list[str],
    budget: int,
    expected: str,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "rejected-repair.jsonl"
    for event in blocked_review_events(base, findings, budget=budget):
        append_event(events, event)
    append_event(
        events,
        {
            "event": "repair-plan",
            "work_item": "parent",
            "data": {
                "charter_id": "parent-charter",
                "generation": 1,
                "review_decision_id": "review-1",
                "review_target": base,
                "finding_ids": finding_ids,
            },
        },
    )
    result, rejected = validate_state(events, "repair", repo=repo)
    assert result.returncode == 1
    assert any(expected in error for error in rejected["errors"])


def test_ledger_validates_complete_campaign_and_renders_canonical_markdown(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "run" / "events.jsonl"
    batch = tmp_path / "events.json"
    batch.write_text(json.dumps(valid_campaign_events(base)), encoding="utf-8")

    result, appended = helper(
        LEDGER,
        "append-batch",
        "--events",
        str(events),
        "--from-file",
        str(batch),
    )
    assert result.returncode == 0, appended
    assert appended["count"] == len(valid_campaign_events(base))

    result, state = validate_state(events, "complete", repo=repo)
    assert result.returncode == 0, state
    assert state["allowed"] is True
    assert state["campaign_status"] == "complete"

    result, plan = helper(
        LEDGER,
        "closeout-plan",
        "--events",
        str(events),
        "--repo",
        str(repo),
    )
    assert result.returncode == 0, plan
    assert plan["actions"] == []

    ledger = tmp_path / "run" / "LEDGER.md"
    result, rendered = helper(
        LEDGER,
        "render",
        "--events",
        str(events),
        "--output",
        str(ledger),
    )
    assert result.returncode == 0, rendered
    text = ledger.read_text(encoding="utf-8")
    assert "Generated from `events.jsonl`; do not edit." in text
    assert "ticket-1" in text and "ticket implementation" in text


def test_canonical_closeout_requires_one_repairable_friction_synthesis(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "canonical-closeout.jsonl"
    campaign = valid_campaign_events(base)
    campaign[0]["data"]["charter"] = {
        "id": "parent-charter",
        "runtime_contract": 2,
        "repair_generation_budget": 2,
        "review_invocation_budget": 3,
        "review_invocations_required": 1,
    }
    campaign[8] = {
        "event": "review-invocation",
        "event_id": "review-1",
        "work_item": "parent",
        "integration_sha": base,
        "data": {"mode": "initial", "reason": "first integrated candidate"},
    }
    campaign[9]["data"] = {
        "review_invocation_id": "review-1",
        "mode": "initial",
        "findings": [],
    }
    for event in campaign:
        append_event(events, event)

    result, missing = validate_state(events, "complete", repo=repo)
    assert result.returncode == 1
    assert any("Workflow Friction synthesis" in error for error in missing["errors"])

    append_event(
        events,
        {
            "event": "friction",
            "event_id": "friction-synthesis",
            "work_item": "parent",
            "data": {
                "kind": "synthesis",
                "observations": [],
                "deduplicated_themes": [],
                "none_observed": True,
            },
        },
    )
    result, complete = validate_state(events, "complete", repo=repo)
    assert result.returncode == 0, complete

    ledger = tmp_path / "LEDGER.md"
    result, rendered = helper(
        LEDGER,
        "render",
        "--events",
        str(events),
        "--output",
        str(ledger),
    )
    assert result.returncode == 0, rendered
    text = ledger.read_text(encoding="utf-8")
    assert "## Workflow Friction" in text
    assert "None observed." in text


def test_ledger_blocks_wrong_closeout_head_and_unreleased_lane(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    events = tmp_path / "wrong-head.jsonl"
    campaign = valid_campaign_events(base)
    campaign[10]["integration_sha"] = "0" * 40
    for event in campaign:
        append_event(events, event)
    result, state = validate_state(events, "complete", repo=repo)
    assert result.returncode == 1
    assert any("closeout HEAD" in error for error in state["errors"])

    events = tmp_path / "dirty-lane.jsonl"
    campaign = valid_campaign_events(base)
    campaign[-2]["data"]["state"] = "blocked-dirty"
    campaign[-2]["data"]["registered_after"] = True
    for event in campaign:
        append_event(events, event)
    result, state = validate_state(events, "complete", repo=repo)
    assert result.returncode == 1
    assert any("lane-1" in error and "blocked-dirty" in error for error in state["errors"])

    events = tmp_path / "missing-lock.jsonl"
    campaign = [
        event for event in valid_campaign_events(base) if event["event"] != "tracker-lock"
    ]
    for event in campaign:
        append_event(events, event)
    result, state = validate_state(events, "complete", repo=repo)
    assert result.returncode == 1
    assert any("tracker Lock" in error for error in state["errors"])

    events = tmp_path / "cleanup-after-release.jsonl"
    campaign = valid_campaign_events(base)
    campaign[-2], campaign[-1] = campaign[-1], campaign[-2]
    for event in campaign:
        append_event(events, event)
    result, state = validate_state(events, "complete", repo=repo)
    assert result.returncode == 1
    assert any("after release" in error or "active lanes" in error for error in state["errors"])
