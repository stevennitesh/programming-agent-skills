from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

from scripts import skill_pack_contract, validate_skills


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"


def implicit_policy(skill: Path) -> bool:
    text = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    match = re.search(r"allow_implicit_invocation:\s*(true|false)", text)
    assert match is not None
    return match.group(1) == "true"


def test_router_names_every_custom_skill() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    skill_names = {skill.name for skill in CUSTOM.iterdir() if skill.is_dir()}
    routes = re.findall(
        r"(?m)^\| (?!-)([^|]+?) \| `\$([a-z0-9][a-z0-9-]*)` \|$", router
    )
    routed = [skill for _, skill in routes]

    assert set(routed) | {"repo-bootstrap"} == skill_names - {"skill-router"}
    assert len(routed) == len(set(routed))


def test_handoff_compacts_context_without_advancing_work() -> None:
    skill_dir = CUSTOM / "handoff"
    handoff = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert re.findall(r"(?m)^\*\*([A-Za-z]+)\.\*\*", handoff) == [
        "Trace",
        "Snapshot",
        "Compact",
        "Redact",
        "Save",
        "Verify",
        "Return",
    ]
    template = handoff.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", template) == [
        "Purpose",
        "Current State",
        "Key Decisions",
        "Source Trace",
        "Validation",
        "Open Questions",
        "Next Step",
        "Suggested Skills",
    ]
    assert "<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>.md" in handoff
    assert "$repo-bootstrap" in handoff
    assert "Continue from `<absolute-path>`. Read the handoff first, then execute its Next Step." in handoff


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


def test_triage_label_template_respects_tracker_pr_policy() -> None:
    labels = (CUSTOM / "repo-bootstrap/triage-labels.md").read_text(encoding="utf-8")
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")

    assert "Every triaged work item" in labels
    assert "Every triaged issue or PR" not in labels
    assert "Triage PRs only when the tracker enables them" in triage


def test_github_closeout_clears_dependency_frontier_safely() -> None:
    github_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
    )
    for tracker in github_trackers:
        text = tracker.read_text(encoding="utf-8")
        assert "**Close implemented items:** yes." in text
        assert "**Non-completed closure**" in text

    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    assert "GitHub default: yes" in bootstrap
    assert "GitLab default: no" in bootstrap


def test_repo_bootstrap_reconciles_existing_setup_without_reset() -> None:
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", bootstrap) == [
        "Inventory",
        "Reconcile",
        "Choose",
        "Draft",
        "Provision",
        "Verify",
    ]
    assert bootstrap.index("## Draft") < bootstrap.index("## Provision")


def test_repo_bootstrap_marks_and_validates_setup_schema() -> None:
    schema = json.loads(
        (CUSTOM / "repo-bootstrap/setup-schema.json").read_text(encoding="utf-8")
    )
    marker = (
        "<!-- programming-agent-skills setup-schema: "
        f"{schema['version']}:{schema['contract_sha256'][:12]} -->"
    )
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    validator = (CUSTOM / "repo-bootstrap/scripts/validate_setup.py").read_text(
        encoding="utf-8"
    )
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert marker in bootstrap
    assert marker in validator
    assert marker in agents
    assert "[setup-schema.json](setup-schema.json)" in bootstrap
    assert validate_skills.validate_setup_schema_manifest(ROOT) == []


