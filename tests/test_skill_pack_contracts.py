from __future__ import annotations

import hashlib
import json
import re
import runpy
from pathlib import Path

import yaml

from scripts import (
    pack_contract,
    skill_pack_contract,
    validate_skills,
)


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"


def exact_tree_hash(directory: Path) -> str:
    files = [
        (name, content)
        for name, (kind, content) in skill_pack_contract.tree_entries(directory).items()
        if kind == "file"
    ]
    digest = hashlib.sha256()
    for name, content in sorted(files, key=lambda item: item[0].encode("utf-8")):
        file_sha256 = hashlib.sha256(content).hexdigest()
        digest.update(f"{name}\t{len(content)}\t{file_sha256}\n".encode("utf-8"))
    return digest.hexdigest()


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

    assert set(routed) | {"repo-bootstrap", "high-assurance-review"} == (
        skill_names - {"skill-router"}
    )
    assert len(routed) == len(set(routed))
    assert "High Assurance Review is an explicit user-selected alternative" in router


def test_handoff_compacts_context_without_advancing_work() -> None:
    skill_dir = CUSTOM / "handoff"
    handoff = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    handoff_flat = " ".join(handoff.split())

    assert not implicit_policy(skill_dir)
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", handoff) == [
        "Qualify",
        "Gather",
        "Write",
        "Check",
        "Return",
    ]
    template = handoff.split("```markdown", 1)[1].split("```", 1)[0]
    assert re.findall(r"(?m)^## (.+)$", template) == [
        "Purpose and boundary",
        "State, decisions, blockers, and authority",
        "Sources and proof",
        "Next action and preconditions",
    ]
    assert "<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>[-<NN>].md" in handoff
    assert "$repo-bootstrap" in handoff
    for contract in (
        "fresh task or context that can read the same work root",
        "Use `/compact` within the same conversation",
        "never overwrite",
        "Treat completed, verified work as inherited evidence",
        "Reference durable truth instead of copying it",
        "Write only the Handoff artifact",
        "ignored when Git applies",
        "verification a precondition for any action that depends on an unverified pointer",
        "remove only incomplete state created by this invocation",
        "refresh state and authority before acting",
    ):
        assert contract in handoff_flat
    assert "Suggested Skills" not in handoff
    assert "not-created" not in handoff


def test_to_questionnaire_owns_one_safe_recipient_artifact() -> None:
    skill_dir = CUSTOM / "to-questionnaire"
    questionnaire = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    questionnaire_flat = " ".join(questionnaire.split())
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")
    grilling_gap = (CUSTOM / "grilling/references/TERMINAL-GAP-ROUTING.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(skill_dir)
    assert re.findall(r"(?m)^\*\*([A-Za-z]+)\.\*\*", questionnaire) == [
        "Boundary",
        "Admit",
        "Define",
        "Gap",
        "Draft",
        "Cover",
        "Save",
        "Verify",
        "Return",
    ]
    for contract in (
        "Grill the send, not the subject.",
        "facts, judgment, or decision authority unavailable from claim-owning sources",
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
        "e660daf7b4e62055998399e3f15f2277f86c8bced907994304e14f4d91cc226f"
    )
    assert (
        "| One external stakeholder holds missing knowledge and needs an async "
        "discovery questionnaire | `$to-questionnaire` |"
    ) in router
    assert "`$to-questionnaire` for an external stakeholder" in " ".join(
        grilling_gap.split()
    )


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
        assert failures == []
        assert wayfinder_failures(text, str(tracker)) == []

    assert "**Campaign snapshot:**" not in trackers[0].read_text(encoding="utf-8")
    assert "GITHUB_CAMPAIGN_SNAPSHOT_TOKENS" not in validator

    hosted = trackers[0].read_text(encoding="utf-8").replace(
        "Blocked: waiting - <gist>", "Blocked: paused - <gist>"
    )
    assert any(
        "Blocked: waiting - <gist>" in item
        for item in wayfinder_failures(hosted, "hosted")
    )
    prose_reworded = trackers[0].read_text(encoding="utf-8").replace(
        "exact return record", "complete return details"
    )
    assert wayfinder_failures(prose_reworded, "hosted") == []

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
    assert "Retain each claim through verified non-dispatchable closeout" in parallel
    assert "Close the parent only after every child verifies" in parallel


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


def test_repo_bootstrap_domain_contract_validates_owned_structure() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["domain_contract_failures"]
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")

    assert check(domain, "docs/agents/domain.md") == []
    reworded = domain.replace("never silently override them", "do not replace them")
    assert check(reworded, "docs/agents/domain.md") == []

    invalid = domain.replace("CONTEXT-MAP.md", "CONTEXT-INDEX.md")
    failures = check(invalid, "docs/agents/domain.md")
    assert failures == [
        "docs/agents/domain.md is missing CONTEXT-MAP.md"
    ]
    assert check(domain, "docs/agents/domain.md") == []


def assert_repo_bootstrap_semantic_contract(
    package_root: Path,
    *,
    profile: str,
) -> None:
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
    marker = validator["PORTABLE_OWNER_MARKER"]
    assert fallback.count(marker) == 1
    partial_adoption = fallback.replace("# Global Codex Instructions", "")
    assert validator["portable_owner_failures"](partial_adoption) == failures
    reworded = fallback.replace(
        "Use this as your global `AGENTS.md` when the skill pack is not installed.",
        "This file supplies global engineering defaults without an installed pack.",
    )
    assert validator["portable_owner_failures"](reworded) == failures
    assert validator["portable_owner_failures"](
        fallback.replace(marker, "")
    ) == []

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
    assert validator["setup_schema_marker_failures"](
        f"```text\n{marker}\n```\n"
    ) == expected_marker_failure

    valid_agents = (
        f"# Repository Instructions\n\n{marker}\n\n"
        "Repository-specific guidance.\n\n"
        "## Commands\n\n- Test: `python -m pytest`\n"
    )
    command_failure = ["AGENTS.md must contain one unfenced ## Commands heading"]
    assert validator["agents_commands_failures"](valid_agents) == []
    assert validator["agents_commands_failures"](
        valid_agents.replace("## Commands", "## Local Commands")
    ) == command_failure
    assert validator["agents_commands_failures"](
        valid_agents.replace("## Commands", "```text\n## Commands\n```")
    ) == command_failure
    assert validator["agents_commands_failures"](
        valid_agents + "\n## Commands\n"
    ) == command_failure

    assert validator["git_root_failures"](ROOT) == []
    assert validator["git_root_failures"](ROOT / "skills") == [
        "Target must be the Git repository root"
    ]


def test_engineering_contract_validation_is_structural_and_causal() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["engineering_contract_failures"]
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")

    assert check(contract, "engineering-contract.md") == []
    for invalid in (
        contract.replace("# Engineering Contract\n", ""),
        contract.replace(
            "# Engineering Contract\n",
            "# Engineering Contract\n\n# Engineering Contract\n",
        ),
        contract.replace(
            "# Engineering Contract\n",
            "```text\n# Engineering Contract\n```\n",
        ),
        contract.replace("<!-- programming-agent-skills setup-file:", "<!-- stale:"),
        contract.replace(
            "<!-- programming-agent-skills setup-file: engineering-contract.md:",
            "<!-- programming-agent-skills setup-file: engineering-contract.md:deadbeefdead -->\n"
            "<!-- programming-agent-skills setup-file: engineering-contract.md:",
        ),
        contract.replace(
            "<!-- programming-agent-skills setup-file:",
            "```text\n<!-- programming-agent-skills setup-file:",
        ).replace(" -->\n\nExplore imaginatively", " -->\n```\n\nExplore imaginatively", 1),
    ):
        assert check(invalid, "engineering-contract.md")

    renamed_outline = contract.replace(
        "## Design Defaults — Prefer", "## Design Guidance"
    ).replace("### Use A Negative Control", "### Exercise A Failing Case")
    assert check(renamed_outline, "engineering-contract.md") == []
    marker = validator["SETUP_FILE_MARKER_RE"].findall(contract)[0]
    assert check(f"# Engineering Contract\n\n{marker}\n", "engineering-contract.md")
    assert check(
        f"# Engineering Contract\n\n{marker}\n\n## Empty\n\n<!-- comment only -->\n",
        "engineering-contract.md",
    )
    assert check(
        f"# Engineering Contract\n\n{marker}\n\n## Empty\n\n"
        "```text\nexample only\n```\n",
        "engineering-contract.md",
    )


def test_repo_bootstrap_accepts_reworded_owner_pointers() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    pointers = validator["AGENT_POINTERS"]
    reworded = "Read these owners when their contracts apply:\n" + "\n".join(
        f"- {pointer}" for pointer in pointers
    )
    failures: list[str] = []
    validator["require_tokens"](reworded, "AGENTS.md", pointers, failures)
    assert failures == []

    failures = []
    validator["require_tokens"](
        reworded.replace("docs/agents/engineering-contract.md", "docs/engineering.md"),
        "AGENTS.md",
        pointers,
        failures,
    )
    assert failures == [
        "AGENTS.md is missing docs/agents/engineering-contract.md"
    ]


def test_outdated_setup_routes_to_repo_bootstrap() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    template = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )

    assert "$repo-bootstrap" in router
    assert "$repo-bootstrap" in template


