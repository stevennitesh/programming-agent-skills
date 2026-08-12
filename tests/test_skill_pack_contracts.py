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

    assert "**Campaign snapshot:**" not in trackers[0].read_text(encoding="utf-8")
    assert "GITHUB_CAMPAIGN_SNAPSHOT_TOKENS" not in validator

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
        exact_tree_hash(package_root)
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
        "c914dc0bb12d0724af2ecc5ae18f6e9506f89cb4d5a6371c1c6a54b5e576d942",
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
    for source_term in (
        "deep modules",
        "information hiding",
        "change amplification",
        "cognitive load",
        "unknown unknowns",
        "somewhat general-purpose interfaces",
        "a test as the first user",
        "state testing",
        "interaction testing",
    ):
        assert source_term in design_flat.lower()
    assert len(re.findall(r"(?m)^## \d+\. ", direct)) == 5
    for required in (
        "decision-needed",
        "evidence-gap",
        "Failure Atomicity",
        "Trust Boundaries",
        "Proof Seam establishes meaning",
        "Test Portfolio",
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
    review_summary = (
        ROOT / "docs/synthesis/skills/change-review.md"
    ).read_text(encoding="utf-8")
    assurance_summary = (
        ROOT / "docs/synthesis/skills/high-assurance-review.md"
    ).read_text(encoding="utf-8")

    assert re.search(r"(?m)^name: change-review$", review)
    assert re.search(r"(?m)^name: high-assurance-review$", convergent)
    assert "$high-assurance-review" not in review
    assert "$change-review" not in convergent.split("## 1. Admit", 1)[1].split(
        "## 2. Pin", 1
    )[0]
    review_flat = " ".join(review.split())
    assert "Candidate kind, size, release status, and supported risk neither invoke review" in review_flat
    assert "Accept only when the user explicitly names" in convergent
    assert "explicitly user-selected immutable candidate" in assurance_summary
    assert "No workflow selects High-Assurance Review automatically" in assurance_summary
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
        "Semantic agent: ordinary-reviewer | integration-reviewer | standalone",
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
        ("ordinary-reviewer", "default", "gpt-5.6-sol", "high"),
        ("integration-reviewer", "default", "gpt-5.6-sol", "xhigh"),
        ("har-spec-reviewer", "default", "gpt-5.6-sol", "xhigh"),
        ("har-standards-reviewer", "default", "gpt-5.6-sol", "xhigh"),
        ("har-specialist", "default", "gpt-5.6-sol", "xhigh"),
    ]
    assert "A named agent type loads its custom TOML" in profiles_flat
    assert "Enforce a row only for a spawned actor" in profiles_flat
    assert "public interface, cross-owner invariant" in profiles_flat
    assert "`transport-invalid` and receives no review credit" in profiles_flat
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in implement
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in review
    assert "[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md)" in assurance
    assert "passes it directly when starting the worker" in profiles_flat
    assert "first matching capable worker using the ordered conditions" in implement_flat
    assert "Luna/max `clear-worker`" not in implement
    assert not (CUSTOM / "parallel-implement/scripts/run_ledger.py").exists()
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
        "original accepted commitments",
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
    assert "Risk is a cross-cutting modifier after review is admitted." in finding_flat
    assert "It never invokes Change Review" in finding_flat
    assert "PR existence, size, labels, and hypothetical cases do not qualify." in finding_flat
    assert "not a blind Cartesian product" in review
    assert "not a blind Cartesian product" in convergent_flat
    assert "Omit inapplicable classes" in convergent_flat
    assert "inapplicable classes `N/A`" not in convergent_flat
    assert "Reuse proof tied to the exact snapshot" in review
    assert "Reuse exact-snapshot proof" in convergent_flat
    assert "release candidate, or implementation candidate" in review
    assert "FINDING-CONTRACT.md" in convergent
    assert "neither required nor sufficient for invocation" in convergent_flat
    assert "supported-risk candidate needs read-only judgment" in router
    assert "High Assurance Review is an explicit user-selected alternative" in router


