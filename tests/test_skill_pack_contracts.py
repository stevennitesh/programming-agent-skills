from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

from scripts import validate_skills


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

    assert skill_names - {"skill-router"} <= {
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


def test_github_closeout_clears_dependency_frontier_safely() -> None:
    github_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
    )
    required = (
        "**Close implemented items:** yes.",
        "close the implementation issue as completed",
        "Preserve dependency links",
        "**Non-completed closure**",
        "false-ready frontier",
        "affected dependents",
        "resulting frontier",
    )

    for tracker in github_trackers:
        text = tracker.read_text(encoding="utf-8")
        for token in required:
            assert token in text, f"{tracker} is missing {token}"

    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    assert "GitHub default: yes" in bootstrap
    assert "GitLab default: no" in bootstrap


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
    assert "marker identifies a legacy setup" in bootstrap
    assert "a different fingerprint identifies an outdated setup" in bootstrap
    assert validate_skills.validate_setup_schema_manifest(ROOT) == []


def test_portable_fallback_adoption_removes_the_portable_contract_owner() -> None:
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )

    assert "replace its portable title and owner preamble" in bootstrap
    failures = validator["portable_owner_failures"](fallback)
    assert failures == [
        "AGENTS.md still declares the portable engineering-contract owner; "
        "complete portable-fallback adoption through $repo-bootstrap."
    ]
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


def test_outdated_setup_routes_to_repo_bootstrap() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    template = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )

    assert "missing or outdated setup contract" in router
    assert "missing or outdated repo setup surface" in template


def test_router_returns_exactly_one_next_skill() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")

    assert "Route the current situation to exactly one next skill" in router
    assert "skill or flow" not in router
    assert "`$to-spec` then `$to-tickets`" not in router


def test_branch_heavy_skills_disclose_branch_procedure() -> None:
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")

    assert "[ATTENTION-SCAN.md](ATTENTION-SCAN.md)" in triage
    assert "[SPECIFIC-ITEM.md](SPECIFIC-ITEM.md)" in triage
    assert "[QUICK-OVERRIDE.md](QUICK-OVERRIDE.md)" in triage
    assert "## Specific Item" not in triage
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

    assert "When loaded only as vocabulary" in design
    assert "retain the caller's artifact, mutation boundary, and completion criterion" in design
    assert "recommend `$improve-codebase-architecture` and stop" in design
    assert "Orient -> Diagnose -> Deepen -> Compare -> Recommend" in direct
    assert "Recommend `$improve-codebase-architecture` and stop" in direct
    assert "Classify -> Place -> Substitute -> Replace -> Migrate" in deepening
    for category in (
        "In-process",
        "Local-substitutable",
        "Remote-owned",
        "True external",
    ):
        assert category in deepening
    assert "add, rewrite, keep, or delete" in deepening
    assert "Frame -> Diverge -> Compare -> Commit" in alternatives
    assert "at least three genuinely different interfaces" in alternatives


def test_wayfinder_chart_preserves_unresolved_child_decisions() -> None:
    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(encoding="utf-8")

    assert "**charting bound**" in wayfinder
    assert "Defer it explicitly to a named Wayfinder ticket" in wayfinder
    assert "zero tickets have recorded outcomes" in wayfinder
    assert "exactly one selected ticket has a substantive outcome" in wayfinder
    assert "every other ticket mutation is consequence-only" in wayfinder
    assert "**Bound.**" in grill_docs
    assert "caller bounds" in grill_docs
    assert "caller's named artifact or workflow" in grill_docs


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
    assert "$grill-with-docs` is the sole composer" in relationships
    for verb in ("Compose", "Disclose", "Bound", "Reconcile", "Return"):
        assert f"**{verb}.**" in grill_docs
    assert "confirmed domain terms may update routed domain docs" in grill_docs
    assert "ADRs require explicit approval" in grill_docs
    assert "complete domain delta" in grill_docs
    assert "changed paths and ADR outcomes" in grill_docs


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")

    for verb in ("Trace", "Challenge", "Resolve", "Persist", "Return"):
        assert f"**{verb}.**" in domain

    assert "[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)" in domain
    assert "[ADR-FORMAT.md](./ADR-FORMAT.md)" in domain
    assert "explicit request or user approval" in domain
    assert "Mutate only `CONTEXT.md`, `CONTEXT-MAP.md`, and ADR files" in domain
    assert "Return a **domain delta**" in domain


