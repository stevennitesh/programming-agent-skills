---
name: coding-router
description: Use when starting nontrivial coding, debugging, refactoring, repo cleanup, GitHub tracking, or skill-authoring work where scope, assumptions, workflow choice, or completion evidence could drift.
---

# Coding Router

Work-routing skill. Use it to choose the smallest reliable path, then let the specialized skill own the detailed workflow.

## Core Rule

Do the real job with the fewest steps, tools, and agents that still protect correctness.

## Start

For small work, do this mentally and move. For nontrivial work, say it briefly:

1. Goal: what outcome must exist when done?
2. Risk: what could drift, break, or be misunderstood?
3. Evidence: what source, doc, test, command, issue, or user instruction matters?
4. Route: which one downstream skill should control the next move?
5. Done check: what would make the completion claim honest?

## Routing

Route by the active failure mode, not by the task label. Pick one controlling route for the next move; do not load or perform every related workflow just because several could apply.

| Situation | Use |
| --- | --- |
| Tiny mechanical edit | Micro-loop: inspect, edit, check |
| Code question or explanation | Inspect the relevant source/docs, answer with evidence |
| Fuzzy feature or product behavior | `clarify-scope` |
| Multi-step approved work | `thin-plan` |
| Behavior change | `tdd-slice` |
| Bug, failing test, regression, flaky behavior | `diagnose-loop` |
| Refactor, cleanup, duplicated or tangled structure | `codebase-cleanup` |
| GitHub issues, PRDs, PR tracking | `github-work-tracking` |
| Subagents requested or clearly useful | `manage-subagents` |
| Completion claim, PR, merge readiness | `verify-before-done` |
| Branching, dirty tree, risky git operation | `workspace-safety` |
| Creating or changing skills | `author-skills` |

## Control And Gates

Most work should have one controlling skill at a time:

- `clarify-scope`, `thin-plan`, `tdd-slice`, `diagnose-loop`, `codebase-cleanup`, and `author-skills` can control the main work.
- `workspace-safety`, `github-work-tracking`, `manage-subagents`, and `verify-before-done` are usually gates: call them when the procedure reaches edit risk, durable tracking, delegation, or completion evidence.
- After a gate is handled, return to the controlling skill or choose a new one if evidence changed the job.

## Rerouting

- If new evidence shows the route is wrong, switch routes and say why.
- If a refactor uncovers a bug, switch to `diagnose-loop`.
- If a cleanup changes observable behavior, switch to `tdd-slice`.
- If the worktree, branch, or user changes create edit risk, switch to `workspace-safety`.
- If durable request tracking, PRD, issues, or PR evidence becomes useful, call `github-work-tracking`.
- If subagents are dispatched, call `manage-subagents` before sending packets and after reports return.
- Before saying work is done, fixed, ready, safe, or mergeable, call `verify-before-done`.
- If no specialized route adds value, stay in the micro-loop.

## Source Discipline

Intent decides target. Evidence reveals baseline. Checks prove the move.

- Use docs, plans, summaries, and `CONTEXT.md` as maps.
- Treat `CONTEXT.md` as shared language memory: terms, roles, boundaries, and "means / does not mean" distinctions.
- Do not use `CONTEXT.md` for progress, plans, skill summaries, or completion evidence.
- When preserving or explaining current behavior, inspect the relevant source and tests.
- When an approved spec, design doc, migration plan, or user instruction defines intended behavior, treat it as the target even if current code differs.
- During refactors, current code is baseline and compatibility evidence; the approved request or doc is target evidence.
- If docs and code disagree, identify whether the disagreement is stale documentation, intentional target behavior, or an implementation gap before editing.
- Do not add metadata systems, ledgers, or process bureaucracy unless the user asks.

## Ask Or Act

- Ask only when a missing answer changes correctness, scope, reversibility, security, data integrity, cost, or user-visible behavior.
- If repo evidence can answer the question cheaply, inspect first.
- If the uncertainty is non-blocking, state the assumption and continue with a reversible slice.
- Stop before destructive operations, broad rewrites, new dependencies, or irreversible external actions unless the user approved them.

## Scope Discipline

- Prefer deletion, simplification, and narrow validated slices.
- Push back on broad rewrites, speculative abstractions, and unnecessary agents.
- Every changed line should trace to the request, a test, or a necessary cleanup caused by the change.

## Finish

For nontrivial work, end with:

```text
Changed:
Verified:
Still uncertain:
Next useful action:
```
