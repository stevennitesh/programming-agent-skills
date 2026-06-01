---
name: coding-router
description: "Use when starting nontrivial repo work: source changes, debugging, refactoring, cleanup, GitHub/PR tracking, CI/check triage, or coding-agent skill authoring where scope, assumptions, route choice, or completion evidence could drift."
---

# Coding Router

Route repo work to the smallest reliable source read, edit, check, or specialized skill. Let the controlling skill own the detailed workflow.

## Core Rule

Do the real repo job with the fewest source reads, edits, tools, checks, and agents that still protect correctness.

## Start

For small work, do this mentally and move. For nontrivial work, say it briefly:

1. Goal: what outcome must exist when done?
2. Risk: what source behavior, public contract, data/state, dependency/config behavior, or user work could drift or break?
3. Evidence: what repo evidence matters: source, tests, fixtures, logs, docs, diffs, commands, CI/check output, issues/PRs, or user instruction?
4. Route: which controlling skill or gate should own the next move?
5. Done check: what verification command, manual check, diff review, or PR/CI evidence would make the completion claim honest?

## Routing

Route by the active failure mode, not by the task label. Pick one controlling route for the next move; do not load or perform every related workflow just because several could apply.

| Situation | Use |
| --- | --- |
| Unfamiliar repo, stale repo context, unknown commands/checks, or skill-pack adoption | `repo-onboarding` |
| Tiny source, test, docs, config, or workflow edit | Micro-loop: inspect, edit, check |
| Code question or explanation | Inspect relevant source, docs, tests, fixtures, or logs; answer with evidence |
| Unclear user- or caller-visible feature, API, CLI, UI, module behavior, or public contract | `clarify-scope` |
| Multi-step approved repo work or handoff | `slice-plan` |
| Approved work should become a plan doc, GitHub issues, and issue-by-issue checkpoints | `issue-driven-execution` |
| Caller-visible behavior change or new regression check | `tdd-slice` |
| Bug, failing test, build/CI failure, regression, flaky behavior, or unexplained log/error | `diagnose-loop` |
| Behavior-preserving refactor, cleanup, duplicated logic, or tangled module boundary | `codebase-cleanup` |
| GitHub issues, issue metadata, PRDs, issue claims/updates, implementation slice issues, PR body/check/review tracking | `github-tracking` |
| Subagents requested or useful for independent codebase exploration, implementation slices, or review | `subagent-workflow` |
| Approved parallel implementation across agents or sessions needs separate branches/worktrees | `worktree-isolation` |
| Completion claim, PR readiness, CI status, review resolution, or merge safety | `verify-before-done` |
| Branching, dirty tree, staging, generated output, dependency install, or risky git operation | `workspace-safety` |
| Creating or changing coding-agent skills | `author-skills` |

## Control And Gates

Most work should have one controlling skill at a time:

- `repo-onboarding`, `clarify-scope`, `slice-plan`, `issue-driven-execution`, `tdd-slice`, `diagnose-loop`, `codebase-cleanup`, and `author-skills` can control the main work.
- `workspace-safety`, `worktree-isolation`, `github-tracking`, `subagent-workflow`, and `verify-before-done` are usually gates: call them when the work reaches dirty-tree or git risk, approved parallel implementation, durable issue/PR tracking, delegation, or completion evidence.
- After a gate is handled, return to the controlling skill or choose a new one if evidence changed the job.

## Rerouting

- If new evidence shows the route is wrong, switch routes and say why.
- If repo instructions, commands, checks, GitHub conventions, or durable context locations are unknown and matter to the task, switch to `repo-onboarding`.
- If the user wants a plan document, GitHub issues, and issue-by-issue implementation checkpoints, switch to `issue-driven-execution`.
- If a refactor uncovers a bug, switch to `diagnose-loop`.
- If a cleanup changes caller-visible behavior, public contracts, state/data, or dependency/config behavior, switch to `tdd-slice`.
- If the worktree, branch, generated output, dependency install, staging, or user changes create edit risk, switch to `workspace-safety`.
- If durable request tracking, issue metadata, PRD, implementation issue, issue claim/update, PR body, CI/check status, or review-thread evidence becomes useful, call `github-tracking`.
- If subagents are dispatched, call `subagent-workflow` before sending task packets and after code, diff, or review reports return.
- If approved parallel implementation will run across agents or sessions, call `worktree-isolation`; overlap also needs an integration strategy.
- Before saying work is done, fixed, passing, reviewed, ready, safe, or mergeable, call `verify-before-done`.
- If no specialized route adds value, stay in the micro-loop.

## Repo Evidence Discipline

Intent decides target. Evidence reveals baseline. Checks prove the move.

- Use docs, plans, summaries, and `CONTEXT.md` as maps, not proof.
- Treat `CONTEXT.md` as shared repo vocabulary: recurring terms, module boundaries, public contracts, state transitions, and "means / does not mean" distinctions.
- Never use `CONTEXT.md` for progress, plans, skill summaries, or completion evidence.
- For current behavior, inspect relevant source, callers, tests, fixtures, logs, commands, and recent diffs.
- For target behavior, use the approved spec, design doc, issue, PRD, migration plan, or user instruction.
- During behavior-preserving refactors, current source, tests, fixtures, and public or caller contracts are baseline and compatibility evidence; the approved request or doc is target evidence.
- If docs and source disagree, identify whether the disagreement is stale documentation, intentional target behavior, or an implementation gap before editing.
- Do not add metadata systems, ledgers, or process bureaucracy unless the user asks.

## Ask Or Act

- Ask only when a missing answer changes correctness, source shape, public contract, test strategy, reversibility, security, data integrity, dependency/config behavior, cost, or user-/caller-visible behavior.
- If repo evidence can answer the question cheaply, inspect first.
- If the uncertainty is non-blocking, state the assumption and continue with a reversible slice.
- Stop before destructive operations, broad rewrites, new dependencies, migrations, generated-output churn, or irreversible external actions unless the user approved them.

## Scope Discipline

- Prefer deletion, simplification, and narrow validated slices.
- Push back on broad rewrites, speculative abstractions, and unnecessary agents.
- Every changed source, test, docs, config, workflow, fixture, migration, lockfile, or generated line should trace to the request, an acceptance check, or a necessary cleanup caused by the change.

## Finish

For nontrivial work, end with:

```text
Changed files/behavior:
Verified:
Diff review:
Still uncertain:
Next useful action:
```
