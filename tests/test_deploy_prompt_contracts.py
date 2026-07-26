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
        "state-location ledger",
        "working tree, index, committed tree, connector, and remote",
        "Map every transition to an M0 unit and viability case",
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

    independent = research.index("independent problem-first packet")
    catalog = research.index("Query the canonical Research Catalog")
    retrieval = research.index("Perform bounded retrieval")
    assert independent < catalog < retrieval

    for term in (
        "Mandatory read-only evidence and discovery unit",
        "alternatives and counterevidence",
        "Attribute only observed behavior to the pack",
        "Never fabricate or generalize a conversation",
        "`independently-supported`, `contested`, `pack-specific`, or `unverified`",
        "Stop after the finite sequence",
        "zero or one named gap",
        "same-campaign `intent-reopen`",
        "write only the affected decision delta",
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
        "**`C0` incumbent runtime:**",
        "C0 is comparison evidence, not M0 authority",
        "M0 is minimal by behavioral scope",
        "P1 is minimal by proved wording and package load",
        "**Runtime load profile:**",
        "Never invent prevalence or probability weights",
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
        "observable entry predicate",
        "`common`, `situational`, `rare`, or `unknown` applicability",
        "Fixture frequency does not establish real-world prevalence",
        "weak-but-still-M0-compliant counterexample",
        "`M0-recruited`",
        "discriminate under realistic difficulty",
        "wrong-condition cases",
        "fixed rubric",
        "H1 cannot make M0 viable",
        "`unresolved removal risk`",
        "For each current-only unit",
        "isolate `M0 + incumbent unit` as a `current-observed` H1",
        "use exact C0 only when isolation is impossible",
        "Never protect all of C0 or require a full C0 behavioral wave",
        "`quality-lift` is the bounded exploratory lane",
        "needs no previously observed defect",
        "Prompt 4's control decides",
        "Do not create hypotheses to satisfy a quota",
        "expected load effect and acceptance budget",
        "Seed one schema-validated, machine-readable campaign manifest",
        "one versioned final shape with nullable later-stage sections",
        "C0 identity",
        "current-only causal dispositions",
        "separate semantic, behavioral, and load claim slots",
        "required and forbidden semantic IDs",
        "protected helpers and compatibility surfaces",
        "carried-forward evidence identities",
        "forbidden semantic ID and absence-proof obligation",
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


def test_shared_behavior_protocol_owns_fixture_isolation_and_sampling() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    protocol = _section(
        deploy,
        "## Shared Behavioral Evaluation Protocol",
        "## Deploy Campaign: Orchestrate One Skill",
    )

    for term in (
        "minimum proof-coverage matrix",
        "Run deterministic schema, identity, relationship, ordering",
        "collapse cases that exercise the same decision mechanism",
        "specific independent branch or proof reason",
        "worker-fixture schema version 2",
        "worker-visible `decision_state`",
        "`target_resolution`",
        "`evidence_availability`",
        "`mutation_permission`",
        "Do not expose expected terminal",
        "required feasibility roles and adjacent terminals",
        "root judgment still owns whether the cited evidence",
        "python -m scripts.campaign_artifacts lint-fixture WORKER_FIXTURE.json",
        "python -m scripts.campaign_artifacts lint-registration WORKER_FIXTURE.json ROOT_REGISTRATION.json",
        "python -m scripts.campaign_artifacts lint-payload WORKER_FIXTURE.json CASE_ID PAYLOAD.json",
        "python -m scripts.campaign_artifacts compare-payloads WORKER_FIXTURE.json CASE_ID M0_PAYLOAD.json H1_PAYLOAD.json",
        "remove the exact runtime slot and require byte-identical",
        "Immediately before each dispatch, rerun `lint-payload`",
        "record its dispatch hash",
        "Spread the existing minimum five samples for a broad claim",
        "share one entry predicate, arm delta, rubric, and joint disposition",
        "Do not infer per-unit contribution from a bundled arm",
        "dispatch and inspect one control before the remaining wave",
        "A valid first sample counts",
        "an invalid sample receives zero credit",
        "Any worker-visible clarification changes the fixture or payload identity",
        "five fresh exact M0 controls",
        "`reject-no-control-deficit`",
        "five fresh entry-positive H1 samples",
        "wrong-condition M0/H1 pairs",
        "no registered-load-budget violation",
        "`reject-insufficient-contribution`",
        "`reject-regression`",
        "unavailable decision-bearing telemetry returns `needs-more-evidence`",
        "Keep reconstructible per-sample payloads disposable",
        "including model, host, and tools",
    ):
        assert term in protocol


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
        "exact C0 comparison evidence",
        "prefer the isolated `M0 + incumbent unit` arm",
        "Materialize a C0 arm only when the unit cannot be isolated",
        "incumbent-removal ablation or bounded C0 comparison",
        "expected load effect",
        "non-inferiority bound",
        "Do not create a separate no-guidance control when M0 already supplies",
        "matching campaign manifest",
        "Populate only the Prompt 3-owned manifest fields",
        "Every forbidden semantic must have an absence check",
        "A prose claim that a rejected behavior was removed is insufficient",
        "Under the Shared Behavioral Evaluation Protocol",
        "Freeze the worker fixture, root registration, resolved dispatch envelopes",
        "all required Shared Behavioral Evaluation Protocol command results",
        "an M0-only or no-H1 arm",
        "Prompt 3 samples nothing",
        "terminal feasibility, family coverage, or arm isolation fails",
        "Reference rather than copy the authoritative intended contract",
        "candidate-aware focused compatibility preflight",
        "one shared, parameterized semantic assertion owner",
        "accepts an explicit package root and expected tree identity",
        "prove the factorization preserved the incumbent contract",
        "Prompts 4 and 5 and the Pruning Pass reuse that same owner",
        "Bind every assertion to the explicit candidate root and recorded tree identity",
        "resolves the canonical package is canonical proof, not candidate proof",
        "only when shared parameterization is infeasible",
        "record the reason and residual duplication",
        "Never provisionally promote a candidate to obtain Prompt 3 proof",
        "Classify each directly affected assertion as semantic prose or a machine-consumed contract",
        "do not change candidate wording merely to satisfy a prose snapshot",
        "If M0 itself omitted a required intended or compatibility contract",
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
    no_h1 = prompt_4.index("If no H1 units survive")
    assert audit_m0 < m0_passes < no_h1

    for term in (
        "H1 never receives credit for making M0 viable",
        "verify Prompt 3's frozen proof matrix",
        "Execute the Shared Behavioral Evaluation Protocol",
        "bounded source-completeness repair",
        "shared parameterized semantic assertion owner",
        "`writing-great-skills/BEHAVIOR-EVALS.md`",
        "five-entry-positive-control floor",
        "Applicability evidence and conditional efficacy remain separate",
        "Resolve plausible incumbent-removal units through the same adaptive gate",
        "Use exact C0 only for affected cases when isolation is impossible",
        "do not attribute a whole-C0 result to one clause",
        "no preservation, causal comparison, or resolved non-inferiority proof",
        "Apply the shared first-sample gate",
        "A protocol deviation receives no behavioral credit",
        "If no H1 units survive, set V1 = M0",
        "Unit rejection never terminates a campaign while viable M0",
        "capability, or quality risk",
        "every plausible incumbent-removal risk is resolved",
        "preserve the active runtime",
        "Populate only the Prompt 4-owned manifest fields",
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
        "Reuse the exact runtime-clause map",
        "do not restate every `keep` mapping",
        "If all cuts fail, set P1 = V1",
        "`pruned`, `pruning-not-needed`, or `cuts-rejected`",
        "Do not create a Pruning-specific equivalent verifier",
        "Pruning capsule in the consolidated decisions record",
        "Create no standalone verifier or transcript",
    ):
        assert term in pruning

    assert "Promotes only exact P1" in prompt_5
    assert "promote P1 into the canonical skill" in prompt_5
    assert "verify canonical/installed parity" in prompt_5
    assert "Populate only the Prompt 5-owned manifest fields" in prompt_5
    for term in (
        "three separate terminal claims",
        "semantic contract status",
        "behavioral contribution or non-regression",
        "runtime-load direction",
        "List every promotion-critical path once in the final manifest",
        "resolves inside the repository, exists, and is not ignored",
        "`.scratch/` is durable only when intentionally included in Prompt 6 scope",
        "`.tmp/` and discarded captures may appear only by hash",
        "Classify any proof failure before routing it",
        "repair that proof to heading-bounded normalized semantics",
        "Return to Prompt 3 when the executable candidate fails a frozen M0 semantic",
        "Prompt 1 when M0 itself omitted a required intended or compatibility contract",
        "Prompt 4 only when behavioral evidence is invalid or insufficient",
        "Prompt 3's shared parameterized semantic assertion owner",
        "Do not replace it with a Prompt 5-specific semantic checker",
    ):
        assert term in prompt_5


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
        "read-only managed-install dry-run",
        "same-worktree Deploy Campaign lease",
        "use a separate worktree or return `blocked`",
        "one fixed child-brief envelope",
        "canonical method path, exact unit heading, bounded content fingerprint",
        "Do not copy the unit body into the brief",
        "manifest identity keys",
        "exact allowed source paths and forbidden source categories",
        "ambient validation failures",
        "ambient changed cohort",
        "newly appeared unrelated drift is a fresh scope gap",
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


def test_campaign_ordinary_path_uses_the_narrow_control_interface() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Freeze M0",
    )

    start = "`python -m scripts.campaign_artifacts start SKILL [DELIVERY_MODE]`"
    verify = "`python -m scripts.campaign_artifacts verify MANIFEST`"
    assert campaign.count(start) == 1
    assert campaign.count(verify) == 1
    assert "Invoke `verify MANIFEST` once at each applicable boundary" in campaign

    for advanced in (
        "`status`",
        "`release`",
        "`--force-proof`",
        "`--stage`",
        "`--no-execute`",
        "low-level lint and comparison commands",
        "advanced or recovery",
    ):
        assert advanced in campaign

    for duplicated_command in (
        "scripts.install_skills",
        "scripts.validate_skills",
        "campaign_artifacts hash-tree",
        "campaign_artifacts lint-fixture",
        "campaign_artifacts lint-registration",
        "campaign_artifacts lint-payload",
        "campaign_artifacts compare-payloads",
    ):
        assert duplicated_command not in campaign


