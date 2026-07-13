---
name: parallel-implement
description: Run two or more ready, non-overlapping work items as a wavefront through isolated worktrees, fresh-context one-commit workers, serial integration, root-owned review, tracker lock, and release sweep.
---

# Parallel Implement

Run a **wavefront** over ready-for-agent work:

**ready frontier -> two isolations -> fresh-context lane workers -> accepted packets -> serial integration -> root-owned review -> tracker lock -> release sweep**

- **Orchestrator**: sole dispatcher and final owner of Source Trace, scope, DAG, routing packet, thin ledger, worker acceptance, review route, tracker mutation, closeout, and release.
- **Integration lane**: serially lands accepted commits and runs routed integration validation. The orchestrator owns it by default; a hot or late integrator owns it only when routed. A child integrator returns a review-ready packet and never dispatches subagents or invokes formal review.
- **Lane workers**: each direct fresh-context child owns one ready item in one isolated worktree and returns one clean local commit plus focused proof, or a blocker packet. Within this skill, `worker` means lane worker.

**Two isolations:** a fresh subagent context isolates attention; a Git worktree isolates files. A delegated lane is ready only when both are established and preflight proves the assigned checkout.

**Root-only fan-out:** workers, an optional integrator, and formal reviewers are direct children of the orchestrator. Workers and integrators never spawn. The workflow never depends on recursive delegation.

A **ready frontier** is the set of unblocked, unclaimed work items that can start now without dependency, write-scope, or semantic overlap. A wave requires at least two and must outrun serial work without outrunning integration.

**Downshift:** when only one bounded item is in scope, return `$implement` as the next route and stop before dispatch. When several items must serialize because isolation cannot be established, return their order and route the first through `$implement`. Use **shallow mode** only when at least two isolated lane workers can still run in one finite wave. Return readiness gaps to shaping.

## References

- Start a routed hot or late integrator with `references/INTEGRATOR-BRIEF.md`.
- Launch isolated workers or a dedicated integration lane with `references/CODEX-WORKTREE-LAUNCH.md`.
- Dispatch workers with `references/WORKER-BRIEF.md`.
- Build the routing packet and track the run in `references/RUN-LEDGER.md`.

## Preconditions