def test_router_returns_one_exact_skill_or_truthful_none() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    router_flat = " ".join(router.split())
    bootstrap = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )

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
    assert "Skill: <skill-name | none>" in router
    assert "exact unmet routing predicates" in router
    assert "`none` is a terminal abstention, not a recommendation" in router_flat
    assert "never substitute the nearest or weakest route" in router_flat
    assert "not instead of one allowed clarification" in router_flat
    assert "or abstain when no available skill satisfies the exact contract" in router
    assert "one exact route or truthful none" in bootstrap
    assert "it returns one route and stops" not in bootstrap
    assert "truthful `none` when no available skill fits" in readme
    assert "recommends exactly one next skill" not in readme
    selected = next(
        row for row in contract["selected_skills"]
        if row["canonical_name"] == "skill-router"
    )
    capability = next(
        row for row in contract["capabilities"]
        if row["capability_id"] == "CAP-025"
    )
    assert "truthful no-match result" in selected["completion_condition"]
    assert "exact unmet routing predicates" in selected["failure_return"]
    assert "exact skill or none" in selected["return_packet"]
    assert "truthfully return none" in capability["observable_outcome"]
    assert "no-match abstention" in capability["required_authority_mutation"][0]
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
        "standalone explicitly test-first behavior to `$tdd`",
        "ordinary test, integration-test, regression-test, or coverage work to `$implement`",
        "uncertain broken behavior that needs dedicated investigation to `$diagnosing-bugs`",
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
    assert "[DEEPENING.md](DEEPENING.md)" in design
    assert "[DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)" in design
    assert "## 1. Understand" in design


def test_codebase_design_preserves_lean_branch_contracts() -> None:
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")
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
    deepening_flat = " ".join(deepening.split())
    alternatives_flat = " ".join(alternatives.split())

    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", design) == [
        "Understand",
        "Diagnose",
        "Shape",
        "Compare",
        "Recommend",
    ]
    assert "Write the ordinary caller usage first" in design
    assert "dominant reads, writes, and transitions" in design_flat
    assert "phase-shaped modules" in design
    assert "current shape and the simplest credible no-new-seam option" in design_flat
    assert "test double alone does not earn one" in design_flat
    assert "resolve only the applicable lifecycle" in design_flat
    assert "representative allowed and forbidden callers" in design_flat
    assert "a check capable of failing" in design_flat
    assert "Classify only dependencies that can change the design" in deepening
    assert "Do not create a test census" in deepening_flat
    assert "two or more materially different architecture shapes" in alternatives_flat
    assert "simplest no-new-seam option" in alternatives_flat
    assert "Do not return a menu" in alternatives_flat
    assert "Create no separate design packet" in design_flat
    assert not (CUSTOM / "codebase-design/DIRECT-DESIGN.md").exists()
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
    operations = {
        name: (skill_dir / "references" / f"{name.upper()}.md").read_text(
            encoding="utf-8"
        )
        for name in ("chart", "advance", "maintain", "closure", "terminate")
    }
    chart = operations["chart"]
    advance = operations["advance"]
    maintain = operations["maintain"]
    closure = operations["closure"]

    assert not implicit_policy(skill_dir)
    assert "MAP-FORMAT.md#" in wayfinder
    assert re.findall(r"(?m)^## (.+)$", wayfinder) == [
        "Model",
        "Orient",
        "Mutation Gate",
        "Resolver Gate",
        "Reconcile",
        "Return",
    ]
    for name, body in operations.items():
        filename = f"{name.upper()}.md"
        assert f"[{filename}](references/{filename})" in wayfinder
        assert f"selects `{name.title()}`" in body
        assert "Otherwise do not load it." in " ".join(body.split())
        assert f"## {name.title()}" not in wayfinder
    assert "Do not load any unselected operation procedure." in wayfinder
    for earlier, later in (
        ("**Bound.**", "**Admit.**"),
        ("**Admit.**", "**Sweep.**"),
        ("**Sweep.**", "**Approve.**"),
        ("**Approve.**", "**Create.**"),
        ("**Create.**", "**Complete.**"),
    ):
        assert chart.index(earlier) < chart.index(later)
    for earlier, later in (
        ("**Select.**", "**Freeze.**"),
        ("**Freeze.**", "**Resolve.**"),
        ("**Resolve.**", "**Commit.**"),
        ("**Commit.**", "**Complete.**"),
    ):
        assert advance.index(earlier) < advance.index(later)
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
    assert orient_flat.index("Require inspect and read-back") < orient_flat.index(
        "After selecting one operation"
    )
    assert "A no-mutation Return requires none of those mutation capabilities" in orient_flat
    assert "zero-match initial or successor identity" in chart_flat
    assert "Predecessor:" in map_format
    assert "Terminal kind: settled source | terminal decision" in map_format
    assert "a non-conversational resolver" in admit_flat
    assert "return `not-needed`" in admit_flat
    assert "recommend `$implement` for one settled bounded implementation" in admit_flat
    assert "`$to-spec` only when a durable parent decision contract remains useful" in admit_flat
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
    assert chart_flat.index("[MAP-FORMAT.md](../MAP-FORMAT.md)-conforming") < chart_flat.index(
        "Run the Mutation Gate's initial-map exception"
    )
    assert "confirm zero matches" in mutation_flat
    assert "sole created canonical map" in mutation_flat
    assert chart_flat.index("read back identities") < chart_flat.index(
        "wire edges from those identities"
    )
    assert "no ticket outcome" in chart_flat
    assert "no ticket outcome" in " ".join(maintain.split())
    assert "independently selects `Closure`" in closure


def test_wayfinder_prototype_preserves_judgment_and_authority() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    resolver = wayfinder.split("## Resolver Gate", 1)[1].split("## Reconcile", 1)[0]
    resolver_flat = " ".join(resolver.split())
    for contract in (
        "named human judge uses HITL",
        "predeclared objective rule may use AFK",
        "transports named authority evidence",
        "does not create authority",
        "[Prototype fields](MAP-FORMAT.md#prototype-fields)",
    ):
        assert contract in resolver_flat

    chart = (skill_dir / "references/CHART.md").read_text(encoding="utf-8")
    approve = chart.split("4. **Approve.**", 1)[1].split(
        "5. **Create.**", 1
    )[0]
    approve_flat = " ".join(approve.split())
    assert "[MAP-FORMAT.md](../MAP-FORMAT.md)-conforming packet" in approve_flat
    assert "exact map title" in approve_flat
    assert "resolver fields" in approve_flat

    for field in (
        "Judgment: human:",
        "rule: <predeclared objective rule>",
        "Representative evidence:",
        "Run and cleanup:",
    ):
        assert field in map_format
    prototype_fields = map_format.split("### Prototype Fields", 1)[1].split(
        "### Questionnaire Fields", 1
    )[0]
    assert "When `Type: Prototype`, append only" in prototype_fields


