# Repair allowances

Read when an implementation candidate fails acceptance, execution fails, new
evidence invalidates the approach, or review requires corrections. These rules
apply to direct and delegated work. Use [Model policy](model-policy.md) for
permitted recovery routes.

## Implementation recovery

Classify failures before spending another attempt. Resolve missing context,
environment faults, or invalid acceptance at their source. Track implementation
recovery per coherent work unit and final review repairs against the integrated
candidate, for both sequential and concurrent implementation.
An attempt is a candidate submitted for acceptance, whether returned by a worker
or implemented by the parent, followed by its acceptance checks. Local edits and
test commands are not separate attempts; failed acceptance cannot be relabeled
as internal work to evade the limit. If evidence invalidates the approach or acceptance
criteria, pause dependent work and resolve the affected decision with the planner
or user as appropriate. Reuse unaffected work.

## Allowed transitions

| State | Next action |
| --- | --- |
| Initial implementation fails acceptance | One focused repair by the same implementer, then affected checks |
| That repair fails acceptance | One stronger permitted recovery attempt suited to the demonstrated weakness |
| Recovery fails or no stronger permitted route exists | Preserve work and ask for a revised route |
| Review requires corrections | Affected units' current implementers repair the batch, followed by composed checks and the same reviewer's recheck when checks pass; two rounds total across all implementers |
| Required corrections or checks remain after two review rounds | Ask for more rounds; for recurring bugs also propose and request a stronger implementer and further work |

Increasing effort counts as implementation escalation. The successful recovery
actor becomes the current implementer. When the accepted plan assigns root coordination only, the root retains
coordination and acceptance; product repairs stay delegated. Follow provider retry and repository
recovery rules; outages do not establish model incapability. Report repeated
environment failures without new evidence instead of looping indefinitely.

Before review, attribute an integration failure to an existing coherent work unit
and use its remaining implementation-recovery allowance. Create an integration
unit only when the failure has no existing owner; never rename or split failed
work to obtain fresh attempts. During review, corrections use the integrated
candidate's shared review allowance.

Before dispatching a cross-unit correction, assign one accountable implementer
and explicit write scope under accepted ownership and custody rules. Preserve
affected units' counters; reassignment or reslicing does not reset them.

Each review round covers one submitted batch of required corrections, repairs by
the affected units' current implementers, composed checks, and the same reviewer's
recheck when checks pass. Localized findings return to their unit's current
implementer but consume this shared allowance; neither each finding nor each
implementer receives separate rounds.
A failed repair or required check consumes the round. Review repairs do not reopen
implementation recovery or allow automatic escalation. Optional suggestions alone
do not block completion or consume rounds; use change-review's acceptance rules
without relabeling required corrections as optional. Preserve both counters across
changed symptoms, replanning, and replacement; further rounds require authorization.

For concurrent implementation, also read
[Parallel recovery](../../parallel-implement/references/recovery.md) for
lane-specific recovery and safe custody.
