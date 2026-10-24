"""Current proof projections, bounded source inspection, and unobserved previews."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from test_astra_atlas import analysis_manifest, atlas, audit_manifest, finding, identity, publish, report, sha
from test_astra_atlas_maintenance import candidate_work, event, outcomes, reconcile, started, state


def two_findings(root: Path) -> None:
    started(root, analyzed=False)
    audit = audit_manifest(root, report(root))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append(second["id"])
    audit["candidates"][0]["finding_ids"].append(second["id"])
    publish(root, "audit-subsystem", audit)


def source_packets(value):
    if isinstance(value, dict):
        if {"paths", "sha256"} <= value.keys():
            yield value
        for item in value.values():
            yield from source_packets(item)
    elif isinstance(value, list):
        for item in value:
            yield from source_packets(item)


def test_retained_map_inventory_obeys_source_paging_without_changing_history(tmp_path: Path) -> None:
    started(tmp_path)
    original_inventory = deepcopy(state(tmp_path)["map_inventory"])
    reconcile(tmp_path, subsystems=[{"id": "alpha", "ownership": "Reviewed validation ownership"}])
    before = report(tmp_path).read_bytes()
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), history=True, source_limit=1)
    inventory = next(row for row in selected["history"] if row["operation"] == "reconcile")["superseded"]["map"]["map_inventory"]
    assert inventory["paths"] == original_inventory["paths"][:1]
    assert inventory["paths_total"] == len(original_inventory["paths"]) and inventory["paths_has_more"]
    assert "fingerprints" not in inventory and not inventory["fingerprints_included"]
    page = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), history=True,
                                include_fingerprints=True, source_limit=1, source_offset=1)
    next_inventory = next(row for row in page["history"] if row["operation"] == "reconcile")["superseded"]["map"]["map_inventory"]
    path = original_inventory["paths"][1]
    assert next_inventory["paths"] == [path]
    assert next_inventory["fingerprints"] == {path: original_inventory["fingerprints"][path]}
    full = state(tmp_path)
    stored = next(row for row in full["history"] if row["operation"] == "reconcile")["superseded"]["map"]["map_inventory"]
    assert stored == original_inventory
    assert report(tmp_path).read_bytes() == before


def test_current_linked_proof_is_separate_from_changed_retained_history(tmp_path: Path) -> None:
    two_findings(tmp_path)
    outcomes(tmp_path, event(tmp_path, "old-group-proof", "verified"))
    original = deepcopy(state(tmp_path)["outcomes"][0])
    (tmp_path / "src/a.py").write_text("VALUE=9\n", encoding="utf-8")
    outcomes(tmp_path, event(tmp_path, "first-renewed-proof", "verified", target_kind="finding", target_id="alpha-defect"))
    partial = candidate_work(tmp_path)
    assert partial["current_completion"] == "verification changed"
    assert partial["current_proof_freshness"] == "changed"
    outcomes(tmp_path, event(tmp_path, "second-renewed-proof", "verified", target_kind="finding", target_id="second-defect"))
    current = candidate_work(tmp_path)
    assert current["status"] == current["current_completion"] == "verified"
    assert current["current_proof_freshness"] == "fresh"
    assert current["current_proof_outcome_ids"] == ["first-renewed-proof", "second-renewed-proof"]
    assert current["historical_outcome_ids"] == ["old-group-proof"]
    assert current["historical_outcome_freshness"] == current["outcome_freshness"] == "changed"
    assert state(tmp_path)["outcomes"][0] == original
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix", outstanding=True)["total"] == 0


@pytest.mark.parametrize("decision,completion", [("reopened", "open"), ("implemented", "implemented"), ("deferred", "deferred")])
def test_later_decision_never_reuses_an_earlier_verified_completion(tmp_path: Path, decision: str, completion: str) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "earlier-proof", "verified"))
    outcomes(tmp_path, event(tmp_path, "later-decision", decision))
    current = candidate_work(tmp_path)
    assert current["status"] == current["current_completion"] == completion
    assert current["current_proof_outcome_ids"] == []
    assert current["current_proof_freshness"] == ""
    assert "earlier-proof" in current["historical_outcome_ids"]
    assert current["implementation_epoch_outcome_id"] == ("later-decision" if decision != "deferred" else "")


def test_fresh_narrow_proof_does_not_claim_complete_candidate_scope(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["affected_scope"] = audit["findings"][0]["affected_scope"] = ["alpha"]
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    narrow = event(tmp_path, "narrow-proof", "verified", target_kind="finding", target_id="alpha-defect")
    narrow["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    outcomes(tmp_path, narrow)
    current = candidate_work(tmp_path)
    assert current["current_completion"] == "verification changed"
    assert current["current_proof_freshness"] == "changed"
    assert current["current_proof_outcome_ids"] == ["narrow-proof"]
    assert state(tmp_path)["outcome_freshness"]["narrow-proof"] == "fresh"


def test_current_proof_retains_candidate_membership_guard(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    outcomes(tmp_path, event(tmp_path, "old-membership-proof", "verified"))
    audit = audit_manifest(tmp_path, report(tmp_path))
    second = finding()
    second["id"] = "second-defect"
    audit["findings"].append(second)
    audit["lenses"][0]["finding_ids"].append(second["id"])
    audit["candidates"][0]["finding_ids"].append(second["id"])
    publish(tmp_path, "audit-subsystem", audit)
    outcomes(tmp_path, event(tmp_path, "added-finding-proof", "verified", target_kind="finding", target_id="second-defect"))
    current = candidate_work(tmp_path)
    assert current["current_completion"] == "verification changed"
    assert current["current_proof_freshness"] == "changed"
    assert current["current_proof_outcome_ids"] == ["old-membership-proof"]


@pytest.mark.parametrize("renewal", ["implemented", "reopened"])
def test_current_proof_requires_every_linked_finding_after_latest_epoch(tmp_path: Path, renewal: str) -> None:
    two_findings(tmp_path)
    outcomes(tmp_path, event(tmp_path, "old-proof", "verified"))
    outcomes(tmp_path, event(tmp_path, "new-epoch", renewal))
    outcomes(tmp_path, event(tmp_path, "first-current-proof", "verified", target_kind="finding", target_id="alpha-defect"))
    partial = candidate_work(tmp_path)
    assert partial["current_completion"] == ("implemented" if renewal == "implemented" else "open")
    assert partial["current_proof_freshness"] == "" and partial["current_proof_outcome_ids"] == []
    outcomes(tmp_path, event(tmp_path, "second-current-proof", "verified", target_kind="finding", target_id="second-defect"))
    complete = candidate_work(tmp_path)
    assert complete["current_completion"] == "verified" and complete["current_proof_freshness"] == "fresh"
    assert complete["current_proof_outcome_ids"] == ["first-current-proof", "second-current-proof"]
    assert complete["implementation_epoch_outcome_id"] == "new-epoch"


def test_selected_detail_and_history_bound_sources_without_changing_saved_proof(tmp_path: Path) -> None:
    started(tmp_path, analyzed=False)
    proof_dir = tmp_path / "proofs"
    proof_dir.mkdir()
    extra = []
    for number in range(36):
        path = proof_dir / f"input-{number:02}.txt"
        path.write_text(str(number), encoding="utf-8")
        extra.append(path.relative_to(tmp_path).as_posix())
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", *extra])
    publish(tmp_path, "audit-subsystem", audit)
    # A second revision leaves large source packets in retained history too.
    audit["expected_report_sha256"] = sha(report(tmp_path))
    publish(tmp_path, "audit-subsystem", audit)
    original = report(tmp_path).read_bytes()
    selected = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", history=True, source_limit=5)
    packets = list(source_packets(selected))
    assert packets and all("fingerprints" not in packet for packet in packets)
    assert all(len(packet["paths"]) <= 5 for packet in packets)
    large = selected["rows"][0]["audit_source_identity"]
    assert large["sha256"] == audit["source_identity"]["sha256"]
    assert large["paths_total"] == large["fingerprints_total"] == 39
    assert large["paths_has_more"] and not large["fingerprints_included"]
    assert any(packet["paths_total"] == 39 for entry in selected["history"] for packet in source_packets(entry))
    fingerprints = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", include_fingerprints=True,
                                        source_limit=7, source_offset=5)["rows"][0]["audit_source_identity"]
    expected = audit["source_identity"]["paths"][5:12]
    assert fingerprints["paths"] == list(fingerprints["fingerprints"]) == expected
    assert fingerprints["paths_offset"] == 5 and fingerprints["paths_limit"] == 7
    complete = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), full=True)["state"]
    assert complete["subsystems"][0]["audit"]["source_identity"] == audit["source_identity"]
    assert report(tmp_path).read_bytes() == original


@pytest.mark.parametrize("fields", [{"source_limit": 0}, {"source_limit": 101}, {"source_offset": -1}])
def test_source_pagination_rejects_invalid_bounds(tmp_path: Path, fields: dict) -> None:
    started(tmp_path)
    saved = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="source limit"):
        atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path), finding="alpha-defect", **fields)
    assert report(tmp_path).read_bytes() == saved


def test_pending_preview_preserves_unobserved_state_and_exact_viewed_revision(tmp_path: Path) -> None:
    started(tmp_path)
    observation = dict(repo_root=tmp_path, report=report(tmp_path), environment="test-host", capability="html-preview",
                       state="pending", reason="Opening accepted; rendering not yet observed.", evidence=["Host queued opening request."])
    pending = atlas.record_preview(**observation)
    assert pending["preview_state"] == "pending"
    saved = report(tmp_path).read_bytes()
    repeated = atlas.record_preview(**observation)
    assert repeated["unchanged"] and report(tmp_path).read_bytes() == saved
    preview = state(tmp_path)["preview"][0]
    assert preview["state"] == "pending" and "report_sha256" not in preview
    assert "rendering unobserved" in saved.decode("utf-8")
    assert not atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["visual_verification"]["performed_by_check_report"]
    with pytest.raises(atlas.ReportError, match="do not claim report verification"):
        atlas.record_preview(**observation, viewed_report_sha256=sha(report(tmp_path)))
    viewed = sha(report(tmp_path))
    verified = dict(observation, state="verified", reason="Observed rendered map and navigation.", evidence=["Rendered controls inspected."])
    with pytest.raises(atlas.ReportError, match="current report revision"):
        atlas.record_preview(**verified, viewed_report_sha256="0" * 64)
    atlas.record_preview(**verified, viewed_report_sha256=viewed)
    assert state(tmp_path)["preview"][0]["report_sha256"] == viewed
    assert state(tmp_path)["preview"][0]["state"] == "verified"


def test_prior_work_projection_renders_identical_loadable_report_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    started(tmp_path)
    outcomes(tmp_path, event(tmp_path, "original-proof", "verified"))
    atlas.record_preview(repo_root=tmp_path, report=report(tmp_path), environment="prior-host", capability="html-preview",
                         state="unavailable", reason="Host has no preview surface.", evidence=["Capability unavailable."])
    saved = report(tmp_path).read_bytes()
    original_work = atlas._work_status
    legacy_keys = {"status", "commit_pending", "deployment_pending", "commits", "deployments", "outcome_ids", "outcome_freshness"}
    depth = 0

    def legacy_projection(*args, **kwargs):
        nonlocal depth
        depth += 1
        try:
            work = original_work(*args, **kwargs)
        finally:
            depth -= 1
        return work if depth else {key: work[key] for key in legacy_keys}

    retained = state(tmp_path)
    with monkeypatch.context() as prior:
        prior.setattr(atlas, "_work_status", legacy_projection)
        prior_bytes = atlas._render(retained)
    assert prior_bytes == saved
    report(tmp_path).write_bytes(prior_bytes)
    assert candidate_work(tmp_path)["current_completion"] == "verified"
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
