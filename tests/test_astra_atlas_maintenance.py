"""Resumed atlas runs preserve evidence while recording structural and work changes."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from copy import deepcopy
from html import escape
from pathlib import Path

import pytest

from test_astra_atlas import (
    SCRIPT, analysis_manifest, atlas, audit_manifest, elements, finding, identity,
    make_repo, map_manifest, publish, report, sha, write_json,
)


def started(root: Path, *, analyzed: bool = True) -> dict:
    make_repo(root)
    publish(root, "render-report", map_manifest(root))
    publish(root, "audit-subsystem", audit_manifest(root, report(root)))
    if analyzed:
        publish(root, "analyze-candidate", analysis_manifest(root, report(root)))
    return state(root)


def state(root: Path) -> dict:
    return atlas.inspect_report(repo_root=root, report=report(root), full=True)["state"]


def guarded(root: Path, **fields) -> dict:
    return {"version": atlas.MANIFEST_VERSION, "expected_report_sha256": sha(report(root)), **fields}


def reconcile(root: Path, **fields) -> dict:
    return publish(root, "reconcile-map", guarded(root, observation_identity=atlas.inventory(repo_root=root)["identity"], **fields))


def event(root: Path, identifier: str, kind: str, *, target_kind: str = "candidate", target_id: str = "alpha-fix", **fields) -> dict:
    value = {"id": identifier, "target": {"kind": target_kind, "id": target_id}, "type": kind,
             "summary": f"Observed {kind}", "evidence": ["Relevant checks exercised both callers."], **fields}
    if kind in {"implemented", "verified"}:
        value["source_identity"] = identity(root, ["src/a.py", "src/b.py", "tests/test_a.py"])
    return value


def outcomes(root: Path, *events: dict, **fields) -> dict:
    return publish(root, "record-outcome", guarded(root, events=list(events), **fields))


def candidate_work(root: Path) -> dict:
    rows = atlas.status_report(repo_root=root, report=report(root), candidate="alpha-fix")["rows"]
    return rows[0]["work"]


def test_new_and_deleted_tracked_paths_are_detected_without_invalidating_unrelated_evidence(tmp_path: Path) -> None:
    before = started(tmp_path)
    (tmp_path / "src/new.py").write_text("VALUE=3\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", "src/new.py"], cwd=tmp_path, check=True)
    live = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))
    assert live["map_drift"]["unowned_paths"] == ["src/new.py"]
    assert live["summary"]["current_audits"] == 1
    assert state(tmp_path) == before  # Live inspection never publishes observation changes.
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["ownership_current"] is False
    reconcile(tmp_path, ownership_changes=[{"path": "src/new.py", "owner": "alpha", "reason": "New validation entry."}])
    added = state(tmp_path)
    assert added["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert added["freshness"]["alpha"] == "changed"
    assert added["source_changes"]["alpha"]["scope_changed"] is True
    assert added["source_changes"]["alpha"]["changed_paths"] == ["src/new.py"]
    assert added["map_drift"]["needs_reconcile"] is False
    subprocess.run(["git", "rm", "--", "src/b.py"], cwd=tmp_path, check=True, capture_output=True)
    drift = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["map_drift"]
    assert drift["removed_paths"] == drift["missing_owned_paths"] == ["src/b.py"]
    reconcile(tmp_path, subsystems=[{"id": "alpha", "dependencies": []}],
              retirements=[{"id": "beta", "replacement_ids": [], "reason": "Delivery behavior removed."}])
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["ownership_current"] is True
    assert state(tmp_path)["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]


def test_reconciliation_moves_ownership_without_rewriting_audits_or_history(tmp_path: Path) -> None:
    before = started(tmp_path)
    reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Proof is maintained by delivery."}])
    after = state(tmp_path)
    assert after["history"][:-1] == before["history"]
    assert after["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert after["subsystems"][1]["owned_paths"] == ["src/b.py", "tests/test_a.py"]
    assert after["source_changes"]["alpha"]["changed_paths"] == ["tests/test_a.py"]
    assert after["candidate_freshness"]["alpha-fix"] == "changed"


@pytest.mark.parametrize("patch", [{"ownership": "Validation belongs to the write boundary."},
                                    {"authority": ["Reviewed write policy"]},
                                    {"dependencies": []}])
def test_structural_changes_preserve_evidence_but_invalidate_its_audit_baseline(tmp_path: Path, patch: dict) -> None:
    before = started(tmp_path)
    reconcile(tmp_path, subsystems=[{"id": "alpha", **patch}])
    after = state(tmp_path)
    assert after["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert after["subsystems"][0]["owned_paths"] == before["subsystems"][0]["owned_paths"]
    assert after["freshness"]["alpha"] == after["candidate_freshness"]["alpha-fix"] == "changed"
    observation = after["source_changes"]["alpha"]
    assert observation["changed_paths"] == []
    assert observation["structure_changes"] == {"alpha": sorted(patch)}
    assert after["freshness"]["beta"] == "fresh"
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["source_changes"]["audit"]["structure_changed"]
    assert "alpha: " + next(iter(patch)) + " changed" in report(tmp_path).read_text(encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "changed"
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    assert state(tmp_path)["freshness"]["alpha"] == "fresh"
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "fresh"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_affected_owner_metadata_changes_require_current_analysis_without_repeating_unaffected_audit(tmp_path: Path) -> None:
    before = started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "verified-1", "verified"))
    reconcile(tmp_path, subsystems=[{"id": "beta", "ownership": "Reviewed delivery ownership."}])
    after = state(tmp_path)
    assert after["freshness"]["alpha"] == "fresh"
    assert after["candidate_freshness"]["alpha-fix"] == "changed"
    assert after["candidate_source_changes"]["alpha-fix"]["scope"]["structure_changes"] == {"beta": ["ownership"]}
    assert candidate_work(tmp_path)["status"] == "verified"
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "fresh"
    assert state(tmp_path)["subsystems"][0]["audit"]["source_identity"] == before["subsystems"][0]["audit"]["source_identity"]


def test_restored_structure_and_display_renaming_reuse_the_unchanged_audit(tmp_path: Path) -> None:
    before = started(tmp_path)
    reconcile(tmp_path, subsystems=[{"id": "alpha", "ownership": "Changed policy owner."}])
    assert state(tmp_path)["freshness"]["alpha"] == "changed"
    reconcile(tmp_path, subsystems=[{"id": "alpha", "ownership": before["subsystems"][0]["ownership"], "name": "Validation"}])
    after = state(tmp_path)
    assert after["freshness"]["alpha"] == after["candidate_freshness"]["alpha-fix"] == "fresh"
    assert after["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]


def test_ownership_removed_from_an_affected_owner_changes_analysis_even_when_source_is_unchanged(tmp_path: Path) -> None:
    started(tmp_path)
    reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed proof owner."}])
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "fresh"
    gamma = deepcopy(map_manifest(tmp_path)["subsystems"][1])
    gamma.update(id="gamma", name="Proof owner", owned_paths=["tests/test_a.py"])
    reconcile(tmp_path, subsystems=[gamma], ownership_changes=[{"path": "tests/test_a.py", "owner": "gamma", "reason": "Reviewed proof boundary."}])
    after = state(tmp_path)
    assert after["freshness"]["alpha"] == "fresh"
    assert after["candidate_freshness"]["alpha-fix"] == "changed"
    assert after["candidate_source_changes"]["alpha-fix"]["scope"]["structure_changes"] == {"beta": ["owned_paths"]}
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_retired_owner_keeps_stable_ids_and_original_evidence_selectable(tmp_path: Path) -> None:
    before = started(tmp_path)
    replacement = deepcopy(map_manifest(tmp_path)["subsystems"][0])
    replacement.update(id="gamma", name="Validation owner")
    reconcile(tmp_path, subsystems=[replacement], retirements=[{"id": "alpha", "replacement_ids": ["gamma"], "reason": "New boundary."}])
    after = state(tmp_path)
    assert after["retired_subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert atlas._current_scope(after, ["alpha", "beta"]) == {"gamma", "beta"}
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=False, candidate="alpha-fix", history=True)
    assert selected["rows"][0]["historical"] is True
    assert selected["rows"][0]["record"]["analysis"] == before["subsystems"][0]["audit"]["candidates"][0]["analysis"]
    outcomes(tmp_path, event(tmp_path, "verified-after-retirement", "verified"))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"] is True
    old_bytes = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="cannot be reused"):
        reconcile(tmp_path, subsystems=[{"id": "alpha", "name": "Reused"}])
    assert report(tmp_path).read_bytes() == old_bytes


@pytest.mark.parametrize("bad", ["unowned", "unknown replacement", "cyclic retirement", "stale identity"])
def test_invalid_reconciliation_preserves_report(tmp_path: Path, bad: str) -> None:
    started(tmp_path)
    packet = guarded(tmp_path, observation_identity=atlas.inventory(repo_root=tmp_path)["identity"])
    if bad == "unowned":
        packet["subsystems"] = [{"id": "alpha", "owned_paths": []}]
    elif bad == "unknown replacement":
        packet["retirements"] = [{"id": "alpha", "replacement_ids": ["unknown"], "reason": "Move"}]
    elif bad == "cyclic retirement":
        packet["subsystems"] = [{"id": "beta", "owned_paths": ["src/a.py", "src/b.py", "tests/test_a.py"]}]
        packet["retirements"] = [{"id": "alpha", "replacement_ids": ["alpha"], "reason": "Cycle"}]
    else:
        packet["observation_identity"]["tracked_content_sha256"] = "0" * 64
    original = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError):
        publish(tmp_path, "reconcile-map", packet)
    assert report(tmp_path).read_bytes() == original


@pytest.mark.parametrize("excluded", [None, {}, [{}], ["not an object"],
                                     [{"path": 3, "reason": "Reviewed"}],
                                     [{"path": "src/a.py", "reason": ""}]])
@pytest.mark.parametrize("owner", ["beta", None])
def test_reconciliation_rejects_malformed_exclusions_before_ownership_changes(tmp_path: Path, excluded, owner) -> None:
    started(tmp_path, analyzed=False)
    packet = guarded(tmp_path, observation_identity=atlas.inventory(repo_root=tmp_path)["identity"],
                     excluded=excluded, ownership_changes=[{"path": "src/a.py", "owner": owner, "reason": "Reviewed move."}])
    original = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="excluded"):
        publish(tmp_path, "reconcile-map", packet)
    assert report(tmp_path).read_bytes() == original
    cli = subprocess.run([sys.executable, str(SCRIPT), "reconcile-map", "--repo-root", str(tmp_path),
                          "--report", str(report(tmp_path)), "--manifest", str(tmp_path / "reconcile-map.json")],
                         capture_output=True, text=True)
    assert cli.returncode == 2
    result = json.loads(cli.stdout)
    assert result["ok"] is False and result["stage"] == "validate" and "excluded" in result["error"]
    assert cli.stderr == ""
    assert report(tmp_path).read_bytes() == original


@pytest.mark.parametrize("field", ["outcome type", "target kind", "preview state"])
@pytest.mark.parametrize("invalid", [None, [], {}, 3, True, ""])
def test_maintenance_discriminators_return_structured_validation_errors(tmp_path: Path, field: str, invalid) -> None:
    started(tmp_path, analyzed=False)
    if field == "preview state":
        objective = "record-preview"
        packet = guarded(tmp_path, preview={"environment": "test", "capability": "HTML", "state": invalid,
                                           "reason": "Observed capability", "evidence": ["Checked host support"]})
    else:
        objective = "record-outcome"
        record = event(tmp_path, "deferred-1", "deferred")
        if field == "outcome type":
            record["type"] = invalid
        else:
            record["target"]["kind"] = invalid
        packet = guarded(tmp_path, events=[record])
    original = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match=field):
        publish(tmp_path, objective, packet)
    cli = subprocess.run([sys.executable, str(SCRIPT), objective, "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                          "--manifest", str(tmp_path / f"{objective}.json")], capture_output=True, text=True)
    assert cli.returncode == 2 and cli.stderr == ""
    response = json.loads(cli.stdout)
    assert response["ok"] is False and response["stage"] == "validate" and field in response["error"]
    assert report(tmp_path).read_bytes() == original


@pytest.mark.parametrize("owned_paths", [None, {}, "src/a.py", [3], ["../escape"]])
def test_reconciliation_validates_owned_paths_before_applying_changes(tmp_path: Path, owned_paths) -> None:
    started(tmp_path, analyzed=False)
    packet = guarded(tmp_path, observation_identity=atlas.inventory(repo_root=tmp_path)["identity"],
                     subsystems=[{"id": "alpha", "owned_paths": owned_paths}],
                     ownership_changes=[{"path": "src/a.py", "owner": "beta", "reason": "Reviewed move."}])
    original = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="owned"):
        publish(tmp_path, "reconcile-map", packet)
    cli = subprocess.run([sys.executable, str(SCRIPT), "reconcile-map", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                          "--manifest", str(tmp_path / "reconcile-map.json")], capture_output=True, text=True)
    assert cli.returncode == 2 and cli.stderr == ""
    response = json.loads(cli.stdout)
    assert response["ok"] is False and response["stage"] == "validate"
    assert report(tmp_path).read_bytes() == original


@pytest.mark.parametrize("work_status", ["implemented", "verification changed"])
@pytest.mark.parametrize("analysis_state", ["analyzed", "blocked"])
def test_fresh_analysis_with_pending_verification_selects_inspection(tmp_path: Path, work_status: str, analysis_state: str) -> None:
    started(tmp_path)
    if work_status == "implemented":
        outcomes(tmp_path, event(tmp_path, "implemented-1", "implemented"))
    else:
        outcomes(tmp_path, event(tmp_path, "verified-1", "verified"))
        (tmp_path / "src/a.py").write_text("VALUE=7\n", encoding="utf-8")
        publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    analysis = analysis_manifest(tmp_path, report(tmp_path))
    analysis.update(state=analysis_state, question="Which caller owns policy?" if analysis_state == "blocked" else "")
    publish(tmp_path, "analyze-candidate", analysis)
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "fresh"
    assert candidate_work(tmp_path)["status"] == work_status
    commands = {item["data-copy"] for item in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy")}
    assert "$audit-codebase inspect candidate alpha-fix in atlas run run-1" in commands
    assert "$audit-codebase analyze candidate alpha-fix in atlas run run-1" not in commands
    assert not any(command.startswith("Use ") for command in commands)
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_fix_verification_preserves_stale_analysis_and_tracks_delivery_separately(tmp_path: Path) -> None:
    before = started(tmp_path)
    (tmp_path / "src/a.py").write_text("VALUE=4\n", encoding="utf-8")
    target = {"kind": "candidate", "id": "alpha-fix"}
    outcomes(tmp_path, event(tmp_path, "implemented-1", "implemented"), event(tmp_path, "verified-1", "verified"),
             delivery_requirements=[{"target": target, "commit": True, "deployments": ["local"], "reason": "User requested commit and install."}])
    after = state(tmp_path)
    assert after["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert after["candidate_freshness"]["alpha-fix"] == "changed"
    work = candidate_work(tmp_path)
    assert work["status"] == "verified"
    assert work["commit_pending"] and work["deployment_pending"] == ["local"]
    outcomes(tmp_path, event(tmp_path, "committed-1", "committed", reference="a" * 40))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert candidate_work(tmp_path)["deployment_pending"] == ["local"]
    outcomes(tmp_path, event(tmp_path, "installed-1", "deployed", reference="a" * 40, destination="local"))
    assert candidate_work(tmp_path)["commit_pending"] is False
    assert not candidate_work(tmp_path)["deployment_pending"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), outstanding=True)["total"] == 0
    text = report(tmp_path).read_text(encoding="utf-8")
    assert elements(text, "id", "candidate-alpha-fix")[0]["data-work-status"] == "verified"
    assert not any(item["data-copy"].startswith("Use analyzed audit candidate") for item in elements(text, "data-copy"))
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    (tmp_path / "src/b.py").write_text("VALUE=5\n", encoding="utf-8")
    assert candidate_work(tmp_path)["status"] == "verification changed"


def test_committing_and_deferring_do_not_claim_verification_or_implicit_deployment(tmp_path: Path) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "committed-1", "committed", reference="b" * 40))
    work = candidate_work(tmp_path)
    assert work["status"] == "open"
    assert work["deployment_pending"] == []
    outcomes(tmp_path, event(tmp_path, "deferred-1", "deferred"))
    assert candidate_work(tmp_path)["status"] == "deferred"
    outcomes(tmp_path, event(tmp_path, "reopened-1", "reopened"))
    assert candidate_work(tmp_path)["status"] == "open"
    assert candidate_work(tmp_path)["commits"] == []


def test_outcomes_are_atomic_append_only_and_validate_target_source(tmp_path: Path) -> None:
    started(tmp_path)
    original = report(tmp_path).read_bytes()
    invalid = event(tmp_path, "verified-invalid", "verified")
    invalid["source_identity"] = identity(tmp_path, ["src/b.py"])
    with pytest.raises(atlas.ReportError, match="omits required"):
        outcomes(tmp_path, event(tmp_path, "deferred-valid", "deferred"), invalid)
    assert report(tmp_path).read_bytes() == original
    packet = write_json(tmp_path / "outcomes.json", guarded(tmp_path, events=[event(tmp_path, "verified-1", "verified")]))
    result = atlas.mutate_report(objective="record-outcome", repo_root=tmp_path, report=report(tmp_path), manifest=packet, validate_only=True)
    assert result["validated"] and not result["published"]
    assert report(tmp_path).read_bytes() == original
    outcomes(tmp_path, event(tmp_path, "verified-1", "verified"))
    saved = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="new and unique"):
        outcomes(tmp_path, event(tmp_path, "verified-1", "verified"))
    assert report(tmp_path).read_bytes() == saved
    with pytest.raises(atlas.ReportError, match="expected_report_sha256"):
        atlas.mutate_report(objective="record-outcome", repo_root=tmp_path, report=report(tmp_path), manifest=packet)
    assert report(tmp_path).read_bytes() == saved


def test_candidate_group_outcomes_do_not_resolve_later_added_findings(tmp_path: Path) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "verified-group", "verified"))
    audit = audit_manifest(tmp_path, report(tmp_path))
    added = finding()
    added.update(id="second-defect", title="Another unchecked entry")
    audit["findings"].append(added)
    audit["candidates"][0]["finding_ids"].append("second-defect")
    audit["lenses"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    assert candidate_work(tmp_path)["status"] == "verification changed"
    rows = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="second-defect")["rows"]
    assert rows[0]["work"]["status"] == "open"
    outcomes(tmp_path, event(tmp_path, "verified-second", "verified", target_kind="finding", target_id="second-defect"))
    # A direct group verification still refers to its original finding set.
    assert candidate_work(tmp_path)["status"] == "verification changed"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_candidate_group_implementation_does_not_implement_later_added_findings(tmp_path: Path) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "group-implemented", "implemented"))
    audit = audit_manifest(tmp_path, report(tmp_path))
    added = finding()
    added.update(id="second-defect", title="Another entry still needs work")
    audit["findings"].append(added)
    audit["candidates"][0]["finding_ids"].append("second-defect")
    audit["lenses"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    assert state(tmp_path)["outcomes"][0]["finding_ids"] == ["alpha-defect"]
    assert candidate_work(tmp_path)["status"] == "open"
    current = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="second-defect")["rows"][0]
    assert current["work"]["status"] == "open"
    html = report(tmp_path).read_text(encoding="utf-8")
    assert elements(html, "id", "candidate-alpha-fix")[0]["data-work-status"] == "open"
    outcomes(tmp_path, event(tmp_path, "second-implemented", "implemented", target_kind="finding", target_id="second-defect"))
    assert candidate_work(tmp_path)["status"] == "implemented"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_retired_systemic_findings_stay_historical_in_all_live_counts(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit.update(systemic_findings=audit["findings"], findings=[], candidates=[])
    publish(tmp_path, "audit-subsystem", audit)
    gamma = deepcopy(map_manifest(tmp_path)["subsystems"][0])
    gamma.update(id="gamma", name="Replacement validation")
    reconcile(tmp_path, subsystems=[gamma], retirements=[{"id": "alpha", "replacement_ids": ["gamma"], "reason": "Reviewed boundary."}])
    html = report(tmp_path).read_text(encoding="utf-8")
    beta = re.search(r'<article[^>]*id="subsystem-beta".*?</article>', html, re.S).group()
    assert "0 findings · 0 candidates" in beta
    assert '<strong>0</strong><span>Findings</span>' in html
    assert "systemic findings" not in atlas._architecture_svg(state(tmp_path))
    assert elements(html, "id", "finding-alpha-defect")
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["historical"]
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


@pytest.mark.parametrize("chained", [False, True])
def test_live_systemic_counts_resolve_retired_affected_owners(tmp_path: Path, chained: bool) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit.update(systemic_findings=audit["findings"], findings=[], candidates=[])
    publish(tmp_path, "audit-subsystem", audit)
    original = state(tmp_path)["systemic_findings"][0]
    prior = "beta"
    for sid in (["gamma", "delta"] if chained else ["gamma"]):
        replacement = deepcopy(map_manifest(tmp_path)["subsystems"][1])
        replacement.update(id=sid, name=f"Delivery {sid}")
        reconcile(tmp_path, subsystems=[replacement, {"id": "alpha", "dependencies": [{"id": sid, "evidence": ["Reviewed replacement."]}]}],
                  retirements=[{"id": prior, "replacement_ids": [sid], "reason": "Reviewed affected boundary."}])
        prior = sid
    current = state(tmp_path)
    assert current["systemic_findings"][0] == original
    html = report(tmp_path).read_text(encoding="utf-8")
    card = re.search(rf'<article[^>]*id="subsystem-{prior}".*?</article>', html, re.S).group()
    assert "1 findings · 0 candidates" in card
    node = re.search(rf'<a href="#subsystem-{prior}".*?</a>', atlas._architecture_svg(current), re.S).group()
    assert "1 systemic findings" in node
    assert '<strong>1</strong><span>Findings</span>' in html
    assert not atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]["historical"]
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


@pytest.mark.parametrize("event_kind", ["candidate", "finding"])
def test_outcome_cards_include_inherited_status_evidence_with_unique_anchors(tmp_path: Path, event_kind: str) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append("second-defect")
    audit["candidates"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    if event_kind == "candidate":
        events = [event(tmp_path, "group-verified", "verified", summary="Group proof covers both findings.")]
        inherited_targets = [{"kind": "finding", "id": fid} for fid in ("alpha-defect", "second-defect")]
    else:
        events = [event(tmp_path, f"{fid}-verified", "verified", target_kind="finding", target_id=fid,
                        summary=f"Current proof for {fid}.") for fid in ("alpha-defect", "second-defect")]
        inherited_targets = [{"kind": "candidate", "id": "alpha-fix"}]
    outcomes(tmp_path, *events, delivery_requirements=[
        {"target": target, "commit": True, "deployments": [], "reason": "User requested delivery."} for target in inherited_targets
    ])
    html = report(tmp_path).read_text(encoding="utf-8")
    for target in inherited_targets:
        identifier = f"work-{target['kind']}-{target['id']}"
        card = re.search(rf'<article[^>]*id="{identifier}".*?</article>', html, re.S).group()
        assert elements(card, "data-work-status", "verified")
        for recorded in events:
            assert recorded["summary"] in card and recorded["evidence"][0] in card
            assert elements(card, "href", f"#outcome-{recorded['id']}")
            assert recorded["source_identity"]["sha256"] in card
    for recorded in events:
        assert len(elements(html, "id", f"outcome-{recorded['id']}")) == 1
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_standalone_systemic_finding_scope_changes_are_visible_and_selectable(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit.update(systemic_findings=audit["findings"], findings=[], candidates=[])
    publish(tmp_path, "audit-subsystem", audit)
    reconcile(tmp_path, subsystems=[{"id": "beta", "ownership": "Reviewed delivery authority."}])
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    observed = state(tmp_path)
    assert observed["freshness"]["alpha"] == "fresh" and observed["candidate_freshness"] == {}
    html = report(tmp_path).read_text(encoding="utf-8")
    assert elements(html, "id", "finding-alpha-defect")[0]["data-freshness"] == "changed"
    assert "beta: ownership changed" in html
    assert elements(html, "href", "#finding-alpha-defect")
    assert elements(html, "data-copy", "$audit-codebase inspect finding alpha-defect in atlas run run-1")
    checked = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert checked["finding_freshness"]["alpha-defect"] == "changed"
    publish(tmp_path, "audit-subsystem", audit_manifest_without_work(tmp_path, systemic=True))
    assert elements(report(tmp_path).read_text(encoding="utf-8"), "id", "finding-alpha-defect")[0]["data-freshness"] == "fresh"


def audit_manifest_without_work(root: Path, *, systemic: bool = False, subsystem: str = "alpha") -> dict:
    audit = audit_manifest(root, report(root))
    audit.update(subsystem_id=subsystem, candidates=[])
    if systemic:
        audit.update(systemic_findings=audit["findings"], findings=[])
    else:
        audit.update(findings=[], systemic_findings=[])
        audit["lenses"][0]["finding_ids"] = []
    return audit


def test_changed_path_inspection_returns_audits_without_work_records(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    publish(tmp_path, "audit-subsystem", audit_manifest_without_work(tmp_path))
    saved = report(tmp_path).read_bytes()
    (tmp_path / "src/a.py").write_text("VALUE=8\n", encoding="utf-8")
    for inspect in (atlas.inspect_report, atlas.status_report):
        selected = inspect(repo_root=tmp_path, report=report(tmp_path), changed_paths=["src/a.py"], history=True)
        assert selected["rows"] == [] and selected["total"] == 0
        assert selected["subsystems_total"] == 1
        row = selected["subsystems"][0]
        assert row["subsystem_id"] == "alpha" and row["state"] == "audited"
        assert row["matching_paths"] == ["src/a.py"]
        assert row["source_changes"]["freshness"] == "changed"
        assert row["source_changes"]["changed_paths"] == ["src/a.py"]
        assert any(event["operation"] == "audit" and event["selection"] == "alpha" for event in selected["history"])
    for command in ("inspect", "status"):
        cli = subprocess.run([sys.executable, str(SCRIPT), command, "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                              "--changed-path", "src/a.py"], check=True, capture_output=True, text=True)
        assert json.loads(cli.stdout)["subsystems"][0]["source_changes"]["freshness"] == "changed"
    assert report(tmp_path).read_bytes() == saved


def test_matching_subsystem_observations_and_paths_are_bounded_and_paginated(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    for sid in ("alpha", "beta"):
        publish(tmp_path, "audit-subsystem", audit_manifest_without_work(tmp_path, subsystem=sid))
    (tmp_path / "src/a.py").write_text("VALUE=8\n", encoding="utf-8")
    first = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["src"], limit=1)
    assert first["subsystems_total"] == 2 and first["subsystems_has_more"]
    assert [row["subsystem_id"] for row in first["subsystems"]] == ["alpha"]
    assert first["subsystems"][0]["matching_paths"] == ["src/a.py"]
    assert first["subsystems"][0]["matching_paths_total"] == 2 and first["subsystems"][0]["matching_paths_has_more"]
    second = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["src"], limit=1, offset=1)
    assert [row["subsystem_id"] for row in second["subsystems"]] == ["beta"]
    assert second["subsystems_has_more"] is False


def test_individual_findings_can_resolve_candidate_without_rewriting_analysis(tmp_path: Path) -> None:
    started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["candidates"][0]["finding_ids"].append("second-defect")
    audit["lenses"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    outcomes(tmp_path, event(tmp_path, "verified-first", "verified", target_kind="finding", target_id="alpha-defect"))
    assert candidate_work(tmp_path)["status"] == "open"
    outcomes(tmp_path, event(tmp_path, "verified-second", "verified", target_kind="finding", target_id="second-defect"))
    assert candidate_work(tmp_path)["status"] == "verified"
    outcomes(tmp_path, event(tmp_path, "implemented-again", "implemented"))
    assert candidate_work(tmp_path)["status"] == "implemented"


def test_removed_active_candidate_can_receive_outcomes_and_filtered_history(tmp_path: Path) -> None:
    before = started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit.update(findings=[], candidates=[])
    for lens in audit["lenses"]:
        lens["finding_ids"] = []
    publish(tmp_path, "audit-subsystem", audit)
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=False, candidate="alpha-fix", history=True)
    assert selected["rows"][0]["record"] == before["subsystems"][0]["audit"]["candidates"][0]
    assert selected["rows"][0]["historical"] is True
    assert any(item.get("candidate_revision") for item in selected["history"])
    outcomes(tmp_path, event(tmp_path, "historical-verified", "verified"))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    text = report(tmp_path).read_text(encoding="utf-8")
    assert any(button["data-copy"] == "$audit-codebase inspect candidate alpha-fix in atlas run run-1" for button in elements(text, "data-copy"))
    assert any(button["data-copy"] == "$audit-codebase inspect finding alpha-defect in atlas run run-1" for button in elements(text, "data-copy"))


def test_compact_inspection_is_readonly_bounded_and_filters_external_evidence(tmp_path: Path) -> None:
    started(tmp_path)
    (tmp_path / "analysis-context.txt").write_text("Constraint", encoding="utf-8")
    analysis = analysis_manifest(tmp_path, report(tmp_path))
    analysis["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", "analysis-context.txt"])
    publish(tmp_path, "analyze-candidate", analysis)
    original = report(tmp_path).read_bytes()
    (tmp_path / "analysis-context.txt").write_text("Changed constraint", encoding="utf-8")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=False, candidate="alpha-fix")
    assert selected["rows"][0]["source_changes"]["analysis"]["changed_paths"] == ["analysis-context.txt"]
    assert selected["rows"][0]["record"]["analysis"]["source_identity"]["fingerprints"]
    filtered = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["analysis-context.txt"])
    assert [row["target"]["id"] for row in filtered["rows"]] == ["alpha-fix"]
    page = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), limit=1)
    assert len(page["rows"]) == 1 and page["has_more"] and page["total"] == 2
    assert "record" not in page["rows"][0]
    assert "state" not in page
    assert report(tmp_path).read_bytes() == original
    full = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=True)
    assert full["response_version"] == page["response_version"] == selected["response_version"] == 2
    assert "state" in full
    assert len(json.dumps(page)) < len(json.dumps(full))
    assert "state" not in atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))
    for arguments, has_state in ((["--limit", "1"], False), (["--full"], True)):
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)), *arguments], check=True, capture_output=True, text=True)
        response = json.loads(result.stdout)
        assert response["response_version"] == 2
        assert ("state" in response) is has_state


def test_per_path_identity_rejects_forged_or_missing_fingerprints(tmp_path: Path) -> None:
    started(tmp_path)
    packet = atlas.source_identity(repo_root=tmp_path, paths=["src/a.py", "src/b.py"])
    bound = {key: packet[key] for key in ("paths", "sha256", "fingerprints")}
    forged = deepcopy(bound)
    forged["fingerprints"]["src/a.py"] = "0" * 64
    with pytest.raises(atlas.ReportError, match="fingerprints"):
        atlas._verify_source_packet(tmp_path, forged, [])
    (tmp_path / "src/a.py").write_text("changed", encoding="utf-8")
    assert atlas._packet_observation(tmp_path, bound)["changed_paths"] == ["src/a.py"]
    with pytest.raises(atlas.ReportError, match="fingerprints"):
        atlas._source_packet({key: bound[key] for key in ("paths", "sha256")}, "incomplete source")


def test_check_report_distinguishes_static_checks_from_visual_and_catches_renderer_errors(tmp_path: Path, monkeypatch) -> None:
    started(tmp_path)
    checked = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert all(checked["checks"].values())
    assert checked["visual_verification"]["performed_by_check_report"] is False
    original_render = atlas._render
    monkeypatch.setattr(atlas, "_render", lambda value: original_render(value).replace(b'</main>', b'<a id="map" href="#unknown">Broken</a></main>'))
    report(tmp_path).write_bytes(atlas._render(state_from_bytes(report(tmp_path).read_bytes())))
    with pytest.raises(atlas.ReportError, match="duplicate ids or unresolved anchors"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


def test_check_report_exposes_analysis_and_verification_changes_without_changing_the_report(tmp_path: Path) -> None:
    started(tmp_path)
    (tmp_path / "analysis-input.txt").write_text("Original constraint", encoding="utf-8")
    (tmp_path / "verification-input.txt").write_text("Passing proof input", encoding="utf-8")
    paths = ["src/a.py", "src/b.py", "tests/test_a.py"]
    analysis = analysis_manifest(tmp_path, report(tmp_path))
    analysis["source_identity"] = identity(tmp_path, paths + ["analysis-input.txt"])
    publish(tmp_path, "analyze-candidate", analysis)
    verified = event(tmp_path, "verified-extra", "verified")
    verified["source_identity"] = identity(tmp_path, paths + ["verification-input.txt"])
    outcomes(tmp_path, verified)
    fresh = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert fresh["candidate_freshness"] == {"alpha-fix": "fresh"}
    assert fresh["outcome_freshness"] == {"verified-extra": "fresh"}
    assert fresh["finding_freshness"] == {"alpha-defect": "fresh"}
    assert all(fresh[name] == {} for name in ("source_changes", "candidate_source_changes", "outcome_source_changes", "finding_source_changes"))
    saved = report(tmp_path).read_bytes()
    (tmp_path / "analysis-input.txt").write_text("Changed constraint", encoding="utf-8")
    (tmp_path / "verification-input.txt").write_text("Changed proof input", encoding="utf-8")
    changed = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert changed["valid"] and changed["freshness"] == {"alpha": "fresh", "beta": "fresh"}
    assert changed["candidate_freshness"] == {"alpha-fix": "changed"}
    assert changed["outcome_freshness"] == {"verified-extra": "changed"}
    assert changed["candidate_source_changes"]["alpha-fix"]["analysis"]["changed_paths"] == ["analysis-input.txt"]
    assert changed["outcome_source_changes"]["verified-extra"]["changed_paths"] == ["verification-input.txt"]
    assert changed["finding_freshness"] == {"alpha-defect": "fresh"}
    cli = subprocess.run([sys.executable, str(SCRIPT), "check-report", "--repo-root", str(tmp_path), "--report", str(report(tmp_path))],
                         check=True, capture_output=True, text=True)
    response = json.loads(cli.stdout)
    assert response["candidate_source_changes"] == changed["candidate_source_changes"]
    assert response["outcome_source_changes"] == changed["outcome_source_changes"]
    assert report(tmp_path).read_bytes() == saved


@pytest.mark.parametrize("historical", [False, True])
@pytest.mark.parametrize("systemic", [False, True])
def test_finding_scope_observes_affected_owner_structure_at_its_original_audit(tmp_path: Path, historical: bool, systemic: bool) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    audit = audit_manifest(tmp_path, report(tmp_path))
    if systemic:
        audit["systemic_findings"], audit["findings"] = audit["findings"], []
    publish(tmp_path, "audit-subsystem", audit)
    before = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    reconcile(tmp_path, subsystems=[{"id": "beta", "ownership": "Reviewed delivery authority."}])
    if historical:
        renewed = audit_manifest(tmp_path, report(tmp_path))
        renewed.update(findings=[], candidates=[], systemic_findings=[])
        renewed["lenses"][0]["finding_ids"] = []
        publish(tmp_path, "audit-subsystem", renewed)
    saved = report(tmp_path).read_bytes()
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["historical"] is historical
    assert selected["record"] == before["record"]
    assert selected["audit_source_identity"] == before["audit_source_identity"]
    assert selected["source_changes"]["audit"]["freshness"] == "fresh"
    assert selected["source_changes"]["scope"]["freshness"] == "changed"
    assert selected["source_changes"]["scope"]["structure_changes"] == {"beta": ["ownership"]}
    checked = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert checked["finding_freshness"] == {"alpha-defect": "changed"}
    assert checked["finding_source_changes"]["alpha-defect"] == selected["source_changes"]
    cli = subprocess.run([sys.executable, str(SCRIPT), "inspect", "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                          "--finding", "alpha-defect"], check=True, capture_output=True, text=True)
    assert json.loads(cli.stdout)["rows"][0]["source_changes"] == selected["source_changes"]
    assert report(tmp_path).read_bytes() == saved


def test_historical_candidate_observes_structure_from_its_original_analysis(tmp_path: Path) -> None:
    started(tmp_path)
    original = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["record"]
    reconcile(tmp_path, subsystems=[{"id": "beta", "ownership": "Reviewed delivery authority."}])
    renewed = audit_manifest(tmp_path, report(tmp_path))
    renewed.update(findings=[], candidates=[])
    renewed["lenses"][0]["finding_ids"] = []
    publish(tmp_path, "audit-subsystem", renewed)
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]
    assert selected["historical"] and selected["record"] == original
    assert selected["source_changes"]["analysis"]["freshness"] == "changed"
    assert selected["source_changes"]["analysis"]["structure_changes"] == {"beta": ["ownership"]}
    checked = atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
    assert checked["candidate_freshness"] == {"alpha-fix": "changed"}
    assert checked["candidate_source_changes"]["alpha-fix"] == selected["source_changes"]
    outcomes(tmp_path, delivery_requirements=[{"target": {"kind": "candidate", "id": "alpha-fix"}, "commit": True,
                                               "deployments": [], "reason": "Requested delivery remains pending."}])
    for filters in ({"subsystem": "beta"}, {"outstanding": True}, {"history": True}):
        rows = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), **filters)["rows"]
        candidate_row = next(row for row in rows if row["target"] == {"kind": "candidate", "id": "alpha-fix"})
        assert candidate_row["source_changes"] == selected["source_changes"]


@pytest.mark.parametrize("scenario", ["all", "audit", "presented", "analyzed", "blocked", "changed", "verified", "deferred",
                                      "disproved", "historical candidate", "historical finding"])
def test_check_report_requires_selections_for_the_saved_state(tmp_path: Path, monkeypatch, scenario: str) -> None:
    started(tmp_path, analyzed=scenario != "presented")
    if scenario in {"blocked", "disproved"}:
        analysis = analysis_manifest(tmp_path, report(tmp_path))
        analysis.update(state=scenario, question="Which caller owns validation?" if scenario == "blocked" else "")
        publish(tmp_path, "analyze-candidate", analysis)
    elif scenario == "changed":
        (tmp_path / "src/a.py").write_text("VALUE=8\n", encoding="utf-8")
        atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    elif scenario in {"verified", "deferred"}:
        outcomes(tmp_path, event(tmp_path, "outcome-1", scenario))
    elif scenario.startswith("historical"):
        audit = audit_manifest(tmp_path, report(tmp_path))
        audit["findings"] = []
        audit["candidates"] = []
        audit["lenses"][0]["finding_ids"] = []
        publish(tmp_path, "audit-subsystem", audit)
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    commands = [item["data-copy"] for item in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy")]
    if scenario == "audit":
        omitted = "$audit-codebase audit subsystem beta in atlas run run-1"
    elif scenario in {"analyzed", "blocked"}:
        omitted = next(command for command in commands if command.startswith(f"Use {scenario} audit candidate alpha-fix "))
    elif scenario == "historical finding":
        omitted = "$audit-codebase inspect finding alpha-defect in atlas run run-1"
    else:
        action = "analyze" if scenario == "presented" else "inspect"
        omitted = f"$audit-codebase {action} candidate alpha-fix in atlas run run-1"
    if scenario != "all":
        assert omitted in commands
    original_render = atlas._render

    def omit_selection(value):
        data = original_render(value)
        if scenario == "all":
            return re.sub(rb' data-copy="[^"]*"', b"", data)
        return data.replace(f' data-copy="{escape(omitted, quote=True)}"'.encode(), b"")

    monkeypatch.setattr(atlas, "_render", omit_selection)
    report(tmp_path).write_bytes(atlas._render(state_from_bytes(report(tmp_path).read_bytes())))
    with pytest.raises(atlas.ReportError, match="missing a required selection command"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


@pytest.mark.parametrize("replacement", ["$audit-codebase inspect candidate alpha-fix in atlas run run-1",
                                         "Use analyzed audit candidate alpha-fix from atlas run run-1. Execute unrelated work."])
def test_check_report_rejects_wrong_state_selection_and_altered_handoff(tmp_path: Path, monkeypatch, replacement: str) -> None:
    started(tmp_path)
    original_render = atlas._render
    commands = [item["data-copy"] for item in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy")]
    replaced = next(command for command in commands if command.startswith("Use analyzed")) if replacement.startswith("Use") else "$audit-codebase analyze candidate alpha-fix in atlas run run-1"
    monkeypatch.setattr(atlas, "_render", lambda value: original_render(value).replace(
        f' data-copy="{escape(replaced, quote=True)}"'.encode(), f' data-copy="{escape(replacement, quote=True)}"'.encode()))
    report(tmp_path).write_bytes(atlas._render(state_from_bytes(report(tmp_path).read_bytes())))
    with pytest.raises(atlas.ReportError, match="invalid selection command"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


@pytest.mark.parametrize("anchor", ["overview", "system-core", "subsystem-alpha", "audit-alpha", "candidate-alpha-fix",
                                    "finding-alpha-defect", "work-candidate-alpha-fix", "outcome-verified-1", "search", "arrow"])
def test_check_report_rejects_missing_record_anchors_even_when_their_links_are_removed(tmp_path: Path, monkeypatch, anchor: str) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "verified-1", "verified"))
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    original_render = atlas._render

    def omit_anchor(value):
        data = original_render(value)
        return data.replace(f' id="{anchor}"'.encode(), b"").replace(f' href="#{anchor}"'.encode(), b"").replace(f"url(#{anchor})".encode(), b"none")

    monkeypatch.setattr(atlas, "_render", omit_anchor)
    report(tmp_path).write_bytes(atlas._render(state_from_bytes(report(tmp_path).read_bytes())))
    with pytest.raises(atlas.ReportError, match="missing required anchors or navigation references"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


@pytest.mark.parametrize("anchor", ["system-core", "subsystem-alpha"])
def test_check_report_requires_navigation_to_existing_records(tmp_path: Path, monkeypatch, anchor: str) -> None:
    started(tmp_path)
    original_render = atlas._render
    monkeypatch.setattr(atlas, "_render", lambda value: original_render(value).replace(f' href="#{anchor}"'.encode(), b""))
    report(tmp_path).write_bytes(atlas._render(state_from_bytes(report(tmp_path).read_bytes())))
    with pytest.raises(atlas.ReportError, match="missing required anchors or navigation references"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))


def state_from_bytes(data: bytes) -> dict:
    from html import unescape
    encoded = atlas._STATE.findall(data.decode("utf-8"))[0][1]
    return json.loads(unescape(encoded))


@pytest.mark.parametrize("preview_state", ["verified", " verified "])
def test_preview_limitation_is_once_per_capability_and_visual_proof_is_revision_bound(tmp_path: Path, preview_state: str) -> None:
    started(tmp_path)
    preview = {"environment": "Windows desktop", "capability": "HTML preview v1", "state": "unavailable",
               "reason": "Preview surface unavailable", "evidence": ["Host reported no preview capability."]}
    publish(tmp_path, "record-preview", guarded(tmp_path, preview=preview))
    original = report(tmp_path).read_bytes()
    repeated = publish(tmp_path, "record-preview", guarded(tmp_path, preview=preview))
    assert repeated["unchanged"] and not repeated["published"]
    assert report(tmp_path).read_bytes() == original
    updated = dict(preview, capability="HTML preview v2", state=preview_state, reason="Inspected map, filters, navigation, and labels.", report_sha256=sha(report(tmp_path)))
    publish(tmp_path, "record-preview", guarded(tmp_path, preview=updated))
    after = state(tmp_path)
    assert len(after["preview"]) == 2
    assert after["preview"][1]["state"] == "verified"
    assert after["preview"][1]["report_sha256"] != sha(report(tmp_path))  # It names the viewed revision before recording metadata.
    with pytest.raises(atlas.ReportError, match="current report revision"):
        publish(tmp_path, "record-preview", guarded(tmp_path, preview=updated))
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["visual_verification"]["performed_by_check_report"] is False


@pytest.mark.parametrize("old_version", [1, 2, 3])
def test_only_current_report_format_is_accepted(tmp_path: Path, old_version: int) -> None:
    started(tmp_path)
    data = report(tmp_path).read_bytes()
    current = f'name="audit-codebase-report-version" content="{atlas.REPORT_VERSION}"'.encode()
    old = f'name="audit-codebase-report-version" content="{old_version}"'.encode()
    report(tmp_path).write_bytes(data.replace(current, old))
    with pytest.raises(atlas.ReportError, match="create a new current-format map"):
        atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))


def test_finding_delivery_counts_and_duplicate_structural_changes(tmp_path: Path) -> None:
    started(tmp_path)
    target = {"kind": "finding", "id": "alpha-defect"}
    outcomes(tmp_path, event(tmp_path, "finding-verified", "verified", target_kind="finding", target_id="alpha-defect"),
             delivery_requirements=[{"target": target, "commit": True, "deployments": [], "reason": "User requested commit."}])
    summary = atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["summary"]
    assert summary["delivery_pending"] == 1
    assert summary["verified_findings"] == 1
    previous = report(tmp_path).read_bytes()
    change = {"path": "src/a.py", "owner": "alpha", "reason": "Reviewed owner."}
    with pytest.raises(atlas.ReportError, match="repeat a path"):
        reconcile(tmp_path, ownership_changes=[change, change])
    with pytest.raises(atlas.ReportError, match="repeat an id"):
        reconcile(tmp_path, subsystems=[{"id": "alpha"}, {"id": "alpha"}])
    assert report(tmp_path).read_bytes() == previous


@pytest.mark.parametrize("renewal", ["reopened", "implemented"])
def test_reopening_one_finding_invalidates_group_completion_and_delivery(tmp_path: Path, renewal: str) -> None:
    started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append("second-defect")
    audit["candidates"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    target = {"kind": "candidate", "id": "alpha-fix"}
    outcomes(tmp_path, event(tmp_path, "group-verified", "verified"),
             event(tmp_path, "group-committed", "committed", reference="a" * 40),
             event(tmp_path, "group-deployed", "deployed", reference="a" * 40, destination="local"),
             delivery_requirements=[{"target": target, "commit": True, "deployments": ["local"], "reason": "Requested delivery."}])
    outcomes(tmp_path, event(tmp_path, "finding-renewed", renewal, target_kind="finding", target_id="alpha-defect"))
    work = candidate_work(tmp_path)
    assert work["status"] == ("open" if renewal == "reopened" else "implemented")
    assert work["commits"] == work["deployments"] == []
    assert work["commit_pending"] and work["deployment_pending"] == ["local"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", outstanding=True)["total"] == 1
    # The unaffected finding's passing proof remains useful after its sibling reopens.
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), finding="second-defect")["rows"][0]["work"]["status"] == "verified"
    outcomes(tmp_path, event(tmp_path, "finding-reverified", "verified", target_kind="finding", target_id="alpha-defect"))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert candidate_work(tmp_path)["commit_pending"]
    outcomes(tmp_path, event(tmp_path, "group-recommitted", "committed", reference="b" * 40),
             event(tmp_path, "group-redeployed", "deployed", reference="b" * 40, destination="local"))
    assert not candidate_work(tmp_path)["commit_pending"] and not candidate_work(tmp_path)["deployment_pending"]


@pytest.mark.parametrize("replace_owner", [False, True])
def test_affected_ownership_additions_change_analysis_and_verification(tmp_path: Path, replace_owner: bool) -> None:
    before = started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "group-verified", "verified"))
    (tmp_path / "src/new.py").write_text("VALUE=3\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", "src/new.py"], cwd=tmp_path, check=True)
    fields = {}
    owner = "beta"
    if replace_owner:
        replacement = deepcopy(map_manifest(tmp_path)["subsystems"][1])
        replacement.update(id="gamma", name="New delivery owner")
        owner = "gamma"
        fields = {"subsystems": [replacement, {"id": "alpha", "dependencies": [{"id": "gamma", "evidence": ["Reviewed replacement."]}]}],
                  "retirements": [{"id": "beta", "replacement_ids": ["gamma"], "reason": "Reviewed new boundary."}]}
    reconcile(tmp_path, ownership_changes=[{"path": "src/new.py", "owner": owner, "reason": "New delivery entry."}], **fields)
    current = state(tmp_path)
    assert current["candidate_freshness"]["alpha-fix"] == "changed"
    assert current["candidate_source_changes"]["alpha-fix"]["analysis"]["changed_paths"] == ["src/new.py"]
    assert current["outcome_source_changes"]["group-verified"]["changed_paths"] == ["src/new.py"]
    assert current["outcome_freshness"]["group-verified"] == "changed"
    assert candidate_work(tmp_path)["status"] == "verification changed"
    assert not current["map_drift"]["needs_reconcile"]
    assert current["subsystems"][0]["audit"] == before["subsystems"][0]["audit"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["src/new.py"], candidate="alpha-fix")["total"] == 1
    for target_kind, identifier in (("candidate", "alpha-fix"), ("finding", "alpha-defect")):
        selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["src/new.py"], **{target_kind: identifier})["rows"][0]
        assert selected["outcome_source_changes"]["group-verified"]["changed_paths"] == ["src/new.py"]
        assert selected["outcome_observations_total"] == 1
    new_proof = event(tmp_path, "group-reverified", "verified")
    new_proof["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "src/new.py", "tests/test_a.py"])
    outcomes(tmp_path, new_proof)
    assert candidate_work(tmp_path)["status"] == "verified"
    assert state(tmp_path)["candidate_freshness"]["alpha-fix"] == "changed"


def test_filtered_inspection_reports_outcome_only_proof_deltas(tmp_path: Path) -> None:
    started(tmp_path)
    (tmp_path / "proof.txt").write_text("proof v1", encoding="utf-8")
    observed = event(tmp_path, "group-verified", "verified")
    observed["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", "proof.txt"])
    outcomes(tmp_path, observed)
    saved = report(tmp_path).read_bytes()
    (tmp_path / "proof.txt").write_text("proof v2", encoding="utf-8")
    rows = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["proof.txt"])["rows"]
    assert {row["target"]["id"] for row in rows} == {"alpha-fix", "alpha-defect"}
    for row in rows:
        assert row["work"]["status"] == "verification changed"
        assert row["outcome_source_changes"]["group-verified"]["changed_paths"] == ["proof.txt"]
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]
    assert selected["outcome_source_changes"]["group-verified"]["freshness"] == "changed"
    assert selected["outcomes"][0]["source_identity"] == state_from_bytes(saved)["outcomes"][0]["source_identity"]
    assert report(tmp_path).read_bytes() == saved
    # Later records do not hide the path-matched proof observation from a bounded query.
    for index in range(3):
        outcomes(tmp_path, event(tmp_path, f"delivery-{index}", "committed", reference=str(index) * 40))
    limited = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", changed_paths=["proof.txt"], limit=1)["rows"][0]
    assert len(limited["outcomes"]) == 1 and limited["outcomes_has_more"]
    assert limited["outcome_source_changes"]["group-verified"]["changed_paths"] == ["proof.txt"]


@pytest.mark.parametrize("boundary", ["replacement", "split", "merge"])
def test_retired_systemic_findings_have_one_historical_anchor(tmp_path: Path, boundary: str) -> None:
    started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["systemic_findings"], audit["findings"] = audit["findings"], []
    publish(tmp_path, "audit-subsystem", audit)
    before = state(tmp_path)
    first = deepcopy(map_manifest(tmp_path)["subsystems"][0])
    first.update(id="gamma", name="Validation replacement")
    replacements = ["gamma"]
    patches = [first]
    if boundary == "split":
        second = deepcopy(first)
        first["owned_paths"] = ["src/a.py"]
        second.update(id="proof", name="Validation proof", owned_paths=["tests/test_a.py"])
        patches.append(second)
        replacements.append("proof")
    elif boundary == "merge":
        first.update(owned_paths=["src/a.py", "src/b.py", "tests/test_a.py"], dependencies=[])
    retirements = [{"id": "alpha", "replacement_ids": replacements, "reason": "Reviewed boundary."}]
    if boundary == "merge":
        retirements.append({"id": "beta", "replacement_ids": ["gamma"], "reason": "Reviewed merge."})
    reconcile(tmp_path, subsystems=patches, retirements=retirements)
    current = state(tmp_path)
    assert current["systemic_findings"] == before["systemic_findings"]
    text = report(tmp_path).read_text(encoding="utf-8")
    assert len(elements(text, "id", "finding-alpha-defect")) == 1
    assert any(button["data-copy"] == "$audit-codebase inspect finding alpha-defect in atlas run run-1" for button in elements(text, "data-copy"))
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["historical"] and selected["record"] == before["systemic_findings"][0]


@pytest.mark.parametrize("outcome_type", ["implemented", "verified"])
def test_outcomes_bind_scope_added_by_analysis(tmp_path: Path, outcome_type: str) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = audit["findings"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    previous = report(tmp_path).read_bytes()
    incomplete = event(tmp_path, "narrow-outcome", outcome_type)
    incomplete["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    with pytest.raises(atlas.ReportError, match="omits required bound source"):
        outcomes(tmp_path, incomplete)
    assert report(tmp_path).read_bytes() == previous
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), subsystem="beta")["total"] == 1
    outcomes(tmp_path, event(tmp_path, "complete-outcome", outcome_type))
    (tmp_path / "src/b.py").write_text("VALUE=9\n", encoding="utf-8")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]
    assert selected["outcome_source_changes"]["complete-outcome"]["changed_paths"] == ["src/b.py"]
    if outcome_type == "verified":
        assert selected["work"]["status"] == "verification changed"


def test_indirect_group_verification_cannot_omit_expanded_analysis_scope(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = audit["findings"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    narrow = event(tmp_path, "finding-verified", "verified", target_kind="finding", target_id="alpha-defect")
    narrow["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    outcomes(tmp_path, narrow)
    assert candidate_work(tmp_path)["status"] == "verification changed"
    outcomes(tmp_path, event(tmp_path, "group-verified", "verified"))
    assert candidate_work(tmp_path)["status"] == "verified"


def test_fresh_finding_proof_supersedes_stale_group_proof_without_reimplementation(tmp_path: Path) -> None:
    started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append("second-defect")
    audit["candidates"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    outcomes(tmp_path, event(tmp_path, "group-verified", "verified"))
    saved = state(tmp_path)["outcomes"][0]
    (tmp_path / "src/a.py").write_text("VALUE=9\n", encoding="utf-8")
    outcomes(tmp_path, event(tmp_path, "first-reverified", "verified", target_kind="finding", target_id="alpha-defect"))
    assert candidate_work(tmp_path)["status"] == "verification changed"
    outcomes(tmp_path, event(tmp_path, "second-reverified", "verified", target_kind="finding", target_id="second-defect"))
    assert candidate_work(tmp_path)["status"] == "verified"
    current = state(tmp_path)
    assert current["outcomes"][0] == saved
    assert current["outcome_freshness"]["group-verified"] == "changed"
    assert current["outcome_freshness"]["first-reverified"] == current["outcome_freshness"]["second-reverified"] == "fresh"
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", outstanding=True)["total"] == 0


@pytest.mark.parametrize("renewal", ["implemented", "reopened"])
def test_finding_proof_completes_candidate_after_group_renewal(tmp_path: Path, renewal: str) -> None:
    started(tmp_path)
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append("second-defect")
    audit["candidates"][0]["finding_ids"].append("second-defect")
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    original_analysis = state(tmp_path)["subsystems"][0]["audit"]["candidates"][0]["analysis"]
    outcomes(tmp_path, event(tmp_path, "previous-verification", "verified"))
    outcomes(tmp_path, event(tmp_path, "group-renewed", renewal))
    pending = "implemented" if renewal == "implemented" else "open"
    assert candidate_work(tmp_path)["status"] == pending
    outcomes(tmp_path, event(tmp_path, "first-verified", "verified", target_kind="finding", target_id="alpha-defect"))
    assert candidate_work(tmp_path)["status"] == pending
    outcomes(tmp_path, event(tmp_path, "second-verified", "verified", target_kind="finding", target_id="second-defect"))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["summary"]["verified_candidates"] == 1
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), outstanding=True)["total"] == 0
    assert elements(report(tmp_path).read_text(encoding="utf-8"), "id", "candidate-alpha-fix")[0]["data-work-status"] == "verified"
    # A new group implementation invalidates all earlier finding proof.
    outcomes(tmp_path, event(tmp_path, "group-implemented-again", "implemented"))
    assert candidate_work(tmp_path)["status"] == "implemented"
    outcomes(tmp_path, event(tmp_path, "first-reverified", "verified", target_kind="finding", target_id="alpha-defect"))
    assert candidate_work(tmp_path)["status"] == "implemented"
    outcomes(tmp_path, event(tmp_path, "second-reverified", "verified", target_kind="finding", target_id="second-defect"))
    assert candidate_work(tmp_path)["status"] == "verified"
    assert state(tmp_path)["subsystems"][0]["audit"]["candidates"][0]["analysis"] == original_analysis
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


@pytest.mark.parametrize("transition", ["retirement", "audit replacement"])
@pytest.mark.parametrize("pending", ["delivery", "implemented", "reopened"])
def test_outstanding_inspection_keeps_unfinished_historical_targets(tmp_path: Path, transition: str, pending: str) -> None:
    started(tmp_path)
    targets = [{"kind": "candidate", "id": "alpha-fix"}, {"kind": "finding", "id": "alpha-defect"}]
    if pending == "delivery":
        outcomes(tmp_path, event(tmp_path, "verified", "verified"), delivery_requirements=[
            {"target": target, "commit": True, "deployments": ["local"], "reason": "User requested delivery."}
            for target in targets
        ])
    else:
        outcomes(tmp_path, event(tmp_path, "work-pending", pending))
    if transition == "retirement":
        replacement = deepcopy(map_manifest(tmp_path)["subsystems"][0])
        replacement.update(id="gamma", name="Validation replacement")
        reconcile(tmp_path, subsystems=[replacement], retirements=[
            {"id": "alpha", "replacement_ids": ["gamma"], "reason": "Reviewed new owner."}
        ])
    else:
        audit = audit_manifest(tmp_path, report(tmp_path))
        audit.update(findings=[], candidates=[])
        for lens in audit["lenses"]:
            lens["finding_ids"] = []
        publish(tmp_path, "audit-subsystem", audit)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path))["total"] == 0
    outstanding = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), outstanding=True)
    assert outstanding["total"] == 2
    assert [row["target"] for row in outstanding["rows"]] == targets
    assert all(row["historical"] for row in outstanding["rows"])
    assert outstanding["summary"]["outstanding_candidates"] == outstanding["summary"]["outstanding_findings"] == 1
    if pending == "delivery":
        assert outstanding["summary"]["delivery_pending"] == 2
        assert all(row["work"]["commit_pending"] and row["work"]["deployment_pending"] == ["local"] for row in outstanding["rows"])
        outcomes(tmp_path, event(tmp_path, "committed", "committed", reference="a" * 40),
                 event(tmp_path, "deployed", "deployed", reference="a" * 40, destination="local"))
    else:
        outcomes(tmp_path, event(tmp_path, "verified", "verified"))
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), outstanding=True)["total"] == 0
    history = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), history=True)
    assert history["total"] == 2 and all(row["historical"] for row in history["rows"])
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


@pytest.mark.parametrize("outcome_type", ["implemented", "verified"])
def test_group_source_covers_every_bound_findings_scope(tmp_path: Path, outcome_type: str) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    saved = report(tmp_path).read_bytes()
    narrow = event(tmp_path, "narrow-group", outcome_type)
    narrow["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    with pytest.raises(atlas.ReportError, match="omits required bound source"):
        outcomes(tmp_path, narrow)
    assert report(tmp_path).read_bytes() == saved
    outcomes(tmp_path, event(tmp_path, "complete-group", outcome_type))
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["work"]["status"] == outcome_type
    (tmp_path / "src/b.py").write_text("VALUE=99\n", encoding="utf-8")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["outcome_source_changes"]["complete-group"]["changed_paths"] == ["src/b.py"]
    assert selected["work"]["status"] == ("verification changed" if outcome_type == "verified" else "implemented")
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_group_proof_observes_bound_finding_scope_expansion_and_retirement(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = audit["findings"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    narrow = event(tmp_path, "original-group-proof", "verified")
    narrow["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    outcomes(tmp_path, narrow)
    original = state(tmp_path)["outcomes"][0]
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    assert candidate_work(tmp_path)["status"] == "verification changed"
    assert state(tmp_path)["outcome_source_changes"]["original-group-proof"]["changed_paths"] == ["src/b.py"]
    (tmp_path / "src/new.py").write_text("VALUE=3\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", "src/new.py"], cwd=tmp_path, check=True)
    replacement = deepcopy(map_manifest(tmp_path)["subsystems"][1])
    replacement.update(id="gamma", name="Expanded delivery owner", owned_paths=["src/b.py", "src/new.py"])
    reconcile(tmp_path, subsystems=[replacement, {"id": "alpha", "dependencies": [{"id": "gamma", "evidence": ["Reviewed replacement."]}]}],
              retirements=[{"id": "beta", "replacement_ids": ["gamma"], "reason": "Expanded owner."}])
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert selected["work"]["status"] == "verification changed"
    assert selected["outcome_source_changes"]["original-group-proof"]["changed_paths"] == ["src/b.py", "src/new.py"]
    proof = event(tmp_path, "current-group-proof", "verified")
    proof["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "src/new.py", "tests/test_a.py"])
    outcomes(tmp_path, proof)
    assert candidate_work(tmp_path)["status"] == "verified"
    assert state(tmp_path)["outcomes"][0] == original
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


@pytest.mark.parametrize("target_kind", ["candidate", "finding"])
def test_selected_history_retains_delivery_and_ownership_revisions(tmp_path: Path, target_kind: str) -> None:
    started(tmp_path)
    identifier = "alpha-fix" if target_kind == "candidate" else "alpha-defect"
    target = {"kind": target_kind, "id": identifier}
    requested = {"target": target, "commit": True, "deployments": ["local"], "reason": "User requested delivery."}
    withdrawn = {"target": target, "commit": False, "deployments": [], "reason": "User withdrew delivery."}
    outcomes(tmp_path, delivery_requirements=[requested])
    outcomes(tmp_path, delivery_requirements=[withdrawn])
    reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed proof owner."}])
    reconcile(tmp_path, subsystems=[{"id": "beta", "name": "Delivery and proof"}])
    saved = report(tmp_path).read_bytes()
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), history=True, **{target_kind: identifier})
    deliveries = [entry for entry in selected["history"] if entry["operation"] == "outcome"]
    assert len(deliveries) == 2
    assert deliveries[0]["delivery_requirements"] == [requested]
    assert deliveries[0]["prior_delivery_requirements"] == []
    assert deliveries[1]["delivery_requirements"] == [withdrawn]
    assert deliveries[1]["prior_delivery_requirements"] == [requested]
    reconciliations = [entry for entry in selected["history"] if entry["operation"] == "reconcile"]
    assert len(reconciliations) == 2
    moved = reconciliations[0]
    assert moved["ownership_changes"] == [{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed proof owner."}]
    assert "tests/test_a.py" in next(sub for sub in moved["prior_subsystems"] if sub["id"] == "alpha")["owned_paths"]
    assert "tests/test_a.py" in next(sub for sub in moved["subsystems"] if sub["id"] == "beta")["owned_paths"]
    assert reconciliations[1]["prior_subsystems"][1]["name"] != "Delivery and proof"
    assert reconciliations[1]["subsystems"][0]["name"] == "Delivery and proof"
    assert all("map_source" not in sub for entry in reconciliations for sub in entry["prior_subsystems"])
    pages = [atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), history=True, limit=1, offset=index,
                                  **{target_kind: identifier}) for index in range(selected["history_total"])]
    assert [page["history"][0] for page in pages] == selected["history"]
    assert all(page["history_total"] == selected["history_total"] for page in pages)
    assert pages[0]["history_has_more"] and not pages[-1]["history_has_more"]
    assert report(tmp_path).read_bytes() == saved


@pytest.mark.parametrize("kind", ["local", "systemic"])
@pytest.mark.parametrize("transition", ["current", "retired", "superseded"])
def test_finding_inspection_preserves_originating_audit_proof(tmp_path: Path, kind: str, transition: str) -> None:
    started(tmp_path, analyzed=False)
    (tmp_path / "audit-proof.txt").write_text("Proof v1", encoding="utf-8")
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", "audit-proof.txt"])
    original = deepcopy(audit["source_identity"])
    if kind == "systemic":
        audit["systemic_findings"], audit["findings"] = audit["findings"], []
        audit["candidates"] = []
    publish(tmp_path, "audit-subsystem", audit)
    if transition == "retired":
        replacement = deepcopy(map_manifest(tmp_path)["subsystems"][0])
        replacement.update(id="gamma", name="Validation replacement")
        reconcile(tmp_path, subsystems=[replacement], retirements=[{"id": "alpha", "replacement_ids": ["gamma"], "reason": "Reviewed owner."}])
    elif transition == "superseded":
        replacement = audit_manifest(tmp_path, report(tmp_path))
        replacement.update(findings=[], candidates=[])
        for lens in replacement["lenses"]:
            lens["finding_ids"] = []
        publish(tmp_path, "audit-subsystem", replacement)
    (tmp_path / "audit-proof.txt").write_text("Proof v2", encoding="utf-8")
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", changed_paths=["audit-proof.txt"])
    assert selected["total"] == 1
    row = selected["rows"][0]
    assert row["historical"] == (transition != "current")
    assert row["audit_source_identity"] == original
    assert row["source_changes"]["audit"]["changed_paths"] == ["audit-proof.txt"]
    assert row["outcome_source_changes"] == {}
    discovered = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), changed_paths=["audit-proof.txt"], history=True)
    assert "alpha-defect" in {item["target"]["id"] for item in discovered["rows"]}
    outcomes(tmp_path, event(tmp_path, "finding-proof", "verified", target_kind="finding", target_id="alpha-defect"))
    row = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect")["rows"][0]
    assert row["source_changes"]["audit"]["freshness"] == "changed"
    assert row["outcome_source_changes"]["finding-proof"]["freshness"] == "fresh"
    assert row["work"]["status"] == "verified" and row["audit_source_identity"] == original
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_retained_current_format_history_uses_canonical_map_snapshots(tmp_path: Path) -> None:
    make_repo(tmp_path)
    # Unchanged state captured from the initial independent supported-API probe.
    # Its reconciliation predates the derived metadata; it is still format 4.
    fixture = Path(__file__).parent / "fixtures/astra_atlas/retained_history.json"
    original = json.loads(fixture.read_text(encoding="utf-8"))
    assert original["state_version"] == atlas.STATE_VERSION == 4
    assert "affected_subsystems" not in original["history"][-1]
    report(tmp_path).parent.mkdir(parents=True)
    report(tmp_path).write_bytes(atlas._render(original))
    saved = report(tmp_path).read_bytes()
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    for inspect in (atlas.inspect_report, atlas.status_report):
        selected = inspect(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)
        assert any(entry["operation"] == "reconcile" for entry in selected["history"])
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)
    moved = next(entry for entry in selected["history"] if entry["operation"] == "reconcile")
    assert "tests/test_a.py" in next(sub for sub in moved["prior_subsystems"] if sub["id"] == "alpha")["owned_paths"]
    assert "tests/test_a.py" in next(sub for sub in moved["subsystems"] if sub["id"] == "beta")["owned_paths"]
    for command in ("inspect", "status"):
        cli = subprocess.run([sys.executable, str(SCRIPT), command, "--repo-root", str(tmp_path), "--report", str(report(tmp_path)),
                              "--candidate", "alpha-fix", "--history"], capture_output=True, text=True)
        assert cli.returncode == 0, cli.stderr
        assert any(entry["operation"] == "reconcile" for entry in json.loads(cli.stdout)["history"])
    assert report(tmp_path).read_bytes() == saved
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    assert state(tmp_path)["history"] == original["history"]
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", history=True)["history"] == selected["history"]


def test_check_report_rejects_missing_retained_map_records(tmp_path: Path) -> None:
    started(tmp_path)
    reconcile(tmp_path, ownership_changes=[{"path": "tests/test_a.py", "owner": "beta", "reason": "Reviewed proof owner."}])
    invalid = state(tmp_path)
    del invalid["history"][-1]["superseded"]["map"]["subsystems"]
    payload = atlas._canonical(invalid)
    encoded = payload.decode("utf-8").replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    block = f'<script id="audit-codebase-state" type="application/json" data-sha256="{atlas._digest(payload)}">{encoded}</script>'
    damaged = atlas._STATE.sub(lambda _: block, report(tmp_path).read_text(encoding="utf-8"))
    report(tmp_path).write_text(damaged, encoding="utf-8", newline="\n")
    with pytest.raises(atlas.ReportError, match="retained map subsystems must be a list"):
        atlas.check_report(repo_root=tmp_path, report=report(tmp_path))
