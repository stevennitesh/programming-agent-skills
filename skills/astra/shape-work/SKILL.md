---
name: shape-work
description: Develop an idea into an agreed specification, or reconcile domain meaning and durable decisions. Exclude architecture selection, routine implementation, and general context cleanup.
---

# Shape work

Work with the user to develop and challenge an idea until its consequential goals,
scope, behavior, and acceptance are aligned. Choose the brainstorming, interview,
investigation, and specification methods suited to the task. Preserve freedom over
implementation wherever the accepted outcome allows it.

For a direct domain clarification or settled decision capture, including an ADR,
use [Domain meaning and decision records](references/domain-modeling.md) without
requiring a feature interview.

## Develop and challenge the idea

Recover the purpose, existing decisions, constraints, and relevant facts from the
conversation and available sources. Distinguish accepted requirements from current
behavior, recommendations, and assumptions. Look up accessible facts rather than
asking the user to retrieve them. Reopen a settled choice when new evidence creates
a material conflict, not to complete an interview.

Actively surface missing workflows, weak assumptions, conflicting priorities, and
consequential tradeoffs. Explore useful possibilities and recommend simpler or
stronger alternatives when warranted. Goals, intended users, features, exclusions,
important details, and success criteria are prompts for judgment, not a mandatory
questionnaire. Keep new ideas as proposals until their inclusion is settled.

Choose question order, grouping, depth, and examples for the uncertainty and the
user's preferred pace. Ask about decisions that materially change the result;
resolve routine technical choices within the accepted scope. Explain a useful
recommendation and its decisive tradeoff instead of handing every choice back to
the user. Respect dependencies between questions and continue independent work
while an answer is pending.

Reflect consequential interpretations back while they can still be corrected.
Use concrete scenarios to expose differences hidden by abstract agreement. Do not
treat an unanswered proposal as accepted or require approval after every section.

Use [Long-horizon shaping](references/long-horizon-shaping.md) when the discussion
needs continuity across many dependent decisions or sessions. Use
[codebase-design](../codebase-design/SKILL.md) for a consequential unresolved
architecture, interface, ownership, or migration decision, and
[prototype](../prototype/SKILL.md) when a new observation is needed to decide.
Keep conclusions conditional when decisive evidence or authority is unavailable.

## Make agreement usable

Describe behavior and acceptance precisely enough that reasonable implementations
cannot produce materially different outcomes the user did not intend. Preserve
what must remain true and identify evidence that distinguishes success from a
plausible consequential failure. Include rejection, partial success, state, or
completion details where they change the contract.

Keep proposed mechanisms and optional hardening distinct from required behavior.
A safeguard should address a realistic wrong result or broken workflow; recording
a mechanism does not make it accepted. Leave implementation details open unless
they are themselves constraints. For cross-boundary results, persisted state,
conflicting rules, measured claims, or competing completion criteria, read
[Acceptance meaning](references/acceptance-meaning.md).

When a specification is requested, produce the specification. A small clarification
can remain in conversation; persist other decisions when future work would
otherwise need to rediscover them. Read [Durable decisions](references/durable-decisions.md)
for a specification or other durable record. Choose a useful format and preserve
the distinction between agreed behavior, recommendations, and unresolved choices.

Shaping can settle priorities, product stages, and meaningful dependencies, and
include a useful delivery outline. The execution lead owns the adaptable
implementation plan, assignments, checkpoints, and review; cost-aware-coding
organizes these when selected. Ordinary planning needs no additional skill phase.

## Keep affected decisions coherent

Use [Domain meaning and decision records](references/domain-modeling.md) when
terms, invariants, relationships, or durable decision rationale need clarification
or capture. Reconcile the current specs, domain records, ADRs, and guidance affected
by the decisions being settled. Use
[Document reconciliation](references/document-reconciliation.md) for conflicts or
replacement of current sources. General repository context maintenance belongs to
[context-hygiene](../context-hygiene/SKILL.md); shaping does not require a wider audit.

When accepted meaning changes while tickets, workers, or proof depend on it, use
[Active delivery revisions](references/active-delivery-revisions.md).

## Finish within the requested scope

Shaping is complete when the requested specification or decision record is
delivered, affected current guidance is coherent, and implementation need not
invent consequential product policy or domain meaning. For a discussion-only
request, an agreed understanding is sufficient. If unresolved decisions prevent
readiness, identify them and their impact; a useful draft can remain explicitly
unsettled.

Continue into implementation when it was already authorized and the active
workflow permits it. Ticket decomposition belongs to
[to-tickets](../to-tickets/SKILL.md) when requested or required by that workflow.
Creating a spec or decision record does not itself authorize implementation,
delegation, publication, or external effects.
