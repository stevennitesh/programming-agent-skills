from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
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


PRESENTED_PROGRESS = (
    "presented:1,decision-pending:0,analyzed:0,"
    "implemented:0,disproved:0,blocked:0"
)


def _report(repo: Path) -> Path:
    report = (
        repo
        / ".scratch"
        / "audit-codebase"
        / "run-001"
        / "report.html"
    )
    report.parent.mkdir(parents=True)
    report.write_text(
        """<!doctype html>
<html lang="en"><head>
<meta name="audit-codebase-report-version" content="3">
</head><body>
<!-- audit-codebase:summary:report-header:start -->
<header id="report-header" data-candidate-progress="{progress}">Audit</header>
<!-- audit-codebase:summary:report-header:end -->
<main>
<!-- audit-codebase:subsystem:alpha:start -->
<section id="subsystem-alpha">
  <p>old subsystem</p>
  <table><tbody>
  <!-- audit-codebase:candidate-index:alpha-fix:start -->
  <tr id="candidate-index-alpha-fix"
      data-candidate-id="alpha-fix"
      data-state="presented"
      data-strength="Strong">
    <td><code data-candidate-pickup="alpha-fix"
      data-pickup-view="index">{pickup}</code></td>
  </tr>
  <!-- audit-codebase:candidate-index:alpha-fix:end -->
  </tbody></table>
  <!-- audit-codebase:candidate:alpha-fix:start -->
  <article id="candidate-alpha-fix"
      data-candidate-id="alpha-fix"
      data-state="presented"
      data-strength="Strong">
    <p>old candidate</p>
    <code data-candidate-pickup="alpha-fix"
      data-pickup-view="card">{pickup}</code>
  </article>
  <!-- audit-codebase:candidate:alpha-fix:end -->
</section>
<!-- audit-codebase:subsystem:alpha:end -->
<!-- audit-codebase:summary:progress:start -->
<section id="summary-progress" data-candidate-progress="{progress}">
  <p>old progress</p>
</section>
<!-- audit-codebase:summary:progress:end -->
</main>
<!-- audit-codebase:summary:report-footer:start -->
<footer id="report-footer" data-candidate-progress="{progress}">Audit</footer>
<!-- audit-codebase:summary:report-footer:end -->
</body></html>
""".format(
            progress=PRESENTED_PROGRESS,
            pickup="$audit-codebase analyze alpha-fix from report",
        ),
        encoding="utf-8",
    )
    return report


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fragment(tmp_path: Path, name: str, markup: str) -> Path:
    path = tmp_path / name
    path.write_text(markup, encoding="utf-8")
    return path


def _progress_sections(tmp_path: Path, progress: str) -> tuple[tuple[str, str, Path], ...]:
    return tuple(
        (
            "summary",
            identifier,
            _fragment(
                tmp_path,
                f"{identifier}.html",
                f'<{tag} id="{element_id}" data-candidate-progress="{progress}">'
                f"{identifier}</{tag}>",
            ),
        )
        for identifier, element_id, tag in (
            ("report-header", "report-header", "header"),
            ("progress", "summary-progress", "section"),
            ("report-footer", "report-footer", "footer"),
        )
    )


def _candidate_sections(
    tmp_path: Path,
    *,
    state: str,
    pickup: str,
    row_state: str | None = None,
    evidence: str = "",
) -> tuple[tuple[str, str, Path], ...]:
    card_pickup = (
        f'<code data-candidate-pickup="alpha-fix" '
        f'data-pickup-view="card">{pickup}</code>'
        if pickup
        else ""
    )
    index_pickup = (
        f'<code data-candidate-pickup="alpha-fix" '
        f'data-pickup-view="index">{pickup}</code>'
        if pickup
        else ""
    )
    candidate = _fragment(
        tmp_path,
        "candidate.html",
        f"""<article id="candidate-alpha-fix"
data-candidate-id="alpha-fix" data-state="{state}"
data-strength="Strong">
new{card_pickup}{evidence}
</article>""",
    )
    index = _fragment(
        tmp_path,
        "candidate-index.html",
        f"""<tr id="candidate-index-alpha-fix"
data-candidate-id="alpha-fix" data-state="{row_state or state}"
data-strength="Strong"><td>new{index_pickup}</td></tr>""",
    )
    return (
        ("candidate", "alpha-fix", candidate),
        ("candidate-index", "alpha-fix", index),
    )


def _progress_for(state: str) -> str:
    states = (
        "presented",
        "decision-pending",
        "analyzed",
        "implemented",
        "disproved",
        "blocked",
    )
    return ",".join(
        f"{candidate_state.replace(' ', '-')}:{int(candidate_state == state)}"
        for candidate_state in states
    )


