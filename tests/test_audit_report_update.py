from __future__ import annotations

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
        "version": MODULE.MANIFEST_VERSION,
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
        "version": MODULE.MANIFEST_VERSION,
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
        "version": MODULE.MANIFEST_VERSION,
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
        "tracker": tracker,
        "next_owner": {"skill": "", "reason": "", "prerequisite": "", "invocation": ""},
    }


def _close_values(
    root: Path,
    report: Path,
    commit: str,
    tree: str,
    *,
    completion_route: str = "tracker-frontier",
    reviewed: bool = False,
) -> dict[str, object]:
    values: dict[str, object] = {
        "version": MODULE.MANIFEST_VERSION,
        "expected_report_sha256": _digest(report),
        "completion_route": completion_route,
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
        "changed_scope": "src/alpha.py",
        "change_closure": "complete",
        "residual_risk": "none",
        "last_verified_identity": "tree-alpha-003",
        "candidate_bundle_sha256": _candidate_digest(root, report),
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
    if reviewed:
        values |= {
            "formal_review_decision": "accepted",
            "formal_review_provenance": "change-review accepted the pinned diff",
        }
    if completion_route == "tracker-frontier":
        values |= {
            "tracker_mutation_identity": "issue-17-readback",
            "ready_issue_url": "https://github.example/issues/17",
        }
    else:
        values["direct_implementation_authority"] = (
            "current user authorized this exact direct implementation before landing"
        )
    return values


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


def _published_analysis(
    root: Path,
    *,
    tracker_status: str = "ready-graph",
) -> Path:
    report = _published_audit(root)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(root, report),
        tracker_ready=tracker_status == "ready-graph",
    )
    if tracker_status == "authority-required":
        values["tracker"] = {
            "status": "authority-required",
            "issue_urls": [],
            "ready_issue_url": "",
        }
    elif tracker_status != "ready-graph" and tracker_status != "not-applicable":
        raise AssertionError(f"unsupported test tracker status: {tracker_status}")
    manifest = _write(root / "analyze.json", values)
    _prepare_and_publish("analyze-candidate", root, report, manifest)
    return report


def _local_markdown_graph(
    root: Path,
    candidate_digest: str,
    *,
    status: str = "ready-for-agent",
    blocked_by: str = "none",
    claimed_by: str | None = None,
    implementation_notes: str | None = None,
) -> dict[str, object]:
    parent_ref = ".scratch/alpha-fix/SPEC.md"
    issue_ref = ".scratch/alpha-fix/issues/01-alpha-fix.md"
    parent = root / parent_ref
    issue = root / issue_ref
    issue.parent.mkdir(parents=True, exist_ok=True)
    parent.write_text(
        "\n".join(
            (
                "# Alpha Fix",
                "",
                "Status: needs-triage",
                "",
                "## Settled Source",
                "",
                "- Candidate: `alpha-fix`",
                f"- Candidate bundle SHA-256: `{candidate_digest}`",
                "",
                "## Ordered Implementation Graph",
                "",
                "1. [`01-alpha-fix.md`](issues/01-alpha-fix.md)",
                "",
            )
        ),
        encoding="utf-8",
    )
    issue_lines = [
        "# Alpha Fix",
        "",
        "Category: bug",
        f"Status: {status}",
        "Parent: ../SPEC.md",
        f"Blocked by: {blocked_by}",
    ]
    if claimed_by is not None:
        issue_lines.append(f"Claimed by: {claimed_by}")
    issue_lines.extend(
        (
            "",
            "## Intent",
            "",
            f"Implement candidate `alpha-fix` with bundle `{candidate_digest}`.",
            "",
            "## Delivery",
            "",
            "- Ready state after publication verification: `ready-for-agent`.",
        )
    )
    if implementation_notes is not None:
        issue_lines.extend(("", "## Implementation Notes", "", implementation_notes))
    issue.write_text("\n".join(issue_lines) + "\n", encoding="utf-8")
    return {
        "status": "ready-graph",
        "issue_urls": [],
        "ready_issue_url": "",
        "provider": "local-markdown",
        "parent_ref": parent_ref,
        "issue_refs": [issue_ref],
        "ready_issue_ref": issue_ref,
        "readiness": "ready-for-agent",
        "blockers": [],
        "claim_state": "unclaimed",
        "frontier": [issue_ref],
        "candidate_bundle_sha256": candidate_digest,
        "mutation_identity": "local-graph-readback-001",
        "read_back": True,
    }


