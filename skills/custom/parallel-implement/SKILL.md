---
name: parallel-implement
description: Deliver one explicitly requested parent through its exhaustive non-empty Ready-for-agent ticket graph using delegated workers, isolated concurrent lanes, serial integration, independent review, and child-first closeout. Root-only; exclude single-item delivery, graph shaping, generic parallel work, and delegated invocation.
---

# Parallel Implement

**Admit -> Freeze -> Wave -> Land -> Review -> Lock**

Deliver one parent-backed graph. Parallelism is optional; the reviewed, proved,
and closed parent outcome is the result.

## Admit

Pass only at the top-level root after an explicit request to deliver one parent
and its exhaustive, non-empty Ready-for-agent graph. The parent bounds delivery;
it is not direct implementation scope.

The root alone freezes scope, qualifies concurrency, claims and dispatches
tickets, accepts returns, lands commits, routes corrections and conflicts,
selects formal review, applies caller Repair and residual-risk decisions,
mutates the tracker, closes items, and declares completion. Workers neither
widen nor dispatch the campaign. Publication and Git delivery remain with their
separately authorized owners. The root never authors implementation, tests,
integration corrections, or Review Repair.

Return before mutation:

- delegated invocation -> routing blocker;
- one standalone item -> `scope-mismatch`;
- incomplete or contradictory graph -> one exhaustive `$to-tickets` repair
  packet;
- unsettled source meaning -> its source owner;
- missing or incompatible setup -> recommend `$repo-bootstrap` and stop.

Exclude graph shaping, generic parallel work, review-only work, and invocation
based only on available concurrency. Apply the repository engineering, tracker,
and domain contracts.

## Freeze

Freeze the parent outcome, exhaustive children and follow-ups, Charter, Source
Trace, fixed point, acceptance, Commitment Boundary, non-goals, dependency
edges, proof-responsibility map, review-selection policy, closeout rule, and
any caller-supplied residual-risk policy with its identity and evidence. Freeze
each ticket's To Tickets execution profile. Tickets remain factual and
model-neutral; absent residual-risk policy means caller-only acceptance.

Require every profile to record grounding, semantic ownership, authority,
dependencies, expected production writes, correctness and robustness,
canonical proof owners and consumers, Change Closure, and any applicable
state-boundary matrix. Missing or contradictory readiness, profile, authority,
closure, matrix, or proof ownership is a graph defect; return the complete
repair packet instead of reconstructing its owner's judgment.

Freeze supplied Repair and review budgets; otherwise use the ledger defaults.

Start one canonical stream through
[RUN-LEDGER.md](references/RUN-LEDGER.md) and `scripts/run_ledger.py`.
`events.jsonl` is authority; projections are derived and judgments are explicit.
After interaction or resume, reconcile Git, worktrees, actors, tasks, claims,
tracker, and derived state; include remote state only when separately authorized
delivery depends on it. Missing state is not completed state.

## Wave

Repeat **Frontier -> Dispatch -> Drain** until the exhaustive graph is drained.

**Frontier.** Derive the dependency-ready set from reconciled graph and ledger
state. A proved same-campaign landing may satisfy campaign readiness as
`landed-awaiting-lock` only while its landing and proof remain valid. It never
closes the ticket; its claim remains through verified child closeout. Rollback,
invalidation, or failed proof removes it and reblocks dependents.

Qualify concurrency from semantic ownership, production writes, proof seams,
canonical test mutations, scarce proof resources, ordering, and serial
tripwires. Dispatch only independently bounded, inspectable packets; downshift
uncertain or overlapping work to serial. Protected data, permissions, trust
boundaries, migrations, cutovers, and irreversible state require one
production-path tracer first with retry, rollback, and partial-state proof.

If nothing is executable, return the exact blockers without widening scope.

**Dispatch.** Choose the cheapest capable semantic agent ID from this ordered
escalation. A matching later condition overrides every earlier one:

- `clear-worker`: fully specified, repeatable work;
- `adaptive-worker`: bounded work with material local choices;
- `fast-adaptive-worker`: adaptive work under an explicit latency preference;
- `demanding-worker`: architectural, broadly coupled, or materially ambiguous
  work.

Claim each selected ticket and read back the claim. Launch each worker through
[CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md), which owns the
concrete task binding, starting state, isolation, readiness, liveness, Return,
and cleanup contract. Delegate serial work in the integration checkout under
exclusive worker custody. Give concurrent workers separate Codex tasks and
distinct managed worktrees.

Generate the bounded assignment through
[WORKER-BRIEF.md](references/WORKER-BRIEF.md).

**Drain.** Accept only a task-lane-matched Return satisfying the Worker Brief.
`blocker` and `needs-feedback` claim no completion. Retry only after the
blocking condition changes. Route pre-landing correction through the current
task lane.

