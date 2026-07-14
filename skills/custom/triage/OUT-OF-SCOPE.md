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

## Classify

- **Confirm:** add the tracker reference under the existing decision.
- **Reconsider:** propose an update or deletion, then return the triggering request to normal triage. Historical issues remain historical.
- **Distinguish:** continue normal triage when the concepts are materially different.
- **Already implemented:** point to the existing behavior; no rejection record is needed.
- **Rejected bug:** explain the rejection; no rejection record is needed.

For a rejected enhancement, return the matched or proposed concept path, durable reason, `Prior requests` delta, and required tracker outcome to the active triage branch. A knowledge-base change may occur only inside that branch's explicitly approved mutation packet; the branch owns application and proof.
