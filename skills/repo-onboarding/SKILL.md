---
name: repo-onboarding
description: Use when entering an unfamiliar repo, adopting this skill pack in a repo, resuming work after repo context is stale, or when build/test/GitHub/context conventions are unknown before coding.
---

# Repo Onboarding

Learn the repo's operating facts before changing code. Build only enough context to choose the right first source read, command, edit, or handoff.

## Rule

Onboarding should make later coding safer and faster, not create a repo dossier. Prefer source-of-truth files, runnable commands, and current repo state over summaries or assumptions.

## Inputs

Read only what helps the current coding work:

- Repo instructions: `AGENTS.md`, `CLAUDE.md`, README, contributor docs, test docs, or nearby overrides
- Project manifests and scripts that reveal setup, lint, typecheck, test, build, format, or run commands
- CI/workflow files when local commands are unclear or PR readiness matters
- Git state, branch conventions, remotes, and ignored scratch/worktree locations
- Existing issues, PRs, review threads, or release notes only when the task is tied to GitHub state
- `CONTEXT.md`, `CONTEXT-MAP.md`, or ADRs only for shared repo vocabulary, module boundaries, public contracts, and decisions

Do not use durable context files for progress, status, onboarding notes, or skill summaries.

## Process

1. Establish the baseline:
   - repo root and current branch
   - working tree state
   - relevant repo instructions and source-of-truth docs
   - known commands and whether they are cheap, expensive, external-service dependent, or destructive
2. Identify the likely first route:
   - implementation or behavior change -> `coding-router`
   - unclear target behavior or public contract -> `clarify-scope`
   - failing command, test, CI job, crash, log, or wrong output -> `diagnose-loop`
   - broad cleanup or refactor -> `codebase-cleanup`
   - plan doc, GitHub issues, and issue-by-issue execution -> `issue-driven-execution`
   - issue, PR, CI, or review-thread work -> `github-tracking`
3. Record only the operating facts needed for the next step:
   - relevant commands/checks
   - source or test entry points
   - repo-specific safety constraints
   - durable context locations
   - open questions that affect correctness, reversibility, data/state, security, dependencies, or external systems
4. If adopting this skill pack, confirm which skill files or repo instructions the user wants installed or referenced before writing setup files.

## Stop Or Ask

Ask or stop before continuing when:

- dependency install, migration, code generation, external service access, secrets, or credentials are needed
- docs and source disagree about a public contract, command, branch rule, or release path
- no safe verification command can be identified for the requested work
- the working tree has unrelated dirty files that overlap the intended edit scope
- GitHub or CI state is required but unavailable

If a missing fact is not blocking, state the assumption and continue with the smallest reversible next step.

## Output

```text
Repo:
Relevant instructions:
Commands/checks:
Source or test entry points:
Git/GitHub context:
Durable context:
Safety constraints:
Open questions:
Next route:
```

## Handoff

- Return to `coding-router` when enough repo context exists to choose the next workflow.
- Use `workspace-safety` before dirty-tree edits, branch/worktree actions, dependency installs, generated output, staging, commits, or PRs.
- Use `issue-driven-execution` when the user wants a plan doc, GitHub issues, and issue-by-issue execution after repo conventions are known.
- Use `github-tracking` when issue, PR, CI, review-thread, or durable GitHub state is part of the work.
- Use `verify-before-done` before claiming the repo is ready, checks are known, setup is complete, or adoption work is finished.
