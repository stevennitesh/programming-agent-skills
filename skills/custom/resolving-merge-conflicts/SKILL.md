---
name: resolving-merge-conflicts
description: Inspect or resolve an active conflicted merge, rebase, cherry-pick, revert, or unmerged index. Status, explanation, and review are read-only. Exclude operation planning or start, ordinary diffs, completed operations, marker-like text without Git conflict state, and post-operation bugs.
---

# Resolving merge conflicts

Resolve intended behavior, not markers, in one repository worktree and one
observed conflict state.

A status, explanation, or review request permits no mutation. A request to
resolve permits only the requested working-tree changes. Staging and native
continuation require a separate explicit request. A finish request may inspect,
prove, and continue an already-prepared or automatically staged resolution
without requiring new working-tree edits.

## 1. See the conflict

Inspect `git status`, operation metadata, `git ls-files -u`, the requested
scope, and unrelated work. Identify the operation and its goal before changing
anything. If no active operation or unmerged index remains, stop unchanged and
report what Git shows. Marker-like text alone is not a Git conflict.

Reread this state before mutation whenever user, worker, tool, or continuation
activity may have changed it.

## 2. Understand the sides

Read [OPERATIONS.md](OPERATIONS.md) only for the observed operation and any
special conflict type present. Map index stages to their actual operation
roles. Treat missing stages and multi-path topology as evidence, not malformed
input.

Trace intent from the Git objects and operation goal, then the nearest caller,
contract, test, or history that explains why each side exists. Preserve
compatible intent. When required intents conflict, follow the governing
behavior or return the unresolved decision to its owner.

For a status, explanation, or review request, stop here and report the observed
state and intent without running resolution proof.

## 3. Resolve the requested paths

Change only the requested reconciliation scope, including traced dependent
paths needed to make the result coherent. Stop before expanding that scope.
Keep traced behavior. A whole-side result is valid only when the trace shows
the other side obsolete. Inspect each complete resulting artifact, including
its path, mode, references, and generated or submodule boundary when
applicable. Do not stage unless finishing was explicitly requested.

## 4. Check the result

Run the nearest useful repository check and inspect the resolved artifacts and
remaining unmerged paths. When resolution was requested, repair a clear
in-scope resolution defect and check again. Otherwise stop with the defect,
failing evidence, and exact operation state.

## 5. Finish only when requested

Reread Git state, stage exact resolved paths, require `git ls-files -u` to be
empty, and inspect the full staged delta so unrelated state cannot enter the
operation. Never use `git add -A`. Continue with the operation's native command.
A new conflict returns to step 1. After the operation exits, read final state
back and rerun only proof invalidated by continuation. If continuation stops on
an exceptional operation choice, read its `OPERATIONS.md` guidance and stop
unless that action was explicitly requested.

## Completion

Complete when the requested inspection remains unchanged, the requested
resolution is checked with exact Git state reported, or the explicitly
authorized operation has exited with final state read back. State which paths
changed, what check ran, whether the operation remains active, and any decision
still needed.
