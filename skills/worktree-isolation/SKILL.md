---
name: worktree-isolation
description: Use when approved parallel implementation across agents or sessions needs separate git branches/worktrees, when a user explicitly asks for isolated worktrees, or when `parallel-disjoint`/`parallel-overlap` execution needs branch, ownership, integration, or cleanup safety before editing.
---

# Worktree Isolation

Create or select isolated git worktrees only when isolation is required. Keep normal sequential work in the current workspace.

## Rule

Sequential implementation does not require a worktree by default.

Any approved parallel implementation gets one branch/worktree per active implementation issue, session, or subagent. `parallel-overlap` also needs an integration owner, overlap description, comparison strategy, and final verification path.

Worktrees prevent workspace collisions; they do not remove merge, design, or integration risk.

A linked worktree contains tracked files. It does not automatically contain ignored local resources from the parent checkout, such as raw data, generated artifacts, caches, local manifests, `.tmp` outputs, virtualenvs, credentials, or local config.

The parent owns worktree selection, safety checks, integration, cleanup, and final verification.

Owner terms: `Owner` is the person, agent, session, issue, or role responsible for the work. `Ownership scope` is the files, modules, contracts, or behavior that work may touch. `Cleanup owner/condition` is who may remove the workspace and when.

## Fast Gate

Before creating or selecting a worktree:

1. If implementation is sequential and isolation was not explicitly requested, do not create a worktree. Return to the current route.
2. If already in a linked worktree, record path, branch or detached HEAD, owner, and cleanup condition if known. Continue there unless the user explicitly requested a separate worktree.
3. If work is parallel or explicitly isolated, require ownership scope, forbidden scope, base branch, verification command, cleanup owner/condition, and resource parity plan before creation.

Stop or route back before editing when the gate cannot answer:

- Is implementation parallel or explicitly isolated?
- Is ownership and forbidden scope clear?
- Is the base branch and worktree location safe?
- Are required ignored/generated resources present, intentionally absent, or explicitly provided?
- Is there a path-sensitive smoke/check from inside the selected worktree when paths or resources matter?

If execution mode is missing, treat it as `sequential`; do not create implementation worktrees unless the user or repo policy explicitly requires isolation.

## Use Or Avoid

Use when:

- a plan or issue declares `parallel-disjoint` or `parallel-overlap` implementation
- the user explicitly asks for an isolated worktree or separate implementation workspace
- two or more agents or sessions will edit source, tests, docs, config, generated output, lockfiles, or workflows at the same time
- parallel work is nominally disjoint but could collide through accidental edits, generated files, branch state, or shared test artifacts
- `parallel-overlap` has an approved integration strategy and the overlap is worth the extra branch, merge, review, and verification cost

Avoid when:

- work is read-only exploration, review, planning, triage, or issue writing
- implementation is sequential, tiny, or handled by one parent-owned workspace
- one decision or one failing check should be handled locally first
- the need is ordinary overlapping dirty-path or risky Git safety without parallel implementation; use `workspace-safety`
- ownership scope, forbidden scope, acceptance check, verification command, base branch, or cleanup owner is unknown

## Full Path

Use the full path only when the Fast Gate requires an isolated workspace.

1. Detect the current checkout/worktree.
   - Use `workspace-safety` before branch/worktree creation, dependency installs, generated output, staging, commits, pushes, or cleanup.
   - Inspect current branch, base branch, working tree, worktree list, and issue/plan execution mode when that state affects isolation.
   - For linked-worktree detection, compare `git rev-parse --git-dir` with `git rev-parse --git-common-dir`, check `git branch --show-current`, and check `git rev-parse --show-superproject-working-tree` so submodules are not mistaken for linked worktrees.
   - If the current checkout is already a linked worktree, record path, branch state, owner if known, and cleanup condition. Skip creating another worktree unless explicitly requested.
2. Create or select a worktree only when required.
   - Prefer host or harness-native worktree controls before manual `git worktree add`.
   - Prefer a repo convention such as `.worktrees/` or `worktrees/`. Verify repo-local worktree directories are ignored before creating paths there.
   - Use manual `git worktree add` only as an approved fallback. Use a descriptive branch tied to the issue, slice, or subagent task.
   - Record path, branch, base commit, execution mode, owner, mechanism, directory ignore status, and cleanup condition.
3. Establish resource parity before implementation.
   - Inspect repo docs, config, manifests, tests, commands, and task scope for required ignored or generated resources.
   - Check the selected worktree for those resources before the first source edit or smoke command.
4. Run baseline/checks from the selected worktree.
   - Run the smallest known check that distinguishes pre-existing failures from new failures when baseline matters.
   - Label any parent-checkout or external-resource check explicitly.
   - Treat setup, installs, generated output, and lockfile changes through `workspace-safety`.
