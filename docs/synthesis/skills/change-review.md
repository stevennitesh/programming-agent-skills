# Change Review Synthesis

Status: current runtime summary.

Runtime authority is `skills/custom/change-review/`.

Change Review owns one ordinary branch, WIP, staged, since-X diff, or ordinary
PR from a fixed snapshot. It judges Spec and Standards separately through the
shared Finding Contract and returns one read-only gate decision. Release
candidates and supported high-risk changes return intact to the delivery caller
as route mismatches; immutable repository-baseline audits recommend
`$audit-codebase` and stop.

Implement and Parallel Implement select Change Review for ordinary candidates
and retain Repair, mutation, Lock, and successor-snapshot authority. The shared
Finding Contract owns review classes, risk triggers, admission, severity, and
remediation bounds; High Assurance Review consumes that owner without duplicate
wording.
