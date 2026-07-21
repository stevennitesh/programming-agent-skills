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


def test_to_questionnaire_owns_one_safe_recipient_artifact() -> None:
    skill_dir = CUSTOM / "to-questionnaire"
    questionnaire = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

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
    assert "<work-root>/.tmp/to-questionnaire/<slug>.md" in questionnaire


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
        for token in (
            "MAP-FORMAT.md",
            "Claim token:",
            "Claimed at:",
            "codex/<lowercase UUIDv4>",
            "<YYYY-MM-DDTHH:MM:SSZ>",
            "Maintain claims the map",
            "never reuse it across invocations",
            "different token owns the item",
            "Elapsed time alone never makes a claim stale.",
            "explicit user approval",
            "takeover reason",
            "Mutation read-back",
        ):
            assert token in wayfinding, f"{tracker} is missing {token}"
        assert "Its body holds Destination" not in wayfinding


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
    domain = (CUSTOM / "repo-bootstrap/domain.md").read_text(encoding="utf-8")
    assert re.findall(r"(?m)^## ([A-Za-z]+)$", bootstrap) == [
        "Inventory",
        "Reconcile",
        "Choose",
        "Draft",
        "Provision",
        "Verify",
    ]
    assert bootstrap.index("## Draft") < bootstrap.index("## Provision")
    assert "<context-root>/docs/adr/" in domain
    assert "following the context root recorded in `CONTEXT-MAP.md`" in domain
    assert "src/<context>/docs/adr/" not in domain


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
    chart, modes = wayfinder.split("### Chart", 1)[1].split("### Advance", 1)
    advance, remaining = modes.split("### Maintain", 1)
    maintain, closure = remaining.split("## Closure", 1)
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
    assert re.findall(r"(?m)^### (Chart|Advance|Maintain)$", wayfinder) == [
        "Chart",
        "Advance",
        "Maintain",
    ]
    assert "At the end of Advance or Maintain" in closure
    assert "zero frontier tickets have substantive outcomes" in maintain
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


def test_wayfinder_prototype_participation_matches_judgment() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    tickets = wayfinder.split("## Tickets", 1)[1].split("## Modes", 1)[0]
    rules = re.findall(
        r"(?m)^- `(shape/feel|design evidence)` — (HITL|AFK) (.+)\.$",
        tickets,
    )
    assert [(claim, mode) for claim, mode, _ in rules] == [
        ("shape/feel", "HITL"),
        ("design evidence", "AFK"),
        ("design evidence", "HITL"),
    ]
    assert "objective verdict criteria" in rules[1][2]
    assert "explicitly reserves the verdict for a human" in rules[2][2]
    assert "reconciled verdict packet and cleanup or preservation state" in tickets

    approve = wayfinder.split("4. **Approve.**", 1)[1].split("5. **Chart.**", 1)[0]
    for field in ("claim level", "human judge", "objective verdict criteria"):
        assert field in approve
    assert "reject" in approve and "participation rule" in approve

    for field in ("Claim level:", "Human judge:", "Verdict criteria:"):
        assert field in map_format