def test_wayfinder_routes_by_authority_and_accounts_for_fog() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")
    map_flat = " ".join(map_format.split())
    advance = (skill_dir / "references/ADVANCE.md").read_text(encoding="utf-8")
    maintain = (skill_dir / "references/MAINTAIN.md").read_text(encoding="utf-8")
    closure = (skill_dir / "references/CLOSURE.md").read_text(encoding="utf-8")

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
    assert "only after the user approves its [Questionnaire fields]" in resolver_flat
    assert "`Questionnaire ready` is Waiting, never an answer" in resolver_flat
    assert "supported map use, scope, exact state, Source Trace" in resolver_flat
    assert "Task" in resolver_flat and "no durable mutation" in resolver_flat
    for pointer in (
        "[Research fields](MAP-FORMAT.md#research-fields)",
        "[Prototype fields](MAP-FORMAT.md#prototype-fields)",
        "[Questionnaire fields](MAP-FORMAT.md#questionnaire-fields)",
    ):
        assert pointer in resolver
    for field in (
        "Resolution owner:",
        "Resolver:",
        "Expected return:",
        "Re-entry owner: $wayfinder",
        "Type: Research | Prototype | Diagnosis | Grilling | Questionnaire | Task",
    ):
        assert field in map_format
    research_fields = map_format.split("### Research Fields", 1)[1].split(
        "### Prototype Fields", 1
    )[0]
    questionnaire_fields = map_format.split("### Questionnaire Fields", 1)[1].split(
        "## Resolution Comment", 1
    )[0]
    assert "When `Type: Research`, append only" in research_fields
    assert "When `Type: Questionnaire`, append only" in questionnaire_fields
    assert "Research note path and write mode:" not in map_format.split(
        "### Research Fields", 1
    )[0]
    assert "Questionnaire packet and approval:" not in map_format.split(
        "### Questionnaire Fields", 1
    )[0]

    advance_flat = " ".join(advance.split())
    resolve = advance.split("3. **Resolve.**", 1)[1].split("4. **Commit.**", 1)[0]
    resolve_flat = " ".join(resolve.split())
    assert "exclusively claim and read back the ticket" in resolve_flat
    assert "Waiting or Blocked ticket" in advance_flat
    assert "validating the attributable return" in advance_flat
    assert "acquire the map claim with the same token" in advance_flat
    assert "no tracker outcome or map mutation" in resolver_flat
    assert "frozen-boundary resolver effects" in resolver_flat
    assert "release both claims, prove absence, and Orient" in advance_flat
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

    reconcile = wayfinder.split("## Reconcile", 1)[1].split("## Return", 1)[0]
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

    maintain_flat = " ".join(maintain.split())
    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", maintain) == [
        "Bound",
        "Apply",
        "Reconcile",
        "Complete",
    ]
    assert "no resolver judgment or ticket outcome" in maintain_flat
    assert "Mutation Gate with the map claim" in maintain_flat
    assert "proved wait or blocker transition" in maintain_flat
    assert "fog trigger that now makes its question sharp" in maintain_flat
    assert "approval only to increase the allowance" in maintain_flat

    closure_flat = " ".join(closure.split())
    assert "independently selects `Closure` from `closeable` state" in closure_flat
    assert "Hold no claim" in closure_flat
    assert "invoke `$domain-modeling` once" in closure_flat
    assert "unaccounted durable-language or ADR consequence" in closure_flat
    assert "`persist authorized` only with exact domain-write authority" in closure_flat
    assert "`render only` otherwise" in closure_flat
    assert "it is not itself a blocker" in closure_flat
    assert "separately material blocker leaves the map open" in closure_flat
    assert "route-closing condition" in closure_flat
    assert "newly sharp gap as exact Maintain input" in closure_flat
    assert "creates and wires its ticket within the approved allowance" in closure_flat
    assert "Build [MAP-FORMAT.md](../MAP-FORMAT.md#closing-packet)'s closing packet" in closure_flat
    assert closure_flat.index("post the packet") < closure_flat.index(
        "close as `delivered`"
    )
    assert closure_flat.index("close as `delivered`") < closure_flat.index(
        "read back closed state and empty frontier"
    )
    assert "one settled bounded implementation" in closure_flat
    assert "durable parent decision contract" in closure_flat
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
    grilling_gap = (CUSTOM / "grilling/references/TERMINAL-GAP-ROUTING.md").read_text(
        encoding="utf-8"
    )
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
    assert "Status: Confirmed" not in grill_docs
    assert "current Grilling understanding or intact gap" in " ".join(
        grill_docs.split()
    )
    assert "declared return owner, or the user on direct invocation" in " ".join(
        grill_docs.split()
    )
    assert (
        "either the confirmed understanding or intact gap plus the current "
        "Domain Delta, or the concrete composition blocker"
        in " ".join(grill_docs.split())
    )
    assert "When active `$wayfinder` is the return owner" in grilling_gap
    for contract in (
        "each settled material answer to Domain Modeling",
        "every returned collision or blocker to Grilling",
        "never merge or reinterpret it",
        "A material Domain Delta blocker prevents a confirmed combined result",
        "return that blocker, its owner, and re-entry condition",
        "Preserve an originating Grilling gap and its owner",
    ):
        assert contract in " ".join(grill_docs.split())

    grill_docs_synthesis = (
        ROOT / "docs" / "synthesis" / "skills" / "grill-with-docs.md"
    ).read_text(encoding="utf-8")
    assert "They are historical, not current instructions" in grill_docs_synthesis
    assert "# Layer Two: Historical Normative Design" in grill_docs_synthesis


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
    assert domain.count("Reconcile proposed material") == 1
    assert (
        "Within one context, its local model owns canonical meaning. Across "
        "contexts, preserve independent meanings unless an explicit "
        "relationship contract or Shared Kernel says otherwise."
    ) in context_format_flat
    assert context_format.count("routed current records") == 1
    assert "executable procedures or algorithm specifications" in context_format_flat
    adr_format = (CUSTOM / "domain-modeling/ADR-FORMAT.md").read_text(
        encoding="utf-8"
    )
    adr_format_flat = " ".join(adr_format.split())
    assert domain.count("(./ADR-FORMAT.md)") == 1
    assert "`superseded by ADR-NNNN`" in adr_format
    assert "- **Applicability:**" in adr_format
    assert "all partial-successor links" in adr_format_flat
    assert "algorithm choice" in adr_format_flat
    assert "executable algorithm specification" in adr_format_flat
    root_context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    assert "Reconcile proposed material with routed current records" not in root_context
    assert "partial-successor links" not in root_context


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
    skill_dir = CUSTOM / "grilling"
    grilling = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    gap = (skill_dir / "references/TERMINAL-GAP-ROUTING.md").read_text(
        encoding="utf-8"
    )
    grilling_plain = " ".join(grilling.replace("**", "").split())
    gap_plain = " ".join(gap.split())

    assert re.findall(r"(?m)^## \d+\. ([A-Za-z ]+)$", grilling) == [
        "Bound",
        "Learn",
        "Grill",
        "Confirm and return",
    ]
    for contract in (
        "decision frontier",
        "highest-leverage decision",
        "blocked branch pause only its dependents",
        "trace real callers and existing constraints",
        "not material without a reachable consequence",
        "Never repeat an unchanged question",
        "explicit choice also confirms the understanding",
        "Stop without selecting or starting downstream work",
    ):
        assert contract in grilling_plain
    assert "(references/TERMINAL-GAP-ROUTING.md)" in grilling
    assert "Otherwise do not load it." in grilling_plain
    for contract in (
        "several interdependent unresolved decisions",
        "When active `$wayfinder` is the return owner",
        "recommend uninvoked `$wayfinder`",
        "Choose `$research` when claim-owning sources can answer",
        "original decision owner",
        "Preserve the gap identity across the detour",
        "preserve the evidence or decision owner",
        "add uninvoked `$handoff` only as transport",
        "Handoff neither answers nor owns the gap",
    ):
        assert contract in gap_plain
        assert contract not in grilling_plain
    assert "$to-spec" not in grilling
    assert "$to-spec" not in gap
    assert "Spec source:" not in grilling
    assert "Interview relentlessly" not in grilling
    assert "Relay" not in grilling
    assert "diagnosis-required" not in gap


def test_prototype_preserves_lean_evidence_and_branch_gates() -> None:
    skill_dir = CUSTOM / "prototype"
    prototype = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    prototype_flat = " ".join(prototype.split())
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    logic_flat = " ".join(logic.split())
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    ui_flat = " ".join(ui.split())
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")
    measure_flat = " ".join(measure.split())
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    audit_followup = (
        CUSTOM / "audit-codebase/CANDIDATE-FOLLOWUP.md"
    ).read_text(encoding="utf-8")
    pack = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    prototype_followup = next(
        relationship
        for relationship in pack["relationships"]
        if relationship["relationship_id"] == "REL-020"
    )

    assert re.findall(r"(?m)^## \d+\. (.+)$", prototype) == [
        "Frame",
        "Choose",
        "Build",
        "Observe and decide",
        "Clear and return",
    ]
    for contract in (
        "one unsettled design choice",
        "If the answer needs human judgment, name the judge",
        "objective rule before observing results",
        ".tmp/prototype/<question-slug>/",
        "authority for the allowed paths and effects is present and verified",
        "A caller packet transports authority; it does not create it",
        "Read only the branch that owns the needed evidence",
        "[MEASURE.md](MEASURE.md)",
        "smallest artifact that could change the answer",
        "Source inspection and a successful start are not a verdict",
        "no unauthorized or live Prototype state remains",
        "recommend `$diagnosing-bugs` and stop before mutation",
        "Start no downstream work",
    ):
        assert contract in prototype_flat

    for removed in (
        "[RESUME.md](RESUME.md)",
        "$handoff",
        "$domain-modeling",
        "status: answered | awaiting-verdict | blocked | not-admitted",
    ):
        assert removed not in prototype

    assert "happy, boundary, and rejected behavior" in logic_flat
    assert "Repeated deterministic runs should agree" in logic_flat
    assert "Omitting links does not prove production isolation" in ui_flat
    assert "one representative UI" in ui_flat
    assert "two or three structurally different variants" in ui_flat
    assert "actual browser or target UI" in ui_flat
    assert "Do not report only the best run" in measure_flat
    assert "does not diagnose an unexplained slowdown" in measure_flat
    unresolved = "unresolved runnable-evidence question"
    assert unresolved in relationships
    assert unresolved in audit_followup
    assert unresolved in prototype_followup["entry_condition"]


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    formal = (CUSTOM / "change-review/references/FORMAL-REVIEW.md").read_text(
        encoding="utf-8"
    )
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    review_summary = (
        ROOT / "docs/synthesis/skills/change-review.md"
    ).read_text(encoding="utf-8")
    assurance_summary = (
        ROOT / "docs/synthesis/skills/high-assurance-review.md"
    ).read_text(encoding="utf-8")

    assert re.search(r"(?m)^name: change-review$", review)
    assert re.search(r"(?m)^name: high-assurance-review$", convergent)
    assert "$high-assurance-review" not in review
    review_flat = " ".join(review.split())
    formal_flat = " ".join(formal.split())
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", review) == [
        "Pin",
        "Understand",
        "Inspect",
        "Verify",
        "Return",
    ]
    assert "Otherwise do not load it" in review_flat
    assert "A whole-repository or subsystem baseline audit is outside" in review_flat
    assert "Review the captured candidate, not a later version" in review_flat
    assert "another agent's report" in review_flat
    assert "An empty review is valid" in (
        CUSTOM / "change-review/FINDING-CONTRACT.md"
    ).read_text(encoding="utf-8")
    assert "model choice and runtime transport are not review evidence" in formal_flat
    assert "fresh task or context" in formal_flat
    assert "distinct from every implementation and integration author" in formal_flat
    assert "pass with residual risk" in formal
    assert "Accept only when the user explicitly names" in convergent
    assert "explicitly user-selected immutable candidate" in assurance_summary
    assert "No workflow selects High-Assurance Review automatically" in assurance_summary
    assert not (CUSTOM / "change-review/SMELL-BASELINE.md").exists()
    assert "formal review" in review_summary.lower()
    assert "Implementation-worker profiles remain with implementation dispatch" in review_summary


