---
name: hillclimb
description: Repeatedly improve one measurable runtime, resource, cost, capacity, or product outcome of a fixed representative workload against a settled target. Use only when explicitly selected; exclude one-off fixes, causal diagnosis, disposable design probes, and code-shape simplification.
---

# Hillclimb

Improve one measurable result through a bounded sequence of comparable
experiments. Keep only changes that produce a material measured win without
breaking accepted behavior.

The invocation authorizes repeated local source attempts inside the named
target. It does not authorize staging, commits, push, live or external
mutation, or unrelated cleanup. Preserve unrelated work. Apply repository
instructions and the engineering contract.

## 1. Frame

Settle the accepted behavior, representative real workload, metric and unit,
improvement direction, target, practical improvement threshold, attempt or
time/cost ceiling, and nearest useful correctness checks. The target and
campaign ceiling must come from the request or an authoritative repository
contract; ask when either is missing. Infer only mechanical measurement details.

If the workload does not reproduce the property or no stable meaningful metric
is available, return that measurement gap before mutating production code.

## 2. Baseline

Prefer an existing repository measurement path. Create the smallest disposable
probe only when needed, and exercise the real caller or artifact whenever
practical.

Hold material environment, configuration, workload, cache, warmup, and ordering
conditions constant. Take enough observations to expose relevant variation;
do not select one best run. Confirm that the ruler distinguishes a meaningful
change, define the keep threshold before candidate results, record the
baseline, then freeze the workload and comparison method.

If the workload or ruler must change after attempts begin, stop this campaign
as incomparable. Continue only under a separately bounded campaign.

## 3. Climb

Trace the current owner, callers, and data path far enough to form one
mechanism-specific hypothesis. Test one coherent hypothesis per attempt; it may
require several coordinated edits, but keep it isolated from unrelated work.
Inspect existing target changes and capture the invocation baseline. Do not try
an edit that cannot later be removed without touching pre-existing work or an
accepted attempt; if exact removal becomes uncertain, preserve state and stop.

Measure under the frozen conditions. Prove that baseline and candidate perform
equivalent work inside identical measured boundaries; otherwise reject the
attempt. If the improvement clears the practical threshold, run the nearest
correctness check and keep it only when accepted behavior remains intact.
Otherwise remove only that attempt. Code inspection or a plausible explanation
is not a measured win.

Run decisive measurements serially so competing work does not distort the
result.

## 4. Learn

Retain only enough attempt history to avoid cycling and choose the next
distinct supported mechanism. Keep it in the conversation, or under
`.tmp/hillclimb/<run>/` only when resumption or comparison needs it; no formal
ledger or schema is required.

Do not stack unmeasured changes, weaken the target after seeing results, or add
permanent harness machinery when an existing command or disposable probe is
enough. Continue only while a worthwhile authorized hypothesis remains.

Stop when the target is met, the declared ceiling is reached, no worthwhile
supported hypothesis remains, or measurement, proof, or authority fails.

## 5. Finish

Remeasure the integrated candidate against the original baseline under the
same conditions. When observed variation could change the keep decision,
confirm the result against a fresh baseline in alternating or counterbalanced
order. Inspect the final diff and real artifact. Remove rejected
attempt residue, debug scaffolding, and complexity that no accepted win needs;
when two candidates perform equivalently, keep the simpler one.

Return the workload and metric, baseline and final result, delta, retained
changes, correctness evidence, and either target attainment or the bounded
stopping reason. Do not automatically stage, commit, publish,
review, document, or start another workflow.

Complete when the final candidate has a trustworthy baseline-to-final
comparison, relevant behavior passes, rejected attempts are absent, the final
diff contains only accepted changes, and the target result or bounded stop is
reported honestly.
