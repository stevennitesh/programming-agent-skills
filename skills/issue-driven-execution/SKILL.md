---
name: issue-driven-execution
description: Use when approved repo work should be turned into a plan document, GitHub issues, and one verified implementation or research issue at a time with commit/push checkpoints.
---

# Issue Driven Execution

Coordinate durable repo work without duplicating planning, GitHub tracking, implementation, debugging, cleanup, workspace safety, or verification skills.

## Rule

Use this only when the user wants approved repo work turned into a plan document, GitHub issues, and issue-by-issue execution. If the user asks only for local implementation, only a plan, only issue creation, only PR work, or a tiny obvious edit, use the narrower skill instead of creating this workflow.

First confirm the full durable workflow and checkpoint policy:

```text
Approved workflow: plan doc + GitHub issues + issue-by-issue execution
Source scope:
GitHub availability:
Existing plan/issue coverage:
Checkpoint policy:
```

Before creating plan docs, GitHub issues, branches, commits, or pushes, account for the approved goal and non-goals, source scope, public or caller contract, acceptance checks, verification strategy, GitHub remote/auth, existing plan or issue coverage, dirty-tree risk, execution mode, readiness/blockers, and checkpoint policy.

Commit and push only after the current issue is implemented, verified, diff-reviewed, and allowed by user instruction or repo policy.

## Required Inputs

This skill can run only when these are available or explicitly approved:

- durable workflow approval: plan doc, GitHub issues, and issue-by-issue execution
- source scope and accepted goal/non-goals
- GitHub remote/auth and issue tracker access
- existing plan, issue, PRD, branch, or PR coverage checked when relevant
- checkpoint policy: no commits, local commits only, push after each issue, or push only at PR/release checkpoint
- repo conventions for plans, branches, PRs, and commits when they matter

## Fast Gate

If the request is missing any of these, stop this skill and use the narrower route:

- plan document
- GitHub issues
- issue-by-issue execution
- checkpoint policy

Use `slice-plan` for plan-only work, `github-tracking` for issue-only or PR-only work, and the relevant implementation skill for local source work.

## Thin Orchestration Loop

1. Confirm full workflow approval and checkpoint policy.
2. Establish repo, GitHub, and workspace safety; inspect existing plans, issues, PRDs, branches, and recent activity that may already cover the work.
3. Use `slice-plan` for the plan shape and save it in the repo's established planning location.
4. Use `github-tracking` for duplicate checks, issue creation, readiness/blocker wording, live GitHub records, claim comments, issue updates, PR links, review threads, and CI/check state.
5. Execute one unblocked issue through the controlling implementation route:
   - behavior change or durable regression check -> `tdd-slice`
   - failing check, regression, crash, log, or unclear cause -> `diagnose-loop`
   - behavior-preserving refactor or cleanup -> `codebase-cleanup`
   - research or docs-only issue -> inspect repo evidence and update the issue/plan with findings
6. Checkpoint before moving on: verify the issue claim, inspect the diff against the issue and plan, update tracking, then commit or push only if the approved checkpoint policy allows it.

Keep edits scoped to the current issue unless the plan and tracking records are updated. Do not execute from a chat summary, plan title, issue title, or issue list alone when current repo or GitHub evidence is cheap to inspect.

## Stop Or Ask

Stop before continuing when:

- the user has not approved durable plan docs, GitHub issues, issue-by-issue execution, or the requested checkpoint action
- no GitHub remote, auth, issue tracker, or branch workflow is available
- `plans/` conventions are unclear and creating a new convention would matter
- an existing plan, issue, PRD, or PR may already cover the work and has not been inspected
- the source scope, public or caller contract, acceptance checks, verification strategy, execution mode, readiness, or checkpoint policy is missing from the plan or issue
- issue scope expands beyond the approved plan
- verification fails or does not exercise the issue's acceptance check
- an issue is marked `needs human decision` and the missing decision, artifact, access, dependency, or manual review is still absent
- an issue would be marked `agent-ready` without enough repo evidence to start safely
- the working tree contains unrelated or overlapping user changes
- parallel work is expected but the plan or issue does not explicitly declare `parallel-disjoint` or `parallel-overlap`
- a parallel implementation issue lacks worktree isolation
- `parallel-overlap` lacks an approved integration strategy
- committing or pushing would include unrelated files, secrets, generated output, or unverified behavior
- local commits or remote pushes are not allowed by user instruction, repo policy, or the approved checkpoint policy

## Output

```text
Plan:
Issues:
Current issue:
Execution mode:
Readiness:
Claim:
Worktree/branch:
Changed files:
Verified:
Committed:
Pushed:
Updated tracking:
Open risks:
Next issue:
```

## Handoff

- `repo-onboarding`: repo commands, GitHub conventions, `plans/` conventions, or safety constraints are unknown.
- `clarify-scope`: target behavior, public or caller contract, risk, or success criteria are unclear.
- `slice-plan`: plan document structure and reviewable slices.
- `worktree-isolation`: approved parallel implementation needs separate worktrees; overlap also needs an integration strategy.
- `github-tracking`: issues, PRDs, PRs, CI/check evidence, review threads, and issue updates.
- `subagent-workflow`: approved issue work needs bounded subagent exploration, implementation, or review.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: implementation work for each issue.
- `workspace-safety`: before edits in dirty trees, plan-file creation, staging, commits, pushes, generated output, or dependency installs.
- `verify-before-done`: before claiming an issue, commit, push, plan, or overall workflow is complete.
