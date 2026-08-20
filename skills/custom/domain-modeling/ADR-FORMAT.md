# ADR format

Follow the repository's routed ADR convention. An ADR records durable rationale,
the chosen trade-off, and material consequences. It does not own the current
executable specification, procedure, commands, mutable state, or implementation
inventory.

## Worthiness

Offer an ADR only when all three are true:

1. **Hard to reverse.** Changing course later has meaningful cost.
2. **Surprising without context.** A future reader would reasonably ask why.
3. **Real trade-off.** Genuine alternatives existed and one was chosen for a
   specific reason.

Ordinary terminology, reversible implementation details, unresolved decisions,
and obvious choices do not need an ADR.

## Approval and history

Record only an identified, already-settled candidate with separate explicit
approval. Context-write authority does not grant ADR authority.

Before creating one, inspect applicable ADRs for the same decision. Preserve a
predecessor. The successor names what it replaces and what remains. Keep one
current applicability statement on the predecessor naming all controlling
successors and its exact remaining scope. It remains accepted only while that
scope is nonempty; otherwise mark it superseded by the controlling successors.
Update authorized current links in the same change.

## Fallback

When the repository has no convention, use root `docs/adr/` for system-wide
decisions or the `docs/adr/` beside a routed context record for context-local
decisions. Create the directory lazily. Scan that directory and use the next
`NNNN-slug.md`; ambiguous or concurrent numbering is a blocker.

Start with one short record:

```md
# <Decision title>

<What pressure or constraint mattered, what was chosen, and why.>
```

Add status, applicability, rejected alternatives, or consequences only when
they preserve non-obvious durable information or the repository requires them.
Read back every created or changed ADR and return its path and actual state.
