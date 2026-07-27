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
        "The catch-all does not cover a known ledger item.",
        "<work-root>/.tmp/to-questionnaire/<slug>.md",
        "resolve the absolute `.md` target",
        "overwrite of that exact target is authorized",
        "Refresh that state immediately before Save.",
        "Render and reread the complete candidate",
        "changed only the authorized file",
        "Status: Questionnaire ready | Not admitted | Incomplete",
        "Artifact path: <absolute path> | none",
        "Delivery: not performed",
        "`Questionnaire ready` requires one verified artifact",
        "`Not admitted` requires a proven failed Admit predicate",
        "`Incomplete` names missing intake",
    ):
        assert contract in questionnaire
    for rejected in ("Wayfinder", ".scratch/to-questionnaire"):
        assert rejected not in questionnaire
    assert policy.endswith("policy:\n  allow_implicit_invocation: false\n")
    assert skill_pack_contract.tree_hash(skill_dir) == (
        "a5c63f7c0ecbe2971dbbd20bb1774ece83990e08fa97d3df6d9f49c3b41cf3c4"
    )
    assert (
        "| One external stakeholder holds missing knowledge and needs an async "
        "discovery questionnaire | `$to-questionnaire` |"
    ) in router
    assert "`$to-questionnaire` for an external stakeholder" in grilling


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
    assert "pass its decision owner, claim level, judgment mode" in tickets
    assert "supported result, evidence, limits, and cleanup state" in tickets

    approve = wayfinder.split("4. **Approve.**", 1)[1].split("5. **Chart.**", 1)[0]
    for field in (
        "decision owner",
        "claim level",
        "judgment mode",
        "human judge",
        "objective verdict criteria",
    ):
        assert field in approve
    assert "reject" in approve and "participation rule" in approve

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
    } >= {"wayfinder", "triage"}


def test_domain_modeling_owns_durable_domain_truth() -> None:
    domain = (CUSTOM / "domain-modeling/SKILL.md").read_text(encoding="utf-8")

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
        assert contract in domain


def test_grilling_preserves_one_decision_confirmed_exit_and_evidence_routes() -> None:
    grilling = (CUSTOM / "grilling/SKILL.md").read_text(encoding="utf-8")
    grilling_plain = grilling.replace("**", "")

    assert re.findall(r"(?m)^\*\*([A-Za-z ]+)\.\*\*", grilling) == [
        "Bound",
        "Grill",
        "Confirm",
        "Gap",
        "Return",
    ]
    for contract in (
        "Relay every settled material answer",
        "pause dependent progress",
        "a repeated non-answer makes that decision authority unavailable",
        "Choose `$research` for an authoritative source",
        "Downstream execution: none",
    ):
        assert contract in grilling_plain