def _completion(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "implementation_outcome": "complete",
                "report": str(
                    path.parent
                    / ".scratch"
                    / "audit-codebase"
                    / "run-001"
                    / "report.html"
                ),
                "run_id": "run-001",
                "subsystem_id": "alpha",
                "candidate_id": "alpha-fix",
                "commit_identity": "a" * 40,
                "commit_tree_identity": "b" * 40,
                "current_source_result": "reachable",
                "accepted_proof": "focused and contract suites passed",
                "formal_review_decision": "accepted",
                "repair_generations_used": 1,
                "changed_scope": "alpha implementation",
                "change_closure": "complete",
                "residual_risk": "none",
                "last_verified_identity": "a" * 40,
            }
        ),
        encoding="utf-8",
    )
    return path


def test_inspect_returns_local_candidate_packet(tmp_path: Path) -> None:
    report = _report(tmp_path)

    result = MODULE.inspect_report(
        repo_root=tmp_path,
        report=report,
        candidate_id="alpha-fix",
    )

    assert result["report_version"] == "3"
    assert result["run_id"] == "run-001"
    assert result["sha256"] == _digest(report)
    assert result["candidate"] == {
        "id": "alpha-fix",
        "state": "presented",
        "strength": "Strong",
        "pickup": "$audit-codebase analyze alpha-fix from report",
    }


def test_validate_prepares_update_without_filesystem_mutation(tmp_path: Path) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()
    candidate = _candidate_sections(
        tmp_path,
        state="analyzed",
        pickup="",
    )
    progress = _progress_sections(tmp_path, _progress_for("analyzed"))

    result = MODULE.validate_report_update(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        sections=(*candidate, *progress),
    )

    assert result["stage"] == "validate"
    assert result["mutation_started"] is False
    assert result["report_unchanged"] is True
    assert result["candidate_states"] == {"alpha-fix": "analyzed"}
    assert report.read_bytes() == before
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


def test_validation_error_reports_zero_mutation_boundary(tmp_path: Path) -> None:
    report = _report(tmp_path)
    fragment = _fragment(
        tmp_path,
        "candidate.html",
        '<article id="wrong-anchor">bad</article>',
    )

    with pytest.raises(MODULE.ReportUpdateError) as raised:
        MODULE.validate_report_update(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(("candidate", "alpha-fix", fragment),),
        )

    assert raised.value.stage == "validate"
    assert raised.value.mutation_started is False
    assert raised.value.report_unchanged is True


def test_replace_error_reports_started_mutation_and_preserves_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()
    sections = (
        *_candidate_sections(tmp_path, state="analyzed", pickup=""),
        *_progress_sections(tmp_path, _progress_for("analyzed")),
    )

    def fail_replace(source: Path, target: Path) -> None:
        raise OSError("controlled replacement failure")

    monkeypatch.setattr(MODULE.os, "replace", fail_replace)
    with pytest.raises(MODULE.ReportUpdateError) as raised:
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=sections,
        )

    assert raised.value.stage == "replace"
    assert raised.value.mutation_started is True
    assert raised.value.report_unchanged is True
    assert report.read_bytes() == before
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


def test_close_candidate_derives_all_report_projections(tmp_path: Path) -> None:
    report = _report(tmp_path)
    analyzed = _candidate_sections(
        tmp_path,
        state="analyzed",
        pickup="$implement candidate alpha-fix from report",
    )
    MODULE.update_report(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        sections=(
            *analyzed,
            *_progress_sections(tmp_path, _progress_for("analyzed")),
        ),
    )
    completion = _completion(tmp_path / "completion.json")

    result = MODULE.close_candidate(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        candidate_id="alpha-fix",
        completion_path=completion,
    )

    updated = report.read_text(encoding="utf-8")
    assert result["candidate_states"] == {"alpha-fix": "implemented"}
    assert result["candidate_progress"] == _progress_for("implemented")
    assert 'data-state="implemented"' in updated
    assert 'data-implementation-result="complete"' in updated
    assert 'data-candidate-pickup="alpha-fix"' not in updated
    assert 'data-implemented-banner="alpha-fix"' in updated


def test_updates_selected_regions_atomically(tmp_path: Path) -> None:
    report = _report(tmp_path)
    candidate = _fragment(
        tmp_path,
        "candidate.html",
        """<article id="candidate-alpha-fix"
data-candidate-id="alpha-fix" data-state="analyzed"
data-strength="Strong">
<a href="#summary-progress">new</a>
</article>""",
    )
    index = _fragment(
        tmp_path,
        "candidate-index.html",
        """<tr id="candidate-index-alpha-fix"
data-candidate-id="alpha-fix" data-state="analyzed"
data-strength="Strong"><td>new</td></tr>""",
    )
    progress = (
        "presented:0,decision-pending:0,analyzed:1,"
        "implemented:0,disproved:0,blocked:0"
    )

    result = MODULE.update_report(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        sections=(
            ("candidate", "alpha-fix", candidate),
            ("candidate-index", "alpha-fix", index),
            *_progress_sections(tmp_path, progress),
        ),
    )

    updated = report.read_text(encoding="utf-8")
    assert "new" in updated
    assert "old subsystem" in updated
    assert result["candidate_states"] == {"alpha-fix": "analyzed"}
    assert result["candidate_progress"] == progress
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


