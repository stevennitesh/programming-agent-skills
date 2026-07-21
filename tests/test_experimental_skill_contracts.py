from __future__ import annotations

import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTAL = ROOT / "skills/experimental"


def test_experimental_domain_modeling_preserves_compact_ddd_contract() -> None:
    skill_dir = EXPERIMENTAL / "domain-modeling"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    context_format = (skill_dir / "CONTEXT-FORMAT.md").read_text(encoding="utf-8")
    adr_format = (skill_dir / "ADR-FORMAT.md").read_text(encoding="utf-8")
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")

    for contract in (
        "Model, don't catalog.",
        "Trace -> Challenge -> Resolve -> Reconcile -> (Persist -> Verify | Render) -> Return",
        "Overload, Alias, Leakage, Boundary, and Contradiction",
        "evidence settles source facts",
        "Bounded contexts follow model and responsibility boundaries",
        "Create no empty record",
        "`persist authorized`",
        "`render only`",
        "routing/setup",
        "persistence/verification",
        "Domain Delta",
        "$grill-with-docs",
        "$skill-router",
    ):
        assert contract in skill

    for contract in (
        "## Invariants",
        "Authority:",
        "owner | reference | translation | shared kernel",
        "customer-supplier | conformist | shared kernel | translation",
    ):
        assert contract in context_format

    for contract in (
        "Hard to reverse",
        "Surprising without context",
        "Real trade-off",
        "explicit approval",
        "already settled",
    ):
        assert contract in adr_format

    assert policy == "policy:\n  allow_implicit_invocation: true\n"


def test_experimental_grill_with_docs_preserves_concise_composer_contract() -> None:
    skill_dir = EXPERIMENTAL / "grill-with-docs"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")

    for contract in (
        "Admit -> Disclose -> Compose [Grill <-> Relay <-> Model] -> Join -> Return",
        "a direct user, Wayfinder, Triage, or Improve Codebase",
        "an admission-ready bound and authority lock for each component",
        "`persist authorized` or `render only`",
        "ADR creation always requires separate explicit approval",
        "Relay each settled material answer",
        "Domain Modeling's authoritative current cumulative Domain Delta",
        "The composer filters or merges neither",
        "Status: Confirmed | Evidence gap | Blocked",
        "This is a return, not a general handoff",
        "downstream execution remains unstarted",
    ):
        assert contract in skill

    assert "## Align" not in skill
    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {"SKILL.md", "agents/openai.yaml"}
    assert policy == "policy:\n  allow_implicit_invocation: true\n"


def test_experimental_composer_family_shares_one_relay_handshake() -> None:
    grilling_dir = EXPERIMENTAL / "grilling"
    domain_dir = EXPERIMENTAL / "domain-modeling"
    composer_dir = EXPERIMENTAL / "grill-with-docs"
    grilling = (grilling_dir / "SKILL.md").read_text(encoding="utf-8")
    domain = (domain_dir / "SKILL.md").read_text(encoding="utf-8")
    composer = (composer_dir / "SKILL.md").read_text(encoding="utf-8")

    for contract in (
        "return each settled material answer",
        "pause dependent questioning",
        "Integrate the returned domain collision or blocker",
        "never classify the domain consequence yourself",
        "caller identity and opaque identifiers when supplied",
    ):
        assert contract in grilling

    for contract in (
        "accept every settled material answer",
        "including answers with no durable consequence",
        "return any collision or blocker before dependent Grilling progress",
        "Never decide answer materiality or interview branching",
        "every composed answer has a returned current delta",
    ):
        assert contract in domain

    for contract in (
        "an admission-ready bound and authority lock for each component",
        "Each component validates its own requirements",
        "Relay each settled material answer",
        "return every material collision or blocker to Grilling",
        "The composer filters or merges neither",
    ):
        assert contract in composer

    for skill_dir in (grilling_dir, domain_dir, composer_dir):
        assert (skill_dir / "agents/openai.yaml").read_text(
            encoding="utf-8"
        ) == "policy:\n  allow_implicit_invocation: true\n"


