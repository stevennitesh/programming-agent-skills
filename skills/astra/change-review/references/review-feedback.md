# Review feedback

Read for supplied feedback, repair reviews, or a requested bounded review-and-repair
loop. Apply [Finding standards](finding-standards.md) to assess each technical claim;
reviewer preferences do not override accepted behavior. For GitHub feedback
retrieval or authorized replies and resolutions, use PR delivery's
[GitHub review threads](../../pr-delivery/references/github-review-threads.md).

## Reconcile each item

Bind the feedback to the actual candidate and check its claimed obligation,
trigger, and consequence against current code, requirements, and relevant context.

Classify claimed defects as:

- **admitted:** it satisfies Finding standards;
- **disproved:** current evidence shows the claimed problem does not apply;
- **unclear:** a material premise or owner-held decision is missing; or
- **superseded:** the candidate or governing decision changed so the comment no
  longer addresses the current state.

Preserve supplied finding IDs and track validity separately from whether a fix is
pending or verified. Explain dispositions from current evidence; a missing prior
report limits claims about resolving it but permits a clearly labeled fresh review.

When repairs are authorized, make the smallest sufficient supported correction
and necessary in-scope changes. Distinguish required fixes from optional proposals;
do not add unrelated cleanup or drop accepted behavior to satisfy a reviewer.
External replies, resolutions, publication, merge, and risk acceptance require
their own existing authority. Keep reviewers read-only while the execution owner
repairs.

## Bounded review and repair loops

For an iterative review, choose a round or cost limit proportionate to risk,
uncertainty, and the user's budget. Associate candidate identities, stable finding
IDs, dispositions, and decisive evidence with each round; report usage only when
exposed. Preserve execution custody between assessment and repair.

After a correction, verify affected behavior and review the successor's changes,
open findings, and expanded impact. Use [Impact analysis](impact-analysis.md) when
ownership, validation, persistence, or compatibility changes. Retain still-valid
coverage and useful reviewer context. Editorial changes need new behavioral review
only when they change an obligation or invalidate evidence.

Finish when applicable review obligations are satisfied and findings have supported
dispositions. At budget exhaustion, a repeated dispute without new evidence, or an
unavailable required reviewer, report unresolved items and evidence without calling
the result approval. Use Finding standards for any requested gate verdict and
continue independent authorized work where useful.