def test_fresh_research_is_finite_and_prompt2_owns_claim_adjacency() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    research = _section(
        deploy,
        "## Deploy Research Pass: Investigate The Intended Behavior",
        "## Conditional Prototype Interlude",
    )
    prompt_2 = _section(
        deploy,
        "## Deploy Prompt 2: Finalize H1 Synthesis",
        "## Deploy Prompt 3: Build M0 And H1",
    )

    for phrase in (
        "Execute this finite sequence once",
        "independent problem-first packet",
        "Query the canonical Research Catalog only after that freeze",
        "exact Card ID, claim ID, Card fingerprint, claim relation",
        "source fixed point",
        "exactly one named evidence gap",
    ):
        assert phrase in research
    assert "Prompt 2 alone owns the H1 and claim-adjacency decision" in prompt_2
    for relation in (
        "`supports-method`",
        "`contests`",
        "`limits`",
        "`informs-only`",
    ):
        assert relation in prompt_2
    assert (
        "Research's `supports`, `contradicts`, `qualifies`, and `unrelated` "
        "labels are evidence inputs, not valid H1 adjacency values"
    ) in prompt_2
    for field in (
        "`h1_id`",
        "exact Card ID and claim ID",
        "applicability bridge to the named M0 weakness",
        "counterconditions and wrong condition",
        "source fixed point",
        "local-inference label",
        "claim limits",
        "synthesis disposition",
        "proof IDs",
    ):
        assert field in prompt_2


