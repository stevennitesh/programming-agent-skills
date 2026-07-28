from __future__ import annotations

import hashlib
import importlib.util
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
<html lang="en"><main>
<!-- audit-codebase:subsystem:alpha:start -->
<section id="subsystem-alpha">
  <p>old subsystem</p>
  <!-- audit-codebase:candidate:alpha-fix:start -->
  <article id="candidate-alpha-fix"><p>old candidate</p></article>
  <!-- audit-codebase:candidate:alpha-fix:end -->
</section>
<!-- audit-codebase:subsystem:alpha:end -->
<!-- audit-codebase:summary:progress:start -->
<section id="summary-progress"><p>old progress</p></section>
<!-- audit-codebase:summary:progress:end -->
</main></html>
""",
        encoding="utf-8",
    )
    return report


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_updates_selected_regions_atomically(tmp_path: Path) -> None:
    report = _report(tmp_path)
    candidate = tmp_path / "candidate.html"
    candidate.write_text(
        '<article id="candidate-alpha-fix"><a href="#summary-progress">new</a></article>',
        encoding="utf-8",
    )
    summary = tmp_path / "summary.html"
    summary.write_text(
        '<section id="summary-progress"><p>1 analyzed</p></section>',
        encoding="utf-8",
    )

    result = MODULE.update_report(
        repo_root=tmp_path,
        report=report,
        expected_sha256=_digest(report),
        sections=(
            ("candidate", "alpha-fix", candidate),
            ("summary", "progress", summary),
        ),
    )

    updated = report.read_text(encoding="utf-8")
    assert "new" in updated
    assert "1 analyzed" in updated
    assert "old subsystem" in updated
    assert result["sections"] == ["candidate:alpha-fix", "summary:progress"]
    assert not list(report.parent.glob("report.html.audit-update-*.tmp"))


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
