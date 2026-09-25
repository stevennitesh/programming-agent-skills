---
name: diagnosing-bugs
description: Find the causal mechanism of a difficult or intermittent failure. Exclude obvious local fixes and open-ended optimization.
---

# Diagnosing bugs

Establish a supported causal explanation for an existing failure. When repair is
requested, verify that the scoped fix addresses that mechanism rather than merely
suppressing the symptom.

Diagnosis is complete when the evidence supports a mechanism strongly enough to
distinguish it from credible alternatives. A fix is complete when the causal
repair is applied and the relevant failure and required behavior checks pass.

If the expected behavior itself is consequentially unsettled, use
[shape-work](../shape-work/SKILL.md) to resolve that meaning rather than treating
current output as the specification.

## 1. Establish the failure faithfully

Identify expected and actual behavior, the symptom, and the conditions that expose
it. Preserve the evidence needed to distinguish the reported failure from a nearby
setup problem or different crash.

A characterization test records what happens; it does not establish what should
happen. Use the cheapest feedback loop that faithfully preserves the reported
mechanism. Reuse attributable incident evidence when it is sufficient; a local
reproducer is not required before reasoning from trustworthy production evidence.

Read the relevant section of
[Investigation methods](references/investigation-methods.md) when intermittency,
concurrency, cross-system behavior, environment differences, history, test order,
performance, or repeated failed fixes sharing one premise affect the diagnosis. Do not simulate away the mechanism under
investigation.

## 2. Establish the causal mechanism

Identify the earliest evidenced divergence from expected behavior and a mechanism
that explains how it produces the reported symptom.

Form a falsifiable explanation with a predicted observation. When credible
alternatives remain, prefer an observation or controlled intervention that
distinguishes them over another observation that merely agrees with the favored
explanation. Keep alternative hypotheses only while the evidence does not separate
them.

Confirm that diagnostic instrumentation reaches the intended path and still
exposes the original failure rather than replacing or suppressing it. A reduced
case is useful only while it preserves the same mechanism.

Support a causal claim with both the mechanism and evidence that separates it from
viable alternatives, not a plausible story or one green run after an edit. Use a
reversible intervention or negative control when observations alone fit multiple
causal explanations.

Allow multiple contributing causes when the evidence requires them. When repeated
attempts stop producing new information, challenge the shared assumption or the
instrument instead of trying another variation of the same idea. Preserve rejected
explanations only when a long investigation would otherwise risk repeating them.

## 3. Repair the cause when authorized

For diagnosis alone, return the supported correction direction without retaining a
product change. For an authorized fix, repair the owner of the violated rule and
the affected callers within scope.

Do not call a guard, retry, fallback, or suppression a root-cause repair when it
only masks unexplained upstream corruption or incomplete work. Keep mitigation
separate from causal repair: a mitigation can reduce active impact without proving
the cause or restoring the full required behavior.

Before claiming a class of failures is fixed, inspect other callers that share the
causal owner or mechanism.

Add or update durable regression evidence when it protects the real failure or
repository policy requires it. Prefer a check that fails for the original mechanism
over one that mirrors the repaired implementation.

## 4. Verify and return

For an applied fix, use the original faithful feedback loop when available and
verify the required behavior, not merely disappearance of the error message.
Diagnosis alone may conclude from sufficient attributable evidence without replay.

For intermittent or variable failures, report evidence strength and remaining
uncertainty rather than treating a finite clean run as proof of elimination. A
local substitute cannot certify an unavailable production-specific property it
does not preserve.

Use repository scratch and isolation conventions for temporary diagnostics.
Remove or account for instrumentation and resources created by the investigation,
preserve requested evidence or reproducers, and repeat decisive verification when
removing instrumentation could change the observed behavior.

Return the supported cause or precise unresolved alternatives, the decisive
evidence, the requested repair if any, verification, and material limits.
