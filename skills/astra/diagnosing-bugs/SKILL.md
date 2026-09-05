---
name: diagnosing-bugs
description: Root-cause difficult bugs, intermittent failures, or environment and cross-system faults when the cause is unclear. Exclude obvious fixes and optimization without a defect.
---

# Diagnosing bugs

Establish a supported causal explanation of the reported failure, then verify a
causal fix when requested. A diagnosis-only request permits inspection and scoped
temporary local probes, not a retained product change. A fix request can continue
through repair without another approval gate. If the cause turns out to be simple,
finish the requested work rather than returning a routing error.

## 1. Establish the failure and evidence

Identify expected behavior from the request or governing contract, actual behavior,
the precise symptom, and conditions that expose it. Preserve the relevant error,
input, sequence, version, and environment facts. A characterization test records
what happens; it does not establish what should happen. If intended behavior is
unsettled, isolate that decision instead of treating current output as the oracle.

Build the cheapest faithful feedback loop: an existing check, ordinary caller,
captured replay, differential comparison, or small harness. It must distinguish
this failure from a nearby crash or setup problem. Inspect code and form provisional
hypotheses when needed to construct that loop; a local reproducer is not a
prerequisite for reasoning from attributable incident evidence.

Read [Investigation methods](references/investigation-methods.md) for intermittent,
cross-system, environment, history, or performance-dependent failures. Improve the
loop's speed and signal where useful, but preserve the mechanism causing the bug.
Do not simulate away the concurrency, persistence, or protocol under investigation.

## 2. Locate the causal mechanism

Trace backward from the visible failure to the earliest evidenced divergence from
expected state, then forward to explain the original symptom. Examine the actual
owner, inputs, transitions, and relevant callers. Compare working and failing
conditions; recent edits or a suspicious component are leads, not proof of cause.

State a falsifiable explanation, its predicted observation, and the strongest
credible alternative. Keep multiple explanations only while they remain useful;
no hypothesis quota is required. Choose the cheapest observation or controlled
intervention whose outcomes distinguish them. Prefer targeted state inspection
over broad logging. A coherent intervention may change several lines, but avoid
bundling independent guesses so the result remains interpretable.

Check that the instrument reached the intended path and that its error did not
replace the original failure. Minimize inputs or steps only while the reduced
case still represents that failure. Record rejected explanations and decisive
observations briefly so the investigation does not cycle through old guesses.

Support a causal claim with the mechanism and evidence that distinguishes it from
viable alternatives, not merely a plausible story or one green run after an edit.
A reversible intervention or negative control is especially useful when the
observations also fit a different cause. Investigate multiple contributing causes
when the evidence requires them; do not force every incident into one faulty line.

If attempts stop teaching anything, reconsider the hypothesis, instrument, scope,
or missing evidence before trying another patch. Repeated failures do not by
themselves prove an architectural defect. Return a precise unresolved cause or
next discriminating observation when progress needs unavailable evidence.

## 3. Repair within the requested scope

For diagnosis alone, recommend a correction and preserve the supporting evidence.
For an authorized fix, repair the enforcing owner and affected callers within
scope. A guard is appropriate when that owner must reject invalid input; it is
not a causal repair when it hides unexplained corruption or incomplete work.
Check sibling paths before claiming the whole bug pattern is fixed.

Keep mitigation distinct from root-cause repair. An authorized reversible measure
may reduce active impact before the cause is established; state its limits and
preserve evidence needed for continued investigation. Do not claim mitigation
proves the cause or restores behavior it has not demonstrated.

Remove rejected experimental edits without disturbing unrelated work or accepted
changes. If removal cannot be isolated safely, preserve the state and report it.
Add a durable regression check when it protects the real failure or repository
policy requires one. Prefer a check that fails for the original mechanism over
one that simply mirrors the repaired implementation.

## 4. Verify and return

Rerun the original feedback loop under relevant conditions and verify the requested
behavior, not just absence of the error message. For intermittent or performance
failures, compare observations under equivalent conditions and report exposure,
variation, and remaining uncertainty. A passing local substitute cannot certify
an unavailable production environment.

Use invocation-owned scratch paths under repository conventions, defaulting to
`.tmp/diagnosing-bugs/<case>/`. Remove temporary instrumentation and release owned
processes or resources on completion or interruption. Preserve a useful requested
reproducer or evidence artifact with its rerun conditions; do not erase the only
record supporting the conclusion. Capture only necessary diagnostic data, redact
secrets, and keep live instrumentation and external effects within actual authority.
Repeat decisive verification after removing instrumentation when its removal
could change the observed outcome.

Return the symptom and expected behavior, supported mechanism or unresolved
hypotheses, decisive evidence, applied or proposed correction, verification, and
material limits. Diagnosis is complete when the cause is supported; an unresolved
investigation remains unresolved. A fix is complete when the scoped causal repair
is applied and relevant checks of the original failure and required behavior pass.
Report statistical uncertainty explicitly; unavailable required checks leave
verification incomplete.
