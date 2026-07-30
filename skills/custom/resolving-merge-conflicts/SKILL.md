---
name: resolving-merge-conflicts
description: Inspect or reconcile an already-conflicted merge, rebase, cherry-pick, revert, unmerged index, or plausible marker state. Status, explanation, or review is read-only. Exclude operation planning or start, ordinary diffs, clean completed merges, and post-operation bugs.
---

# Resolving Merge Conflicts

Resolve meaning, not markers, across one repository worktree and one observed
conflict state.

**Read-only: State -> Trace -> Return.**

**Reconcile: State -> Trace -> Reconcile -> Prove -> Return; add Finish before
Return only with finish authority.**

**Reconciliation authority** permits only requested in-scope working-tree
changes. **Finish authority** separately permits exact-path staging and native
continuation of the observed operation. The request or caller packet grants them
separately; invocation alone grants neither.

## Process

1. **State.** Read repo instructions and
   `docs/agents/engineering-contract.md` when present. Inspect `git status`,
   operation metadata, `git ls-files -u`, plausible markers, index, worktree,
   untracked and unrelated state, operation goal, scope, and both authorities.
   An unmerged index with unknown operation may be inspected or reconciled only
   from proven object and intent roles and has no **Finish**. Markers are
   signals, not proof of conflict.
2. **Trace.** Load [OPERATIONS.md](OPERATIONS.md) only for the observed
   operation and relevant conflict-class rows. Inspect the base and sides in
   their actual operation roles. Trace intent through the operation goal and
   objects, then governing specs, ADRs, domain rules, tests, history, PRs,
   issues, and callers as available. Classify each resolution as **Compose**,
   **Transform**, or **Prefer** with evidence; when required intents conflict
   without authority, return `decision required`.

Without reconciliation authority, stop after **State** and **Trace** with no
mutation. Refresh live State before every mutation, after user or worker input,
after Diagnosis, and after every continuation.

3. **Reconcile.** Author only the in-scope candidate working-tree and path
   topology. Preserve compatible intents and keep only traced behavior. Inspect
   every complete resolved artifact, its path and mode, generated or submodule
   boundary when applicable, and remaining plausible markers. Do not stage.
4. **Prove.** Run focused repo-owned checks and broader checks required by risk
   or repo convention. Repair an obvious in-scope resolution defect and reprove.
   When failure causality is uncertain, return `diagnosis-required` with the
   operation, goal, exact state, evidence, authorities, and Return owner. Return
   `blocked` for a required
   out-of-scope, authority-gated, or blocking pre-existing correction. A proven
   unrelated failure may remain explicit residual risk. Focused resolution
   proof must pass before **Finish**.
5. **Finish.** Only with finish authority, require all operation conflicts
   resolved, stage exact authorized paths, inspect the full staged-index delta,
   and exclude unrelated state. Never use `git add -A`. Continue through the
   operation's native command. A new conflict returns to **State**; an empty
   change, hook failure, edit request, or recovery choice returns
   `decision required` or `blocked`. After operation exit, refresh State and run
   proof invalidated or required by continuation.

## Guardrails

Preserve unrelated dirty and index state. Abort, skip, quit, reset, whole-side
selection, strategy replacement, todo or message-policy change, hook bypass, and
allow-empty handling each require action-specific authority. Use a whole side
only when Trace proves the other intent obsolete. An automatic or reused
resolution remains unproved until inspected and tested.

## Return

Return exactly one status: `inspection`, `prepared reconciliation`, `finished
operation`, `decision required`, `blocked`, or `route mismatch`. Report
repository/worktree, operation and goal, scope and both authorities, inspected
and changed paths, Compose/Transform/Prefer decisions, proof and residual risk,
exact current Git/index/worktree state, and the next owner or authorized
command.

## Completion

`inspection` completes after **State** and **Trace** report exact unchanged
state. `prepared reconciliation` requires every in-scope candidate traced,
authored, fully inspected, and proved while index and operation state remain
unfinished. `finished operation` additionally requires no targeted operation or
unmerged entries, an audited index, final state read-back, and current required
proof.

A blocked path, unresolved resolution-caused failure, unapproved decision, or
route mismatch never returns completion.
