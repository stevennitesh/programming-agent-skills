from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

from scripts import campaign_artifacts, skill_pack_contract, validate_skills


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
    handoff_flat = " ".join(handoff.split())

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
    assert "<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>[-<NN>].md" in handoff
    assert "$repo-bootstrap" in handoff
    for contract in (
        "receiver can read the same work root",
        "never overwrite",
        "read first` or `conditional",
        "exact condition that requires proof to rerun",
        "Do not route here",
        "refresh its volatile Current State",
        "only if its authority and preconditions still hold",
        "Do not create or message the receiving task",
    ):
        assert contract in handoff_flat


def test_to_questionnaire_owns_one_safe_recipient_artifact() -> None:
    skill_dir = CUSTOM / "to-questionnaire"
    questionnaire = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    questionnaire_flat = " ".join(questionnaire.split())
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert re.findall(r"(?m)^\*\*([A-Za-z]+)\.\*\*", questionnaire) == [
        "Boundary",
        "Admit",
        "Lock",
        "Gap",
        "Draft",
        "Cover",
        "Save",
        "Verify",
        "Return",
    ]
    for contract in (
        "Grill the send, not the subject.",
        "facts, judgment, or decision authority unavailable from inspectable sources",
        "missing sender-known information that materially changes",
        "skill defaults are not assumptions",
        "Invite partial answers and explicit unknowns.",
        "Treat the default as disposable.",
        "The catch-all does not cover a known ledger item.",
        "<work-root>/.tmp/to-questionnaire/<slug>.md",
        "resolve the absolute `.md` target",
        "overwrite of that exact target is authorized",
        "Refresh that state immediately before Save.",
        "Render and reread the complete candidate",
        "changed only the authorized file",
        "Status: Questionnaire ready | Not admitted | Incomplete",
        "origin owner and identity are context for returning answers",
        "Origin owner and identity:",
        "Answers return to:",
        "Artifact path: <absolute path> | none",
        "Artifact durability: disposable default | authorized durable path | none",
        "Delivery: not performed",
        "`Questionnaire ready` requires one verified artifact",
        "`Not admitted` requires a proven failed Admit predicate",
        "`Incomplete` names missing intake",
    ):
        assert contract in questionnaire_flat
    for rejected in ("Wayfinder", ".scratch/to-questionnaire"):
        assert rejected not in questionnaire
    assert policy.endswith("policy:\n  allow_implicit_invocation: false\n")
    assert skill_pack_contract.tree_hash(skill_dir) == (
        "18fb2f5e88ac8764092605e198c1bb002a7a84a7bdd184592bac18c6a7637ed7"
    )
    assert (
        "| One external stakeholder holds missing knowledge and needs an async "
        "discovery questionnaire | `$to-questionnaire` |"
    ) in router
    assert "`$to-questionnaire` for an external stakeholder" in grilling


def test_tracker_templates_share_ready_state_navigation_and_readback() -> None:
    trackers = [
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    ]
    required = (
        "**Ready-for-agent state**",
        "**Ready-for-human state**",
        "navigation metadata",
        "not proof of content completeness",
        "$triage",
        "$to-tickets",
        "**Ready query**",
        "agent and human frontiers separately",
        "**Mutation read-back**",
        "partial mutation is blocked",
    )
    producer_owned = (
        "Source Trace",
        "observable acceptance criteria",
        "proof lane",
        "expected write scope",
        "parallel-safety note",
        "scope fence",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for token in required:
            assert token in normalized, f"{tracker} is missing {token}"
        work_items = " ".join(
            text.split("## Work-item operations", 1)[1].split()
        ).lower()
        for token in producer_owned:
            assert token.lower() not in work_items, f"{tracker} still owns {token}"


def test_wayfinder_tracker_claims_distinguish_sessions_and_recover_explicitly() -> None:
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )
    for tracker in trackers:
        wayfinding = tracker.read_text(encoding="utf-8").split(
            "## Wayfinding operations", 1
        )[1]
        wayfinding_flat = " ".join(wayfinding.split())
        for token in (
            "MAP-FORMAT.md",
            "Resolution owner:",
            "Re-entry owner: $wayfinder",
            "diagnosis",
            "approved map order",
            "Claim token:",
            "Claimed at:",
            "codex/<lowercase UUIDv4>",
            "<YYYY-MM-DDTHH:MM:SSZ>",
            "Maintain claims the map",
            "claims the map before recording any ticket outcome",
            "reuse it for both claims",
            "waiting",
            "exact return trigger",
            "through Advance",
            "never reuse it across invocations",
            "different token owns the item",
            "Elapsed time alone never makes a claim stale.",
            "explicit user approval",
            "takeover reason",
            "Mutation read-back",
        ):
            assert token in wayfinding_flat, f"{tracker} is missing {token}"
        assert "Its body holds Destination" not in wayfinding


def test_repo_bootstrap_validates_wrapped_provider_specific_wayfinder_prose() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["wayfinder_contract_failures"]
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        assert check(text, str(tracker)) == []

    hosted = trackers[0].read_text(encoding="utf-8").replace(
        "wait by adding the waiting marker", "wait without a marker"
    )
    assert any(
        "wait by adding the waiting marker" in item
        for item in check(hosted, "hosted")
    )

    local = " ".join(trackers[2].read_text(encoding="utf-8").split()).replace(
        "set `Waiting` with its return record", "record an unspecified pause"
    )
    assert any(
        "set `Waiting` with its return record" in item
        for item in check(local, "local")
    )


def test_triage_label_template_respects_tracker_pr_policy() -> None:
    labels = (CUSTOM / "repo-bootstrap/triage-labels.md").read_text(encoding="utf-8")
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    triage_flat = " ".join(triage.split())

    assert "Every triaged work item" in labels
    assert "Every triaged issue or PR" not in labels
    assert "Triage PRs only when the tracker enables them" in triage_flat


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


def test_github_relationship_modes_are_explicit_before_publication() -> None:
    github_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
    )
    for tracker in github_trackers:
        text = tracker.read_text(encoding="utf-8")
        assert "**Parent / child mode:** native-sub-issues." in text
        assert "**Dependency mode:** native-dependencies." in text
        assert "Resolve the authenticated operation and read-back route before" in text
        assert "never switch representations during a publication" in text
        assert "when available" not in text

    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    normalized_tickets = " ".join(tickets.split())
    assert "resolve their operation and read-back routes once before" in (
        normalized_tickets
    )
    assert "The first authorized child and its read-back prove live" in (
        normalized_tickets
    )
    assert "first applicable blocking edge" in normalized_tickets
    assert (
        "Never switch the frozen relationship representation" in normalized_tickets
    )


def test_repo_bootstrap_rejects_unconfigured_github_relationship_modes() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    tracker = (ROOT / "docs/agents/issue-tracker.md").read_text(encoding="utf-8")
    check = validator["github_relationship_mode_failures"]

    assert check(tracker) == []
    invalid = tracker.replace("native-sub-issues", "when-available", 1)
    assert check(invalid) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitHub mode"
    ]
    assert check(tracker) == []


def assert_repo_bootstrap_semantic_contract(
    package_root: Path,
    expected_tree_sha256: str,
    *,
    profile: str,
) -> None:
    assert (
        campaign_artifacts.campaign_tree_hash(package_root)["sha256"]
        == expected_tree_sha256
    )
    bootstrap = (package_root / "SKILL.md").read_text(encoding="utf-8")
    domain = (package_root / "domain.md").read_text(encoding="utf-8")
    normalized = " ".join(bootstrap.lower().split())
    assert re.search(r"(?m)^name: repo-bootstrap$", bootstrap)
    assert not implicit_policy(package_root)

    if profile == "incumbent":
        assert re.findall(r"(?m)^## ([A-Za-z]+)$", bootstrap) == [
            "Inventory",
            "Reconcile",
            "Choose",
            "Draft",
            "Provision",
            "Verify",
        ]
        assert bootstrap.index("## Draft") < bootstrap.index("## Provision")
    else:
        assert profile == "m0"
        headings = [
            "Entry And Ownership",
            "Resolve And Inventory",
            "Compare And Propose",
            "Preflight And Reconcile",
            "Read Back And Validate",
            "Return",
        ]
        assert re.findall(r"(?m)^## (.+)$", bootstrap) == headings
        sections: dict[str, str] = {}
        for heading in headings:
            span = skill_pack_contract.level_two_section_span(
                bootstrap,
                f"## {heading}",
            )
            assert span is not None, (package_root, heading)
            sections[heading] = " ".join(bootstrap[slice(*span)].lower().split())
        required = (
            ("Entry And Ownership", "human explicitly names repo bootstrap|source trace|explicit approval for the exact bounded delta|does not start, resume, or complete this skill|$wayfinder"),
            ("Resolve And Inventory", "every applicable authoritative location|working tree, index, and `head`|.tmp/|.scratch/|read-only evidence|does not establish semantic compatibility or persisted mutation"),
            ("Compare And Propose", "compatible:|delta:|conflict:|not applicable:|not a pack version or behavioral proof|one exact local and remote proposal"),
            ("Preflight And Reconcile", "preflight all required local and external transitions|apply only the exact approved setup-owned delta|create only approved missing labels|refetch the authoritative label state|do not mutate tracker items, domain truth, the git index, `head`|after any partial failure, stop further mutation"),
            ("Read Back And Validate", "reread every changed file|compare each observed result with the approved proposal|index and `head` to match their pre-run identities|validation is structural proof, not mutation read-back"),
            ("Return", "compatible, changed, unchanged, blocked, and inapplicable|residual gaps|complete only when every required setup owner is compatible|setup incomplete|downstream work and the recommending workflow remain unstarted"),
        )
        for heading, obligations in required:
            assert all(
                obligation in sections[heading]
                for obligation in obligations.split("|")
            ), heading
        for forbidden in (
            "saga",
            "compensating transaction",
            "durable workflow state",
            "telemetry",
            "browser tooling",
            "if-match",
            "claim token:",
            "wayfinder:map",
        ):
            assert forbidden not in normalized
        assert "do not claim automatic rollback" in normalized
    assert "<context-root>/docs/adr/" in domain
    assert "following the context root recorded in `CONTEXT-MAP.md`" in domain
    assert "src/<context>/docs/adr/" not in domain


def test_repo_bootstrap_reconciles_existing_setup_without_reset() -> None:
    assert_repo_bootstrap_semantic_contract(
        CUSTOM / "repo-bootstrap",
        "b55d6b0cbcbbbfa0d762913051c6a90d41f47f79ac89962329c3f1b4e94a6516",
        profile="incumbent",
    )


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
    router_flat = " ".join(router.split())

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
    assert "missing, incompatible, or outdated setup surface" in router_flat
    assert (
        "| Settled source needs a durable parent decision contract before ticket "
        "slicing | `$to-spec` |"
    ) in router
    assert (
        "| A `ready-spec` or equivalent settled bounded source needs a "
        "dependency-ordered implementation ticket graph and actionable "
        "frontier | `$to-tickets` |"
    ) in router
    tie_breaker = " ".join(
        router.split("**Unknown-owner tie-breaker:**", 1)[1].split(
            "### Build", 1
        )[0].split()
    )
    for contract in (
        "`$research`",
        "`$prototype`",
        "`$to-questionnaire`",
        "`$grilling`",
        "`$grill-with-docs`",
        "only after the destination is bounded",
        "`$wayfinder`",
    ):
        assert contract in tie_breaker
    existing_code = " ".join(
        router.split("**Existing-code tie-breaker:**", 1)[1].split(
            "**Conflict tie-breaker:**", 1
        )[0].split()
    )
    for contract in (
        "selected ready item to `$implement`",
        "standalone settled red-testable behavior to `$tdd`",
        "uncertain broken behavior to `$diagnosing-bugs`",
        "existing diff needing judgment",
    ):
        assert contract in existing_code


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
    assert "Skip ordinary request verification" in quick
    assert "unseen mutation packet" in quick
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
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    design_flat = " ".join(design.split())
    direct_flat = " ".join(direct.split())
    deepening_flat = " ".join(deepening.split())
    alternatives_flat = " ".join(alternatives.split())

    assert "[DIRECT-DESIGN.md](DIRECT-DESIGN.md)" in design
    assert (
        "before planning or implementation only when one consequential"
        in design_flat
    )
    assert "Proof Seam" in design
    assert "test double alone does not earn one" in design_flat
    assert len(re.findall(r"(?m)^## \d+\. ", direct)) == 5
    for required in (
        "decision-needed",
        "evidence-gap",
        "Failure Atomicity",
        "Trust Boundaries",
        "Proof Seam establishes meaning",
        "Behavior-Owned Test Portfolio",
        "Change Closure",
    ):
        assert required in direct_flat
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
    assert "canonical test owner" in deepening_flat
    assert "Removal Trigger" in deepening_flat
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", alternatives) == [
        "Frame",
        "Diverge",
        "Compare",
        "Recommend",
    ]
    assert "**No-new-seam**" in alternatives
    assert "applicable engineering and domain obligations" in alternatives_flat
    assert "create no separate workflow step" in design_flat
    assert 'CodeDesign["codebase-design"] --> Contract' in relationships
    assert "CodeDesign --> DomainRouter" in relationships
    assert "| `to-spec` | Load | `$codebase-design` |" in relationships
    assert "| `audit-codebase` | Load | `$codebase-design` |" in relationships
    for caller in ("research", "tdd", "simplify-code"):
        assert f"| `{caller}` | Recommend and stop | `$codebase-design` |" not in (
            relationships
        )


