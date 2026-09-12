# Continuation

For concurrent execution, resume from
[parallel-implement's run record](../../parallel-implement/SKILL.md#2-isolate-and-dispatch)
and follow [Parallel recovery](../../parallel-implement/references/recovery.md).
Preserve the accepted worker transport, model allocations, ownership restrictions,
budget constraints, integrated review state, and consumed repair allowances with
that record. Reconcile actual actors and lane custody before dispatch or mutation;
the single-implementer instructions below apply only to serial execution.

Preserve only:

- lead and implementer task IDs/hosts, accepted model and effort;
- authorized communication scope and any unresolved approval rejection;
- checkout, baseline, candidate, custody owner, and writer state;
- current assignment ID and stage, accepted outcome, last processed return, unresolved findings,
  and consumed repair allowances.

Use existing task context; do not reload skills, plans, or repository files merely
because a new turn began. Normal matching callbacks follow the main workflow.

## When the user resumes you after interruption

Check the known Sol task's current status and latest relevant message/return once.
App closure or idle status alone does not establish stopped processes or release.

| Observed state | Your next action |
| --- | --- |
| Sol is running with custody | Leave it working and end your turn; await its message. |
| Sol is interrupted or idle with custody, without a candidate return | Resume the same assignment by message, preserving its allowance. |
| Sol has an unanswered question | Answer it; obtain release first if repository inspection is necessary. |
| Sol returned a candidate and released custody | Process an unhandled return through acceptance classification and review or recovery. |
| You already hold custody for review | Reconcile the candidate and continue the unfinished review. |
| Custody or assignment is uncertain | Reconcile by message before repository access or reassignment. |

Sol's initial assignment carries its receiver-side recovery rules. A user can
resume Sol directly while it retains custody without involving you. If it has
released custody, it requests a new grant; do not grant while your repository
activity or other writers remain active.

## Delayed or duplicate messages

Use sender task, assignment ID, and recorded stage to identify the expected
return. A question is not a candidate return. Record receipt before review and
completion of processing afterward so interruption resumes unfinished review
rather than skipping it. A repeated return must not start a second review,
repair dispatch, or allowance charge. No acknowledgement message is required.

A stale assignment cannot override newer custody. Reconcile a mismatched return
with the known task's latest state before acting; preserve new evidence without
treating it as permission. For uncertain delivery, inspect the latest task return
instead of blindly redispatching implementation. No background recovery is implied
after a turn ends; unavailable callbacks require completion waits or a user resume.
If message approval was rejected, inspect the saved question or handoff and the
exact rejection. Explain the destination and information involved, then request
informed approval in the sending task when the runtime requires direct user input;
do not relay an approval claim as a substitute or retry around the rejection.
A failed question delivery is not an implementation failure and does not change
custody. Until the channel is restored, treat automatic resumption as unavailable.
