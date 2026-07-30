# Worker Brief Contract

Generate one assignment with `run_ledger.py brief`, then add the ticket-owned
execution packet that the ledger cannot infer.

## Common assignment

- Work item and mode
- Actor ID and preflight packet
- Charter and Source Trace
- Applicable engineering and domain pointers
- Verified base and absolute worktree
- Stable temp, pytest, and cache roots
- Grounding: current owner, representative callers and entry paths, Repository
  Reuse, and repository constraints
- Acceptance, Commitment Boundary, prohibited behavior, exclusions, and
  dependencies
- Applicable Invariants, Trust Boundaries, supported states, and failure,
  recovery, compatibility, environmental, and observability obligations
- Confirmed authority boundary
- Change Closure: `<displaced paths and retention obligations / not applicable>`
- State-boundary matrix:
  `<applicable branches and interactions / not applicable>`
- Proof responsibility: `<behavior or branch, canonical test surface or proof
  lane, consumers, expected reuse / extend / add>`
- Expected write scope; proposed concrete write set when shared fixtures are
  plausible
- Focused proof and validation environment
- Observable liveness checkpoint
- Report transport

The assigned worktree is the workspace. Reconcile its root, base, clean status,
actor, proof startup, Python import provenance, and temp roots before editing.
Use it as `workdir` for every command and edit only beneath it. Stop on
mismatch.

One worker owns one lane and returns one packet. Never spawn, integrate,
formally review, mutate trackers, push, or widen scope. Use `$tdd` for
red-testable behavior. For an uncertain bug, return `needs-feedback` with a
`diagnosis-required` packet containing the facts, evidence, environment, exact
lane state, authorities, and root Return owner; stop.

Choose implementation technique under the routed Code Quality Contract. Start
from assigned grounding and refresh only facts that current evidence makes
stale or contradictory.

Prove every assigned acceptance, prohibited behavior, correctness and
robustness obligation, matrix branch, and proof responsibility. Reuse or extend
the assigned canonical test owner; add a separate test only for a distinct
responsibility. If repository inspection contradicts the assignment or reveals
an omitted supported semantic branch or overlapping test owner, return it as
`needs-feedback`; do not silently rewrite the packet, narrow acceptance, or
widen the commitment boundary.

Run focused proof by default. Run broader proof only for shared-behavior risk or
an explicit route. Product intent, public/domain contracts, dependency meaning,
security posture, and adjacent work remain outside the lane unless the Source
Trace authorizes them.

## Mode additions

### Implementation

Implement exactly the assigned acceptance slice. Discoveries outside it are
scope notes, not authority. Return one clean commit or an exact
blocker/needs-feedback packet.

### Integration correction

Include the regression event ID, prior integration HEAD, correction route,
authorized owner and actor, structured write-scope IDs, trusted RED, and
required proof. Start from that HEAD, select only authorized IDs, reproduce or
reconcile the RED, and prove failing and affected paths. Return selected IDs,
actual changed files, one clean correction commit, and evidence. Do not land it.

An existing worker may receive this correction only while the root-recorded
route, reconciled lane, authority, and bounded assignment remain current.
Otherwise use a fresh lane.

### Review repair

Include the caller admission record, repair generation, blocked reviewed HEAD,
complete blocking finding set, exact admitted IDs, automatic classification and
Charter-preservation evidence for every blocker, both frozen budget states,
scopes, and required proof. Accept the assignment only when the admitted IDs
equal every blocking ID and every blocker passes all gates. Change only those
admitted findings under the original Charter. Prove each remedy and regression.
Adjacent observations authorize no work.

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
test portfolio delta: <reused / extended / added / consolidated / removed +
  responsibility>
commands and results:
skipped checks:
liveness checkpoint:
risk or blocker:
next need:
scope notes:
final status: <clean / dirty + reason>
```

`done` requires reconciled preflight, every criterion, proof responsibility,
and assigned Change Closure obligation accounted for, one commit, focused
proof, and clean status. `blocker` and `needs-feedback` claim no completion and
preserve exact state.
