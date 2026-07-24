from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CONTEXT = ROOT / "CONTEXT.md"
DEPLOY_PROMPTS = ROOT / "docs" / "synthesis" / "methods" / "deploy-prompts.md"
SYNTHESIS_README = ROOT / "docs" / "synthesis" / "README.md"
METHODS_README = ROOT / "docs" / "synthesis" / "methods" / "README.md"
SOURCE_FLOW = (
    ROOT / "docs" / "synthesis" / "methods" / "source-distillation-flow.md"
)
SOURCE_SEARCH = (
    ROOT
    / "docs"
    / "synthesis"
    / "methods"
    / "prompts"
    / "03-search-and-verify-sources.md"
)
WRITING_SKILL = ROOT / "skills" / "custom" / "writing-great-skills" / "SKILL.md"
BEHAVIOR_EVALS = (
    ROOT / "skills" / "custom" / "writing-great-skills" / "BEHAVIOR-EVALS.md"
)


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _section(text: str, heading: str, next_heading: str) -> str:
    return text.split(heading, 1)[1].split(next_heading, 1)[0]


def test_prompt_1_freezes_intent_derived_m0_before_research_or_current() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_1 = _section(
        deploy,
        "## Deploy Prompt 1: Freeze M0",
        "## Deploy Research Pass: Investigate The Intended Behavior",
    )

    local_intent = prompt_1.index("Read local intent authorities")
    specify_m0 = prompt_1.index("Specify M0 from that settled floor")
    cut_audit = prompt_1.index("clause-to-intent cut audit")
    checkpoint = prompt_1.index("Freeze one M0 checkpoint")

    assert local_intent < specify_m0 < cut_audit < checkpoint
    for term in (
        "Never inspect research, upstream packages, or the target's current skill body",
        "behavior-minimal, not word-count-minimal",
        "complete M0 viability suite",
        "authorized research-note path",
        "`ready-for-research`",
    ):
        assert term in prompt_1


def test_research_pass_is_mandatory_independent_and_non_self_validating() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    research = _section(
        deploy,
        "## Deploy Research Pass: Investigate The Intended Behavior",
        "## Conditional Prototype Interlude",
    )

    independent = research.index("First perform independent online discovery")
    inspect_packs = research.index("Only after recording that blind search")
    targeted = research.index("targeted independent online verification")
    assert independent < inspect_packs < targeted

    for term in (
        "Mandatory read-only evidence and discovery unit",
        "alternatives and counterevidence",
        "Attribute only observed behavior to the pack",
        "Upstream repetition proves shared pack usage only",
        "Never fabricate or generalize a conversation",
        "`independently-supported`, `contested`, `pack-specific`, or `unverified`",
        "Use decision saturation, not a source quota",
        "`research-complete`, `intent-reopen`, `evidence-gap`, or `blocked`",
    ):
        assert term in research


def test_shared_model_separates_intent_research_pack_current_and_proof() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    shared = _section(deploy, "## Shared Model", "## Shared Run Contract")

    for role in (
        "| Local intent authorities |",
        "| Independent professional evidence |",
        "| Upstream packages |",
        "| Current canonical runtime |",
        "| Candidate-owned proof |",
    ):
        assert role in shared

    for term in (
        "not prove correctness or local fit",
        "Never simulate a practitioner conversation",
        "M0 is minimal by behavioral scope",
        "P1 is minimal by proved wording and package load",
        "Pack-specific or unverified behavior may be a clearly labeled local experiment",
    ):
        assert term in shared

    assert "Upstream packages and credible research" not in shared
    assert "source-derived executable minimum" not in shared


def test_prompt_2_builds_h1_from_five_discovery_lanes_with_honest_authority() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_2 = _section(
        deploy,
        "## Deploy Prompt 2: Finalize H1 Synthesis",
        "## Deploy Prompt 3: Build M0 And H1",
    )

    for origin in (
        "`professional-method`",
        "`current-observed`",
        "`pack-observed`",
        "`pack-composition`",
        "`intent-adjacent`",
    ):
        assert origin in prompt_2

    for term in (
        "`locally-justified experimental`",
        "`defect-correction`",
        "`quality-lift`",
        "expected M0 weakness",
        "wrong-condition cases",
        "fixed rubric",
        "H1 cannot make M0 viable",
        "`unresolved removal risk`",
    ):
        assert term in prompt_2


def test_intent_adjacent_vocabulary_maps_to_observable_contribution() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    shared = _section(deploy, "## Shared Model", "## Shared Run Contract")

    assert "**Intent-adjacent steering hypothesis:**" in shared
    assert (
        "`term -> recruited behavior -> expected M0 weakness -> observable gate -> "
        "comparative proof`"
        in shared
    )
    assert "preserves the intended contract" in shared


def test_prompt_3_materializes_m0_without_research_leakage_and_builds_exact_h1() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_3 = _section(
        deploy,
        "## Deploy Prompt 3: Build M0 And H1",
        "## Deploy Prompt 4: Prove M0 And H1",
    )

    for term in (
        "Materialize exact M0 solely from the frozen M0 checkpoint",
        "Do not import research language",
        "Construct exact H1 from M0 plus only admitted additions and substitutions",
        "Store M0 once as the immutable control and H1 once as the candidate",
        "Do not create a separate no-guidance control when M0 already supplies",
        "M0 must be exact and executable",
    ):
        assert term in prompt_3


