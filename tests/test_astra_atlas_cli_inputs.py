"""Public CLI input transport and composed operations preserve proof contracts."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from test_astra_atlas import SCRIPT, atlas, make_repo, report, write_json
from test_astra_atlas_maintenance import started


def run_cli(root: Path, command: str, *args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), command, "--repo-root", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert not completed.stderr, completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def test_file_paths_merge_with_explicit_paths_and_compare_saved_identity(tmp_path: Path) -> None:
    make_repo(tmp_path)
    path_list = tmp_path / "paths.json"
    path_list.write_text(json.dumps(["src/b.py", "src/a.py", "src/b.py"]), encoding="utf-8-sig")
    code, captured = run_cli(tmp_path, "source-identity", "--paths-file", path_list.name,
                             "--path", "tests/test_a.py")
    assert code == 0
    expected = atlas.source_identity(repo_root=tmp_path, paths=["src/a.py", "src/b.py", "tests/test_a.py"])
    assert captured == expected
    saved = write_json(tmp_path / "saved.json", captured)
    code, same = run_cli(tmp_path, "source-identity", "--compare", saved.name)
    assert code == 0 and same["matches"]
    (tmp_path / "src/a.py").write_text("VALUE=123\n", encoding="utf-8")
    code, changed = run_cli(tmp_path, "source-identity", "--compare", saved.name, "--limit", "1")
    assert code == 0 and not changed["matches"]
    assert changed["changed_paths"] == ["src/a.py"]


@pytest.mark.parametrize("contents", ['{"paths": ["src/a.py"]}', '["../outside"]',
                                      '["C:/outside.txt"]', '["C:outside.txt"]', '[2]', 'not-json'])
def test_invalid_file_path_list_fails_without_mutating_report(tmp_path: Path, contents: str) -> None:
    started(tmp_path)
    before = report(tmp_path).read_bytes()
    path_list = tmp_path / "invalid.json"
    path_list.write_text(contents, encoding="utf-8")
    code, rejected = run_cli(tmp_path, "prepare-outcomes", "--report", str(report(tmp_path)),
                             "--target", "candidate:alpha-fix", "--type", "verified",
                             "--paths-file", path_list.name)
    assert code == 2 and rejected["ok"] is False
    assert "invalid.json" in rejected["error"]
    assert report(tmp_path).read_bytes() == before


def test_bulk_proof_paths_use_file_transport_for_verification_and_preparation(tmp_path: Path) -> None:
    started(tmp_path)
    (tmp_path / "proof").mkdir()
    paths = []
    for index in range(420):
        path = "proof/" + f"{index:04d}-" + "input" * 13 + ".txt"
        (tmp_path / path).write_text(str(index), encoding="utf-8")
        paths.append(path)
    assert sum(len(path) + len(" --path ") for path in paths) > 32767
    path_list = write_json(tmp_path / "proof-paths.json", paths)
    code, checked = run_cli(tmp_path, "verify", "--report", str(report(tmp_path)),
                            "--id", "bulk-check", "--target", "candidate:alpha-fix",
                            "--environment", "isolated-test", "--paths-file", path_list.name,
                            "--", sys.executable, "-c", "print('bulk proof command passed')")
    assert code == 0 and checked["passed"], checked
    assert checked["check"]["source_paths_total"] >= len(paths)
    code, prepared = run_cli(tmp_path, "prepare-outcomes", "--report", str(report(tmp_path)),
                             "--target", "candidate:alpha-fix", "--type", "implemented", "--type", "verified",
                             "--paths-file", path_list.name, "--check", "bulk-check")
    assert code == 0 and prepared["prepared"]
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    assert [event["type"] for event in packet["events"]] == ["implemented", "verified"]
    for event in packet["events"]:
        assert set(paths) <= set(event["source_identity"]["paths"])


def test_direct_pending_preview_is_unverified_and_rejects_mixed_input_modes(tmp_path: Path) -> None:
    started(tmp_path)
    arguments = ("--report", str(report(tmp_path)), "--environment", "queued-test-host",
                 "--capability", "html-preview", "--pending", "--reason", "Opening was queued",
                 "--evidence", "The host accepted the open operation without a rendered observation.")
    code, result = run_cli(tmp_path, "record-preview", *arguments)
    assert code == 0 and result["published"]
    state = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=True)["state"]
    preview = state["preview"][-1]
    assert preview["state"] == "pending" and "report_sha256" not in preview
    code, rejected = run_cli(tmp_path, "record-preview", *arguments, "--manifest", "unused.json")
    assert code == 2 and "cannot be combined" in rejected["error"]
