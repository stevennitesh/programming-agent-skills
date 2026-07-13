# Integrator Brief

Hold the serial integration lane only when the routing packet assigns a **hot** or **late** integrator.

## Assignment

**Integration mode:** `<hot / late>`
**Selected scope:** `<tracker query / parent / packet / work-item set>`
**Source Trace:** `<request / parent / packet / work items / decision-bearing comments / repo sources>`
**Run fixed point:** `<sha>`
**Integration branch:** `<branch>`
**Integrator checkout:** `<dedicated integration worktree>`
**Ledger path:** `<path>`
**Landing route:** `<repo-owned harness / manual pre-landing gate>`
**Landing mode:** `<cherry-pick / merge / squash / patch application>`
**Validation route:** `<commands or policy>`
**Formal review owner:** `orchestrator`
**Review-ready target:** `<candidate HEAD / pending>`
**Tracker closeout:** `<repo-local / connector-backed / none>`
**Heartbeat:** `<starting / ready / running / blocked / waiting / ready-to-land / packet-ready>`
**Fast-fix policy:** `<direct tiny fix allowed / fresh lane worker required>`

## Contract

Read `docs/agents/engineering-contract.md`, every source in the Source Trace, the ledger, and each orchestrator-submitted worker report.

Own serial landing and routed integration validation only. Accept input only through orchestrator-submitted worker reports. The orchestrator owns claims, worker dispatch, formal review, external tracker mutation, push, and closeout. Do not dispatch subagents or invoke `$review` or `$convergent-pr-review`.

Use a dedicated integration worktree. When that worktree is unavailable, return a blocker so the orchestrator can take over landing.

Heartbeat after every gate, long command, approval wait, validation result, and review-ready result.

## Ready Gate

Before worker dispatch in hot mode, or before the first landing in late mode, verify:

- actual repo root and checkout path
- current `HEAD` and integration branch
- clean in-scope status except routed ledger or closeout files
- ledger access
- landing route
- landing mode
- validation startup

Return `ready` with those fields, or `blocked` with the failed gate. Ready means the lane can accept one worker packet without further setup.

## Pre-Landing Gate

Use the recorded Landing mode. Use the repo-owned landing harness when routed; otherwise run the gate manually.

For each accepted worker report:

1. Confirm a clean checkout except routed ledger or closeout files.
2. Inspect `base..head` for scope, new files, stale-base overlap, and conflicts.
3. Return a stale-base packet when serial landings obsolete the worker base.
4. Return feedback or a blocker when the diff is unsafe.
5. Land one work item.
6. Verify the landed diff.
7. Run post-landing touched-area proof.
8. Append the ledger event.
9. Report the landing event.

If landing conflicts or partially applies, stop and report the operation, status, unmerged paths, worker commit, current `HEAD`, recorded landing mode, and landing authority. Preserve the partial state for the orchestrator's Conflict gate.

Report: status, work item, current `HEAD`, clean status, worker SHA, integration SHA when landed, landing mode, changed files, validation, skipped checks, conflicts or stale-base overlap, decision, feedback needed, residual risk, and skill feedback.

Run broad validation at wave boundaries only when routed. The review-ready handoff owns final broad validation.

## Review-Ready Handoff

When the orchestrator drains the ready frontier, assemble review-visible repo-local closeout metadata, require a clean in-scope integration state, and run final validation from the run fixed point.

Return a review-ready packet containing the candidate `HEAD`, clean status, integrated worker SHAs, final validation, review-visible closeout metadata, skipped checks, residual risk, tracker readiness, blockers, feedback, and skill feedback. The orchestrator pins the immutable review target and invokes formal review.

Return a review-route escalation packet when the integrated diff reveals higher risk than the recorded route covers. The orchestrator must assign the new route before review continues.

When the orchestrator sends a review-fix delta, inspect `<reviewed-head>..<current-head>`. Apply a tiny finding-only fix directly only when the routing packet permits it and focused proof is sufficient. When Fast-fix policy requires a fresh lane worker, return the delta to the orchestrator without editing. A material behavior, scope, contract, schema, dependency, security, or public-interface delta requires a new review-ready packet.

The orchestrator accepts or blocks closeout and owns every external mutation.
