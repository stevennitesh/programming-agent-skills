---
name: hillclimb
description: Optimize a measurable outcome through comparable experiments. Exclude causal debugging, one-off feasibility probes, and unmeasured cleanup.
---

# Hillclimb

Iteratively improve a measurable outcome while preserving accepted behavior.
A measured win updates the retained candidate, not necessarily task completion.
Use [prototype](../prototype/SKILL.md) for one bounded empirical uncertainty and
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for an unexplained causal failure.
Optimization authorizes bounded reversible local experiments, not external spend,
live-system effects, publication, or deployment beyond existing authority.

## Define the objective and valid comparison

Establish the metric/unit, useful workload, preserved behavior, target or budget,
and keep criterion before evaluating candidates. Include noise and material
secondary costs. Do not silently trade correctness, quality, or another accepted
objective for a better score. Use a finite proportionate local stopping rule when
none is supplied; ask only about unresolved owner-held tradeoffs or external cost.

Measure the real useful work and verify output independently of the metric.
Preserve baseline identity/conditions and distinguish pre-existing failures from
regressions; do not weaken required checks. Read
[Measurement integrity](references/measurement-integrity.md) when variation,
adaptive selection, proxy measurements, harness changes, or regression thresholds
affect retention or final confirmation.

Repair ordinary benchmark, setup, instrument, or isolation problems within scope
and budget. Verify intended work remains measured. A materially changed ruler
requires remeasuring both baseline and candidate; its score correction is not a
system improvement. A difficult causal failure may need diagnosis, not every
ordinary harness repair.

## Search and retain supported candidates

Choose profiling, coordinated edits, parameter search, ablations, or another
useful method; no one-change-at-a-time rule is required. Keep attempts identifiable
and separable from the retained candidate and unrelated work. Exploratory attempts
may lose. Before promotion, compare with the current best under equivalent
conditions and apply the keep rule and required behavior checks. A combined gain
does not prove each component caused it.

Do not stack unmeasured changes onto the retained candidate or report a plausible
mechanism as a measured win. Equivalent performance may justify simplicity without
being a numerical gain. For substantial runs, retain baseline/current-best,
conditions, meaningful attempts, evidence, and remaining budget to resume without
repeating failures, using existing records and no fixed log format. A combination
of earlier attempts is a new candidate. A plateau may change
the search, not accepted success criteria.

## Confirm and finish

Continue until the target is confirmed, bounded effort ends, no worthwhile supported
hypothesis remains, or an unresolved measurement/authority blocker prevents progress.
Reserve effort for final confirmation. Compare the integrated retained result with
the original baseline under the final valid method; isolated gains need not compose.
Apply Measurement integrity's fresh-run/held-out rules when tuning could bias
selection, preserving frozen evaluation authority.

If confirmation fails, return to the last qualifying candidate or baseline. If
restoration risks unrelated work, preserve and identify the unresolved state.
Retain proportionate regression protection when later changes could erase a material
gain; preserve representative workload, valid outputs, and baseline conditions at
the existing test/benchmark owner. Clean up only experiment-owned work.

Return the final comparison, retained mechanisms, correctness/quality checks,
variability, evidence limits, material harness repairs, and stopping reason.
No improvement is valid; failed measurement is not evidence of no improvement.
Do not claim a global optimum or extrapolate beyond measured conditions.