def _https_only_local_recovery(candidate_digest: str) -> dict[str, object]:
    return {
        "status": "recovery",
        "issue_urls": [],
        "ready_issue_url": "",
        "candidate_bundle_sha256": candidate_digest,
        "mutation_identity": "local-graph-readback-001",
        "observed_issue_state": (
            "Publication recovery: local Markdown graph alpha-fix read back with "
            "one unclaimed ready-for-agent child, no blockers, and frontier 01. "
            "The audit Analyze schema requires an absolute HTTPS ready_issue_url, "
            "but the configured tracker supplies only local repository paths; no "
            "truthful hosted URL exists, so the graph cannot be recorded as ready-graph."
        ),
    }


def _commit_local_markdown_completion(
    root: Path,
    candidate_digest: str,
) -> tuple[str, str]:
    _local_markdown_graph(
        root,
        candidate_digest,
        status="implemented",
        implementation_notes="Proof and accepted review read back.",
    )
    (root / "src" / "alpha.py").write_text("VALUE = 3\n", encoding="utf-8")
    subprocess.run(["git", "add", "src/alpha.py"], cwd=root, check=True)
    subprocess.run(["git", "add", "-f", ".scratch/alpha-fix"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "implement alpha fix"], cwd=root, check=True)
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


def _local_close_values(
    root: Path,
    report: Path,
    commit: str,
    tree: str,
    completion_digest: str,
    *,
    route: str = "tracker-frontier",
) -> dict[str, object]:
    values = _close_values(root, report, commit, tree)
    values["completion_route"] = route
    values.pop("ready_issue_url")
    values["tracker_mutation_identity"] = "local-graph-readback-001"
    return values | {
        "tracker_provider": "local-markdown",
        "parent_ref": ".scratch/alpha-fix/SPEC.md",
        "issue_refs": [".scratch/alpha-fix/issues/01-alpha-fix.md"],
        "ready_issue_ref": ".scratch/alpha-fix/issues/01-alpha-fix.md",
        "tracker_completion_sha256": completion_digest,
    }


def _write_invalid_canonical_state(report: Path, state: dict[str, object]) -> None:
    validator = MODULE._validate_state
    try:
        MODULE._validate_state = lambda value: None
        invalid_report = MODULE._render_html(state)
    finally:
        MODULE._validate_state = validator
    report.write_bytes(invalid_report)


