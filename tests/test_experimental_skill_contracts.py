from __future__ import annotations

import re
import runpy
from pathlib import Path

from scripts.skill_pack_contract import tree_hash


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"
EXPERIMENTAL = ROOT / "skills/experimental"


def test_promoted_domain_modeling_preserves_compact_ddd_contract() -> None:
    skill_dir = CUSTOM / "domain-modeling"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    context_format = (skill_dir / "CONTEXT-FORMAT.md").read_text(encoding="utf-8")
    context_format_flat = " ".join(context_format.split())
    adr_format = (skill_dir / "ADR-FORMAT.md").read_text(encoding="utf-8")
    adr_format_flat = " ".join(adr_format.split())
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")

    for contract in (
        "Model, don't catalog.",
        "Trace -> Challenge -> Resolve -> (Persist -> Verify | Render) -> Return",
        "language collisions",
        "model boundaries",
        "contradictions",
        "evidence settles source facts",
        "the direct user unless a source names another authority",
        "Direct use may ask focused questions",
        "Bounded contexts follow model, language, responsibility, and consistency boundaries",
        "Create the first record only for an authorized settled resolution",
        "`persist authorized`",
        "`render only`",
        "return the accepted topology and exact setup requirement",
        "preserve verified changes",
        "Domain Delta",
        "$grill-with-docs",
        "Semantic outcome: no-change | resolved | partial | unresolved",
        "Persistence outcome: complete | partial | failed | not-applicable",
        "Return every other consequence or residual to its owner and stop",
    ):
        assert contract in skill_flat

    for contract in (
        "## Invariants",
        "Authority:",
        "Language: <owner, reference, or explicit translation>",
        "Partnership",
        "Customer/Supplier Development",
        "Anticorruption Layer",
        "Published Language",
        "Separate Ways",
        "Big Ball of Mud",
        "it is not itself a Context Mapping pattern",
        "A boundary that translates into a distinct local model is an **Anticorruption Layer**, not Conformist",
        "A versioned or published schema alone does not establish it",
    ):
        assert contract in context_format_flat

    for contract in (
        "Hard to reverse",
        "Surprising without context",
        "Real trade-off",
        "explicit approval",
        "already-settled",
    ):
        assert contract in adr_format_flat

    for rejected in (
        "Trace -> Challenge -> Resolve -> Reconcile",
        "Overload, Alias, Leakage, Boundary, and Contradiction",
        "$skill-router",
        "Domain subject and source:",
    ):
        assert rejected not in skill

    assert {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file()
    } == {
        "ADR-FORMAT.md",
        "CONTEXT-FORMAT.md",
        "SKILL.md",
        "agents/openai.yaml",
    }
    assert policy == "policy:\n  allow_implicit_invocation: true\n"


def test_promoted_grilling_and_domain_modeling_preserve_composer_inputs() -> None:
    grilling_dir = CUSTOM / "grilling"
    domain_dir = CUSTOM / "domain-modeling"
    grilling = (grilling_dir / "SKILL.md").read_text(encoding="utf-8")
    grilling_plain = " ".join(grilling.replace("**", "").split())
    grilling_policy = (grilling_dir / "agents/openai.yaml").read_text(
        encoding="utf-8"
    )
    domain = (domain_dir / "SKILL.md").read_text(encoding="utf-8")
    domain_flat = " ".join(domain.split())

    for contract in (
        "Maintain the decision frontier",
        "Let blocked evidence pause only its dependent branches",
        "Relay every settled material answer",
        "pause dependent progress",
        "domain collision or blocker returns",
        "Grilling owns materiality, not domain consequences",
        "Spec source: ready | not ready | not requested",
        "Add caller identifiers when supplied",
    ):
        assert contract in grilling_plain

    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(
        encoding="utf-8"
    )
    grill_docs_plain = " ".join(grill_docs.split())
    for contract in (
        "every returned collision or blocker to Grilling",
        "never merge or reinterpret it",
        "Any material blocker in the current Domain Delta makes the "
        "combined status `Blocked`",
        "Composition blocker, owner, and re-entry condition",
    ):
        assert contract in grill_docs_plain

    for contract in (
        "accept every settled material answer",
        "including one with no durable consequence",
        "Return the authoritative cumulative Domain Delta and any collision before dependent questioning continues",
        "never choose interview materiality or branching",
    ):
        assert contract in domain_flat

    for contract in (
        'display_name: "Grilling"',
        'short_description: "Stress-test thinking one question at a time"',
        "allow_implicit_invocation: true",
    ):
        assert contract in grilling_policy

    assert (domain_dir / "agents/openai.yaml").read_text(
        encoding="utf-8"
    ) == "policy:\n  allow_implicit_invocation: true\n"