def test_wayfinder_chart_preserves_unresolved_child_decisions() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert "[MAP-FORMAT.md](MAP-FORMAT.md)" in wayfinder
    chart, modes = wayfinder.split("### Chart", 1)[1].split("### Advance", 1)
    advance, remaining = modes.split("### Maintain", 1)
    maintain, closure = remaining.split("## Closure", 1)
    for earlier, later in (
        ("**Bound.**", "**Admit.**"),
        ("**Admit.**", "**Sweep.**"),
        ("**Sweep.**", "**Approve.**"),
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
    assert re.findall(r"(?m)^### (Chart|Advance|Maintain)$", wayfinder) == [
        "Chart",
        "Advance",
        "Maintain",
    ]
    assert "Close only while holding the map claim" in closure
    assert "zero substantive ticket outcomes" in maintain
    bound = chart.split("1. **Bound.**", 1)[1].split("2. **Admit.**", 1)[0]
    bound_flat = " ".join(bound.split())
    for field in (
        "destination owner",
        "outcome",
        "scope",
        "route-closing condition",
        "terminal kind",
        "return owner",
    ):
        assert field in bound_flat
    assert "Invoke the applicable conversational resolver" in bound_flat
    admit = chart.split("2. **Admit.**", 1)[1].split("3. **Sweep.**", 1)[0]
    admit_flat = " ".join(admit.split())
    assert "exact destination tuple" in admit_flat
    assert "at least one non-conversational resolver" in admit_flat
    assert "Wayfinding not needed" in admit_flat
    assert "recommend `$to-spec` only when the source is already ready" in admit_flat
    map_template = map_format.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", map_template) == [
        "Destination",
        "Scope Boundary",
        "Notes",
        "Decisions So Far",
        "Not Yet Specified",
        "Out Of Scope",
    ]
    assert "approved repo-local note path" in map_format
    advance_flat = " ".join(advance.split())
    assert advance_flat.index("Continue only after its exact owner") < (
        advance_flat.index("4. **Resolve.**")
    )
    chart_flat = " ".join(chart.split())
    assert chart_flat.index("[MAP-FORMAT.md](MAP-FORMAT.md)") < (
        chart_flat.index("show one complete mutation packet")
    )
    assert "repeat the destination-tuple search" in chart_flat
    assert "sole canonical match" in chart_flat
    assert "read back their exact identities, then wire" in chart_flat


def test_wayfinder_prototype_participation_matches_judgment() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    tickets = wayfinder.split("## Tickets", 1)[1].split("## Modes", 1)[0]
    tickets_flat = " ".join(tickets.split())
    for contract in (
        "`shape/feel` uses HITL, human judgment",
        "`design evidence` uses AFK and rule-based judgment by default",
        "`design evidence` uses HITL only when the caller reserves the verdict",
        "decision owner, claim level, judgment mode",
    ):
        assert contract in tickets_flat
    assert (
        "supported answer or truthful residual, supported decision implications, "
        "evidence, limits, and cleanup state"
    ) in tickets_flat

    approve = wayfinder.split("4. **Approve.**", 1)[1].split("5. **Chart.**", 1)[0]
    approve_flat = " ".join(approve.split())
    for field in (
        "decision owner",
        "claim level",
        "judgment mode",
        "human judge",
        "objective verdict criteria",
    ):
        assert field in approve_flat
    assert "Reject" in approve and "incompatible Prototype fields" in approve

    for field in (
        "Decision owner:",
        "Claim level:",
        "Judgment mode:",
        "Human judge:",
        "Verdict criteria:",
    ):
        assert field in map_format


def test_wayfinder_routes_by_authority_and_accounts_for_fog() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")
    map_flat = " ".join(map_format.split())

    tickets = wayfinder.split("## Tickets", 1)[1].split("## Modes", 1)[0]
    tickets_flat = " ".join(tickets.split())
    assert "current user owns a conversation-only decision" in tickets_flat
    assert "repository contracts and objective proof" in tickets_flat
    assert "Classify by resolution authority" in tickets_flat
    assert "Split independently resolvable" in tickets_flat
    assert "Invoke `$grilling`" in tickets_flat
    assert "Invoke `$grill-with-docs`" in tickets_flat
    assert "Pass the user as decision owner" in tickets_flat
    assert "context action, and separate ADR action" in tickets_flat
    assert "Invoke `$diagnosing-bugs` in diagnosis mode" in tickets_flat
    assert "Invoke `$to-questionnaire` only after the user explicitly approves" in (
        tickets_flat
    )
    assert "`Questionnaire ready` is `Waiting`, never an answer." in tickets_flat
    for field in (
        "Resolution owner:",
        "Resolver:",
        "Expected return:",
        "Re-entry owner: $wayfinder",
        "Type: research | prototype | diagnosis | grilling | task",
    ):
        assert field in map_format

    advance = wayfinder.split("### Advance", 1)[1].split("### Maintain", 1)[0]
    advance_flat = " ".join(advance.split())
    claim = advance.split("3. **Claim.**", 1)[1].split("4. **Resolve.**", 1)[0]
    claim_flat = " ".join(claim.split())
    assert "this invocation's token" in claim_flat
    assert "exact owner, token, and claimed-at value" in claim_flat
    assert "Waiting and the supplied attributable evidence matches" in advance_flat
    assert "validate the supplied return for a selected Waiting ticket" in advance_flat
    assert "claim the map with the same invocation token" in advance_flat
    assert "record no outcome or shared mutation" in advance_flat
    assert "Run **Closure** while the map claim is still held" in advance_flat
    assert "Release the ticket claim and read back its absence" in advance
    assert "release the map claim, read back its absence" in advance_flat
    for outcome in ("Resolved", "Blocked", "Waiting", "Out of scope"):
        assert f"**{outcome}:**" in advance

    reconcile = advance.split("5. **Reconcile.**", 1)[1].split(
        "6. **Verify.**", 1
    )[0]
    assert re.findall(r"(?m)^   - \*\*(Retain|Graduate|Resolve|Exclude):\*\*", reconcile) == [
        "Retain",
        "Graduate",
        "Resolve",
        "Exclude",
    ]
    assert "give each affected fog item exactly one disposition" in advance_flat
    assert "sole fog container" in map_flat
    assert "None - all remaining in-scope questions are ticket-owned." in map_flat
    assert "future-work owner, governing resolution, or map pointer" in map_flat
    assert "Do not create a ticket only to supply a link." in map_flat

    maintain = wayfinder.split("### Maintain", 1)[1].split("## Closure", 1)[0]
    maintain_flat = " ".join(maintain.split())
    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", maintain) == [
        "Orient",
        "Bound",
        "Approve",
        "Claim",
        "Repair",
        "Verify",
        "Expose",
    ]
    assert "Record no child outcome" in maintain_flat
    assert "claim the map" in maintain_flat
    assert "representation has drifted and no question needs an answer" in maintain_flat
    assert "scope indexes" in maintain_flat
    assert "Give affected fog one disposition" in maintain_flat

    closure = wayfinder.split("## Closure", 1)[1].split("## Return", 1)[0]
    closure_flat = " ".join(closure.split())
    assert "read back its absence" in closure_flat
    assert "invoke `$domain-modeling` once" in closure_flat
    assert "no current Domain Delta accounts for it" in closure_flat
    assert "`persist authorized` only with exact domain-write authority" in closure_flat
    assert "`render only` otherwise" in closure_flat
    assert "separate explicit approval" in closure_flat
    assert "A material Domain Delta blocker leaves the map open" in closure
    assert "compact closing packet" in closure_flat
    assert "settled parent-spec source" in closure_flat
    assert "terminal decision" in closure_flat

    returned = wayfinder.split("## Return", 1)[1]
    returned_flat = " ".join(returned.split())
    assert (
        "Next frontier: [<ticket title>](<link>). Invoke $wayfinder to advance it."
        in returned_flat
    )
    assert "Status: charted | advanced | maintained | waiting | blocked" in returned_flat
    assert "Domain Delta: <intact packet or not applicable>" in returned_flat


def test_grill_with_docs_package_and_relationship_contract() -> None:
    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(encoding="utf-8")
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert implicit_policy(CUSTOM / "grill-with-docs")
    assert {
        path.relative_to(CUSTOM / "grill-with-docs").as_posix()
        for path in (CUSTOM / "grill-with-docs").rglob("*")
        if path.is_file()
    } == {"SKILL.md", "agents/openai.yaml"}
    assert "$grilling" in grill_docs and "$domain-modeling" in grill_docs
    assert "$domain-modeling" not in grilling
    assert "$grilling" not in domain
    rows = re.findall(
        r"(?m)^\| `([a-z0-9-]+)` \| (Load|Invoke|Compose|Hand off|Recommend and stop) \| `\$([a-z0-9-]+)` \|",
        relationships,
    )
    assert {
        caller for caller, verb, callee in rows if verb == "Compose" and callee == "domain-modeling"
    } == {"grill-with-docs"}
    assert {
        caller
        for caller, verb, callee in rows
        if verb == "Recommend and stop" and callee == "grill-with-docs"
    } >= {"triage"}
    assert ("wayfinder", "Invoke", "grill-with-docs") in rows
    assert ("wayfinder", "Invoke", "grilling") in rows
    assert ("wayfinder", "Invoke", "to-questionnaire") in rows
    assert ("grilling", "Recommend and stop", "wayfinder") in rows
    assert ("grilling", "Recommend and stop", "to-spec") not in rows
    assert "Status: Confirmed | Evidence gap | Route gap | Blocked" in grill_docs
    assert "Route gap` preserves Grilling's uninvoked" in grill_docs
    for contract in (
        "each settled material answer to Domain Modeling",
        "every returned collision or blocker to Grilling",
        "never merge or reinterpret it",
        "Any material blocker in the current Domain Delta makes the "
        "combined status `Blocked`",
        "Composition blocker, owner, and re-entry condition",
        "preserves the originating blocker and owner",
    ):
        assert contract in " ".join(grill_docs.split())


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())

    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", domain) == [
        "Trace",
        "Challenge",
        "Resolve",
        "Return",
    ]
    assert "Trace -> Challenge -> Resolve -> (Persist -> Verify | Render) -> Return" in domain
    for target in ("CONTEXT-FORMAT.md", "ADR-FORMAT.md"):
        assert (CUSTOM / "domain-modeling" / target).is_file()
        assert f"({f'./{target}'})" in domain
    for contract in (
        "accept every settled material answer",
        "Return the authoritative cumulative Domain Delta and any collision before dependent questioning continues",
        "never choose interview materiality or branching",
        "Domain Delta",
    ):
        assert contract in domain_flat


def test_grilling_preserves_one_decision_confirmed_exit_and_evidence_routes() -> None:
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")
    grilling_plain = " ".join(grilling.replace("**", "").split())

    assert re.findall(r"(?m)^\*\*([A-Za-z ]+)\.\*\*", grilling) == [
        "Bound",
        "Grill",
        "Confirm",
        "Gap",
        "Return",
    ]
    for contract in (
        "Maintain the decision frontier",
        "highest-leverage decision",
        "Let blocked evidence pause only its dependent branches",
        "readiness as an exit test, never a question filter",
        "an owned nonblocking deferral whose answer cannot change the parent commitment",
        "only when no frontier decision can advance",
        "Relay every settled material answer",
        "pause dependent progress",
        "a repeated non-answer makes that decision authority unavailable",
        "Choose `$research` for an authoritative source",
        "recommend uninvoked `$wayfinder`",
        "original decision owner without changing the gap identity",
        "preserve that owner and add uninvoked `$handoff` only as transport",
        "Handoff neither answers nor owns the gap",
        "Transport: $handoff (uninvoked)",
        "required result, and exact re-entry instruction",
        "Spec source: ready | not ready | not requested",
        "Downstream execution: none",
    ):
        assert contract in grilling_plain
    assert "$to-spec" not in grilling


