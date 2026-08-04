from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

from scripts import (
    campaign_artifacts,
    pack_contract,
    skill_pack_contract,
    validate_skills,
)


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
        "## Work-item representation",
        "**State:**",
        "navigation metadata",
        "not proof that a packet or transition is valid",
        "**Ready query:**",
        "agent and human frontiers separately",
        "## Mutation read-back",
        "unverified partial mutation",
    )
    skill_owned = (
        "Source Trace",
        "observable acceptance criteria",
        "proof lane",
        "expected write scope",
        "parallel-safety note",
        "scope fence",
        "landed-awaiting-lock",
        "Elapsed time alone never makes a claim stale",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for token in required:
            assert token in normalized, f"{tracker} is missing {token}"
        for token in skill_owned:
            assert token.lower() not in normalized.lower(), (
                f"{tracker} still owns {token}"
            )


def test_wayfinder_owns_claim_lifecycle_while_trackers_own_representation() -> None:
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )
    for tracker in trackers:
        wayfinding = tracker.read_text(encoding="utf-8").split(
            "## Wayfinding representation", 1
        )[1]
        wayfinding_flat = " ".join(wayfinding.split())
        for foreign_procedure in (
            "codex/<lowercase UUIDv4>",
            "<YYYY-MM-DDTHH:MM:SSZ>",
            "Elapsed time alone never makes a claim stale.",
            "approver authority",
        ):
            assert foreign_procedure not in wayfinding_flat

    wayfinder = " ".join(
        (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8").split()
    )
    for token in (
        "codex/<lowercase UUIDv4>",
        "<YYYY-MM-DDTHH:MM:SSZ>",
        "For each invocation",
        "never across invocations",
        "A different token owns an item",
        "elapsed time alone never makes a claim stale.",
        "exclusive claim route with an observable losing-race result",
        "affirmed destination owner or provider administrator",
        "approver authority",
        "verify claim absence",
    ):
        assert token in wayfinder


def test_repo_bootstrap_validates_provider_tracker_templates() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    wayfinder_failures = validator["wayfinder_contract_failures"]
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        failures: list[str] = []
        validator["require_tokens"](
            text,
            str(tracker),
            validator["WORK_ITEM_TOKENS"],
            failures,
        )
        validator["require_prose_tokens"](
            text,
            str(tracker),
            validator["WORK_ITEM_PROSE_TOKENS"],
            failures,
        )
        assert failures == []
        assert wayfinder_failures(text, str(tracker)) == []

    github = trackers[0].read_text(encoding="utf-8")
    failures = []
    validator["require_tokens"](
        github,
        str(trackers[0]),
        validator["GITHUB_CAMPAIGN_SNAPSHOT_TOKENS"],
        failures,
    )
    assert failures == []
    missing_snapshot = github.replace("**Campaign snapshot:**", "**Snapshot:**", 1)
    failures = []
    validator["require_tokens"](
        missing_snapshot,
        str(trackers[0]),
        validator["GITHUB_CAMPAIGN_SNAPSHOT_TOKENS"],
        failures,
    )
    assert failures == [
        f"{trackers[0]} is missing **Campaign snapshot:**"
    ]

    hosted = trackers[0].read_text(encoding="utf-8").replace(
        "Blocked: waiting - <gist>", "Blocked: paused - <gist>"
    )
    assert any(
        "Blocked: waiting - <gist>" in item
        for item in wayfinder_failures(hosted, "hosted")
    )

    local = trackers[2].read_text(encoding="utf-8").replace(
        "Status: Pending | In Progress | Resolved | Blocked | Waiting | Out Of Scope",
        "Status: Pending | Resolved",
    )
    assert any(
        "Status: Pending | In Progress | Resolved | Blocked | Waiting | Out Of Scope"
        in item
        for item in wayfinder_failures(local, "local")
    )

    misplaced = hosted.replace("Store `Participation:`", "Store participation")
    misplaced += "\nParticipation:\n"
    assert any(
        "section ## Wayfinding representation is missing Participation:" in item
        for item in wayfinder_failures(misplaced, "hosted")
    )

    missing_boundary = hosted.replace("`Mutation boundary:`, ", "")
    assert any(
        "section ## Wayfinding representation is missing Mutation boundary:" in item
        for item in wayfinder_failures(missing_boundary, "hosted")
    )

    fenced_decoy = hosted.replace("Store `Participation:`", "Store participation")
    fenced_decoy += "\n```text\n## Wayfinding representation\nParticipation:\n```\n"
    assert any(
        "section ## Wayfinding representation is missing Participation:" in item
        for item in wayfinder_failures(fenced_decoy, "hosted")
    )

    fenced_token = hosted.replace(
        "Store `Participation:`",
        "Store participation\n\n```text\nParticipation:\n```",
    )
    assert any(
        "section ## Wayfinding representation is missing Participation:" in item
        for item in wayfinder_failures(fenced_token, "hosted")
    )


def test_triage_label_template_respects_tracker_pr_policy() -> None:
    labels = (CUSTOM / "repo-bootstrap/triage-labels.md").read_text(encoding="utf-8")
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    triage_flat = " ".join(triage.split())

    assert "Every triaged work item" in labels
    assert "Every triaged issue or PR" not in labels
    assert "`wayfinder:questionnaire`" in labels
    assert "Triage PRs only when the tracker enables them" in triage_flat


def test_delivery_skills_own_custody_and_trackers_map_closeout() -> None:
    hosted_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
    )
    for tracker in hosted_trackers:
        normalized = " ".join(tracker.read_text(encoding="utf-8").split())
        assert "**Closeout:**" in normalized
        assert "## Mutation read-back" in normalized
        assert "false-ready dependent" in normalized
        assert "named recovery custodian" not in normalized

    github = hosted_trackers[0].read_text(encoding="utf-8")
    assert "**Close implemented items:** yes." in github

    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    assert "closure defaults to yes for GitHub and no for GitLab" in bootstrap

    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    for token in ("landed-awaiting-lock", "indeterminate-closeout claim"):
        assert token in parallel


def test_github_relationship_modes_are_explicit_before_publication() -> None:
    github_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
    )
    for tracker in github_trackers:
        text = tracker.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        assert "**Parent / child mode:** native-sub-issues." in text
        assert "**Dependency mode:** native-dependencies." in text
        assert "Resolve the authenticated operation and read-back route before" in (
            normalized
        )
        assert "never switch representations during one publication" in normalized
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


def test_repo_bootstrap_domain_contract_is_wrap_safe_and_causal() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["domain_contract_failures"]
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")

    assert check(domain, "docs/agents/domain.md") == []
    wrapped = domain.replace(
        "Do not flatten different meanings across contexts.",
        "Do not flatten different meanings\nacross contexts.",
    )
    assert check(wrapped, "docs/agents/domain.md") == []

    invalid = domain.replace(
        "never silently override them",
        "may override them",
    )
    failures = check(invalid, "docs/agents/domain.md")
    assert failures == [
        "docs/agents/domain.md is missing never silently override them"
    ]
    assert check(domain, "docs/agents/domain.md") == []


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
    domain_flat = " ".join(domain.split())
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
        for obligation in (
            "current user names it",
            "grants no execution, mutation, resumption, or completion authority",
            "inventory through draft is read-only",
            "identity is structural evidence",
            "`compatible`, `delta`, `conflict`, or `not applicable`",
            "a `conflict` blocks only its affected delta",
            "with zero delta, mutate nothing",
            "proposal only",
            "before each effect",
            "never recompute a delta under old approval",
            "create or reconcile",
            "`applied`, `failed`, `unknown`, or `not attempted`",
            "never retry without new proof or assume rollback",
            "setup incomplete",
            "verified zero delta or verified approved delta",
        ):
            assert obligation in normalized
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
    for contract in (
        "**Configured layout:** <single-context | multi-context>",
        "## Route",
        "## Preserve The Model",
        "**single-context:** root `CONTEXT.md` and applicable `docs/adr/`.",
        "`CONTEXT-MAP.md`",
        "`<context-root>/docs/adr/`",
        "setup neither creates nor recommends them.",
        "$domain-modeling` alone may create or change domain truth",
        "canonical terms, invariants, ownership, and relationship language",
        "Do not flatten different meanings across contexts.",
        "return the exact gap",
        "never silently override them",
        "decision owner",
    ):
        assert contract in domain_flat
    assert "src/<context>/docs/adr/" not in domain


def test_repo_bootstrap_reconciles_existing_setup_without_reset() -> None:
    assert_repo_bootstrap_semantic_contract(
        CUSTOM / "repo-bootstrap",
        "053d87ef0a66f935725ac8746b566a481f7985788321a9dc30953fc79b402601",
        profile="incumbent",
    )


