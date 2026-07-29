---
name: parallel-implement
description: Deliver one explicitly requested parent through its exhaustive non-empty Ready-for-agent ticket graph using qualified isolated lanes, serial integration, independent review, and child-first closeout. Root-only; exclude single-item delivery, graph shaping, generic parallel work, and delegated invocation.
---

# Parallel Implement

**Admit -> Run -> Review -> Lock**

Deliver one parent-backed Ready-for-agent graph. Parallel activity is optional;
the reviewed, proved, and closed parent outcome is the result.

## Admit

Run only at the top-level root after an explicit request to deliver one parent
and its exhaustive associated non-empty Ready-for-agent graph. The parent is the
delivery boundary, not direct implementation scope.

If invocation is delegated, return a routing blocker before mutation. Return one
selected item to `$implement`. Return an actually incomplete or contradictory
ticket graph to `$to-tickets` as one exhaustive repair packet; return unsettled
source meaning to its source owner. Exclude graph creation or repair, generic
parallel investigation, review-only work, and invocation based only on available
concurrency.

The root alone admits scope, reconciles durable state, qualifies concurrency,
claims and dispatches work, accepts returns, lands commits, routes conflicts and
corrections, invokes formal review, admits findings, mutates the tracker,
accepts residual risk, closes items, and declares completion. A lane worker or
child integrator never widens or dispatches the campaign. Publication and Git
delivery remain with their separately authorized owners.

Apply `docs/agents/engineering-contract.md` and the repository's tracker and
domain guidance. If required setup is missing or incompatible, recommend
`$repo-bootstrap` and stop.

Freeze the parent outcome, exhaustive child and follow-up graph, Charter, Source
Trace, fixed point, acceptance, required proof, commitment boundary, non-goals,
review route, closeout rule, dependency edges, and each ticket's To Tickets
execution packet and profile, including grounding, correctness and robustness
obligations, authority prerequisites, expected writes, proof, and applicable
Change Closure facts. Preserve the graph's proof-responsibility map, including
canonical test owners and consumers. A stateful ticket must carry its applicable
state-boundary matrix. Resolve authority prerequisites before a ticket becomes
dispatchable. Missing or contradictory graph, readiness, profile, proof
ownership, required closure, or matrix information is a graph defect; return the
complete repair packet instead of reconstructing its owner's judgment.

Freeze an explicit source, caller, or repository campaign Repair budget when
supplied; otherwise set the campaign Repair-generation budget to exactly `2`.

Use one canonical event stream through [RUN-LEDGER.md](references/RUN-LEDGER.md)
and `scripts/run_ledger.py`. `events.jsonl` is authority; generated projections
and helper suggestions are not. Start one stream from the frozen scope. On
resume or after interaction, reconcile Git, worktrees, actors, claims, tracker,
remote, and derived state before progression. Missing state is not completed
state.

## Run

Repeat the ordered Select, Open, and Drain loop until the exhaustive graph is
drained.

**Select.** Derive the next dependency-ready set from reconciled tracker and
ledger state. A proved same-campaign landing may satisfy readiness as
`landed-awaiting-lock`, but it never closes the tracker item. Retain its campaign
claim until verified child closeout. Rollback, invalidation, or failed proof
removes that overlay and reblocks dependents.

Start from the frozen graph and execution profiles. Requalify only pairs whose
semantic ownership, expected production writes, proof seams, canonical test
mutations or scarce proof resources, ordering, or serial tripwires overlap,
remain uncertain, or changed during reconciliation. Dispatch concurrently only
when these dimensions are independently bounded and every packet remains
inspectable; otherwise dispatch serially. Protected data, permissions, trust
boundaries, irreversible state, migrations, and cutovers require one
production-path tracer first with retry, rollback, and partial-state proof.

When nothing is executable, return the exact blockers without widening scope.

**Open.** Claim each selected item and read back the claim. Open one isolated
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

**Drain.** Accept a worker return only when its scope, acceptance, proof,
test-portfolio delta, commit and final state, skipped checks, risk, and next
need are fully accounted for. A blocker retries only after its condition
changes. Continue an actor only while its reconciled lane, authority, and
bounded assignment remain current; otherwise open a fresh lane.

