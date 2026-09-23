# GPT-6 model policy

Use this policy for cost-aware routing within the GPT-6 family. Model and reasoning
effort are part of the token-efficiency strategy.

## Default roles

| Role | Default route | Use when |
| --- | --- | --- |
| Lead | **Astra Medium** | Consequential reasoning, shaping, ambiguous decisions, orchestration, exception handling, and final review |
| Implementer | **Sol Medium** | Substantial repository investigation, coding, debugging, verification, and repair |
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

Start with Astra Medium, Sol Medium, and Luna Max.

For a difficult consequential lead decision or final review, escalate Astra
**Medium → High → XHigh → Max** only when additional reasoning can materially
change the decision. Do not use Astra Ultra inside this serial route: in Codex,
Ultra changes multi-agent behavior by enabling proactive delegation rather than
serving as a simple next reasoning tier.

For implementation or debugging that remains implementation-shaped, escalate
**Sol Medium → Sol High → Sol Max** only as evidence warrants before pulling the
work into Astra. Do not spend stronger-model tokens on missing requirements,
broken environments, permissions, or invalid acceptance.

Luna has no effort ladder in this policy: bounded Luna work uses **Luna Max**.
If the assignment outgrows a compact bounded contract, move it to Sol.

Prefer the least expensive route that reliably meets acceptance after accounting
for briefing, supervision, correction, and review churn—not token price in
isolation.

Availability and supported effort controls are host-dependent. If a requested
route is unavailable, use the closest supported route that preserves these role
boundaries and report the substitution when it materially affects the user's cost
or quality intent.
