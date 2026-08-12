---
name: implement
description: Deliver one explicitly selected bounded ready item through the smallest acceptance-complete change, focused proof, final diff and state read-back, condition-triggered review, and applicable Git or tracker closeout.
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
work. Preserve foreign changes. Keep the accepted outcome, commitments, scope,
exclusions, proof, and fixed point available without creating another control
artifact.

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

Before either path chooses an implementation seam, trace each acceptance
commitment to its proof seam. When a commitment depends on integration, follow
the real caller or runtime entry path to the observable output and proof. Existing
code or component tests count only when that path reaches them. Do this
directly; create no matrix or artifact.

Use `$tdd` for settled red-testable behavior. For a bug whose expected behavior,
cause, or trusted reproduction is uncertain, return `diagnosis-required` with
the observed evidence rather than guessing.

Choose the lowest-total-burden solution across callers, maintenance,
migration, operation, coordination, and proof. Reuse the existing behavior owner when it
fits. Add a boundary only when it has a named caller, observable proof,
ownership, and a concrete reason to exist now. Validate machine-consumed
actionable input once at its trust boundary; do not validate ordinary prose
handoffs or Returns.

Apply Hyrum's Law as a compatibility-risk heuristic when changing observable
behavior: distinguish the intended contract from actual dependence, and treat
demonstrated dependence as migration evidence rather than automatically as a
new commitment.

Bind proof to the exact candidate and inputs. Run focused checks that prove the
change, plus broader checks only when repository policy or shared impact makes
them necessary. When safe execution is unavailable, use the strongest safe
proxy and report what remains unproved.

## Check, Conditional Review, And Repair

Inspect the complete owned diff, current repository state, real-caller
behavior, focused proof, Change Closure, and unrelated-state exclusion.
Correct an accepted in-scope defect exposed by this check, then rerun only
invalidated proof. Required proof must pass before review; missing proof returns
`partial` or `blocked` and is never relabeled Residual Risk.

Invoke `$change-review` only when the user or repository explicitly requires
independent review; the candidate contains mutations from two or more
independent authors; or focused proof establishes behavior but a material
shared-contract or irreversible-migration acceptance judgment still warrants
fresh independent judgment and review is the lowest-burden way to obtain it.
One delegated edit, candidate size, novelty, PR or release packaging, generic
or supported risk, security or production adjacency, and reviewer availability
do not trigger review. An untriggered branch creates no review packet or
explanation.

When review triggers, pin the exact candidate while preserving the starting
index and unrelated work. For staged review, stage only owned paths or hunks
and never unstage foreign work. Stop if the candidate cannot be isolated. Use
one fresh `ordinary-reviewer` through `$change-review`, with an actor, task, and
context distinct from every implementation actor. Supply the accepted request
and commitments, source, fixed point, immutable candidate, implementation
identities, proof, material skips, supported facts, contradictory evidence,
and `Spec required: yes`.

Accept only a complete Review Return bound to the candidate. Review grants no
mutation. Repair only admitted `automatic-in-scope` blockers that preserve the
accepted commitments and scope. Send a localized finding to the current
implementer when safely resumable; if the caller required root execution, keep
repair with the root; otherwise use one fresh implementation worker when the
current implementer is not safely resumable. Rerun invalidated proof and repeat
Change Review only while the original trigger still applies. One review
invocation authorizes at most one automatic repair successor; any blocker in
that successor review returns to the caller rather than opening another
automatic repair cycle. Return
decision-required, scope-changing, speculative, mixed, or unsupported findings
to the caller intact. If the same blocker recurs without a new authorized
in-scope repair path, stop under the terminal classifier.

A pre-judgment review transport failure may be retried once while the candidate
remains unchanged. Otherwise preserve the candidate and return `partial`. Do
not describe direct self-check as independent review.

## Lock And Return

Lock the final checked tree, and when review ran the reviewed tree, plus only
applicable closeout. Any other delta requires new proof and reevaluation of the
review trigger. Reuse valid proof. When the delivery branch requires a commit,
require its tree to equal the locked tree and run only commit-boundary
checks that policy or invalidation requires.

When a delivery commit is required, create it if the accepted candidate is not
already exactly committed. Do not rewrite an exact accepted commit merely to
satisfy a commit count. Retry a failed commit only after proving `HEAD`
unchanged. Otherwise preserve the final checked candidate and stop before
commit.

For hosted trackers, retain the claim through commit and configured closeout,
read back non-dispatchability, then release the claim and verify the frontier.
For Local Markdown, include required mechanical closeout in the final checked
tree. Direct work has no tracker closeout.

Apply the configured Mutation read-back rules to every tracker closeout.

Do not return `partial` merely because the first bounded seam is green. Continue
while an unmet acceptance commitment remains safely actionable within current
scope and authority.

Return:

```text
Outcome: complete | partial | blocked
Commit identity and tree: <evidence> | not applicable
Proof and material skips; Change Review provenance when activated:
Changed scope and Change Closure:
Tracker closeout and frontier: <evidence> | not applicable
Residual risk:
Caller-owned next action: <action> | none
```

Return `complete` only when acceptance, focused proof, final diff and state
read-back, every triggered Change Review, every branch-applicable commit,
tracker closeout and claim release, Change Closure, and unrelated-state
exclusion pass. Otherwise preserve state and
report the failed gate, evidence, custody, needed authority, and safest
recovery. `blocked` means no authorized in-scope progress is possible until a
named authority or external-state change. `partial` means accepted progress is
preserved while an internal execution, proof, review, or cleanup gate remains
safely resumable. When both descriptions apply, return `blocked`.

Stop before another item, parent closure, deployment, PR creation, merge, or
unauthorized push.