5. Hand off implementation only after the selected worktree is ready.
   - Give the implementer path, branch, execution mode, ownership scope, forbidden scope, resource parity status, first check, acceptance check, verification command, and cleanup rule.
   - Do not duplicate `subagent-workflow` packet templates here.
6. Integrate and clean up deliberately.
   - Inspect each worktree diff before merging, cherry-picking, committing, or opening a PR.
   - For `parallel-overlap`, compare overlapping changes explicitly; do not merge by habit.
   - Cleanup only worktrees created for this task and only after needed changes are integrated, pushed, or explicitly abandoned.

## Resource Parity

For each required ignored or generated resource, record one status:

- present in worktree
- intentionally absent and not needed
- copied with approval
- symlinked with approval
- accessed through an explicit absolute path or config override
- blocked until provided

Do not assume ignored files from the parent checkout exist in the worktree.

If a check or smoke uses parent-checkout resources, label it as external resource access. Record the parent path, why it was used, and whether the result proves worktree-local behavior or only configured external-resource behavior.

Stop before editing when required resources are absent and there is no approved copy, symlink, absolute-path override, config override, or user-provided substitute.

## Command Directory Discipline

Run source edits, tests, smokes, and git commands from the selected worktree unless the command is explicitly labeled as parent-checkout, integration, cleanup, or external-resource work.

Do not report a check as worktree verification if it ran in the parent checkout.

When config, manifests, file paths, data roots, cache paths, or generated-output paths changed, run at least one path-sensitive smoke from inside the selected worktree. If the smoke must read files outside the worktree, record the exact external path and the override or config that made it intentional.

When reporting status, distinguish parent checkout status from isolated worktree status. Include untracked files in the worktree; `git diff --stat` alone hides new manifests, configs, fixtures, and generated files.

## Integration And Cleanup

Record cleanup provenance: existing checkout, harness-managed worktree, user-created worktree, or worktree created for this task.

Do not remove harness-managed, detached-HEAD, user-created, or unknown-owner worktrees unless explicitly approved. If removal is approved, run it from the main repo root, not from inside the worktree being removed.

Use `verify-before-done` on each worktree result and again after integration when integration changes repo state. Do not claim integration, cleanup, branch, PR, or merge readiness until the exact claim is mapped to fresh evidence.

## Stop Or Ask

Stop before creating or using a worktree when:

- current checkout appears to be a submodule and the repo boundary is unclear
- an existing linked worktree is detected but branch state, owner, or cleanup responsibility is unclear
- a native worktree control appears available but has not been checked
- no safe base branch or branch naming convention is known
- a repo-local worktree directory is not ignored and editing `.gitignore` is not approved
- implementation is sequential or unspecified and no user or repo policy requires isolation
- parallel work lacks issue claim, ownership scope, forbidden scope, expected check, verification command, or branch/worktree plan
- `parallel-overlap` lacks integration owner, comparison strategy, or acceptance check
- overlap touches migrations, generated output, dependency/config state, or public or caller contracts without a stronger integration plan
- required ignored or generated resources are missing from the worktree and no approved substitute exists
- config, manifest, data-root, cache-path, or generated-output behavior changes but no path-sensitive smoke can run from the selected worktree
- setup commands require network, credentials, external services, or dependency changes that are not approved
- baseline checks fail and the failure affects the task's acceptance check
- manual `git worktree add` fails because of sandbox or permission limits
- cleanup provenance is unknown or cleanup would delete unmerged, unpushed, or unreviewed changes
- worktree removal would run from inside the target worktree

## Report

Fast report:

```text
Worktree decision:
Worktree/path:
Resource parity:
Verification directory:
Open risks:
```

Full report adds:

```text
Execution mode:
Parent checkout status:
Worktree status:
Untracked worktree files:
External resource access:
Baseline:
Path-sensitive smoke:
Integration plan:
Cleanup owner/condition:
```

## Handoff

- `subagent-workflow`: return after branch/worktree paths are assigned for approved parallel implementation.
- `issue-driven-execution`: return after worktree setup when plan issues declare `parallel-disjoint` or `parallel-overlap`.
- `workspace-safety`: before branch/worktree creation, dependency install, generated output, staging, commits, pushes, or cleanup.
- `tdd-slice`, `diagnose-loop`, or `codebase-cleanup`: the controlling implementation skill inside the worktree.
- `github-tracking`: when worktree branches need durable issue/PR links, claim/status comments, readiness/blocker updates, or recorded CI/review evidence.
- `verify-before-done`: before claiming a worktree task, integration, branch, PR, or cleanup is complete.
