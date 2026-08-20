from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"
EXPERIMENTAL = ROOT / "skills/experimental"
def test_retired_wayfinder_is_absent_from_experimental_runtime() -> None:
    assert not (EXPERIMENTAL / "wayfinder").exists()
    manifest = json.loads((EXPERIMENTAL / "manifest.json").read_text(encoding="utf-8"))
    assert "wayfinder" not in manifest["skills"]


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
        "## 1. Ground",
        "## 2. Clarify",
        "## 3. Settle",
        "## 4. Capture",
        "## 5. Return",
        "They do not settle intended meaning",
        "scenario only when its answer could change the model",
        "explicit persistence request or exact caller authority",
        "ADR recording always needs separate approval",
        "every verified intermediate state retains readable current truth",
        "Reread every attempted target",
        "return each unapplied consequence to its owner",
        "authoritative cumulative Domain Delta",
        "$grill-with-docs",
        "Do not mutate foreign-owner consequences",
    ):
        assert contract in skill_flat

    for contract in (
        "## Invariants",
        "non-obvious durable distinction",
        "Never force a pattern",
        "Preserve independent meanings across contexts",
        "Revise or remove covered or conflicting material",
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
        "Semantic outcome:",
        "Persistence outcome:",
        "persist authorized",
        "render only",
        "offer only",
        "Big Ball of Mud",
    ):
        assert rejected not in skill and rejected not in context_format

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
        "decision frontier",
        "blocked branch pause only its dependents",
        "trace real callers and existing constraints",
        "Never repeat an unchanged question",
        "Include caller identifiers only when supplied",
    ):
        assert contract in grilling_plain

    grill_docs = (CUSTOM / "grill-with-docs/SKILL.md").read_text(
        encoding="utf-8"
    )
    grill_docs_plain = " ".join(grill_docs.split())
    for contract in (
        "every returned collision or blocker to Grilling",
        "never merge or reinterpret it",
        "A material Domain Delta blocker prevents a confirmed combined result",
        "return that blocker, its owner, and re-entry condition",
    ):
        assert contract in grill_docs_plain

    for contract in (
        "accept each settled material answer",
        "authoritative cumulative Domain Delta after every settled material answer",
        "including one with no durable consequence",
        "does not choose interview materiality",
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
