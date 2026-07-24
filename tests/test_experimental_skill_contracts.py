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
    context_format = (skill_dir / "CONTEXT-FORMAT.md").read_text(encoding="utf-8")
    adr_format = (skill_dir / "ADR-FORMAT.md").read_text(encoding="utf-8")
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
        assert contract in skill

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
        assert contract in context_format

    for contract in (
        "Hard to reverse",
        "Surprising without context",
        "Real trade-off",
        "explicit approval",
        "already-settled",
    ):
        assert contract in adr_format

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
    grilling_plain = grilling.replace("**", "")
    grilling_policy = (grilling_dir / "agents/openai.yaml").read_text(
        encoding="utf-8"
    )
    domain = (domain_dir / "SKILL.md").read_text(encoding="utf-8")

    for contract in (
        "Relay every settled material answer",
        "pause dependent progress",
        "domain collision or blocker returns",
        "Grilling owns materiality, not domain consequences",
        "Add caller identifiers when supplied",
    ):
        assert contract in grilling_plain

    for contract in (
        "accept every settled material answer",
        "including one with no durable consequence",
        "Return the authoritative cumulative Domain Delta and any collision before dependent questioning continues",
        "never choose interview materiality or branching",
    ):
        assert contract in domain

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
    logic = (skill_dir / "LOGIC.md").read_text(encoding="utf-8")
    ui = (skill_dir / "UI.md").read_text(encoding="utf-8")
    measure = (skill_dir / "MEASURE.md").read_text(encoding="utf-8")
    policy = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    wayfinder_map = (CUSTOM / "wayfinder" / "MAP-FORMAT.md").read_text(
        encoding="utf-8"
    )
    wayfinder = (CUSTOM / "wayfinder" / "SKILL.md").read_text(encoding="utf-8")

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
        assert contract in skill

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

    assert "happy, boundary, and rejected cases" in logic
    assert "repeated runs are equivalent" in logic
    assert "positively isolates the whole prototype surface" in ui
    assert "never exceed five" in ui
    assert "actual browser or target UI" in ui
    assert "variance and worst observed result" in measure
    assert "known confounders and unsupported extrapolations" in measure
    assert "does not diagnose an unexplained slowdown" in measure
    assert "Decision owner: <who>" in wayfinder_map
    assert "Claim level: shape/feel | design evidence" in wayfinder_map
    assert "Judgment mode: human | rule-based" in wayfinder_map
    assert "pass its decision owner, claim level, judgment mode" in wayfinder
    assert "human judge when human" in wayfinder
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


def test_prototype_b0_and_description_pruning_controls_are_exact() -> None:
    b0_dir = ROOT / "docs/validation/evals/prototype-b0"
    candidate_dir = CUSTOM / "prototype"
    description_control_dir = (
        ROOT / "docs/validation/evals/prototype-description-pre-prune"
    )

    assert tree_hash(b0_dir) == (
        "c1a79fa3a144e1cac39be80233e1a3a2756c2f5130af14d3bc20c53418c6d307"
    )
    assert tree_hash(candidate_dir) == (
        "ed5832972cbd1a093656087a7efc61e679f4068b3bea330204ba6559fb78ce33"
    )
    assert tree_hash(description_control_dir) == (
        "22614fe625ec8ecbb176ef8af07cb4c0b186e92dee1348f9efb85be10120f668"
    )

    assert {
        path.relative_to(b0_dir).as_posix()
        for path in b0_dir.rglob("*")
        if path.is_file()
    } == {"LOGIC.md", "SKILL.md", "UI.md", "agents/openai.yaml"}
    assert {
        path.relative_to(description_control_dir).as_posix()
        for path in description_control_dir.rglob("*")
        if path.is_file()
    } == {
        "LOGIC.md",
        "MEASURE.md",
        "SKILL.md",
        "UI.md",
        "agents/openai.yaml",
    }

    b0 = (b0_dir / "SKILL.md").read_text(encoding="utf-8")
    for required in (
        "Before mutation, read back:",
        "the selected Logic or UI evidence surface",
        "Stop Prototype-created processes",
        "State truthfully whether the question was answered",
        "Return directly to the current caller",
        "Do not select, recommend, or invoke a downstream route",
    ):
        assert required in b0
    for c1_only in (
        "Admit without mutation only when all are true",
        "Before mutation, read back five locks",
        "Load exactly one branch reference",
        "[MEASURE.md](MEASURE.md)",
        "status: answered | awaiting-verdict | blocked | not-admitted",
        "`authorized-durable-evidence`",
        "[RESUME.md](RESUME.md)",
    ):
        assert c1_only not in b0

    for forbidden_recommendation in ("$handoff", "$domain-modeling"):
        assert forbidden_recommendation not in b0
        assert forbidden_recommendation not in (
            candidate_dir / "SKILL.md"
        ).read_text(encoding="utf-8")

    candidate_files = {
        path.relative_to(candidate_dir).as_posix(): path
        for path in candidate_dir.rglob("*")
        if path.is_file()
    }
    control_files = {
        path.relative_to(description_control_dir).as_posix(): path
        for path in description_control_dir.rglob("*")
        if path.is_file()
    }
    assert candidate_files.keys() == control_files.keys()
    for relative in candidate_files.keys() - {"SKILL.md"}:
        assert candidate_files[relative].read_bytes() == control_files[
            relative
        ].read_bytes()

    old_skill = control_files["SKILL.md"].read_text(encoding="utf-8")
    new_skill = candidate_files["SKILL.md"].read_text(encoding="utf-8")
    old_description = old_skill.splitlines()[2]
    new_description = new_skill.splitlines()[2]
    assert old_skill.replace(old_description, new_description, 1) == new_skill


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