def test_prototype_preserves_lifecycle_boundaries_and_branch_gates() -> None:
    skill_dir = CUSTOM / "prototype"
    prototype = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    prototype_flat = " ".join(prototype.split())
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    logic_flat = " ".join(logic.split())
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    ui_flat = " ".join(ui.split())
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")
    measure_flat = " ".join(measure.split())

    for contract in (
        "Before mutation, read back:",
        "claim level: shape/feel | design evidence",
        "judgment mode: human | rule-based",
        "Decision owner and human judge are independent authorities",
        ".tmp/prototype/<question-slug>/",
        "Read only the decision-bearing branch",
        "[MEASURE.md](MEASURE.md)",
        "preserve-for-verdict",
        "authorized-durable-evidence",
        "No terminal return leaves a live resource",
        "Never carry caller identity from a preceding request or supplied result",
        "Do not select, recommend, or invoke a downstream route",
        "resolved by judgeable disposable evidence or returned with a truthful residual",
        "supported answer or residual, supported decision implications, evidence, limitations, and artifact dispositions",
    ):
        assert contract in prototype_flat

    for removed in (
        "[RESUME.md](RESUME.md)",
        "$handoff",
        "$domain-modeling",
        "status: answered | awaiting-verdict | blocked | not-admitted",
    ):
        assert removed not in prototype

    assert "happy, boundary, and rejected cases" in logic_flat
    assert "repeated runs are equivalent" in logic_flat
    assert "positively isolates the whole prototype surface" in ui_flat
    assert "actual browser or target UI" in ui_flat
    assert "variance and worst observed result" in measure_flat
    assert "does not diagnose an unexplained slowdown" in measure_flat
    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {
        "LOGIC.md",
        "MEASURE.md",
        "SKILL.md",
        "UI.md",
        "agents/openai.yaml",
    }


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    baseline = (CUSTOM / "change-review/SMELL-BASELINE.md").read_text(
        encoding="utf-8"
    )

    assert not (CUSTOM / "review").exists()
    assert not (CUSTOM / "convergent-pr-review").exists()
    assert re.search(r"(?m)^name: change-review$", review)
    assert re.search(r"(?m)^name: high-assurance-review$", convergent)
    assert "## Pin" in review
    assert "## 2. Pin" in convergent
    assert "$high-assurance-review" in review.split("---", 2)[1]
    assert "only when documented repo standards" in " ".join(baseline.split())
    assert "concrete, actionable maintainability risk" in baseline
    assert (
        "change-review/SMELL-BASELINE.md` only when Standards are thin"
        in " ".join(convergent.split())
    )
    review_steps = re.findall(r"(?m)^## (Pin|Cover|Judge|Gate)$", review)
    assert review_steps == ["Pin", "Cover", "Judge", "Gate"]
    convergent_steps = re.findall(r"(?m)^## \d+\. (.+)$", convergent)
    assert convergent_steps == [
        "Admit",
        "Pin",
        "Review",
        "Converge",
        "Gate",
    ]
    report = review.split("```text", 2)[2].split("```", 1)[0]
    assert report.lstrip().startswith("Review mode: initial | remediation")
    assert "Coverage: complete | incomplete" in report
    assert (
        "Decision: pass | pass with residual risk | blocked | incomplete"
        in report
    )
    assert "Standards findings:" in report
    assert "Spec findings:" in report


def test_review_finding_interface_and_return_boundary_are_shared() -> None:
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    finding = (CUSTOM / "change-review/FINDING-CONTRACT.md").read_text(
        encoding="utf-8"
    )

    fields = finding.split("```text", 1)[1].split("```", 1)[0]
    assert set(re.findall(r"(?m)^([A-Za-z ]+):", fields)) == {
        "ID",
        "Axis",
        "Class",
        "Severity",
        "Location",
        "Anchor",
        "Supported scenario",
        "Behavior or failure path",
        "Evidence",
        "Impact",
        "Supported risk trigger",
        "Blocking",
        "Remediation",
        "Required proof",
    }
    assert {
        "automatic-in-scope",
        "decision-required",
        "residual-hardening",
    } <= set(re.findall(r"(?m)^- `([^`]+)`(?:\:| )", finding))
    severity = finding.split("## Severity And Remediation", 1)[1]
    assert re.findall(r"(?m)^- `(P[0-3])`:", severity) == ["P0", "P1", "P2", "P3"]
    for skill in (review, convergent):
        assert "FINDING-CONTRACT.md" in skill
        assert not re.search(r"(?m)^- (?:\*\*)?`?P[0-3]", skill)
        assert "Return boundary: caller" in skill
        assert "Mutation authority: none" in skill
        assert "Successor snapshot authority: none" in skill
    assert "Test count or runtime alone does not admit a finding" in finding
    assert "distinct responsibility or justified failure isolation" in finding