def test_wayfinder_routes_by_authority_and_accounts_for_fog() -> None:
    skill_dir = CUSTOM / "wayfinder"
    wayfinder = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    map_format = (skill_dir / "MAP-FORMAT.md").read_text(encoding="utf-8")

    tickets = wayfinder.split("## Tickets", 1)[1].split("## Modes", 1)[0]
    assert "user owns the resolution" in tickets
    assert "accepted repository contracts and objective proof" in tickets
    assert "Classify by resolution authority" in tickets
    assert "Split a ticket" in tickets

    advance = wayfinder.split("### Advance", 1)[1].split("### Maintain", 1)[0]
    claim = advance.split("3. **Claim.**", 1)[1].split("4. **Resolve.**", 1)[0]
    assert "current session's claim identity" in claim
    assert "exact session identity or claimed-at value" in claim

    reconcile = advance.split("5. **Reconcile.**", 1)[1].split(
        "6. **Verify.**", 1
    )[0]
    assert re.findall(r"(?m)^   - \*\*(Retain|Graduate|Resolve|Exclude):\*\*", reconcile) == [
        "Retain",
        "Graduate",
        "Resolve",
        "Exclude",
    ]
    assert "every affected fog item has exactly one disposition" in advance
    assert "sole fog container" in map_format
    assert "None — all remaining in-scope questions are ticket-owned." in map_format
    assert "future-work owner, governing resolution, or map pointer" in map_format
    assert "Do not create a ticket solely to supply a link." in map_format

    maintain = wayfinder.split("### Maintain", 1)[1].split("## Closure", 1)[0]
    assert re.findall(r"(?m)^\d+\. \*\*([A-Za-z]+)\.\*\*", maintain) == [
        "Orient",
        "Bound",
        "Approve",
        "Claim",
        "Repair",
        "Verify",
        "Expose",
    ]
    assert "Record no child outcome" in maintain
    assert "claim the map" in maintain
    assert "specific predicate takes precedence over Advance" in maintain
    assert "evidence-backed scope indexing" in maintain
    assert "every affected fog item exactly one Advance disposition" in maintain
    assert "linked resolution" in maintain and "governing exclusion pointer" in maintain

    closure = wayfinder.split("## Closure", 1)[1].split("## Return", 1)[0]
    assert "read back the absence of that claim" in closure

    returned = wayfinder.split("## Return", 1)[1]
    assert "Next frontier: [<ticket title>](<link>). Invoke $wayfinder to advance it." in returned


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
        "Boundary",
        "Admit",
        "Disclose",
        "Compose",
        "Join",
        "Return",
    ]
    for contract in (
        "Admit -> Disclose -> Compose [Grill <-> Relay <-> Model] -> Join -> Return",
        "Relay each settled material answer",
        "return every material collision or blocker to Grilling",
        "The composer filters or merges neither",
        "Status: Confirmed | Evidence gap | Blocked",
        "This is a return, not a general handoff",
    ):
        assert contract in grill_docs
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
        "Reconcile",
        "Return",
    ]
    assert "Trace -> Challenge -> Resolve -> Reconcile -> (Persist -> Verify | Render) -> Return" in domain
    for target in ("CONTEXT-FORMAT.md", "ADR-FORMAT.md"):
        assert (CUSTOM / "domain-modeling" / target).is_file()
        assert f"({f'./{target}'})" in domain
    for contract in (
        "accept every settled material answer",
        "return any collision or blocker before dependent Grilling progress",
        "Never decide answer materiality or interview branching",
        "Domain Delta",
    ):
        assert contract in domain


def test_grilling_preserves_one_decision_confirmed_exit_and_evidence_routes() -> None:
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")

    assert re.findall(r"(?m)^\*\*([A-Za-z ]+)\.\*\*", grilling) == [
        "Boundary",
        "Bound",
        "Find",
        "Grill",
        "Integrate",
        "Confirm",
        "Gap",
        "Return",
    ]
    for contract in (
        "return each settled material answer",
        "pause dependent questioning",
        "Integrate the returned domain collision or blocker",
        "never classify the domain consequence yourself",
    ):
        assert contract in grilling


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
    assert {"Model", "Surface", "Smoke"} <= set(
        re.findall(r"(?m)^## (.+)$", logic)
    )
    assert re.findall(r"(?m)^## (.+)$", ui) == ["Host", "Bet", "Switch", "Smoke"]
    assert "smallest explicit decision interface" in logic
    surface = logic.split("## Surface", 1)[1].split("## Smoke", 1)[0]
    interactive = surface.split("### Interactive", 1)[1].split(
        "### Deterministic", 1
    )[0]
    deterministic = surface.split("### Deterministic", 1)[1]
    assert "Read one command" in interactive and "until quit" in interactive
    assert "caller-locked objective criteria" in deterministic
    assert "without prompts" in deterministic
    assert "Human judgment" in judge and "human-reserved design verdict" in judge
    assert "Objective design evidence" in judge and "criterion results" in judge
    assert "entire prototype surface" in ui
    assert "unreachable in production builds" in ui


