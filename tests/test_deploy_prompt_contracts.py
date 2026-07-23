from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CONTEXT = ROOT / "CONTEXT.md"
DEPLOY_PROMPTS = ROOT / "docs" / "synthesis" / "methods" / "deploy-prompts.md"
SYNTHESIS_README = ROOT / "docs" / "synthesis" / "README.md"
METHODS_README = ROOT / "docs" / "synthesis" / "methods" / "README.md"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _section(text: str, heading: str, next_heading: str) -> str:
    return text.split(heading, 1)[1].split(next_heading, 1)[0]


def test_prompt_1_builds_b0_from_intent_and_evidence_before_current() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_1 = _section(
        deploy,
        "## Deploy Prompt 1: Establish The Minimum-Runtime Decision",
        "## Conditional Research Interlude",
    )
    prompt_3 = _section(
        deploy,
        "## Deploy Prompt 3: Build B0 And C1",
        "## Deploy Prompt 4: Audit And Prove Behavior",
    )
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Audit And Prove Behavior",
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
    )

    blind_pass = prompt_1.index("Blind intent and evidence pass:")
    intent_pass = prompt_1.index("Intent pass:")
    evidence_pass = prompt_1.index("Evidence pass:")
    frozen_checkpoint = prompt_1.index(
        "Freeze one source-first checkpoint before opening current."
    )
    current_reconciliation = prompt_1.index(
        "Current reconciliation: only now completely read"
    )

    assert (
        blind_pass
        < intent_pass
        < evidence_pass
        < frozen_checkpoint
        < current_reconciliation
    )
    for term in (
        "intersection",
        "settled viability floor",
        "credible source mechanics",
        "Current presence creates neither intent",
        "Never retrofit B0 after current",
    ):
        assert term in prompt_1
    for term in (
        "frozen intersection",
        "intended contract",
        "source mechanics",
        "B0 minimum-runtime suite",
    ):
        assert term in prompt_3
    assert "Only after B0 passes" in prompt_4
    assert "C1 never receives credit for making B0 viable" in prompt_4
    assert "Select the simplest credible baseline" not in deploy


def test_c1_has_four_discovery_origins_and_b0_first_admission() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)

    for origin in (
        "`current-retention`",
        "`pack-composition`",
        "`source-mechanism`",
        "`intent-counterexample`",
    ):
        assert origin in deploy

    for term in (
        "Origin invites inspection",
        "expected B0 failure",
        "wrong-condition case",
        "required local contract",
        "belongs in B0",
        "disproves minimum viability",
        "reopen B0 instead",
        "run B0 first",
        "exact caller/callee scenario",
    ):
        assert term in deploy


def test_prompt_4_rejects_c1_units_without_terminating_viable_b0() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Audit And Prove Behavior",
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
    )
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Establish The Minimum-Runtime Decision",
    )

    for term in (
        "`rejected-no-control-failure`",
        "do not run that C1 arm",
        "`rejected-regression`",
        "rederive exact C1 as B0 plus surviving units",
        "Do not rerun identical B0 arms",
        "If no C1 units survive, set C1 = B0",
        "Viable B0 remains the behavior-complete candidate",
        "unit dispositions, not terminal Prompt 4 decisions",
        "Return `accepted`, `needs-more-evidence`, or `blocked`",
    ):
        assert term in prompt_4

    assert "unit-level C1 rejection cannot terminate" in campaign
    assert "legacy terminal rejection may re-enter Prompt 4" in campaign
    assert "`evidence-gap`, `blocked`, `needs-more-evidence`" in campaign


def test_checkpoint_reentry_d0_and_missing_b0_proof_are_explicit() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)

    for term in (
        "load `Shared Model`, `Shared Run Contract`, `Proportionate Proof Budget`",
        "standalone or delegated unit",
        "opens another unit only to dispatch or verify it",
        "**Semantic behavior unit:**",
        "**Source-first checkpoint:**",
        "**`D0` no-guidance control:**",
        "verify its Git HEAD, local intent authorities, upstream revisions",
        "apply only that delta and issue a successor checkpoint",
        "Map each instruction-bearing runtime passage to one unit key",
        "Reuse the matching B0 viability arm as the candidate arm",
        "If D0 matches B0 without a meaningful variance benefit",
        "return `ready-for-prompt-3` for an evidence-only route",
    ):
        assert term in deploy


