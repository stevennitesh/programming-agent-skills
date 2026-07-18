from __future__ import annotations

import argparse
import json
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


def helper(script: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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

    result, budget = helper(
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
        "ticket-3",
        "--max-path",
        "10",
    )
    assert result.returncode == 1
    assert "path budget exceeded" in budget["error"]

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
    append_event(events, {"event": "review-target", "work_item": "parent", "integration_sha": repaired})
    append_event(
        events,
        {
            "event": "review-decision",
            "work_item": "parent",
            "integration_sha": repaired,
            "decision": "pass",
            "data": {"mode": "remediation", "findings": []},
        },
    )
    result, lock = validate_state(events, "lock", repo=repo)
    assert result.returncode == 0, lock


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
            "Repair Budget",
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
