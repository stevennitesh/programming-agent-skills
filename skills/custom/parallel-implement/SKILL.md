---
name: parallel-implement
description: Implement one root-owned parent spec or PRD ticket graph through dependency-ready frontiers, isolated fresh-context lanes, serial landing, separately budgeted repair and review, event-sourced authority, friction accounting, and verified closeout. Use only from the top-level root agent; delegated invocation is a routing blocker.
---

# Parallel Implement

**Trace -> Gate -> Drain -> Review -> Repair -> Lock -> Release**

Drain one parent-backed implementation graph to verified closeout.

**Root-only orchestration.** The top-level root is the sole dispatcher, campaign decision-maker, formal-review invoker, state writer, and release owner. If invoked inside a delegated task, stop before Trace or mutation and return a routing blocker.

- **Lane worker:** own one ready ticket, isolated worktree, clean commit, and focused proof.
- **Integration lane:** own serial landing and integration proof only. Keep it with the root unless a shallow, hot, or late child integrator is justified.
- **Formal review:** the root invokes the selected review skill. That skill owns its reviewers and returns one terminal decision; campaign workers and integrators never review their own work.

Create campaign workers and any integrator as direct children with `fork_turns="none"`. They do not spawn. Use `followup_task` only once for a narrow `needs-feedback` continuation when the same actor must answer for its evidence or finish an omitted deliverable. Replace a blocked, stalled, superseded, or context-contaminated actor only after its input, base, route, capability, authority, or task shape changes.

**Two isolations:** every lane needs fresh context and a preflighted worktree.

**Event-sourced authority:** `events.jsonl` is canonical and `LEDGER.md` is generated. Prefer `run_ledger.py append-receipt` for canonical events. `committed: true` means only that the event was durably appended; act only when the requested intent has `allowed: true` in authority derived from the current stream. A same-ID replay at the stream tail returns the stored receipt; after later events it preserves the append acknowledgement but recomputes authority from the full stream. Never infer append success from missing output.

## Operating Surface

- Apply `docs/agents/engineering-contract.md`.
- Read `docs/agents/issue-tracker.md` before tracker work and `docs/agents/domain.md` when domain semantics matter.
- Use [RUN-LEDGER.md](references/RUN-LEDGER.md) and `scripts/run_ledger.py` for campaign state, authority, rendering, and closeout.
- Use [FINDING-CONTRACT.md](../review/FINDING-CONTRACT.md) for review admission and remediation classes.
- Use [CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md) and `scripts/lane_worktree.py` for lane lifecycle and recovery.
- Dispatch with [WORKER-BRIEF.md](references/WORKER-BRIEF.md). Read [INTEGRATOR-BRIEF.md](references/INTEGRATOR-BRIEF.md) only when selecting or operating a child integrator.

## Trace

Apply the **setup gate**. When a required setup surface or named operation is absent or incompatible, recommend `$repo-bootstrap` and stop.

**Resume:** when an event stream exists, run `resume-status`, reconcile Git, worktrees, agents, tracker, and remote state, then append that evidence. A missing actor is not completion. Redispatch only from a reconciled classification authorized by the receipt or `validate-state`.

Otherwise resolve exactly one parent and its exhaustive child and follow-up graph. Record the Source Trace, fixed point, child-set snapshot, dependencies, readiness, exclusions, and parent closeout rule. The parent selects work; it is never direct implementation scope.

Record one Charter in the `scope` event with `runtime_contract: 2`, the parent outcome, exhaustive children, acceptance, supported workflows and environments, required proof, commitment boundary, non-goals, fixed point, review route, and these independent counters:

```yaml
repair_generation_budget: 2
review_invocation_budget: 3
review_invocations_required: 1
```

The Repair Generation Budget is a ceiling on automatic repair batches; any explicit nonnegative caller value is valid. The Review Invocation Budget is a positive ceiling on formal top-level review calls and defaults to Repair Generation Budget plus one. Review Invocations Required is the caller's positive minimum of completed formal reviews and defaults to one. Internal reviewer replacement, challenge rounds, and root fallback passes belong to the review invocation and do not consume campaign review invocations. Continue accepting legacy `repair_budget` when it does not conflict with the canonical value.

A budget is a ceiling, not an obligation. Change budgets or required review count after Trace only through a `scope-change` event with exact prior values, explicit caller source, and reason. Never lower a value below consumption, lower required reviews, or self-grant more budget. A changed child set or commitment still requires scope reconciliation and caller authority where it changes commitments.

Every open in-scope ticket must satisfy the repo's Ready-for-agent contract. When graph repair is required, return one exhaustive repair packet covering every missing slice, dependency edge, readiness defect, acceptance ambiguity, and unsliced commitment. Recommend `$to-tickets` and stop until the complete repaired graph is published, read back, and reconciled.

## Gate

Build the frontier from reconciled tracker and ledger state. A landed item satisfies execution dependencies; tracker closeout waits for Lock.

Apply the **frontier gate** across acceptance, contracts, write scopes, proof, dependencies, slots, and review bandwidth. Disjoint files do not prove semantic independence.