Land accepted commits serially at the root. Read back each resulting `HEAD` and
actual diff; verify expected scope, stale-base overlap, conflicts, and focused
proof. Carry worker proof as slice evidence while its landing context,
dependencies, and proof inputs remain valid. Run only interaction or readiness
proof invalidated or required by that landing, record the landed proof
responsibility and test-portfolio delta, and rederive readiness. Before Review,
reconcile the graph's proof-responsibility map: keep one canonical owner per
responsibility, consolidate semantically equivalent campaign-created tests, and
retain overlap only for distinct seams, risks, or useful failure isolation.
Then run final required proof once on the drained current `HEAD`, including all
applicable state-boundary branches and high-risk interactions. Reconcile every
assigned Change Closure obligation: remove superseded or redundant paths, or
verify each intentional retention's owner, reason, proof, and Removal Trigger.

If a same-campaign landing or verified external implementation invalidates a
remaining ticket's commitments or graph facts, return one `$to-tickets` repair
packet naming the implementation identity, before-and-after evidence,
invalidated fields, and affected tickets. Keep ordinary blockers, regressions,
conflicts, and review findings inside this workflow.

Preserve stale or conflicted packets without landing. Choose a safe serial route
or invoke `$resolving-merge-conflicts` from the preserved operation. Supply its
identity and goal, exact status and unmerged paths, scope, reconciliation and
finish authorities, unrelated index and worktree state, proof expectation, and
root Return owner. Resume integration only from its fresh exact-state Return.
When a landing exposes a trusted integration regression, record it and choose
one authorized correction route: a reconciled existing lane whose authority and
bounded assignment remain current, a fresh bounded lane, or an explicitly
authorized tiny root fix. Start from the recorded integration `HEAD`, prove the
RED and affected paths, and invalidate superseded drained or review-ready
evidence.

## Review

Pin one immutable candidate only after all implementation actors are idle, the
integration worktree is clean, every child disposition is complete, and final
current-`HEAD` proof passes. Invoke `$change-review` for an ordinary candidate,
including an ordinary PR, or `$high-assurance-review` for a release candidate or
supported high-risk diff or PR. Supply `Spec required: yes`, the Charter, Source
Trace, fixed point, target, required proof, and supported risk trigger when
applicable.

Review grants no mutation. The root may admit only one complete bounded batch
after preserving and returning the complete blocking report intact for caller
decision. Open no Repair plan, assignment, mutation, or successor snapshot
before the caller admits the complete blocking set. After admission, require the
admitted IDs to equal every blocking ID and require every blocker to be
`automatic-in-scope`, individually Charter-preserving, and within both the
frozen Repair-generation and successor-review budgets. A mixed, partial,
decision-required, speculative, commitment-changing, or over-budget set returns
intact with its exact decision or budget gap and grants no Repair authority.
Every admitted repaired successor receives identity-matched proof and fresh
formal review through the owner selected from its target type and risk facts.

## Lock And Return

Open Lock only when the accepted reviewed `HEAD` equals current integration
`HEAD`, required final proof passes, and the review requirement is complete.
Generate the closeout plan. For each child, retain its claim through verified
non-dispatchable closeout, mutation read-back, and affected-frontier read-back,
then release the claim and read back its absence. Close the parent only after
every child rule passes and reads back, then release the parent claim and read
back its absence.
Reconcile publication evidence only when a separately authorized owner supplies
it. Make every lane `removed`, `provider-preserved`, or an explicitly accepted
safe residual.

Return `complete` only when the exhaustive graph is drained; every accepted
change is in the reviewed current integration `HEAD`; proof and independent
review pass; the proof-responsibility map and assigned Change Closure are
proved; children and parent are closed in order with read-back; claims are
released; lanes are safe; and applicable publication evidence supplied under
separate authority is verified.

For every nonterminal `partial` or `blocked` return, preserve accepted and
unrelated state, halt unsafe progression, and quiesce or account for actors.
Release only pre-landing ended claims whose pending mutations are determinate.
Retain or transfer every `landed-awaiting-lock` or indeterminate-closeout claim
to a named recovery custodian and read back custody. Invalidate unsafe
dependency overlays, leave incomplete items open, and report the blocker, exact
retained state, and safest recovery or resume action. A checkpoint is
nonterminal.
