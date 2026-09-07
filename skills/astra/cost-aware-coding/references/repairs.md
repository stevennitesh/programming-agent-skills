# Repair allowances

Read when an implementation candidate fails acceptance, execution fails, new
evidence invalidates the approach, or review requires corrections. These rules
apply to direct and delegated work. Use [Model policy](model-policy.md) for
permitted recovery routes.

## Implementation recovery

Classify failures before spending another attempt. Resolve missing context,
environment faults, or invalid acceptance at their source. Track two separate
repair allowances per coherent work unit: implementation recovery and
review repairs below.
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
| Review requires corrections | Current implementer repairs the batch, runs affected checks, then the same reviewer rechecks when checks pass; at most two rounds |
| Required corrections or checks remain after two review rounds | Ask for more rounds; for recurring bugs also propose and request a stronger implementer and further work |

Increasing effort counts as implementation escalation. The successful recovery
actor becomes the current implementer. When the accepted plan assigns root coordination only, the root retains
coordination and acceptance; product repairs stay delegated. Follow provider retry and repository
recovery rules; outages do not establish model incapability. Report repeated
environment failures without new evidence instead of looping indefinitely.

Each review round is one submitted repair for the current batch of required
findings, followed by affected checks and the reviewer's recheck when checks pass.
A failed repair or required check consumes the round. Review repairs do not reopen
implementation recovery or allow automatic escalation. Optional suggestions alone
do not block completion or consume rounds; use change-review's acceptance rules
without relabeling required corrections as optional. Preserve both counters across
changed symptoms, replanning, and replacement; further rounds require authorization.

For concurrent implementation, also read
[Parallel recovery](../../parallel-implement/references/recovery.md) for
per-item implementation accounting, integrated review rounds, and safe custody.