## Land

The root mechanically lands one accepted commit at a time. For an isolated
lane, require a clean integration checkout at the recorded prior `HEAD` before
landing. For a serial same-checkout lane, require clean current `HEAD` to equal
the returned commit and descend from the recorded prior `HEAD`, then adopt it.
Otherwise preserve state and reconcile. Inspect the actual `base..head` diff
for scope, new files, stale-base overlap, conflicts, and proof; this is not
formal review. After landing, read back integration `HEAD` and the actual diff,
run only proof invalidated or required by the transition, record the landed
proof responsibility and test-portfolio delta, and rederive the frontier.

Carry worker proof only while its landing context, dependencies, and inputs
remain valid. Before Review, reconcile one canonical owner per proof
responsibility, consolidate equivalent campaign-created tests, run final
required proof once on drained current `HEAD`, cover applicable state-boundary
branches and high-risk interactions, and remove or justify every displaced
Change Closure path.

Branch only on observed failure:

- invalidated ticket commitments -> return one `$to-tickets` packet naming the
  implementation, before-and-after evidence, invalidated fields, and affected
  tickets;
- stale or conflicted landing -> preserve it, choose a safe serial route, or
  invoke `$resolving-merge-conflicts` with exact state and authorities; resume
  only from its fresh exact-state Return;
- trusted integration regression -> record the RED and prior integration
  `HEAD`, then return an owned correction to its current worker or route
  cross-worker work to `serial-integrator`.

Every correction proves the RED and affected paths and invalidates superseded
drained or review-ready evidence.

## Review

Pin one immutable candidate only when all implementation and integration tasks
are idle, the integration worktree is clean, every child disposition is
complete, and final current-`HEAD` proof passes.

Select `ordinary-reviewer` with `$change-review` for an ordinary candidate or
`assurance-coordinator` with `$high-assurance-review` for a release candidate
or supported high-risk diff or PR. Launch it through the task-lane contract as
a fresh task distinct from every implementation and integration task. Supply
only `Spec required: yes`, the implementation and integration actor and task
IDs, Charter, Source Trace, fixed point, candidate, proof, skips, risk, and
contradictory evidence. Withhold
implementation hypotheses, expected conclusions, partial findings, and
terminal cues.

Accept a Review Return only when complete, current, and bound to the exact
candidate and fresh task provenance. The candidate passes Review only with no
blocker or unaccepted residual. If no valid independent Return arrives, preserve
the candidate and return `partial`; never self-certify.

On `scope-mismatch`, preserve the factual packet and select the other route once
for the same generation in a new fresh task. If it also mismatches, preserve the
candidate and return `partial`.

**Repair.** Review grants no mutation. Preserve and return the complete blocking
set for caller decision. Open Repair only when caller-admitted IDs equal every
blocking ID, every blocker is `automatic-in-scope` and individually
Charter-preserving, and the complete batch fits both frozen budgets. Return any
mixed, partial, speculative, decision-required, commitment-changing, or
over-budget set intact with its exact gap.

Delegate one serial Repair worker in the integration checkout. Use the original
worker's agent ID for a localized finding; use `serial-integrator` for
cross-worker findings. Every admitted successor gets identity-matched proof, a
route selected from its actual risk, and formal review with new actor and task
identities. Never resume a prior reviewer or assurance run.

## Lock

Open Lock only when accepted reviewed `HEAD` equals current integration `HEAD`,
required final proof passes, independent review is complete, and any residual
risk has caller or identified frozen-policy acceptance.

Generate the closeout plan. For each child, retain its claim through verified
non-dispatchable closeout, mutation read-back, and affected-frontier read-back;
then release the claim and read back absence. Close the parent only after every
child passes and reads back; then release the parent claim and read back
absence. Reconcile publication evidence only when its separately authorized
owner supplies it. Leave every lane `removed`, `provider-preserved`, or an
explicitly accepted safe residual.

Return `complete` only when the exhaustive graph is drained; every accepted
change is in reviewed current integration `HEAD`; final proof, proof ownership,
Change Closure, and independent review pass; children and parent close
child-first with read-back; claims are released; lanes are safe; and any
separately supplied publication evidence is verified.

Return `partial` when safe, already-authorized work remains resumable; return
`blocked` when progress requires changed external state or new caller
authority. In either case, preserve accepted and unrelated state, halt unsafe
progression, and account for every task and lane. Release only pre-landing ended
claims with determinate pending mutations. Retain or transfer every
`landed-awaiting-lock` or indeterminate-closeout claim to a named recovery
custodian and read back custody. Invalidate unsafe dependency overlays, leave
incomplete tickets open, and report the blocker, exact retained state, and
safest resume action. A checkpoint is nonterminal.