def test_repo_bootstrap_owns_optional_parallel_support_and_reconciliation(
    tmp_path: Path,
) -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["parallel_support_failures"]
    bootstrap = " ".join(
        (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8").split()
    )
    root = tmp_path / "repo"
    root.mkdir()

    assert check(root) == []
    assert "When support is absent, ask whether to enable it" in bootstrap
    assert "goes directly through Reconcile without this question" in bootstrap
    assert "one missing or stale half is a `delta`" in bootstrap
    assert "do not create worktrees or external directories" in bootstrap

    agent = root / validator["PARALLEL_AGENT"]
    agent.parent.mkdir(parents=True)
    template = CUSTOM / "parallel-implement/assets/luna_max.toml"
    agent.write_bytes(template.read_bytes())
    assert check(root) == [
        "Parallel implementation support is missing .codex/config.toml"
    ]

    config = root / validator["PARALLEL_CONFIG"]
    lane_root = tmp_path / "lanes" / "wt"
    encoded_lane_root = json.dumps(str(lane_root.resolve()))
    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{encoded_lane_root} = true\n"
        f"{json.dumps(str((tmp_path / 'cache').resolve()))} = true\n",
        encoding="utf-8",
    )
    assert check(root) == []

    nested_root = root / "nested" / "wt"
    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{json.dumps(str(nested_root.resolve()))} = true\n",
        encoding="utf-8",
    )
    assert check(root) == ["parallel lane root must be outside the repository"]

    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{encoded_lane_root} = true\n",
        encoding="utf-8",
    )

    agent.write_text("name = \"stale\"\n", encoding="utf-8")
    assert check(root) == [
        ".codex/agents/luna_max.toml does not match the current template"
    ]


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
        assert signature in (validator["markdown_section"](fallback, heading) or "")
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
    flat = " ".join(wayfinder.split())

    assert not implicit_policy(skill_dir)
    assert "[MAP-FORMAT.md](MAP-FORMAT.md)" in wayfinder
    chart, modes = wayfinder.split("## Chart", 1)[1].split("## Advance", 1)
    advance, remaining = modes.split("## Maintain", 1)
    maintain, closure = remaining.split("## Closure", 1)
    for earlier, later in (
        ("**Bound.**", "**Admit.**"),
        ("**Admit.**", "**Sweep.**"),
        ("**Sweep.**", "**Approve.**"),
        ("**Approve.**", "**Create.**"),
        ("**Create.**", "**Verify.**"),
    ):
        assert chart.index(earlier) < chart.index(later)
    for earlier, later in (
        ("**Select.**", "**Claim.**"),
        ("**Claim.**", "**Resolve.**"),
        ("**Resolve.**", "**Commit.**"),
        ("**Commit.**", "**Verify.**"),
    ):
        assert advance.index(earlier) < advance.index(later)
    assert re.findall(
        r"(?m)^## (Chart|Advance|Maintain|Closure|Terminate)$", wayfinder
    ) == [
        "Chart",
        "Advance",
        "Maintain",
        "Closure",
        "Terminate",
    ]
    for field in (
        "Destination:",
        "owner",
        "outcome",
        "scope",
        "route-closing condition",
        "terminal kind",
        "return owner",
    ):
        assert field in flat
    admit = chart.split("2. **Admit.**", 1)[1].split("3. **Sweep.**", 1)[0]
    admit_flat = " ".join(admit.split())
    chart_flat = " ".join(chart.split())
    assert "exact destination tuple" in flat
    assert "a successor may enter Chart only with one explicitly selected closed predecessor" in flat
    assert "destination tuple plus predecessor" in flat
    orient = wayfinder.split("## Mutation Gate", 1)[0]
    orient_flat = " ".join(orient.split())
    assert "select exactly one branch" in orient_flat
    assert orient_flat.index("a successor may enter Chart only") < orient_flat.index(
        "one explicitly selected closed match returns its immutable packet"
    )
    assert "Run exactly one selected operation and return its verified result" in orient_flat
    assert "may independently select Closure" in orient_flat
    assert "zero-match initial or successor identity" in chart_flat
    assert "Predecessor:" in map_format
    assert "a non-conversational resolver" in admit_flat
    assert "return `not-needed`" in admit_flat
    assert "recommend `$to-spec` only for an already settled source" in admit_flat
    map_template = map_format.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", map_template) == [
        "Destination",
        "Scope Boundary",
        "Notes",
        "Decisions So Far",
        "Not Yet Specified",
        "Out Of Scope",
    ]
    assert "approved repo-local path" in map_format
    mutation_flat = " ".join(
        wayfinder.split("## Mutation Gate", 1)[1]
        .split("## Resolver Gate", 1)[0]
        .split()
    )
    assert "Chart is the only pre-claim exception" in mutation_flat
    assert mutation_flat.index("approve the exact packet") < mutation_flat.index(
        "create only the map"
    )
    assert mutation_flat.index("repeat identity search") < mutation_flat.index(
        "claim the sole created canonical map"
    )
    assert chart_flat.index("[MAP-FORMAT.md](MAP-FORMAT.md)-conforming") < chart_flat.index(
        "Apply the initial-map exception"
    )
    assert "confirm zero matches" in mutation_flat
    assert "sole created canonical map" in mutation_flat
    assert chart_flat.index("read back identities") < chart_flat.index(
        "wire edges from those identities"
    )
    assert "no ticket outcome" in chart_flat
    assert "no ticket outcome" in " ".join(maintain.split())
    assert "independently selectable" in closure


def test_wayfinder_prototype_participation_matches_judgment() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    resolver = wayfinder.split("## Resolver Gate", 1)[1].split("## Reconcile", 1)[0]
    resolver_flat = " ".join(resolver.split())
    for contract in (
        "`shape/feel` uses HITL, human judgment",
        "Objective `design evidence` defaults to AFK/rule-based",
        "named human verdict owner makes it HITL",
        "[MAP-FORMAT.md](MAP-FORMAT.md)'s complete Prototype packet",
    ):
        assert contract in resolver_flat

    approve = wayfinder.split("4. **Approve.**", 1)[1].split(
        "5. **Create.**", 1
    )[0]
    approve_flat = " ".join(approve.split())
    assert "[MAP-FORMAT.md](MAP-FORMAT.md)-conforming packet" in approve_flat
    assert "exact map title" in approve_flat
    assert "resolver fields" in approve_flat

    for field in (
        "Decision owner:",
        "Result recipient:",
        "Claim level:",
        "Judgment mode:",
        "Human judge:",
        "Verdict criteria:",
        "Prototype evidence surface and representative cases:",
        "Prototype paths and final disposition:",
        "Prototype effects, entry, bound, and limits:",
    ):
        assert field in map_format


def test_wayfinder_routes_by_authority_and_accounts_for_fog() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")
    map_flat = " ".join(map_format.split())

    resolver = wayfinder.split("## Resolver Gate", 1)[1].split("## Reconcile", 1)[0]
    resolver_flat = " ".join(resolver.split())
    assert "conversation-only user decision" in resolver_flat
    assert "objectively provable repository or operational fact" in resolver_flat
    assert "Wayfinder normalizes the intact resolver Return" in resolver_flat
    assert "Intact Research `conflicted`" in resolver_flat
    assert "never `resolved` or generic `incomplete`" in resolver_flat
    assert "**Frontier:** `Pending`, dependency-unblocked, unclaimed tickets" in wayfinder
    assert "Waiting and Blocked enter only through their evidence-qualified" in wayfinder
    assert "`$grilling`" in resolver_flat
    assert "`$grill-with-docs`" in resolver_flat
    assert "Advance receives nested Grilling `Route gap`" in resolver_flat
    assert "never recommend Wayfinder to itself" in resolver_flat
    assert "claim-free proposed Chart input" in resolver_flat
    assert "require exact approval of the resulting packet" in resolver_flat
    assert "`diagnosis-required`" in resolver_flat
    assert "$diagnosing-bugs" not in resolver_flat
    assert "only after the user approves its exact caller packet" in resolver_flat
    assert "`Questionnaire ready` is Waiting, never an answer" in resolver_flat
    assert "supported map use, scope, exact state, Source Trace" in resolver_flat
    assert "Task" in resolver_flat and "no durable mutation" in resolver_flat
    for field in (
        "Resolution owner:",
        "Resolver:",
        "Expected return:",
        "Re-entry owner: $wayfinder",
        "Type: Research | Prototype | Diagnosis | Grilling | Questionnaire | Task",
    ):
        assert field in map_format

    advance = wayfinder.split("## Advance", 1)[1].split("## Maintain", 1)[0]
    advance_flat = " ".join(advance.split())
    claim = advance.split("2. **Claim.**", 1)[1].split("3. **Resolve.**", 1)[0]
    claim_flat = " ".join(claim.split())
    assert "exclusively claim the ticket" in claim_flat
    assert "owner, token, and claimed-at read-back" in claim_flat
    assert "Waiting or Blocked ticket" in advance_flat
    assert "validate the attributable return" in advance_flat
    assert "Acquire the map claim with the same token" in advance_flat
    assert "no tracker outcome or map mutation" in resolver_flat
    assert "frozen-boundary resolver effects" in resolver_flat
    assert "release both and Orient" in advance_flat
    mutation = wayfinder.split("## Mutation Gate", 1)[1].split(
        "## Resolver Gate", 1
    )[0]
    assert "release both claims and verify their absence" in " ".join(mutation.split())
    for outcome in ("resolved", "blocked", "waiting", "out of scope"):
        assert f"`{outcome}`" in resolver

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }
    research_edge = next(
        row
        for row in contract["relationships"]
        if names[row["caller_skill_id"]] == "wayfinder"
        and names[row["target_skill_id"]] == "research"
        and row["verb"] == "Invoke"
    )
    for field in (
        "Wayfinder question",
        "supported map use",
        "scope and exclusions",
        "applicable state",
        "approved note path and write mode",
        "Source Trace",
        "return owner",
    ):
        assert field in research_edge["input_packet"]

    reconcile = wayfinder.split("## Reconcile", 1)[1].split("## Chart", 1)[0]
    reconcile_flat = " ".join(reconcile.split())
    for disposition in ("**retain**", "**graduate**", "**resolve**", "**exclude**"):
        assert disposition in reconcile
    assert "post-Chart ticket allowance" in reconcile_flat
    assert "Every later ticket creation consumes one" in reconcile_flat
    assert "## Not Yet Specified" in map_format
    assert "None - all remaining in-scope questions are ticket-owned." in map_flat
    for fog_field in (
        "Owner:",
        "Sharpening source:",
        "Observable trigger:",
        "Fallback:",
        "Affecting tickets:",
    ):
        assert fog_field in map_format

    maintain = wayfinder.split("## Maintain", 1)[1].split("## Closure", 1)[0]
    maintain_flat = " ".join(maintain.split())
    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", maintain) == [
        "Bound",
        "Claim",
        "Apply",
        "Verify",
    ]
    assert "no resolver judgment or ticket outcome" in maintain_flat
    assert "exclusively claim the map" in maintain_flat
    assert "proved wait or blocker transition" in maintain_flat
    assert "fog trigger that now makes its question sharp" in maintain_flat
    assert "approval only to increase the allowance" in maintain_flat

    closure = wayfinder.split("## Closure", 1)[1].split("## Terminate", 1)[0]
    closure_flat = " ".join(closure.split())
    assert "independently selectable from `closeable` state" in closure_flat
    assert "Hold no claim" in closure_flat
    assert "invoke `$domain-modeling` once" in closure_flat
    assert "unaccounted durable-language or ADR consequence" in closure_flat
    assert "`persist authorized` only with exact domain-write authority" in closure_flat
    assert "`render only` otherwise" in closure_flat
    assert "material blocker leaves the map open" in closure
    assert "route-closing condition" in closure_flat
    assert "newly sharp gap as exact Maintain input" in closure_flat
    assert "creates and wires its ticket within the approved allowance" in closure_flat
    assert "Build [MAP-FORMAT.md](MAP-FORMAT.md)'s closing packet" in closure_flat
    assert closure_flat.index("post the packet") < closure_flat.index(
        "close as `delivered`"
    )
    assert closure_flat.index("close as `delivered`") < closure_flat.index(
        "read back closed state and empty frontier"
    )
    assert "settled parent-spec source" in closure_flat
    assert "terminal decision" in closure_flat

    returned = wayfinder.split("## Return", 1)[1]
    returned_flat = " ".join(returned.split())
    assert (
        "Next frontier: [<ticket title>](<link>). Invoke $wayfinder to advance it."
        in returned_flat
    )
    operation_values = re.search(r"Operation result: ([^\n]+)", returned)
    assert operation_values is not None
    assert operation_values.group(1).strip() == (
        "oriented | charted | advanced | maintained | closed | terminated | "
        "not-needed | incomplete"
    )
    assert "Map condition: active | waiting | blocked | closeable | closed" in returned_flat
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
    assert "Preserve every `Evidence gap` or `Route gap` field exactly" in " ".join(
        grill_docs.split()
    )
    assert "declared return owner, or the user on direct invocation" in " ".join(
        grill_docs.split()
    )
    assert "When active `$wayfinder` is the return owner" in grilling
    for contract in (
        "each settled material answer to Domain Modeling",
        "every returned collision or blocker to Grilling",
        "never merge or reinterpret it",
        "Any material blocker in the current Domain Delta makes the "
        "combined status `Blocked`",
        "Composition blocker, owner, and re-entry condition",
        "preserves its originating blocker and owner",
    ):
        assert contract in " ".join(grill_docs.split())


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())
    context_format = (
        CUSTOM / "domain-modeling/CONTEXT-FORMAT.md"
    ).read_text(encoding="utf-8")
    context_format_flat = " ".join(context_format.split())

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
        "implementation defect, model correction, or intentional migration",
    ):
        assert contract in domain_flat
    assert (
        "Within one context, its local model owns canonical meaning. Across "
        "contexts, preserve independent meanings unless an explicit "
        "relationship contract or Shared Kernel says otherwise."
    ) in context_format_flat


