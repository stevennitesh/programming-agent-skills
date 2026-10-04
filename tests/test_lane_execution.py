"""Behavior of the current Astra execution and run-inventory extensions."""
from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import time
from pathlib import Path

import pytest

from test_lane_worktree import git, repository, run


HELPER = Path(__file__).resolve().parents[1] / "skills/astra/parallel-implement/scripts/lane_worktree.py"
LEGACY = HELPER.parents[3] / "custom/parallel-implement/scripts/lane_worktree.py"


def call(*args: str):
    result = run(sys.executable, str(HELPER), *args)
    return result.returncode, json.loads(result.stdout)


def lane(tmp_path: Path, *, named: bool = False, legacy: bool = False):
    repo, base = repository(tmp_path)
    root = tmp_path / "lanes"
    args = ["prepare", "--repo", str(repo), "--root", str(root), "--base", base, "--name", "one"]
    if named:
        args.extend(["--run", "delivery"])
    result = run(sys.executable, str(LEGACY if legacy else HELPER), *args)
    packet = json.loads(result.stdout)
    assert result.returncode == 0, packet
    return repo, root, base, packet


def target(repo, root, packet):
    return ["--repo", str(repo), "--root", str(root), "--lane", packet["worktree"]]


def test_existing_lane_remains_inspectable_executable_and_cleanable(tmp_path):
    repo, root, base, packet = lane(tmp_path, legacy=True)
    code, inspected = call("inspect", *target(repo, root, packet))
    assert code == 0 and inspected["readiness"]["state"] == "not-recorded"
    code, executed = call("exec", *target(repo, root, packet), "--", sys.executable, "-c", "print('old lane')")
    assert code == 0 and "old lane" in executed["commands"][0]["output_tail"]
    Path(packet["runtime_root"], "readiness.json").write_text("invalid old metadata")
    code, cleaned = call("cleanup", "--repo", str(repo), "--root", str(root),
                         "--completed", packet["worktree"], "--integration-head", base)
    assert code == 0, cleaned
    assert not Path(packet["worktree"]).exists()


def test_readiness_uses_shared_inputs_local_outputs_and_real_imports(tmp_path):
    repo, root, base, packet = lane(tmp_path)
    data = tmp_path / "durable.txt"
    data.write_text("retained")
    profile = tmp_path / "profile.json"
    profile.write_text(json.dumps({
        "inputs": {"DATA": str(data)}, "outputs": {"RESULTS": "results"},
        "env": {"EXPECTED": "local"},
        "setup": [[sys.executable, "-c", "import os,pathlib; pathlib.Path(os.environ['RESULTS'],'setup.txt').write_text('done')"]],
        "checks": [[sys.executable, "-c", "import os,pathlib,test_smoke; "
                    "assert pathlib.Path(test_smoke.__file__).parent == pathlib.Path(os.environ['LANE_WORKTREE']); "
                    "assert pathlib.Path(os.environ['DATA']).read_text() == 'retained'; "
                    "assert pathlib.Path(os.environ['RESULTS'],'setup.txt').read_text() == 'done'; "
                    "assert os.environ['EXPECTED'] == 'local'; print('ready')"]],
    }))
    code, ready = call("ready", *target(repo, root, packet), "--profile", str(profile))
    assert code == 0, ready
    assert len(ready["commands"]) == 2
    assert ready["inputs"]["DATA"] == str(data.resolve())
    code, executed = call("exec", *target(repo, root, packet), "--profile", str(profile),
                          "--", sys.executable, "-c", "import os; print(os.environ['RESULTS'])")
    assert code == 0, executed
    assert ready["outputs"]["RESULTS"] in executed["commands"][0]["output_tail"]
    assert git(Path(packet["worktree"]), "status", "--porcelain") == ""
    code, cleaned = call("cleanup", "--repo", str(repo), "--root", str(root),
                         "--completed", packet["worktree"], "--integration-head", base)
    assert code == 0, cleaned
    assert data.read_text() == "retained"