def test_portable_fallback_adoption_removes_the_portable_contract_owner() -> None:
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )

    failures = validator["portable_owner_failures"](fallback)
    assert len(failures) == 1
    assert "$repo-bootstrap" in failures[0]
    assert validator["portable_owner_failures"](
        "# Repository Instructions\n\n## Skill Pack\n\nAGENTS primes.\n"
    ) == []
    partial_adoption = fallback.replace("# Portable Engineering Contract", "")
    partial_adoption = partial_adoption.replace(
        "This contract owns engineering taste, gates, and completion.", ""
    )
    assert validator["portable_owner_failures"](partial_adoption) == failures
    repo_specific_headings = "# Repository Instructions\n"
    for heading in validator["PORTABLE_SECTION_HEADINGS"]:
        repo_specific_headings += f"\n{heading}\n\nRepo-specific guidance.\n"
    assert validator["portable_owner_failures"](repo_specific_headings) == []
    for heading, signature in validator["PORTABLE_SECTION_SIGNATURES"]:
        assert validator["markdown_section_contains"](fallback, heading, signature)
        split_pair = (
            "# Repository Instructions\n\n"
            f"{heading}\n\nRepo-specific guidance.\n\n"
            "## Unrelated\n\n"
            f"{signature}\n"
        )
        assert validator["portable_owner_failures"](split_pair) == []
        nested = f"# Repository Instructions\n\n{heading}\n\n### Detail\n\n{signature}\n"
        assert validator["portable_owner_failures"](nested) == failures

    marker = validator["SETUP_SCHEMA_TOKEN"]
    stale = "<!-- programming-agent-skills setup-schema: 1:deadbeefdead -->"
    assert validator["setup_schema_marker_failures"](marker) == []
    expected_marker_failure = [
        "AGENTS.md must contain exactly one current programming-agent-skills "
        "setup-schema marker"
    ]
    assert validator["setup_schema_marker_failures"](
        f"{marker}\n{marker}\n"
    ) == expected_marker_failure
    assert validator["setup_schema_marker_failures"](
        f"{stale}\n{marker}\n"
    ) == expected_marker_failure

    primer = validator["ENGINEERING_PRIMER_TOKEN"]
    valid_primer = (
        f"# Repository Instructions\n\n{marker}\n\n{primer}\n\n"
        "## Commands\n\n- Test: `python -m pytest`\n"
    )
    assert validator["engineering_primer_failures"](valid_primer) == []
    primer_failure = [
        "AGENTS.md must place the engineering primer between the current "
        "setup-schema marker and ## Commands"
    ]
    assert validator["engineering_primer_failures"](
        valid_primer.replace(primer, f"> {primer}")
    ) == primer_failure
    assert validator["engineering_primer_failures"](
        valid_primer.replace(primer, f"## History\n\n{primer}")
    ) == primer_failure

    assert validator["git_root_failures"](ROOT) == []
    assert validator["git_root_failures"](ROOT / "skills") == [
        "Target must be the Git repository root"
    ]


def test_outdated_setup_routes_to_repo_bootstrap() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    template = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )

    assert "$repo-bootstrap" in router
    assert "$repo-bootstrap" in template


def test_router_returns_exactly_one_next_skill() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "skill-router")
    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", router) == [
        "Inspect",
        "Clarify",
        "Route",
        "Stop",
    ]
    stop = router.split("4. **Stop.**", 1)[1].split("## Route Map", 1)[0]
    assert re.findall(r"`(Skill|Reason|Precondition):", stop) == [
        "Skill",
        "Reason",
        "Precondition",
    ]


def test_branch_heavy_skills_disclose_branch_procedure() -> None:
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    attention = (CUSTOM / "triage/ATTENTION-SCAN.md").read_text(encoding="utf-8")
    quick = (CUSTOM / "triage/QUICK-OVERRIDE.md").read_text(encoding="utf-8")
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")

    assert "[ATTENTION-SCAN.md](ATTENTION-SCAN.md)" in triage
    assert "[SPECIFIC-ITEM.md](SPECIFIC-ITEM.md)" in triage
    assert "[QUICK-OVERRIDE.md](QUICK-OVERRIDE.md)" in triage
    assert "## Specific Item" not in triage
    run = triage.split("3. **Run.**", 1)[1].split("4. **Prove.**", 1)[0]
    assert "selected branch" in run
    assert "For any mutation branch" in run
    assert "tracker state stayed unchanged" in attention
    assert "Skip request verification and grilling" in quick
    assert "[DIRECT-DESIGN.md](DIRECT-DESIGN.md)" in design
    assert "## 1. Orient" not in design


def test_codebase_design_preserves_lean_branch_contracts() -> None:
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")
    direct = (CUSTOM / "codebase-design/DIRECT-DESIGN.md").read_text(
        encoding="utf-8"
    )
    deepening = (CUSTOM / "codebase-design/DEEPENING.md").read_text(
        encoding="utf-8"
    )
    alternatives = (CUSTOM / "codebase-design/DESIGN-IT-TWICE.md").read_text(
        encoding="utf-8"
    )

    assert "[DIRECT-DESIGN.md](DIRECT-DESIGN.md)" in design
    assert len(re.findall(r"(?m)^## \d+\. ", direct)) == 5
    assert len(re.findall(r"(?m)^## \d+\. ", deepening)) == 5
    for category in (
        "In-process",
        "Local-substitutable",
        "Remote-owned",
        "True external",
    ):
        assert category in deepening
    for disposition in ("Add", "Rewrite", "Keep", "Delete"):
        assert f"**{disposition}**" in deepening
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", alternatives) == [
        "Frame",
        "Diverge",
        "Compare",
        "Recommend",
    ]
    assert "**No-new-seam**" in alternatives