def test_review_baselines_are_discovered_and_independence_is_honest() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")
    baseline = (CUSTOM / "review/SMELL-BASELINE.md").read_text(encoding="utf-8")

    assert "## 1. Pin" in review
    assert "## 1. Pin" in convergent
    assert "$convergent-pr-review" in review.split("---", 2)[1]
    assert "only when documented repo standards" in baseline
    assert "concrete, actionable maintainability risk" in baseline
    assert "baseline judgement call" in review
    assert "baseline judgement call" in convergent
    review_steps = re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", review)
    assert {"Pin", "Trace", "Admit", "Judge", "Return"} <= set(review_steps)
    assert review_steps.index("Pin") < review_steps.index("Trace") < review_steps.index("Admit")
    assert review_steps.index("Admit") < review_steps.index("Judge") < review_steps.index("Return")
    convergent_steps = re.findall(r"(?m)^## \d+\. ([A-Za-z]+)$", convergent)
    assert {"Pin", "Trace", "Isolate", "Challenge", "Verify", "Return"} <= set(
        convergent_steps
    )
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
        "Return boundary",
        "Mutation authority",
        "Successor snapshot authority",
    ]


def test_review_finding_interface_and_return_boundary_are_shared() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    finding = (CUSTOM / "review/FINDING-CONTRACT.md").read_text(encoding="utf-8")

    fields = finding.split("```text", 1)[1].split("```", 1)[0]
    assert set(re.findall(r"(?m)^([A-Za-z ]+):", fields)) == {
        "ID",
        "Axis",
        "Severity",
        "Location",
        "Anchor",
        "Supported scenario",
        "Evidence",
        "Impact",
        "Blocking",
        "Remediation",
        "Required proof",
    }
    assert {
        "automatic-in-scope",
        "decision-required",
        "residual-hardening",
    } <= set(re.findall(r"(?m)^- `([^`]+)`:", finding))
    severity = finding.split("## Severity", 1)[1].split("## Bound", 1)[0]
    assert re.findall(r"(?m)^- `(P[0-3])`:", severity) == ["P0", "P1", "P2", "P3"]
    for skill in (review, convergent):
        assert "FINDING-CONTRACT.md" in skill
        assert not re.search(r"(?m)^- (?:\*\*)?`?P[0-3]", skill)
        assert "Return boundary: caller" in skill
        assert "Mutation authority: none" in skill
        assert "Successor snapshot authority: none" in skill


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
        "advisories",
        "skipped checks",
        "blockers",
    }


def test_convergent_review_has_root_guard_capacity_modes_and_advisories() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    advisory = (CUSTOM / "review/ADVISORY-CONTRACT.md").read_text(encoding="utf-8")

    assert "**Root-only guard:**" in convergent
    assert "stop before Pin" in convergent
    assert {"initial", "remediation", "assurance"} <= set(
        re.findall(r"(?m)^- `([^`]+)`:", convergent)
    )
    for capacity in (
        "At least two fresh completed reviewers",
        "Exactly one fresh completed reviewer",
        "Zero fresh completed reviewers",
        "Any required lens or evidence axis remains uncovered",
    ):
        assert capacity in convergent
    assert "Reduced-capacity execution never produces plain `pass`" in convergent
    assert "[ADVISORY-CONTRACT.md](../review/ADVISORY-CONTRACT.md)" in convergent
    assert "repair-ready handoff" in convergent
    assert "advisory patch-ready handoff" not in convergent
    assert "never affect confidence or a terminal decision" in advisory
    assert "Never demote" in advisory


