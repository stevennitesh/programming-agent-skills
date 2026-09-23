# Agent lanes

Read when concurrent workers need isolated writable checkouts or when helper-owned
lanes need inspection or cleanup. The bundled
`scripts/lane_worktree.py --help` owns the current command syntax; this reference
owns the operational contract.

## Prepare

Choose an allowed worktree root outside the repository. If safe placement is not
available, preserve the scope and serialize instead of weakening isolation.

The root alone performs helper mutations, sequentially. The helper owns only lanes
it prepared; it does not own host-created or unrelated worktrees.

Prepare each concurrent lane from the exact integration HEAD at dispatch.
Siblings selected together may share that base; a dependent starts from the newer
integration HEAD after its predecessors land.

Start a worker only after preparation succeeds. Pass the complete returned lane
packet and retain it until final cleanup verification. The worker uses the returned
checkout and runtime paths for repository commands, temporary files, caches,
generated databases, logs, and tests when those tools support redirection.

One active writer owns each lane. Git worktrees still share repository refs and
stash state, so concurrent workers must not stash, switch or rebase shared
branches, or mutate shared refs. Give every writable resource outside the checkout
an owner or serialize it.

A helper-lane worker returns a task-scoped commit and its focused proof. Before
return, it stops background processes and command sessions it started. The helper
cannot establish actor or process quiescence.

## Inspect and integrate

Inspect a lane after a worker return, before replacement, before landing or cleanup,
and when resuming interrupted work.

`ok: true` means the helper inspection ran successfully; it is not permission to
resume, land, or clean. Require
`mechanical.resume_or_land_eligible` before normal resume or landing and
`mechanical.cleanup_eligible` before cleanup.

For dirty or uncertain partial work, use [Recovery](recovery.md). Never infer
cancellation from silence or replace an actor that may still write.

The root lands accepted lane commits while preserving their ancestry. Do not
cherry-pick or squash helper-lane commits when doing so would break the ancestry
the cleanup contract uses. If integration has advanced since the lane base,
reassess semantic interference before landing even when Git can merge cleanly.

## Cleanup

Before cleanup, establish actor quiescence and retain evidence needed for unresolved
failures. Clean Git status does not make ignored or externally owned artifacts
disposable. The helper treats ignored entries as cleanup blockers; remove only
artifacts whose ownership and disposability are already established, then inspect
again.

Clean only named lanes that are clean, free of ignored artifacts, and integrated
into the current final candidate. Before unregistering a lane, the helper records
the lane's filesystem identity in its cleanup receipt when the platform exposes
one. A residual path is eligible for automatic retry only when it is absent or
still matches that recorded identity; a new object at the same pathname is
preserved. Only the current receipt schema is accepted. Older or malformed
receipts are preserved as unsupported recovery state rather than migrated or
overwritten automatically. Partial cleanup must retain the receipt and helper
state needed for recovery. Do not replace helper recovery with manual recursive
deletion.

After cleanup attempts, run the helper's cleanup verification over the complete
retained lane set. Finish only when it reports `finish_clean: true` for the
proved final integration HEAD.

For a version-controlled local tracker, use the final delivery HEAD H only after
[Tracker delivery](tracker-delivery.md) establishes that its C..H metadata changes
do not invalidate the code proof.

The helper never proves code semantics or actor liveness, forces removal, deletes
branches, changes global Git configuration, or chooses a lane for the caller.
