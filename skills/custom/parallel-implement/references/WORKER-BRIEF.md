# Worker Brief

**Bind -> Ground -> Implement -> Prove -> Return**

The dispatch helper seals the complete assignment before spawn. The initial
spawn message names its path and SHA-256; no follow-up assignment is required.

## Bind

Verify the assignment SHA-256, work item, attempt, semantic profile, actor,
lane, checkout, exact base, environment, Charter, tracker snapshot, and write
scope before editing. Reconcile the provider task ID from the current runtime;
it is intentionally absent from the pre-spawn brief.

Use the assigned checkout for every command and write only inside its authorized
scope. An isolated worker may read ignored inputs from the recorded root
checkout but never writes there. Stop on mismatch.

One worker owns one item and returns one packet. Never spawn, delegate, claim
tickets, integrate, mutate trackers, push, review, or decide campaign
completion. Do not invoke `$change-review` or `$high-assurance-review`.

## Ground

Read the frozen tracker snapshot for the Source Trace, applicable engineering
and domain pointers, current owner, acceptance, Commitment Boundary, prohibited
behavior, dependencies, applicable Invariants, Trust Boundaries, confirmed
authority, proof responsibility, Change Closure, and any applicable state-boundary matrix.
Refresh current repository grounding: implementation
seams, callers, fixtures, canonical proof owners, and the concrete write set
inside the authorized scope.

Contradictions return `needs-feedback` when live repository evidence contradicts the frozen
assignment, invalidates acceptance, exposes an omitted semantic branch, or
requires overlapping ownership. Report the exact evidence; do not rewrite or
widen scope.

## Implement

Choose the implementation technique under the routed engineering contract.
Use `$tdd` for red-testable behavior. Keep discoveries outside the assignment
as scope notes.

For a pre-landing correction, continue in the same task, lane, and checkout;
amend or supersede the returned commit, name the superseded commit, and bind the
Return to the root feedback event. For an
integration correction or Review Repair, obey the exact recorded event, prior
integration `HEAD`, generation, finding IDs, write scope, and proof.

## Prove

Map every acceptance and robustness obligation to evidence. Reuse or extend the
canonical proof owner. Run focused proof by default and broader proof only for
shared-behavior risk or an explicit assignment. Finish with one clean commit and
a clean checkout.

## Return

Return exact binding:

- work item, actor, provider task ID, lane, checkout, base, assignment reference,
  and assignment SHA-256;
- status: `done | blocker | needs-feedback` and commit or superseded commit when
  applicable;
- actual changed files;
- `grounding_and_scope`: repository grounding, concrete write set, and scope
  discoveries;
- `proof`: acceptance-to-evidence mapping, checks and results, proof-owner or
  test-portfolio change, and skips;
- `risk_or_blocker`;
- `required_root_action`;
- `final_worktree`: structured exact `head` and `clean` status.

`done` requires every assigned obligation accounted for, one commit, focused
proof, and clean status. Other statuses preserve exact state and claim no
completion.