def test_deploy_campaign_is_discoverable_bounded_and_repeatable() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    agents = _normalized(AGENTS)
    context = _normalized(CONTEXT)
    shared = _section(deploy, "## Shared Run Contract", "## Proportionate Proof Budget")
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Establish The Minimum-Runtime Decision",
    )

    assert "Run Deploy Campaign on <skill>" in agents
    assert "docs/synthesis/methods/deploy-prompts.md" in agents
    assert "**Deploy Campaign**" in context
    assert "one-skill controller" in context
    assert "mega-prompt" in context

    for term in (
        "Prompts 1 through 5",
        "fresh campaign epoch",
        "not Git delivery",
        "Prior campaign artifacts never satisfy",
        "reruns only missing, drifted, contaminated",
        "`and commit`",
        "`and push`",
        "The root owns transitions",
        "Do not create a controller ledger",
        '`fork_turns="none"`',
        "method path and unit",
        "loads the shared sections plus its unit",
        "Serialize all writers",
        "verify its allowed status",
        "`ready-for-prompt-N`",
        "`research-gap` and `prototype-gap`",
        "Prompt 4 `accepted`",
        "unit-level C1 rejection cannot terminate",
        "Prompt 5 `complete`",
        "Before returning a successful terminal",
        "runs every numbered unit plus the Pruning Pass again",
        "Do not ask the user to authorize ordinary unit transitions",
    ):
        assert term in campaign

    assert "coordinator alone may dispatch a verified successor" in shared
    assert "unit invocation performs exactly one" in shared


def test_each_campaign_runs_all_units_and_reuses_only_exact_proof() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_1 = _section(
        deploy,
        "## Deploy Prompt 1: Establish The Minimum-Runtime Decision",
        "## Conditional Research Interlude",
    )
    prompt_2 = _section(
        deploy,
        "## Deploy Prompt 2: Finalize Decision-Complete Synthesis",
        "## Deploy Prompt 3: Build B0 And C1",
    )
    prompt_3 = _section(
        deploy,
        "## Deploy Prompt 3: Build B0 And C1",
        "## Deploy Prompt 4: Audit And Prove Behavior",
    )
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Audit And Prove Behavior",
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
    )
    pruning = _section(
        deploy,
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
        "## Deploy Prompt 5: Promote And Install",
    )
    prompt_5 = _section(
        deploy,
        "## Deploy Prompt 5: Promote And Install",
        "## Deploy Prompt 6: Git Delivery",
    )

    assert "always returns `ready-for-prompt-2`" in prompt_1
    assert "always returns `ready-for-prompt-3`" in prompt_2
    assert "current-epoch B0/C1 identities" in prompt_3
    assert "do not rerun identical samples" in prompt_4
    assert "recommends the Deploy Pruning Pass" in prompt_4
    assert "`complete` always recommends Prompt 5" in pruning
    assert "no-op integration read-back" in prompt_5
    assert "record no-op installation parity" in prompt_5


def test_pruning_is_a_separate_bounded_non_regression_unit() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Audit And Prove Behavior",
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
    )
    pruning = _section(
        deploy,
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
        "## Deploy Prompt 5: Promote And Install",
    )
    prompt_5 = _section(
        deploy,
        "## Deploy Prompt 5: Promote And Install",
        "## Deploy Prompt 6: Git Delivery",
    )

    assert "Never prune" in prompt_4
    assert "behavior-complete C1 hash" in prompt_4
    for term in (
        "`keep`, `collapse`, `disclose`, or `delete`",
        "Word count is diagnostic, never the objective",
        "If no material cut exists",
        "create no pre-prune fixture or behavioral wave",
        "Build one final C1, group proposed cuts by affected proof lane",
        "Run only the affected final-C1 arms",
        "no-control-failure rejection does not apply",
        "Revert any regressing, ambiguous, or unproved cut group",
        "do not search combinations",
        "`pruned`, `pruning-not-needed`, or `cuts-rejected`",
        "failed cuts fall back to the proved pre-prune candidate",
    ):
        assert term in pruning
    assert "completed Pruning Pass record" in prompt_5
    assert "final bytes differ from the pruning record" in prompt_5