def test_spawned_agents_share_one_runtime_profile_owner() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    profiles = (
        CUSTOM / "parallel-implement/references/RUNTIME-PROFILES.md"
    ).read_text(
        encoding="utf-8"
    )
    profiles_flat = " ".join(profiles.split())

    assert re.findall(
        r"(?m)^\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|$",
        profiles,
    ) == [
        ("clear-worker", "luna_max", "gpt-5.6-luna", "max"),
        ("adaptive-worker", "default", "gpt-5.6-terra", "xhigh"),
        ("fast-adaptive-worker", "default", "gpt-5.6-sol", "medium"),
        ("demanding-worker", "default", "gpt-5.6-sol", "high"),
    ]
    assert "A named agent type loads its custom TOML" in profiles_flat
    assert "Enforce a row only for a spawned implementation actor" in profiles_flat
    assert "public interface, cross-owner invariant" in profiles_flat
    assert "Review roles use their owning review skill's fresh-context" in profiles_flat
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in implement
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" not in review
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" not in assurance
    assert "passes it directly when starting the worker" in profiles_flat
    assert "If the user explicitly requests subagents" in implement_flat
    assert "delegate only a bounded edit that one worker can own" in implement_flat
    assert "Luna/max `clear-worker`" not in implement
    assert not (CUSTOM / "parallel-implement/scripts/run_ledger.py").exists()
    custom_agents = sorted((ROOT / ".codex/agents").glob("*.toml"))
    assert [path.name for path in custom_agents] == ["luna_max.toml"]
    luna = custom_agents[0].read_text(encoding="utf-8")
    assert 'model = "gpt-5.6-luna"' in luna
    assert 'model_reasoning_effort = "max"' in luna
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
    finding_flat = " ".join(finding.split())

    assert re.findall(r"(?m)^- \*\*([^*]+):\*\*", finding) == [
        "Anchor",
        "Reach",
        "Evidence",
        "Impact",
        "Proportion",
    ]
    assert re.findall(r"(?m)^- `(P[0-3])`", finding) == ["P0", "P1", "P2", "P3"]
    assert "stable ID when a later formal remediation review may occur" in finding_flat
    for removed in (
        "automatic-in-scope",
        "decision-required",
        "residual-hardening",
        "Supported risk trigger:",
        "Blocking:",
    ):
        assert removed not in finding
    for skill in (review, convergent):
        assert "FINDING-CONTRACT.md" in skill


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

    for contract in (
        "accepted requirement, repository rule, or supported behavior",
        "concrete scenario inside the selected change",
        "direct evidence from the reviewed candidate",
        "correctness, contract, data, operability, proof, or maintainability",
        "smallest required correction or proof",
    ):
        assert contract in finding_flat
    assert "preference-only" in finding_flat
    assert "reviewer agreement does not establish a finding" in finding_flat
    assert "Reuse proof bound to the candidate" in review
    assert "Reuse exact-snapshot proof" in convergent_flat
    assert "FINDING-CONTRACT.md" in convergent
    assert "neither required nor sufficient for invocation" in convergent_flat
    assert "supported-risk candidate needs read-only judgment" in router
    assert "High Assurance Review is an explicit user-selected alternative" in router


def test_review_assurance_route_has_one_domain_decision() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    normalized_context = " ".join(context.split())
    prior_adr = (
        ROOT / "docs/adr/0015-independent-change-review-is-condition-triggered.md"
    ).read_text(encoding="utf-8")
    adr = (
        ROOT / "docs/adr/0016-ordinary-and-formal-review-share-one-lean-judgment-owner.md"
    ).read_text(encoding="utf-8")
    normalized_adr = " ".join(adr.split())

    for term in (
        "**Change review candidate**",
        "**High-assurance review candidate**",
        "**Supported high-risk trigger**",
    ):
        assert context.count(term) == 1
    assert "ADR-0016" in context
    assert "The caller owns activation" in normalized_context
    assert "each review skill validates its admitted candidate" in normalized_context
    assert "risk expands only applicable candidate-scoped judgment" in normalized_context
    assert "**Status**: superseded by ADR-0016" in prior_adr
    assert "**Status**: accepted" in adr
    normalized_prior_adr = " ".join(prior_adr.split())
    assert "Supported facts expand ordinary candidate-scoped coverage" in normalized_prior_adr
    assert "Candidate size, PR or release packaging" in normalized_prior_adr
    assert "Missing required proof stops the work" in normalized_prior_adr
    assert "High Assurance Review remains explicit-only" in normalized_adr
    assert "semantic roles, not model or reasoning assignments" in normalized_adr
    superseded = (
        ROOT / "docs/adr/0011-review-assurance-follows-release-risk.md"
    ).read_text(encoding="utf-8")
    assert "superseded by ADR-0013" in superseded


