---
name: issue-driven-execution
description: Use when approved repo work should be turned into a plan document, GitHub issues, and one verified implementation or research issue at a time with commit/push checkpoints.
---

# Issue Driven Execution

Coordinate durable repo work without duplicating planning, GitHub tracking, implementation, debugging, cleanup, workspace safety, or verification skills.

## Rule

Use this only when the user wants approved repo work turned into a plan document, GitHub issues, and issue-by-issue execution. If the user asks only for local implementation, only a plan, only issue creation, only PR work, or a tiny obvious edit, use the narrower skill instead of creating this workflow.

Before creating plan docs, GitHub issues, branches, commits, or pushes, account for the approved goal and non-goals, source scope, public or caller contract, acceptance checks, verification strategy, GitHub remote/auth, existing plan or issue coverage, dirty-tree risk, execution mode, readiness/blockers, and checkpoint policy.

Commit and push only after the current issue is implemented, verified, diff-reviewed, and allowed by user instruction or repo policy.

## Inputs

- Approved task, issue, PRD, review request, bug, cleanup goal, research goal, or user instruction
- Repo instructions, source, tests, docs, logs, diffs, CI/check output, and GitHub state relevant to the task
- Existing `plans/` conventions, issue templates, branch rules, PR rules, and commit message conventions
- Existing open issues or plan docs that might already cover the work
- User-approved checkpoint policy: no commits, local commits only, push after each issue, or push only at PR/release checkpoint

## Process

1. Establish operating context.
   - Use `repo-onboarding` if repo commands, GitHub conventions, `plans/` conventions, or safety constraints are unknown.
   - Use `clarify-scope` if the target behavior, public or caller contract, risk, or success criteria are unclear.
   - Use `workspace-safety` before creating plan docs, branches, commits, pushes, dependency installs, generated output, or dirty-tree edits.
   - Inspect existing plan docs, issues, PRDs, branches, and recent activity when they may already cover the request.
   - Do not proceed from a chat summary alone when current repo or GitHub evidence is cheap to inspect.
2. Create the plan document.
   - Use `slice-plan` to shape the work into reviewable source, test, docs, research, or verification slices.
   - Save the plan under `plans/` using a concise slug, unless the repo has another established planning location.
   - Include goal, non-goals, constraints, acceptance checks, issue list, verification strategy, risks, and stop conditions.
   - Record `Execution mode: sequential | parallel-disjoint | parallel-overlap`. If the plan does not explicitly say parallel, treat it as `sequential`.
   - For parallel modes, record parallel groups, issue ownership, dependency order, worktree requirement, and integration owner.
   - For later slices, record the prior output, source path, helper, test, contract, or issue result they build on or must preserve.
   - Record issue readiness when it affects execution: `agent-ready` when repo evidence is enough to proceed, or `needs human decision` when behavior, architecture, security/data, access, dependency, or manual review is still required.
   - Do not copy source code into the plan unless an exact API, CLI, schema, fixture, or contract is the task.
   - Do not publish issues from a plan that lacks accepted scope, issue list, execution mode, readiness/blockers, acceptance checks, or verification strategy.
3. Create GitHub issues.
   - Use `github-tracking` to check for duplicates, follow issue conventions, and create issues from the plan.
   - Before publishing, scan the planned issue list for vertical tracer-bullet shape. Prefer issues that deliver one end-to-end behavior, bug fix, refactor, research answer, or verification result through the real repo path.
   - Do not publish layer-only issues such as "just schema", "just API", or "just UI" unless the issue is an intentional blocking technical step with a dependency, verification command, and reason it cannot be folded into a behavior slice.
   - Each issue should reference the plan doc and carry its own acceptance check, continuity context, likely files/modules, verification command, readiness state when relevant, and out-of-scope notes.
   - Copy the plan's execution coordination and continuity fields into each issue: mode, parallel group, dependencies, expected overlap, worktree requirement, claim protocol, prior output to preserve, and existing logic to reuse or extend.
   - For `needs human decision` issues, name the specific decision, artifact, public or caller contract, access, dependency, or manual review needed before implementation can start.
   - Decide GitHub metadata from plan scale and coordination needs; leave metadata unset for sequential single-agent work when body/comments are enough.
   - Use relationships, milestones, projects, assignees, labels, or Development links only when they improve dependency tracking, release grouping, filtering, ownership, or branch/PR traceability.
   - Update the plan with issue links after creation.
   - Do not mark an issue `agent-ready` unless the issue body and current repo evidence are enough for an implementer to start without a new human decision.
4. Execute one issue at a time.
   - Pick the next unblocked issue.
   - Inspect the current issue body, comments, metadata, linked PRs, and recent activity before editing.
   - If the issue is marked `needs human decision`, do not implement it until the missing decision or artifact is supplied and the issue is updated.
   - For later issues, inspect completed dependency issue comments, commits, and current source before editing; name the implementation path to reuse, extend, or preserve.
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
   - Do not start implementation from the plan title, issue title, or issue list alone. Use the issue body, dependency results, current source, accepted scope, public or caller contract, and claim state as the baseline.
5. Checkpoint after each issue.
   - Use `verify-before-done` before claiming the issue is complete.
   - Inspect the diff against the issue and plan.
   - Update the issue and plan with changed files, checks run, commit/branch/PR, established logic for dependent issues to reuse or extend, readiness changes, open risks, claim status, and next issue.
   - Check that comments, Development links, relationships, dependencies, and open risks agree before moving on.
   - Use `workspace-safety` before staging, committing, or pushing.
   - Commit only the current issue's intended files from the parent workspace or assigned worktree, then push the branch when the workflow calls for remote checkpoints.
   - Do not commit or push if verification failed, diff review does not match the issue, the claim/status comment is stale, or unrelated files would be included.

## Stop Or Ask

Stop before continuing when:

- the user has not approved durable plan docs, GitHub issues, commits, or pushes
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