def test_wayfinder_chart_preserves_unresolved_child_decisions() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert "[MAP-FORMAT.md](MAP-FORMAT.md)" in wayfinder
    chart, advance = wayfinder.split("### Chart", 1)[1].split("### Advance", 1)
    for earlier, later in (
        ("**Bound.**", "**Approve.**"),
        ("**Approve.**", "**Chart.**"),
        ("**Chart.**", "**Verify.**"),
    ):
        assert chart.index(earlier) < chart.index(later)
    for earlier, later in (
        ("**Orient.**", "**Claim.**"),
        ("**Claim.**", "**Resolve.**"),
        ("**Resolve.**", "**Reconcile.**"),
        ("**Reconcile.**", "**Verify.**"),
        ("**Verify.**", "**Expose.**"),
    ):
        assert advance.index(earlier) < advance.index(later)
    assert re.findall(r"(?m)^### (Chart|Advance)$", wayfinder) == ["Chart", "Advance"]
    assert "#### Advance Closure" in advance
    map_template = map_format.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", map_template) == [
        "Destination",
        "Scope Boundary",
        "Notes",
        "Decisions So Far",
        "Not Yet Specified",
        "Out Of Scope",
    ]
    assert "caller-approved repo-local note path" in map_format
    assert advance.index("Mutation read-back before resolution work") < advance.index(
        "4. **Resolve.**"
    )


def test_grill_with_docs_owns_interview_domain_composition() -> None:
    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(encoding="utf-8")
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert "$grilling" in grill_docs
    assert "$domain-modeling" in grill_docs
    assert "$domain-modeling" not in grilling
    assert "$grilling" not in domain
    assert re.findall(r"(?m)^\*\*([A-Za-z]+)\.\*\*", grill_docs) == [
        "Compose",
        "Disclose",
        "Bound",
        "Reconcile",
        "Return",
    ]
    rows = re.findall(
        r"(?m)^\| `([a-z0-9-]+)` \| (Load|Invoke|Compose|Hand off|Recommend and stop) \| `\$([a-z0-9-]+)` \|",
        relationships,
    )
    assert {
        caller for caller, verb, callee in rows if verb == "Compose" and callee == "domain-modeling"
    } == {"grill-with-docs"}


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")

    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", domain) == [
        "Trace",
        "Challenge",
        "Resolve",
        "Persist",
        "Return",
    ]
    for target in ("CONTEXT-FORMAT.md", "ADR-FORMAT.md"):
        assert (CUSTOM / "domain-modeling" / target).is_file()
        assert f"({f'./{target}'})" in domain
    assert "**domain delta**" in domain


def test_grilling_preserves_one_decision_confirmed_exit_and_evidence_routes() -> None:
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")

    assert re.findall(r"(?m)^\*\*([A-Za-z ]+)\.\*\*", grilling) == [
        "Orient",
        "Find",
        "Pressure",
        "Ask",
        "Confirm",
        "Evidence gap",
        "Return",
    ]


def test_prototype_preserves_lifecycle_boundaries_and_branch_gates() -> None:
    prototype = (CUSTOM / "prototype/SKILL.md").read_text(encoding="utf-8")
    logic = (CUSTOM / "prototype/LOGIC.md").read_text(encoding="utf-8")
    ui = (CUSTOM / "prototype/UI.md").read_text(encoding="utf-8")

    judge = prototype.split("## 5. Judge", 1)[1].split("## 6. Reconcile", 1)[0]
    reconcile = prototype.split("## 6. Reconcile", 1)[1].split("## Completion", 1)[0]
    assert "Record the verdict fields" in judge
    assert "return the verdict packet" not in judge
    assert reconcile.index("Finalize the cleanup or preservation state") < reconcile.index(
        "return the verdict packet"
    )
    assert "[LOGIC.md](LOGIC.md)" in prototype
    assert "[UI.md](UI.md)" in prototype
    assert set(re.findall(r"`(answered|awaiting-verdict|blocked)`", prototype)) == {
        "answered",
        "awaiting-verdict",
        "blocked",
    }
    assert re.findall(r"(?m)^## (.+)$", logic) == ["Model", "Drive", "Smoke"]
    assert re.findall(r"(?m)^## (.+)$", ui) == ["Host", "Bet", "Switch", "Smoke"]
    assert "smallest explicit decision interface" in logic
    assert "entire prototype surface" in ui
    assert "unreachable in production builds" in ui


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")
    baseline = (CUSTOM / "review/SMELL-BASELINE.md").read_text(encoding="utf-8")

    assert "## 1. Pin" in review
    assert "## 1. Pin" in convergent
    assert "$convergent-pr-review" in review.split("---", 2)[1]
    assert "$review" in convergent.split("---", 2)[1]
    assert "only when documented repo standards" in baseline
    assert "concrete, actionable maintainability risk" in baseline
    assert "baseline judgement call" in review
    assert "baseline judgement call" in convergent
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", review) == [
        "Pin",
        "Trace",
        "Judge",
        "Report",
    ]
    report = review.split("```markdown", 1)[1].split("```", 1)[0]
    assert report.lstrip().startswith("Review status: complete")
    assert re.findall(r"(?m)^## (Standards|Spec)$", report) == ["Standards", "Spec"]
    incomplete = review.split("```text", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^([A-Za-z ]+):", incomplete) == [
        "Review status",
        "Review target",
        "Sources",
        "Blocker",
        "Skipped",
    ]