def test_grilling_preserves_one_decision_confirmed_exit_and_evidence_routes() -> None:
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")

    for verb in ("Orient", "Find", "Pressure", "Ask", "Confirm", "Pause", "Return"):
        assert f"**{verb}.**" in grilling

    required = (
        "exactly one decision",
        "cite every load-bearing fact",
        "The user owns every material decision",
        "recommendations remain advisory",
        "Repeat **Pressure -> Ask** until **Confirm** or **Pause**",
        "every material branch is resolved or explicitly deferred",
        "only after the user confirms shared understanding",
        "Recommend `$research`",
        "`$prototype` for runnable evidence",
        "Recommend `$handoff`",
        "Return the packet to an invoking caller",
        "Leave the plan unexecuted",
    )
    for token in required:
        assert token in grilling


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "discover the repository default branch and merge base" in review
    assert "Base ref: `main`" not in convergent
    assert "distinct but non-independent" in convergent
    assert "reduced-confidence" in convergent
    assert "Hand off local PRs or high-risk local diffs to $convergent-pr-review" in review
    assert "Hand off ordinary fixed-point Standards/Spec review to $review" in convergent


def test_convergent_review_uses_fresh_context_and_root_only_fanout() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    required = (
        '**Fresh-context independence:**',
        'fork_turns="none"',
        "The review root is the only dispatcher.",
        "Reviewers never spawn subagents",
        "Parent-context forks do not satisfy independence.",
        "Do not resend the whole ledger",
        "Inline it when compact.",
        "A Git commit or tree SHA is already immutable",
        "the review root may finish that reading while reviewers run",
    )
    for token in required:
        assert token in convergent

    assert "Record the packet path and content hash." not in convergent


def test_convergent_review_returns_a_lock_usable_decision() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    required = (
        "**Review decision:** return exactly one:",
        "`pass with residual risk`",
        "The review root owns this decision.",
        "The caller owns whether `pass with residual risk` is acceptable for Lock.",
        "No `candidate` or `unverified` item survives the final report.",
        "No accepted findings; disputed: <IDs>.",
        "A required pre-capture ref fetch may update Git metadata",
        "PR reviews or comments",
        "Follow `docs/agents/issue-tracker.md` for PR and issue transport",
    )
    for token in required:
        assert token in convergent

    assert "unavailable verification -> `not checked`" not in convergent
    assert (
        "`review`, `convergent-pr-review`, `wayfinder`" in relationships
    )


def test_convergent_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    assert "For a branch or PR, compare the current target head with the captured head." in convergent
    assert "For a live worktree, compare the current `HEAD`, index, status, and in-scope untracked content with the captured snapshot." in convergent
    assert "changed from the pinned fixed point" not in convergent


def test_implement_selects_one_risk_scaled_review_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    assert "Invoke exactly one route:" in implement
    assert "`$review` for an ordinary diff" in implement
    assert "`$convergent-pr-review` for a local PR or matching high-risk diff" in implement
    assert "repeat the selected route" in implement


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
    assert "Apply the caller-loaded engineering contract when supplied" in tdd


def test_tdd_routes_architecture_followups_by_scope() -> None:
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")

    assert (
        "Recommend `$codebase-design` and stop for one bounded interface or seam "
        "question. Recommend `$improve-codebase-architecture` and stop for a wide "
        "candidate-finding survey."
    ) in refactoring
    assert "Recommend `$codebase-design` or `$improve-codebase-architecture`" not in refactoring