def test_prototype_preserves_lifecycle_boundaries_and_branch_gates() -> None:
    skill_dir = CUSTOM / "prototype"
    prototype = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")

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
    ):
        assert contract in prototype

    for removed in (
        "[RESUME.md](RESUME.md)",
        "$handoff",
        "$domain-modeling",
        "status: answered | awaiting-verdict | blocked | not-admitted",
    ):
        assert removed not in prototype

    assert "happy, boundary, and rejected cases" in logic
    assert "repeated runs are equivalent" in logic
    assert "positively isolates the whole prototype surface" in ui
    assert "actual browser or target UI" in ui
    assert "variance and worst observed result" in measure
    assert "does not diagnose an unexplained slowdown" in measure
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
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")
    baseline = (CUSTOM / "review/SMELL-BASELINE.md").read_text(encoding="utf-8")

    assert "## Pin" in review
    assert "## 2. Pin One Complete Snapshot" in convergent
    assert "$convergent-pr-review" in review.split("---", 2)[1]
    assert "only when documented repo standards" in baseline
    assert "concrete, actionable maintainability risk" in baseline
    assert "SMELL-BASELINE.md` only when local\nStandards are thin" in convergent
    review_steps = re.findall(
        r"(?m)^## (Route|Pin|Trace|Judge|Admit|Return)$", review
    )
    assert review_steps == ["Route", "Pin", "Trace", "Judge", "Admit", "Return"]
    convergent_steps = re.findall(r"(?m)^## \d+\. (.+)$", convergent)
    assert convergent_steps == [
        "Route, Guard, And Freeze The Caller Packet",
        "Pin One Complete Snapshot",
        "Trace Sources And Freeze Coverage",
        "Isolate Candidate Generation",
        "Converge And Admit",
        "Read Back Drift",
        "Decide, Return, And Stop",
    ]
    reports = review.split("```text")
    report = reports[1].split("```", 1)[0]
    assert report.lstrip().startswith("Review status: complete")
    assert "Standards findings:" in report
    assert "Spec findings:" in report
    incomplete = reports[2].split("```", 1)[0]
    assert re.findall(r"(?m)^([A-Za-z ]+):", incomplete) == [
        "Review status",
        "Review mode",
        "Fixed point",
        "Snapshot identity",
        "Target",
        "Sources",
        "Covered work",
        "Verified findings",
        "Carried dispositions",
        "Blocker",
        "Skipped work",
        "Residual risk",
        "Drift",
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
    } <= set(re.findall(r"(?m)^- `([^`]+)`(?:\:| )", finding))
    severity = finding.split("## Classify", 1)[1]
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

    assert "Require the top-level root." in convergent
    assert "root-only blocker before Pin" in convergent
    assert {"initial", "remediation", "assurance"} <= set(
        re.findall(r"(?m)^- `([^`]+)` (?:judges|requires)", convergent)
    )
    for capacity in (
        "At least two",
        "Exactly one",
        "Zero",
        "Any required lens or evidence axis remains uncovered",
    ):
        assert capacity in convergent
    assert "Maximum clean decision" in convergent
    assert convergent.count("`pass with residual risk`") >= 3
    assert "`ADVISORY-CONTRACT.md` only when the caller enabled advisories" in convergent
    assert "Repair authority" in convergent
    assert "advisory patch-ready handoff" not in convergent
    assert "never affect confidence or a terminal decision" in advisory
    assert "Never demote" in advisory