def test_convergent_review_uses_fresh_context_and_root_only_fanout() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert 'fork_turns="none"' in convergent
    contract = convergent.split("```text", 1)[1].split("```", 1)[0]
    assert set(re.findall(r"(?m)^([a-z ]+):", contract)) == {
        "status",
        "axis",
        "lens",
        "coverage",
        "findings",
        "skipped checks",
        "blockers",
    }


def test_convergent_review_returns_a_lock_usable_decision() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    decisions = set(
        re.findall(
            r"(?m)^- `(pass|pass with residual risk|blocked|incomplete)`: ",
            convergent,
        )
    )
    assert decisions == {"pass", "pass with residual risk", "blocked", "incomplete"}
    ledger_states = set(
        re.findall(
            r"(?m)^Status is (?:`([^`]+)`, `([^`]+)`, `([^`]+)`, `([^`]+)`, or `([^`]+)`)\.",
            convergent,
        )[0]
    )
    assert ledger_states == {"candidate", "accepted", "rejected", "duplicate", "disputed"}


def test_convergent_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    verify = convergent.split("## 5. Verify", 1)[1].split("## 6. Report", 1)[0]
    for surface in (
        "`HEAD`",
        "index tree",
        "staged diff",
        "unstaged diff",
        "status",
        "untracked paths and content",
    ):
        assert surface in verify


def test_implement_selects_one_risk_scaled_review_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_section = implement.split("## Review", 1)[1].split("## Lock", 1)[0]
    assert re.findall(r"(?m)^- `\$(review|convergent-pr-review)`", review_section) == [
        "review",
        "convergent-pr-review",
    ]


def test_architecture_report_matches_the_survey_gate() -> None:
    architecture = (CUSTOM / "improve-codebase-architecture/SKILL.md").read_text(
        encoding="utf-8"
    )
    report = (CUSTOM / "improve-codebase-architecture/HTML-REPORT.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(CUSTOM / "improve-codebase-architecture")
    assert "$improve-codebase-architecture Candidate N" in architecture
    assert "**No candidate recommended**" in architecture
    assert re.findall(r"(?m)^## (.+)$", report) == [
        "Portability",
        "Layout",
        "Theme",
        "Candidate",
        "Diagram",
        "Top Recommendation",
        "Voice",
    ]
    assert "`color-scheme: dark`" in report
    assert "`Strong` or `Worth exploring`" in report
    survey = architecture.split("## Survey", 1)[1].split("## Selected Candidate", 1)[0]
    selected = architecture.split("## Selected Candidate", 1)[1].split("## Completion", 1)[0]
    assert survey.index("### Report") < survey.index("Candidate N")
    assert "### Grill" not in survey
    assert selected.index("explicitly resumes") < selected.index("### Grill")
    top_recommendation = report.split("## Top Recommendation", 1)[1].split(
        "## Voice", 1
    )[0]
    assert "**No candidate recommended**" in top_recommendation
    assert "surveyed region" in top_recommendation


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")

    assert re.findall(r"(?m)^## \d+\. ([A-Z]+)$", tdd) == [
        "TRACE",
        "RED",
        "GREEN",
        "REFACTOR",
        "RETURN",
    ]
    for helper in ("tests.md", "mocking.md", "refactoring.md"):
        assert (CUSTOM / "tdd" / helper).is_file()
        assert f"[{helper}]({helper})" in tdd


def test_tdd_routes_architecture_followups_by_scope() -> None:
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")

    assert "$codebase-design" in refactoring
    assert "$improve-codebase-architecture" in refactoring


def test_bug_routing_is_disjoint_and_non_bouncing() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tdd_tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")

    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^## \d+\. ([A-Za-z]+)$", diagnosing)
    ] == ["Trace", "Loop", "Minimise", "Hypothesise", "Probe", "Prove", "Return"]
    assert "[SKILL.md](SKILL.md)" in tdd_tests
    assert "$diagnosing-bugs" in tdd.split("---", 2)[1]
    assert "expected behavior" in diagnosing.split("---", 2)[1]
    assert "expected behavior" in tdd.split("---", 2)[1]
    assert "observed failing result" in tdd


