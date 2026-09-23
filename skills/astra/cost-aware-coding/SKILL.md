---
name: cost-aware-coding
description: Reduce GPT-6 lead-token churn by routing consequential reasoning and final review to Astra, substantial implementation to Sol, and tightly bounded tasks to Luna Max. Use only when explicitly requested; exclude parallel implementation.
---

# Cost-aware coding

Minimize expensive Astra token and context use without weakening the accepted
result. Keep Astra focused on consequential reasoning, exception handling, and
final review; move implementation-heavy exploration, coding, debugging, and
verification to Sol; use Luna Max for compact bounded tasks when briefing and
verification stay cheap.

The routing objective is lead-token efficiency, not delegation for its own sake.
Delegate only when expected Astra-context savings exceed assignment,
coordination, verification, and recovery overhead. If Astra must continuously
follow, reconstruct, or supervise implementation to keep it on track, the route is
not cost-efficient.

Read [GPT-6 model policy](references/model-policy.md) before selecting a worker.

## 1. Choose the cheapest sufficient route

Keep work with Astra when consequential reasoning, ambiguous requirements,
lead-owned context, or a very small task makes delegation overhead dominate.

Use Sol for substantial repository implementation whose investigation, coding,
debugging, and checks would otherwise consume significant Astra context.

Use Luna Max for a tightly bounded task with a compact self-contained assignment,
clear acceptance, and cheap verification. Do not fragment one coherent Sol task
into Luna microtasks when repeated briefing, synthesis, or verification would cost
more Astra tokens than it saves.

This skill has one delegated writer at a time. A Luna Max task may replace Sol for
a bounded assignment or perform read-only bounded support, but it does not create
a second writer for the delegated checkout.

Reuse accepted requirements and plans. Use [shape-work](../shape-work/SKILL.md)
when consequential behavior or accepted meaning remains unresolved.

This skill does not coordinate parallel fanout. When the user explicitly combines
it with [parallel-implement](../parallel-implement/SKILL.md), retain this skill's
GPT-6 model and effort routing, budget policy, and final review requirement while
parallel-implement owns decomposition, lane custody, concurrency, integration,
and parallel recovery.

For coordinated serial delivery with meaningful checkpoints, read
[Planned delivery](references/planned-delivery.md). When usage measurement or a
hard budget materially affects routing, read [Telemetry](references/telemetry.md).

## 2. Assign work without importing it into Astra

Read only enough to settle the assignment and lead-owned decisions. Use
[Worker assignment](references/worker-assignment.md) to give the worker the
outcome, accepted context, scope, authority, checkout, acceptance, and return
contract it cannot infer. Do not assume inherited conversation or skill context.

Give one actor write custody of the delegated checkout at a time. While a worker
holds custody, Astra stays dormant with respect to implementation: do not follow
the work in parallel, reread intermediate changes merely to stay informed,
reproduce worker reasoning, request routine summaries, or poll for progress.

Use the host's event-driven wait/resume mechanism. Re-engage only when a
lead-owned decision is required, a stable candidate is ready, execution fails, the
user intervenes, or another consequential event occurs. Read-only work on
independent immutable context is fine when it cannot race with the worker or
recreate its implementation investigation.

If Astra must inspect or take over the delegated checkout, first obtain explicit
custody release and establish that worker-owned writers or subprocesses stopped.
Idle, interrupted, or timed-out status alone does not establish release.

## 3. Review and recover

A reviewable return identifies the candidate, material changes, decisive checks
and limits, and releases write custody. It returns decision-relevant evidence, not
an implementation transcript.

Review the candidate with [change-review](../change-review/SKILL.md), reusing valid
candidate-bound evidence. Pending required proof remains incomplete until it
passes or its owner revises the requirement.

Return locally correctable implementation findings to the same worker when its
accumulated context is still useful. Reusing worker context is usually cheaper
than reconstructing implementation state in Astra or a replacement.

Read [Recovery](references/recovery.md) for blocking questions, prerequisite
failures, interruption, custody uncertainty, worker replacement, or route failure.

Do not escalate model or effort because requirements are incomplete, acceptance is
contradictory, permissions are missing, or the environment is broken. Resolve
those causes at their owner.

For a demonstrated implementation-reasoning failure, increase Sol effort before
moving coherent implementation back into Astra. Move implementation ownership to
Astra only when the task has become a lead-owned consequential reasoning problem
or the accepted worker route cannot safely complete it.

## 4. Finish

Complete when the accepted outcome is present in the reviewed candidate, required
checks pass, and material evidence limits are resolved or explicitly owned.

Report the candidate, decisive evidence, and material remaining limits. Do not
replay the worker's implementation history into the final response.

Include usage or cost telemetry only when requested or needed for a governing
budget. Review success does not authorize merge, publication, deployment, or
other external effects.
