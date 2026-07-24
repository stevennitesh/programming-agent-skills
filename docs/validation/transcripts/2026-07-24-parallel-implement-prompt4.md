# Parallel Implement — Deploy Prompt 4

Campaign epoch: `2026-07-24`
Skill: `parallel-implement`
Authorized unit: `Deploy Prompt 4: Prove M0 And H1`
Authority: `writing-great-skills / Audit`
Starting Git HEAD: `94d68e78d8812e9a2ceffd093e729402cac1cff2`

## Decision

Decision: `blocked`.

Campaign shape: `minimum-candidate`.

```text
current: 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
M0 = H1: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
V1: not established
```

Exact M0 passed deterministic construction and helper viability, but failed
the frozen behavioral floor. Both Family B samples blocked the F1
`automatic-in-scope` repair while F2 remained `decision-required`; the rubric
requires only F1 to enter the bounded Repair generation. The exact K-02 helper
surface enforces the same refusal. Because H1 is byte-identical to M0, there is
no contribution arm or viable successor runtime in this unit.

## Fixed Protocol And Sampling

The frozen candidate checker passed before sampling. The maintained helper
suite passed `46/46`. Worker and evaluator fixture identities matched the
protocol manifest, and the worker-visible fixture contained no hypothesis,
rubric, score, candidate term, or conclusion.

Exactly five fresh blinded samples ran with `gpt-5.6-sol`, high reasoning, and
fresh contexts. A-01 and B-01 were dispatched and inspected before the
remaining A-02, A-03, and B-02 wave. Every worker read only the exact runtime
and its assigned worker-visible family and wrote only its assigned capture.
All external mutations remained simulated.

| Sample | Family | Score | Result |
| --- | --- | ---: | --- |
| A-01 | A | 8/8 | pass |
| A-02 | A | 8/8 | pass |
| A-03 | A | 8/8 | pass |
| B-01 | B | 7/8 | fail |
| B-02 | B | 6/8 | fail |

Aggregate: 37/40 criteria, mean 7.4/8, range 6-8, population
variance 0.64, 3/5 sample passes, zero critical failures, and zero protocol
deviations. B-02 is the worst case. Family A had no decision-changing
variance. Both B samples independently failed M0-14; B-02 also deferred the
formal-review owner, while B-01 selected `$review`.

The authoritative per-sample identities and scores are in
[`../evals/parallel-implement-prompt4/results-manifest.json`](../evals/parallel-implement-prompt4/results-manifest.json).
The aggregate decision is in
[`../evals/parallel-implement-prompt4/results.md`](../evals/parallel-implement-prompt4/results.md).

## Protected Behavior And Dispositions

- M0-01 through M0-12 and M0-15 through M0-17 passed.
- M0-13 showed review-route variance in one of two applicable samples.
- M0-14 failed systematically.
- K-01 through K-08 passed deterministic compatibility checks, but unchanged
  K-02 behavior conflicts with M0-14.
- All eight relationship rows passed structural ownership traces; the
  behavioral review-owner selection gap remains.
- The current-only runtime push action and arbitrary same-actor-once rule
  remain rejected from M0; no sample showed regression from those removals.
- No H1 unit exists, no H1 sample ran, and no H1 contribution is claimed.

No V1 was established. Current remains the active canonical runtime. The
experimental runtime, frozen protocol and fixtures, canonical package,
relationships, installation, staging, commit, push, and unrelated dirty
`implement` campaign work were not changed by this unit.

## Evidence Limits

The samples prove judgment only over the supplied simulations. Live
tracker/provider partial mutation, remote publication, irreversible closeout,
provider-specific idempotency, and wider isolation remain unproved. Exact
backend build, random seed, token counts, and latency were unavailable.
Transfer is limited to the frozen bytes, fixtures, model, host, reasoning
configuration, tools, and five samples.

The safe recovery is a bounded Prompt 3 reconstruction that resolves the
M0-14/K-02 contradiction, refreezes runtime and protocol identities, and
reruns Prompt 4. The authorized mutation boundary forbids making that runtime
change here.

## Return

Authorized unit completed: Deploy Prompt 4
Decision: blocked
Campaign shape: minimum-candidate
Runtime identities: current `036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`; M0 = H1 `bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05`; V1 not established
Artifacts changed: five exact raw captures; `docs/validation/evals/parallel-implement-prompt4/results-manifest.json`; `docs/validation/evals/parallel-implement-prompt4/results.md`; this Prompt 4 transcript; current-epoch synthesis evidence reconciliation
Evidence used or reused: exact Prompt 1, Research, Prompt 2, and Prompt 3 identities; deterministic candidate checker; 46 helper tests; five fresh blinded M0 samples; root-held rubric scoring; final repository checks
Residual gaps: M0-14/K-02 construction contradiction; M0-13 review-route variance; live external mutation, provider idempotency, wider isolation, telemetry, and transfer limits
Recommended next unit: Deploy Prompt 3 bounded reconstruction and refreeze
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: exact M0 failed protected behavioral viability, H1 is identical, runtime repair is outside this unit's mutation boundary, and Prompt 4 stops before pruning
