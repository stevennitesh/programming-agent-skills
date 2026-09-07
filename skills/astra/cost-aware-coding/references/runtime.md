# Runtime selection

Inspect the active tools, host and permitted models before promising a route.
Use exact identifiers and supported effort values from that runtime. When
model-specific delegation is selected, pass both explicitly using supported
spawn arguments or a verified custom-agent configuration. Do not invent agent
roles from a draft. Verify effective selection from host metadata when exposed;
a worker's self-description is not verification. If unavailable, report that
limit; when exact routing or a cost cap is required, return route-only rather
than silently falling back to the current parent.

## Context inheritance and model selection

For this Codex collaboration tool, `fork_turns="all"` is a formal full-history
fork: it inherits the parent's model and reasoning effort and disallows explicit
overrides. `fork_turns="none"` or a positive turn count permits explicit model
and reasoning overrides. Confirm the active tool schema before dispatch; this
restriction belongs to the collaboration tool, not the general OpenAI API.

For example, a planner can receive the ten most recent turns plus a focused
assignment while explicitly selecting Astra Medium:

```json
{
  "task_name": "feature_plan",
  "fork_turns": "10",
  "model": "gpt-6-astra",
  "reasoning_effort": "medium",
  "message": "<accepted requirements, relevant findings, open decisions, and expected plan>"
}
```

Ten is an example, not a default. Recent turns can omit earlier decisions or
include unrelated material; supply missing facts in the assignment. Describe
this as a recent-history fork even when it contains all task-relevant context.

Choose context for its purpose:

- Workers: default to a focused packet with requirements, owned scope, relevant
  file pointers, established findings, decisions, acceptance, and useful failed
  approaches. Inherit relevant recent turns when reconstructing those facts would
  cost more or lose meaning. Fresh context does not require repeating discovery;
  verify the dependencies of the change and inspect gaps or drift.
- Planners continuing feature discovery: retain relevant discussion, rationale,
  constraints, and unresolved questions. Use a supported same-task transition or
  a recent-history fork plus assignment when selecting another model/effort.
- Reviewers and independent design challengers: use fresh context with accepted
  requirements, the candidate, relevant evidence, and necessary decisions. Do
  not supply a preferred verdict or require agreement with the author.
  Raising the implementer's effort in the same context remains self-review.
  Review assumptions as well as code; normally return fixes to the implementer
  and recheck affected behavior within the workflow's ownership and repair limits.

Use full history when useful and inherited settings are intended. Account for
context volume and rediscovery together; fresh context is not inherently cheaper.

## Reuse and wait

Keep agent identifiers, roles, observed model/effort, assignments, and status in
working context; no separate artifact is required. Reuse an available agent whose
role, model/effort, and relevant context all fit before spawning another.
Keep useful planners, implementers,
and reviewers available throughout the run where supported; a phase or parent-turn
boundary alone does not justify replacement. Verify availability after interruption
instead of assuming an old identifier still works.

Use the original planner for related design questions, the implementer for repairs,
and the reviewer for rechecking fixes. Matching model/effort alone is insufficient:
do not reuse an author as its independent reviewer. Fresh context is appropriate
for independent judgment, unrelated scope, or misleading/excessive accumulated
context. When replacement is needed, preserve useful findings and writer custody.

Prefer completion notifications or blocking waits using the active tool's documented
behavior. When bounded waits are needed, roughly 30–60 seconds is a starting point,
subject to runtime limits and responsiveness to user input. A wait timeout alone
does not call for a health check. Inspect status after unexpected silence relative
to the assignment, a missed agreed checkpoint, or an error; request a brief blocker
report only when it would inform intervention. Several minutes of silence can be
normal. Do not reread files, poll workers, or request updates just to fill a routine
user progress message. Resume dependent work when the result arrives.

## Runtime verification and transitions

The model policy governs executor selections and substantive direct execution.
An active parent outside its defaults may do necessary routing and custody work.
Retain it for a small direct change only when transfer overhead is unlikely to
pay back and no explicit user ceiling applies; otherwise use a permitted route
or provide exact resume instructions. Do not silently substitute providers or
models when an exact selection is required.

Where custom-agent files are used, inspect their model and effort overrides as
well as spawn arguments and session defaults. Precedence and available controls
can differ by build. Validate the selected route with a harmless probe only when
needed and within the user's task/budget; do not repeat probes on every segment
when the relevant configuration has not changed.

A skill cannot change the current model by declaring a new parent. Direct work
keeps execution with the root; delegation assigns bounded work while the root
retains coordination and acceptance; a handoff transfers coordination ownership
through a supported mechanism after custody is settled. A child cannot promote
itself to a delegating root.

Use a verified parent-transition mechanism within authorization. If unavailable,
retain the parent for coordination and delegate to a permitted executor, or work
directly when policy permits. Give resume instructions only when no authorized
route can continue; an unavailable optional handoff alone is not a blocker. Creating
a separate app task requires an explicit request for that task.

Before transferring ownership, use [continuation guidance](continuation.md).
On routing failure, preserve active ownership and partial work. Stop actors only
when their authority, restrictions, or ownership are affected; continue unaffected
authorized work. Reconcile writer state before reassignment: a failed dispatch
does not stop existing processes.

Installation is separate from execution. Only when requested, configure the
actual host that runs the task. Prefer scoped profiles or explicit dispatch
settings over changing global subagent defaults for one workflow. Runtime limits
can enforce concurrency; prompt instructions alone do not enforce spending or
prevent every child effect.

Official starting references, verified 2026-09-06; recheck when configuring a
new host/build or when behavior conflicts with the documentation:

- [Subagents and custom-agent precedence](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
