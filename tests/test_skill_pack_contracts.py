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

    assert set(routed) | {"repo-bootstrap"} == skill_names - {"skill-router"}
    assert len(routed) == len(set(routed))
    assert routed.count("high-assurance-review") == 1


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
    grilling_gap = (CUSTOM / "grilling/references/TERMINAL-GAP-ROUTING.md").read_text(
        encoding="utf-8"
    )
    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    synthesis = (ROOT / "docs/synthesis/skills/to-questionnaire.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(skill_dir)
    questionnaire_instructions = re.sub(
        r"```.*?```", "", questionnaire, flags=re.DOTALL
    )
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", questionnaire_instructions) == [
        "Identify",
        "Draft",
        "Write",
    ]
    for contract in (
        "Grill the send, not the subject.",
        "one recipient and one downstream decision",
        "return the proposed split instead of blending them",
        "Preserve a supplied answer-return destination.",
        "supplied context already answers the gap",
        "Remove any question that does not affect the downstream decision.",
        "Invite partial answers and explicit unknowns.",
        "Every item the user needs back must have a substantive question.",
        "A catch-all does not count as coverage.",
        "Do not include or ask for credentials or secrets",
        "to-questionnaire-<slug>.md",
        "Never overwrite an existing file without explicit authority",
        "Reread the complete intended file as the recipient.",
        "If the write or reread failed or was partial, do not claim completion",
        "Delivery: not performed",
        "Stop before delivery, answer handling, or the downstream decision.",
    ):
        assert contract in questionnaire_flat
    for rejected in (
        "Status: Questionnaire ready",
        "Artifact durability:",
        "attributable mutation",
        ".tmp/to-questionnaire",
        "$repo-bootstrap",
        "Wayfinder",
    ):
        assert rejected not in questionnaire
    assert policy.endswith("policy:\n  allow_implicit_invocation: false\n")
    current_reconciliation = synthesis.split("Decision: Prompt 5", 1)[0]
    assert skill_pack_contract.tree_hash(skill_dir) in current_reconciliation
    assert "unavailable from inspectable sources and the user" in questionnaire
    assert (
        "| One external stakeholder holds missing knowledge and needs an async "
        "discovery questionnaire | `$to-questionnaire` |"
    ) in router
    assert "`$to-questionnaire` for an external stakeholder" in " ".join(
        grilling_gap.split()
    )
    assert "| `$audit-codebase` | Recommend and stop | `$to-questionnaire` |" in synthesis
    assert questionnaire.index("supplied context already answers the gap") < (
        questionnaire.index("Ask one compact intake")
    )
    wayfinder_resolvers = (
        CUSTOM / "wayfinder/references/RESOLVERS.md"
    ).read_text(encoding="utf-8")
    wayfinder_flat = " ".join(wayfinder_resolvers.split())
    assert "exact `$to-questionnaire` plus Wayfinder re-entry instruction" in wayfinder_flat
    assert "Do not invoke the explicit-only skill" in wayfinder_flat

    pack = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    relationships = {
        row["relationship_id"]: row for row in pack["relationships"]
    }
    assert "REL-104" not in relationships
    questionnaire_edge = relationships["REL-096"]
    assert questionnaire_edge["verb"] == "Recommend and stop"
    assert questionnaire_edge["context_loaded"] == []
    assert questionnaire_edge["return_packet"].endswith(
        "questionnaire work unstarted"
    )


def test_tracker_templates_keep_provider_configuration_and_readback_only() -> None:
    trackers = [
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    ]
    required = (
        "## Operations",
        "## Representation",
        "## Mutation read-back",
        "safest recovery",
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
        "## Wayfinding representation",
        "**Ready query:**",
        "**Closeout:**",
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
        wayfinding_flat = " ".join(tracker.read_text(encoding="utf-8").split())
        for foreign_procedure in (
            "codex/<lowercase UUIDv4>",
            "<YYYY-MM-DDTHH:MM:SSZ>",
            "Elapsed time alone never makes a claim stale.",
            "approver authority",
            "Claim token:",
            "Decision owner:",
        ):
            assert foreign_procedure not in wayfinding_flat

    mutation = " ".join(
        (CUSTOM / "wayfinder/references/MUTATION.md")
        .read_text(encoding="utf-8")
        .split()
    )
    for token in (
        "fresh unpredictable claim token",
        "same tracker account remain distinguishable",
        "Another token owns the item",
        "Time alone never expires a claim",
        "destination-owner or provider-administrator",
        "prove the assignee and claim token are absent",
    ):
        assert token in mutation
    assert "codex/<lowercase UUIDv4>" not in mutation
    assert "<YYYY-MM-DDTHH:MM:SSZ>" not in mutation


def test_repo_bootstrap_validates_provider_tracker_templates() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["tracker_configuration_failures"]
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        assert check(text) == []
        for retired in (
            "## Wayfinding representation",
            "**Ready query:**",
            "Claim token:",
            "Decision owner:",
        ):
            assert retired not in text

    github = trackers[0].read_text(encoding="utf-8")
    missing_mode = github.replace("native-sub-issues", "when-available", 1)
    assert check(missing_mode) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitHub mode"
    ]


def test_triage_label_template_respects_tracker_pr_policy() -> None:
    labels = (CUSTOM / "repo-bootstrap/triage-labels.md").read_text(encoding="utf-8")
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    triage_flat = " ".join(triage.split())

    assert "Map active skill-pack roles" in labels
    assert "Include these labels only when Wayfinder is active" in labels
    assert "`wayfinder:questionnaire`" in labels
    assert "`wayfinder:diagnosis`" not in labels
    assert "`wayfinder:diagnosis`" not in (
        CUSTOM / "repo-bootstrap/triage-labels.md"
    ).read_text(encoding="utf-8")
    assert "external PR or MR only when the tracker configuration permits it" in (
        triage_flat
    )