def test_review_family_shares_one_bounded_quality_and_risk_model() -> None:
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    finding = (CUSTOM / "change-review/FINDING-CONTRACT.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    finding_flat = " ".join(finding.split())
    convergent_flat = " ".join(convergent.split())

    for class_name in (
        "Commitment Fidelity",
        "Scope and Contracts",
        "Acceptance and Change Closure",
        "Semantic Correctness",
        "Robustness and Operability",
        "Code Quality and Design",
        "Proof Discipline",
        "Stewardship",
    ):
        assert finding.count(f"**{class_name}**") == 1
    assert "Behavior is evidence used by both axes, not another axis." in finding_flat
    assert "Risk is a cross-cutting modifier." in finding_flat
    assert "Hypothetical permutations do not qualify." in finding_flat
    assert "not a blind Cartesian product" in review
    assert "not a blind Cartesian product" in convergent_flat
    assert "Reuse proof tied to the exact snapshot" in review
    assert "Reuse exact-snapshot proof" in convergent
    assert "ordinary local PRs" in review
    assert "PR existence, diff size, repository size" in convergent
    assert "ordinary PR needs read-only judgment" in router
    assert "supported high-risk diff or PR needs a terminal release decision" in router


def test_review_assurance_route_has_one_domain_decision() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    adr = (
        ROOT / "docs/adr/0011-review-assurance-follows-release-risk.md"
    ).read_text(encoding="utf-8")
    normalized_adr = " ".join(adr.split())

    for term in (
        "**Change review candidate**",
        "**High-assurance review candidate**",
        "**Supported high-risk trigger**",
    ):
        assert context.count(term) == 1
    assert "ADR-0011" in context
    assert "**Status**: accepted" in adr
    assert "PR existence" in normalized_adr
    assert "choose exactly one review route" in normalized_adr
    assert "Revision 3" in normalized_adr
    assert "Behavioral Proof" in normalized_adr


def test_high_assurance_review_uses_fresh_context_and_root_only_fanout() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert 'fork_turns="none"' in convergent
    contract = (
        convergent.split("this return contract:", 1)[1]
        .split("```text", 1)[1]
        .split("```", 1)[0]
    )
    assert set(re.findall(r"(?m)^([a-z ]+):", contract)) == {
        "status",
        "reviewer",
        "axis",
        "classes",
        "coverage",
        "candidates",
        "skipped checks",
        "blockers",
    }


def test_high_assurance_review_has_root_guard_bounded_capacity_and_risk() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    convergent_flat = " ".join(convergent.split())

    assert "Require the top-level root." in convergent
    assert "root-only blocker before Pin" in convergent
    for mode in ("initial", "remediation", "assurance"):
        assert f"- `{mode}`" in convergent
    for capacity in (
        "Two",
        "One",
        "Zero",
        "Any required class, evidence seam, or specialist lane remains uncovered",
    ):
        assert capacity in convergent
    assert "Maximum clean decision" in convergent
    assert convergent.count("`pass with residual risk`") >= 3
    assert "Repair authority" in convergent_flat
    assert "at most one specialist" in convergent
    assert "at most one unbiased replacement" in convergent
    assert not (CUSTOM / "change-review/ADVISORY-CONTRACT.md").exists()


def test_audit_codebase_is_thorough_incremental_html_atlas() -> None:
    skill_dir = CUSTOM / "audit-codebase"
    audit = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    defect = (skill_dir / "DEFECT-CONTRACT.md").read_text(encoding="utf-8")
    quality = (skill_dir / "QUALITY-LENS.md").read_text(encoding="utf-8")
    candidate = (skill_dir / "CANDIDATE-CONTRACT.md").read_text(encoding="utf-8")
    followup = (skill_dir / "CANDIDATE-FOLLOWUP.md").read_text(encoding="utf-8")
    reliability = (skill_dir / "RELIABILITY-LENS.md").read_text(encoding="utf-8")
    domain = (skill_dir / "DOMAIN-LENS.md").read_text(encoding="utf-8")
    design = (skill_dir / "DESIGN-LENS.md").read_text(encoding="utf-8")
    simplification = (skill_dir / "SIMPLIFICATION-LENS.md").read_text(
        encoding="utf-8"
    )
    practices = (skill_dir / "CODING-PRACTICES-LENS.md").read_text(
        encoding="utf-8"
    )
    performance = (skill_dir / "PERFORMANCE-LENS.md").read_text(encoding="utf-8")
    performance_lower = performance.lower()
    report = (skill_dir / "HTML-REPORT.md").read_text(encoding="utf-8")
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    audit_flat = " ".join(audit.split())
    quality_flat = " ".join(quality.split())
    report_flat = " ".join(report.split())
    map_section = audit.split("## Map", 1)[1].split("## Audit One Subsystem", 1)[0]
    audit_section = audit.split("## Audit One Subsystem", 1)[1].split(
        "## Analyze One Candidate", 1
    )[0]
    analyze_section = audit.split("## Analyze One Candidate", 1)[1]

    assert not implicit_policy(skill_dir)
    assert "**Root-owned:**" in audit
    assert 'fork_turns="none"' in audit
    assert "up to six" in audit
    assert "one user objective per invocation" in audit
    assert "prerequisite source refresh in the same invocation" in audit_flat
    assert "Release decision: none" in audit
    assert "a complete audit may contain severe defects" in " ".join(
        audit.lower().split()
    )
    assert "[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md)" in audit
    assert "[QUALITY-LENS.md](QUALITY-LENS.md)" in audit
    assert "[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md)" in audit
    for reference in (
        "RELIABILITY-LENS.md",
        "DOMAIN-LENS.md",
        "DESIGN-LENS.md",
        "SIMPLIFICATION-LENS.md",
        "CODING-PRACTICES-LENS.md",
    ):
        assert f"[{reference}]({reference})" in audit
    assert "[PERFORMANCE-LENS.md](PERFORMANCE-LENS.md)" in audit
    assert "[HTML-REPORT.md](HTML-REPORT.md)" in audit
    assert "RELIABILITY-LENS.md" not in map_section
    assert "CANDIDATE-CONTRACT.md" in analyze_section
    assert all(
        reference in audit_section
        for reference in (
            "RELIABILITY-LENS.md",
            "DOMAIN-LENS.md",
            "DESIGN-LENS.md",
            "SIMPLIFICATION-LENS.md",
            "CODING-PRACTICES-LENS.md",
        )
    )
    assert "ADVISORY-CONTRACT.md" not in audit
    assert ".scratch/audit-codebase/<run-id>/report.html" in audit
    assert "durable repository atlas" in report_flat
    assert "atlas.json" not in audit
    assert "atlas.json" not in report
    assert "FINDING-CONTRACT.md" not in audit
    assert re.findall(
        r"(?m)^## (Map|Audit One Subsystem|Analyze One Candidate)$", audit
    ) == [
        "Map",
        "Audit One Subsystem",
        "Analyze One Candidate",
    ]
    assert "## Reconcile" not in audit
    assert "Map:     observe current repository -> map remaining ownership -> publish" in audit
    assert "Use one branch:" in audit
    for branch in ("**New:**", "**Continue:**", "**Refresh:**"):
        assert branch in audit
    assert "Map: none | incomplete | complete" in audit
    assert "Subsystem: none | mapped | incomplete | audited" in audit
    assert (
        "Candidate: none | presented | decision pending | analyzed | disproved | blocked"
        in audit
    )
    assert "shared infrastructure with one audit-owning subsystem" in audit
    assert "Do not audit or rank a subsystem during Map" in " ".join(audit.split())
    assert "never selects a subsystem or candidate" in " ".join(audit.split())
    assert "next selection authority: user" in audit.lower()
    assert "offline and script-free" not in audit
    assert "## Burden Of Proof" in defect
    assert "Severity orders defects" in defect
    assert "## Suggest One Owner" not in defect
    for severity in ("P0", "P1", "P2", "P3"):
        assert f"**{severity}:**" in defect
    assert "downstream execution: none" in audit.lower()
    assert "$audit-codebase analyze <candidate-id>" in audit
    assert "load `$codebase-design` Direct Design as a discipline" in " ".join(
        audit.split()
    )
    assert "Create no second design artifact" in audit
    assert "decision pending" in audit
    assert "Never replace an invalid or ambiguous Audit or Analyze" in " ".join(
        audit.split()
    )
    assert "Never substitute checkout bytes for a supplied Git object." in audit
    assert "Snapshot: none | current | stale" not in audit
    assert "complete logical manifest" not in audit
    assert "Do not render a per-file hash ledger" in audit
    for route in (
        "$research",
        "$prototype",
        "$domain-modeling",
        "$grill-with-docs",
        "$grilling",
        "$diagnosing-bugs",
        "$to-questionnaire",
        "$to-spec",
        "$to-tickets",
        "$implement",
        "$simplify-code",
        "$wayfinder",
    ):
        assert route in followup
        assert route not in candidate
    assert "$codebase-design" in candidate
    assert (
        "Material Responsibilities, Interfaces, Seams, and Proof Seams:"
        in candidate
    )
    assert (
        "material Responsibilities, Interfaces, Seams, and Proof Seams"
        in report_flat
    )
    assert "$tdd" not in defect
    assert "Suggested invocation:" in followup
    assert "candidate ID" in followup
    assert "absolute report path" in followup
    assert "Result recipient:" in followup
    assert "Audit re-entry:" in followup
    assert "gap-only hypotheses" in " ".join(candidate.lower().split())
    assert "declared:<lens-id>" in candidate
    assert "`Questionnaire ready` is not answer evidence" in followup
    assert "unchanged exhausted or blocked return" in followup
    assert "Multiple interdependent unresolved decisions or prerequisites" in followup
    assert "## Mandatory Lens Gate" in quality
    for disposition in (
        "finding",
        "retained complexity",
        "gap",
        "examined-no-finding",
        "not applicable",
    ):
        assert disposition in quality
    assert "`not applicable` requires source evidence" in quality
    for lens in (
        "Reliability",
        "Domain",
        "Design",
        "Simplification",
        "Coding practice",
        "Performance",
    ):
        assert f"| {lens} |" in quality
    assert "A missing disposition keeps the subsystem `incomplete`" in quality_flat
    assert "Always read:" in audit_section
    assert "Load a detailed owner when" in audit_section
    assert "A class is never skipped silently." in " ".join(audit_section.split())
    assert "Unrelated repository changes do not block." in analyze_section
    assert "repeat its admission gate before changing the candidate" in (
        " ".join(analyze_section.split())
    )
    for question in ("Necessary", "Available", "Owned", "Deep", "Clear", "Provable", "Faithful"):
        assert f"**{question}:**" in quality
    for gate in ("Reach", "Evidence", "Cost", "Alternative", "Proof"):
        assert f"**{gate}:**" in quality
    assert "Do not estimate lines or dependencies saved" in quality
    assert "## Stale Code" in quality
    assert "## Retain" in quality
    for state in (
        "presented",
        "decision pending",
        "analyzed",
        "disproved",
        "blocked",
    ):
        assert state in audit
    for strength in ("Strong", "Worth exploring", "Speculative"):
        assert strength in candidate
    assert "The card is a lead, not current proof." in candidate
    for validity in ("confirmed", "changed", "disproved", "blocked"):
        assert validity in candidate
    assert "Current shape and demonstrated cost:" in candidate
    assert "Smallest sufficient change:" in candidate
    assert "Structural change:" in candidate
    assert "Replacement:" in candidate
    assert "Recommended direction:" in candidate
    assert "Rejected alternatives and why:" in candidate
    assert "Affected contracts and decisions:" in candidate
    assert "Compatibility, migration, cutover, and rollback:" in candidate
    assert "Proof plan:" in candidate
    assert "Residual risk:" in candidate
    assert "`not applicable` needs evidence" in candidate
    assert "CANDIDATE-FOLLOWUP.md" in candidate
    assert "Without one of those conditions" in candidate
    assert "Domain Delta" in followup
    assert "# Improvement Candidate Contract" in candidate
    assert "Improvement direction:" in candidate
    for concept in (
        "Semantic Correctness",
        "Robustness",
        "Root Cause",
        "Trust Boundary",
        "Failure Atomicity",
        "State Lifecycle",
        "Observability",
    ):
        assert concept in reliability
    assert "Proof Seam alone does not earn an Adapter" in reliability
    assert "Causal owner and affected callers:" in defect
    for concept in (
        "Ubiquitous Language",
        "Bounded Context",
        "Context Relationship",
        "Language Collision",
        "ADR Conflict",
    ):
        assert concept in domain
    for concept in (
        "Module",
        "Interface",
        "Depth",
        "Seam",
        "Adapter",
        "Leverage",
        "Locality",
        "Deletion Test",
    ):
        assert concept in design
    for concept in (
        "YAGNI",
        "KISS",
        "DRY",
        "Readability First",
        "Repository Reuse",
        "Standard Library",
        "Native Platform",
        "Installed Dependency",
        "Collapse",
        "Known Ceiling",
    ):
        assert concept in simplification
    assert "Surgical Change" not in simplification
    assert "Surgical Change" in candidate
    assert "Goal-Driven Execution" in candidate
    for concept in (
        "Descriptive Naming",
        "Type Safety",
        "Immutability Default",
        "Explicit Error Handling",
        "Input Validation",
        "Clear Control Flow",
        "Why Comments",
        "Behavior Tests",
        "Behavior-Owned Test Portfolio",
    ):
        assert concept in practices
    assert "**Like-for-like:**" in performance
    assert "smell alone" in performance
    for field in ("Workload:", "Environment:", "Baseline:", "Observed:", "Sample count and variance:"):
        assert field in performance
    assert "performance defect" in performance_lower
    assert "performance opportunity" in performance_lower
    assert "performance evidence gap" in performance_lower
    assert "a comparison baseline counts only when authority defines pass/fail" in " ".join(
        performance_lower.split()
    )
    assert "advisory" not in defect.lower()
    assert "advisory" not in performance_lower
    assert "advisories" not in report.lower()
    assert "offline" in report
    assert "executable scripts" in report
    assert "## Portable Template" in report
    assert "## Entry Gate" in report
    assert "## Provenance And Freshness" in report
    assert "Do not validate every unrelated count" in report
    assert "Do not render a per-file hash ledger" in report
    assert "Older sections are historical evidence" in report
    assert "Never encode state by color alone" in report
    assert "a `viewBox`" in report
    assert "## Linked System Map" in report
    assert "one repository relationship figure" in report
    assert "every unique direct evidence-backed dependency exactly once" in report_flat
    assert "reverse caller or dependent duplicates" in report
    assert "one current-state context-flow figure" in report
    assert "Never render a proposed candidate shape" in report_flat
    assert "perform no separate diagram analysis" in audit_flat
    assert "create no graph ledger or layout-engine dependency" in audit_flat
    assert "## Subsystem Audit" in report
    assert "## Candidate Card And Analysis" in report
    assert "## Stable Update Markers" in report
    assert "## Map Publish Gate" in report
    assert "## Incremental Publish Gate" in report
    assert "scripts/update_report.py" in report
    assert "attempt incremental publication exactly once" in report
    assert "Do not rerun the helper" in report
    assert "hand-edit the report" in report
    assert "use another publication mechanism" in report
    assert "delay the Return" in report
    assert "one-attempt Incremental Publish Gate" in audit_flat
    assert (skill_dir / "scripts/update_report.py").is_file()
    assert "atomically replace" in report
    assert "changed-fragment links" in report
    assert "report SHA-256 is unchanged" in report
    assert "return completed source analysis" in report.lower()
    assert 'content="2"' in report
    assert '<html lang="en">' in report
    assert '<section id="system-<system-id>">' in report
    assert '<section id="subsystem-<subsystem-id>">' in report
    assert "candidate links inside their subsystem" in report_flat
    assert "Never rank subsystems or add a global recommendation" in report_flat
    assert "subsystem-local recommendation" in report_flat
    assert "Snapshot status: current | stale" not in report
    assert "An identity mismatch permits only one atomic status update" not in report
    assert re.search(
        r"(?m)^\| A repository needs a whole-system map, one selected subsystem "
        r"audit, or one selected audit-candidate analysis \| `\$audit-codebase` \|$",
        router,
    )


def test_high_assurance_review_returns_a_lock_usable_decision() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    decision_section = convergent.split("Derive exactly one decision", 1)[1].split(
        "Return one caller-bound packet", 1
    )[0]
    decisions = set(
        re.findall(
            r"(?m)^- `(pass|pass with residual risk|blocked|incomplete)`",
            decision_section,
        )
    )
    assert decisions == {"pass", "pass with residual risk", "blocked", "incomplete"}
    ledger_sentence = convergent.split("and one state:", 1)[1].split(".", 1)[0]
    ledger_states = set(re.findall(r"`([^`]+)`", ledger_sentence))
    assert ledger_states == {"candidate", "accepted", "rejected", "duplicate", "disputed"}


def test_high_assurance_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    verify = convergent.split("## 5. Gate", 1)[1]
    verify = " ".join(verify.split())
    for surface in (
        "`HEAD`",
        "index tree",
        "staged diff",
        "unstaged diff",
        "status",
        "untracked path and its bytes",
    ):
        assert surface in verify


def test_implement_selects_one_risk_scaled_review_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_section = implement.split("## Review", 1)[1].split(
        "## Lock And Return", 1
    )[0]
    review_flat = " ".join(review_section.split())
    assert "Stage only selected work" in review_flat
    assert "Pin routing classification and Finding Contract" in review_flat
    assert "then choose exactly one formal review route for the run" in review_flat
    assert "Invoke it once for the initial proved candidate" in review_flat
    assert "invoke the same route once in remediation mode" in review_flat
    assert "request an explicitly staged-only review" in review_flat
    assert "Never unstage foreign work" in review_flat
    assert "Return without Review" in review_flat
    assert set(
        re.findall(r"`\$(change-review|high-assurance-review)`", review_section)
    ) == {
        "change-review",
        "high-assurance-review",
    }
    assert "ordinary diff or PR" in review_flat
    assert "release candidate or supported high-risk diff or PR" in review_flat
    assert "supported risk trigger when applicable" in review_flat
    assert "already-loaded Finding Contract" in review_flat
    assert "complete caller-admitted" in review_flat
    assert "mixed-authority, partial, out-of-scope, or" in review_flat


def test_audit_codebase_replaces_improve_codebase() -> None:
    audit = (CUSTOM / "audit-codebase/SKILL.md").read_text(encoding="utf-8")
    quality = (CUSTOM / "audit-codebase/QUALITY-LENS.md").read_text(encoding="utf-8")
    design = (CUSTOM / "audit-codebase/DESIGN-LENS.md").read_text(encoding="utf-8")
    simplification = (
        CUSTOM / "audit-codebase/SIMPLIFICATION-LENS.md"
    ).read_text(encoding="utf-8")
    candidate = (CUSTOM / "audit-codebase/CANDIDATE-CONTRACT.md").read_text(
        encoding="utf-8"
    )

    assert not (CUSTOM / "improve-codebase/SKILL.md").exists()
    assert "stale code" in quality.lower()
    assert "complexity" in audit.lower()
    assert "Deep Module" in design
    assert "deepens" in candidate
    assert "Collapse" in simplification
    assert "retain" in quality
    assert "Top recommendation" in candidate or "Recommendation strength" in candidate
    assert "decision pending" in candidate


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")

    assert "Use directly for one bounded red-testable behavior" in tdd
    assert "inner loop of an implementation owner" in tdd
    assert "Exclude whole-ticket delivery and closeout" in tdd
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
    assert "existing Behavior Test, case table, or contract suite" in tdd
    assert "Add a test only when the tracer has a distinct proof" in tdd
    assert "## Behavior-Owned Test Portfolio" in tests
    assert "Test count is not a target" in tests


def test_tdd_routes_improvement_followups_by_scope() -> None:
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")
    refactoring_flat = " ".join(refactoring.split())

    assert "$simplify-code" in refactoring
    assert "$codebase-design" not in refactoring
    assert (
        "Return an already-framed Interface or Seam question to the caller as "
        "a design gap"
    ) in refactoring_flat
    assert "$audit-codebase" in refactoring


def test_simplify_code_is_explicit_bounded_and_behavior_preserving() -> None:
    skill_dir = CUSTOM / "simplify-code"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    bound = skill.split("## Bound", 1)[1].split("## Baseline", 1)[0]
    bound_flat = " ".join(bound.split())
    baseline = skill.split("## Baseline", 1)[1].split("## Reduce", 1)[0]
    reduce = skill.split("## Reduce", 1)[1].split("## Prove", 1)[0]
    reduce_flat = " ".join(reduce.split())
    returned = skill.split("## Return", 1)[1]
    returned_flat = " ".join(returned.split())

    assert not implicit_policy(skill_dir)
    assert "one explicitly selected existing-code target" in skill
    assert "**Bound -> Baseline -> Reduce -> Prove -> Return.**" in skill
    assert "Return exactly one outcome" in skill
    for outcome in ("`simplified`", "`no-safe-simplification`", "`blocked`"):
        assert outcome in returned
    assert "The user may name the current diff as that target" in bound
    assert "never infer or replace the target" in bound_flat.lower()
    assert "one coherent current diff" not in skill
    assert "Without a target, return `blocked`" in bound_flat
    assert "exact `$audit-codebase` candidate selected by the user" in bound
    assert "reuse its trace and selected direction" in bound_flat
    assert "In default mode, do not repeat wide tracing" in bound_flat
    assert "An `until-clean` request names its region" in bound_flat
    assert "smallest trusted proof" in skill
    assert "semantically inadequate baseline returns `blocked`" in " ".join(
        baseline.split()
    )
    assert "adequate baseline is required for a `no-safe-simplification`" in " ".join(
        baseline.split()
    )
    assert "before and after proof" in returned_flat
    assert "Refresh changed paths and work state after proof" in skill
    assert "evidence proves no use remains" in skill
    assert "staged-state shape" in skill
    assert "keeps the index and unrelated state as found" in skill_flat
    assert "verified `$audit-codebase` atlas" not in skill
    assert "configuration, compatibility, or abstraction proved" in reduce
    assert "deepen, merge, or inline only within settled existing boundaries" in (
        reduce_flat
    )
    assert "Known Ceiling" in reduce_flat
    assert "Revisit Trigger" in reduce_flat
    assert "complete applicable inspection" in reduce
    assert "selected Audit direction in default mode or the" in reduce_flat
    assert "full ladder for other targets and `until-clean`" in reduce_flat
    assert "Enter only when the user explicitly requests `until-clean`" in skill
    assert re.findall(r"(?m)^\d\. \*\*([^*]+)\*\*", reduce)[:5] == [
        "Delete",
        "Reuse",
        "Standardize, native-first",
        "Collapse",
        "Shrink",
    ]

    standardize = skill.split("3. **Standardize, native-first**", 1)[1].split(
        "4. **Collapse**", 1
    )[0]
    assert standardize.index("standard/runtime") < standardize.index(
        "platform/framework"
    )
    assert standardize.index("platform/framework") < standardize.index(
        "already-installed dependency"
    )


def test_simplify_code_until_clean_has_a_finite_convergence_contract() -> None:
    skill = (CUSTOM / "simplify-code/SKILL.md").read_text(encoding="utf-8")
    branch = skill.split("## Until Clean", 1)[1].split("## Return", 1)[0]
    branch_flat = " ".join(branch.split())

    assert "names one region" in branch
    assert "finite positive successful-cut budget" in branch
    assert "Hold one invariant behavior contract and Proof Seam" in branch_flat
    assert "use exactly `3` successful cuts when omitted" in branch_flat
    assert "`Baseline -> Reduce -> Prove`" in branch
    assert "strict monotonic reduction" in branch_flat
    assert "complete five-rung inspection" in branch_flat
    assert "presentation-only changes as progress" in branch_flat
    assert "A failed attempt consumes no successful-cut budget" in branch_flat
    assert "Do not widen or parallelize the region, renew the budget" in branch_flat
    assert re.findall(r"(?m)^\d\. \*\*([^*]+):\*\*", branch) == [
        "Clean",
        "Budget exhausted",
        "Diminishing return",
        "Oscillation",
        "Failed cut",
        "Boundary stop",
    ]

    returned = skill.split("## Return", 1)[1]
    returned_flat = " ".join(returned.split())
    assert "initial budget, successful-cut ledger, remaining budget" in returned_flat
    assert "with no cut and a `Clean` terminal returns" in returned_flat
    assert "failed or boundary stop returns `blocked`" in returned_flat


def test_codebase_design_compares_replacement_with_incremental_evolution() -> None:
    direct = (CUSTOM / "codebase-design/DIRECT-DESIGN.md").read_text(encoding="utf-8")

    assert "deepen, merge, inline, retain, replace" in direct
    assert "compare it explicitly with incremental evolution" in direct
    for gate in ("parity", "migration", "cutover", "rollback"):
        assert gate in direct


def test_bug_routing_is_disjoint_and_non_bouncing() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    diagnosing_flat = " ".join(diagnosing.split())
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tdd_flat = " ".join(tdd.split())
    tdd_tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")

    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^## \d+\. ([A-Za-z]+)$", diagnosing)
    ] == ["Trace", "Loop", "Minimise", "Hypothesise", "Probe", "Prove", "Return"]
    assert "[SKILL.md](SKILL.md)" in tdd_tests
    assert "Hand off to `$diagnosing-bugs`" in tdd
    assert "expected behavior" in diagnosing.split("---", 2)[1]
    assert "expected behavior" in tdd.split("---", 2)[1]
    assert "observed failing result" in tdd
    assert "canonical test owner" in diagnosing_flat
    assert (
        "distinct proof responsibility or necessary failure isolation" in diagnosing_flat
    )
    assert "test-portfolio delta" in diagnosing_flat
    assert "applicable Change Closure" in diagnosing_flat
    assert "explicit seam gap" in tdd_flat


