---
name: worktree-isolation
description: Use when approved parallel implementation across agents or sessions needs separate git branches/worktrees, when a user explicitly asks for isolated worktrees, or when `parallel-disjoint`/`parallel-overlap` execution needs branch, ownership, integration, or cleanup safety before editing.
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

A linked worktree contains tracked files. It does not automatically contain ignored local resources from the parent checkout, such as raw data, generated artifacts, caches, local manifests, `.tmp` outputs, virtualenvs, credentials, or local config.

The parent agent owns worktree selection, safety checks, integration, cleanup, and final verification.

Owner terms: `Owner` is the person, agent, session, issue, or role responsible for the work. `Ownership scope` is the files, modules, contracts, or behavior that work may touch. `Worktree owner` is who created or controls the workspace. `Cleanup owner/condition` is who may remove it and when.

When this skill triggers, first write the isolation decision before creating or selecting a worktree: execution mode, whether a worktree is required, active implementers, ownership scope, overlap, integration owner, base branch, mechanism, directory ignore evidence, expected checks, and cleanup owner. This changes the route from "make a branch" to "prove the workspace split will not collide with user or agent work."

Worktree-ready means the task has an approved execution mode, source ownership scope, forbidden scope, public or caller contract or behavior, acceptance check, verification command, base branch, branch naming plan, worktree mechanism, directory location, cleanup condition, and resource parity plan. If those fields cannot be filled from the plan, issue, repo evidence, or user instruction, inspect or clarify before running `git worktree add`.

Do not create a worktree from a task title, stale plan summary, or vague "use agents" request alone. If execution mode is missing, treat it as `sequential`; do not create implementation worktrees unless the user or repo policy explicitly requires isolation.

## Use Or Avoid

Use when:

- A plan or issue declares `parallel-disjoint` or `parallel-overlap` implementation.
- The user explicitly asks for an isolated worktree or separate workspace for implementation.
- Two or more agents or sessions will edit source, tests, docs, config, generated output, lockfiles, or workflows at the same time.
- Parallel work is nominally disjoint but could collide through accidental edits, generated files, branch state, or shared test artifacts.
- `parallel-overlap` has an approved integration strategy and the overlap is worth the extra branch, merge, review, and verification cost.

Avoid when:

- Work is read-only exploration, review, planning, triage, or issue writing.
- Implementation is sequential, tiny, or handled by one parent-owned workspace.
- The next step is blocked on one decision or one failing check that should be handled locally first.
- The need is ordinary dirty-tree or risky Git safety without parallel implementation; use `workspace-safety`.
- The task lacks ownership scope, forbidden scope, acceptance check, verification command, base branch, or cleanup owner.

## Inputs

- Execution coordination block: mode, parallel group, dependencies, expected overlap, worktree requirement, and claim status
- Repo root, current branch, base branch, current working-tree state, and existing worktree list
- Environment detection: git dir/common dir, current branch, superproject path, and whether the current checkout is already isolated
- Repo instructions for branch names, worktree locations, setup, tests, generated output, and cleanup
- Runtime resources needed by the task: ignored data, generated artifacts, caches, `.tmp` outputs, local manifests, virtualenvs, credentials, local config, external service state, and absolute paths
- Task, issue, or subagent scope: owned files/modules, forbidden scope, public or caller contract or behavior, acceptance check, and verification command
- Integration strategy for `parallel-overlap`
- Chosen worktree mechanism, cleanup owner, and ignored-directory status for repo-local worktrees

## Process

