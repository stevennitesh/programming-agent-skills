# Programming Agent Skills

A small skill pack for coding agents working in real software repos.

These skills give coding agents just enough operating structure to learn a repo, clarify scope, make reviewable source changes, debug from evidence, protect user work, track GitHub context, coordinate subagents, and verify before claiming success. The goal is better engineering behavior, not a bigger process framework.

## Why This Exists

Coding agents often fail in predictable ways. They over-plan, overbuild, trust stale summaries, skip reproduction, edit before understanding the baseline, lose track of user changes, or report completion without fresh evidence.

This pack nudges agents toward a better default:

- Read relevant source, tests, fixtures, logs, docs, diffs, or CI output before acting.
- Choose one useful workflow instead of every possible process.
- Prefer small, reviewable changes over broad rewrites.
- Treat tests, commands, diffs, CI status, and observed behavior as evidence.
- Protect user work and state uncertainty honestly.

## Design Influences

This pack was shaped by a few ideas people in the coding-agent space already recognize: Superpowers-style skill workflows, Matt Pocock's bias toward engineering discipline, and Andrej Karpathy's discussions of agent failure modes and the tradeoffs of coding with agents.

The intent is not to give agents a giant rulebook. It is to steer them toward grounded, scoped, verified work while leaving room for exploration when the task calls for it.

## Who This Is For

- Developers using coding agents to make real repo changes.
- Maintainers who want portable guardrails for coding-agent behavior.
- Teams that want fewer skipped checks, unsafe Git moves, and vague completion claims.
- People who like small reusable procedures more than heavyweight process.

## Quick Start

For portable repo defaults, copy [AGENTS.md](AGENTS.md) into a programming repo and adapt the repo-specific source-of-truth files, commands, constraints, and release rules.

For skill-based agent setups, copy the skills you want into your local skill directory, or point your tooling at `skills/` if it supports repo-local skills.

For a Codex-style local setup:

```bash
cp -R skills/coding-router "$CODEX_HOME/skills/"
cp -R skills/repo-onboarding "$CODEX_HOME/skills/"
cp -R skills/clarify-scope "$CODEX_HOME/skills/"
cp -R skills/tdd-slice "$CODEX_HOME/skills/"
```

You can copy the whole pack, but you do not have to. Start with `repo-onboarding` for unfamiliar repos, then use `coding-router` when you want the agent to choose the right route for actual work.

## How It Works

Most nontrivial work starts with `coding-router`. It chooses the smallest reliable next workflow based on the request, repo evidence, risk, and expected completion check.

The pack uses two kinds of skills:

- Controlling skills own the main workflow: repo entry, scope, planning, implementation, debugging, cleanup, or skill authoring.
- Gate skills step in at risk boundaries: workspace safety, GitHub tracking, subagent coordination, or final verification.

Typical paths:

- New repo or stale repo context: `repo-onboarding` -> `coding-router` -> selected workflow
- Feature or behavior request: `coding-router` -> `clarify-scope` or `slice-plan` -> `tdd-slice` -> `verify-before-done`
- Bug, failing test, build, CI job, or log error: `coding-router` -> `diagnose-loop` -> focused source change and regression check -> `verify-before-done`
- Cleanup or refactor: `coding-router` -> `codebase-cleanup` -> behavior-preserving slice -> `verify-before-done`
- PR or review work: `coding-router` -> `github-tracking` -> source change or response -> `verify-before-done`
- Multi-agent work: controlling skill -> `subagent-workflow` -> parent diff review and verification

## Skill Map

| Skill | Use it when |
| --- | --- |
| `repo-onboarding` | A coding agent needs to learn an unfamiliar repo's instructions, commands, context, GitHub conventions, and safety constraints before work. |
| `coding-router` | A nontrivial repo task needs the right next workflow. |
| `clarify-scope` | The request is unclear, broad, user-facing, caller-facing, architectural, or risky. |
| `slice-plan` | Approved work needs multiple reviewable source, test, docs, or tracking slices. |
| `tdd-slice` | You are implementing or changing one caller-visible behavior with a focused check. |
| `diagnose-loop` | Tests, builds, CI, logs, output, crashes, or behavior are failing and the cause is not yet clear. |
| `codebase-cleanup` | Cleanup or refactor work should preserve behavior while making future changes easier. |
| `github-tracking` | Issues, PRDs, PRs, CI status, review threads, or durable GitHub records are useful. |
| `subagent-workflow` | Bounded codebase exploration, implementation, or review can safely run through subagents. |
| `workspace-safety` | Dirty trees, branches, staging, commits, generated output, dependency installs, or risky Git/file operations need care. |
| `verify-before-done` | The agent is about to claim work is done, fixed, reviewed, passing, safe, ready, or mergeable. |
| `author-skills` | You are creating or revising coding-agent skills or skill-pack instructions. |

## What This Is Not

- Not a package manager or runtime framework.
- Not a replacement for repo docs, source code, tests, review, CI, or user instruction.
- Not a rule that every task needs extra process. Tiny safe edits can use a tiny source-read, edit, check loop.
- Not a promise that process creates correctness. Evidence still has to come from the repo and the checks that matter.

## Principles

- Evidence over impressions.
- Source, tests, fixtures, logs, diffs, and CI output over stale summaries.
- One controlling workflow at a time.
- Smallest useful slice before broad rewrites.
- Reproduce bugs before fixing them.
- Preserve existing behavior during refactors unless asked to change it.
- Protect user work, agent work, and unrelated changes.
- Verify before completion claims.
- Use subagents only when the work is bounded and the parent can review the result.

## What This Repo Contains

- `skills/`: reusable coding-agent skills. Each skill has a `SKILL.md` with trigger, purpose, procedure, stop/ask conditions, and handoffs.
- `AGENTS.md`: a compact, copyable example agent guide for a programming repo.
- `scripts/validate-public-readiness.ps1`: a lightweight release check for this repo.
- `ACKNOWLEDGMENTS.md`: inspiration and no-affiliation notes.
- `LICENSE`: MIT license.

## Status

This is an experimental baseline, but it is not untested. These skills have been used across five programming repos and currently match the maintainer's preferred coding-agent workflow.

Future revisions are expected as real work exposes weak wording, missing checks, unclear handoffs, or unnecessary process.

## Maintainer Check

Before publishing or cutting a release, run:

```powershell
pwsh -File scripts/validate-public-readiness.ps1
```

This checks skill metadata and basic public-repo hygiene.

## License

MIT. See [LICENSE](LICENSE).
