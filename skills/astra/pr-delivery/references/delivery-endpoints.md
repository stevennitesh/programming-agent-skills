# Delivery endpoints

Read when the user requests end-to-end delivery or asks for a PR ready for human
merge. Preserve the actual endpoint and existing authority throughout the work.
There is no required command phrase or additional skill pipeline.

## Complete through an authorized merge

Carry the authorized implementation, corrections, verification, publication, and
requested CI/review follow-through to the main skill's verified merge endpoint.
Implementation retains its execution owner; delivery selects no extra reviewer
model, review loop, or skill pipeline.

## Complete requested work after merge

Use the confirmed merge and target branch as the starting point. Continue through
the requested effects with their maintained owners:

- Use [Git cleanup](../../git-cleanup/SKILL.md) for requested synchronization and
  branch or worktree cleanup. Verify the intended local branch against the
  current remote target and read back the disposition of the affected refs and
  worktrees.
- Follow the repository's installation instructions for the intended host or
  target. Use the verified merged revision or another authorized revision that
  contains the delivered change. Verify the installed version or content at
  the destination.

Order these steps by their dependencies and the user's request. If a step is
blocked, complete independent authorized steps and report the state of each
requested result.

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
