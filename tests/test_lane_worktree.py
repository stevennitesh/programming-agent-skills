from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/custom/parallel-implement/scripts/lane_worktree.py"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git(repo: Path, *args: str) -> str:
    result = run("git", "-C", str(repo), *args)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def repository(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    assert run("git", "init", "-b", "main", str(repo)).returncode == 0
    git(repo, "config", "user.name", "Skill Tests")
    git(repo, "config", "user.email", "skills@example.test")
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
    (repo / "test_smoke.py").write_text(
        "def test_smoke():\n    assert True\n", encoding="utf-8"
    )
    git(repo, "add", "tracked.txt", "test_smoke.py")
    git(repo, "commit", "-m", "base")
    return repo, git(repo, "rev-parse", "HEAD")


def helper(*args: str) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    result = run(sys.executable, str(HELPER), *args)
    packet = json.loads(result.stdout)
    return result, packet


def prepare(repo: Path, root: Path, base: str, name: str) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    return helper(
        "prepare",
        "--repo",
        str(repo),
        "--root",
        str(root),
        "--base",
        base,
        "--name",
        name,
    )


def test_prepare_creates_exact_base_and_reusable_pytest_environment(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"

    result, prepared = prepare(repo, lane_root, base, "ticket-67")

    assert result.returncode == 0, prepared
    assert prepared["ok"] is True
    assert prepared["worktree"] == str((lane_root / "ticket-67").resolve())
    assert prepared["base"] == base
    assert prepared["reused"] is False
    assert prepared["pytest"] == "passed"
    worktree = Path(str(prepared["worktree"]))
    assert git(worktree, "rev-parse", "HEAD") == base
    assert git(worktree, "status", "--porcelain") == ""
    for field in ("temp_root", "pytest_basetemp", "pytest_cache"):
        path = Path(str(prepared[field]))
        assert path.is_dir()
        assert not path.is_relative_to(worktree)
        assert path.is_relative_to(lane_root / ".state" / "ticket-67")


def test_prepare_skips_pytest_when_checkout_does_not_declare_it(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    git(repo, "rm", "test_smoke.py")
    git(repo, "commit", "-m", "remove pytest surface")
    base = git(repo, "rev-parse", "HEAD")

    lane_root = tmp_path / "lanes"
    result, prepared = prepare(repo, lane_root, base, "non-pytest")

    assert result.returncode == 0, prepared
    assert prepared["ok"] is True
    assert prepared["pytest"] == "not-applicable"
    for field in ("temp_root", "pytest_basetemp", "pytest_cache"):
        assert Path(str(prepared[field])).is_dir()
        assert Path(str(prepared[field])).is_relative_to(
            lane_root / ".state" / "non-pytest"
        )


def test_prepare_detects_arbitrary_depth_tracked_python_tests(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    git(repo, "rm", "test_smoke.py")
    nested = repo / "backend" / "components" / "feature" / "specs" / "test_deep.py"
    nested.parent.mkdir(parents=True)
    nested.write_text("def test_deep():\n    assert True\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "move test to arbitrary tracked depth")
    base = git(repo, "rev-parse", "HEAD")

    result, prepared = prepare(repo, tmp_path / "lanes", base, "deep-pytest")

    assert result.returncode == 0, prepared
    assert prepared["pytest"] == "passed"


def test_prepare_blocks_on_pytest_collection_failure_and_reclaims_new_lane(
    tmp_path: Path,
) -> None:
    repo, _ = repository(tmp_path)
    (repo / "test_smoke.py").write_text("def broken(:\n", encoding="utf-8")
    git(repo, "add", "test_smoke.py")
    git(repo, "commit", "-m", "break collection")
    base = git(repo, "rev-parse", "HEAD")
    lane_root = tmp_path / "lanes"

    result, blocked = prepare(repo, lane_root, base, "broken")

    assert result.returncode == 1
    assert blocked["ok"] is False
    assert "pytest collection failed" in str(blocked["error"])
    assert "worktree" not in blocked
    assert not (lane_root / "broken").exists()
    assert not (lane_root / ".state" / "broken").exists()


def test_prepare_preserves_reused_lane_after_pytest_failure(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    (repo / "test_smoke.py").write_text("def broken(:\n", encoding="utf-8")
    git(repo, "add", "test_smoke.py")
    git(repo, "commit", "-m", "break collection")
    base = git(repo, "rev-parse", "HEAD")
    lane_root = tmp_path / "lanes"
    worktree = lane_root / "reused-broken"
    assert run(
        "git", "-C", str(repo), "worktree", "add", "--detach", str(worktree), base
    ).returncode == 0

    result, blocked = prepare(repo, lane_root, base, "reused-broken")

    assert result.returncode == 1
    assert "pytest collection failed" in str(blocked["error"])
    assert blocked["worktree"] == str(worktree.resolve())
    assert worktree.exists()


def test_prepare_reuses_only_the_clean_expected_base(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    first_result, first = prepare(repo, lane_root, base, "reused")
    assert first_result.returncode == 0, first

    second_result, second = prepare(repo, lane_root, base, "reused")
    assert second_result.returncode == 0, second
    assert second["reused"] is True

    worktree = Path(str(second["worktree"]))
    (worktree / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    dirty_result, dirty = prepare(repo, lane_root, base, "reused")
    assert dirty_result.returncode == 1
    assert "not clean" in str(dirty["error"])


def test_cleanup_removes_oldest_safe_and_preserves_active_dirty_and_unintegrated(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    prepared: dict[str, Path] = {}
    for name in ("oldest", "newer", "active", "uncertain", "dirty", "unintegrated"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        prepared[name] = Path(str(packet["worktree"]))

    os.utime(prepared["oldest"], (1, 1))
    os.utime(prepared["newer"], (2, 2))
    (prepared["dirty"] / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    (prepared["unintegrated"] / "new.txt").write_text("new\n", encoding="utf-8")
    git(prepared["unintegrated"], "add", "new.txt")
    git(prepared["unintegrated"], "commit", "-m", "not integrated")

    result, cleaned = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--oldest",
        "--completed",
        str(prepared["oldest"]),
        "--completed",
        str(prepared["newer"]),
        "--completed",
        str(prepared["dirty"]),
        "--completed",
        str(prepared["unintegrated"]),
    )

    assert result.returncode == 0, cleaned
    assert cleaned["removed"] == [str(prepared["oldest"].resolve())]
    assert not prepared["oldest"].exists()
    for name in ("newer", "active", "uncertain", "dirty", "unintegrated"):
        assert prepared[name].exists()
    reasons = {Path(item["worktree"]).name: item["reason"] for item in cleaned["preserved"]}
    assert reasons == {
        "newer": "capacity retained",
        "active": "not completed",
        "uncertain": "not completed",
        "dirty": "not clean",
        "unintegrated": "not integrated",
    }


def test_graph_end_cleanup_removes_all_safe_lanes(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("one", "two"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktrees.append(Path(str(packet["worktree"])))

    arguments = ["cleanup", "--repo", str(repo), "--root", str(lane_root)]
    for worktree in worktrees:
        arguments.extend(["--completed", str(worktree)])
    result, cleaned = helper(*arguments)

    assert result.returncode == 0, cleaned
    assert cleaned["removed"] == [str(path.resolve()) for path in worktrees]
    assert all(not path.exists() for path in worktrees)


def test_cleanup_rejects_completed_lane_outside_exact_root(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    first_root = tmp_path / "first-lanes"
    result, packet = prepare(repo, first_root, base, "complete")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    other_root = tmp_path / "other-lanes"

    result, blocked = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(other_root),
        "--completed",
        str(worktree),
    )

    assert result.returncode == 1
    assert blocked["ok"] is False
    assert "outside the configured root" in str(blocked["error"])
    assert not other_root.exists()
    assert worktree.exists()


def test_cleanup_rejects_unregistered_completed_lane(tmp_path: Path) -> None:
    repo, _ = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    lane_root.mkdir()
    unregistered = lane_root / "not-registered"

    result, blocked = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--completed",
        str(unregistered),
    )

    assert result.returncode == 1
    assert blocked["ok"] is False
    assert "not a registered worktree" in str(blocked["error"])


def test_cleanup_rejects_nested_registered_worktree(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    nested = lane_root / "nested" / "lane"
    nested.parent.mkdir(parents=True)
    assert run(
        "git", "-C", str(repo), "worktree", "add", "--detach", str(nested), base
    ).returncode == 0

    result, blocked = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--completed",
        str(nested),
    )

    assert result.returncode == 1
    assert blocked["ok"] is False
    assert "not a direct child of the configured root" in str(blocked["error"])
    assert nested.exists()


def test_cleanup_rejects_reserved_state_worktree_name(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    reserved = lane_root / ".state"
    lane_root.mkdir()
    assert run(
        "git", "-C", str(repo), "worktree", "add", "--detach", str(reserved), base
    ).returncode == 0

    result, blocked = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--completed",
        str(reserved),
    )

    assert result.returncode == 1
    assert blocked["ok"] is False
    assert "does not match prepare lane naming" in str(blocked["error"])
    assert reserved.exists()


def test_cleanup_removes_helper_owned_lane_state(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "preserve-state")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    sentinel = Path(str(packet["pytest_cache"])) / "sentinel.txt"
    sentinel.write_text("keep\n", encoding="utf-8")

    result, cleaned = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--completed",
        str(worktree),
    )

    assert result.returncode == 0, cleaned
    assert cleaned["removed"] == [str(worktree.resolve())]
    assert not worktree.exists()
    assert not sentinel.exists()


def test_capacity_cleanup_returns_blocker_when_no_lane_is_safe(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "active")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))

    result, blocked = helper(
        "cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--oldest",
    )

    assert result.returncode == 2
    assert blocked["ok"] is False
    assert blocked["error"] == "capacity blocked: no safe completed worktree"
    assert worktree.exists()


def test_prepare_blocks_wrong_base_and_unregistered_target(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"

    result, wrong_base = prepare(repo, lane_root, "missing-base", "wrong-base")
    assert result.returncode == 1
    assert wrong_base["ok"] is False
    assert not (lane_root / "wrong-base").exists()

    unregistered = lane_root / "unregistered"
    unregistered.mkdir(parents=True)
    result, blocked = prepare(repo, lane_root, base, "unregistered")
    assert result.returncode == 1
    assert "not a registered worktree" in str(blocked["error"])


def test_prepare_reports_worktree_creation_failure(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    namespace = runpy.run_path(str(HELPER))
    prepare_lane = namespace["prepare"]
    original_git = prepare_lane.__globals__["git"]

    def failing_git(checkout, *args, check=True):
        if args[:2] == ("worktree", "add"):
            return subprocess.CompletedProcess(args, 1, "", "creation denied")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(prepare_lane.__globals__, "git", failing_git)
    with pytest.raises(namespace["LaneError"], match="creation denied"):
        prepare_lane(
            Namespace(repo=str(repo), root=str(lane_root), base=base, name="failed")
        )


def test_cleanup_reports_partial_failure_and_oldest_falls_through(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("first", "second"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktrees.append(Path(str(packet["worktree"])))
    os.utime(worktrees[0], (1, 1))
    os.utime(worktrees[1], (2, 2))

    namespace = runpy.run_path(str(HELPER))
    cleanup = namespace["cleanup"]
    original_git = cleanup.__globals__["git"]

    def fail_first_remove(checkout, *args, check=True):
        if args[:3] == ("worktree", "remove", str(worktrees[0])):
            return subprocess.CompletedProcess(args, 1, "", "worktree locked")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup.__globals__, "git", fail_first_remove)
    common = Namespace(
        repo=str(repo),
        root=str(lane_root),
        completed=[str(path) for path in worktrees],
        oldest=True,
    )
    code, packet = cleanup(common)
    assert code == 0
    assert packet["ok"] is True
    assert packet["removed"] == [str(worktrees[1])]
    assert packet["preserved"] == [
        {
            "worktree": str(worktrees[0]),
            "reason": "remove failed",
            "error": "worktree locked",
            "lane_state": "removed",
            "worktree_state": "registered",
            "path_state": "present",
        }
    ]

    common.oldest = False
    common.completed = [str(worktrees[0])]
    code, packet = cleanup(common)
    assert code == 1
    assert packet["ok"] is False
    assert packet["error"] == "cleanup incomplete"
    assert packet["preserved"][0]["error"] == "worktree locked"
    assert packet["preserved"][0]["lane_state"] == "absent"
    assert packet["preserved"][0]["worktree_state"] == "registered"
    assert packet["preserved"][0]["path_state"] == "present"


def test_cleanup_reports_removed_when_git_unregisters_before_error(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "unregistered-first")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))

    namespace = runpy.run_path(str(HELPER))
    cleanup = namespace["cleanup"]
    original_git = cleanup.__globals__["git"]

    def remove_then_error(checkout, *args, check=True):
        if args[:3] == ("worktree", "remove", str(worktree)):
            removed = original_git(checkout, *args, check=check)
            assert removed.returncode == 0
            return subprocess.CompletedProcess(args, 1, "", "late filesystem error")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup.__globals__, "git", remove_then_error)
    code, cleaned = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(worktree)],
            oldest=False,
        )
    )

    assert code == 0
    assert cleaned == {"ok": True, "removed": [str(worktree)], "preserved": []}


def test_cleanup_reports_unregistered_residual_path_after_remove_error(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "residual-path")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))

    namespace = runpy.run_path(str(HELPER))
    cleanup = namespace["cleanup"]
    original_git = cleanup.__globals__["git"]

    def remove_then_leave_path(checkout, *args, check=True):
        if args[:3] == ("worktree", "remove", str(worktree)):
            removed = original_git(checkout, *args, check=check)
            assert removed.returncode == 0
            worktree.mkdir()
            return subprocess.CompletedProcess(args, 1, "", "late filesystem error")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup.__globals__, "git", remove_then_leave_path)
    code, cleaned = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(worktree)],
            oldest=False,
        )
    )

    assert code == 1
    assert cleaned["ok"] is False
    assert cleaned["preserved"] == [
        {
            "worktree": str(worktree),
            "reason": "remove incomplete",
            "error": "late filesystem error",
            "lane_state": "removed",
            "worktree_state": "unregistered",
            "path_state": "present",
        }
    ]


