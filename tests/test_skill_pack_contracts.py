from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"


def implicit_policy(skill: Path) -> bool:
    text = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    match = re.search(r"allow_implicit_invocation:\s*(true|false)", text)
    assert match is not None
    return match.group(1) == "true"


def test_router_names_every_explicit_only_skill() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    explicit = {
        skill.name
        for skill in CUSTOM.iterdir()
        if skill.is_dir() and not implicit_policy(skill)
    }

    assert explicit - {"skill-router"} <= {
        token.removeprefix("$")
        for token in re.findall(r"\$[a-z0-9][a-z0-9-]*", router)
    }


def test_tracker_templates_share_ready_and_readback_contracts() -> None:
    trackers = [
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    ]
    required = (
        "**Ready-for-agent contract**",
        "bounded slice",
        "Source Trace",
        "acceptance criteria",
        "dependency state",
        "proof lane",
        "write scope",
        "parallel-safety note",
        "scope fence",
        "**Mutation read-back**",
        "partial mutation is blocked",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        for token in required:
            assert token in text, f"{tracker} is missing {token}"


def test_branch_heavy_skills_disclose_branch_procedure() -> None:
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")

    assert "[ATTENTION-SCAN.md](ATTENTION-SCAN.md)" in triage
    assert "[SPECIFIC-ITEM.md](SPECIFIC-ITEM.md)" in triage
    assert "[QUICK-OVERRIDE.md](QUICK-OVERRIDE.md)" in triage
    assert "## Specific Item" not in triage
    assert "[DIRECT-DESIGN.md](DIRECT-DESIGN.md)" in design
    assert "## 1. Orient" not in design


def test_wayfinder_chart_preserves_unresolved_child_decisions() -> None:
    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(encoding="utf-8")

    assert "**charting bound**" in wayfinder
    assert "Defer it explicitly to a named Wayfinder ticket" in wayfinder
    assert "zero tickets have recorded outcomes" in wayfinder
    assert "When a caller supplies a bound" in grill_docs


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "discover the repository default branch and merge base" in review
    assert "Base ref: `main`" not in convergent
    assert "distinct, not independent" in convergent
    assert "reduced-confidence" in convergent


def test_mutating_workflows_require_readback() -> None:
    for name in ("implement", "parallel-implement", "to-spec", "to-tickets", "wayfinder"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "Mutation read-back" in text, name


def test_worker_modes_have_distinct_completion_artifacts() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "**staged worker**" in contract
    assert "**lane worker**" in contract
    assert "**Staged worker:**" in implement
    assert "**Lane workers**" in parallel