def test_workflow_trace_matches_to_spec_publication_authority() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "to-spec")
    assert re.findall(r"(?m)^### \d+\. (.+)$", to_spec) == [
        "Setup",
        "Trace settled source and state",
        "Draft and cover",
        "Publish, verify, and reconcile",
    ]
    normalized = " ".join(to_spec.split())
    assert "For exact matching state, reuse the verified parent" in normalized
    assert "delegate exactly one create operation" in normalized
    assert "compare it with the frozen draft" in normalized
    assert "recommend `$to-tickets` only after verified success" in normalized
    for gap_kind in (
        "user-decision",
        "domain-decision",
        "source-evidence",
        "runnable-evidence",
        "stakeholder-evidence",
        "multi-decision-fog",
    ):
        assert gap_kind in normalized
    assert "exact return owner" in normalized
    assert "do not invoke or recommend a resolver" in normalized.lower()


def test_to_spec_handoff_keeps_ticket_design_downstream() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    to_tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    spec = " ".join(to_spec.split())
    tickets = " ".join(to_tickets.split())
    spec_lower = spec.lower()
    tickets_lower = tickets.lower()

    for owned_concept in (
        "purpose",
        "boundaries",
        "limitations",
        "decisions and their owners",
        "required behavioral",
        "acceptance objectives",
        "Source Trace",
        "Removal Trigger",
    ):
        assert owned_concept.lower() in spec_lower
    for downstream_concept in (
        "bounded repository grounding",
        "ticket slices",
        "expected writes",
        "concrete proof lanes",
        "dependency graph and ready frontier",
        "execution profiles",
        "parallel-safety decisions",
        "implementation technique",
        "default Repair budgets",
    ):
        assert downstream_concept.lower() in spec_lower
    for ticket_owner in (
        "inspect enough code to ground",
        "ticket boundaries",
        "expected durable writes",
        "dependency order",
        "ready frontier",
        "execution profiles",
        "parallel-safety judgment",
    ):
        assert ticket_owner.lower() in tickets_lower
    assert "Paths are evidence, not an implementation plan." in spec
    assert "## Code Quality Contract" not in to_spec
    assert "`ready-spec`" in spec
    assert "`published-spec`" not in spec


def test_implementation_closeout_requires_the_spec_axis() -> None:
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (review, convergent):
        assert "`Spec required: yes | no`" in text
    assert "Supply `Spec required: yes`; the required Spec" in " ".join(
        implement.split()
    )
    assert "`Spec required: yes`" in " ".join(parallel.split())


def test_implementation_workflows_compress_steps_without_repeating_proof() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    integrator = (
        CUSTOM / "parallel-implement/references/INTEGRATOR-BRIEF.md"
    ).read_text(encoding="utf-8")
    implement_synthesis = (
        ROOT / "docs/synthesis/skills/implement.md"
    ).read_text(encoding="utf-8")
    parallel_synthesis = (
        ROOT / "docs/synthesis/skills/parallel-implement.md"
    ).read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())
    parallel_flat = " ".join(parallel.split())
    integrator_flat = " ".join(integrator.split())

    assert re.findall(r"(?m)^## (.+)$", implement) == [
        "Admit",
        "Execute",
        "Review",
        "Lock And Return",
    ]
    assert re.findall(r"(?m)^## (.+)$", parallel) == [
        "Admit",
        "Run",
        "Review",
        "Lock And Return",
    ]
    assert "tracker and label owners only for tracker-backed work" in implement_flat
    assert "Reuse settled packet facts" in implement_flat
    assert "exact candidate and proof inputs remain unchanged" in implement_flat
    assert "rerun only invalidated or repository-required proof" in implement_flat
    assert "Start from the frozen graph and execution profiles" in parallel_flat
    assert "Requalify only" in parallel_flat
    assert "Carry worker proof as slice evidence" in parallel_flat
    assert "only interaction or readiness proof" in parallel_flat
    assert "final required proof once on the drained current `HEAD`" in parallel_flat
    assert "only invalidated interaction or readiness proof" in integrator_flat
    assert "final required validation belongs to the review-ready handoff" in (
        integrator_flat
    )
    assert "run touched-area proof" not in integrator_flat
    assert "canonical test owner" in implement_flat
    assert "proof-responsibility map" in parallel_flat
    assert "consolidate semantically equivalent campaign-created tests" in parallel_flat
    for synthesis in (implement_synthesis, parallel_synthesis):
        synthesis_flat = " ".join(synthesis.replace("> ", "").split())
        assert "historical evidence for the exact pre-efficiency bytes" in synthesis_flat
        assert "Prior hashes and evaluations below do not prove current wording" in (
            synthesis_flat
        )
        assert "No installed sync is claimed" in synthesis_flat


def test_planning_and_delivery_activate_preventive_code_quality_contract() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    to_tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(
        encoding="utf-8"
    )
    worker = (
        CUSTOM / "parallel-implement/references/WORKER-BRIEF.md"
    ).read_text(encoding="utf-8")
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

    normalized = {
        name: " ".join(text.split())
        for name, text in {
            "to-spec": to_spec,
            "to-tickets": to_tickets,
            "implement": implement,
            "review": review,
            "parallel": parallel,
            "worker": worker,
            "convergent": convergent,
        }.items()
    }

    assert "implementation-adjacent source claims" in normalized["to-spec"]
    assert "Removal Trigger" in normalized["to-spec"]
    assert "Repository Reuse" in normalized["to-tickets"]
    assert "Change Closure" in normalized["to-tickets"]
    assert "Removal Trigger" in normalized["to-tickets"]
    assert "Code Quality Contract" in normalized["implement"]
    assert "Change Closure" in normalized["implement"]
    assert "Removal Trigger" in normalized["implement"]
    assert "`Spec required: yes`" in normalized["implement"]
    assert "engineering-contract.md" in normalized["review"]
    assert "Change Closure" in normalized["review"]
    assert "displaced" in normalized["review"]
    assert "**Must**" in normalized["review"]
    assert "**Prefer**" in normalized["review"]
    assert "Change Closure" in normalized["parallel"]
    assert "Change Closure" in normalized["worker"]
    assert "Change Closure" in normalized["convergent"]
    assert "ToSpec --> Contract" in relationships
    assert "ToTickets --> Contract" in relationships
    contract_owner = next(
        line
        for line in relationships.splitlines()
        if line.startswith("| `docs/agents/engineering-contract.md` |")
    )
    assert "`to-spec`" in contract_owner


def test_ticket_and_delivery_packets_preserve_quality_and_route_repairs() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(
        encoding="utf-8"
    )
    worker = (
        CUSTOM / "parallel-implement/references/WORKER-BRIEF.md"
    ).read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    tickets_flat = " ".join(tickets.split())
    implement_flat = " ".join(implement.split())
    parallel_flat = " ".join(parallel.split())
    worker_flat = " ".join(worker.split())

    for field in (
        "**Intent:**",
        "**Grounding:**",
        "**Correctness:**",
        "**Scope and proof:**",
        "**Delivery:**",
        "**Closure:**",
    ):
        assert field in tickets
    assert "Treat paths as evidence, not ticket boundaries or implementation" in (
        tickets_flat
    )
    assert "non-goal, which is outside delivery scope" in tickets_flat
    assert "prohibited behavior, which requires an acceptance or proof obligation" in (
        tickets_flat
    )
    assert "default exactly to `2`" in tickets_flat
    assert "Never infer a higher budget from ticket size or risk" in tickets_flat
    assert "5,500 characters as a soft target" in tickets_flat
    assert "Separate packet readiness from frontier eligibility" in tickets_flat
    assert "Mixed graphs may contain both states" in tickets_flat
    assert "only the human frontier is non-empty" in tickets_flat
    assert "Dependency edges and tracker order remain graph facts" in tickets_flat
    assert "proof-responsibility map" in tickets_flat
    assert "one canonical responsibility" in tickets_flat
    assert "adding a test requires a distinct responsibility" in tickets_flat
    assert "create no second planning artifact" in tickets_flat

    assert "Preserve the complete source-owned packet" in implement_flat
    assert "Add only the runtime fixed point and confirmed authorized writes" in (
        implement_flat
    )
    assert "default the selected-item budget to exactly `2`" in implement_flat
    assert "Refresh only a stale, uncertain, or contradicted seam" in implement_flat
    assert "Recommend `$to-tickets` only when a verified landed predecessor" in (
        implement_flat
    )
    assert "malformed item to its caller, source, or triage owner" in implement_flat
    assert "canonical proof responsibility" in implement_flat
    assert "surviving portfolio preserves each distinct responsibility" in (
        implement_flat
    )

    assert "Tickets execution packet and profile" in parallel_flat
    assert "Resolve authority prerequisites before a ticket becomes dispatchable" in (
        parallel_flat
    )
    assert "campaign Repair-generation budget to exactly `2`" in parallel_flat
    assert "same-campaign landing or verified external implementation invalidates" in (
        parallel_flat
    )
    assert "proof-responsibility map" in parallel_flat
    assert "test-portfolio delta" in parallel_flat
    for field in (
        "Applicable engineering and domain pointers",
        "Grounding: current owner",
        "Commitment Boundary, prohibited behavior",
        "Applicable Invariants, Trust Boundaries",
        "Confirmed authority boundary",
        "Proof responsibility:",
        "routed Code Quality Contract",
        "return it as `needs-feedback`",
    ):
        assert field in worker_flat
    assert "Ordinary malformed or unsettled source returns to its caller" in (
        relationships
    )
    assert "Ordinary blockers, regressions, conflicts, and review findings remain" in (
        relationships
    )


def test_interface_alternatives_receive_curated_fresh_context() -> None:
    design = (CUSTOM / "codebase-design/DESIGN-IT-TWICE.md").read_text(
        encoding="utf-8"
    )
    research = (CUSTOM / "research/SKILL.md").read_text(encoding="utf-8")
    audit = (CUSTOM / "audit-codebase/SKILL.md").read_text(encoding="utf-8")

    assert 'fork_turns="none"' in design
    assert 'fork_turns="none"' not in research
    assert 'fork_turns="none"' in audit
    assert "read-only delegates" in audit
    assert "root repeats decisive checks" in " ".join(audit.split())


def test_research_owns_one_authorized_cited_note() -> None:
    skill_dir = CUSTOM / "research"
    research = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert implicit_policy(skill_dir)
    assert re.findall(r"(?m)^## (.+)$", research) == [
        "Admission And Lock",
        "Evidence",
        "Output",
        "Verify And Return",
    ]
    assert {"`supported`", "`conflicted`", "`unknown`"} <= set(
        re.findall(r"`[^`]+`", research)
    )
    for status in ("answered", "conflicted", "blocked", "not-admitted"):
        assert f"`{status}`" in research
    assert "create or update only that Markdown file" in research
    assert re.search(r"make no\s+tracked mutation", research)
    for contract in (
        "Treat a source as authoritative only for the claim it owns",
        "not comparative superiority or real-world reliability",
        "opinion and case reports own the viewpoint or observed case",
        "Challenge the strongest plausible answer",
        "another credible applicable search lane is unlikely to change the answer",
        "require applicable independent evidence",
    ):
        assert contract in " ".join(research.split())
    assert research.index("## Output") < research.index("## Verify And Return")
    assert "Return to the caller without deciding its artifact" in research
    assert "starting downstream work" in research


