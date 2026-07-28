# Change Review Synthesis

Status: current rename amendment; canonical proof pending.

Runtime authority is `skills/custom/change-review/`. The former `review`
campaign and its exact evidence remain at
[Review Deployment Synthesis](review.md) under their historical identity.

Change Review owns one ordinary branch, WIP, staged, since-X diff, or ordinary
PR from a fixed snapshot. It judges Spec and Standards separately through the
shared Finding Contract and returns one read-only gate decision. Release
candidates and supported high-risk changes hand off once to
`$high-assurance-review`; immutable repository-baseline audits recommend
`$audit-codebase` and stop.

Implement and Parallel Implement select Change Review for ordinary candidates
and retain Repair, mutation, Lock, and successor-snapshot authority. The rename
does not claim installed parity or fresh wording efficacy.
