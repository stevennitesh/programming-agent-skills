# Repair allowances

Read when a returned candidate fails acceptance or review requires corrections.
Resolve missing requirements, invalid acceptance criteria, and environment faults
at their source instead of spending a model escalation.

| State | Next action |
| --- | --- |
| Before review, with the stronger attempt unused, the implementer returns blocked with concrete evidence that its current reasoning effort is insufficient | Skip the focused repair. Recommend a user-applied effort increase on the same Sol task: High by default, or XHigh when justified; then allow one stronger attempt. |
| First implementation return fails acceptance | The same implementer gets one focused repair. |
| Focused repair return fails because implementation reasoning is insufficient | Recommend a user-applied effort increase on the same Sol task: High by default, or XHigh when justified; then allow one stronger attempt. |
| Failure comes from requirements, design, or environment | Resolve it at its source, then continue within the remaining allowance for the current stage; suggest raising your effort only if that decision needs more reasoning. |
| Stronger return fails or recovery is unavailable | Preserve the candidate and request a revised route. |
| Review returns required corrections | The current implementer repairs one batch and returns it to the same Astra reviewer; two repair rounds total. |
| Required corrections remain after two returned repair batches | Preserve the candidate and request more rounds or a revised route. |

An implementation attempt or review-repair round is consumed when the implementer
returns its candidate as ready or blocked. Editing, debugging, and test runs before
that return belong to the same attempt. A review-repair round begins with one batch
of required findings and includes the implementer's checks and the same reviewer's
follow-up when a candidate is ready. The initial review and optional suggestions
do not consume a round.

Once review begins, returned corrections use only the shared review-repair
allowance. Failed correction checks do not open implementation recovery. If a
review repair needs higher Sol effort, the user-applied change uses the next
remaining review-repair round rather than creating another allowance.

The user changes an existing task's effort; that action accepts the escalation.
Reuse the same Sol task and its context without claiming that cached computation
is preserved. Changing models or creating another implementer requires an accepted
revised route. For later routine corrections, suggest returning Sol to Medium.

Track implementation recovery per coherent work unit and share the two
review-repair rounds across the integrated candidate. Replacement, repartitioning,
or a new lane does not reset either allowance. For concurrent implementation,
[Parallel recovery](../../parallel-implement/references/recovery.md) owns the
mechanics.
Its agreed worker transport determines how an effort increase can be applied.
The same-app-task instructions above apply only where that mechanism is available;
otherwise request a revised recovery route without resetting the allowance.