def test_audit_codebase_is_serial_cumulative_html_report() -> None:
    skill_dir = CUSTOM / "audit-codebase"
    audit = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    defect = (skill_dir / "DEFECT-CONTRACT.md").read_text(encoding="utf-8")
    quality = (skill_dir / "QUALITY-LENS.md").read_text(encoding="utf-8")
    candidate = (skill_dir / "CANDIDATE-CONTRACT.md").read_text(encoding="utf-8")
    candidate_flat = " ".join(candidate.split())
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
    report_flat = " ".join(report.split())
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    map_section = audit.split("## Map", 1)[1].split("## Audit One Subsystem", 1)[0]
    audit_section = audit.split("## Audit One Subsystem", 1)[1].split(
        "## Analyze One Candidate", 1
    )[0]
    analyze_section = audit.split("## Analyze One Candidate", 1)[1]

    assert not implicit_policy(skill_dir)
    assert "**Root-owned:**" in audit
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
    assert "It is the sole durable map" in report
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
    assert "Map:     Pin or verify snapshot -> Map remaining repository -> Publish" in audit
    assert "Choose one branch:" in audit
    for branch in ("**New:**", "**Continue:**", "**Refresh:**"):
        assert branch in audit
    assert "Invocation outcome: complete | incomplete | blocked" in audit
    assert "Map: none | incomplete | complete" in audit
    assert "Subsystem: none | mapped | incomplete | audited" in audit
    assert (
        "Candidate: none | presented | decision pending | analyzed | disproved | blocked"
        in audit
    )
    assert "shared infrastructure with one audit-owning subsystem" in audit
    assert "Do not audit or rank a subsystem during Map" in " ".join(audit.split())
    assert "the user selects one subsystem" in audit
    assert "Audit never selects either" in " ".join(audit.split())
    assert "Next selection authority: user" in audit
    assert "offline and script-free" not in audit
    assert "## Burden Of Proof" in defect
    assert "Severity orders defects" in defect
    assert "## Suggest One Owner" not in defect
    for severity in ("P0", "P1", "P2", "P3"):
        assert f"**{severity}:**" in defect
    assert "Downstream execution: none" in audit
    assert "$audit-codebase analyze <candidate-id>" in audit
    assert "Invoke nothing" in audit
    assert "decision pending" in audit
    assert "Candidate analysis is optional." in audit
    assert "Never replace an explicit invalid, ambiguous, or stale Audit" in " ".join(
        audit.split()
    )
    assert "semantic rebuild or fresh audit" in audit
    assert "Snapshot: none | current | stale" in audit
    for route in (
        "$research",
        "$prototype",
        "$grill-with-docs",
        "$grilling",
        "$diagnosing-bugs",
        "$to-questionnaire",
        "$to-spec",
        "$to-tickets",
        "$implement",
        "$simplify-code",
        "$codebase-design",
        "$wayfinder",
    ):
        assert route in candidate
    assert "Cross-session transport is not a semantic route" in candidate_flat
    assert "$tdd" not in defect
    assert "One non-reduction direct item has settled outcome" in candidate
    assert "Suggested invocation:" in candidate
    assert "candidate ID, absolute report" in candidate
    assert "Result recipient:" in candidate
    assert "Audit re-entry:" in candidate
    assert "gap-only hypotheses" in candidate.lower()
    assert "declared:<lens-id>" in candidate
    assert "Questionnaire ready` is not answer evidence" in candidate
    assert "unchanged exhausted or blocked return" in candidate
    assert "authority, commitments, acceptance, dependency meaning" in candidate_flat
    assert (
        "Multiple interdependent unresolved decisions or prerequisites"
        in candidate_flat
    )
    assert "implementation requires multiple slices" in candidate_flat
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
    assert "Smallest sufficient change:" in candidate
    assert "Structural change:" in candidate
    assert "Replacement:" in candidate
    assert "Domain Delta" in candidate
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
    assert "runtime JavaScript" in report_flat
    assert "## Dark Theme" in report
    assert "## Snapshot Manifest" in report
    assert "### Resume Gate" in report
    assert "### Finalize Gate" in report
    assert "## Scope And Evidence Gaps" in report
    assert "report path is excluded from the" in report
    assert '<meta name="color-scheme" content="dark">' in report
    assert ":root { color-scheme: dark; }" in report
    assert "--background: #0b1020;" in report
    assert "--text: #f3f4f6;" in report
    assert "Do not add a light-theme toggle" in report
    assert "Never encode status by color alone" in report_flat
    assert "## Linked System Map" in report
    assert "## File Coverage" in report
    assert "## Subsystem Audit" in report
    assert "## Candidate Cards" in report
    assert "## Candidate Analysis" in report
    assert "## Navigation" in report
    assert "## Atomic Publish And Verification" in report
    assert "atomically replace `report.html`" in report
    assert "source-report SHA-256" in report
    assert "resolved `HEAD` tree plus a sorted overlay" in report
    assert "explicit deletion marker instead of a hash" in report_flat
    assert "native `<details>`" in report
    assert "strict internal ASCII grammar" in report
    assert "item-defect-<subsystem-id>-<item-id>" in report
    assert "when present, otherwise" in report
    assert '<html lang="en">' in report
    assert "<caption>" in report
    assert 'role="img"' in report
    assert "An identity mismatch permits only one atomic status update" in report_flat
    assert "an explicitly requested fresh audit shows only Refresh" in report_flat
    assert '<section id="system-<system-id>">' in report
    assert '<section id="subsystem-<subsystem-id>">' in report
    assert "display no placeholder token" in report
    assert "Invocation outcome: complete | incomplete | blocked" in report
    assert "Snapshot status: current | stale" in report
    assert "Map status: incomplete | complete" in report
    assert "candidate links inside their owning subsystem" in report
    assert "Never require one diagram to contain the whole repository" in " ".join(
        report.split()
    )
    assert "Never rank subsystems or add a global recommendation" in report
    assert "subsystem-local recommendation" in report
    assert "user selection required" in report
    assert re.search(
        r"(?m)^\| A repository needs an exhaustive system map, serial subsystem audit, .*performance \| `\$audit-codebase` \|$",
        router,
    )


