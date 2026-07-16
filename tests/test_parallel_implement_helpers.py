from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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
        "--proof-command-json",
        json.dumps([sys.executable, "-c", "print('started')"]),
    )
    assert result.returncode == 0, preflight
    assert preflight["detached"] is True
    assert preflight["status"] == "clean"
    assert set(preflight["probes"].values()) == {"passed"}
    assert preflight["proof_startup"]["returncode"] == 0
    assert preflight["git_trust"] in {"normal", "command-scoped-safe-directory"}

    result, cleanup = helper(
        LANE,
        "cleanup",
        "--repo",
        str(repo),
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