def test_map_render_is_deterministic_and_dark(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _report(tmp_path)
    compact = _write(tmp_path / "compact.json", _map_values(tmp_path), indent=None)
    reordered = _map_values(tmp_path)
    reordered["title"] = "  Repository atlas  "
    reordered["systems"].reverse()
    reordered["subsystems"].reverse()
    pretty = _write(tmp_path / "pretty.json", reordered, indent=2)

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
    assert 'content="10"' in source
    assert 'data-state="mapped"' in source


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
        (
            lambda values: values["subsystems"][0].update({"state": "audited"}),
            "unknown fields: state",
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
                            _close_values(tmp_path, report, commit, tree),
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
    state = inspected["state"]
    candidate = state["candidates"][0]
    findings = {item["id"]: item for item in state["findings"]}
    assert candidate["state"] == "implemented"
    assert candidate["pickup"] == ""
    assert candidate["implementation"]["commit_identity"] == commit
    assert findings["alpha-defect"]["state"] == "resolved"
    assert findings["alpha-gap"]["state"] == "active"
    assert "Completion Route" not in report.read_text(encoding="utf-8")
    persisted = MODULE._load_report(tmp_path, report)[3]["candidates"][0]
    assert persisted["history"][-1]["member_ids"] == ["alpha-defect", "alpha-gap"]
    assert persisted["history"][-1]["tracker"]["status"] == "ready-graph"
    source = report.read_text(encoding="utf-8")
    assert source.count('data-candidate-id="alpha-fix"') == 1
    assert 'data-state="implemented"' in source
    assert "Formal Review Decision" not in source
    assert "Repair Generations Used" not in source


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


def test_candidate_is_one_record_and_projections_are_derived(tmp_path: Path) -> None:
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
    assert candidate["pickup"] == ""


def test_analyze_publishes_verified_local_markdown_ready_graph(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    values = _analysis_values(_digest(report), candidate_digest)
    values["tracker"] = _local_markdown_graph(tmp_path, candidate_digest)
    manifest = _write(tmp_path / "analyze-local.json", values)

    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)

    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )["candidate"]
    assert candidate["tracker"]["provider"] == "local-markdown"
    assert candidate["tracker"]["graph_sha256"]
    assert candidate["tracker"]["frontier"] == [
        ".scratch/alpha-fix/issues/01-alpha-fix.md"
    ]
    assert "tracker item .scratch/alpha-fix/issues/01-alpha-fix.md" in candidate["pickup"]
    assert "Ready tracker item identity" in candidate["pickup"]
    assert "Ready issue URL" not in candidate["pickup"]
    assert "https://" not in candidate["pickup"]


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("missing", "missing or escapes"),
        ("wrong-digest", "does not match the selected candidate"),
        ("blocked", "frontier does not match"),
        ("claimed", "frontier does not match"),
        ("not-ready", "frontier does not match"),
    ],
)
def test_local_markdown_analyze_rejects_unverified_graph_without_writing(
    tmp_path: Path,
    fault: str,
    message: str,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    tracker = _local_markdown_graph(tmp_path, candidate_digest)
    if fault == "missing":
        (tmp_path / str(tracker["ready_issue_ref"])).unlink()
    elif fault == "wrong-digest":
        for ref in (tracker["parent_ref"], tracker["ready_issue_ref"]):
            path = tmp_path / str(ref)
            path.write_text(
                path.read_text(encoding="utf-8").replace(candidate_digest, "0" * 64),
                encoding="utf-8",
            )
    elif fault == "blocked":
        _local_markdown_graph(tmp_path, candidate_digest, blocked_by="99")
    elif fault == "claimed":
        _local_markdown_graph(tmp_path, candidate_digest, claimed_by="worker")
    else:
        _local_markdown_graph(tmp_path, candidate_digest, status="needs-triage")
    values = _analysis_values(_digest(report), candidate_digest)
    values["tracker"] = tracker
    manifest = _write(tmp_path / f"analyze-local-{fault}.json", values)
    before = report.read_bytes()

    with pytest.raises(MODULE.ReportError, match=message):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )

    assert report.read_bytes() == before


