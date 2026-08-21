from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pytest

MODULE_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "custom"
    / "audit-codebase"
    / "scripts"
    / "update_report.py"
)
SPEC = importlib.util.spec_from_file_location("audit_report_update", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
old = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    SPEC.loader.exec_module(MODULE)
finally:
    sys.dont_write_bytecode = old


def _write(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")
    return path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _identity(root: Path, paths: list[str]) -> dict[str, object]:
    packet = MODULE.source_identity(repo_root=root, paths=paths)
    return {"paths": packet["paths"], "sha256": packet["sha256"]}


def _repo(root: Path) -> None:
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src" / "alpha.py").write_text("VALUE=1\n")
    (root / "src" / "beta.py").write_text("VALUE=2\n")
    (root / "tests" / "test_alpha.py").write_text("def test_ok(): assert True\n")
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "a@b.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Audit"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        ["git", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True
    )


def _report(root: Path) -> Path:
    return root / ".tmp" / "audit-codebase" / "run-1" / "report.html"


def _map(root: Path, title="Atlas <unsafe>") -> dict[str, object]:
    return {
        "version": MODULE.MANIFEST_VERSION,
        "expected_report_sha256": "absent",
        "title": title,
        "observation_identity": MODULE.inventory(repo_root=root)["identity"],
        "systems": [
            {"id": "core", "name": "Core"},
            {"id": "delivery", "name": "Delivery"},
        ],
        "subsystems": [
            {
                "id": "alpha",
                "system_id": "core",
                "name": "Alpha",
                "purpose": "Own identity policy.",
                "ownership": "Identity validation",
                "authority": ["CONTEXT.md"],
                "callers": ["beta"],
                "dependencies": [{"id": "beta", "evidence": ["alpha imports beta"]}],
                "interfaces": ["validated identity"],
                "proof_seams": ["tests/test_alpha.py"],
                "owned_paths": ["src/alpha.py", "tests/test_alpha.py"],
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
                "owned_paths": ["src/beta.py"],
            },
        ],
        "excluded": [],
        "coverage": "Every tracked path has one owner.",
        "evidence_limits": "Runtime not executed.",
    }


def _finding(fid="alpha-defect") -> dict[str, object]:
    return {
        "id": fid,
        "kind": "defect",
        "primary_class": "reliability",
        "title": "Unchecked entry",
        "expectation": "All identities are checked.",
        "locations": ["src/alpha.py"],
        "evidence": ["alternate caller bypasses validation"],
        "impact": "Invalid identity crosses boundary.",
        "causal_owner": "shared write seam",
        "affected_scope": ["alpha", "beta"],
        "direction": "Move policy to owner.",
        "proof": ["exercise both callers"],
        "confidence": "high",
        "severity": "P1",
        "scenario": "An alternate caller submits an unchecked identity.",
    }


def _candidate() -> dict[str, object]:
    return {
        "id": "alpha-fix",
        "title": "Centralize validation",
        "primary_class": "design",
        "finding_ids": ["alpha-defect"],
        "affected_scope": ["alpha", "beta"],
        "problem": "Policy is scattered.",
        "evidence": ["two callers coordinate it"],
        "direction": "Own at write seam.",
        "benefit": "One invariant owner.",
        "risks": ["format compatibility"],
        "required_proof": ["both callers reject invalid input"],
    }


def _audit(report: Path, subsystem="alpha") -> dict[str, object]:
    lenses = [
        {
            "class": name,
            "state": "evidence gap" if name == "performance" else "complete",
            "evidence": [] if name == "performance" else [f"{name} evidence"],
            "finding_ids": ["alpha-defect"] if name == "reliability" else [],
            "reason": "Inspected current owner.",
        }
        for name in MODULE._LENSES
    ]
    return {
        "version": MODULE.MANIFEST_VERSION,
        "expected_report_sha256": _sha(report),
        "subsystem_id": subsystem,
        "source_identity": _identity(
            report.parents[3],
            ["src/alpha.py", "src/beta.py", "tests/test_alpha.py"],
        ),
        "source_trace": {
            "summary": "Traced both entry paths.",
            "entry_points": ["validate"],
            "callers": ["beta"],
            "dependencies": ["beta"],
            "interfaces": ["validated identity"],
            "proof_seams": ["tests/test_alpha.py"],
            "representative_flows": ["input to write"],
            "history_signals": ["validation moved twice"],
        },
        "lenses": lenses,
        "findings": [_finding()],
        "candidates": [_candidate()],
        "systemic_findings": [],
        "coverage": "All six classes resolved or have explicit gaps.",
        "evidence_limits": "No production trace.",
        "recommendation": "User may select alpha-fix.",
    }


def _analysis(
    report: Path, candidate="alpha-fix", state="analyzed", question=""
) -> dict[str, object]:
    return {
        "version": MODULE.MANIFEST_VERSION,
        "expected_report_sha256": _sha(report),
        "candidate_id": candidate,
        "state": state,
        "question": question,
        "source_identity": _identity(
            report.parents[3],
            ["src/alpha.py", "src/beta.py", "tests/test_alpha.py"],
        ),
        "summary": "One owner can hide policy.",
        "cause": "Callers coordinate validation.",
        "affected_scope": ["alpha", "beta"],
        "options": [
            {
                "name": "centralize",
                "description": "Move to write seam.",
                "tradeoffs": ["touch two callers"],
            }
        ],
        "recommendation": "Centralize.",
        "tradeoffs": ["small migration"],
        "proof": ["exercise both callers"],
        "evidence_limits": "Exact API unsettled.",
    }


def _publish(
    root: Path, objective: str, manifest: dict[str, object], report: Path | None = None
) -> dict[str, object]:
    path = report or _report(root)
    packet = _write(root / f"{objective}.json", manifest)
    return MODULE.mutate_report(
        objective=objective, repo_root=root, report=path, manifest=packet
    )


def test_map_is_deterministic_escaped_and_inspectable(tmp_path: Path) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    manifest = _write(tmp_path / "map.json", _map(tmp_path))
    first = MODULE.mutate_report(
        objective="render-report",
        repo_root=tmp_path,
        report=report,
        manifest=manifest,
        validate_only=True,
    )
    second = MODULE.mutate_report(
        objective="render-report",
        repo_root=tmp_path,
        report=report,
        manifest=manifest,
        validate_only=True,
    )
    assert (
        first["report_sha256"] == second["report_sha256"]
        and first["state_sha256"] == second["state_sha256"]
    )
    MODULE.mutate_report(
        objective="render-report", repo_root=tmp_path, report=report, manifest=manifest
    )
    text = report.read_text()
    assert "Atlas &lt;unsafe&gt;" in text and "Atlas <unsafe>" not in text
    for visible in (
        "System: Core",
        "System: Delivery",
        "alpha imports beta",
        "CONTEXT.md",
        "validated identity",
        "tests/test_alpha.py",
        "Tracked content",
        "Excluded paths",
    ):
        assert visible in text
    inspected = MODULE.inspect_report(repo_root=tmp_path, report=report)
    assert inspected["state"]["subsystems"][0]["ownership"] == "Identity validation"


def test_map_requires_complete_nonoverlapping_ownership(tmp_path: Path) -> None:
    _repo(tmp_path)
    manifest = _map(tmp_path)
    manifest["subsystems"][0]["owned_paths"] = ["src/alpha.py"]
    with pytest.raises(MODULE.ReportError, match="neither owned nor excluded"):
        _publish(tmp_path, "render-report", manifest)
    manifest = _map(tmp_path)
    manifest["subsystems"][1]["owned_paths"] = ["src/alpha.py", "src/beta.py"]
    with pytest.raises(MODULE.ReportError, match="multiple owners"):
        _publish(tmp_path, "render-report", manifest)


def test_audit_updates_selected_subsystem_and_preserves_six_class_coverage(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    _publish(tmp_path, "audit-subsystem", _audit(report))
    state = MODULE.inspect_report(repo_root=tmp_path, report=report)["state"]
    alpha, beta = state["subsystems"]
    assert alpha["state"] == "audited" and beta["state"] == "mapped"
    assert [x["class"] for x in alpha["audit"]["lenses"]] == list(MODULE._LENSES)
    assert alpha["audit"]["lenses"][-1]["state"] == "evidence gap"


def test_audit_requires_explicit_valid_selection_and_never_falls_back(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    before = report.read_bytes()
    manifest = _audit(report, "missing")
    with pytest.raises(MODULE.ReportError, match="choose one of: alpha, beta"):
        _publish(tmp_path, "audit-subsystem", manifest)
    assert (
        report.read_bytes() == before
        and MODULE.inspect_report(repo_root=tmp_path, report=report)["state"][
            "subsystems"
        ][0]["state"]
        == "mapped"
    )


def test_analyze_updates_only_user_selected_candidate_and_stops_there(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    _publish(tmp_path, "audit-subsystem", _audit(report))
    _publish(tmp_path, "analyze-candidate", _analysis(report))
    state = MODULE.inspect_report(repo_root=tmp_path, report=report)["state"]
    candidate = state["subsystems"][0]["audit"]["candidates"][0]
    assert (
        candidate["state"] == "analyzed"
        and candidate["analysis"]["recommendation"] == "Centralize."
    )
    serialized = json.dumps(state)
    assert (
        "tracker" not in serialized
        and "implement" not in serialized
        and "close" not in serialized
    )


def test_analyze_invalid_selection_does_not_fall_back_or_write(tmp_path: Path) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    _publish(tmp_path, "audit-subsystem", _audit(report))
    before = report.read_bytes()
    with pytest.raises(MODULE.ReportError, match="choose one of: alpha-fix"):
        _publish(tmp_path, "analyze-candidate", _analysis(report, "other"))
    assert report.read_bytes() == before


def test_analyze_can_stop_disproved_or_blocked_with_exact_question(
    tmp_path: Path,
) -> None:
    for state, question in (
        ("disproved", ""),
        ("blocked", "May the public format change?"),
    ):
        root = tmp_path / state
        root.mkdir()
        _repo(root)
        report = _report(root)
        _publish(root, "render-report", _map(root))
        _publish(root, "audit-subsystem", _audit(report))
        _publish(
            root, "analyze-candidate", _analysis(report, state=state, question=question)
        )
        candidate = MODULE.inspect_report(repo_root=root, report=report)["state"][
            "subsystems"
        ][0]["audit"]["candidates"][0]
        assert (
            candidate["state"] == state
            and candidate["analysis"]["question"] == question
        )
    root = tmp_path / "invalid"
    root.mkdir()
    _repo(root)
    report = _report(root)
    _publish(root, "render-report", _map(root))
    _publish(root, "audit-subsystem", _audit(report))
    with pytest.raises(MODULE.ReportError, match="requires an exact question"):
        _publish(root, "analyze-candidate", _analysis(report, state="blocked"))


def test_validate_only_is_no_write_and_digest_bound(tmp_path: Path) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    manifest = _map(tmp_path)
    packet = _write(tmp_path / "map.json", manifest)
    result = MODULE.mutate_report(
        objective="render-report",
        repo_root=tmp_path,
        report=report,
        manifest=packet,
        validate_only=True,
    )
    assert result["validated"] and not result["published"] and not report.exists()
    _publish(tmp_path, "render-report", manifest)
    before = report.read_bytes()
    audit = _audit(report)
    audit["expected_report_sha256"] = "0" * 64
    with pytest.raises(MODULE.ReportError, match="does not match"):
        _publish(tmp_path, "audit-subsystem", audit)
    assert report.read_bytes() == before


def test_atomic_publish_readback_and_tamper_rejection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    called = []
    real_replace = MODULE.os.replace

    def observed(source: object, target: object) -> None:
        called.append((source, target))
        real_replace(source, target)

    monkeypatch.setattr(MODULE.os, "replace", observed)
    _publish(tmp_path, "render-report", _map(tmp_path))
    assert len(called) == 1 and not list(report.parent.glob("*.tmp"))
    report.write_text(
        report.read_text().replace("Repository coverage", "Changed coverage", 1)
    )
    with pytest.raises(MODULE.ReportError, match="canonical"):
        MODULE.inspect_report(repo_root=tmp_path, report=report)


def test_report_path_and_source_identity_are_bounded_and_content_sensitive(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    first = MODULE.source_identity(
        repo_root=tmp_path, paths=["src/beta.py", "src/alpha.py"]
    )
    assert first["paths"] == ["src/alpha.py", "src/beta.py"]
    (tmp_path / "src" / "alpha.py").write_text("VALUE=9\n")
    second = MODULE.source_identity(
        repo_root=tmp_path, paths=["src/alpha.py", "src/beta.py"]
    )
    assert first["sha256"] != second["sha256"]
    with pytest.raises(MODULE.ReportError, match="report must be"):
        _publish(tmp_path, "render-report", _map(tmp_path), tmp_path / "report.html")


def test_all_modes_reject_stale_source_identity(tmp_path: Path) -> None:
    map_root = tmp_path / "map"
    map_root.mkdir()
    _repo(map_root)
    stale_map = _map(map_root)
    (map_root / "src" / "alpha.py").write_text("VALUE=3\n")
    with pytest.raises(MODULE.ReportError, match="observation_identity"):
        _publish(map_root, "render-report", stale_map)

    root = tmp_path / "updates"
    root.mkdir()
    _repo(root)
    report = _report(root)
    _publish(root, "render-report", _map(root))
    stale_audit = _audit(report)
    (root / "src" / "alpha.py").write_text("VALUE=4\n")
    with pytest.raises(MODULE.ReportError, match="current bound source"):
        _publish(root, "audit-subsystem", stale_audit)

    audit = _audit(report)
    _publish(root, "audit-subsystem", audit)
    stale_analysis = _analysis(report)
    (root / "src" / "beta.py").write_text("VALUE=5\n")
    with pytest.raises(MODULE.ReportError, match="current bound source"):
        _publish(root, "analyze-candidate", stale_analysis)


def test_audit_identity_includes_shared_evidence_beyond_owned_paths(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    stale = _audit(report)
    (tmp_path / "src" / "beta.py").write_text("VALUE=8\n")
    with pytest.raises(MODULE.ReportError, match="current bound source"):
        _publish(tmp_path, "audit-subsystem", stale)

    omitted = _audit(report)
    omitted["source_identity"] = _identity(tmp_path, ["src/beta.py"])
    with pytest.raises(MODULE.ReportError, match="omits required"):
        _publish(tmp_path, "audit-subsystem", omitted)


def test_repeated_updates_preserve_superseded_evidence(tmp_path: Path) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    _publish(tmp_path, "audit-subsystem", _audit(report))
    _publish(tmp_path, "analyze-candidate", _analysis(report))

    replacement = _audit(report)
    replacement["recommendation"] = "Re-audited current source."
    _publish(tmp_path, "audit-subsystem", replacement)
    state = MODULE.inspect_report(repo_root=tmp_path, report=report)["state"]
    superseded_audit = state["history"][-1]["superseded"]["audit"]
    assert (
        superseded_audit["candidates"][0]["analysis"]["recommendation"] == "Centralize."
    )

    _publish(tmp_path, "analyze-candidate", _analysis(report))
    revised = _analysis(report)
    revised["summary"] = "Re-analysis retained the owner conclusion."
    _publish(tmp_path, "analyze-candidate", revised)
    state = MODULE.inspect_report(repo_root=tmp_path, report=report)["state"]
    assert (
        state["history"][-1]["superseded"]["analysis"]["summary"]
        == "One owner can hide policy."
    )


def test_audit_rejects_invalid_finding_relationships(tmp_path: Path) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))

    ghost = _audit(report)
    ghost["lenses"][0]["finding_ids"] = ["ghost-finding"]
    with pytest.raises(MODULE.ReportError, match="unknown finding"):
        _publish(tmp_path, "audit-subsystem", ghost)

    omitted = _audit(report)
    omitted["lenses"][0]["finding_ids"] = []
    with pytest.raises(MODULE.ReportError, match="omitted from lens ledger"):
        _publish(tmp_path, "audit-subsystem", omitted)

    gap_only = _audit(report)
    finding = gap_only["findings"][0]
    finding.update(
        {
            "kind": "gap",
            "missing_evidence": "Production trace",
            "boundary_reason": "Read-only access has no production logs.",
            "reentry": "Provide one production trace.",
        }
    )
    finding.pop("severity")
    finding.pop("scenario")
    with pytest.raises(MODULE.ReportError, match="requires a defect or opportunity"):
        _publish(tmp_path, "audit-subsystem", gap_only)


def test_analysis_widened_scope_requires_widened_source_identity(
    tmp_path: Path,
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    audit = _audit(report)
    audit["candidates"][0]["affected_scope"] = ["alpha"]
    _publish(tmp_path, "audit-subsystem", audit)

    analysis = _analysis(report)
    analysis["source_identity"] = _identity(
        tmp_path, ["src/alpha.py", "tests/test_alpha.py"]
    )
    with pytest.raises(MODULE.ReportError, match="omits required"):
        _publish(tmp_path, "analyze-candidate", analysis)


def test_concurrent_writers_cannot_erase_each_other(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _repo(tmp_path)
    report = _report(tmp_path)
    _publish(tmp_path, "render-report", _map(tmp_path))
    first_manifest = _write(tmp_path / "first.json", _audit(report))
    second = _audit(report)
    second["recommendation"] = "Second writer."
    second_manifest = _write(tmp_path / "second.json", second)

    entered = threading.Event()
    release = threading.Event()
    real_replace = MODULE.os.replace

    def held_replace(source: object, target: object) -> None:
        entered.set()
        assert release.wait(5)
        real_replace(source, target)

    monkeypatch.setattr(MODULE.os, "replace", held_replace)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(
            MODULE.mutate_report,
            objective="audit-subsystem",
            repo_root=tmp_path,
            report=report,
            manifest=first_manifest,
        )
        assert entered.wait(5)
        second_write = pool.submit(
            MODULE.mutate_report,
            objective="audit-subsystem",
            repo_root=tmp_path,
            report=report,
            manifest=second_manifest,
        )
        with pytest.raises(MODULE.ReportError, match="writer is active"):
            second_write.result(timeout=5)
        release.set()
        assert first.result(timeout=5)["published"]
