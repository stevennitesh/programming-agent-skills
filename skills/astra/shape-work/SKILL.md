---
name: shape-work
description: Clarify an underspecified change into settled behavior, constraints, and acceptance, or explicitly reconcile project domain meaning and accepted decisions. Exclude straightforward implementation, routine lookup, and ticket decomposition.
---

# Shape work

Resolve consequential ambiguity so implementation does not invent product policy
or accepted meaning. Use conversation, evidence, and a durable specification only
when useful. Shaping alone does not authorize implementation.

Shaping is complete when implementation can proceed without inventing a
consequential product, scope, risk, or domain decision.

For a direct request to clarify domain meaning or capture a settled domain
decision, use [Domain modeling](references/domain-modeling.md) without a feature
interview.

## 1. Recover settled intent

Establish the requested outcome, relevant purpose, settled decisions, and
constraints that can change the result. Use the supplied conversation, brief,
issue, audit finding, repository contract, and other decision-bearing sources.

Distinguish accepted requirements and project meaning from current implementation
facts, recommendations, assumptions, and deferred choices. Do not reopen a settled
choice merely to run a complete interview. Revisit it only when new evidence
creates a material conflict.

Look up accessible facts instead of asking the user to retrieve them. When a
proposed solution depends on an existing capability, inspect enough of its actual
behavior to know whether it can satisfy the intended outcome. Surface a
contradiction when it would change an accepted commitment.

## 2. Resolve only consequential uncertainty

Separate the required outcome from a proposed mechanism. When the mechanism is
not settled, check whether an existing capability or materially smaller approach
satisfies the outcome. Compare alternatives only when a real tradeoff remains;
do not manufacture options to complete a process.

Resolve ordinary technical choices within the settled requirements. Ask the user
or another decision owner only for unresolved choices that materially change
accepted behavior, product priority, scope, risk tolerance, constraints, or
domain meaning. Group independent questions when that reduces unnecessary turns;
do not ask dependent questions before their prerequisites are settled. Continue
useful independent work while an answer is pending.

Use a distinguishing scenario when abstract wording could conceal materially
different outcomes. Explain a recommendation and its decisive tradeoff when useful;
do not invent an owner-held answer.

When shaping changes or exposes a conflict in domain terms, invariants,
responsibilities, or relationships, read
[Domain modeling](references/domain-modeling.md) before building decisions that
depend on that meaning.

Use [codebase-design](../codebase-design/SKILL.md) when the unresolved choice is
primarily architecture, integration, ownership, interface, or migration design.
Use [prototype](../prototype/SKILL.md) when a new observation is needed to decide.
Keep a conclusion conditional when decisive evidence or authority is unavailable.

## 3. Make behavior and acceptance discriminating

Describe representative behavior from input or trigger to observable outcome when
doing so removes consequential ambiguity. Include materially different rejection,
partial-success, state, or completion behavior only when it changes the contract.

State what must remain true and what evidence could distinguish the intended
result from a plausible consequentially wrong result. Avoid implementation
recipes unless a mechanism is itself an accepted constraint.

Before adding a safeguard to acceptance, identify the realistic wrong result or
broken workflow it prevents. Preserve explicit commitments while keeping proposed
mechanisms and optional hardening distinct from required behavior. Writing a
mechanism into a plan or specification does not make it accepted.

If two reasonable implementations could satisfy the wording while producing
materially different outcomes, resolve the unintended ambiguity or keep the
remaining owner-held decision explicit. Preserve implementation freedom where the
accepted behavior does not require a specific mechanism.

For cross-boundary results, durable state, conflicting rules, measured claims, or
competing completion criteria, read
[Acceptance meaning](references/acceptance-meaning.md).

## 4. Capture only what future work needs

Keep a small settled outcome in the conversation when that is sufficient. Persist
the result when requested or when future sessions, implementers, or decision
owners would otherwise need to rediscover consequential decisions.

When a specification or domain update is useful, read
[Durable decisions](references/durable-decisions.md). Reuse the existing owner of a
decision instead of creating competing current documents. Include only what future
work needs to preserve the contract: intended outcome, relevant scope and
constraints, settled behavior, acceptance, and material uncertainty. Preserve
rationale when it can change later decisions.

If the durable update replaces or retires a competing current document, read
[Document reconciliation](references/document-reconciliation.md). If accepted
meaning must change while tickets, workers, or delivery proof already depend on
it, read
[Active delivery revisions](references/active-delivery-revisions.md).

## 5. Finish or continue within existing authority

Do not call work ready when implementation would still need to invent
consequential policy or accepted meaning. If shaping is blocked, return the exact
decision or evidence still needed and its impact.

Once the behavior is sufficiently settled, continue implementation only when it
was already authorized and within the active workflow's ownership boundaries.
Ticketing is separate and optional; use [to-tickets](../to-tickets/SKILL.md) only
when requested or required by an active workflow.

A specification, plan, or ticket does not itself authorize implementation,
delegation, publication, or external effects.
