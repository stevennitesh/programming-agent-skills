---
name: workspace-safety
description: "Use as a lightweight gate when overlapping dirty tracked paths, relevant untracked protected paths, or repo operations could overwrite, delete, publish, mix, stage, regenerate, or depend on unknown work: staging, commit, PR, push, merge, branch/worktree changes, installs, lockfiles, migrations, generators, broad formatters, generated cleanup, or destructive Git/filesystem commands."
---

# Workspace Safety

Protect unknown user work without slowing routine edits.

Protected paths means source, tests, docs, config, workflows, fixtures, migrations, lockfiles, checked-in generated artifacts, scripts, and untracked repo files.

## Rule

For risky work, first run:

```bash
git status --short --branch
```

Then name the intended touched paths and choose Fast Path or Escalation Path.

Classify only paths that overlap the requested action, expected command output, staging scope, branch/worktree operation, or destructive target. Do not classify every dirty file just because it exists.

Within one turn, reuse the latest status snapshot until an edit, formatter, generator, install, test, staging command, branch/worktree action, or cleanup command could have changed the tree.

If Git is unavailable or status cannot run, say what workspace evidence is missing and use the smallest safer file-level read before editing.

## Fast Path

Use for read-only questions, normal narrow edits, and focused checks.

Proceed when:

- the task is read-only and repo state does not matter
- intended touched paths are clean
- dirty paths are clearly unrelated to the touched scope
- no staging, commit, PR, branch/worktree, dependency, generator, migration, broad formatter, cleanup, or destructive action is involved

Do not inspect, classify, or report unrelated dirty files beyond the brief scope needed to show they do not overlap.

## Escalation Path

Use the full safety route when:

- touching a dirty tracked file
- an untracked protected path could be relevant
- staging, commit, PR, push, merge, branch, worktree, install, formatter, generator, migration, or cleanup is involved
- deleting, restoring, resetting, cleaning, force-pushing, or recursively moving files
- command output unexpectedly changes protected paths

Before touching a dirty tracked file, inspect the relevant hunks and work around unrelated changes. Stop or ask when unknown changes overlap the same lines, public or caller contract, data/state path, config/dependency behavior, generated output, migration, workflow, branch, or worktree operation.

## Decision Table

| Situation | Route |
| --- | --- |
| Read-only question | No status unless repo state matters. |
| Clean tree and narrow edit | Status, edit, focused check. |
| Dirty unrelated paths | Status, briefly name unrelated scope, edit intended clean files. |
| Dirty touched file | Inspect relevant hunks before editing. |
| Formatter, generator, install, or migration | Status before and after, then inspect produced diffs. |
| Stage, commit, PR, push, or merge | Use the commit/PR gate. |
| Delete, restore, reset, clean, force push, or recursive move | Inspect targets, dry-run when available, and require explicit approval unless the user explicitly requested that exact operation for exact targets. |

## Scratch And Generated Output

Use ignored `.tmp/` when available for scratch files, command logs, reproduction notes, generated issue/PR bodies, caches, and local experiment output.

Before relying on repo-local scratch, cache, generated-output, or worktree paths, verify they are ignored with repo evidence such as `git check-ignore -v <path>` or `git status --ignored --short <path>`, or keep them outside the repo.

Keep only generated, dependency, lockfile, formatter, or migration changes that support the requested work or verification. If unexpected paths change, stop and classify the diff before continuing.

## Destructive Actions

Never run destructive commands unless explicitly requested and the affected source, generated, scratch, and Git paths are understood:

- `git reset --hard`
- `git clean`
- `git checkout -- <path>`
- `git restore <path>`
- branch deletion
- force push
- recursive delete or move of files

If `git clean` is approved, dry-run first with `git clean -n` and compare the listed paths to the user's intent. Avoid `-x` unless ignored files are explicitly part of the cleanup.

Prefer non-interactive Git commands. When asking for approval, show the target paths, source scope, generated/scratch impact, and whether the action can be undone.

## Commit / PR Gate

Before commit or PR:

- inspect final working-tree diff
- confirm current branch and HEAD when push, PR, merge, or commit state matters
- run relevant checks after the final source, test, config, docs, workflow, migration, lockfile, or generated-file change
- stage only intended files unless the user explicitly asks for all changes
- run `git diff --check` for working-tree or PR-ready diffs, and `git diff --cached --check` when staging or committing
- leave unrelated work untouched
- use `verify-before-done` before claiming ready, safe, passing, mergeable, or complete

## Short Reporting

For fast-path work, keep safety reporting brief:

```text
Safety: <branch>, dirty paths do not overlap touched scope.
```

Expand only when there is overlap, ambiguity, generated output, branch/PR work, or destructive risk.

## Stop Or Ask

Stop or ask when:

- relevant dirty changes are unknown and overlap the work
- a dirty file must be edited but relevant hunks were not inspected
- an untracked protected path could be user work and could be touched
- a generated, dependency, formatter, migration, or tool command changed unexpected paths
- destructive action scope is unclear
- branch, PR, CI, merge, or worktree state matters but current state is unknown
- the safest route is a smaller edit, separate worktree, or user decision

## Handoff

Return to the controlling skill after the safety route is handled. Use `worktree-isolation` for approved parallel implementation, `github-tracking` for durable issue/PR record updates or recorded CI/review evidence, and `verify-before-done` for final readiness claims.
