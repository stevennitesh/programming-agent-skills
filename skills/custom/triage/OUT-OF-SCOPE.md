# Out-of-Scope Knowledge Base

The repo's `.out-of-scope/` directory stores durable decisions for rejected enhancements:

1. **Institutional memory:** preserve why the concept was rejected.
2. **Deduplication:** connect later requests to that decision.

Use one short kebab-case file per **concept**, not per issue. Group every request for the same concept under `## Prior requests`.

## File Format

Write a short, readable decision record:

```markdown
# <Rejected concept>

Decision: Out of scope because <durable product, technical, or strategic reason>.

Not sufficient: temporary capacity or priority.

## Prior requests

- <tracker reference> - "<request title>"
```

## Screen For Prior Rejection

- **Screen:** inspect filenames and headings, then search by domain concept.
- **Load:** read likely matches in full; read the entire directory only when it is small.
- **Match:** compare concepts, not keywords.
- **Confirm:** append the request and close under the existing decision.
- **Reconsider:** require an explicit maintainer decision, then include any update or deletion in the mutation packet.
- **Distinguish:** continue normal triage when the concepts are related but materially different.

## Write Gate

A maintainer-approved rejected enhancement opens this knowledge-base write gate. This applies equally to enhancement issues and configured enhancement PRs.

- **Rejected enhancement:** create or update one concept file, link it from the tracker comment, then close.
- **Already implemented:** point to the existing behavior in the tracker.
- **Rejected bug:** explain the rejection in the tracker.
- **Reconsidered concept:** update or delete the concept file only through the approved mutation packet.

## Apply The Decision

1. Find or create the concept file.
2. Preserve the durable decision and reason.
3. Append the request under `## Prior requests`.
4. Post the disclaimer-prefixed tracker comment with the file path.
5. Apply `wontfix` and close through the tracker contract.

When a maintainer reopens the concept, update or delete the record through the approved mutation packet. Historical issues remain historical; the triggering request continues through normal triage.