def test_audit_codebase_is_terminal_html_audit_with_bounded_suggestions() -> None:
    skill_dir = CUSTOM / "audit-codebase"
    audit = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    defect = (skill_dir / "DEFECT-CONTRACT.md").read_text(encoding="utf-8")
    performance = (skill_dir / "PERFORMANCE-LENS.md").read_text(encoding="utf-8")
    performance_lower = performance.lower()
    report = (skill_dir / "HTML-REPORT.md").read_text(encoding="utf-8")
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert "**Root-owned:**" in audit
    assert "Release decision: none" in audit
    assert "a complete audit may contain severe defects" in audit
    assert "[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md)" in audit
    assert "[PERFORMANCE-LENS.md](PERFORMANCE-LENS.md)" in audit
    assert "[HTML-REPORT.md](HTML-REPORT.md)" in audit
    assert ".tmp/audit-codebase/<run-id>/report.html" in audit
    assert "FINDING-CONTRACT.md" not in audit
    assert "**Terminal:**" in audit
    assert "**Chain of custody.**" in audit
    assert "$wayfinder" not in audit
    assert "$to-tickets" not in audit
    assert "offline and script-free" not in audit
    assert "## Burden Of Proof" in defect
    assert "Severity orders defects" in defect
    assert "exactly zero or one" in defect
    assert "Severity orders defects; evidence state and work shape choose the suggestion" in defect
    assert "Downstream execution: none" in audit
    for route in (
        "$research",
        "$prototype",
        "$grill-with-docs",
        "$diagnosing-bugs",
        "$to-spec",
        "$to-tickets",
        "$implement",
        "$improve-codebase",
        "$wayfinder",
    ):
        assert route in defect
    assert "$tdd" not in defect
    assert "Exactly one bounded remediation item is ready" in defect
    assert "multiple unresolved decisions or prerequisites" in defect
    assert "solution is settled and only slicing remains" in defect
    assert "**Like-for-like:**" in performance
    assert "smell alone" in performance
    for field in ("Workload:", "Environment:", "Baseline:", "Observed:", "Sample count and variance:"):
        assert field in performance
    assert "performance defect" in performance_lower
    assert "performance opportunity" in performance_lower
    assert "performance evidence gap" in performance_lower
    assert "offline" in report
    assert "runtime JavaScript" in report
    assert "Coverage Matrix" in report
    assert "Suggested Handoffs" in report
    assert "## Top Recommendation" not in report
    assert "**Ledger, not leaderboard:**" in report
    assert "caller selection required" in report
    assert re.search(
        r"(?m)^\| An immutable repository baseline .*domain robustness.*performance.* \| `\$audit-codebase` \|$",
        router,
    )


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

    verify = convergent.split("## 5. Verify", 1)[1].split("## 6. Return", 1)[0]
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
    repair_section = implement.split("## Repair", 1)[1].split("## Lock", 1)[0]
    assert "FINDING-CONTRACT.md" in repair_section
    assert {"automatic-in-scope", "decision-required"} <= set(
        re.findall(r"`([^`]+)`", repair_section)
    )


