# Repair allowances

Read when an implementation candidate fails acceptance, execution fails, new
evidence invalidates the approach, or review requires corrections. These rules
apply to direct and delegated work. Use [Model policy](model-policy.md) for
permitted recovery routes.

## Implementation recovery

Classify failures before spending another attempt. Resolve missing context,
environment faults, or invalid acceptance at their source. Track two separate
repair allowances per coherent work unit: implementation recovery and
review repairs below. Preserve both across interruptions and agent replacements.
An attempt is a candidate submitted for acceptance, whether returned by a worker
or implemented by the parent, followed by its acceptance checks. Local edits and
test commands are not separate attempts; failed acceptance cannot be relabeled
as internal work to evade the limit. If evidence invalidates the approach or acceptance
criteria, pause dependent work and resolve the affected decision with the planner
or user as appropriate. Reuse unaffected work; replanning does not reset counters.

Before review, use this implementation sequence: first implementation attempt,
integration/acceptance checks, one focused repair by the same implementer if those
checks fail, then repeat the affected checks. If they fail again, assign one recovery
attempt to a permitted model/effort suited to the demonstrated weakness, using the
model policy rather than a fixed ladder; increasing effort counts as that
escalation. The successful recovery agent becomes the implementer for subsequent
review repairs. If recovery fails or no stronger permitted route exists, preserve
the work and ask the user how to proceed. Do not reset this allowance by changing
symptoms or actors. Missing decisions must be resolved before dependent retries.
Follow provider retry and repository recovery rules; outages do not prove model
incapability. Report repeated environment failures without new evidence rather
than looping outside the repair allowance.

## Review repairs

Optional suggestions alone do not block completion or consume repair rounds.
Use change-review's governing acceptance rules; do not relabel required
corrections as optional to pass the gate.

Review repairs allow two rounds by the current implementer (the successful recovery
agent, if used). Each round is one returned repair attempt for the current batch
of findings requiring correction, followed by affected checks and the same reviewer's recheck when checks
pass. A failed repair or required check consumes that round; carry it into the
remaining round. Review repairs do not reopen implementation recovery or grant its
automatic escalation. Agent replacement does not reset either counter.

If required corrections or required checks remain unresolved after two rounds, report them
and ask for additional review-repair rounds. If the same bug keeps recurring,
also propose a more capable implementer and request authorization for that route
and further repair/review work. Do not silently start a third round or escalate
review repairs.

For concurrent implementation, also read
[Parallel recovery](../../parallel-implement/references/recovery.md) for
per-item implementation accounting, integrated review rounds, and safe custody.
