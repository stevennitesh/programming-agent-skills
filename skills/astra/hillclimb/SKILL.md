---
name: hillclimb
description: Optimize a measurable outcome through comparable experiments. Exclude causal debugging, one-off feasibility probes, and unmeasured cleanup.
---

# Hillclimb

Improve a measurable outcome while preserving accepted behavior. Use
[prototype](../prototype/SKILL.md) to resolve a feasibility question and
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for an unexplained causal failure.
Run reversible local experiments within scope. External spend, live-system
effects, publication, and deployment require existing authority.

## Make a comparable measurement

Identify the metric the user cares about, a representative workload, and the
behavior and material costs to preserve. Compare the baseline and candidate on
equivalent useful work. Check the outputs separately from the metric and preserve
existing correctness and quality requirements. A quick comparison can establish
a clear gain. For a query-count optimization, count the calls and check that
the same records come back.

Read [Measurement integrity](references/measurement-integrity.md) when noise
or repeated tuning could change which candidate you keep, when a proxy or
broader claim needs confirmation, when the benchmark changes, or when adding a
regression threshold. Repair ordinary measurement problems within scope. A
material change to the measurement requires rerunning both versions.

## Choose and retain experiments

Choose the experiments most likely to change what you keep. Try a promising
change directly, profile, vary parameters, or test a combination as the evidence
warrants. Compare each candidate you would keep with the current best and
verify the required behavior. Measure changes together before claiming a
combined gain. Attribute the result to the measured combination unless the
evidence isolates a component's contribution. Get the user's decision for
unresolved tradeoffs between accepted requirements.

Keep experiments distinguishable from the retained candidate and unrelated
work. For a longer search, record the baseline and current best, conditions,
useful attempts, evidence, and remaining effort so the work can resume. Reuse
existing notes when available.

## Confirm and finish

Honor the user's target, budget, and stopping conditions. For a narrow task
with no further search requested, one useful confirmed gain can suffice. Stop
when further experiments are unlikely to change the decision or exceed the
scope. Surface unresolved measurement or authority blockers when they prevent
a sound comparison.

Report the final retained result against the original baseline under the final
valid method. Reuse sufficient evidence for the exact final candidate. For a
noisy or repeatedly tuned result, apply the reference's fresh-run and held-out
rules as applicable. If confirmation fails, return to a still-supported
candidate or the baseline. Preserve and report any state whose restoration
would risk unrelated work. Keep regression protection at the existing
benchmark or test owner when a material gain could otherwise be lost.

For quick work, report the comparison, the behavior check, and material limits.
For a longer search, also summarize what was kept, relevant variability or
benchmark repairs, and why the search ended. Report inconclusive evidence or a
comparison that found no useful gain plainly. Clean up only experiment-owned work.
