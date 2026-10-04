"""Behavior of the current Astra execution and run-inventory extensions."""
from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import time
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

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


@pytest.mark.parametrize("host", ["nt", "posix"])
@pytest.mark.parametrize("env,inputs,posix_valid", [
    ({"DATA": "upper"}, {"data": "lower"}, True),
    ({"lane_runtime": "custom"}, {}, True),
    ({"DATA": "upper"}, {"DATA": "duplicate"}, False),
    ({"LANE_RUNTIME": "replacement"}, {}, False),
])
def test_profile_key_collisions_respect_host_case_rules(
    tmp_path, monkeypatch, host, env, inputs, posix_valid,
):
    profile = tmp_path / "profile.json"
    profile.write_text(json.dumps({"env": env, "inputs": inputs}), encoding="utf-8")
    ns = runpy.run_path(str(HELPER))
    parse = ns["execution_profile"]
    monkeypatch.setitem(parse.__globals__, "os", SimpleNamespace(name=host))
    args = Namespace(profile=str(profile), env=[], inputs=[], outputs=[], timeout=None)
    manifest = {key: str(tmp_path / key) for key in (
        "worktree", "runtime_root", "temp_root", "cache_root", "pytest_basetemp", "pytest_cache",
    )}
    if host == "posix" and posix_valid:
        result = parse(args, manifest)
        assert result["env"] == env and result["inputs"] == inputs
    else:
        with pytest.raises(ns["LaneError"], match="overlap or replace lane identity"):
            parse(args, manifest)


def test_exec_preserves_case_distinct_environment_on_supported_hosts(tmp_path):
    repo, root, _, packet = lane(tmp_path)
    code, result = call(
        "exec", *target(repo, root, packet),
        "--env", "DATA=upper", "--env", "data=lower", "--env", "lane_runtime=custom",
        "--", sys.executable, "-c",
        "import os; assert os.environ['DATA'] == 'upper'; "
        "assert os.environ['data'] == 'lower'; assert os.environ['lane_runtime'] == 'custom'; "
        "assert os.environ['LANE_RUNTIME'] != 'custom'; print('case preserved')",
    )
    if os.name == "nt":
        assert code == 1 and result["commands"] == []
    else:
        assert code == 0, result
        assert "case preserved" in result["commands"][0]["output_tail"]


@pytest.mark.parametrize("host", ["nt", "posix"])
@pytest.mark.parametrize("field", ["env", "inputs", "outputs"])
@pytest.mark.parametrize("override", [False, True])
def test_profile_rejects_case_collisions_before_cli_overrides(tmp_path, monkeypatch, host, field, override):
    profile = tmp_path / "profile.json"
    profile.write_text(json.dumps({field: {"DATA": "upper", "data": "lower"}}), encoding="utf-8")
    ns = runpy.run_path(str(HELPER))
    parse = ns["execution_profile"]
    monkeypatch.setitem(parse.__globals__, "os", SimpleNamespace(name=host))
    args = Namespace(profile=str(profile), env=[], inputs=[], outputs=[], timeout=None)
    if override:
        setattr(args, field, ["DATA=override"])
    manifest = {key: str(tmp_path / key) for key in (
        "worktree", "runtime_root", "temp_root", "cache_root", "pytest_basetemp", "pytest_cache",
    )}
    if host == "nt":
        with pytest.raises(ns["LaneError"], match=f"profile {field}.*distinct"):
            parse(args, manifest)
    else:
        assert parse(args, manifest)[field] == {
            "DATA": "override" if override else "upper", "data": "lower",
        }


@pytest.mark.parametrize("host", ["nt", "posix"])
@pytest.mark.parametrize("field", ["env", "inputs", "outputs"])
def test_profile_allows_cli_override_under_host_case_rules(tmp_path, monkeypatch, host, field):
    profile = tmp_path / "profile.json"
    profile.write_text(json.dumps({field: {"data": "original"}}), encoding="utf-8")
    ns = runpy.run_path(str(HELPER))
    parse = ns["execution_profile"]
    monkeypatch.setitem(parse.__globals__, "os", SimpleNamespace(name=host))
    args = Namespace(profile=str(profile), env=[], inputs=[], outputs=[], timeout=None)
    setattr(args, field, ["DATA=override" if host == "nt" else "data=override"])
    manifest = {key: str(tmp_path / key) for key in (
        "worktree", "runtime_root", "temp_root", "cache_root", "pytest_basetemp", "pytest_cache",
    )}
    assert parse(args, manifest)[field] == {"DATA" if host == "nt" else "data": "override"}


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


