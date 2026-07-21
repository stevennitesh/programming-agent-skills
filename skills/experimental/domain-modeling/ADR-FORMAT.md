# ADR Format

ADRs record why an already settled, durable trade-off was chosen. Domain Modeling records approved ADRs; the decision's product, domain, interface, architecture, or engineering owner settles the decision.

## Worthiness Gate

Offer an ADR only when all three are true:

1. **Hard to reverse:** changing course later has meaningful cost.
2. **Surprising without context:** a future reader would reasonably ask why.
3. **Real trade-off:** genuine alternatives existed and one was chosen for specific reasons.

Ordinary terminology, reversible implementation detail, unresolved judgment, and decisions without a real alternative omit the ADR branch.

## Approval Gate

Create an ADR only after explicit approval identifies the candidate decision. Domain-record persistence authority does not grant ADR approval. Preserve an unapproved candidate as `offered`, `deferred`, or `declined` without writing.

## Location And Numbering

Use root `docs/adr/` for system-wide decisions. For a context-local decision, follow `CONTEXT-MAP.md` and use the `docs/adr/` directory beside that context's `CONTEXT.md`.

Create the directory lazily. Scan the target directory for the highest existing number and create the next `NNNN-slug.md`; concurrent or ambiguous numbering returns a blocker instead of overwriting.

## Record

```md
# <Decision title>

<Context: the pressure and constraints that made a decision necessary.>

<Decision: what was chosen and why.>
```

Add only sections that preserve material information:

- **Status:** `accepted`, `deprecated`, or `superseded by ADR-NNNN` when lifecycle matters.
- **Considered Options:** when rejected alternatives remain instructive.
- **Consequences:** when non-obvious effects, obligations, or risks matter downstream.

Reread every created or changed ADR. Return the candidate, approval authority, path, outcome, and read-back state in the Domain Delta.
