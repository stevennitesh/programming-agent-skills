# Recovery

Read for interrupted, failed, dirty, conflicting, or otherwise off-contract
parallel work. Reconstruct the run from actual candidate, helper, process, and
applicable tracker state before resuming. Retained lane packets identify owned
lanes; directory names alone do not.

When cost-aware-coding also governs execution, use its
[Recovery](../../cost-aware-coding/references/recovery.md) contract for model-route
failure attribution and worker replacement. Parallel lane custody, integration
provenance, and composed proof still belong here.

## Recover the actual state

- **Silence or missed checkpoint:** inspect actor/process and lane state. Silence
  is not cancellation.
- **Requirement, permission, environment, or acceptance problem:** resolve it at
  its owner rather than treating it as worker incapability.
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
- **Prepare or cleanup partially failed:** inspect helper registration, manifest,
  receipt, checkout, and runtime state. Use the helper's supported retry only
  when its evidence says the residual is eligible; otherwise preserve it.
- **Final integration HEAD changed:** prior cleanup eligibility and proof tied to
  the older candidate must be reconsidered.

The helper cannot observe actor liveness, code semantics, forgotten lane packets,
or unrelated concurrent writers. The root owns one serialized stream of
integration and helper mutations.

If the host cannot establish isolated checkout placement or exclusive write
ownership, preserve recoverable state and continue serially instead.

A pending cleanup receipt remains unfinished work. Follow
[Agent lanes](agent-lanes.md#cleanup) until the eligible retry completes or the
residual state is preserved and reported.
