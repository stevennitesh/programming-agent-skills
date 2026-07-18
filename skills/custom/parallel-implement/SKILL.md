---
name: parallel-implement
description: Drain one parent spec or PRD's implementation ticket graph automatically through isolated lanes, serial integration, bounded review repair, and verified child and parent closeout.
---

# Parallel Implement

Drain one parent-backed implementation graph to verified closeout.

- **Orchestrator:** owns scope, state, dispatch, acceptance, serial landing, review, mutations, outcome, and release.
- **Lane worker:** owns one ready ticket, isolated worktree, clean commit, and focused proof.
- **Integration lane:** owns serial landing and integration proof only; the orchestrator holds it unless explicitly routed.

**Two isolations:** every lane requires fresh context and a preflighted worktree. Workers, an optional integrator, and reviewers are direct fresh-context children; they never spawn.

**State machine:** `events.jsonl` is canonical. Append records evidence; `run_ledger.py validate-state` grants authority. A successful append never authorizes dispatch, landing, Review, Lock, push, or `complete`.

Run one resumable wavefront campaign:

**Trace -> Gate -> Drain -> Review -> Repair -> Lock -> Release**

## Operating Surface

- Always apply `docs/agents/engineering-contract.md`.
- Read `docs/agents/issue-tracker.md` before tracker work and `docs/agents/domain.md` when domain semantics affect the campaign.
- Use `references/RUN-LEDGER.md` and `scripts/run_ledger.py` for campaign state, authority, rendering, and closeout.
- Use [FINDING-CONTRACT.md](../review/FINDING-CONTRACT.md) for review admission and remediation classes.
- Use `references/CODEX-WORKTREE-LAUNCH.md` and `scripts/lane_worktree.py` for lane lifecycle and recovery.
- Dispatch workers with `references/WORKER-BRIEF.md`.
- Read `references/INTEGRATOR-BRIEF.md` only when deciding or operating a shallow, hot, or late child integrator.

## Trace

Apply the **setup gate**. When a required setup surface or named operation is absent or incompatible, recommend `$repo-bootstrap` and stop.

**Resume:** when an event stream exists, Resume inside Trace. Run `resume-status`, reconcile Git, worktrees, agents, tracker, and remote state, then append that evidence. A missing agent is not completion; redispatch only from a reconciled classification authorized by `validate-state`.

Otherwise resolve exactly one parent and its exhaustive child and follow-up graph. Build the Source Trace and record the fixed point, child-set snapshot, dependencies, readiness, exclusions, and parent closeout rule.

Record one campaign **Charter** in the `scope` event: parent outcome, exhaustive child set, acceptance criteria, supported workflows and environments, required validation, commitment boundary, non-goals, fixed point, review route, and Repair Budget. Default the Budget to two generations unless the caller explicitly sets a smaller bound. A changed child set or commitment requires scope reconciliation; an authority-changing commitment requires a caller decision before mutation.

Every open in-scope ticket must satisfy the repo's Ready-for-agent contract. The parent selects work; it is never direct implementation scope.

When graph repair is required, return one **exhaustive repair packet** covering every visible missing slice, dependency edge, readiness defect, acceptance ambiguity, and unsliced commitment. Recommend `$to-tickets` and stop. Resume only after the entire repaired graph is published, read back, and reconciled.

## Gate

Build the frontier from reconciled tracker and ledger state. A landed item satisfies execution dependencies; tracker closeout waits for Lock. A changed child set reopens scope reconciliation.

Apply the **frontier gate** across acceptance, contracts, write scopes, proof, dependencies, slots, and review bandwidth. Disjoint files do not prove semantic independence.

**Tripwire:** protected data, permissions, trust boundaries, irreversible state, migrations, or cutovers close broad parallelism. Run one end-to-end tracer through production-path semantics, including crash, retry, rollback, and partial-state proof. Reopen the frontier only after it passes.

**Downshift:** use serial execution whenever independence, write scope, slots, or review bandwidth is uncertain. Reopen parallelism only from evidence.

- **Serial:** select the first ready ticket in tracker order.
- **Parallel:** select up to the worker limit only when at least two ready tickets are semantically independent.
- **Blocked:** return the unfinished tickets and exact blockers when no ticket is executable.

The worker limit is the smaller of three or live slots after reserving the orchestrator and any integrator. Parallelism requires bandwidth to inspect every packet before the next frontier decision. No worker slot means blocked, not `$implement`.

## Drain

