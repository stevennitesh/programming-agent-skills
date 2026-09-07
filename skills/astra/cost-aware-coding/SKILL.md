---
name: cost-aware-coding
description: Route authorized coding work across models to control execution cost, or resume a routed run. Use only when requested; exclude ordinary implementation without a cost-routing request and model comparisons unrelated to execution.
---

# Cost-aware coding

Complete authorized work with justified model allocation and evidence that the
result is acceptable. Model choices here are experimental starting policies,
not demonstrated savings or capability guarantees. The engineering contract
owns coding quality; this skill owns routing, execution custody, and escalation.

## 1. Establish the outcome and cost constraint

Infer the requested mode: route-only recommends a route without implementation;
execute performs authorized work; resume reconciles an existing run before
continuing. An explicit mode takes precedence over defaults. A bare invocation
with no identifiable coding task requires the missing task, not speculative work.

Establish the task from current repository guidance, requirements, code and checks.
Reuse an existing plan or ticket.
Resolve consequential missing product decisions with the user.

A coordinated feature run means this workflow owns delivery of a feature from its
idea or accepted requirements through completion, even when the parent implements
directly. It requires delegated independent review. A bounded fix or edit does not
acquire this gate merely because it is routed. Preserve existing discovery context;
use a separate planning pass only for unresolved substantial decisions.
When planning or revising the feature approach, use
[shape-work](../shape-work/SKILL.md) to resolve decisions and define behavior and
acceptance. An Astra Medium root does this directly; other roots delegate planning
to Astra Medium. Give the planner the shape-work reference and relevant discovery
context. Reuse settled decisions
without restarting discovery or requiring a new specification artifact.
Discussion-only and route-only requests stop at their requested outcome.

Identify any user-selected model, spending limit, latency requirement, or minimum
assurance. Distinguish API spend, subscription allowance, and elapsed time; infer
the priority from the request and clarify only when a material tradeoff remains
unresolved. Choose a sufficient route considering total work through acceptance:
context transfer, execution, repairs, verification, and integration. Without reliable
accounting, use qualitative judgment; do not invent a budget or promise savings.
Read [Model policy](references/model-policy.md) when selecting a route.
Enforce a hard budget only with reliable accounting and bounded dispatch;
otherwise provide a route-only result or obtain agreement to an observable proxy.

## 2. Choose direct work, delegation, or handoff

Use direct execution when the current model is sufficient and transfer overhead
is unlikely to pay back. Group work around coherent behavior and shared context,
not individual files or checklist bullets. Choose an executor using the model policy.
The root can fill a working role: Sol Medium can implement directly; Astra Medium
can brainstorm, plan, or handle difficult work itself. Do not spawn an equivalent
agent merely to fill a phase.

Delegate when a bounded chunk benefits from a different model or independent
judgment enough to justify a new context. This explicitly invoked execution
workflow permits such bounded delegation within the authorized task. Keep it at
the execution root; workers must not delegate. Default to one write-capable
actor at a time, including the parent. Up to two independent read-only children
may run when useful. They may use isolated scratch checks, but must not mutate
the reviewed candidate or shared product state.

For a long execution loop, consider handing ownership to a cheaper sufficient
parent when transfer costs will pay back. Before any delegation or model transition,
read [Runtime selection](references/runtime.md) for selection controls and context.

For explicitly requested concurrent implementation, use
[parallel implement](../parallel-implement/SKILL.md). Supply model choices to its
scheduler. It owns admission, custody, integration, and safe recovery mechanics;
this skill retains model and budget restrictions, repair allowances, and the
coordinated feature review gate.

Route-only ends with the proposed model/effort, rationale, unresolved constraints,
and next action. Save a record only if requested or needed for continuation.
Execution proceeds directly when no transfer or delegation is warranted.

## 3. Execute with bounded ownership

Before a worker starts, give it the accepted outcome, constraints, owned scope,
required inputs, acceptance evidence, prohibited effects, and escalation triggers.
Include applicable repository instructions and task-relevant references; do not
assume a worker sees the parent's loaded skills or load the whole custom pack.
Workers implement directly under the engineering contract.

After dispatch, work only on useful independent responsibilities or wait for the
return. Do not duplicate its assigned investigation while it runs. If a concrete
gap requires intervention, coordinate with the worker rather than silently doing
the same work again.
Use the runtime guidance for agent reuse, completion waits, and health checks.

For ownership transfer, interruption, replacement, or a run that must be resumed
after the current context ends, read
[Continuation and evidence](references/continuation.md). Preserve partial work
and confirm prior writers and subprocesses have stopped before reassignment.
Unknown writer state blocks reassignment, not evidence preservation.

If execution or candidate acceptance fails, or evidence invalidates the approach,
read [Repair allowances](references/repairs.md) before retrying or escalating.
It owns separate implementation and review limits, preserved across replanning,
interruptions, and agent replacements.

If a supplied budget is exhausted or cannot be enforced as required, stop before
further discretionary work, preserve state and report the remaining outcome.
Safe cancellation and custody reconciliation still take precedence over saving
an extra turn. Do not silently exceed a model restriction or premium-use cap.

## 4. Accept the actual result

For a coordinated feature run, once accepted requirements and any existing plan
are implemented and required checks pass, delegate
[change review](../change-review/SKILL.md) before declaring
completion. Use an independent Astra Medium reviewer; use Astra XHigh only when
explicitly selected for intensive review. Supply the accepted requirements and
any existing plan, actual candidate, relevant callers, and test evidence; review
plan assumptions as well as the code. Request a gate decision under change-review's
finding standards, identifying required corrections and nonblocking findings.
Resolve any residual-risk acceptance with its authorized owner before completion;
a review verdict alone does not grant that acceptance.
XHigh effort does not activate the change-review skill's high-assurance
mode; that remains a separate user choice.
Hold the candidate stable under change-review's custody rules; resume
implementation only after review returns.

If review requires corrections, read [Repair allowances](references/repairs.md)
before dispatching repairs. If independent review cannot run, report the unmet gate
rather than substitute self-review or claim completion. Outside coordinated feature
runs, review remains conditional on the user's request or a concrete correctness concern.

The root accepts the actual candidate under the engineering contract and repository
checks, including additions, deletions and untracked changes. A worker's PASS is
a claim to verify. Confirm decisive evidence covers the final behavior and material
interactions, including requirements omitted from the worker packet.
Use returned findings to target acceptance and integration checks; do not reproduce
the worker's investigation. Reinspect for a concrete gap, contradiction, relevant
drift, or required independent assurance. The delegated reviewer owns the independent
diff review; the root need not perform another full review.

Reuse valid evidence; recheck behavior affected by candidate or environment drift.
Independent review supplements executable proof.

## 5. Finish with evidence and limits

Report the outcome, actual models used when observed, changed scope, decisive
checks, escalations, and remaining uncertainty. Distinguish planned/requested
models from verified effective models. Include usage or cost only when measured,
with its accounting basis; absent telemetry means cost is unknown. Do not infer
savings from short output or fewer premium turns. Do not publish, commit, install configuration, or
transfer to a new app task unless the user's authorization covers that action.
