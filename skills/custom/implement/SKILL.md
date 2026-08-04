---
name: implement
description: Deliver one explicitly selected bounded ready item through proof, review, Lock, applicable tracker closeout, and one commit.
---

# Implement

Deliver exactly one caller-selected ready item.

Implement owns technique and repository delivery inside the Charter. The caller
owns commitments, permissions, irreversible external effects, and residual-risk
acceptance. Push requires separate authority.

## Admit

Load the repository's applicable setup, engineering, and domain owners. Load
tracker and label owners only for tracker-backed work.

Accept only a settled outcome with operational acceptance, Source Trace,
commitment boundary, dependencies, scope authority, and proof lane. For
tracker-backed work, also require configured readiness, expected write scope,
parallel-safety judgment, and scope fence. For direct work, derive a missing
scope fence from the caller's selection.

Keep the named item and all source-owned commitments unchanged. Do not
substitute, split, widen, or make incomplete work ready.

Reconcile the packet, repository, authority, fixed point, worktree, index,
tracker state, and unrelated work. Stop on ambiguity, contradiction, unsafe
overlap, missing authority, or incomplete readiness.

Claim tracker-backed work and read the claim back. Direct work creates no
tracker state.

Freeze one Charter containing the accepted outcome, commitments, scope, writes,
proof, exclusions, fixed point, and Repair budget. Use the source, caller, or
repository budget; otherwise default to exactly `2`. Unless the caller
restricts Repair before Freeze, the delivery request authorizes every admitted
`automatic-in-scope` blocker that fits this budget.

Return malformed or unsettled work to its source owner. Return an exhaustive
parent graph or review-only request intact to the caller as `blocked` with
`scope-mismatch`. Recommend `$repo-bootstrap` for missing setup and stop. Hand
conflicts to `$resolving-merge-conflicts`. Recommend `$to-tickets` only when
verified landed implementation invalidated the selected ticket's commitments
or graph facts.

Every Return or handoff carries the exact source, state, scope, authorities,
proof, and Return owner. Ticket invalidation also names the implementation
identity, before-and-after evidence, invalidated fields, and affected ticket.
Stop before mutation.

## Execute

Apply the engineering contract's binding floors, preferences, and
condition-triggered methods. Start from source grounding and refresh only
stale, uncertain, or contradicted evidence.

When a separately admitted delegated route supplies a worker, load the
[Plain Worker Handoff](references/WORKER-HANDOFF.md). Send fresh ticket-specific
context and accept its evidence as provisional until the delivery owner verifies
the diff, requested commit, and observed proof. This is ordinary task context, not a schema.
The reference defines handoff meaning only; #69 owns activation
and the current direct route remains available.

Implement the smallest acceptance-complete path. Prove every assigned behavior
and supported state through its canonical seam. Reuse the canonical test owner.
Perform Change Closure and remove authored scaffolding.

Use `$tdd` for settled red-testable behavior. For a bug, use `$tdd` only when its
expected behavior, symptom, cause, and trusted red-capable reproduction are
known. Otherwise return `diagnosis-required` with expected and actual behavior,
evidence, environment, exact work state, authorities, and Return owner; stop.

Bind proof to the exact candidate and inputs. Reuse unchanged proof. Rerun only
invalidated or repository-required checks. When execution is unsafe or
unavailable, use the strongest safe structural proxy and record the unrun
behavior and residual risk.

## Review

Stage one exact candidate while preserving the starting index and unrelated
work. In shared work, stage exact paths or hunks and request staged-only review.
Never unstage foreign work. Stop when the candidate cannot be isolated. Pin the
proved tree as one immutable candidate generation.

Apply `$change-review`'s
[Finding Contract](../change-review/FINDING-CONTRACT.md) supported-risk
predicate to the pinned candidate. Load the
[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md). Give
each generation one fresh read-only collaboration subagent using the exact
semantic profile and runtime binding:
`ordinary-reviewer` with `$change-review` for an ordinary candidate, or
`assurance-coordinator` with `$high-assurance-review` for a release candidate or
supported high-risk candidate. Record candidate-bound route evidence with its source,
`ordinary | release | supported-high-risk` basis, and trigger when applicable.
Use new review actor and task IDs distinct from all implementation actor and
task IDs. Supply `Spec required: yes`, those implementation IDs, Charter,
Source Trace, fixed point, candidate, proof, skips, risk, and contradictory
evidence; withhold hypotheses, expected conclusions, partial findings, and
terminal cues.

Accept only a complete current Return bound to the generation and review
semantic agent, actor, and task IDs, with no blocker or unaccepted residual
risk. Require requested and observed-or-unavailable runtime binding provenance
to match the Runtime Profiles. On `scope-mismatch`, reselect from the
returned facts once in a new fresh task. Treat transport failure before candidate-bound judgment as
`transport-invalid` and retry once in another fresh task; after a second failure
or route mismatch, preserve the candidate and return `partial`.

Review grants no mutation. The delivery owner validates the complete blocking
set and automatically opens Repair only when every blocker is
`automatic-in-scope`, Charter-preserving, and within the frozen budget. Return
every other set intact with its exact gap.

Prove each repaired generation, reselect its route from current facts, and
review it under new actor and task IDs. Send `Invocation: formal-delivery`,
`Review mode: remediation`, and the Finding Contract's remediation packet.
Never resume a prior review.

## Lock And Return

Use the configured tracker representation to encode this skill's claim,
closeout, custody, and Mutation read-back rules.

- Add only mechanical Local Markdown closeout after review and before Lock.
  Commit it with the selected work.
- For GitHub or GitLab, retain the claim through Lock and commit. Apply the
  configured closeout, refetch and prove every effect plus durable
  non-dispatchability, release the claim, then refetch claim absence and the
  affected frontier.
- Create no tracker state for direct work.

Lock the reviewed tree plus applicable Local Markdown closeout. Send every other
review-to-lock delta through formal review. Require the index and commit trees
to equal the locked tree. Run only checks invalidated or required at the commit
boundary.

Create exactly one commit. Retry a failed commit only after proving `HEAD`
unchanged; do not retry blindly.

On an early Return before commit, release a claim only after pending mutations
are determinate and no recovery duty remains. After a post-commit hosted
closeout failure, preserve the commit, refetch state, avoid blind replay, and
retain or transfer custody to a named recovery custodian until closeout and
frontier proof finish.

Push only with separate authority and verify the approved commit remotely.

Return:

```text
Outcome: complete | partial | blocked
Commit identity and tree:
Proof, skips, and formal-review provenance:
Repair generations:
Changed scope and Change Closure:
Tracker closeout, claim, and frontier: <evidence> | not applicable
Residual risk:
Caller-owned next action: <action> | none
```

Report but do not infer or start caller-owned next actions.

Return `complete` only when acceptance, proof, review, Lock, commit identity,
applicable tracker order, relationships, claim release, frontier, Change
Closure, unrelated-state exclusion, and every authorized external read-back
pass.

Otherwise return `partial` or `blocked` with the failed gate, preserved state,
evidence, custody, skipped checks, needed authority, and safest recovery.

Stop before another item, parent closure, deployment, PR creation, merge, or
unauthorized push.
