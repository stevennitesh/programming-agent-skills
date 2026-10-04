# Domain meaning and decision records

Use for a direct domain clarification, reconciliation of accepted meaning, or
capture of a settled decision, including a technical ADR. This branch needs no
feature interview, specification, ticket graph, or implementation.

## Establish the meaning or decision

Read the relevant domain route, accepted decisions, supplied design, and other
sources that govern the question. Code and tests show current behavior, not
automatically intended meaning. Do not redefine the domain merely to excuse an
implementation conflict.

For settled input, capture it without reopening the choice. Ask only about a
consequential unresolved meaning or contradiction. If the technical choice itself
is unresolved, use [codebase-design](../../codebase-design/SKILL.md); recording its
settled result does not require repeating that analysis.

## Model distinctions that affect behavior

Keep the project language, defining behavior, invariants, responsibilities, and
relationships future agents would otherwise misapply. Concrete inclusion,
exclusion, transition, or failure scenarios can clarify an overloaded term.

Use consistent terms within a context, preserving independent meanings across
contexts unless an accepted shared model joins them. Context boundaries follow
meaning and responsibility rather than directory or service layout. Use a state
table, schema, diagram, or prose when it makes the consequential distinction clear;
no modeling framework or context map is required.

Prefer updating an existing definition over adding a parallel one. Keep commands,
execution state, and decision history at their own owners. Make relevant invariants
and valid transitions clear enough to preserve without prescribing implementation
structure unless that structure is an accepted constraint.

## Record consequential rationale

Use an ADR when a settled consequential choice and its rationale will matter to
future work, such as a meaningful tradeoff or a decision costly to reverse.
Routine implementation details and ordinary terminology need no ADR.

Capture the context, decision, decisive rationale, consequences, and applicability
at the level the repository needs. Include alternatives when they explain the
choice; do not manufacture an option comparison. Distinguish proposals from
accepted decisions using repository conventions.

Reconcile an existing record rather than duplicating it. Preserve predecessor
rationale and make current applicability, partial replacement, or supersession
clear. A decision record can preserve an accepted technical constraint without
making every incidental implementation detail permanent.

## Reconcile and return

Use [Durable decisions](durable-decisions.md) for persistence and
[Document reconciliation](document-reconciliation.md) for conflicts or displaced
current sources. Changed definitions or decisions should not leave contradictory
acceptance or guidance. If active work depends on the old meaning, use
[Active delivery revisions](active-delivery-revisions.md).

Apply the requested local update within authority. For an analysis-only request,
return the resolved distinction or recommendation, proposed owner, and remaining
uncertainty. A domain or ADR request can finish here; broader shaping can reuse the
result without another interview.