def test_prompt_4_proves_m0_then_defect_correction_or_quality_lift() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prompt_4 = _section(
        deploy,
        "## Deploy Prompt 4: Prove M0 And H1",
        "## Deploy Pruning Pass: Derive P1",
    )

    audit_m0 = prompt_4.index("Audit M0 first")
    m0_passes = prompt_4.index("Only after M0 passes")
    h1_samples = prompt_4.index("run at least five fresh H1 samples")
    assert audit_m0 < m0_passes < h1_samples

    for term in (
        "H1 never receives credit for making M0 viable",
        "`defect-correction`",
        "`quality-lift`",
        "`rejected-no-control-deficit`",
        "`rejected-regression`",
        "`needs-more-evidence`",
        "If no H1 units survive, set V1 = M0",
        "Unit rejection never terminates a campaign while viable M0",
        "model, host, tools, configuration",
        "preserve the active runtime",
    ):
        assert term in prompt_4


def test_pruning_freezes_v1_and_promotes_only_regression_checked_p1() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    pruning = _section(
        deploy,
        "## Deploy Pruning Pass: Derive P1",
        "## Deploy Prompt 5: Promote And Install P1",
    )
    prompt_5 = _section(
        deploy,
        "## Deploy Prompt 5: Promote And Install P1",
        "## Deploy Prompt 6: Git Delivery",
    )

    for term in (
        "Freeze V1 once as the immutable behavior-complete control",
        "Build one P1",
        "Treat pruning as non-regression",
        "Revert every regressing, ambiguous, or unproved cut group",
        "If all cuts fail, set P1 = V1",
        "`pruned`, `pruning-not-needed`, or `cuts-rejected`",
    ):
        assert term in pruning

    assert "Promotes only exact P1" in prompt_5
    assert "promote P1 into the canonical skill" in prompt_5
    assert "verify canonical/installed parity" in prompt_5


def test_campaign_runs_mandatory_research_and_every_runtime_stage() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    agents = _normalized(AGENTS)
    context = _normalized(CONTEXT)
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Freeze M0",
    )

    for term in (
        "Prompt 1, Research Pass, Prompts 2 through 4, Pruning Pass, and Prompt 5",
        "`and commit`",
        "`and push`",
        "The root owns transitions",
        '`fork_turns="none"`',
        "Serialize all writers",
        "Prompt 1 `ready-for-research` dispatches the Research Pass",
        "Research `research-complete` dispatches Prompt 2",
        "Prompt 4 `accepted` dispatches the Pruning Pass",
        "Every fresh campaign runs every ordinary unit once",
    ):
        assert term in campaign

    assert "Run Deploy Campaign on <skill>" in agents
    assert "Research Pass" in agents
    assert "**Deploy Campaign**" in context
    assert "**Deploy runtime identities**" in context


def test_interludes_own_only_contract_or_technical_uncertainty() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    prototype = _section(
        deploy,
        "## Conditional Prototype Interlude",
        "## Conditional Behavior Decision Interlude",
    )
    behavior = _section(
        deploy,
        "## Conditional Behavior Decision Interlude",
        "## Deploy Prompt 2: Finalize H1 Synthesis",
    )

    assert deploy.count("## Conditional ") == 2
    for term in (
        "$prototype",
        "one frozen agent-owned technical choice",
        "Production correctness and behavioral steering remain untested",
    ):
        assert term in prototype
    for term in (
        "$grill-with-docs",
        "one bounded intended-contract decision",
        "Do not choose agent technique",
        "minimum-viability answer returns to Prompt 1",
        "H1-only contract answer",
    ):
        assert term in behavior


def test_behavior_evaluation_contract_supports_quality_lift_and_adaptive_cost() -> None:
    evals = _normalized(BEHAVIOR_EVALS)
    writing = _normalized(WRITING_SKILL)

    for term in (
        "`defect-correction` or `quality-lift`",
        "meaningful rubric deficit",
        "at least five independent control samples",
        "candidate samples only when the registered control deficit appears",
        "Extend sampling only for material variance",
        "`reject-no-control-deficit`",
        "residual transfer gap",
    ):
        assert term in evals

    assert "registered defect" in writing
    assert "pre-registered quality deficit" in writing


def test_source_method_and_indexes_match_independent_verification_model() -> None:
    source_flow = _normalized(SOURCE_FLOW)
    source_search = _normalized(SOURCE_SEARCH)
    synthesis = _normalized(SYNTHESIS_README)
    methods = _normalized(METHODS_README)

    for text in (source_flow, source_search):
        assert "search independently" in text
        assert "professional" in text
        assert "upstream" in text or "skill pack" in text
        assert "counterevidence" in text

    for text in (synthesis, methods):
        for term in ("M0", "H1", "V1", "P1", "Research Pass"):
            assert term in text
        assert "intent-derived" in text
        assert "pack-specific" in text
        assert "quality lift" in text


def test_live_workflow_avoids_legacy_source_derived_baseline_contract() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    methods = _normalized(METHODS_README)

    for stale in (
        "Conditional Research Interlude",
        "source-derived executable minimum",
        "Draft B0 from the intersection",
        "D0 no-guidance control",
        "Build B0 And C1",
    ):
        assert stale not in deploy

    assert "source-derived executable minimum" not in methods