**Tripwire:** protected data, permissions, trust boundaries, irreversible state, migrations, or cutovers close broad parallelism. Run one end-to-end tracer through production-path semantics, including crash, retry, rollback, and partial-state proof. Reopen the frontier only after it passes.

**Downshift:** use serial execution whenever independence, write scope, slots, or review bandwidth is uncertain. Reopen parallelism only from evidence.

- **Serial:** select the first ready ticket in tracker order.
- **Parallel:** select up to the worker limit only when at least two ready tickets are semantically independent.
- **Blocked:** return the unfinished tickets and exact blockers when no ticket is executable.

The worker limit is the smaller of three or live slots after reserving the root and any integrator. Require bandwidth to inspect every packet before the next frontier decision. No worker slot means blocked, not `$implement`.

## Drain

Before dispatch, claim and read back tracker state, establish the lane, append its evidence, and require a receipt authorizing `dispatch`. Launch one direct worker with its brief, absolute worktree, stable temp roots, and liveness checkpoint.

Classify each return: accept or reject a verified `done`; continue `needs-feedback` once under the narrow rule above; retry `blocker` only after its blocking condition changes. Use the launch reference's **Stall** branch when a worker misses its checkpoint without agent or process progress.

Only accepted `done` may land. Land serially through the recorded route; detached one-commit workers default to `cherry-pick`. Inspect `base..head`, scope, stale-base overlap, conflicts, and proof, then require a receipt authorizing `land`.

Apply the **proof budget**: worker focused, integration touched-area, loop-close broad. After landing, verify the diff and proof, record the integration SHA, append draft closeout evidence, refetch the relationship fingerprint, reconcile any graph change, and repeat.

A **stale-base packet** returns for rebase, redispatch, serialization, or rejection. A partial or conflicted landing preserves Git state and invokes `$resolving-merge-conflicts` before resuming.

## Review

Enter Review only when a receipt authorizes `review`. Require the drained graph, child accounting, clean integration state, final validation, and idle lanes. Pin immutable integration `HEAD`.

Append one `review-invocation` immediately before each formal review with the immutable target, event ID, mode, reason, and route. Its decision must reference that event ID.

- `initial`: review the first integrated candidate.
- `remediation`: review a successor created from one admitted Repair generation.
- `assurance`: re-examine the same accepted snapshot through `$convergent-pr-review` with a new run, ledger, and fresh reviewers because the caller required additional confidence.
- An `incomplete` invocation may retry the same target and mode when review budget remains.

Invoke `$review` by default or `$convergent-pr-review` for high risk, with `Spec required: yes`, the Charter, Source Trace, fixed point, target, mode, and mode-specific packet. If assurance is required but the Charter selected ordinary review, return the route change for caller-authorized reconciliation.

Keep Lock closed for an unavailable or incomplete review, admitted blocker, missing required proof, unmet required-review count, or residual risk needing separate authority. `pass with residual risk` is acceptable automatically only when every residual is nonblocking under the Charter and policy requires no separate acceptance.

The review report is evidence. It grants no mutation, repair, or successor-snapshot authority.

## Repair

Classify the complete review result through the finding contract. Continue automatically only when every blocker is admitted, `automatic-in-scope`, Charter-preserving, bounded by proof, and both one Repair generation and one successor Review invocation remain. An `incomplete` review is never repair authority.

Append one `repair-plan` tied to the blocked review decision and target. Batch every eligible blocker into the generation with owners, write scopes, and proof. If any blocker is ambiguous or `decision-required`, return the whole decision packet without partial repair.

Apply a tiny routed fix or dispatch isolated repair workers. Repair never widens the parent graph or mutates tracker closeout state. Land packets serially, run finding, regression, and integration proof, append `repair-complete`, pin one successor `HEAD`, and invoke `remediation` review.

Stop when review is acceptable, a decision is required, or either budget is exhausted.

## Lock

Open Lock only when a receipt authorizes `lock` and proves the latest accepted reviewed `HEAD` equals current integration `HEAD` and the required review count is complete.

Generate the closeout plan from the event stream. Execute tracker mutations child-first under tracker policy, render each verified packet, and perform **Mutation read-back** after every change. Close the parent only when its rule passes and the complete related set reads back correctly.

Push only when a receipt authorizes `push`; verify the remote resolves to the approved SHA.

## Release

Append structured friction observations from worker, integrator, reviewer, and root packets. Before `complete`, append exactly one synthesis referencing every observation, or `none_observed: true`. Friction is process evidence only: it never grants dispatch, landing, repair, review, Lock, or push authority. A missing synthesis may be repaired after the release event by appending that evidence alone.

Finish every actor. Release each lane through the helper and preserve dirty, unintegrated, conflicted, unauthorized, or residual state. Render `LEDGER.md` from `events.jsonl`; never edit generated prose.

Return exactly one outcome from `validate-state`: `complete`, `partial`, or `blocked`. `complete` requires the approved current `HEAD`, accepted latest review, required review count, final proof, verified child and parent closeout, applicable push proof, friction synthesis, no open Repair generation, and safe lane dispositions. Every outcome includes recovery-ready state and leaves no active lane or uncertain partial mutation unaccounted.
