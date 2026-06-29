---
name: issue-driven-execution
description: Use when approved repo work should be coordinated through a plan document, GitHub issues, one verified implementation or research issue at a time, and an explicit checkpoint policy.
---

# Issue Driven Execution

Coordinate durable repo work without duplicating planning, GitHub tracking, implementation, debugging, cleanup, workspace safety, or verification skills.

## Rule

Use this only when the user wants approved repo work coordinated through a plan document, GitHub issues, issue-by-issue execution, and an explicit checkpoint policy. If the user asks only for local implementation, only a plan, only issue creation, only PR work, or a tiny obvious edit, use the narrower skill instead of creating this workflow.

First record or derive the workflow inputs. If the user already supplied them, do not reconfirm. Ask only when the missing answer changes source scope, acceptance checks, GitHub access, checkpoint policy, external state, or safe execution.

```text
Approved workflow: plan doc + GitHub issues + issue-by-issue execution
Source scope:
GitHub availability:
Existing plan/issue coverage:
Checkpoint policy:
```

Before creating new plan docs, GitHub issues, branches, commits, or pushes, inspect existing plans, issues, PRDs, branches, PRs, and recent activity. Reuse or update matching artifacts instead of creating duplicates. Account for the approved goal and non-goals, source scope, public or caller contract, acceptance checks, verification strategy, GitHub remote/auth, overlapping dirty-path risk, execution mode, readiness/blockers, and checkpoint policy.

Commit or push are checkpoint actions. Perform them only after the current issue is implemented, verified, diff-reviewed, and allowed by user instruction or repo policy.

## Required Inputs

This skill can run only when these are available from user instruction, repo or GitHub evidence, or explicit approval:

- durable workflow approval: plan doc, GitHub issues, and issue-by-issue execution
- source scope and accepted goal/non-goals
- GitHub remote/auth and issue tracker access
- existing plan, issue, PRD, branch, or PR coverage checked when relevant
- checkpoint policy: no commits, local commits only, push after each issue, or push only at PR/release checkpoint
- repo conventions for plans, branches, PRs, and commits when they matter

## Fast Gate

If the request and available evidence are missing any of these, stop this skill and use the narrower route:

- plan document
- GitHub issues
- issue-by-issue execution
- checkpoint policy

Use `slice-plan` for plan-only work, `github-tracking` for issue-only or PR-record-only work, and the relevant implementation skill for local source work.

## Thin Orchestration Loop

1. Record full workflow approval and checkpoint policy; ask only if missing policy would change external actions or safe execution.
2. Establish repo, GitHub, and workspace safety; inspect and reuse or update existing plans, issues, PRDs, branches, PRs, and recent activity that already cover the work.
3. Use `slice-plan` only for plan shape, task boundaries, checks, continuity, or handoff fields that are not already clear in an existing plan; save or update the plan in the repo's established planning location.
4. Use `github-tracking` only at GitHub record boundaries: duplicate checks, issue creation, readiness/blocker wording, existing GitHub records, claim comments, issue updates, PR links, or recorded CI/review evidence.
5. Execute one unblocked issue through the controlling implementation route:
   - behavior change or durable regression check -> `tdd-slice`
   - failing check, regression, crash, log, or unclear cause -> `diagnose-loop`
   - cleanup discovery, explicit reviewability cleanup, or behavior-preserving refactor with structure, caller-interface, testability, duplication, or obsolete-code risk -> `codebase-cleanup`
   - research or docs-only issue -> inspect repo evidence and update the issue/plan with findings
6. Before implementing an issue, read the live issue body/comments, plan doc if present, affected source/tests/docs, and relevant checks or logs. Note any unavailable GitHub or repo evidence that affects the claim.
7. Checkpoint before moving on: verify the issue claim, inspect the diff against the issue and plan, update tracking, then commit or push only if the approved checkpoint policy allows it.

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
- overlapping dirty paths or staging/commit/push risk could mix unrelated files into the current issue
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
Evidence checked/unavailable:
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
- `github-tracking`: issues, PRDs, PR record updates, issue updates, readiness/blocker comments, PR links, and recorded CI/review evidence.
- `subagent-workflow`: approved issue work needs bounded subagent exploration, implementation, or review.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: implementation work for each issue.
- `workspace-safety`: before edits that overlap dirty paths, plan-file creation, staging, commits, pushes, generated output, or dependency installs.
- `verify-before-done`: before claiming an issue, commit, push, plan, or overall workflow is complete.