1. Establish safety and detect the current workspace.
   - Use `workspace-safety` before branch/worktree creation, dependency installs, generated output, staging, commits, pushes, or cleanup.
   - Check the current branch, base branch, working tree, worktree list, and issue claim state.
   - Do not proceed from memory, a plan title, or a subagent request alone; verify current repo, branch, and issue/plan coordination state when it affects isolation.
   - Run read-only detection before deciding to create anything:
     ```bash
     git_dir=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
     git_common=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
     branch=$(git branch --show-current)
     superproject=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
     ```
   - Interpret the result:
     - `git_dir == git_common`: normal checkout.
     - `superproject` is non-empty: submodule; do not treat `git_dir != git_common` as linked-worktree proof until the repo boundary is clear.
     - `git_dir != git_common` and `superproject` is empty: already in a linked worktree.
     - `git_dir != git_common`, `superproject` is empty, and `branch` is empty: linked worktree with detached HEAD, likely harness-managed or user-created.
   - If the current checkout is already a linked worktree, record the path, branch state, owner if known, and cleanup owner; skip creating another worktree unless the user explicitly requested a separate one.
   - If mode is missing, treat it as `sequential` and do not create worktrees unless the user or repo policy explicitly requires them.
   - Confirm each parallel issue or subagent has distinct ownership, even when overlap is intentional.
   - For `parallel-overlap`, confirm the integration owner, comparison strategy, and final verification path before editing.
   - Stop before creation if unknown dirty work overlaps the same files, public or caller contract, generated output, dependency/config behavior, branch state, or cleanup target.
2. Choose a worktree mechanism and location.
   - Prefer host or harness-native worktree controls before manual git, such as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or a `--worktree` mode.
   - If a native control creates or selects the worktree, record the mechanism and any cleanup owner it implies.
   - Use manual `git worktree add` only as a fallback when no native tool applies and worktree creation is approved.
   - Prefer an existing repo convention such as `.worktrees/` or `worktrees/`.
   - For the chosen repo-local worktree directory, verify the directory is ignored before creating worktrees there, for example `git check-ignore -q -- .worktrees/` or `git check-ignore -q -- worktrees/`, and record the evidence.
   - If the chosen repo-local directory is not ignored, ask before adding an ignore rule, choose an approved external location, or stop.
   - Do not create a repo-local worktree path that would appear as untracked source, docs, config, generated output, or local-only data.
3. Create or select the worktree.
   - If an existing or native worktree is selected, record the path, branch state, mechanism, owner, and cleanup condition.
   - If using manual git fallback, use a descriptive branch name tied to the issue, slice, or subagent task.
   - Create or select one worktree per active implementation issue, session, or subagent.
   - If manual `git worktree add` fails because of sandbox or permission limits, report the failure and stop unless the user approves a different route.
   - Record the path, branch, base commit, execution mode, parallel group, owner, expected check, worktree mechanism, and directory ignore status.
   - After creation or selection, confirm the worktree path and branch match the assigned task before handing it to an implementer.
4. Establish resource parity before implementation.
   - Inspect the task, repo docs, config, manifests, tests, and commands for required ignored or generated resources.
   - Check the selected worktree for those resources before the first source edit or smoke command.
   - For each required resource, record one status:
     - present in worktree
     - intentionally absent and not needed
     - copied with approval
     - symlinked with approval
     - accessed through an explicit absolute path or config override
     - blocked until provided
   - Do not assume ignored files from the parent checkout exist in the worktree.
   - If a check or smoke uses parent-checkout resources, label it as external resource access. Record the parent path, why it was used, and whether the result proves worktree-local behavior or only configured external-resource behavior.
   - Stop before editing when required resources are absent and there is no approved copy, symlink, absolute-path override, config override, or user-provided substitute.
5. Establish a baseline when it matters.
   - Run the smallest known check that distinguishes pre-existing failures from new failures.
   - Run baseline commands from the selected worktree unless explicitly labeled as a parent-checkout or external-resource check.
   - If setup or dependency install is required, follow repo instructions.
   - Treat generated or lockfile changes as task output only when expected.
   - If the baseline fails, report the failure and decide whether to diagnose, continue with known risk, or stop.
6. Keep current-directory discipline.
   - Run every source edit, test, smoke, and git command from the selected worktree unless the command is explicitly labeled as parent-checkout, integration, cleanup, or external-resource work.
   - Do not report a check as worktree verification if it ran in the parent checkout.
   - When config, manifests, file paths, data roots, cache paths, or generated-output paths changed, run at least one path-sensitive smoke from inside the selected worktree.
   - If the path-sensitive smoke must read files outside the worktree, record the exact external path and the override or config that made it intentional.
   - When reporting status, include both parent checkout status and isolated worktree status. Include untracked files in the worktree; `git diff --stat` alone is not enough because it hides new manifests, configs, fixtures, and generated files.
