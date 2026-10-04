---
name: hillclimb
description: Optimize a measurable outcome through comparable experiments. Exclude causal debugging, one-off feasibility probes, and unmeasured cleanup.
---

# Hillclimb

Iteratively improve a measurable objective through comparable experiments. Retain
only evidence-backed changes that preserve required behavior.

A measured win updates the current best candidate; it does not by itself complete
the task. Continue until the requested target or a meaningful bounded stopping
condition is reached, then confirm the final result.

An optimization request authorizes bounded reversible local experiments, not
external spend, live-system effects, publication, deployment, or other effects
outside existing authority.

Use [prototype](../prototype/SKILL.md) for one bounded empirical uncertainty and
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for an unexplained causal failure.

## Define the objective and keep rule

Identify the requested metric and unit, useful workload, behavior that must remain
intact, and any supplied target or budget.

Choose the keep criterion before evaluating candidates. Account for measurement
noise and material secondary costs such as memory, latency, quality, compatibility,
or maintenance burden when they affect the requested outcome. Do not silently
trade one accepted objective for another.

If no effort limit is supplied, use a finite local stopping rule proportionate to
the task. Ask only when an unresolved external cost, acceptable quality loss, or
other owner-held tradeoff changes what qualifies as a win.

Stop when the requested target is confirmed, the bounded effort limit is reached,
no supported worthwhile hypothesis remains, or a measurement or authority blocker
cannot be resolved within scope. Allow for final confirmation within the budget.

## Establish and maintain trustworthy measurement

Use the cheapest valid measurement surface that exercises the real useful work.
Verify that the metric can distinguish an actual improvement from incomplete work
or a correctness or quality regression.

Preserve enough baseline identity and conditions to make later comparisons
meaningful. Distinguish pre-existing failures from regressions rather than weakening
the checks to make optimization easier.

Repair or improve benchmark scripts, fixtures, instrumentation, test harnesses,
and experiment-loop tooling when needed within scope and budget. Ordinary
reversible local repairs and reruns need no renewed permission. Verify that a
repair measures the intended work and preserves required correctness and quality;
do not remove required work or weaken checks to improve the score. Use the
diagnosis workflow when a difficult causal failure needs it, not for every harness
repair.

Read [Measurement integrity](references/measurement-integrity.md) when variation,
adaptive search, proxy measurements, harness changes, or multi-objective tradeoffs
could change the keep decision.

If the workload or measurement method changes materially, rerun the relevant
baseline and retained candidate under the new method. Results measured under the
old ruler do not establish a gain under the new one. Distinguish a measurement
correction from an improvement to the system being optimized.

## Adapt the search and promote supported candidates

Choose and adapt the search method from the evidence. Profiling, parameter
searches, coordinated edits, interaction tests, or ablations can all be useful;
no particular optimization algorithm or one-change-at-a-time method is required.
Keep candidates identifiable and comparisons interpretable. Exploratory attempts
may perform worse; only promotion must satisfy the keep rule. A measured combined
gain does not establish each component's causal contribution.

Keep the experimental attempt separable from the current retained candidate and
preserve unrelated work. Repair ordinary setup or isolation problems and repeat
affected measurements within scope and budget. If safe separation or trustworthy
comparison remains blocked, preserve and report the unresolved state.

Before promotion, compare the candidate with the current best under equivalent
conditions and check both the target metric and required correctness or quality.
Cheap screening can guide exploration; retention needs evidence sufficient for
the requested claim. Retain only candidates that clear the keep criterion.

Do not stack an unmeasured change onto the retained candidate, and do not report a
plausible mechanism as a measured win. A simpler candidate may be preferred when
it satisfies the keep rule, but do not label an equivalent result as a numerical
gain.

Keep enough history to avoid repeating failed attempts. For substantial runs,
retain baseline and current-best identities, measurement conditions, meaningful
attempts and their evidence, and the remaining budget so work can resume. Reuse
existing records; no fixed log format or narrative for every attempt is required.
A plateau can justify revising the bottleneck hypothesis or search strategy; it
does not justify changing accepted success criteria to manufacture a win. A
combination of prior attempts is a new candidate and needs its own comparison.

## Confirm and leave a clear result

Compare the integrated retained candidate with the original baseline under the
final valid method. Individually measured gains do not automatically compose.

When repeated tuning could bias selection, use the confirmation rules in
Measurement integrity rather than treating the best observed development run as
final proof.

If final confirmation fails, fall back to the last candidate that still meets
acceptance under the valid method, or the baseline if none does. Do not report
earlier isolated wins as the final result. If restoration would risk unrelated
work, preserve and clearly identify the unresolved state and remaining work.

Clean up only experiment-owned changes: leave the supported candidate and
intentionally retained measurement support while preserving unrelated user work.

Return the baseline and final comparison, retained mechanism or mechanisms,
correctness or quality constraints checked, material variability or evidence
limits, material harness repairs, and why the loop stopped. A bounded
no-improvement result is valid. If trustworthy measurement could not be established,
report that limitation rather than inferring no improvement.
Do not claim a global optimum or extrapolate beyond the measured conditions.
