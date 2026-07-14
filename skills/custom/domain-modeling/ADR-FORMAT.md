# ADR Format

ADRs record why a settled, durable trade-off was chosen. Keep unresolved choices in the domain delta.

## ADR-Worthy Gate

Offer an ADR only when all three are true:

1. **Hard to reverse:** changing course later has meaningful cost.
2. **Surprising without context:** a future reader would reasonably ask why.
3. **Real trade-off:** genuine alternatives existed and one was chosen for specific reasons.

## Approval Gate

Create the ADR only after an explicit request or user approval.

## Location

Use root `docs/adr/` for system-wide decisions.

In multi-context repos, use `CONTEXT-MAP.md` to choose the relevant context. Put context-local ADRs in the `docs/adr/` directory beside that context's `CONTEXT.md`.

Create ADR directories lazily, only when the first ADR is needed.

## Template

Use sequential numbering: scan the target directory for the highest existing number, then create `NNNN-slug.md` with the next number.

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

This is enough for most ADRs.

## Optional Sections

Include these only when they add genuine value:

- **Status** frontmatter (`accepted | deprecated | superseded by ADR-NNNN`) - useful when decisions are revisited.
- **Considered Options** - only when rejected alternatives are worth remembering.
- **Consequences** - only when non-obvious downstream effects need to be called out.
