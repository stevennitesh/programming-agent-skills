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
- Existing repo agent setup such as `docs/agents/`, issue-tracker docs, label/readiness vocabulary, local issue folders, or skill-pack notes only when adopting or refreshing agent workflow setup

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
4. If adopting or refreshing this skill pack, run the adoption branch below.

## Adoption Branch

Use this branch only when the user is installing this pack in a repo, asking whether repo agent setup is complete, or when missing repo workflow facts would make several skills guess.

Discover:

- Agent instruction target: existing `AGENTS.md` or `CLAUDE.md`, including nearby overrides and any existing agent-skills block
- Issue tracker: GitHub, GitLab, local markdown, other tracker, or none; include the command/tool only when repo evidence or the user confirms it
- Triage/readiness vocabulary: issue labels or status fields used for waiting, ready for agent, ready for human, won't-fix, blocked, or similar states
- Domain docs: `CONTEXT.md`, `CONTEXT-MAP.md`, ADR locations, glossary files, architecture docs, and whether the repo is single-context or multi-context
- Work locations: where plans, scratch files, generated logs, local issues, and handoff docs belong
- Verification facts: cheap local checks, expensive checks, external-service checks, release gates, and commands that should not run by default

Present:

- Found facts
- Missing facts that affect future skill behavior
- Assumptions that are safe to carry for the next small task
- Decisions that need the user because repo evidence cannot choose safely

Write only after approval:

- Prefer updating the existing repo instruction file over creating a parallel one.
- If neither `AGENTS.md` nor `CLAUDE.md` exists, ask which convention to create before writing.
- Update an existing agent-skills block in place instead of appending a duplicate.
- Create optional `docs/agents/` files only when the same issue-tracker, label, domain-doc, or verification facts will be reused by multiple skills.
- Keep repo setup docs as durable facts and conventions, not progress notes, task status, or skill summaries.

## Stop Or Ask

Ask or stop before continuing when:

- dependency install, migration, code generation, external service access, secrets, or credentials are needed
- docs and source disagree about a public contract, command, branch rule, or release path
- no safe verification command can be identified for the requested work
- the working tree has unrelated dirty files that overlap the intended edit scope
- GitHub or CI state is required but unavailable
- adopting the skill pack would create or rewrite repo instructions, `docs/agents/` files, labels, issue tracker settings, or workflow conventions without user approval
- existing repo instructions conflict about issue tracking, branch rules, checks, domain docs, or agent setup

If a missing fact is not blocking, state the assumption and continue with the smallest reversible next step.

## Output

```text
Repo:
Relevant instructions:
Commands/checks:
Source or test entry points:
Git/GitHub context:
Durable context:
Adoption facts:
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