def test_campaign_adoption_preserves_semantic_authority_and_proves_ceremony() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    campaign = _section(
        deploy,
        "## Deploy Campaign: Orchestrate One Skill",
        "## Deploy Prompt 1: Freeze M0",
    )

    for term in (
        "never invents missing semantic state",
        "Existing manual campaigns remain operable",
        "changed intent requires Restart",
        "failed verification",
        "re-entry command",
        "Prompt 5 still owns promotion and installation",
        "Prompt 6 still owns Git delivery",
        "Representative ceremony comparison",
        "manual commands",
        "copied identities",
        "proof executions",
        "no authored per-stage artifact",
        "runtime-no-change",
        "minimum-only",
        "hypothesis",
        "pruning-no-op",
        "material-pruning",
        "terminal success",
        "terminal failure",
        "no behavioral arms",
        "exact reusable evidence",
        "fresh behavioral sampling",
        "concurrent unrelated work",
    ):
        assert term in campaign


def test_campaign_records_one_authoritative_unit_decision_without_duplication() -> None:
    deploy = _normalized(DEPLOY_PROMPTS)
    shared = _section(deploy, "## Shared Run Contract", "## Shared Proof Core")
    proof = _section(
        deploy,
        "## Shared Proof Core",
        "## Shared Behavioral Evaluation Protocol",
    )
    prompt_5 = _section(
        deploy,
        "## Deploy Prompt 5: Promote And Install P1",
        "## Deploy Prompt 6: Git Delivery",
    )
    prompt_6 = deploy.split("## Deploy Prompt 6: Git Delivery", 1)[1]

    for term in (
        "one authoritative decision record per unit",
        "Prefer one `decisions.md` with immutable marker-bounded unit capsules",
        "seed its versioned final shape with nullable lifecycle sections",
        "user-facing Return",
        "do not copy it verbatim into a durable transcript",
        "One schema-validated, machine-readable campaign manifest",
        "Synthesis owns only the active decision and final dispositions",
        "stage capsule owns the ordinary unit decision and delta",
        "Transcripts own only exceptional chronology",
        "the transcript may be omitted",
        "Do not append dated unit logs to synthesis",
        "immutable marker-bounded stage capsule",
        "never on mutable active synthesis, candidate, or whole campaign-manifest bytes",
        "manifest names the active verifier",
        "repeating hashes, sample tables, or chronology",
        "bound all decision-bearing content with markers",
        "content fingerprint as its semantic identity",
        "`python -m scripts.campaign_artifacts hash-tree PATH`",
        "do not reimplement path ordering",
        "manifest keys such as `runtime_identities.m0`",
        "Never make a manually copied digest authoritative",
        "Manifest field ownership is fixed",
        "| Prompt 2 | Fixed point, C0, M0 and research fingerprints",
        "| Prompt 6 | No manifest mutation",
    ):
        assert term in shared

    for term in (
        "whenever any unit changes Markdown",
        "After any unit writes repository artifacts",
        "before freezing final identities",
        "correct every failure it introduced",
        "heading-bounded normalized semantics",
        "Do not snapshot sentences or line wrapping",
        "machine-consumed token, path, field, or command",
        "proof once as a receipt keyed by command",
        "Do not duplicate a full suite",
    ):
        assert term in proof

    assert "compare it with the controller's ambient cohort" in prompt_5
    assert "newly appeared unrelated drift as a fresh scope gap" in prompt_5
    assert "Persist one compact final manifest" in prompt_5
    assert "one consolidated marker-bounded decisions record" in prompt_5
    assert "Freeze it as the terminal Prompt 5 state" in prompt_5
    assert "never transiently delete active synthesis" in prompt_5
    assert "must not depend on an omitted or disposable path" in prompt_5
    for term in (
        "every promotion-critical path named by the final manifest",
        "staged or already tracked at its recorded identity",
        "A required `.scratch/` path belongs in the commit",
        "a `.tmp/` path cannot",
        "The frozen Prompt 5 manifest remains unchanged",
        "the Git commit and this Prompt 6 Return are delivery authority",
    ):
        assert term in prompt_6


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
    register = _section(evals, "## Register the control", "## Freeze the cohorts")
    sample = _section(evals, "## Freeze the cohorts", "## Judge conditional efficacy")
    judge = _section(evals, "## Judge conditional efficacy", "## Record the result")
    record = evals.split("## Record the result", 1)[1]
    claim_proof = _section(writing, "## Claim-Matched Proof", "## Author Lock")

    def assert_tokens_in_order(section: str, *tokens: str) -> None:
        cursor = 0
        for token in tokens:
            cursor = section.index(token, cursor) + len(token)

    for token in ("`defect-correction`", "`quality-lift`"):
        assert token in register
    assert_tokens_in_order(register, "meaningful", "rubric", "deficit")
    assert_tokens_in_order(register, "observable", "entry", "predicate")
    assert_tokens_in_order(register, "applicability", "`common`", "`situational`", "`rare`", "`unknown`")
    assert_tokens_in_order(register, "evidence", "basis")
    assert_tokens_in_order(
        register,
        "registered",
        "control",
        "deficit",
        "does not",
        "appear",
        "stop",
        "H1",
        "`reject-no-control-deficit`",
    )

    assert_tokens_in_order(sample, "entry-positive", "wrong-condition", "cohorts")
    assert_tokens_in_order(sample, "fresh", "contexts")
    assert_tokens_in_order(sample, "five", "fresh", "M0", "entry-positive", "controls")
    assert_tokens_in_order(
        sample,
        "five",
        "fresh",
        "H1",
        "entry-positive",
        "samples",
        "only",
        "deficit",
        "appears",
    )
    assert_tokens_in_order(
        sample,
        "wrong-condition",
        "M0/H1",
        "pairs",
        "only",
        "after",
        "entry-positive",
        "contribution",
        "gate",
    )
    assert_tokens_in_order(sample, "do not", "dilute", "situational", "non-triggering")
    assert_tokens_in_order(sample, "Extend", "variance", "borderline", "protocol")
    assert_tokens_in_order(sample, "Five", "minimum", "not", "automatic", "sufficiency")
    assert_tokens_in_order(sample, "rejected", "candidate", "no", "wrong-condition")

    assert_tokens_in_order(judge, "conditional", "efficacy", "entry-positive")
    assert_tokens_in_order(judge, "applicability", "separate", "efficacy")

    for token in (
        "`accept`",
        "`reject-no-control-deficit`",
        "`reject-insufficient-contribution`",
        "`reject-regression`",
        "`needs-more-evidence`",
        "`blocked`",
    ):
        assert token in record
    assert_tokens_in_order(record, "residual", "transfer", "gap")
    assert_tokens_in_order(
        record,
        "`reject-regression`",
        "observed",
        "critical",
        "protected",
        "behavior",
        "regression",
    )

    assert "[BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md)" in claim_proof
    assert_tokens_in_order(
        claim_proof,
        "attributes",
        "changed",
        "invocation",
        "judgment",
        "action",
        "context loading",
        "Return",
        "completion",
    )
    assert_tokens_in_order(claim_proof, "uncontaminated", "direct", "controls")


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