def test_instantiated_domain_helper_preserves_routing_and_ownership() -> None:
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())

    assert "**Configured layout:** single-context." in domain
    assert "setup-file:" not in domain
    for contract in (
        "Missing records are not setup gaps.",
        "setup neither creates nor recommends them.",
        "$domain-modeling` alone may create or change domain truth",
        "Do not flatten different meanings across contexts.",
        "never silently override them",
        "decision owner",
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
        "Except for the named Fit mismatch above, do not select, recommend, or invoke a downstream route",
        "recommend `$diagnosing-bugs` and stop before mutation",
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

    assert re.search(r"(?m)^name: change-review$", review)
    assert re.search(r"(?m)^name: high-assurance-review$", convergent)
    assert "$high-assurance-review" not in review
    assert "$change-review" not in convergent.split("## 1. Admit", 1)[1].split(
        "## 2. Pin", 1
    )[0]
    assert "scope-mismatch" in review
    assert "scope-mismatch" in convergent
    assert "only when documented repo standards" in " ".join(baseline.split())
    assert "concrete, actionable maintainability risk" in baseline
    assert (
        "change-review/SMELL-BASELINE.md` only when Standards are thin"
        in " ".join(convergent.split())
    )
    report = review.split("```text", 2)[2].split("```", 1)[0]
    for field in (
        "Invocation: formal-delivery | standalone",
        "Review mode: initial | remediation",
        "Semantic agent: ordinary-reviewer",
        "Reviewer actor ID:",
        "Reviewer task ID:",
        "Runtime binding: agent type <value or standalone>; requested <model and reasoning or standalone>; observed <values or unavailable>",
        "Fresh-context and separation evidence: <evidence> | standalone",
        "Coverage: complete | incomplete",
        "Decision: pass | pass with residual risk | blocked | incomplete",
        "Standards findings:",
        "Spec findings:",
        "Candidate:",
    ):
        assert field in report


def test_spawned_agents_share_one_runtime_profile_owner() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    profiles = (
        CUSTOM / "parallel-implement/references/RUNTIME-PROFILES.md"
    ).read_text(
        encoding="utf-8"
    )
    ledger_script = (
        CUSTOM / "parallel-implement/scripts/run_ledger.py"
    ).read_text(encoding="utf-8")
    profiles_flat = " ".join(profiles.split())

    assert re.findall(
        r"(?m)^\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|$",
        profiles,
    ) == [
        ("parallel-root", "current", "gpt-5.6-sol", "high"),
        ("clear-worker", "luna_max", "gpt-5.6-luna", "max"),
        ("adaptive-worker", "default", "gpt-5.6-terra", "xhigh"),
        ("fast-adaptive-worker", "default", "gpt-5.6-sol", "medium"),
        ("demanding-worker", "default", "gpt-5.6-sol", "high"),
        ("serial-integrator", "default", "gpt-5.6-sol", "medium"),
        ("ordinary-reviewer", "default", "gpt-5.6-sol", "high"),
        ("assurance-coordinator", "default", "gpt-5.6-sol", "high"),
        ("har-spec-reviewer", "default", "gpt-5.6-sol", "xhigh"),
        ("har-standards-reviewer", "default", "gpt-5.6-sol", "xhigh"),
        ("har-specialist", "default", "gpt-5.6-sol", "xhigh"),
    ]
    assert "A named agent type loads its custom TOML" in profiles_flat
    assert "`transport-invalid` and receives no review credit" in profiles_flat
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in implement
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in review
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in assurance
    assert 'references/RUNTIME-PROFILES.md' in ledger_script
    assert "assurance reviewer binding does not match" in ledger_script
    custom_agents = sorted((ROOT / ".codex/agents").glob("*.toml"))
    assert [path.name for path in custom_agents] == ["luna_max.toml"]
    luna = custom_agents[0].read_text(encoding="utf-8")
    assert 'model = "gpt-5.6-luna"' in luna
    assert 'model_reasoning_effort = "max"' in luna
    review_flat = " ".join(review.split())
    assert "missing or mismatched formal-delivery binding" in review_flat
    assert "`transport-invalid` before candidate judgment" in review_flat
    assert "Standalone review records its current runtime provenance" in " ".join(
        review.split()
    )
    for skill in (implement, review, assurance):
        assert "gpt-5.6" not in skill


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
    assert "A frozen delivery request authorizes `automatic-in-scope` remediation" in (
        " ".join(finding.split())
    )
    assert "every other class returns for caller decision" in " ".join(
        finding.split()
    )
    remediation = finding.split("## Remediation Review", 1)[1].split(
        "## Severity And Remediation", 1
    )[0]
    remediation_flat = " ".join(remediation.split())
    for field in (
        "`Invocation: formal-delivery`",
        "`Review mode: remediation`",
        "original Charter",
        "prior snapshot identity",
        "stable carried IDs",
        "caller-owned Repair delta",
        "remaining acceptance",
        "fixed point",
        "successor candidate",
    ):
        assert field in remediation_flat
    for skill in (review, convergent):
        assert "Finding Contract's remediation packet and coverage boundary" in " ".join(
            skill.split()
        )


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
    assert "PR existence, size, labels, and hypothetical cases do not qualify." in finding_flat
    assert "not a blind Cartesian product" in review
    assert "not a blind Cartesian product" in convergent_flat
    assert "Reuse proof tied to the exact snapshot" in review
    assert "Reuse exact-snapshot proof" in convergent_flat
    assert "ordinary local PR" in review
    assert "FINDING-CONTRACT.md" in convergent
    assert "governed by at least one supported" in convergent_flat
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

    assert (
        "exactly two direct core reviewer lanes as fresh read-only collaboration subagents"
        in " ".join(convergent.split())
    )
    assert "Record each lane's semantic agent ID, runtime agent type, actor ID, task ID" in convergent
    contract = (
        convergent.split("this return contract:", 1)[1]
        .split("```text", 1)[1]
        .split("```", 1)[0]
    )
    assert set(re.findall(r"(?m)^([a-z ]+):", contract)) == {
        "status",
        "lane",
        "axis",
        "classes",
        "coverage",
        "finding candidates",
        "skipped checks",
        "blockers",
    }


def test_high_assurance_review_has_root_guard_bounded_capacity_and_risk() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    convergent_flat = " ".join(convergent.split())

    assert "the `assurance-coordinator`, the root of its review run" in convergent_flat
    assert "requested and observed-or-unavailable model and reasoning" in convergent_flat
    assert "binding returns `transport-invalid` before Pin" in convergent_flat
    assert "nested review lane that invokes this skill returns `incomplete` before Pin" in convergent_flat
    assert "other nested review lane that invokes this skill" in convergent_flat
    for mode in ("initial", "remediation"):
        assert f"- `{mode}`" in convergent
    assert "valid reviewer quorum" in convergent
    assert "exactly two valid fresh core returns" in convergent
    assert "coordinator never substitutes for a reviewer" in convergent
    assert "no Repair, Lock, or residual-risk acceptance authority" in convergent_flat
    assert "at most one `har-specialist`" in convergent
    assert "at most one fresh unbiased replacement per invalid lane" in convergent
    for agent_id in (
        "har-spec-reviewer",
        "har-standards-reviewer",
        "har-specialist",
    ):
        assert agent_id in convergent
    for overlap in (
        "supported risk",
        "failure and recovery paths",
        "Change Closure",
        "evidence completeness",
    ):
        assert overlap in convergent
    assert not (CUSTOM / "change-review/ADVISORY-CONTRACT.md").exists()


def test_audit_codebase_is_thorough_incremental_html_atlas() -> None:
    skill_dir = CUSTOM / "audit-codebase"
    audit = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    defect = (skill_dir / "DEFECT-CONTRACT.md").read_text(encoding="utf-8")
    quality = (skill_dir / "QUALITY-LENS.md").read_text(encoding="utf-8")
    candidate = (skill_dir / "CANDIDATE-CONTRACT.md").read_text(encoding="utf-8")
    followup = (skill_dir / "CANDIDATE-FOLLOWUP.md").read_text(encoding="utf-8")
    metadata = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    simplification = (skill_dir / "SIMPLIFICATION-LENS.md").read_text(encoding="utf-8")
    report = (skill_dir / "HTML-REPORT.md").read_text(encoding="utf-8")
    report_quick = (skill_dir / "REPORT-QUICK-REFERENCE.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    audit_frontmatter = audit.split("---", 2)[1]

    assert not implicit_policy(skill_dir)
    assert re.findall(
        r"(?m)^## (Map|Audit One Subsystem|Analyze One Candidate|Close One Candidate)$",
        audit,
    ) == ["Map", "Audit One Subsystem", "Analyze One Candidate", "Close One Candidate"]
    assert "$to-tickets" not in audit_frontmatter
    assert "An invalid selection never falls back to Map" in audit
    assert "Never choose the next subsystem or candidate" in audit
    assert "Use only" in audit and "REPORT-QUICK-REFERENCE.md" in audit
    assert "Never open, parse, copy, or edit HTML" in report_quick
    assert "Close is a separate user-selected objective" in audit
    assert "Release decision: none" in audit
    assert "product mutation authority: none" in audit
    assert "next selection authority: user" in audit
    assert (
        "Tracker publication: ready-graph | reused | recovery | authority-required | not-applicable"
        in audit
    )

    for reference in (
        "RELIABILITY-LENS.md",
        "QUALITY-LENS.md",
        "DEFECT-CONTRACT.md",
        "CANDIDATE-CONTRACT.md",
        "HTML-REPORT.md",
        "REPORT-QUICK-REFERENCE.md",
    ):
        assert f"[{reference}]({reference})" in audit
    for reference in (
        "DOMAIN-LENS.md",
        "DESIGN-LENS.md",
        "SIMPLIFICATION-LENS.md",
        "CODING-PRACTICES-LENS.md",
        "PERFORMANCE-LENS.md",
    ):
        assert f"({reference})" in quality
    assert "## Six-Class Coverage" in quality
    assert "| Reliability |" in quality
    assert "| Performance |" in quality
    for lens in ("DOMAIN-LENS.md", "DESIGN-LENS.md", "SIMPLIFICATION-LENS.md",
                 "CODING-PRACTICES-LENS.md", "PERFORMANCE-LENS.md"):
        assert f"({lens})" in quality
    assert "Coverage: complete | incomplete" in quality
    assert "An admitted item does not close class coverage" in quality
    assert "`authority-required`" in audit
    assert "`authority-required`" in followup
    assert "`authority-required|not-applicable`" in candidate
    assert "current-source evidence" in quality
    assert "selected objective's current source identity" in " ".join(defect.split())
    assert "separately user-selected `$audit-codebase` objective" in candidate
    normalized_followup = " ".join(followup.split())
    assert "The helper generates one Implement pickup" in normalized_followup
    assert "exact Close packet" in normalized_followup
    assert "$to-tickets" not in metadata
    assert "helper derives the linked Analyze pickup" in candidate
    assert "conditional To Tickets authority" in candidate
    assert "`schema --objective close --completion-route <route>`" in candidate
    assert "Known Ceiling" in simplification and "Revisit Trigger" in simplification

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    relationships = {
        row["relationship_id"]: row for row in contract["relationships"]
    }
    ticket_edge = relationships["REL-028"]
    assert ticket_edge["verb"] == "Invoke"
    assert ticket_edge["explicit_target_authority"] == "exact-user-approved-packet"
    assert ticket_edge["ordering_impact"] == "callee-before-caller"
    assert "generated candidate Analyze prompt" in ticket_edge["entry_condition"]
    assert "authority-required" in ticket_edge["wrong_condition"]
    assert "Generated To Tickets invocation" in ticket_edge["input_packet"]
    assert "configured tracker mutation" in " ".join(
        ticket_edge["callee_owned_gates_mutations"]
    )
    assert "candidate-bundle-bound ready/reused graph" in ticket_edge["return_packet"]
    assert "verified tracker graph" in relationships["REL-056"]["input_packet"]
    assert "analyzed-candidate closeout" in relationships["REL-047"]["entry_condition"]
    for relationship_id in ("REL-021", "REL-026"):
        packet = relationships[relationship_id]["input_packet"]
        assert "digest-bound current audit report" in packet
        assert "last verified source identity" in packet
    capability = next(
        row for row in contract["capabilities"] if row["capability_id"] == "CAP-017"
    )
    assert "analyzed-candidate closeout" in capability["entry_conditions"][0]
    assert "authority-required" in capability["completion_return"]
    selected_skill = next(
        row for row in contract["selected_skills"] if row["skill_id"] == "SK-017"
    )
    assert "authority-required" in selected_skill["completion_condition"]

    assert "accepts exactly structural version 10" in report
    assert "embedded canonical JSON state" in " ".join(report.split())
    assert "The helper alone owns" in report
    assert "HTML, markup, projections" in report
    for state_token in (
        "mapped",
        "audited",
        "presented",
        "analyzed",
        "implemented",
    ):
        assert state_token in report
    assert "`implemented` is reachable only through `close-candidate`" in " ".join(report.split())

    for command in (
        "schema",
        "inspect",
        "source-identity",
        "inventory",
        "render-report",
        "audit-subsystem",
        "analyze-candidate",
        "close-candidate",
    ):
        assert command in report_quick
    assert "Never open, parse, copy, or edit HTML" in report_quick
    assert re.search(
        r"(?m)^\| A repository needs a whole-system map, one selected subsystem "
        r"audit, one selected audit-candidate analysis, or one selected "
        r"analyzed-candidate closeout \| `\$audit-codebase` \|$",
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

    pin = " ".join(
        convergent.split("## 2. Pin", 1)[1].split("## 3. Review", 1)[0].split()
    )
    for surface in (
        "`HEAD`",
        "index tree",
        "staged diff",
        "unstaged diff",
        "status",
        "untracked path and its bytes",
    ):
        assert surface in pin
    verify = " ".join(convergent.split("## 5. Gate", 1)[1].split())
    assert "every cell of the pinned candidate identity" in verify
    assert "Do not recapture" in verify


def test_implement_selects_one_risk_scaled_review_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_section = implement.split("## Review", 1)[1].split(
        "## Lock And Return", 1
    )[0]
    review_flat = " ".join(review_section.split())
    assert "Stage one exact candidate" in review_flat
    assert "immutable candidate generation" in review_flat
    assert "[Finding Contract](../change-review/FINDING-CONTRACT.md)" in review_section
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in review_section
    assert "exact semantic profile and runtime binding" in review_flat
    assert "candidate-bound route evidence" in review_flat
    assert "`ordinary | release | supported-high-risk` basis" in review_flat
    assert "`ordinary-reviewer` with `$change-review`" in review_flat
    assert "`assurance-coordinator` with `$high-assurance-review`" in review_flat
    assert "distinct from all implementation actor and task IDs" in review_flat
    assert "withhold hypotheses" in review_flat
    assert "transport-invalid" in review_flat
    assert "reselect its route from current facts" in review_flat
    assert "review it under new actor and task IDs" in review_flat
    assert "Never resume a prior review" in review_flat
    assert "`Invocation: formal-delivery`" in review_flat
    assert "`Review mode: remediation`" in review_flat
    assert "Finding Contract's remediation packet" in review_flat
    assert "request staged-only review" in review_flat
    assert "Never unstage foreign work" in review_flat
    assert "Stop when the candidate cannot be isolated" in review_flat
    assert set(
        re.findall(r"`\$(change-review|high-assurance-review)`", review_section)
    ) == {
        "change-review",
        "high-assurance-review",
    }
    assert "ordinary-reviewer" in review_flat
    assert "assurance-coordinator" in review_flat
    assert "Charter, Source Trace, fixed point, candidate, proof," in review_flat
    assert "complete current Return" in review_flat
    assert "runtime binding provenance to match the Runtime Profiles" in review_flat
    assert "automatically opens Repair" in review_flat
    assert "Unless the caller restricts Repair before Freeze" in " ".join(
        implement.split()
    )
    assert "every blocker is `automatic-in-scope`" in review_flat
    assert "Return every other set intact with its exact gap" in review_flat
    for field in (
        "Commit identity and tree:",
        "Proof, skips, and formal-review provenance:",
        "Repair generations:",
        "Changed scope and Change Closure:",
        "Tracker closeout, claim, and frontier:",
        "Residual risk:",
        "Caller-owned next action:",
    ):
        assert field in implement
    assert "do not infer or start caller-owned" in " ".join(implement.split())
    assert "audit-codebase" not in implement.lower()
    assert "report.html" not in implement
    assert "update_report.py" not in implement

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    review_edges = {
        row["relationship_id"]: row
        for row in contract["relationships"]
        if row["relationship_id"] in {"REL-013", "REL-016"}
    }
    assert set(review_edges) == {"REL-013", "REL-016"}
    for row in review_edges.values():
        assert "implementation actor and task identities" in row["input_packet"]
        assert "fresh-task provenance" in row["return_packet"]


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")

    assert (
        'description: \'Test-driven development. Use when the user wants to build '
        'features or fix bugs test-first, mentions "red-green-refactor", or wants '
        "integration tests.'"
    ) in tdd
    assert "Own one inner loop:" in tdd
    assert "The caller owns bounded scope" in tdd
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


def test_tdd_returns_every_outbound_gap_to_its_caller() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")
    refactoring_flat = " ".join(refactoring.split())

    assert "`design-evidence-required`" in tdd
    assert "with the intact facts" in tdd
    assert "to the caller and stop" in tdd
    assert "The caller owns any later route" in refactoring_flat
    for callee in (
        "$audit-codebase",
        "$codebase-design",
        "$diagnosing-bugs",
        "$prototype",
        "$simplify-code",
    ):
        assert callee not in tdd
        assert callee not in refactoring


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
    assert "`diagnosis-required`" in tdd
    assert "$diagnosing-bugs" not in tdd
    assert "expected behavior" in diagnosing_flat
    assert "expected behavior" in tdd_flat
    assert "observed failing result" in tdd
    assert "canonical test owner" in diagnosing_flat
    assert (
        "distinct proof responsibility or necessary failure isolation" in diagnosing_flat
    )
    assert "test-portfolio delta" in diagnosing_flat
    assert "applicable Change Closure" in diagnosing_flat
    assert "intact facts" in tdd_flat


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
    assert "`Spec required: yes`" in " ".join(implement.split())
    assert "`Spec required: yes`" in " ".join(parallel.split())


def test_implementation_workflows_keep_local_proof_owners() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())
    parallel_flat = " ".join(parallel.split())

    assert "tracker and label owners only for tracker-backed work" in implement_flat
    assert "all source-owned commitments unchanged" in implement_flat
    assert "Bind proof to the exact candidate and inputs" in implement_flat
    assert "Rerun only invalidated or repository-required checks" in implement_flat
    assert "each ticket's To Tickets execution profile" in parallel_flat
    assert "Qualify concurrency from semantic ownership" in parallel_flat
    assert "Carry worker proof only while" in parallel_flat
    assert "run only proof invalidated or required by the transition" in parallel_flat
    assert "run final required proof once on drained current `HEAD`" in parallel_flat
    assert "canonical test owner" in implement_flat
    assert "proof-responsibility map" in parallel_flat
    assert "consolidate equivalent campaign-created tests" in parallel_flat


def test_implement_owns_one_plain_worker_handoff_without_a_new_route() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    reference_path = CUSTOM / "implement/references/WORKER-HANDOFF.md"

    assert reference_path.is_file()
    assert "[Plain Worker Handoff](references/WORKER-HANDOFF.md)" in implement
    assert (
        "[implement-owned Plain Worker Handoff]"
        "(../implement/references/WORKER-HANDOFF.md)"
    ) in parallel
    assert "does not invoke `$implement`" in parallel
    assert "ordinary task context, not a schema" in implement
    assert "implement/references/WORKER-HANDOFF.md" in relationships
    assert "plain handoff meaning" in relationships
    assert "WORKER-BRIEF.md" in relationships
    handoff = reference_path.read_text(encoding="utf-8")
    for required in (
        "Ticket and desired outcome",
        "Fixed decisions and relevant context",
        "Acceptance criteria",
        "Owned write scope",
        "Required validation",
        "Stop and escalation conditions",
        "Expected evidence return",
        "completed | partial | blocked",
    ):
        assert required in handoff
    assert "schema" not in handoff.lower()
    assert not (CUSTOM / "implement/scripts/execution_assignment.py").exists()
    assert not (CUSTOM / "implement/references/EXECUTION-ASSIGNMENT.md").exists()
    assert not (CUSTOM / "implement/scripts/executor_capsule.py").exists()
    assert not (CUSTOM / "implement/references/EXECUTOR-CAPSULE.md").exists()
    assert not (CUSTOM / "delegated-execution").exists()


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
    assert "binding floors, preferences, and condition-triggered methods" in (
        normalized["implement"]
    )
    assert "Change Closure" in normalized["implement"]
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

    assert "all source-owned commitments unchanged" in implement_flat
    assert "Freeze one Charter" in implement_flat
    assert "otherwise default to exactly `2`" in implement_flat
    assert "refresh only stale, uncertain, or contradicted evidence" in implement_flat
    assert "Recommend `$to-tickets` only when verified landed" in implement_flat
    assert "Return malformed or unsettled work to its source owner" in implement_flat
    assert "Reuse the canonical test owner" in implement_flat
    assert "Perform Change Closure" in implement_flat

    assert "each ticket's To Tickets execution profile" in parallel_flat
    assert "Tickets remain factual and model-neutral" in parallel_flat
    assert "Missing or contradictory readiness, profile, authority" in parallel_flat
    assert "otherwise use the ledger default" in parallel_flat
    assert "repair_generation_budget = 2" in (
        CUSTOM / "parallel-implement/scripts/run_ledger.py"
    ).read_text(encoding="utf-8")
    assert "A proved same-campaign landing may satisfy campaign readiness" in parallel_flat
    assert "proof-responsibility map" in parallel_flat
    assert "test-portfolio delta" in parallel_flat
    for field in (
        "applicable engineering and domain pointers",
        "current owner",
        "Commitment Boundary, prohibited behavior",
        "applicable Invariants, Trust Boundaries",
        "confirmed authority",
        "proof responsibility",
        "routed engineering contract",
        "return `needs-feedback`",
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
        "finite enumerated claim set",
        "provisionally route each claim",
        "evidence for a definition does not by itself support effectiveness",
        "Do not demote a source solely as secondary",
        "For a legal or policy claim",
        "price basis, availability channel, and date when applicable",
        "For a quantitative claim, record the applicable measurand",
        "For a quantitative method",
        "For any point-in-time claim",
        "depends on target-specific meaning or operation",
        "even when the request does not explicitly ask for a comparison",
        "complete local chain needed for the claim",
        "reread mutable load-bearing surfaces",
        "classify each applicable layer independently",
        "If sufficient applicable evidence for a layer is unavailable",
        "do not substitute evidence from another layer",
        "An evidenced `aligned` or `materially different`",
        "mapping resolution does not determine the packet's terminal status",
        "packet's terminal status",
        "source-supported alignment constraints",
        "Static correspondence supports neither by itself",
        "only explicitly described applicable alternatives",
        "For an admitted packet, always include",
        "a target or repository mapping when applicable",
        "an empirical remainder when applicable",
        "For `not-admitted`, return only the Admission contract",
        "Do not silently replace a required repo-local note",
        "Challenge the strongest plausible answer",
        "Scale counterevidence to answer impact",
        "another credible applicable search lane is unlikely to change the answer",
        "at least one credible independent lane capable of disconfirming",
        "do not capture a repository mutation baseline solely for Research",
        "A direct request comes from the current user",
        "identify every exact missing field",
        "Treat required sources as evidentiary conditions",
        "never block solely on a preference",
        "Use discovery results to refine vocabulary and locate direct sources",
        "Put only public information or caller-approved search terms",
        "use it only within the locked audience, destination, and tool authority",
        "Judge independence against the challenged failure mode",
        "sharing the claim's subject alone does not defeat independence",
        "For a direct admitted request, lead with the answer when `answered`",
        "For a caller invocation, use the complete structured Return contract",
    ):
        assert contract in " ".join(research.split())
    assert research.index("## Output") < research.index("## Verify And Return")
    assert "Return to the caller without deciding its artifact" in research
    assert "starting downstream work" in research


def test_writing_great_skills_keeps_shape_and_relationship_boundary() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    glossary = (skill_dir / "GLOSSARY.md").read_text(encoding="utf-8")
    behavior_evals = (skill_dir / "BEHAVIOR-EVALS.md").read_text(
        encoding="utf-8"
    )
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    normalized_skill = " ".join(skill.split())
    normalized_glossary = " ".join(glossary.split())
    normalized_evals = " ".join(behavior_evals.split())
    normalized_context = " ".join(context.split())

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
    assert re.findall(
        r"^## (Resolve|Trace|Shape|Prune|Prove|Return)$",
        skill,
        flags=re.MULTILINE,
    ) == ["Resolve", "Trace", "Shape", "Prune", "Prove", "Return"]
    assert "read-only proof branch within either operation" in normalized_skill
    assert "not a third operation" in normalized_skill
    assert "exact next-owner handoff" in normalized_skill
    assert "Use steps for ordered actions or state changes" in normalized_skill
    assert "Use gates for cross-cutting checks" in normalized_skill
    assert "condition, passing evidence, and safe failure action" in normalized_skill
    assert "do not defer it to review" in normalized_skill
    assert "Recheck only after a transition could invalidate it" in normalized_skill
    assert "Never report a failed branch complete" in normalized_skill
    assert "weakest load-bearing evidence" in normalized_skill
    assert "every proposed step, field, artifact, view, and check" in normalized_skill
    assert "use the term consistently where the practice must stay salient" in normalized_skill
    assert "Audit complete" in skill and "Author complete" in skill
    assert "## Prune" in skill
    assert all(term in skill for term in (
        "`Keep`",
        "`Collapse`",
        "`Disclose`",
        "`Delete`",
    ))
    assert all(term in glossary for term in (
        "**Leading word:**",
        "**Implicitly invocable:**",
        "**Explicit-only:**",
        "**Description:**",
        "**Branch-only reference:**",
        "**Skill split:**",
        "**Transfer gate:**",
        "**Derived view:**",
    ))
    assert "sharpen that pointer first" in normalized_glossary
    assert "narrowest shared owner" in normalized_glossary
    assert "projection of its owning facts" in normalized_glossary
    assert (
        "one prospective mutation, then validate their agreement before publication"
        in normalized_glossary
    )
    assert "begin any attempt limit only at the effect boundary" in normalized_skill
    assert "read-only proof branch" in normalized_evals
    assert "fresh isolated model executions" in normalized_evals
    assert "parent operation status plus one evaluation decision" in normalized_evals
    assert all(term in normalized_context for term in (
        "leading words",
        "reference loading",
        "skill splitting",
        "transfer gates",
        "derived views",
        "completion",
        "pruning stay inline",
    ))
    assert "fork_turns" not in skill
    assert (
        "bundled system `skill-creator` owns new-package scaffolding and metadata mechanics"
        in relationships
    )
    assert "$writing-great-skills` owns semantic quality" in relationships
    assert all(term in relationships for term in (
        "leading-word",
        "reference-loading",
        "skill-splitting",
        "derived-state",
        "fresh-context counterfactual wording evaluation",
    ))


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


def test_portable_fallback_remains_standalone_from_the_repo_contract() -> None:
    loop = "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock"
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    fallback_flat = " ".join(fallback.split())
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    bootstrap_flat = " ".join(bootstrap.split())

    assert loop in fallback
    assert loop not in contract
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
        "How To Read This Contract",
        "Shared Concepts",
        "Keep Faith With The Work",
        "Shape Code For Understanding",
        "Methods When The Condition Applies",
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
    assert "replace any portable contract owner preamble" in bootstrap_flat
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

    assert "It is not a workflow, checklist, review gate, completion contract" in (
        " ".join(contract.split())
    )
    assert re.findall(r"(?m)^### (.+) — Must$", contract) == [
        "Preserve Commitments And Domain Truth",
        "Make Correctness Robust",
        "Respect Trust And Data Boundaries",
        "Keep Evidence Honest",
        "Practice Stewardship",
    ]
    assert re.findall(r"(?m)^### (.+) — Prefer$", contract) == [
        "Deep Simplicity",
        "Local Readability",
        "Fit Before Novelty",
        "Build Only What Is Needed",
        "Keep Tests Lean And Meaningful",
    ]
    assert re.findall(r"(?m)^### (.+) — Method$", contract) == [
        "Reason Across State Boundaries",
        "Use A Negative Control",
        "Close Displaced Paths",
        "Measure Consequential Claims",
    ]
    for concept in (
        "**Bounded slice:**",
        "**Commitment boundary:**",
        "**Proof seam:**",
        "**Proof lane:**",
        "**Change closure:**",
        "**Residual risk:**",
    ):
        assert concept in contract
    for required in (
        "operational definition or exact authoritative owner",
        "not merely a successful happy path",
        "A focused check proves only its covered slice",
        "Apply YAGNI",
        "Apply DRY to shared meaning and policy",
        "Test count is not a goal",
        "controlled violation fails for the intended reason",
        "measure before claiming improvement",
    ):
        assert required in " ".join(contract.split())
    for foreign_procedure in (
        "## Tight Engineering Spine",
        "## Work State",
        "## Lock",
        "**Git mutation owners.**",
        "Observe RED before GREEN",
        ".tmp/",
        ".scratch/",
    ):
        assert foreign_procedure not in contract


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
            normalized = " ".join(text.split())
            assert "Mutation read-back" in normalized
        elif name == "parallel-implement":
            assert "mutation read-back" in text
            assert "affected-frontier read-back" in text
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
    assert "symbolic child identities" in publish_contract
    assert "publication operation templates" in publish_contract
    assert "bind each returned tracker identity to its symbolic child" in (
        publish_contract
    )
    assert "before any dependent mutation" in publish_contract
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
    assert "existing claim or divergence" in return_contract
    assert "missing or unclear authority for the frozen tracker transition" in (
        return_contract
    )
    assert "source-owned ambiguity remains `source-gap`" in return_contract
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
            "2f009005fbef524e6d43c9d0c104400db94dc138e90a8d231bbfefa2d1b81eeb",
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
                "01b1bb2c254861ae2012e22ce67ec7458c629ad750e5873289068248ab6036f1",
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


def test_git_and_parallel_delivery_roles_stay_out_of_the_shared_contract() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(
        encoding="utf-8"
    )
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for shared in (contract, seed):
        normalized = " ".join(shared.split())
        assert "Git mutation owners" not in normalized
        assert "starting index" not in normalized
        assert "registered worktrees" not in normalized

    assert "lane worker" not in contract
    assert "preserving the starting index and unrelated work" in " ".join(
        implement.split()
    )
    implement_admit = implement.split("## Admit", 1)[1].split("## Execute", 1)[0]
    assert "`scope-mismatch`" in implement_admit
    assert "$parallel-implement" not in implement_admit
    assert "Workers neither widen nor dispatch" in " ".join(parallel.split())


def test_parallel_implement_separates_context_checkout_and_review_ownership() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    lanes = (
        CUSTOM / "parallel-implement/references/AGENT-LANES.md"
    ).read_text(encoding="utf-8")
    profiles = (
        CUSTOM / "parallel-implement/references/RUNTIME-PROFILES.md"
    ).read_text(encoding="utf-8")
    ledger = (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").read_text(
        encoding="utf-8"
    )
    assert re.findall(r"(?m)^## (.+)$", parallel) == [
        "Admit",
        "Freeze",
        "Wave",
        "Land",
        "Review",
        "Lock",
    ]
    run = parallel.split("## Wave", 1)[1].split("## Land", 1)[0]
    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^\*\*(Frontier|Dispatch|Drain)\.\*\*", run)
    ] == ["Frontier", "Dispatch", "Drain"]
    dispatch = run.split("**Dispatch.**", 1)[1].split("**Drain.**", 1)[0]
    assert re.findall(
        r"(?m)^- `([^`]+-worker)`: ", dispatch
    ) == [
        "clear-worker",
        "adaptive-worker",
        "fast-adaptive-worker",
        "demanding-worker",
    ]
    assert "A matching later condition overrides every earlier one" in dispatch
    assert "Give every concurrent writer a distinct helper-created worktree" in " ".join(
        lanes.split()
    )
    admit = parallel.split("## Admit", 1)[1].split("## Freeze", 1)[0]
    admit_flat = " ".join(admit.split())
    assert "one standalone item -> `scope-mismatch`" in admit_flat
    assert "$implement" not in admit
    assert re.findall(r"(?m)^## (.+)$", lanes) == [
        "Prepare",
        "Dispatch",
        "Await",
        "Release",
        "Isolated Worktree",
    ]
    assert "scripts/lane_worktree.py" in lanes
    assert "fresh-context collaboration subagent" in lanes
    assert "transport `subagent-v2`" in lanes
    assert "helper-created worktree" in lanes
    for row in (
        "| `parallel-root` | `current` | `gpt-5.6-sol` | `high` |",
        "| `clear-worker` | `luna_max` | `gpt-5.6-luna` | `max` |",
        "| `adaptive-worker` | `default` | `gpt-5.6-terra` | `xhigh` |",
        "| `fast-adaptive-worker` | `default` | `gpt-5.6-sol` | `medium` |",
        "| `demanding-worker` | `default` | `gpt-5.6-sol` | `high` |",
        "| `serial-integrator` | `default` | `gpt-5.6-sol` | `medium` |",
        "| `ordinary-reviewer` | `default` | `gpt-5.6-sol` | `high` |",
        "| `har-spec-reviewer` | `default` | `gpt-5.6-sol` | `xhigh` |",
    ):
        assert row in profiles
    profiles_flat = " ".join(profiles.split())
    assert "binding is `transport-blocked`" in profiles_flat
    assert "formal-review mismatch is `transport-invalid`" in profiles_flat
    assert (
        "Escalate `serial-integrator` to `high` only for conflicting architectural "
        "intent, cross-module invariants, migrations or compatibility behavior, "
        "security-sensitive boundaries, or a repeated failed correction."
    ) in profiles_flat
    lanes_flat = " ".join(lanes.split())
    assert "Spawn once with those arguments" in lanes_flat
    assert "Dispatch generates writer assignments through [WORKER-BRIEF.md]" in lanes_flat
    assert "Supply observed facts explicitly; the helper derives none of them" in lanes_flat
    assert "record its assignment path and SHA-256 with the observed task and provider receipt" in lanes_flat
    assert "gpt-5.6" not in parallel
    assert "gpt-5.6" not in worker
    assert "gpt-5.6" not in ledger
    assert not (
        CUSTOM / "parallel-implement/references/INTEGRATOR-BRIEF.md"
    ).exists()
    parallel_flat = " ".join(parallel.split())
    assert "The root mechanically lands one accepted commit at a time" in parallel_flat
    assert "For an isolated lane, require a clean integration checkout at the recorded prior `HEAD`" in parallel_flat
    assert "For a serial same-checkout lane, require clean current `HEAD` to equal the returned commit" in parallel_flat
    assert "read back integration `HEAD` and the actual diff" in parallel_flat
    assert "run only proof invalidated or required by the transition" in parallel_flat
    for field in (
        "grounding_and_scope",
        "proof",
        "risk_or_blocker",
        "required_root_action",
        "final_worktree",
    ):
        assert f"`{field}`" in worker
    assert "acceptance-to-evidence mapping" in worker
    assert "$diagnosing-bugs" not in worker
    assert "Do not invoke `$change-review` or `$high-assurance-review`" in " ".join(
        worker.split()
    )
    assert "Never spawn, delegate" in worker
    assert "recorded root checkout but never writes there" in " ".join(worker.split())
    assert "The root never authors implementation, tests, integration corrections, or Review Repair" in (
        " ".join(parallel.split())
    )
    assert "## Start" in ledger
    assert "## Status" in ledger
    assert "## Dispatch" in ledger
    assert "## Apply" in ledger
    assert "## Finish" in ledger
    assert "events.jsonl" in ledger
    assert "derives the ordered graph from it" in " ".join(ledger.split())
    assert "rehashes the frozen tracker snapshot" in " ".join(ledger.split())
    assert "LEDGER.md" in ledger and "generated" in ledger.lower()
    for command_name in ("start", "status", "dispatch", "apply", "finish"):
        assert f"run_ledger.py {command_name}" in ledger
    ledger_script = (
        CUSTOM / "parallel-implement/scripts/run_ledger.py"
    ).read_text(encoding="utf-8")
    assert "validate-state" not in ledger_script
    assert "ASSURANCE_REVIEWER_IDS" in ledger_script
    assert "- ASSURANCE_REVIEWER_IDS" in ledger_script
    assert "assurance_returns" in ledger_script
    assert "residual_risks" in ledger_script
    assert 'review_decision == "scope-mismatch"' in ledger_script

    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    review_flat = " ".join(review.split())
    assert "[Finding Contract](../change-review/FINDING-CONTRACT.md)" in review
    assert "candidate-bound route evidence" in review_flat
    assert (
        "fresh collaboration subagent distinct from every implementation and integration actor"
        in review_flat
    )
    assert "fresh task provenance" in review_flat
    assert "new actor and task identities" in review_flat
    assert "Accept a Review Return only when complete" in review_flat
    assert "candidate passes Review only with no blocker" in review_flat
    assert "If it also mismatches, preserve the candidate and return `partial`" in review_flat
    assert "`Invocation: formal-delivery`" in review_flat
    assert "`Review mode: remediation`" in review_flat
    assert "Finding Contract's remediation packet" in review_flat
    assert "automatically opens Repair" in review_flat
    assert "Unless the caller restricts Repair before Freeze" in parallel_flat
    assert "resume only from its fresh exact-state Return" in parallel_flat
    freeze = parallel.split("## Freeze", 1)[1].split("## Wave", 1)[0]
    assert "caller-supplied residual-risk policy with its identity and evidence" in (
        " ".join(freeze.split())
    )
    assert "absent residual-risk policy means caller-only acceptance" in (
        " ".join(freeze.split())
    )

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    review_edges = {
        row["relationship_id"]: row
        for row in contract["relationships"]
        if row["relationship_id"] in {"REL-030", "REL-034"}
    }
    assert set(review_edges) == {"REL-030", "REL-034"}
    for row in review_edges.values():
        assert "implementation and integration actor identities" in row["input_packet"]
        assert "review actor and fresh-task provenance" in row["return_packet"]


def test_parallel_implement_owns_recovery_authority_and_outcome_gates() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    worker = (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").read_text(
        encoding="utf-8"
    )
    lanes = (
        CUSTOM / "parallel-implement/references/AGENT-LANES.md"
    ).read_text(encoding="utf-8")
    ledger = (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").read_text(
        encoding="utf-8"
    )
    event_types = runpy.run_path(
        str(CUSTOM / "parallel-implement/scripts/run_ledger.py")
    )["EVENT_TYPES"]
    run = parallel.split("## Wave", 1)[1].split("## Land", 1)[0]
    drain = run.split("**Drain.**", 1)[1]
    assert "Accept only a task-lane-matched Return satisfying the Worker Brief" in drain
    assert "`blocker`" in drain
    assert "`done | blocker | needs-feedback`" in worker
    for outcome in ("complete", "partial", "blocked"):
        assert f"`{outcome}`" in parallel
    assert "Return `partial` when safe, already-authorized work remains resumable" in " ".join(parallel.split())
    assert "return `blocked` when progress requires changed external state or new caller authority" in " ".join(parallel.split())
    assert {
        "scope",
        "resume",
        "checkpoint",
        "integration-regression",
        "integration-correction",
        "review-invocation",
        "repair-plan",
        "repair-complete",
    } <= event_types
    assert "## Release" in lanes
    lock = parallel.split("## Lock", 1)[1]
    open_gate = run.split("**Dispatch.**", 1)[1].split("**Drain.**", 1)[0]
    assert "claim" in open_gate
    assert "read back" in parallel.lower()
    assert "closeout plan" in lock and "mutation read-back" in lock
    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    assert "idle" in review


def test_parallel_implement_has_root_receipts_and_lean_worktree_lifecycle() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    ledger = (skill_dir / "references/RUN-LEDGER.md").read_text(encoding="utf-8")
    launch = (skill_dir / "references/AGENT-LANES.md").read_text(
        encoding="utf-8"
    )
    worker = (skill_dir / "references/WORKER-BRIEF.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    script = (skill_dir / "scripts/run_ledger.py").read_text(encoding="utf-8")
    lane_script = (skill_dir / "scripts/lane_worktree.py").read_text(encoding="utf-8")
    codex_config = (ROOT / ".codex/config.toml").read_text(encoding="utf-8")

    assert "Pass only at the top-level root" in parallel
    assert "Return before mutation" in parallel
    assert "repair_generation_budget" in script
    assert "Repair budget" in ledger
    assert "Start -> Status -> Dispatch -> Apply -> Finish" in ledger
    assert "Spawn once" in ledger
    assert "contains no provider-created task identity" in " ".join(ledger.split())
    assert "reviewer" in ledger
    assert "review-invocation" in script
    launch_flat = " ".join(launch.split())
    assert "lane_worktree.py prepare" in launch_flat
    assert "lane_worktree.py cleanup" in launch_flat
    assert "--repo <repo> --root <worktree-root> --base <sha> --name <lane-name>" in launch_flat
    assert "checkout-external pytest temp and cache roots" in launch_flat
    assert "Dirty, not-completed, unintegrated, and uncertain lanes stay preserved" in launch_flat
    assert "--oldest" in launch and "--completed" in launch
    assert 'operations.add_parser("prepare")' in lane_script
    assert 'operations.add_parser("cleanup")' in lane_script
    assert '"--collect-only"' in lane_script
    assert '"addopts="' in lane_script
    assert "shutil.rmtree" not in lane_script
    assert 'cleanup_parser.add_argument("--oldest", action="store_true")' in lane_script
    assert 'cleanup_parser.add_argument("--completed", action="append", default=[])' in lane_script
    assert "project_key" not in lane_script
    assert "project marker" not in lane_script.lower()
    assert "python_provenance" not in lane_script
    assert "proof-command" not in lane_script
    assert "Python provenance" not in ledger
    assert "startup proof" not in ledger
    assert "permanent project key" not in bootstrap
    assert "derived base and lane roots" not in bootstrap
    assert "--global" not in lane_script
    expected_lane_root = str(Path(ROOT.anchor) / "pi" / "pas-001" / "wt")
    encoded_lane_root = expected_lane_root.replace("\\", "\\\\")
    assert f'"{encoded_lane_root}" = true' in codex_config
    assert "runtime contract 7" in ledger.lower()
    assert "reads the repo-local parallel-lane setup" in " ".join(ledger.split())
    assert "integration_regression" in script
    assert "runtime contract 7" in ledger
    assert (skill_dir / "assets/luna_max.toml").read_bytes() == (
        ROOT / ".codex/agents/luna_max.toml"
    ).read_bytes()
    assert "return an owned correction to its current worker" in " ".join(parallel.split())
    assert "integration correction" in worker.lower()
    assert "exact recorded event" in worker
    worker_flat = " ".join(worker.split())
    assert "prior integration `HEAD`" in worker_flat
    assert "write scope" in worker_flat
    assert '"write_scope_ids"' in script
    assert "lane_actor == actor_id" in script
    assert '"prepare"' in script


def test_parallel_implement_exposes_parent_graph_frontier_and_closeout_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    ledger = (skill_dir / "references/RUN-LEDGER.md").read_text(encoding="utf-8")
    ledger_flat = " ".join(ledger.split())
    event_types = runpy.run_path(str(skill_dir / "scripts/run_ledger.py"))["EVENT_TYPES"]
    closeout_fields = runpy.run_path(str(skill_dir / "scripts/run_ledger.py"))[
        "CLOSEOUT_FIELDS"
    ]
    launch = (skill_dir / "references/AGENT-LANES.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(skill_dir)
    assert "recommend `$implement` and stop" not in parallel

    gate = parallel.split("## Wave", 1)[1].split("**Dispatch.**", 1)[0]
    gate_flat = " ".join(gate.split())
    assert "Qualify concurrency" in gate_flat
    assert "downshift uncertain or overlapping work to serial" in gate_flat
    assert "return the exact blockers" in gate_flat

    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    lock = parallel.split("## Lock", 1)[1]
    assert "$change-review" in review
    assert "mutation read-back" in lock
    assert lock.index("child") < lock.index("parent")
    parallel_flat = " ".join(parallel.split())
    lock_flat = " ".join(lock.split())
    assert "claim remains through verified child closeout" in parallel_flat
    assert "verified non-dispatchable closeout" in lock_flat
    assert "affected-frontier read-back" in lock_flat
    assert "release only pre-landing ended claims" in lock_flat.lower()
    assert "named recovery custodian" in lock_flat
    assert "released claims" in ledger_flat
    assert "safe lanes" in ledger_flat

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
        "claim_release",
        "affected_frontier_readback",
    }
    assert {
        "child-closeout",
        "parent-closeout",
    } <= event_types
    assert "serial-frontier" not in event_types
    assert "parallel-frontier" not in event_types
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
        assert "landed-awaiting-lock" not in text, path

    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    for token in (
        "landed-awaiting-lock",
        "same-campaign",
        "through verified child closeout",
        "reblocks dependents",
    ):
        assert token in parallel


def test_state_boundary_reasoning_has_one_owner_and_explicit_consumers() -> None:
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
        "### Reason Across State Boundaries — Method When correctness depends on "
        "cached, persisted, resumed, grouped, projected, distributed, or "
        "session-scoped state"
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
    assert "final required proof once on drained current `HEAD`" in parallel_flat
    assert "cover applicable state-boundary branches" in parallel_flat
    assert "applicable state-boundary matrix" in worker
    assert "return `needs-feedback`" in " ".join(worker.split())
    ledger_flat = " ".join(ledger.split())
    assert "The root supplies decisions; the helper performs deterministic checks" in ledger_flat
    assert "does not choose the frontier, concurrency, worker profile, proof, review, or completion" in ledger_flat


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())

    assert not implicit_policy(CUSTOM / "implement")
    assert "Deliver exactly one caller-selected ready item" in implement_flat
    assert "Keep the named item" in implement_flat
    assert "Do not substitute, split, widen" in implement_flat
    assert "exhaustive parent graph or review-only request intact" in implement_flat
    assert "`scope-mismatch`" in implement_flat
    admit = implement.split("## Admit", 1)[1].split("## Execute", 1)[0]
    assert "$parallel-implement" not in admit

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    edge = next(
        row for row in contract["relationships"] if row["relationship_id"] == "REL-018"
    )
    assert "Verified landed implementation invalidated" in edge["entry_condition"]
    assert "malformed, unsettled, unsliced" in edge["wrong_condition"]


def test_implement_closeout_enters_lock_and_preserves_connector_custody() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())

    assert "Stage one exact candidate" in implement_flat
    assert "preserving the starting index and unrelated work" in implement_flat
    assert "stage exact paths or hunks" in implement_flat
    review_tree = implement_flat.index("Pin the proved tree")
    closeout = implement_flat.index("mechanical Local Markdown closeout")
    lock_tree = implement_flat.index("Lock the reviewed tree")

    assert review_tree < closeout < lock_tree
    assert "Mutation read-back rules" in implement_flat
    assert "Send every other review-to-lock delta through formal review" in implement_flat
    assert "Add only mechanical Local Markdown closeout" in implement_flat
    assert "Create exactly one commit" in implement_flat
    assert "proving `HEAD` unchanged" in implement_flat
    assert "do not retry blindly" in implement_flat
    assert "For GitHub or GitLab, retain the claim through Lock and commit" in implement_flat
    assert "durable non-dispatchability" in implement_flat
    assert "refetch and prove every effect" in implement_flat
    assert "release the claim, then refetch claim absence and the affected frontier" in implement_flat
    assert "post-commit hosted closeout failure, preserve the commit, refetch state" in implement_flat
    assert "Tracker closeout, claim, and frontier: <evidence> | not applicable" in implement
    assert "named recovery custodian" in implement_flat
    assert "early Return before commit, release a claim only after" in implement_flat
    assert "pending mutations are determinate" in implement_flat
    assert "retain or transfer custody" in implement_flat
    assert "closeout and frontier proof finish" in implement_flat