def test_convergent_review_returns_a_lock_usable_decision() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    decision_section = convergent.split("Derive exactly one decision", 1)[1].split(
        "Never let an advisory", 1
    )[0]
    decisions = set(
        re.findall(
            r"(?m)^- `(pass|pass with residual risk|blocked|incomplete)`",
            decision_section,
        )
    )
    assert decisions == {"pass", "pass with residual risk", "blocked", "incomplete"}
    ledger_sentence = convergent.split("exactly one state:", 1)[1].split(".", 1)[0]
    ledger_states = set(re.findall(r"`([^`]+)`", ledger_sentence))
    assert ledger_states == {"candidate", "accepted", "rejected", "duplicate", "disputed"}


def test_convergent_review_checks_snapshot_drift_not_baseline_drift() -> None:
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(encoding="utf-8")

    verify = convergent.split("## 6. Read Back Drift", 1)[1].split(
        "## 7. Decide, Return, And Stop", 1
    )[0]
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

    review_section = implement.split("## Review", 1)[1].split("## Close", 1)[0]
    assert "Invoke exactly one formal route" in review_section
    assert re.findall(r"`\$(review|convergent-pr-review)`", review_section)[:2] == [
        "review",
        "convergent-pr-review",
    ]
    assert "Finding Contract" in review_section
    assert "complete caller-admitted" in review_section
    assert "mixed-authority, partial, out-of-scope, or" in review_section


def test_audit_codebase_replaces_improve_codebase() -> None:
    audit = (CUSTOM / "audit-codebase/SKILL.md").read_text(encoding="utf-8")
    quality = (CUSTOM / "audit-codebase/QUALITY-LENS.md").read_text(encoding="utf-8")
    candidate = (CUSTOM / "audit-codebase/CANDIDATE-CONTRACT.md").read_text(
        encoding="utf-8"
    )

    assert not (CUSTOM / "improve-codebase/SKILL.md").exists()
    assert "stale code" in quality.lower()
    assert "complexity" in audit.lower()
    assert "Deep Module" in audit
    assert "deepening" in candidate
    assert "Collapse" in audit
    assert "retain" in quality
    assert "Top recommendation" in candidate or "Recommendation strength" in candidate
    assert "decision pending" in candidate


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
    assert "$audit-codebase" in refactoring


