# Agent Lanes

Task context and checkout isolation are separate facts. Isolate concurrent
writers; do not add a worktree for a serial worker merely for uniformity.

## Prepare And Start

Give one serial writer exclusive custody of the clean integration checkout at
the exact base. The root performs no repository or Git mutation until Return.

Give every concurrent writer a distinct helper-created worktree at the exact
base:

```text
python <skill-dir>/scripts/lane_worktree.py prepare \
  --repo <repo> --root <worktree-root> --base <sha> --name <lane-name>
```

The helper creates or reuses the lane, checks registration, exact `HEAD`, clean
status, and basic Git operation, creates checkout-external pytest temp and cache
roots, and runs a quick pytest collection smoke. Start the worker only when the
single result says `ok: true`; otherwise preserve the lane and report the
reason. Assign one active writer per worktree.

Send the selected runtime profile and plain assignment directly to one fresh
worker. The accepted start request is enough launch evidence when resolved
telemetry is unavailable. Do not create a dispatch record, sealed brief,
receipt, or Return schema.

## Await And Verify

Wait for the started worker. A missed checkpoint triggers inspection, not a
duplicate start. Reconcile its task state, checkout, `HEAD`, status, commit, and
claim before replacing it. Preserve dirty or uncertain work.

Treat the worker's prose Return as evidence. Verify the actual worktree, base,
commit, diff, scope, and proof before landing. A pre-landing localized
correction may return to the same worker if its lane is still safe.

Formal review is read-only and needs no writer worktree.

## Cleanup

At graph end, remove all safe completed lanes:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --root <worktree-root> [--completed <path> ...]
```

When the worktree limit is reached, add `--oldest` to remove the oldest safe
completed lane first. Pass only explicitly completed worktrees. The helper
removes only registered lanes contained by the explicit root whose `HEAD` is
already integrated and whose checkout is clean. Dirty, active, uncertain, and
unintegrated lanes remain preserved; a capacity-blocked result means no new
concurrent worker may start.

The helper never forces removal, deletes branches, changes global Git config,
or recursively deletes worker-writable temp state.
