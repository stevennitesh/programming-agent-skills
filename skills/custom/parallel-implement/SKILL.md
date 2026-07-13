---
name: parallel-implement
description: Run a ready-frontier wavefront with isolated one-commit lane workers and an adaptive serial integration lane.
---

# Parallel Implement

Run a **wavefront** over ready-for-agent work.

The loop is **ready frontier -> isolated one-commit lane workers -> accepted packets -> adaptive integration lane -> loop-close lock -> tracker lock -> release sweep**.

- **Orchestrator**: owns source trace, scope, DAG, routing packet, ledger, worker acceptance, review route, tracker lock, closeout decision, and release sweep.
- **Integration lane**: serially lands accepted work. The orchestrator owns it by default; a hot or late integrator owns it only when routed.
- **Lane workers**: isolated one-item worktrees; produce one clean local commit plus focused proof, or a blocker packet. Within this skill, `worker` means lane worker.

A **ready frontier** is the set of unblocked, unclaimed work items that can start now without dependency or write-scope overlap. A wave requires at least two.

Use this when a ready frontier exists and parallel implementation can outrun serial work without outrunning integration.

**Downshift:** when only one bounded item is in scope, return `$implement` as the next route and stop before dispatch. When several items must serialize because isolation cannot be established, return their order and route the first through `$implement`. Use **shallow mode** only when at least two isolated lane workers can still run in one finite wave. Return readiness gaps to shaping.

Shallow mode means one wave of two or three workers, focused proof, orchestrator-owned landing, loop-close lock, applicable tracker lock, and no persistent integrator.

## References

- Start a routed hot or late integrator with `references/INTEGRATOR-BRIEF.md`.
- Launch isolated workers or a dedicated integration lane with `references/CODEX-WORKTREE-LAUNCH.md`.
- Dispatch workers with `references/WORKER-BRIEF.md`.
- Build the routing packet and track the run in `references/RUN-LEDGER.md`.

## Preconditions