def test_review_assurance_route_has_one_domain_decision() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    adr = (
        ROOT / "docs/adr/0015-independent-change-review-is-condition-triggered.md"
    ).read_text(encoding="utf-8")
    normalized_adr = " ".join(adr.split())

    for term in (
        "**Change review candidate**",
        "**High-assurance review candidate**",
        "**Supported high-risk trigger**",
    ):
        assert context.count(term) == 1
    assert "ADR-0015" in context
    assert "**Status**: accepted" in adr
    assert "Supported facts expand ordinary candidate-scoped coverage" in normalized_adr
    assert "Candidate size, PR or release packaging" in normalized_adr
    assert "Missing required proof stops the work" in normalized_adr
    assert "High-Assurance Review remains explicit-only" in normalized_adr
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

    assert "top-level root of its review run" in convergent_flat
    assert "semantic assurance coordinator" in convergent_flat
    assert "without a model or reasoning gate" in convergent_flat
    assert "nested review lane that invokes this skill returns `incomplete` before Pin" in convergent_flat
    assert "other nested review lane that invokes this skill" in convergent_flat
    for mode in ("initial", "remediation"):
        assert f"- `{mode}`" in convergent
    assert "valid reviewer quorum" in convergent
    assert "exactly two valid fresh core returns" in convergent
    assert "coordinator never substitutes for a reviewer" in convergent
    assert "no Repair, Lock, or residual-risk acceptance authority" in convergent_flat
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


