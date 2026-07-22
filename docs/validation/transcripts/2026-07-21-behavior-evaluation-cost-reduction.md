# Behavioral Evaluation Cost Reduction

Date: 2026-07-21

## Decision

Reduce Deploy Prompt 4 sampling overhead through control-first scheduling,
compatible same-context claim grouping, exact-arm reuse, and compact worker
returns. Preserve the existing five-independent-samples-per-arm floor,
contamination controls, root-held rubric, output inspection, variance record,
and residual-gap requirements.

This changes the deployment method only. It does not change Writing Great
Skills instructions, relationships, promotion state, installation, or Git
state. Commit preflight separately normalized two trailing blank lines in the
accepted experimental package, producing current hash
`c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`;
no instruction-bearing text changed.

## Replay Of The Writing Great Skills Evaluation

The completed Prompt 4 evaluation used five waves and 25 fresh contexts:

| Wave | Arm | Contexts |
| --- | --- | ---: |
| 1 | upstream metadata | 5 |
| 2 | candidate metadata | 5 |
| 3 | upstream full package | 5 |
| 4 | candidate full package | 5 |
| 5 | admitted pre-prune full package | 5 |

The candidate full-package arm was already reused for pruning equivalence. The
new method also lets each metadata arm lock its routing decisions before the
same workers see their assigned package body. The equivalent schedule is:

| Wave | Locked work in each fresh context | Contexts |
| --- | --- | ---: |
| 1 | upstream metadata decision, then upstream full-package cases | 5 |
| 2 | candidate metadata decision, then candidate full-package cases | 5 |
| 3 | admitted pre-prune full-package cases | 5 |

The final candidate arm in wave 2 serves both the upstream baseline-delta and
pre-prune pruning-equivalence comparisons because its package hash, fixed
cases, rubric, runtime, and authority are identical for both claims. The
schedule therefore preserves five independent samples for every behavioral
arm while reducing fresh contexts and dispatch waves from 25 to 15, a 40
percent reduction. Compact action-and-Return packets reduce output tokens
without replacing root semantic judgment.

## Preserved Evidence Invariants

- Every behavioral claim still has a realistic control that can exhibit its
  failure.
- Controls are judged before candidate dispatch; absent control failure stops
  the candidate arm.
- Metadata decisions are locked before body disclosure.
- Candidate language, expected behavior, conclusions, and peer outputs remain
  outside neutral worker protocols and control contexts.
- Arm reuse requires unchanged assigned bytes, neutral protocol and inputs,
  model and reasoning settings, tools, authority, evidence, and runtime.
- A changed candidate reruns behaviorally affected candidate arms; unchanged
  controls remain reusable.
- Each unique context counts only for claims its fixed scenario and root-held
  rubric actually exercise.
- Read-back, mechanical checks, and relationship traces continue to prove
  nonbehavioral claims without behavioral sampling.
- The root inspects every result and records per-sample outcomes, aggregate,
  variance, worst result, critical failures, deviations, unavailable telemetry,
  and residual gaps.

## Proof Boundary

This is a schedule-equivalence proof over the immutable Prompt 4 protocol and
recorded arms, not a new claim about skill wording. No new behavioral wave is
warranted because the fixed tasks, sample floor, arm bytes, rubric, and
acceptance gates are unchanged. Read-back and diff checks prove the method
change; a future Prompt 4 run will provide operational timing and token
telemetry when those measurements are available.
