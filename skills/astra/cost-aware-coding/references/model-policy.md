# GPT-6 model policy

Use this policy for cost-aware routing within the GPT-6 family. Model and reasoning
effort are part of the token-efficiency strategy.

## Default roles

| Role | Default route | Use when |
| --- | --- | --- |
| Lead | **User-selected starting model and effort** | Consequential reasoning, shaping, ambiguous decisions, orchestration, exception handling, and final acceptance |
| Implementer | **Sol High** | Substantial repository investigation, coding, debugging, verification, and repair |
| Bounded worker | **Luna Max** | Fine-grained edits, extraction, classification, targeted inspection, or other compact tasks with clear inputs and cheap verification |
| Optional isolated reviewer | **Astra Medium or XHigh** | Read-only candidate review when fresh context materially helps; choose effort by review difficulty |

These are default economic roles, not universal quality rankings. Preserve an
explicit user-selected route when it is available and compatible with the task.

The user starts the work with the lead. Do not select, replace, or change the
lead's model or effort. The routes and escalation below govern subagents, not the
active lead session.

## Route by ambiguity and verification burden

Keep Astra on lead-owned decisions rather than implementation throughput.

Use Sol instead of Luna Max when the task requires substantial repository
reasoning, long debugging context, nontrivial implementation judgment, or
verification whose failure would be expensive to reconstruct.

Use Luna Max when the assignment can remain compact and the result is cheap to
judge. Luna Max intentionally buys the strongest Luna reasoning for bounded work;
do not spend Astra tokens trying to save marginal Luna effort.

A cheap worker is not a cheap workflow when Astra must write a large brief,
reconstruct missing context, deeply verify intermediate work, or repeatedly repair
the result. Do not split one coherent Sol assignment into many Luna tasks merely
because Luna tokens are inexpensive.

If Astra cannot remain mostly dormant during worker implementation, reconsider
the route: enlarge the worker's ownership, move a pseudo-bounded Luna task to Sol,
or keep the task direct when handoff overhead dominates.

## Effort escalation

Use **Sol High** for every Sol assignment. For an optional isolated reviewer,
choose **Astra Medium** by default and **Astra XHigh** when intensive reasoning
can materially change the review conclusion.

For a demonstrated implementation-reasoning failure, escalate
**Sol High → Astra Medium → Astra XHigh** as evidence warrants. Transfer custody
before an Astra subagent takes over implementation. This escalation does not
change the lead's model or effort.

These are the allowed subagent efforts: Sol High, Astra Medium or XHigh,
and Luna Max. Reserve **Max exclusively for Luna**; do not use other Sol or Astra
efforts. Do not spend stronger-model tokens on missing requirements, broken
environments, permissions, or invalid acceptance.

Luna has no effort ladder in this policy: bounded Luna work uses **Luna Max**.
If the assignment outgrows a compact bounded contract, move it to Sol High.

Prefer the least expensive route that reliably meets acceptance after accounting
for briefing, supervision, correction, and review churn—not token price in
isolation.

Availability and supported effort controls are host-dependent. If a requested
subagent route is unavailable, use a supported route within these allowed efforts that
preserves the role boundaries and report the substitution when it materially
affects the user's cost or quality intent. If none is suitable, surface the
unavailable route rather than silently selecting an excluded effort.
