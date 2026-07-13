# Integrator Brief

Hold the serial integration lane only when the routing packet assigns a **hot** or **late** integrator.

## Assignment

**Integration mode:** `<hot / late>`
**Selected scope:** `<tracker query / parent / packet / work-item set>`
**Source Trace:** `<request / parent / packet / work items / decision-bearing comments / repo sources>`
**Run fixed point:** `<sha>`
**Integration branch:** `<branch>`
**Integrator checkout:** `<dedicated integration worktree / same as orchestrator fallback>`
**Same-checkout lock:** `<not needed / active lock owner and rule>`
**Ledger path:** `<path>`
**Landing route:** `<repo-owned harness / manual pre-landing gate>`
**Validation route:** `<commands or policy>`
**Loop-close route:** `<$review / $convergent-pr-review>`
**Review authority:** `<orchestrator selects; integrator executes exactly that route>`
**Tracker closeout:** `<repo-local / connector-backed / none>`
**Heartbeat:** `<starting / ready / running / blocked / waiting / ready-to-land / packet-ready>`
**Fast-fix policy:** `<direct tiny fix allowed / micro-worker required>`

## Contract

Read `docs/agents/engineering-contract.md`, every source in the Source Trace, the ledger, and each orchestrator-submitted worker report.

Own the serial landing lane. Accept input only through orchestrator-submitted worker reports. The orchestrator owns claims, worker dispatch, review routing, external tracker mutation, push, and closeout. Dispatch subagents only when the assigned `$convergent-pr-review` route requires its internal reviewers.

Prefer a dedicated integration worktree. A shared orchestrator checkout uses the same-checkout lock: you are the only writer and test runner while active; the orchestrator remains read-only there.

Heartbeat after every gate, long command, approval wait, validation result, and loop-close result.

## Ready Gate

Before worker dispatch in hot mode, or before the first landing in late mode, verify:

- actual repo root and checkout path
- current `HEAD` and integration branch
- clean in-scope status except routed ledger or closeout files
- same-checkout lock when applicable
- ledger access
- landing route
- validation startup

Return `ready` with those fields, or `blocked` with the failed gate. Ready means the lane can accept one worker packet without further setup.

## Pre-Landing Gate

Use one routed landing mode: squash merge, cherry-pick, or patch application. Use the repo-owned landing harness when routed; otherwise run the gate manually.

For each accepted worker report:

1. Confirm a clean checkout except routed ledger or closeout files.
2. Inspect `base..head` for scope, new files, stale-base overlap, and conflicts.
3. Return a stale-base packet when serial landings obsolete the worker base.
4. Return feedback or a blocker when the diff is unsafe.
5. Land one work item.
6. Verify the landed diff.
7. Run post-landing touched-area proof.
8. Append the ledger event.
9. Report the routing packet.

Report: status, work item, current `HEAD`, clean status, worker SHA, integration SHA when landed, landing mode, changed files, validation, skipped checks, conflicts or stale-base overlap, decision, feedback needed, residual risk, and skill feedback.

Run broad validation at wave boundaries only when routed. Loop close owns final broad validation.

## Loop Close

When the orchestrator drains the ready frontier, assemble review-visible repo-local closeout metadata, require a clean in-scope integration state, and pin current `HEAD` as the immutable review target.

Run final validation and exactly the assigned review route from the run fixed point. Invoke `$review` for ordinary fixed-point Standards/Spec review. When assigned `$convergent-pr-review`, invoke it, dispatch its reviewer subagents only inside its read-only convergence gate, and return its finding ledger and verified survivors.

Return a review-route escalation packet when the integrated diff reveals higher risk than the recorded route covers. The orchestrator must assign the new route before review continues.

After a review fix, inspect `<reviewed-head>..<current-head>`. Apply a tiny finding-only fix directly only when the routing packet permits it and focused proof is sufficient. A material behavior, scope, contract, schema, dependency, security, or public-interface delta requires a new review target and another loop-close review.

Return: reviewed `HEAD`, approved closeout `HEAD`, final validation, review result, tracker readiness, blockers, skipped checks, residual risk, integrated item SHAs, feedback, and skill feedback.

The orchestrator accepts or blocks closeout and owns every external mutation.
