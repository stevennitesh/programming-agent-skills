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

## Screen

Inspect filenames and headings, search by domain concept, and read likely matches in full. Read the entire directory only when it is small. Match concepts, not keywords.

## Decide

A maintainer-approved rejected enhancement opens the write gate for issues and configured PRs.

- **Confirm:** record the request under the existing decision.
- **Reconsider:** update or delete the record through the approved mutation packet, then continue the triggering request through normal triage. Historical issues remain historical.
- **Distinguish:** continue normal triage when the concepts are materially different.
- **Already implemented:** point to the existing behavior in the tracker; do not write a rejection record.
- **Rejected bug:** explain the rejection in the tracker; do not write a rejection record.

## Record

1. Find or create the concept file.
2. Preserve the durable decision and reason.
3. Append the request under `## Prior requests`.

## Close

Post the disclaimer-prefixed tracker comment with the file path, apply `wontfix`, and close through the tracker contract.