def test_high_assurance_review_uses_fresh_context_and_root_only_fanout() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert (
        "exactly two direct core reviewer lanes as fresh read-only collaboration subagents"
        in " ".join(convergent.split())
    )
    assert "Record each lane's actor and task IDs" in convergent
    contract = (
        convergent.split("return contract:", 1)[1]
        .split("```text", 1)[1]
        .split("```", 1)[0]
    )
    assert set(re.findall(r"(?m)^([a-z ]+):", contract)) == {
        "status",
        "lane",
        "axis",
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

    assert "top-level root of its review run" in convergent_flat
    assert "semantic assurance coordinator" in convergent_flat
    assert "nested review lane that invokes this skill returns `incomplete` before Pin" in convergent_flat
    assert "other nested review lane that invokes this skill" in convergent_flat
    for mode in ("initial", "remediation"):
        assert f"- `{mode}`" in convergent
    assert "valid reviewer quorum" in convergent
    assert "exactly two valid fresh core returns" in convergent
    assert "coordinator never substitutes for a reviewer" in convergent
    assert (
        "no Repair, candidate acceptance or closeout, or residual-risk acceptance authority"
        in convergent_flat
    )
    assert "at most one `har-specialist`" in convergent
    assert "explicitly names one bounded specialist objective" in convergent_flat
    assert "Supported risk alone never selects a specialist" in convergent_flat
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
        "complete replacement or removal",
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
    assert "Coverage: complete | incomplete" in quality
    assert "An admitted item does not close class coverage" in quality
    assert "`authority-required`" in audit
    assert "`authority-required`" in followup
    assert "`authority-required|not-applicable`" in candidate
    assert "selected objective's current source identity" in " ".join(defect.split())
    assert "separately user-selected `$audit-codebase` objective" in candidate
    normalized_followup = " ".join(followup.split())
    assert "The helper generates one Implement pickup" in normalized_followup
    assert "exact Close packet" in normalized_followup
    assert "$to-tickets" not in metadata
    assert "helper derives the linked Analyze pickup" in candidate
    assert "conditional To Tickets authority" in candidate
    assert "`schema --objective close --completion-route <route>`" in candidate

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

def test_high_assurance_review_returns_a_caller_usable_decision() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    formal = (
        CUSTOM / "change-review/references/FORMAL-REVIEW.md"
    ).read_text(encoding="utf-8")
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
    formal_decision_section = formal.split("return exactly one decision", 1)[1].split(
        "## Return", 1
    )[0]
    for section in (formal_decision_section, decision_section):
        assert section.index("- `blocked`") < section.index("- `incomplete`")
        assert "blocker takes precedence over unrelated" in section
    formal_flat = " ".join(formal.split())
    for field in (
        "prior formal Return and candidate identity",
        "fixed successor identity",
        "exact repair delta",
        "all carried IDs",
        "remaining acceptance",
    ):
        assert field in formal_flat
    assert "partial remediation packet is `incomplete`" in formal_flat
    ledger_sentence = convergent.split("and one state:", 1)[1].split(".", 1)[0]
    ledger_states = set(re.findall(r"`([^`]+)`", ledger_sentence))
    assert ledger_states == {"candidate", "accepted", "rejected", "duplicate", "disputed"}


def test_audit_close_owns_raw_review_admission() -> None:
    candidate = (CUSTOM / "audit-codebase/CANDIDATE-CONTRACT.md").read_text(
        encoding="utf-8"
    )
    quick = (CUSTOM / "audit-codebase/REPORT-QUICK-REFERENCE.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(candidate.split())

    assert "raw decision and provenance" in normalized
    assert "`pass` is admissible" in candidate
    assert "`pass with residual risk` is admissible only" in candidate
    assert "`blocked` is inadmissible" in candidate
    assert "`incomplete` is inadmissible" in candidate
    assert "formal_review_residual_risk_acceptance" in candidate
    assert "former synthetic `accepted` value remain readable as legacy state" in normalized
    assert "New Close manifests cannot supply or persist it" in normalized
    assert "returned accepted" not in normalized
    assert "admits `pass with residual risk` only with that evidence" in " ".join(
        quick.split()
    )


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


def test_implement_uses_condition_triggered_change_review() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = implement.split("## 4. Prove", 1)[1].split("## 5. Finish", 1)[0]
    flat = " ".join(review.split())

    assert "user or repository requires independent review" in flat
    assert "two or more independent authors" in flat
    assert "material shared-contract or irreversible-migration judgment" in flat
    assert "freeze the proved candidate" in flat
    assert "fresh `ordinary-reviewer`" in flat
    assert "`Formal review: yes`" in flat
    assert "`Mode: initial`" in flat
    assert "`Mode: remediation`" in flat
    assert "required proof and material skips" in flat
    assert "fresh task or context" in flat
    assert "Do not finish from `blocked` or `incomplete`" in flat
    assert "caller accepts the named risk" in flat
    assert "Review grants no authority to widen scope" in flat


def test_review_policy_is_consistent_across_delivery_metadata() -> None:
    implement = yaml.safe_load(
        (CUSTOM / "implement/agents/openai.yaml").read_text(encoding="utf-8")
    )
    parallel = yaml.safe_load(
        (CUSTOM / "parallel-implement/agents/openai.yaml").read_text(
            encoding="utf-8"
        )
    )
    assurance = yaml.safe_load(
        (CUSTOM / "high-assurance-review/agents/openai.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert "Use heavier workflows only when their stated condition applies" in (
        implement["interface"]["default_prompt"]
    )
    assert "Change Review only when its trigger applies" in (
        parallel["interface"]["default_prompt"]
    )
    assert assurance["policy"]["allow_implicit_invocation"] is False
    assert assurance["interface"]["default_prompt"].startswith("Explicitly use")


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")
    mocking = (CUSTOM / "tdd/mocking.md").read_text(encoding="utf-8")

    description = tdd.split("---", 2)[1]
    assert "explicitly requests TDD" in description
    assert "repository policy requires TDD" in description
    assert "integration tests" in description
    assert "alone do not trigger it" in description
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
    assert "existing behavior test, case table, or contract suite" in tdd
    assert "Add a test only when the tracer has a distinct proof" in tdd
    return_fields = set(
        re.findall(
            r"(?m)^- \*\*([^*]+):\*\*",
            tdd.split("## 5. RETURN", 1)[1],
        )
    )
    assert return_fields == {
        "Source Trace",
        "RED",
        "GREEN",
        "Test portfolio",
        "Coverage",
        "Refactor",
        "Residual risk",
    }
    tests_flat = " ".join(tests.split())
    assert "Independent:" in tests and "not the implementation under test" in tests_flat
    assert "establishes actuality, not correctness" in tests_flat
    assert "broad or combinatorial domain" in tests_flat
    assert "Otherwise prefer focused examples or an exhaustive small table" in tests_flat
    assert mocking.index("1. Real in-process code") < mocking.index(
        "2. Local substitute"
    )
    mocking_flat = " ".join(mocking.split())
    assert "otherwise record the unverified fidelity risk" in mocking_flat
    assert "Reconsider the seam when fidelity is unclear" in mocking_flat


def test_tdd_invocation_gate_is_consistent_across_active_owners() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    engineering = (
        ROOT / "docs/agents/engineering-contract.md"
    ).read_text(encoding="utf-8")
    projected = (
        CUSTOM / "repo-bootstrap/engineering-contract.md"
    ).read_text(encoding="utf-8")
    portable = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")

    assert implicit_policy(CUSTOM / "tdd")
    for owner in (tdd, implement, parallel, router, relationships):
        assert "explicit" in owner.lower()
        assert "repository policy" in owner.lower()
    assert "integration tests, regression tests, or coverage alone do not trigger" in tdd
    assert "TRACE owns finding or creating" in " ".join(tdd.split())
    assert "Otherwise implement directly and use ordinary tests" in " ".join(
        implement.split()
    )
    assert "never runs a second TDD loop" in " ".join(parallel.split())
    assert "Ordinary bug investigation stays with the worker" in parallel
    assert "`diagnosis-required` to the root" in parallel
    assert "resumes implementation only from a complete TDD proof" in " ".join(
        parallel.split()
    )
    assert "stops that lane before behavior mutation" in " ".join(parallel.split())
    assert (
        "ordinary test, integration-test, regression-test, or coverage work to "
        "`$implement`"
    ) in " ".join(router.split())
    assert "TDD only when the user explicitly requests" in engineering
    assert "TDD only when the user explicitly requests" in projected
    assert "only when the user explicitly requests it or repository policy requires it" in " ".join(
        portable.split()
    )

    skill = next(
        row for row in contract["selected_skills"] if row["canonical_name"] == "tdd"
    )
    assert skill["invocation_mode"] == "implicit"
    assert "explicitly requests TDD" in skill["positive_entry_predicate"]
    assert "independent oracle are settled" in skill["positive_entry_predicate"]
    assert "does not explicitly require TDD" in skill["negative_exclusion_predicates"][0]

    names = {
        row["skill_id"]: row["canonical_name"] for row in contract["selected_skills"]
    }
    inbound = {
        (row["relationship_id"], names[row["caller_skill_id"]], row["verb"]): row
        for row in contract["relationships"]
        if names[row["target_skill_id"]] == "tdd"
    }
    assert set(inbound) == {
        ("REL-017", "implement", "Invoke"),
        ("REL-035", "parallel-implement", "Invoke"),
        ("REL-064", "skill-router", "Recommend and stop"),
    }
    for relationship in inbound.values():
        assert "requires TDD" in relationship["entry_condition"]
        assert "independent oracle" in relationship["entry_condition"]
        if relationship["verb"] == "Invoke":
            assert "TRACE owns harness readiness" in relationship["entry_condition"]
        assert "asks only for tests" in relationship["wrong_condition"]


def test_tdd_returns_every_outbound_gap_to_its_caller() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")
    refactoring_flat = " ".join(refactoring.split())

    assert "`design-evidence-required`" in tdd
    assert "with the intact facts" in tdd
    assert "to the caller and stop" in tdd
    tdd_flat = " ".join(tdd.split())
    assert "no hard failure requires diagnosis" in tdd_flat
    assert "RED would encode an unmade design decision" in tdd_flat
    assert (
        "no single accepted behavior and independent oracle yet decide" in tdd_flat
    )
    for field in (
        "settled source, constraints, and non-diagnostic facts",
        "exact unresolved design question and live alternatives",
        "decision owner and return owner",
        "discriminating cases, observation, and verdict criteria",
        "why an implementation RED cannot answer",
    ):
        assert field in tdd_flat
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
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    simplify = next(
        selected
        for selected in contract["selected_skills"]
        if selected["canonical_name"] == "simplify-code"
    )

    assert not implicit_policy(skill_dir)
    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^## \d+\. (.+)$", skill)
    ] == ["Understand", "Choose", "Simplify", "Prove and return"]
    assert simplify["invocation_mode"] == "explicit-only"
    assert simplify["relationship_ids"] == []
    assert {
        relationship["caller_skill_id"]
        for relationship in contract["relationships"]
        if relationship["target_skill_id"] == simplify["skill_id"]
    } == {"SK-017", "SK-025"}
    assert all(
        relationship["caller_skill_id"] != simplify["skill_id"]
        for relationship in contract["relationships"]
    )
    for old_contract in (
        "until-clean",
        "finite positive successful-cut budget",
        "successful-cut ledger",
        "Known Ceiling",
        "Revisit Trigger",
        "Return exactly one outcome",
        "staged-state shape",
        "complete applicable inspection",
    ):
        assert old_contract not in skill


def test_codebase_design_bounds_replacement_and_compatibility() -> None:
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(design.split())

    assert "retain, delete, inline, merge, deepen, replace" in flat
    assert "actual dependents and intended behavior are traceable" in flat
    assert "real interface provides parity proof" in flat
    assert "named compatibility or migration need" in flat


def test_bug_routing_is_disjoint_and_non_bouncing() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    diagnosing_flat = " ".join(diagnosing.split())
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tdd_flat = " ".join(tdd.split())
    tdd_tests = (CUSTOM / "tdd/tests.md").read_text(encoding="utf-8")

    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^## \d+\. ([A-Za-z]+)$", diagnosing)
    ] == ["Reproduce", "Discriminate", "Resolve", "Return"]
    assert "[SKILL.md](SKILL.md)" in tdd_tests
    assert "`diagnosis-required`" in tdd
    assert "$diagnosing-bugs" not in tdd
    assert "observed failing result" in tdd
    assert "Ordinary bug investigation" in implement_flat
    assert "initially unknown cause" in tdd_flat
    assert "original feedback loop" in diagnosing_flat
    assert "intact facts" in tdd_flat

    diagnosis_producers = (
        CUSTOM / "implement/SKILL.md",
        CUSTOM / "parallel-implement/SKILL.md",
        CUSTOM / "tdd/SKILL.md",
        CUSTOM / "simplify-code/SKILL.md",
        CUSTOM / "resolving-merge-conflicts/SKILL.md",
        CUSTOM / "audit-codebase/CANDIDATE-FOLLOWUP.md",
        CUSTOM / "grilling/references/TERMINAL-GAP-ROUTING.md",
    )
    for path in diagnosis_producers:
        content = " ".join(path.read_text(encoding="utf-8").split())
        for match in re.finditer("diagnosis-required", content):
            context = content[max(0, match.start() - 500) : match.end() + 500]
            assert "dedicated" in context, path


def test_workflow_trace_makes_durable_specification_proportional() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    normalized = " ".join(to_spec.split())

    assert not implicit_policy(CUSTOM / "to-spec")
    assert "`not-needed`" in to_spec
    assert "Create no draft or tracker state" in normalized
    assert "Recommend `$to-tickets` only when several implementation slices" in normalized
    assert "otherwise recommend `$implement`" in normalized
    assert "draft only when a new or updated durable publication is required" in normalized
    assert "For exact matching state, reuse the verified parent" in normalized
    assert "Do not invoke or recommend a resolver" in normalized


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
        "removal condition",
    ):
        assert owned_concept.lower() in spec_lower
    for downstream_concept in (
        "bounded repository grounding",
        "ticket slices",
        "expected writes",
        "concrete checks and test owners",
        "dependency graph and ready frontier",
        "static execution facts",
        "live concurrency decisions",
        "implementation technique",
    ):
        assert downstream_concept.lower() in spec_lower
    for ticket_owner in (
        "inspect enough code to ground",
        "ticket boundaries",
        "expected durable writes",
        "dependency order",
        "ready frontier",
        "static execution facts",
        "known overlap or serial tripwires",
    ):
        assert ticket_owner.lower() in tickets_lower
    assert "Paths are evidence, not an implementation plan." in spec
    assert "## Code Quality Contract" not in to_spec
    assert "`ready-spec`" in spec
    assert "`published-spec`" not in spec


