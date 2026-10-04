---
name: prototype
description: Run a bounded experiment to resolve a design, integration, interaction, or performance uncertainty. Exclude root-cause debugging and sustained optimization.
---

# Prototype

Resolve a bounded uncertainty with evidence credible enough to guide the calling
decision. Choose the experiment design, tools, fidelity, variants, measurements,
and reporting format. Keep the effort proportionate to the question. A successful
probe does not establish production readiness.

Use [diagnosing-bugs](../diagnosing-bugs/SKILL.md) when the question is why an
existing failure occurs. Use [hillclimb](../hillclimb/SKILL.md) when the goal is an
ongoing measured improvement loop. A bounded prototype can use multiple runs and
revisions to answer its question.

## 1. Define the deciding observation

State the uncertainty, the decision it affects, and the observation capable of
distinguishing the credible outcomes. Reuse an existing result when it already
settles the question; do not build a ceremonial prototype.

Define consequential comparison conditions or success criteria before the
decisive run so the result is not judged retrospectively. Include a condition
that can expose the relevant limitation when a happy-path demonstration would
not distinguish the decision.

Do not use an experiment to decide an unresolved product preference on the user's
behalf. If exploration changes the question or metric, state that change rather
than silently moving the success rule.

## 2. Preserve necessary fidelity

Use the cheapest existing or temporary surface that can faithfully expose the
deciding property. Simplify incidental infrastructure, state, and polish, not the
mechanism whose behavior is being tested.

A substitute supports only claims about properties it preserves. An in-memory
model cannot establish database isolation, and a static render cannot establish
interaction behavior. If the required mechanism or environment is unavailable,
determine whether ordinary setup or instrument repair can make it usable within
scope. When faithful evidence remains unavailable, report the gap and limit
substitute-based claims to the properties actually exercised.

For state, logic, integration, visual interaction, or variable measurements, read
the relevant section of [Evidence methods](references/evidence-methods.md).

## 3. Run the experiment

Follow repository scratch and isolation conventions. Keep experiment effects
within authorized development targets and account for processes, services, files,
or other resources the probe creates. A disposable local path does not isolate a
shared database or external service.

Exercise the actual behavior, rendering, or measurement under the framed
conditions. Confirm that the instrument reaches the intended mechanism and makes
the deciding observation visible.

Use exploratory runs, comparisons, instrument improvements, and reruns when they
help resolve the uncertainty. Repair ordinary probe errors, missing local setup,
or faulty instrumentation within authorized scope and continue. A broken
instrument is not evidence that the proposed approach fails.

Keep question or criterion changes visible and distinguish exploratory findings
from evidence for the revised conclusion. Stop experimenting when the question is
answered, a genuine blocker establishes the evidence gap, or further effort is
unlikely to improve the decision enough to justify its cost.

Do not expand the experiment into production implementation merely to obtain a
favorable result.

## 4. Deliver the result and continue within scope

Return the decisive observation, the conditions and substitutions that bound it,
and the resulting conclusion or precise evidence gap. Deliver any requested
runnable demo, comparison artifact, or reusable experiment with enough context to
use or rerun it. Identify blocked deliverables explicitly. Preserve other
reproduction detail when future verification or comparison needs it.

Completion includes the requested evidence and artifacts and accounting for the
probe's resources. Stop or account for created processes and services; retain
requested artifacts and remove other disposable material when safe. Preserve
unrelated work.

Prototype code is evidence first. Reuse it in production only after the calling
work evaluates it against production ownership, quality, and integration
requirements.

When the experiment supports already-authorized implementation, carry its result
back into that work and continue within the active workflow. A prototype-only
request ends with its result; the experiment does not itself authorize production
implementation or other effects outside its scope.
