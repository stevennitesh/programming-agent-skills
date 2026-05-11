---
name: issue-driven-execution
description: Use when approved repo work should be turned into a plan document, GitHub issues, and one verified implementation or research issue at a time with commit/push checkpoints.
---

# Issue Driven Execution

Coordinate durable repo work without duplicating planning, GitHub tracking, implementation, debugging, cleanup, workspace safety, or verification skills.

## Rule

Use this only when the user wants a plan document, GitHub issues, and issue-by-issue execution. Do not turn small local edits into a plan-and-issue workflow.

Commit and push only after the current issue is implemented, verified, diff-reviewed, and allowed by user instruction or repo policy.

## Inputs

- Approved task, issue, PRD, review request, bug, cleanup goal, research goal, or user instruction
- Repo instructions, source, tests, docs, logs, diffs, CI/check output, and GitHub state relevant to the task
- Existing `plans/` conventions, issue templates, branch rules, PR rules, and commit message conventions
- Existing open issues or plan docs that might already cover the work

## Process

1. Establish operating context.
   - Use `repo-onboarding` if repo commands, GitHub conventions, `plans/` conventions, or safety constraints are unknown.
   - Use `clarify-scope` if the target behavior, public/caller contract, risk, or success criteria are unclear.
   - Use `workspace-safety` before creating plan docs, branches, commits, pushes, dependency installs, generated output, or dirty-tree edits.
2. Create the plan document.
   - Use `slice-plan` to shape the work into reviewable source, test, docs, research, or verification slices.
   - Save the plan under `plans/` using a concise slug, unless the repo has another established planning location.
   - Include goal, non-goals, constraints, acceptance checks, issue list, verification strategy, risks, and stop conditions.
   - Record `Execution mode: sequential | parallel-disjoint | parallel-overlap`. If the plan does not explicitly say parallel, treat it as `sequential`.
   - For parallel modes, record parallel groups, issue ownership, dependency order, worktree requirement, and integration owner.
   - Do not copy source code into the plan unless an exact API, CLI, schema, fixture, or contract is the task.
3. Create GitHub issues.
   - Use `github-tracking` to check for duplicates, follow issue conventions, and create issues from the plan.
   - Each issue should reference the plan doc and carry its own acceptance check, likely files/modules, verification command, and out-of-scope notes.
   - Copy the plan's execution coordination into each issue: mode, parallel group, dependencies, expected overlap, worktree requirement, and claim protocol.
   - Decide GitHub metadata from plan scale and coordination needs; leave metadata unset for sequential single-agent work when body/comments are enough.
   - Use relationships, milestones, projects, assignees, labels, or Development links only when they improve dependency tracking, release grouping, filtering, ownership, or branch/PR traceability.
   - Update the plan with issue links after creation.
4. Execute one issue at a time.
   - Pick the next unblocked issue.
   - Inspect the current issue body, comments, metadata, linked PRs, and recent activity before editing.
   - Post the `github-tracking` claim comment before source, test, docs, config, or workflow edits.
   - When starting implementation, link the branch or PR through GitHub Development metadata when the repo workflow supports it.
   - Derive workspace shape from execution mode:
     - `sequential`: use the parent workspace unless user instruction or repo policy says otherwise.
     - `parallel-disjoint`: use `worktree-isolation` for each active implementation issue.
     - `parallel-overlap`: use `worktree-isolation` and the approved integration strategy before editing.
   - Choose the controlling skill by issue type:
     - behavior change or feature -> `tdd-slice`
     - reproduced bug, failing check, regression, crash, log, or unclear cause -> `diagnose-loop`
     - behavior-preserving refactor or cleanup -> `codebase-cleanup`
     - research or docs-only investigation -> inspect repo evidence and update the issue/plan with findings
   - Keep edits scoped to the current issue unless the plan is updated.
5. Checkpoint after each issue.
   - Use `verify-before-done` before claiming the issue is complete.
   - Inspect the diff against the issue and plan.
   - Update the issue and plan with changed files, checks run, commit/branch/PR, open risks, claim status, and next issue.
   - Check that comments, Development links, relationships, dependencies, and open risks agree before moving on.
   - Use `workspace-safety` before staging, committing, or pushing.
   - Commit only the current issue's intended files from the parent workspace or assigned worktree, then push the branch when the workflow calls for remote checkpoints.

## Stop Or Ask

Stop before continuing when:

- the user has not approved durable plan docs, GitHub issues, commits, or pushes
- no GitHub remote, auth, issue tracker, or branch workflow is available
- `plans/` conventions are unclear and creating a new convention would matter
- issue scope expands beyond the approved plan
- verification fails or does not exercise the issue's acceptance check
- the working tree contains unrelated or overlapping user changes
- parallel work is expected but the plan or issue does not explicitly declare `parallel-disjoint` or `parallel-overlap`
- a parallel implementation issue lacks worktree isolation
- `parallel-overlap` lacks an approved integration strategy
- committing or pushing would include unrelated files, secrets, generated output, or unverified behavior

## Output

```text
Plan:
Issues:
Current issue:
Execution mode:
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
- `clarify-scope`: target behavior, public/caller contract, risk, or success criteria are unclear.
- `slice-plan`: plan document structure and reviewable slices.
- `worktree-isolation`: approved parallel implementation needs separate worktrees; overlap also needs an integration strategy.
- `github-tracking`: issues, PRDs, PRs, CI/check evidence, review threads, and issue updates.
- `subagent-workflow`: approved issue work needs bounded subagent exploration, implementation, or review.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: implementation work for each issue.
- `workspace-safety`: before edits in dirty trees, plan-file creation, staging, commits, pushes, generated output, or dependency installs.
- `verify-before-done`: before claiming an issue, commit, push, plan, or overall workflow is complete.