def test_diagnosis_is_an_explicit_leaf_with_bounded_recommendations() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    prototype = (CUSTOM / "prototype/SKILL.md").read_text(encoding="utf-8")
    resolver = (CUSTOM / "resolving-merge-conflicts/SKILL.md").read_text(
        encoding="utf-8"
    )
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    assert (
        'description: \'Diagnosis loop for hard bugs and performance regressions. '
        'Use when the user says "diagnose"/"debug this", or reports something '
        "broken/throwing/failing/slow.'"
    ) in diagnosing
    packet = diagnosing.split("Return one diagnosis packet containing:", 1)[1]
    assert len(re.findall(r"(?m)^- ", packet)) >= 7
    rows = set(
        re.findall(
            r"(?m)^\| `([a-z0-9-]+)` \| (Load|Invoke|Compose|Hand off|Recommend and stop) \| `\$([a-z0-9-]+)` \|",
            relationships,
        )
    )
    assert not implicit_policy(CUSTOM / "diagnosing-bugs")
    assert "Start no successor; any recommendation below remains unstarted" in (
        " ".join(diagnosing.split())
    )
    assert set(re.findall(r"\$[a-z0-9-]+", diagnosing)) == {"$audit-codebase"}
    assert "recommend `$diagnosing-bugs` and stop before mutation" in prototype
    assert "recommend `$diagnosing-bugs`" in resolver
    assert {
        (caller, verb, callee)
        for caller, verb, callee in rows
        if caller == "diagnosing-bugs" or callee == "diagnosing-bugs"
    } == {
        ("prototype", "Recommend and stop", "diagnosing-bugs"),
        ("diagnosing-bugs", "Recommend and stop", "audit-codebase"),
        ("resolving-merge-conflicts", "Recommend and stop", "diagnosing-bugs"),
    }
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }
    assert {
        (names[row["caller_skill_id"]], row["verb"], names[row["target_skill_id"]])
        for row in contract["relationships"]
        if names[row["caller_skill_id"]] == "diagnosing-bugs"
        or names[row["target_skill_id"]] == "diagnosing-bugs"
    } == {
        ("skill-router", "Recommend and stop", "diagnosing-bugs"),
        ("prototype", "Recommend and stop", "diagnosing-bugs"),
        ("diagnosing-bugs", "Recommend and stop", "audit-codebase"),
        ("resolving-merge-conflicts", "Recommend and stop", "diagnosing-bugs"),
    }
    for skill in CUSTOM.iterdir():
        if skill.is_dir() and skill.name not in {
            "diagnosing-bugs",
            "prototype",
            "resolving-merge-conflicts",
            "skill-router",
        }:
            for path in skill.rglob("*.md"):
                assert "$diagnosing-bugs" not in path.read_text(encoding="utf-8")


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
        ("to-questionnaire", "Recommend and stop", "repo-bootstrap"),
        ("to-spec", "Load", "codebase-design"),
        ("wayfinder", "Invoke", "research"),
        ("wayfinder", "Invoke", "prototype"),
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
        ("implement", "Invoke", "change-review"),
        ("implement", "Invoke", "high-assurance-review"),
        ("implement", "Hand off", "resolving-merge-conflicts"),
        ("change-review", "Recommend and stop", "audit-codebase"),
        ("high-assurance-review", "Recommend and stop", "audit-codebase"),
        ("parallel-implement", "Invoke", "high-assurance-review"),
        ("parallel-implement", "Invoke", "resolving-merge-conflicts"),
        ("prototype", "Recommend and stop", "diagnosing-bugs"),
        ("diagnosing-bugs", "Recommend and stop", "audit-codebase"),
        ("resolving-merge-conflicts", "Recommend and stop", "diagnosing-bugs"),
        ("audit-codebase", "Recommend and stop", "domain-modeling"),
        ("audit-codebase", "Recommend and stop", "grill-with-docs"),
        ("audit-codebase", "Recommend and stop", "grilling"),
        ("audit-codebase", "Recommend and stop", "research"),
        ("audit-codebase", "Recommend and stop", "prototype"),
        ("audit-codebase", "Recommend and stop", "to-questionnaire"),
        ("audit-codebase", "Load", "codebase-design"),
        ("audit-codebase", "Recommend and stop", "wayfinder"),
        ("audit-codebase", "Recommend and stop", "to-spec"),
        ("audit-codebase", "Invoke", "to-tickets"),
        ("audit-codebase", "Recommend and stop", "simplify-code"),
        ("audit-codebase", "Recommend and stop", "implement"),
        ("simplify-code", "Recommend and stop", "audit-codebase"),
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
    assert {
        edge for edge in edges if edge[0] == "tdd"
    } == set()
    assert ("audit-codebase", "Invoke", "codebase-design") not in edges
    for removed_edge in (
        ("audit-codebase", "Recommend and stop", "codebase-design"),
        ("research", "Recommend and stop", "codebase-design"),
        ("simplify-code", "Recommend and stop", "codebase-design"),
        ("tdd", "Recommend and stop", "codebase-design"),
    ):
        assert removed_edge not in edges
    assert not any(
        {caller, callee} == {"change-review", "high-assurance-review"}
        for caller, _, callee in edges
    )
    assert not any(
        {caller, callee} == {"implement", "parallel-implement"}
        for caller, _, callee in edges
    )
    assert {
        edge
        for edge in edges
        if edge[1] == "Invoke"
        and edge[2] in {"change-review", "high-assurance-review"}
    } == {
        ("implement", "Invoke", "change-review"),
        ("implement", "Invoke", "high-assurance-review"),
        ("parallel-implement", "Invoke", "change-review"),
        ("parallel-implement", "Invoke", "high-assurance-review"),
    }

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    skill_names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }
    machine_relationships = {
        (
            skill_names[row["caller_skill_id"]],
            row["verb"],
            skill_names[row["target_skill_id"]],
        ): row
        for row in contract["relationships"]
    }
    machine_edges = set(machine_relationships)
    assert not any(
        {caller, callee} == {"change-review", "high-assurance-review"}
        for caller, _, callee in machine_edges
    )
    assert not any(
        {caller, callee} == {"implement", "parallel-implement"}
        for caller, _, callee in machine_edges
    )
    assert {
        edge for edge in edges if "wayfinder" in {edge[0], edge[2]}
    } == {
        edge
        for edge in machine_edges
        if edge[0] != "skill-router" and "wayfinder" in {edge[0], edge[2]}
    }
    assert (
        "to-questionnaire",
        "Recommend and stop",
        "repo-bootstrap",
    ) in machine_edges
    prototype_packet = machine_relationships[
        ("wayfinder", "Invoke", "prototype")
    ]["input_packet"]
    for field in (
        "evidence surface",
        "representative cases",
        "authorized paths and effects",
        "entry point or recipe",
        "finite bound",
        "known limits",
    ):
        assert field in prototype_packet
    questionnaire = machine_relationships[
        ("wayfinder", "Invoke", "to-questionnaire")
    ]
    assert "external Questionnaire prerequisite" in questionnaire["entry_condition"]
    for field in (
        "explicitly authorized durable path",
        "retention owner",
        "answer-return destination",
    ):
        assert field in questionnaire["input_packet"]
    assert ("wayfinder", "Recommend and stop", "to-tickets") not in edges
    assert ("wayfinder", "Recommend and stop", "implement") not in edges
    assert ("to-questionnaire", "Recommend and stop", "grill-with-docs") not in edges
    assert ("research", "Recommend and stop", "to-questionnaire") not in edges

    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    closure = wayfinder.split("## Closure", 1)[1].split("\n## ", 1)[0]
    assert "`$to-spec`" in closure
    assert "settled parent-spec source" in closure
    assert "Never route directly to" in closure
    for forbidden in ("`$to-tickets`", "`$implement`", "`$parallel-implement`"):
        assert forbidden in closure

    skill_names = {skill.name for skill in CUSTOM.iterdir() if skill.is_dir()}
    approved_explicit_invocations = {
        ("audit-codebase", "Invoke", "to-tickets"),
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
