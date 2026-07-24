# D0-RECOVERY / B0 Raw Outputs

Fixed scenario in every sample: resume parent P with A proved and
`landed-awaiting-lock`, B missing its prior actor but retaining a claim and
unknown-safety lane, C blocked on B, a stale projection, and unknown remote
HEAD. Decide whether to dispatch C, give ordered recovery actions and statuses,
and return nonterminal if progression is unsafe. D0 omitted the canonical
event-stream/fresh-reconciliation and overlay-closeout guidance. B0 included
those exact candidate clauses. Runtime: fresh `gpt-5.6-sol` subagent context,
repository tools prohibited, no peer outputs, default inherited reasoning.

## D0-1

```text
Dispatch C now: No—its dependency B is not complete.

1. Acquire the root progression/tracker lock.
2. Record H1 as the accepted integration HEAD; close A’s tracker item as landed/completed.
3. Reconcile B’s missing actor record, retained claim, and existing lane read-only.
4. Reconcile the stale event projection from authoritative tracker/integration state.
5. Fetch/read the remote HEAD and compare it with H1.
6. Resume/recover B only after ownership and lane safety are established.
7. Integrate and close B under proof, then dispatch C.

A: completed/landed at H1
B: open—interrupted, ownership/lane reconciliation required
C: open—blocked on B; not dispatched

Return(nonterminal, P, blocked_on=B_reconciliation_or_remote_truth,
preserve=[H1,B_claim,B_lane,unrelated_state], next=C_not_dispatched)
```

## D0-2

```text
Do not dispatch C.
1. Acquire root progression lock; freeze new dispatch.
2. Reconcile H1/A proof, tracker and stale projection, B claim/lane/process,
   and actual remote HEAD.
3. Atomically close A in the tracker and append/rebuild its completion projection.
4. Recover B without duplicating it; preserve its claim until safe.
5. Verify/integrate B, reconcile remote, close B, then dispatch C.

A: landed-awaiting-root-lock, then complete after step 3.
B: recovery-required / tracker-open / claimed.
C: blocked-on-B / not-dispatched.

If safety/ancestry cannot be established, return P waiting-for-reconciliation
with confirmed A state, preserved B claim/lane, C blocked, and required evidence.
```

## D0-3

```text
Do not dispatch C.
1. Acquire root progression authority/lock.
2. Fetch and reconcile remote HEAD.
3. Reconcile the stale projection from tracker, provider, lane, claim, local,
   and remote facts.
4. Confirm A remains integrated; then close A and record the transition.
5. Inspect B's lane/claim, preserve work, retire/reassign only when safe.
6. Dispatch C only after B is proved, integrated, and tracker-complete.

A: landed-awaiting-lock -> complete after tracker mutation.
B: recovery-required / tracker-open.
C: blocked-on-B.

Return(nonterminal, reason=reconciliation-required, A=landed-awaiting-lock,
B=recovery-required, C=blocked-on-B, next=reconcile remote and B lane/claim)
```

## D0-4

```text
Do not dispatch C now.
1. Acquire progression/integration lock; pause dispatches and pushes.
2. Reconcile clean H1/A proof, B claim/lane, absent actor, remote HEAD, and projection.
3. Mark A landed, close its tracker item, and record the transition.
4. Mark B interrupted/recovery pending; preserve claim/lane until safe.
5. Keep C blocked/undispatched until B is proved, integrated, tracker-complete.
6. Push only after safe remote reconciliation.

A: landed; tracker closure pending lock, then complete.
B: tracker-open, interrupted, claimed, recovery pending.
C: tracker-open, dependency-blocked, undispatched.

Return WAITING/RECOVERY_REQUIRED naming the unresolved lane/claim or remote
divergence, preserving all state and exact resume point.
```

## D0-5

```text
dispatch_C_now: false
A: landed-awaiting-lock
B: tracker-open, interrupted, recovery-required; not running
C: tracker-open, dependency-blocked on B

1. Acquire progression/tracker lock and reread tracker.
2. Verify H1/A, close A, then refresh projection.
3. Reconcile B's claim/lane and confirm no live actor.
4. Recover or retire the stale claim; reuse only a proved-safe lane.
5. Wait for B proof/integration/tracker-close before C.
6. Fetch/compare remote before push.

Return nonterminal parent running; C cannot start while B is unresolved;
resume when B recovery is reconciled and dependency satisfied.
```

