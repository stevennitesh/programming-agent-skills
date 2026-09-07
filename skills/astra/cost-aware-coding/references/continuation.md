# Continuation and evidence

Use [continuation handoffs](../../writing-for-agents/references/continuation-handoffs.md)
for receiving context, authority, state and proof. Add only model-allocation facts
needed to continue this execution; recording a handoff does not transfer custody.

Keep the accepted request, or existing canonical plan/ticket, as the requirements
and completion authority. Add routing observations to the existing handoff record
rather than maintaining another plan or requiring a separate artifact.

Record as applicable:

- Canonical request/plan identity and revision; repository, checkout, branch and
  observed HEAD; relevant dirty-state identity, including untracked files and
  known owners. A HEAD alone does not identify uncommitted work.
- Current execution owner, child/process identities and observed writer state;
  preserved partial patches and their owners; next authorized unit and its inputs.
  Include the reusable-agent roster and pending reviewer findings when relevant;
  distinguish implementation finished from review and acceptance complete.
- Selected and observed model/effort, reason for transfer, restrictions, observed
  budget use, implementation repairs and escalation consumed, review-repair rounds
  consumed, current phase, and recurring findings. Keep the two allowances separate.
- Candidate-bound checks and artifact locations, relevant environment, acceptance
  still missing, and which claims were independently inspected versus reported.

On resume, compare actual state with that record. Reconcile changed requirements,
dependency outputs, code, environment, and actor state before continuing affected
work. Invalidate only the routing and proof affected by drift. If ownership is
unknown, preserve the state and obtain quiescence before reassignment; never reset
or delete partial work merely to make a fresh attempt easier.
Before continuing pending repairs, read [Repair allowances](repairs.md) and
retain the recorded counters.

For returns that support continuation, adapt this example to the role and existing
workflow format. Omit irrelevant fields; preserve critical evidence without a
fixed word cap.

```text
OUTCOME: complete | partial | blocked | environment-failure | decision-needed
CHANGES: all in-scope additions, edits, deletions; candidate identity
CHECKS: exact command, result, tested state; evidence paths when needed
DEVIATIONS: none | difference from authorized scope or assumptions
OWNERSHIP: completed/stopped actor and processes, or unresolved writer state
LIMITS: unproved behavior, residual risk, unavailable model/cost telemetry
NEXT: remaining authorized action or required decision
```
