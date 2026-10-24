"""Exact source inputs, bounded comparisons, and operation-local proof observations."""
from __future__ import annotations

import importlib
import os
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest


@pytest.fixture
def helpers(tmp_path: Path, monkeypatch):
    # Set isolation before importing test/tool modules, including future path caches.
    home = tmp_path / "isolated-home"
    home.mkdir()
    for name in ("HOME", "USERPROFILE", "XDG_CONFIG_HOME"):
        monkeypatch.setenv(name, str(home))
    return importlib.import_module("test_astra_atlas_workflow")


@pytest.mark.parametrize("directory", ["src", "ordinary"])
def test_source_directory_diagnostic_names_exact_file_transport(tmp_path: Path, helpers, directory: str) -> None:
    helpers.started(tmp_path)
    (tmp_path / "ordinary").mkdir()
    with pytest.raises(helpers.atlas.ReportError, match="ordinary directory.*exact files.*--paths-file") as caught:
        helpers.atlas.source_identity(repo_root=tmp_path, paths=[directory])
    assert caught.value.stage == "source-input"


@pytest.mark.skipif(os.name != "nt", reason="Windows drive-qualified path transport")
def test_large_source_selection_rejects_an_absolute_sibling_path(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    outside = tmp_path.parent / (tmp_path.name + "-outside.txt")
    outside.write_text("benign sibling proof fixture", encoding="utf-8")
    paths = []
    for index in range(300):
        path = f"proof-{index:04d}-" + "input" * 13 + ".txt"
        (tmp_path / path).write_text("owned proof", encoding="utf-8")
        paths.append(path)
    try:
        with pytest.raises(helpers.atlas.ReportError, match="repository-relative"):
            helpers.atlas.source_identity(repo_root=tmp_path, paths=[outside.as_posix(), *paths])
    finally:
        outside.unlink()


@pytest.mark.parametrize("shape", ["packet", "response", "prepared"])
def test_public_source_comparison_accepts_saved_public_shapes(tmp_path: Path, helpers, shape: str) -> None:
    helpers.started(tmp_path)
    atlas = helpers.atlas
    expected = atlas.source_identity(repo_root=tmp_path, paths=["src/a.py"])
    if shape != "response":
        expected.pop("response_version")
    if shape == "prepared":
        expected = {"version": atlas.MANIFEST_VERSION, "source_identity": expected, "subsystem_id": "alpha"}
    original = deepcopy(expected)
    comparison = atlas.compare_source_identity(repo_root=tmp_path, expected=expected, required_paths=["src/a.py"])
    assert comparison["matches"] and comparison["freshness"] == "fresh" and comparison["categories"] == []
    assert comparison["expected_sha256"] == comparison["current_sha256"]
    assert expected == original and "fingerprints" not in comparison


def test_source_comparison_bounds_changed_unavailable_and_required_paths(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    atlas = helpers.atlas
    paths = [f"proof-{number}.txt" for number in range(6)]
    for path in paths:
        (tmp_path / path).write_text("original", encoding="utf-8")
    expected = atlas.source_identity(repo_root=tmp_path, paths=paths)
    for path in paths[:3]:
        (tmp_path / path).write_text("changed", encoding="utf-8")
    for path in paths[3:5]:
        (tmp_path / path).unlink()
    result = atlas.compare_source_identity(repo_root=tmp_path, expected=expected, limit=1,
                                           required_paths=["missing-a", "missing-b", "missing-c"])
    assert not result["matches"] and result["truncated"] and result["current_sha256"] is None
    assert result["categories"] == ["required_paths_missing", "source_unavailable", "source_identity_changed"]
    assert result["changed_path_count"] == 5 and result["unavailable_path_count"] == 2
    assert result["missing_required_path_count"] == 3
    assert result["changed_paths"] == [paths[0]] and result["unavailable_paths"] == [paths[3]]
    assert result["missing_required_paths"] == ["missing-a"]


def test_source_comparison_checks_fingerprints_even_when_aggregate_is_unchanged(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    atlas = helpers.atlas
    expected = atlas.source_identity(repo_root=tmp_path, paths=["src/a.py"])
    expected["fingerprints"]["src/a.py"] = "0" * 64
    result = atlas.compare_source_identity(repo_root=tmp_path, expected=expected)
    assert not result["matches"] and result["changed_paths"] == ["src/a.py"]
    assert result["categories"] == ["source_identity_changed"]


def test_observations_preserve_missing_untracked_index_and_mode_distinctions(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    atlas = helpers.atlas
    path = "extra.txt"
    target = tmp_path / path
    target.write_text("proof", encoding="utf-8")
    untracked = atlas.source_identity(repo_root=tmp_path, paths=[path])
    content = atlas._content_identity(tmp_path, [path])
    subprocess.run(["git", "add", "--", path], cwd=tmp_path, check=True)
    indexed = atlas.source_identity(repo_root=tmp_path, paths=[path])
    assert atlas._packet_observation(tmp_path, untracked)["changed_paths"] == [path]
    assert atlas._content_identity(tmp_path, [path]) == content
    subprocess.run(["git", "update-index", "--chmod=+x", "--", path], cwd=tmp_path, check=True)
    assert atlas._packet_observation(tmp_path, indexed)["changed_paths"] == [path]
    target.unlink()
    missing = atlas.source_identity(repo_root=tmp_path, paths=[path])
    assert atlas._packet_observation(tmp_path, missing)["freshness"] == "fresh"
    subprocess.run(["git", "rm", "--cached", "-f", "--", path], cwd=tmp_path, check=True, capture_output=True)
    observed = atlas._packet_observation(tmp_path, missing)
    assert observed["freshness"] == "changed" and observed["changed_paths"] == [path]
    assert "source path does not exist" in observed["error"]


def test_large_proof_selection_ignores_unrelated_unresolved_index_entries(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    atlas = helpers.atlas
    paths = [f"bulk-{number:03d}-{'x' * 55}.txt" for number in range(300)]
    for path in paths:
        (tmp_path / path).write_text("proof", encoding="utf-8")
    oid = subprocess.run(["git", "hash-object", "src/a.py"], cwd=tmp_path, check=True,
                         capture_output=True, text=True, encoding="utf-8").stdout.strip()
    unresolved = "".join(f"100644 {oid} {stage}\tconflict.txt\n" for stage in (1, 2, 3))
    subprocess.run(["git", "update-index", "--index-info"], cwd=tmp_path, check=True,
                   input=unresolved.encode("utf-8"), capture_output=True)
    staged = subprocess.run(["git", "ls-files", "--stage", "-z", "--", "conflict.txt"], cwd=tmp_path,
                            check=True, capture_output=True).stdout
    assert staged.count(b"\tconflict.txt\0") == 3
    assert atlas.source_identity(repo_root=tmp_path, paths=paths)["paths"] == sorted(paths)
    with pytest.raises(atlas.ReportError, match="unresolved entry: conflict.txt"):
        atlas.source_identity(repo_root=tmp_path, paths=paths + ["conflict.txt"])


def test_refresh_deduplicates_deleted_overlap_and_does_not_cache_across_operations(tmp_path: Path, helpers, monkeypatch) -> None:
    helpers.mapped(tmp_path)
    atlas = helpers.atlas
    stored = helpers.state(tmp_path)
    deleted = [f"historical-{number}.txt" for number in range(20)]
    for path in deleted:
        (tmp_path / path).write_text("old", encoding="utf-8")
    subprocess.run(["git", "add", "--", *deleted], cwd=tmp_path, check=True)
    for sub in stored["subsystems"]:
        packet = atlas.source_identity(repo_root=tmp_path, paths=deleted + sub["owned_paths"])
        sub["map_source"] = {key: packet[key] for key in ("paths", "sha256", "fingerprints")}
    subprocess.run(["git", "rm", "--cached", "--", *deleted], cwd=tmp_path, check=True, capture_output=True)
    for path in deleted:
        (tmp_path / path).unlink()
    calls = []
    original = atlas._git
    def counted(root, *args):
        calls.append(args)
        return original(root, *args)
    monkeypatch.setattr(atlas, "_git", counted)
    atlas._refresh_observation(stored, tmp_path)
    assert len(calls) == 3  # Two disjoint pending-path index reads and one map inventory.
    assert all(row["changed_paths"] == sorted(deleted) for row in stored["source_changes"].values())
    (tmp_path / "src/a.py").write_text("changed after first refresh", encoding="utf-8")
    atlas._refresh_observation(stored, tmp_path)
    assert len(calls) == 6
    assert "src/a.py" in stored["source_changes"]["alpha"]["changed_paths"]


def test_reuse_diagnostic_preserves_full_environment_equality_without_values(tmp_path: Path, helpers, monkeypatch) -> None:
    helpers.started(tmp_path)
    original = helpers.check(tmp_path)
    before = helpers.report(tmp_path).read_bytes()
    monkeypatch.setenv("ATLAS_TEST_SECRET_VALUE", "do-not-display-this-sensitive-value")
    with pytest.raises(helpers.atlas.ReportError, match="process environment changed.*run the check") as caught:
        helpers.check(tmp_path, "carry", reuse="probe")
    assert caught.value.stage == "verification-reuse"
    assert "do-not-display" not in str(caught.value) and "ATLAS_TEST_SECRET_VALUE" not in str(caught.value)
    assert helpers.report(tmp_path).read_bytes() == before
    assert not helpers.report(tmp_path).with_name("check-carry.log").exists()
    assert original["passed"]


def test_reuse_diagnostic_identifies_proof_paths_without_running_command(tmp_path: Path, helpers) -> None:
    helpers.started(tmp_path)
    proof = tmp_path / "proof.txt"
    proof.write_text("before", encoding="utf-8")
    helpers.check(tmp_path, paths=[proof.name])
    proof.write_text("after", encoding="utf-8")
    before = helpers.report(tmp_path).read_bytes()
    with pytest.raises(helpers.atlas.ReportError, match="proof content changed: proof.txt"):
        helpers.check(tmp_path, "carry", reuse="probe", paths=[proof.name])
    assert helpers.report(tmp_path).read_bytes() == before
    assert not helpers.report(tmp_path).with_name("check-carry.log").exists()
