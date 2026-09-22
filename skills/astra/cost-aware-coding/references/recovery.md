# Recovery

Use when delegated implementation is interrupted, blocked, off-contract, or cannot
safely continue. Preserve actual candidate and custody state before choosing the
next action.

## Reconcile state first

Establish the worker identity, assignment, checkout and base, current candidate,
writer/subprocess state, custody owner, last substantive return or question, and
required proof still missing. For checkpointed delivery, also preserve the active
checkpoint and its accepted coverage.

Do not create a competing writer while the previous worker may still mutate the
checkout. Idle, interrupted, unavailable, or timed-out status does not by itself
prove writer quiescence or custody release.

## Resolve the actual cause

- **Blocking question:** answer the reserved decision and renew custody if it had
  been released.
- **Missing prerequisite, permission, environment, or contradictory acceptance:**
  resolve it at its owner; do not treat it as worker incapability.
- **Locally correctable implementation failure:** return focused findings to the
  same worker when its context remains useful.
- **Worker/runtime interruption:** resume the same assignment when custody and
  checkout state are still known and safe.
- **Worker unavailable or demonstrated capability failure:** establish writer
  quiescence, inspect the preserved candidate, then transfer the actual state to
  an accepted replacement route.
- **Custody uncertain:** stop before repository mutation until ownership and
  writer state are reconciled.

There is no universal repair-round count. Keep recovery bounded by the user's
explicit budget, remaining value of the worker's context, evidence that another
attempt can change the result, and the cost of route replacement.

Changing worker route does not solve incomplete requirements, broken environments,
or invalid acceptance criteria. Resolve those first.

## Preserve continuity without ceremony

A resume does not reset accepted scope, candidate identity, completed proof, or
the active checkpoint. Process repeated returns once and do not redo valid
candidate-bound review or verification merely because execution was interrupted.

When replacement is necessary, transfer a compact packet containing the assignment,
actual candidate, failed or missing proof, decisive observations, custody state,
and remaining work. Do not transfer obsolete conversation history as policy.

Finish recovery only when one actor again has clear write custody or the work is
safely preserved as blocked with the next required decision explicit.
