from __future__ import annotations

import json
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


def test_prepare_creates_exact_base_and_isolated_temp_environment(
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
    worktree = Path(str(prepared["worktree"]))
    assert git(worktree, "rev-parse", "HEAD") == base
    assert git(worktree, "status", "--porcelain") == ""
    assert prepared["schema_version"] == 1
    assert prepared["repository"] == str(repo.resolve())
    for field in (
        "runtime_root",
        "temp_root",
        "cache_root",
        "pytest_basetemp",
        "pytest_cache",
    ):
        path = Path(str(prepared[field]))
        assert path.is_dir()
        assert not path.is_relative_to(worktree)
        assert path.is_relative_to(lane_root / ".state" / "ticket-67")
    manifest = Path(str(prepared["lane_manifest"]))
    assert json.loads(manifest.read_text(encoding="utf-8")) == {
        key: value for key, value in prepared.items() if key not in {"ok", "reused"}
    }
    assert Path(str(prepared["cleanup_receipt"])) == (
        lane_root / ".state" / "ticket-67.cleanup.json"
    ).resolve()


def test_prepare_rolls_back_when_a_runtime_probe_fails(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    namespace = runpy.run_path(str(HELPER))
    prepare_lane = namespace["prepare"]
    original_probe = prepare_lane.__globals__["probe_directory"]

    def fail_cache(path: Path) -> None:
        if Path(path).name == "cache":
            raise OSError("cache probe denied")
        original_probe(path)

    monkeypatch.setitem(prepare_lane.__globals__, "probe_directory", fail_cache)
    with pytest.raises(namespace["LaneError"], match="cache probe denied"):
        prepare_lane(
            Namespace(repo=str(repo), root=str(lane_root), base=base, name="probe")
        )
    assert not (lane_root / "probe").exists()
    assert not (lane_root / ".state" / "probe").exists()


def test_inspect_reports_lane_runtime_and_checkout_cache_violations(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, prepared = prepare(repo, lane_root, base, "inspectable")
    assert result.returncode == 0, prepared
    worktree = Path(str(prepared["worktree"]))

    result, inspected = helper(
        "inspect",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--lane",
        str(worktree),
    )
    assert result.returncode == 0, inspected
    assert inspected["manifest"] == {
        "valid": True,
        "schema_version": 1,
        "error": None,
    }
    assert inspected["registered"] is True
    assert inspected["clean"] is True
    assert inspected["integrated"] is True
    assert inspected["checkout_cache_violations"] == []
    assert inspected["mechanical"] == {
        "resume_or_land_eligible": True,
        "cleanup_eligible": True,
        "actor_quiescence_unverified": True,
    }
    assert set(inspected["runtime"]) == {
        "runtime_root",
        "temp_root",
        "cache_root",
        "pytest_basetemp",
        "pytest_cache",
    }

    (worktree / ".tmp" / "uv-cache").mkdir(parents=True)
    (worktree / ".pytest_cache").mkdir()
    (worktree / ".tmp" / "uv-cache" / "entry").write_text("cache", encoding="utf-8")
    (worktree / ".pytest_cache" / "entry").write_text("cache", encoding="utf-8")
    result, inspected = helper(
        "inspect",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--lane",
        str(worktree),
    )
    assert result.returncode == 0, inspected
    assert inspected["clean"] is False
    assert inspected["mechanical"]["resume_or_land_eligible"] is False
    assert inspected["checkout_cache_violations"] == [
        str(worktree / ".tmp" / "uv-cache"),
        str(worktree / ".pytest_cache"),
    ]


def test_inspect_never_marks_uncertain_residual_ancestry_cleanup_eligible(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, prepared = prepare(repo, lane_root, base, "residual")
    assert result.returncode == 0, prepared
    worktree = Path(str(prepared["worktree"]))
    namespace = runpy.run_path(str(HELPER))
    write_receipt = namespace["write_cleanup_receipt"]
    write_receipt(repo.resolve(), lane_root.resolve(), worktree, base, base)
    git(repo, "worktree", "remove", str(worktree))

    inspect_lane = namespace["inspect_lane"]
    original_git = inspect_lane.__globals__["git"]

    def uncertain_ancestry(checkout, *args, check=True):
        if args[:2] == ("merge-base", "--is-ancestor"):
            return subprocess.CompletedProcess(args, 2, "", "ancestry unavailable")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(inspect_lane.__globals__, "git", uncertain_ancestry)
    code, inspected = inspect_lane(
        Namespace(repo=str(repo), root=str(lane_root), lane=str(worktree))
    )
    assert code == 0
    assert inspected["integrated"] is None
    assert inspected["mechanical"]["cleanup_eligible"] is False


def test_inspect_rejects_a_redirected_runtime_path(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, prepared = prepare(repo, lane_root, base, "redirected")
    assert result.returncode == 0, prepared
    worktree = Path(str(prepared["worktree"]))
    cache_root = Path(str(prepared["cache_root"]))
    namespace = runpy.run_path(str(HELPER))
    inspect_lane = namespace["inspect_lane"]
    original_reparse = inspect_lane.__globals__["is_reparse_point"]

    def redirect_cache(path: Path) -> bool:
        return Path(path) == cache_root or original_reparse(path)

    monkeypatch.setitem(
        inspect_lane.__globals__, "is_reparse_point", redirect_cache
    )
    code, inspected = inspect_lane(
        Namespace(repo=str(repo), root=str(lane_root), lane=str(worktree))
    )
    assert code == 0
    assert inspected["runtime"]["cache_root"] == {
        "path": str(cache_root),
        "exists": True,
        "directory": False,
        "error": "runtime path is a reparse point",
    }
    assert inspected["mechanical"]["resume_or_land_eligible"] is False


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


def test_dependent_lane_uses_integration_head_after_predecessor_lands(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    first_result, first = prepare(repo, lane_root, base, "first")
    assert first_result.returncode == 0, first
    first_lane = Path(str(first["worktree"]))

    (first_lane / "predecessor.txt").write_text("landed\n", encoding="utf-8")
    git(first_lane, "add", "predecessor.txt")
    git(first_lane, "commit", "-m", "predecessor")
    git(repo, "merge", "--ff-only", git(first_lane, "rev-parse", "HEAD"))
    current_head = git(repo, "rev-parse", "HEAD")

    second_result, second = prepare(repo, lane_root, current_head, "dependent")
    assert second_result.returncode == 0, second
    second_lane = Path(str(second["worktree"]))
    assert git(second_lane, "rev-parse", "HEAD") == current_head
    assert (second_lane / "predecessor.txt").read_text(encoding="utf-8") == "landed\n"


def test_cleanup_accepts_fast_forward_and_merged_sibling_commits(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    prepared: list[Path] = []
    heads: list[str] = []
    for name in ("first", "second"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        lane = Path(str(packet["worktree"]))
        (lane / f"{name}.txt").write_text(f"{name}\n", encoding="utf-8")
        git(lane, "add", f"{name}.txt")
        git(lane, "commit", "-m", name)
        prepared.append(lane)
        heads.append(git(lane, "rev-parse", "HEAD"))

    git(repo, "merge", "--ff-only", heads[0])
    git(repo, "merge", "--no-ff", "-m", "merge second", heads[1])
    integration_head = git(repo, "rev-parse", "HEAD")
    for head in heads:
        git(repo, "merge-base", "--is-ancestor", head, integration_head)

    arguments = ["cleanup", "--repo", str(repo), "--root", str(lane_root)]
    for lane in prepared:
        arguments.extend(["--completed", str(lane)])
    result, cleaned = helper(*arguments)

    assert result.returncode == 0, cleaned
    assert cleaned["removed"] == [str(lane.resolve()) for lane in prepared]


def test_cleanup_removes_named_safe_lanes_and_preserves_dirty_and_unintegrated(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    prepared: dict[str, Path] = {}
    for name in ("oldest", "newer", "active", "uncertain", "dirty", "unintegrated"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        prepared[name] = Path(str(packet["worktree"]))

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
        "--completed",
        str(prepared["oldest"]),
        "--completed",
        str(prepared["newer"]),
        "--completed",
        str(prepared["dirty"]),
        "--completed",
        str(prepared["unintegrated"]),
    )

    assert result.returncode == 1, cleaned
    assert cleaned["removed"] == [
        str(prepared["oldest"].resolve()),
        str(prepared["newer"].resolve()),
    ]
    assert not prepared["oldest"].exists()
    assert not prepared["newer"].exists()
    for name in ("active", "uncertain", "dirty", "unintegrated"):
        assert prepared[name].exists()
    reasons = {Path(item["worktree"]).name: item["reason"] for item in cleaned["preserved"]}
    assert reasons == {
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
    verify_arguments = [
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        base,
    ]
    for worktree in worktrees:
        verify_arguments.extend(["--lane", str(worktree)])
    result, verified = helper(*verify_arguments)
    assert result.returncode == 0, verified
    assert verified["finish_clean"] is True


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
    assert blocked["error"] == "cleanup incomplete"
    assert blocked["preserved"][0]["reason"] == "cleanup receipt is missing"


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
    assert worktree not in {
        Path(path.removeprefix("worktree ")).resolve()
        for path in git(repo, "worktree", "list", "--porcelain").splitlines()
        if path.startswith("worktree ")
    }
    assert not (lane_root / ".state" / "preserve-state").exists()


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


def test_prepare_rollback_preserves_state_until_worktree_removal_is_confirmed(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "rollback")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    state = lane_root / ".state" / "rollback"
    marker = state / "recovery.txt"
    marker.write_text("inspectable\n", encoding="utf-8")

    namespace = runpy.run_path(str(HELPER))
    rollback = namespace["rollback_created_lane"]
    original_git = rollback.__globals__["git"]

    def fail_remove(checkout, *args, check=True):
        if args[:3] == ("worktree", "remove", str(worktree)):
            return subprocess.CompletedProcess(args, 1, "", "worktree locked")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(rollback.__globals__, "git", fail_remove)
    blocked = rollback(repo, lane_root, worktree, base, "rollback")

    assert blocked is not None
    assert "worktree removal failed: worktree locked" in blocked
    assert "lane state preserved; worktree registered; path present" in blocked
    assert marker.read_text(encoding="utf-8") == "inspectable\n"
    assert worktree in {
        Path(path.removeprefix("worktree ")).resolve()
        for path in git(repo, "worktree", "list", "--porcelain").splitlines()
        if path.startswith("worktree ")
    }

    monkeypatch.setitem(rollback.__globals__, "git", original_git)
    assert rollback(repo, lane_root, worktree, base, "rollback") is None
    assert not worktree.exists()
    assert not state.exists()


def test_cleanup_reports_partial_failure_and_continues_named_lanes(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("first", "second"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktrees.append(Path(str(packet["worktree"])))

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
    )
    code, packet = cleanup(common)
    assert code == 1
    assert packet["ok"] is False
    assert packet["error"] == "cleanup incomplete"
    assert packet["removed"] == [str(worktrees[1])]
    assert packet["preserved"] == [
        {
            "worktree": str(worktrees[0]),
                "reason": "remove failed",
                "phase": "worktree removal",
                "path": str(worktrees[0]),
                "error": "worktree locked",
                "errno": None,
                "winerror": None,
                "retry_count": 0,
            "lane_state": "preserved",
            "worktree_state": "registered",
            "path_state": "present",
        }
    ]
    first_state = lane_root / ".state" / "first"
    assert first_state.exists()

    monkeypatch.setitem(cleanup.__globals__, "git", original_git)
    common.completed = [str(worktrees[0])]
    code, packet = cleanup(common)
    assert code == 0
    assert packet == {"ok": True, "removed": [str(worktrees[0])], "preserved": []}
    assert not worktrees[0].exists()
    assert not first_state.exists()


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
        )
    )

    assert code == 0
    assert cleaned == {"ok": True, "removed": [str(worktree)], "preserved": []}
    assert not (lane_root / ".state" / "unregistered-first").exists()


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
            (worktree / "residual.txt").write_text("retry me\n", encoding="utf-8")
            return subprocess.CompletedProcess(args, 1, "", "late filesystem error")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup.__globals__, "git", remove_then_leave_path)
    code, cleaned = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(worktree)],
        )
    )

    assert code == 1
    assert cleaned["ok"] is False
    assert cleaned["preserved"] == [
        {
            "worktree": str(worktree),
                "reason": "remove failed",
                "phase": "worktree removal",
                "path": str(worktree),
                "error": "late filesystem error",
                "errno": None,
                "winerror": None,
                "retry_count": 0,
            "lane_state": "preserved",
            "worktree_state": "unregistered",
            "path_state": "present",
        }
    ]
    state = lane_root / ".state" / "residual-path"
    receipt = lane_root / ".state" / "residual-path.cleanup.json"
    assert state.exists()
    assert receipt.is_file()

    monkeypatch.setitem(cleanup.__globals__, "git", original_git)
    arguments = Namespace(
        repo=str(repo),
        root=str(lane_root),
        completed=[str(worktree)],
    )

    receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
    receipt_payload["repository"] = str(repo / "wrong")
    receipt.write_text(json.dumps(receipt_payload), encoding="utf-8")
    code, blocked = cleanup(arguments)
    assert code == 1
    assert blocked["error"] == "cleanup incomplete"
    assert blocked["preserved"][0]["reason"] == (
        "cleanup receipt does not match the requested lane"
    )
    assert (worktree / "residual.txt").exists()
    assert state.exists()

    receipt_payload["repository"] = str(repo)
    receipt.write_text(json.dumps(receipt_payload), encoding="utf-8")
    monkeypatch.setitem(
        cleanup.__globals__, "tree_has_reparse_point", lambda _path: True
    )
    code, blocked = cleanup(arguments)
    assert code == 1
    assert blocked["preserved"][0]["reason"] == (
        "unregistered residual path contains a reparse point"
    )
    assert worktree.exists()

    monkeypatch.setitem(
        cleanup.__globals__, "tree_has_reparse_point", lambda _path: False
    )
    code, retried = cleanup(arguments)
    assert code == 0
    assert retried == {"ok": True, "removed": [str(worktree)], "preserved": []}
    assert not worktree.exists()
    assert not state.exists()
    assert not receipt.exists()


def test_cleanup_preserves_failed_lane_state_and_continues_named_lanes(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("first", "second"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktrees.append(Path(str(packet["worktree"])))

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
        )
    )

    assert code == 1
    assert packet["ok"] is False
    assert packet["error"] == "cleanup incomplete"
    assert packet["removed"] == [str(worktrees[1])]
    assert packet["preserved"] == [
        {
            "worktree": str(worktrees[0]),
            "reason": "cleanup incomplete",
            "lane_state": "preserved",
            "worktree_state": "unregistered",
            "path_state": "missing",
            "phase": "lane state cleanup",
            "path": str(first_state),
            "error": "state locked",
            "errno": None,
            "winerror": None,
            "retry_count": 0,
        }
    ]
    assert not worktrees[0].exists()
    assert first_state.exists()
    assert not worktrees[1].exists()
    first_receipt = lane_root / ".state" / "first.cleanup.json"
    assert first_receipt.is_file()

    monkeypatch.setattr(cleanup.__globals__["shutil"], "rmtree", original_rmtree)
    code, retried = cleanup(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(worktrees[0])],
        )
    )
    assert code == 0
    assert retried == {
        "ok": True,
        "removed": [str(worktrees[0])],
        "preserved": [],
    }
    assert not first_state.exists()
    assert not first_receipt.exists()


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
        )
    )

    assert code == 1
    assert cleaned == {
        "ok": False,
        "removed": [],
        "preserved": [{"worktree": str(worktree), "reason": "uncertain"}],
        "error": "cleanup incomplete",
    }
    assert worktree.exists()


def test_remove_tree_retries_only_named_windows_errors(
    tmp_path: Path, monkeypatch,
) -> None:
    namespace = runpy.run_path(str(HELPER))
    remove_tree = namespace["remove_tree"]
    original_rmtree = remove_tree.__globals__["shutil"].rmtree
    calls = 0
    target = tmp_path / "runtime"
    target.mkdir()

    def transient(path: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            error = OSError(5, "sharing violation")
            error.winerror = 32
            raise error
        original_rmtree(path)

    monkeypatch.setattr(remove_tree.__globals__["shutil"], "rmtree", transient)
    monkeypatch.setattr(remove_tree.__globals__["time"], "sleep", lambda _delay: None)
    assert remove_tree(
        target, phase="runtime cleanup", receipt_authorized=False
    ) is None
    assert calls == 2

    target.mkdir()

    def persistent(path: Path) -> None:
        error = OSError(13, "denied")
        raise error

    monkeypatch.setattr(remove_tree.__globals__["shutil"], "rmtree", persistent)
    assert remove_tree(
        target, phase="runtime cleanup", receipt_authorized=False
    ) == {
        "phase": "runtime cleanup",
        "path": str(target),
        "error": "[Errno 13] denied",
        "errno": 13,
        "winerror": None,
        "retry_count": 0,
    }


def test_prepare_rejects_pending_cleanup_and_residual_state(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "stale")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))

    namespace = runpy.run_path(str(HELPER))
    namespace["write_cleanup_receipt"](
        repo.resolve(), lane_root.resolve(), worktree, base, base
    )
    result, blocked = prepare(repo, lane_root, base, "stale")
    assert result.returncode == 1
    assert "pending cleanup" in str(blocked["error"])

    Path(str(packet["cleanup_receipt"])).unlink()
    git(repo, "worktree", "remove", str(worktree))
    result, blocked = prepare(repo, lane_root, base, "stale")
    assert result.returncode == 1
    assert "residual helper state" in str(blocked["error"])


