---
name: resolving-merge-conflicts
description: Use when the repo is in an in-progress merge, rebase, cherry-pick, revert, or has conflict markers; resolve conflicts by tracing both sides to source intent, preserving behavior, running checks, and stopping before commit or rebase continuation unless the user asked to finish.
---

# Resolving Merge Conflicts

Use this when Git is in a conflicted state or files contain conflict markers.

Resolve by preserving **both intents**, not by choosing sides mechanically.

## Process

1. **See the state.** Inspect `git status`, the operation in progress, conflicted files, and the merge/rebase/cherry-pick goal. Read repo instructions before editing.
2. **Trace both intents.** For each conflict, find the primary sources: commit messages, branch diffs, PRs, issues, ADRs, PRDs, tests, and nearby code. Understand what each side was trying to preserve.
3. **Resolve hunks.** Preserve both intents where compatible. Where incompatible, choose the result that matches the operation's stated goal and record the trade-off. Do not invent new behavior.
4. **Check locally.** Run the smallest meaningful checks for the touched area, then broader checks if risk or repo convention requires them. Fix only breakage caused by the resolution.
5. **Stop at the commitment boundary.** If the user asked to finish the merge/rebase/cherry-pick, stage the resolved files and continue the operation. Otherwise report resolved files, checks, unresolved risks, and the exact command the user can run next.

## Guardrails

- Do not run `git merge --abort`, `git rebase --abort`, `git reset --hard`, or discard either side without explicit approval.
- Do not use wholesale `--ours` or `--theirs` unless the source trace proves one side is obsolete for the operation's goal.
- Do not resolve by deleting tests, relaxing assertions, or changing public behavior unless the source trace supports it.
- Do not stage unrelated dirty files.
- Do not commit, continue a rebase, or complete a cherry-pick unless the user explicitly asked you to finish that operation.

## Completion Criteria

Done means every conflict marker in the intended scope is resolved or explicitly reported as blocked; each resolution is tied to source intent; relevant checks ran or were intentionally skipped with a reason; and the handoff states whether the operation was finished or exactly what remains.
