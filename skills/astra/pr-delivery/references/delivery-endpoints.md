# Delivery endpoints

Read when the user requests end-to-end delivery or asks for a PR ready for human
merge. Preserve the actual endpoint and existing authority throughout the work.
There is no required command phrase or additional skill pipeline.

## Complete through an authorized merge

Carry the authorized implementation, corrections, verification, publication, and
requested CI/review follow-through to the main skill's verified merge endpoint.
Implementation retains its execution owner; delivery selects no extra reviewer
model, review loop, or skill pipeline.

## Prepare for the human to merge

Complete the requested preparation, corrections, checks, and review, then leave
the PR open and unmerged. Do not merge, enable auto-merge, enqueue it for merging,
or delegate those actions. Inspect existing automatic-merge and queue state before
publishing changes that could trigger a merge, and refresh it before handoff.

If existing automation can merge the PR, disable auto-merge or remove its queued
entry only within existing authority and through supported controls. Verify and
report that change. If it cannot be prevented or controlled within scope, pause
dependent publication and explain the blocker; do not claim the unmerged endpoint
is secured. This does not imply control over other people who can merge it.

Refresh the live base, exact head, draft/open state, required checks, requested
reviews, mergeability, and automation state at handoff. Report one of:

- **Ready for human merge:** the requested readiness conditions pass on the
  identified candidate, which remains open, non-draft, and not set to auto-merge.
- **Waiting for required approval:** only identified required human approval
  remains; do not describe it as fully ready under an unsatisfied gate.
- **Blocked:** identify the unsatisfied condition, attempted recovery, and needed
  input or authority. If someone else merged the PR, report that observed outcome.

Include the PR, head, decisive verification and review outcomes, and material
limits. Release owned monitoring resources using
[PR monitoring](pr-monitoring.md) when applicable.
