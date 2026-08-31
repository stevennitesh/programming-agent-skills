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

Start the worker only when the result says `ok: true`. The helper persists the
returned lane packet as `lane_manifest`. Pass the whole packet to the
worker. It includes absolute `worktree`, `runtime_root`, `temp_root`,
`cache_root`, `pytest_basetemp`, `pytest_cache`, and cleanup paths. The worker
must confirm the lane's `HEAD` and clean status before mutation, use the
worktree for every repository and Git command, and route temporary files,
tests, package caches, generated databases, and logs to the returned runtime
paths when the tool supports redirection. Record any off-contract runtime path;
it invalidates proof when it can change repository bytes, shared state,
cleanup, or the truth of proof.

One active writer owns each lane. Worktrees still share repository refs and
stash state, so concurrent workers must not stash, switch or rebase shared
branches, or mutate shared refs. Assign or serialize every writable resource
outside the checkout.

Before a worker return, record its exact proof commands and runtime paths, then
stop every background process and command session it started. A worker response
does not prove process exit.

## Inspect

Inspect after a worker returns, before replacement, before landing or cleanup,
and when resuming interrupted work:

```text
python <skill-dir>/scripts/lane_worktree.py inspect \
  --repo <repo> --root <worktree-root> --lane <path>
```

The result reports manifest validity, registration, `HEAD`, clean and
integration state, runtime directory presence, cleanup receipt state, known
checkout-local cache violations, and mechanical eligibility for landing or
cleanup. It cannot prove that an actor or command session stopped. The root
checks that separately. Never infer cancellation from silence and never start a
replacement while the prior actor may still write.

## Cleanup

After landing, pass only explicitly completed lanes:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --root <worktree-root> --completed <path>
```

After the root confirms actor quiescence, the helper removes only a direct
child of the exact external root when the lane is registered, clean, and
integrated into current repository `HEAD`. It also
supports an exact retry after Git removed the worktree but helper-owned state
remains. Dirty, unintegrated, active, or uncertain work stays in place.

Before unregistering a lane, the helper writes an authorization receipt beside
its state. If Git unregisters the worktree before filesystem cleanup finishes,
rerun the same command. The helper rechecks the exact repository, root, lane,
commit ancestry, and path, rejects reparse points, then removes residual lane
and state content. It removes the receipt last.

Cleanup retries only Windows sharing or access failures 32 and 5 on a bounded
250 ms, 500 ms, 1 second, and 2 second schedule. It may clear read-only
attributes only below the exact receipt-authorized lane or helper state. It
never changes ownership or ACLs. A persistent failure reports its phase, exact
path, errno, Windows error, retry count, registration, and path state.

The helper never forces removal, deletes branches, changes global Git config,
or chooses a lane on the caller's behalf.
