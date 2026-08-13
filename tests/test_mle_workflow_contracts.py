from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MLE = ROOT / "skills" / "extra" / "mle-workflow"


def read(relative: str) -> str:
    return (MLE / relative).read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.index(marker)
    end = text.find("\n## ", start + len(marker))
    return text[start:] if end == -1 else text[start:end]


def flat(text: str) -> str:
    return " ".join(text.split())


def markdown_targets(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def test_common_core_binds_evaluation_history_population_and_inference() -> None:
    skill = read("SKILL.md")
    evaluation = read("references/EVALUATION-BRANCHES.md")
    contract = flat(section(skill, "Freeze the Evaluation Contract before candidate results"))
    confirmatory = flat(section(evaluation, "Confirmatory inference"))

    for phrase in (
        "one versioned **Evaluation Contract**",
        "Purpose Lock accountable owner or named delegate",
        "protocol or analysis owner when different",
        "access capable of revealing a reserved final or outcome result",
        "information revealed",
        "never backfills them as prospective",
        "selection procedure and evidence selection-exposed",
        "eligibility and sampling frame",
        "observed support or coverage",
        "must not use unconfirmed values",
        "including an `uncertainty-indeterminate` result",
        "Realized evaluation or analysis population",
        "estimator, weighting, aggregation, and uncertainty procedure",
        "restricted-feedback or reusable-holdout protocol",
    ):
        assert phrase in contract

    for phrase in (
        "estimator, weighting, and aggregation target the declared estimand",
        "claim-family boundary and its rationale before outcome access",
        "supports the same decision or conclusion",
        "Family-wise error rate normally fits individually claim-bearing",
        "false-discovery rate fits a discovery-oriented claim",
        "consistency/treatment-version",
        "exchangeability/confounding",
        "design, domain, or external evidence that supports it",
        "does not establish no effect",
        "do not claim an exact zero effect",
    ):
        assert phrase in confirmatory


def test_finance_branch_closes_market_identity_and_economic_claims() -> None:
    skill = flat(read("SKILL.md"))
    evaluation = read("references/EVALUATION-BRANCHES.md")
    finance = flat(read("references/FINANCE-BACKTESTING.md"))

    assert markdown_targets(read("SKILL.md")).count("references/FINANCE-BACKTESTING.md") == 1
    assert "historical securities or portfolio simulation" in skill
    assert "Do not activate this branch merely because" in skill
    assert "## Recurring forecasts or time-indexed decisions" in evaluation
    assert "## Recurring forecasts or time-indexed decisions" not in finance
    for phrase in (
        "historically eligible universe",
        "delisting returns",
        "corporate actions consistently",
        "revision or restatement vintage",
        "A no-fill remains in opportunity identity",
        "It is not a loss or a win",
        "exclude the no-fill from outcome fitting",
        "position and cash state -> portfolio net outcome",
        "bid-ask spread, slippage, market impact",
        "turnover, gross and net exposure, concentration, leverage",
        "Gross-only evidence cannot support a net-economic claim",
        "Do not make a legal or regulatory applicability conclusion",
        "exact specialist handoff",
        "Do not require execution or portfolio machinery for a prediction-only claim",
        "quantity and unit or notional",
        "exercise, expiry, and settlement terms",
    ):
        assert phrase in finance


def test_composed_ai_branch_owns_identity_state_trust_and_evaluation() -> None:
    skill = flat(read("SKILL.md"))
    composed = flat(read("references/COMPOSED-AI.md"))
    risk = flat(section(read("references/RISK-BRANCHES.md"), "Generative and tool-using capabilities"))

    assert markdown_targets(read("SKILL.md")).count("references/COMPOSED-AI.md") == 1
    assert "execute every matching section" in skill
    for phrase in (
        "resolved model/version or as-of time",
        "mark identity `unresolved`",
        "answerable question class",
        "surface the conflict, or abstain",
        "tenant or user access control",
        "correction and deletion propagation",
        "An invalid, unvalidated, or out-of-scope grader result is `unknown`",
        "Forbidden actions and forbidden intermediate or final states",
        "read authoritative state before retry",
        "zero-real-effect seam",
        "reconciliation establishes that a new attempt is safe",
        "direct injection",
        "indirect injection",
        "A reviewer, queue, button, or confirmation screen is structural evidence only",
        "Provider list prices and averages alone do not establish workload economics",
        "require abstention or zero protected disclosure",
    ):
        assert phrase in composed
    assert "The composed-AI branch owns behavior identity" in risk
    assert "test prompt/resource injection" not in risk


def test_operations_require_objectives_semantic_signals_and_readback() -> None:
    skill = flat(section(read("SKILL.md"), "Map the system and delivery contract"))
    operate = flat(read("references/OPERATE.md"))

    for phrase in (
        "semantic-health measure",
        "retry budget/backoff",
        "target or budget",
        "recovery read-back",
    ):
        assert phrase in skill
    for phrase in (
        "authoritative target state and material external effects",
        "`not attempted`, `zero effect`, `success`, `partial effect`, and `uncertain effect`",
        "owner-confirmed service objectives",
        "provider SLA or component uptime",
        "semantic-health signals",
        "maximum permitted age by operating context",
        "Before declaring recovery complete, read back the active release or artifact",
        "representative real caller/consumer path",
    ):
        assert phrase in operate


def test_routing_keeps_conditional_references_out_of_unrelated_work() -> None:
    skill = flat(read("SKILL.md"))
    composed = flat(read("references/COMPOSED-AI.md"))
    finance = flat(read("references/FINANCE-BACKTESTING.md"))
    metadata = read("agents/openai.yaml")

    assert "Do not activate this branch merely because the data, organization, or prediction target is financial" in skill
    assert "Read this file only when model output is evaluated through a historical securities or portfolio simulation" in finance
    assert "instruction-following generative behavior with untrusted supplied context" in skill
    assert "instruction-following generative behavior with untrusted supplied context" in composed
    assert "Execute every matching section and no others" in composed
    assert "allow_implicit_invocation: false" in metadata


def test_promotion_and_completion_require_real_proof_and_terminal_review() -> None:
    skill_text = read("SKILL.md")
    promotion = flat(section(skill_text, "Package, promote, and roll out an immutable candidate"))
    completion = flat(section(skill_text, "Complete proportionately"))
    experiments = flat(section(skill_text, "Run traceable experiments"))

    for phrase in (
        "every project-owned, reconstructible component",
        "For provider-owned components",
        "Possession of packaged bytes is not rebuild proof",
    ):
        assert phrase in experiments
    for phrase in (
        "exact packaged candidate through the real project entry point",
        "representative named downstream consumer",
        "not real-caller production proof",
    ):
        assert phrase in promotion
    for phrase in (
        "Complete only the requested operation",
        "A Review returns exactly one terminal verdict",
        "`PASS`",
        "`FAIL`",
        "`INCONCLUSIVE`",
        "fully recovered evidence yields `uncertainty-indeterminate`",
        "For non-Review operations, return exactly one operation status",
        "When data use or training was in scope",
        "When decision-bearing evaluation was in scope",
        "candidate-bound Review verdict and blockers",
    ):
        assert phrase in completion