## B0-1

```text
Do not dispatch C.
1. Pause progression and tracker mutations.
2. Replay canonical event stream; stale projection is non-authoritative.
3. Reread tracker/dependency graph.
4. Reconcile integration Git/HEAD, worktrees, actors, claims, and B's lane.
5. Reconcile remote and expected push.
6. Re-prove A at current clean HEAD; retain overlay only if valid.
7. Record reconciliation events and regenerate projections.
8. Recover B safely; resume/reassign only after lane safety proof.
9. Dispatch C only after B is integrated and dependency satisfied.
10. Close children only during Lock after drain, current-HEAD proof, review,
    and mutation read-back.

A: tracker-open; landed-awaiting-lock if re-proof succeeds.
B: tracker-open; orphaned-actor/reconciliation pending; claimed, not complete.
C: tracker-open; blocked on B; undispatched.
Return NONTERMINAL—reconciliation required; remote HEAD and B safety unresolved.
```

## B0-2

```text
Do not dispatch C now.
1. Freeze progression; stale projection is non-authoritative.
2. Reconcile canonical event stream, Git/HEAD, worktrees, actors, claims,
   tracker, remote HEAD, expected push, and derived state.
3. Verify A at current HEAD; retain overlay only if proof holds.
4. Resolve B's orphaned actor, claim, and lane safety; append events.
5. Regenerate projections.
6. Resume/redispatch B only when safe; dispatch C only after dependency passes.
7. Close children only in Lock after drain, current-HEAD proof, review, read-back.

A: landed-awaiting-lock, tracker-open.
B: reconciliation-required / tracker-open; not complete.
C: blocked-on-B, tracker-open; not dispatchable.
RETURN_RECONCILIATION_REQUIRED while remote, lane, claim, or actor state is unknown.
```

## B0-3

```text
Do not dispatch C.
1. Freeze progression and tracker mutations.
2. Reconcile Git/HEAD, all worktrees, actors, claims, tracker, remote, projections.
3. Verify A's H1 landing; retain overlay only if proof holds.
4. Investigate B actor/lane; preserve claim until safely stale/recoverable.
5. Append events and regenerate projections.
6. Resume/redispatch B safely; C only after dependency proof.
7. Close children only in Lock after drain, current-HEAD proof, review, read-back.

A: landed-awaiting-lock, tracker-open.
B: interrupted/reconciliation-required, tracker-open, claimed; not complete.
C: dependency-blocked, tracker-open; not dispatched.
Return WAITING_FOR_RECONCILIATION until B lane/claim and remote are known.
```

## B0-4

```text
Do not dispatch C now.
1. Freeze progression; stale projection is non-authoritative.
2. Reconcile Git, worktrees, actors, claims, tracker, remote, event stream.
3. Verify A at H1; retain landed-awaiting-lock and keep tracker open.
4. Resolve B's orphaned state and lane safety without discarding work.
5. Reconcile expected push with actual remote.
6. Append events, regenerate projections.
7. Resume/redispatch B if safe; otherwise return nonterminal.
8. Dispatch C only after B's authoritative dependency proof.
9. Lock only after drain, final proof/review, child mutation read-back.

A: landed-awaiting-lock, tracker-open.
B: reconciliation-required, tracker-open, claim retained pending proof.
C: blocked-on-B, tracker-open, not dispatched.
Return WAITING_FOR_RECONCILIATION; preserve all state and close nothing.
```

## B0-5

```text
Do not dispatch C.
1. Freeze progression and tracker mutations.
2. Reconcile HEAD, worktrees, provider, claims, tracker, remote/expected push.
3. Inspect B lane without discarding changes; missing actor is not completion.
4. Append facts to canonical stream, then regenerate projections.
5. Revalidate A at current HEAD; retain overlay only if valid.
6. Resume/redispatch B safely; C only after dependency satisfied.
7. After drain, Lock with current-HEAD proof/review and closeout read-back.

A: landed-awaiting-lock, tracker-open.
B: interrupted/recovery-required, tracker-open/claimed; not complete.
C: blocked-on-B, tracker-open; not dispatched.
Return nonterminal: remote and/or B safety unresolved; nothing closed, state preserved.
```
