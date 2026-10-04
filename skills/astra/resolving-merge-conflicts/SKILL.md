---
name: resolving-merge-conflicts
description: Inspect or resolve conflicts in an active Git merge, rebase, cherry-pick, revert, or unmerged index.
---

# Resolving merge conflicts

Recover the intended combined behavior, preserve unrelated work, and stop at the
requested Git endpoint. Removing conflict markers alone does not establish a
correct resolution.

Choose the investigation tools, resolution techniques, and grouping of related
conflicts. Preserve necessary ordering: understand state and authority before
mutation, and inspect the resolved candidate before continuation.

## Establish the operation and authority

Inspect the worktree identity, status, Git-resolved operation metadata, unmerged
index (`git ls-files -u`), relevant commits, conflicted paths, and existing
staged, unstaged, and untracked work. In linked worktrees, do not assume `.git`
is a directory.

Establish the requested endpoint before mutation. Status, explanation, and review
requests are read-only. A request to finish an active operation carries its normal
resolution, staging, and native continuation effects within repository policy; a
resolve-only request does not by itself authorize a commit. Preserve an explicit
endpoint such as leaving resolutions unstaged or leaving a no-commit operation
prepared.

If neither an active operation nor unmerged entries remain, report the observed state
instead of starting an integration. An active operation may still await review or
continuation after conflicts have already been staged. Do not resolve a worktree
concurrently with another integration owner. Re-observe state after another actor
or unexpected change.

## Reconcile the intended combination

Read the applicable operation row and any special conflict types actually present
in [Operation details](references/operations.md). Map index stages and side names
to their real objects before using side-selection commands; `ours`, `theirs`,
and marker labels are not statements of intent.

Use the accepted requirements and affected code to determine the intended combined
behavior. Preserve compatible intent from both changes. When the changes disagree
semantically, follow the governing requirement and surface only a consequential
decision that lacks an owner-held answer.

Resolve affected neighboring paths when the conflict changes a contract they
consume. Whole-side selection is valid when the resulting candidate satisfies the
governing requirements and preserves required intent. Inspect final path presence,
names, content, and modes rather than only marker locations.

## Verify the resolved candidate

Treat manual, automatic, merge-driver, and `rerere` resolutions as candidates to
inspect. Require the resulting unmerged/index state and resolved delta to represent
the intended combination.

Choose intermediate checks for the affected behavior and the risk of continuing,
honoring any repository-required per-commit checks. Reuse still-valid evidence;
each replay does not automatically require a full suite. Verify the final combined
result at the requested endpoint with repository-required checks and focused
evidence. When the conflict changes an integration seam, prove the ordinary
combined producer/consumer path rather than relying only on tests that passed
independently on each side.

Repair resolution-caused failures and routine local tooling problems within scope
and existing authority, then rerun affected checks. These repairs and retries
need no renewed permission; preserve required checks and repository policy.

Choose a staging method that includes only changes owned by this resolution and
preserves unrelated user-owned changes. Whole-worktree staging is appropriate only
when every change it would include has been verified to belong to the resolution.

## Reach the authorized endpoint

Before native continuation, require an empty unmerged index and inspect the staged
delta. If continuation would necessarily commit or otherwise absorb unrelated
user-owned work, stop and report that conflict. Do not stash, discard, rewrite,
unstage, or commit unrelated work merely to make continuation possible without
authority.

When continuation is authorized, use the observed operation's native continuation
and preserve its selected commits, mainline, messages, options, and policy. Do not
replace a replay operation with a plain commit. Continue through subsequent
conflicts without renewed permission, refreshing operation state and affected
context as needed. Stop at the requested endpoint, for an unresolved consequential
decision or missing authority, or when an execution blocker cannot be resolved
within scope.

For no-commit endpoints, empty replays, editor/hook/signing failures, abort/skip/
quit choices, strategy or mainline changes, or other recovery effects, use
[Operation details](references/operations.md) rather than improvising a shortcut.

Finish by re-observing status, unmerged entries, and operation metadata. Report the
endpoint reached, material intent choices, resulting revision when applicable,
decisive checks, preserved unrelated work, and any remaining blocker.
