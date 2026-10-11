"""Prepared collaboration, append-only evidence, and verification provenance."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from test_astra_atlas import SCRIPT, analysis_manifest, atlas, candidate, elements, finding, publish, report, sha
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