def test_cleanup_preserves_registered_lane_when_runtime_cleanup_fails(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "runtime-locked")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    cache = Path(str(packet["cache_root"]))
    (cache / "large.bin").write_bytes(b"x" * 1024)

    namespace = runpy.run_path(str(HELPER))
    cleanup_lane = namespace["cleanup"]
    original_remove_tree = cleanup_lane.__globals__["remove_tree"]

    def fail_cache(path, *, phase, receipt_authorized):
        if Path(path) == cache:
            return {
                "phase": phase,
                "path": str(path),
                "error": "cache locked",
                "errno": 13,
                "winerror": 5,
                "retry_count": 4,
            }
        return original_remove_tree(
            path, phase=phase, receipt_authorized=receipt_authorized
        )

    monkeypatch.setitem(
        cleanup_lane.__globals__, "remove_tree", fail_cache
    )
    code, blocked = cleanup_lane(
        Namespace(repo=str(repo), root=str(lane_root), completed=[str(worktree)])
    )
    assert code == 1
    assert blocked["preserved"][0]["reason"] == "runtime cleanup incomplete"
    assert worktree.exists()
    assert worktree in {
        Path(path.removeprefix("worktree ")).resolve()
        for path in git(repo, "worktree", "list", "--porcelain").splitlines()
        if path.startswith("worktree ")
    }
    assert Path(str(packet["lane_manifest"])).is_file()
    assert Path(str(packet["cleanup_receipt"])).is_file()

    monkeypatch.setitem(
        cleanup_lane.__globals__, "remove_tree", original_remove_tree
    )
    code, cleaned = cleanup_lane(
        Namespace(repo=str(repo), root=str(lane_root), completed=[str(worktree)])
    )
    assert code == 0, cleaned
    assert not worktree.exists()
    assert not Path(str(packet["runtime_root"])).exists()
    assert not Path(str(packet["cleanup_receipt"])).exists()


