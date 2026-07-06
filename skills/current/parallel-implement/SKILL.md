---
name: parallel-implement
description: Run a three-lane implementation loop over a ready frontier: orchestrator, serial integrator, and fresh isolated workers.
---

# Parallel Implement

Run orchestrated fan-out over a ready frontier of independently-grabbable issues.

The loop is **ready frontier -> fresh isolated workers -> proof lanes -> serial landing -> loop-close review -> tracker lock**.

- **Orchestrator**: owns scope, gates, ledger, review route, tracker lock, and closeout approval.
- **Integrator**: persistently lands accepted worker commits one at a time.
- **Workers**: fresh isolated worktrees, one issue each.

Use this when orchestration pays: multiple ready issues, dependency-aware fan-out, incoming tracker work, or integration/review work that would block the orchestrator. For one small fixed issue, keep it shallow: one worker, one landing, one review, closeout.

## References

- Start the integrator with `references/INTEGRATOR-BRIEF.md`.
- Dispatch workers with `references/WORKER-BRIEF.md`.
- Track the run in `references/RUN-LEDGER.md`.

## Preconditions

This is execution, not shaping. Read `docs/agents/engineering-contract.md`; read tracker docs only for scope, labels, readiness, or closeout; read `docs/agents/domain.md` only when domain semantics may affect the run.

Require a ready frontier: independently-grabbable issues with acceptance criteria, dependency order, parallel-safety notes, proof lanes, and load-bearing seams where needed. If readiness is weak, stop with gaps; do not repair readiness in this flow.

## Loop

Routing packet: ready frontier, blockers, dependency order, write-scope risks, worker limit, validation environment, loop-close route, tracker closeout rule, and cleanup rule.

Launch gate: `$parallel-implement` authorizes subagents for this run. Dispatch one fresh worker per issue only through a verified worktree route.

Handoff gate: delegated work is not done until the worker sends a work-done handoff and the orchestrator accepts its result packet. Do not infer completion from dispatch, silence, elapsed time, or partial progress.

Verified worktree route: prefer Codex-managed worktrees created by the Codex app, not `git worktree`.

1. Run `codex_app.list_projects` and choose the saved project for this repo.
2. Run `codex_app.create_thread` once per issue with a Worktree target:

```json
{
  "prompt": "<worker prompt built from WORKER-BRIEF.md>",
  "target": {
    "type": "project",
    "projectId": "<projectId>",
    "environment": {
      "type": "worktree",
      "startingState": { "type": "branch", "branchName": "<existing base branch or ref>" }
    }
  }
}
```

Omit `startingState` to use the project default branch. Use `{ "type": "working-tree" }` only when the worker must inherit current local uncommitted changes. Do not use `startingState` to name a new branch.

A Codex-managed worktree counts as verified only after the worker reports: thread ID or pending worktree ID, actual repo root, `HEAD`, branch or detached state, clean starting status, scratch write/delete result, and focused-proof preflight result.

If the app tool is unavailable, create the thread manually in the Codex app: new thread -> Worktree -> existing starting branch/ref -> submit the worker prompt. If no Codex-managed worktree can be created, stop and report the blocked launch, or ask the user to approve the manual worktree fallback.

Manual fallback worktrees are not Codex-managed: `<repo-parent>/worktrees/<repo>/<run-id>/<issue-id>`, with `<repo-parent>/worktrees/` approved as a writable root.

Loop-close route: default to `$review` from the run fixed point over the integrated diff. Use approved `$convergent-pr-review` only for high-risk integrated diffs: release gates, shared plumbing, migrations, security/permissions, CI/workflow/config, public interfaces, data contracts, performance/cache risk, or broad integration uncertainty.

Proof lanes: route one concrete focused proof command and validation env per worker. Workers run focused proof; the integrator runs post-landing proof; loop close runs final review and broad validation.

Worker-safe proof is for focused worker checks, not loop-close validation. Use single-process/no-cache focused tests when repo defaults are too broad, too parallel, or cache-sensitive.

Record loop-close route, executor, fixed point, and fallback in the ledger.
Record run friction, skill bugs, and skill/supporting-file improvement ideas in the ledger and final report.

For shallow runs, use minimal ledger mode: run, worker result, serial landing, final checks, and run summary.

1. Select scope and ready frontier.
2. Capture run fixed point.
3. Start ledger.
4. Start the persistent integrator subagent.
5. Verify the integrator is ready.
6. Claim ready issues up to worker limit.
7. Dispatch only workers with verified worktree checkout paths.
8. Wait for work-done handoffs; orchestrator checks the packet, then integrator checks the integration diff.
9. Queue accepted work; route feedback to workers.
10. Integrator lands serially and reports status.
11. Rescan until scope is drained or blocked.
12. Trigger loop-close review.
13. Orchestrator approves closeout, updates tracker, and releases workers/integrator.

## Gates

Worker fixes pass two acceptance gates before landing:

- **Orchestrator acceptance**: result packet, scope, acceptance proof, residual risk.
- **Integrator pre-landing gate**: actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof.

Pre-landing gate is acceptance, not formal review. If the worker diff needs deeper review before landing, the integrator returns a blocker or review-route escalation packet to the orchestrator.

Review is orchestrator-owned and integrator-executed. The orchestrator selects `$review`, approved `$convergent-pr-review`, or a local fallback in the routing packet; the integrator runs exactly that route. If landing reveals higher risk, the integrator returns a review-route escalation packet instead of silently changing route.

## Lock

Move accepted work to `implemented`; close only when tracker docs or the user say to close. Make repo-local tracker closeout review-visible before final review. Mutate connector-backed trackers only after review passes and required commits exist.

Workers and integrator may prepare closeout notes; only the orchestrator mutates connector-backed tracker labels, comments, or state.

Orchestrator approval is the main agent's post-review gate unless the user asks to confirm.

Release lanes means stop active workers/integrator and remove worker worktrees; keep worker branches unless cleanup rules say otherwise.

Done means the scope is complete or blocked; accepted work landed serially; validation and loop-close review passed or blockers are recorded; tracker lock was respected; durable notes carry worker SHAs, integration SHAs, validation, skipped checks, residual risk, and skill feedback; unrelated work is preserved.
