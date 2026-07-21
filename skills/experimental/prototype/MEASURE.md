# Measure Prototype

Use this branch for one comparative design question whose relevant latency, throughput, resource, variability, or scaling observations may vary across runs. [SKILL.md](SKILL.md) owns Freeze, authority, the lifecycle, reconciliation, and Return. This file owns only Measure Probe, Smoke, verdict-evidence mechanics, and return to main Judge.

## Fit

Measure compares predeclared design alternatives under one frozen workload. It does not diagnose an unexplained slowdown, certify a production baseline, prove an SLO, or replace production-scale validation. Route uncertain symptoms to diagnosis; return production performance proof to its delivery or audit owner.

## Measurement Contract

Freeze and expose:

- hypothesis or compared directions;
- metric and unit;
- representative workload and input distribution;
- environment facts that materially affect interpretation;
- warmup and sample rules;
- verdict threshold or comparison rule;
- known confounders and unsupported extrapolations.

Use existing repository measurement tooling when suitable. Keep compared directions isolated, workloads and material conditions identical, and the harness small enough to delete. Do not tune the workload or threshold after seeing decisive results.

## Observe

Record individual samples or distribution summaries, not only a best run. Report variance and worst observed result when variability affects the decision. Identify environmental noise, cache state, warm versus cold behavior, and ordering effects when material.

## Smoke And Evidence

Smoke passes when the harness executes the frozen workload for every direction and records the declared metric. Smoke does not prove production representativeness.

Verdict evidence applies only the frozen rule to the collected samples and states the limits and confounders. A changed rule or workload requires a fresh invocation.

Return to `Judge` in [SKILL.md](SKILL.md); this branch does not Reconcile or Return.
