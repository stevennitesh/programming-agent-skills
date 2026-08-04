# Change Review Synthesis

Status: current runtime summary.

Runtime authority is `skills/custom/change-review/`.

Change Review owns one branch, WIP, staged, since-X diff, local PR, release
candidate, or supported-risk implementation candidate from a fixed snapshot.
It judges Spec and Standards separately through the shared Finding Contract,
expands coverage proportionally to supported risk, and returns one read-only
gate decision. Immutable repository-baseline audits recommend `$audit-codebase`
and stop.

Implement and Parallel Implement select Change Review for every accepted
candidate and retain Repair, mutation, Lock, and successor-snapshot authority. The shared
Finding Contract owns review classes, risk triggers, admission, severity, and
remediation bounds; High Assurance Review consumes that owner without duplicate
wording.