def test_status_preserves_cleaned_candidate_and_rechecks_current_integration(tmp_path):
    repo, root, base, packet = lane(tmp_path, named=True)
    worktree = Path(packet["worktree"])
    git(worktree, "commit", "--allow-empty", "-m", "lane work")
    lane_head = git(worktree, "rev-parse", "HEAD")
    git(repo, "merge", "--ff-only", lane_head)
    code, cleaned = call("cleanup", "--repo", str(repo), "--root", str(root),
                         "--run", "delivery", "--integration-head", lane_head)
    assert code == 0, cleaned
    git(repo, "commit", "--allow-empty", "-m", "later integration")
    status_args = ["status", "--repo", str(repo), "--root", str(root), "--run", "delivery"]
    code, result = call(*status_args)
    assert code == 0 and result["ok"], result
    completed = result["lanes"][0]
    assert completed["state"] == "cleaned"
    assert completed["lane_head"] == lane_head
    assert completed["observed_lane_head"] is None
    assert completed["integration_head"] == lane_head
    assert completed["integrated"] is True and completed["finish_clean"] is True

    git(repo, "switch", "--detach", base)
    code, result = call(*status_args)
    assert code == 0, result
    completed = result["lanes"][0]
    assert completed["lane_head"] == lane_head
    assert completed["integration_head"] == lane_head
    assert completed["integrated"] is False and completed["finish_clean"] is False


@pytest.mark.parametrize("damage,expected", [
    ("manifest-corrupt", "manifest is unreadable"),
    ("manifest-missing", "manifest is missing"),
    ("receipt-corrupt", "receipt is unreadable"),
])
def test_status_fails_for_invalid_lifecycle_metadata(tmp_path, damage, expected):
    repo, root, _, packet = lane(tmp_path, named=True)
    if damage == "manifest-missing":
        Path(packet["lane_manifest"]).unlink()
    else:
        key = "cleanup_receipt" if damage == "receipt-corrupt" else "lane_manifest"
        Path(packet[key]).write_text("invalid json", encoding="utf-8")
    code, result = call("status", "--repo", str(repo), "--root", str(root), "--run", "delivery")
    assert code == 1 and result["ok"] is False, result
    assert expected in result["lanes"][0]["error"]
    assert Path(packet["worktree"]).is_dir()


@pytest.mark.parametrize("field", [
    "path_error", "status_error", "ignored_error", "runtime", "integrated",
])
def test_status_propagates_soft_observation_errors(tmp_path, monkeypatch, field):
    repo, root, _, packet = lane(tmp_path, named=True)
    ns = runpy.run_path(str(HELPER))
    status = ns["status_run"]
    observe = status.__globals__["observe_lane"]
    def unreadable(*args, **kwargs):
        snapshot = observe(*args, **kwargs)
        if field == "runtime":
            snapshot["runtime"]["temp_root"]["error"] = "access denied to test runtime"
        elif field == "integrated":
            snapshot[field] = None
        else:
            snapshot[field] = f"access denied to test {field}"
        return snapshot
    monkeypatch.setitem(status.__globals__, "observe_lane", unreadable)
    code, result = status(Namespace(repo=str(repo), root=str(root), run="delivery"))
    assert code == 1 and result["ok"] is False, result
    expected = "integration could not be determined" if field == "integrated" else "access denied"
    assert expected in result["lanes"][0]["error"]
    assert Path(packet["worktree"]).is_dir()