def test_writing_great_skills_keeps_shape_and_relationship_boundary() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    glossary = (skill_dir / "GLOSSARY.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    normalized_skill = " ".join(skill.split())
    normalized_glossary = " ".join(glossary.split())

    assert implicit_policy(skill_dir)
    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {
        "BEHAVIOR-EVALS.md",
        "GLOSSARY.md",
        "SKILL.md",
        "agents/openai.yaml",
    }
    assert set(re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", skill)) == {
        "BEHAVIOR-EVALS.md",
        "GLOSSARY.md",
    }
    assert all((skill_dir / target).is_file() for target in (
        "BEHAVIOR-EVALS.md",
        "GLOSSARY.md",
    ))
    assert "Make canonical skill behavior predictable" in normalized_skill
    assert "## Behavior Shape" in skill
    assert (
        "Each gate names its condition, passing evidence, and safe failure action"
        in normalized_skill
    )
    for contract in (
        "narrowest shared owner",
        "one materially different applicable case",
        "closest non-applicable case",
        "every term that changes admission, branching, ordering, pass/fail, or completion",
        "counting scope and invalidation condition",
        "derived view as a projection of its owning facts",
        "Prune removal test to every proposed step, required field, artifact, view, or check",
        "transition that could invalidate it",
        "directly checkable invariants before the judgment or action they protect",
        "failed gate to the smallest dependent action or output",
        "each independent supported result",
        "its own weakest load-bearing evidence",
        "exact claim, candidate state, and invalidation boundary",
        "does not establish unobserved live behavior",
    ):
        assert contract in normalized_skill
    assert "## Prune" in skill
    assert all(term in skill for term in (
        "`Keep`",
        "`Collapse`",
        "`Disclose`",
        "`Delete`",
    ))
    assert all(term in glossary for term in (
        "**Predictable behavior**",
        "**Leading word**",
        "**Gate**",
        "**Completion criterion**",
    ))
    assert (
        "sharpen the pointer's target and loading condition first"
        in normalized_glossary
    )
    assert "only if the sharpened pointer still fails" in normalized_glossary
    assert "fork_turns" not in skill
    assert (
        "bundled system `skill-creator` owns new-package scaffolding and metadata mechanics"
        in relationships
    )
    assert "$writing-great-skills` owns semantic quality" in relationships


def test_merge_conflict_resolution_is_three_way_and_finish_bounded() -> None:
    skill_dir = CUSTOM / "resolving-merge-conflicts"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    operations = (skill_dir / "OPERATIONS.md").read_text(encoding="utf-8")

    assert implicit_policy(skill_dir)
    read_only = re.search(r"\*\*Read-only: (.+?)\.\*\*", skill_flat)
    reconcile = re.search(r"\*\*Reconcile: (.+?)\.\*\*", skill_flat)
    assert read_only is not None and reconcile is not None
    assert "Reconcile" not in read_only.group(1)
    assert "Finish" not in read_only.group(1)
    assert reconcile.group(1).index("Prove") < reconcile.group(1).index("Return")
    assert "only with finish authority" in reconcile.group(1)
    assert "`git ls-files -u`" in skill
    assert "[OPERATIONS.md](OPERATIONS.md)" in skill
    assert "## Operation Roles" in operations
    assert "## Conflict Classes" in operations
    assert "## Finish Checks" in operations
    assert "prepared reconciliation" in skill
    assert "finished operation" in skill
    assert "Never use `git add -A`" in skill
    assert "Rebase" in operations and "commit being replayed" in operations
    assert "## Guardrails" in skill
    assert "## Return" in skill


def test_portable_fallback_carries_the_standalone_engineering_contract() -> None:
    loop = "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock"
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    fallback_flat = " ".join(fallback.split())
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
        "Code Quality Contract",
        "Tight Engineering Spine",
        "Proof Discipline",
        "Work State",
        "Lock",
    ]
    north_star = fallback.split("## North Star", 1)[1].split("## Engineering Taste", 1)[0]
    vocabulary = set(re.findall(r"(?m)^- \*\*([^*]+):\*\*", north_star))
    assert vocabulary >= {
        "Source trace",
        "Bounded slice",
        "Commitment boundary",
        "Operational acceptance",
        "Behavior-owned test portfolio",
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
    hard_gates_flat = " ".join(hard_gates.split())
    for mutation in ("filesystem", "Git", "tracker", "deployment", "external"):
        assert mutation in hard_gates
    assert "**Change closure / Stewardship:**" in hard_gates
    assert "made obsolete or duplicate" in hard_gates_flat
    assert "Removal Trigger" in hard_gates
    shape = fallback.split("## Shape Before Build", 1)[1].split(
        "## Implementation Taste", 1
    )[0]
    assert re.findall(r"(?m)^- \*\*([^*]+):\*\*", shape) == [
        "Interview",
        "Map",
        "Research",
        "Probe",
        "Diagnose",
        "Plan",
        "Slice",
        "Handoff",
    ]
    shape_flat = " ".join(shape.split())
    for planning_field in (
        "purpose",
        "boundaries",
        "limitations",
        "decisions",
        "owners",
        "acceptance",
        "actions",
    ):
        assert planning_field in shape_flat
    implementation = fallback.split("## Implementation Taste", 1)[1].split(
        "## Review And Report", 1
    )[0]
    implementation_flat = " ".join(implementation.split())
    assert implementation_flat.index("RED") < implementation_flat.index("GREEN")
    for discipline in (
        "Root Cause",
        "failure atomicity",
        "recovery",
        "idempotency",
        "state lifecycle",
        "observability",
        "oracle",
        "trust-boundary validation",
        "small interfaces",
        "behavior tests",
        "behavior-owned test portfolio",
        "consolidate superseded overlap",
        "measure performance like-for-like",
    ):
        assert discipline.lower() in implementation_flat.lower()
    review = fallback.split("## Review And Report", 1)[1]
    review_flat = " ".join(review.split())
    assert re.findall(r"(?m)^- \*\*(Standards|Spec):\*\*", review) == [
        "Standards",
        "Spec",
    ]
    assert "Lock" in review
    assert "Change Closure resolved every superseded or redundant path" in review_flat
    for bounded_risk in ("supported scenario", "reachable path", "concrete impact"):
        assert bounded_risk in review_flat
    assert "Do not invent speculative edge cases" in review_flat
    assert "one owner, one boundary" in fallback_flat.lower()

    quality = contract.split("## Code Quality Contract", 1)[1].split(
        "## Tight Engineering Spine", 1
    )[0]
    assert "**Must** marks a correctness or safety" in quality
    assert "deviation alone is not a defect" in quality
    assert "not another workflow stage" in quality
    for rule in (
        "**Grounded implementation — must.**",
        "**Correct and robust — must.**",
        "**Domain faithful — must.**",
        "**Change closure — must.**",
        "**Deep and local — prefer.**",
        "**Simple after proof — prefer.**",
        "**Readable by default — prefer.**",
        "**Explicit and provable — must.**",
        "**Measured when relevant — must for claims.**",
    ):
        assert rule in quality
    assert "**Lean test portfolio — prefer.**" in quality
    assert "supported compatibility obligation" in quality
    assert "Removal Trigger" in quality
    assert "**Operational acceptance:**" in contract
    proof = contract.split("## Proof Discipline", 1)[1].split("## Work State", 1)[0]
    proof_flat = " ".join(proof.split())
    assert "Command availability does not determine proof scope" in proof_flat
    assert "Focused and applicable conformance proof are sufficient" in proof_flat
    assert "repository completion policy" in proof_flat
    spine = contract.split("## Tight Engineering Spine", 1)[1].split(
        "## Proof Discipline", 1
    )[0]
    assert "**Simplify:** perform Change Closure" in spine
    lock = contract.split("## Lock", 1)[1]
    assert "Change Closure proved every path superseded or made redundant" in " ".join(
        lock.split()
    )


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
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    specific = (CUSTOM / "triage/SPECIFIC-ITEM.md").read_text(encoding="utf-8")
    quick = (CUSTOM / "triage/QUICK-OVERRIDE.md").read_text(encoding="utf-8")
    brief = (CUSTOM / "triage/AGENT-BRIEF.md").read_text(encoding="utf-8")
    out_of_scope = (CUSTOM / "triage/OUT-OF-SCOPE.md").read_text(encoding="utf-8")

    assert specific.index("mutation packet") < specific.index(
        "universal approval"
    )
    assert "## Completion" in quick
    normalized_triage = " ".join(triage.split())
    assert "Codex-ready brief and Ready Gate" in normalized_triage
    assert "Ready-for-agent state and queries" in normalized_triage
    assert "tracker's Ready-for-agent contract" not in triage
    assert not (CUSTOM / "triage/AGENT-BRIEF-EXAMPLES.md").exists()
    assert "tracker state is navigation metadata" in " ".join(brief.split())
    assert "### Scope And Proof" in brief
    assert "Canonical test owner or proof surface" in brief
    assert "a new test requires a distinct responsibility" in brief
    assert "acceptance is operational and observable" in " ".join(brief.split())
    assert "### Change Closure" in brief
    assert "Removal Trigger" in brief
    assert "## Branch Emphasis" in brief
    for branch in ("Bug tracer", "Enhancement tracer", "Support slice", "PR finish"):
        assert f"| {branch} |" in brief
    for route in ("$grilling", "$grill-with-docs", "$wayfinder", "$to-tickets"):
        assert route in specific
    assert "label-only" not in specific
    assert "not-confirmed" in specific
    assert "does not prove the report false" in specific
    assert "refresh the item, affected dependents, and local targets" in (
        normalized_triage
    )
    assert triage.index("Apply prerequisites and local") < triage.index("close last")
    for status in (
        "scan-complete",
        "decision-required",
        "mutation-complete",
        "blocked-partial",
    ):
        assert f"`{status}`" in triage
    assert "maintainer-override" in quick
    assert "disclaimer-prefixed triage note" in (
        CUSTOM / "triage/ATTENTION-SCAN.md"
    ).read_text(encoding="utf-8")
    assert "Leave it unstaged and stop before commit, push" in out_of_scope
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
        if name == "implement":
            assert "Mutation read-back" in text
            assert "partial or failed closeout Returns" in " ".join(text.split())
        elif name == "parallel-implement":
            assert "mutation read-back" in text
            assert "read that mutation back" in text
        elif name == "to-spec":
            normalized = " ".join(text.split())
            assert (
                "Refetch or reread the full created or reused parent" in normalized
            )
            assert "compare it with the frozen draft" in normalized
            assert "durable read-back" in normalized
        elif name == "to-tickets":
            publish_span = skill_pack_contract.level_two_section_span(
                text, "## Publish"
            )
            assert publish_span is not None
            publish = " ".join(text[slice(*publish_span)].split()).lower()
            assert re.search(
                r"refetch .*complete affected graph.*compare .*verify",
                publish,
            )
            assert "reading back each transition" in publish
        elif name == "triage":
            assert "Mutation read-back" in " ".join(text.split())
        else:
            assert "Mutation read-back" in text, name


def assert_to_tickets_semantic_contract(
    package_root: Path,
    expected_tree_sha256: str,
    *,
    profile: str,
) -> None:
    assert campaign_artifacts.campaign_tree_hash(package_root)["sha256"] == (
        expected_tree_sha256
    )
    tickets = (package_root / "SKILL.md").read_text(encoding="utf-8")
    normalized_runtime = re.sub(r"\s+", " ", tickets.lower())

    def level_two_section(name: str) -> str:
        match = re.search(
            rf"(?ms)^## {re.escape(name)}\n(.*?)(?=^## |\Z)", tickets
        )
        assert match is not None, (package_root, name)
        return re.sub(r"\s+", " ", match.group(1).lower())

    assert not implicit_policy(package_root)
    assert "explicit" in normalized_runtime and "settled" in normalized_runtime
    assert "source" in normalized_runtime and "ready-for-agent" in normalized_runtime
    assert "$repo-bootstrap" in tickets

    shape_contract = level_two_section("Shape")
    assert "vertical behavior slice" in shape_contract
    assert "commitment ledger" in shape_contract
    assert "blocking edge" in shape_contract
    assert re.search(r"dependent consumes.*predecessor outcome", shape_contract, re.S)
    assert re.search(
        r"tracker order and serial constraints are not blockers", shape_contract
    )
    assert "state-boundary matrix" in shape_contract
    assert "treat source-owned responsibilities, interfaces, and seams as fixed" in (
        shape_contract
    )
    assert "do not create or move a seam" in shape_contract
    assert "source-owned proof seam" in shape_contract
    assert "concrete proof lane" in shape_contract
    assert "supported" in shape_contract and "variant" in shape_contract
    assert "not applicable" in shape_contract
    for profile_field in (
        "execution profile",
        "semantic ownership",
        "production writes",
        "proof seams",
        "scarce proof resources",
        "serial tripwire",
    ):
        assert profile_field in shape_contract
    assert "finite nonnegative repair generation budget" in shape_contract
    assert "operational and observable acceptance" in shape_contract
    assert "test every acceptance term" in shape_contract
    assert "operational definition or exact authoritative owner" in shape_contract
    assert "rather than delegate meaning to implementation" in shape_contract
    assert "`not applicable — <reason>` instead of padding" in shape_contract
    assert "never use it for identity, acceptance, scope, proof lane" in shape_contract
    assert "preserve an explicit source or caller value" in shape_contract
    assert "otherwise default exactly to `2`" in shape_contract
    assert "never infer a higher budget from ticket size or risk" in shape_contract
    assert "packet readiness from frontier eligibility" in shape_contract
    assert "ready-for-human" in shape_contract
    assert "mixed graphs may contain both states" in shape_contract
    assert "their union is the actionable frontier" in shape_contract
    assert "at least one must be non-empty" in shape_contract
    assert "dependency order is topological" in shape_contract
    assert "stable tracker order breaks ties" in shape_contract
    assert "ready-for-agent and ready-for-human frontiers separately" in (
        shape_contract
    )
    assert "expand-migrate-contract" in shape_contract
    assert re.search(r"contract only after old usage ends", shape_contract)

    publish_contract = level_two_section("Publish")
    assert re.search(r"freeze .*before .*mutation", publish_contract, re.S)
    assert "preflight proves that configured operations exist" in normalized_runtime
    assert "only the first real mutation proves live behavior" in normalized_runtime
    assert "prove live parent/child behavior" in publish_contract
    assert "prove live dependency behavior" in publish_contract
    assert re.search(
        r"create .*relationship.*activate each ticket's mapped ready-for-agent",
        publish_contract,
        re.S,
    )
    for observed_surface in (
        "affected dependent",
        "bodies",
        "relationships",
        "roles",
        "assignee",
        "state",
        "frontier",
    ):
        assert observed_surface in publish_contract
    for recovery_fact in (
        "applied",
        "failed operation",
        "observed",
        "frontier",
        "safest",
        "recovery",
    ):
        assert recovery_fact in publish_contract

    return_contract = level_two_section("Return")
    assert "exactly one" in return_contract
    assert "$parallel-implement" in return_contract
    assert "$implement" in return_contract
    assert "explicitly requested" in return_contract
    assert "top-level" in return_contract
    assert "non-empty" in return_contract
    assert "parent" in return_contract
    assert "compact cross-ticket proof-owner and serialization summaries" in (
        return_contract
    )
    assert "ticket bodies remain authoritative" in return_contract
    assert "successors refetch their pointers" in return_contract
    assert "per-ticket execution profiles and state matrices" not in return_contract
    assert "no successor" in return_contract or "without starting" in return_contract

    if profile == "incumbent":
        assert re.findall(r"(?m)^## ([A-Za-z]+)$", tickets) == [
            "Shape",
            "Publish",
            "Return",
        ]
        assert re.search(
            r"every source-visible implementation commitment.*ticket acceptance.*"
            r"deferral or exclusion.*no-ticket reason",
            shape_contract,
            re.S,
        )
        assert re.search(
            r"no implementation ticket.*preserve tracker state.*recommend `none`.*stop",
            shape_contract,
            re.S,
        )
        for result_kind in (
            "setup precondition",
            "source-gap packet",
            "no-ticket coverage result",
            "consumer repair packet",
            "partial-publication recovery",
            "published graph",
        ):
            assert result_kind in return_contract
        assert "claim no complete graph" in publish_contract
        assert "exact safe continuation" in return_contract
        assert "recommend and stop without invoking the owner" in return_contract
        assert "every commitment has a disposition" in return_contract
        assert "every authorized mutation and affected relationship reads back" in (
            return_contract
        )
        return

    assert profile == "prompt3-candidate"
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", tickets) == [
        "Admit",
        "Shape",
        "Publish",
        "Return",
    ]
    for result_kind in (
        "`setup-precondition`",
        "`source-gap`",
        "`existing-state-conflict`",
        "`publication-recovery`",
        "`ready-graph`",
    ):
        assert result_kind in return_contract
    assert "one or more implementation tickets" in shape_contract
    assert "their union is the actionable frontier" in shape_contract
    assert "consumer repair" not in return_contract
    assert "no-ticket" not in return_contract
    assert "exact body" not in publish_contract
    assert "normalized-semantic" in publish_contract
    for forbidden_literal in (
        "approved source",
        "tracer bullet",
        "one fresh session",
        "proposal approval",
        "blockers-first",
        "invest checklist",
        "implementation script",
        "preparatory refactoring",
        "coordination requirements",
        "transitive reduction",
        "mutation journal",
    ):
        assert forbidden_literal not in normalized_runtime


