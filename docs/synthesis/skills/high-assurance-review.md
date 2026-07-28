# High-Assurance Review Synthesis

Status: current rename amendment; canonical proof pending.

Runtime authority is `skills/custom/high-assurance-review/`. The former
`convergent-pr-review` campaign and its exact evidence remain at
[Convergent PR Review Active Deploy Synthesis](convergent-pr-review.md) under
their historical identity.

High-Assurance Review owns one release candidate or supported high-risk diff
or PR. It pins one immutable target, dispatches exactly two fresh core
reviewers plus at most one supported-risk specialist, admits findings at the
root, and returns one read-only release decision. Ordinary diffs and PRs hand
off once to `$change-review`; immutable repository-baseline audits recommend
`$audit-codebase` and stop.

Implement and Parallel Implement select High-Assurance Review only for release
candidates or supported high-risk changes and retain Repair, mutation, Lock,
and successor-snapshot authority. The rename does not claim installed parity
or fresh wording efficacy.
