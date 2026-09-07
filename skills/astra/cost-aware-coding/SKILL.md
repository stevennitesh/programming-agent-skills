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
Shape-work owns feature design and implementation planning. When revising or
planning the feature approach, use
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
order. Choose implementation ownership:

- **Root implements:** coherent work fits the root's model/effort and benefits from
  shared context. Bounded read-only specialists and independent review can assist
  without changing this ownership. Schema, API, UI, and tests can be one assignment.
- **Root coordinates:** managing dependencies, integration, or competing work units
  warrants dedicated coordination. Size, step count, or specialist assistance alone
  does not establish this need. The root plans, coordinates, integrates,
  and accepts; delegate product implementation and repairs. One reusable worker
  may execute several sequential units. Keep root integration to landing and
  verification; return product-code corrections to their implementer.

Coordination protects the root's attention; it is not automatically cheaper.
For root implementation, retain sufficient permitted work at the root unless a cheaper
actor is likely to repay transfer and coordination costs over the remaining work.
Reuse a suitable actor before spawning. Record each delegation's benefit in the
proposal, or its assignment if not previously planned; reassess only when
circumstances change. Capability, independence, useful concurrency, sufficient
savings, or dedicated coordination can justify delegation when direct work or
an existing actor cannot supply the benefit. Phases, role labels, file count,
and repository boundaries alone cannot. No separate ledger or table is required.

Planning permits justified read-only specialists and isolated scratch checks,
but no product implementation or execution-worker pre-spawning before acceptance.
Only the root delegates; workers must not delegate. During execution, default to one write-capable
actor at a time, including the parent. Up to two independent read-only children
may run when useful. They may use isolated scratch checks, but must not mutate
the reviewed candidate or shared product state.

Read [Runtime selection](references/runtime.md) once when establishing the route;
reuse it until the runtime, route, or relevant configuration changes. Retain a
sufficient root; include any justified model/effort switch in the proposal.

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

End with one acceptance request and, if needed, ask the user to switch this
conversation's root model/effort before execution. Reuse existing acceptance; it
covers the proposed route and recovery allowances, not unrelated effects.

## 3. Execute the accepted plan

Verify root settings against the accepted route using runtime guidance; resolve
a missing required switch rather than silently substituting a route. Follow
the accepted ownership and assignments; routine dispatch, suitable actor reuse,
and permitted repairs need no renewed approval. Material changes to scope,
ownership, model constraints, or approach outside the accepted route and recovery
allowances require an affected plan revision for acceptance before dependent work.
Preserve unaffected work and counters.

Use [Telemetry](references/telemetry.md) for cheap best-effort start/end capture
when available. Missing telemetry does not delay work unless required accounting
makes it necessary.

Use the runtime guidance for worker packets, context selection, actor reuse,
and waits. Workers implement directly under the engineering contract.

After dispatch, work only on useful independent responsibilities or wait for the
return. Do not duplicate its assigned investigation while it runs. If a concrete
gap requires intervention, coordinate with the worker rather than silently doing
the same work again.

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
coordinates, once the requirements and any existing plan are implemented and
required checks pass, delegate
[change review](../change-review/SKILL.md) before declaring
completion. Use an independent Astra Medium child even when the root is Astra
Medium and did not implement. Astra XHigh requires explicit selection; it does
not activate high-assurance review, which remains a separate user choice.
Supply the accepted requirements/plan, candidate and proof; request a gate decision
that challenges plan assumptions as well as code. Change-review owns inspection,
finding standards, and rules for residual-risk acceptance. Hold the candidate
stable under its custody rules until review returns. Resolve required corrections
and any residual-risk acceptance with its authorized owner before completion;
a review verdict does not grant that authority.

If review requires corrections, read [Repair allowances](references/repairs.md)
before dispatching repairs. If independent review cannot run, report the unmet gate
rather than substitute self-review or claim completion. Bounded fixes and edits
do not acquire this gate merely by being routed; their review remains conditional
on the user's request or a concrete correctness concern.

The root verifies decisive evidence for the final candidate, including additions,
deletions, untracked changes, material interactions, and requirements omitted from
worker packets. A worker's PASS is a claim to verify. Reuse valid evidence under
the engineering contract and repository checks; investigate concrete gaps,
contradictions, drift, or required assurance without repeating the worker's
investigation or the delegated diff review. Independent review supplements
executable proof.

## 5. Finish with evidence and limits

Report the outcome, decisive checks, material limits, and a brief actor/repair
summary. Include measured usage with its scope and cutoff; mention missing usage
only when measurement was requested or its absence affected a decision. Follow
the telemetry reference for interpretation. Omit empty fields and routine narration.

Authorization carries across phases, actors, and continuation of the same scoped
objective; pass its boundaries to the receiver. It does not cover unrelated future
work. Commit, publish, install, or create a new app task only when authorized.
