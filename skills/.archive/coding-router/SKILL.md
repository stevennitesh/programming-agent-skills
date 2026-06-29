---
name: coding-router
description: "Use when starting nontrivial repo work where route choice, scope, assumptions, or completion evidence could drift; defaults to a micro-loop and prevents skill pileups."
---

# Coding Router

Route repo work to the smallest reliable source read, edit, check, or skill. Make "no extra skill needed" the default success path.

## Rule

Default route: micro-loop.

Do not load another skill when a direct source read, answer, narrow edit, and focused check is enough. A specialized skill is justified only when it prevents a specific failure mode: stale repo setup, unclear behavior, unreproduced failure, unsafe workspace operation, weak completion claim, PR review drift, cleanup exhaustion drift, durable tracking drift, or authorized delegation/parallel work.

Pick one controlling route for the next move. Use gates only for the specific risk that appeared, then return to source/read/edit/check quickly.

## Micro-Loop

Use this for tiny safe edits, direct code questions, narrow source reads, and routine source/test/docs/config/workflow changes when no gate risk applies.

1. Inspect the smallest relevant source, docs, tests, logs, diffs, or command output.
2. Answer or make the narrow edit.
3. Run the smallest useful check when behavior, public or caller contract, config, workflow, or generated output changed.
4. Use `verify-before-done` only before completion, readiness, passing, reviewed, safe, or mergeable claims.

If the task still fits the micro-loop, do not route to another skill.

## Choose One Controller

| Situation | Controller |
| --- | --- |
| Unfamiliar repo, stale repo context, or unknown repo instructions/commands that matter now | `repo-onboarding` |
| Unclear behavior, interface, or public or caller contract after cheap repo evidence | `clarify-scope` |
| Bug, failing command, build/CI failure, regression, flake, crash, or unexplained error | `diagnose-loop` |
| Behavior change, new user-visible or caller-visible path, or regression check needed | `tdd-slice` |
| Cleanup discovery, continued cleanup, explicit human-reviewability cleanup, behavior-preserving refactor with structure or testability risk, duplicated logic, module-boundary or caller-interface cleanup, or obsolete-code removal | `codebase-cleanup` |
| Branch, commit, working tree, or PR-ready diff needs semantic correctness review | `pre-pr-review` |
| Creating or changing coding-agent skills | `author-skills` |
| Multi-step approved work truly needs a written plan or handoff | `slice-plan` |
| User explicitly wants plan doc + GitHub issues + issue-by-issue execution with an explicit checkpoint policy | `issue-driven-execution` |

Do not use `slice-plan` for one behavior, one bug, a tiny edit, or a plan that can stay in the chat.

Use `pre-pr-review` for review requests before opening, updating, or merging a PR. Do not route those straight to `verify-before-done`; review finds diff-introduced issues, while verification calibrates final claims.

## Use Gates Only When Needed

| Risk | Gate |
| --- | --- |
| Overlapping dirty tracked paths, relevant untracked protected paths, staging, destructive operation, branch/worktree action, dependency install, formatter/generator/migration, generated output, or cleanup could affect workspace state | `workspace-safety` |
| Final completion, readiness, passing, reviewed, safe, or mergeable claim | `verify-before-done` |
| Durable issue/PR recordkeeping, accepted scope/status record updates, or long-lived GitHub record state that must be written or updated | `github-tracking` |
| Explicit user request for subagents, approved plan delegation, or clearly independent review/exploration with enough scope | `subagent-workflow` |
| Approved parallel implementation or real workspace isolation needs separate branches/worktrees | `worktree-isolation` |

Do not use `github-tracking` for generic live GitHub triage, PR publishing, CI debugging, or review-comment resolution when a GitHub-specific plugin skill or direct tool flow owns that job.

Do not use `subagent-workflow` merely because parallelism seems useful. Delegation needs authorization, clear scope, and parent integration.

## Reroute

- If evidence shows the chosen route is wrong, switch routes and name the reason; avoid oscillating.
- If a review turns into fixes, PR tracking, merge, planning, cleanup, or unclear next-route work, return here and choose the next controller.
- If a refactor uncovers a bug, route to `diagnose-loop`.
- If cleanup changes behavior, route to `tdd-slice`.
- If a gate expands into the main job, return here instead of letting the gate become the workflow.
- If the selected skill is not installed or available, do not simulate it. Use the closest installed route only if it prevents the same failure mode; otherwise stay in the micro-loop and name the missing skill as unavailable.
- If no specialized route prevents a failure mode, stay in the micro-loop.

## Evidence

Use docs, plans, summaries, and issues as maps. Current behavior comes from source, tests, fixtures, logs, diffs, commands, CI/check output, and live tracker state when relevant.

## Stop Or Ask

Ask only when the missing answer changes behavior, public or caller contract, data/state, security, dependency/config behavior, cost, reversibility, external state, or destructive scope.

Stop before broad rewrites, new dependencies, migrations, generated-output churn, destructive commands, irreversible external actions, or publishing unless the user approved the route and scope.

## Finish

For nontrivial work, end with changed files/behavior, checks or evidence, diff-review result, remaining uncertainty, and the next useful action. For tiny micro-loop work, keep the report short.
