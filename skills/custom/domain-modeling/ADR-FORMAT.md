# ADR Format

ADRs record why a durable trade-off was chosen.

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

ADRs use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's enough for most ADRs. The value is recording that a decision was made and why, not filling out sections.

## Optional Sections

Only include these when they add genuine value. Most ADRs will not need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) - useful when decisions are revisited.
- **Considered Options** - only when rejected alternatives are worth remembering.
- **Consequences** - only when non-obvious downstream effects need to be called out.

## Numbering

Scan the target ADR directory for the highest existing number and increment by one.

## What Qualifies

ADR-worthy decisions include:

- **Architectural shape**: monorepo, event sourcing, read/write model split.
- **Integration patterns between contexts**: domain events vs synchronous HTTP.
- **Technology choices with real lock-in**: database, message bus, auth provider, deployment target. Not every library.
- **Boundary and scope decisions**: ownership of domain data, context boundaries, explicit no-s.
- **Deliberate deviations from the obvious path**: manual SQL instead of an ORM, custom build step instead of framework default.
- **Constraints not visible in code**: compliance limits, latency contracts, partner requirements.
- **Rejected alternatives worth remembering**: GraphQL considered, REST chosen; queue considered, synchronous request chosen.
