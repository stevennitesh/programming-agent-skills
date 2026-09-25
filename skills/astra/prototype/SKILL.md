---
name: prototype
description: Run a bounded experiment to resolve a design, integration, interaction, or performance uncertainty. Exclude root-cause debugging and sustained optimization.
---

# Prototype

Produce the smallest trustworthy observation that can settle a bounded uncertainty.
A successful probe does not establish production readiness.

The prototype is complete when the calling work has judgeable evidence or a
precise evidence gap. Production implementation is outside the experiment unless
it was already authorized.

Use [diagnosing-bugs](../diagnosing-bugs/SKILL.md) when the question is why an
existing failure occurs. Use [hillclimb](../hillclimb/SKILL.md) when the goal is an
iterative measured improvement loop rather than one bounded uncertainty.

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
return the remaining evidence gap rather than presenting a substitute as
equivalent.

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

Do not interpret a broken or invalid instrument as evidence about the design.
Stop when the question is answered, a blocking limitation establishes the gap, or
additional runs cannot change the decision.

Do not expand the experiment into production implementation merely to obtain a
favorable result.

## 4. Return the evidence

Return the decisive observation, the conditions and substitutions that bound it,
and the resulting conclusion or remaining gap. Preserve reproduction detail only
when future verification, comparison, or requested reuse needs it.

Stop or account for resources created by the probe. Preserve requested demos or
evidence artifacts with enough rerun context; otherwise remove disposable
experiment material when safe. Preserve unrelated work.

Prototype code is evidence first. Reuse it in production only after the calling
work evaluates it against production ownership, quality, and integration
requirements.