def test_workflow_trace_matches_to_spec_publication_authority() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "to-spec")
    assert re.findall(r"(?m)^### \d+\. ([A-Za-z]+)$", to_spec) == [
        "Trace",
        "Choose",
        "Draft",
        "Cover",
        "Publish",
    ]
    draft = to_spec.split("Use these sections:", 1)[1].split("Write a comprehensive", 1)[0]
    assert len(re.findall(r"(?m)^- `[^`]+`", draft)) >= 10


def test_implementation_closeout_requires_the_spec_axis() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (review, convergent):
        assert "`Spec required: yes | no`" in text
    for text in (implement, parallel):
        assert "`Spec required: yes`" in text


def test_independent_scouts_receive_curated_fresh_context() -> None:
    design = (CUSTOM / "codebase-design/DESIGN-IT-TWICE.md").read_text(
        encoding="utf-8"
    )
    research = (CUSTOM / "research/SKILL.md").read_text(encoding="utf-8")
    architecture = (CUSTOM / "improve-codebase-architecture/SKILL.md").read_text(
        encoding="utf-8"
    )

    for text in (design, research, architecture):
        assert 'fork_turns="none"' in text


def test_research_owns_one_authorized_cited_note() -> None:
    research = (CUSTOM / "research/SKILL.md").read_text(encoding="utf-8")

    authorized = re.search(r"(?m)^\*\*Authorized note: (.+)\.\*\*$", research)
    inline = re.search(r"(?m)^\*\*Inline or blocker: (.+)\.\*\*$", research)
    assert authorized is not None and inline is not None
    assert (
        authorized.group(1).index("Write")
        < authorized.group(1).index("Verify")
        < authorized.group(1).index("Return")
    )
    assert (
        inline.group(1).index("Gate")
        < inline.group(1).index("Verify")
        < inline.group(1).index("Return")
    )
    assert research.index("7. **Verify.**") < research.index("8. **Return.**")
    template = research.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", template) == [
        "Answer",
        "Findings",
        "Conflicts and Uncertainty",
        "Source Trace",
        "Next",
    ]
    assert "Status: answered | conflicted | blocked" in template


def test_writing_great_skills_authorizes_bounded_direct_subagents() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    writing = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert implicit_policy(skill_dir)
    assert "[GLOSSARY.md](GLOSSARY.md)" in writing
    assert 'fork_turns="none"' in writing


def test_writing_great_skills_defines_format_neutral_semantic_surface() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    writing = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    glossary = (skill_dir / "GLOSSARY.md").read_text(encoding="utf-8")
    surface = glossary.split("### Semantic Skill Surface", 1)[1].split("### Steps", 1)[0]

    roles = (
        "Outcome",
        "Boundary and authority",
        "route-aware spine",
        "steps",
        "Return",
        "Completion criterion",
    )
    positions = [surface.index(role) for role in roles]
    assert positions == sorted(positions)
    assert "not mandatory headings" in writing
    assert "universal template" in surface


def test_merge_conflict_resolution_is_three_way_and_finish_bounded() -> None:
    skill_dir = CUSTOM / "resolving-merge-conflicts"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert implicit_policy(skill_dir)
    read_only = re.search(r"(?m)^\*\*Read-only: (.+)\.\*\*$", skill)
    reconcile = re.search(r"(?m)^\*\*Reconcile: (.+)\.\*\*$", skill)
    assert read_only is not None and reconcile is not None
    assert "Reconcile" not in read_only.group(1)
    assert "Finish" not in read_only.group(1)
    assert reconcile.group(1).index("Prove") < reconcile.group(1).index("Return")
    assert "only with finish authority" in reconcile.group(1)
    assert "`git ls-files -u`" in skill
    assert "## Guardrails" in skill
    assert "## Return" in skill


