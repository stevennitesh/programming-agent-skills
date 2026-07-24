---
name: parallel-implement
description: Deliver one explicitly requested parent through its exhaustive non-empty Ready-for-agent ticket graph using qualified isolated lanes, serial integration, independent review, and child-first closeout. Root-only; exclude single-item delivery, graph shaping, generic parallel work, and delegated invocation.
---

# Parallel Implement

**Trace -> Select -> Open -> Drain -> Review -> Lock**

Deliver one parent-backed Ready-for-agent graph. Parallel activity is optional;
the reviewed, proved, and closed parent outcome is the result.

## Admission

Run only at the top-level root after an explicit request to deliver one parent
and its exhaustive associated non-empty Ready-for-agent graph. The parent is
the delivery boundary, not direct implementation scope.

If invocation is delegated, return a routing blocker before mutation. Return
one selected item to `$implement`; return an incomplete, ambiguous, unsettled,
or unready graph to `$to-tickets` as one exhaustive repair packet. Exclude
graph creation or repair, generic parallel investigation, review-only work,
and invocation based only on available concurrency.

The root alone admits scope, reconciles durable state, qualifies concurrency,
claims and dispatches work, accepts returns, lands commits, routes conflicts
and corrections, invokes formal review, admits findings, mutates the tracker,
accepts residual risk, closes items, pushes when authorized, and declares
completion. A lane worker or child integrator never widens or dispatches the
campaign.

## Trace

Apply `docs/agents/engineering-contract.md` and the repository's tracker and
domain guidance. If required setup is missing or incompatible, recommend
`$repo-bootstrap` and stop.

Freeze the parent outcome, exhaustive child and follow-up graph, Charter,
Source Trace, fixed point, acceptance, required proof, commitment boundary,
non-goals, review route, closeout rule, dependency edges, and each ticket's To
Tickets execution profile. A stateful ticket must carry its applicable
state-boundary matrix. Missing or contradictory graph, readiness, profile, or
matrix information is a graph defect; return the complete repair packet
instead of reconstructing its owner's judgment.

Use one canonical event stream through
[RUN-LEDGER.md](references/RUN-LEDGER.md) and `scripts/run_ledger.py`.
`events.jsonl` is authority; generated projections and helper suggestions are
not. Start one stream from the frozen scope. On resume or after interaction,
reconcile Git, worktrees, actors, claims, tracker, remote, and derived state
before progression. Missing state is not completed state.

## Select

Derive the next dependency-ready set from reconciled tracker and ledger state.
A proved same-campaign landing may satisfy readiness as
`landed-awaiting-lock`, but it never closes the tracker item. Rollback,
invalidation, or failed proof removes that overlay and reblocks dependents.

Qualify every pair across semantic ownership, expected production writes,
proof seams and scarce proof resources, ordering, and serial tripwires.
Dispatch concurrently only when these dimensions are independently bounded
and every packet remains inspectable; otherwise dispatch serially. Protected
data, permissions, trust boundaries, irreversible state, migrations, and
cutovers require one production-path tracer first with retry, rollback, and
partial-state proof.

When nothing is executable, return the exact blockers without widening scope.

## Open

Claim each selected item and read back the claim. Open one isolated
fresh-context lane from the exact base through `scripts/lane_worktree.py` and
[CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md). Dispatch only
from `ok: true, state: ready` evidence that accounts for containment,
provenance, startup proof, actor, checkout, and cleanup.

Generate the complete bounded assignment from
[WORKER-BRIEF.md](references/WORKER-BRIEF.md). The worker owns only that item
and returns one typed packet; it does not spawn, integrate, formally review,
mutate trackers, push, or declare campaign completion. Use `$tdd` for
red-testable new behavior or a fully known red-capable bug. Use
`$diagnosing-bugs` when expected behavior, symptom, cause, or a trusted
reproduction is unsettled.

The root normally integrates. Use
[INTEGRATOR-BRIEF.md](references/INTEGRATOR-BRIEF.md) only when serial
integration itself is a genuinely bounded independent lane. The integrator
returns landing and review authority to the root.

## Drain

Accept a worker return only when its scope, acceptance, proof, commit and final
state, skipped checks, risk, and next need are fully accounted for. A blocker
retries only after its condition changes. Continue the same actor once only
when it must complete or explain its own bounded result; otherwise reconcile
and open a fresh lane.

Land accepted commits one at a time at the root. Inspect the actual diff,
expected scope, stale-base overlap, conflicts, and focused proof. After each
landing, run affected recombined proof, record the new integration `HEAD`, and
rederive readiness. Before Review, run final proof across all applicable
state-boundary branches and high-risk interactions on the current integration
`HEAD`.

Preserve stale or conflicted packets without landing. Choose a safe serial
route or invoke `$resolving-merge-conflicts` from the preserved operation.
When a landing exposes a trusted integration regression, record it and choose
one authorized correction route: the original worker once, a fresh bounded
lane, or an explicitly authorized tiny root fix. Start from the recorded
integration `HEAD`, prove the RED and affected paths, and invalidate superseded
drained or review-ready evidence.

Repeat Select, Open, and Drain until the exhaustive graph is drained.

## Review

Pin one immutable candidate only after all implementation actors are idle, the
integration worktree is clean, every child disposition is complete, and final
current-`HEAD` proof passes. Invoke `$review` for an ordinary candidate or
`$convergent-pr-review` for a local PR or bounded high-risk diff. Supply `Spec
required: yes`, the Charter, Source Trace, fixed point, target, and required
proof.

Review grants no mutation. The root may admit only one complete bounded batch
of Charter-preserving `automatic-in-scope` findings within the recorded Repair
and successor-review budgets. Return ambiguous or decision-required findings
as one decision packet. Every repaired successor receives fresh formal review.

## Lock

Open Lock only when the accepted reviewed `HEAD` equals current integration
`HEAD`, required final proof passes, and the review requirement is complete.
Generate the closeout plan, close every child with mutation read-back, then
close the parent only after its rule passes and read that mutation back.
Release every claim. Push only when authorized, then verify the approved
closeout SHA at the remote. Make every lane `removed`, `provider-preserved`, or
an explicitly accepted safe residual.

Return `complete` only when the exhaustive graph is drained; every accepted
change is in the reviewed current integration `HEAD`; proof and independent
review pass; children and parent are closed in order with read-back; claims are
released; lanes are safe; and applicable push evidence is verified.

For every nonterminal `partial` or `blocked` return, preserve accepted and
unrelated state, halt unsafe progression, quiesce or account for actors,
release ended claims, invalidate unsafe dependency overlays, leave incomplete
items open, and report the blocker, exact retained state, and safest recovery
or resume action. A checkpoint is nonterminal.
