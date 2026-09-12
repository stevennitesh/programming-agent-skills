# Repair allowances

Read when a returned candidate fails acceptance or review requires corrections.
Resolve missing requirements, invalid acceptance criteria, and environment faults
at their source instead of spending a model escalation. Resolving an external
fault does not renew exhausted allowances: another repair requires an accepted
revised route. Rechecking an unchanged candidate need not create a repair attempt.

| State | Next action |
| --- | --- |
| Before review, with the stronger attempt unused, the implementer returns blocked with concrete evidence that its current reasoning effort is insufficient | Skip the focused repair. Propose a stronger Sol replacement: High by default, or XHigh when justified; after acceptance, allow one stronger attempt. |
| First implementation return fails acceptance | The same implementer gets one focused repair. |
| Focused repair return fails because implementation reasoning is insufficient | Propose a stronger Sol replacement: High by default, or XHigh when justified; after acceptance, allow one stronger attempt. |
| Failure comes from requirements, design, or environment | Resolve it at its source, then continue within the remaining allowance for the current stage; suggest raising your effort only if that decision needs more reasoning. |
| Stronger return fails or recovery is unavailable | Preserve the candidate and request a revised route. |
| Review returns required corrections | The current implementer repairs one batch and returns it to the same Astra reviewer; two repair rounds total. |
| Required corrections remain after two returned repair batches | Preserve the candidate and request more rounds or a revised route. |

An implementation attempt or review-repair round is consumed when the implementer
returns its candidate as ready or blocked. Editing, debugging, and test runs before
that return belong to the same attempt. A review-repair round begins with one batch
of required findings and includes the implementer's checks and the same reviewer's
follow-up when a candidate is ready. The initial review and optional suggestions
do not consume a round. A clarification question, interruption, or resume is not
a candidate return and consumes no attempt. Retransmitting a return does not
consume another attempt; preserve the original accounting.

Once review begins, returned corrections use only the shared review-repair
allowance. Failed correction checks do not open implementation recovery. If a
review repair needs higher Sol effort, the accepted replacement uses the next
remaining review-repair round rather than creating another allowance.

Native followup_task cannot change an existing agent's model or effort. Obtain
acceptance for the stronger setting/replacement unless already authorized. After
the old agent releases custody and its writers stop, spawn the replacement with
explicit settings and a compact candidate/failure handoff. Do not imply its
context or prompt cache transfers automatically. Retire the old writer and reuse
the replacement for subsequent corrections. Your own model/effort changes remain
user actions. If the runtime cannot provide the accepted route, report the limit.

Track implementation recovery per coherent work unit and share the two
review-repair rounds across the integrated candidate. Replacement, repartitioning,
or a new lane does not reset either allowance. For concurrent implementation,
[Parallel recovery](../../parallel-implement/references/recovery.md) owns mechanics;
verify its worker transport supports the accepted recovery route.
