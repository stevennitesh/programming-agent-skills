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


def test_repo_bootstrap_reconciles_existing_setup_without_reset() -> None:
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    required = (
        "treat this run as a **reconcile**, not a reset",
        "**Preserve:** confirmed tracker",
        "**Delta:** propose only changes required by the current pack.",
        "**Re-ask:** revisit a choice only when it is missing, ambiguous, incompatible, or explicitly reopened by the user.",
        "Reconcile existing local contracts in place.",
        "Preserve repo-specific additions.",
    )

    for token in required:
        assert token in bootstrap


def test_repo_bootstrap_marks_and_validates_setup_schema() -> None:
    marker = "<!-- programming-agent-skills setup-schema: 1 -->"
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    validator = (CUSTOM / "repo-bootstrap/scripts/validate_setup.py").read_text(
        encoding="utf-8"
    )
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert marker in bootstrap
    assert marker in validator
    assert marker in agents
    assert "A missing `programming-agent-skills setup-schema` marker identifies a legacy setup." in bootstrap


def test_outdated_setup_routes_to_repo_bootstrap() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    template = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )

    assert "missing or outdated setup contract" in router
    assert "missing or outdated repo setup surface" in template


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
    assert "exactly one selected ticket has a substantive outcome" in wayfinder
    assert "every other ticket mutation is consequence-only" in wayfinder
    assert "When a caller supplies a bound" in grill_docs


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "discover the repository default branch and merge base" in review
    assert "Base ref: `main`" not in convergent
    assert "distinct, not independent" in convergent
    assert "reduced-confidence" in convergent


def test_convergent_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "For a branch or PR, compare the current target head with the captured head." in convergent
    assert "For a live worktree, compare the current `HEAD`, index, status, and in-scope untracked content with the captured snapshot." in convergent
    assert "changed from the pinned fixed point" not in convergent


def test_implement_selects_one_risk_scaled_review_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    assert "**Review route:** Use `$review` by default." in implement
    assert "Use `$convergent-pr-review` for a local PR or high-risk diff matching its trigger." in implement
    assert "invoke exactly that route" in implement
    assert "another pass through the selected review route" in implement


def test_architecture_research_requires_tracked_mutation_approval() -> None:
    architecture = (CUSTOM / "improve-codebase-architecture/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert architecture.count("only when the caller approves that tracked mutation") == 2
    assert "otherwise record a named evidence gap" in architecture
    assert "tracked state remains unchanged except for any approved `$research` note" in architecture


def test_direct_workflows_gate_on_setup_compatibility() -> None:
    for name in ("implement", "parallel-implement", "to-spec", "to-tickets"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "absent or incompatible with this skill" in text, name

    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    assert "absent or incompatible with triage" in triage


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")

    assert "only when test shape, oracle, or seam remains unclear after inspecting nearby tests" in tdd


def test_triage_ready_examples_use_the_shared_proof_lane_schema() -> None:
    examples = (CUSTOM / "triage/AGENT-BRIEF-EXAMPLES.md").read_text(encoding="utf-8")

    assert examples.count("**Proof lane:**") == 4
    assert "**Validation notes:**" not in examples


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
