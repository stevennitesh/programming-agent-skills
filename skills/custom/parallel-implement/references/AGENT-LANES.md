# Agent lanes

Use this reference when concurrent workers need checkout isolation or when
helper-owned lanes need inspection or cleanup. The bundled
`scripts/lane_worktree.py --help` owns current command syntax.

## Prepare

Create each concurrent lane from the exact integration `HEAD` at dispatch.
Siblings selected together may share that base; a dependent starts from the newer
integration `HEAD` after its predecessors land.

Start a worker only after preparation succeeds. Pass the complete returned lane
packet and retain it until final cleanup verification. The worker uses the returned
checkout and runtime paths for repository commands, temporary files, caches,
generated databases, logs, and tests when those tools support redirection.

One active writer owns each lane. Git worktrees still share repository refs and
stash state, so concurrent workers must not stash, switch or rebase shared
branches, or mutate shared refs. Assign or serialize every writable resource
outside the checkout.

A lane reused for another worker must still match its expected base, have a clean
Git worktree, and contain no ignored artifacts. Before return, the worker stops
background processes and command sessions it started. The helper does not prove
actor or process quiescence.

## Inspect and integrate

Inspect after a worker return, before replacement, before landing or cleanup, and
when resuming interrupted work.

`ok: true` means inspection completed; it is not permission to resume, land, or
clean. Require `mechanical.resume_or_land_eligible` before normal resume or
landing and `mechanical.cleanup_eligible` before cleanup.

Ignored files are reported explicitly and make resume, landing, and cleanup
ineligible until their ownership and disposability are resolved. The helper does
not silently discard ignored artifacts.

The root lands accepted lane commits while preserving ancestry used by cleanup.
Do not infer semantic independence from a clean Git merge.

## Cleanup

After actor quiescence, clean only named lanes that are clean, free of ignored
artifacts, and integrated into the current final candidate.

Before unregistering a lane, the helper writes the current cleanup-receipt schema
with the lane commit, authorization HEAD, and filesystem identity when the
platform exposes one. A residual path is eligible for automatic retry only when
it is absent or still matches that identity. A new object at the same pathname is
preserved.

Only the current receipt schema is accepted. Older or malformed receipts remain
unsupported recovery state and are not migrated or overwritten automatically.

Partial cleanup retains the receipt and helper state needed for retry. Do not
replace helper recovery with manual recursive deletion.

After cleanup attempts, run cleanup verification over every retained lane and
finish only when `finish_clean: true` is reported for the proved final
integration `HEAD`.

The helper never proves code semantics or actor liveness, overrides Git repository
trust, forces removal, deletes branches, changes global Git configuration, or
chooses a lane for the caller.