def test_to_tickets_preserves_coverage_readiness_and_frontier_contract() -> None:
    packages = (
        (
            CUSTOM / "to-tickets",
            "d24e9829d9d95f8e1823585a40e5eeb99db654f69482ee3a0736e2aad88f108f",
            "prompt3-candidate",
        ),
    )
    for package_root, expected_tree_sha256, profile in packages:
        assert_to_tickets_semantic_contract(
            package_root,
            expected_tree_sha256,
            profile=profile,
        )


def assert_to_spec_semantic_contract(
    package_root: Path,
    expected_tree_sha256: str,
    *,
    profile: str,
) -> None:
    assert campaign_artifacts.campaign_tree_hash(package_root)["sha256"] == (
        expected_tree_sha256
    )
    assert sorted(
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*")
        if path.is_file()
    ) == ["SKILL.md", "agents/openai.yaml"]
    skill = (package_root / "SKILL.md").read_text(encoding="utf-8")
    normalized = re.sub(r"\s+", " ", skill.lower())
    assert re.search(r"(?m)^name: to-spec$", skill)
    assert not implicit_policy(package_root)

    if profile == "author-handoff":
        assert re.findall(r"(?m)^### \d+\. ([A-Za-z ,]+)$", skill) == [
            "Setup",
            "Trace settled source and state",
            "Draft and cover",
            "Publish, verify, and reconcile",
        ]
        for current_semantic in (
            "one durable parent decision contract",
            "bidirectional commitment ledger",
            "source trace",
            "paths are evidence, not an implementation plan",
            "bounded repository grounding",
            "publication-or-reuse proof",
            "publication-recovery",
            "ready-spec",
            "$repo-bootstrap",
            "$to-tickets",
            "apply direct design before drafting",
            "material seam belongs in the spec",
            "create no separate design packet",
            "concrete proof lanes and test owners",
            "exactly one gap kind",
            "do not invoke or recommend a resolver",
            "verified source correction",
            "decision-changing correction is a `source-gap`",
        ):
            assert current_semantic in normalized
        assert re.search(r"reuse only an exact match.*verified absence", normalized)
        assert "published-spec" not in normalized
        return

    assert profile in {
        "m0",
        "h1-01",
        "h1-02",
        "h1-combined",
    }
    headings = re.findall(r"(?m)^## ([A-Za-z]+)$", skill)
    assert headings == [
        "Ownership",
        "Admit",
        "Synthesize",
        "Freeze",
        "Publish",
        "Return",
        "Completion",
    ]

    def section(name: str) -> str:
        span = skill_pack_contract.level_two_section_span(skill, f"## {name}")
        assert span is not None, (package_root, name)
        return re.sub(r"\s+", " ", skill[slice(*span)].lower())

    ownership = section("Ownership")
    admit = section("Admit")
    synthesize = section("Synthesize")
    freeze = section("Freeze")
    publish = section("Publish")
    return_contract = section("Return")
    completion = section("Completion")

    for owner_semantic in (
        "user and accepted source own",
        "without changing domain truth",
        "issue-tracker.md",
        "triage-labels.md",
        "$codebase-design",
        "$to-tickets",
        "$repo-bootstrap",
    ):
        assert owner_semantic in ownership
    for caller_semantic in (
        "direct explicit request",
        "$grill-with-docs",
        "current domain delta",
        "closed wayfinder map",
        "selected improvement",
        "verified audit finding",
        "caller payload identities",
    ):
        assert caller_semantic in admit
    assert re.search(
        r"verified absence.*exact existing equality.*divergence.*unknown state",
        admit,
    )
    assert "source-gap" in admit and "existing-state-conflict" in admit

    for packet_semantic in (
        "source trace",
        "supported paths, states, transitions",
        "security, privacy, permissions",
        "compatibility, migration, rollback",
        "proof seams, proof lanes",
        "map every in-scope commitment",
        "map every specification commitment back",
        "child implementation ticket",
    ):
        assert packet_semantic in synthesize
    assert ".tmp/to-spec/<source-slug>.md" in freeze
    assert re.search(r"read back.*exact bytes.*freeze", freeze)
    assert re.search(r"explicit invocation authorizes.*one-parent", freeze)
    assert re.search(r"reuse only.*exact.*otherwise create once", publish)
    assert re.search(r"immediately refetch.*before applying", publish)
    for observable in (
        "title",
        "body",
        "roles",
        "labels",
        "assignee",
        "relationships",
        "affected frontier",
    ):
        assert observable in publish
    assert "never repeat an indeterminate create" in publish
    assert re.search(r"delete the draft only after verified", publish)

    return_types = (
        "setup-precondition",
        "source-gap",
        "existing-state-conflict",
        "publication-recovery",
        "ready-spec",
    )
    for return_type in return_types:
        assert f"`{return_type}`" in return_contract
    assert "`published-spec`" not in return_contract
    assert "exactly one status" in return_contract
    assert "complete only on `ready-spec`" in completion
    assert "no successor starts" in completion
    assert "git index" in completion and "`head`" in completion

    assert "highest existing" not in normalized
    assert "comprehensive, numbered set of user stories" not in normalized
    assert "value-flow gate" not in normalized
    assert "ears" not in normalized
    assert not re.findall(r"(?m)^### \d+\.", skill)
    assert re.search(
        r"never invent a label, category, or parent ready-for-agent state",
        publish,
    )

    aspect_delta = "test each listed aspect family against source-visible triggers"
    portfolio_delta = "choose an adequate scope-matched portfolio by proof objective"
    assert (aspect_delta in synthesize) == (
        profile in {"h1-01", "h1-combined"}
    )
    assert (portfolio_delta in synthesize) == (
        profile in {"h1-02", "h1-combined"}
    )


def test_to_spec_prompt3_packages_share_the_parameterized_semantic_owner() -> None:
    packages = (
        (
            CUSTOM / "to-spec",
            "4fdfea5b659b73de29c46b7651a4d8e1f449ddecfae3ce168d3786c800b91c32",
            "author-handoff",
        ),
        (
            ROOT / "skills/experimental/to-spec",
            "47c223639318b041e6c86e6144b7fb23399634ead73e18ddcf306ab8242effeb",
            "h1-01",
        ),
    )
    for package_root, expected_tree_sha256, profile in packages:
        assert_to_spec_semantic_contract(
            package_root,
            expected_tree_sha256,
            profile=profile,
        )


def test_parallel_delivery_roles_stay_out_of_the_shared_contract() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "staged worker" not in contract
    assert "lane worker" not in contract
    assert "staged worker" not in implement
    assert "exhaustive parent graph to\n`$parallel-implement`" in implement
    assert "A lane worker or child integrator" in " ".join(parallel.split())


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
    assert re.findall(r"(?m)^## (.+)$", parallel) == [
        "Admit",
        "Run",
        "Review",
        "Lock And Return",
    ]
    run = parallel.split("## Run", 1)[1].split("## Review", 1)[0]
    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^\*\*(Select|Open|Drain)\.\*\*", run)
    ] == ["Select", "Open", "Drain"]
    assert "isolated\nfresh-context lane" in parallel
    assert "## Review-Ready Handoff" in integrator
    assert re.findall(r"(?m)^## (.+)$", launch) == [
        "Open",
        "Startup proof",
        "Dispatch and liveness",
        "Recovery commands",
        "Cleanup",
    ]
    assert "scripts/lane_worktree.py" in launch
    assert "runtime-managed" in launch and "manual Git" in launch
    report = worker.split("```text", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^([^:\n]+):", report) == [
        "status",
        "work item",
        "mode",
        "actor ID",
        "base",
        "commit",
        "changed scope IDs",
        "actual changed files",
        "acceptance proof",
        "test portfolio delta",
        "commands and results",
        "skipped checks",
        "liveness checkpoint",
        "risk or blocker",
        "next need",
        "scope notes",
        "final status",
    ]
    assert "criterion -> evidence" in report
    assert "$diagnosing-bugs" in worker
    assert "## Normal path" in ledger
    assert "## Phases and decisions" in ledger
    assert "## Branch packets" in ledger
    assert "## Advanced and compatibility surface" in ledger
    assert "events.jsonl" in ledger
    assert "LEDGER.md" in ledger and "generated" in ledger
    for command_name in ("start", "status", "apply", "brief", "finish"):
        assert f"run_ledger.py {command_name}" in ledger
    assert "validate-state" in ledger
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
    event_types = runpy.run_path(
        str(CUSTOM / "parallel-implement/scripts/run_ledger.py")
    )["EVENT_TYPES"]
    run = parallel.split("## Run", 1)[1].split("## Review", 1)[0]
    drain = run.split("**Drain.**", 1)[1]
    assert "Accept a worker return only when" in drain
    assert "A blocker" in drain
    report_status = re.search(r"(?m)^status: <([^>]+)>$", worker)
    assert report_status is not None
    assert {status.strip() for status in report_status.group(1).split("/")} == {
        "done",
        "needs-feedback",
        "blocker",
    }
    for outcome in ("complete", "partial", "blocked"):
        assert f"`{outcome}`" in parallel
    assert {
        "scope",
        "scope-change",
        "resume",
        "frontier",
        "checkpoint",
        "integration-regression",
        "integration-correction",
        "review-invocation",
        "repair-plan",
        "repair-complete",
    } <= event_types
    assert "## Cleanup" in launch
    lock = parallel.split("## Lock And Return", 1)[1]
    open_gate = run.split("**Open.**", 1)[1].split("**Drain.**", 1)[0]
    assert "claim" in open_gate
    assert "read back" in parallel.lower()
    assert "closeout plan" in lock and "mutation read-back" in lock
    review = parallel.split("## Review", 1)[1].split(
        "## Lock And Return", 1
    )[0]
    assert "idle" in review


