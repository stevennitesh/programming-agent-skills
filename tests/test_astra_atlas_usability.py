"""Agent-facing packet and presentation operations preserve audit evidence."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from test_astra_atlas import (
    SCRIPT, analysis_manifest, atlas, candidate, elements, finding, make_repo,
    map_manifest, publish, report, sha, write_json,
)
from test_astra_atlas_maintenance import event, outcomes, reconcile, started, state


def cli(root: Path, command: str, *args: str) -> tuple[int, dict]:
    result = subprocess.run([sys.executable, str(SCRIPT), command, "--repo-root", str(root),
                             "--report", str(report(root)), *args], capture_output=True, text=True)
    assert not result.stderr, result.stderr
    return result.returncode, json.loads(result.stdout)


def mapped(root: Path) -> None:
    make_repo(root)
    manifest = map_manifest(root)
    for sub in manifest["subsystems"]:
        for key in ("ownership", "authority", "callers", "dependencies", "interfaces", "proof_seams"):
            sub.pop(key)
    for key in ("coverage", "evidence_limits", "excluded"):
        manifest.pop(key)
    publish(root, "render-report", manifest)


def filled_packet(root: Path) -> Path:
    result = atlas.prepare_audit(repo_root=root, report=report(root), subsystem="alpha", affected_subsystems=["beta"])
    path = Path(result["packet"])
    packet = json.loads(path.read_text(encoding="utf-8"))
    packet["source_trace"]["summary"] = "Traced both validation entries and the shared write."
    fact = finding()
    for key in ("causal_owner", "direction", "proof", "confidence", "severity"):
        fact.pop(key)
    proposed = candidate()
    for key in ("affected_scope", "problem", "evidence", "benefit", "risks", "required_proof"):
        proposed.pop(key)
    packet.update(findings=[fact], candidates=[proposed],
                  lenses=[{"class": "reliability", "state": "complete", "finding_ids": [fact["id"]]}])
    return write_json(path, packet)


def test_prepared_packet_is_editable_and_publishes_without_repeated_evidence(tmp_path: Path) -> None:
    mapped(tmp_path)
    packet = filled_packet(tmp_path)
    result = atlas.mutate_report(objective="audit-subsystem", repo_root=tmp_path, report=report(tmp_path), manifest=packet)
    assert result["published"]
    saved = state(tmp_path)["subsystems"][0]["audit"]
    assert saved["candidates"][0]["affected_scope"] == ["alpha", "beta"]
    assert not saved["candidates"][0]["evidence"]
    observed = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))
    assert observed["summary"]["coverage"]["design"]["not inspected"] == 1
    assert observed["summary"]["coverage"]["design"]["not audited"] == 1
    assert observed["summary"]["coverage"]["reliability"]["complete"] == 1
    assert observed["summary"]["finding_counts"]["defect"] == 1
    html = report(tmp_path).read_text(encoding="utf-8")
    assert len(elements(html, "href", "#finding-alpha-defect")) == 2  # lens + candidate
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    # One supported recommendation needs no invented alternatives or empty prose fields.
    analysis = analysis_manifest(tmp_path, report(tmp_path))
    for key in ("options", "question", "tradeoffs", "evidence_limits"):
        analysis.pop(key)
    publish(tmp_path, "analyze-candidate", analysis)
    assert state(tmp_path)["subsystems"][0]["audit"]["candidates"][0]["analysis"]["options"] == []


def test_preparation_never_overwrites_judgments_or_publishes_a_draft(tmp_path: Path) -> None:
    mapped(tmp_path)
    saved_report = report(tmp_path).read_bytes()
    code, prepared = cli(tmp_path, "prepare-audit", "--subsystem", "alpha")
    assert code == 0 and prepared["prepared"] and not prepared["published"]
    packet = Path(prepared["packet"])
    draft = packet.read_bytes()
    assert json.loads(draft)["source_identity"]["paths"] == ["src/a.py", "tests/test_a.py"]
    code, error = cli(tmp_path, "audit-subsystem", "--manifest", str(packet))
    assert code == 2 and "summary" in error["error"]
    code, error = cli(tmp_path, "prepare-audit", "--subsystem", "alpha")
    assert code == 2 and "already exists" in error["error"]
    assert packet.read_bytes() == draft and report(tmp_path).read_bytes() == saved_report
    code, second = cli(tmp_path, "prepare-audit", "--subsystem", "alpha", "--output", "second.json")
    assert code == 0 and Path(second["packet"]).parent == packet.parent
    assert packet.read_bytes() == draft


def test_explicit_candidate_scope_cannot_hide_linked_inputs(tmp_path: Path) -> None:
    mapped(tmp_path)
    packet = filled_packet(tmp_path)
    raw = json.loads(packet.read_text(encoding="utf-8"))
    raw["candidates"][0]["affected_scope"] = ["alpha"]
    atlas.mutate_report(objective="audit-subsystem", repo_root=tmp_path, report=report(tmp_path), manifest=write_json(packet, raw))
    assert state(tmp_path)["subsystems"][0]["audit"]["candidates"][0]["affected_scope"] == ["alpha", "beta"]
    (tmp_path / "src/b.py").write_text("VALUE=3\n", encoding="utf-8")
    selected = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")
    assert selected["rows"][0]["source_changes"]["scope"]["freshness"] == "changed"
    damaged = state(tmp_path)
    damaged["subsystems"][0]["audit"]["candidates"][0]["affected_scope"] = ["alpha"]
    report(tmp_path).write_bytes(atlas._render(damaged))
    with pytest.raises(atlas.ReportError, match="candidate scope omits linked finding scope"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


@pytest.mark.parametrize("change", ["source", "report"])
def test_prepared_packet_keeps_source_and_report_guards(tmp_path: Path, change: str) -> None:
    mapped(tmp_path)
    packet = filled_packet(tmp_path)
    if change == "source":
        (tmp_path / "src/b.py").write_text("VALUE=3\n", encoding="utf-8")
    else:
        atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="subsystem", identifier="alpha", title="Validation")
    saved = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="current bound source|expected_report_sha256"):
        atlas.mutate_report(objective="audit-subsystem", repo_root=tmp_path, report=report(tmp_path), manifest=packet)
    assert report(tmp_path).read_bytes() == saved


@pytest.mark.parametrize("destination", ["src/a.json", ".tmp/audit-codebase/other/audit.json", ".tmp/audit-codebase/run-1/report.html"])
def test_packet_output_stays_in_its_invocation_directory(tmp_path: Path, destination: str) -> None:
    mapped(tmp_path)
    with pytest.raises(atlas.ReportError, match="JSON file in the report directory"):
        atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", output=Path(destination))
    assert not (tmp_path / destination).exists() or destination.endswith("report.html")


def test_preparation_rejects_unknown_scope_and_includes_explicit_proof(tmp_path: Path) -> None:
    mapped(tmp_path)
    with pytest.raises(atlas.ReportError, match="unknown or retired"):
        atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="unknown")
    (tmp_path / "proof.txt").write_text("Extra proof input", encoding="utf-8")
    prepared = atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", paths=["proof.txt"])
    assert "proof.txt" in prepared["source_paths"]


def test_presentation_edit_preserves_analysis_outcomes_and_freshness(tmp_path: Path) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "checked", "verified"))
    before = state(tmp_path)
    title = ("Shared validation for alternate callers <unsafe> " * 4).strip()
    code, result = cli(tmp_path, "edit-presentation", "--kind", "candidate", "--id", "alpha-fix", "--title", title)
    assert code == 0 and result["published"]
    after = state(tmp_path)
    for key in ("subsystems", "systemic_findings", "outcomes", "delivery_requirements", "freshness", "candidate_freshness", "outcome_freshness"):
        assert after[key] == before[key]
    assert after["history"][:-1] == before["history"]
    assert after["history"][-1]["operation"] == "presentation"
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)
    assert selected["rows"][0]["title"] == "Centralize validation"
    assert selected["rows"][0]["display_title"] == title
    assert selected["rows"][0]["work"]["status"] == "verified"
    assert selected["history"][-1]["operation"] == "presentation"
    html = report(tmp_path).read_text(encoding="utf-8")
    assert "<unsafe>" not in html and "&lt;unsafe&gt;" in html
    assert len(elements(html, "id", "candidate-alpha-fix")) == 1
    assert len(elements(html, "class", "candidate-heading")) == 1
    unchanged = atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="candidate", identifier="alpha-fix", title=title)
    assert unchanged["unchanged"] and not unchanged["published"]
    cli(tmp_path, "edit-presentation", "--kind", "candidate", "--id", "alpha-fix", "--clear")
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["display_title"] == "Centralize validation"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_labels_survive_retirement_and_do_not_renew_changed_evidence(tmp_path: Path) -> None:
    started(tmp_path)
    before = state(tmp_path)["subsystems"][0]["audit"]
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="finding", identifier="alpha-defect", title="Caller bypass")
    (tmp_path / "src/a.py").write_text("VALUE=9\n", encoding="utf-8")
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="subsystem", identifier="alpha", title="Validation with longer ownership wording")
    assert state(tmp_path)["freshness"]["alpha"] == "changed"
    assert state(tmp_path)["subsystems"][0]["audit"] == before
    replacement = map_manifest(tmp_path)["subsystems"][0]
    replacement.update(id="gamma", name="Replacement")
    reconcile(tmp_path, subsystems=[replacement], retirements=[{"id": "alpha", "replacement_ids": ["gamma"], "reason": "Moved owner"}])
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", history=True)
    assert selected["rows"][0]["historical"] and selected["rows"][0]["display_title"] == "Caller bypass"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_clearing_absent_label_is_a_complete_no_op(tmp_path: Path) -> None:
    mapped(tmp_path)
    before = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=True)
    result = atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="subsystem", identifier="alpha", title=None)
    assert result["unchanged"] and not result["published"]
    assert result["report_sha256"] == before["report_sha256"]
    assert result["state_sha256"] == before["state_sha256"]
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=True)["state"] == before["state"]


def test_label_history_filters_qualified_ids_and_keeps_relevant_owner_labels(tmp_path: Path) -> None:
    started(tmp_path)
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="subsystem", identifier="beta", title="Result delivery")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)
    assert any(record["operation"] == "presentation" and record["selection"] == "beta" for record in selected["history"])
    # IDs are reserved within their own kind; a matching finding ID is a different target.
    packet = json.loads((tmp_path / "audit-subsystem.json").read_text(encoding="utf-8"))
    packet["expected_report_sha256"] = sha(report(tmp_path))
    packet["findings"][0]["id"] = "alpha-fix"
    packet["candidates"][0]["finding_ids"] = ["alpha-fix"]
    packet["lenses"][0]["finding_ids"] = ["alpha-fix"]
    publish(tmp_path, "audit-subsystem", packet)
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="candidate", identifier="alpha-fix", title="Candidate label")
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="finding", identifier="alpha-fix", title="Finding label")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-fix", history=True)
    edits = [record for record in selected["history"] if record["operation"] == "presentation"]
    assert not any(record["kind"] == "candidate" for record in edits)
    assert any(record["kind"] == "finding" for record in edits)


@pytest.mark.parametrize("kind,identifier,title", [("candidate", "missing", "Title"), ("unknown", "alpha-fix", "Title"), ("finding", "alpha-defect", "")])
def test_invalid_presentation_edits_preserve_report(tmp_path: Path, kind: str, identifier: str, title: str) -> None:
    started(tmp_path, analyzed=False)
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError):
        atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind=kind, identifier=identifier, title=title)
    assert report(tmp_path).read_bytes() == before


def test_direct_preview_records_observations_without_claiming_open_or_static_proof(tmp_path: Path) -> None:
    mapped(tmp_path)
    args = ["--environment", "test-host", "--capability", "html-preview", "--unavailable",
            "--reason", "Host cannot render HTML", "--evidence", "Supported host operation returned unavailable"]
    code, result = cli(tmp_path, "record-preview", *args)
    assert code == 0 and result["preview_state"] == "unavailable"
    saved = report(tmp_path).read_bytes()
    code, result = cli(tmp_path, "record-preview", *args)
    assert code == 0 and result["unchanged"] and not result["published"]
    assert report(tmp_path).read_bytes() == saved
    verified = ["--environment", "test-host", "--capability", "html-preview", "--verified",
                "--reason", "Inspected the rendered revision", "--evidence", "Titles and selection controls checked"]
    for digest in (None, "0" * 64):
        code, result = cli(tmp_path, "record-preview", *verified, *([] if digest is None else ["--viewed-report-sha256", digest]))
        assert code == 2 and "report" in result["error"]
        assert report(tmp_path).read_bytes() == saved
    viewed = sha(report(tmp_path))
    code, result = cli(tmp_path, "record-preview", *verified, "--viewed-report-sha256", viewed)
    assert code == 0 and result["preview_state"] == "verified"
    assert state(tmp_path)["preview"][0]["report_sha256"] == viewed
    assert sha(report(tmp_path)) != viewed  # Metadata publication is a distinct revision.
    code, error = cli(tmp_path, "record-preview", "--manifest", "unused.json", *args)
    assert code == 2 and "cannot be combined" in error["error"]


def test_counts_separate_defects_from_retained_complexity_and_gaps(tmp_path: Path) -> None:
    mapped(tmp_path)
    packet = filled_packet(tmp_path)
    raw = json.loads(packet.read_text(encoding="utf-8"))
    raw["findings"] = [{**raw["findings"][0], "id": f"defect-{n}"} for n in range(3)]
    raw["candidates"] = []
    raw["lenses"] = []
    common = {"primary_class": "design", "locations": ["src/a.py"], "evidence": ["Read owner and callers"], "impact": "Decision is bounded", "affected_scope": ["alpha"]}
    raw["findings"] += [{**common, "id": "retained", "kind": "retained complexity", "title": "Policy owner is justified", "protected_constraint": "Separate policy lifecycle"},
                         {**common, "id": "gap", "kind": "gap", "title": "Runtime profile unavailable", "missing_evidence": "Production trace"}]
    atlas.mutate_report(objective="audit-subsystem", repo_root=tmp_path, report=report(tmp_path), manifest=write_json(packet, raw))
    counts = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["summary"]["finding_counts"]
    assert counts == {"defect": 3, "opportunity": 0, "retained complexity": 1, "gap": 1}
    html = report(tmp_path).read_text(encoding="utf-8")
    assert re.search(r'<strong>3</strong><span>Defects</span>', html)
    assert re.search(r'<strong>1</strong><span>Retained complexity</span>', html)