def test_portable_fallback_carries_the_standalone_engineering_contract() -> None:
    loop = "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock"
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")

    assert loop in fallback
    assert loop in contract
    assert re.findall(r"(?m)^## (.+)$", fallback) == [
        "North Star",
        "Engineering Taste",
        "Working Loop",
        "Hard Gates",
        "Shape Before Build",
        "Implementation Taste",
        "Review And Report",
    ]
    assert re.findall(r"(?m)^## (.+)$", contract) == [
        "Shared Engineering Language",
        "Engineering Taste",
        "Tight Engineering Spine",
        "Proof Discipline",
        "Work State And Workers",
        "Lock",
    ]
    north_star = fallback.split("## North Star", 1)[1].split("## Engineering Taste", 1)[0]
    vocabulary = set(re.findall(r"(?m)^- \*\*([^*]+):\*\*", north_star))
    assert vocabulary >= {
        "Source trace",
        "Bounded slice",
        "Commitment boundary",
        "Semantic proof",
        "Fixed point",
        "Spec / Standards",
        "Residual risk",
        "Lock",
    }
    assert "portable engineering-contract owner" in bootstrap
    assert re.findall(r"\$[a-z0-9][a-z0-9-]*", fallback) == []
    assert len(fallback.split()) <= 950
    assert not any(line.startswith("  ") for line in fallback.splitlines())

    hard_gates = fallback.split("## Hard Gates", 1)[1].split("## Shape Before Build", 1)[0]
    for mutation in ("filesystem", "Git", "tracker", "deployment", "external"):
        assert mutation in hard_gates
    implementation = fallback.split("## Implementation Taste", 1)[1].split(
        "## Review And Report", 1
    )[0]
    assert implementation.index("RED") < implementation.index("GREEN")
    assert "oracle" in implementation
    review = fallback.split("## Review And Report", 1)[1]
    assert re.findall(r"(?m)^- \*\*(Standards|Spec):\*\*", review) == [
        "Standards",
        "Spec",
    ]
    assert "Lock" in review


def test_readme_exposes_both_adoption_paths() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    headings = re.findall(r"(?m)^(#{2,3}) (.+)$", readme)
    assert ("##", "Setup") in headings
    assert ("###", "Full Skill Pack") in headings
    assert ("###", "Portable Contract Only") in headings
    assert ("##", "Using The Full Pack") in headings
    setup = readme.split("## Setup", 1)[1].split("## What's Included", 1)[0]
    assert "| Full Skill Pack | Portable Contract |" in setup
    assert "[Install the full pack](#full-skill-pack)" in setup
    assert "[Use the portable contract](AGENTS_PORTABLE_FALLBACK.md)" in setup
    for language in ("bash", "powershell"):
        block = readme.split(f"```{language}", 1)[1].split("```", 1)[0]
        assert "python -m scripts.install_skills" in block
        assert "python -m scripts.validate_skills" in block
    assert readme.count("```mermaid") == 1


def test_triage_branches_share_the_authoritative_brief_schema() -> None:
    specific = (CUSTOM / "triage/SPECIFIC-ITEM.md").read_text(encoding="utf-8")
    quick = (CUSTOM / "triage/QUICK-OVERRIDE.md").read_text(encoding="utf-8")
    examples = (CUSTOM / "triage/AGENT-BRIEF-EXAMPLES.md").read_text(encoding="utf-8")
    brief = (CUSTOM / "triage/AGENT-BRIEF.md").read_text(encoding="utf-8")
    out_of_scope = (CUSTOM / "triage/OUT-OF-SCOPE.md").read_text(encoding="utf-8")

    assert specific.index("mutation packet") < specific.index(
        "explicit maintainer approval"
    )
    assert "## Completion" in quick
    assert brief.count("**Proof lane:**") == 1
    assert "concrete example" not in brief
    assert examples.startswith("# Brief Branch Emphasis")
    assert "| Branch | Emphasize |" in examples
    for branch in ("Bug tracer", "Enhancement tracer", "Support slice", "PR finish"):
        assert f"| {branch} |" in examples
    assert [
        title for title, _, _ in skill_pack_contract.level_two_heading_spans(out_of_scope)
    ] == [
        "File Format",
        "Screen",
        "Classify",
    ]


def test_mutating_workflows_require_readback() -> None:
    for name in ("implement", "parallel-implement", "to-spec", "to-tickets", "triage", "wayfinder"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "Mutation read-back" in text, name


def test_to_tickets_preserves_approval_coverage_and_frontier_contract() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "to-tickets")
    assert re.findall(r"(?m)^### \d+\. ([A-Za-z]+)$", tickets) == [
        "Trace",
        "Map",
        "Slice",
        "Approve",
        "Publish",
    ]


def test_worker_modes_have_distinct_completion_artifacts() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "**staged worker**" in contract
    assert "**lane worker**" in contract
    assert "**Staged worker:**" in implement
    assert "**Lane worker:**" in parallel


