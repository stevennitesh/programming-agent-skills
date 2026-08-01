from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

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
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
PREVIOUS_DONT_WRITE_BYTECODE = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    SPEC.loader.exec_module(MODULE)
finally:
    sys.dont_write_bytecode = PREVIOUS_DONT_WRITE_BYTECODE


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value: object, *, indent: int | None = 2) -> Path:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=indent),
        encoding="utf-8",
    )
    return path


def _init_repo(root: Path) -> tuple[str, str]:
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src" / "alpha.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "src" / "beta.py").write_text("VALUE = 2\n", encoding="utf-8")
    (root / "tests" / "test_alpha.py").write_text(
        "def test_alpha(): assert True\n", encoding="utf-8"
    )
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "audit@example.invalid"],
        cwd=root,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Audit Test"],
        cwd=root,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "show", "-s", "--format=%T", commit],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return commit, tree


def _report(root: Path) -> Path:
    return root / ".scratch" / "audit-codebase" / "run-001" / "report.html"


def _map_values(root: Path, *, title: str = "Repository atlas") -> dict[str, object]:
    return {
        "version": 1,
        "expected_report_sha256": "absent",
        "map_state": "complete",
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
                "name": "Alpha contracts",
                "state": "mapped",
                "source_identity": "tree-alpha-001",
                "purpose": "Own shared contracts.",
                "authority": ["CONTEXT.md"],
                "callers": ["Beta delivery"],
                "responsibility": "Validate identities.",
                "dependencies": [
                    {
                        "id": "beta",
                        "evidence": ["src/alpha.py imports the Beta contract"],
                    }
                ],
                "interfaces": ["validated identity"],
                "proof_seams": ["tests/test_alpha.py"],
                "owned_paths": ["src/alpha.py", "tests/test_alpha.py"],
            },
            {
                "id": "beta",
                "system_id": "delivery",
                "name": "Beta delivery",
                "state": "mapped",
                "source_identity": "tree-beta-001",
                "purpose": "Deliver results.",
                "authority": [],
                "callers": ["operators"],
                "responsibility": "Publish accepted results.",
                "dependencies": [],
                "interfaces": ["delivery packet"],
                "proof_seams": [],
                "owned_paths": ["src/beta.py"],
            },
        ],
        "excluded": [{ "path": ".scratch", "reason": "generated audit state" }],
        "coverage": "Every in-scope tracked file is assigned once.",
        "evidence_limits": "Runtime behavior was not executed during Map.",
        "next_selection": "Select one mapped subsystem to Audit.",
    }


def _candidate() -> dict[str, object]:
    return {
        "id": "alpha-fix",
        "title": "Centralize identity validation",
        "primary_class": "reliability",
        "member_ids": ["alpha-defect", "alpha-gap"],
        "files_modules": ["src/alpha.py"],
        "supported_behavior": "Every identity is validated.",
        "problem": "One entry path bypasses validation.",
        "evidence": ["src/alpha.py:1 routes the unchecked path."],
        "direction": "Enforce the invariant at the shared write seam.",
        "benefit": "All callers receive the same validation.",
        "safety_floors": ["Preserve accepted identity formats."],
        "required_proof": ["Negative control through both entry paths."],
        "decision_questions": [],
        "strength": "Strong",
        "strength_reason": "Direct evidence and one proof seam.",
    }