def test_canonical_tdd_is_the_exact_single_cut_baseline() -> None:
    canonical_dir = ROOT / "skills/custom/tdd"
    pre_prune_dir = ROOT / "docs/validation/evals/tdd-pruning-pre-prune"
    inventory = {
        "SKILL.md",
        "tests.md",
        "mocking.md",
        "refactoring.md",
        "agents/openai.yaml",
    }

    for package in (canonical_dir, pre_prune_dir):
        assert {
            path.relative_to(package).as_posix()
            for path in package.rglob("*")
            if path.is_file()
        } == inventory

    for relative in inventory - {"tests.md"}:
        assert (canonical_dir / relative).read_bytes() == (
            pre_prune_dir / relative
        ).read_bytes()

    async_waiting = """## Async Waiting

Wait for the observable condition or event with a bounded timeout and useful failure diagnostic.

```python
wait_for(
    lambda: job.status == "complete",
    timeout=5,
    description="job to complete",
)
```

Use elapsed delay only when time is the behavior. Observe the trigger first, derive the duration from the contract, and state why that duration proves it.

```python
wait_for(lambda: events.contains("DEBOUNCE_STARTED"), timeout=1)
advance_clock(DEBOUNCE_INTERVAL)
assert events.contains("SEARCH_REQUESTED")
```

"""
    pre_prune_tests = (pre_prune_dir / "tests.md").read_text(encoding="utf-8")
    canonical_tests = (canonical_dir / "tests.md").read_text(encoding="utf-8")

    assert pre_prune_tests.count(async_waiting) == 1
    assert canonical_tests == pre_prune_tests.replace(async_waiting, "", 1)


def test_promoted_implement_matches_accepted_pruning_contract() -> None:
    canonical_dir = CUSTOM / "implement"
    inventory = {"SKILL.md", "agents/openai.yaml"}

    assert {
        path.relative_to(canonical_dir).as_posix()
        for path in canonical_dir.rglob("*")
        if path.is_file()
    } == inventory

    assert tree_hash(canonical_dir) == (
        "1f61b9880b881771b579372075dd89e3bccb7ce9c94ae3bd0e30f1f43ae8724f"
    )
    promoted = (canonical_dir / "SKILL.md").read_text(encoding="utf-8")
    normalized = " ".join(promoted.split())

    for contract in (
        "Deliver exactly one selected bounded Ready-for-agent item",
        "A named target remains binding",
        "exhaustive parent graph to `$parallel-implement`",
        "Freeze one immutable Charter",
        "finite Repair budget",
        "Invoke exactly one formal route",
        "complete caller-admitted, Charter-preserving, proof-bounded batch",
        "For Local Markdown, append the final closeout packet",
        "retain the open item and claim through Lock and commit",
        "commit once",
        "commit tree to equal the locked tree",
        "partial or failed closeout Returns",
        "Return `complete` only after every applicable gate reads back",
    ):
        assert contract in normalized

    for rejected in (
        "staged worker",
        "two generations",
        "Invoke exactly one campaign route",
        "`automatic-in-scope`",
    ):
        assert rejected not in promoted