def test_bug_routing_is_disjoint_and_non_bouncing() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tdd_tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    uncertain = "exact symptom, cause, or trusted red-capable reproduction is uncertain"
    known = (
        "expected behavior, the exact symptom, the cause, and a trusted "
        "red-capable reproduction are known"
    )
    for text in (diagnosing, tdd, implement, worker, router, relationships):
        assert uncertain in text
        assert known in text

    assert "are known before Phase 1" in diagnosing
    assert "**Relentless diagnosis:**" in diagnosing
    assert uncertain in diagnosing.split("---", 2)[1]
    assert uncertain in tdd.split("---", 2)[1]
    assert known in tdd.split("---", 2)[1]
    assert "Use for red-testable new behavior. Use for bug fixes only when" in tdd.split(
        "---", 2
    )[1]
    assert "Use `$tdd` directly for known-repro bugs." not in tdd
    assert "Apply the bug ownership gate in [SKILL.md](SKILL.md)" in tdd_tests
    assert "known-repro bugs" not in tdd_tests
    assert "the router owns the exact diagnosis/TDD boundary" in readme
    assert "Known behavior with a red-capable seam" not in readme
    assert "Behavior and a trusted reproduction are already known" not in relationships
    assert "with this lane worker as its caller" in worker
    assert "WorkerBrief --> Debug" in relationships


def test_workflow_trace_matches_to_spec_publication_authority() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    transcript = (
        ROOT
        / "docs/validation/transcripts/2026-07-13-whole-pack-workflow-traces.md"
    ).read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "to-spec")
    assert "and publish it to the configured tracker" in to_spec
    assert "Apply the **approval gate**" not in to_spec
    assert (
        "Its explicit invocation authorizes the bounded `.tmp/` draft and one "
        "published parent spec"
    ) in transcript
    assert "both publication gates wait for approval/read-back" not in transcript


def test_implementation_closeout_requires_the_spec_axis() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (review, convergent):
        assert "`Spec required: yes | no`" in text
        assert "Default to `no` for standalone review." in text
        assert "never skip or replace the Spec axis" in text

    assert "When `Spec required: yes`" in review
    assert "When `Spec required: yes`" in convergent
    assert "return `incomplete` before reviewer dispatch" in convergent
    assert "`Spec required: yes`, the selected work item" in implement
    assert "`Spec required: yes`, the run Source Trace" in parallel
    assert (
        "Accepted residual risk must be authorized by the selected item, repo "
        "policy, or user"
    ) in implement
    for text in (review, convergent):
        assert (
            "Carry the caller-supplied Spec requirement, Source Trace and Spec "
            "sources, fixed point, and captured target into the handoff."
        ) in text
    assert "an incomplete Spec axis keeps Lock closed" in parallel


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
        assert "direct fresh-context" in text
        assert "never edit files, mutate external state, or spawn" in text

    assert "same self-contained factual brief" in design
    assert "Exclude parent hypotheses, preferred solutions, other candidates, and peer results." in design
    assert "fork only the minimum necessary recent context" in design
    assert "main agent may contribute one independent design" not in design
    assert "one complete research contract" in research
    assert "main agent alone judges evidence and writes the note" in research
    assert "one bounded region or pressure" in architecture
    assert "main agent alone owns synthesis" in architecture


