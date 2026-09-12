# Continuation

For concurrent execution, resume from
[parallel-implement's run record](../../parallel-implement/SKILL.md#2-isolate-and-dispatch)
and follow [Parallel recovery](../../parallel-implement/references/recovery.md).
Preserve the accepted worker transport, model allocations, ownership restrictions,
budget constraints, integrated review state, and consumed repair allowances with
that record. Reconcile actual actors and lane custody before dispatch or mutation;
the single-implementer instructions below apply only to serial execution.

Preserve only:

- the current implementer task, host, model, and effort;
- checkout, baseline, candidate, custody owner, and writer state;
- current assignment and stage, accepted outcome, last return, unresolved findings,
  and consumed repair allowances.

On resume, first reconcile the task identity, custody owner, and writer state with
the actual task status. If Sol still owns custody, wait or answer only.
If custody is uncertain, preserve the work and establish that writers stopped
before repository inspection or reassignment. After Sol releases custody and
you acquire it, reconcile the checkout and candidate, then reuse the existing
implementer for the same candidate.