def test_cleanup_reports_runtime_enumeration_failure_and_continues(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    packets = []
    for name in ("blocked", "cleaned"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        packets.append(packet)

    namespace = runpy.run_path(str(HELPER))
    cleanup_lane = namespace["cleanup"]
    path_type = type(Path())
    original_iterdir = path_type.iterdir
    blocked_state = Path(str(packets[0]["runtime_root"]))

    def fail_blocked_state(path):
        if Path(path) == blocked_state:
            raise OSError("state enumeration denied")
        return original_iterdir(path)

    monkeypatch.setattr(path_type, "iterdir", fail_blocked_state)
    code, packet = cleanup_lane(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            completed=[str(item["worktree"]) for item in packets],
        )
    )
    assert code == 1
    assert packet["preserved"][0]["reason"] == "runtime cleanup incomplete"
    assert packet["preserved"][0]["phase"] == "lane runtime enumeration"
    assert packet["removed"] == [str(Path(str(packets[1]["worktree"])).resolve())]


def test_cleanup_receipt_requires_valid_read_back(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "receipt")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    namespace = runpy.run_path(str(HELPER))
    write_receipt = namespace["write_cleanup_receipt"]
    monkeypatch.setitem(
        write_receipt.__globals__,
        "read_cleanup_receipt",
        lambda *_args: (None, "simulated read-back failure"),
    )
    with pytest.raises(namespace["LaneError"], match="read-back failed"):
        write_receipt(repo.resolve(), lane_root.resolve(), worktree, base, base)
    assert worktree.exists()


def test_cleanup_rechecks_repository_identity_before_unregistering(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "head-drift")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    namespace = runpy.run_path(str(HELPER))
    cleanup_lane = namespace["cleanup"]
    original_git = cleanup_lane.__globals__["git"]
    repo_head_reads = 0

    def drift_after_receipt(checkout, *args, check=True):
        nonlocal repo_head_reads
        if Path(checkout) == repo.resolve() and args[:2] == ("rev-parse", "HEAD"):
            repo_head_reads += 1
            if repo_head_reads > 1:
                return subprocess.CompletedProcess(args, 0, "0" * 40 + "\n", "")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(cleanup_lane.__globals__, "git", drift_after_receipt)
    code, blocked = cleanup_lane(
        Namespace(repo=str(repo), root=str(lane_root), completed=[str(worktree)])
    )
    assert code == 1
    assert blocked["preserved"][0]["reason"] == "cleanup identity changed"
    assert worktree.exists()
    assert Path(str(packet["cleanup_receipt"])).is_file()


def test_verify_cleanup_accounts_for_every_explicit_lane(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    worktrees = []
    for name in ("one", "two"):
        result, packet = prepare(repo, lane_root, base, name)
        assert result.returncode == 0, packet
        worktree = Path(str(packet["worktree"]))
        worktrees.append(worktree)
        namespace = runpy.run_path(str(HELPER))
        namespace["write_cleanup_receipt"](
            repo.resolve(), lane_root.resolve(), worktree, base, base
        )
        git(repo, "worktree", "remove", str(worktree))

    arguments = [
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        base,
    ]
    for worktree in worktrees:
        arguments.extend(["--lane", str(worktree)])

    result, blocked = helper(*arguments)
    assert result.returncode == 1
    assert blocked["finish_clean"] is False
    assert blocked["retry_cleanup"] == [str(path.resolve()) for path in worktrees]
    assert {
        item["required_action"] for item in blocked["lanes"]
    } == {"retry-cleanup"}

    cleanup_arguments = ["cleanup", "--repo", str(repo), "--root", str(lane_root)]
    for worktree in worktrees:
        cleanup_arguments.extend(["--completed", str(worktree)])
    result, cleaned = helper(*cleanup_arguments)
    assert result.returncode == 0, cleaned

    result, verified = helper(*arguments)
    assert result.returncode == 0, verified
    assert verified["finish_clean"] is True
    assert all(item["required_action"] == "none" for item in verified["lanes"])


def test_verify_cleanup_requires_lane_inventory_and_exact_commit_id(
    tmp_path: Path,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    lane_root.mkdir()

    result, blocked = helper(
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        base,
    )
    assert result.returncode == 1
    assert "at least one --lane" in str(blocked["error"])

    lane = lane_root / "complete"
    result, blocked = helper(
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        "HEAD",
        "--lane",
        str(lane),
    )
    assert result.returncode == 1
    assert "full commit ID" in str(blocked["error"])

    (repo / "tracked.txt").write_text("advanced\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-m", "advance")
    result, blocked = helper(
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        base,
        "--lane",
        str(lane),
    )
    assert result.returncode == 1
    assert blocked["head_matches"] is False


def test_path_presence_does_not_hide_access_failure(
    tmp_path: Path, monkeypatch,
) -> None:
    namespace = runpy.run_path(str(HELPER))
    path_type = type(Path())
    original_lstat = path_type.lstat
    blocked = tmp_path / "blocked"

    def deny_target(path):
        if Path(path) == blocked:
            raise PermissionError(13, "access denied", str(blocked))
        return original_lstat(path)

    monkeypatch.setattr(path_type, "lstat", deny_target)
    with pytest.raises(PermissionError, match="access denied"):
        namespace["path_present"](blocked)


def test_verify_cleanup_clears_actions_when_repository_head_changes(
    tmp_path: Path, monkeypatch,
) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    result, packet = prepare(repo, lane_root, base, "verify-head-drift")
    assert result.returncode == 0, packet
    worktree = Path(str(packet["worktree"]))
    namespace = runpy.run_path(str(HELPER))
    verify = namespace["verify_cleanup"]
    original_git = verify.__globals__["git"]
    repo_head_reads = 0

    def drift_after_scan(checkout, *args, check=True):
        nonlocal repo_head_reads
        if Path(checkout) == repo.resolve() and args[:2] == ("rev-parse", "HEAD"):
            repo_head_reads += 1
            if repo_head_reads > 1:
                return subprocess.CompletedProcess(args, 0, "0" * 40 + "\n", "")
        return original_git(checkout, *args, check=check)

    monkeypatch.setitem(verify.__globals__, "git", drift_after_scan)
    code, blocked = verify(
        Namespace(
            repo=str(repo),
            root=str(lane_root),
            integration_head=base,
            lane=[str(worktree)],
        )
    )
    assert code == 1
    assert blocked["head_matches"] is False
    assert blocked["cleanup"] == []
    assert blocked["retry_cleanup"] == []
    assert blocked["lanes"][0]["required_action"] == "preserve-and-report"
    assert "does not match" in blocked["lanes"][0]["reason"]


def test_verify_cleanup_rejects_dangling_lane_state_link(tmp_path: Path) -> None:
    repo, base = repository(tmp_path)
    lane_root = tmp_path / "lanes"
    state_root = lane_root / ".state"
    state_root.mkdir(parents=True)
    dangling_target = state_root / "missing-target"
    linked_state = state_root / "linked"
    if sys.platform == "win32":
        dangling_target.mkdir()
        created = run(
            "cmd", "/c", "mklink", "/J", str(linked_state), str(dangling_target)
        )
        if created.returncode != 0:
            pytest.skip(f"directory junctions unavailable: {created.stderr}")
        dangling_target.rmdir()
    else:
        linked_state.symlink_to(dangling_target, target_is_directory=True)

    result, blocked = helper(
        "verify-cleanup",
        "--repo",
        str(repo),
        "--root",
        str(lane_root),
        "--integration-head",
        base,
        "--lane",
        str(lane_root / "linked"),
    )
    assert result.returncode == 1
    assert blocked["ok"] is False
    assert runpy.run_path(str(HELPER))["path_present"](linked_state)
