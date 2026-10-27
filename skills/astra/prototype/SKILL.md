---
name: prototype
description: Run a bounded experiment to resolve a design, integration, interaction, or performance uncertainty. Exclude root-cause debugging and sustained optimization.
---

# Prototype

Resolve a bounded uncertainty with a new observation. Reuse existing evidence
when it already decides the question. Use [diagnosing-bugs](../diagnosing-bugs/SKILL.md)
for an existing failure's cause and [hillclimb](../hillclimb/SKILL.md) for sustained
measured improvement. A prototype may still need several runs or revisions.

## Frame faithful evidence

State the uncertainty, affected decision, and observation that distinguishes
credible outcomes. Set consequential comparison conditions or success criteria
before the decisive run, including a limitation case when happy-path behavior
cannot decide. Do not use an experiment to settle a user-owned product preference.

Use the cheapest surface that preserves the deciding mechanism. Simplify incidental
infrastructure and polish, not concurrency, persistence, interaction, or another
property being tested. Read the relevant [Evidence methods](references/evidence-methods.md)
section for state/logic/integration, visual interaction, or variable measurements.
Substitutes prove only properties they preserve, not production readiness.

## Run and adapt

Follow repository scratch and isolation rules and authorized development targets.
A local path does not isolate a shared database or service. Account for created
files, processes, and other resources; preserve unrelated work.

Exercise the actual behavior and verify the instrument reaches the mechanism and
exposes the deciding observation. Repair ordinary setup or instrumentation within
scope and continue; a broken instrument does not disprove the approach. If faithful
evidence remains unavailable, state the gap and bound substitute-based claims.

Use exploratory runs, comparisons, or revised instruments as needed. Make question
or criterion changes explicit and distinguish exploratory evidence from proof of
the revised conclusion. Stop when answered, genuinely blocked, or further effort
cannot justify its decision value. Do not expand into production work to obtain
a favorable result.

## Return and continue within scope

Deliver the observation, conditions, substitutions, conclusion or exact gap, and
requested demo, comparison, or reusable experiment. Preserve reproduction detail
when future use needs it. Account for resources, stop or explicitly retain created
services/processes, preserve requested artifacts, and safely remove other disposable
material. Identify blocked deliverables.

Prototype code remains evidence until the calling work evaluates production
ownership, quality, and integration. Resume already-authorized implementation when
the result unblocks it; a prototype-only request ends with the result and grants
no wider production or external effects.