def test_experimental_prototype_preserves_selected_leaf_contract() -> None:
    skill_dir = EXPERIMENTAL / "prototype"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")

    for contract in (
        "Admit -> Freeze -> Load -> Probe -> Smoke -> Judge -> Reconcile -> Return",
        "request_subject",
        "Before mutation, read back five locks",
        "claim_kind: shape/feel | design-evidence",
        "judgment_mode: human | rule-based",
        ".tmp/prototype/<question-slug>/",
        "Load exactly one branch reference",
        "[MEASURE.md](MEASURE.md)",
        "preserve-for-verdict",
        "authorized-durable-evidence",
        "No terminal return leaves a live resource",
        "Resume is permitted only from an `awaiting-verdict` packet",
        "invoke `$skill-router` only when the active Router policy admits terminal residuals",
        "one `verdict`",
        "every started operation either meets its criterion or returns `blocked`",
    ):
        assert contract in skill

    for removed in (
        "supported_direction",
        "Admit -> Freeze -> Branch",
    ):
        assert removed not in skill
    assert (
        "Do not add universal `last_operation` or `next_required_action` fields"
        in skill
    )

    assert "happy, boundary, and rejected cases" in logic
    assert "repeated runs are equivalent" in logic
    assert "positively isolates the whole prototype surface" in ui
    assert "never exceed five" in ui
    assert "actual browser or target UI" in ui
    assert "variance and worst observed result" in measure
    assert "known confounders and unsupported extrapolations" in measure
    assert "does not diagnose an unexplained slowdown" in measure
    for branch in (logic, ui, measure):
        assert "Return to `Judge` in [SKILL.md](SKILL.md)" in branch
        assert "this branch does not Reconcile or Return" in branch

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
    assert policy == "policy:\n  allow_implicit_invocation: true\n"


def test_experimental_repo_bootstrap_preserves_per_file_reconciliation() -> None:
    bootstrap = (EXPERIMENTAL / "repo-bootstrap/SKILL.md").read_text(
        encoding="utf-8"
    )

    for rule in (
        "do not wait until Verify",
        "Compare every managed surface",
        "setup-file",
        "Markers are provenance evidence",
    ):
        assert rule in bootstrap


def test_experimental_repo_bootstrap_validates_each_managed_source() -> None:
    skill_dir = EXPERIMENTAL / "repo-bootstrap"
    validator = runpy.run_path(str(skill_dir / "scripts/validate_setup.py"))
    targets = {
        "docs/agents/issue-tracker.md": skill_dir / "issue-tracker-github.md",
        "docs/agents/triage-labels.md": skill_dir / "triage-labels.md",
        "docs/agents/domain.md": skill_dir / "domain.md",
        "docs/agents/engineering-contract.md": skill_dir / "engineering-contract.md",
    }

    for relative, template in targets.items():
        text = template.read_text(encoding="utf-8")
        marker = validator["expected_setup_file_marker"](relative, text)
        first_line, remainder = text.split("\n", 1)
        installed_text = f"{first_line}\n\n{marker}\n\n{remainder}"
        assert validator["setup_file_marker_failures"](
            installed_text, relative, marker
        ) == []
        stale = re.sub(r":[0-9a-f]{12} -->", ":deadbeefdead -->", marker)
        failures = validator["setup_file_marker_failures"](
            installed_text.replace(marker, stale), relative, marker
        )
        assert failures == [
            f"{relative} must contain exactly one current setup-file source marker: "
            f"{marker}"
        ]

    assert "**State-boundary matrix.**" in validator["CONTRACT_LITERAL_TOKENS"]


def test_experimental_aggregate_marker_cannot_hide_stale_setup_file() -> None:
    skill_dir = EXPERIMENTAL / "repo-bootstrap"
    validator = runpy.run_path(str(skill_dir / "scripts/validate_setup.py"))
    relative = "docs/agents/engineering-contract.md"
    current = (skill_dir / "engineering-contract.md").read_text(encoding="utf-8")
    expected = validator["expected_setup_file_marker"](relative, current)

    assert validator["setup_schema_marker_failures"](
        validator["SETUP_SCHEMA_TOKEN"]
    ) == []
    failures = validator["setup_file_marker_failures"](
        current.replace(expected, ""), relative, expected
    )
    assert failures == [
        f"{relative} must contain exactly one current setup-file source marker: "
        f"{expected}"
    ]
