# Long-running instructions

Use this reference when an instruction governs a genuinely long autonomous run and
continuation, steering, predictable permissions, or durable progress can
materially change behavior. Apply only the branches the receiving task needs.

## Name the finish and the escape

Pair the finish line with an escape condition: state both what "done" means and the
concrete uncertainty, failure, missing access, or authority condition that should
stop the receiver for input. Do not make the escape so broad that ordinary
implementation choices become approval gates.

A long run should not infer completion from elapsed effort, one green check, an
intermediate phase, or a progress summary when the stated outcome remains
unfinished.

## Surface only already-granted authority

When the task predictably requires a separately authorized effect, permission, or
sensitive operation, make that authority explicit up front only when the user or
governing source has actually granted it. Do not infer, broaden, or manufacture
authority merely to avoid a future question.

Distinguish permission to perform the task from permission for publication,
deployment, destructive changes, durable external effects, secrets, or other
separately governed actions.

## Define continuation and steering

For long-running work, state the continuation policy when it can change behavior.
Keep going through non-blocking findings, status updates, and reversible choices
that are already within scope. Stop only when required user input or authorization,
or a hard safety or operational boundary, prevents safe progress. A progress
report, offer to continue, or list of non-blocking options is not completion
unless the instruction explicitly makes it one.

When status updates are useful, ask the receiver to pair the update with its next
safe action in the same turn when practical instead of reporting and pausing.

When mid-run steering is expected, define how later messages relate to the
accepted objective when that distinction matters. Treat an added constraint or
task as an amendment to the still-active objective unless the sender explicitly
replaces, cancels, or conflicts with earlier scope. Reconcile a conflict instead
of silently dropping an earlier accepted obligation.

## Persist progress only when continuity needs it

For genuinely long autonomous work whose useful state may be lost to context
compaction or a fresh receiver, use a small durable progress artifact only when it
materially improves continuity. Record the accepted objective or finish line,
completed work, remaining work, and real blockers.

Update an existing authoritative plan or tracker when one already owns that state
instead of creating a parallel task file. Do not create a progress artifact for
ordinary bounded work or merely to make activity visible.

## Check the receiver behavior

Read the finished instruction as a fresh receiver. Confirm that it can identify
the finish line and real escape condition, continue through non-blocking status,
preserve still-active obligations under later steering, and distinguish explicit
permission from effects that remain separately governed.

Look for the opposite failure modes as well: an instruction that makes the agent
bulldoze through real uncertainty, that adds approval gates for ordinary
implementation judgment, or that creates progress ceremony without continuity
value. Confirm that avoiding a permission question did not broaden authority.