def test_publishes_complete_implementation_evidence(tmp_path: Path) -> None:
    report = _report(tmp_path)
    evidence = f"""<dl data-implementation-result="complete"
data-candidate-id="alpha-fix"
data-commit-sha="{'a' * 40}" data-tree-sha="{'b' * 40}"
data-source-status="reachable" data-proof-status="accepted"
data-review-status="accepted" data-repair-generations="1"
data-closure-status="complete" data-blockers="none"><dt>Done</dt></dl>"""
    progress = _progress_for("implemented")

    result = MODULE.update_report(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        sections=(
            *_candidate_sections(
                tmp_path,
                state="implemented",
                pickup="",
                evidence=evidence,
            ),
            *_progress_sections(tmp_path, progress),
        ),
    )

    assert result["candidate_states"] == {"alpha-fix": "implemented"}
    assert result["candidate_progress"] == progress


@pytest.mark.parametrize(
    ("state", "pickup", "row_state", "evidence", "error"),
    (
        ("analyzed", "resume", "blocked", "", "projection disagree"),
        ("implemented", "retry", None, "", "forbids pickup"),
        ("implemented", "", None, "", "needs one evidence element"),
    ),
)
def test_candidate_consistency_failure_preserves_report(
    tmp_path: Path,
    state: str,
    pickup: str,
    row_state: str | None,
    evidence: str,
    error: str,
) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()

    with pytest.raises(MODULE.ReportUpdateError, match=error):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(
                *_candidate_sections(
                    tmp_path,
                    state=state,
                    pickup=pickup,
                    row_state=row_state,
                    evidence=evidence,
                ),
                *_progress_sections(tmp_path, _progress_for(state)),
            ),
        )

    assert report.read_bytes() == before
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


def test_progress_projection_failure_preserves_report(tmp_path: Path) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()
    progress = _progress_for("analyzed")
    summary = _progress_sections(tmp_path, progress)[1]

    with pytest.raises(MODULE.ReportUpdateError, match="report-header.*inconsistent"):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(
                *_candidate_sections(
                    tmp_path,
                    state="analyzed",
                    pickup="",
                ),
                summary,
            ),
        )

    assert report.read_bytes() == before


def test_requires_report_version_three(tmp_path: Path) -> None:
    report = _report(tmp_path)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            'content="3"',
            'content="2"',
            1,
        ),
        encoding="utf-8",
    )
    before = report.read_bytes()
    fragment = _fragment(
        tmp_path,
        "candidate.html",
        '<article id="candidate-alpha-fix">new</article>',
    )

    with pytest.raises(MODULE.ReportUpdateError, match="version 3"):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(("candidate", "alpha-fix", fragment),),
        )

    assert report.read_bytes() == before


def test_collision_preserves_report(tmp_path: Path) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()
    fragment = tmp_path / "candidate.html"
    fragment.write_text(
        '<article id="candidate-alpha-fix">new</article>',
        encoding="utf-8",
    )

    with pytest.raises(MODULE.ReportUpdateError, match="report collision"):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256="0" * 64,
            sections=(("candidate", "alpha-fix", fragment),),
        )

    assert report.read_bytes() == before


@pytest.mark.parametrize(
    "fragment",
    (
        '<article id="candidate-alpha-fix"><script>bad()</script></article>',
        '<article id="candidate-alpha-fix"><a href="//example.com">bad</a></article>',
        '<article id="candidate-alpha-fix"><a href="ftp://example.com">bad</a></article>',
        '<article id="candidate-alpha-fix"><svg onload="bad()"></svg></article>',
        "<!-- audit-codebase:candidate:other:start -->"
        '<article id="candidate-alpha-fix">bad</article>',
        '<article id="wrong-anchor">bad</article>',
    ),
)
def test_unsafe_fragment_preserves_report(tmp_path: Path, fragment: str) -> None:
    report = _report(tmp_path)
    before = report.read_bytes()
    fragment_path = tmp_path / "candidate.html"
    fragment_path.write_text(fragment, encoding="utf-8")

    with pytest.raises(MODULE.ReportUpdateError):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(("candidate", "alpha-fix", fragment_path),),
        )

    assert report.read_bytes() == before
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


def test_rejects_overlapping_parent_and_child_updates(tmp_path: Path) -> None:
    report = _report(tmp_path)
    subsystem = tmp_path / "subsystem.html"
    subsystem.write_text(
        '<section id="subsystem-alpha"><p>new subsystem</p></section>',
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate.html"
    candidate.write_text(
        '<article id="candidate-alpha-fix"><p>new candidate</p></article>',
        encoding="utf-8",
    )

    with pytest.raises(MODULE.ReportUpdateError, match="overlapping replacements"):
        MODULE.update_report(
            repo_root=tmp_path,
            report=report,
            expected_sha256=_digest(report),
            sections=(
                ("subsystem", "alpha", subsystem),
                ("candidate", "alpha-fix", candidate),
            ),
        )
