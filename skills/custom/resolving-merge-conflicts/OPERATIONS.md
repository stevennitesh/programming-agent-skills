# Conflict operations

Load only the row for the observed operation and the rows for special conflict
types actually present. `SKILL.md` owns scope, mutation, proof, and completion.

## Operation roles

| Operation | Goal | Stage 1 / 2 / 3 | Native finish |
| --- | --- | --- | --- |
| Merge | Integrate histories | merge base / current target / merged side | `git merge --continue` |
| Rebase | Replay a commit onto the rebased target | replay base / so-far rebased target / commit being replayed | `git rebase --continue` |
| Cherry-pick | Apply one selected commit delta | selected parent or mainline / current target / selected commit | `git cherry-pick --continue` |
| Revert | Apply the inverse of one selected commit | selected commit / current target / selected parent or mainline | `git revert --continue` |
| Unmerged, unknown | Reconcile only from proven object and intent roles | inspect objects without assigning side labels | none |

Never use bare `ours` or `theirs` as intent. Map stages to their operation roles
first. A stage may be absent in add/add, modify/delete, root-commit, and related
cases. Rename conflicts may span old and new paths. Reconcile the observed path
set rather than assuming one file with three stages.

## Special conflict types

| Type | Resolve and check |
| --- | --- |
| Add, delete, rename, or path topology | Prove intended presence and name, update live references and registrations, and retain an old path only for a supported compatibility need. |
| Generated or filtered artifact | Resolve the authoritative source and regenerate with the repository command when available. If regeneration changes paths outside scope, stop rather than admitting them silently. |
| Binary, executable mode, or symlink | Compare object identity and modes, then inspect the resulting artifact and staged representation. |
| Submodule gitlink | Resolve the intended commit, verify the exact gitlink object, and leave fetching objects or changing the nested checkout to separate authority. |
| `rerere`, mergetool, or automatic merge result | Inspect the worktree and staged content as a candidate. An empty unmerged index does not prove the resolution or authorize continuation. Do not change tool configuration or caches without a separate request. |

## Exceptional operation choices

An empty change, hook or editor stop, signing problem, new conflict, or failed
continuation is observed state, not permission to improvise recovery. Abort,
skip, quit, reset, stash, strategy changes, todo or message changes, hook
bypass, and allow-empty handling each require an explicit request after their
consequence is known.
