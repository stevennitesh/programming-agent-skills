# Domain modeling and settled-decision capture

Use for a direct request to clarify or reconcile project meaning, or when shaping
exposes a durable domain distinction. This path does not require a feature spec,
ticket graph, or implementation. For persistent writes, also read the publication
section of [Durable decisions](durable-decisions.md).

## Locate the meaning and its authority

Read the relevant repository domain route, current context records, accepted
decisions, and the supplied source. Follow existing destinations and formats.
A missing record is not a setup failure; do not require bootstrap merely because
the first useful domain record has not been written. A configured route change
is separate from recording content under that route.

Identify the distinction and its decision owner. Code, tests, and widespread usage
show current behavior, not automatically intended meaning. Honor sources explicitly
designated as governing. When implementation and accepted meaning disagree, identify
whether the owner intends a defect correction, model revision, or migration; do not
silently rewrite the definition to excuse existing code.

For already-settled input, proceed to reconciliation. Ask only about consequential
unresolved meaning or a contradiction; return the exact gap if the owner or evidence
is unavailable. A collision blocks its dependents, not independent settled updates.

## Model distinctions, not a glossary inventory

Record project-specific meaning, defining behavior, invariants, responsibility,
and relationships whose omission would make future work guess. Use concrete
inclusion, exclusion, transition, or failure scenarios to distinguish overloaded
terms. Avoid generic technical vocabulary, speculative concepts, and synonyms
whose differences do not affect behavior or understanding.

Use one canonical term within a context. Preserve independent meanings across
contexts unless an accepted shared model joins them. Context boundaries follow
meaning, responsibility, and consistency requirements, not directories or services.
For a relationship, record only the direction, crossing contract, translation,
ownership, or change authority needed to avoid ambiguity. Do not force DDD pattern
labels; an explicit mapping is more useful than a guessed taxonomy.

Make invariants and valid transitions precise enough for a designer to enforce.
A state table or small accepted schema can express meaning better than prose.
Selecting a reducer, adapter, queue, or other implementation structure belongs to
codebase-design or implementation; the domain record supplies what must remain true.

## Reconcile the current record

Capture only non-obvious durable meaning future work would likely misapply.
Prefer no change, replacement, merge, relocation, or removal over appending a
parallel definition. Keep executable procedure, commands, current work state,
code inventories, and historical rationale with their respective owners.
Identify existing acceptance and references affected by a changed meaning.
Reconcile their authorized changes and return unapplied consequences explicitly;
updating a definition alone must not silently leave a contradictory current spec.

Follow the configured format. Without one, a short record containing context
purpose, canonical terms with defining behavior, and relevant invariants is enough.
Use an existing suitable documentation location; root CONTEXT.md is a possible
fallback only when it does not displace another purpose. Create a context map only
when several actual contexts need routing, linking their records and meaningful
relationships. Omit empty sections and create files lazily.

## Record rationale when it earns an ADR

An ADR earns its place when a settled choice involves meaningful reversal cost,
is surprising without context, and reflects a real tradeoff. Ordinary terminology,
obvious choices, unresolved proposals, and reversible implementation details do
not automatically need one. Follow existing approval rules and the user's actual
authority; permission to edit context is not automatically permission for an
unrequested ADR or a change to its accepted decision.

Inspect prior ADRs about the same decision before creating a duplicate. Preserve
the predecessor's historical rationale. When superseding, state the successor,
what it replaces, and any remaining applicability; partial supersession must not
erase still-governing decisions. Update authorized current pointers coherently.
Keep one current applicability statement on the predecessor naming its controlling
successors and exact remaining scope. Mark it superseded when no scope remains.
Use repository naming/numbering conventions and check for collisions before writes.

## Return the domain result

Within authorized persistence scope, apply the bounded reconciliation, respecting
dependent-write ordering and read-back from Durable decisions. Otherwise return
proposed wording and its destination. Report the settled distinction, verified
paths or no-change result, and any unresolved meaning or unapplied consequences.
A domain-only request ends here. During broader shaping, return the result to that
conversation and continue only the work already authorized.