@pytest.mark.parametrize("integrated", [True, False, None])
def test_status_uses_receipt_candidate_during_interrupted_cleanup(tmp_path, monkeypatch, integrated):
    repo, root, base, packet = lane(tmp_path, named=True)
    worktree = Path(packet["worktree"])
    git(worktree, "commit", "--allow-empty", "-m", "lane work")
    candidate = git(worktree, "rev-parse", "HEAD")
    git(repo, "merge", "--ff-only", candidate)
    ns = runpy.run_path(str(HELPER))
    ns["write_cleanup_receipt"](repo.resolve(), root.resolve(), worktree, candidate, candidate)
    git(repo, "worktree", "remove", packet["worktree"])
    Path(packet["lane_manifest"]).unlink()
    status = ns["status_run"]
    if integrated is False:
        git(repo, "switch", "--detach", base)
    elif integrated is None:
        original_git = status.__globals__["git"]
        def failed_merge_base(checkout, *args, **kwargs):
            if args[:2] == ("merge-base", "--is-ancestor"):
                return subprocess.CompletedProcess(args, 128, "", "cannot read candidate")
            return original_git(checkout, *args, **kwargs)
        monkeypatch.setitem(status.__globals__, "git", failed_merge_base)
    code, result = status(Namespace(repo=str(repo), root=str(root), run="delivery"))
    assert code == (1 if integrated is None else 0), result
    assert result["ok"] is (integrated is not None)
    observed = result["lanes"][0]
    assert observed["state"] == "prepared" and observed["present"] is False
    assert observed["lane_head"] == candidate and observed["observed_lane_head"] is None
    assert observed["integrated"] is integrated
    assert observed["cleanup_eligible"] is (integrated is True)
    assert observed["finish_clean"] is False
    if integrated is None:
        assert "integration could not be determined" in observed["error"]
    assert Path(packet["cleanup_receipt"]).is_file()


@pytest.mark.parametrize("readiness", [
    "missing", "failed", "corrupt", "non-object", "inaccessible", "redirected",
])
def test_status_distinguishes_unreadable_readiness_from_absent_or_failed_checks(tmp_path, monkeypatch, readiness):
    repo, root, _, packet = lane(tmp_path, named=True)
    record = Path(packet["runtime_root"], "readiness.json")
    if readiness != "missing":
        content = {"corrupt": "invalid json", "non-object": "[]"}.get(
            readiness, '{"state":"failed","ok":false}',
        )
        record.write_text(content, encoding="utf-8")
    ns = runpy.run_path(str(HELPER))
    status = ns["status_run"]
    if readiness == "inaccessible":
        original_read = Path.read_text
        def denied_read(path, *args, **kwargs):
            if path == record:
                raise PermissionError("readiness access denied")
            return original_read(path, *args, **kwargs)
        monkeypatch.setattr(Path, "read_text", denied_read)
    elif readiness == "redirected":
        original_reparse = status.__globals__["is_reparse_point"]
        monkeypatch.setitem(
            status.__globals__, "is_reparse_point", lambda path: path == record or original_reparse(path),
        )
    code, result = status(Namespace(repo=str(repo), root=str(root), run="delivery"))
    unreadable = readiness not in {"missing", "failed"}
    assert code == int(unreadable) and result["ok"] is not unreadable, result
    observed = result["lanes"][0]
    if unreadable:
        assert observed["readiness"]["state"] == "unreadable"
        assert "readiness metadata is unreadable" in observed["error"]
    elif readiness == "missing":
        assert observed["readiness"]["state"] == "not-recorded"
    else:
        assert observed["readiness"]["last_result"]["state"] == "failed"
    assert Path(packet["worktree"]).is_dir()


def test_status_accepts_observable_unfinished_work(tmp_path):
    repo, root, _, packet = lane(tmp_path, named=True)
    worktree = Path(packet["worktree"])
    git(worktree, "commit", "--allow-empty", "-m", "not yet integrated")
    (worktree / "tracked.txt").write_text("in progress", encoding="utf-8")
    Path(packet["runtime_root"], "active-command.json").write_text("{}", encoding="utf-8")
    code, result = call("status", "--repo", str(repo), "--root", str(root), "--run", "delivery")
    assert code == 0 and result["ok"], result
    observed = result["lanes"][0]
    assert observed["clean"] is False and observed["integrated"] is False
    assert observed["command_active_or_interrupted"] is True
    assert observed["cleanup_eligible"] is False and observed["finish_clean"] is False


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
