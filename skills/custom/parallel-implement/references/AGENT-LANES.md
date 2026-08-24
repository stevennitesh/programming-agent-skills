# Agent lanes

Use this reference when concurrent workers need checkout isolation or when
their lanes need cleanup.

## Prepare

Create each concurrent lane from integration `HEAD` at dispatch. Siblings
selected together share that base. A later dependent lane uses the newer
integration `HEAD` after its predecessors land:

```text
python <skill-dir>/scripts/lane_worktree.py prepare \
  --repo <repo> --root <worktree-root> --base <sha> --name <lane-name>
```

Start the worker only when the result says `ok: true`. Pass it the returned
absolute `worktree`, `temp_root`, `pytest_basetemp`, and `pytest_cache`. The
worker must confirm the lane's `HEAD` and clean status before mutation and use
that path for every repository and Git command.

One active writer owns each lane. Worktrees still share repository refs and
stash state, so concurrent workers must not stash, switch or rebase shared
branches, or mutate shared refs. Assign or serialize every writable resource
outside the checkout.

If a worker stops or disappears, inspect its actor state, lane, `HEAD`, status,
and commit before resuming or replacing it. Never infer cancellation from
silence and never start a replacement while the prior actor may still write.

## Cleanup

After landing, pass only explicitly completed lanes:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --root <worktree-root> --completed <path>
```

The helper removes only a direct child of the exact external root when the lane
is registered, clean, and integrated into current repository `HEAD`. It also
supports an exact retry after Git removed the worktree but helper-owned state
remains. Dirty, unintegrated, active, or uncertain work stays in place.

Before unregistering a lane, the helper writes an authorization receipt beside
its state. If Git unregisters the worktree before filesystem cleanup finishes,
rerun the same command. The helper rechecks the exact repository, root, lane,
commit ancestry, and path, rejects reparse points, then removes residual lane
and state content. It removes the receipt last.

The helper never forces removal, deletes branches, changes global Git config,
or chooses a lane on the caller's behalf.
