---
name: diagnosing-bugs
description: Find the causal mechanism of a difficult or intermittent failure. Exclude obvious local fixes and open-ended optimization.
---

# Diagnosing bugs

Explain an existing failure with a supported causal mechanism. Diagnosis alone
returns that explanation or unresolved alternatives; an authorized fix must address
the cause and verify required behavior. If expected behavior is unsettled, use
[shape-work](../shape-work/SKILL.md) rather than treating current output as policy.

## Establish the failure and discriminate causes

Identify expected versus actual behavior, symptom, and exposing conditions. Keep
the failure distinct from nearby setup errors. A characterization records what
happens, not what should happen. Use a faithful feedback loop; attributable
production evidence may suffice without a local reproducer.

Trace the earliest evidenced divergence and how it produces the symptom. Form a
falsifiable explanation with predicted observations. When existing evidence fits
credible alternatives, execute a targeted probe or reversible intervention within
authority that distinguishes them. More agreeing observations or one green run
after an edit do not establish cause.

Use the relevant [Investigation methods](references/investigation-methods.md) for
runtime inspection, controlled experiments, intermittency, cross-system failures,
history/reduction, stalled investigations, or performance regressions. Verify that
instrumentation reaches the path and could observe the event. Establish whether it
changes or suppresses the failure and account for that effect before interpreting
observations. A reduced case must preserve the original mechanism.

Allow contributing causes when supported. If attempts stop adding information,
challenge the premise, classifier, or instrument rather than repeating variations.
Retain rejected explanations when needed to avoid repeating a long investigation.

## Repair and verify within authority

For diagnosis alone, retain no product change. For a requested fix, repair the
violated rule's owner and affected callers. Before claiming a failure class fixed,
inspect sibling callers sharing the mechanism. A guard, retry, fallback, or
suppression may be a mitigation without explaining upstream corruption or restoring
the required outcome; label that distinction.

Add or update regression evidence when it protects the real failure or policy
requires it. Prefer detecting the original mechanism over mirroring the patch.
Verify the required behavior through the original faithful loop when available,
not just disappearance of the error. Finite clean runs do not prove elimination
of intermittent failure, and a substitute cannot certify properties it bypasses.

Use repository scratch/isolation rules. Remove or account for diagnostic
instrumentation and resources, preserve requested reproducers/evidence, and repeat
decisive checks when removing instrumentation could change behavior.

Return the cause or precise remaining alternatives, decisive evidence, requested
repair, verification, and limits. If unresolved, distinguish established or ruled-out
facts from plausible causes, identify the next deciding observation and its blocker,
and continue useful authorized checks rather than stopping at a proposed probe.
