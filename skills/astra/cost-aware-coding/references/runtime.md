# Runtime selection

Inspect the active tools, host and permitted models before promising a route.
Use exact identifiers and supported effort values from that runtime. When
model-specific delegation is selected, pass both explicitly using supported
spawn arguments or a verified custom-agent configuration. Do not invent agent
roles. Verify effective selection from host metadata when exposed. If unavailable,
report that limit; when exact routing or a cost cap is required, return a coordination proposal rather
than silently falling back to the current parent.

For the current root, prefer host-provided turn metadata. If absent, use the
bounded [telemetry lookup](telemetry.md) for the identified session's latest
observed model and effort. Treat them as current only when the record
matches the active turn; an older record does not establish current settings.
Configuration defaults and self-description do not establish
current settings; per-turn overrides and rerouting may differ. Record unknowns,
and refresh after a model transition rather than guessing from task difficulty.

## Context inheritance and model selection

For Codex collaboration, confirm the active schema and select the fork mode:

| `fork_turns` | Context and settings |
| --- | --- |
| `"all"` | Full history; inherits parent model/effort, with no explicit overrides |
| `"none"` | Assignment only; permits explicit model/effort |
| Positive turn count | Recent history plus assignment; permits explicit model/effort |

This restriction belongs to the collaboration tool, not the general OpenAI API.
Choose recent turns for relevance and supply omitted decisions in the assignment;
receiving all relevant facts does not make it a formal full-history fork.

Before a worker starts, supply the accepted outcome, constraints, owned scope,
required inputs, acceptance evidence, prohibited effects, and escalation triggers.
Include applicable repository instructions and task-relevant references; a worker
may not see the parent's loaded skills. Do not load the whole custom pack.

Choose context for its purpose:

- Workers: add file pointers, findings, decisions, and useful failed approaches.
  Inherit relevant turns when reconstructing them would cost more or lose meaning;
  inspect dependencies, gaps, and drift rather than repeating discovery.
- Planners: retain relevant discussion, rationale, constraints, and open questions.
  Use the fork rules above when selecting different model/effort settings.
- Reviewers and design challengers: use fresh context with accepted requirements,
  candidate, evidence, and necessary decisions; do not supply a preferred verdict.
  Challenge assumptions as well as code. Increasing an author's effort in the same
  context remains self-review. Repairs and follow-up reviews follow the workflow's ownership
  and repair limits.

Use full history when useful and inherited settings are intended. Account for
context volume and rediscovery together; fresh context is not inherently cheaper.

## Reuse and wait

Count the root in the working roster. Keep actor IDs, roles, logged model/effort,
owned scope, status, and dispatch reasons in existing run context; no separate
ledger is required. Default to one reusable non-independent actor per needed
model/effort, created only when needed. Required independence, useful concurrency,
unavailable actors, or unsuitable accumulated context can justify additional actors.
A coordination-only root does not fill implementation capacity; reuse one suitable
worker even when its settings match the root. Settings alone do not establish
suitability. Recheck availability after interruption.

Reuse the planner for related decisions, the implementer for repairs, and the
reviewer for follow-up reviews. A specialist may investigate and implement related work
once write authority and custody transfer; keep its context rather than commissioning
an equivalent worker. A reviewer must be independent of the candidate's authors,
including specialists whose design assumptions the review must challenge.
Preserve useful actors across phases and parent turns; follow continuation
guidance before replacement.

Prefer completion notifications or blocking waits using the active tool's documented
behavior. When bounded waits are needed, roughly 30–60 seconds is a starting point,
subject to runtime limits and responsiveness to user input. A wait timeout alone
does not call for a health check. Inspect status after unexpected silence relative
to the assignment, a missed agreed checkpoint, or an error; request a brief blocker
report only when it would inform intervention. Several minutes of silence can be
normal. Do not reread files, poll workers, or request updates just to fill a routine
user progress message. Resume dependent work when the result arrives.

## When the root is outside the model policy

The model policy governs executor selections and substantive direct execution.
An active parent outside its defaults may do necessary routing and custody work.
For planned root implementation, retain it for a small change only when transfer overhead is unlikely to
pay back and no explicit user ceiling applies; otherwise use a permitted route
or provide exact resume instructions. Do not silently substitute providers or
models when an exact selection is required.

## When configuring custom agents

Inspect their model/effort overrides, spawn arguments and session defaults. Precedence and available controls
can differ by build. Validate the selected route with a harmless probe only when
needed and within the user's task/budget; do not repeat probes on every segment
when the relevant configuration has not changed.

## When the accepted plan changes the root

Prefer a user-applied model/effort change in the same conversation at a completed
turn boundary. This changes the root settings, not the task or accepted ownership.
Preserve the accepted plan, active actor identities, custody, and repair counters;
verify current settings before execution. A user acceptance is not proof of a switch.

A separate coordination handoff is only for an explicitly requested transfer or
a concrete runtime/task constraint; use continuation guidance. It transfers
coordination ownership after custody is settled.
A skill cannot change the current model by declaration, and a child cannot
promote itself to a delegating root.

For a separate handoff, use a verified transition mechanism within authorization. If unavailable,
retain the parent for coordination and delegate to a permitted executor, or work
directly when accepted implementation ownership and model policy permit. Do not
replace a required root switch with an unaccepted route. Give resume instructions only when no authorized
route can continue; an unavailable optional handoff alone is not a blocker. Creating
a separate app task requires an explicit request for that task.

Before transferring ownership, use [continuation guidance](continuation.md).

## When routing fails

Preserve active ownership and partial work. Stop actors only
when their authority, restrictions, or ownership are affected; continue unaffected
authorized work. Reconcile writer state before reassignment: a failed dispatch
does not stop existing processes.

## When host setup is requested

Configure the actual host that runs the task. Prefer scoped profiles or explicit dispatch
settings over changing global subagent defaults for one workflow. Runtime limits
can enforce concurrency; prompt instructions alone do not enforce spending or
prevent every child effect.

Official starting references, verified 2026-09-06; recheck when configuring a
new host/build or when behavior conflicts with the documentation:

- [Subagents and custom-agent precedence](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
