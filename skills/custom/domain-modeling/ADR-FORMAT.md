# ADR Format

Domain Modeling records approved ADRs; the originating product, domain,
interface, architecture, or engineering owner settles the decision. Follow the
repository's routed ADR convention, using the fallback below only when none
exists.

An ADR owns durable rationale, the chosen trade-off, and material consequences,
including a hard-to-reverse algorithm choice when worthy. It does not own the
current executable algorithm specification, procedure, commands, mutable state,
or implementation inventory.

## Worthiness

Offer an ADR only when all three are true:

1. **Hard to reverse:** changing course later has meaningful cost.
2. **Surprising without context:** a future reader would reasonably ask why.
3. **Real trade-off:** genuine alternatives existed and one was chosen for
   specific reasons.

Ordinary terminology, reversible implementation detail, unresolved judgment, and
decisions without a real alternative omit this branch.

## Approval

Create an ADR only after explicit approval identifies the already-settled
candidate. Context persistence does not grant ADR approval. Preserve an
unapproved candidate as `offered`, `deferred`, or `declined` without writing.

## Fallback Location And Numbering

Use root `docs/adr/` for system-wide decisions. For a context-local decision,
follow `CONTEXT-MAP.md` and use the `docs/adr/` directory beside that context's
record.

Create the directory lazily. Scan the target directory for the highest number
and create the next `NNNN-slug.md`; ambiguous or concurrent numbering returns a
blocker instead of overwriting.

Before numbering a new ADR, inspect applicable ADRs for the same
decision. A successor names its predecessor and the exact scope it replaces,
including retained bounded decisions. Mark the predecessor `superseded by
ADR-NNNN` only when the successor replaces it as a whole; otherwise state the
exact replaced and retained scope in the successor and update one predecessor
applicability note with every partial successor and the scope that remains. The
predecessor stays `accepted` only for that retained scope. Preserve the
predecessor file as history. Update authorized current routes in the same
change, and return every foreign route consequence to its owner.

## Record

```md
# <Decision title>

<Context: the pressure and constraints that made a decision necessary.>

<Decision: what was chosen and why.>
```

Add only sections that preserve material information:

- **Status:** `accepted`, `deprecated`, or `superseded by ADR-NNNN` when
  lifecycle matters.
- **Applicability:** all partial-successor links and the predecessor scope that
  remains current, when partially replaced.
- **Considered Options:** when rejected alternatives remain instructive.
- **Consequences:** when non-obvious effects, obligations, or risks matter
  downstream.

Reread every created or changed ADR. Return the candidate, approval authority,
path, outcome, and read-back state in the Domain Delta.
