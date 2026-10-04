# Recovery

Read for interrupted, failed, dirty, conflicting, or otherwise off-contract
parallel work. Reconstruct the run from actual candidate, lifecycle-owner, process,
and applicable tracker state before resuming. Retained host identities or helper
packets identify owned lanes; directory names alone do not.

When cost-aware-coding also governs execution, use its
[Recovery](../../cost-aware-coding/references/recovery.md) contract for model-route
failure attribution and worker replacement. Parallel lane custody, integration
provenance, and composed proof still belong here.

## Recover the actual state

- **Silence or missed checkpoint:** inspect actor/process and lane state. Silence
  is not cancellation.
- **Requirement, permission, environment, or acceptance problem:** resolve it at
  its owner rather than treating it as worker incapability.
- **Runtime, dependency, data, or permission drift:** repeat the affected readiness
  checks in [Agent lanes](agent-lanes.md) before resuming implementation. Verify
  effective paths, input versions, and write destinations; re-evaluate earlier
  evidence when its inputs or environment changed.
- **Helper command interrupted:** inspect its active-command marker and command
  evidence, then establish process quiescence. Preserve needed output before
  removing the marker to acknowledge recovery. A stale PID alone does not prove
  the command tree has stopped. Rerun the affected checks; missing readiness
  metadata does not invalidate an otherwise supported lane manifest.
- **Worker replacement:** stop the prior actor and attached writers, confirm
  quiescence, inspect preserved work, then transfer exclusive custody. Never run
  two writers against the same lane.
- **Dirty or off-contract return:** preserve it under exclusive custody. Repair
  with the original worker when useful, or transfer it only after confirmed
  termination. Do not reset or invent a commit merely to regain eligibility.
- **Integration advanced:** reassess semantic and proof interference. Incorporate
  the current integration candidate in the lane and rerun affected proof when
  needed; the original lane base remains provenance.
- **Active conflict:** preserve the conflict state, stop competing integration
  writers, resolve the intended behaviors within authority, then recheck the
  composition. A clean merge is not by itself a correct resolution.
- **Host preparation or cleanup partially failed:** inspect the host operation and
  returned worktree identity, checkout, and resources. Recover through that host's
  supported lifecycle without creating a duplicate or taking over an unrelated
  worktree. Preserve state when its identity or ownership cannot be established.
- **Helper preparation or cleanup partially failed:** inspect registration,
  manifest, receipt, checkout, and runtime state. Use the helper's supported retry
  only when its evidence says the residual is eligible; otherwise preserve it.
  For named runs, use `status --run` to recover the complete lane inventory and
  retain that run identity for cleanup and final verification. A `preparing`
  inventory entry is not evidence that worktree creation succeeded.
- **Final integration HEAD changed:** prior cleanup eligibility and proof tied to
  the older candidate must be reconsidered.

The helper cannot observe actor liveness, code semantics, forgotten lane packets,
or unrelated concurrent writers. Host lifecycle status likewise does not prove
that worker-owned processes have stopped. The root owns one serialized stream of
integration and coordinates lifecycle mutations with each lane's owner.

If the host cannot establish isolated checkout placement or exclusive write
ownership, preserve recoverable state and continue serially instead.

A pending cleanup receipt remains unfinished work. Follow
[Agent lanes](agent-lanes.md#cleanup), and [Helper lanes](helper-lanes.md#cleanup)
for helper receipts, until the eligible retry completes or residual state is
preserved and reported. Shared durable data remains outside lane cleanup ownership.
