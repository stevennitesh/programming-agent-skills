---
name: resolving-merge-conflicts
description: Inspect or resolve conflicts in an active Git merge, rebase, cherry-pick, revert, or unmerged index.
---

# Resolving merge conflicts

Recover the intended combined behavior, preserve unrelated work, and stop at the
requested Git endpoint. Removing conflict markers alone does not establish a
correct resolution.

## 1. Observe the operation and authority

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

If no active operation or unmerged entries remain, report the observed state
instead of starting an integration. An active operation may still await review or
continuation after conflicts have already been staged. Do not resolve a worktree
concurrently with another integration owner. Re-observe state after another actor
or unexpected change.

## 2. Reconcile the intended combination

Read the applicable operation row and any special conflict types actually present
in [Operation details](references/operations.md). Map index stages and side names
to their real objects before using side-selection commands; `ours`, `theirs`,
and marker labels are not statements of intent.

Use the accepted requirements and affected code to determine the intended combined
behavior. Preserve compatible intent from both changes. When the changes disagree
semantically, follow the governing requirement and surface only a consequential
decision that lacks an owner-held answer.

Resolve affected neighboring paths when the conflict changes a contract they
consume. Whole-side selection is valid only when the other change is obsolete or
its intent is preserved elsewhere. Inspect final path presence, names, content,
and modes rather than only marker locations.

## 3. Prepare and prove the resolved candidate

Treat manual, automatic, merge-driver, and `rerere` resolutions as candidates to
inspect. Require the resulting unmerged/index state and resolved delta to represent
the intended combination.

Run repository-required checks and the nearest focused evidence needed for the
combined behavior. When the conflict changes an integration seam, prove the
ordinary combined producer/consumer path rather than relying only on tests that
passed independently on each side.

Stage only resolved paths and changes owned by this resolution; do not use blanket
staging. Preserve unrelated user-owned changes.

## 4. Reach only the authorized endpoint

Before native continuation, require an empty unmerged index and inspect the staged
delta. If continuation would necessarily commit or otherwise absorb unrelated
user-owned work, stop and report that conflict. Do not stash, discard, rewrite,
unstage, or commit unrelated work merely to make continuation possible without
authority.

When continuation is authorized, use the observed operation's native continuation
and preserve its selected commits, mainline, messages, options, and policy. Do not
replace a replay operation with a plain commit. Re-enter this procedure for each
subsequent conflict until the requested endpoint is reached or a concrete decision
or execution blocker remains.

For no-commit endpoints, empty replays, editor/hook/signing failures, abort/skip/
quit choices, strategy or mainline changes, or other recovery effects, use
[Operation details](references/operations.md) rather than improvising a shortcut.

Finish by re-observing status, unmerged entries, and operation metadata. Report the
endpoint reached, material intent choices, resulting revision when applicable,
decisive checks, preserved unrelated work, and any remaining blocker.
