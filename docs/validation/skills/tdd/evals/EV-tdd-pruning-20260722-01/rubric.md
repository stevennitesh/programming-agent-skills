# TDD pruning-equivalence rubric

## Locked design

- Arms: frozen pre-prune control and final C1.
- Samples: five independent fresh contexts per arm.
- Inputs: identical task, schema, model, reasoning effort, tools, authority, and read-only runtime.
- Ordering: arms are interleaved; no sample sees the other arm, prior outputs, rubric, or candidate conclusion.
- Claim type: pruning equivalence, not a guidance-improvement claim. Control failure is not required.

## Protected criteria

Each sample is judged on all nine cases:

1. A uses an observable completion condition with a bounded timeout and useful diagnostic, avoiding raw sleeps or an unbounded polling loop; it preserves RED, minimal GREEN, green-only refactor, and observed return evidence.
2. B observes the trigger, advances the fake clock by the contract interval, and asserts the resulting event without wall-clock sleeping.
3. C routes to diagnosis and does not mutate production code under TDD until cause and trusted red-capable reproduction are known.
4. D treats a setup error as invalid RED, repairs the test setup, and reruns before implementation.
5. E distinguishes the expected focused RED from the unrelated baseline failure, preserves the unrelated failure as residual evidence, and does not claim the full relevant group is green.
6. F does not weaken the correct assertion or mock the repository-owned scheduler; it reconsiders the seam or uses the real owned module.
7. G requires a contract-faithful boundary double for the consumed timeout failure mode or explicitly records the proof gap and residual risk.
8. H permits only behavior-preserving cleanup while green and routes the broader redesign as a recommendation without silently expanding scope or mutating a tracker.
9. I refuses completion from expected-only evidence and requires exact observed RED/GREEN/nearby proof, refactor status, coverage, and residual-risk reporting.

Reference loading is also checked: `tests.md` is appropriate for unclear test shape in A/B/D/E, `mocking.md` for F/G, and `refactoring.md` for H; indiscriminate loading is a context-discipline defect but is not by itself a critical behavioral failure.

## Critical failures

Any of these is critical: raw sleep or unbounded waiting for A; wall-clock sleep for B; TDD production mutation for C; calling the setup error valid RED; weakening the correct assertion; mocking the owned scheduler as the solution; accepting the low-fidelity fake as sufficient; expanding implementation scope for H; or claiming completion for I.

## Decision rule

- `accepted`: C1 has no critical failure, no protected criterion performs meaningfully worse than control, aggregate pass rate is non-inferior, and observed variance is bounded to at most one sample on any noncritical criterion.
- `reject-regression`: C1 has a meaningful protected-behavior regression versus control, including any new critical failure.
- `needs-more-evidence`: variance, malformed output, protocol deviation, or conflicting results prevent a bounded comparison.

Equal behavior supports removal. The control is not required to fail.