def _audit_values(report: Path, report_sha: str) -> dict[str, object]:
    lenses = []
    for name in MODULE._LENSES:
        lenses.append(
            {
                "class": name,
                "applicability": (
                    "not applicable" if name in {"domain", "performance"} else "applicable"
                ),
                "coverage": "complete",
                "evidence": [f"{name} evidence"],
                "item_ids": ["alpha-defect"] if name == "reliability" else [],
                "detailed_owner_loaded": name == "reliability",
                "reason": f"{name} was bounded by current source.",
            }
        )
    return {
        "version": 1,
        "expected_report_sha256": report_sha,
        "subsystem_id": "alpha",
        "state": "audited",
        "source_identity": "tree-alpha-002",
        "source_trace": {
            "summary": "Current source confirms one unchecked path.",
            "authority": ["CONTEXT.md"],
            "entry_points": ["validate"],
            "callers": ["Beta delivery"],
            "responsibility": "Validate identities.",
            "dependencies": ["beta"],
            "interfaces": ["validated identity"],
            "proof_seams": ["tests/test_alpha.py"],
            "scenarios": ["accepted identity", "rejected identity"],
        },
        "lenses": lenses,
        "findings": [
            {
                "id": "alpha-defect",
                "kind": "defect",
                "primary_class": "reliability",
                "title": "Unchecked identity entry path",
                "state": "active",
                "severity": "P2",
                "expectation": "Every identity is validated.",
                "location": ["src/alpha.py"],
                "evidence": ["The alternate caller writes directly."],
                "impact": "Invalid identities can cross the public interface.",
                "direction": "Move validation to the shared write seam.",
                "proof": ["Exercise both entry paths with one invalid identity."],
                "confidence": "high",
            },
            {
                "id": "alpha-gap",
                "kind": "gap",
                "primary_class": "reliability",
                "title": "Production input mix unavailable",
                "state": "active",
                "location": ["src/alpha.py"],
                "evidence": ["No production trace is repository-owned."],
                "impact": "Frequency is unknown.",
                "direction": "Re-enter with an attributable trace.",
                "proof": ["Compare the trace to supported formats."],
                "confidence": "bounded",
            },
        ],
        "candidates": [_candidate()],
        "coverage": "All six classes are complete.",
        "evidence_limits": "Production frequency remains unknown.",
        "recommendation": "Select a candidate from the report.",
        "skill_links": {
            "audit_codebase": "C:/skills/audit-codebase/SKILL.md",
            "to_tickets": "C:/skills/to-tickets/SKILL.md",
            "implement": "C:/skills/implement/SKILL.md",
        },
    }


def _candidate_digest(root: Path, report: Path) -> str:
    return str(
        MODULE.inspect_report(
            repo_root=root,
            report=report,
            objective="analyze",
            candidate_id="alpha-fix",
        )["candidate_bundle_sha256"]
    )


def _analysis_values(
    report_sha: str,
    candidate_digest: str,
    *,
    tracker_ready: bool = True,
) -> dict[str, object]:
    tracker: dict[str, object]
    if tracker_ready:
        tracker = {
            "status": "ready-graph",
            "issue_urls": ["https://github.example/issues/17"],
            "ready_issue_url": "https://github.example/issues/17",
            "candidate_bundle_sha256": candidate_digest,
            "mutation_identity": "issue-17-readback",
            "read_back": True,
        }
    else:
        tracker = {
            "status": "not-applicable",
            "issue_urls": [],
            "ready_issue_url": "",
        }
    return {
        "version": 1,
        "expected_report_sha256": report_sha,
        "candidate_id": "alpha-fix",
        "member_ids": ["alpha-defect", "alpha-gap"],
        "finding_transitions": [],
        "current_source_validity": "confirmed",
        "last_verified_identity": "tree-alpha-003",
        "source_trace": ["src/alpha.py", "tests/test_alpha.py"],
        "state": "analyzed",
        "analysis": {
            "validity_reason": "The bypass remains reachable.",
            "changed_evidence_members": [],
            "current_shape_cost": "Validation policy is split across entry paths.",
            "keep": "Retains the known bypass.",
            "smallest_sufficient_change": "Move validation to the write seam.",
            "structural_change": "Not needed.",
            "replacement": "Not applicable; incremental correction is smaller.",
            "recommended_direction": "Use the smallest sufficient change.",
            "rejected_alternatives": ["Caller-by-caller checks duplicate policy."],
            "contracts_decisions": ["Accepted identity formats remain unchanged."],
            "responsibilities_interfaces_seams": ["The shared write seam owns validation."],
            "compatibility_migration": "No stored-format migration.",
            "proof_plan": ["Negative control through both entry paths."],
            "residual_risk": "Production frequency remains unknown.",
            "decision_status": "settled",
        },
        "implementation_ready": tracker_ready,
        "tracker": tracker,
        "next_owner": {"skill": "", "reason": "", "prerequisite": "", "invocation": ""},
    }


