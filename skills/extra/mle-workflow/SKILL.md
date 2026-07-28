---
name: mle-workflow
description: Build, review, or harden production machine-learning systems through explicit prediction and data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use for production ML features, model refreshes, ranking or recommendation systems, classifiers, embeddings, forecasting pipelines, notebook-to-pipeline conversions, promotion criteria, training-serving consistency, drift, leakage, and model operations. Do not use for one-off exploratory notebook analysis that has no production or reproducibility requirement.
---

# Machine Learning Engineering Workflow

Turn model work into a production ML system with clear contracts, repeatable
training, measurable quality gates, deployable artifacts, and operational
monitoring.

## Calibrate the scope

Use only the lanes the system needs. Do not assume supervised labels, online
serving, a feature store, GPUs, human review, A/B tests, or real-time feedback.
Prefer the smallest set of controls that makes the work reproducible and
reviewable. A data contract, baseline, evaluation script, and rollback note may
be enough.

Before changing code:

- Inspect the repository for existing data, training, evaluation, serving,
  deployment, and monitoring paths.
- State missing assumptions instead of silently selecting labels, metrics,
  slices, thresholds, or infrastructure.
- Start from the decision affected by the model, not from a preferred algorithm.
- Do not introduce a parallel ML stack without evidence that the existing path
  cannot support the requirement.

## Write the iteration compact

For ambiguous, high-impact, or metric-heavy work, capture this compact before
implementation. Keep it short enough for a pull request description.

```text
Goal:
Who cares:
Decision owner:
Action changed by the model:
Success metric:
Guardrail metrics:
Mistake budget:
Unacceptable mistakes:
Assumptions and constraints:
Labels and data snapshot:
Baseline:
Candidate signals:
Threshold or configuration plan:
Evaluation slices:
Known risks:
Next experiment:
Rollback or fallback:
```

Skip fields that genuinely do not apply; do not invent values to fill the
template.

## Core workflow

### 1. Define the prediction contract

Specify:

- The prediction target, decision owner, and product or system behavior affected
- Input entity, output schema, confidence or calibration fields, and latency
  limits
- Batch, online, streaming, or hybrid serving mode
- Fallback behavior when the model or a dependency is unavailable
- Human review or override paths for high-impact decisions
- Privacy, retention, and audit requirements

Do not accept "improve the model" as the complete requirement. Tie the work to
observable behavior and a measurable acceptance gate.

### 2. Lock the data contract

Record:

- Entity grain and primary key
- Label definition, timestamp, availability delay, and confidence
- Feature timestamp, freshness expectation, and point-in-time join rules
- Train, validation, test, and backtest split policy
- Required columns, allowed nulls, ranges, categories, and units
- Sensitive fields excluded from training artifacts and logs
- Dataset version or immutable snapshot identifier

Check leakage before model complexity. Remove any feature unavailable at
prediction time or joined with future information.

### 3. Establish a baseline and mistake economics

Choose metrics from failure costs:

- Use a confusion matrix when false positives and false negatives apply.
- Favor precision when incorrect positive decisions dominate the cost.
- Favor recall when missed positives dominate the cost.
- Use ranking metrics when order matters more than one threshold.
- Track calibration, latency, throughput, memory, and cost when relevant.
- Compare against a simple baseline and the current production model.

State which mistake each metric makes cheaper, which it may make more likely,
and who absorbs the cost. Do not add model complexity until error analysis
shows why additional signal or capacity could help.

### 4. Build a reproducible pipeline

Make training runnable without hidden notebook state:

- Put hyperparameters, paths, and feature options in typed or validated config.
- Pin relevant package and model dependencies.
- Set random seeds and document unavoidable nondeterminism.
- Record the dataset version, code revision, config hash, metrics, and artifact
  location.
- Package preprocessing with the model artifact.
- Share train, evaluation, and inference transformations or prove their
  equivalence with tests.
- Make retries idempotent.

Prefer immutable configuration and pure feature transforms over global mutable
state.

### 5. Declare evaluation and promotion gates

Define gates before training finishes:

- Primary metric aligned with the product decision
- Baseline and current-production comparisons
- Guardrails for latency, calibration, important slices, cost, and error
  concentration
- Repeated-run variance or confidence intervals when results are noisy
- Human review of failure examples for high-impact models
- Explicit fail-closed "do not ship" thresholds

Treat offline metrics as gates, not guarantees. When a model changes live
behavior, select a proportionate shadow, canary, A/B, or staged rollout.

### 6. Package the serving contract

Require:

- A versioned artifact containing config, preprocessing, and training-data
  reference
- Input validation for missing, stale, invalid, and out-of-range features
- Model version in outputs or prediction logs
- Timeout, batching, resource limits, and fallback behavior where applicable
- Safe artifact loading and logs that exclude secrets and sensitive data
- Integration tests for bad input, empty batches, dependency failure, and
  fallback behavior

Never allow training-only feature logic to diverge from serving logic without
an equivalence test.

### 7. Deploy with rollback

Name the rollout method, traffic or batch boundary, dashboards, quality and
system guardrails, rollback triggers, previous known-good artifact, and
traffic-switch mechanism. A rollback must not require retraining.

### 8. Monitor and refresh

Monitor the signals that apply:

- Availability, errors, timeouts, queue depth, and latency
- Feature nulls, ranges, categories, and freshness drift
- Prediction and confidence distribution drift
- Label arrival health and delayed quality metrics
- Business guardrails by model version and important slice

Assign alert ownership and define retraining or investigation criteria. Do not
equate distribution drift with quality degradation without supporting evidence.

## Run the error-analysis loop

After each meaningful experiment:

1. Separate false positives, false negatives, abstentions, low-confidence
   cases, and system failures.
2. Cluster errors by relevant traits such as time, source, language, geography,
   device, sparsity, freshness, label source, or model version.
3. Distinguish model errors from data bugs, ambiguous labels, product ambiguity,
   instrumentation gaps, and serving mismatches.
4. Map each important cluster to better labels, features, thresholds,
   configuration, or product fallback.
5. Preserve important failures as a regression test, evaluation slice,
   dashboard signal, or runbook entry.
6. Express the next iteration as a falsifiable experiment.

## Keep an observation ledger

```text
Iteration:
Change and reason:
Metric and slice movement:
False positives and false negatives:
Unexpected errors:
Decision:
Tradeoff accepted:
Regression added:
Debt created:
Next iteration:
```

## Review checklist

- [ ] Prediction contract is explicit and testable
- [ ] Data contract covers grain, label timing, feature timing, and version
- [ ] Leakage is checked against prediction-time availability
- [ ] Training is reproducible from code, config, data version, and seed
- [ ] Metrics compare with a baseline and current production behavior
- [ ] Important slices and operational guardrails are evaluated
- [ ] Promotion gates are automated and fail closed
- [ ] Training and serving transformations are shared or equivalence-tested
- [ ] Artifact contains version, config, data reference, and preprocessing
- [ ] Serving validates inputs and defines fallback and rollback behavior
- [ ] Monitoring covers system health and applicable model-quality signals
- [ ] Sensitive data is excluded from artifacts, logs, prompts, and examples

## Return

Return the concrete artifacts appropriate to the request: iteration compact,
data contract, baseline plan, evaluation and promotion gates, pipeline changes,
test evidence, deployment and rollback plan, monitoring plan, or review
findings. Clearly identify unresolved unknowns that block production readiness.
