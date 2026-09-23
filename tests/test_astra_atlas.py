"""Current-format tests for the Astra visual audit workbench."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "skills/astra/audit-codebase/scripts/atlas.py"
SPEC = importlib.util.spec_from_file_location("astra_atlas", SCRIPT)
assert SPEC and SPEC.loader
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)


def write_json(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")
    return path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_repo(root: Path) -> None:
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src/a.py").write_text("VALUE=1\n", encoding="utf-8")
    (root / "src/b.py").write_text("VALUE=2\n", encoding="utf-8")
    (root / "tests/test_a.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "a@b.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Audit"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True)


def report(root: Path) -> Path:
    return root / ".tmp/audit-codebase/run-1/report.html"


def identity(root: Path, paths: list[str]) -> dict[str, object]:
    packet = atlas.source_identity(repo_root=root, paths=paths)
    return {"paths": packet["paths"], "sha256": packet["sha256"]}


def map_manifest(root: Path) -> dict[str, object]:
    return {
        "version": atlas.MANIFEST_VERSION,
        "expected_report_sha256": "absent",
        "title": "Architecture atlas",
        "observation_identity": atlas.inventory(repo_root=root)["identity"],
        "systems": [{"id": "core", "name": "Core"}, {"id": "delivery", "name": "Delivery"}],
        "subsystems": [
            {
                "id": "alpha",
                "system_id": "core",
                "name": "Alpha",
                "purpose": "Own validation.",
                "ownership": "Identity policy",
                "authority": ["CONTEXT.md"],
                "callers": ["beta"],
                "dependencies": [{"id": "beta", "evidence": ["alpha imports beta"]}],
                "interfaces": ["validated identity"],
                "proof_seams": ["tests/test_a.py"],
                "owned_paths": ["src/a.py", "tests/test_a.py"],
            },
            {
                "id": "beta",
                "system_id": "delivery",
                "name": "Beta",
                "purpose": "Deliver results.",
                "ownership": "Delivery",
                "authority": [],
                "callers": ["operators"],
                "dependencies": [],
                "interfaces": ["result"],
                "proof_seams": [],
                "owned_paths": ["src/b.py"],
            },
        ],
        "excluded": [],
        "coverage": "Every tracked path has one owner.",
        "evidence_limits": "Runtime not executed.",
    }


def finding() -> dict[str, object]:
    return {
        "id": "alpha-defect",
        "kind": "defect",
        "primary_class": "reliability",
        "title": "Unchecked entry",
        "expectation": "All identities are checked.",
        "locations": ["src/a.py"],
        "evidence": ["alternate caller bypasses validation"],
        "impact": "Invalid identity crosses boundary.",
        "causal_owner": "shared write seam",
        "affected_scope": ["alpha", "beta"],
        "direction": "Move policy to owner.",
        "proof": ["exercise both callers"],
        "confidence": "high",
        "severity": "P1",
        "scenario": "Alternate caller submits unchecked identity.",
    }


def candidate() -> dict[str, object]:
    return {
        "id": "alpha-fix",
        "title": "Centralize validation",
        "primary_class": "design",
        "strength": "strong",
        "finding_ids": ["alpha-defect"],
        "affected_scope": ["alpha", "beta"],
        "problem": "Policy is scattered.",
        "evidence": ["two callers coordinate it"],
        "direction": "Own policy at the write seam.",
        "benefit": "One invariant owner.",
        "risks": ["format compatibility"],
        "required_proof": ["both callers reject invalid input"],
    }


def audit_manifest(root: Path, rpt: Path) -> dict[str, object]:
    lenses = [
        {
            "class": name,
            "state": "evidence gap" if name == "performance" else "complete",
            "evidence": [] if name == "performance" else [f"{name} evidence"],
            "finding_ids": ["alpha-defect"] if name == "reliability" else [],
            "reason": "Inspected current owner.",
        }
        for name in atlas._LENSES
    ]
    return {
        "version": atlas.MANIFEST_VERSION,
        "expected_report_sha256": sha(rpt),
        "subsystem_id": "alpha",
        "source_identity": identity(root, ["src/a.py", "src/b.py", "tests/test_a.py"]),
        "source_trace": {
            "summary": "Traced both entry paths.",
            "entry_points": ["validate"],
            "callers": ["beta"],
            "dependencies": ["beta"],
            "interfaces": ["validated identity"],
            "proof_seams": ["tests/test_a.py"],
            "representative_flows": ["input to write"],
            "history_signals": ["validation moved twice"],
        },
        "lenses": lenses,
        "findings": [finding()],
        "candidates": [candidate()],
        "systemic_findings": [],
        "coverage": "All six classes resolved or have explicit gaps.",
        "evidence_limits": "No production trace.",
        "recommendation": "User may select alpha-fix.",
    }


def analysis_manifest(root: Path, rpt: Path) -> dict[str, object]:
    return {
        "version": atlas.MANIFEST_VERSION,
        "expected_report_sha256": sha(rpt),
        "candidate_id": "alpha-fix",
        "state": "analyzed",
        "question": "",
        "source_identity": identity(root, ["src/a.py", "src/b.py", "tests/test_a.py"]),
        "summary": "One owner can hide policy.",
        "cause": "Callers coordinate validation.",
        "affected_scope": ["alpha", "beta"],
        "options": [
            {"name": "Keep", "description": "Leave coordination in callers.", "tradeoffs": ["cost remains"]},
            {"name": "Smallest", "description": "Move policy to write seam.", "tradeoffs": ["touch two callers"]},
        ],
        "recommendation": "Use the existing write seam as owner.",
        "tradeoffs": ["small migration"],
        "proof": ["exercise both callers"],
        "evidence_limits": "Exact interface remains implementation-owned.",
    }


def publish(root: Path, objective: str, manifest: dict[str, object]) -> dict[str, object]:
    packet = write_json(root / f"{objective}.json", manifest)
    return atlas.mutate_report(
        objective=objective, repo_root=root, report=report(root), manifest=packet
    )


def test_map_renders_visual_workbench(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    text = report(tmp_path).read_text(encoding="utf-8")
    for value in (
        "Architecture map",
        "Subsystem explorer",
        "Audit atlas",
        "Copy audit command",
        "$audit-codebase audit subsystem alpha in atlas run run-1",
        "Subsystem dependency map",
        "alpha imports beta",
    ):
        assert value in text
    state = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert state["run_id"] == "run-1"
    assert state["freshness"] == {"alpha": "fresh", "beta": "fresh"}


def test_audit_adds_findings_candidates_and_coverage(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    text = report(tmp_path).read_text(encoding="utf-8")
    for value in (
        "Unchecked entry",
        "Centralize validation",
        "Strong",
        "Current problem",
        "Required proof",
        "$audit-codebase analyze candidate alpha-fix in atlas run run-1",
        "Performance",
    ):
        assert value in text
    state = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    alpha = state["subsystems"][0]
    assert alpha["state"] == "audited"
    assert alpha["audit"]["candidates"][0]["strength"] == "strong"


def test_analyze_updates_only_selected_candidate(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    state = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    cand = state["subsystems"][0]["audit"]["candidates"][0]
    assert cand["state"] == "analyzed"
    assert cand["analysis"]["recommendation"] == "Use the existing write seam as owner."
    text = report(tmp_path).read_text(encoding="utf-8")
    assert "Leave coordination in callers." in text
    assert "Move policy to write seam." in text
    assert "Copy next-action handoff" in text
    assert "Help me choose the appropriate next owner" in text


def test_refresh_marks_changed_source_without_revalidating(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    before = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    (tmp_path / "src/a.py").write_text("VALUE=9\n", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    after = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert before["subsystems"][0]["audit"] == after["subsystems"][0]["audit"]
    assert after["freshness"]["alpha"] == "changed"
    assert "Source changed" in report(tmp_path).read_text(encoding="utf-8")


def test_source_and_report_drift_are_rejected(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    stale = audit_manifest(tmp_path, report(tmp_path))
    (tmp_path / "src/a.py").write_text("VALUE=3\n", encoding="utf-8")
    with pytest.raises(atlas.ReportError, match="current bound source"):
        publish(tmp_path, "audit-subsystem", stale)


def test_map_requires_complete_nonoverlapping_ownership(tmp_path: Path) -> None:
    make_repo(tmp_path)
    manifest = map_manifest(tmp_path)
    manifest["subsystems"][0]["owned_paths"] = ["src/a.py"]
    with pytest.raises(atlas.ReportError, match="neither owned nor excluded"):
        publish(tmp_path, "render-report", manifest)
    manifest = map_manifest(tmp_path)
    manifest["subsystems"][1]["owned_paths"] = ["src/a.py", "src/b.py"]
    with pytest.raises(atlas.ReportError, match="multiple owners"):
        publish(tmp_path, "render-report", manifest)


def test_current_format_only_and_tamper_detection(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    rpt = report(tmp_path)
    raw = rpt.read_text(encoding="utf-8")
    assert 'audit-codebase-report-version" content="1"' in raw
    assert "https://" not in raw and "http://" not in raw
    assert "cdn" not in raw.lower() and "mermaid" not in raw.lower()
    rpt.write_text(raw.replace("Architecture map", "Changed architecture", 1), encoding="utf-8")
    with pytest.raises(atlas.ReportError, match="canonical"):
        atlas.inspect_report(repo_root=tmp_path, report=rpt)


def test_invalid_candidate_strength_and_selection_are_rejected(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    bad = audit_manifest(tmp_path, report(tmp_path))
    bad["candidates"][0]["strength"] = "99"
    with pytest.raises(atlas.ReportError, match="candidate strength"):
        publish(tmp_path, "audit-subsystem", bad)

    publish(tmp_path, "audit-subsystem", audit_manifest(tmp_path, report(tmp_path)))
    invalid = analysis_manifest(tmp_path, report(tmp_path))
    invalid["candidate_id"] = "other"
    with pytest.raises(atlas.ReportError, match="choose one of: alpha-fix"):
        publish(tmp_path, "analyze-candidate", invalid)


def test_writer_lock_preserves_report(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    rpt = report(tmp_path)
    before = rpt.read_bytes()
    lock = rpt.with_name("report.lock")
    lock.write_text("active", encoding="utf-8")
    manifest = write_json(tmp_path / "audit.json", audit_manifest(tmp_path, rpt))
    with pytest.raises(atlas.ReportError, match="writer is active"):
        atlas.mutate_report(
            objective="audit-subsystem",
            repo_root=tmp_path,
            report=rpt,
            manifest=manifest,
        )
    assert rpt.read_bytes() == before
