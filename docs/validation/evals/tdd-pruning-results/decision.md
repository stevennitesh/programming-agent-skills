# TDD Prompt 4 Pruning-Equivalence Decision

Decision: `accepted`

This is a pruning-equivalence result, not a guidance-improvement claim. Equal
behavior supports removal; the control was not required to fail.

## Fixed Comparison

| Field | Frozen value |
| --- | --- |
| Pre-prune control | `docs/validation/evals/tdd-pruning-pre-prune/` |
| Control tree SHA-256 | `2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae` |
| Final C1 | `skills/experimental/tdd/` |
| C1 tree SHA-256 | `35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c` |
| Samples | Five fresh contexts per arm |
| Task | `protocol.md`, identical for every sample |
| Output contract | `response.schema.json`, identical for every sample |
| Rubric | `rubric.md`, hidden from samples and fixed before sampling |
| Runtime | Fresh-context workers, read-only authority, no test execution |
| Model and reasoning | Same session defaults for every worker; no per-sample override |
| Tools and evidence | Same filesystem tools; only the protocol, schema, and assigned package disclosed |

The intended isolated CLI runner could not authenticate and produced no sample
output. It was replaced before sampling by fresh-context workers. This is a
recorded runtime deviation, not a changed arm input: every admitted sample used
the same replacement runtime and fixed protocol.

## Adjudicated Results

| Arm | Sample | Protected cases passed | Async cases passed | Critical failures | Advisory flags |
| --- | ---: | ---: | ---: | ---: | ---: |
| Control | 1 | 9/9 | 2/2 | 0 | 0 |
| Control | 2 | 9/9 | 2/2 | 0 | 0 |
| Control | 3 | 9/9 | 2/2 | 0 | 0 |
| Control | 4 | 9/9 | 2/2 | 0 | 0 |
| Control | 5 | 9/9 | 2/2 | 0 | 0 |
| C1 | 1 | 9/9 | 2/2 | 0 | 0 |
| C1 | 2 | 9/9 | 2/2 | 0 | 1 |
| C1 | 3 | 9/9 | 2/2 | 0 | 0 |
| C1 | 4 | 9/9 | 2/2 | 0 | 0 |
| C1 | 5 | 9/9 | 2/2 | 0 | 0 |

Aggregate protected-behavior result: control 45/45; C1 45/45. Aggregate
asynchronous result: control 10/10; C1 10/10. No sample used raw sleep,
wall-clock waiting, or an unbounded loop. Every sample selected bounded
condition waiting with a diagnostic for observable completion and
trigger-relative fake-clock advancement for timing behavior.

Every sample also preserved the four-fact bug gate, invalid-RED handling,
unrelated-baseline disclosure, correct assertions, real owned modules,
boundary-double fidelity, GREEN-only bounded refactoring, and the complete
Return evidence boundary.

## Flag Inspection And Variance

`raw/c1-2.json`, case I, ends with the sentence `May claim only that an
expected RED was observed.` The fixed case stated that no command result was
observed. The same answer's action rejects completion, its proof requires an
observed RED and GREEN packet, and the remainder of its claim boundary refuses
GREEN, validation, refactor, TDD, and overall completion claims. The flag is
therefore a contradictory wording defect, not loss of the protected completion
boundary and not a critical failure under the frozen rubric.

Observed variance is one noncritical advisory in one C1 sample and zero
criterion or critical-failure variance. This is within the predeclared bound
of at most one sample on a noncritical criterion. No async-specific variance
was observed.

## Raw Evidence

The ten schema-valid responses are preserved under `raw/` as
`control-1.json` through `control-5.json` and `c1-1.json` through `c1-5.json`.
Every file contains exactly nine cases in A-through-I order. The neutral task,
schema, and predeclared rubric are adjacent to this decision.

## Decision Basis And Limits

C1 has no critical failure, no meaningful protected-behavior regression,
equal aggregate behavior, and bounded variance. Removing the complete Async
Waiting section is accepted for these fixed cases and runtime.

This result does not prove universal equivalence, mechanism contribution,
installed-mirror parity, or behavior outside the fixed cases. It authorizes
Prompt 5 promotion review only; it does not change canonical bytes,
relationships, installation state, or Git delivery.
