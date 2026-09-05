# Operation details

Read the observed operation row and the special cases actually present.
The main skill owns authority, scope, proof, and completion.

## Object roles and continuation

| Operation | Stage 1 / 2 / 3, for ordinary three-way conflicts | Native continuation |
| --- | --- | --- |
| Merge | merge base (possibly synthesized) / current target / merged side | `git merge --continue` |
| Rebase | parent of replayed change / so-far rebased target / commit being replayed | `git rebase --continue` |
| Cherry-pick | selected parent or mainline / current target / selected commit | `git cherry-pick --continue` |
| Revert | selected commit / current target / selected parent or mainline | `git revert --continue` |
| Unmerged index without a known operation | inspect actual objects and provenance; do not invent side roles | none |

Rebase's `ours` is the rebased target and `theirs` is the change being replayed.
Do not equate those words with the user's branch or preferred intent. For merge
commits, reconstructed merges, or unusual backends, inspect the actual operation
and objects rather than forcing them into the ordinary replay row. Preserve the
selected mainline for cherry-pick/revert; changing it changes the requested delta.
Respect an existing no-commit operation's endpoint instead of inventing a commit.
For `merge --no-commit`, leave the resolved index prepared: `merge --continue`
would create the merge commit. For conflicted cherry-pick/revert sequences begun
with `--no-commit`, do not assume that `--continue` preserves that endpoint merely
because saved options say no-commit: continuation can fail or create a commit.
Leave the resolved index and sequence intact unless a continuation method is
verified for the installed Git and authorized endpoint. Report the blocked
remainder; do not commit or alter the sequence as a workaround. If the original
endpoint cannot be recovered from Git state, use the task context rather than
inferring commit authority.

A stage may be missing in add/add, modify/delete, and root-commit cases. Rename
and directory/file conflicts can span multiple paths. Inspect the whole path set.

## Conditional conflict handling

| Present condition | Resolution and evidence |
| --- | --- |
| Add/delete/rename or directory/file collision | Establish intended presence and destination; reconcile callers, imports, registrations, and case-sensitive path differences. Retain compatibility paths only for an accepted consumer need. |
| Generated file or lockfile | Reconcile the owning source or dependency declarations, then use the repository's generator/resolver. Inspect its diff for accidental version changes or unrelated churn; do not admit out-of-scope effects silently. |
| Attributes, filters, line endings | Compare repository and worktree representations. Use the established normalization/generation rules; avoid changing attributes or global configuration just to hide a conflict. |
| Binary, executable bit, or symlink | Inspect the chosen object and mode as well as its usable result; textual marker removal cannot establish correctness. |
| Submodule | Resolve and verify the exact gitlink commit and its intended history. Inspect the nested repository when needed; fetch or mutate it only within existing task authority. Do not equate its current checkout with the selected gitlink. |
| `rerere`, merge driver, or mergetool output | Review the reused or generated result, including already staged content. Empty conflict listings do not prove preserved intent. Do not rewrite caches or configuration as an incidental fix. |
| Autostash restoration | A merge/rebase may finish before restoring local changes produces new conflicts. Inspect the remaining index, worktree, and stash evidence. Preserve recoverable data; do not repeat continuation when that operation has ended. Resolve the restoration only within task authority and report its distinct state. |

## Stops and recovery

For an empty replay, compare the requested delta with the target: it may already
be present, intentionally empty, or accidentally erased by the resolution.
Establish which before following the operation's configured empty-change policy.
Do not skip, allow-empty, or alter the todo list simply to advance the sequencer.

For editor, hook, or signing failures, inspect the error and whether Git advanced.
Fix a routine invocation problem within existing authority while preserving the
message and policy. Do not disable hooks or signing to obtain a passing command.

Abort, skip, quit, reset, stash manipulation, strategy/mainline changes, and history
or message edits have different effects on retained work. Use them only when the
task already authorizes that consequence; otherwise explain the concrete choice
and obtain the missing decision. Existing authorization need not be repeated.
Before recovery, verify the current operation and what work would be lost or
retained. Neither "always abort" nor "never abort" is a safe general rule.