def test_label_consumers_own_explicit_role_transitions() -> None:
    texts = {
        name: " ".join((CUSTOM / name / "SKILL.md").read_text(encoding="utf-8").split())
        for name in ("triage", "to-tickets", "wayfinder", "implement", "parallel-implement")
    }
    texts["parallel-implement"] += " " + " ".join(
        (CUSTOM / "parallel-implement/references/TRACKER-DELIVERY.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "Use `bug` only for a defect" in texts["triage"]
    assert "`needs-triage` marks unprocessed intake" in texts["triage"]
    assert "Non-ready means no readiness state role" in texts["to-tickets"]
    assert "apply and read back `ready-for-agent` only" in texts["to-tickets"]
    for role in (
        "wayfinder:map",
        "wayfinder:research",
        "wayfinder:prototype",
        "wayfinder:grilling",
        "wayfinder:questionnaire",
        "wayfinder:task",
    ):
        assert role in texts["wayfinder"]
    for name in ("implement", "parallel-implement"):
        assert "docs/agents/triage-labels.md" in texts[name]
        assert "apply `implemented`" in texts[name]
        assert "apply `ready-for-agent` only" in texts[name]


def test_delivery_skills_own_closeout_and_trackers_keep_readback() -> None:
    hosted_trackers = (
        ROOT / "docs/agents/issue-tracker.md",
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
    )
    for tracker in hosted_trackers:
        normalized = " ".join(tracker.read_text(encoding="utf-8").split())
        assert "**Closeout:**" not in normalized
        assert "## Mutation read-back" in normalized
        assert "must not expose a dependent as ready" in normalized
        assert "named recovery custodian" not in normalized

    github = hosted_trackers[0].read_text(encoding="utf-8")
    assert "**Close implemented items:** yes." in github

    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel_tracker = " ".join(
        (CUSTOM / "parallel-implement/references/TRACKER-DELIVERY.md")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "For tracker-backed delivery" in parallel
    assert "After all children finish" in parallel_tracker
    assert "Apply `implemented` to the parent" in parallel_tracker
    assert "only when every child is implemented" in parallel_tracker


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
        assert "Resolve the operation and its independent read-back route before" in (
            normalized
        )
        assert "Do not switch relationship representations" in normalized
        assert "when available" not in text

    tracker = (ROOT / "docs/agents/issue-tracker.md").read_text(encoding="utf-8")
    assert "skills/custom/to-tickets/scripts/github_issue_relationships.py" in tracker
    tickets = " ".join(
        (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "configured relationship mutation and read-back route" in tickets


def test_repo_bootstrap_rejects_unconfigured_github_relationship_modes() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    tracker = (ROOT / "docs/agents/issue-tracker.md").read_text(encoding="utf-8")
    check = lambda text: validator["relationship_mode_failures"](
        text, "GitHub", validator["GITHUB_RELATIONSHIP_MODES"]
    )

    assert check(tracker) == []
    invalid = tracker.replace("native-sub-issues", "when-available", 1)
    assert check(invalid) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitHub mode"
    ]
    assert check(tracker) == []


def test_repo_bootstrap_validates_selected_domain_layout() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["domain_layout_failures"]
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")

    assert check(domain) == []
    assert check(domain.replace("single-context.", "unknown.")) == [
        "docs/agents/domain.md must set Configured layout to "
        "single-context or multi-context"
    ]
    assert check(domain.replace("$domain-modeling", "$domain-owner")) == [
        "docs/agents/domain.md must point to $domain-modeling"
    ]


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
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    normalized = " ".join(bootstrap.split())

    assert not implicit_policy(CUSTOM / "repo-bootstrap")
    assert re.findall(r"(?m)^## \d\. (.+)$", bootstrap) == [
        "Inspect",
        "Reconcile",
        "Propose",
        "Apply",
        "Verify",
    ]
    for obligation in (
        "only the setup branches relevant",
        "Preserve repository instructions",
        "exact local edits, external operations",
        "approval of that exact delta",
        "Refresh every affected target before writing",
        "Read back each external effect",
        "Do not retry blindly or assume rollback",
        "Run a repository command only when it can disprove a claim",
        "Leave the recommending workflow unstarted",
    ):
        assert obligation in normalized
    for retired in (
        "`compatible`, `delta`, `conflict`, or `not applicable`",
        "Proposal only",
        "Setup incomplete",
        "`applied`, `failed`, `unknown`, or `not attempted`",
    ):
        assert retired not in bootstrap


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
    assert "only when the user requested it" in bootstrap
    assert "`$parallel-implement` returned that exact blocker" in bootstrap
    assert "do not create worktrees or lane directories" in bootstrap
    assert "ask whether to enable it" not in bootstrap

    config = root / validator["PARALLEL_CONFIG"]
    config.parent.mkdir(parents=True)
    config.write_text('default_permissions = "workspace"\n', encoding="utf-8")
    assert check(root) == []

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


def test_repo_bootstrap_validates_internal_setup_schema_without_target_marker() -> None:
    schema = json.loads(
        (CUSTOM / "repo-bootstrap/setup-schema.json").read_text(encoding="utf-8")
    )
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    validator = (CUSTOM / "repo-bootstrap/scripts/validate_setup.py").read_text(
        encoding="utf-8"
    )
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert schema["format"] == 1
    assert "programming-agent-skills setup-schema:" not in bootstrap
    assert "programming-agent-skills setup-schema:" not in validator
    assert "programming-agent-skills setup-schema:" not in agents
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

    valid_agents = (
        "# Repository Instructions\n\n"
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
    assert check(
        f"# Engineering Contract\n\n{marker}\n\nprose outside a section\n\n## Empty\n",
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
    assert validator["agent_pointer_failures"](reworded) == []

    assert validator["agent_pointer_failures"](
        reworded.replace("docs/agents/engineering-contract.md", "docs/engineering.md")
    ) == [
        "AGENTS.md is missing docs/agents/engineering-contract.md"
    ]
    commented = "\n".join(f"<!-- {pointer} -->" for pointer in pointers)
    assert validator["agent_pointer_failures"](commented) == [
        f"AGENTS.md is missing {pointer}" for pointer in pointers
    ]


def test_outdated_setup_routes_to_repo_bootstrap() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    template = (ROOT / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").read_text(
        encoding="utf-8"
    )

    assert "$repo-bootstrap" in router
    assert "$repo-bootstrap" in template


def test_repo_bootstrap_is_recommended_only_and_callers_read_installed_contracts() -> None:
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }
    inbound = [
        edge
        for edge in contract["relationships"]
        if names[edge["target_skill_id"]] == "repo-bootstrap"
    ]

    assert inbound
    for edge in inbound:
        assert edge["verb"] == "Recommend and stop"
        assert edge["context_loaded"] == []
        assert "No callee execution" in edge["callee_owned_gates_mutations"][0]

    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    projected_callers = set(
        re.findall(
            r"(?m)^\| `([^`]+)` \| Recommend and stop \| `\$repo-bootstrap` \|",
            relationships,
        )
    )
    assert projected_callers == {
        names[edge["caller_skill_id"]] for edge in inbound
    }

    required_pointers = {
        "domain-modeling": ("docs/agents/domain.md",),
        "implement": (
            "docs/agents/issue-tracker.md",
            "docs/agents/triage-labels.md",
        ),
        "parallel-implement": (
            "docs/agents/issue-tracker.md",
            "docs/agents/triage-labels.md",
        ),
        "to-spec": ("docs/agents/issue-tracker.md",),
        "to-tickets": (
            "docs/agents/issue-tracker.md",
            "docs/agents/triage-labels.md",
        ),
        "triage": (
            "docs/agents/issue-tracker.md",
            "docs/agents/triage-labels.md",
        ),
        "wayfinder": (
            "docs/agents/issue-tracker.md",
            "docs/agents/triage-labels.md",
        ),
    }
    for skill_name, pointers in required_pointers.items():
        entrypoint = (CUSTOM / skill_name / "SKILL.md").read_text(encoding="utf-8")
        if skill_name == "parallel-implement":
            assert "[Tracker Delivery](references/TRACKER-DELIVERY.md)" in entrypoint
            text = (
                CUSTOM / "parallel-implement/references/TRACKER-DELIVERY.md"
            ).read_text(encoding="utf-8")
        else:
            text = entrypoint
        flat = " ".join(text.split())
        for pointer in pointers:
            assert pointer in text
        assert "$repo-bootstrap" in text
        assert "missing or incompatible" in flat
        assert "stop" in flat


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
    assert "explicitly asks which skill to use" in router.split("---", 2)[1]
    steps = re.findall(r"(?m)^\d+\. \*\*[^*]+\.\*\*", router)
    assert 3 <= len(steps) <= 6
    stop = router.split("4. **Stop.**", 1)[1].split("## Route Map", 1)[0]
    assert "Skill: <skill-name | none>" in stop
    assert "Reason: <winning contract | exact unmet routing predicates>" in stop
    assert "Precondition:" in stop
    assert "only when the user" in stop
    assert "missing, incompatible, or outdated" in router_flat
    assert "Skill: <skill-name | none>" in router
    assert "exact unmet routing predicates" in router
    assert "`none` is a terminal abstention, not a recommendation" in router_flat
    assert "never substitute the nearest or weakest route" in router_flat
    assert "not instead of one allowed clarification" in router_flat
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
    assert "explicitly asks which engineering skill" in selected["positive_entry_predicate"]
    assert "when one exists" in selected["return_packet"]
    assert "truthfully return none" in capability["observable_outcome"]
    assert "explicitly asks which engineering skill" in capability["entry_conditions"][0]
    assert "when one exists" in capability["completion_return"]
    assert "no-match abstention" in capability["required_authority_mutation"][0]
    routes = dict(
        (skill, situation.strip())
        for situation, skill in re.findall(
            r"(?m)^\| (?!-)([^|]+?) \| `\$([a-z0-9][a-z0-9-]*)` \|$", router
        )
    )
    assert "durable parent" in routes["to-spec"]
    assert "ticket graph" in routes["to-tickets"]
    assert "explicitly requests" in routes["high-assurance-review"]
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
    design = (CUSTOM / "codebase-design/SKILL.md").read_text(encoding="utf-8")

    assert "[ATTENTION-SCAN.md](ATTENTION-SCAN.md)" in triage
    assert "When the maintainer names an exact state" in triage
    assert not (CUSTOM / "triage/SPECIFIC-ITEM.md").exists()
    assert not (CUSTOM / "triage/QUICK-OVERRIDE.md").exists()
    assert "without changing tracker state" in attention
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
    assert "| `to-spec` | Load | `$codebase-design` |" not in relationships
    assert "| `audit-codebase` | Load | `$codebase-design` |" in relationships
    for caller in ("research", "tdd", "simplify-code"):
        assert f"| `{caller}` | Recommend and stop | `$codebase-design` |" not in (
            relationships
        )


def test_wayfinder_has_one_lean_decision_map_job() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")
    flat = " ".join(wayfinder.split())

    assert not implicit_policy(skill_dir)
    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {
        "SKILL.md",
        "MAP-FORMAT.md",
        "agents/openai.yaml",
        "references/MUTATION.md",
        "references/RESOLVERS.md",
    }
    assert re.findall(r"(?m)^## (Bound|Chart|Advance|Reconcile|Finish)$", wayfinder) == [
        "Bound",
        "Chart",
        "Advance",
        "Reconcile",
        "Finish",
    ]
    assert "several coupled questions or prerequisites" in flat
    assert "at least one non-conversational resolver" in flat
    assert "durable sequencing across sessions" in flat
    assert "one conversation, one resolver, or settled source" in flat
    assert "Wayfinding plans; it never implements the destination" in flat
    assert "does not do more than one of those" in flat
    assert "unblock, invalidate, or reshape" in flat
    assert "Use map order as the tie-breaker" in flat

    chart = wayfinder.split("## Chart", 1)[1].split("## Advance", 1)[0]
    chart_flat = " ".join(chart.split())
    assert chart_flat.index("After exact approval") < chart_flat.index(
        "create the map first"
    )
    assert chart_flat.index("create the map first") < chart_flat.index(
        "repeat the identity search"
    )
    assert "then create its tickets and edges" in chart_flat
    assert "[Mutation](references/MUTATION.md)" in chart

    for field in (
        "Owner:",
        "Outcome:",
        "In scope:",
        "Out of scope:",
        "Close when:",
        "Return to:",
        "Decision owner:",
        "Accept when:",
        "## Why this matters",
    ):
        assert field in map_format
    for retired in (
        "Post-Chart ticket allowance",
        "Post-Chart tickets used",
        "Terminal kind:",
        "Participation:",
        "Resolution owner:",
        "Resolver:",
        "Expected return:",
        "Re-entry owner:",
        "Growth allowance:",
    ):
        assert retired not in map_format
    assert "## Closing record" in map_format
    assert "## Termination record" in map_format
    assert "Blocked by:" not in map_format
    assert "configured tracker relationship mode" in map_format
    assert "Route-closing satisfaction" not in map_format
    assert "Closing evidence:" in map_format
    assert "Confirmed by:" in map_format


def test_wayfinder_keeps_only_triggered_tracker_protection() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    mutation = (skill_dir / "references/MUTATION.md").read_text(encoding="utf-8")
    mutation_flat = " ".join(mutation.split())

    assert "fresh unpredictable claim token" in mutation_flat
    assert "same tracker account remain distinguishable" in mutation_flat
    assert "Another token owns the item" in mutation_flat
    assert "Time alone never expires a claim" in mutation_flat
    assert "serialize ownership or expose an observable losing race" in mutation_flat
    assert "Before every write or release" in mutation_flat
    assert "establish one creation writer" in mutation_flat
    assert "claim and read it back before creating children and edges" in mutation_flat
    assert "designate one canonical shell" in mutation_flat
    assert "Read back one exact match" in mutation_flat
    assert "resume the already-approved children and edges" in mutation_flat
    assert "For Finish, claim and read back the map" in mutation_flat
    assert mutation_flat.index("claim and read back the ticket") < mutation_flat.index(
        "Claim the map only for reconciliation"
    )
    assert "reread the question, owner, resolver route, dependencies" in mutation_flat
    assert "Ignore unrelated comments or metadata" in mutation_flat
    assert "Material drift records no outcome" in mutation_flat
    assert "resulting frontier" in mutation_flat
    assert "prove the assignee and claim token are absent" in mutation_flat
    assert "inspected before retry" in mutation_flat
    assert "applied, failed, and unknown effects" in mutation_flat
    assert "codex/<lowercase UUIDv4>" not in mutation
    assert "Claimed at:" not in mutation

    advance = wayfinder.split("## Advance", 1)[1].split("## Reconcile", 1)[0]
    advance_flat = " ".join(advance.split())
    assert advance_flat.index("explicit-only resolver") < advance_flat.index(
        "claim the ticket"
    )
    assert "before any claim or shared mutation" in advance_flat
    assert "Never retain a claim across an external or user wait" in " ".join(
        wayfinder.split()
    )

    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )
    for tracker in trackers:
        body = tracker.read_text(encoding="utf-8")
        for field in ("Type:", "Decision owner:", "Accept when:", "Claim token:"):
            assert field not in body
        assert "## Representation" in body
        assert "## Mutation read-back" in body
        for retired in (
            "Participation:",
            "Resolution owner:",
            "Resolver:",
            "Expected return:",
            "Re-entry owner: $wayfinder",
            "Claimed at:",
        ):
            assert retired not in body


def test_wayfinder_resolvers_and_relationships_stop_at_the_settled_result() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    resolvers = (skill_dir / "references/RESOLVERS.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }

    for route in (
        "$research",
        "$prototype",
        "$grilling",
        "$grill-with-docs",
        "$to-questionnaire",
    ):
        assert route in resolvers
    assert "A questionnaire file is waiting evidence, not an answer" in resolvers
    assert "Do not invoke the explicit-only skill" in resolvers
    for field in (
        "selected question",
        "why it matters",
        "decision owner",
        "acceptance evidence",
        "Source Trace",
        "mutation boundary",
        "return owner",
        "Wayfinder re-entry",
    ):
        assert field in resolvers
    assert (
        "A malformed, mismatched, unauthorized, or non-admitted return records no outcome"
        in " ".join(resolvers.split())
    )
    assert "After Finish it starts no downstream skill" in " ".join(
        wayfinder.split()
    )

    wayfinder_edges = {
        (names[row["target_skill_id"]], row["verb"])
        for row in contract["relationships"]
        if names[row["caller_skill_id"]] == "wayfinder"
    }
    assert wayfinder_edges == {
        ("grill-with-docs", "Invoke"),
        ("prototype", "Invoke"),
        ("repo-bootstrap", "Recommend and stop"),
        ("research", "Invoke"),
        ("grilling", "Invoke"),
        ("to-questionnaire", "Recommend and stop"),
    }
    for retired in ("$domain-modeling", "$implement", "$to-spec"):
        assert f"| `wayfinder` | Invoke | `{retired}` |" not in relationships
        assert f"| `wayfinder` | Recommend and stop | `{retired}` |" not in relationships

    research_edge = next(
        row
        for row in contract["relationships"]
        if names[row["caller_skill_id"]] == "wayfinder"
        and names[row["target_skill_id"]] == "research"
    )
    for field in (
        "Wayfinder question",
        "why it matters",
        "scope and exclusions",
        "applicable state",
        "acceptance evidence",
        "approved note path or no-write mode",
        "Source Trace",
        "return owner",
    ):
        assert field in research_edge["input_packet"]

    wayfinder_capability = next(
        row for row in contract["capabilities"] if row["capability_id"] == "CAP-021"
    )
    wayfinder_skill = next(
        row for row in contract["selected_skills"] if row["canonical_name"] == "wayfinder"
    )
    canonical_entry = (
        "One bounded destination has several coupled questions or prerequisites, "
        "at least one non-conversational resolver, and needs tracker-backed "
        "multi-session sequencing"
    )
    assert wayfinder_capability["entry_conditions"] == [canonical_entry]
    assert wayfinder_skill["positive_entry_predicate"] == canonical_entry
    grilling_edge = next(
        row for row in contract["relationships"] if row["relationship_id"] == "REL-094"
    )
    for condition in (
        "bounded destination",
        "several coupled unresolved questions or prerequisites",
        "at least one non-conversational resolver",
        "tracker-backed multi-session sequencing",
    ):
        assert condition in grilling_edge["entry_condition"]
    assert "no non-conversational resolver is required" in grilling_edge[
        "wrong_condition"
    ]


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
    assert "Domain Modeling owns intended meaning" not in grill_docs
    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", grill_docs) == [
        "Bound",
        "Compose",
        "Return",
    ]
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
    } == {"audit-codebase"}
    assert ("wayfinder", "Invoke", "grill-with-docs") in rows
    assert ("wayfinder", "Invoke", "grilling") in rows
    assert ("wayfinder", "Recommend and stop", "to-questionnaire") in rows
    assert ("grilling", "Recommend and stop", "wayfinder") in rows
    assert ("grilling", "Recommend and stop", "to-spec") not in rows
    grill_docs_flat = " ".join(grill_docs.split())
    for contract in (
        "needs both live questioning and domain reconciliation",
        "before Grilling asks a dependent question",
        "Grilling owns questioning, materiality judgment, and confirmation",
        "Domain Modeling owns domain relevance, reconciliation, and the domain result",
        "Keep Domain Modeling's context-write and ADR approval gates intact",
        "A material domain collision prevents confirmation",
        "stop before downstream work",
    ):
        assert contract in grill_docs_flat
    for retired_protocol in (
        "Source Trace",
        "Domain Delta",
        "Status: Confirmed",
        "re-entry condition",
        "never merge or reinterpret",
    ):
        assert retired_protocol not in grill_docs
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    grill_docs_contract = next(
        skill
        for skill in contract["selected_skills"]
        if skill["canonical_name"] == "grill-with-docs"
    )
    assert grill_docs_contract["required_input"] == (
        "One bounded repo-backed decision owned by the current user, plus a "
        "return owner on caller invocation and any supplied context-write or ADR authority"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    assert (
        "One current-user-owned repo-backed decision needs live grilling and "
        "domain reconciliation as answers settle"
    ) in router
    router_edge = next(
        relationship
        for relationship in contract["relationships"]
        if relationship["relationship_id"] == "REL-052"
    )
    assert "current-user-owned repo-backed decision" in router_edge["entry_condition"]
    assert "When active `$wayfinder` is the return owner" in grilling_gap

    grill_docs_synthesis = (
        ROOT / "docs" / "synthesis" / "skills" / "grill-with-docs.md"
    ).read_text(encoding="utf-8")
    assert "They are historical, not current instructions" in grill_docs_synthesis
    assert "# Layer Two: Historical Normative Design" in grill_docs_synthesis
    assert (
        skill_pack_contract.tree_hash(CUSTOM / "grill-with-docs")
        in grill_docs_synthesis
    )
    assert "Current reconciliation: Pack composition revision 26" in (
        grill_docs_synthesis
    )


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())
    description = domain.split("---", 2)[1]
    assert (
        "description: Resolve or capture project-specific domain meaning, "
        "invariants, bounded contexts, relationships, or an already-settled "
        "ADR candidate. Exclude vocabulary lookup, code-structure design, and "
        "unresolved product or architecture decisions."
    ) in " ".join(description.split())
    context_format = (
        CUSTOM / "domain-modeling/CONTEXT-FORMAT.md"
    ).read_text(encoding="utf-8")
    context_format_flat = " ".join(context_format.split())

    assert re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", domain) == [
        "Ground",
        "Clarify",
        "Settle",
        "Capture",
        "Return",
    ]
    for target in ("CONTEXT-FORMAT.md", "ADR-FORMAT.md"):
        assert (CUSTOM / "domain-modeling" / target).is_file()
        assert f"({f'./{target}'})" in domain
    for contract in (
        "They do not settle intended meaning",
        "scenario only when its answer could change the model",
        "implementation defect, model correction, or intentional migration",
        "Reconcile with routed current records before adding text",
        "every verified intermediate state retains readable current truth",
        "Reread every attempted target",
        "verified changed, verified unchanged, or unknown",
        "return each unapplied consequence to its owner",
        "return the current domain result after each answer that may affect domain meaning",
        "A no-change result is valid",
        "Accumulate only current domain consequences",
        "does not choose interview materiality",
    ):
        assert contract in domain_flat
    assert (
        "Preserve independent meanings across contexts unless an explicit "
        "relationship or Shared Kernel joins them."
    ) in context_format_flat
    assert "non-obvious durable distinction" in context_format_flat
    assert "Never force a pattern" in context_format_flat
    assert "Big Ball of Mud" not in context_format
    assert "Anticorruption Layer, not Conformist" in context_format_flat
    assert "schema alone does not establish an Open-host Service" in context_format_flat
    assert "executable procedure, algorithm specifications" in context_format_flat
    adr_format = (CUSTOM / "domain-modeling/ADR-FORMAT.md").read_text(
        encoding="utf-8"
    )
    adr_format_flat = " ".join(adr_format.split())
    assert domain.count("(./ADR-FORMAT.md)") == 1
    for contract in (
        "Hard to reverse",
        "Surprising without context",
        "Real trade-off",
        "separate explicit approval",
        "all controlling successors and its exact remaining scope",
        "accepted only while that scope is nonempty",
        "superseded by the controlling successors",
    ):
        assert contract in adr_format_flat
    assert "executable specification" in adr_format_flat
    for stale_packet in (
        "Semantic outcome:",
        "Persistence outcome:",
        "persist authorized",
        "render only",
        "offer only",
    ):
        assert stale_packet not in domain
    root_context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    assert "Reconcile with routed current records" not in root_context
    assert "partial-successor links" not in root_context

    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    assert "`skill-router`, `grill-with-docs`, `audit-codebase`, `repo-bootstrap`" in relationships
    pack = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    audit_edge = next(
        row for row in pack["relationships"] if row["relationship_id"] == "REL-093"
    )
    assert "context-write authority" in audit_edge["input_packet"]
    assert "separate ADR approval" in audit_edge["input_packet"]


def test_instantiated_domain_helper_preserves_routing_and_ownership() -> None:
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())

    assert "**Configured layout:** single-context." in domain
    assert "setup-file:" not in domain
    for contract in (
        "Missing domain records are not setup gaps.",
        "$domain-modeling` owns settled domain meaning",
        "Repo Bootstrap only configures this route.",
        "`CONTEXT.md`",
        "`CONTEXT-MAP.md`",
        "`docs/adr/`",
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
        "several coupled unresolved questions",
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
    unresolved = "disposable runnable probe or comparative measurement"
    assert unresolved in relationships
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
    assert "Use only when the user explicitly requests" in convergent
    assert "fixed code candidate" in assurance_summary
    assert "two fresh whole-candidate" in assurance_summary
    assert "No workflow selects High-Assurance Review automatically" in assurance_summary
    assert not (CUSTOM / "change-review/SMELL-BASELINE.md").exists()
    assert "formal review" in review_summary.lower()
    assert "Implementation-worker profiles remain with implementation dispatch" in review_summary


def test_spawned_agents_use_runtime_defaults_without_pack_profiles() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    implement_flat = " ".join(implement.split())
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "If the user explicitly requests subagents" in implement_flat
    assert "delegate only a bounded edit that one worker can own" in implement_flat
    assert "fresh capable worker under the active runtime" in implement_flat
    assert "unless the user selects a model" in implement_flat
    assert not (CUSTOM / "parallel-implement/scripts/run_ledger.py").exists()
    assert not (CUSTOM / "parallel-implement/references/RUNTIME-PROFILES.md").exists()
    assert not (CUSTOM / "parallel-implement/assets/luna_max.toml").exists()
    assert not (ROOT / ".codex/agents/luna_max.toml").exists()
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
    assert "Reuse valid candidate-bound proof" in convergent_flat
    assert "FINDING-CONTRACT.md" in convergent
    assert "Do not activate from PR presence" in convergent_flat
    assert "novelty, or risk" in convergent_flat
    assert "supported-risk candidate needs read-only judgment" in router
    assert re.search(
        r"(?m)^\| The user explicitly requests high-assurance, heavy, or final review "
        r"of one fixed complete code candidate \| `\$high-assurance-review` \|$",
        router,
    )


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
    assert "**Status**: superseded in part by ADR-0017" in adr
    current_adr = (
        ROOT
        / "docs/adr/0017-parallel-delivery-keeps-structural-isolation-not-dispatch-ceremony.md"
    ).read_text(encoding="utf-8")
    assert "**Status**: accepted" in current_adr
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

    flattened = " ".join(convergent.split())
    assert "Dispatch exactly two fresh, read-only reviewers" in flattened
    assert "same pinned candidate and factual brief" in flattened
    assert "use a fresh task or context" in flattened
    assert "separate from every identified author" in flattened
    assert "freshness or required separation cannot be established" in flattened
    assert "identity and independence basis" in flattened
    assert "Each applies Change Review directly" in flattened
    assert "without spawning another reviewer" in flattened
    assert "actor and task IDs" not in flattened
    assert "return contract:" not in flattened


def test_high_assurance_review_has_root_guard_bounded_capacity_and_risk() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    convergent_flat = " ".join(convergent.split())

    assert "Run as the top-level coordinator" in convergent_flat
    assert "Reviewers do not invoke High-Assurance Review" in convergent_flat
    assert "exactly two fresh" in convergent_flat
    assert (
        "caller retains repair, merge, tracker, release, residual-risk acceptance"
        in convergent_flat
    )
    assert "Add at most one specialist" in convergent_flat
    assert "user explicitly names one bounded specialist question" in convergent_flat
    assert "Do not activate from PR presence" in convergent_flat
    assert "novelty, or risk" in convergent_flat
    for retired in (
        "valid reviewer quorum",
        "actor and task IDs",
        "fresh unbiased replacement",
        "har-spec-reviewer",
        "har-standards-reviewer",
        "har-specialist",
    ):
        assert retired not in convergent
    assert not (CUSTOM / "change-review/ADVISORY-CONTRACT.md").exists()


def test_audit_codebase_is_thorough_incremental_html_atlas() -> None:
    skill_dir = CUSTOM / "audit-codebase"
    audit = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    defect = (skill_dir / "DEFECT-CONTRACT.md").read_text(encoding="utf-8")
    quality = (skill_dir / "QUALITY-LENS.md").read_text(encoding="utf-8")
    candidate = (skill_dir / "CANDIDATE-CONTRACT.md").read_text(encoding="utf-8")
    metadata = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    report = (skill_dir / "HTML-REPORT.md").read_text(encoding="utf-8")
    report_quick = (skill_dir / "REPORT-QUICK-REFERENCE.md").read_text(
        encoding="utf-8"
    )
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    audit_frontmatter = audit.split("---", 2)[1]

    assert not implicit_policy(skill_dir)
    assert re.findall(
        r"(?m)^## (Map the repository|Audit one subsystem|Analyze one candidate)$",
        audit,
    ) == ["Map the repository", "Audit one subsystem", "Analyze one candidate"]
    assert "$to-tickets" not in audit_frontmatter
    assert "An invalid or stale selection changes nothing" in " ".join(audit.split())
    assert "The user chooses every subsystem and candidate" in audit
    assert "Use [Report CLI](REPORT-QUICK-REFERENCE.md)" in audit
    assert "Never scrape or hand-edit the HTML" in report_quick
    assert "Never invoke it, publish tickets" in " ".join(audit.split())
    assert "start implementation" in audit

    for reference in (
        "RELIABILITY-LENS.md",
        "QUALITY-LENS.md",
        "DEFECT-CONTRACT.md",
        "CANDIDATE-CONTRACT.md",
        "HTML-REPORT.md",
        "REPORT-QUICK-REFERENCE.md",
    ):
        assert f"({reference})" in audit
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
    assert "selected objective's current source identity" in " ".join(defect.split())
    assert "user-selectable improvement boundary" in candidate
    assert "span several" in " ".join(candidate.split())
    assert "sibling callers" in audit
    assert "cross-subsystem" in audit
    assert "$to-tickets" not in metadata

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    relationships = {
        row["relationship_id"]: row for row in contract["relationships"]
    }
    assert "REL-028" not in relationships
    assert relationships["REL-056"]["verb"] == "Recommend and stop"
    assert "bounded implementation-ready change" in relationships["REL-056"]["entry_condition"]
    assert "implementation unstarted" in relationships["REL-056"]["return_packet"]
    assert "user-selected candidate analysis" in relationships["REL-047"]["entry_condition"]
    capability = next(
        row for row in contract["capabilities"] if row["capability_id"] == "CAP-017"
    )
    assert "user-selected candidate analysis" in capability["entry_conditions"][0]
    assert "no downstream work started" in capability["completion_return"]
    selected_skill = next(
        row for row in contract["selected_skills"] if row["skill_id"] == "SK-017"
    )
    assert "no downstream work starts" in selected_skill["completion_condition"]

    assert "Embedded canonical JSON" in " ".join(report.split())
    assert "The helper owns rendering" in report
    assert "Agents use [Report CLI]" in report
    for state_token in (
        "mapped",
        "audited",
        "presented",
        "analyzed",
    ):
        assert state_token in report

    for command in (
        "inspect",
        "source-identity",
        "inventory",
        "render-report",
        "audit-subsystem",
        "analyze-candidate",
    ):
        assert command in report_quick
    assert "Never scrape or hand-edit the HTML" in report_quick
    assert re.search(
        r"(?m)^\| A repository needs a whole-system HTML map, one user-selected "
        r"subsystem audit, or one user-selected audit-candidate analysis "
        r"\| `\$audit-codebase` \|$",
        router,
    )

def test_high_assurance_review_returns_a_caller_usable_decision() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    formal = (
        CUSTOM / "change-review/references/FORMAL-REVIEW.md"
    ).read_text(encoding="utf-8")
    decision_section = convergent.split("Return exactly one decision", 1)[1].split(
        "Return the candidate identity", 1
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
    assert "blocker takes precedence over unrelated" in formal_decision_section
    assert "A blocker takes precedence over unrelated" in " ".join(convergent.split())
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
    for field in (
        "candidate identity",
        "coverage",
        "admitted findings",
        "material rejected or disputed claims",
        "checks and evidence limits",
        "residual risk",
        "drift result",
        "decision",
    ):
        assert field in convergent
    assert "Carry prior admitted finding IDs" in convergent
    assert "review the full new candidate" in " ".join(convergent.split())
    assert "and one state:" not in convergent
    assert "admitted `P0` or `P1`" in convergent
    assert "Nonblocking findings remain visible" in " ".join(convergent.split())
    assert "Disposition every reviewer finding candidate" in " ".join(convergent.split())


def test_audit_stops_before_review_and_implementation_closeout() -> None:
    candidate = (CUSTOM / "audit-codebase/CANDIDATE-CONTRACT.md").read_text(
        encoding="utf-8"
    )
    quick = (CUSTOM / "audit-codebase/REPORT-QUICK-REFERENCE.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(candidate.split())
    quick_normalized = " ".join(quick.split())

    for retired in (
        "close-candidate",
        "formal_review_residual_risk_acceptance",
        "tracker-frontier",
        "ready-graph",
        "implementation_outcome",
    ):
        assert retired not in normalized
        assert retired not in quick_normalized
    assert "start implementation" in normalized


def test_high_assurance_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "high-assurance-review/SKILL.md").read_text(
        encoding="utf-8"
    )

    pin = " ".join(
        convergent.split("## 1. Fix", 1)[1].split("## 2. Ground", 1)[0].split()
    )
    for surface in (
        "fixed point",
        "head commit",
        "tree",
        "selected diff bytes",
        "exact base, head, and diff",
        "`HEAD`",
        "staged and unstaged changes",
        "status",
        "untracked path and its bytes",
    ):
        assert surface in pin
    verify = " ".join(convergent.split("## 5. Gate", 1)[1].split())
    assert "Recheck mutable candidate identity using the original resolution" in verify
    assert "do not recapture" in verify


def test_implement_uses_condition_triggered_change_review() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = implement.split("## 4. Prove", 1)[1].split("## 5. Finish", 1)[0]
    flat = " ".join(review.split())

    assert "user or repository requires it" in flat
    assert "concrete unresolved shared-contract or migration judgment" in flat
    assert "Pin the clean candidate" in flat
    assert "let Change Review own its procedure" in flat
    assert "Multiple authors alone do not trigger review" in flat
    assert "`Formal review: yes`" not in flat


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
    assert "one root integrator" in parallel["interface"]["default_prompt"]
    assert "focused integrated proof" in parallel["interface"]["default_prompt"]
    assert assurance["policy"]["allow_implicit_invocation"] is False
    assert assurance["interface"]["default_prompt"].startswith("Explicitly use")


def test_tdd_discloses_test_reference_only_for_an_evidence_gap() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tests = (CUSTOM / "tdd/references/TEST-SHAPE.md").read_text(encoding="utf-8")
    doubles = (CUSTOM / "tdd/references/TEST-DOUBLES.md").read_text(
        encoding="utf-8"
    )
    synthesis = (ROOT / "docs/synthesis/skills/tdd.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    tdd_flat = " ".join(tdd.split())

    description = tdd.split("---", 2)[1]
    assert "explicitly requests TDD" in description
    assert "repository policy requires TDD" in description
    assert "integration tests" in description
    assert "alone do not trigger it" in description
    assert re.findall(r"(?m)^## ([A-Z]+)$", tdd) == ["RED", "GREEN", "REFACTOR"]
    assert "No observed behavioral RED, no TDD" in tdd
    assert "realistic production break it should catch" in tdd_flat
    assert "An honest gap is better than a bad test" in tdd_flat
    assert "observed RED, final GREEN and nearby proof" in tdd_flat
    assert "references/TEST-SHAPE.md" in tdd
    assert "references/TEST-DOUBLES.md" in tdd
    assert (
        'TDD --> TddRefs["references/TEST-SHAPE.md<br/>'
        'references/TEST-DOUBLES.md"]'
    ) in relationships
    assert 'TddRefs["tests.md / mocking.md / refactoring.md"]' not in relationships
    for retired in ("tests.md", "mocking.md", "refactoring.md"):
        assert not (CUSTOM / "tdd" / retired).exists()
    tests_flat = " ".join(tests.split())
    assert "Derive the expected result independently" in tests_flat
    assert "does not establish correctness" in tests_flat
    assert "Test count and coverage percentage are not targets" in tests_flat
    doubles_flat = " ".join(doubles.split())
    assert "Keep owned in-process code real" in doubles_flat
    assert "only at a real boundary adapter" in doubles_flat
    assert "interaction is part of the contract" in doubles_flat
    assert skill_pack_contract.tree_hash(CUSTOM / "tdd") in synthesis
    assert "Pack composition revision 16" in synthesis


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
    for owner in (tdd, implement, router, relationships):
        assert "explicit" in owner.lower()
        assert "repository policy" in owner.lower()
        for trigger in ("TDD", "test-first work", "RED-GREEN-REFACTOR"):
            assert trigger in owner
    for trigger in ("TDD", "test-first work", "RED-GREEN-REFACTOR"):
        assert trigger not in parallel
    assert "integration tests, regression tests, or coverage alone do not trigger" in tdd
    assert "safe red-capable check" in " ".join(tdd.split())
    assert "Otherwise implement directly and use ordinary tests" in " ".join(
        implement.split()
    )
    assert "for each materially distinct settled behavior and independent oracle" in (
        " ".join(implement.split())
    )
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
        ("REL-064", "skill-router", "Recommend and stop"),
    }
    for relationship in inbound.values():
        assert "requires TDD" in relationship["entry_condition"]
        assert "independent oracle" in relationship["entry_condition"]
        if relationship["verb"] == "Invoke":
            assert "inner loop" in relationship["entry_condition"]
        assert "asks only for tests" in relationship["wrong_condition"]


def test_tdd_stops_at_a_material_gap_without_routing() -> None:
    tdd = (CUSTOM / "tdd/SKILL.md").read_text(encoding="utf-8")
    tdd_flat = " ".join(tdd.split())
    assert "stop before production mutation and report that material gap" in tdd_flat
    assert "behavior, oracle, authority, or a safe red-capable check" in tdd_flat
    assert "do not claim TDD" in tdd_flat
    for retired_status in ("diagnosis-required", "design-evidence-required"):
        assert retired_status not in tdd
    for callee in (
        "$audit-codebase",
        "$codebase-design",
        "$diagnosing-bugs",
        "$prototype",
        "$simplify-code",
    ):
        assert callee not in tdd


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


def test_hillclimb_owns_only_bounded_comparable_improvement_campaigns() -> None:
    skill_dir = CUSTOM / "hillclimb"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    hillclimb = next(
        selected
        for selected in contract["selected_skills"]
        if selected["canonical_name"] == "hillclimb"
    )
    names = {
        selected["skill_id"]: selected["canonical_name"]
        for selected in contract["selected_skills"]
    }

    assert not implicit_policy(skill_dir)
    assert 3 <= len(re.findall(r"(?m)^## \d+\. (.+)$", skill)) <= 6
    assert hillclimb["invocation_mode"] == "explicit-only"
    assert hillclimb["relationship_ids"] == []
    inbound = {
        (names[row["caller_skill_id"]], row["verb"]): row
        for row in contract["relationships"]
        if row["target_skill_id"] == hillclimb["skill_id"]
    }
    assert set(inbound) == {("skill-router", "Recommend and stop")}
    blueprint = pack_contract.contract_blueprint(contract, hillclimb["skill_id"])
    assert "ECG-009" in {
        issue["issue_id"] for issue in blueprint["slice"]["issues"]
    }


def test_wizard_is_an_explicit_template_free_human_procedure_leaf() -> None:
    skill_dir = CUSTOM / "wizard"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    wizard = next(
        selected
        for selected in contract["selected_skills"]
        if selected["canonical_name"] == "wizard"
    )

    assert not implicit_policy(skill_dir)
    assert 3 <= len(re.findall(r"(?m)^## \d+\. (.+)$", skill)) <= 6
    assert not any(path.name == "template.sh" for path in skill_dir.rglob("*"))
    assert wizard["invocation_mode"] == "explicit-only"
    assert wizard["relationship_ids"] == []
    inbound = {
        (relationship["caller_skill_id"], relationship["verb"])
        for relationship in contract["relationships"]
        if relationship["target_skill_id"] == wizard["skill_id"]
    }
    assert inbound == {("SK-025", "Recommend and stop")}
    assert all(
        relationship["caller_skill_id"] != wizard["skill_id"]
        for relationship in contract["relationships"]
    )
    blueprint = pack_contract.contract_blueprint(contract, wizard["skill_id"])
    assert "ECG-009" in {
        issue["issue_id"] for issue in blueprint["slice"]["issues"]
    }


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
    tdd_tests = (CUSTOM / "tdd/references/TEST-SHAPE.md").read_text(
        encoding="utf-8"
    )

    assert [
        match.group(1)
        for match in re.finditer(r"(?m)^## \d+\. ([A-Za-z]+)$", diagnosing)
    ] == ["Reproduce", "Discriminate", "Resolve", "Return"]
    assert "corrective RED" in tdd_tests
    assert "`diagnosis-required`" not in tdd
    assert "$diagnosing-bugs" not in tdd
    assert "No observed behavioral RED" in tdd
    assert "Ordinary bug investigation" in implement_flat
    assert "original feedback loop" in diagnosing_flat
    assert "stop before production mutation" in tdd_flat

    diagnosis_producers = (
        CUSTOM / "implement/SKILL.md",
        CUSTOM / "parallel-implement/SKILL.md",
        CUSTOM / "simplify-code/SKILL.md",
        CUSTOM / "resolving-merge-conflicts/SKILL.md",
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
    assert "return `not needed`" in normalized
    assert "Create nothing" in normalized
    assert "several valuable implementation slices" in normalized
    assert "otherwise recommend unstarted `$implement`" in normalized
    assert "Reuse only when exactly one parent matches" in normalized
    assert "Perform at most one parent create" in normalized
    assert "Never retry an indeterminate create blindly" in normalized
    completion = " ".join(to_spec.split("## Completion", 1)[1].split())
    assert "`not needed` returns the exact bounded source" in completion
    assert "published or reused parent" in completion
    assert "Require one returned identity and pointer" in normalized
    assert "$codebase-design" not in to_spec
    assert ".tmp/to-spec" not in to_spec


def test_to_spec_handoff_keeps_ticket_design_downstream() -> None:
    to_spec = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    to_tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    spec = " ".join(to_spec.split())
    tickets = " ".join(to_tickets.split())
    spec_lower = spec.lower()
    tickets_lower = tickets.lower()

    for owned_concept in (
        "source identity and owners",
        "problem, outcome, scope, and exclusions",
        "settled behavior, decisions, constraints",
        "caller-visible interfaces",
        "observable acceptance",
        "residual uncertainty",
    ):
        assert owned_concept.lower() in spec_lower
    for downstream_concept in (
        "ticket slices",
        "expected writes",
        "concrete commands",
        "test ownership",
        "dependency order",
        "implementation technique",
    ):
        assert downstream_concept.lower() in spec_lower
    for ticket_owner in (
        "current behavior owner",
        "fewest cohesive tickets",
        "observable acceptance",
        "true blockers",
        "dependent consumes a required predecessor outcome",
        "first actionable ticket",
    ):
        assert ticket_owner.lower() in tickets_lower
    assert "Paths may support a source claim" in spec
    assert "## Code Quality Contract" not in to_spec
    assert "Return `ready spec`" in spec
    assert "`published-spec`" not in spec


def test_implementation_closeout_requires_the_spec_axis() -> None:
    formal = (
        CUSTOM / "change-review/references/FORMAL-REVIEW.md"
    ).read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "`Spec required: yes | no`" in formal
    assurance_flat = " ".join(assurance.split())
    assert "governing issue or specification" in assurance_flat
    assert "missing or conflicting source" in assurance_flat
    assert "Skip an optional absent source" in assurance_flat
    assert "accepted request is always required" in assurance_flat
    assert "record why it is optional" in assurance_flat
    assert "let Change Review own its procedure" in parallel
    assert "`Spec required: yes`" not in parallel


def test_implementation_workflows_keep_local_proof_owners() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel_tracker = " ".join(
        (CUSTOM / "parallel-implement/references/TRACKER-DELIVERY.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "Trace the real callers, data flow, and existing proof seam" in implement
    assert (
        "demonstrated caller dependence as compatibility and migration evidence"
        in implement
    )
    assert "Run the nearest useful check" in implement
    assert "Inspect the real output or caller path" in implement
    assert "run proof invalidated by that transition" in parallel
    assert "real callers, and material interactions" in parallel
    assert "Do not repeat worker proof that remains valid" in parallel


def test_implement_owns_one_plain_worker_handoff_without_parallel_loading_it() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    handoff_path = CUSTOM / "implement/references/WORKER-HANDOFF.md"
    handoff = handoff_path.read_text(encoding="utf-8")

    assert handoff_path.is_file()
    assert "[Plain Worker Handoff](references/WORKER-HANDOFF.md)" in implement
    assert "WORKER-HANDOFF.md" not in parallel
    assert "If the user explicitly requests subagents" in " ".join(implement.split())
    assert "The root inspects the returned diff and proof" in " ".join(implement.split())
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
    assert "scope, allowed writes, acceptance" in parallel
    assert "real callers, and material interactions" in parallel
    assert (
        "Call the item complete only when the requested behavior works"
        in implement
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
    assert "fewest cohesive tickets" in tickets
    assert "smallest integrated design" in implement
    assert "Remove code made obsolete by the change" in implement
    assert "complete replacement or removal" in review
    assert "Parallelism is useful only when independent work saves more time" in (
        " ".join(parallel.split())
    )
    assert "ToSpec --> Contract" in relationships
    assert "ToTickets --> Contract" in relationships


def test_ticket_and_delivery_packets_are_compact_and_preserve_repairs() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    tickets_flat = " ".join(tickets.split())
    implement_flat = " ".join(implement.split())
    parallel_flat = " ".join(parallel.split())

    for field in (
        "one outcome and observable acceptance",
        "source identity, fixed decisions, scope",
        "true blockers",
        "material compatibility, migration, trust, authority, or recovery constraints",
    ):
        assert field in tickets_flat
    assert "omit inapplicable sections" in tickets_flat
    assert "graph-level Repair generation budget" not in tickets_flat
    assert "Create nothing" in tickets_flat
    for retired in ("**Grounding:**", "5,500", "Ready-for-human", "state matrix"):
        assert retired not in tickets
    assert "Use the caller's selection as the scope fence" in implement_flat
    assert "Direct work creates no tracker state" in implement_flat
    assert "Return a concise summary" in implement_flat
    assert "campaign ledger" not in parallel_flat
    assert "Worker prose is evidence, not state" in parallel_flat
    assert "Send vague work" in parallel_flat
    assert "A caller with campaign claims retains them throughout repair" in tickets_flat


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
    audit_flat = " ".join(audit.split())
    assert "Use read-only subagents only when the user requests them" in audit_flat
    assert "Inspect their evidence before relying on it" in audit_flat


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
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )

    assert implicit_policy(skill_dir)
    assert "status, explanation, or review request permits no mutation" in skill_flat
    assert "Staging and native continuation require a separate explicit request" in skill_flat
    assert "already-prepared or automatically staged resolution" in skill_flat
    assert "When resolution was requested, repair" in skill_flat
    assert "active conflicted operation or unmerged index" in implement
    assert "hand off to `$resolving-merge-conflicts`" in implement
    assert "`git ls-files -u`" in skill
    assert "[OPERATIONS.md](OPERATIONS.md)" in skill
    assert "## Operation roles" in operations
    assert "## Special conflict types" in operations
    assert "Never use `git add -A`" in skill
    assert "Rebase" in operations and "commit being replayed" in operations
    assert "A stage may be absent" in operations
    assert "Rename conflicts may span old and new paths" in operations
    assert "`rerere`, mergetool, or automatic merge result" in operations
    for retired in (
        "Compose",
        "Transform",
        "Prefer",
        "prepared reconciliation",
        "finished operation",
        "route mismatch",
        "diagnosis-required",
    ):
        assert retired not in skill


def test_portable_fallback_remains_standalone_from_the_repo_contract() -> None:
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(
        encoding="utf-8"
    )
    validator = (CUSTOM / "repo-bootstrap/scripts/validate_setup.py").read_text(
        encoding="utf-8"
    )
    fallback_flat = " ".join(fallback.split())
    contract_flat = " ".join(contract.split())

    assert fallback.startswith("# Global Codex Instructions\n")
    assert "when the skill pack is not installed" in fallback_flat
    assert "each repository its own short `AGENTS.md`" in fallback_flat
    assert "portable-contract-owner" in validator
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
        "Apply the deletion test",
        "Trust internal types and established invariants",
        "Run the nearest useful check",
        "name the realistic behavior break it catches",
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


def test_tracer_bullet_is_a_conditional_learning_role_not_a_slice_alias() -> None:
    contract = " ".join(
        (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8").split()
    )
    tickets = " ".join(
        (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    readme = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())

    assert "tracer bullet** only when a named risk warrants early feedback" in contract
    assert "learning role, not a substitute for acceptance" in contract
    assert "Otherwise omit the learning role" in tickets
    assert "tracer bullet" not in parallel
    assert "the terms are not synonyms" in readme
    assert "deliver observable vertical slices" not in readme


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


def test_triage_is_lean_and_preserves_tracker_boundaries() -> None:
    triage = (CUSTOM / "triage/SKILL.md").read_text(encoding="utf-8")
    attention = (CUSTOM / "triage/ATTENTION-SCAN.md").read_text(encoding="utf-8")
    brief = (CUSTOM / "triage/AGENT-BRIEF.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "triage")
    assert "## 1. Read the intake" in triage
    assert "## 5. Verify and stop" in triage
    assert "A failed reproduction does not prove a report false" in " ".join(
        triage.split()
    )
    assert "$diagnosing-bugs" in triage
    assert "$change-review" in triage
    assert "$to-tickets" in triage
    assert "every durable effect authorizes only those effects" in " ".join(
        triage.split()
    )
    assert "Do not create a false-ready or invalid item" in " ".join(triage.split())
    assert "changes the disposition, note, roles, or close state" in " ".join(
        triage.split()
    )
    assert "do not retry blindly" in triage
    assert "without changing tracker state" in attention
    assert "observable acceptance" in brief
    assert "without a new product decision" in " ".join(brief.split())
    assert "Add interface," in brief
    for retired in (
        "mutation packet",
        "Ready Gate",
        "scan-complete",
        "decision-required",
        "mutation-complete",
        "blocked-partial",
        ".out-of-scope/",
        "generated by AI during triage",
    ):
        assert retired not in triage + attention + brief
    for retired_path in (
        "SPECIFIC-ITEM.md",
        "QUICK-OVERRIDE.md",
        "OUT-OF-SCOPE.md",
    ):
        assert not (CUSTOM / "triage" / retired_path).exists()

    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    projection_edges = set(
        re.findall(
            r"(?m)^\| `([a-z0-9-]+)` \| (Recommend and stop) \| `\$([a-z0-9-]+)` \|",
            relationships,
        )
    )
    assert {
        edge for edge in projection_edges if edge[0] == "triage"
    } == {
        ("triage", "Recommend and stop", "change-review"),
        ("triage", "Recommend and stop", "diagnosing-bugs"),
        ("triage", "Recommend and stop", "repo-bootstrap"),
        ("triage", "Recommend and stop", "to-tickets"),
    }

    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    names = {
        skill["skill_id"]: skill["canonical_name"]
        for skill in contract["selected_skills"]
    }
    machine_edges = {
        (names[row["caller_skill_id"]], row["verb"], names[row["target_skill_id"]])
        for row in contract["relationships"]
        if names[row["caller_skill_id"]] == "triage"
    }
    assert machine_edges == {
        ("triage", "Recommend and stop", "change-review"),
        ("triage", "Recommend and stop", "diagnosing-bugs"),
        ("triage", "Recommend and stop", "repo-bootstrap"),
        ("triage", "Recommend and stop", "to-tickets"),
    }
    relationship_ids = {
        row["relationship_id"] for row in contract["relationships"]
    }
    assert not relationship_ids.intersection(
        {"REL-084", "REL-097", "REL-098", "REL-099"}
    )


def test_mutating_workflows_require_proportional_readback() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel_tracker = " ".join(
        (CUSTOM / "parallel-implement/references/TRACKER-DELIVERY.md")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "Read back every durable external mutation" in implement
    assert "recovery path before an operation that can partially succeed" in implement
    assert "read back integration `HEAD`" in parallel
    assert "read the result back" in parallel_tracker

    for name in ("to-spec", "to-tickets", "triage", "wayfinder"):
        text = (CUSTOM / name / "SKILL.md").read_text(encoding="utf-8")
        assert "read-back" in text.lower(), name


def test_to_tickets_is_proportional_and_preserves_actionable_frontier() -> None:
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(tickets.split())
    synthesis = (ROOT / "docs/synthesis/skills/to-tickets.md").read_text(
        encoding="utf-8"
    )

    assert not implicit_policy(CUSTOM / "to-tickets")
    assert "one bounded outcome and proof path" in tickets
    assert "Create nothing" in flat
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", tickets) == [
        "Admit",
        "Trace",
        "Slice",
        "Approve",
        "Publish",
    ]
    assert "one bounded fresh `$implement` run" in flat
    assert "accept such a graph unchanged" in flat
    assert "skip Slice, Approve, and Publish, then use the common return selection" in flat
    assert "present the revised graph for approval" in flat
    assert "already approved these exact effects or explicitly waived preview" in flat
    assert "`reuse` or `create` or `update` disposition" in flat
    assert "bind each new identity through immediate read-back" in flat
    assert "apply and read back `ready-for-agent` only" in flat
    assert "refetch the parent and children" in flat
    assert "stop further mutation" in flat
    assert "caller-held resumable ticket" in flat
    assert "if it gates any ticket" in flat
    assert "preserve any caller-held assignee" in flat
    assert flat.index("If the settled source itself establishes") < flat.index(
        "Once a graph is warranted, read `docs/agents/issue-tracker.md` and"
    )
    assert flat.index("configured inspect and read-back routes") < flat.index(
        "Inspect the intended parent and existing children"
    )
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    implement_edge = next(
        edge for edge in contract["relationships"] if edge["relationship_id"] == "REL-081"
    )
    for field in ("entry_condition", "input_packet", "return_packet"):
        assert "bounded direct item" in implement_edge[field].lower()
    parallel_edge = next(
        edge for edge in contract["relationships"] if edge["relationship_id"] == "REL-082"
    )
    assert "approved or exact-reuse verified graph" in parallel_edge["entry_condition"]
    to_tickets_contract = next(
        skill for skill in contract["selected_skills"] if skill["canonical_name"] == "to-tickets"
    )
    assert "approved or exact-reuse actionable graph" in to_tickets_contract[
        "completion_condition"
    ]
    assert "approved or exact-reuse graph" in flat
    current_reconciliation = synthesis.split(
        "The decision-bearing content is bounded below", 1
    )[0]
    assert exact_tree_hash(CUSTOM / "to-tickets") in current_reconciliation


def test_to_spec_canonical_is_lean_and_experimental_evidence_stays_frozen() -> None:
    canonical = (CUSTOM / "to-spec/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(canonical.split())
    synthesis = (ROOT / "docs/synthesis/skills/to-spec.md").read_text(
        encoding="utf-8"
    )

    assert "return `not needed`" in flat
    assert "one bounded implementation" in flat
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", canonical) == [
        "Admit",
        "Read",
        "Write",
        "Publish",
        "Completion",
    ]
    assert "Perform at most one parent create" in flat
    assert "Create no children" in flat
    assert "$codebase-design" not in canonical
    assert ".tmp/to-spec" not in canonical
    assert "Verified Source Correction" not in canonical
    assert "source-gap" not in canonical
    assert flat.index("If the source already defines one bounded implementation") < flat.index(
        "Read `docs/agents/issue-tracker.md` only after the durable-parent branch wins"
    )
    current_reconciliation = synthesis.split("Status: Deploy Prompt 4", 1)[0]
    assert exact_tree_hash(CUSTOM / "to-spec") in current_reconciliation

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
    assert "Concurrent workers do not" in " ".join(parallel.split())
    assert "dispatch successors" in " ".join(parallel.split())


def test_parallel_implement_separates_plain_context_checkout_and_review() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lanes = (skill_dir / "references/AGENT-LANES.md").read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    assert re.findall(r"(?m)^## (.+)$", parallel) == [
        "Admit", "Isolate", "Dispatch", "Land", "Prove", "Finish"
    ]
    assert "one root integrator" in flat.lower()
    assert "Multiple workers alone do not trigger review" in flat
    assert "let Change Review own its procedure" in flat
    assert "WORKER-HANDOFF.md" not in parallel
    assert "quick pytest collection" not in " ".join(lanes.split())
    assert not (skill_dir / "references/RUNTIME-PROFILES.md").exists()
    assert not (skill_dir / "scripts/run_ledger.py").exists()
    assert not (skill_dir / "references/RUN-LEDGER.md").exists()
    assert not (skill_dir / "references/WORKER-BRIEF.md").exists()


def test_parallel_implement_owns_recovery_authority_and_outcome_gates() -> None:
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    assert "Silence or a missed checkpoint triggers inspection" in flat
    assert "stop the prior actor, confirm it stopped" in flat
    assert "Never run two actors on one item" in flat
    assert "Let healthy active workers finish" in flat
    assert "cleanup failure or residual helper-owned state is unfinished" in flat
    assert "report the exact retry" in flat
    for required_resume_fact in (
        "integration `HEAD`",
        "actor, lane, base",
        "commit or dirty state",
        "landing state",
        "blocker",
        "next safe action",
    ):
        assert required_resume_fact in flat
    for retired in ("`complete`", "`partial`", "`blocked`", "campaign ledger"):
        assert retired not in parallel


def test_parallel_implement_has_one_lean_worktree_lifecycle() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lanes = (skill_dir / "references/AGENT-LANES.md").read_text(encoding="utf-8")
    lane_script = (skill_dir / "scripts/lane_worktree.py").read_text(encoding="utf-8")
    codex_config = (ROOT / ".codex/config.toml").read_text(encoding="utf-8")
    flat = " ".join(lanes.split())

    assert "Run only at the top-level root" in parallel
    assert "lane_worktree.py prepare" in flat
    assert "lane_worktree.py cleanup" in flat
    assert "`temp_root`, `pytest_basetemp`, and `pytest_cache`" in lanes
    assert "quick pytest collection" not in flat
    assert "Start the worker only when" in flat and "`ok: true`" in flat
    assert "--oldest" not in lanes and "--completed" in lanes
    assert "Dirty, unintegrated, active, or uncertain work stays in place" in flat
    assert "exact retry after Git removed the worktree" in flat
    assert 'operations.add_parser("prepare")' in lane_script
    assert 'operations.add_parser("cleanup")' in lane_script
    assert '"--collect-only"' not in lane_script and '"--oldest"' not in lane_script
    assert "lane_state(root, worktree.name)" in lane_script
    assert "shutil.rmtree(state)" in lane_script and "--global" not in lane_script
    assert not (skill_dir / "assets/luna_max.toml").exists()
    expected_lane_root = str(Path(ROOT.anchor) / "pi" / "pas-001" / "wt")
    assert expected_lane_root.replace("\\", "\\\\") in codex_config


def test_parallel_implement_exposes_live_frontier_and_closeout_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    tracker_delivery = (
        skill_dir / "references/TRACKER-DELIVERY.md"
    ).read_text(encoding="utf-8")
    tracker_delivery_flat = " ".join(tracker_delivery.split())
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    tickets_flat = " ".join(tickets.split())
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    flat = " ".join(parallel.split())

    assert not implicit_policy(skill_dir)
    assert "ready frontier" in flat
    assert "non-empty ready frontier" in flat
    assert "independent work saves more time than coordination costs" in flat
    assert "run the affected items serially" in flat
    assert "complete tracker-backed parent graph" in flat
    assert "claim the parent and initial ready frontier" in tracker_delivery_flat
    assert "demonstrably retained by this run" in tracker_delivery_flat
    assert "Stop on any other or ambiguous ownership" in tracker_delivery_flat
    assert "confirm one current actor before dispatch" in tracker_delivery_flat
    assert "Leave blocked descendants unclaimed" in tracker_delivery_flat
    assert "only when every child is implemented" in tracker_delivery_flat
    assert "a dependent item starts only after its predecessors land" in flat
    assert "Accept that direct landing without applying its commit again" in flat
    assert "Verify and land accepted worker commits one at a time" in flat
    assert "Complete when every accepted item is landed" in flat
    assert "every named completed lane is safely removed" in flat
    assert re.search(
        r"(?m)^\| One explicit fixed delivery set has at least two accepted "
        r"implementation items and a non-empty ready frontier "
        r"\| `\$parallel-implement` \|$",
        router,
    )
    assert "selected directly or as a Ready-for-agent item" in router
    assert "recommend `$parallel-implement` only when the user explicitly requested" in tickets_flat
    assert "owns live concurrency and integration" in tickets_flat
    assert "`to-tickets` | Recommend and stop | `$parallel-implement`" in relationships


def test_parallel_uses_current_landed_state_without_a_dependency_overlay() -> None:
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "dependencies whose changes are already integrated" in parallel
    assert "recompute the ready frontier" in parallel
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
        assert "expected to retry, resume, or restart" in normalized
        assert "converge on rerun without duplicate effects" in normalized
        assert "Handle state, retry, recovery, cancellation, concurrency" not in normalized
    flat = " ".join(tickets.split())
    assert "material compatibility, migration, trust, authority, or recovery constraints" in flat
    assert "Use a matrix" not in flat
    assert "Cartesian" not in flat


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
    assert "follow the claim and closeout rules" in flat
    assert "do not push without separate authority" in flat
    assert "Read back every durable external mutation" in flat
    assert "recovery path before an operation that can partially succeed" in flat
    assert "Call the item complete only when the requested behavior works" in flat
    assert "Return a concise summary" in flat
    assert "Outcome: complete | partial | blocked" not in flat
    assert "let Change Review own its procedure" in flat
    assert "Mode: remediation" not in flat


def test_parallel_relationships_keep_review_conditional_and_shaping_external() -> None:
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

    assert "Multiple workers alone do not trigger review" in flat
    assert "vague work, unsettled meaning, missing dependencies" in flat
    assert "leave shaping or graph repair to To Tickets" in flat
    assert "downstream work unstarted" in repair["return_packet"]
    assert "campaign custody" not in repair["return_packet"]


def test_diagnosis_is_an_explicit_leaf_with_bounded_recommendations() -> None:
    diagnosing = (CUSTOM / "diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
    prototype = (CUSTOM / "prototype/SKILL.md").read_text(encoding="utf-8")
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
    assert {
        (caller, verb, callee)
        for caller, verb, callee in rows
        if caller == "diagnosing-bugs" or callee == "diagnosing-bugs"
    } == {
        ("prototype", "Recommend and stop", "diagnosing-bugs"),
        ("triage", "Recommend and stop", "diagnosing-bugs"),
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
        ("triage", "Recommend and stop", "diagnosing-bugs"),
    }
    for skill in CUSTOM.iterdir():
        if skill.is_dir() and skill.name not in {
            "diagnosing-bugs",
            "prototype",
            "skill-router",
            "triage",
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
        ("to-spec", "Recommend and stop", "implement"),
        ("to-spec", "Recommend and stop", "to-tickets"),
        ("to-tickets", "Recommend and stop", "implement"),
        ("to-tickets", "Recommend and stop", "parallel-implement"),
        ("implement", "Invoke", "change-review"),
        ("parallel-implement", "Invoke", "change-review"),
        ("triage", "Recommend and stop", "change-review"),
        ("triage", "Recommend and stop", "diagnosing-bugs"),
        ("triage", "Recommend and stop", "to-tickets"),
    ):
        assert edge in edges
    assert not any(
        caller == "wayfinder" and callee in {"domain-modeling", "implement", "to-spec"}
        for caller, _, callee in edges
    )
    assert ("skill-router", "Recommend and stop", "high-assurance-review") in edges
    assert not any(
        callee == "high-assurance-review"
        and caller in {"implement", "parallel-implement", "change-review"}
        for caller, _, callee in edges
    )
    assert not any(
        {caller, callee} == {"implement", "parallel-implement"}
        for caller, _, callee in edges
    )
    assert ("implement", "Recommend and stop", "to-tickets") not in edges
    assert "Multiple authors alone do not trigger review" in relationships_flat
    assert "Multiple workers alone do not trigger review" in relationships_flat
    assert "review trigger or independent authors" not in relationships_flat
    assert "remains after proof" in relationships_flat
    assert "Supported risk modifies coverage only after review admission" in relationships_flat
    assert "ToSpec --> Labels" not in relationships
    assert not implicit_policy(CUSTOM / "high-assurance-review")


def test_router_and_synthesis_keep_active_ownership_unambiguous() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")
    synthesis_index = (ROOT / "docs/synthesis/README.md").read_text(encoding="utf-8")

    assert "target-spine.md" not in synthesis_index
    assert "language-direction.md" not in synthesis_index
    assert "support tickets" not in tickets
    assert "support slices" not in tickets
