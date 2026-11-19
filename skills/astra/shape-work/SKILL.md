---
name: shape-work
description: Explore an idea with the user, shape it into an agreed specification, or reconcile domain meaning and durable decisions. Exclude architecture selection, routine implementation, and general context cleanup.
---

# Shape work

Build a shared understanding of the goal, scope, intended behavior, and what
would count as success. Keep implementation methods open within accepted
constraints. For direct domain clarification or settled ADR capture, use
[Domain meaning and decision records](references/domain-modeling.md).

## Resolve consequential uncertainty

Use the request and relevant sources to form a working understanding. Reuse
settled decisions and briefly reflect the goal, constraints, and any assumption
that could materially change the outcome. Surface changes in that understanding
while the user can still correct them. When a request starts with a proposed
solution, check whether a simpler or better approach would meet the same goal.

Help the user weigh choices that affect the result. Explain the practical
consequence, give a recommendation when supported, and choose questions,
examples, or investigation as useful. For example, “I’d keep valid rows and
report rejected rows individually so users can fix and retry those rows.
Do you need the whole file to succeed or fail together?”

Treat unanswered proposals as open. Resolve routine technical choices within
scope and continue independent work while a user decision is pending.

Use [Long-horizon shaping](references/long-horizon-shaping.md) when many dependent
decisions or sessions need continuity. Use [codebase-design](../codebase-design/SKILL.md)
for unresolved technical ownership, interfaces, or migration, and
[prototype](../prototype/SKILL.md) when a new observation must settle the question.
Keep conclusions conditional when decisive evidence or authority is missing.

## Make agreement usable

State behavior and acceptance precisely enough to distinguish the intended result
from a plausible consequential failure. Include rejection, partial success,
state, or completion details when they change the contract. Separate requirements
from suggested mechanisms and optional hardening. For cross-boundary results,
persisted meaning, measured claims, or competing completion criteria, read
[Acceptance meaning](references/acceptance-meaning.md).

Deliver a specification when requested.
Use [Durable decisions](references/durable-decisions.md) when future work needs a
specification or other record. Preserve accepted choices, recommendations,
assumptions, and unknowns as distinct states.

Reconcile affected specs, domain records, decisions, and guidance through
[Document reconciliation](references/document-reconciliation.md). Broader repository
context maintenance belongs to [context-hygiene](../context-hygiene/SKILL.md).
If tickets, workers, or proof depend on meaning being revised, use
[Active delivery revisions](references/active-delivery-revisions.md).

## Close the discussion

For exploration, return the meaningful options, any recommendation, and remaining
uncertainty. For an agreed direction, recap the settled scope and observable
success, and identify any open choice that could change implementation. A short
chat recap can be enough. A usable agreement lets implementation proceed without
inventing consequential product or domain policy. Label unsettled drafts and their
remaining decisions.

Accepted product stages may constrain delivery; the execution lead owns adaptable
implementation sequencing, assignments, and review. Ordinary planning needs no
extra skill. Use [ticketing](../ticketing/SKILL.md) for requested decomposition,
not as a mandatory next stage. Continue implementation only when already authorized;
shaping grants no new implementation, delegation, publication, or external authority.
