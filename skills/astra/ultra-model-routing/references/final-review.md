# Final review

Use before this workflow opens an authorized PR, or when the user requests this
sequence. This reference owns the count and progression;
[change-review](../../change-review/SKILL.md) owns candidate evidence, findings,
independence, correction review, and any requested gate decision.

## Complete three sequential rounds

Start each round with a fresh, read-only reviewer independent of implementation
and integration, using [Shared model routing](../../controlled-delegation/references/model-policy.md).
Give it the accepted requirements, fixed candidate and comparison, relevant
sources, verification, and material limits under change-review. Each assessment
covers the accepted outcome; complementary emphases do not waive obligations.

A round includes assessment, lead triage, authorized repairs, and the necessary
verification and correction review. Complete that work before starting the next
round. Concurrent reviewers count as one round. A still-independent reviewer may
verify corrections within a round; the next required round starts fresh.
Do not manufacture findings or repeat checks whose evidence remains valid.

## Finish on the delivery candidate

Bind each assessment to fixed content or review custody and refresh evidence
affected by successor changes. A third-round defect still needs repair and review
of affected successor behavior before delivery. Choose further coverage for its
impact; do not restart all three rounds mechanically.

Missing required coverage or an unavailable required reviewer remains incomplete.
The lead resolves findings by evidence and retains acceptance; reviewer agreement
alone establishes no gate. Report the final candidate, round status, decisive
checks, and material limits concisely.

Complete the sequence before PR opening, using [pr-delivery](../../pr-delivery/SKILL.md)
only for the authorized endpoint. Explicit user changes to the count or arrangement
take precedence. This sequence grants no publication or risk-acceptance authority
and adds no PR workflow to implementation-only or review-only work.
