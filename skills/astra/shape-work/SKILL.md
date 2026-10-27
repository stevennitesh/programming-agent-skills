---
name: shape-work
description: Develop an idea into an agreed specification, or reconcile domain meaning and durable decisions. Exclude architecture selection, routine implementation, and general context cleanup.
---

# Shape work

Work with the user to settle the goals, scope, behavior, and acceptance that
implementation must preserve. Challenge the idea and recommend simpler or stronger
alternatives when useful. Keep implementation methods open within accepted
constraints. Direct domain clarification or settled ADR capture uses
[Domain meaning and decision records](references/domain-modeling.md), without
another feature interview.

## Resolve consequential uncertainty

Reuse settled decisions. Choose questions, scenarios, investigation, and pacing
for what can change the result; no questionnaire or approval after every section
is required. Reflect consequential interpretations while they can be corrected.
An unanswered proposal is not acceptance. Resolve routine technical choices
within scope and continue independent work while a decision is pending.

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

Deliver a specification when requested; a small clarification may remain in chat.
Use [Durable decisions](references/durable-decisions.md) when future work needs a
specification or other record. Preserve accepted choices, recommendations,
assumptions, and unknowns as distinct states.

Reconcile affected specs, domain records, decisions, and guidance through
[Document reconciliation](references/document-reconciliation.md). Broader repository
context maintenance belongs to [context-hygiene](../context-hygiene/SKILL.md).
If tickets, workers, or proof depend on meaning being revised, use
[Active delivery revisions](references/active-delivery-revisions.md).

## Return the settled outcome

Finish when the requested artifact or discussion result is usable without
inventing consequential product or domain policy, and affected current guidance
is coherent. Label a useful but unsettled draft and its remaining decisions.

Accepted product stages may constrain delivery; the execution lead owns adaptable
implementation sequencing, assignments, and review. Ordinary planning needs no
extra skill. Use [ticketing](../ticketing/SKILL.md) for requested decomposition,
not as a mandatory next stage. Continue implementation only when already authorized;
shaping grants no new implementation, delegation, publication, or external authority.
