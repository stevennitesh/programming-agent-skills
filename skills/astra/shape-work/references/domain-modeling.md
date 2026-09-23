# Domain modeling and settled-decision capture

Use for a direct request to clarify or reconcile project meaning, or when shaping
exposes a durable domain distinction. This path does not require a feature spec,
ticket graph, or implementation.

## Locate meaning and authority

Read the relevant repository domain route, current context records, accepted
decisions, and supplied source. A missing preferred record is not a setup failure.

Identify the distinction and its decision owner. Code, tests, and widespread usage
show current behavior, not automatically intended meaning. Honor sources explicitly
designated as governing. When implementation and accepted meaning disagree, do not
rewrite the definition merely to excuse the code.

For already-settled input, proceed without reopening the decision. Ask only about
a consequential unresolved meaning or contradiction.

## Model distinctions that affect behavior

Record project-specific meaning, defining behavior, invariants, responsibilities,
and relationships whose omission would make future work guess. Use concrete
inclusion, exclusion, transition, or failure scenarios when a term is overloaded.

Use one canonical term within a context. Preserve independent meanings across
contexts unless an accepted shared model joins them. Context boundaries follow
meaning, responsibility, and consistency requirements rather than directory or
service layout.

Make invariants and valid transitions precise enough for design and implementation
to preserve them. A small state table or schema can express meaning better than
prose. Implementation structure belongs to design or implementation; the domain
record states what must remain true.

## Reconcile the current owner

Capture only non-obvious durable meaning future work would likely misapply. Prefer
updating, replacing, merging, relocating, or removing an existing definition over
adding a parallel one.

Keep commands, executable procedure, active work state, inventories, and historical
rationale with their own owners. If changed meaning affects current acceptance or
other active references, identify those consequences rather than leaving
contradictory current truth.

Follow the repository's configured format. Without one, a short record containing
the context, canonical terms with defining behavior, and relevant invariants is
enough. Create files and context maps only when real content needs them.

## Record rationale when it will matter later

Use an ADR when the rationale behind a settled consequential decision is likely to
matter in future work, such as a meaningful tradeoff or a choice costly to reverse.
Ordinary terminology, obvious choices, unresolved proposals, and routine
implementation details do not require one.

Reconcile an existing decision instead of duplicating it. Preserve predecessor
history and make current applicability clear when a decision is superseded or
partially replaced. Follow repository ADR conventions.

For persistence mechanics and publication authority, use
[Durable decisions](durable-decisions.md). If the change replaces a competing
current document, use [Document reconciliation](document-reconciliation.md). If
active tickets or workers already depend on the accepted meaning, use
[Active delivery revisions](active-delivery-revisions.md).

## Return the domain result

Within authorized persistence scope, apply the bounded reconciliation. Otherwise
return the settled distinction, proposed owner, and any unresolved meaning or
downstream consequence.

A domain-only request ends here. During broader shaping, return the resolved
meaning to that work and continue only within existing authority.
