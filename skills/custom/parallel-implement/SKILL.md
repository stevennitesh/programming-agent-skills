---
name: parallel-implement
description: Implement one root-owned parent ticket graph through dependency-ready isolated lanes, serial landing, formal review, and verified closeout. Root-only; delegated invocation is a routing blocker.
---

# Parallel Implement

**Trace -> Select -> Open -> Drain -> Review -> Lock -> Release**

Drain one parent-backed implementation graph without confusing parallel activity with completion.

**Root only.** The root owns scope, dispatch, landing, formal review, tracker mutation, and release. If invoked by a delegated agent, stop before mutation and return a routing blocker.

**Lane worker:** a direct fresh-context child with one isolated worktree, one clean commit, and focused proof. Workers do not spawn, integrate, review themselves, mutate trackers, or push. The root normally integrates; use a child integrator only when the integration branch itself is a bounded independent lane. Formal review stays separate from implementation.

`events.jsonl` is canonical and `LEDGER.md` is generated. Use [RUN-LEDGER.md](references/RUN-LEDGER.md) and `scripts/run_ledger.py`; do not hand-author event IDs, receipts, or rendered state on the normal path. The reducer remains the authority: a helper suggestion never overrides a failed gate.

## Trace

Apply `docs/agents/engineering-contract.md`. Read tracker and domain guidance before touching those surfaces. If required setup is missing or incompatible, recommend `$repo-bootstrap` and stop.

Resolve exactly one parent and its exhaustive child and follow-up graph. Record the Source Trace, parent outcome, fixed point, child snapshot, dependency edges, acceptance, required proof, commitment boundary, non-goals, review route, and parent closeout rule. The parent selects work; it is not direct implementation scope.

Start through `run_ledger.py start` with one scope packet. Runtime contract 3 is the default. Repair generations default to two, review invocations to three, and required completed reviews to one. These are ceilings, not quotas; change them only from explicit caller authority and never below consumption.

When an existing stream is present, use `status`. Resume a checkpoint only after fresh Git, worktree, actor, tracker, claim, and remote reconciliation. A missing actor is not completion.

If the graph is incomplete, ambiguous, or not Ready-for-agent, return one exhaustive repair packet and recommend `$to-tickets`; do not dispatch a partial interpretation.

For any stateful ticket, verify that acceptance carries the applicable state-boundary matrix. Missing supported branches are a Ready-for-agent defect: include them in the exhaustive graph-repair packet rather than treating them as optional worker discovery.

## Select

Choose the next dependency-ready frontier from reconciled tracker and ledger state. A verified landing may satisfy an in-campaign execution dependency as `landed-awaiting-lock`; tracker closure still waits for Lock. Rollback, invalidation, or failed proof reblocks it.

Apply the frontier gate across semantics, acceptance, write scope, proof, dependencies, live slots, and root review bandwidth. Disjoint files alone do not prove independence.

- Select one ticket when independence or review capacity is uncertain.
- Select up to three only when at least two tickets are semantically independent and every packet can be inspected before the next frontier.
- Stop with exact blockers when nothing is executable.

**Tripwire:** protected data, permissions, trust boundaries, irreversible state, migrations, and cutovers require one production-path tracer first, including retry, rollback, and partial-state proof.

**Downshift:** serialize whenever independence, scope, slots, or review bandwidth is uncertain. Reopen parallelism only from evidence.

## Open

Claim each selected ticket and read back the claim. Open its lane through `lane_worktree.py open` using [CODEX-WORKTREE-LAUNCH.md](references/CODEX-WORKTREE-LAUNCH.md). Dispatch only from `ok: true` preflight evidence for the exact base, actor, checkout, startup proof, and Python import provenance.

Apply the lane packet to the ledger, generate the mode-specific brief with `run_ledger.py brief`, then launch one direct child with `fork_turns="none"`, the absolute worktree, stable temp roots, and an observable liveness checkpoint.

A proposed concrete write set is useful when shared fixtures or generated artifacts are plausible. Require it before deep work only when expected scopes do not expose likely overlap.

## Drain

Classify every worker return. Accept only a clean committed `done` with criterion-to-proof evidence. A `blocker` retries only after its condition changes. A `needs-feedback` packet may continue once when the same actor must complete or explain its own bounded result. Otherwise open a fresh reconciled lane.

Land accepted packets serially. Inspect the worker diff, expected and actual scope, stale-base overlap, conflicts, and focused proof. Then run touched-area integration proof, record the new integration HEAD, refetch the dependency fingerprint, and select again. Loop-close proof recombines applicable state-boundary matrices across landed interfaces, especially where access paths, configuration variants, or lifecycle transitions interact. Broad loop-close proof is required before Review.

If integration proof fails after landing and before formal review, record one trusted regression and choose an authorized correction route: the original worker once, a fresh correction lane, or an explicitly authorized tiny root fix. The correction must start from the recorded integration HEAD, stay within structured scope IDs, prove the RED and affected paths, descend from that HEAD, and leave integration clean. It advances integration HEAD and invalidates prior drained or review-ready evidence; it does not consume a Review Repair generation.

Stale or conflicted packets do not land. Rebase, redispatch, serialize, reject, or invoke `$resolving-merge-conflicts` from preserved state.

When execution must stop before the graph drains, quiesce all actors and record a nonterminal checkpoint with outcome `partial` or `blocked`. Account for current HEAD, safe lane dispositions, continuation, frontier, blockers, tracker and remote state, and every retained or released claim. Resume only through fresh reconciliation. Release is never used for a resumable partial campaign.

## Review

Pin one immutable candidate only after the graph is drained, lanes are idle, integration is clean, child dispositions are complete, and loop-close proof passes. Invoke `$review` by default or `$convergent-pr-review` for high risk, with `Spec required: yes`, the Charter, Source Trace, fixed point, target, and required proof.

The review report grants no mutation. Automatically repair only one complete batch whose blockers are admitted, `automatic-in-scope`, Charter-preserving, bounded by proof, and within both the Repair and successor-review budgets. Any ambiguous or decision-required blocker returns the whole decision packet. Every repaired successor receives a fresh formal review.

## Lock

Open Lock only when the accepted reviewed HEAD equals current integration HEAD and the required review count is complete. Generate the closeout plan from the ledger; mutate trackers child first, perform **Mutation read-back** after every change, close the parent only after its rule passes, and release claims. Push only the approved closeout SHA and verify the remote.

## Release

Quiesce every actor and clean or explicitly preserve every lane. Apply structured friction observations; `run_ledger.py finish` records `none_observed` when there are none, validates terminal completion, and renders `LEDGER.md`. Observed friction still requires deliberate synthesis.

Runtime-contract-3 Release is terminal and accepts only `complete`: approved current HEAD, accepted formal review, required review count, final proof, verified child and parent closeout, applicable push proof, friction synthesis, no open repair, and safe lanes. Return recovery-ready state for every nonterminal outcome.
