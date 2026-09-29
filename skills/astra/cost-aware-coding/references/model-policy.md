# GPT-6 model policy

Use this policy for cost-aware routing within the GPT-6 family. Model and reasoning
effort are part of the token-efficiency strategy.

## Default roles

| Role | Default route | Use when |
| --- | --- | --- |
| Lead | **Astra Medium or XHigh** | Consequential reasoning, shaping, ambiguous decisions, orchestration, exception handling, and final review; choose effort by reasoning intensity |
| Implementer | **Sol High** | Substantial repository investigation, coding, debugging, verification, and repair |
| Bounded worker | **Luna Max** | Fine-grained edits, extraction, classification, targeted inspection, or other compact tasks with clear inputs and cheap verification |

These are default economic roles, not universal quality rankings. Preserve an
explicit user-selected route when it is available and compatible with the task.

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

Use **Sol High** for every Sol assignment. Choose **Astra Medium** for ordinary
lead work and **Astra XHigh** when intensive reasoning can materially change a
consequential decision or final review. The lead may start at either effort.

For a demonstrated implementation-reasoning failure, escalate
**Sol High → Astra Medium → Astra XHigh** as evidence warrants. Transfer custody
before Astra takes over implementation. The implementation escalation route is
separate from the lead's selected effort.

These are the allowed efforts in this policy: Sol High, Astra Medium or XHigh,
and Luna Max. Reserve **Max exclusively for Luna**; do not use other Sol or Astra
efforts. Do not spend stronger-model tokens on missing requirements, broken
environments, permissions, or invalid acceptance.

Luna has no effort ladder in this policy: bounded Luna work uses **Luna Max**.
If the assignment outgrows a compact bounded contract, move it to Sol High.

Prefer the least expensive route that reliably meets acceptance after accounting
for briefing, supervision, correction, and review churn—not token price in
isolation.

Availability and supported effort controls are host-dependent. If a requested
route is unavailable, use a supported route within these allowed efforts that
preserves the role boundaries and report the substitution when it materially
affects the user's cost or quality intent. If none is suitable, surface the
unavailable route rather than silently selecting an excluded effort.
