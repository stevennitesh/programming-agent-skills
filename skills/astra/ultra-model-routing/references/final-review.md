# Final review

Use for this skill's review requirement before opening an authorized PR, or
when the user explicitly requests this final-review sequence. Use
[change-review](../../change-review/SKILL.md) for review evidence and findings;
this reference owns the round count and progression.

## Preserve the requested sequence

Complete three sequential final-review rounds with fresh, read-only reviewers.
Use the review route in the [main skill](../SKILL.md); retain targeted Max
escalation under [Model policy](model-policy.md). Explicit user changes to the
count or arrangement take precedence for their stated scope.

A round consists of an independent assessment of an identified candidate,
triage of its findings, authorized repairs, and necessary verification of those
repairs. Begin the next round after that work is complete. Multiple reviewers
of the same candidate running concurrently belong to one round; they do not
satisfy three sequential rounds.

Give each reviewer the accepted requirements, applicable repository guidance,
candidate and comparison, verification evidence, and material known limits.
Provide prior findings where correction review needs them, without treating a
previous verdict as evidence that the successor is correct.

Bind the review to fixed content or review custody. Do not let mutable checkout
changes invalidate a review silently. Preserve each review's identity when the
candidate changes and reassess affected evidence.

## Use each round to improve coverage

Let reviewers choose their investigations and useful checks. Each round must
assess the candidate against the accepted outcome; a narrower emphasis does not
waive an applicable correctness obligation. Useful complementary emphases are:

1. **First round:** required behavior, implementation correctness, and supported
   behavior that must be preserved.
2. **Second round:** failure paths, interactions, compatibility, security where
   relevant, and cases the existing checks may miss.
3. **Third round:** the integrated candidate, effects of repairs, remaining
   obligations, and readiness for the requested delivery endpoint.

These emphases guide coverage rather than prescribe a universal checklist.
Use the existing review finding standards; do not manufacture findings to fill
a round or repeat expensive checks whose evidence remains applicable.

The lead assesses findings by evidence, resolves contradictory conclusions,
and returns actionable corrections to the appropriate worker. Reviewer
agreement is not a vote that establishes correctness. Keep ordinary repairs
with the worker whose context remains useful.

## Finish on the actual delivery candidate

Complete the required rounds before opening the PR. If the third round finds
a defect, repair it and review the affected successor behavior before delivery.
Three completed assessments do not excuse unresolved findings or an unreviewed
correction. Choose further focused or broader review according to the repair's
impact; do not mechanically restart all three rounds for every change.

Keep required checks, candidate freshness, and material evidence gaps separate.
Do not mark an unavailable review as completed or replace independent review
with the implementation worker's self-assessment. A consequential unresolved
block means review readiness is incomplete, even if useful implementation
work has finished.

Return the final candidate, review coverage and round status, decisive checks,
resolved findings, and remaining material limits concisely. No new report
schema, permanent ledger, or blanket testing campaign is required.

Review readiness does not authorize publication, risk acceptance, merge, or
deployment. Use [PR delivery](../../pr-delivery/SKILL.md) for the already-requested
delivery endpoint. For review-only work, return the findings and review status.
For implementation without PR delivery, perform the requested or applicable
reviews without inventing a PR-opening task.