Apply the **setup gate**: read `docs/agents/engineering-contract.md`; when tracker work is in scope, read `docs/agents/issue-tracker.md` and what it points to. If a required setup document or named operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`. Read `docs/agents/domain.md` only when domain semantics affect the run.

Build the **Source Trace** from the current request, selected parent or packet, every in-scope work item and decision-bearing comment, repo `AGENTS.md`, and every named source. Record it once in the thin ledger. Pass each worker its relevant slice unchanged and give the integration lane the full trace for loop-close review.

Require every frontier item to have settled acceptance criteria, dependency order, parallel-safety notes, a proof lane, expected write scope, and load-bearing seams where needed. Return gaps to shaping before dispatch.

Require a **contract matrix** when correctness depends on data contracts, claim levels, permissions, public semantics, or state transitions: `case | allowed | invalid examples | proof`.

## Integration Modes

- **Shallow mode:** one finite wave; the orchestrator lands accepted commits after or between worker completions.
- **Hot integrator:** a persistent subagent lands while workers continue or when a landing unlocks the next frontier.
- **Late integrator:** a fresh subagent assembles a completed wave when integration is semantically complex or loop-close validation is long, but no useful overlap exists.

**Overlap gate:** start a hot integrator only when it can land accepted work while another worker continues, or when a landing unlocks the next frontier. Otherwise the orchestrator owns serial landing. Spawn a late integrator only when its fresh integration context is worth more than its startup and handoff cost.

## Loop

Build the routing packet from `references/RUN-LEDGER.md`. Resolve every field or mark it `not applicable` before dispatch.

**Review bandwidth** sets wave size: default `2-3`. Reserve one agent slot for the orchestrator and one for an active integrator; cap the rest by the worker packets the orchestrator can inspect and the integration lane can land before the next frontier decision. Increase only after write scopes and env isolation are proven.

**Permission plan:** record likely sandbox-crossing or external actions: worktree creation and cleanup, dependency installation, network access, push, and connector-backed tracker mutation. External mutations follow tool and repo policy at the point of action.

**Landing harness:** use a repo-owned deterministic landing command when available. Otherwise run the pre-landing gate manually. Either route verifies base, scope, new files, stale-base overlap, landing result, touched-area proof, and the ledger event.

**Dispatch:** choose the integration mode first. For a hot integrator, start it and accept its integrator-ready packet before workers launch. Then launch one fresh worker per selected frontier item, up to the worker limit, through the isolated route in `references/CODEX-WORKTREE-LAUNCH.md`. For a late integrator, start it after the wave finishes and accept its ready packet before the first landing.

**Wavefront:** dispatch only the independent work in the current frontier. Rescan after serial landings. Blocked, dependent, or write-overlapping work stays out of the wave.

**Handoff gate:** only an accepted work-done packet closes delegated work. Dispatch, silence, elapsed time, or partial progress leaves the gate open.

**Proof budget:** workers run focused proof; the integration lane runs post-landing touched-area proof; loop close runs broad validation and fixed-point review. Worker broad suites require shared-behavior risk or an explicit route. Shared-behavior risk includes public APIs, shared modules, schema or migrations, cross-cutting config, cache or performance behavior, and data contracts.

**Env lock:** each lane uses its own repo-local `.tmp/parallel-implement/<run-id>/lanes/<lane-id>/` cache and temp paths, plus an isolated venv, or leaves dependency mutation to the integration lane. Broad dependency-mutating commands against a shared checkout or environment require an explicit route.

**Hot integrator:** prefer a dedicated integration worktree. A shared orchestrator checkout uses a same-checkout lock: the integrator is the only writer and test runner while active; the orchestrator remains read-only there. The integrator reports `starting`, `ready`, `running`, `blocked`, `waiting`, `ready-to-land`, or `packet-ready` after gates, long commands, approval waits, and validation results.

**Delta packets:** continuation prompts carry only the delta: work item, ledger event, expected base, accepted worker SHA, and next need.

**Thin ledger:** instantiate the run ledger from `references/RUN-LEDGER.md`, append each event once, and derive routing and closeout from that stream.

1. Trace sources, select scope, build the DAG, and name the ready frontier.
2. Capture the run fixed point, start the thin ledger, and resolve the routing packet.
3. Choose the integration mode; start and ready the routed integrator at its mode-specific gate.
4. Claim and dispatch the current wave through isolated worktrees.
5. Accept or reject worker result packets.
6. Land accepted commits serially through the assigned integration lane and landing route.
7. Rescan the frontier after landings; repeat until drained or blocked.
8. Assemble review-visible repo-local closeout metadata and pin the immutable review target.
9. Run loop-close validation and review; apply the delta gate until the closeout target is approved.
10. Accept or block closeout, apply tracker lock, and run the release sweep.

## Gates

Worker fixes pass two acceptance gates before landing:

- **Orchestrator acceptance:** result packet, scope, acceptance proof, and residual risk.
- **Pre-landing gate:** actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof.

The orchestrator or routed integrator executes the pre-landing gate. It is acceptance, not formal review. A diff needing deeper review returns a blocker or review-route escalation packet.

**Stale-base packet:** when serial landings obsolete a worker base, the integration lane returns the packet; the orchestrator chooses rebase, re-dispatch, serialization, or rejection.

**Review route:** invoke `$review` by default. Invoke `$convergent-pr-review` for high-risk integrated diffs matching its trigger. The orchestrator selects and records the route; the integration lane executes only that route. An unavailable route blocks closeout. Higher risk discovered during landing returns a review-route escalation packet.

**Loop-close lock:** before review, require a clean in-scope integration state with all integrated work and review-visible repo-local closeout metadata committed. Pin the integration `HEAD` as the immutable review target and run the assigned route from the run fixed point.

After any review fix lands, inspect `<reviewed-head>..<current-head>`. A tiny finding-only fix may use targeted proof when the routing packet permits it. A material behavior, scope, contract, schema, dependency, security, or public-interface delta requires a new review target and another loop-close review.

Record the approved closeout `HEAD`. External tracker mutation, push, and release require the current integration `HEAD` to match it.

## Lock

**Tracker lock:** follow `docs/agents/issue-tracker.md`. Fill the ledger closeout summary before mutation, include repo-local closeout changes in final review, and mutate connector-backed tracker state only after the approved closeout `HEAD` and required commits exist. Close only when tracker policy or the user says to close. The orchestrator owns external tracker mutations and push.

Apply the tracker's **Mutation read-back** rule before recording tracker lock complete. A partial or unverifiable mutation blocks closeout.

Workers and the integration lane may prepare closeout notes. The orchestrator accepts or blocks closeout after review and asks the user only when requested confirmation or tracker policy requires it.

**Release sweep:** close only after one ledger event accounts for every selected item and every active lane. Finish or stop every worker and integrator, release claims, remove worker worktrees under the routed cleanup rule, preserve branches unless that rule says otherwise, and record tracker, push, skipped-check, and residual-risk state.

Return the ledger-derived Closeout Summary. Every selected item is integrated, rejected, blocked, or routed to follow-up; every lane and claim has a release state.

## Completion Criteria

Complete only when Source Trace and the routing packet are recorded; the integration mode is chosen; every routed integrator passed its ready gate; every worker packet is accepted, rejected, or blocked; accepted work landed serially; the approved closeout `HEAD` passed validation and its assigned review route; tracker lock was respected; the release sweep accounts for every item, lane, claim, worktree, branch, tracker action, and push state; skipped checks, residual risk, and skill feedback are reported; and unrelated work is preserved.
