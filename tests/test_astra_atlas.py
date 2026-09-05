"""Behavioral checks for the standalone Astra report workflow."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "skills/astra/audit-codebase/scripts/atlas.py"
SPEC = importlib.util.spec_from_file_location("astra_atlas", SCRIPT)
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    for name in ["src/a.py", "src/b.py", "README.md"]:
        path = tmp_path / name
        path.parent.mkdir(exist_ok=True)
        path.write_text("original\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    report = tmp_path / ".tmp/audit-codebase/test/report.html"
    state = {"version": 1, "repo": str(tmp_path.resolve()), "title": "Test atlas", "records": {}, "history": []}
    atlas.publish(tmp_path, report, state, "absent")
    return tmp_path, report


def subsystem(repo, paths=("src/a.py",), name="Orders"):
    root, report = repo
    draft = atlas.prepare(root, report, "subsystem", paths=paths)
    draft["content"].update(name=name, system="Application", purpose="Accept orders", ownership="Order state")
    atlas.apply(root, report, draft)
    return draft["record_id"]


def finding(repo, owner):
    root, report = repo
    draft = atlas.prepare(root, report, "finding", subsystem=owner)
    draft["content"].update(title="Duplicated policy", scenario="Submit order", evidence="src/a.py caller",
                            consequence="Two owners must change", direction="Concentrate the policy",
                            preserve_and_verify="Both callers retain rejection behavior",
                            priority="high", priority_rationale="Repeated changes", confidence_and_limits="Source confirmed")
    return draft


def test_incremental_records_scoped_read_and_history(repo):
    root, report = repo
    first = subsystem(repo)
    second = subsystem(repo, ("src/b.py",), "Shipping")
    draft = finding(repo, first)
    atlas.apply(root, report, draft)
    before, _ = atlas.load(root, report)
    update = atlas.prepare(root, report, "finding", ident=draft["record_id"])
    update["content"]["status"] = "disproved"
    update["content"]["evidence"] = "Caller owns an independent policy"
    atlas.apply(root, report, update)
    after, _ = atlas.load(root, report)
    assert after["records"][second] == before["records"][second]
    assert after["history"][-1]["previous"]["content"]["status"] == "open"
    scoped = atlas.inspect(root, report, first)
    assert set(scoped["records"]) == {first, draft["record_id"]}
    assert atlas.inspect(root, report)["inventory"]["unmapped"] == 1


@pytest.mark.parametrize("drift", ["source", "report", "new_selected_file"])
def test_prepared_update_rejects_drift_without_overwrite(repo, drift):
    root, report = repo
    owner = subsystem(repo, ("src",))
    draft = finding(repo, owner)
    if drift == "source":
        (root / "src/a.py").write_text("changed\n")
    elif drift == "new_selected_file":
        (root / "src/c.py").write_text("new\n")
        subprocess.run(["git", "-C", str(root), "add", "src/c.py"], check=True)
    else:
        other = atlas.prepare(root, report, "subsystem", ident=owner)
        other["content"]["purpose"] = "Revised purpose"
        atlas.apply(root, report, other)
    previous = report.read_bytes()
    with pytest.raises(atlas.AtlasError, match="changed"):
        atlas.apply(root, report, draft)
    assert report.read_bytes() == previous


def test_unrelated_source_change_does_not_block_selected_evidence(repo):
    root, report = repo
    owner = subsystem(repo)
    draft = finding(repo, owner)
    (root / "src/b.py").write_text("changed\n")
    atlas.apply(root, report, draft)
    assert atlas.inspect(root, report, draft["record_id"])["freshness"][draft["record_id"]]["state"] == "unchanged"


def test_refresh_flags_changes_without_revalidating_or_erasing_findings(repo):
    root, report = repo
    owner = subsystem(repo)
    draft = finding(repo, owner)
    atlas.apply(root, report, draft)
    state, revision = atlas.load(root, report)
    original = state["records"]
    (root / "src/a.py").unlink()
    atlas.publish(root, report, state, revision)
    updated, _ = atlas.load(root, report)
    assert updated["records"] == original
    assert updated["freshness"][draft["record_id"]]["state"] == "changed"


def test_overlap_rejected_and_lock_released(repo):
    root, report = repo
    subsystem(repo)
    previous = report.read_bytes()
    with pytest.raises(atlas.AtlasError, match="overlapping"):
        subsystem(repo, ("src",), "Wrong owner")
    assert report.read_bytes() == previous
    assert not report.with_suffix(".lock").exists()


def test_explicit_removal_requires_no_dependents(repo):
    root, report = repo
    owner = subsystem(repo)
    draft = finding(repo, owner)
    atlas.apply(root, report, draft)
    removal = atlas.prepare(root, report, "subsystem", ident=owner)
    removal["remove"] = True
    with pytest.raises(atlas.AtlasError, match="dependent"):
        atlas.apply(root, report, removal)
    remove_finding = atlas.prepare(root, report, "finding", ident=draft["record_id"])
    remove_finding["remove"] = True
    atlas.apply(root, report, remove_finding)
    assert owner in atlas.load(root, report)[0]["records"]


def test_escaped_html_and_tamper_detection(repo):
    root, report = repo
    value = '</script><img src=x onerror="alert(1)">'
    owner = subsystem(repo, name=value)
    raw = report.read_text(encoding="utf-8")
    assert value not in raw
    assert "&lt;img" in raw
    assert atlas.load(root, report)[0]["records"][owner]["content"]["name"] == value
    report.write_bytes(report.read_bytes().replace(b"Order state", b"Other state", 1))
    with pytest.raises(atlas.AtlasError):
        atlas.load(root, report)


def test_writer_conflict_and_path_escape_preserve_report(repo):
    root, report = repo
    before = report.read_bytes()
    report.with_suffix(".lock").write_text("active")
    with pytest.raises(atlas.AtlasError, match="writer"):
        subsystem(repo)
    assert report.read_bytes() == before
    with pytest.raises(atlas.AtlasError, match="traversal"):
        atlas.snapshot(root, ["../outside"])
    with pytest.raises(atlas.AtlasError, match="report must"):
        atlas.report_path(root, root / "elsewhere.html")


def test_cli_prepare_apply_actual_html_roundtrip(repo):
    root, report = repo
    draft_path = report.parent / "draft.json"
    base = [sys.executable, str(SCRIPT), "--repo", str(root), "--report", str(report)]
    prepared = subprocess.run(base + ["prepare", "--kind", "subsystem", "--path", "src", "--out", str(draft_path)],
                              check=True, capture_output=True, text=True)
    ident = json.loads(prepared.stdout)["record_id"]
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    draft["content"].update(name="CLI system", system="Product", purpose="Roundtrip", ownership="Source")
    draft_path.write_text(json.dumps(draft), encoding="utf-8")
    subprocess.run(base + ["apply", "--draft", str(draft_path)], check=True, capture_output=True)
    result = subprocess.run(base + ["inspect", "--id", ident], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout)["records"][ident]["content"]["name"] == "CLI system"
    assert b'CLI system' in report.read_bytes()
    again = subprocess.run(base + ["prepare", "--kind", "subsystem", "--path", "src", "--out", str(draft_path)],
                           capture_output=True, text=True)
    assert again.returncode == 2


def test_deleted_source_can_be_removed_and_ids_are_not_recycled(repo):
    root, report = repo
    first = subsystem(repo)
    subprocess.run(["git", "-C", str(root), "rm", "-f", "src/a.py"], check=True, capture_output=True)
    removal = atlas.prepare(root, report, "subsystem", ident=first)
    removal["remove"] = True
    atlas.apply(root, report, removal)
    second = subsystem(repo, ("src/b.py",))
    assert second != first
    state, _ = atlas.load(root, report)
    assert state["history"][-2]["previous"]["content"]["name"] == "Orders"


def test_reassign_record_preserves_id_and_new_owner(repo):
    root, report = repo
    first = subsystem(repo)
    second = subsystem(repo, ("src/b.py",))
    draft = finding(repo, first)
    atlas.apply(root, report, draft)
    moved = atlas.prepare(root, report, "finding", ident=draft["record_id"], subsystem=second, paths=["src/b.py"])
    atlas.apply(root, report, moved)
    record = atlas.inspect(root, report, draft["record_id"])["records"][draft["record_id"]]
    assert record["subsystem"] == second
    assert set(record["source"]) == {"src/b.py"}


def test_source_change_during_publication_does_not_replace_report(repo, monkeypatch):
    root, report = repo
    owner = subsystem(repo)
    draft = finding(repo, owner)
    before = report.read_bytes()
    original = atlas.observations

    def mutate_after_observation(root, state):
        original(root, state)
        (root / "src/a.py").write_text("concurrent change\n")

    monkeypatch.setattr(atlas, "observations", mutate_after_observation)
    with pytest.raises(atlas.AtlasError, match="source changed during"):
        atlas.apply(root, report, draft)
    assert report.read_bytes() == before


def test_assessment_is_explicit_and_defect_needs_expectation(repo):
    root, report = repo
    owner = subsystem(repo)
    assert b"mapped; not audited" in report.read_bytes()
    draft = atlas.prepare(root, report, "assessment", subsystem=owner)
    draft["content"].update(examined="Order intake", dimensions=["ownership"], limits="No deployment audit")
    atlas.apply(root, report, draft)
    assert b"mapped; not audited" not in report.read_bytes()
    defect = finding(repo, owner)
    defect["content"]["kind"] = "defect"
    with pytest.raises(atlas.AtlasError, match="accepted expectation"):
        atlas.apply(root, report, defect)


def test_comprehensive_coverage_requires_accounting_and_displays_gaps(repo):
    root, report = repo
    owner = subsystem(repo)
    draft = atlas.prepare(root, report, "assessment", subsystem=owner, coverage="comprehensive")
    draft["content"].update(examined="Order intake and rejection", limits="No production workload")
    assert set(draft["content"]["lens_coverage"]) == set(atlas.LENSES)
    before = report.read_bytes()
    with pytest.raises(atlas.AtlasError, match="pending lens"):
        atlas.apply(root, report, draft)
    assert report.read_bytes() == before
    for row in draft["content"]["lens_coverage"].values():
        row.update(status="examined", details="Order caller and rejection contract in src/a.py")
    draft["content"]["lens_coverage"]["performance"] = {"status": "gap", "details": "Production workload unavailable; runtime cost unproved"}
    draft["content"]["lens_coverage"]["domain"] = {"status": "excluded", "details": ""}
    with pytest.raises(atlas.AtlasError, match="exclusion reason"):
        atlas.apply(root, report, draft)
    draft["content"]["lens_coverage"]["domain"]["details"] = "No separate domain model in this fixture"
    atlas.apply(root, report, draft)
    assert b"comprehensive with evidence gaps" in report.read_bytes()
    restored, _ = atlas.load(root, report)
    assert restored["records"][draft["record_id"]]["content"]["lens_coverage"]["performance"]["status"] == "gap"


def test_comprehensive_cannot_skip_ledger_but_incomplete_can_save_pending(repo):
    root, report = repo
    owner = subsystem(repo)
    draft = atlas.prepare(root, report, "assessment", subsystem=owner)
    draft["content"].update(coverage="comprehensive", examined="Order caller", limits="Pending investigation")
    with pytest.raises(atlas.AtlasError, match="six-lens ledger"):
        atlas.apply(root, report, draft)
    full = atlas.prepare(root, report, "assessment", subsystem=owner, coverage="comprehensive")
    full["content"].update(coverage="incomplete", examined="Order caller", limits="Five lenses remain")
    atlas.apply(root, report, full)
    scoped = atlas.inspect(root, report, full["record_id"])
    assert scoped["records"][full["record_id"]]["content"]["coverage"] == "incomplete"