def _prepare_and_publish(
    command: str,
    root: Path,
    report: Path,
    manifest: Path,
) -> dict[str, object]:
    prepared = MODULE.mutate_report(
        command=command,
        repo_root=root,
        report=report,
        manifest_path=manifest,
        validate_only=True,
        expected_bundle_sha256=None,
    )
    assert prepared["mutation_started"] is False
    return MODULE.mutate_report(
        command=command,
        repo_root=root,
        report=report,
        manifest_path=manifest,
        validate_only=False,
        expected_bundle_sha256=prepared["bundle_sha256"],
    )


def _cli(*arguments: str, cwd: Path, hash_seed: str | None = None) -> dict[str, object]:
    environment = os.environ.copy()
    if hash_seed is not None:
        environment["PYTHONHASHSEED"] = hash_seed
    process = subprocess.run(
        [sys.executable, str(MODULE_PATH), *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert process.returncode == 0, process.stdout
    assert process.stderr == ""
    return json.loads(process.stdout)


def _published_map(root: Path, *, indent: int | None = 2) -> Path:
    report = _report(root)
    manifest = _write(root / "map.json", _map_values(root), indent=indent)
    _prepare_and_publish("render-report", root, report, manifest)
    return report


def _published_audit(root: Path) -> Path:
    report = _published_map(root)
    manifest = _write(root / "audit.json", _audit_values(report, _digest(report)))
    _prepare_and_publish("audit-subsystem", root, report, manifest)
    return report


def _published_analysis(root: Path, *, tracker_ready: bool = True) -> Path:
    report = _published_audit(root)
    manifest = _write(
        root / "analyze.json",
        _analysis_values(
            _digest(report),
            _candidate_digest(root, report),
            tracker_ready=tracker_ready,
        ),
    )
    _prepare_and_publish("analyze-candidate", root, report, manifest)
    return report


def test_map_render_is_deterministic_and_dark(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _report(tmp_path)
    compact = _write(tmp_path / "compact.json", _map_values(tmp_path), indent=None)
    pretty = _write(tmp_path / "pretty.json", _map_values(tmp_path), indent=2)

    first = MODULE.mutate_report(
        command="render-report",
        repo_root=tmp_path,
        report=report,
        manifest_path=compact,
        validate_only=True,
        expected_bundle_sha256=None,
    )
    second = MODULE.mutate_report(
        command="render-report",
        repo_root=tmp_path,
        report=report,
        manifest_path=pretty,
        validate_only=True,
        expected_bundle_sha256=None,
    )

    assert first["report_sha256"] == second["report_sha256"]
    assert first["bundle_sha256"] == second["bundle_sha256"]
    assert not report.exists()
    published = MODULE.mutate_report(
        command="render-report",
        repo_root=tmp_path,
        report=report,
        manifest_path=compact,
        validate_only=False,
        expected_bundle_sha256=first["bundle_sha256"],
    )
    source = report.read_text(encoding="utf-8")
    assert published["effect"] == "created"
    assert 'data-theme="dark"' in source
    assert '<meta name="color-scheme" content="dark">' in source
    assert 'content="9"' in source
    assert 'data-state="mapped"' in source
    assert "mapped · 2 files" in source


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda values: values["subsystems"][1]["owned_paths"].append("src/alpha.py"),
            "owned by both",
        ),
        (
            lambda values: values["excluded"].append(
                {"path": "src/alpha.py", "reason": "wrong"}
            ),
            "duplicate ownership or exclusion",
        ),
        (
            lambda values: values["subsystems"][0]["dependencies"][0].update(
                {"evidence": []}
            ),
            "must be a list",
        ),
    ],
)
def test_map_rejects_false_ownership_claims(
    tmp_path: Path,
    mutation,
    message: str,
) -> None:
    _init_repo(tmp_path)
    values = _map_values(tmp_path)
    mutation(values)
    manifest = _write(tmp_path / "invalid.json", values)
    with pytest.raises(MODULE.ReportError, match=message):
        MODULE.mutate_report(
            command="render-report",
            repo_root=tmp_path,
            report=_report(tmp_path),
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert not _report(tmp_path).exists()


def test_complete_map_is_bound_to_inventory_and_rejects_ancestor_overlap(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    values = _map_values(tmp_path)
    values["observation_identity"] = "stale"
    manifest = _write(tmp_path / "stale.json", values)
    with pytest.raises(MODULE.ReportError, match="current tracked inventory"):
        MODULE.mutate_report(
            command="render-report",
            repo_root=tmp_path,
            report=_report(tmp_path),
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )

    values = _map_values(tmp_path)
    values["excluded"].append({"path": "src", "reason": "overbroad"})
    manifest = _write(tmp_path / "overlap.json", values)
    with pytest.raises(MODULE.ReportError, match="ancestor scope"):
        MODULE.mutate_report(
            command="render-report",
            repo_root=tmp_path,
            report=_report(tmp_path),
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_render_escapes_text_and_embedded_state(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    values = _map_values(tmp_path, title='Atlas </script><img src=x onerror="bad">')
    manifest = _write(tmp_path / "map.json", values)
    _prepare_and_publish("render-report", tmp_path, _report(tmp_path), manifest)
    source = _report(tmp_path).read_text(encoding="utf-8")
    assert "</script><img" not in source
    assert "&lt;/script&gt;&lt;img" in source
    assert "\\u003c/script\\u003e" in source
    MODULE.inspect_report(
        repo_root=tmp_path,
        report=_report(tmp_path),
        objective="map",
    )


def test_full_cli_lifecycle_derives_every_html_projection(tmp_path: Path) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)

    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )
    assert inspected["candidate"]["state"] == "analyzed"
    assert inspected["candidate"]["tracker"]["ready_issue_url"].endswith("/17")
    assert "[$implement](C:/skills/implement/SKILL.md)" in inspected["candidate"]["pickup"]
    assert "[$audit-codebase](C:/skills/audit-codebase/SKILL.md) Close" in inspected["candidate"]["pickup"]
    assert inspected["member_findings"][0]["evidence"]

    close = {
        "version": 1,
        "expected_report_sha256": _digest(report),
        "implementation_outcome": "complete",
        "report": str(report),
        "run_id": "run-001",
        "subsystem_id": "alpha",
        "candidate_id": "alpha-fix",
        "commit_identity": commit,
        "commit_tree_identity": tree,
        "current_source_result": "current",
        "accepted_proof": "focused and contract suites passed",
        "skipped_checks": "none",
        "formal_review_decision": "accepted",
        "formal_review_provenance": "change-review accepted the pinned diff",
        "repair_generations_used": 1,
        "changed_scope": "src/alpha.py",
        "change_closure": "complete",
        "residual_risk": "none",
        "last_verified_identity": "tree-alpha-003",
        "candidate_bundle_sha256": _candidate_digest(tmp_path, report),
        "tracker_mutation_identity": "issue-17-readback",
        "ready_issue_url": "https://github.example/issues/17",
        "finding_transitions": [
            {
                "finding_id": "alpha-defect",
                "state": "resolved",
                "reason": "Accepted implementation protects both entry paths.",
            },
            {
                "finding_id": "alpha-gap",
                "state": "active",
                "reason": "Production frequency remains unavailable.",
            },
        ],
    }
    manifest = _write(tmp_path / "close.json", close)
    before = report.read_bytes()
    prepared = MODULE.mutate_report(
        command="close-candidate",
        repo_root=tmp_path,
        report=report,
        manifest_path=manifest,
        validate_only=True,
        expected_bundle_sha256=None,
    )
    assert report.read_bytes() == before
    _prepare_and_publish("close-candidate", tmp_path, report, manifest)
    state = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="map",
    )["state"]
    candidate = next(item for item in state["candidates"] if item["id"] == "alpha-fix")
    findings = {item["id"]: item for item in state["findings"]}
    assert candidate["state"] == "implemented"
    assert candidate["pickup"] == ""
    assert candidate["implementation"]["commit_identity"] == commit
    assert findings["alpha-defect"]["state"] == "resolved"
    assert findings["alpha-gap"]["state"] == "active"
    assert prepared["bundle_sha256"]
    source = report.read_text(encoding="utf-8")
    assert source.count('data-candidate-id="alpha-fix"') == 1
    assert 'data-state="implemented"' in source


def test_public_cli_runs_the_same_two_phase_transaction_for_all_objectives(
    tmp_path: Path,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _report(tmp_path)
    packets: list[tuple[str, Path]] = [
        ("render-report", _write(tmp_path / "map.json", _map_values(tmp_path)))
    ]

    for index, (command, manifest) in enumerate(packets):
        prepared = _cli(
            command,
            "--repo-root",
            str(tmp_path),
            "--report",
            str(report),
            "--manifest",
            str(manifest),
            "--validate-only",
            cwd=tmp_path,
            hash_seed=str(index * 2 + 1),
        )
        assert prepared["command"] == command
        assert prepared["response_version"] == 1
        assert prepared["mutation_started"] is False
        published = _cli(
            command,
            "--repo-root",
            str(tmp_path),
            "--report",
            str(report),
            "--manifest",
            str(manifest),
            "--expected-bundle-sha256",
            str(prepared["bundle_sha256"]),
            cwd=tmp_path,
            hash_seed=str(index * 2 + 2),
        )
        assert published["report_state"] == "updated"

        if index == 0:
            packets.extend(
                [
                    (
                        "audit-subsystem",
                        _write(
                            tmp_path / "audit.json",
                            _audit_values(report, _digest(report)),
                        ),
                    )
                ]
            )
        elif index == 1:
            packets.extend(
                [
                    (
                        "analyze-candidate",
                        _write(
                            tmp_path / "analyze.json",
                            _analysis_values(
                                _digest(report),
                                _candidate_digest(tmp_path, report),
                            ),
                        ),
                    )
                ]
            )
        elif index == 2:
            packets.extend(
                [
                    (
                        "close-candidate",
                        _write(
                            tmp_path / "close.json",
                            {
                                "version": 1,
                                "expected_report_sha256": _digest(report),
                                "implementation_outcome": "complete",
                                "report": str(report),
                                "run_id": "run-001",
                                "subsystem_id": "alpha",
                                "candidate_id": "alpha-fix",
                                "commit_identity": commit,
                                "commit_tree_identity": tree,
                                "current_source_result": "current",
                                "accepted_proof": "proof",
                                "skipped_checks": "none",
                                "formal_review_decision": "accepted",
                                "formal_review_provenance": "review receipt",
                                "repair_generations_used": 0,
                                "changed_scope": "src/alpha.py",
                                "change_closure": "complete",
                                "residual_risk": "none",
                                "last_verified_identity": "tree-alpha-003",
                                "candidate_bundle_sha256": _candidate_digest(tmp_path, report),
                                "tracker_mutation_identity": "issue-17-readback",
                                "ready_issue_url": "https://github.example/issues/17",
                                "finding_transitions": [
                                    {
                                        "finding_id": "alpha-defect",
                                        "state": "resolved",
                                        "reason": "fixed",
                                    },
                                    {
                                        "finding_id": "alpha-gap",
                                        "state": "active",
                                        "reason": "still unavailable",
                                    },
                                ],
                            },
                        ),
                    )
                ]
            )

    inspected = _cli(
        "inspect",
        "--repo-root",
        str(tmp_path),
        "--report",
        str(report),
        "--objective",
        "map",
        cwd=tmp_path,
    )
    assert inspected["state"]["candidates"][0]["state"] == "implemented"


def test_audit_requires_complete_six_lens_coverage(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_map(tmp_path)
    values = _audit_values(report, _digest(report))
    values["lenses"][0]["coverage"] = "incomplete"
    manifest = _write(tmp_path / "audit.json", values)
    before = report.read_bytes()
    with pytest.raises(MODULE.ReportError, match="complete coverage for every lens"):
        MODULE.mutate_report(
            command="audit-subsystem",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert report.read_bytes() == before


def test_candidate_is_one_record_and_views_are_derived(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )
    candidate = inspected["candidate"]
    assert candidate["member_ids"] == ["alpha-defect", "alpha-gap"]
    assert "[$audit-codebase](C:/skills/audit-codebase/SKILL.md)" in candidate["pickup"]
    assert "If implementation-ready" in candidate["pickup"]
    assert "[$to-tickets](C:/skills/to-tickets/SKILL.md)" in candidate["pickup"]
    source = report.read_text(encoding="utf-8")
    assert source.count('id="candidate-alpha-fix"') == 1


def test_analyze_not_ready_has_no_implementation_pickup(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    manifest = _write(
        tmp_path / "analyze.json",
        _analysis_values(
            _digest(report),
            _candidate_digest(tmp_path, report),
            tracker_ready=False,
        ),
    )
    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)
    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )["candidate"]
    assert candidate["tracker"]["status"] == "not-applicable"
    assert candidate["implementation_ready"] is False
    assert candidate["pickup"] == ""


def test_implementation_ready_analyze_requires_to_tickets_result(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
        tracker_ready=False,
    )
    values["implementation_ready"] = True
    manifest = _write(tmp_path / "missing-tickets-result.json", values)
    with pytest.raises(MODULE.ReportError, match="requires the To Tickets result"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_implementation_ready_analyze_without_ticket_authority_returns_analyze_reentry(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
        tracker_ready=False,
    )
    values["implementation_ready"] = True
    values["tracker"] = {
        "status": "authority-required",
        "issue_urls": [],
        "ready_issue_url": "",
    }
    manifest = _write(tmp_path / "ticket-authority-required.json", values)
    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)

    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )["candidate"]
    assert candidate["implementation_ready"] is True
    assert candidate["tracker"]["status"] == "authority-required"
    assert "[$audit-codebase](C:/skills/audit-codebase/SKILL.md)" in candidate["pickup"]
    assert "If implementation-ready" in candidate["pickup"]
    assert "$implement" not in candidate["pickup"]


def test_authority_required_tracker_rejects_mutation_facts(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
        tracker_ready=False,
    )
    values["implementation_ready"] = True
    values["tracker"] = {
        "status": "authority-required",
        "issue_urls": [],
        "ready_issue_url": "",
        "mutation_identity": "must-not-exist",
    }
    manifest = _write(tmp_path / "ticket-authority-with-mutation.json", values)
    with pytest.raises(MODULE.ReportError, match="forbids tracker mutation facts"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_authority_required_tracker_requires_ready_analysis(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
        tracker_ready=False,
    )
    values["tracker"] = {
        "status": "authority-required",
        "issue_urls": [],
        "ready_issue_url": "",
    }
    manifest = _write(tmp_path / "ticket-authority-not-ready.json", values)
    with pytest.raises(MODULE.ReportError, match="requires an implementation-ready candidate"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_tracker_recovery_forbids_implement_pickup(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
    )
    values["tracker"] = {
        "status": "recovery",
        "issue_urls": ["https://github.example/issues/17"],
        "ready_issue_url": "",
        "candidate_bundle_sha256": _candidate_digest(tmp_path, report),
        "mutation_identity": "attempt-17",
        "read_back": False,
        "observed_issue_state": "Issue 17 exists but relationship read-back failed.",
    }
    manifest = _write(tmp_path / "analyze.json", values)
    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)
    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )["candidate"]
    assert candidate["tracker"]["status"] == "recovery"
    assert "$implement" not in candidate["pickup"]
    assert "$audit-codebase" in candidate["pickup"]


def test_analyze_rejects_wrong_candidate_digest_and_changed_ready_state(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(_digest(report), "a" * 64)
    manifest = _write(tmp_path / "wrong-digest.json", values)
    with pytest.raises(MODULE.ReportError, match="candidate bundle"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )

    values = _analysis_values(_digest(report), _candidate_digest(tmp_path, report))
    values["current_source_validity"] = "changed"
    manifest = _write(tmp_path / "changed-ready.json", values)
    with pytest.raises(MODULE.ReportError, match="confirmed current source"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_publication_lock_rejects_a_second_writer_without_mutation(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _report(tmp_path)
    manifest = _write(tmp_path / "map.json", _map_values(tmp_path))
    prepared = MODULE.mutate_report(
        command="render-report",
        repo_root=tmp_path,
        report=report,
        manifest_path=manifest,
        validate_only=True,
        expected_bundle_sha256=None,
    )
    report.parent.mkdir(parents=True)
    lock = report.with_name(report.name + ".lock")
    lock.write_text("held", encoding="utf-8")
    try:
        with pytest.raises(MODULE.ReportError, match="transaction lock") as caught:
            MODULE.mutate_report(
                command="render-report",
                repo_root=tmp_path,
                report=report,
                manifest_path=manifest,
                validate_only=False,
                expected_bundle_sha256=str(prepared["bundle_sha256"]),
            )
        assert caught.value.report_state == "unknown"
        assert not report.exists()
    finally:
        lock.unlink()


def test_bundle_and_report_collisions_preserve_report(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_map(tmp_path)
    manifest = _write(tmp_path / "audit.json", _audit_values(report, _digest(report)))
    prepared = MODULE.mutate_report(
        command="audit-subsystem",
        repo_root=tmp_path,
        report=report,
        manifest_path=manifest,
        validate_only=True,
        expected_bundle_sha256=None,
    )
    before = report.read_bytes()
    with pytest.raises(MODULE.ReportError, match="publication bundle collision"):
        MODULE.mutate_report(
            command="audit-subsystem",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=False,
            expected_bundle_sha256="0" * 64,
        )
    assert report.read_bytes() == before
    values = _audit_values(report, "0" * 64)
    _write(manifest, values)
    with pytest.raises(MODULE.ReportError, match="report collision"):
        MODULE.mutate_report(
            command="audit-subsystem",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert prepared["report_unchanged"] is True
    assert report.read_bytes() == before


def test_report_tampering_and_unsupported_version_are_rejected(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_map(tmp_path)
    source = report.read_text(encoding="utf-8")
    report.write_text(source.replace("Repository atlas", "Changed", 1), encoding="utf-8")
    with pytest.raises(MODULE.ReportError, match="canonical projection"):
        MODULE.inspect_report(repo_root=tmp_path, report=report, objective="map")

    report.write_text(source.replace('content="9"', 'content="8"'), encoding="utf-8")
    with pytest.raises(MODULE.ReportError, match="version 9 is required"):
        MODULE.inspect_report(repo_root=tmp_path, report=report, objective="map")


def test_schema_and_cli_errors_are_one_json_document(tmp_path: Path) -> None:
    schema = MODULE._schema("audit")
    assert schema["response_version"] == 1
    assert len(schema["template"]["lenses"]) == 6

    process = subprocess.run(
        [sys.executable, str(MODULE_PATH), "inspect", "--unknown"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 2
    assert process.stderr == ""
    payload = json.loads(process.stdout)
    assert payload == {
        "command": "inspect",
        "error": "the following arguments are required: --repo-root, --report, --objective",
        "mutation_started": False,
        "ok": False,
        "report_state": "unchanged",
        "report_unchanged": True,
        "response_version": 1,
        "stage": "arguments",
    }


@pytest.mark.parametrize(
    "command",
    ["render-report", "audit-subsystem", "analyze-candidate", "close-candidate"],
)
def test_mutation_commands_share_one_transaction_interface(command: str) -> None:
    parser = MODULE._parser()
    help_text = parser.format_help()
    assert command in help_text
    subparser = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    ).choices[command]
    options = {option for action in subparser._actions for option in action.option_strings}
    assert {"--manifest", "--validate-only", "--expected-bundle-sha256"} <= options


def test_source_identity_is_sorted_and_object_sensitive(tmp_path: Path) -> None:
    commit, _ = _init_repo(tmp_path)
    path_list = tmp_path / "paths.txt"
    path_list.write_text("src/beta.py\nsrc/alpha.py\n", encoding="utf-8")
    live = MODULE.source_identity(repo_root=tmp_path, path_list=path_list)
    frozen = MODULE.source_identity(
        repo_root=tmp_path,
        path_list=path_list,
        git_object=commit,
    )
    assert live["paths"] == ["src/alpha.py", "src/beta.py"]
    assert live["identity"] != frozen["identity"]
    (tmp_path / "src" / "alpha.py").write_text("VALUE = 3\n", encoding="utf-8")
    changed = MODULE.source_identity(repo_root=tmp_path, path_list=path_list)
    assert changed["identity"] != frozen["identity"]


def test_close_rejects_unreachable_commit_and_incomplete_transitions(
    tmp_path: Path,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    values = {
        "version": 1,
        "expected_report_sha256": _digest(report),
        "implementation_outcome": "complete",
        "report": str(report),
        "run_id": "run-001",
        "subsystem_id": "alpha",
        "candidate_id": "alpha-fix",
        "commit_identity": commit,
        "commit_tree_identity": tree,
        "current_source_result": "current",
        "accepted_proof": "proof",
        "skipped_checks": "none",
        "formal_review_decision": "accepted",
        "formal_review_provenance": "review receipt",
        "repair_generations_used": 0,
        "changed_scope": "src/alpha.py",
        "change_closure": "complete",
        "residual_risk": "none",
        "last_verified_identity": "tree-alpha-003",
        "candidate_bundle_sha256": _candidate_digest(tmp_path, report),
        "tracker_mutation_identity": "issue-17-readback",
        "ready_issue_url": "https://github.example/issues/17",
        "finding_transitions": [],
    }
    manifest = _write(tmp_path / "close.json", values)
    before = report.read_bytes()
    with pytest.raises(MODULE.ReportError, match="every active candidate finding"):
        MODULE.mutate_report(
            command="close-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert report.read_bytes() == before


def test_close_rejects_analyzed_candidate_without_ready_tracker(tmp_path: Path) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path, tracker_ready=False)
    values = {
        "version": 1,
        "expected_report_sha256": _digest(report),
        "implementation_outcome": "complete",
        "report": str(report),
        "run_id": "run-001",
        "subsystem_id": "alpha",
        "candidate_id": "alpha-fix",
        "candidate_bundle_sha256": _candidate_digest(tmp_path, report),
        "tracker_mutation_identity": "not-published",
        "ready_issue_url": "https://github.example/issues/17",
        "commit_identity": commit,
        "commit_tree_identity": tree,
        "current_source_result": "current",
        "accepted_proof": "proof",
        "skipped_checks": "none",
        "formal_review_decision": "accepted",
        "formal_review_provenance": "review receipt",
        "repair_generations_used": 0,
        "changed_scope": "src/alpha.py",
        "change_closure": "complete",
        "residual_risk": "none",
        "last_verified_identity": "tree-alpha-003",
        "finding_transitions": [
            {"finding_id": "alpha-defect", "state": "resolved", "reason": "fixed"},
            {"finding_id": "alpha-gap", "state": "active", "reason": "unknown"},
        ],
    }
    manifest = _write(tmp_path / "close-not-ready.json", values)
    with pytest.raises(MODULE.ReportError, match="implementation-ready tracker frontier"):
        MODULE.mutate_report(
            command="close-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
