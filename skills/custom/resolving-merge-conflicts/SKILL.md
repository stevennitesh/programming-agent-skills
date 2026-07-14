---
name: resolving-merge-conflicts
description: Reconcile an in-progress merge, rebase, cherry-pick, revert, or conflict-marked file when the user asks to resolve conflicts. For status, explanation, or review, perform only read-only State and Trace.
---

# Resolving Merge Conflicts

Treat every conflict as a **three-way merge**: base, both sides, and the operation goal.

**State -> Trace -> Reconcile -> Prove -> Finish.**

**Reconciliation authority** permits resolving requested in-scope conflicts. **Finish authority** separately permits staging and continuing the Git operation.

## Process

1. **State.** Read repo instructions and `docs/agents/engineering-contract.md` when present. Inspect `git status`, operation metadata, `git ls-files -u`, markers, dirty and index state, operation goal, scope, and both authorities. Identify the operation or marker-only state before mutation.
2. **Trace.** Inspect the available base and both sides for every in-scope conflict; build the Source Trace for each intent. Map index stages to their actual roles. During rebase, `ours` is the so-far rebased target and `theirs` is the commit being replayed. Unproven required intent blocks that path.

Without reconciliation authority, stop after **State** and **Trace**. Report uncertainty and exact remaining state; leave files, index, commits, and Git-operation state unchanged.

3. **Reconcile.** Resolve every in-scope content or path conflict. Preserve compatible intents; where incompatible, follow the Source Trace, operation goal, and commitment boundary, then record the trade-off. Keep only traced behavior. Inspect each full resolved file and rescan for markers.
4. **Prove.** Run focused repo-owned checks and any broader canonical checks required by risk or repo convention. Repair only proven resolution-caused breakage. It blocks **Finish**; hand uncertain failures to `$diagnosing-bugs`; classify proven pre-existing failures as residual risk.
5. **Finish.** With finish authority, block unrelated index state from the commit, stage only resolved in-scope paths, and continue the operation. Each new conflict returns to **State** until Git exits or a blocker remains. Without finish authority, leave staging, commit, and continuation untouched. Stage or commit marker-only work only when separately requested.

## Guardrails

Abort, hard reset, or side discard requires explicit approval. Use wholesale `--ours` or `--theirs` only when the Source Trace proves the other side obsolete. Preserve unrelated dirty work and existing index state.

## Handoff

Report the operation and goal, both authorities, inspected/resolved/blocked paths, intent trade-offs, proof and residual risk, current `git status`, and the finished operation or exact next command.

## Completion

Read-only work completes after **State** and **Trace** are reported with exact remaining state and no mutation.

Reconciliation completes only when every in-scope entry and marker is resolved; each resolution has three-way trace and full-file inspection; proof is classified; unrelated work is preserved; and Git is finished only under finish authority or handed off in exact remaining state. A blocked path returns a blocked outcome, never completion.
