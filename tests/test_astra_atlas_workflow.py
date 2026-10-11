"""Prepared collaboration, append-only evidence, and verification provenance."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from test_astra_atlas import SCRIPT, analysis_manifest, atlas, audit_manifest, candidate, elements, finding, identity, publish, report, sha
from test_astra_atlas_maintenance import event, outcomes, reconcile, started, state
from test_astra_atlas_usability import mapped


def prepared_audit(root: Path, sid: str, output: str | None = None, append: bool = False) -> dict:
    prepared = atlas.prepare_audit(repo_root=root, report=report(root), subsystem=sid,
                                   affected_subsystems=["beta"] if sid == "alpha" else [],
                                   output=Path(output) if output else None, append=append)
    raw = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    raw["source_trace"]["summary"] = "Inspected the selected inputs."
    f = finding()
    f.update(id=f"{sid}-followup" if append else f"{sid}-defect", affected_scope=[sid])
    c = candidate()
    c.update(id=f"{sid}-followup-fix" if append else f"{sid}-fix", finding_ids=[f["id"]], affected_scope=[sid])
    raw.update(findings=[f], candidates=[c])
    return raw


def add_gap_finding(root: Path) -> dict:
    prepared = atlas.prepare_audit(repo_root=root, report=report(root), subsystem="alpha", affected_subsystems=["beta"], append=True)
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    gap = finding()
    for key in ("severity", "scenario"):
        gap.pop(key)
    gap.update(id="scope-gap", kind="gap", missing_evidence="A runtime trace is needed.")
    packet.update(findings=[gap], source_trace={"summary": "Inspected the shared uncertainty."})
    publish(root, "append-findings", packet)
    return gap


def independent_findings(root: Path, *, gaps: bool = False) -> None:
    mapped(root)
    for sid, source in (("alpha", "src/a.py"), ("beta", "src/b.py")):
        packet = prepared_audit(root, sid)
        packet["findings"][0]["locations"] = [source]
        if gaps:
            row = packet["findings"][0]
            for key in ("severity", "scenario"):
                row.pop(key)
            row.update(kind="gap", missing_evidence="A runtime trace is needed.")
            packet["candidates"] = []
        publish(root, "audit-subsystem", packet)


def test_prepared_audit_cannot_change_its_selected_owner(tmp_path: Path) -> None:
    mapped(tmp_path)
    prepared = atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", affected_subsystems=["beta"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet.update(subsystem_id="beta", source_trace={"summary": "Inspected the packet."})
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "audit-subsystem", packet)
    assert report(tmp_path).read_bytes() == before


def test_finding_packet_guard_includes_new_candidate_group_events(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["finding:alpha-defect"], outcome_type="verified")
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["events"][0].update(summary="Finding verified.", evidence=["Focused probe passed."])
    outcomes(tmp_path, event(tmp_path, "group-reopened", "reopened"))
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "record-outcome", packet)
    assert report(tmp_path).read_bytes() == before


@pytest.mark.parametrize("work", ["outcome", "check", "delivery", "gap"])
def test_prepared_reaudit_rejects_intervening_target_bound_work(tmp_path: Path, work: str) -> None:
    started(tmp_path)
    packet = prepared_audit(tmp_path, "alpha", "revised-alpha.json")
    packet["findings"][0]["title"] = "A revised defect judgment."
    if work == "outcome":
        outcomes(tmp_path, event(tmp_path, "old-record-verified", "verified", target_kind="finding", target_id="alpha-defect"))
    elif work == "check":
        check(tmp_path)
    elif work == "delivery":
        outcomes(tmp_path, delivery_requirements=[{"target": {"kind": "candidate", "id": "alpha-fix"}, "commit": True,
                                                 "deployments": [], "reason": "Selected delivery."}])
    else:
        prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), lenses=["alpha:performance"])
        gap = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
        gap["gaps"][0].update(disposition="closed", summary="Original uncertainty resolved.", evidence=["Trace reviewed."])
        publish(tmp_path, "record-gaps", gap)
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "audit-subsystem", packet)
    assert report(tmp_path).read_bytes() == before


def test_prepared_reaudit_accepts_unrelated_outcomes(tmp_path: Path) -> None:
    independent_findings(tmp_path)
    packet = prepared_audit(tmp_path, "alpha", "revised-alpha.json")
    outcomes(tmp_path, event(tmp_path, "unrelated-deferred", "deferred", target_kind="finding", target_id="beta-defect"))
    publish(tmp_path, "audit-subsystem", packet)
    assert state(tmp_path)["outcomes"][0]["id"] == "unrelated-deferred"


@pytest.mark.parametrize("target_kind,target_id", [("candidate", "alpha-fix"), ("finding", "alpha-defect")])
def test_reintroducing_historical_ids_rejects_intervening_target_work(tmp_path: Path, target_kind: str, target_id: str) -> None:
    started(tmp_path, analyzed=False)
    cleared = audit_manifest(tmp_path, report(tmp_path))
    cleared.update(findings=[], candidates=[])
    for lens in cleared["lenses"]:
        lens["finding_ids"] = []
    publish(tmp_path, "audit-subsystem", cleared)
    packet = prepared_audit(tmp_path, "alpha", "reintroduced-alpha.json")
    outcomes(tmp_path, event(tmp_path, "historical-deferred", "deferred", target_kind=target_kind, target_id=target_id))
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "audit-subsystem", packet)
    assert report(tmp_path).read_bytes() == before
    assert state(tmp_path)["outcomes"][-1]["id"] == "historical-deferred"


@pytest.mark.parametrize("assigned,changed", [("implemented", "verified"), ("verified", "implemented")])
def test_prepared_outcomes_preserve_the_assigned_transition(tmp_path: Path, assigned: str, changed: str) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], outcome_type=assigned)
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["events"][0].update(type=changed, summary="Edited the assigned state transition.", evidence=["Focused probe passed."])
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "record-outcome", packet)
    assert report(tmp_path).read_bytes() == before and state(tmp_path)["outcomes"] == []


@pytest.mark.parametrize("operation", ["audit-subsystem", "analyze-candidate", "record-outcome", "record-gaps"])
@pytest.mark.parametrize("change", ["scope", "snapshot"])
def test_prepared_packets_preserve_their_assigned_source_identity(tmp_path: Path, operation: str, change: str) -> None:
    started(tmp_path, analyzed=False)
    proof = tmp_path / "proof.txt"
    proof.write_text("original proof", encoding="utf-8")
    if operation == "audit-subsystem":
        packet = prepared_audit(tmp_path, "alpha", "assigned-audit.json")
        row, removed, changed_path = packet, "src/b.py", tmp_path / "src/a.py"
    else:
        if operation == "analyze-candidate":
            prepared = atlas.prepare_analysis(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", paths=["proof.txt"])
        elif operation == "record-outcome":
            prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                              outcome_type="verified", paths=["proof.txt"])
        else:
            prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), lenses=["alpha:performance"], paths=["proof.txt"])
        packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
        if operation == "analyze-candidate":
            judgments = analysis_manifest(tmp_path, report(tmp_path))
            packet.update({key: judgments[key] for key in ("state", "summary", "cause", "recommendation", "proof")})
            row = packet
        elif operation == "record-outcome":
            row = packet["events"][0]
            row.update(summary="Selected work verified.", evidence=["Proof reviewed."])
        else:
            row = packet["gaps"][0]
            row.update(summary="Trace remains needed.", evidence=["Probe inspected."], remaining_question="What is runtime latency?",
                       revisit_when="A trace is available.")
        removed, changed_path = "proof.txt", proof
    paths = row["source_identity"]["paths"]
    if change == "scope":
        paths = [path for path in paths if path != removed]
    else:
        changed_path.write_text("changed inspected input", encoding="utf-8")
    row["source_identity"] = identity(tmp_path, paths)
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, operation, packet)
    assert report(tmp_path).read_bytes() == before


def test_batch_rebases_independent_packets_and_retry_has_one_receipt(tmp_path: Path, monkeypatch) -> None:
    mapped(tmp_path)
    packets = [{"operation": "audit-subsystem", "manifest": prepared_audit(tmp_path, sid)} for sid in ("alpha", "beta")]
    original = atlas._publish_prepared

    def lost_response(prepared, root):
        original(prepared, root)
        raise atlas.ReportError("response lost after publication")

    monkeypatch.setattr(atlas, "_publish_prepared", lost_response)
    with pytest.raises(atlas.ReportError, match="response lost"):
        atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="owners", packets=packets)
    saved = report(tmp_path).read_bytes()
    monkeypatch.setattr(atlas, "_publish_prepared", original)
    result = atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="owners", packets=packets)
    assert result["already_published"] and report(tmp_path).read_bytes() == saved
    assert len(state(tmp_path)["batches"]) == 1
    assert all("audit" in sub for sub in state(tmp_path)["subsystems"])
    changed = deepcopy(packets)
    changed[0]["manifest"]["source_trace"]["summary"] = "Different judgments."
    with pytest.raises(atlas.ReportError, match="different packets"):
        atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="owners", packets=changed)


@pytest.mark.parametrize("conflict", ["same-target", "source", "ownership", "publication-source"])
def test_conflicting_batch_does_not_publish_partial_work(tmp_path: Path, monkeypatch, conflict: str) -> None:
    mapped(tmp_path)
    packets = [{"operation": "audit-subsystem", "manifest": prepared_audit(tmp_path, "alpha")}]
    if conflict == "same-target":
        packets.append({"operation": "audit-subsystem", "manifest": prepared_audit(tmp_path, "alpha", "second.json")})
    elif conflict == "source":
        (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
    elif conflict == "ownership":
        reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed owner."}])
    else:
        original = atlas._publish_prepared

        def drift(prepared, root):
            (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
            original(prepared, root)

        monkeypatch.setattr(atlas, "_publish_prepared", drift)
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts|bound source"):
        atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="conflict", packets=packets)
    assert report(tmp_path).read_bytes() == before


def test_analysis_and_outcome_preparation_bind_scope_and_proof_inputs(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    (tmp_path / "proof.txt").write_text("probe configuration", encoding="utf-8")
    prepared = atlas.prepare_analysis(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", paths=["proof.txt"])
    path = Path(prepared["packet"])
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["affected_scope"] == ["alpha", "beta"] and "proof.txt" in raw["source_identity"]["paths"]
    judgments = analysis_manifest(tmp_path, report(tmp_path))
    for field in ("state", "summary", "cause", "recommendation", "proof"):
        raw[field] = judgments[field]
    publish(tmp_path, "analyze-candidate", raw)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix", "finding:alpha-defect"], outcome_type="verified", paths=["proof.txt"])
    raw = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    assert len(raw["events"]) == 2 and all("proof.txt" in row["source_identity"]["paths"] for row in raw["events"])
    for row in raw["events"]:
        row.update(summary="Both entries reject invalid input.", evidence=["Focused probe passed."])
    publish(tmp_path, "record-outcome", raw)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verified"


@pytest.mark.parametrize("receipts", [False, True])
def test_prepared_outcomes_bind_only_their_target_and_shared_proof(tmp_path: Path, receipts: bool) -> None:
    independent_findings(tmp_path)
    (tmp_path / "shared-proof.txt").write_text("shared setup", encoding="utf-8")
    check_ids = []
    if receipts:
        for sid in ("alpha", "beta"):
            (tmp_path / f"{sid}-proof.txt").write_text(f"{sid} probe", encoding="utf-8")
            atlas.verify(repo_root=tmp_path, report=report(tmp_path), identifier=f"{sid}-check", targets=[f"finding:{sid}-defect"],
                         command=[sys.executable, "-c", "print('passed')"], environment="fixture", paths=[f"{sid}-proof.txt"])
            check_ids.append(f"{sid}-check")
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["finding:alpha-defect", "finding:beta-defect"],
                                      outcome_type="verified", paths=["shared-proof.txt"], check_ids=check_ids)
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    for row, other in zip(packet["events"], ("beta", "alpha")):
        assert "shared-proof.txt" in row["source_identity"]["paths"]
        assert f"src/{'b' if other == 'beta' else 'a'}.py" not in row["source_identity"]["paths"]
        if receipts:
            assert f"{other}-proof.txt" not in row["source_identity"]["paths"]
        row.update(summary="Relevant behavior verified.", evidence=row["evidence"] or ["Focused probe passed."])
    publish(tmp_path, "record-outcome", packet)
    (tmp_path / "src/b.py").write_text("VALUE=4\n", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    alpha = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    beta = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="beta-defect")["rows"][0]
    assert alpha["work"]["status"] == "verified" and beta["work"]["status"] == "verification changed"
    (tmp_path / "shared-proof.txt").write_text("changed shared setup", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["work"]["status"] == "verification changed"


def test_prepared_candidate_outcome_covers_its_linked_finding_scopes(tmp_path: Path) -> None:
    independent_findings(tmp_path)
    packet = prepared_audit(tmp_path, "alpha", "wider-alpha.json")
    packet["findings"][0]["affected_scope"] = ["alpha", "beta"]
    publish(tmp_path, "audit-subsystem", packet)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], outcome_type="verified")
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["events"][0].update(summary="Both affected owners verified.", evidence=["Both probes passed."])
    assert "src/b.py" in packet["events"][0]["source_identity"]["paths"]
    publish(tmp_path, "record-outcome", packet)


@pytest.mark.parametrize("kind", ["implemented", "verified", "deferred", "reopened", "committed", "deployed"])
def test_explicit_proof_paths_are_guarded_and_retained_for_all_outcomes(tmp_path: Path, kind: str) -> None:
    started(tmp_path)
    proof = tmp_path / "proof.txt"
    proof.write_text("original proof", encoding="utf-8")
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_type=kind, paths=["proof.txt"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    row = packet["events"][0]
    row.update(summary="Recorded selected decision.", evidence=["Proof reviewed."])
    if kind == "committed":
        row["reference"] = atlas._git(tmp_path, "rev-parse", "HEAD")
    elif kind == "deployed":
        row.update(reference="fixture-v1", destination="fixture-host")
    assert "proof.txt" in row["source_identity"]["paths"] and "proof.txt" in prepared["source_paths"]
    before = report(tmp_path).read_bytes()
    proof.write_text("changed proof", encoding="utf-8")
    with pytest.raises(atlas.ReportError, match="current bound source"):
        publish(tmp_path, "record-outcome", packet)
    assert report(tmp_path).read_bytes() == before
    proof.write_text("original proof", encoding="utf-8")
    publish(tmp_path, "record-outcome", packet)
    assert state(tmp_path)["outcomes"][-1]["source_identity"] == row["source_identity"]
    proof.write_text("later proof", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    current = state(tmp_path)
    assert current["outcome_freshness"][row["id"]] == "changed"
    assert current["freshness"]["alpha"] == "fresh" and current["candidate_freshness"]["alpha-fix"] == "fresh"
    html = report(tmp_path).read_text(encoding="utf-8")
    for identifier in ("candidate-alpha-fix", "finding-alpha-defect", "work-candidate-alpha-fix", "subsystem-alpha", "subsystem-beta"):
        assert elements(html, "id", identifier)[0]["data-outcome-freshness"] == "changed"
    assert elements(html, "id", "work-candidate-alpha-fix")[0]["data-freshness"] == "changed"
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["outcome_freshness"] == "changed"


def test_independent_outcome_packets_with_same_id_in_separate_namespaces(tmp_path: Path) -> None:
    independent_findings(tmp_path)
    alpha = prepared_audit(tmp_path, "alpha", "alpha-shared.json")
    alpha["candidates"][0]["id"] = "shared"
    publish(tmp_path, "audit-subsystem", alpha)
    beta = prepared_audit(tmp_path, "beta", "beta-shared.json")
    beta["findings"][0]["id"] = "shared"
    beta["candidates"][0]["finding_ids"] = ["shared"]
    publish(tmp_path, "audit-subsystem", beta)
    packets = []
    for kind in ("candidate", "finding"):
        prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=[f"{kind}:shared"],
                                          outcome_type="deferred", output=Path(f"{kind}-outcome.json"))
        packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
        packet["events"][0].update(summary="Selected work deferred.", evidence=["Reviewed scope."])
        packets.append({"operation": "record-outcome", "manifest": packet})
    atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="namespace-outcomes", packets=packets)
    assert len(state(tmp_path)["outcomes"]) == 2
    for kind in ("candidate", "finding"):
        assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), **{kind: "shared"})["rows"][0]["work"]["status"] == "deferred"


@pytest.mark.parametrize("operation", ["check", "outcome", "analyze"])
def test_history_keeps_candidate_and_finding_namespaces_separate(tmp_path: Path, operation: str) -> None:
    independent_findings(tmp_path)
    alpha = prepared_audit(tmp_path, "alpha", "alpha-shared.json")
    alpha["candidates"][0]["id"] = "shared"
    publish(tmp_path, "audit-subsystem", alpha)
    beta = prepared_audit(tmp_path, "beta", "beta-shared.json")
    beta["findings"][0]["id"] = "shared"
    beta["candidates"][0]["finding_ids"] = ["shared"]
    publish(tmp_path, "audit-subsystem", beta)
    if operation == "check":
        atlas.verify(repo_root=tmp_path, report=report(tmp_path), identifier="candidate-only", targets=["candidate:shared"],
                     command=[sys.executable, "-c", "print('passed')"], environment="fixture")
    elif operation == "outcome":
        outcomes(tmp_path, event(tmp_path, "candidate-only", "deferred", target_id="shared"))
    else:
        packet = analysis_manifest(tmp_path, report(tmp_path))
        packet["candidate_id"] = "shared"
        publish(tmp_path, "analyze-candidate", packet)
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="shared", history=True)["history"]
    unrelated = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="shared", history=True)["history"]
    assert any(row["operation"] == operation for row in selected)
    assert not any(row["operation"] == operation for row in unrelated)


@pytest.mark.parametrize("collection", ["events", "delivery_requirements", "gaps"])
@pytest.mark.parametrize("problem", ["object", "missing-target", "non-object-row"])
def test_malformed_prepared_rows_return_json_without_publishing(tmp_path: Path, collection: str, problem: str) -> None:
    started(tmp_path)
    operation = "record-gaps" if collection == "gaps" else "record-outcome"
    if collection == "gaps":
        prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), lenses=["alpha:performance"])
    else:
        prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], outcome_type="deferred")
    path = Path(prepared["packet"])
    packet = json.loads(path.read_text(encoding="utf-8"))
    packet[collection] = {} if problem == "object" else [{}] if problem == "missing-target" else [None]
    path.write_text(json.dumps(packet), encoding="utf-8")
    before = report(tmp_path).read_bytes()
    result = subprocess.run([sys.executable, str(SCRIPT), operation, "--repo-root", str(tmp_path),
                             "--report", str(report(tmp_path)), "--manifest", str(path)],
                            capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 2 and not result.stderr, result.stderr
    response = json.loads(result.stdout)
    assert response["ok"] is False and collection in response["error"]
    assert report(tmp_path).read_bytes() == before


def test_followup_retains_analysis_and_lenses_with_its_own_source(tmp_path: Path) -> None:
    started(tmp_path)
    before = deepcopy(state(tmp_path)["subsystems"][0]["audit"])
    (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
    raw = prepared_audit(tmp_path, "alpha", append=True)
    publish(tmp_path, "append-findings", raw)
    audit = state(tmp_path)["subsystems"][0]["audit"]
    assert audit["candidates"][0] == before["candidates"][0]
    assert audit["lenses"] == before["lenses"] and audit["source_identity"] == before["source_identity"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["source_changes"]["scope"]["freshness"] == "changed"
    row = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-followup")["rows"][0]
    assert row["audit_source_identity"] == raw["source_identity"] and row["source_changes"]["scope"]["freshness"] == "fresh"
    selected_history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-followup", history=True)["history"]
    assert next(entry for entry in selected_history if entry["operation"] == "append")["packet"]["source_identity"] == raw["source_identity"]
    compact_history = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-followup", history=True)["history"]
    assert all("packet" not in entry for entry in compact_history)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-followup-fix")["rows"][0]["source_changes"]["scope"]["freshness"] == "fresh"
    card = elements(report(tmp_path).read_text(encoding="utf-8"), "id", "candidate-alpha-followup-fix")[0]
    assert card["data-freshness"] == "fresh" and card["data-freshness-cause"] == "none"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    with pytest.raises(atlas.ReportError, match="new"):
        publish(tmp_path, "append-findings", {**raw, "prepared": atlas._guard_view("append-findings", raw, state(tmp_path))})


@pytest.mark.parametrize("rebound", [False, True])
def test_superseded_followups_retain_each_records_original_source_binding(tmp_path: Path, rebound: bool) -> None:
    started(tmp_path)
    proof = tmp_path / "append-proof.txt"
    proof.write_text("append-only evidence", encoding="utf-8")
    prepared = atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", append=True, paths=["append-proof.txt"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    f = {**finding(), "id": "alpha-followup", "affected_scope": ["alpha"]}
    c = {**candidate(), "id": "alpha-followup-fix", "finding_ids": [f["id"]], "affected_scope": ["alpha"]}
    packet.update(findings=[f], candidates=[c], source_trace={"summary": "Inspected the follow-up evidence."})
    publish(tmp_path, "append-findings", packet)
    original = packet["source_identity"]
    latest = original
    if rebound:
        updated = audit_manifest(tmp_path, report(tmp_path))
        updated["findings"].append(f)
        updated["candidates"].append(c)
        publish(tmp_path, "audit-subsystem", updated)
        latest = updated["source_identity"]
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding=f["id"], history=True)
    assert selected["rows"][0]["historical"] and selected["rows"][0]["audit_source_identity"] == latest
    revisions = [revision for row in selected["history"] for revision in row.get("finding_revisions", [])]
    assert revisions[0]["source_identity"] == original and revisions[-1]["source_identity"] == latest
    history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate=c["id"], history=True)["history"]
    candidate_revisions = [row["candidate_revision"] for row in history if "candidate_revision" in row]
    assert candidate_revisions[0]["source_identity"] == original and candidate_revisions[-1]["source_identity"] == latest
    first = next(row["superseded"] for row in state(tmp_path)["history"] if "audit" in row.get("superseded", {}))
    assert first["source_bindings"][f"finding:{f['id']}"]["source_identity"] == original
    assert first["source_bindings"][f"candidate:{c['id']}"]["source_identity"] == original
    proof.write_text("changed append evidence", encoding="utf-8")
    if not rebound:
        observation = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding=f["id"])["rows"][0]["source_changes"]["scope"]
        assert observation["freshness"] == "changed" and "append-proof.txt" in observation["changed_paths"]


def check(root: Path, identifier: str = "probe", reuse: str | None = None, paths=(), command=None, environment="fixture") -> dict:
    return atlas.verify(repo_root=root, report=report(root), identifier=identifier, targets=["candidate:alpha-fix"],
                        command=command or [sys.executable, "-c", "print('verified')"], environment=environment, paths=paths, reuse=reuse)


def test_verification_carries_across_index_changes_and_binds_verified_outcome(tmp_path: Path) -> None:
    started(tmp_path)
    (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
    tested = check(tmp_path)
    assert tested["passed"]
    subprocess.run(["git", "add", "src/a.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "change"], cwd=tmp_path, check=True, capture_output=True)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    carried = check(tmp_path, "carried", reuse="probe")
    assert carried["reused"] and carried["check"]["source_identity"] != tested["check"]["source_identity"]
    assert carried["check"]["content_identity"] == tested["check"]["content_identity"]
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], outcome_type="verified", check_ids=["carried"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["events"][0]["summary"] = "The unchanged inputs retain passing regression proof."
    publish(tmp_path, "record-outcome", packet)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verified"
    assert state(tmp_path)["checks"][0] == tested["check"]
    selected_history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)["history"]
    assert {entry["check_id"] for entry in selected_history if entry["operation"] == "check"} == {"probe", "carried"}


def test_receipts_preserve_original_membership_and_reject_expanded_groups(tmp_path: Path) -> None:
    started(tmp_path)
    original = check(tmp_path)["check"]
    assert original["candidate_findings"] == {"alpha-fix": ["alpha-defect"]}
    verified = event(tmp_path, "original-verification", "verified", check_ids=["probe"])
    outcomes(tmp_path, verified)
    packet = audit_manifest(tmp_path, report(tmp_path))
    additional = {**finding(), "id": "alpha-additional"}
    packet["findings"].append(additional)
    packet["candidates"][0]["finding_ids"].append(additional["id"])
    publish(tmp_path, "audit-subsystem", packet)
    with pytest.raises(atlas.ReportError, match="changed"):
        check(tmp_path, "old-carried", reuse="probe")
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], outcome_type="verified", check_ids=["probe"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["events"][0]["summary"] = "Expanded group verified."
    with pytest.raises(atlas.ReportError, match="membership changed"):
        publish(tmp_path, "record-outcome", packet)
    current = state(tmp_path)
    assert current["checks"][0] == original and current["outcomes"][0]["finding_ids"] == ["alpha-defect"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-additional")["rows"][0]["work"]["status"] == "open"
    check(tmp_path, "expanded")
    verified["id"] = "expanded-verification"
    verified["check_ids"] = ["expanded"]
    outcomes(tmp_path, verified)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-additional")["rows"][0]["work"]["status"] == "verified"


@pytest.mark.parametrize("target_kind", ["candidate", "finding"])
@pytest.mark.parametrize("field,value", [("proof", ["Both callers reject negative and missing values"]),
                                         ("expectation", "Both callers reject negative and missing values"),
                                         ("scenario", "A missing value bypasses validation in the second caller")])
def test_verification_binds_the_finding_claim_even_when_source_is_unchanged(tmp_path: Path, target_kind: str, field: str, value) -> None:
    started(tmp_path)
    target_id = "alpha-fix" if target_kind == "candidate" else "alpha-defect"
    targets = [f"{target_kind}:{target_id}"]
    args = dict(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                command=[sys.executable, "-c", "print('verified')"], environment="fixture")
    receipt = atlas.verify(identifier="original", **args)["check"]
    outcomes(tmp_path, event(tmp_path, "original-verified", "verified", target_kind=target_kind,
                             target_id=target_id, check_ids=["original"]))
    original_outcome = state(tmp_path)["outcomes"][0]
    packet = audit_manifest(tmp_path, report(tmp_path))
    packet["findings"][0][field] = value
    publish(tmp_path, "audit-subsystem", packet)
    current = state(tmp_path)
    assert current["checks"][0] == receipt and current["outcomes"][0] == original_outcome
    assert current["outcome_source_changes"]["original-verified"]["changed_findings"] == ["alpha-defect"]
    assert current["outcome_source_changes"]["original-verified"]["changed_paths"] == []
    selected = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["work"]["status"] == "verification changed"
    with pytest.raises(atlas.ReportError, match="changed"):
        atlas.verify(identifier="stale-carried", reuse="original", **args)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                                      outcome_type="verified", check_ids=["original"], output=Path("stale-outcome.json"))
    stale = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    stale["events"][0]["summary"] = "Attempted to reuse proof of the old claim."
    with pytest.raises(atlas.ReportError, match="finding claim changed"):
        publish(tmp_path, "record-outcome", stale)
    atlas.verify(identifier="revised", **args)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                                      outcome_type="verified", check_ids=["revised"], output=Path("revised-outcome.json"))
    renewed = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    renewed["events"][0]["summary"] = "Checked the revised claim."
    publish(tmp_path, "record-outcome", renewed)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["work"]["status"] == "verified"
    assert state(tmp_path)["checks"][0] == receipt


def test_unchanged_reaudit_and_presentation_edits_preserve_claim_verification(tmp_path: Path) -> None:
    started(tmp_path)
    original = check(tmp_path)["check"]
    outcomes(tmp_path, event(tmp_path, "verified", "verified", check_ids=["probe"]))
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="finding", identifier="alpha-defect", title="Clearer finding label")
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="candidate", identifier="alpha-fix", title="Clearer candidate label")
    carried = check(tmp_path, "carried", reuse="probe")
    assert carried["reused"] and carried["check"]["finding_sha256"] == original["finding_sha256"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["work"]["status"] == "verified"


def test_agent_supplied_verification_retains_its_claim_revision(tmp_path: Path) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "verified", "verified"))
    original = state(tmp_path)["outcomes"][0]
    packet = audit_manifest(tmp_path, report(tmp_path))
    packet["findings"][0]["proof"] = ["Additional evidence is required for the revised claim."]
    publish(tmp_path, "audit-subsystem", packet)
    assert state(tmp_path)["outcomes"][0] == original
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["work"]["status"] == "verification changed"


@pytest.mark.parametrize("target_kind", ["candidate", "finding"])
@pytest.mark.parametrize("field,value", [("proof", ["Check both callers and the revised failure path"]),
                                         ("cause", "The second caller owns the failure path"),
                                         ("recommendation", "Keep distinct owners and share only input parsing")])
def test_revised_candidate_analysis_requires_current_group_proof(tmp_path: Path, target_kind: str, field: str, value) -> None:
    started(tmp_path)
    target_id = "alpha-fix" if target_kind == "candidate" else "alpha-defect"
    targets = [f"{target_kind}:{target_id}"]
    args = dict(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                command=[sys.executable, "-c", "print('verified')"], environment="fixture")
    original = atlas.verify(identifier="original", **args)["check"]
    outcomes(tmp_path, event(tmp_path, "verified", "verified", target_kind=target_kind,
                             target_id=target_id, check_ids=["original"]))
    before = state(tmp_path)
    packet = analysis_manifest(tmp_path, report(tmp_path))
    packet[field] = value
    publish(tmp_path, "analyze-candidate", packet)
    current = state(tmp_path)
    assert current["checks"][0] == original and current["outcomes"] == before["outcomes"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verification changed"
    with pytest.raises(atlas.ReportError, match="changed"):
        atlas.verify(identifier="stale-carried", reuse="original", **args)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                                      outcome_type="verified", check_ids=["original"], output=Path("stale-analysis.json"))
    stale = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    stale["events"][0]["summary"] = "Proof predates the revised candidate contract."
    if target_kind == "candidate":
        assert current["outcome_source_changes"]["verified"]["changed_candidates"] == ["alpha-fix"]
        assert current["outcome_source_changes"]["verified"]["changed_paths"] == []
        with pytest.raises(atlas.ReportError, match="candidate analysis changed"):
            publish(tmp_path, "record-outcome", stale)
    else:
        publish(tmp_path, "record-outcome", stale)
        assert state(tmp_path)["outcomes"][-1]["candidate_sha256"] == {}
        assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["work"]["status"] == "verified"
        assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verification changed"
    atlas.verify(identifier="revised", **args)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                                      outcome_type="verified", check_ids=["revised"], output=Path("revised-analysis.json"))
    renewed = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    renewed["events"][0]["summary"] = "Current proof supports the revised candidate analysis."
    publish(tmp_path, "record-outcome", renewed)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verified"


def test_candidate_verification_binds_declared_analysis_proof_inputs(tmp_path: Path) -> None:
    started(tmp_path)
    proof = tmp_path / "analysis-proof.txt"
    proof.write_text("original probe input", encoding="utf-8")
    packet = analysis_manifest(tmp_path, report(tmp_path))
    packet["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", proof.name])
    publish(tmp_path, "analyze-candidate", packet)
    first = check(tmp_path)["check"]
    assert proof.name in first["source_identity"]["paths"]
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_type="verified", check_ids=["probe"])
    outcome = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    assert proof.name in outcome["events"][0]["source_identity"]["paths"]
    outcome["events"][0]["summary"] = "Proof includes the declared analysis input."
    publish(tmp_path, "record-outcome", outcome)
    proof.write_text("changed probe input", encoding="utf-8")
    with pytest.raises(atlas.ReportError, match="changed"):
        check(tmp_path, "stale", reuse="probe")
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verification changed"
    assert state(tmp_path)["checks"][0] == first


def test_new_analysis_input_changes_the_contract_even_if_the_receipt_already_bound_its_bytes(tmp_path: Path) -> None:
    started(tmp_path)
    proof = tmp_path / "analysis-proof.txt"
    proof.write_text("probe input", encoding="utf-8")
    first = check(tmp_path, paths=[proof.name])["check"]
    packet = analysis_manifest(tmp_path, report(tmp_path))
    packet["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", proof.name])
    publish(tmp_path, "analyze-candidate", packet)
    with pytest.raises(atlas.ReportError, match="changed"):
        check(tmp_path, "stale", reuse="probe", paths=[proof.name])
    renewed = check(tmp_path, "renewed")
    assert renewed["check"]["content_identity"] == first["content_identity"]
    assert renewed["check"]["candidate_sha256"] != first["candidate_sha256"]


@pytest.mark.parametrize("keep_original", [False, True])
def test_check_history_uses_membership_recorded_when_the_check_ran(tmp_path: Path, keep_original: bool) -> None:
    started(tmp_path)
    original = check(tmp_path)["check"]
    packet = audit_manifest(tmp_path, report(tmp_path))
    later = {**finding(), "id": "alpha-later"}
    packet["findings"] = packet["findings"] + [later] if keep_original else [later]
    packet["candidates"][0]["finding_ids"] = [row["id"] for row in packet["findings"]]
    if not keep_original:
        for lens in packet["lenses"]:
            lens["finding_ids"] = ["alpha-later" if identifier == "alpha-defect" else identifier for identifier in lens["finding_ids"]]
    publish(tmp_path, "audit-subsystem", packet)
    check(tmp_path, "later-probe")
    def checks_for(identifier: str) -> set[str]:
        history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding=identifier, history=True)["history"]
        return {row["check_id"] for row in history if "check_id" in row}
    assert checks_for("alpha-later") == {"later-probe"}
    assert checks_for("alpha-defect") == ({"probe", "later-probe"} if keep_original else {"probe"})
    assert state(tmp_path)["checks"][0] == original


@pytest.mark.parametrize("removed", [False, True])
def test_verified_outcomes_require_unchanged_existing_receipt_logs(tmp_path: Path, removed: bool) -> None:
    started(tmp_path)
    receipt = check(tmp_path)["check"]
    log = tmp_path / receipt["log"]["path"]
    if removed:
        log.unlink()
    else:
        log.write_text("Changed output", encoding="utf-8")
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="log is missing or changed"):
        outcomes(tmp_path, event(tmp_path, "unsupported-verification", "verified", check_ids=["probe"]))
    assert report(tmp_path).read_bytes() == before
    assert state(tmp_path)["checks"][0] == receipt  # Historical inspection remains available.


@pytest.mark.parametrize("removed", [False, True])
def test_verified_outcomes_observe_receipt_log_integrity_after_publication(tmp_path: Path, removed: bool) -> None:
    started(tmp_path)
    receipt = check(tmp_path)["check"]
    check(tmp_path, "carried", reuse="probe")
    outcomes(tmp_path, event(tmp_path, "verified", "verified", check_ids=["probe", "carried"]))
    original = state(tmp_path)["outcomes"][0]
    log = tmp_path / receipt["log"]["path"]
    saved_log = log.read_bytes()
    saved_report = report(tmp_path).read_bytes()
    if removed:
        log.unlink()
    else:
        log.write_text("Changed proof output", encoding="utf-8")
    selected = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]
    assert selected["work"]["status"] == "verification changed"
    inspected = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert inspected["valid"] and inspected["outcome_freshness"]["verified"] == "changed"
    assert inspected["outcome_source_changes"]["verified"]["changed_checks"] == ["probe", "carried"]
    assert report(tmp_path).read_bytes() == saved_report
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    current = state(tmp_path)
    assert current["checks"][0] == receipt and current["outcomes"][0] == original
    assert current["outcome_freshness"]["verified"] == "changed"
    log.write_bytes(saved_log)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verified"


def test_relative_path_verifier_runs_from_repository_and_binds_actual_binary(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    started(root)
    caller = tmp_path / "caller"
    (caller / "bin").mkdir(parents=True)
    (root / "bin").mkdir()
    runtime = Path(os.environ["COMSPEC"]) if os.name == "nt" else Path("/bin/sh")
    name = "probe.exe" if os.name == "nt" else "probe"
    repo_exe, caller_exe = root / "bin" / name, caller / "bin" / name
    shutil.copy2(runtime, repo_exe)
    shutil.copy2(runtime, caller_exe)
    with caller_exe.open("ab") as stream:
        stream.write(b"caller verifier")
    monkeypatch.chdir(caller)
    monkeypatch.setenv("PATH", "bin" + os.pathsep + os.environ.get("PATH", ""))
    calls = []
    original = subprocess.run
    def observe(args, **kwargs):
        calls.append(args[0])
        return original(args, **kwargs)
    monkeypatch.setattr(atlas.subprocess, "run", observe)
    command = [name, "/c" if os.name == "nt" else "-c", "echo repo-verifier"]
    first = check(root, command=command)
    assert first["passed"] and str(repo_exe) in calls and str(caller_exe) not in calls
    assert "repo-verifier" in (root / first["check"]["log"]["path"]).read_text(encoding="utf-8")
    assert check(root, "carried", reuse="probe", command=command)["reused"]
    with repo_exe.open("ab") as stream:
        stream.write(b"changed repository verifier")
    with pytest.raises(atlas.ReportError, match="environment changed"):
        check(root, "stale-carried", reuse="probe", command=command)


@pytest.mark.parametrize("changed", ["content", "proof", "proof-scope", "ownership", "environment", "command", "log"])
def test_check_reuse_rejects_changed_relevant_inputs(tmp_path: Path, changed: str) -> None:
    started(tmp_path)
    (tmp_path / "proof.txt").write_text("probe", encoding="utf-8")
    first = check(tmp_path, paths=["proof.txt"])
    args = {"paths": ["proof.txt"]}
    if changed == "content":
        (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
    elif changed == "proof":
        (tmp_path / "proof.txt").write_text("different probe", encoding="utf-8")
    elif changed == "proof-scope":
        args["paths"] = []
    elif changed == "ownership":
        reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed owner."}])
    elif changed == "environment":
        args["environment"] = "other host"
    elif changed == "command":
        args["command"] = [sys.executable, "-c", "print('different check')"]
    else:
        (tmp_path / first["check"]["log"]["path"]).write_bytes(b"replaced log")
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="changed|missing"):
        check(tmp_path, "carried", reuse="probe", **args)
    assert report(tmp_path).read_bytes() == before


@pytest.mark.parametrize("command", [[sys.executable, "-c", "raise SystemExit(3)"],
    [sys.executable, "-c", "from pathlib import Path; Path('src/a.py').write_text('VALUE=4\\n')"]])
def test_failing_or_source_mutating_check_cannot_establish_verification(tmp_path: Path, command) -> None:
    started(tmp_path)
    result = check(tmp_path, command=command)
    assert not result["passed"]
    with pytest.raises(atlas.ReportError, match="passing"):
        check(tmp_path, "carried", reuse="probe", command=command)
    verified = event(tmp_path, "verified", "verified")
    verified["check_ids"] = ["probe"]
    with pytest.raises(atlas.ReportError, match="passing"):
        outcomes(tmp_path, verified)


@pytest.mark.parametrize("failure", ["startup", "publication"])
def test_failed_check_setup_can_retry_the_same_id(tmp_path: Path, monkeypatch, failure: str) -> None:
    started(tmp_path)
    original = atlas._publish_prepared
    command = None
    if failure == "startup":
        command = [str(tmp_path / "missing-executable")]
    else:
        def fail_publication(prepared, root):
            raise atlas.ReportError("publication unavailable")
        monkeypatch.setattr(atlas, "_publish_prepared", fail_publication)
    with pytest.raises(atlas.ReportError, match="cannot run|publication unavailable"):
        check(tmp_path, command=command)
    assert not report(tmp_path).with_name("check-probe.log").exists()
    assert state(tmp_path)["checks"] == []
    monkeypatch.setattr(atlas, "_publish_prepared", original)
    assert check(tmp_path)["passed"]


@pytest.mark.parametrize("failure", [PermissionError, FileNotFoundError])
def test_verifier_identity_failures_return_json_and_leave_the_id_retryable(tmp_path: Path, monkeypatch, capsys, failure) -> None:
    started(tmp_path)
    before = report(tmp_path).read_bytes()
    executable = Path(sys.executable).resolve()
    original = Path.read_bytes
    def unreadable(path):
        if path.resolve() == executable:
            raise failure("Verifier identity is unavailable.")
        return original(path)
    with monkeypatch.context() as patch:
        patch.setattr(Path, "read_bytes", unreadable)
        result = atlas.main(["verify", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                             "--id", "probe", "--target", "candidate:alpha-fix", "--environment", "fixture", "--",
                             sys.executable, "-c", "print('verified')"])
    captured = capsys.readouterr()
    assert result == 2 and not captured.err
    assert "cannot capture verification executable identity" in json.loads(captured.out)["error"]
    assert report(tmp_path).read_bytes() == before and not report(tmp_path).with_name("check-probe.log").exists()
    assert check(tmp_path)["passed"]


@pytest.mark.parametrize("failure", ["missing", "unreadable", "cleanup-denied"])
def test_log_finalization_failures_return_json_and_preserve_recovery(tmp_path: Path, monkeypatch, capsys, failure: str) -> None:
    started(tmp_path)
    before = report(tmp_path).read_bytes()
    log = report(tmp_path).with_name("check-probe.log")
    read, unlink = Path.read_bytes, Path.unlink
    def unreadable(path):
        if path == log:
            raise (FileNotFoundError if failure == "missing" else PermissionError)("Verification log is unavailable.")
        return read(path)
    def protected(path, **kwargs):
        if path == log:
            raise PermissionError("Unused log cleanup is unavailable.")
        return unlink(path, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(Path, "read_bytes", unreadable)
        if failure == "cleanup-denied":
            patch.setattr(Path, "unlink", protected)
        result = atlas.main(["verify", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                             "--id", "probe", "--target", "candidate:alpha-fix", "--environment", "fixture", "--",
                             sys.executable, "-c", "print('verified')"])
    captured = capsys.readouterr()
    assert result == 2 and not captured.err
    error = json.loads(captured.out)["error"]
    assert "cannot finalize verification log" in error
    assert report(tmp_path).read_bytes() == before and state(tmp_path)["checks"] == []
    if failure == "cleanup-denied":
        assert "cannot remove unused verification log" in error and log.is_file()
        log.unlink()
    else:
        assert not log.exists()
    assert check(tmp_path)["passed"]


@pytest.mark.parametrize("existing", [True, False])
def test_failed_check_cleanup_preserves_existing_or_published_logs(tmp_path: Path, monkeypatch, existing: bool) -> None:
    started(tmp_path)
    log = report(tmp_path).with_name("check-probe.log")
    if existing:
        log.write_bytes(b"Existing evidence")
        with pytest.raises(atlas.ReportError, match="cannot run"):
            check(tmp_path)
        assert log.read_bytes() == b"Existing evidence"
    else:
        original = atlas._publish_prepared
        def lost_response(prepared, root):
            original(prepared, root)
            raise atlas.ReportError("response lost after publication")
        monkeypatch.setattr(atlas, "_publish_prepared", lost_response)
        with pytest.raises(atlas.ReportError, match="response lost"):
            check(tmp_path)
        assert log.is_file() and state(tmp_path)["checks"][0]["log"]["sha256"] == sha(log)


@pytest.mark.parametrize("kind", ["lens", "finding"])
@pytest.mark.parametrize("change", ["ownership", "metadata"])
def test_gap_freshness_follows_current_ownership_and_reassessment(tmp_path: Path, kind: str, change: str) -> None:
    started(tmp_path)
    if kind == "finding":
        add_gap_finding(tmp_path)
    selection = {"lenses": ["alpha:performance"]} if kind == "lens" else {"findings": ["scope-gap"]}
    def close(output: str):
        prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), output=Path(output), **selection)
        packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
        packet["gaps"][0].update(disposition="closed", summary="Trace resolves the question.", evidence=["Relevant trace inspected."])
        publish(tmp_path, "record-gaps", packet)
        return packet["gaps"][0]["id"]
    first = close("first-gap.json")
    if change == "ownership":
        (tmp_path / "src/new.py").write_text("VALUE=3\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", "src/new.py"], cwd=tmp_path, check=True)
        reconcile(tmp_path, ownership_changes=[{"path": "src/new.py", "owner": "alpha", "reason": "Reviewed new entry."}])
    else:
        reconcile(tmp_path, subsystems=[{"id": "alpha", "ownership": "Reviewed new boundary."}])
    rows = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", gaps=True)["gaps"]
    row = next(row for row in rows if row["event_id"] == first)
    assert row["disposition"] == "closed" and row["source_changes"]["freshness"] == "changed"
    assert row["source_changes"]["structure_changes"]["alpha"]
    if change == "ownership":
        assert "src/new.py" in row["source_changes"]["changed_paths"]
    second = close("second-gap.json")
    row = next(row for row in atlas.status_report(repo_root=tmp_path, report=report(tmp_path), gaps=True)["gaps"] if row["event_id"] == second)
    assert row["source_changes"]["freshness"] == "fresh"


@pytest.mark.parametrize("retired", [False, True])
def test_gap_filter_includes_affected_current_owners(tmp_path: Path, retired: bool) -> None:
    started(tmp_path)
    gap = add_gap_finding(tmp_path)
    owner = "beta"
    if retired:
        replacement = {key: value for key, value in state(tmp_path)["subsystems"][1].items() if key not in {"state", "map_source"}}
        replacement.update(id="gamma", name="Gamma")
        reconcile(tmp_path, subsystems=[replacement, {"id": "alpha", "dependencies": [{"id": "gamma", "evidence": ["Reviewed replacement."]}]}],
                  retirements=[{"id": "beta", "replacement_ids": ["gamma"], "reason": "New boundary."}])
        owner = "gamma"
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), subsystem=owner, gaps=True)
    assert {"kind": "finding", "id": gap["id"]} in [row["target"] for row in selected["gaps"]]
    index = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["subsystems"]
    assert next(row for row in index if row["subsystem_id"] == owner)["work_counts"]["gaps"] == 1


def test_prepared_gaps_keep_unrelated_targets_fresh(tmp_path: Path) -> None:
    independent_findings(tmp_path, gaps=True)
    prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), findings=["alpha-defect", "beta-defect"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    for row in packet["gaps"]:
        row.update(summary="More evidence remains needed.", evidence=["Scoped probe inspected."],
                   remaining_question="What is runtime latency?", revisit_when="A trace is available.")
    publish(tmp_path, "record-gaps", packet)
    (tmp_path / "src/b.py").write_text("VALUE=4\n", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    alpha = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", gaps=True)["gaps"][0]
    beta = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="beta-defect", gaps=True)["gaps"][0]
    assert alpha["source_changes"]["freshness"] == "fresh" and beta["source_changes"]["freshness"] == "changed"


@pytest.mark.parametrize("kind", ["finding", "lens"])
def test_independently_prepared_gap_packets_publish_together(tmp_path: Path, kind: str) -> None:
    independent_findings(tmp_path, gaps=True)
    if kind == "lens":
        for sid in ("alpha", "beta"):
            packet = prepared_audit(tmp_path, sid, f"{sid}-lens.json")
            packet["lenses"] = [{"class": "performance", "state": "evidence gap", "reason": "A trace is needed."}]
            publish(tmp_path, "audit-subsystem", packet)
    packets = []
    for sid in ("alpha", "beta"):
        selection = {"findings": [f"{sid}-defect"]} if kind == "finding" else {"lenses": [f"{sid}:performance"]}
        prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), output=Path(f"{sid}-gaps.json"), **selection)
        packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
        packet["gaps"][0].update(summary="Trace remains needed.", evidence=["Scoped investigation."],
                                 remaining_question="What is runtime latency?", revisit_when="A trace is available.")
        packets.append({"operation": "record-gaps", "manifest": packet})
    atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="independent-gaps", packets=packets)
    saved = report(tmp_path).read_bytes()
    assert atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="independent-gaps", packets=packets)["already_published"]
    assert report(tmp_path).read_bytes() == saved
    assert len(state(tmp_path)["gap_dispositions"]) == 2
    assert all(row["disposition"] == "narrowed" for row in atlas.status_report(repo_root=tmp_path, report=report(tmp_path), gaps=True)["gaps"])


def test_historical_gap_claims_reject_new_dispositions_and_preserve_existing_history(tmp_path: Path) -> None:
    started(tmp_path)
    add_gap_finding(tmp_path)
    prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), findings=["scope-gap"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    packet["gaps"][0].update(disposition="closed", summary="Original uncertainty resolved.", evidence=["Trace reviewed."])
    publish(tmp_path, "record-gaps", packet)
    original = state(tmp_path)["gap_dispositions"][0]
    prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), findings=["scope-gap"], output=Path("later-gap.json"))
    later = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    later["gaps"][0].update(disposition="closed", summary="Another disposition.", evidence=["New trace reviewed."])
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="current gap finding"):
        atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), findings=["scope-gap"], output=Path("historical-gap.json"))
    later.pop("prepared")
    later["expected_report_sha256"] = sha(report(tmp_path))
    with pytest.raises(atlas.ReportError, match="current gap finding"):
        publish(tmp_path, "record-gaps", later)
    assert report(tmp_path).read_bytes() == before and state(tmp_path)["gap_dispositions"] == [original]
    history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="scope-gap", history=True)["history"]
    assert any(original in row.get("gap_dispositions", []) for row in history)


def test_gap_dispositions_do_not_rewrite_audit_or_fix_status(tmp_path: Path) -> None:
    started(tmp_path)
    original = state(tmp_path)["subsystems"][0]["audit"]
    prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), lenses=["alpha:performance"])
    raw = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    raw["gaps"][0].update(id="performance-narrowed", disposition="narrowed",
           summary="The repeated work is bounded; production latency remains unknown.", evidence=["Focused workload probe."],
           remaining_question="Does production latency matter?", revisit_when="A production trace is available.",
    )
    publish(tmp_path, "record-gaps", raw)
    assert state(tmp_path)["subsystems"][0]["audit"] == original and state(tmp_path)["outcomes"] == []
    result = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), gaps=True)
    assert result["gaps"][0]["disposition"] == "narrowed" and result["gaps"][0]["remaining_question"]
    selected_history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", history=True)["history"]
    assert next(entry for entry in selected_history if entry["operation"] == "gap")["gap_dispositions"][0]["id"] == "performance-narrowed"
    assert "performance-narrowed" in report(tmp_path).read_text(encoding="utf-8")
    changed_audit = {"version": 1, "expected_report_sha256": sha(report(tmp_path)), "subsystem_id": "alpha",
                     "source_identity": raw["gaps"][0]["source_identity"], "source_trace": {"summary": "New assessment."},
                     "lenses": [{"class": "performance", "state": "evidence gap", "reason": "Different question."}]}
    publish(tmp_path, "audit-subsystem", changed_audit)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), gaps=True)["gaps"][0]["disposition"] == "open"


def test_compact_gap_status_omits_evidence_without_losing_selected_detail(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_gaps(repo_root=tmp_path, report=report(tmp_path), lenses=["alpha:performance"])
    packet = json.loads(Path(prepared["packet"]).read_text(encoding="utf-8"))
    evidence = ["LARGE_GAP_EVIDENCE" * 10000, "Focused probe output."]
    packet["gaps"][0].update(id="performance-probe", disposition="narrowed", summary="Work is bounded.",
                            evidence=evidence, remaining_question="What is production latency?",
                            revisit_when="A production trace is available.")
    publish(tmp_path, "record-gaps", packet)
    result = subprocess.run([sys.executable, str(SCRIPT), "status", "--repo-root", str(tmp_path),
                             "--report", str(report(tmp_path)), "--gaps", "--limit", "1"],
                            capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    row = json.loads(result.stdout)["gaps"][0]
    assert "evidence" not in row and row["evidence_count"] == len(evidence)
    assert "LARGE_GAP_EVIDENCE" not in result.stdout
    assert row["event_id"] == "performance-probe" and row["remaining_question"]
    detail = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", gaps=True)
    assert detail["gaps"][0]["evidence"] == evidence
    history = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha", history=True)
    assert next(entry for entry in history["history"] if entry["operation"] == "gap")["gap_dispositions"][0]["evidence"] == evidence


def test_immutable_pool_roundtrips_history_and_rejects_tampering(tmp_path: Path) -> None:
    started(tmp_path)
    original = state(tmp_path)
    wire = atlas._pack_state(original)
    assert atlas._unpack_state(wire) == original
    packets = [value for value in wire["objects"].values() if isinstance(value, dict) and "fingerprints" in value]
    assert len(packets) == len({atlas._digest(atlas._canonical(value)) for value in packets})
    saved = report(tmp_path).read_bytes()
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    assert state(tmp_path)["history"] == original["history"]
    identity_key = next(iter(wire["objects"]))
    wire["objects"][identity_key] = ["corrupt"]
    with pytest.raises(atlas.ReportError, match="digest"):
        atlas._unpack_state(wire)
    assert saved and atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_windows_cli_outputs_utf8_without_caller_flags(tmp_path: Path) -> None:
    started(tmp_path)
    atlas.edit_presentation(repo_root=tmp_path, report=report(tmp_path), kind="candidate", identifier="alpha-fix", title="Validation → 確認")
    env = {**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}
    result = subprocess.run([sys.executable, str(SCRIPT), "status", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                             "--candidate", "alpha-fix"], capture_output=True, env=env)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout.decode("utf-8"))["rows"][0]["display_title"] == "Validation → 確認"


def test_verify_cli_keeps_snapshots_in_report_and_propagates_failed_command(tmp_path: Path) -> None:
    started(tmp_path)
    result = subprocess.run([sys.executable, str(SCRIPT), "verify", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                             "--id", "failed-probe", "--target", "candidate:alpha-fix", "--environment", "fixture", "--",
                             sys.executable, "-c", "raise SystemExit(3)"], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 1 and not result.stderr
    summary = json.loads(result.stdout)
    assert not summary["passed"] and summary["check"]["exit_code"] == 3
    assert "fingerprints" not in result.stdout and summary["check"]["source_paths_total"] == 3
    receipt = state(tmp_path)["checks"][0]
    assert receipt["source_identity"]["fingerprints"] and (tmp_path / receipt["log"]["path"]).is_file()
