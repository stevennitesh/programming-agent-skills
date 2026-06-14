---
name: repo-onboarding
description: "Use when entering an unfamiliar repo, adopting this skill pack in a repo, resuming work when stale commands/instructions/context matter now, or when build/test/GitHub/context conventions are unknown before coding."
---

# Repo Onboarding

Learn the repo's operating facts before changing code. Build only enough context to choose the right first source read, command, edit, or handoff.

## Rule

Onboarding should make later coding safer and faster, not create a repo dossier. Prefer source-of-truth files, runnable commands, and current repo state over summaries or assumptions.

When entering an unfamiliar repo, adopting this skill pack, or facing unknown build/test/GitHub/context conventions, first identify the repo root, current branch, working tree state, nearest repo instructions, source-of-truth commands, relevant entry points, safety constraints, and the next route.

Stale context means a command, instruction, branch, dependency, tracker, source entry point, or safety fact could be outdated and matters to the current task. Do not re-onboard only because time passed.

Before changing code, running expensive commands, creating repo instructions, opening issues, or claiming setup is known, account for which facts came from repo evidence, which assumptions are safe for the next small task, which missing facts affect correctness or safety, and what first source read, command, edit, check, or handoff should happen next.

## Inputs

Read only what helps the current coding work:

- nearest repo instructions and command sources
- manifests, scripts, test docs, or CI only when commands/checks matter
- branch, dirty state, remotes, and scratch/worktree rules when safety or GitHub state matters
- relevant source/test entry points for the current task
- `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, issues, PRs, or review threads only when shared terms, contracts, tracker state, or external state matter now
- existing agent setup only when adopting or refreshing repo workflow setup

Do not use durable context files for progress, status, onboarding notes, or skill summaries.

## Fast Path

Default to a 2-minute operating-facts pass:

1. Read the nearest repo instructions and manifest, script, or docs source that identifies commands.
2. Check branch and working tree state.
3. Identify only the commands/checks, entry points, safety constraints, and missing facts needed for the current task.
4. Hand off to `coding-router` or the one obvious controller.

Stop onboarding once the next source read, command, edit, check, or handoff is clear.

## Niche Adoption Path

Use only when the user asks to install, adopt, audit, or refresh repo agent setup, or when several skills would otherwise guess repo workflow facts.

Discover:

- repo instruction target and nearby overrides
- tracker type, readiness vocabulary, and issue/PR conventions when repo evidence establishes them
- durable context docs, work locations, scratch/generated-output rules, and verification facts reused by multiple skills
- public or caller contracts, module boundaries, generated artifacts, dependency/config state, or data/security rules that several skills must preserve

Present:

- Found facts
- Missing facts that affect future skill behavior
- Assumptions that are safe to carry for the next small task
- Decisions that need the user because repo evidence cannot choose safely
- First route and first observable action after onboarding

Write only after approval:

- Prefer updating the existing repo instruction file over creating a parallel one.
- If neither `AGENTS.md` nor `CLAUDE.md` exists, ask which convention to create before writing.
- Update an existing agent-skills block in place instead of appending a duplicate.
- Create optional `docs/agents/` files only when the same issue-tracker, label, domain-doc, or verification facts will be reused by multiple skills.
- Keep repo setup docs as durable facts and conventions, not progress notes, task status, or skill summaries.
- Do not invent labels, readiness states, issue-tracker workflows, scratch locations, worktree conventions, or verification gates when repo evidence does not establish them. Record a safe assumption or ask for the missing decision.

## Stop Or Ask

Ask or stop before continuing when:

- dependency install, migration, code generation, external service access, secrets, or credentials are needed
- docs and source disagree about a public or caller contract, command, branch rule, or release path
- no safe verification command can be identified for the requested work
- the working tree has unrelated dirty files that overlap the intended edit scope
- GitHub or CI state is required but unavailable
- source-of-truth commands are missing, contradictory, destructive, external-service dependent, or too expensive for the requested risk
- adoption would mark a repo `agent-ready`, setup complete, or checks known without enough evidence
- adopting the skill pack would create or rewrite repo instructions, `docs/agents/` files, labels, issue tracker settings, or workflow conventions without user approval
- existing repo instructions conflict about issue tracking, branch rules, checks, domain docs, or agent setup

If a missing fact is not blocking, state the assumption and continue with the smallest reversible next step.

## Avoid

- Guessing commands, branches, package managers, issue trackers, or readiness vocabulary when repo evidence is cheap to inspect.
- Reading broad source trees or history after the first safe route and entry points are already clear.
- Running full suites, dependency installs, code generation, migrations, live commands, or external-service checks just to finish onboarding.
- Treating generated summaries, memory, plans, or chat notes as proof of current repo behavior.
- Writing `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/agents/`, labels, or tracker conventions as progress notes.

## Output

```text
Repo:
Relevant instructions:
Commands/checks:
Source or test entry points:
Safety constraints:
Assumptions/missing facts:
Next route:
```

Add `Adoption facts:` only when the Niche Adoption Path ran.

## Handoff

- Return to `coding-router` when enough repo context exists to choose the next workflow.
- Use `workspace-safety` before dirty-tree edits, branch/worktree actions, dependency installs, generated output, staging, commits, or PRs.
- Use `issue-driven-execution` when the user wants a plan doc, GitHub issues, and issue-by-issue execution after repo conventions are known.
- Use `github-tracking` when issue, PR, CI, review-thread, or durable GitHub state is part of the work.
- Use `verify-before-done` before claiming the repo is ready, checks are known, setup is complete, or adoption work is finished.
