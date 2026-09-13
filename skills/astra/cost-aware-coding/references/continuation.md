# Continuation

Preserve in existing task context: agent ID, requested/observed settings,
assignment and stage, checkout/base and candidate, custody/writer state,
unresolved questions or proof, last processed return, and consumed allowances.
For planned delivery, also preserve the plan revision, whole-plan starting
comparison, completed checkpoint coverage/evidence, next boundary, and any selected
worker-guidance identity. Preserve correction counts per checkpoint and final-review
gate. A resume does not reset coverage or repair allowances.
No separate registry is required. Concurrent work follows
[Parallel recovery](../../parallel-implement/references/recovery.md).

On interruption or uncertain state, check native agent status and relevant
messages once. Reuse known context and evidence; do not reload the repository
while Sol owns it.

| Observed state | Action |
| --- | --- |
| Running with custody | Resume [waiting](../SKILL.md#2-assign-sol-and-wait); do not request routine progress. |
| Idle with an unanswered question | Answer using followup_task; explicitly grant custody if previously released. |
| Idle/interrupted with custody and no candidate return | Resume the same assignment with followup_task after resolving the interruption. |
| Candidate returned with release | Classify evidence and review or repair; process the return once. |
| Prerequisite-only return with release | Resolve the reported prerequisite, then grant custody to resume the same assignment; no attempt is charged. |
| You hold custody for unfinished review | Reconcile candidate identity and continue review. |
| Agent unavailable, errored, or custody uncertain | Establish writer/process state and reconcile custody before repository access or replacement. |

Follow runtime cleanup instructions for finished/idle/errored children, retaining
their IDs for supported follow-ups. An interrupt request or idle status does not
prove subprocesses stopped. If that cannot be established, report the blocker;
do not create a competing writer. When an agent cannot be resumed, transfer a
compact handoff to a replacement only after custody is safe; preserve allowances.

A stale assignment cannot override newer custody. Record a return as received
before review and processed afterward, so interruption resumes unfinished review.
Repeated messages must not duplicate review, repair, or attempt charges.
Ending your turn does not schedule a wakeup; resume from these states when the
user continues you. Native communication does not override action permissions.