Apply the **setup gate**: read `docs/agents/engineering-contract.md`; when tracker work is in scope, read `docs/agents/issue-tracker.md` and what it points to. If a required setup document or named operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`. Read `docs/agents/domain.md` only when domain semantics affect the run.

Build the **Source Trace** from the current request, selected parent or packet, every in-scope work item and decision-bearing comment, repo `AGENTS.md`, and every named source. Record it once in the thin ledger. Pass each worker its relevant slice unchanged and give the integration lane the full trace for integration validation.

Require every frontier item to have settled acceptance criteria, dependency order, parallel-safety notes, a proof lane, expected write scope, and load-bearing seams where needed. Return gaps to shaping before dispatch.

Require a **contract matrix** when correctness depends on data contracts, claim levels, permissions, public semantics, or state transitions: `case | allowed | invalid examples | proof`.

**Frontier gate:** cross-check acceptance criteria, contract matrices, shared interfaces, expected write scopes, proof lanes, and ordering assumptions across frontier items. Non-overlapping files do not prove semantic independence. When one item changes an assumption another consumes, add a dependency edge or apply Downshift before dispatch.

## Integration Modes

- **Shallow mode:** one finite wave of two or three workers, focused proof, orchestrator-owned landing, loop-close Lock, applicable tracker lock, and no persistent integrator.
- **Hot integrator:** a persistent subagent lands while workers continue or when a landing unlocks the next frontier.
- **Late integrator:** a fresh subagent assembles a completed wave when integration is semantically complex or loop-close validation is long, but no useful overlap exists.

**Overlap gate:** start a hot integrator only when it can land accepted work while another worker continues, or when a landing unlocks the next frontier. Otherwise the orchestrator owns serial landing. Spawn a late integrator only when its fresh integration context is worth more than its startup and handoff cost.

## Loop

Build the routing packet from `references/RUN-LEDGER.md`. Resolve every field or mark it `not applicable` before dispatch.

**Resume gate:** before any new dispatch, load the existing run ledger when one is supplied or already exists and reconcile it with Git, worktree, agent, claim, and tracker state. Treat accepted, landed, review-ready, tracker-lock, and release events as authoritative after reconciliation; do not redispatch or reland them. Resume from the first unresolved event. When the ledger and external state cannot be reconciled, return `blocked` with the exact mismatch.

**Slot lock:** set the worker limit to the smaller of three or the live slots remaining after reserving the orchestrator and any active child integrator. Require at least two worker slots for a wave; otherwise apply Downshift. Cap the wave further by the **review bandwidth** needed to inspect every packet before the next frontier decision. Formal review starts after lane agents are idle.

**Permission plan:** predict likely sandbox-crossing, external, or destructive actions before dispatch. The selected run authorizes scoped worker commits and the recorded serial landing route; recording another action does not authorize it. At the point of action, apply tool, repo, and user policy to worktree creation or cleanup, dependency installation, network access, push, connector-backed tracker mutation, external messages, force operations, and branch deletion.

**Landing harness:** record one landing mode and one executor before the first landing. Default detached one-commit workers to `cherry-pick`; use merge, squash, or patch application only when repo policy or the routing packet selects it. Use the repo-owned deterministic landing command when available; otherwise run the pre-landing gate manually. Every route verifies base, scope, new files, stale-base overlap, landing result, touched-area proof, and the ledger event.

**Default lane route:** pair one root-created detached Git worktree at the assigned base with one direct fresh-context worker launched with `fork_turns="none"`. Establish and independently preflight every lane through `references/CODEX-WORKTREE-LAUNCH.md`. A hot or late integrator uses a dedicated integration worktree; when that cannot be established, the orchestrator owns landing. Read **Explicit Background Task** only when the user explicitly requests separate, visible, or background worker tasks.

**Wavefront:** dispatch only the independent work in the current frontier. Rescan after serial landings. Blocked, dependent, or write-overlapping work stays out of the wave.

**Handoff gate:** only an accepted work-done packet closes delegated work. Dispatch, silence, elapsed time, or partial progress leaves the gate open.

**Proof budget:** workers run focused proof; the integration lane runs post-landing touched-area proof; loop close runs broad validation and fixed-point review. Worker broad suites require shared-behavior risk or an explicit route. Shared-behavior risk includes public APIs, shared modules, schema or migrations, cross-cutting config, cache or performance behavior, and data contracts.

**Env lock:** each lane uses lane-local `.tmp/parallel-implement/<run-id>/lanes/<lane-id>/` cache and temp paths. Use a routed shared interpreter or environment read-only when sufficient. When dependency mutation is required, use an isolated lane venv or leave the mutation to the integration lane. Broad shared dependency mutation requires an explicit route.

**Integrator heartbeat:** the child integrator reports `starting`, `ready`, `running`, `blocked`, `waiting`, `ready-to-land`, or `packet-ready` after gates, long commands, approval waits, and validation results.

**Delta packets:** continuation prompts carry only the delta: work item, ledger event, expected base, accepted worker SHA, and next need.

**Packet transport:** inline compact briefs and results. Put large source slices, diffs, logs, or reports under the lane's existing `.tmp/parallel-implement/<run-id>/lanes/<lane-id>/` path and pass exact paths plus a short status envelope. Exact requirements live once in the worker brief; continuations carry only deltas.

**Thin ledger:** instantiate the run ledger from `references/RUN-LEDGER.md`, append each event once, and derive routing and closeout from that stream.

1. Trace sources, select scope, build the DAG, and name the ready frontier.
2. Capture the run fixed point, start the thin ledger, and resolve the routing packet.
3. Choose the integration mode; start and ready the routed integrator at its mode-specific gate.
4. Claim and dispatch the current wave through isolated worktrees.
5. Classify and disposition worker result packets through Worker status.
6. Land accepted commits serially through the assigned integration lane and landing route.
7. Rescan the frontier after landings; repeat until drained or blocked.
8. Assemble review-visible repo-local closeout metadata, run final integration validation, and produce or accept a clean review-ready packet.
9. Wait until lane agents are idle, pin the immutable review target, and have the orchestrator invoke exactly the selected review route.
10. Route any finding fix through the assigned integration lane or a fresh lane worker scoped only to the accepted finding fix, repin when required by the delta gate, then apply tracker lock and run the release sweep.

## Gates

Worker fixes pass two acceptance gates before landing:

- **Orchestrator acceptance:** result packet, scope, acceptance proof, and residual risk.
- **Pre-landing gate:** actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof.

The orchestrator or routed integrator executes the pre-landing gate. It is acceptance, not formal review. A diff needing deeper review returns a blocker or review-route escalation packet.

**Worker status:**

- `done`: verify the complete packet, actual commit, scope, proof, final status, and residual risk; then accept or reject it.
- `needs-feedback`: keep the lane and claim open. Supply the missing decision or context through one delta packet, or return the commitment change to its owner. Do not accept or land the result yet.
- `blocker`: classify the blocker as context, permission or tool, stale base, readiness, task size, or commitment. Retry only after the input, route, base, capability, or task shape changes. Otherwise preserve the worktree and commit state, release the claim when appropriate, and record the blocked disposition.

**Stale-base packet:** when serial landings obsolete a worker base, the integration lane returns the packet; the orchestrator chooses rebase, re-dispatch, serialization, or rejection.

**Conflict gate:** when landing enters an in-progress Git operation, leaves unmerged paths or conflict markers, or partially applies a patch, pause the integration lane and record the operation, status, unmerged paths, landed state, and remaining worker commit. Invoke `$resolving-merge-conflicts` within its owned authorization boundary. Resume only after the integration checkout has a reconciled, explicitly authorized Git state; otherwise return `blocked` and preserve the partial state. Abort, continue, forced cleanup, reset, or side discard requires its normal explicit authority.

**Review route:** the orchestrator invokes `$review` by default and `$convergent-pr-review` for a high-risk integrated diff matching its trigger. The integration lane produces a clean review-ready packet containing the candidate `HEAD`, final validation, closeout metadata, skipped checks, and residual risk; a child integrator returns it and becomes idle. Before formal review, verify that no lane agent is running. Higher risk discovered during landing returns a review-route escalation packet to the orchestrator.

**Review acceptance:** the orchestrator records both the route result and the caller-owned Lock decision.

- `$convergent-pr-review`: `pass` unlocks review; `pass with residual risk` unlocks only when the routing packet or user accepts that residual risk; `blocked` and `incomplete` keep Lock closed.
- `$review`: P0/P1 findings or missing required validation keep Lock closed; an incomplete Spec axis keeps Lock closed. Record lower non-blocking findings as residual risk unless repo or user policy says otherwise.

An unavailable route, unresolved blocking finding, or unaccepted residual-risk result blocks closeout.

**Loop-close lock:** before review, require a clean in-scope integration state with all integrated work and review-visible repo-local closeout metadata committed. Pin the integration `HEAD` as the immutable review target and have the orchestrator invoke exactly the assigned route with `Spec required: yes`, the run Source Trace, selected work items and acceptance criteria, run fixed point, integration `HEAD`, and complete integrated diff.

After any review fix lands, inspect `<reviewed-head>..<current-head>`. A tiny finding-only fix may use targeted proof when the routing packet permits it. A material behavior, scope, contract, schema, dependency, security, or public-interface delta requires a new review target and another loop-close review.

Record the approved closeout `HEAD`. External tracker mutation, push, and release require the current integration `HEAD` to match it.

## Lock

**Tracker lock:** follow `docs/agents/issue-tracker.md`. Fill the ledger closeout summary before mutation, include repo-local closeout changes in final review, and mutate connector-backed tracker state only after the approved closeout `HEAD` and required commits exist. Close only when tracker policy or the user says to close. The orchestrator owns external tracker mutations and push.

Apply the tracker's **Mutation read-back** rule before recording tracker lock complete. A partial or unverifiable mutation blocks closeout.

After an authorized push, verify that the remote branch or PR head resolves to the approved closeout `HEAD` before recording push complete. A failed or unverifiable push remains `partial` or `blocked`.

Workers and the integration lane may prepare closeout notes. The orchestrator accepts or blocks closeout after review and asks the user only when requested confirmation or tracker policy requires it.

**Release sweep:** before any outcome, finish or stop every worker and integrator and append one event accounting for every selected item and active lane. Release claims, remove only clean worker worktrees under the routed cleanup rule, preserve anything blocked from cleanup, preserve branches unless that rule says otherwise, and record tracker, push, skipped-check, and residual-risk state.

Return the ledger-derived Closeout Summary. Every selected item is integrated, rejected, blocked, or routed to follow-up; every lane and claim has a release state.

## Completion Criteria

Return exactly one ledger Outcome: `complete`, `partial`, or `blocked`.

A `complete` outcome requires a current approved closeout `HEAD` that passed final validation and its assigned review route, followed by the applicable tracker lock and release sweep.

A `partial` or `blocked` outcome does not claim an approved closeout `HEAD`, completed review, tracker lock, or push that never occurred. Record the current integration `HEAD` and Git state, landed and unlanded items, exact blockers, next owner, remaining permissions or mutations, and every preserved or released lane, worktree, branch, and claim.

Every outcome requires Source Trace and the routing packet; one disposition for every worker and integrator packet; serial-landing accounting for every accepted commit; no active lane or unaccounted partial mutation; skipped checks, residual risk, and skill feedback; and preservation of unrelated work. A `complete` outcome additionally requires that every delegated lane used both isolations, fan-out stayed root-only, every routed ready gate passed, the integration lane produced a review-ready packet, formal review ran from the orchestrator after lane agents were idle, and the approved closeout `HEAD` has all applicable Lock and release evidence.
