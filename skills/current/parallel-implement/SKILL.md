---
name: parallel-implement
description: Run a wavefront implementation loop over a ready frontier: orchestrator, hot integrator, and isolated one-commit workers.
---

# Parallel Implement

Run a **wavefront** over independently-grabbable issues.

The loop is **ready frontier -> wave dispatch -> one-commit workers -> hot integrator -> loop-close review -> tracker lock -> release sweep**.

- **Orchestrator**: owns scope, DAG, routing packet, ledger, review route, tracker lock, closeout approval, and release sweep.
- **Integrator**: hot serial lane; owns the integration checkout, post-landing proof, loop-close execution, and heartbeat.
- **Workers**: isolated one-issue lanes; produce one clean commit plus focused proof, or a blocker packet.

Use this when a **ready frontier** exists and serial integration would otherwise block implementation throughput.

Ready frontier means two or more unblocked issues can start now without dependency or write-scope overlap.

**Downshift** when fewer than two issues can run independently, the DAG is mostly linear, readiness is missing acceptance/dependency/proof/write-scope detail, env isolation is unavailable, or the first worker pass would be setup work instead of implementation. Use a smaller worker limit, shallow mode, or ordinary `$implement`.

Shallow mode means one worker, one integrator landing, focused proof, loop-close review, and tracker lock without wave dispatch.

## References

- Start the integrator with `references/INTEGRATOR-BRIEF.md`.
- Launch Codex-managed workers with `references/CODEX-WORKTREE-LAUNCH.md`.
- Dispatch workers with `references/WORKER-BRIEF.md`.
- Track the run in `references/RUN-LEDGER.md`.

## Preconditions

This is execution, not shaping. Read `docs/agents/engineering-contract.md`; read tracker docs only for scope, labels, readiness, or closeout; read `docs/agents/domain.md` only when domain semantics may affect the run.

Require a ready frontier: independently-grabbable issues with acceptance criteria, dependency order, parallel-safety notes, proof lanes, and load-bearing seams where needed. If readiness is weak, stop with gaps; do not repair readiness in this flow.

Require a tiny **contract matrix** before dispatch when correctness depends on data contracts, claim levels, permissions, public semantics, or state transitions: `case | allowed | invalid examples | proof`.

## Loop

Routing packet: selected scope, run fixed point, dependency DAG, first wave, worker limit, write-scope risks, proof budget, validation environment, integration checkout, loop-close route, tracker lock, durable closeout destination, cleanup/release rule, and expected Git/tool approvals.

Default worker limit is 2-3.

Never launch more workers than the orchestrator can review and the integrator can land within one wave.

Use more only when write scopes, env isolation, and review bandwidth are proven. Review bandwidth means the orchestrator/integrator can inspect every worker packet before the next frontier decision.

Expected approvals should name likely write/metadata operations: `git cherry-pick`, `git worktree`, `gh issue edit`, `gh issue close`, dependency commands, or tracker connector mutations.

Launch gate: `$parallel-implement` authorizes subagents for this run. Dispatch one fresh worker per issue only through a verified worktree route.

Verified worktree route: prefer Codex-managed worktrees created by the Codex app, not `git worktree`; follow `references/CODEX-WORKTREE-LAUNCH.md` before any manual fallback.

**Wavefront**: dispatch only independent issues in the current frontier. Rescan after serial landings; do not spawn blocked, dependent, or write-overlapping issues. For mostly linear chains, lower the worker limit and keep the integrator hot.

**Handoff gate**: delegated work is not done until the worker sends a work-done handoff and the orchestrator accepts its result packet. Do not infer completion from dispatch, silence, elapsed time, or partial progress.

**Proof budget**: workers run focused proof by default; the integrator runs post-landing touched-area proof; loop close runs broad validation and fixed-point review. Worker broad suites require shared-behavior risk or an explicit route. Shared-behavior risk means public API, shared module, schema/migration, cross-cutting config, cache/performance behavior, or data contract.

