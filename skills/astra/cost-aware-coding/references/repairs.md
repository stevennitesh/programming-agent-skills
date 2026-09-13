# Repair allowances

Classify a failed return before spending an allowance. Requirements, acceptance,
and environment faults need resolution at their source, not model escalation.
That resolution does not renew consumed allowances.

## Choose the next action

| Return or finding | Action |
| --- | --- |
| Before review, blocked with evidence that current reasoning effort is insufficient and stronger attempt unused | Skip focused repair; propose one stronger attempt. |
| First implementation candidate fails acceptance | Give the same implementer one focused repair. |
| Focused repair fails because reasoning effort is insufficient | Propose one stronger attempt. |
| Requirements, design, or environment fault | Resolve at its owner and continue within the current stage's remaining allowance. |
| Stronger attempt fails or recovery unavailable | Preserve the candidate and request a revised route. |
| Review requires corrections and its gate has rounds left | Send one correction batch to the current implementer, then review its return. |
| Required corrections remain at an exhausted gate | Preserve the candidate and request more rounds or a revised route. |

A stronger attempt uses an accepted Sol High replacement, or XHigh when justified.
Obtain acceptance unless already authorized. Native follow-ups cannot change
model/effort: after explicit release and stopped writers, spawn the replacement
with the agreed settings and compact candidate/failure context. Preserve remaining
allowances; prompt cache and context do not automatically transfer. If the runtime
cannot provide that route, report the limit. Your own model changes remain user actions.

## Count returns, not internal work

An implementation attempt is consumed when its candidate returns ready or blocked.
Editing, debugging, and checks before that return belong to the same attempt.
A review-repair round covers one required correction batch, its implementer checks,
and the same reviewer's follow-up. Charge it when that candidate returns, including
failed checks. Initial reviews, optional suggestions, and unchanged-candidate
rechecks consume no correction round.

Questions, prerequisite-only returns before implementation, interruptions, and
resumes are not candidate attempts. Resolve prerequisites and custody before
resuming. Retransmitted returns are processed once.

Once review begins for a scope, corrections use its review-repair allowance and
cannot reopen implementation recovery. Higher-effort repair uses the next remaining
round rather than a new allowance. Later coherent forward work retains its own
implementation recovery; relabeling a correction as forward work does not.

## Keep allowances at their gate

Ordinary delivery has two review-repair rounds for the integrated candidate.
Planned delivery has two per checkpoint and two separately for final review.
Concurrent lanes share their integrated gate's allowance.

Give checkpoints stable identities and coverage before assignment. Future work
outside that coverage is not failed acceptance. Known unresolved findings retain
their gate and counts through renaming, splitting, reopening, or moving work.
A later regression or newly discovered defect uses the gate discovering it,
including final review, even if the affected code passed an earlier checkpoint.

Track implementation recovery per coherent work unit and corrections per gate.
Replacement, repartitioning, or new lanes do not reset either. For concurrent work,
[Parallel recovery](../../parallel-implement/references/recovery.md) owns recovery
mechanics; verify its transport supports the accepted route.