def test_campaign_uses_nested_agents_only_for_independent_evidence() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Establish The Minimum-Runtime Decision",
    )

    for term in (
        "Prompt 1 and Research owners",
        "filesystem-read-only",
        "Prompt 4",
        "evaluation grandchildren",
        "capacity-aware waves",
        "owner fixes the packet and rubric",
        "without parent conclusions or peer outputs",
        "isolated or disposable outputs",
        "None edits shared sources",
        "interacts with the user, or spawns",
        "`behavior-decision-gap` stays root-held",
        "retain the campaign across the user's answers",
        "A summary alone is not evidence",
    ):
        assert term in campaign


def test_three_interludes_separate_source_design_and_intent_uncertainty() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    shared = _section(deploy, "## Shared Model", "## Shared Run Contract")
    research = _section(
        deploy,
        "## Conditional Research Interlude",
        "## Conditional Prototype Interlude",
    )
    prototype = _section(
        deploy,
        "## Conditional Prototype Interlude",
        "## Conditional Behavior Decision Interlude",
    )
    behavior = _section(
        deploy,
        "## Conditional Behavior Decision Interlude",
        "## Deploy Prompt 2: Finalize Decision-Complete Synthesis",
    )

    assert deploy.count("## Conditional ") == 3

    for term in (
        "books, papers, standards, documentation",
        "documented high ratings, professional acclaim, durable adoption",
        "upper-bound engineering discipline",
        "order discovery, never as proof",
    ):
        assert term in shared

    for term in (
        "$research",
        "source question",
        "Shared Model source priority",
        "original or primary evidence",
        "smallest source set",
        "credible counterpressure",
    ):
        assert term in research

    for term in (
        "$prototype",
        "frozen agent-owned design question",
        "smallest runnable probe",
        "production correctness",
        "behavioral steering remain untested",
    ):
        assert term in prototype

    for term in (
        "$grill-with-docs",
        "bounded intended-contract decision",
        "minimum viability",
        "C1 hypothesis",
        "agent-owned technique",
        "efficacy",
    ):
        assert term in behavior


def test_prompts_2_through_4_preserve_intent_source_and_proof_roles() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_2 = _section(
        deploy,
        "## Deploy Prompt 2: Finalize Decision-Complete Synthesis",
        "## Deploy Prompt 3: Build B0 And C1",
    )
    prompt_3 = _section(
        deploy,
        "## Deploy Prompt 3: Build B0 And C1",
        "## Deploy Prompt 4: Audit And Prove Behavior",
    )
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Audit And Prove Behavior",
        "## Deploy Pruning Pass: Minimize Accepted Candidate",
    )

    for term in (
        "intended-contract obligation",
        "credible source mechanic",
        "Research can establish source meaning",
        "grill can settle intent",
        "Prototype can choose",
        "construction evidence only",
    ):
        assert term in prompt_2
    for term in (
        "local intent obligation",
        "source mechanic",
        "Prototype verdict",
        "not behavioral-effect evidence",
    ):
        assert term in prompt_3
    for term in (
        "all four C1 hypothesis origins",
        "**B0 intent and source fidelity:**",
        "Prototype construction evidence",
        "behavioral contribution proof",
    ):
        assert term in prompt_4


def test_synthesis_method_summaries_match_the_revised_workflow() -> None:
    synthesis = _normalized(SYNTHESIS_README)
    methods = _normalized(METHODS_README)

    for text in (synthesis, methods):
        assert "source-derived" in text
        assert "local intended contract" in text
        assert "blind intent" in text
        assert "semantic behavior" in text or "semantic units" in text
        assert "D0" in text
        assert "current-retention" in text or "current retention" in text
        assert "pack-composition" in text or "pack composition" in text
        assert "source-mechanism" in text or "source mechanism" in text
        assert (
            "intent-counterexample" in text
            or "counterexample to settled intent" in text
        )
        assert "Conditional Behavior Decision Interlude" in text
        assert "Conditional Prototype Interlude" in text
        assert "Conditional Research Interlude" in text
        assert "Pruning Pass" in text
        assert "Run Deploy Campaign on <skill>" in text
        assert "fresh-context unit" in text
