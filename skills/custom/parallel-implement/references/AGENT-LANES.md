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
roots, and runs a quick pytest collection smoke when the checkout declares
pytest through root configuration or tracked Python tests. Start the worker only when
the single result says `ok: true`. On failed preflight, the helper removes a
newly created lane only after rechecking exact `HEAD` and cleanliness; it
preserves a reused, changed, dirty, or uncertain lane and reports the reason.
Pass successful temp and cache paths to the worker and assign one active writer
per worktree.

Send the selected runtime profile and plain assignment directly to one fresh
worker. The accepted start request is enough launch evidence when resolved
telemetry is unavailable.

## Await And Verify

Wait for the started worker. A missed checkpoint triggers inspection, not a
duplicate start. Reconcile its task state, checkout, `HEAD`, status, commit, and
claim before replacing it. Preserve dirty or uncertain work.

Treat the worker's prose Return as evidence. Verify the actual worktree, base,
commit, diff, scope, and proof. A serial integration-checkout commit is a
provisional direct landing that the root accepts or rejects after read-back; a
concurrent-lane commit is verified before landing. A localized correction may
return to the same worker if its lane is still safe.

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
concurrent worker may start. Removing a safe lane also removes only its
helper-owned temp and cache state under that explicit root. Every supplied
completed path must belong to that exact root and be a registered worktree; the
helper accepts only the direct-child layout created by `prepare` and rejects an
unaccounted path. If state cleanup or worktree removal fails, the helper reads
back registration and path state, reports the exact remaining custody plus
whether disposable lane state was removed, then tries another safe lane in
capacity mode.

The helper never forces removal, deletes branches, or changes global Git
config.