def test_implement_uses_condition_triggered_change_review() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    review = implement.split("## Check, Conditional Review, And Repair", 1)[1].split(
        "## Lock And Return", 1
    )[0]
    flat = " ".join(review.split())

    assert "user or repository explicitly requires independent review" in flat
    assert "two or more independent authors" in flat
    assert "focused proof establishes behavior" in flat
    assert "One delegated edit" in flat
    assert "do not trigger review" in flat
    assert "missing proof returns `partial` or `blocked`" in flat
    assert "one fresh `ordinary-reviewer` through `$change-review`" in flat
    assert "distinct from every implementation actor" in flat
    assert "repeat Change Review only while the original trigger still applies" in flat
    assert "Do not describe direct self-check as independent review" in flat
    assert "stage only owned paths or hunks" in flat
    assert "never unstage foreign work" in flat.lower()


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

    assert "Change Review only when its trigger applies" in (
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
    assert "## Test Portfolio" in tests
    assert "a test as the first user" in tests
    assert "state testing" in tests
    assert "interaction testing" in tests
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
        "Removal Trigger",
    ):
        assert owned_concept.lower() in spec_lower
    for downstream_concept in (
        "bounded repository grounding",
        "ticket slices",
        "expected writes",
        "concrete proof lanes",
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
    review = (CUSTOM / "change-review/SKILL.md").read_text(encoding="utf-8")
    assurance = (CUSTOM / "high-assurance-review/SKILL.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (review, assurance):
        assert "`Spec required: yes | no`" in text
    assert "`Spec required: yes`" in implement
    assert "`Spec required: yes`" in parallel


def test_implementation_workflows_keep_local_proof_owners() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )

    assert "tracker and label owners only for tracker-backed work" in implement
    assert "all source-owned commitments unchanged" in implement
    assert "Bind proof to the exact candidate and inputs" in implement
    assert "focused checks that prove the change" in implement
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
    assert "guidance, not as a schema" in " ".join(implement.split())
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

    assert "Before either path chooses an implementation seam" in implement
    assert (
        "Before choosing an implementation seam, each worker traces every assigned"
        in parallel
    )
    assert (
        "Do not return `partial` merely because the first bounded seam is green"
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
    assert "smallest acceptance-complete path" in implement
    assert "Change Closure" in implement and "Change Closure" in review
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
    assert "smallest acceptance-complete path" in implement_flat
    assert "plain ticket-specific handoff" in implement_flat
    assert "prose Return as evidence" in implement_flat
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
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    bootstrap = (CUSTOM / "repo-bootstrap/SKILL.md").read_text(encoding="utf-8")
    contract_flat = " ".join(contract.split())

    assert "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock" in fallback
    assert "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock" not in contract
    assert "It is not a workflow, checklist, review gate, completion contract" in contract_flat
    assert "replace any portable contract owner preamble" in " ".join(bootstrap.split())
    assert re.findall(r"\$[a-z0-9][a-z0-9-]*", fallback) == []
    assert "### Deep Modules And Information Hiding — Prefer" in contract
    assert "### Fit Before Novelty — Prefer" in contract
    assert "### Converge Efficiently — Prefer" in contract
    assert "### Use A Negative Control — Method" in contract
    assert "### Prove Durable Artifacts Proportionally — Method" in contract
    assert "controlled violation fails for the intended reason" in contract_flat
    assert "Repeat the conforming case after failure only when state" in contract_flat


def test_source_derived_vocabulary_projects_to_affected_skill_slices() -> None:
    projections = {
        "audit-codebase": (
            "Hyrum's Law",
            "define needless errors out of existence",
            "change amplification",
            "cognitive load",
            "unknown unknowns",
            "state testing",
            "interaction testing",
        ),
        "change-review": ("Hyrum's Law", "essential and accidental complexity"),
        "simplify-code": ("Hyrum's Law", "change amplification", "cognitive load"),
        "implement": ("Hyrum's Law", "actual dependence"),
    }
    paths = {
        "audit-codebase": tuple((CUSTOM / "audit-codebase").glob("*.md")),
        "change-review": tuple((CUSTOM / "change-review").glob("*.md")),
        "simplify-code": (CUSTOM / "simplify-code/SKILL.md",),
        "implement": (CUSTOM / "implement/SKILL.md",),
    }

    for owner, terms in projections.items():
        text = " ".join(
            " ".join(path.read_text(encoding="utf-8").split())
            for path in paths[owner]
        )
        for term in terms:
            assert term in text


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


def test_mutating_workflows_require_proportional_readback() -> None:
    implement = " ".join(
        (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    parallel = " ".join(
        (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8").split()
    )
    assert "Mutation read-back rules" in implement
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
        assert "use an oracle independent of the implementation logic" in normalized
        assert "need not be a separate reviewer" in normalized
        assert "Git mutation owners" not in normalized
        assert "starting index" not in normalized
        assert "registered worktrees" not in normalized
    assert "preserving the starting index and unrelated work" in " ".join(implement.split())
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
    assert "| `integration-reviewer` | `default` | `gpt-5.6-sol` | `xhigh` |" in profiles
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
    assert "one fresh `integration-reviewer`" in flat
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


def test_state_boundary_reasoning_is_proportional_and_has_one_owner() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    seed = (CUSTOM / "repo-bootstrap/engineering-contract.md").read_text(encoding="utf-8")
    tickets = (CUSTOM / "to-tickets/SKILL.md").read_text(encoding="utf-8")

    assert "### Reason Across State Boundaries" in contract
    assert "### Reason Across State Boundaries" in seed
    flat = " ".join(tickets.split())
    assert "whose behavior materially changes by state" in flat
    assert "Use a matrix only when it is clearer than prose" in flat
    assert "never add Cartesian or stateless padding" in flat


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(implement.split())

    assert not implicit_policy(CUSTOM / "implement")
    assert "Deliver exactly one caller-selected ready item" in flat
    assert "an exhaustive parent graph to the caller" in flat
    assert "The caller owns commitments" in flat
    assert "Push requires separate authority" in flat
    assert "Otherwise, direct work creates one only when the caller requests Git delivery" in flat
    assert "expected root effort saved exceeds handoff and verification cost" in flat
    assert "create no score, worksheet, or artifact" in flat
    assert "When the delegation gate fails" in flat


def test_implement_closeout_locks_exact_candidate_and_preserves_custody() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(implement.split())

    assert "pin the exact candidate" in flat.lower()
    assert "stage only owned paths or hunks" in flat
    assert "never unstage foreign work" in flat.lower()
    assert "Lock the final checked tree" in flat
    assert "Do not rewrite an exact accepted commit" in flat
    assert "proving `HEAD` unchanged" in flat
    assert "Otherwise preserve the final checked candidate and stop before commit" in flat
    assert "retain the claim through commit and configured closeout" in flat
    assert "read back non-dispatchability" in flat
    assert "release the claim and verify the frontier" in flat
    assert "exclusive mutation custody of the reconciled checkout until Return" in flat
    assert "caller did not request root execution" in flat
    assert "keep repair with the root" in flat
    assert "every triggered Change Review" in flat
    assert "Repair generations" not in flat


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
    assert "Missing proof stops instead of invoking review" in relationships_flat
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