def test_failed_readiness_replaces_previous_pass_and_stops_sequence(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    code, result = call("ready", *target(repo, root, packet), "--check", json.dumps([sys.executable, "-c", "pass"]))
    assert code == 0, result
    code, result = call("ready", *target(repo, root, packet),
                        "--setup", json.dumps([sys.executable, "-c", "raise SystemExit(7)"]),
                        "--check", json.dumps([sys.executable, "-c", "raise AssertionError('must not run')"]))
    assert code == 1 and len(result["commands"]) == 1
    assert result["commands"][0]["returncode"] == 7
    record = json.loads(Path(packet["runtime_root"], "readiness.json").read_text())
    assert record["state"] == "failed"
    code, result = call("ready", *target(repo, root, packet), "--timeout", "nan")
    assert code == 1 and "finite positive" in result["error"]
    assert json.loads(Path(packet["runtime_root"], "readiness.json").read_text())["ok"] is False


def test_checks_only_reuses_setup_and_cli_expands_runtime_tokens(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    code, result = call("ready", *target(repo, root, packet), "--checks-only",
                        "--setup", json.dumps([sys.executable, "-c", "raise SystemExit(9)"]),
                        "--check", json.dumps([sys.executable, "-c", "pass"]))
    assert code == 0 and len(result["commands"]) == 1
    code, result = call("exec", *target(repo, root, packet), "--", sys.executable, "-c",
                        "import sys; print(sys.argv[1])", "@runtime_root@")
    assert code == 0, result
    assert packet["runtime_root"] in result["commands"][0]["output_tail"]


def test_missing_data_prevents_setup_and_empty_checks_do_not_claim_readiness(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    code, result = call("ready", *target(repo, root, packet), "--input", f"DATA={tmp_path / 'absent'}",
                        "--setup", json.dumps([sys.executable, "-c", "raise AssertionError('must not run')"]),
                        "--check", json.dumps([sys.executable, "-c", "pass"]))
    assert code == 1 and result["commands"] == []
    code, result = call("ready", *target(repo, root, packet))
    assert code == 1 and "health check" in result["error"]


def test_helper_metadata_cannot_be_an_output_directory(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    code, result = call("exec", *target(repo, root, packet), "--output", "RESULTS=readiness.json",
                        "--", sys.executable, "-c", "pass")
    assert code == 1 and "metadata" in result["error"]


def test_environment_names_follow_host_case_rules(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    data = tmp_path / "input.txt"
    data.write_text("data")
    key = "dataFile"
    code, result = call("exec", *target(repo, root, packet), "--input", f"{key}={data}",
                        "--", sys.executable, "-c", f"import os; print(os.environ[{key!r}])")
    assert code == 0, result
    expected_key = key.upper() if os.name == "nt" else key
    assert result["inputs"][expected_key] == str(data.resolve())


@pytest.mark.parametrize("argument", ["--input", "--output"])
def test_data_and_output_paths_cannot_escape_ownership(tmp_path, argument):
    repo, root, _, packet = lane(tmp_path)
    path = packet["runtime_root"] if argument == "--input" else str(tmp_path / "permanent")
    code, result = call("ready", *target(repo, root, packet), argument, f"DATA={path}",
                        "--check", json.dumps([sys.executable, "-c", "pass"]))
    assert code == 1 and result["commands"] == []
    assert not (tmp_path / "permanent").exists()


def test_exec_allows_dirty_work_and_bounds_output(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    Path(packet["worktree"], "tracked.txt").write_text("work in progress")
    code, result = call("exec", *target(repo, root, packet), "--", sys.executable, "-c",
                        "import os,pathlib; assert pathlib.Path.cwd() == pathlib.Path(os.environ['LANE_WORKTREE']); "
                        "assert os.environ['TEMP'].startswith(os.environ['LANE_RUNTIME']); print('x' * 100000)")
    assert code == 0, result
    evidence = result["commands"][0]
    assert evidence["output_truncated"] and len(evidence["output_tail"]) <= 16384
    assert Path(packet["worktree"], "tracked.txt").read_text() == "work in progress"


def test_timeout_stops_launched_process_tree(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    sentinel = Path(packet["runtime_root"]) / "late.txt"
    child = f"import time,pathlib; time.sleep(2); pathlib.Path({str(sentinel)!r}).write_text('late')"
    parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(30)"
    code, result = call("exec", *target(repo, root, packet), "--timeout", "0.5",
                        "--", sys.executable, "-c", parent)
    assert code == 1, result
    assert result["commands"][0]["timed_out"]
    assert not Path(packet["runtime_root"], "active-command.json").exists()
    time.sleep(2.1)
    assert not sentinel.exists()


def test_interrupted_command_blocks_execution_and_cleanup(tmp_path):
    repo, root, base, packet = lane(tmp_path)
    marker = Path(packet["runtime_root"], "active-command.json")
    marker.write_text('{"state":"running","pid":123}')
    code, inspected = call("inspect", *target(repo, root, packet))
    assert code == 0
    assert not inspected["mechanical"]["cleanup_eligible"]
    assert not inspected["mechanical"]["resume_or_land_eligible"]
    code, _ = call("exec", *target(repo, root, packet), "--", sys.executable, "-c", "pass")
    assert code == 1
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--completed", packet["worktree"], "--integration-head", base)
    assert code == 1 and marker.exists()


def test_invalid_receipt_never_advertises_cleanup_eligibility(tmp_path):
    repo, root, base, packet = lane(tmp_path)
    Path(packet["cleanup_receipt"]).write_text('{"format":1}')
    code, inspected = call("inspect", *target(repo, root, packet))
    assert code == 0
    assert inspected["cleanup_receipt"]["state"] == "invalid"
    assert not inspected["mechanical"]["cleanup_eligible"]
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--completed", packet["worktree"], "--integration-head", base)
    assert code == 1 and "invalid" in result["preserved"][0]["reason"]


def test_cleanup_requires_proved_head_before_deleting_runtime(tmp_path):
    repo, root, base, packet = lane(tmp_path)
    sentinel = Path(packet["temp_root"], "keep.txt")
    sentinel.write_text("retain")
    git(repo, "commit", "--allow-empty", "-m", "advance")
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--completed", packet["worktree"], "--integration-head", base)
    assert code == 1 and "proved" in result["error"]
    assert sentinel.read_text() == "retain"
    missing = run(sys.executable, str(HELPER), "cleanup", "--repo", str(repo),
                  "--root", str(root), "--completed", packet["worktree"])
    assert missing.returncode != 0
    assert sentinel.exists()


def test_named_inventory_keeps_all_lanes_and_cleanup_is_repeatable(tmp_path):
    repo, root, base, packet = lane(tmp_path, named=True)
    code, second = call("prepare", "--repo", str(repo), "--root", str(root),
                        "--base", base, "--name", "two", "--run", "delivery")
    assert code == 0, second
    code, status = call("status", "--repo", str(repo), "--root", str(root), "--run", "delivery")
    assert code == 0 and len(status["lanes"]) == 2
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--run", "delivery", "--completed", packet["worktree"], "--integration-head", base)
    assert code == 0, result
    code, result = call("verify-cleanup", "--repo", str(repo), "--root", str(root),
                        "--run", "delivery", "--integration-head", base)
    assert code == 1 and len(result["lanes"]) == 2
    code, result = call("verify-cleanup", "--repo", str(repo), "--root", str(root),
                        "--run", "delivery", "--lane", packet["worktree"], "--integration-head", base)
    assert code == 1 and "entire inventory" in result["error"]
    for _ in range(2):
        code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                            "--run", "delivery", "--integration-head", base)
        assert code == 0, result
    code, result = call("verify-cleanup", "--repo", str(repo), "--root", str(root),
                        "--run", "delivery", "--integration-head", base)
    assert code == 0 and result["finish_clean"]
    Path(packet["worktree"]).mkdir()
    Path(packet["worktree"], "new.txt").write_text("keep")
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--run", "delivery", "--integration-head", base)
    assert code == 1 and Path(packet["worktree"], "new.txt").exists()


def test_run_cannot_adopt_another_runs_lane(tmp_path):
    repo, root, base, packet = lane(tmp_path, named=True)
    code, result = call("prepare", "--repo", str(repo), "--root", str(root),
                        "--base", base, "--name", "one", "--run", "other")
    assert code == 1 and "different run" in result["error"]
    code, result = call("cleanup", "--repo", str(repo), "--root", str(root),
                        "--completed", packet["worktree"], "--integration-head", base)
    assert code == 1 and "ownership" in result["preserved"][0]["reason"]


def test_worktree_inventory_parses_null_delimited_paths(monkeypatch):
    ns = runpy.run_path(str(HELPER))
    listing = ns["registered_worktrees"]
    paths = [Path("odd\nname").resolve(), Path("space and é").resolve()]
    def response(repo, *args):
        assert args == ("worktree", "list", "--porcelain", "-z")
        return subprocess.CompletedProcess(args, 0, "".join(f"worktree {path}\0HEAD abc\0\0" for path in paths), "")
    monkeypatch.setitem(listing.__globals__, "git", response)
    assert listing(Path.cwd()) == set(paths)


def test_failed_prepare_inventory_is_visible_and_cannot_claim_foreign_lane(tmp_path, monkeypatch):
    repo, base = repository(tmp_path)
    root = tmp_path / "lanes"
    ns = runpy.run_path(str(HELPER))
    prepare = ns["prepare"]
    original_git = prepare.__globals__["git"]
    def fail_creation(checkout, *args, **kwargs):
        if args[:2] == ("worktree", "add"):
            return subprocess.CompletedProcess(args, 1, "", "blocked")
        return original_git(checkout, *args, **kwargs)
    monkeypatch.setitem(prepare.__globals__, "git", fail_creation)
    from argparse import Namespace
    with pytest.raises(ns["LaneError"]):
        prepare(Namespace(repo=str(repo), root=str(root), base=base, name="one", run="failed"))
    code, status = call("status", "--repo", str(repo), "--root", str(root), "--run", "failed")
    assert code == 0 and status["lanes"][0]["state"] == "preparing"
    assert not status["lanes"][0]["finish_clean"]
    code, created = call("prepare", "--repo", str(repo), "--root", str(root),
                         "--base", base, "--name", "one", "--run", "new")
    assert code == 0, created
    code, status = call("status", "--repo", str(repo), "--root", str(root), "--run", "failed")
    assert code == 1 and "ownership" in status["lanes"][0]["error"]
    code, verified = call("verify-cleanup", "--repo", str(repo), "--root", str(root),
                          "--run", "failed", "--integration-head", base)
    assert code == 1 and verified["cleanup"] == []
    assert Path(created["worktree"]).is_dir()


def test_residual_cleanup_rechecks_head_before_runtime_deletion(tmp_path, monkeypatch):
    repo, root, base, packet = lane(tmp_path)
    ns = runpy.run_path(str(HELPER))
    worktree = Path(packet["worktree"])
    ns["write_cleanup_receipt"](repo.resolve(), root.resolve(), worktree, base, base)
    git(repo, "worktree", "remove", str(worktree))
    sentinel = Path(packet["temp_root"], "retained.txt")
    sentinel.write_text("retain")
    recover = ns["recover_unregistered_lane"]
    original_observe = recover.__globals__["observe_lane"]
    original_git = recover.__globals__["git"]
    changed = False
    def observe(*args, **kwargs):
        nonlocal changed
        result = original_observe(*args, **kwargs)
        changed = True
        return result
    def drifting_git(checkout, *args, **kwargs):
        if changed and Path(checkout) == repo.resolve() and args[:2] == ("rev-parse", "HEAD"):
            return subprocess.CompletedProcess(args, 0, "0" * 40, "")
        return original_git(checkout, *args, **kwargs)
    monkeypatch.setitem(recover.__globals__, "observe_lane", observe)
    monkeypatch.setitem(recover.__globals__, "git", drifting_git)
    cleaned, reason = recover(repo.resolve(), root.resolve(), worktree, base)
    assert not cleaned and "HEAD changed" in reason
    assert sentinel.read_text() == "retain"
