---
name: hillclimb
description: Optimize a measurable outcome through comparable experiments. Exclude causal debugging, one-off feasibility probes, and unmeasured cleanup.
---

# Hillclimb

Iteratively improve a measurable objective through comparable experiments. Retain
only evidence-backed changes that preserve required behavior.

The loop is complete when a retained candidate clears the keep criterion under a
valid final comparison, or when a bounded stopping condition is reached without a
supported improvement.

An optimization request authorizes bounded reversible local experiments, not
external spend, live-system effects, publication, deployment, or other effects
outside existing authority.

Use [prototype](../prototype/SKILL.md) for one bounded empirical uncertainty and
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for an unexplained causal failure.

## 1. Define the objective and keep rule

Identify the requested metric and unit, useful workload, behavior that must remain
intact, and any supplied target or budget.

Choose the keep criterion before evaluating candidates. Account for measurement
noise and material secondary costs such as memory, latency, quality, compatibility,
or maintenance burden when they affect the requested outcome. Do not silently
trade one accepted objective for another.

If no effort limit is supplied, use a finite local stopping rule proportionate to
the task. Ask only when an unresolved external cost, acceptable quality loss, or
other owner-held tradeoff changes what qualifies as a win.

Stop when the requested target is met, the bounded effort limit is reached, no
supported worthwhile hypothesis remains, or measurement or authority prevents a
trustworthy comparison.

## 2. Establish a valid baseline

Use the cheapest valid measurement surface that exercises the real useful work.
Verify that the metric can distinguish an actual improvement from incomplete work
or a correctness or quality regression.

Preserve enough baseline identity and conditions to make later comparisons
meaningful. Distinguish pre-existing failures from regressions rather than weakening
the checks to make optimization easier.

Read [Measurement integrity](references/measurement-integrity.md) when variation,
adaptive search, or multi-objective tradeoffs could change the keep decision.

If the workload or measurement method changes materially, rerun the relevant
baseline and retained candidate under the new method. Results measured under the
old ruler do not establish a gain under the new one.

## 3. Iterate interpretable candidates

Choose hypotheses supported by source, profiles, prior measurements, or another
credible mechanism. Each attempt should test one interpretable mechanism;
multiple coordinated edits can belong to that mechanism, but unrelated guesses
should not be bundled into one measurement.

Keep the experimental attempt separable from the current retained candidate and
preserve unrelated work. If an attempt cannot be safely reverted or compared
independently, stop and report the state rather than corrupting the experiment.

Compare each attempt with the current retained candidate under equivalent
conditions and check both the target metric and required correctness or quality.
Retain only candidates that clear the keep criterion.

Do not stack an unmeasured change onto the retained candidate, and do not report a
plausible mechanism as a measured win. A simpler candidate may be preferred when
it satisfies the keep rule, but do not label an equivalent result as a numerical
gain.

Keep enough history to distinguish the retained candidate and avoid cycling through
the same failed mechanism. A plateau can justify reconsidering the bottleneck or
hypothesis; it does not justify moving the objective, workload, or keep criterion
to manufacture a win. A combination of prior attempts is a new candidate and
requires its own comparison.

## 4. Confirm the retained result

Compare the integrated retained candidate with the original baseline under the
final valid method. Individually measured gains do not automatically compose.

When repeated tuning could bias selection, use the confirmation rules in
Measurement integrity rather than treating the best observed development run as
final proof.

The final repository state should contain only the retained candidate plus
intentionally preserved measurement support. If final confirmation fails, do not
report earlier isolated wins as the final result.

Return the baseline and final comparison, retained mechanism or mechanisms,
correctness or quality constraints checked, material variability or evidence
limits, and why the loop stopped. A bounded no-improvement result is valid.
Do not claim a global optimum or extrapolate beyond the measured conditions.
