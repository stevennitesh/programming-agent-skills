---
name: resolving-merge-conflicts
description: Use when Git is in an in-progress merge, rebase, cherry-pick, or revert, or files contain conflict markers. Reconcile each conflict through three-way source trace, prove the result, and finish the Git operation only when explicitly requested.
---

# Resolving Merge Conflicts

Treat every conflict as a **three-way merge**: base, both sides, and the operation goal.

**State -> Trace -> Reconcile -> Prove -> Finish.**

**Finish authority** means the user explicitly asked to finish the Git operation.

## Process

1. **State.** Read repo instructions and `docs/agents/engineering-contract.md` when present. Inspect `git status`, operation metadata, `git ls-files -u`, in-scope markers, dirty and index state, the operation goal, and finish authority. Proceed only when the operation or marker-only state, scope, unrelated work, and mutation boundary are known.
2. **Trace.** For every unmerged entry or marker-only conflict, inspect the available base and both sides. Trace behavior and each side's intent through commits, branch diffs, PRs, issues, ADRs, specs, tests, and nearby code. Map index stages to their actual roles; during rebase, `ours` is the so-far rebased target and `theirs` is the commit being replayed. Block any path whose required intent remains unproven.
3. **Reconcile.** Resolve every in-scope content or path conflict. Preserve compatible intents. When intents conflict, follow the source trace, operation goal, and commitment boundary; record the trade-off. Keep only traced behavior. Inspect full resolved files and rescan the scope for markers.
4. **Prove.** Run focused repo-owned checks, then broader canonical checks as risk or repo convention requires. Repair only proven resolution-caused breakage. Such failures block **Finish**; an uncertain failure is a `$diagnosing-bugs` handoff; a proven pre-existing failure is residual risk.
5. **Finish.** With finish authority, stage only resolved in-scope paths and continue the merge, rebase, cherry-pick, or revert. Block before continuation if unrelated index state would enter its commit. A new conflict returns to **State**; repeat until Git exits or a blocker is reported. Without finish authority, leave staging, commit, and continuation untouched. Stage or commit marker-only work only when separately requested.

## Guardrails

- **Preserve Git state.** Abort, hard reset, or discard a side only with explicit approval.
- **Evidence over labels.** Use wholesale `--ours` or `--theirs` only when the source trace proves the other side obsolete for this operation.
- **Preserve proof.** Keep tests, assertions, and public behavior unless the source trace requires their change.
- **Isolate.** Preserve unrelated dirty work and its existing index state.

## Handoff

Report the operation and goal; finish authority; resolved and blocked paths; source-intent trade-offs; checks, skips, and residual risk; current `git status`; and either the finished operation or the exact next command.

## Completion Criteria

Complete only when every in-scope unmerged entry and marker is reconciled or blocked; every resolution has three-way source trace and full-file inspection; checks passed or skips and failures are classified; unrelated work is preserved; and Git is either finished under finish authority or handed off with exact remaining state.
