---
name: cost-aware-coding
description: Propose a cost-aware coordination plan or execute an accepted one. Use only when requested for coding work; exclude ordinary implementation and standalone model comparisons.
---

# Cost-aware coding

Complete authorized work with justified model allocation and evidence that the
result is acceptable. Model choices here are experimental starting policies,
not demonstrated savings or capability guarantees. The engineering contract
owns coding quality; this skill owns routing, execution custody, and escalation.

## 1. Establish the outcome and cost constraint

Use two modes:

- **Coordination plan:** analyze the work, propose ownership and routing, and obtain
  acceptance before product implementation. This is the default for a new task.
- **Execution:** carry out the accepted coordination plan. An explicit execution
  request with a settled route counts as acceptance; do not ask again. If the
  route is unsettled, present it for acceptance first.

A bare invocation without an identifiable task needs the task first. Resume is
execution after state reconciliation, not a third mode.

Establish the task from current repository guidance, requirements, code and checks.
Resolve consequential missing product decisions with the user.

Reuse existing discovery, decisions, and any plan or ticket; add a planning pass
only for unresolved substantial decisions, without requiring a new spec artifact.
Include the [feature review gate](#4-accept-the-actual-result) when selecting the route.
When planning or revising the feature approach, use
[shape-work](../shape-work/SKILL.md) to resolve decisions and define behavior and
acceptance. An Astra Medium root does this directly; other roots delegate planning
to Astra Medium. Give the planner the shape-work reference and relevant discovery
context. Discussion-only requests stop at their requested outcome.

Identify any user-selected model, spending limit, latency requirement, or minimum
assurance. Distinguish API spend, subscription allowance, and elapsed time; infer
the priority from the request and clarify only when a material tradeoff remains
unresolved. Choose a sufficient route considering total work through acceptance:
context transfer, execution, repairs, verification, and integration. Without reliable
accounting, use qualitative judgment; do not invent a budget or promise savings.
Read [Model policy](references/model-policy.md) when selecting a route.
Enforce a hard budget only with reliable accounting and bounded dispatch;
otherwise present a coordination proposal without executing, or obtain agreement
to an observable proxy. These limits also apply to planning work.

## 2. Propose and accept the coordination plan

The root owns coordination planning: who works, with which model, and in what
order. Shape-work owns feature design and implementation planning. Reuse its
accepted output; do not create competing plans. Choose implementation ownership:

- **Root implements:** a small cohesive assignment, with or without a feature plan; the root
  implements when its model/effort fits. Several steps through schema, API, UI, and tests can still
  be one coherent assignment.
- **Root coordinates:** substantial work units need dependency handoffs, different
  expertise, or meaningful integration. The root plans, coordinates, integrates,
  and accepts; delegate product implementation and repairs. One reusable worker
  may execute several sequential units. Keep root integration to landing and
  verification; return product-code corrections to their implementer.

Coordination protects the root's attention; it is not automatically cheaper.
For root implementation, retain sufficient permitted work at the root unless a cheaper
actor is likely to repay transfer and coordination costs over the remaining work.
When transferring work, reuse a suitable available actor before creating one.
Before a new spawn, name in one sentence the concrete benefit that direct work
or a suitable existing actor cannot provide: capability, worthwhile cost reduction,
independence, concurrency, or the chosen coordination responsibility. Phases, role labels,
repository boundaries, and file count alone do not justify a new actor.

Planning permits justified read-only specialists and isolated scratch checks,
but no product implementation or execution-worker pre-spawning before acceptance.
Only the root delegates; workers must not delegate. During execution, default to one write-capable
actor at a time, including the parent. Up to two independent read-only children
may run when useful. They may use isolated scratch checks, but must not mutate
the reviewed candidate or shared product state.

Read [Runtime selection](references/runtime.md) once when establishing the route;
reuse it until the runtime, route, or relevant configuration changes. Most runs
start on Sol Medium; retain a sufficient root. If a different root model/effort
is justified, recommend it with the proposal and ask the user to switch this
conversation before execution. A recommendation does not change runtime settings.

For explicitly requested concurrent implementation, use
[parallel implement](../parallel-implement/SKILL.md). Supply model choices to its
scheduler. It owns admission, custody, integration, and safe recovery mechanics;
this skill retains accepted implementation ownership, model and budget restrictions, repair allowances,
and the feature-delivery review gate.

Present a compact proposal: reference the accepted feature approach, name the
root model/effort and implementation ownership, assign coherent work and reusable
actors with dependencies, and include acceptance checks, review, and permitted
recovery from [Repair allowances](references/repairs.md). Identify unresolved
constraints. A small task may need only two sentences;
no separate artifact or roster of pre-spawned workers is required.

End with one acceptance request, including any root-switch instruction. Acceptance
covers the proposed route and its stated recovery allowances, not unrelated effects.
If acceptance already exists, reuse it. If a required switch has not occurred, do
not silently execute on another route; resolve that mismatch with the user.

## 3. Execute the accepted plan

Verify the root settings against the accepted route using runtime guidance. Follow
the accepted ownership and assignments; routine dispatch, suitable actor reuse,
and permitted repairs need no renewed approval. Material changes to scope,
ownership, model constraints, or approach outside the accepted route and recovery
allowances require an affected plan revision for acceptance before dependent work.
Preserve unaffected work and counters.

Use [Telemetry](references/telemetry.md) for cheap best-effort start/end capture
when available. Missing telemetry does not delay work unless required accounting
makes it necessary.

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
It owns separate implementation and review limits and their persistence.

If a supplied budget is exhausted or cannot be enforced as required, stop before
further discretionary work, preserve state and report the remaining outcome.
Safe cancellation and custody reconciliation still take precedence over saving
an extra turn. Do not silently exceed a model restriction or premium-use cap.

## 4. Accept the actual result

A feature-delivery run means this workflow owns a feature from its idea or
accepted requirements through completion. Whether the root implements or only
coordinates, once the
requirements and any existing plan are implemented and required checks pass, delegate
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
rather than substitute self-review or claim completion. Bounded fixes and edits
do not acquire this gate merely by being routed; their review remains conditional
on the user's request or a concrete correctness concern.

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

Report the outcome, decisive checks, material limits, and a brief actor/repair
summary. Include measured usage with its scope and cutoff; mention missing usage
only when measurement was requested or its absence affected a decision. Follow
the telemetry reference for interpretation. Omit empty fields and routine narration.

Existing authorization carries across phases, actor changes, and continuation of
the same scoped objective; pass its exact boundaries to the receiver. Ask again
only for a material plan revision, a new effect or scope outside that authority, an exhausted allowance, or
an unresolved consequential decision. Earlier Git or publication approval does
not authorize unrelated future work. Commit, publish, install, or create a new
app task only when the existing authorization covers that action.
