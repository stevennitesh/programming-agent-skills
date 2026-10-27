---
name: resolving-merge-conflicts
description: Inspect or resolve conflicts in an active Git merge, rebase, cherry-pick, revert, or unmerged index.
---

# Resolving merge conflicts

Recover the intended combined behavior, preserve unrelated work, and stop at the
requested Git endpoint. Removing conflict markers alone does not establish a
correct resolution.

## Establish the operation and authority

Inspect worktree identity, status, Git-resolved operation metadata, unmerged
index (`git ls-files -u`), relevant commits and paths, and staged, unstaged, and
untracked work. In linked worktrees, `.git` need not be a directory.

Establish the endpoint before mutation. Status, explanation, and review are
read-only. Finishing an active operation carries its normal resolution, staging,
and native continuation effects within repository policy; resolve-only work does
not authorize a commit. Preserve explicit unstaged or no-commit endpoints.

If neither an active operation nor unmerged entries remain, report state rather
than starting an integration. Staged resolutions can still await continuation.
Do not share write custody with another integration owner; refresh state after
another actor or unexpected change.

## Reconcile the intended combination

Read the applicable operation row and any special conflict types actually present
in [Operation details](references/operations.md). Map index stages and side names
to their real objects before using side-selection commands; `ours`, `theirs`,
and marker labels are not statements of intent.

Reconcile the affected code under accepted requirements, preserving compatible
intent from both changes. For semantic disagreement, follow the governing
requirement; surface consequential decisions only when no owner-held answer exists.

Include neighboring consumers when a changed contract affects them. Whole-side
selection is valid when it preserves required intent. Inspect final path presence,
names, content, and modes, including changes beyond marker locations.

## Verify the resolved candidate

Inspect manual, automatic, merge-driver, and `rerere` results as candidates.
The resolved delta and index must represent the intended combination.

Choose intermediate checks for continuation risk and required per-commit policy;
each replay needs no automatic full suite. Verify the final combined result with
required checks and focused evidence, reusing still-valid proof. For changed
integration seams, prove the ordinary combined producer/consumer path; passing
checks on each side alone do not establish integration.

Repair resolution-caused failures and routine local tooling problems within
existing scope and authority, then rerun affected checks without renewed permission.

Stage only resolution-owned changes. Whole-worktree staging is appropriate only
after verifying every included change belongs to the resolution.

## Reach the authorized endpoint

Before native continuation, require an empty unmerged index and inspect the staged
delta. Stop if continuation would absorb unrelated work. Do not stash, discard,
rewrite, unstage, or commit that work to make continuation possible without authority.

Use the observed operation's authorized native continuation, preserving selected
commits, mainline, messages, options, and policy; a plain commit cannot replace
replay continuation. Continue through subsequent conflicts without renewed
permission, refreshing state and context. Stop at the endpoint, for an unresolved
consequential decision or missing authority, or for a blocker that cannot be
resolved within scope.

For no-commit endpoints, empty replays, editor/hook/signing failures, or recovery
choices such as abort, skip, quit, or strategy/mainline changes, use
[Operation details](references/operations.md).

Finish by re-observing status, unmerged entries, and operation metadata. Report the
endpoint reached, material intent choices, resulting revision when applicable,
decisive checks, preserved unrelated work, and any remaining blocker.
