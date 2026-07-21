---
name: parallel-implement
description: Implement one root-owned parent ticket graph through dependency-ready isolated lanes, serial landing, formal review, and verified closeout. Root-only; delegated invocation is a routing blocker.
---

# Parallel Implement

**Trace -> Select -> Open -> Drain -> Downshift -> Checkpoint -> Review -> Lock -> Release**

Drain one parent-backed implementation graph without confusing parallel activity with completion.

**Root only.** The root owns scope, dispatch, landing, formal review, tracker mutation, and release. If invoked by a delegated agent, stop before mutation and return a routing blocker.

**Lane worker:** a direct child with one isolated worktree, one clean commit, and focused proof. The first actor is the **warm primary**: create it with fresh context, then reuse it for successive complete assignments while it is idle, safe, and useful. Reuse the actor, never its checkout. Additional actors are fresh-context children for proved-independent substantial work. Workers do not spawn, integrate, review themselves, mutate trackers, or push. The root normally integrates; use a child integrator only when the integration branch itself is a bounded independent lane. Formal review stays separate from implementation.

`events.jsonl` is canonical and `LEDGER.md` is generated. Use [RUN-LEDGER.md](references/RUN-LEDGER.md) and `scripts/run_ledger.py`; do not hand-author event IDs, receipts, or rendered state on the normal path. The reducer remains the authority: a helper suggestion never overrides a failed gate.

Campaign terms are stable: the **Charter** fixes outcome and authority; a **frontier** is the dependency-ready work considered for assignment; an **assignment** binds one actor to one reconciled lane and proof seam; a **result queue** holds returned but uninspected receipts; the **candidate** is one immutable proved integration SHA; **Lock** proves reviewed-tree and external closeout identity; **Release** is terminal.

Select the legal operation from canonical state:

| Current condition | Operation | Complete when |
| --- | --- | --- |
| No stream or unreconciled resumed stream | **Trace / Resume**, then **Reconcile** | Graph, Charter, checkout, actors, lanes, claims, tracker, remote, budgets, and continuation agree without unknown state |
| Reconciled unfinished graph; no active work or backpressure | **Select** | One executable frontier, width, reason, primary assignment, and latch state are recorded |
| Selected assignment has claim and capacity | **Open** | Claim read-back, exact base, preflight, generated brief, actor, report path, and liveness evidence are recorded |
| Actor active, result queued, commit accepted, or integration regressed | **Drain** | Returns are classified, accepted commits land serially, and current wave proof passes |
| Correctness, overlap, staleness, contention, or backpressure makes width unsafe | **Downshift** | Width one and its cause read back; safe work has a drain or quiesce disposition |
| Safe execution cannot continue | **Checkpoint** | Actors are idle and complete recovery state plus the exact continuation read back |
| Graph drained and current candidate proved | **Review**; then admitted **Repair** or decision | Immutable review decision is recorded; every repaired successor is proved and reviewed again |
| Review accepted at current integration HEAD | **Lock** | Child-first closeout, parent rule, claims, applicable push, and every external read-back match the approved SHA |
| Reducer admits terminal `complete` | **Release** | Actors and lanes are safe, friction is adjudicated, ledger and passive result render |

**Reconcile universally:** refresh Git, worktrees, actors, claims, ledger, tracker, remote, and integration-checkout ownership before every dispatch, landing, resumed mutation, formal review, or terminal transition.

Use artifacts only for their owned claim:

- the absolute `events.jsonl` stream owns durable campaign facts;
- status and `LEDGER.md` are derived projections, never state authority;
- a generated brief scopes one assignment, and its receipt is worker evidence, not acceptance;
- a prepared terminal packet proposes one currently applicable transition but supplies no judgment or provider success;
- review proves one immutable candidate; tracker, remote, claim, and checkout read-backs prove only the external fact observed.

## Trace

Apply `docs/agents/engineering-contract.md`. Read tracker and domain guidance before touching those surfaces. If required setup is missing or incompatible, recommend `$repo-bootstrap` and stop.

Resolve exactly one parent and its exhaustive child and follow-up graph. Record the Source Trace, parent outcome, fixed point, child snapshot, dependency edges, acceptance, required proof, commitment boundary, non-goals, review route, and parent closeout rule. The parent selects work; it is not direct implementation scope.

Start through `run_ledger.py start` with one scope packet and one absolute, initially missing `events.jsonl` path. Runtime contract 3 is the default. Repair generations default to four, review invocations to five, and required completed reviews to one. The extra review slot preserves one successor review for each possible Repair. These are ceilings, not quotas; change them only from explicit caller authority and never below consumption. Record the integration checkout as either user-owned `existing-checkout` or campaign-owned `managed-integration-worktree`; unknown ownership blocks Open.