def test_parallel_implement_separates_context_checkout_and_review_ownership() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    integrator = (
        CUSTOM / "parallel-implement/references/INTEGRATOR-BRIEF.md"
    ).read_text(encoding="utf-8")
    launch = (
        CUSTOM / "parallel-implement/references/CODEX-WORKTREE-LAUNCH.md"
    ).read_text(encoding="utf-8")
    ledger = (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").read_text(
        encoding="utf-8"
    )
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", parallel) == [
        "Contract",
        "References",
        "Trace",
        "Gate",
        "Wave",
        "Integrate",
        "Review",
        "Lock",
        "Release",
    ]
    assert 'fork_turns="none"' in parallel
    assert "## Review-Ready Handoff" in integrator
    assert 'git worktree add --detach' in launch
    assert "## Explicit Background Task" in launch
    report = worker.split("```text", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^([^:\n]+):", report) == [
        "status",
        "work item",
        "source trace",
        "preflight",
        "base",
        "commit",
        "owned files",
        "proof",
        "skipped checks",
        "risk/blockers",
        "next need",
        "scope notes",
        "final status",
        "skill feedback",
    ]
    assert "acceptance criterion" in report.split("proof:", 1)[1].splitlines()[0]
    diagnosis_route = worker.split("When a bug's", 1)[1].split(";", 1)[0]
    assert "expected behavior" in diagnosis_route
    assert "## Routing Packet" in ledger
    assert "## Closeout Summary" in ledger
    assert "candidate integration `HEAD`" in integrator
    assert "`needs-feedback`" in integrator
    assert "`blocker` packet" in integrator
    assert "orchestrator's Conflict gate" not in integrator


def test_parallel_implement_owns_recovery_authority_and_outcome_gates() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    integrator = (
        CUSTOM / "parallel-implement/references/INTEGRATOR-BRIEF.md"
    ).read_text(encoding="utf-8")
    launch = (
        CUSTOM / "parallel-implement/references/CODEX-WORKTREE-LAUNCH.md"
    ).read_text(encoding="utf-8")
    ledger = (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").read_text(
        encoding="utf-8"
    )
    assert set(re.findall(r"(?m)^- `(done|needs-feedback|blocker)`: ", parallel)) == {
        "done",
        "needs-feedback",
        "blocker",
    }
    for outcome in ("complete", "partial", "blocked"):
        assert f"`{outcome}`" in parallel.split("## Release", 1)[1]
    assert "<scope/downshift/resume/frontier/" in ledger
    assert "## Release" in launch
    wave = parallel.split("## Wave", 1)[1].split("## Integrate", 1)[0]
    lock = parallel.split("## Lock", 1)[1].split("## Release", 1)[0]
    assert "claim" in wave and "Mutation read-back" in wave
    assert "closeout tracker mutation" in lock
    assert "idle before formal review" in launch


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "implement")
    owner_route = re.search(r"(?m)^\*\*Owner: (.+)\.\*\*$", implement)
    worker_route = re.search(r"(?m)^\*\*Staged worker: (.+)\.\*\*$", implement)
    assert owner_route is not None and worker_route is not None
    assert "Review" in owner_route.group(1) and "Lock" in owner_route.group(1)
    assert worker_route.group(1).endswith("Return")
    assert "Review" not in worker_route.group(1)
    assert "Lock" not in worker_route.group(1)
    assert re.findall(r"(?m)^- \*\*([^*]+):\*\*", implement)[:2] == [
        "Owner",
        "Staged worker",
    ]


def test_local_tracker_closeout_enters_the_lock_snapshot() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_tree = implement.index("Capture the immutable **review tree**")
    closeout = implement.index("For repo-local trackers, record it")
    lock_tree = implement.index("Capture the **lock tree**")

    assert review_tree < closeout < lock_tree
    assert "Mutation read-back" in implement
    assert "git diff <review-tree> <lock-tree>" in implement


def test_diagnosis_returns_to_one_implementation_owner() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    packet = diagnosing.split("Return one diagnosis packet containing:", 1)[1]
    assert len(re.findall(r"(?m)^- ", packet)) >= 7
    rows = set(
        re.findall(
            r"(?m)^\| `([a-z0-9-]+)` \| (Load|Invoke|Compose|Hand off|Recommend and stop) \| `\$([a-z0-9-]+)` \|",
            relationships,
        )
    )
    assert ("diagnosing-bugs", "Recommend and stop", "implement") in rows
    assert all(
        not (caller == "diagnosing-bugs" and callee == "improve-codebase-architecture")
        for caller, _, callee in rows
    )