**Env lock**: workers must not run broad dependency-mutating commands such as `uv sync`, `pip install`, `npm install`, or cache-rebuilding setup against a shared checkout/env unless routed. Env isolation means worker-specific venv/cache/temp paths, or no worker dependency mutation. Leave env-heavy validation to the integrator and loop close when isolation is weak.

**Hot integrator**: prefer a dedicated integration worktree. If the integrator shares the orchestrator checkout, use a same-checkout lock: only the integrator edits, tests, stages, or lands there while active. While the integrator owns a checkout, the orchestrator is read-only there: no edits, tests, staging, or landing commands. The integrator reports `running`, `blocked`, `waiting`, `ready-to-land`, or `packet-ready` after gates, long commands, approval waits, and validation results.

**Delta packets**: continuation prompts carry only the delta: issue, ledger event, expected base, accepted worker SHA, and next need.

**Thin ledger**: use the append-only event ledger in `references/RUN-LEDGER.md`. Do not maintain duplicate state tables that can drift.

Loop-close route: default to `$review` from the run fixed point over the integrated diff. Use approved `$convergent-pr-review` only for high-risk integrated diffs: release gates, shared plumbing, migrations, security/permissions, CI/workflow/config, public interfaces, data contracts, performance/cache risk, or broad integration uncertainty.

Record loop-close route, executor, fixed point, and fallback in the ledger.
Record run friction, skill bugs, and skill/supporting-file improvement ideas in the ledger and final report.

1. Select scope, build the DAG, and name the ready frontier.
2. Capture run fixed point and start the thin ledger.
3. Start the hot integrator, preferably in a dedicated integration worktree.
4. Claim the first wave up to the worker limit.
5. Dispatch only verified one-commit workers.
6. Accept or reject worker result packets.
7. Queue accepted commits; route feedback or blockers.
8. Integrator lands serially and reports heartbeat packets.
9. Rescan the frontier after landings; repeat waves until drained or blocked.
10. Trigger loop-close validation and review.
11. Orchestrator approves closeout, updates tracker, and runs the release sweep.

## Gates

Worker fixes pass two acceptance gates before landing:

- **Orchestrator acceptance**: result packet, scope, acceptance proof, residual risk.
- **Integrator pre-landing gate**: actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof.

Pre-landing gate is acceptance, not formal review. If the worker diff needs deeper review before landing, the integrator returns a blocker or review-route escalation packet to the orchestrator.

Stale-base packet: if serial landings make a worker base stale, the integrator returns a stale-base packet; the orchestrator decides whether to rebase, re-dispatch, serialize, or reject.

Review is orchestrator-owned and integrator-executed. The orchestrator selects `$review`, approved `$convergent-pr-review`, or a local fallback in the routing packet; the integrator runs exactly that route. If landing reveals higher risk, the integrator returns a review-route escalation packet instead of silently changing route.

Loop-close fixes take the fast path only when tiny, local, low-risk, and orchestrator-approved for direct integrator repair. Tiny fix means one small localized diff with no contract, schema, dependency, security, or public-behavior change. Otherwise dispatch a micro-worker.

## Lock

Move accepted work to `implemented`; close only when tracker docs or the user say to close. Make repo-local tracker closeout review-visible before final review. Fill the ledger closeout summary before tracker mutation. Copy durable facts to the routed closeout destination before cleanup. Mutate connector-backed trackers only after review passes and required commits exist. Batch labels when the tracker supports it; comment from generated closeout notes; close connector or CLI issues one by one when batch close is unsupported.

Workers and integrator may prepare closeout notes; only the orchestrator mutates connector-backed tracker labels, comments, or state.

Orchestrator approval is the main agent's post-review gate unless the user asks to confirm.

Release sweep is done only after the ledger has one release event covering active threads, worktrees, branches, tracker, push state, skipped checks, and residual risk. Remove worker worktrees and keep worker branches unless cleanup rules say otherwise.

Done means the scope is complete or blocked; accepted work landed serially; validation and loop-close review passed or blockers are recorded; tracker lock was respected; durable notes carry worker SHAs, integration SHAs, validation, skipped checks, residual risk, and skill feedback; unrelated work is preserved.
