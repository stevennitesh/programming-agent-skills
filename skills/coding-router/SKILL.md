---
name: coding-router
description: "Use when starting nontrivial repo work: source changes, debugging, refactoring, cleanup, GitHub/PR tracking, CI/check triage, or coding-agent skill authoring where scope, assumptions, route choice, or completion evidence could drift."
---

# Coding Router

Route repo work to the smallest reliable source read, edit, check, or specialized skill. Let the controlling skill own the detailed workflow.

## Core Rule

Do the real repo job with the fewest source reads, edits, tools, checks, and agents that still protect correctness. A route is useful only when it names the next observable action: source read, command, issue/PR lookup, check, edit, gate, or stop condition.

## Start

For small work, do this mentally and move. For nontrivial work, say it briefly:

1. Goal: what outcome must exist when done?
2. Trigger signal: what user phrase, repo signal, failure symptom, or tool output controls the route?
3. Risk: what source behavior, public or caller contract, data/state, dependency/config behavior, or user work could drift or break?
4. Evidence: what repo evidence matters: source, tests, fixtures, logs, docs, diffs, commands, CI/check output, issues/PRs, or user instruction?
5. Route and first action: which controlling skill or gate owns the next move, and what is the first source read, command, check, edit, or question?
6. Done check: what verification command, manual check, diff review, PR/CI evidence, required ledger, or explicit user stop condition would make the completion claim honest?

## Routing

Route by the active failure mode and trigger signal, not by the task label. Pick one controlling route for the next move, then take that route's first action. Do not load or perform every related workflow just because several could apply.

| Situation | Use |
| --- | --- |
| Unfamiliar repo, stale repo context, unknown commands/checks, or skill-pack adoption | `repo-onboarding` |
| Tiny source, test, docs, config, or workflow edit | Micro-loop: inspect, edit, check |
| Code question or explanation | Inspect relevant source, docs, tests, fixtures, or logs; answer with evidence |
| Unclear user- or caller-visible feature, API, CLI, UI, module behavior, or public or caller contract | `clarify-scope` |
| Multi-step approved repo work or handoff | `slice-plan` |
| Approved work should become a plan doc, GitHub issues, and issue-by-issue checkpoints | `issue-driven-execution` |
| Caller-visible behavior change or new regression check | `tdd-slice` |
| Bug, failing test, build/CI failure, regression, flaky behavior, or unexplained log/error | `diagnose-loop` |
| Cleanup discovery, ordered cleanup bundles, human-readable code organization/comments, behavior-preserving refactor, duplicated logic, tangled module boundary, or cleanup requests that say "keep looping", "keep cleaning", "continue until done", or "until nothing useful remains" | `codebase-cleanup` |
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
- If a gate is needed, run the gate for the specific risk and then return to the controlling route. Do not let safety, tracking, delegation, or verification process replace the source read, edit, or check that the work needs.

## Rerouting

- If new evidence shows the route is wrong, switch routes and say why.
- If repo instructions, commands, checks, GitHub conventions, or durable context locations are unknown and matter to the task, switch to `repo-onboarding`.
- If the user wants a plan document, GitHub issues, and issue-by-issue implementation checkpoints, switch to `issue-driven-execution`.
- If a refactor uncovers a bug, switch to `diagnose-loop`.
- If a cleanup changes caller-visible behavior, public or caller contract, state/data, or dependency/config behavior, switch to `tdd-slice`.
- If the worktree, branch, generated output, dependency install, staging, or user changes create edit risk, switch to `workspace-safety`.
- If durable request tracking, issue metadata, PRD, implementation issue, issue claim/update, PR body, CI/check status, or review-thread evidence becomes useful, call `github-tracking`.
- If subagents are dispatched, call `subagent-workflow` before sending task packets and after code, diff, or review reports return.
- If approved parallel implementation will run across agents or sessions, call `worktree-isolation`; overlap also needs an integration strategy.
- Before saying work is done, fixed, passing, reviewed, ready, safe, or mergeable, call `verify-before-done`.
- If no specialized route adds value, stay in the micro-loop.

## Repo Evidence Discipline

Intent decides target. Evidence reveals baseline. Checks prove the move.

- Use docs, plans, summaries, and `CONTEXT.md` as maps, not proof.
- Treat `CONTEXT.md` as shared repo vocabulary: recurring terms, module boundaries, public or caller contracts, state transitions, and "means / does not mean" distinctions.
- Never use `CONTEXT.md` for progress, plans, skill summaries, or completion evidence.
- For current behavior, inspect relevant source, callers, tests, fixtures, logs, commands, and recent diffs.
- For target behavior, use the approved spec, design doc, issue, PRD, migration plan, or user instruction.
- During behavior-preserving refactors, current source, tests, fixtures, and public or caller contracts are baseline and compatibility evidence; the approved request or doc is target evidence.
- If docs and source disagree, identify whether the disagreement is stale documentation, intentional target behavior, or an implementation gap before editing.
- Do not add durable metadata systems, long-lived ledgers, or process bureaucracy unless the user asks. Short working ledgers required by a controlling skill are fine.

## Ask Or Act

- Ask only when a missing answer changes correctness, source shape, public or caller contract, test strategy, reversibility, security, data integrity, dependency/config behavior, cost, or user-/caller-visible behavior.
- If repo evidence can answer the question cheaply, inspect first.
- If the uncertainty is non-blocking, state the assumption and continue with a reversible slice.
- Stop before destructive operations, broad rewrites, new dependencies, migrations, generated-output churn, or irreversible external actions unless the user approved them.

## Scope Discipline

- Prefer deletion, simplification, and narrow validated slices.
- When cleanup wording says "find cleanup opportunities", "ordered cleanup bundles", "organize/comment the code", "keep looping", "keep cleaning", "continue until done", or "until nothing useful remains", route to `codebase-cleanup`. First action: define the inspected scope and start the cleanup coverage ledger before selecting a bundle. Done check: require the ledger, last cleanup signals checked, relevant checks, and a concrete next bundle or stop reason; do not treat one passing slice as completion.
- Push back on broad rewrites, speculative abstractions, and unnecessary agents.
- Do not start implementation, tracker setup, subagents, or broad planning before the route, first action, and completion evidence are clear enough for the current risk.
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