def test_runtime_composition_edges_respect_invocation_policy() -> None:
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )
    rows = re.findall(
        r"(?m)^\| `([a-z0-9][a-z0-9-]*)` \| "
        r"(Load|Invoke|Compose|Hand off|Recommend and stop) \| "
        r"`\$([a-z0-9][a-z0-9-]*)` \|",
        relationships,
    )
    edges = set(rows)

    required = {
        ("grill-with-docs", "Compose", "grilling"),
        ("grill-with-docs", "Compose", "domain-modeling"),
        ("grilling", "Recommend and stop", "research"),
        ("grilling", "Recommend and stop", "prototype"),
        ("grilling", "Recommend and stop", "handoff"),
        ("to-spec", "Load", "codebase-design"),
        ("wayfinder", "Invoke", "research"),
        ("wayfinder", "Invoke", "prototype"),
        ("wayfinder", "Invoke", "grill-with-docs"),
        ("wayfinder", "Recommend and stop", "domain-modeling"),
        ("wayfinder", "Recommend and stop", "to-spec"),
        ("wayfinder", "Recommend and stop", "to-tickets"),
        ("wayfinder", "Recommend and stop", "implement"),
        ("triage", "Invoke", "grill-with-docs"),
        ("improve-codebase-architecture", "Invoke", "grill-with-docs"),
        ("implement", "Invoke", "tdd"),
        ("implement", "Invoke", "diagnosing-bugs"),
        ("implement", "Invoke", "review"),
        ("implement", "Invoke", "convergent-pr-review"),
        ("review", "Hand off", "convergent-pr-review"),
        ("convergent-pr-review", "Hand off", "review"),
        ("parallel-implement", "Invoke", "convergent-pr-review"),
        ("parallel-implement", "Invoke", "resolving-merge-conflicts"),
        ("resolving-merge-conflicts", "Invoke", "diagnosing-bugs"),
        ("improve-codebase-architecture", "Invoke", "research"),
        ("improve-codebase-architecture", "Load", "codebase-design"),
        ("improve-codebase-architecture", "Invoke", "codebase-design"),
        ("improve-codebase-architecture", "Recommend and stop", "implement"),
        ("improve-codebase-architecture", "Recommend and stop", "to-tickets"),
        ("improve-codebase-architecture", "Recommend and stop", "to-spec"),
        ("tdd", "Hand off", "diagnosing-bugs"),
        ("tdd", "Hand off", "prototype"),
        ("tdd", "Recommend and stop", "codebase-design"),
        ("tdd", "Recommend and stop", "improve-codebase-architecture"),
        ("diagnosing-bugs", "Hand off", "tdd"),
        ("diagnosing-bugs", "Recommend and stop", "implement"),
        ("implement", "Recommend and stop", "to-tickets"),
        ("to-tickets", "Recommend and stop", "implement"),
        ("to-tickets", "Recommend and stop", "parallel-implement"),
        ("wayfinder", "Recommend and stop", "repo-bootstrap"),
        ("triage", "Recommend and stop", "repo-bootstrap"),
        ("to-spec", "Recommend and stop", "repo-bootstrap"),
        ("to-spec", "Recommend and stop", "to-tickets"),
        ("to-tickets", "Recommend and stop", "repo-bootstrap"),
        ("handoff", "Recommend and stop", "repo-bootstrap"),
        ("improve-codebase-architecture", "Recommend and stop", "repo-bootstrap"),
    }

    assert required <= edges

    skill_names = {skill.name for skill in CUSTOM.iterdir() if skill.is_dir()}
    for caller, verb, callee in rows:
        assert caller in skill_names
        assert callee in skill_names
        if verb != "Recommend and stop":
            assert implicit_policy(CUSTOM / callee), (
                f"{caller} cannot {verb} explicit-only skill {callee}; "
                "recommend it and stop instead"
            )


def test_router_and_synthesis_keep_active_ownership_unambiguous() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    synthesis_index = (ROOT / "docs/synthesis/README.md").read_text(encoding="utf-8")
    language = (ROOT / "docs/synthesis/language-direction.md").read_text(
        encoding="utf-8"
    )
    spine = (ROOT / "docs/synthesis/target-spine.md").read_text(encoding="utf-8")

    assert "Historical upstream-language decision record" in synthesis_index
    assert "Status: historical synthesis snapshot." in language
    assert "Do not execute the Proposed Changes." in language
    assert "in-scope findings are fixed" not in spine
    assert "every finding is actionable and source-backed" in spine
    assert "support tickets" not in tickets
    assert "support slices" in tickets
