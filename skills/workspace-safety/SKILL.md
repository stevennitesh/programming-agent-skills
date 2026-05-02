---
name: workspace-safety
description: Use before risky edits, branch or worktree changes, commits, PRs, destructive file or git operations, dependency installs, generated output, or when the working tree has user changes.
---

# Workspace Safety

Protect user work. Make local operations reversible whenever practical.

## Rule

Current files belong to the user unless you created the change in this session. Preserve unknown work before optimizing speed.

## Baseline

Before risky edits or git actions when git is available:

```bash
git status --short --branch
```

If files are dirty:

- Identify which changes are yours, user-provided, or unknown.
- Do not revert or overwrite unknown changes.
- If touching a dirty file, inspect the relevant hunks first and work with them.
- If your edit and an unknown edit affect the same lines, stop and ask or choose a smaller edit.
- Treat untracked files as possible user work unless they are known scratch output you created.

## Scratch

- Use `.tmp/` for scratch files, generated issue bodies, caches, logs, and local experiments.
- Do not commit scratch output unless requested.
- `CONTEXT.md` is durable documentation, not scratch. Inspect it before editing if dirty.
- Before relying on a new project-local scratch or worktree directory, verify it is ignored or keep it outside the repo.

## Branches And Worktrees

Use a branch or worktree when:

- Work touches many files or unrelated areas.
- Multiple tasks may run independently.
- User wants isolated feature work.
- Current tree has unrelated changes.

For project-local worktrees:

- Ensure the directory is ignored before creating it.
- Check the current branch and worktree list before removing or switching.
- Run the smallest known baseline check in a new worktree when the work depends on distinguishing new failures from pre-existing failures.
- Do not remove a worktree unless it was created for this task and no needed changes remain, or the user approves.

## Git Safety

Never run destructive commands unless explicitly requested and the affected paths are understood:

- `git reset --hard`
- `git clean`
- `git checkout -- <path>`
- `git restore <path>`
- branch deletion
- force push
- recursive delete or move of files

If `git clean` is approved, dry-run first with `git clean -n` and compare the listed paths to the user's intent. Avoid `-x` unless ignored files are explicitly part of the cleanup.

Prefer non-interactive git commands. Show exact risk, target paths, and whether the action can be undone when asking for approval.

## Generated Or Installed Output

Dependency installs, formatters, code generators, migrations, and build tools can change lockfiles or generated files. Before keeping those changes:

1. Know why the command is needed.
2. Inspect the new diff.
3. Keep only outputs that support the requested work.

## Commit/PR Readiness

Before commit or PR:

1. Review diff.
2. Run relevant checks.
3. Stage only intended files; avoid broad staging in a dirty tree.
4. Use a message that states the real change.
5. Leave unrelated work untouched.
6. Use `verify-before-done` before claiming the branch, commit, or PR is ready.

## Handoff

After safety risk is handled, return to the controlling skill. Use `github-work-tracking` for issues, PRDs, PR creation, or CI evidence. Use `verify-before-done` before any final ready, fixed, passing, safe, or mergeable claim.