def test_writing_great_skills_authorizes_bounded_direct_subagents() -> None:
    writing = (CUSTOM / "writing-great-skills/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "## Delegation" in writing
    assert "**Delegate legwork:**" in writing
    assert "invocation authorizes direct subagents without separate confirmation" in writing
    assert "bounded, read-only evidence lane" in writing
    assert 'fork_turns="none"' in writing
    assert "direct children do not spawn" in writing
    assert (
        "the root owns required source reading, judgment, synthesis, edits, "
        "verification, and completion"
    ) in writing


def test_merge_conflict_resolution_is_three_way_and_finish_bounded() -> None:
    skill_dir = CUSTOM / "resolving-merge-conflicts"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert implicit_policy(skill_dir)
    required = (
        "three-way merge",
        "`git ls-files -u`",
        "during rebase, `ours` is the so-far rebased target",
        "in-scope content or path conflict",
        "Block before continuation if unrelated index state would enter its commit.",
        "A new conflict returns to **State**; repeat until Git exits",
        "**Reconciliation authority** means the user asked to resolve the in-scope conflicts.",
        "Without reconciliation authority, stop after **State** and **Trace** with a read-only report.",
        "Leave files, the index, commits, and Git-operation state unchanged.",
        "Without finish authority, leave staging, commit, and continuation untouched.",
        "hand off an uncertain failure to `$diagnosing-bugs`",
        "Authorized reconciliation is complete only when every in-scope unmerged entry and marker is reconciled.",
        "A blocked path returns a blocked outcome with exact remaining state",
    )
    for token in required:
        assert token in skill

    assert 'Conflict -. "uncertain post-resolution failure" .-> Debug' in relationships
    assert "`resolving-merge-conflicts`, `review`" in relationships


def test_portable_fallback_carries_the_standalone_engineering_contract() -> None:
    loop = "Orient -> Explore -> Decide -> Prove -> Cover -> Converge -> Simplify -> Lock"
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")

    assert loop in fallback
    assert loop in contract
    assert "Portable Engineering Contract" in bootstrap
    assert re.findall(r"\$[a-z0-9][a-z0-9-]*", fallback) == []
    assert len(fallback.split()) <= 950
    assert not any(line.startswith("  ") for line in fallback.splitlines())

    required = (
        "**Source trace:**",
        "**Bounded slice:**",
        "**Semantic proof:**",
        "one highest-leverage decision",
        "against primary sources",
        "Staging, commits, pushes, PRs, tracker changes, deployments, messages",
        "Parallelize only independent write scopes",
        "observe RED before GREEN",
        "known-good example",
        "production implementation",
        "One axis passing never hides the other failing.",
        "Lock only when",
        "at the authorized boundary",
    )
    for token in required:
        assert token in fallback


def test_readme_exposes_both_adoption_paths() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    required = (
        '<h1 align="center">Programming Agent Skills</h1>',
        "img.shields.io/badge/License-MIT",
        "img.shields.io/badge/Python-3.10%2B",
        "## How It Works",
        "flowchart LR",
        "| Common agent failure | Pack response |",
        "| Full Skill Pack | Portable Contract |",
        "### Full Skill Pack",
        "### Portable Contract Only",
        "[`AGENTS_PORTABLE_FALLBACK.md`](AGENTS_PORTABLE_FALLBACK.md)",
        "without installing skills",
        "Choose one engineering-contract owner per repository",
        "## Using The Full Pack",
    )
    for token in required:
        assert token in readme

    assert readme.count("```mermaid") == 1


def test_triage_branches_share_the_authoritative_brief_schema() -> None:
    examples = (CUSTOM / "triage/AGENT-BRIEF-EXAMPLES.md").read_text(encoding="utf-8")
    brief = (CUSTOM / "triage/AGENT-BRIEF.md").read_text(encoding="utf-8")

    assert brief.count("**Proof lane:**") == 1
    assert "| Branch | Emphasize |" in examples
    for branch in ("Bug tracer", "Enhancement tracer", "Support slice", "PR finish"):
        assert f"| {branch} |" in examples


def test_mutating_workflows_require_readback() -> None:
    for name in ("implement", "parallel-implement", "to-spec", "to-tickets", "wayfinder"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "Mutation read-back" in text, name


def test_to_tickets_preserves_approval_coverage_and_frontier_contract() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")

    required = (
        "Apply the **coverage gate**",
        "Get explicit user approval",
        "before publishing",
        "exactly one next action",
        "recommend `$implement`",
        "recommend `$parallel-implement`",
    )
    for token in required:
        assert token in tickets


def test_worker_modes_have_distinct_completion_artifacts() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "**staged worker**" in contract
    assert "**lane worker**" in contract
    assert "**Staged worker:**" in implement
    assert "**Lane workers**" in parallel


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
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

    assert "**Two isolations:**" in parallel
    assert "ready frontier -> two isolations -> fresh-context lane workers" in parallel
    assert "worktree lock" not in parallel
    assert "A delegated lane is ready only when both are established" in parallel
    assert "**Root-only fan-out:**" in parallel
    assert "**Slot lock:**" in parallel
    assert "the smaller of three or the live slots remaining" in parallel
    assert 'fork_turns="none"' in parallel
    assert "**Default lane route:**" in parallel
    assert "Before formal review, verify that no lane agent is running." in parallel
    assert "the integration lane produced a review-ready packet" in parallel
    assert "**Workspace boundary:**" in worker
    assert "**One worker, one lane, one packet:**" in worker
    assert "Do not dispatch subagents or invoke `$review`" in integrator
    assert "## Review-Ready Handoff" in integrator
    assert "`spawn_agent` creates a child context" in launch
    assert 'git worktree add --detach' in launch
    assert "## Explicit Background Task" in launch
    assert "only when the user explicitly asks" in launch
    assert "**Formal review owner:** `orchestrator`" in ledger
    assert "IntegratorBrief --> Review" not in relationships
    assert "IntegratorBrief -. \"ledger-approved only\" .-> CPR" not in relationships
    assert "integration lane executes only that route" not in parallel
    assert "dispatch its reviewer subagents" not in integrator
    assert "native internal worktree" not in parallel
    assert "native internal worktree" not in worker
    assert "native internal worktree" not in launch
    assert "native internal worktree" not in ledger


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
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

    required_parallel = (
        "Run two or more ready, non-overlapping work items as a wavefront",
        "**Frontier gate:**",
        "Non-overlapping files do not prove semantic independence.",
        "**Resume gate:**",
        "do not redispatch or reland them",
        "**Worker status:**",
        "**Conflict gate:**",
        "Invoke `$resolving-merge-conflicts`",
        "**Review acceptance:**",
        "`pass with residual risk` unlocks only when",
        "The selected run authorizes scoped worker commits",
        "record one landing mode and one executor",
        "verify that the remote branch or PR head resolves to the approved closeout `HEAD`",
        "Return exactly one ledger Outcome: `complete`, `partial`, or `blocked`.",
        "A `partial` or `blocked` outcome does not claim an approved closeout `HEAD`",
        "no active lane or unaccounted partial mutation",
    )
    for token in required_parallel:
        assert token in parallel

    assert parallel.count("**Shallow mode:**") == 1
    assert "micro-worker" not in parallel
    assert "downshift or serialize" not in parallel

    assert "**Integration context:**" in worker
    assert "**Report transport:**" in worker
    assert "next need:" in worker
    assert "**Landing mode:**" in integrator
    assert "recorded landing mode, and landing authority" in integrator
    assert "Preserve the partial state for the orchestrator's Conflict gate." in integrator
    assert "fresh lane worker required" in integrator
    assert "micro-worker" not in integrator

    assert "Dirty state, untracked work, or an unpreserved commit blocks cleanup." in launch
    assert "Forced removal and branch deletion require explicit destructive authority." in launch

    for token in (
        "**Landing mode:**",
        "<scope/downshift/resume/frontier/",
        "**Current integration HEAD:**",
        "**Current Git state:**",
        "**Blockers:**",
        "**Next owner:**",
        "**Remaining permissions or mutations:**",
    ):
        assert token in ledger

    assert (
        "| `parallel-implement` | Invoke | `$resolving-merge-conflicts` |"
        in relationships
    )


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    required = (
        "Implement one selected ready work item through review, one commit, and repo-policy closeout",
        "**Select -> Patch -> Review -> Lock -> Close**",
        "Owner mode is the default.",
        "Staged-worker mode requires an explicit assignment and accepting owner.",
        "A parent spec, plan, queue, batch, list, or bare source path is context, not implementation scope.",
        "An explicit target is binding.",
        "report that gate instead of substituting another item",
        "Ask when it does not identify one next item.",
        "Selection reads state; it does not split, relabel, promote, reprioritize, or otherwise repair it.",
        "Owner-mode invocation authorizes in-scope staging, one commit, and repo-policy closeout.",
        "Push, deployment, PR creation, destructive Git, and unrelated external mutations require separate authority.",
    )

    for token in required:
        assert token in implement


def test_local_tracker_closeout_enters_the_lock_snapshot() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_tree = implement.index("Capture the immutable **review tree**")
    closeout = implement.index("For repo-local trackers, record it")
    lock_tree = implement.index("Capture the **lock tree**")

    assert review_tree < closeout < lock_tree
    assert "apply Mutation read-back, and stage the tracker file" in implement
    assert "Only verified closeout metadata may differ from the reviewed tree" in implement
    assert "Any implementation, behavior, scope, or contract delta returns to Review" in implement
    assert "Review: pending" not in implement


def test_diagnosis_returns_to_one_implementation_owner() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")

    assert "invoke `$diagnosing-bugs` in fix mode" in implement
    assert "resume here after regression proof" in implement
    assert "A caller-invoked run returns its diagnosis packet to that caller" in diagnosing
    assert "A standalone diagnosis-only run recommends `$implement`" in diagnosing
    assert "**Return owner:**" in diagnosing


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
        ("to-spec", "Load", "codebase-design"),
        ("wayfinder", "Invoke", "research"),
        ("wayfinder", "Invoke", "prototype"),
        ("wayfinder", "Invoke", "grill-with-docs"),
        ("triage", "Invoke", "grill-with-docs"),
        ("implement", "Invoke", "tdd"),
        ("implement", "Invoke", "diagnosing-bugs"),
        ("implement", "Invoke", "review"),
        ("implement", "Invoke", "convergent-pr-review"),
        ("review", "Hand off", "convergent-pr-review"),
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
        ("to-tickets", "Recommend and stop", "repo-bootstrap"),
        ("handoff", "Recommend and stop", "repo-bootstrap"),
        ("improve-codebase-architecture", "Recommend and stop", "repo-bootstrap"),
    }

    assert required <= edges

    source_wording = {
        CUSTOM / "grill-with-docs/SKILL.md": "`$grilling` session with `$domain-modeling` active throughout",
        CUSTOM / "to-spec/SKILL.md": "Load `$codebase-design` as shared architecture vocabulary",
        CUSTOM / "triage/SPECIFIC-ITEM.md": "invoke `$grill-with-docs`",
        CUSTOM / "implement/SKILL.md": "invoke `$diagnosing-bugs` in fix mode",
        CUSTOM / "parallel-implement/SKILL.md": "the orchestrator invokes `$review` by default",
        CUSTOM / "review/SKILL.md": "Hand off to `$convergent-pr-review` and stop",
        CUSTOM / "tdd/SKILL.md": "Hand off to `$diagnosing-bugs`",
        CUSTOM / "codebase-design/DIRECT-DESIGN.md": "Recommend `$improve-codebase-architecture` and stop",
    }
    for path, token in source_wording.items():
        assert token in path.read_text(encoding="utf-8"), f"{path} is missing {token}"

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

    assert "configured external PR/MR intake" in router
    assert "**Triage / Review:**" in router
    assert "Historical upstream-language decision record" in synthesis_index
    assert "Status: historical synthesis snapshot." in language
    assert "Do not execute the Proposed Changes." in language
    assert "in-scope findings are fixed" not in spine
    assert "every finding is actionable and source-backed" in spine
    assert "support tickets" not in tickets
    assert "support slices" in tickets