def test_parallel_implement_has_root_receipt_budget_and_windows_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    ledger = (skill_dir / "references/RUN-LEDGER.md").read_text(encoding="utf-8")
    launch = (skill_dir / "references/CODEX-WORKTREE-LAUNCH.md").read_text(
        encoding="utf-8"
    )
    worker = (skill_dir / "references/WORKER-BRIEF.md").read_text(encoding="utf-8")
    integrator = (skill_dir / "references/INTEGRATOR-BRIEF.md").read_text(
        encoding="utf-8"
    )
    script = (skill_dir / "scripts/run_ledger.py").read_text(encoding="utf-8")
    lane_script = (skill_dir / "scripts/lane_worktree.py").read_text(encoding="utf-8")

    assert "The root alone admits scope" in parallel
    assert "before mutation" in parallel
    for field in (
        "repair_generation_budget",
        "review_invocation_budget",
        "review_invocations_required",
    ):
        assert field in ledger and field in script
    assert "append-receipt" in ledger and "append-receipt" in script
    assert "`committed: true`" in ledger
    assert "review-invocation" in ledger
    assert "PARALLEL_IMPLEMENT_WORKTREE_ROOT" in launch and "PARALLEL_IMPLEMENT_WORKTREE_ROOT" in lane_script
    assert "E:\\pi" in launch and 'Path("E:/pi")' in lane_script
    assert "maximum path `320`" in launch
    assert "WINDOWS_DEFAULT_MAX_PATH = 320" in lane_script
    assert "--proof-command-file" in launch and "--proof-command-file" in lane_script
    assert "none_observed" in ledger
    assert "runtime contract 3" in ledger.lower()
    assert "Integration correction" in ledger
    assert "correction_authorization" in script
    assert "runtime contract 3" in ledger
    assert "viability, not throughput" in launch and "-n 0" in launch
    assert "project imports must resolve beneath the lane" in launch
    assert "repo-owned configuration" in launch
    assert "namespace-package locations" in launch
    assert "--python-provenance-file" in launch and "--python-provenance-file" in lane_script
    assert "`original-worker`" in integrator
    assert "### Integration correction" in worker
    assert "regression event ID" in worker
    assert "prior integration HEAD" in worker
    assert "structured write-scope IDs" in worker
    assert "structured write-scope IDs" in ledger
    assert "selected scope-ID subset" in ledger
    assert "owner and lane actor" in ledger
    assert "extended-path" in launch


def test_parallel_implement_exposes_parent_graph_frontier_and_closeout_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    ledger = (skill_dir / "references/RUN-LEDGER.md").read_text(encoding="utf-8")
    ledger_flat = " ".join(ledger.split())
    event_types = runpy.run_path(str(skill_dir / "scripts/run_ledger.py"))["EVENT_TYPES"]
    closeout_fields = runpy.run_path(str(skill_dir / "scripts/run_ledger.py"))[
        "CLOSEOUT_FIELDS"
    ]
    launch = (skill_dir / "references/CODEX-WORKTREE-LAUNCH.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(skill_dir)
    assert "recommend `$implement` and stop" not in parallel

    gate = parallel.split("## Run", 1)[1].split("**Open.**", 1)[0]
    gate_flat = " ".join(gate.split())
    assert "Dispatch concurrently only when" in gate_flat
    assert "otherwise dispatch serially" in gate_flat
    assert "return the exact blockers" in gate_flat

    review = parallel.split("## Review", 1)[1].split(
        "## Lock And Return", 1
    )[0]
    lock = parallel.split("## Lock And Return", 1)[1]
    assert "$change-review" in review
    assert "mutation read-back" in lock
    assert lock.index("child") < lock.index("parent")

    assert closeout_fields == {
        "delivered",
        "acceptance_evidence",
        "proof",
        "review",
        "reviewed_head",
        "residual_risk",
        "intended_mutation",
        "posted_comment",
        "mutation_readback",
    }
    assert "Do not copy field-by-field event contracts" in ledger_flat
    assert {
        "serial-frontier",
        "parallel-frontier",
        "child-closeout",
        "parent-closeout",
    } <= event_types
    assert "serial tripwires" in gate_flat

    assert re.search(
        r"(?m)^\| One explicitly requested parent has an exhaustive non-empty "
        r"Ready-for-agent graph \| `\$parallel-implement` \|$",
        router,
    )
    return_span = skill_pack_contract.level_two_section_span(tickets, "## Return")
    assert return_span is not None
    ticket_return = " ".join(tickets[slice(*return_span)].split()).lower()
    assert "$implement" in ticket_return
    assert "$parallel-implement" in ticket_return
    assert "only when the user explicitly requested" in ticket_return
    assert "verified graph" in ticket_return
    assert "`to-tickets` | Recommend and stop | `$parallel-implement`" in relationships
    assert "| `parallel-implement` | Recommend and stop | `$implement` |" not in relationships


def test_parallel_dependency_overlay_is_campaign_scoped_and_reversible() -> None:
    tracker_surfaces = [
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    ]

    for path in tracker_surfaces:
        text = " ".join(path.read_text(encoding="utf-8").split())
        assert "landed-awaiting-lock" in text, path
        assert "same-campaign" in text, path
        assert "until Lock" in text, path
        assert "reblocks dependents" in text, path


def test_state_boundary_proof_has_one_owner_and_explicit_consumers() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(
        encoding="utf-8"
    )
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(
        encoding="utf-8"
    )
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    ledger = (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").read_text(
        encoding="utf-8"
    )

    owner_text = (
        "**State-boundary matrix.** When correctness depends on cached, persisted, "
        "resumed, grouped, projected, or session-scoped state"
    )
    assert owner_text in " ".join(contract.split())
    assert owner_text in " ".join(seed.split())
    admit_span = skill_pack_contract.level_two_section_span(tickets, "## Admit")
    shape_span = skill_pack_contract.level_two_section_span(tickets, "## Shape")
    assert admit_span is not None and shape_span is not None
    admit = " ".join(tickets[slice(*admit_span)].split()).lower()
    shape = " ".join(tickets[slice(*shape_span)].split()).lower()
    assert "engineering contracts" in admit
    assert "foreign contracts" in admit
    assert "state-boundary matrix" in shape
    assert "supported" in shape and "not applicable" in shape
    assert "graph defect" in " ".join(parallel.split())
    parallel_flat = " ".join(parallel.split())
    assert "final required proof once on the drained current `HEAD`" in parallel_flat
    assert "all applicable state-boundary branches" in parallel_flat
    assert "State-boundary matrix:" in worker
    assert "return it as `needs-feedback`" in " ".join(worker.split())
    assert "This compatibility field is not a campaign" in ledger
    assert "outcome or completion proxy" in ledger


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())

    assert not implicit_policy(CUSTOM / "implement")
    assert "Accept one caller-selected item only" in implement_flat
    assert "A named target remains binding" in implement_flat
    assert "do not substitute another item" in implement_flat
    assert "exhaustive parent graph to\n`$parallel-implement`" in implement
    assert "staged worker" not in implement


def test_local_tracker_closeout_enters_the_lock_snapshot() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())

    review_tree = implement.index("pin one immutable proved candidate")
    closeout = implement.index("For Local Markdown, append the final closeout")
    lock_tree = implement.index("Lock the exact reviewed candidate")

    assert review_tree < closeout < lock_tree
    assert "apply Mutation read-back" in implement
    assert "Any other review-to-lock delta Returns to formal review" in implement
    assert "Only configured mechanical closeout fields" in implement_flat
    assert "new narrative or semantic content Returns to formal review" in (
        implement_flat
    )
    assert "Produce exactly one commit" in implement_flat
    assert "read-back proves `HEAD` unchanged" in implement_flat
    assert "do not retry blindly" in implement_flat
    assert "A retry inside the same active run is not a Return" in implement_flat
    assert "terminal `partial` or `blocked` Return releases the claim" in (
        implement_flat
    )
    assert "named retained custodian" in implement_flat


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
    assert "regression proof or an explicit seam gap" in relationships
    assert all(
        not (caller == "diagnosing-bugs" and callee == "audit-codebase")
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
        ("grilling", "Recommend and stop", "to-questionnaire"),
        ("grilling", "Recommend and stop", "handoff"),
        ("to-questionnaire", "Recommend and stop", "research"),
        ("to-questionnaire", "Recommend and stop", "grilling"),
        ("to-spec", "Load", "codebase-design"),
        ("wayfinder", "Invoke", "research"),
        ("wayfinder", "Invoke", "prototype"),
        ("wayfinder", "Invoke", "diagnosing-bugs"),
        ("wayfinder", "Invoke", "grilling"),
        ("wayfinder", "Invoke", "grill-with-docs"),
        ("wayfinder", "Invoke", "to-questionnaire"),
        ("wayfinder", "Invoke", "domain-modeling"),
        ("wayfinder", "Recommend and stop", "to-spec"),
        ("triage", "Recommend and stop", "grilling"),
        ("triage", "Recommend and stop", "grill-with-docs"),
        ("triage", "Recommend and stop", "wayfinder"),
        ("triage", "Recommend and stop", "to-tickets"),
        ("implement", "Invoke", "tdd"),
        ("implement", "Invoke", "diagnosing-bugs"),
        ("implement", "Invoke", "change-review"),
        ("implement", "Invoke", "high-assurance-review"),
        ("implement", "Hand off", "resolving-merge-conflicts"),
        ("change-review", "Hand off", "high-assurance-review"),
        ("change-review", "Recommend and stop", "audit-codebase"),
        ("high-assurance-review", "Recommend and stop", "audit-codebase"),
        ("parallel-implement", "Invoke", "high-assurance-review"),
        ("parallel-implement", "Invoke", "resolving-merge-conflicts"),
        ("resolving-merge-conflicts", "Invoke", "diagnosing-bugs"),
        ("audit-codebase", "Recommend and stop", "domain-modeling"),
        ("audit-codebase", "Recommend and stop", "grill-with-docs"),
        ("audit-codebase", "Recommend and stop", "grilling"),
        ("audit-codebase", "Recommend and stop", "research"),
        ("audit-codebase", "Recommend and stop", "prototype"),
        ("audit-codebase", "Recommend and stop", "diagnosing-bugs"),
        ("audit-codebase", "Recommend and stop", "to-questionnaire"),
        ("audit-codebase", "Load", "codebase-design"),
        ("audit-codebase", "Recommend and stop", "wayfinder"),
        ("audit-codebase", "Recommend and stop", "to-spec"),
        ("audit-codebase", "Recommend and stop", "to-tickets"),
        ("audit-codebase", "Recommend and stop", "simplify-code"),
        ("audit-codebase", "Recommend and stop", "implement"),
        ("simplify-code", "Recommend and stop", "audit-codebase"),
        ("tdd", "Hand off", "diagnosing-bugs"),
        ("tdd", "Hand off", "prototype"),
        ("tdd", "Recommend and stop", "simplify-code"),
        ("tdd", "Recommend and stop", "audit-codebase"),
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
        ("codebase-design", "Recommend and stop", "audit-codebase"),
    }

    assert required <= edges
    assert ("audit-codebase", "Invoke", "codebase-design") not in edges
    for removed_edge in (
        ("audit-codebase", "Recommend and stop", "codebase-design"),
        ("research", "Recommend and stop", "codebase-design"),
        ("simplify-code", "Recommend and stop", "codebase-design"),
        ("tdd", "Recommend and stop", "codebase-design"),
    ):
        assert removed_edge not in edges
    assert ("high-assurance-review", "Hand off", "change-review") not in edges
    assert ("wayfinder", "Recommend and stop", "to-tickets") not in edges
    assert ("wayfinder", "Recommend and stop", "implement") not in edges
    assert ("to-questionnaire", "Recommend and stop", "grill-with-docs") not in edges
    assert ("research", "Recommend and stop", "to-questionnaire") not in edges

    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    closure = wayfinder.split("## Closure", 1)[1].split("\n## ", 1)[0]
    assert "`$to-spec`" in closure
    assert "settled parent-spec source" in closure
    assert "Never route a closed map directly to" in closure
    for forbidden in ("`$to-tickets`", "`$implement`", "`$parallel-implement`"):
        assert forbidden in closure

    skill_names = {skill.name for skill in CUSTOM.iterdir() if skill.is_dir()}
    approved_explicit_invocations = {
        ("wayfinder", "Invoke", "to-questionnaire"),
    }
    for caller, verb, callee in rows:
        assert caller in skill_names
        assert callee in skill_names
        if verb != "Recommend and stop" and (caller, verb, callee) not in (
            approved_explicit_invocations
        ):
            assert implicit_policy(CUSTOM / callee), (
                f"{caller} cannot {verb} explicit-only skill {callee}; "
                "require an exact user-approved invocation packet or recommend it"
            )


def test_router_and_synthesis_keep_active_ownership_unambiguous() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    synthesis_index = (ROOT / "docs/synthesis/README.md").read_text(encoding="utf-8")

    assert "target-spine.md" not in synthesis_index
    assert "language-direction.md" not in synthesis_index
    assert "support tickets" not in tickets
    assert "support slices" not in tickets
