# Specialized Evaluation Branches

Read only the sections activated by the system under evaluation. These branches
extend, but do not replace, the common evaluation contract in `SKILL.md`.

## Confirmatory inference

Use only when the requested decision rests on a claim presented as confirmatory
statistical inference or a causal-effect claim. Do not activate for explicitly
exploratory analysis, diagnostics, ordinary predictive candidate comparison,
deterministic verification, or engineering gate checks.

For prospective Frame or Build work, before accessing outcome evidence reserved
for confirmation, version the protocol and obtain confirmation from the
accountable research or analysis owner identified in the Purpose Lock. In
Review, recover the contemporaneous protocol and report missing or late
declarations; never backfill them as prospective.

Freeze, as applicable:

- the hypothesis, target population and target quantity or estimand;
- the outcome and measurement rule, comparator, sampling design, exclusions,
  missingness or censoring handling, estimator and analysis procedure;
- uncertainty method, precision or power rationale, stopping rule, and decision
  rule; and
- assignment or exposure, observation, analysis, and independent-resampling
  units plus their clustering, repeated-measure, or interference relationships.

Define each confirmatory claim family and which planned hypotheses, outcomes,
metrics, claim-bearing slices, individually claim-bearing candidate
comparisons, and outcome-dependent interim looks it counts. Use a
design-appropriate error-control, hierarchical, sequential, or fresh
independent-confirmation policy. Treat adaptive model or candidate selection
as a locked selection procedure evaluated on untouched outer evidence, not as
ordinary multiple testing.

For a causal-effect claim, additionally state the intervention or exposure,
counterfactual contrast, assignment mechanism or identification strategy, and
applicable confounding, selection, interference, noncompliance, positivity,
attrition, missingness, and transport assumptions. Predictive improvement,
temporal precedence, or regression adjustment alone does not identify a causal
effect. When identification is unsupported, preserve descriptive or predictive
results and block only the causal interpretation.

Timestamp and justify protocol amendments. An amendment may remain confirmatory
when made before access capable of revealing the affected outcome comparison,
or under a predeclared blinded or sequential amendment procedure. A change
informed by the affected comparison is post hoc and makes the affected analysis
exploratory. A deviation that breaks measurement, assignment, identification,
or independence invalidates the affected claim; labeling it is insufficient.
Require new untouched evidence that was not used for selection and satisfies
the declared sampling and dependence boundaries before restoring confirmatory
status.

Complete this branch only when the contemporaneous protocol, data and analysis
identities, deviations, effect and uncertainty, and decision read back
consistently. Otherwise block only the dependent confirmatory or causal claim
and preserve correctly labeled descriptive or exploratory results.

## Recurring forecasts

Use when the system repeatedly predicts future values or events.

- Record every forecast origin or as-of time, horizon set, training window, and
  prediction-time availability of exogenous inputs.
- Define feature windows, outcome windows, and label-maturity time. Purge, gap,
  or embargo examples when windows or dependent entities cross a split
  boundary.
- Use rolling- or expanding-origin backtests when they represent deployment.
- Report quality, bias, and interval or quantile coverage by horizon and
  relevant regime; an aggregate across horizons is insufficient when decisions
  differ by horizon.
- Bind each backtest result to its origins, horizons, data snapshot, split
  specification, and model identity.

Do not generalize a one-cutoff result to recurring production origins. Block
only the origin or horizon claims not supported by the evidence.

## Label-poor, unsupervised, self-supervised, or weak-label systems

Use when trustworthy outcomes are absent, delayed beyond the decision, sparse,
or not the training objective.

- Name the external criterion that makes the output useful. Candidate evidence
  can include downstream outcomes, sampled domain adjudication, seeded known
  cases, retrieval judgments, perturbation/stability tests, simulation,
  invariants, or delayed mature labels.
- Record the limits of synthetic, injected, proxy, or expert-reviewed cases.
  They do not establish population prevalence or production precision.
- For anomaly detection, record the contamination or event-rate assumption,
  alert/capacity budget, threshold owner, and review or delayed-label plan.
- Test score and ranking stability under plausible input, seed, window, and
  prevalence changes.
- Treat reconstruction loss, clustering indices, anomaly scores, embedding
  distance, or arbitrary normalization as internal signals, not accuracy,
  calibrated probability, or decision value.

When no independent criterion exists, report usefulness or promotion quality as
`unknown`. Continue contract, pipeline, reproducibility, and operational work
that does not depend on that claim.

## Feedback-mediated ranking, recommendation, allocation, or intervention

Use when the model changes what can later be observed or labeled.

Preserve a versioned impression or exposure record sufficient for the claim:

- eligible candidates or opportunities;
- displayed or acted-on items and their order/position;
- scores, threshold, policy, and release identity;
- assignment or exposure probability when the analysis requires it;
- intervention, outcome, and feedback times; and
- attribution and label-maturity rules.

Audit selection, position, exposure, intervention, survivorship, and
self-fulfilling feedback before treating observations as labels. Keep a
policy-independent or randomized evaluation slice where feasible. Use
off-policy or counterfactual methods only when their assumptions and required
propensities are satisfied.

If the exposure record is insufficient, block only counterfactual lift,
feedback-as-label, and automatic-refresh claims. Continue descriptive
monitoring and other noncausal analysis with explicit limits.

## Probabilities and thresholds

Use when probabilities or scores drive confidence, expected cost, threshold
choice, abstention, triage, or composition.

- Fit the base model, calibrator, and threshold selector on disjoint or
  cross-fitted ownership as required by the evaluation design.
- Freeze the model-transform-calibrator-threshold composite before untouched
  evaluation.
- Use reliability evidence with bin counts or equivalent support information
  and a proper scoring rule; do not treat one aggregate score as
  calibration-only evidence.
- Recheck calibration and threshold economics after material prevalence,
  population, or policy change.

Do not require calibration when only ordering matters and probabilities have no
semantic use.
