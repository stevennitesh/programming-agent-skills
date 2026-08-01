# Worker Brief

**Bind -> Implement -> Prove -> Return**

Generate the ledger-owned assignment with
[Campaign Runtime](RUN-LEDGER.md) `brief`, then add only ticket-owned meaning.

## Assignment

The ledger supplies the work item, mode, semantic agent ID, actor, task, lane,
base, checkout, temp roots, Charter, launch receipt, liveness cursor, and Return
transport.

The root adds:

- Source Trace and applicable engineering and domain pointers;
- current owner, representative callers and entry paths, Repository Reuse, and
  repository constraints;
- acceptance, Commitment Boundary, prohibited behavior, exclusions, and
  dependencies;
- applicable Invariants, Trust Boundaries, supported states, and failure,
  recovery, compatibility, environmental, and observability obligations;
- confirmed authority, expected write scope, and proposed concrete write set
  when shared fixtures are plausible;
- Change Closure and any applicable state-boundary matrix;
- proof responsibility, canonical owner and consumers, expected reuse, extend,
  or add decision, focused proof, and validation environment.

## Bind

Reconcile the final augmented assignment SHA-256 from the dispatch receipt,
launch receipt, current directory, task, actor, lane, exact base, clean status,
startup proof, project provenance, and temp roots before editing. Use the
assigned checkout for every command and edit only beneath it. Stop on mismatch.

One worker owns one item and returns one packet. Never spawn or delegate. Leave
dispatch, integration, tracker mutation, remote Git delivery, scope changes,
and campaign completion to their owners. Do not invoke
`$change-review` or `$high-assurance-review`; formal review belongs to the
root-selected owner.

## Implement

Choose implementation technique under the routed engineering contract. Refresh
assigned grounding only when current evidence makes it stale or contradictory.
Discoveries outside the assignment are scope notes, not authority.

Use `$tdd` for red-testable behavior. An uncertain bug returns
`needs-feedback` with a `diagnosis-required` packet containing facts, evidence,
environment, exact task and lane state, authorities, and the root Return owner.

If repository evidence contradicts the assignment or reveals an omitted
supported semantic branch or overlapping test owner, return `needs-feedback`;
do not rewrite the packet, narrow acceptance, or widen the Commitment Boundary.

## Prove

Prove every acceptance, prohibited behavior, correctness and robustness
obligation, matrix branch, proof responsibility, and Change Closure obligation.
Reuse or extend the assigned canonical test owner; add a separate test only for
a distinct responsibility.

Run focused proof by default. Run broader proof only for shared-behavior risk or
an explicit route. Product intent, public or domain contracts, dependency
meaning, security posture, and adjacent work remain outside the lane unless the
Source Trace authorizes them.

## Branches

**Pre-landing correction.** Continue only in the same current task, lane, and
checkout. Amend or supersede the returned commit, prove the requested fix, and
name the superseded commit in Return.

**Integration correction.** Require the regression event ID, prior integration
`HEAD`, correction route, authorized owner and actor, write-scope IDs, trusted
RED, and required proof. Start from that `HEAD`, change only authorized IDs,
prove the RED and affected paths, and return one clean correction commit. An
owned correction returns to its current worker; cross-worker work belongs to
`serial-integrator`.

**Review Repair.** Require caller admission, generation, blocked reviewed
`HEAD`, complete blocking set, exact admitted IDs, per-blocker automatic and
Charter-preservation evidence, both budgets, write scope, and required proof.
Accept only when admitted IDs equal every blocker and every gate passes. Change
only those findings under the original Charter and prove each remedy and
regression.

## Return

```text
status: <done / blocker / needs-feedback>
work item:
mode:
agent ID:
actor ID:
task ID and host ID:
transport:
lane and worktree:
base:
assignment ref:
assignment SHA-256:
commit:
supersedes commit: <prior returned commit / none>
changed scope IDs: <when authorized IDs exist>
actual changed files:
acceptance proof: <criterion -> evidence>
test portfolio delta: <reused / extended / added / consolidated / removed + responsibility>
commands and results:
skipped checks:
liveness cursor:
risk or blocker:
next need:
scope notes:
final status: <clean / dirty + reason>
```

`done` requires a matching launch receipt, every assigned obligation accounted
for, one commit, focused proof, and clean status. `blocker` and
`needs-feedback` preserve exact state and claim no completion.
