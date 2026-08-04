---
name: implement
description: Deliver one explicitly selected bounded ready item through the smallest acceptance-complete change, focused proof, one fresh Change Review, and applicable Git or tracker closeout.
---

# Implement

Deliver exactly one caller-selected ready item. Prefer the smallest
repository-native integrated solution that satisfies its real callers and
proof obligations. Novelty and familiarity are neutral.

Implement owns technique and repository delivery inside the selected boundary.
The caller owns commitments, permissions, irreversible external effects, and
residual-risk acceptance. Push requires separate authority.

## Admit

Load the repository's setup, engineering, and domain owners. Load tracker and
label owners only for tracker-backed work.

Accept a settled outcome with operational acceptance, source, scope authority,
dependencies, and a useful proof seam. For tracker-backed work, require the
configured ready state and claim rules. For direct work, use the caller's
selection as the scope fence. Return unsettled meaning to its owner, an
exhaustive parent graph to the caller, missing setup to `$repo-bootstrap`, and
an active conflict to `$resolving-merge-conflicts` before mutation.

Keep the selected outcome and all source-owned commitments unchanged. Do not
substitute, split, or widen the item.

Reconcile the repository, `HEAD`, index, worktree, tracker state, and unrelated
work. Preserve foreign changes. Freeze a compact Charter containing the
outcome, commitments, scope, exclusions, proof, fixed point, and one Repair
budget; preserve an explicit value or default to `2`.

One Repair generation is one admitted complete blocker set, one bounded repair
batch with proof, and one fresh successor review. Increment once per batch, not
per finding or worker. Transport retry and proof-only rerun do not consume a
generation.

Claim tracker-backed work and read the claim back. Direct work creates no
tracker state. Require a delivery commit for tracker-backed work and whenever
repository policy requires one. Otherwise, direct work creates one only when
the caller requests Git delivery.

## Implement

At the top-level root, delegate only when fresh collaboration is available, the
caller did not request root execution, a worker can independently own the
bounded edit and proof, and the expected root effort saved exceeds handoff and
verification cost. Make that judgment directly from the item and checkout;
create no score, worksheet, or artifact. When the gate passes, choose the first
matching capable worker using the ordered conditions in
[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md), then
send one plain ticket-specific handoff to one fresh worker. Use the
[Plain Worker Handoff](references/WORKER-HANDOFF.md) as guidance, not as a
schema. Once the information is sent, start the worker; do not add a capsule
validator, receipt protocol, ledger, or sealed brief. A delegated Implement
worker implements directly and never delegates again. The worker has exclusive
mutation custody of the reconciled checkout until Return; the root performs no
repository or Git mutation during that interval.

The worker implements the smallest acceptance-complete path, proves the
assigned behavior through the repository's canonical seam, performs Change
Closure, and creates a bounded commit only when the delivery branch requires
one. It returns the changed scope, concise proof, residual-risk evidence, and
the commit when created. The root treats that prose Return as evidence, then
verifies the actual diff, scope, proof, and applicable commit before accepting
it.
When the delegation gate fails, the root follows the same implementation path
directly.

Use `$tdd` for settled red-testable behavior. For a bug whose expected behavior,
cause, or trusted reproduction is uncertain, return `diagnosis-required` with
the observed evidence rather than guessing.

Choose the lowest-total-burden solution across callers, maintenance,
migration, operation, coordination, and proof. Reuse the existing behavior owner when it
fits. Add a boundary only when it has a named caller, observable proof,
ownership, and a concrete reason to exist now. Validate machine-consumed
actionable input once at its trust boundary; do not validate ordinary prose
handoffs or Returns.

Bind proof to the exact candidate and inputs. Run focused checks that prove the
change, plus broader checks only when repository policy or shared impact makes
them necessary. When safe execution is unavailable, use the strongest safe
proxy and report what remains unproved.

## Review And Repair

Pin the exact candidate while preserving the starting index and unrelated work.
For staged review, stage only owned paths or hunks and never unstage foreign
work. Stop if the candidate cannot be isolated.

Launch exactly one fresh `ordinary-reviewer` using `$change-review`, with an
actor, task, and context distinct from every implementation actor. Supply the
Charter, source, fixed point, immutable candidate, implementation identities,
proof, skips, risks, contradictory evidence, and `Spec required: yes`.
Supported risk changes review coverage; it does not select another automatic
review system. `$high-assurance-review` runs only when the user explicitly
invokes it.

Accept only a complete Review Return bound to the candidate. Review grants no
mutation. Automatically repair only when every blocker is Charter-preserving,
in scope, and within the frozen budget. Send localized findings to the current
implementer when safely resumable. If the caller explicitly required root
execution, keep repair mutation with the root; otherwise use one fresh
implementation worker when the current implementer is not safely resumable.
Prove the repaired candidate and launch a new fresh Change Review.
Return decision-required, scope-changing, speculative, mixed, or over-budget
findings to the caller intact.

Treat a pre-judgment review transport failure as invalid and retry once with a
fresh reviewer. Preserve the candidate and return `partial` after a second
failure. Never self-certify.

## Lock And Return

Lock the reviewed tree plus only applicable closeout. Any other delta requires
new proof and review. Reuse valid proof. When the delivery branch requires a
commit, require its tree to equal the locked tree and run only commit-boundary
checks that policy or invalidation requires.

When a delivery commit is required, create it if the accepted candidate is not
already exactly committed. Do not rewrite an exact accepted commit merely to
satisfy a commit count. Retry a failed commit only after proving `HEAD`
unchanged. Otherwise preserve the reviewed locked candidate and stop before
commit.

For hosted trackers, retain the claim through commit and configured closeout,
read back non-dispatchability, then release the claim and verify the frontier.
For Local Markdown, include required mechanical closeout in the reviewed and
locked tree. Direct work has no tracker closeout.

Apply the configured Mutation read-back rules to every tracker closeout.

Return:

```text
Outcome: complete | partial | blocked
Commit identity and tree: <evidence> | not applicable
Proof, skips, and Change Review provenance:
Repair generations: <used and remaining>
Changed scope and Change Closure:
Tracker closeout and frontier: <evidence> | not applicable
Residual risk:
Caller-owned next action: <action> | none
```

Return `complete` only when acceptance, focused proof, Change Review, Lock,
every branch-applicable commit, tracker closeout, and claim release, Change
Closure, and unrelated-state exclusion pass. Otherwise preserve state and
report the failed gate, evidence, custody, needed authority, and safest
recovery. `blocked` means no authorized in-scope progress is possible until a
named authority or external-state change. `partial` means accepted progress is
preserved while an internal execution, proof, review, or cleanup gate remains
safely resumable. When both descriptions apply, return `blocked`.

Stop before another item, parent closure, deployment, PR creation, merge, or
unauthorized push.