def test_local_markdown_refs_must_be_contained_repository_paths(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    with pytest.raises(MODULE.ReportError, match="contained .scratch relative path"):
        MODULE._contained_local_markdown_ref(tmp_path, "../SPEC.md", "tracker ref")


def test_local_markdown_rejects_duplicate_numeric_issue_identity(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    tracker = _local_markdown_graph(tmp_path, candidate_digest)
    first_ref = str(tracker["ready_issue_ref"])
    second_ref = ".scratch/alpha-fix/issues/01-alpha-fix-copy.md"
    (tmp_path / second_ref).write_bytes((tmp_path / first_ref).read_bytes())
    parent = tmp_path / str(tracker["parent_ref"])
    parent.write_text(
        parent.read_text(encoding="utf-8").replace(
            "1. [`01-alpha-fix.md`](issues/01-alpha-fix.md)",
            "1. [`01-alpha-fix.md`](issues/01-alpha-fix.md)\n"
            "2. [`01-alpha-fix-copy.md`](issues/01-alpha-fix-copy.md)",
        ),
        encoding="utf-8",
    )
    tracker["issue_refs"] = [first_ref, second_ref]
    tracker["ready_issue_ref"] = second_ref
    tracker["frontier"] = [second_ref]
    values = _analysis_values(_digest(report), candidate_digest)
    values["tracker"] = tracker
    manifest = _write(tmp_path / "analyze-duplicate-local-id.json", values)

    with pytest.raises(MODULE.ReportError, match="duplicate numeric stable identity"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )


def test_local_markdown_ready_graph_requires_committed_closeout_before_close(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    values = _analysis_values(_digest(report), candidate_digest)
    values["tracker"] = _local_markdown_graph(tmp_path, candidate_digest)
    manifest = _write(tmp_path / "analyze-local.json", values)
    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)

    with pytest.raises(MODULE.ReportError, match="not implemented"):
        MODULE.inspect_report(
            repo_root=tmp_path,
            report=report,
            objective="close",
            candidate_id="alpha-fix",
        )

    _local_markdown_graph(
        tmp_path,
        candidate_digest,
        status="implemented",
    )
    with pytest.raises(MODULE.ReportError, match="incomplete closeout"):
        MODULE.inspect_report(
            repo_root=tmp_path,
            report=report,
            objective="close",
            candidate_id="alpha-fix",
        )
    commit, tree = _commit_local_markdown_completion(tmp_path, candidate_digest)
    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="close",
        candidate_id="alpha-fix",
    )
    assert inspected["completion_route"] == "tracker-frontier"
    close_values = _local_close_values(
        tmp_path,
        report,
        commit,
        tree,
        inspected["tracker_completion_sha256"],
    )
    close_manifest = _write(tmp_path / "close-local.json", close_values)

    wrong_mutation = dict(close_values)
    wrong_mutation["tracker_mutation_identity"] = "changed-readback"
    wrong_manifest = _write(tmp_path / "close-local-wrong-mutation.json", wrong_mutation)
    with pytest.raises(MODULE.ReportError, match="mutation identity"):
        MODULE.mutate_report(
            command="close-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=wrong_manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )

    issue = tmp_path / ".scratch/alpha-fix/issues/01-alpha-fix.md"
    issue.write_text(
        issue.read_text(encoding="utf-8") + "Uncommitted closeout drift.\n",
        encoding="utf-8",
    )
    with pytest.raises(MODULE.ReportError, match="not exact in the implementation commit"):
        MODULE.mutate_report(
            command="close-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=close_manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    _local_markdown_graph(
        tmp_path,
        candidate_digest,
        status="implemented",
        implementation_notes="Proof and accepted review read back.",
    )

    _prepare_and_publish("close-candidate", tmp_path, report, close_manifest)

    candidate = MODULE._load_report(tmp_path, report)[3]["candidates"][0]
    assert candidate["state"] == "implemented"
    assert candidate["implementation"]["tracker_completion_sha256"] == inspected[
        "tracker_completion_sha256"
    ]


def test_fresh_analyze_rejects_https_only_local_markdown_recovery_shape(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    values = _analysis_values(_digest(report), candidate_digest)
    values["tracker"] = _https_only_local_recovery(candidate_digest)
    manifest = _write(tmp_path / "analyze-forged-recovery.json", values)
    before = report.read_bytes()

    with pytest.raises(MODULE.ReportError, match="must record Local Markdown directly"):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )

    assert report.read_bytes() == before


def test_existing_https_only_local_markdown_recovery_closes_without_remap(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    candidate_digest = _candidate_digest(tmp_path, report)
    _local_markdown_graph(tmp_path, candidate_digest)
    values = _analysis_values(_digest(report), candidate_digest)
    legacy_tracker = _https_only_local_recovery(candidate_digest)
    values["tracker"] = {
        "status": "recovery",
        "issue_urls": [],
        "ready_issue_url": "",
        "candidate_bundle_sha256": candidate_digest,
        "mutation_identity": "local-graph-readback-001",
        "observed_issue_state": "Legacy fixture publication requires persisted-state repair.",
    }
    analyze_manifest = _write(tmp_path / "analyze-recovery.json", values)
    _prepare_and_publish("analyze-candidate", tmp_path, report, analyze_manifest)
    legacy_state = MODULE._load_report(tmp_path, report)[3]
    legacy_state["candidates"][0]["tracker"] = legacy_tracker
    report.write_bytes(MODULE._render_html(legacy_state))

    commit, tree = _commit_local_markdown_completion(tmp_path, candidate_digest)

    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="close",
        candidate_id="alpha-fix",
    )
    assert inspected["completion_route"] == "local-markdown-recovery"
    close_values = _local_close_values(
        tmp_path,
        report,
        commit,
        tree,
        inspected["tracker_completion_sha256"],
        route="local-markdown-recovery",
    )
    close_manifest = _write(tmp_path / "close-recovery.json", close_values)

    _prepare_and_publish("close-candidate", tmp_path, report, close_manifest)

    candidate = MODULE._load_report(tmp_path, report)[3]["candidates"][0]
    assert candidate["state"] == "implemented"
    assert candidate["tracker"]["status"] == "ready-graph"
    assert candidate["tracker"]["provider"] == "local-markdown"
    assert any(item["tracker"]["status"] == "recovery" for item in candidate["history"])


def test_close_invalid_selection_does_not_fall_back_to_another_candidate(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path)
    report = _published_analysis(tmp_path)

    with pytest.raises(MODULE.ReportError, match="candidate not found: missing-candidate"):
        MODULE.inspect_report(
            repo_root=tmp_path,
            report=report,
            objective="close",
            candidate_id="missing-candidate",
        )


def test_analyze_without_ticket_authority_returns_analyze_reentry(
    tmp_path: Path,
) -> None:
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
    manifest = _write(tmp_path / "ticket-authority-required.json", values)
    _prepare_and_publish("analyze-candidate", tmp_path, report, manifest)

    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="analyze",
        candidate_id="alpha-fix",
    )["candidate"]
    assert candidate["tracker"]["status"] == "authority-required"
    assert "[$audit-codebase](C:/skills/audit-codebase/SKILL.md)" in candidate["pickup"]
    assert "If implementation-ready" in candidate["pickup"]
    assert "$implement" not in candidate["pickup"]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda tracker: tracker.update({"mutation_identity": "must-not-exist"}),
        lambda tracker: tracker.update(
            {"issue_urls": ["https://github.example/issues/fabricated"]}
        ),
        lambda tracker: tracker.update(
            {"ready_issue_url": "https://github.example/issues/fabricated"}
        ),
    ],
)
def test_authority_required_tracker_rejects_tracker_facts(
    tmp_path: Path,
    mutation,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    values = _analysis_values(
        _digest(report),
        _candidate_digest(tmp_path, report),
        tracker_ready=False,
    )
    tracker = {
        "status": "authority-required",
        "issue_urls": [],
        "ready_issue_url": "",
    }
    mutation(tracker)
    values["tracker"] = tracker
    manifest = _write(tmp_path / "ticket-authority-with-facts.json", values)
    before = report.read_bytes()
    with pytest.raises(
        MODULE.ReportError,
        match="forbids tracker mutation fields or issues",
    ):
        MODULE.mutate_report(
            command="analyze-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert report.read_bytes() == before


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
    with pytest.raises(MODULE.ReportError, match="no admissible Close completion route"):
        MODULE.inspect_report(
            repo_root=tmp_path,
            report=report,
            objective="close",
            candidate_id="alpha-fix",
        )
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

    report.write_text(source.replace('content="10"', 'content="9"'), encoding="utf-8")
    with pytest.raises(MODULE.ReportError, match="version 10 is required"):
        MODULE.inspect_report(repo_root=tmp_path, report=report, objective="map")

    state = MODULE._normalize_map_manifest(
        _map_values(tmp_path),
        tmp_path,
        report,
    )
    state["subsystems"][0]["retired_field"] = True
    with pytest.raises(MODULE.ReportError, match="unknown fields: retired_field"):
        MODULE._validate_state(state)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda state: state.update({"state_version": 1}), "requires version 2"),
        (
            lambda state: state["findings"][0].update({"kind": "legacy-kind"}),
            "unsupported kind or state",
        ),
    ],
)
def test_public_inspect_rejects_retired_or_invalid_canonical_state(
    tmp_path: Path,
    mutation,
    message: str,
) -> None:
    _init_repo(tmp_path)
    report = _published_audit(tmp_path)
    state = MODULE._load_report(tmp_path, report)[3]
    mutation(state)
    _write_invalid_canonical_state(report, state)
    with pytest.raises(MODULE.ReportError, match=message):
        MODULE.inspect_report(repo_root=tmp_path, report=report, objective="map")


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda candidate: (
                candidate["tracker"].update(
                    {
                        "status": "recovery",
                        "observed_issue_state": "relationship read-back failed",
                    }
                ),
                candidate["tracker"].pop("read_back"),
            ),
            "no valid completion route",
        ),
        (
            lambda candidate: candidate["implementation"].update(
                {"formal_review_decision": "rejected"}
            ),
            "supplied review must be accepted",
        ),
        (
            lambda candidate: candidate["implementation"].update(
                {"commit_tree_identity": "invalid"}
            ),
            "invalid commit or tree identity",
        ),
    ],
)
def test_public_inspect_rejects_invalid_implementation_state(
    tmp_path: Path,
    mutation,
    message: str,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    manifest = _write(
        tmp_path / "close.json",
        _close_values(
            tmp_path,
            report,
            commit,
            tree,
            # Exercise persisted validation of the activated review branch.
            reviewed=True,
        ),
    )
    _prepare_and_publish("close-candidate", tmp_path, report, manifest)
    state = MODULE._load_report(tmp_path, report)[3]
    mutation(state["candidates"][0])
    _write_invalid_canonical_state(report, state)
    with pytest.raises(MODULE.ReportError, match=message):
        MODULE.inspect_report(repo_root=tmp_path, report=report, objective="map")


def test_all_objectives_reject_retired_manifest_version(tmp_path: Path) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    packets = [
        (
            "Map",
            _map_values(tmp_path),
            lambda value: MODULE._normalize_map_manifest(value, tmp_path, report),
        ),
        (
            "Audit",
            _audit_values(report, _digest(report)),
            lambda value: MODULE._normalize_audit_manifest(value, report),
        ),
        (
            "Analyze",
            _analysis_values(
                _digest(report),
                _candidate_digest(tmp_path, report),
            ),
            MODULE._normalize_analyze_manifest,
        ),
        (
            "Close",
            _close_values(tmp_path, report, commit, tree),
            MODULE._normalize_close_manifest,
        ),
    ]
    for objective, packet, normalize in packets:
        packet["version"] = 1
        with pytest.raises(MODULE.ReportError, match=f"{objective} manifest requires version 4"):
            normalize(packet)


def test_schema_and_cli_errors_are_one_json_document(tmp_path: Path) -> None:
    schema = MODULE._schema("audit")
    assert schema["response_version"] == 1
    assert schema["template"]["version"] == MODULE.MANIFEST_VERSION == 4
    assert MODULE.STATE_VERSION == 2
    assert len(schema["template"]["lenses"]) == 6
    tracker_close = MODULE._schema("close", "tracker-frontier")["template"]
    reviewed_tracker_close = MODULE._schema(
        "close", "tracker-frontier", reviewed=True
    )["template"]
    local_analyze = MODULE._schema("analyze", tracker_provider="local-markdown")[
        "template"
    ]
    local_close = MODULE._schema(
        "close", "tracker-frontier", "local-markdown"
    )["template"]
    recovery_close = MODULE._schema("close", "local-markdown-recovery")["template"]
    direct_close = MODULE._schema("close", "authorized-direct-recovery")["template"]
    assert tracker_close["completion_route"] == "tracker-frontier"
    assert "tracker_mutation_identity" in tracker_close
    assert "direct_implementation_authority" not in tracker_close
    assert "formal_review_decision" not in tracker_close
    assert "formal_review_provenance" not in tracker_close
    assert reviewed_tracker_close["formal_review_decision"] == "accepted"
    assert reviewed_tracker_close["formal_review_provenance"] == ""
    assert "repair_generations_used" not in reviewed_tracker_close
    assert local_analyze["tracker"]["provider"] == "local-markdown"
    assert "ready_issue_ref" in local_analyze["tracker"]
    assert local_close["tracker_provider"] == "local-markdown"
    assert "ready_issue_ref" in local_close
    assert "ready_issue_url" not in local_close
    assert recovery_close["completion_route"] == "local-markdown-recovery"
    assert recovery_close["tracker_provider"] == "local-markdown"
    assert direct_close["completion_route"] == "authorized-direct-recovery"
    assert "direct_implementation_authority" in direct_close
    assert "tracker_mutation_identity" not in direct_close
    assert "ready_issue_url" not in direct_close
    assert _cli(
        "schema",
        "--objective",
        "close",
        "--completion-route",
        "tracker-frontier",
        "--reviewed",
        cwd=tmp_path,
    )["template"] == reviewed_tracker_close
    assert _cli(
        "schema",
        "--objective",
        "close",
        "--completion-route",
        "authorized-direct-recovery",
        cwd=tmp_path,
    )["template"] == direct_close
    assert _cli(
        "schema",
        "--objective",
        "analyze",
        "--tracker-provider",
        "local-markdown",
        cwd=tmp_path,
    )["template"] == local_analyze

    process = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "schema",
            "--objective",
            "analyze",
            "--reviewed",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 2
    assert process.stderr == ""
    assert json.loads(process.stdout)["error"] == "reviewed applies only to Close schema"


def test_close_accepts_legacy_manifest_repair_count_without_persisting_it(
    tmp_path: Path,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    values = _close_values(tmp_path, report, commit, tree)
    values["repair_generations_used"] = 1
    manifest = _write(tmp_path / "close-legacy.json", values)

    _prepare_and_publish("close-candidate", tmp_path, report, manifest)

    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="map",
    )["state"]["candidates"][0]
    assert candidate["state"] == "implemented"
    assert "repair_generations_used" not in candidate["implementation"]


def test_inspect_accepts_legacy_report_repair_count(tmp_path: Path) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    manifest = _write(
        tmp_path / "close.json",
        _close_values(tmp_path, report, commit, tree),
    )
    _prepare_and_publish("close-candidate", tmp_path, report, manifest)
    state = MODULE._load_report(tmp_path, report)[3]
    state["candidates"][0]["implementation"]["repair_generations_used"] = 1
    _write_invalid_canonical_state(report, state)

    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="map",
    )

    assert inspected["state"]["candidates"][0]["implementation"][
        "repair_generations_used"
    ] == 1
    with pytest.raises(MODULE.ReportError, match="applies only to Analyze or Close"):
        MODULE._schema("map", tracker_provider="local-markdown")
    with pytest.raises(MODULE.ReportError, match="requires one completion_route"):
        MODULE._schema("close")

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


