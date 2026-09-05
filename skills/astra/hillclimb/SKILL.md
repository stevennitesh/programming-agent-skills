---
name: hillclimb
description: Iteratively improve a measurable runtime, resource, cost, capacity, or quality outcome through controlled local experiments. Use for a requested optimization loop against a representative workload; exclude causal debugging, one-off feasibility probes, and unmeasured code cleanup.
---

# Hillclimb

Improve the actual implementation through comparable experiments. Keep a change
only when evidence supports a worthwhile result and required behavior survives.
This skill owns the optimization loop; prototype explores a bounded design
question, and diagnosing-bugs investigates an unexplained failure.

An optimization request permits scoped local attempts, not automatic commits,
deployment, paid runs, or effects on live systems. Keep external targets and costs
within the user's existing authority. Do not require another approval for ordinary
reversible work already requested.

## 1. Define the objective and stopping conditions

Identify the requested outcome, metric and unit, representative workload, and
behavior that must remain intact. Use the user's target and budget when supplied.
If no effort budget is supplied, choose and state a reasonable finite local budget
whether or not the target is numeric. If the request gives only a direction, state
an exploratory objective; do not invent a product requirement or promise a
particular gain. Ask when a missing tradeoff, external cost limit,
or acceptable quality loss belongs to the user.

Choose a practical keep criterion before seeing candidate results. Account for
noise, maintenance burden, and relevant secondary costs. An apparent improvement
that sacrifices required correctness, quality, memory, latency, or compatibility
does not qualify. Do not silently exchange one objective for another.

Stop at the requested target, the agreed or stated effort limit, lack of worthwhile
supported hypotheses, or a measurement or authority boundary that prevents progress.
No minimum number of attempts is required after the goal is met. Unattended future
runs or scheduling require their own authorization.

## 2. Establish a trustworthy baseline

Inspect the relevant owner and real execution path. Prefer an existing measurement
command; build a small harness only when needed. Verify that it measures the desired
outcome and performs the required useful work. Record the initial source state,
workload, method, environment, and baseline correctness results before changing code.
Distinguish pre-existing failures from regressions; do not weaken the check to hide
either. If the metric or correctness evidence cannot support a keep decision,
resolve that limitation before optimization edits.

Read [Measurement integrity](references/measurement-integrity.md) for variable
measurements, adaptive search, or multi-objective tradeoffs. Take enough baseline
observations to reveal variation that could change the decision. Keep the comparison
method stable. If a material method or workload change is necessary, label the new
comparison and remeasure the initial and retained candidates under it; old numbers
do not establish a gain on the revised objective.

## 3. Try one interpretable hypothesis

Use source, profiles, or prior observations to identify a specific mechanism that
could improve the metric. Test one coherent hypothesis per attempt; coordinated
edits may be necessary, but do not bundle unrelated guesses. Prefer removing work,
using existing capabilities, or improving the actual bottleneck before adding
machinery without evidence.

Preserve the original state and current retained candidate separately. Establish
how to remove the attempted delta without disturbing unrelated work or earlier
accepted changes. Use repository-native isolation when useful; do not reset a dirty
checkout or infer ownership from a short file list. If exact removal becomes
uncertain, preserve the state and report the boundary.

Compare the attempt with the current retained candidate under equivalent conditions.
Check both the metric and relevant correctness or quality constraints. Retain only
a result that clears the keep criterion; otherwise remove that attempt and verify
the retained state is restored. Do not stack unmeasured changes or report a plausible
mechanism as a measured win. A simpler equivalent candidate can win when it satisfies
the stated criterion, but label it as simplification rather than a numerical gain.

## 4. Learn without gaming the measurement

Keep a compact record of the hypothesis, candidate, comparable result, relevant
checks, keep/reject decision, and reason. Use the conversation or repository scratch
conventions, defaulting to `.tmp/hillclimb/<run>/`, unless durable tracking is useful.
No mandatory report schema or commit per attempt.

Use rejected attempts to choose a different supported mechanism rather than cycling.
A plateau can justify reconsidering the bottleneck or a different approach; it does
not justify endless search, arbitrary complexity, or changing the scoring rule to
make an attempt pass. Proposed combinations of earlier attempts are new candidates
and need their own measurement and correctness check.

## 5. Confirm the final implementation

Compare the integrated retained candidate with the original baseline under the
same valid method. Individual gains do not automatically add up. Use confirmation
evidence appropriate to adaptive search, and repeat decisive checks after removing
measurement scaffolding when its removal can affect the result.

Inspect the final change and remove rejected edits, temporary instrumentation,
and resources the run owns. Retain a useful reproducible measurement artifact when
needed to support the result. If final confirmation fails, do not claim the earlier
wins still hold; return to the last verified candidate when safely possible or
report the unresolved state and remaining verification.

Return baseline and final results with units, workload, material variability,
retained changes, correctness/quality evidence, and either target attainment or
the bounded stopping reason. An applied candidate with unavailable required
verification is incomplete. A valid no-improvement result is better than retaining
unsupported changes. Do not claim a global optimum or extrapolate beyond the evidence.
