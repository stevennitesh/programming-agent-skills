---
name: cost-aware-coding
description: Organize coding across a lead, worker, reviewer, and bounded worker to reduce expensive model usage while preserving acceptance. Exclude parallel implementation coordination.
---

# Cost-aware coding

Deliver the accepted outcome using capable workers while reserving expensive
Astra attention for planning, architecture, codebase ownership, consequential
questions, and review. Judge efficiency across the completed task, including
briefing, implementation, verification, review, and repair.

## Roles and default team

The default team has one lead, one primary worker, and one bounded worker
available for useful support. The lead can also be the reviewer; use an isolated
reviewer when fresh context helps. Activate roles when they have useful work,
rather than creating idle agents to fill a roster.

| Role | Responsibility |
| --- | --- |
| Lead | Preserve the user's starting model and effort, normally Astra. Plan and divide the work, own architecture and codebase decisions, answer consequential questions, and retain final acceptance. |
| Worker | Sol owns implementation, investigation, debugging, verification, and repair within its assignment. It chooses how to deliver the accepted result. |
| Bounded worker | Luna handles clearly scoped searching, retrieval, extraction, bulk writing, mechanical work, or other tasks with limited judgment, including large input contexts and output volumes. |
| Reviewer | The lead or an isolated Astra reviewer assesses the candidate against acceptance and relevant engineering obligations. |

Read [Model policy](references/model-policy.md) before selecting subagent models
or effort. The user selects the lead; this skill never reconfigures that session.

Default to one implementation writer. A bounded helper can provide read-only
support without starting parallel implementation. Use
[parallel-implement](../parallel-implement/SKILL.md) when the user requests parallel
implementation; it owns decomposition, concurrency, lane custody, integration,
and parallel recovery. This skill retains model routing, budget, and final review.
Additional read-only reviewers follow [change-review](../change-review/SKILL.md).

## Plan and assign

The lead establishes the outcome, useful division of responsibilities, acceptance,
and consequential constraints. Reuse accepted plans and repository knowledge.
Choose the amount of planning and its format for the task; a formal plan artifact
or another planning phase is not required. Keep a trivial task direct when
delegation overhead would dominate.

Use phases or checkpoints when they help organization, continuity, or early
verification. Read [Planned delivery](references/planned-delivery.md) when using
them. A phase can remain worker-owned; not every phase needs a lead handoff.

Before delegating implementation, establish the behavior, preservation
requirements, and decision boundaries needed for that assignment. Delegate
bounded investigation when it is needed to resolve those questions. Use
[shape-work](../shape-work/SKILL.md) for unresolved behavior or accepted meaning,
and [codebase-design](../codebase-design/SKILL.md) for unresolved reuse, ownership,
interfaces, or migration. Repeat this readiness check when follow-up instructions
materially change the plan.

Give the worker scope, acceptance, relevant codebase context, and important
implementation constraints through [Worker assignment](references/worker-assignment.md).
Carry transition and retirement obligations into the assignment when behavior is
replaced or consolidated. Leave routine implementation decisions and investigation
with the worker. Luna can gather bounded context for planning or support Sol
without bringing the raw source volume into the lead's context.

## Support implementation, then wait

While the worker implements, the lead waits through the host's event-driven
mechanism. Use the longest practical event-driven wait; if it returns without a
meaningful change, wait again. Do not poll, narrate elapsed time, inspect evolving
changes merely to stay informed, or invent reading and commentary to fill idle
time.

Re-engage for a consequential question, unexpected codebase or architectural
issue, changed requirements, execution failure, an agreed checkpoint, a completed
candidate, or user input. Answer the needed question and let the worker continue.
Use existing knowledge or relevant fixed evidence; do not reconstruct the entire
implementation investigation.

One actor holds write custody at a time. If the lead must inspect the mutable
checkout or take over work, obtain explicit release and confirm worker-owned
writers and subprocesses have stopped. Idle or interrupted status alone does not
establish release. Read-only support uses fixed inputs or independent material
that cannot race with the writer.

## Review and finish

A reviewable return identifies the candidate, changed behavior, decisive checks,
material limits, and released custody. Review it with
[change-review](../change-review/SKILL.md), reusing evidence that remains valid.
The lead reviews directly or selects isolated review according to difficulty,
context independence, coverage, and budget. Scoped high assurance remains
available under change-review; final acceptance stays with the lead.

For replacement or consolidation, assess whether affected callers use the intended
owner, superseded material has been removed within scope, and any retained path is
justified. Check that test cleanup preserves coverage of supported behavior.

Return correctable implementation findings to the same worker when its context
remains useful. When a follow-up changes validation ownership, shared interfaces,
or persisted-input acceptance, carry forward the original preservation
requirements and check affected callers and compatibility obligations. Include a
distinguishing regression test for changed shared validation or persisted-input
acceptance, and review the correction's expanded impact.

Read [Recovery](references/recovery.md) for interruption, custody uncertainty,
blocking questions, or a failing assignment. Model effort cannot resolve missing
requirements, permissions, broken environments, or contradictory acceptance.

Continue through authorized work and corrections until the complete accepted
outcome is present in the reviewed candidate, required checks pass, and material
limits are resolved or explicitly owned. A checkpoint or progress update is not
completion. Return the result, decisive evidence, and remaining limits without
replaying the implementation history.

Read [Telemetry](references/telemetry.md) only when measurement is requested or a
budget materially affects the work. Review success does not authorize publication,
merge, deployment, or other external effects.