def test_source_identity_is_sorted_and_live_content_sensitive(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    path_list = tmp_path / "paths.txt"
    path_list.write_text("src/beta.py\nsrc/alpha.py\n", encoding="utf-8")
    initial = MODULE.source_identity(repo_root=tmp_path, path_list=path_list)
    assert initial["paths"] == ["src/alpha.py", "src/beta.py"]
    assert initial["mode"] == "live-worktree"
    (tmp_path / "src" / "alpha.py").write_text("VALUE = 3\n", encoding="utf-8")
    changed = MODULE.source_identity(repo_root=tmp_path, path_list=path_list)
    assert changed["identity"] != initial["identity"]


def test_close_rejects_incomplete_transitions(
    tmp_path: Path,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path)
    values = _close_values(tmp_path, report, commit, tree)
    values["finding_transitions"] = []
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


@pytest.mark.parametrize("tracker_status", ["authority-required", "not-applicable"])
def test_authorized_direct_recovery_closes_without_a_tracker_frontier(
    tmp_path: Path,
    tracker_status: str,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path, tracker_status=tracker_status)
    inspected = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="close",
        candidate_id="alpha-fix",
    )
    assert inspected["completion_route"] == "authorized-direct-recovery"
    manifest = _write(
        tmp_path / "close-direct.json",
        _close_values(
            tmp_path,
            report,
            commit,
            tree,
            completion_route="authorized-direct-recovery",
        ),
    )
    _prepare_and_publish("close-candidate", tmp_path, report, manifest)
    candidate = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        objective="map",
    )["state"]["candidates"][0]
    assert candidate["state"] == "implemented"
    assert candidate["tracker"] == {
        "status": tracker_status,
        "issue_urls": [],
        "ready_issue_url": "",
    }
    assert "direct_implementation_authority" in candidate["implementation"]
    assert "Completion Route</dt><dd>authorized-direct-recovery" in report.read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize(
    ("completion_route", "tracker_status", "mutation", "message"),
    [
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"formal_review_decision": "accepted"}),
            "review decision and provenance must be supplied together",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update(
                {"formal_review_provenance": "change-review accepted the pinned diff"}
            ),
            "review decision and provenance must be supplied together",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update(
                {
                    "tracker_mutation_identity": "fabricated",
                    "ready_issue_url": "https://github.example/issues/retroactive",
                }
            ),
            "forbids tracker fields",
        ),
        (
            "tracker-frontier",
            "ready-graph",
            lambda values: values.update(
                {"direct_implementation_authority": "wrong route"}
            ),
            "mixed or incomplete tracker identity fields",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"candidate_bundle_sha256": "0" * 64}),
            "candidate bundle identity",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"commit_tree_identity": "0" * 40}),
            "commit tree identity",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"accepted_proof": ""}),
            "Close accepted_proof must be a non-empty string",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update(
                {
                    "formal_review_decision": "rejected",
                    "formal_review_provenance": "change-review rejected the pinned diff",
                }
            ),
            "supplied review must be accepted",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"repair_generations_used": -1}),
            "legacy repair_generations_used must be a non-negative integer",
        ),
        (
            "authorized-direct-recovery",
            "authority-required",
            lambda values: values.update({"candidate_ids": ["alpha-fix"]}),
            "unknown fields: candidate_ids",
        ),
    ],
)
def test_close_routes_preserve_packet_and_completion_gates(
    tmp_path: Path,
    completion_route: str,
    tracker_status: str,
    mutation,
    message: str,
) -> None:
    commit, tree = _init_repo(tmp_path)
    report = _published_analysis(tmp_path, tracker_status=tracker_status)
    values = _close_values(
        tmp_path,
        report,
        commit,
        tree,
        completion_route=completion_route,
    )
    mutation(values)
    manifest = _write(tmp_path / "close-direct-invalid.json", values)
    before = report.read_bytes()
    with pytest.raises(MODULE.ReportError, match=message):
        MODULE.mutate_report(
            command="close-candidate",
            repo_root=tmp_path,
            report=report,
            manifest_path=manifest,
            validate_only=True,
            expected_bundle_sha256=None,
        )
    assert report.read_bytes() == before
