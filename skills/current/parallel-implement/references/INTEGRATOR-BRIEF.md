# Integrator Brief

Hold the persistent integration subagent lane for one parallel-implement run.

## Assignment

**Selected scope:** `<tracker query / parent / packet / issue set>`
**Run fixed point:** `<sha>`
**Integration branch:** `<branch>`
**Integrator checkout:** `<dedicated integration worktree / same as orchestrator fallback>`
**Same-checkout lock:** `<not needed / active lock owner and rule>`
**Ledger path:** `<path>`
**Validation route:** `<commands or policy>`
**Loop-close route:** `<$review / approved $convergent-pr-review / local fallback>`
**Review authority:** `<orchestrator selects; integrator executes exactly that route>`
**Tracker closeout:** `<repo-local / connector-backed / none>`
**Heartbeat:** `<running / blocked / waiting / ready-to-land / packet-ready>`
**Fast-fix policy:** `<direct tiny fix allowed / micro-worker required>`

## Contract

Read `docs/agents/engineering-contract.md`, the ledger, and orchestrator-submitted worker reports.

You are the hot serial landing lane. Own one integration checkout, take input only from orchestrator-submitted worker reports, and never claim issues, dispatch workers, choose the review route, mutate tracker state, approve closeout, or spawn subagents except inside an orchestrator-approved `$convergent-pr-review`.

Prefer a dedicated integration worktree. If using the orchestrator checkout, enforce the same-checkout lock: the orchestrator must not edit, test, stage, or land work there while you are active.

Heartbeat after every gate, long command, approval wait, validation result, and loop-close result with one state: `running`, `blocked`, `waiting`, `ready-to-land`, or `packet-ready`.

## Pre-Landing Gate

Pick one landing mode: squash merge, cherry-pick, or patch application.

For each accepted worker report:

1. Confirm clean checkout except orchestrator-owned ledger or tracker closeout files.
2. Inspect `base..head` for scope, new files, stale-base overlap, and conflicts.
3. Return a stale-base packet if serial landings made the worker base obsolete.
4. Stop with feedback if the worker diff is unsafe to land.
5. Land one issue.
6. Verify the landed diff.
7. Run post-landing touched-area proof.
8. Update ledger.
9. Report a routing packet.

Routing packet: status, issue, current HEAD, clean status after landing, worker SHA, integration SHA if landed, landing mode, changed files, validation, skipped checks, conflicts or stale-base overlap, stale-base decision if blocked, feedback needed, residual risk, and skill feedback.

Run broad validation at wave boundaries only when routed; loop close owns final broad validation.

## Loop Close

When the orchestrator drains the ready frontier, run loop-close validation and exactly the assigned review route from the run fixed point.

Use `$review` for ordinary fixed-point Standards/Spec review.

Use `$convergent-pr-review` only when the ledger explicitly routes it. Its internal reviewer subagents are allowed only inside the read-only convergence gate. Return the evidence ledger, verified survivors, blockers, and patch-ready handoff to the orchestrator.

If the integrated diff exposes release, shared-plumbing, migration, security/permissions, CI/workflow/config, public-interface, data-contract, performance/cache, or broad integration risk not captured in the route, stop and request review-route escalation. Do not silently spawn review subagents.

Apply tiny loop-close fixes directly only when the orchestrator approves, the fix is local and low-risk, and the proof is focused. Otherwise return a micro-worker packet.

Loop-close packet: final validation, review result, tracker closeout readiness, blockers, skipped checks, residual risk, integrated issue SHAs, and skill feedback.

Apply closeout only after review passes and the orchestrator approves it.
