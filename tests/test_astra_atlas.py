"""Current-format tests for the Astra visual audit workbench."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from html.parser import HTMLParser
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


def elements(text: str, attribute: str, value: str | None = None) -> list[dict[str, str]]:
    class Reader(HTMLParser):
        def handle_starttag(self, tag, attributes):
            attrs = dict(attributes)
            if attribute in attrs and (value is None or attrs[attribute] == value):
                found.append(attrs)

    found = []
    Reader().feed(text)
    return found


def comparison(caption: str = "Move validation behind its owner") -> dict[str, object]:
    return {
        "caption": caption,
        "before": {
            "nodes": [{"id": "caller", "label": "Caller coordinates policy"}, {"id": "check", "label": "Separate check"}],
            "edges": [{"from": "caller", "to": "check", "label": "coordinates"}],
        },
        "after": {"nodes": [{"id": "owner", "label": "Owner hides validation policy"}], "edges": []},
    }


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
    assert f'audit-codebase-report-version" content="{atlas.REPORT_VERSION}"' in raw
    assert "https://" not in raw and "http://" not in raw
    assert "cdn" not in raw.lower() and "mermaid" not in raw.lower()
    rpt.write_text(raw.replace(f'audit-codebase-report-version" content="{atlas.REPORT_VERSION}"', 'audit-codebase-report-version" content="1"'), encoding="utf-8")
    with pytest.raises(atlas.ReportError, match="report version"):
        atlas.inspect_report(repo_root=tmp_path, report=rpt)
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


@pytest.mark.parametrize("lens_state", ["complete", "not applicable", "evidence gap"])
def test_coverage_accounts_for_unaudited_and_changed_scope(tmp_path: Path, lens_state: str) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    manifest = audit_manifest(tmp_path, report(tmp_path))
    for lens in manifest["lenses"]:
        if lens["class"] == "performance":
            lens.update(state=lens_state, evidence=["Measured representative work"] if lens_state == "complete" else [])
    publish(tmp_path, "audit-subsystem", manifest)
    row = elements(report(tmp_path).read_text(encoding="utf-8"), "data-lens", "performance")[0]
    assert row["data-total"] == "2"
    assert row["data-not-audited"] == "1"
    assert row[f'data-{lens_state.replace(" ", "-")}'] == "1"
    assert sum(int(row[f'data-{name}']) for name in ("complete", "not-applicable", "evidence-gap", "changed", "not-audited")) == 2

    (tmp_path / "src/a.py").write_text("VALUE=8\n", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    row = elements(report(tmp_path).read_text(encoding="utf-8"), "data-lens", "performance")[0]
    assert row["data-changed"] == "1"
    assert row["data-complete"] == row["data-not-applicable"] == row["data-evidence-gap"] == "0"
    assert row["data-not-audited"] == "1"


@pytest.mark.parametrize("changed_path", ["src/b.py", "analysis-context.txt"])
def test_analysis_freshness_tracks_its_own_evidence_and_preserves_judgment(tmp_path: Path, changed_path: str) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["source_identity"] = identity(tmp_path, ["src/a.py", "tests/test_a.py"])
    publish(tmp_path, "audit-subsystem", audit)
    (tmp_path / "analysis-context.txt").write_text("original constraint", encoding="utf-8")
    analysis = analysis_manifest(tmp_path, report(tmp_path))
    analysis["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", "analysis-context.txt"])
    publish(tmp_path, "analyze-candidate", analysis)
    before = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert before["candidate_freshness"] == {"alpha-fix": "fresh"}

    (tmp_path / changed_path).write_text("changed evidence", encoding="utf-8")
    if changed_path == "src/b.py":
        beta = audit_manifest(tmp_path, report(tmp_path))
        beta.update(subsystem_id="beta", source_identity=identity(tmp_path, ["src/b.py"]), findings=[], candidates=[])
        for lens in beta["lenses"]:
            lens["finding_ids"] = []
        publish(tmp_path, "audit-subsystem", beta)
    else:
        atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    after = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert after["freshness"] == {"alpha": "fresh", "beta": "fresh"}
    assert after["candidate_freshness"] == {"alpha-fix": "changed"}
    assert before["subsystems"][0]["audit"]["candidates"][0]["analysis"] == after["subsystems"][0]["audit"]["candidates"][0]["analysis"]
    text = report(tmp_path).read_text(encoding="utf-8")
    card = elements(text, "id", "candidate-alpha-fix")[0]
    assert card["data-state"] == "analyzed"
    assert card["data-freshness"] == "changed"
    assert not any(button["data-copy"].startswith("Use analyzed audit candidate") for button in elements(text, "data-copy"))
    assert any(button["data-copy"].startswith("$audit-codebase analyze candidate alpha-fix") for button in elements(text, "data-copy"))

    updated = analysis_manifest(tmp_path, report(tmp_path))
    updated["source_identity"] = identity(tmp_path, analysis["source_identity"]["paths"])
    publish(tmp_path, "analyze-candidate", updated)
    state = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert state["candidate_freshness"] == {"alpha-fix": "fresh"}
    assert any(button["data-copy"].startswith("Use analyzed audit candidate") for button in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy"))


def test_analysis_keeps_originating_audit_evidence_bound(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    evidence = tmp_path / "audit-context.txt"
    evidence.write_text("original constraint", encoding="utf-8")
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["source_identity"] = identity(tmp_path, ["src/a.py", "src/b.py", "tests/test_a.py", "audit-context.txt"])
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    before = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    evidence.write_text("changed constraint", encoding="utf-8")
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    after = atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]
    assert after["candidate_freshness"] == {"alpha-fix": "changed"}
    assert before["subsystems"][0]["audit"]["candidates"][0]["analysis"] == after["subsystems"][0]["audit"]["candidates"][0]["analysis"]
    assert not any(button["data-copy"].startswith("Use analyzed audit candidate") for button in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy"))

    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]["candidate_freshness"] == {"alpha-fix": "changed"}
    audit["expected_report_sha256"] = sha(report(tmp_path))
    audit["source_identity"] = identity(tmp_path, audit["source_identity"]["paths"])
    publish(tmp_path, "audit-subsystem", audit)
    publish(tmp_path, "analyze-candidate", analysis_manifest(tmp_path, report(tmp_path)))
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]["candidate_freshness"] == {"alpha-fix": "fresh"}
    assert any(button["data-copy"].startswith("Use analyzed audit candidate") for button in elements(report(tmp_path).read_text(encoding="utf-8"), "data-copy"))


@pytest.mark.parametrize("initialized", [False, True])
def test_gitlinks_can_be_mapped_and_track_source_changes(tmp_path: Path, initialized: bool) -> None:
    make_repo(tmp_path)
    oid = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    path = "vendor/dep"
    if initialized:
        checkout = tmp_path / path
        checkout.mkdir(parents=True)
        make_repo(checkout)
        oid = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, check=True, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"160000,{oid},{path}"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "gitlink"], cwd=tmp_path, check=True, capture_output=True)
    inventory = atlas.inventory(repo_root=tmp_path)
    assert inventory["tracked_entries"][path] == {"mode": "160000", "object_id": oid}
    mapping = map_manifest(tmp_path)
    mapping["subsystems"][1]["owned_paths"].append(path)
    publish(tmp_path, "render-report", mapping)
    before = identity(tmp_path, [path])
    if initialized:
        (tmp_path / path / "untracked.txt").write_text("outside tracked coverage", encoding="utf-8")
        assert identity(tmp_path, [path]) == before
        (tmp_path / path / "src/a.py").write_text("changed dependency", encoding="utf-8")
    else:
        changed_oid = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "update-index", "--cacheinfo", f"160000,{changed_oid},{path}"], cwd=tmp_path, check=True)
    assert identity(tmp_path, [path]) != before
    assert atlas.inventory(repo_root=tmp_path)["identity"]["tracked_content_sha256"] != inventory["identity"]["tracked_content_sha256"]
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]["freshness"]["beta"] == "changed"


@pytest.mark.parametrize("materialization", ["absent", "plain file", "symlink"])
def test_tracked_symlink_entries_do_not_require_the_target(tmp_path: Path, materialization: str) -> None:
    make_repo(tmp_path)
    path = tmp_path / "dependency-link"
    target = "missing-target"
    oid = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=target, cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"120000,{oid},{path.name}"], cwd=tmp_path, check=True)
    if materialization == "plain file":
        path.write_text(target, encoding="utf-8")
    elif materialization == "symlink":
        try:
            path.symlink_to(target)
        except OSError as exc:
            pytest.skip(f"symlink creation unavailable: {exc}")
    mapping = map_manifest(tmp_path)
    mapping["subsystems"][1]["owned_paths"].append(path.name)
    publish(tmp_path, "render-report", mapping)
    before = identity(tmp_path, [path.name])
    (tmp_path / target).write_text("not dereferenced", encoding="utf-8")
    assert identity(tmp_path, [path.name]) == before


def test_missing_tracked_entries_can_be_mapped_and_restoration_changes_identity(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "src/b.py").unlink()
    mapping = map_manifest(tmp_path)
    publish(tmp_path, "render-report", mapping)
    before = identity(tmp_path, ["src/b.py"])
    (tmp_path / "src/b.py").write_text("VALUE=2\n", encoding="utf-8")
    assert identity(tmp_path, ["src/b.py"]) != before
    atlas.refresh_report(repo_root=tmp_path, report=report(tmp_path))
    assert atlas.inspect_report(repo_root=tmp_path, report=report(tmp_path))["state"]["freshness"]["beta"] == "changed"
    with pytest.raises(atlas.ReportError, match="source path does not exist"):
        identity(tmp_path, ["never-tracked.txt"])


def test_optional_comparisons_are_safe_and_analysis_can_refine_them(tmp_path: Path) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["comparison"] = comparison('Candidate <script>alert("x")</script>')
    audit["candidates"][0]["comparison"]["before"]["nodes"][0]["label"] = '<img src=x onerror="alert(1)">'
    audit["candidates"][0]["comparison"]["before"]["edges"][0]["label"] = '</text><script>alert(2)</script>'
    publish(tmp_path, "audit-subsystem", audit)
    text = report(tmp_path).read_text(encoding="utf-8")
    assert '<script>alert("x")</script>' not in text
    assert '<img src=x onerror="alert(1)">' not in text
    assert '</text><script>alert(2)</script>' not in text
    assert 'Candidate &lt;script&gt;' in text
    assert len(elements(text, "role", "img")) == 9  # Six coverage bars, map, two comparison diagrams.
    assert len(elements(text, "marker-end")) == 2  # Map dependency and before diagram relationship.

    analysis = analysis_manifest(tmp_path, report(tmp_path))
    analysis["comparison"] = comparison("Refined data flow")
    publish(tmp_path, "analyze-candidate", analysis)
    visible = report(tmp_path).read_text(encoding="utf-8").split('<script id="audit-codebase-state"', 1)[0]
    assert "Refined data flow" in visible
    assert "Candidate &lt;script&gt;" not in visible


@pytest.mark.parametrize("invalid", ["unknown endpoint", "duplicate node", "no nodes"])
def test_comparison_relationship_errors_preserve_the_report(tmp_path: Path, invalid: str) -> None:
    make_repo(tmp_path)
    publish(tmp_path, "render-report", map_manifest(tmp_path))
    before = report(tmp_path).read_bytes()
    audit = audit_manifest(tmp_path, report(tmp_path))
    audit["candidates"][0]["comparison"] = comparison()
    graph = audit["candidates"][0]["comparison"]["before"]
    if invalid == "unknown endpoint":
        graph["edges"][0]["to"] = "missing"
    elif invalid == "duplicate node":
        graph["nodes"].append(dict(graph["nodes"][0]))
    else:
        graph["nodes"] = []
    with pytest.raises(atlas.ReportError):
        publish(tmp_path, "audit-subsystem", audit)
    assert report(tmp_path).read_bytes() == before