def test_promoted_prototype_preserves_selected_leaf_contract() -> None:
    skill_dir = CUSTOM / "prototype"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    logic_flat = " ".join(logic.split())
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    ui_flat = " ".join(ui.split())
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")
    measure_flat = " ".join(measure.split())
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    wayfinder_map = (CUSTOM / "wayfinder" / "MAP-FORMAT.md").read_text(
        encoding="utf-8"
    )
    wayfinder = (CUSTOM / "wayfinder" / "SKILL.md").read_text(encoding="utf-8")
    wayfinder_flat = " ".join(wayfinder.split())

    assert (
        "description: Prototype one bounded design question with a disposable "
        "runnable probe; exclude production proof, uncertain defects, and "
        "multi-decision design."
        in skill
    )

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
        "Production correctness remains with the real coding workflow",
    ):
        assert contract in skill_flat

    for removed in (
        "supported_direction",
        "Before mutation, read back five locks",
        "status: answered | awaiting-verdict | blocked | not-admitted",
        "[RESUME.md](RESUME.md)",
        "$skill-router",
        "$handoff",
        "$domain-modeling",
    ):
        assert removed not in skill

    assert "happy, boundary, and rejected cases" in logic_flat
    assert "repeated runs are equivalent" in logic_flat
    assert "positively isolates the whole prototype surface" in ui_flat
    assert "never exceed five" in ui_flat
    assert "actual browser or target UI" in ui_flat
    assert "variance and worst observed result" in measure_flat
    assert "known confounders and unsupported extrapolations" in measure_flat
    assert "does not diagnose an unexplained slowdown" in measure_flat
    assert "Decision owner: <who>" in wayfinder_map
    assert "Claim level: shape/feel | design evidence" in wayfinder_map
    assert "Judgment mode: human | rule-based" in wayfinder_map
    assert "with the decision owner, claim level, judgment mode" in wayfinder_flat
    assert "human judge or objective verdict criteria" in wayfinder_flat
    for branch in (logic_flat, ui_flat, measure_flat):
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


def test_current_implement_preserves_promoted_and_author_contract() -> None:
    canonical_dir = CUSTOM / "implement"
    inventory = {"SKILL.md", "agents/openai.yaml"}

    assert {
        path.relative_to(canonical_dir).as_posix()
        for path in canonical_dir.rglob("*")
        if path.is_file()
    } == inventory

    assert tree_hash(canonical_dir) == (
        "479b5242121887c38cdb2139da93f77e5dd57589086e462f58c34fc8e6ffaab5"
    )
    promoted = (canonical_dir / "SKILL.md").read_text(encoding="utf-8")
    normalized = " ".join(promoted.split())

    for contract in (
        "Deliver exactly one caller-selected ready item",
        "Keep the named item and all source-owned commitments unchanged",
        "exhaustive parent graph to `$parallel-implement`",
        "conflicts to `$resolving-merge-conflicts`",
        "Freeze one Charter",
        "otherwise default to exactly `2`",
        "Pin classification and Finding Contract",
        "complete caller-admitted, Charter-preserving batch",
        "mechanical Local Markdown closeout after review and before Lock",
        "Retain GitHub or GitLab claims through Lock and commit",
        "Create exactly one commit",
        "proving `HEAD` unchanged",
        "Complete connector closeout",
        "connector failure, preserve the commit, refetch state",
        "Tracker closeout, claim, and frontier:",
        "Before commit, release a claim only after",
        "After commit, retain custody until closeout",
        "index and commit trees to equal the locked tree",
        "named recovery custodian",
        "Return `complete` only when acceptance, proof, review, Lock",
    ):
        assert contract in normalized

    for rejected in (
        "staged worker",
        "two generations",
        "Invoke exactly one campaign route",
        "`automatic-in-scope`",
    ):
        assert rejected not in promoted