When an existing stream is present, use `status`. Resume a checkpoint only after fresh Git, worktree, actor, tracker, claim, and remote reconciliation. A missing actor is not completion.

If the graph is incomplete, ambiguous, or not Ready-for-agent, return one exhaustive repair packet and recommend `$to-tickets`; do not dispatch a partial interpretation.

For any stateful ticket, verify that acceptance carries the applicable state-boundary matrix. Missing supported branches are a Ready-for-agent defect: include them in the exhaustive graph-repair packet rather than treating them as optional worker discovery.

## Select

Choose the next dependency-ready frontier from reconciled tracker and ledger state. Keep the critical-path item with the warm primary. A verified landing may satisfy an in-campaign execution dependency as `landed-awaiting-lock`; tracker closure still waits for Lock. Rollback, invalidation, or failed proof reblocks it.

Apply the frontier gate across semantics, acceptance, write scope, proof, dependencies, live slots, and root review bandwidth. Disjoint files alone do not prove independence.

- Select one ticket by default and keep one implementation actor.
- A cold start may use two actors only for two obviously substantial items with disjoint semantic ownership, production writes, proof fixtures, and immediate root inspection capacity.
- After an eligible clean parallel wave, widen by one only when another independent substantial item is ready, no result is queued, no serial latch is active, and root capacity is immediate. Count implementation actors and a child integrator against the five-subagent ceiling; preserve capacity for prompt inspection and later independent Review.
- Add a fresh actor only when the expected implementation saving exceeds dispatch, context loading, root inspection, landing, and recombined-proof cost.
- Keep shared caller-facing seams, shared production files, performance work, terminal integration, corrections, and Review Repairs serial.
- Never open behind an uninspected result queue or beyond immediate root review bandwidth.
- Stop with exact blockers when nothing is executable.

Five concurrent subagents is the ceiling, not a target. The root remains one of the six active slots and must retain enough attention to inspect every returned lane promptly.

Record every selected frontier with width and one compact reason: `serial-default`, `serial-tripwire`, `serial-backpressure`, `parallel-independent`, or `widen-after-clean-wave`. The helper validates recorded mechanics and the five-agent cap; the root alone attests substantial work, semantic independence, proof isolation, and inspection capacity.

**Tripwire:** protected data, permissions, trust boundaries, irreversible state, migrations, and cutovers require one production-path tracer first, including retry, rollback, and partial-state proof.

**Downshift:** serialize new dispatch whenever correctness, overlap, invalidation, contention, proof capacity, or root inspection capacity makes parallel work unsafe. Record the corresponding `downshift-*` reason and latch width one. Preserve and drain safe active work; do not discard it. A clean serial wave does not reopen parallelism. Clear the latch only with recorded evidence that an external capacity or workload change removed its cause, then reopen at no more than two.

## Open

Claim each selected ticket and read back the claim. Open its lane through `lane_worktree.py open` using [CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md). Dispatch only from `ok: true` preflight evidence for the exact base, actor, checkout, startup proof, and Python import provenance.

Apply the lane packet to the ledger and generate the mode-specific brief with `run_ledger.py brief`. For the first assignment, launch the primary with `fork_turns="none"`. For later serial assignments, send the idle primary only the new complete generated brief. Launch every additional actor with `fork_turns="none"`. Always supply the absolute worktree, file-backed proof command, stable temp roots, report path, and an observable liveness checkpoint.

Replace the primary only at a clean boundary when it is unavailable, unsafe to resume, or materially misled by retained context. Record the checkpoint and replacement reason; create the replacement with fresh context. Do not change an actor's reasoning tier in place or choose tiers automatically.

A proposed concrete write set is useful when shared fixtures or generated artifacts are plausible. Require it before deep work only when expected scopes do not expose likely overlap.

## Drain

Classify every queued worker return before new dispatch. The compact receipt must name status, commit when done, changed-scope summary, proof outcome and log path, structured slice-proof evidence, skipped checks, risks, report path, and final status. Successful proof records command identity, exit code, duration, counts, environment identity, and log digest; failed proof adds one capped excerpt. Accept only a clean committed `done` with criterion-to-proof evidence in the report. A `blocker` retries only after its condition changes. A `needs-feedback` packet may continue once when the same actor must complete or explain its own bounded result. Otherwise open a fresh reconciled lane.