def test_capacity_cleanup_falls_through_after_lane_state_failure(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("first", "second"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktrees.append(Path(str(packet["worktree"])))
    os.utime(worktrees[0], (1, 1))
    os.utime(worktrees[1], (2, 2))

    namespace = runpy.run_path(str(HELPER))
    cleanup = namespace["cleanup"]
    original_rmtree = cleanup.__globals__["shutil"].rmtree
    first_state = lane_root / ".state" / "first"

    def fail_first_state(path):
        if Path(path) == first_state:
            raise OSError("state locked")
        return original_rmtree(path)

    monkeypatch.setattr(cleanup.__globals__["shutil"], "rmtree", fail_first_state)
    code, packet = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(path) for path in worktrees],
            oldest=True,
        )
    )

    assert code == 0
    assert packet["ok"] is True
    assert packet["removed"] == [str(worktrees[1])]
    assert packet["preserved"] == [
        {
            "worktree": str(worktrees[0]),
            "reason": "lane state cleanup failed",
            "error": "state locked",
        }
    ]
    assert worktrees[0].exists()
    assert first_state.exists()
    assert not worktrees[1].exists()


def test_cleanup_preserves_git_uncertainty(tmp_path: Path, monkeypatch) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "uncertain")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))

    namespace = runpy.run_path(str(HELPER))
    cleanup = namespace["cleanup"]
    original_git = cleanup.__globals__["git"]

    def fail_status(checkout, *args, check=True):
        if checkout == worktree and args[:2] == ("status", "--porcelain"):
            return subprocess.CompletedProcess(args, 1, "", "status denied")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup.__globals__, "git", fail_status)
    code, cleaned = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(worktree)],
            oldest=False,
        )
    )

    assert code == 0
    assert cleaned == {
        "ok": True,
        "removed": [],
        "preserved": [{"worktree": str(worktree), "reason": "uncertain"}],
    }
    assert worktree.exists()