7. Hand off the isolated work.
   - Give each implementer the worktree path, branch, execution mode, ownership scope, forbidden scope, resource parity plan, checks, and output schema.
   - Tell implementers they are not alone in the repo and must not touch other worktrees or parent-owned files.
   - Include the public or caller contract or behavior, acceptance check, first check, verification command, dependency/setup expectations, resource access rules, and cleanup rule.
8. Integrate deliberately.
   - Inspect each worktree diff before merging, cherry-picking, committing, or opening a PR.
   - For `parallel-overlap`, compare overlapping changes explicitly; do not merge by habit.
   - Use `verify-before-done` on each worktree result and again after integration when integration changes repo state.
   - Record cleanup provenance: existing checkout, harness-managed worktree, user-created worktree, or worktree created for this task.
   - Cleanup only worktrees created for this task, after needed changes are integrated, pushed, or explicitly abandoned.
   - Do not remove harness-managed, detached-HEAD, user-created, or unknown-owner worktrees unless explicitly approved.
   - If removal is approved, run it from the main repo root, not from inside the worktree being removed.
   - Do not claim integration, cleanup, branch, PR, or merge readiness until `verify-before-done` maps the exact claim to fresh evidence.

## Stop Or Ask

Stop before creating or using a worktree when:

- current checkout appears to be a submodule and the repo boundary is unclear
- an existing linked worktree is detected but branch state, owner, or cleanup responsibility is unclear
- a native worktree control appears available but has not been checked
- no safe base branch or branch naming convention is known
- a repo-local worktree directory is not ignored and editing `.gitignore` is not approved
- implementation is sequential or unspecified and no user or repo policy requires isolation
- parallel work has no issue claim, ownership scope, forbidden scope, expected check, verification command, or branch/worktree plan
- `parallel-overlap` has no integration owner, comparison strategy, or acceptance check
- overlap touches migrations, generated output, dependency/config state, or public or caller contracts without a stronger integration plan
- required ignored or generated resources are missing from the worktree and there is no approved copy, symlink, absolute-path override, config override, or user-provided substitute
- config, manifest, data-root, cache-path, or generated-output behavior changes but no path-sensitive smoke can run from the selected worktree
- setup commands require network, credentials, external services, or dependency changes that are not approved
- baseline checks fail and the failure affects the task's acceptance check
- manual `git worktree add` fails because of sandbox or permission limits
- cleanup provenance is unknown or cleanup would delete unmerged, unpushed, or unreviewed changes
- worktree removal would run from inside the target worktree

## Output

```text
Execution mode:
Parallel group:
Worktree required:
Existing isolation:
Worktree mechanism: native | git fallback | existing
Worktree:
Branch:
Base:
Directory ignored: yes | no | external | not applicable
Directory ignore evidence:
Parent checkout status:
Worktree status:
Untracked worktree files:
Runtime resources:
Resource parity:
External resource access:
Verification working directory:
Path-sensitive smoke:
Task/issue:
Owner:
Worktree owner: task | user | harness | unknown
Ownership scope:
Forbidden scope:
Public or caller contract:
Baseline check:
Verification command:
Integration plan:
Cleanup owner/condition:
Open risks:
```

## Handoff

- `subagent-workflow`: return after branch/worktree paths are assigned for approved parallel implementation.
- `issue-driven-execution`: return after worktree setup when plan issues declare `parallel-disjoint` or `parallel-overlap`.
- `workspace-safety`: before branch/worktree creation, dependency install, generated output, staging, commits, pushes, or cleanup.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: the controlling implementation skill inside the worktree.
- `github-tracking`: when worktree branches map to issues, PRs, CI/check status, or review threads.
- `verify-before-done`: before claiming a worktree task, integration, branch, PR, or cleanup is complete.
