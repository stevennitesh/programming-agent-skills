# Worker Brief Contract

Generate one assignment with `run_ledger.py brief`, then add the ticket-owned Source Trace, acceptance, expected scope, and focused proof that the ledger cannot infer.

## Common assignment

- Work item and mode
- Actor ID and preflight packet
- Charter and Source Trace
- Verified base and absolute worktree
- Stable temp, pytest, and cache roots
- Acceptance, exclusions, and dependencies
- State-boundary matrix: `<applicable branches and interactions / not applicable>`
- Expected write scope; proposed concrete write set when shared fixtures are plausible
- Focused proof and validation environment
- Observable liveness checkpoint
- Report transport

The assigned worktree is the workspace. Reconcile its root, base, clean status, actor, proof startup, Python import provenance, and temp roots before editing. Use it as `workdir` for every command and edit only beneath it. Stop on mismatch.

One worker owns one lane and returns one packet. Never spawn, integrate, formally review, mutate trackers, push, or widen scope. Use `$tdd` for red-testable behavior. For an uncertain bug, use `$diagnosing-bugs` in fix mode and return after trusted regression proof.

Prove every assigned matrix branch. If repository inspection reveals a supported semantic branch omitted from the assignment, return it as `needs-feedback`; do not silently narrow acceptance or widen the commitment boundary.

Run focused proof by default. Run broader proof only for shared-behavior risk or an explicit route. Product intent, public/domain contracts, dependency meaning, security posture, and adjacent work remain outside the lane unless the Source Trace authorizes them.

## Mode additions

### Implementation

Implement exactly the assigned acceptance slice. Discoveries outside it are scope notes, not authority. Return one clean commit or an exact blocker/needs-feedback packet.

### Integration correction

Include the regression event ID, prior integration HEAD, correction route, authorized owner and actor, structured write-scope IDs, trusted RED, and required proof. Start from that HEAD, select only authorized IDs, reproduce or reconcile the RED, and prove failing and affected paths. Return selected IDs, actual changed files, one clean correction commit, and evidence. Do not land it.

The original worker may receive this as its one narrow continuation only when the root records that route and supplies a reconciled correction lane. Otherwise use a fresh lane.

### Review repair

Include the repair generation, blocked reviewed HEAD, complete assigned finding IDs, scopes, and required proof. Change only those admitted findings under the original Charter. Prove each remedy and regression. Adjacent observations authorize no work.

## Return packet

```text
status: <done / blocker / needs-feedback>
work item:
mode:
actor ID:
base:
commit:
changed scope IDs: <when authorized IDs exist>
actual changed files:
acceptance proof: <criterion -> evidence>
commands and results:
skipped checks:
liveness checkpoint:
risk or blocker:
next need:
scope notes:
final status: <clean / dirty + reason>
skill feedback: <none, or surface | evidence | impact | suggestion>
```

`done` requires reconciled preflight, every criterion accounted for, one commit, focused proof, and clean status. `blocker` and `needs-feedback` claim no completion and preserve exact state.

Skill feedback is process evidence only. The root may record it as friction; it grants no implementation authority.
