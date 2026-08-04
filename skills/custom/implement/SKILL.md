---
name: implement
description: Deliver one explicitly selected bounded ready item through the smallest acceptance-complete change, focused proof, one fresh Change Review, applicable closeout, and commit; use one Luna implementer when top-level delegation is available.
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

Claim tracker-backed work and read the claim back. Direct work creates no
tracker state.

## Implement

At the top-level root, when fresh collaboration delegation is available, send
one plain ticket-specific handoff to a fresh `clear-worker` from the
[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md). Use
the [Plain Worker Handoff](references/WORKER-HANDOFF.md) as guidance, not as a
schema. Once the information is sent, start the worker; do not add a capsule
validator, receipt protocol, ledger, or sealed brief. A delegated Implement
worker implements directly and never delegates again.

The worker implements the smallest acceptance-complete path, proves the
assigned behavior through the repository's canonical seam, performs Change
Closure, commits its bounded change, and returns the commit plus concise proof
and residual-risk evidence. The root treats that prose Return as evidence,
then verifies the actual diff, scope, commit, and proof before accepting it.
When delegation is unavailable or the caller explicitly requests direct work,
the current owner follows the same implementation path directly.

Use `$tdd` for settled red-testable behavior. For a bug whose expected behavior,
cause, or trusted reproduction is uncertain, return `diagnosis-required` with
the observed evidence rather than guessing.

Choose the lowest-total-burden solution across callers, maintenance,
migration, operation, coordination, and proof. Reuse the current owner when it
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

Launch exactly one fresh `ordinary-reviewer` using `$change-review`, with a
runtime distinct from every implementation actor. Supply the Charter, source,
fixed point, immutable candidate, implementation identities, proof, skips,
risks, contradictory evidence, and `Spec required: yes`. Supported risk changes review coverage; it
does not select another automatic review system. `$high-assurance-review` runs
only when the user explicitly invokes it.

Accept only a complete Review Return bound to the candidate. Review grants no
mutation. Automatically repair only when every blocker is Charter-preserving,
in scope, and within the frozen budget. Send localized findings to the current
implementer when safely resumable; otherwise use one fresh implementation
worker. Prove the repaired candidate and launch a new fresh Change Review.
Return decision-required, scope-changing, speculative, mixed, or over-budget
findings to the caller intact.

Treat a pre-judgment review transport failure as invalid and retry once with a
fresh reviewer. Preserve the candidate and return `partial` after a second
failure. Never self-certify.

## Lock And Return

Lock the reviewed tree plus only applicable closeout. Any other delta requires
new proof and review. Require the commit tree to equal the locked tree. Reuse
valid proof and run only commit-boundary checks that policy or invalidation
requires.

Create the delivery commit if the accepted candidate is not already exactly
committed. Do not rewrite an exact accepted commit merely to satisfy a commit
count. Retry a failed commit only after proving `HEAD` unchanged.

For hosted trackers, retain the claim through commit and configured closeout,
read back non-dispatchability, then release the claim and verify the frontier.
For Local Markdown, include required mechanical closeout in the reviewed and
locked tree. Direct work has no tracker closeout.

Apply the configured Mutation read-back rules to every tracker closeout.

Return:

```text
Outcome: complete | partial | blocked
Commit identity and tree:
Proof, skips, and Change Review provenance:
Repair generations:
Changed scope and Change Closure:
Tracker closeout and frontier: <evidence> | not applicable
Residual risk:
Caller-owned next action: <action> | none
```

Return `complete` only when acceptance, focused proof, Change Review, Lock,
commit identity, applicable tracker closeout, claim release, Change Closure,
and unrelated-state exclusion pass. Otherwise preserve state and report the
failed gate, evidence, custody, needed authority, and safest recovery.

Stop before another item, parent closure, deployment, PR creation, merge, or
unauthorized push.
