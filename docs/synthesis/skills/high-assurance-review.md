# High-Assurance Review Synthesis

Status: current runtime summary.

Runtime authority is `skills/custom/high-assurance-review/`.

High-Assurance Review owns one release candidate or supported high-risk diff
or PR and returns one read-only release decision. Ordinary diffs and PRs return
intact to the delivery caller as route mismatches; immutable
repository-baseline audits recommend `$audit-codebase` and stop.

Implement and Parallel Implement select High-Assurance Review only for release
candidates or supported high-risk changes and retain Repair, mutation, Lock,
and successor-snapshot authority.