def test_implementation_closeout_requires_the_spec_axis() -> None:
    formal = (
        CUSTOM / "change-review/references/FORMAL-REVIEW.md"
    ).read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (formal, assurance):
        assert "`Spec required: yes | no`" in text
    assert "`Spec required: yes`" in parallel


def test_implementation_workflows_keep_local_proof_owners() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )

    assert "Trace the real callers, data flow, and existing proof seam" in implement
    assert "Run the nearest useful check" in implement
    assert "Inspect the real output or caller path" in implement
    assert "proof owners" in parallel
    assert "Carry worker proof only while" in parallel
    assert "run only proof invalidated by the transition" in parallel
    assert "smallest final proof set" in parallel


def test_implement_owns_one_plain_worker_handoff_without_a_schema() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    handoff_path = CUSTOM / "implement/references/WORKER-HANDOFF.md"
    handoff = handoff_path.read_text(encoding="utf-8")

    assert handoff_path.is_file()
    assert "[Plain Worker Handoff](references/WORKER-HANDOFF.md)" in implement
    assert "[Plain Worker Handoff](../implement/references/WORKER-HANDOFF.md)" in parallel
    assert "If the user explicitly requests subagents" in " ".join(implement.split())
    assert "The root inspects the returned diff and proof" in " ".join(implement.split())
    assert "guidance, not a schema" in " ".join(parallel.split())
    assert "implement/references/WORKER-HANDOFF.md" in relationships
    assert "schema" not in handoff.lower()
    assert not (CUSTOM / "parallel-implement/references/WORKER-BRIEF.md").exists()
    assert not (CUSTOM / "parallel-implement/references/RUN-LEDGER.md").exists()
    assert not (CUSTOM / "parallel-implement/scripts/run_ledger.py").exists()