Land accepted packets serially. Inspect the worker diff, expected and actual scope, stale-base overlap, conflicts, and slice proof at the highest meaningful public seam. Then run one recombined wave proof on the current integration HEAD, record that HEAD, refetch the dependency fingerprint, and select again. Loop-close proof recombines applicable state-boundary matrices across landed interfaces, especially where access paths, configuration variants, or lifecycle transitions interact. Run one current candidate proof before Review; do not repeat broad proof for an unchanged candidate.

If integration proof fails after landing and before formal review, record one trusted regression and choose an authorized correction route: the original worker once, a fresh correction lane, or an explicitly authorized tiny root fix. The correction must start from the recorded integration HEAD, stay within structured scope IDs, prove the RED and affected paths, descend from that HEAD, and leave integration clean. It advances integration HEAD and invalidates prior drained or review-ready evidence; it does not consume a Review Repair generation.

Stale or conflicted packets do not land. Rebase, redispatch, serialize, reject, or invoke `$resolving-merge-conflicts` from preserved state.

When execution must stop before the graph drains, quiesce all actors and record a nonterminal checkpoint with outcome `partial` or `blocked`. Account for current HEAD, integration ownership and registration, actor and lane dispositions, continuation, frontier, latch and cause, blockers, result queue, proof state, open correction or Repair, tracker and remote state, and every retained or released claim. Resume only through fresh reconciliation. Release is never used for a resumable partial campaign.

## Review

Pin one immutable candidate only after the graph is drained, lanes are idle, integration is clean, child dispositions are complete, and current candidate proof passes. Use `run_ledger.py prepare --step review`, supply the root-owned route, reason, findings, decision, and residual risk, then apply the packet. Invoke `$review` by default or `$convergent-pr-review` for high risk, with `Spec required: yes`, the Charter, Source Trace, fixed point, target, and required proof.

The review report grants no mutation. Automatically repair only one complete batch whose blockers are admitted, `automatic-in-scope`, Charter-preserving, bounded by proof, and within both the Repair and successor-review budgets. Reuse the original implementation owner or warm primary when safe. Use a fresh actor for independent review, not routine repair. Prepare and apply one Repair plan and its completion packet. Any ambiguous or decision-required blocker returns the whole decision packet. Every repaired successor receives a fresh formal review.

## Lock

Open Lock only when the accepted reviewed HEAD equals current integration HEAD and the required review count is complete. Prepare one closeout plan and typed packet from the ledger; mutate trackers child first, perform **Mutation read-back** after every change, add all read-backs to that packet, close the parent only after its rule passes, and release claims. The helper ingests provider evidence but never performs or infers mutation. Push only the approved closeout SHA and verify the remote.

## Release

Quiesce every actor and clean or explicitly preserve every lane. Prepare and apply Release with deliberate friction synthesis; `run_ledger.py finish` records `none_observed` when there are no observations, validates terminal completion, renders `LEDGER.md`, and returns passive evidence for elapsed time, contexts, width, proof load, queueing, rework, operator packets, fallbacks, correctness, and unavailable telemetry. It never invents a score or token estimate.

Runtime-contract-3 Release is terminal and accepts only `complete`: approved current HEAD, accepted formal review, required review count, final proof, verified child and parent closeout, applicable push proof, friction synthesis, no open repair, and safe lanes. Return recovery-ready state for every nonterminal outcome.

## Context and Return

Load [RUN-LEDGER.md](references/RUN-LEDGER.md) only for start, resume, status disputes, Checkpoint, Review, Repair, closeout, or Release. Load [CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md) only for lane or integration-checkout lifecycle work. Load [WORKER-BRIEF.md](references/WORKER-BRIEF.md) only to generate or interpret an assignment; the worker receives its complete generated brief, not the parent conversation. Load [INTEGRATOR-BRIEF.md](references/INTEGRATOR-BRIEF.md) only for a genuinely bounded child integration lane. Route preserved Git conflicts to `$resolving-merge-conflicts` with their exact state.

Return exactly one of:

- `complete`: released HEAD, proof and review identity, verified child and parent closeout, push/read-back result, lane dispositions, passive efficiency result, and measurement gaps;
- `partial`: current HEAD, canonical stream, completed and remaining graph, safe actors and lanes, claims, result queue, proof state, tracker and remote observations, exact continuation;
- `blocked`: all `partial` recovery fields plus the blocker, authority needed, and decision packet when applicable;
- `decision-required`: immutable target, complete classified finding or authority packet, options and consequences, residual risk, and exact resume operation;
- a routing blocker before mutation when invocation is not root-owned; or
- one exhaustive graph-repair packet before dispatch when readiness is defective.

No campaign completes on dispatch, a worker receipt, a clean commit, a generated packet, a review report, tracker mutation without read-back, or a clean serial wave. Completion is terminal Release at the verified reviewed current HEAD.
