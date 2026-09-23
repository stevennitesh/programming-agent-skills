# Recovery

Use when delegated implementation is interrupted, blocked, off-contract, or cannot
safely continue. Preserve actual candidate and custody state before choosing the
next action.

## Reconcile state first

Establish the worker model/effort when relevant, assignment, checkout and base,
current candidate, writer/subprocess state, custody owner, last substantive return
or question, and required proof still missing. For checkpointed delivery, also
preserve the active checkpoint and its accepted coverage.

Do not create a competing writer while the previous worker may still mutate the
checkout. Idle, interrupted, unavailable, or timed-out status does not prove writer
quiescence or custody release.

## Resolve the actual cause

- **Blocking question:** answer the reserved decision and renew custody if needed.
- **Missing prerequisite, permission, environment, or contradictory acceptance:**
  resolve it at its owner; do not spend stronger-model tokens on a non-model
  problem.
- **Locally correctable implementation failure:** return focused findings to the
  same worker when its retained context makes repair cheaper than reconstruction.
- **Worker/runtime interruption:** resume the same assignment when custody and
  candidate state remain known and safe.
- **Reasoning-capability failure:** increase effort or move to the stronger GPT-6
  route defined by [Model policy](model-policy.md) only when evidence indicates
  additional reasoning is likely to change the result.
- **Worker unavailable:** establish writer quiescence, preserve the candidate, then
  transfer a compact state packet to the accepted replacement.
- **Custody uncertain:** stop before repository mutation until ownership and writer
  state are reconciled.

There is no universal repair-round count. Bound recovery by the user's budget,
remaining value of worker context, likelihood that another attempt changes the
result, and the lead-token cost of reconstructing implementation state.

## Preserve continuity without lead-context churn

A resume does not reset accepted scope, candidate identity, completed proof, or
the active checkpoint. Process repeated returns once and do not redo valid
candidate-bound review or verification merely because execution was interrupted.

When replacement is necessary, transfer the assignment, actual candidate, failed
or missing proof, decisive observations, custody state, and remaining work. Do not
load obsolete conversation history into Astra merely to rebuild a transcript for
the replacement.

Finish recovery only when one actor again has clear write custody or the work is
safely preserved as blocked with the next required decision explicit.