def test_simplify_code_is_explicit_bounded_and_behavior_preserving() -> None:
    skill_dir = CUSTOM / "simplify-code"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    trace = skill.split("## Trace And Baseline", 1)[1].split("## Choose", 1)[0]
    choose = skill.split("## Choose", 1)[1].split("## Cut", 1)[0]
    choose_flat = " ".join(choose.split())

    assert not implicit_policy(skill_dir)
    assert "one unstaged, behavior-preserving reduction" in skill
    assert "No safe simplification" in skill
    assert "smallest trusted proof" in skill
    assert "before and after" in skill
    assert "Refresh changed paths and work state after proof" in skill
    assert "evidence proves no use remains" in skill
    assert "staged-state shape" in skill
    assert "keeps the index and unrelated state as found" in skill_flat
    assert "Without a bounded target, recommend `$audit-codebase` and stop" in skill_flat
    assert "current analyzed candidate" in skill
    assert "verified `$audit-codebase` report" in skill
    assert "behavior-preserving reduction" in skill
    assert "verified `$audit-codebase` atlas" not in skill
    assert "Reuse its Source Trace, supported behavior, proof seam" in trace
    assert "refresh only its affected files, callers" in trace
    assert "Do not repeat wide tracing or reopen the full reduction ladder" in trace
    assert "resurvey the ladder only when refreshed evidence invalidates" in choose
    assert "configuration, compatibility, or abstraction proved" in choose
    assert "deepen, merge, or inline only within settled existing boundaries" in (
        choose_flat
    )
    assert "Known Ceiling" in choose
    assert "Revisit Trigger" in choose
    assert "Enter only when the user explicitly requests `until-clean`" in skill
    assert "`Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`" in skill
    assert re.findall(r"(?m)^\d\. \*\*([^*]+)\*\*", skill.split("## Choose", 1)[1])[:5] == [
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
    branch = skill.split("## Until Clean", 1)[1].split("## Return And Completion", 1)[0]
    branch_flat = " ".join(branch.split())

    assert "names one region" in branch
    assert "finite positive successful-cut budget" in branch
    assert "Hold one invariant behavior contract and proof seam" in branch_flat
    assert "`3` successful cuts by default" in branch_flat
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

    returned = skill.split("## Return And Completion", 1)[1]
    returned_flat = " ".join(returned.split())
    assert "campaign budget and ledger when applicable" in returned_flat


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
    assert re.findall(r"(?m)^### \d+\. (.+)$", to_spec) == [
        "Setup",
        "Trace settled source and state",
        "Draft and cover",
        "Publish, verify, and reconcile",
    ]
    normalized = " ".join(to_spec.split())
    assert "Delegate exactly one create operation" in normalized
    assert "compare it with the frozen draft" in normalized
    assert "recommend `$to-tickets` only after verified success" in normalized


def test_implementation_closeout_requires_the_spec_axis() -> None:
    review = (CUSTOM / "review/SKILL.md").read_text(encoding="utf-8")
    convergent = (CUSTOM / "convergent-pr-review/SKILL.md").read_text(
        encoding="utf-8"
    )
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    for text in (review, convergent):
        assert "`Spec required: yes | no`" in text
    assert "Supply the required Spec" in " ".join(implement.split())
    assert "`Spec required: yes`" in " ".join(parallel.split())


def test_interface_alternatives_receive_curated_fresh_context() -> None:
    design = (CUSTOM / "codebase-design/DESIGN-IT-TWICE.md").read_text(
        encoding="utf-8"
    )
    research = (CUSTOM / "research/SKILL.md").read_text(encoding="utf-8")
    audit = (CUSTOM / "audit-codebase/SKILL.md").read_text(encoding="utf-8")

    assert 'fork_turns="none"' in design
    assert 'fork_turns="none"' not in research
    assert 'fork_turns="none"' not in audit
    assert "Do not delegate, fan out" in audit


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
    assert research.index("## Output") < research.index("## Verify And Return")
    assert "Return to the caller without deciding its artifact" in research
    assert "starting downstream work" in research


def test_writing_great_skills_keeps_promoted_package_and_relationship_boundary() -> None:
    skill_dir = CUSTOM / "writing-great-skills"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")

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
    assert "fork_turns" not in skill
    assert (
        "bundled system `skill-creator` owns new-package scaffolding and metadata mechanics"
        in relationships
    )
    assert "$writing-great-skills` owns semantic quality" in relationships


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
        if name == "implement":
            assert "Mutation read-back" in text
            assert "partial or failed closeout Returns" in " ".join(text.split())
        elif name == "parallel-implement":
            assert "mutation read-back" in text
            assert "read that mutation back" in text
        elif name == "to-spec":
            normalized = " ".join(text.split())
            assert "Refetch or reread the full created parent" in normalized
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
    assert "finite repair generation budget" in shape_contract
    assert "settled source or user" in shape_contract
    assert "otherwise set it to exactly `2`" in shape_contract
    assert "do not infer a higher budget from ticket size or risk" in shape_contract
    assert "expand-migrate-contract" in shape_contract
    assert re.search(r"contract only after old usage ends", shape_contract)

    publish_contract = level_two_section("Publish")
    assert re.search(r"freeze .*before .*mutation", publish_contract, re.S)
    assert re.search(
        r"create .*relationship.*(?:mapped state|activate mapped ready-for-agent)",
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
    assert "non-empty ready frontier" in shape_contract
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
            "9fcd60991c88bfca2561d588762b812bb64bc0451497d964e40aa7fec2779c7a",
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

    if profile == "incumbent":
        assert re.findall(r"(?m)^### \d+\. ([A-Za-z ,]+)$", skill) == [
            "Setup",
            "Trace settled source and state",
            "Draft and cover",
            "Publish, verify, and reconcile",
        ]
        for incumbent_semantic in (
            "one durable parent specification",
            "bidirectional commitment ledger",
            "mutation read-back",
            "publication-recovery",
            "published-spec",
            "$repo-bootstrap",
            "$to-tickets",
        ):
            assert incumbent_semantic in normalized
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
            "3cdb41fbca411d8c2332c4e9cff52b5ef1000dd28a27422615ac6f150133e06b",
            "incumbent",
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


def test_worker_modes_have_distinct_completion_artifacts() -> None:
    contract = (ROOT / "docs/agents/engineering-contract.md").read_text(encoding="utf-8")
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")
    parallel = (CUSTOM / "parallel-implement/SKILL.md").read_text(encoding="utf-8")

    assert "**staged worker**" in contract
    assert "**lane worker**" in contract
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
    parallel_steps = re.findall(r"(?m)^## (.+)$", parallel)
    expected_steps = [
        "Admission",
        "Trace",
        "Select",
        "Open",
        "Drain",
        "Review",
        "Lock",
    ]
    assert all(step in parallel_steps for step in expected_steps)
    assert [parallel_steps.index(step) for step in expected_steps] == sorted(
        parallel_steps.index(step) for step in expected_steps
    )
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
    drain = parallel.split("## Drain", 1)[1].split("## Review", 1)[0]
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
    lock = parallel.split("## Lock", 1)[1]
    assert "claim" in parallel.split("## Open", 1)[1].split("## Drain", 1)[0]
    assert "read back" in parallel.lower()
    assert "closeout plan" in lock and "mutation read-back" in lock
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
    assert "Dispatch concurrently only when" in gate
    assert "otherwise dispatch serially" in gate
    assert "return the exact blockers" in gate

    review = parallel.split("## Review", 1)[1].split("## Lock", 1)[0]
    lock = parallel.split("## Lock", 1)[1]
    assert "$review" in review
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
    assert "Do not copy field-by-field event contracts" in ledger
    assert {
        "serial-frontier",
        "parallel-frontier",
        "child-closeout",
        "parent-closeout",
    } <= event_types
    assert "serial tripwires" in gate and "otherwise dispatch serially" in gate

    assert re.search(r"(?m)^\| One parent spec or PRD .* \| `\$parallel-implement` \|$", router)
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
    admit_span = skill_pack_contract.level_two_section_span(tickets, "## Admit")
    shape_span = skill_pack_contract.level_two_section_span(tickets, "## Shape")
    assert admit_span is not None and shape_span is not None
    admit = " ".join(tickets[slice(*admit_span)].split()).lower()
    shape = " ".join(tickets[slice(*shape_span)].split()).lower()
    assert "engineering contracts" in admit
    assert "foreign contracts" in admit
    assert "state-boundary matrix" in shape
    assert "supported" in shape and "not applicable" in shape
    assert "graph defect" in parallel
    assert "final proof across all applicable\nstate-boundary branches" in parallel
    assert "State-boundary matrix:" in worker
    assert "return it as `needs-feedback`" in worker
    assert "This compatibility field is not a campaign" in ledger
    assert "outcome or completion proxy" in ledger


def test_implement_selection_preserves_one_ready_item_and_explicit_authority() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    assert not implicit_policy(CUSTOM / "implement")
    assert "Accept one caller-selected item only" in implement
    assert "A named target remains binding" in implement
    assert "do not substitute another item" in implement
    assert "exhaustive parent graph to\n`$parallel-implement`" in implement
    assert "staged worker" not in implement


def test_local_tracker_closeout_enters_the_lock_snapshot() -> None:
    implement = (CUSTOM / "implement/SKILL.md").read_text(encoding="utf-8")

    review_tree = implement.index("pin one immutable proved candidate")
    closeout = implement.index("For Local Markdown, append the final closeout")
    lock_tree = implement.index("Lock the exact reviewed candidate")

    assert review_tree < closeout < lock_tree
    assert "apply Mutation read-back" in implement
    assert "Any other review-to-lock delta Returns to formal review" in implement


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
        ("wayfinder", "Recommend and stop", "grill-with-docs"),
        ("wayfinder", "Recommend and stop", "domain-modeling"),
        ("wayfinder", "Recommend and stop", "to-spec"),
        ("triage", "Recommend and stop", "grill-with-docs"),
        ("implement", "Invoke", "tdd"),
        ("implement", "Invoke", "diagnosing-bugs"),
        ("implement", "Invoke", "review"),
        ("implement", "Invoke", "convergent-pr-review"),
        ("review", "Hand off", "convergent-pr-review"),
        ("review", "Recommend and stop", "audit-codebase"),
        ("convergent-pr-review", "Recommend and stop", "audit-codebase"),
        ("parallel-implement", "Invoke", "convergent-pr-review"),
        ("parallel-implement", "Invoke", "resolving-merge-conflicts"),
        ("resolving-merge-conflicts", "Invoke", "diagnosing-bugs"),
        ("audit-codebase", "Recommend and stop", "grill-with-docs"),
        ("audit-codebase", "Recommend and stop", "grilling"),
        ("audit-codebase", "Recommend and stop", "research"),
        ("audit-codebase", "Recommend and stop", "prototype"),
        ("audit-codebase", "Recommend and stop", "diagnosing-bugs"),
        ("audit-codebase", "Recommend and stop", "to-questionnaire"),
        ("audit-codebase", "Recommend and stop", "codebase-design"),
        ("audit-codebase", "Recommend and stop", "wayfinder"),
        ("audit-codebase", "Recommend and stop", "to-spec"),
        ("audit-codebase", "Recommend and stop", "to-tickets"),
        ("audit-codebase", "Recommend and stop", "simplify-code"),
        ("audit-codebase", "Recommend and stop", "implement"),
        ("simplify-code", "Recommend and stop", "audit-codebase"),
        ("simplify-code", "Recommend and stop", "codebase-design"),
        ("tdd", "Hand off", "diagnosing-bugs"),
        ("tdd", "Hand off", "prototype"),
        ("tdd", "Recommend and stop", "simplify-code"),
        ("tdd", "Recommend and stop", "codebase-design"),
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
    assert ("audit-codebase", "Load", "codebase-design") not in edges
    assert ("audit-codebase", "Invoke", "codebase-design") not in edges
    assert ("convergent-pr-review", "Hand off", "review") not in edges
    assert ("wayfinder", "Recommend and stop", "to-tickets") not in edges
    assert ("wayfinder", "Recommend and stop", "implement") not in edges
    assert ("to-questionnaire", "Recommend and stop", "grill-with-docs") not in edges
    assert ("research", "Recommend and stop", "to-questionnaire") not in edges

    wayfinder = (CUSTOM / "wayfinder/SKILL.md").read_text(encoding="utf-8")
    closure = wayfinder.split("## Closure", 1)[1].split("\n## ", 1)[0]
    assert "`$to-spec`" in closure
    assert "successfully delivered implementation map" in closure
    assert "`$to-tickets`" not in closure
    assert "`$implement`" not in closure
    assert "`$parallel-implement`" not in closure

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

    assert "target-spine.md" not in synthesis_index
    assert "language-direction.md" not in synthesis_index
    assert "support tickets" not in tickets
    assert "support slices" not in tickets
