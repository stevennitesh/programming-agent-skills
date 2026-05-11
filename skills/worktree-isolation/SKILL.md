---
name: worktree-isolation
description: Use when approved parallel implementation across agents or sessions needs separate git branches/worktrees; overlap also needs an integration strategy before editing.
---

# Worktree Isolation

Create isolated git worktrees for parallel implementation.

Use this to keep active agents or sessions from clobbering filesystem, branch, generated output, lockfile, or test artifact state.
The parent keeps responsibility for integration.

## Rule

Sequential implementation does not require a worktree by default.

Any approved parallel implementation gets one branch/worktree per active implementation issue, session, or subagent.

`parallel-overlap` still needs more than isolation.
The plan must name the overlap, integration owner, comparison strategy, and final verification path.

Worktrees prevent workspace collisions; they do not remove merge, design, or integration risk.

The parent agent owns worktree selection, safety checks, integration, cleanup, and final verification.

## Use Or Avoid

Use when:

- A plan or issue declares `parallel-disjoint` or `parallel-overlap` implementation.
- Two or more agents or sessions will edit source, tests, docs, config, generated output, lockfiles, or workflows at the same time.
- Parallel work is nominally disjoint but could collide through accidental edits, generated files, branch state, or shared test artifacts.
- `parallel-overlap` has an approved integration strategy and the overlap is worth the extra branch, merge, review, and verification cost.

Avoid when:

- Work is read-only exploration, review, planning, triage, or issue writing.
- Implementation is sequential, tiny, or handled by one parent-owned workspace.
- The next step is blocked on one decision or one failing check that should be handled locally first.
- The need is ordinary dirty-tree or risky Git safety without parallel implementation; use `workspace-safety`.

## Inputs

- Execution coordination block: mode, parallel group, dependencies, expected overlap, worktree requirement, and claim status
- Repo root, current branch, base branch, current working-tree state, and existing worktree list
- Repo instructions for branch names, worktree locations, setup, tests, generated output, and cleanup
- Task, issue, or subagent scope: owned files/modules, forbidden scope, acceptance check, and verification command
- Integration strategy for `parallel-overlap`
- Ignored local directories for repo-local worktrees

## Process

1. Establish safety.
   - Use `workspace-safety` before branch/worktree creation, dependency installs, generated output, staging, commits, pushes, or cleanup.
   - Check the current branch, base branch, working tree, worktree list, and issue claim state.
   - If mode is missing, treat it as `sequential` and do not create worktrees unless the user or repo policy explicitly requires them.
   - Confirm each parallel issue or subagent has distinct ownership, even when overlap is intentional.
   - For `parallel-overlap`, confirm the integration owner, comparison strategy, and final verification path before editing.
2. Choose a worktree location.
   - Prefer an existing repo convention such as `.worktrees/` or `worktrees/`.
   - For repo-local worktree directories, verify the directory is ignored before creating worktrees there.
   - If no convention exists, ask before adding a repo-local ignore rule or use an approved external location.
3. Create the worktree.
   - Use a descriptive branch name tied to the issue, slice, or subagent task.
   - Create one worktree per active implementation issue, session, or subagent.
   - Record the path, branch, base commit, execution mode, parallel group, owner, and expected check.
4. Establish a baseline when it matters.
   - Run the smallest known check that distinguishes pre-existing failures from new failures.
   - If setup or dependency install is required, follow repo instructions.
   - Treat generated or lockfile changes as task output only when expected.
   - If the baseline fails, report the failure and decide whether to diagnose, continue with known risk, or stop.
5. Hand off the isolated work.
   - Give each implementer the worktree path, branch, execution mode, ownership scope, forbidden scope, checks, and output schema.
   - Tell implementers they are not alone in the repo and must not touch other worktrees or parent-owned files.
6. Integrate deliberately.
   - Inspect each worktree diff before merging, cherry-picking, committing, or opening a PR.
   - For `parallel-overlap`, compare overlapping changes explicitly; do not merge by habit.
   - Use `verify-before-done` on each worktree result and again after integration when integration changes repo state.
   - Do not remove a worktree until needed changes are integrated, pushed, or explicitly abandoned.

## Stop Or Ask

Stop before creating or using a worktree when:

- no safe base branch or branch naming convention is known
- a repo-local worktree directory is not ignored and editing `.gitignore` is not approved
- implementation is sequential or unspecified and no user or repo policy requires isolation
- parallel work has no issue claim, ownership scope, expected check, or branch/worktree plan
- `parallel-overlap` has no integration owner, comparison strategy, or acceptance check
- overlap touches migrations, generated output, dependency/config state, or public contracts without a stronger integration plan
- setup commands require network, credentials, external services, or dependency changes that are not approved
- baseline checks fail and the failure affects the task's acceptance check
- cleanup would delete unmerged, unpushed, or unreviewed changes

## Output

```text
Execution mode:
Parallel group:
Worktree required:
Worktree:
Branch:
Base:
Task/issue:
Owner:
Ownership scope:
Forbidden scope:
Baseline check:
Verification command:
Integration plan:
Cleanup condition:
Open risks:
```

## Handoff

- `subagent-workflow`: return after branch/worktree paths are assigned for approved parallel implementation.
- `issue-driven-execution`: return after worktree setup when plan issues declare `parallel-disjoint` or `parallel-overlap`.
- `workspace-safety`: before branch/worktree creation, dependency install, generated output, staging, commits, pushes, or cleanup.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: the controlling implementation skill inside the worktree.
- `github-tracking`: when worktree branches map to issues, PRs, CI/check status, or review threads.
- `verify-before-done`: before claiming a worktree task, integration, branch, PR, or cleanup is complete.