def test_implementation_workflows_trace_acceptance_before_completion() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    handoff = " ".join(
        (CUSTOM / "implement/references/WORKER-HANDOFF.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "Trace the real callers, data flow, and existing proof seam" in implement
    assert (
        "Before choosing an implementation seam, each worker traces every assigned"
        in parallel
    )
    assert (
        "Call the item complete only when the requested behavior works"
        in implement
    )
    assert (
        "Do not accept a lane merely because its first component seam is green"
        in parallel
    )
    assert (
        "component proof counts only when that path exercises the component"
        in handoff
    )


def test_planning_and_delivery_activate_lean_integrated_quality_contract() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

    assert "one bounded implementation" in to_spec
    assert "smallest execution packet" in tickets
    assert "smallest integrated design" in implement
    assert "Remove code made obsolete by the change" in implement
    assert "complete replacement or removal" in review
    assert "Parallelism is an optimization, not a goal" in parallel
    assert "ToSpec --> Contract" in relationships
    assert "ToTickets --> Contract" in relationships


def test_ticket_and_delivery_packets_are_compact_and_preserve_repairs() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    tickets_flat = " ".join(tickets.split())
    implement_flat = " ".join(implement.split())
    parallel_flat = " ".join(parallel.split())

    for field in ("**Intent:**", "**Grounding:**", "**Scope and proof:**", "**Delivery:**"):
        assert field in tickets
    assert "Omit inapplicable optional sections" in tickets_flat
    assert "graph-level Repair generation budget" not in tickets_flat
    assert "Create no graph or tracker state" in tickets_flat
    assert "Use the caller's selection as the scope fence" in implement_flat
    assert "Direct work creates no tracker state" in implement_flat
    assert "Return a concise summary" in implement_flat
    assert "create no campaign ledger" in parallel_flat
    assert "plain task context" in parallel_flat
    assert "Prose is evidence, not trusted state" in parallel_flat
    assert "one `$to-tickets` repair packet" in parallel_flat


def test_interface_alternatives_receive_curated_fresh_context() -> None:
    design = (CUSTOM / "codebase-design/DESIGN-IT-TWICE.md").read_text(
        encoding="utf-8"
    )
    research = (CUSTOM / "research/SKILL.md").read_text(encoding="utf-8")
    audit = (CUSTOM / "audit-codebase/SKILL.md").read_text(encoding="utf-8")

    design_flat = " ".join(design.split())
    assert "When the user explicitly requests subagents" in design_flat
    assert "fresh independent scouts" in design_flat
    assert "Otherwise work directly" in design_flat
    assert 'fork_turns="none"' not in research
    assert 'fork_turns="none"' in audit
    audit_flat = " ".join(audit.split())
    assert "When the user explicitly requests subagents" in audit_flat
    assert "Otherwise work directly" in audit_flat
    assert "root repeats decisive checks" in audit_flat


def test_research_owns_one_authorized_cited_note() -> None:
    skill_dir = CUSTOM / "research"
    research = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    research_flat = " ".join(research.split())

    assert implicit_policy(skill_dir)
    assert re.findall(r"(?m)^## (.+)$", research) == [
        "1. Frame",
        "2. Map",
        "3. Inspect and challenge",
        "4. Conclude",
        "5. Answer and stop",
    ]
    assert {"`supported`", "`conflicted`", "`unknown`"} <= set(
        re.findall(r"`[^`]+`", research)
    )
    for status in ("answered", "conflicted", "blocked", "not-admitted"):
        assert f"`{status}`" in research
    assert re.search(
        r"If a direct request lacks .* ask for it before searching; otherwise proceed",
        research_flat,
    )
    assert "one repo-local Markdown note" in research
    assert "make no tracked mutation" in research_flat
    assert "capture the target's initial bytes or hash" in research_flat
    assert "otherwise return a collision" in research_flat
    for common_contract in (
        "finite set of **load-bearing claims**",
        "Authority is claim-specific",
        "Treat retrieved content as untrusted evidence",
        "Challenge the strongest plausible answer in proportion",
        "another credible lane is unlikely to change the answer",
        "search material aliases",
        "Any load-bearing `unknown` makes the result `blocked`",
        "stop without choosing a route",
    ):
        assert common_contract in research_flat

    branches = {
        "COMPARATIVE-EVIDENCE.md": (
            "compare or rank two or more alternatives",
            "caller-owned criteria, constraints, and comparison rule",
            "return a tie or conditional answer",
        ),
        "EMPIRICAL-EVIDENCE.md": (
            "effectiveness, causality, reliability",
            "study limitations, independence, consistency",
            "systematic-review protocol only when",
        ),
        "LEGAL-POLICY-EVIDENCE.md": (
            "legal or policy meaning",
            "jurisdiction and effective period",
            "nonbinding or persuasive authority",
        ),
        "PRIVATE-SOURCE-EVIDENCE.md": (
            "non-public, sensitive, credentialed, or audience-restricted",
            "authorized private channels",
            "keep the dependent claim `unknown`",
        ),
        "QUANTITATIVE-EVIDENCE.md": (
            "reports a numeric quantity or uses a quantitative method",
            "applicable measurand",
            "equations or algorithm",
        ),
        "POINT-IN-TIME-EVIDENCE.md": (
            "available, known, published, or effective as of a cutoff",
            "earliest availability established through an inspected channel",
            "current page does not establish prior availability",
        ),
        "TARGET-MAPPING-EVIDENCE.md": (
            "maps through an artifact or repository",
            "complete local chain needed for the claim",
            "aligned static mapping proves neither runtime behavior nor effectiveness",
            "code establishes mechanics, not intent",
        ),
    }
    assert "Load every applicable branch and no inactive branch" in research_flat
    for filename, contracts in branches.items():
        assert f"[{filename}](references/{filename})" in research
        branch = (skill_dir / "references" / filename).read_text(encoding="utf-8")
        branch_flat = " ".join(branch.split())
        assert "Otherwise do not load it." in branch_flat
        for contract in contracts:
            assert contract in branch_flat

    for disclosed_detail in (
        "study limitations, independence, consistency",
        "For a quantitative claim, record the applicable measurand",
        "current page does not establish prior availability",
        "Static correspondence is `aligned`",
        "Keep external source systems read-only",
        "code establishes mechanics, not intent",
    ):
        assert disclosed_detail not in research

    assert research.index("## 4. Conclude") < research.index("## 5. Answer and stop")
    assert "For a direct request, lead with the answer" in research
    assert "For a caller invocation, return the status" in research
    assert "$grilling" not in research
    assert "$grill-with-docs" not in research
    assert "$wayfinder" not in research


def test_writing_for_agents_keeps_a_lean_common_path_and_conditional_branches() -> None:
    skill_dir = CUSTOM / "writing-for-agents"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    mechanics = (skill_dir / "references/SKILL-MECHANICS.md").read_text(
        encoding="utf-8"
    )
    behavior_evals = (skill_dir / "references/BEHAVIOR-EVALS.md").read_text(
        encoding="utf-8"
    )
    metadata = yaml.safe_load(
        (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    )
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    normalized_skill = " ".join(skill.split())
    normalized_mechanics = " ".join(mechanics.split())
    normalized_evals = " ".join(behavior_evals.split())
    normalized_context = " ".join(context.split())

    assert implicit_policy(skill_dir)
    assert metadata["interface"] == {
        "display_name": "Writing for Agents",
        "short_description": "Write instructions agents can follow",
    }
    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {
        "SKILL.md",
        "agents/openai.yaml",
        "references/BEHAVIOR-EVALS.md",
        "references/SKILL-MECHANICS.md",
    }
    assert set(re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", skill)) == {
        "references/BEHAVIOR-EVALS.md",
        "references/SKILL-MECHANICS.md",
    }
    assert "Write documents that help an agent take the intended process" in normalized_skill
    assert re.findall(
        r"^## [1-5]\. (.+)$",
        skill,
        flags=re.MULTILINE,
    ) == [
        "Understand the reader",
        "Organize the information",
        "Write the instructions",
        "Prune",
        "Check the result",
    ]
    for concept in (
        "context pointer",
        "Context load",
        "Cognitive load",
        "completion criterion",
        "leading word",
        "environment as a source of truth",
        "no-op sentence",
    ):
        assert concept in skill
    assert "Only when the user explicitly asks" in normalized_skill
    assert "Otherwise do not run behavioral cohorts" in normalized_skill
    assert "installation, publishing, staging, or commit only when the user requests it" in normalized_skill
    assert "Publishing and push require separate authority" in normalized_skill
    assert "Automatic selection is the default" in normalized_mechanics
    assert "description that acts as its context pointer" in normalized_mechanics
    assert "folder name, frontmatter `name`, metadata" in normalized_mechanics
    assert "structural checks prove package integrity" in normalized_mechanics
    assert "only when the user explicitly asks" in normalized_evals
    assert "Start with one fresh control and candidate sample" in normalized_evals
    assert "Add samples only when the result varies" in normalized_evals
    assert "Do not create a durable report unless the user asks" in normalized_evals
    assert all(term in normalized_context for term in (
        "context pointers",
        "context and cognitive load",
        "information hierarchy",
        "leading words",
        "environment caches",
        "explicit-user-request branch",
    ))
    assert (
        "bundled system `skill-creator` owns new-package scaffolding and metadata mechanics"
        in relationships
    )
    assert (
        "`$writing-for-agents` owns the instructions agents consume"
        in relationships
    )
    assert (
        "stops before metadata mechanics, installation, or delivery"
        in relationships
    )
    assert "user explicitly requests behavioral testing" in relationships


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
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(
        encoding="utf-8"
    )
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    fallback_flat = " ".join(fallback.split())
    contract_flat = " ".join(contract.split())

    assert fallback.startswith("# Global Codex Instructions\n")
    assert "when the skill pack is not installed" in fallback_flat
    assert "each repository its own short `AGENTS.md`" in fallback_flat
    assert "replace any portable contract owner preamble" in " ".join(bootstrap.split())
    assert re.findall(r"\$[a-z0-9][a-z0-9-]*", fallback) == []
    assert "It is not a workflow, checklist, review gate, completion format" in contract_flat
    assert "Git mutation owners" not in contract_flat
    assert re.findall(r"(?m)^## (.+)$", seed) == [
        "Understand before changing",
        "Design for simplicity",
        "Implement the whole change",
        "Prove the claim",
        "Activate protection from evidence",
    ]
    for shared_term in (
        "bounded slice",
        "Subtract, reuse, or replace",
        "Trust internal types and established invariants",
        "Run the nearest useful check",
        "An inactive condition creates no checklist",
    ):
        assert shared_term in contract_flat
    for text in (fallback_flat, contract_flat):
        assert "user explicitly requests subagents" in text
        assert "invoked skill owns required fanout" in text
        assert "skill or workflow owns required fanout" not in text
    assert "authorized filesystem, Git, environment, tracker" in fallback_flat

    markerless_contract = re.sub(
        r"(?m)^<!-- programming-agent-skills setup-file: [^\n]+ -->\n\n",
        "",
        contract,
    )
    assert markerless_contract == seed



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
    assert "removal condition" in brief
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


def test_mutating_workflows_require_proportional_readback() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "Read back every durable external mutation" in implement
    assert "recovery path before an operation that can partially succeed" in implement
    assert "mutation read-back" in parallel

    for name in ("to-spec", "to-tickets", "triage", "wayfinder"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "read-back" in text.lower(), name


def test_to_tickets_is_proportional_and_preserves_ready_frontiers() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(tickets.split())

    assert not implicit_policy(CUSTOM / "to-tickets")
    assert "`direct-item`" in tickets
    assert "Create no graph or tracker state" in flat
    assert "smallest execution packet" in flat
    assert "Omit inapplicable optional sections" in flat
    assert "graph-level Repair generation budget" not in flat
    assert "Use a matrix only when it is clearer than prose" in flat
    assert "`$parallel-implement` decides live concurrency" in flat
    assert "Separate packet readiness from frontier eligibility" in flat
    assert "Ready-for-agent and Ready-for-human frontiers separately" in flat
    assert "executor roles and static execution facts" in flat
    assert "execution profiles" not in flat
    assert flat.index("If the settled source is already one bounded implementation") < flat.index(
        "Only after the direct branch is excluded"
    )


def test_to_spec_canonical_is_lean_and_experimental_evidence_stays_frozen() -> None:
    canonical = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(canonical.split())

    assert "`not-needed`" in canonical
    assert "one bounded implementation" in flat
    assert "Create no draft or tracker state" in flat
    assert "draft only when a new or updated durable publication is required" in flat
    assert "Recommend `$to-tickets` only when several implementation slices" in flat
    assert "Load `$codebase-design` only when" in flat
    assert "perform exactly one configured create operation" in flat
    assert "delegate exactly one create operation" not in flat
    assert flat.index("When the settled source already describes one bounded implementation") < flat.index(
        "Only after the direct branch is excluded"
    )
    assert flat.index("Freeze one internally consistent title and parent body") < flat.index(
        "Inspect the intended durable parent target"
    )

    experimental = ROOT / "skills/experimental/to-spec"
    assert exact_tree_hash(experimental) == (
        "47c223639318b041e6c86e6144b7fb23399634ead73e18ddcf306ab8242effeb"
    )


def test_git_and_parallel_delivery_roles_stay_out_of_the_shared_contract() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for shared in (contract, seed):
        normalized = " ".join(shared.split())
        assert "use an independent oracle" in normalized
        assert "Git mutation owners" not in normalized
        assert "starting index" not in normalized
        assert "registered worktrees" not in normalized
    assert "Preserve unrelated work" in " ".join(implement.split())
    assert "Workers never widen scope or dispatch successors" in " ".join(parallel.split())


def test_parallel_implement_separates_plain_context_checkout_and_review() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lanes = (skill_dir / "references/AGENT-LANES.md").read_text(encoding="utf-8")
    profiles = (skill_dir / "references/RUNTIME-PROFILES.md").read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    assert re.findall(r"(?m)^## (.+)$", parallel) == [
        "Admit", "Wave", "Integrate", "Final Check, Conditional Review, And Repair", "Close"
    ]
    for profile in ("clear-worker", "adaptive-worker", "fast-adaptive-worker", "demanding-worker"):
        assert f"`{profile}`" in profiles
    assert "one fresh `integration-reviewer` through `$change-review`" in flat
    assert "two or more independent authors" in flat
    assert "serial execution by one author" in flat
    assert "do not trigger review" in flat
    assert "The root judges integration" in flat
    assert "warm general integrator" in flat
    assert "plain task context" in flat and "not a schema" in flat
    assert "quick pytest collection smoke when the checkout declares" in " ".join(lanes.split())
    assert "`integration-reviewer`" not in profiles
    for field in (
        "`Mode: initial`",
        "`Mode: remediation`",
        "required proof, material skips",
        "fresh task or context",
        "implementation and integration-author identities",
    ):
        assert field in flat
    assert "Do not close from `blocked` or `incomplete`" in flat
    assert "serial-integrator" not in profiles
    assert not (skill_dir / "scripts/run_ledger.py").exists()
    assert not (skill_dir / "references/RUN-LEDGER.md").exists()
    assert not (skill_dir / "references/WORKER-BRIEF.md").exists()


def test_parallel_implement_owns_recovery_authority_and_outcome_gates() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    for outcome in ("`complete`", "`partial`", "`blocked`"):
        assert outcome in parallel
    assert "Retry only after an observed blocking condition changes" in flat
    assert "never duplicate an uncertain task" in flat
    assert "return one `$to-tickets` repair packet" in flat
    assert "transfer only the exact verified campaign-owned claims" in flat
    tickets = " ".join(
        (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "On an explicit To Tickets repair invocation" in flat
    assert "An admitted transferred claim remains expected custody" in tickets
    assert "release transferred claims, verify the assignee state, and derive" in tickets
    assert "use `$resolving-merge-conflicts`" in flat
    assert "If the same blocker recurs" in flat
    assert "without a new authorized in-scope repair path" in flat
    assert "`blocked` means no authorized in-scope progress" in flat
    assert "`partial` means accepted progress is preserved" in flat
    assert "Retain each claim through verified non-dispatchable closeout" in flat
    assert "Close the parent only after every child verifies" in flat
    for required_return_evidence in (
        "integrated `HEAD`",
        "every final proof run and result",
        "review decision (`passed` or `not triggered`)",
        "verified child and parent closeout",
        "final claim state",
        "lane cleanup",
        "preserved recovery evidence (`none` when absent)",
    ):
        assert required_return_evidence in flat
    assert "Missing any one of these fields makes the Return `partial`" in flat


def test_parallel_implement_has_one_lean_worktree_lifecycle() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lanes = (skill_dir / "references/AGENT-LANES.md").read_text(encoding="utf-8")
    lane_script = (skill_dir / "scripts/lane_worktree.py").read_text(encoding="utf-8")
    codex_config = (ROOT / ".codex/config.toml").read_text(encoding="utf-8")
    flat = " ".join(lanes.split())

    assert "Pass only at the top-level root" in parallel
    assert "lane_worktree.py prepare" in flat
    assert "lane_worktree.py cleanup" in flat
    assert "pytest temp and cache roots" in flat
    assert "quick pytest collection smoke when the checkout declares" in flat
    assert "Start the worker only when" in flat and "`ok: true`" in flat
    assert "--oldest" in lanes and "--completed" in lanes
    assert "deletes state only after `git worktree remove` succeeds" in flat
    assert "leaves state intact" in flat
    assert "exact retry whose helper-owned state remains" in flat
    assert "non-empty or uncertain paths remain preserved" in flat
    assert 'operations.add_parser("prepare")' in lane_script
    assert 'operations.add_parser("cleanup")' in lane_script
    assert '"--collect-only"' in lane_script and '"addopts="' in lane_script
    assert "lane_state(root, worktree.name)" in lane_script
    assert "shutil.rmtree(state)" in lane_script and "--global" not in lane_script
    assert (skill_dir / "assets/luna_max.toml").read_bytes() == (
        ROOT / ".codex/agents/luna_max.toml"
    ).read_bytes()
    expected_lane_root = str(Path(ROOT.anchor) / "pi" / "pas-001" / "wt")
    assert expected_lane_root.replace("\\", "\\\\") in codex_config


def test_parallel_implement_exposes_live_frontier_and_closeout_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    tickets_flat = " ".join(tickets.split())
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    assert not implicit_policy(skill_dir)
    assert "dependency-ready frontier" in flat
    assert "expected time saving exceeds coordination and integration cost" in flat
    assert "Uncertain or overlapping items run serially" in flat
    assert "retain the parent campaign through serial or concurrent frontiers" in flat
    assert "Claim the parent and read the claim back before dispatch" in flat
    assert "does not land the same commit again" in flat
    assert flat.index("Close children") < flat.index("Close the parent")
    assert re.search(
        r"(?m)^\| One explicitly requested parent has an exhaustive "
        r"non-empty Ready-for-agent graph \| `\$parallel-implement` \|$",
        router,
    )
    assert "selected directly or as a Ready-for-agent item" in router
    assert "Recommend `$parallel-implement` only when the user explicitly requested" in tickets
    assert "may run any frontier serially" in tickets_flat
    assert "`to-tickets` | Recommend and stop | `$parallel-implement`" in relationships


def test_parallel_uses_current_landed_state_without_a_dependency_overlay() -> None:
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "current landed state" in parallel
    assert "Recompute the frontier after each accepted landing" in parallel
    for token in ("landed-awaiting-lock", "same-campaign", "dependency overlay"):
        assert token not in parallel


def test_shared_protection_uses_a_concrete_trigger_not_a_state_catalog() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")

    for shared in (contract, seed):
        normalized = " ".join(shared.split())
        assert "active trust or effect boundary" in normalized
        assert "Local or personal use alone is not a trigger" in normalized
        assert "Handle state, retry, recovery, cancellation, concurrency" not in normalized
    flat = " ".join(tickets.split())
    assert "whose behavior materially changes by state" in flat
    assert "Use a matrix only when it is clearer than prose" in flat
    assert "never add Cartesian or stateless padding" in flat


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(
        (CUSTOM / "implement/agents/openai.yaml").read_text(encoding="utf-8")
    )
    flat = " ".join(implement.split())
    prompt = metadata["interface"]["default_prompt"]

    assert not implicit_policy(CUSTOM / "implement")
    assert "Deliver exactly one caller-selected ready item" in flat
    assert "Use the caller's selection as the scope fence" in flat
    assert "The caller owns the requested outcome" in flat
    assert "Push requires separate authority" in flat
    assert "Commit only when the user or repository requires Git delivery" in flat
    assert "user explicitly requests subagents" in flat
    assert "Work directly by default" in flat
    assert "smallest sound design" in prompt
    assert "Use heavier workflows only when their stated condition applies" in prompt


def test_implement_closeout_locks_exact_candidate_and_preserves_custody() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(implement.split())

    assert "Direct work creates no tracker state" in flat
    assert "follow the repository's claim and closeout rules" in flat
    assert "do not push without separate authority" in flat
    assert "Read back every durable external mutation" in flat
    assert "recovery path before an operation that can partially succeed" in flat
    assert "Call the item complete only when the requested behavior works" in flat
    assert "Return a concise summary" in flat
    assert "Outcome: complete | partial | blocked" not in flat
    assert "request remediation review only while the original trigger remains" in flat


def test_current_relationships_preserve_candidate_commit_and_repair_claim_custody() -> None:
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )
    flat = " ".join(relationships.split())
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    repair = next(
        relationship
        for relationship in contract["relationships"]
        if relationship["relationship_id"] == "REL-036"
    )

    assert "A repaired successor is reviewed only while the original trigger still applies" in flat
    assert "retain campaign claims" in flat
    assert "Only a later explicit To Tickets invocation" in flat
    assert "releases those claims only after repaired graph read-back" in flat
    assert "campaign claims retained pending later explicit admission" in repair["return_packet"]
    assert "only after repaired graph read-back" in repair["return_packet"]


def test_diagnosis_is_an_explicit_leaf_with_bounded_recommendations() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    prototype = (CUSTOM / "prototype/SKILL.md").read_text(encoding="utf-8")
    resolver = (CUSTOM / "resolving-merge-conflicts/SKILL.md").read_text(
        encoding="utf-8"
    )
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
        encoding="utf-8"
    )

    diagnosing_flat = " ".join(diagnosing.split())
    assert "or reports something broken" not in diagnosing
    assert "hypothesis ledger" not in diagnosing_flat
    assert "every ranked competing hypothesis" not in diagnosing_flat
    assert "Return one diagnosis packet containing:" not in diagnosing
    rows = set(
        re.findall(
            r"(?m)^\| `([a-z0-9-]+)` \| (Load|Invoke|Compose|Hand off|Recommend and stop) \| `\$([a-z0-9-]+)` \|",
            relationships,
        )
    )
    assert not implicit_policy(CUSTOM / "diagnosing-bugs")
    assert "Start no successor" in diagnosing_flat
    assert set(re.findall(r"\$[a-z0-9-]+", diagnosing)) == set()
    assert "recommend `$diagnosing-bugs` and stop before mutation" in prototype
    assert "recommend `$diagnosing-bugs`" in resolver
    assert {
        (caller, verb, callee)
        for caller, verb, callee in rows
        if caller == "diagnosing-bugs" or callee == "diagnosing-bugs"
    } == {
        ("prototype", "Recommend and stop", "diagnosing-bugs"),
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


def test_runtime_composition_edges_respect_lean_review_and_planning_policy() -> None:
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    rows = re.findall(
        r"(?m)^\| `([a-z0-9][a-z0-9-]*)` \| "
        r"(Load|Invoke|Compose|Hand off|Recommend and stop) \| "
        r"`\$([a-z0-9][a-z0-9-]*)` \|",
        relationships,
    )
    edges = set(rows)
    relationships_flat = " ".join(relationships.split())

    for edge in (
        ("wayfinder", "Recommend and stop", "implement"),
        ("wayfinder", "Recommend and stop", "to-spec"),
        ("to-spec", "Recommend and stop", "implement"),
        ("to-spec", "Recommend and stop", "to-tickets"),
        ("to-tickets", "Recommend and stop", "implement"),
        ("to-tickets", "Recommend and stop", "parallel-implement"),
        ("implement", "Invoke", "change-review"),
        ("parallel-implement", "Invoke", "change-review"),
    ):
        assert edge in edges
    assert not any(
        callee == "high-assurance-review" and caller in {
            "skill-router", "implement", "parallel-implement", "change-review"
        }
        for caller, _, callee in edges
    )
    assert not any(
        {caller, callee} == {"implement", "parallel-implement"}
        for caller, _, callee in edges
    )
    assert "mutations from two or more independent authors" in relationships_flat
    assert "Missing proof stops instead" in relationships_flat
    assert "Supported risk modifies coverage only after review admission" in relationships_flat
    assert not implicit_policy(CUSTOM / "high-assurance-review")


def test_router_and_synthesis_keep_active_ownership_unambiguous() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    synthesis_index = (ROOT / "docs/synthesis/README.md").read_text(encoding="utf-8")

    assert "target-spine.md" not in synthesis_index
    assert "language-direction.md" not in synthesis_index
    assert "support tickets" not in tickets
    assert "support slices" not in tickets