def test_improve_codebase_separates_survey_from_selected_candidate() -> None:
    skill_dir = CUSTOM / "improve-codebase"
    survey = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    selected = (skill_dir / "SELECTED-CANDIDATE.md").read_text(encoding="utf-8")
    report = (skill_dir / "HTML-REPORT.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert "[SELECTED-CANDIDATE.md](SELECTED-CANDIDATE.md)" in survey
    assert "$improve-codebase Candidate N from <absolute-report-path>" in survey
    assert "**Terminal.**" in survey
    assert "Start no candidate resolution or execution" in survey
    assert "**No candidate recommended**" in survey
    for disposition in ("Eliminate", "Concentrate", "Retain", "Investigate"):
        assert disposition in survey
    for relationship in ("Independent", "Preparatory", "Absorbed", "Residual"):
        assert relationship in survey
    for field in (
        "behavior and commitment boundary",
        "proof seam",
        "resolution need",
        "sequence relationship",
        "provisional destination",
        "exact immediate pickup invocation",
    ):
        assert field in survey
    for resolution_need in (
        "`none`",
        "`repository`",
        "`source`",
        "`runnable`",
        "`user-decision`",
        "`design`",
    ):
        assert resolution_need in survey
    assert "`Eliminate` -> `$simplify-code`" in survey
    assert "$domain-modeling" not in survey
    assert "never `$tdd` or `$implement`" in report

    assert re.findall(r"(?m)^## (.+)$", report) == [
        "Portability",
        "Layout",
        "Theme And Accessibility",
        "Survey Ledger",
        "Candidate",
        "Visual",
        "Ranking",
        "Top Recommendation",
        "Resolution",
        "Voice",
    ]
    assert "`color-scheme: dark`" in report
    assert "`Strong` or `Worth exploring`" in report
    assert "**No candidate recommended**" in report

    assert "Do not repeat the Survey" in selected
    assert "**Resolve at most one blocker.**" in selected
    for resolver in (
        "$research",
        "$prototype",
        "$grill-with-docs",
        "$codebase-design",
    ):
        assert resolver in selected
    assert "$grilling" not in selected
    assert "design evidence, never production proof" in selected
    assert "settled direction" in selected and "$to-spec" in selected
    assert "multiple interdependent unresolved decisions or prerequisites" in selected
    assert "$wayfinder" in selected
    assert "$simplify-code Candidate N from <absolute-report-path>" in selected
    assert "**Reconcile.**" in selected and "same card" in selected


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


def test_tdd_routes_improvement_followups_by_scope() -> None:
    refactoring = (CUSTOM / "tdd/refactoring.md").read_text(encoding="utf-8")

    assert "$simplify-code" in refactoring
    assert "$codebase-design" in refactoring
    assert "$improve-codebase" in refactoring


def test_simplify_code_is_explicit_bounded_and_behavior_preserving() -> None:
    skill_dir = CUSTOM / "simplify-code"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(skill_dir)
    assert "one proved reduction in total codebase complexity" in skill
    assert "No safe simplification" in skill
    assert "trusted focused proof" in skill
    assert "before and after" in skill
    assert "After the last proof command, refresh worktree status" in skill
    assert "proves that no use remains" in skill
    assert "git ls-files --stage" in skill
    assert "status text alone is not index proof" in skill
    assert "Leave the index, commits, trackers, external systems" in skill
    assert "Without a bounded target, recommend `$improve-codebase` and stop" in skill
    assert "Candidate N" in skill and "verified `$improve-codebase` report" in skill
    assert "Enter this branch only when the invocation explicitly says `until-clean`" in skill
    assert "rerun the complete Trace, Baseline, Hunt, Choose, Cut, Prove, Lock cycle" in skill
    assert re.findall(r"(?m)^\d\. \*\*([A-Za-z]+)\.\*\*", skill) == [
        "Delete",
        "Reuse",
        "Standardize",
        "Collapse",
        "Shrink",
    ]

    standardize = skill.split("3. **Standardize.**", 1)[1].split("4. **Collapse.**", 1)[0]
    assert "**Native-first.**" in standardize
    assert standardize.index("standard-library") < standardize.index("browser")
    assert standardize.index("browser") < standardize.index("already-installed dependency")

    collapse = skill.split("4. **Collapse.**", 1)[1].split("5. **Shrink.**", 1)[0]
    assert "narrowest existing owner" in collapse

    cut = skill.split("## Cut", 1)[1].split("## Prove", 1)[0]
    assert "ceiling" in cut and "revisit trigger" in cut


def test_simplify_code_until_clean_has_a_finite_convergence_contract() -> None:
    skill = (CUSTOM / "simplify-code/SKILL.md").read_text(encoding="utf-8")
    branch = skill.split("## Until Clean", 1)[1].split("## Return", 1)[0]

    for contract_field in ("**Region:**", "**Budget:**", "**Progress unit:**", "**Clean criterion:**"):
        assert contract_field in branch
    assert "`3` successful cuts by default" in branch
    assert "Never infer, extend, or reset the budget" in branch
    assert "strict net reduction" in branch
    assert "all five rungs" in branch
    assert "line-count reduction alone never keeps a campaign open" in branch
    assert "one Cut or Prove attempt" in branch
    assert "continuation requires a new explicit invocation and budget" in branch
    assert re.findall(r"(?m)^\d\. \*\*([^*]+):\*\*", branch) == [
        "Clean",
        "Budget exhausted",
        "Diminishing return",
        "Oscillation",
        "Failed cut",
        "Boundary stop",
    ]

    returned = skill.split("## Return", 1)[1].split("## Completion", 1)[0]
    assert "Campaign: <region; cut budget, used, and remaining | n/a>" in returned
    assert "Progress ledger:" in returned


def test_codebase_design_compares_replacement_with_incremental_evolution() -> None:
    direct = (CUSTOM / "codebase-design/DIRECT-DESIGN.md").read_text(encoding="utf-8")

    assert "deepen, merge, inline, retain, replace" in direct
    assert "compare it explicitly with incremental evolution" in direct
    for gate in ("parity", "migration", "cutover", "rollback"):
        assert gate in direct


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
    improvement = (CUSTOM / "improve-codebase/SKILL.md").read_text(encoding="utf-8")

    for text in (design, research, improvement):
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


def test_writing_great_skills_keeps_concise_authoring_boundary() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    behavior_evals = (skill_dir / "BEHAVIOR-EVALS.md").read_text(
        encoding="utf-8"
    )
    glossary = (skill_dir / "GLOSSARY.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

    assert implicit_policy(skill_dir)
    for contract in (
        "**Audit:** advise read-only",
        "**Author:** edit only the requested canonical skill",
        "Trace",
        "Own",
        "Shape",
        "Prune",
        "Prove",
        "callee, trigger, authority, and return boundary",
        "bundled `skill-creator`",
        "Inspect mirrors only when asked",
        "Stop after canonical proof",
        "delivery needs separate authority",
    ):
        assert contract in skill

    for contract in (
        "Invocation misses or false-fires",
        "A step ends early",
        "at least five independent samples per arm",
        "Ambient collaboration policy decides whether and how workers run",
        "Keep candidate language, conclusions, and prior outputs out of control",
        "reject-no-control-failure",
    ):
        assert contract in behavior_evals

    assert "fork_turns" not in skill
    assert "installed mirrors" not in skill.lower()
    assert "Pack rule:" not in glossary
    assert (
        "bundled system `skill-creator` owns new-package scaffolding and metadata mechanics"
        in relationships
    )
    assert "$writing-great-skills` owns semantic quality" in relationships


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
    assert "Apply the **Semantic Skill Surface**" in writing
    assert "Use only applicable roles" in surface
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
    parallel_steps = re.findall(r"(?m)^## (.+)$", parallel)
    expected_steps = [
        "Trace",
        "Select",
        "Open",
        "Drain",
        "Review",
        "Lock",
        "Release",
    ]
    assert all(step in parallel_steps for step in expected_steps)
    assert [parallel_steps.index(step) for step in expected_steps] == sorted(
        parallel_steps.index(step) for step in expected_steps
    )
    assert 'fork_turns="none"' in parallel
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
        "commands and results",
        "skipped checks",
        "liveness checkpoint",
        "risk or blocker",
        "next need",
        "scope notes",
        "final status",
        "skill feedback",
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
    drain = parallel.split("## Drain", 1)[1].split("## Review", 1)[0]
    assert {"done", "needs-feedback", "blocker"} <= set(
        re.findall(r"`([^`]+)`", drain)
    )
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
    lock = parallel.split("## Lock", 1)[1].split("## Release", 1)[0]
    assert "claim" in parallel.split("## Open", 1)[1].split("## Drain", 1)[0]
    assert "read back" in parallel.lower()
    assert "closeout plan" in lock and "Mutation read-back" in lock
    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    assert "idle" in review


def test_parallel_implement_has_root_receipt_budget_and_windows_contracts() -> None:
    skill_dir = CUSTOM / "parallel-implement"
    parallel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    ledger = (skill_dir / "references/RUN-LEDGER.md").read_text(encoding="utf-8")
    launch = (skill_dir / "references/CODEX-WORKTREE-LAUNCH.md").read_text(
        encoding="utf-8"
    )
    worker = (skill_dir / "references/WORKER-BRIEF.md").read_text(encoding="utf-8")
    script = (skill_dir / "scripts/run_ledger.py").read_text(encoding="utf-8")
    lane_script = (skill_dir / "scripts/lane_worktree.py").read_text(encoding="utf-8")

    assert "**Root only.**" in parallel
    assert "stop before mutation" in parallel
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
    assert "none_observed" in parallel
    assert "runtime contract 3" in parallel.lower()
    assert "Integration correction" in ledger
    assert "correction_authorization" in script
    assert "runtime contract 3" in ledger
    assert "viability, not throughput" in launch and "-n 0" in launch
    assert "project imports must resolve beneath the lane" in launch
    assert "repo-owned configuration" in launch
    assert "namespace-package locations" in launch
    assert "--python-provenance-file" in launch and "--python-provenance-file" in lane_script
    assert "original worker" in parallel
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

    gate = parallel.split("## Select", 1)[1].split("## Open", 1)[0]
    assert "Select one ticket" in gate
    assert "Select up to three" in gate
    assert "Stop with exact blockers" in gate

    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    lock = parallel.split("## Lock", 1)[1].split("## Release", 1)[0]
    assert "$review" in review
    assert "Mutation read-back" in lock
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
    assert "Do not copy field-by-field event contracts" in ledger
    assert {
        "serial-frontier",
        "parallel-frontier",
        "child-closeout",
        "parent-closeout",
    } <= event_types
    assert "**Tripwire:**" in gate and "**Downshift:**" in gate

    assert re.search(r"(?m)^\| One parent spec or PRD .* \| `\$parallel-implement` \|$", router)
    assert tickets.index("`$parallel-implement`") < tickets.index("`$implement`")
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
        text = path.read_text(encoding="utf-8")
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
    assert owner_text in contract
    assert owner_text in seed
    assert "engineering contract's state-boundary matrix" in tickets
    assert "Ready-for-agent defect" in parallel
    assert "Loop-close proof recombines applicable state-boundary matrices" in parallel
    assert "State-boundary matrix:" in worker
    assert "return it as `needs-feedback`" in worker
    assert "**Adjudicate before synthesis.**" in ledger
    for disposition in (
        "generic-skill-gap",
        "repo-contract-gap",
        "run-specific",
        "already-satisfied",
    ):
        assert f"`{disposition}`" in ledger
    assert "Synthesis is adjudication, not transcription." in ledger


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "implement")
    owner_route = re.search(r"(?m)^\*\*Owner: (.+)\.\*\*$", implement)
    worker_route = re.search(r"(?m)^\*\*Staged worker: (.+)\.\*\*$", implement)
    assert owner_route is not None and worker_route is not None
    assert {"Charter", "Review", "Repair", "Lock"} <= set(
        part.strip() for part in owner_route.group(1).split("->")
    )
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
        not (caller == "diagnosing-bugs" and callee == "improve-codebase")
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
        ("wayfinder", "Invoke", "grill-with-docs"),
        ("wayfinder", "Recommend and stop", "domain-modeling"),
        ("wayfinder", "Recommend and stop", "to-spec"),
        ("wayfinder", "Recommend and stop", "to-tickets"),
        ("wayfinder", "Recommend and stop", "implement"),
        ("triage", "Invoke", "grill-with-docs"),
        ("improve-codebase", "Invoke", "grill-with-docs"),
        ("implement", "Invoke", "tdd"),
        ("implement", "Invoke", "diagnosing-bugs"),
        ("implement", "Invoke", "review"),
        ("implement", "Invoke", "convergent-pr-review"),
        ("review", "Hand off", "convergent-pr-review"),
        ("convergent-pr-review", "Recommend and stop", "audit-codebase"),
        ("parallel-implement", "Invoke", "convergent-pr-review"),
        ("parallel-implement", "Invoke", "resolving-merge-conflicts"),
        ("resolving-merge-conflicts", "Invoke", "diagnosing-bugs"),
        ("improve-codebase", "Invoke", "research"),
        ("improve-codebase", "Invoke", "prototype"),
        ("improve-codebase", "Load", "codebase-design"),
        ("improve-codebase", "Invoke", "codebase-design"),
        ("improve-codebase", "Recommend and stop", "wayfinder"),
        ("improve-codebase", "Recommend and stop", "simplify-code"),
        ("improve-codebase", "Recommend and stop", "implement"),
        ("improve-codebase", "Recommend and stop", "to-tickets"),
        ("improve-codebase", "Recommend and stop", "to-spec"),
        ("simplify-code", "Recommend and stop", "improve-codebase"),
        ("simplify-code", "Recommend and stop", "codebase-design"),
        ("tdd", "Hand off", "diagnosing-bugs"),
        ("tdd", "Hand off", "prototype"),
        ("tdd", "Recommend and stop", "simplify-code"),
        ("tdd", "Recommend and stop", "codebase-design"),
        ("tdd", "Recommend and stop", "improve-codebase"),
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
        ("improve-codebase", "Recommend and stop", "repo-bootstrap"),
    }

    assert required <= edges
    assert ("improve-codebase", "Invoke", "grilling") not in edges
    assert ("convergent-pr-review", "Hand off", "review") not in edges

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
