"""Authoring affordances preserve truthful maps, source bindings, and lifecycle order."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from test_astra_atlas import atlas, audit_manifest, identity, make_repo, map_manifest, publish, report
from test_astra_atlas_maintenance import started, state


def packet(result: dict) -> dict:
    return json.loads(Path(result["packet"]).read_text(encoding="utf-8"))


def complete_events(value: dict, root: Path) -> dict:
    for row in value["events"]:
        row["summary"] = f"Observed {row['type']} for the selected scope."
        row["evidence"] = row["evidence"] or ["Inspected the completed owner change."]
        if row["type"] == "committed":
            row["reference"] = atlas.inventory(repo_root=root)["identity"]["commit"]
    return value


def test_prepare_map_keeps_semantics_blank_and_publishes_only_after_authorship(tmp_path: Path) -> None:
    make_repo(tmp_path)
    prepared = atlas.prepare_map(repo_root=tmp_path, report=report(tmp_path))
    draft = packet(prepared)
    assert Path(prepared["packet"]) == report(tmp_path).with_name("map.json")
    assert prepared["published"] is False and prepared["report_sha256"] == "absent"
    assert draft["observation_identity"] == atlas.inventory(repo_root=tmp_path)["identity"]
    assert draft["subsystems"][0]["owned_paths"] == ["src/a.py", "src/b.py", "tests/test_a.py"]
    assert prepared["tracked_path_count"] == 3
    with pytest.raises(atlas.ReportError, match=r"map manifest\.title.*non-empty string"):
        publish(tmp_path, "render-report", draft)
    assert not report(tmp_path).exists()
    draft.update(title="Validation architecture")
    draft["systems"][0]["name"] = "Validation"
    draft["subsystems"][0].update(name="Policy owner", purpose="Own the small validation package.")
    publish(tmp_path, "render-report", draft)
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]
    with pytest.raises(atlas.ReportError, match="absent report"):
        atlas.prepare_map(repo_root=tmp_path, report=report(tmp_path), output=Path("another.json"))


def test_prepare_map_does_not_overwrite_authored_draft_or_escape_report_directory(tmp_path: Path) -> None:
    make_repo(tmp_path)
    prepared = atlas.prepare_map(repo_root=tmp_path, report=report(tmp_path))
    destination = Path(prepared["packet"])
    destination.write_text('{"title":"Retain my work"}\n', encoding="utf-8")
    before = destination.read_bytes()
    with pytest.raises(atlas.ReportError, match="already exists"):
        atlas.prepare_map(repo_root=tmp_path, report=report(tmp_path))
    assert destination.read_bytes() == before
    with pytest.raises(atlas.ReportError, match="report directory"):
        atlas.prepare_map(repo_root=tmp_path, report=report(tmp_path), output=tmp_path / "outside.json")
    assert not (tmp_path / "outside.json").exists()


@pytest.mark.parametrize("section,field,value,expected", [
    ("findings", "impact", ["impact"], "non-empty string; got array"),
    ("findings", "evidence", "trace", "list of non-empty strings; got string"),
    ("candidates", "required_proof", "run the probe", "list of non-empty strings; got string"),
    ("candidates", "risks", [42], "non-empty string; got number"),
])
def test_audit_type_errors_locate_packet_target_and_field(tmp_path: Path, section: str, field: str,
                                                        value: object, expected: str) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    raw = audit_manifest(tmp_path, report(tmp_path))
    raw[section][0][field] = value
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError) as error:
        publish(tmp_path, "audit-subsystem", raw)
    message = str(error.value)
    assert "audit manifest (subsystem alpha)" in message
    assert f"{section}[0] ({raw[section][0]['id']}).{field}" in message
    assert expected in message
    assert report(tmp_path).read_bytes() == before


def test_lens_reference_error_explains_primary_class_relationship(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    raw = audit_manifest(tmp_path, report(tmp_path))
    raw["lenses"][0]["finding_ids"] = []
    raw["lenses"][2]["finding_ids"] = ["alpha-defect"]
    with pytest.raises(atlas.ReportError) as error:
        publish(tmp_path, "audit-subsystem", raw)
    message = str(error.value)
    assert "lenses[2].finding_ids[0]" in message and "alpha-defect" in message
    assert "primary_class equals the lens class" in message
    assert "move alpha-defect to lens reliability" in message


def test_opportunity_rejects_defect_only_fields_with_repair_guidance(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    raw = audit_manifest(tmp_path, report(tmp_path))
    raw["findings"][0]["kind"] = "opportunity"
    with pytest.raises(atlas.ReportError) as error:
        publish(tmp_path, "audit-subsystem", raw)
    message = str(error.value)
    assert "findings[0] (alpha-defect)" in message
    assert "not valid for opportunity: scenario, severity" in message
    assert "only to defect findings" in message


@pytest.mark.parametrize("append", [False, True])
def test_affected_owner_preflight_preserves_report_and_names_reprepare_route(tmp_path: Path, append: bool) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    if append:
        publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    raw = audit_manifest(tmp_path, report(tmp_path))
    raw["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    if append:
        raw.update(lenses=[], coverage="", recommendation="")
        raw["findings"][0]["id"] = "additional-defect"
        raw["candidates"] = []
    operation = "append-findings" if append else "audit-subsystem"
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError) as error:
        publish(tmp_path, operation, raw)
    message = str(error.value)
    assert "source_identity.paths" in message and "beta (src/b.py)" in message
    assert "prepare-audit --subsystem alpha --affected-subsystem beta" in message
    assert (" --append" in message) == append
    assert "--output NEW.json" in message
    assert report(tmp_path).read_bytes() == before
    prepared = atlas.prepare_audit(repo_root=tmp_path, report=report(tmp_path), subsystem="alpha",
                                   affected_subsystems=["beta"], append=append)
    expanded = packet(prepared)
    raw.update(source_identity=expanded["source_identity"], prepared=expanded["prepared"])
    publish(tmp_path, operation, raw)
    assert atlas.check_report(repo_root=tmp_path, report=report(tmp_path))["valid"]


def test_multi_stage_outcomes_keep_phase_order_receipts_and_delivery_for_linked_targets(tmp_path: Path) -> None:
    started(tmp_path)
    targets = ["candidate:alpha-fix", "finding:alpha-defect"]
    atlas.verify(repo_root=tmp_path, report=report(tmp_path), identifier="probe", targets=targets,
                 command=[sys.executable, "-c", "print('verified')"], environment="fixture")
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=targets,
                                      outcome_types=["implemented", "verified", "committed"], check_ids=["probe"])
    raw = complete_events(packet(prepared), tmp_path)
    assert [row["type"] for row in raw["events"]] == ["implemented", "implemented", "verified", "verified", "committed", "committed"]
    assert len({row["id"] for row in raw["events"]}) == 6
    for row in raw["events"]:
        assert ("check_ids" in row) == (row["type"] == "verified")
        assert ("source_identity" in row) == (row["type"] in {"implemented", "verified"})
    arguments = {"repo_root": tmp_path, "report": report(tmp_path), "batch_id": "lifecycle",
                 "packets": [{"operation": "record-outcome", "manifest": raw}]}
    result = atlas.publish_batch(**arguments)
    assert result["published"]
    assert atlas.publish_batch(**arguments)["already_published"]
    work = atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]
    assert work["status"] == "verified"
    assert work["commits"] == [atlas.inventory(repo_root=tmp_path)["identity"]["commit"]]
    assert [row["type"] for row in state(tmp_path)["outcomes"]] == [row["type"] for row in raw["events"]]


def test_reordering_prepared_lifecycle_transitions_is_rejected(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_types=["implemented", "verified"])
    raw = complete_events(packet(prepared), tmp_path)
    raw["events"].reverse()
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="conflicts"):
        publish(tmp_path, "record-outcome", raw)
    assert report(tmp_path).read_bytes() == before


def test_requested_lifecycle_order_is_preserved_without_inferred_prerequisites(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_types=["verified", "implemented"])
    raw = complete_events(packet(prepared), tmp_path)
    publish(tmp_path, "record-outcome", raw)
    assert [row["type"] for row in state(tmp_path)["outcomes"]] == ["verified", "implemented"]
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "implemented"


def test_invalid_late_lifecycle_event_does_not_publish_earlier_events(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_types=["implemented", "verified", "committed"])
    raw = complete_events(packet(prepared), tmp_path)
    raw["events"][-1]["reference"] = "short"
    before = report(tmp_path).read_bytes()
    with pytest.raises(atlas.ReportError, match="full Git commit ID"):
        atlas.publish_batch(repo_root=tmp_path, report=report(tmp_path), batch_id="invalid-lifecycle",
                            packets=[{"operation": "record-outcome", "manifest": raw}])
    assert report(tmp_path).read_bytes() == before and state(tmp_path)["outcomes"] == []


@pytest.mark.parametrize("arguments", [
    {"outcome_types": []}, {"outcome_types": ["fixed"]}, {"outcome_types": "verified"},
    {"outcome_types": ["verified", "verified"]},
    {"outcome_type": "verified", "outcome_types": ["implemented"]},
])
def test_prepare_outcomes_rejects_ambiguous_or_invalid_sequences(tmp_path: Path, arguments: dict) -> None:
    started(tmp_path)
    with pytest.raises(atlas.ReportError):
        atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"], **arguments)


def test_single_type_outcome_api_retains_existing_packet_shape(tmp_path: Path) -> None:
    started(tmp_path)
    prepared = atlas.prepare_outcomes(repo_root=tmp_path, report=report(tmp_path), targets=["candidate:alpha-fix"],
                                      outcome_type="verified")
    raw = complete_events(packet(prepared), tmp_path)
    assert Path(prepared["packet"]).name == "outcomes-verified.json"
    assert len(raw["events"]) == 1 and raw["events"][0]["type"] == "verified"
    publish(tmp_path, "record-outcome", raw)
    assert atlas.status_report(repo_root=tmp_path, report=report(tmp_path), candidate="alpha-fix")["rows"][0]["work"]["status"] == "verified"
