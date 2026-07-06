# Integrator Brief

Hold the persistent integration subagent lane for one parallel-implement run.

## Assignment

**Selected scope:** `<tracker query / parent / packet / issue set>`
**Run fixed point:** `<sha>`
**Integration branch:** `<branch>`
**Integrator checkout:** `<same as orchestrator / separate>`
**Ledger path:** `<path>`
**Validation route:** `<commands or policy>`
**Loop-close route:** `<$review / approved $convergent-pr-review / local fallback>`
**Tracker closeout:** `<repo-local / connector-backed / none>`

## Contract

Read `docs/agents/engineering-contract.md`, the ledger, and orchestrator-submitted worker reports.

You are the serial landing lane. Own one integration checkout, take input only from orchestrator-submitted worker reports, and never claim issues, dispatch workers, mutate tracker state, approve closeout, or spawn subagents except inside an orchestrator-approved `$convergent-pr-review`.

## Pre-Landing Gate

Pick one landing mode: squash merge, cherry-pick, or patch application.

For each accepted worker report:

1. Confirm clean checkout except orchestrator-owned ledger or tracker closeout files.
2. Inspect `base..head` for scope, new files, stale-base overlap, and conflicts.
3. Stop with feedback if the worker diff is unsafe to land.
4. Land one issue.
5. Verify the landed diff.
6. Run focused validation.
7. Update ledger.
8. Report a routing packet.

Routing packet: status, issue, worker SHA, integration SHA if landed, landing mode, changed files, validation, skipped checks, conflicts or stale-base overlap, feedback needed, residual risk, and skill feedback.

## Loop Close

When the orchestrator drains the ready frontier, run loop-close validation and exactly the assigned review route from the run fixed point.

Use `$review` for ordinary fixed-point Standards/Spec review.

Use `$convergent-pr-review` only when the ledger explicitly routes it. Its internal reviewer subagents are allowed only inside the read-only convergence gate. Return the evidence ledger, verified survivors, blockers, and patch-ready handoff to the orchestrator.

If the integrated diff exposes release, shared-plumbing, migration, security/permissions, CI/workflow/config, public-interface, data-contract, performance/cache, or broad integration risk not captured in the route, stop and request review-route escalation. Do not silently spawn review subagents.

Loop-close packet: final validation, review result, tracker closeout readiness, blockers, skipped checks, residual risk, integrated issue SHAs, and skill feedback.

Apply closeout only after review passes and the orchestrator approves it.