Before dispatch, claim and read back tracker state, establish the lane, and require `validate-state --intent dispatch`. Launch one direct worker with `fork_turns="none"`, its brief, absolute worktree, stable temp roots, and liveness checkpoint.

Classify each return: accept or reject a verified `done`; keep `needs-feedback` open for one delta; retry `blocker` only after its input, base, route, capability, authority, or task shape changes.

Use the launch reference's **Stall** branch when a worker misses its recorded checkpoint without agent or process progress. Inspect before redispatch.

Only accepted `done` may land. Land serially through the recorded route; detached one-commit workers default to `cherry-pick`. Inspect `base..head`, scope, stale-base overlap, conflicts, and proof, then require `validate-state --intent land`.

Apply the **proof budget**: worker focused, integration touched-area, loop-close broad. After landing, verify the diff and proof, record the integration SHA, and append draft closeout evidence.

A **stale-base packet** returns for rebase, redispatch, serialization, or rejection. A partial or conflicted landing preserves Git state and invokes `$resolving-merge-conflicts` before resuming.

After each landing, refetch the relationship fingerprint. Fetch full changed tickets when it changes or lacks a safe revision. Reconcile scope, ask `validate-state` for the next transition, and repeat until drained or blocked.

## Review

Enter Review only when `validate-state --intent review` passes. Require the drained graph, child accounting, clean integration state, final validation, and idle lanes. Pin immutable integration `HEAD`.

Invoke `$review` by default or `$convergent-pr-review` for high risk, with `Spec required: yes`, `Review mode: initial`, the Charter, parent, child accounting, Source Trace, fixed point, target `HEAD`, and diff.

Keep Lock closed for an unavailable or incomplete review, admitted blocker, missing required validation, or residual risk requiring separate authority. `pass with residual risk` is acceptable automatically only when every residual is nonblocking under the Charter and tracker or repo policy requires no separate acceptance.

The review report returns evidence; it grants no mutation, worker dispatch, or successor-snapshot authority. The orchestrator's recorded Charter, ledger state, and remaining Budget control Repair. Finalize child closeout evidence only after acceptance.

## Repair

Classify the complete review result through the finding contract before dispatch or editing. Continue automatically only when every blocker is admitted, marked `automatic-in-scope`, preserves the Charter, has bounded proof, and `validate-state --intent repair` passes. If any blocker is ambiguous or `decision-required`, return the whole decision packet without partially repairing it. An `incomplete` review is not repair authority.

Append one `repair-plan` referencing the blocked review-decision event and snapshot, with the generation, every eligible finding ID, owners, write scopes, and proof. Batch all eligible blockers into that generation. The orchestrator may apply a tiny routed fix or dispatch isolated repair workers; every worker receives the Charter, generation, reviewed `HEAD`, assigned finding IDs, owned files, and required proof. Repair work never widens the parent graph or mutates tracker closeout state.

Accept and land repair packets serially. Run finding proof, repair-regression proof, and touched-area integration proof, then append `repair-complete`. Pin one successor `HEAD` and invoke the same review route with `Review mode: remediation`, the original Charter, generation, prior snapshot, carried finding IDs, repair delta, and remaining original acceptance.

Remediation review may judge carried findings, repair regressions, and remaining original acceptance. It may not reopen untouched surfaces with new hardening lenses. Stop when review is acceptable, a decision is required, or two Repair generations have been consumed.

## Lock

Open Lock only when `validate-state --intent lock` proves that the accepted reviewed `HEAD` equals current integration `HEAD`. Generate the closeout plan from the event stream.

Follow tracker policy and execute the generated plan child-first. Render and post each verified packet, apply its mutation, and **Mutation read-back** before advancing. Then refetch the complete related set, close the parent only when its rule passes, and read back the graph.

Push only when `validate-state --intent push` proves current and approved `HEAD` match; verify the remote resolves to that SHA.

## Release

Finish every agent. Release each lane through the helper, recording registration and directory state separately. Preserve dirty, unintegrated, conflicted, unauthorized, or residual state.

Render `LEDGER.md` from `events.jsonl`; never edit generated ledger prose. Return exactly one outcome from `validate-state`: `complete`, `partial`, or `blocked`.

`complete` requires approved current `HEAD`, no admitted blocker, final validation and review, verified child and parent closeout, applicable tracker and push proof, no open Repair generation, and safe lane dispositions. `partial` and `blocked` claim only reconciled events and preserve exact recovery state.

Every outcome includes the Source Trace, child-set snapshot, frontier history, landing and closeout accounting, current Git state, skipped checks, residual risk, and release state. No outcome leaves an active lane or uncertain partial mutation unaccounted.
