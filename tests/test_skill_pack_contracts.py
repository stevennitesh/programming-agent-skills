from __future__ import annotations

import json
import re
from pathlib import Path

from scripts import validate_skills


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


def test_wayfinder_chart_preserves_unresolved_child_decisions() -> None:
    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(encoding="utf-8")

    assert "**charting bound**" in wayfinder
    assert "Defer it explicitly to a named Wayfinder ticket" in wayfinder
    assert "zero tickets have recorded outcomes" in wayfinder
    assert "exactly one selected ticket has a substantive outcome" in wayfinder
    assert "every other ticket mutation is consequence-only" in wayfinder
    assert "When a caller supplies a bound" in grill_docs


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

    assert "**Review route:** Invoke `$review` by default." in implement
    assert "Invoke `$convergent-pr-review` for a local PR or high-risk diff matching its trigger." in implement
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
    assert "Apply the caller-loaded engineering contract when supplied" in tdd


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
        "Without finish authority, leave staging, commit, and continuation untouched.",
        "hand off an uncertain failure to `$diagnosing-bugs`",
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
        "Implement exactly one selected ready work item through staging, review, one commit, and repo-policy tracker closeout",
        "A parent spec, plan, queue, batch, list, or bare source path is selection context, not implementation scope.",
        "**Explicit target:**",
        "stop on that target",
        "**No target:**",
        "repo-visible readiness, dependency, and ordering policy",
        "ask instead of choosing by taste",
        "**Selection boundary:**",
        "Do not substitute, split, relabel, promote, or reprioritize tracker state.",
        "Explicit owner-mode invocation authorizes selected-work staging, one commit, and tracker closeout allowed by repo policy.",
        "Push, deployment, PR creation, unrelated external messages, and destructive Git require separate authority.",
    )

    for token in required:
        assert token in implement


def test_local_tracker_closeout_enters_the_review_snapshot() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    pending = implement.index("`Review: pending`")
    review_tree = implement.index("Capture the immutable **review tree**")
    resolved = implement.index("replace `Review: pending`")

    assert pending < review_tree < resolved
    assert "refresh the provisional closeout metadata" in implement
    assert "the review-result field is the only post-review metadata change" in implement


def test_diagnosis_returns_to_one_implementation_owner() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")

    assert "invoke `$diagnosing-bugs` in fix mode" in implement
    assert "then returns here for Converge" in implement
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
        ("diagnosing-bugs", "Hand off", "tdd"),
        ("diagnosing-bugs", "Recommend and stop", "implement"),
    }

    assert required <= edges

    source_wording = {
        CUSTOM / "grill-with-docs/SKILL.md": "Compose one `$grilling` session with `$domain-modeling` active throughout.",
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
