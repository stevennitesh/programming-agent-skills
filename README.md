# Programming Agent Skills

Small, practical skills for coding agents that need to do real engineering work: understand the goal, stay scoped, use source evidence, protect the workspace, and verify before claiming success.

This repo is a skill pack, not a framework. Each skill is a compact procedure for a common programming situation: clarifying fuzzy work, planning a thin slice, changing behavior with checks, debugging from evidence, cleaning up code safely, tracking work in GitHub, coordinating subagents, and finishing with honest verification.

## Why This Exists

Coding agents often fail in predictable ways. They over-plan, overbuild, trust stale summaries, skip reproduction, edit before understanding the baseline, lose track of user changes, or report completion without fresh evidence.

These skills make the better path easier:

- Start from the real goal and the relevant source.
- Choose one useful workflow instead of every possible process.
- Prefer small, reviewable changes over broad rewrites.
- Use tests, commands, diffs, and observed behavior as evidence.
- Treat uncertainty, failures, and review comments as engineering signals.

## Why Consolidate These Ideas

I created this skill pack because I wanted one lean set of reusable workflows that combines a few useful pressures: Superpowers-style skill workflows, Matt Pocock's bias toward engineering discipline, and Karpathy's discussions of agent failure modes and the tradeoffs of coding with agents.

The goal is not to give agents a giant rulebook. It is to steer without over-constraining: enough guardrails to keep work grounded, scoped, and verified, while leaving room for exploration when the task calls for it and the user has not ruled it out.

## How To Use

Copy the skill folders you want into your local skill system, or point an agent at the `skills/` directory if your tooling supports repo-local skills.

For nontrivial work, start with `coding-router`. It chooses the controlling skill for the next move. Gate skills step in only when needed for workspace safety, GitHub tracking, subagents, or final verification.

For project-level instructions, copy `AGENTS.md` into your repo and adapt the source-of-truth files, commands, and constraints. `AGENTS.md` is a lightweight default operating guide; it does not replace these skills or the repo's own docs, tests, and review process.

## The Process

The skills are meant to work as a small routing system:

1. Start with the current request, repo instructions, source, docs, tests, and working tree.
2. Pick one controlling skill for the active problem.
3. Use the smallest loop that fits the risk.
4. Bring in gate skills only when the work reaches safety, tracking, delegation, or completion evidence.
5. Finish by checking the diff, running the relevant verification, and reporting remaining uncertainty.

Typical paths:

- Feature or behavior request: `coding-router` -> `clarify-scope` or `thin-plan` -> `tdd-slice` -> `verify-before-done`
- Bug or failing test: `coding-router` -> `diagnose-loop` -> focused fix and regression check -> `verify-before-done`
- Cleanup or refactor: `coding-router` -> `codebase-cleanup` -> behavior-preserving slice -> `verify-before-done`
- Multi-agent work: controlling skill -> `manage-subagents` for bounded packets -> parent review and verification

## Skill Map

Start and route:

- `coding-router`: choose the smallest reliable workflow for nontrivial coding, debugging, refactoring, cleanup, GitHub tracking, or skill-authoring work.

Shape the work:

- `clarify-scope`: turn fuzzy or product-facing requests into buildable behavior without over-interviewing.
- `thin-plan`: create compact multi-step plans with clear acceptance checks and reviewable slices.

Build or fix:

- `tdd-slice`: implement one behavior at a time with a focused check when practical.
- `diagnose-loop`: reproduce, minimize, hypothesize, fix, and regression-test bugs or failing workflows.

Improve structure:

- `codebase-cleanup`: find cleanup slices justified by current cost, while preserving behavior.

Coordinate work:

- `github-work-tracking`: use GitHub issues, PRDs, slice issues, and PRs when durable tracking is useful.
- `manage-subagents`: dispatch bounded exploration, implementation, or review work without giving away parent responsibility.

Protect and finish:

- `workspace-safety`: protect user changes, Git state, scratch space, branches, commits, and generated output.
- `verify-before-done`: inspect diffs and run fresh checks before claiming work is done, fixed, safe, passing, or ready.

Extend the skill pack:

- `author-skills`: create or revise skills from real failure modes, not one-off project notes.

## What This Is Not

- Not a package manager or runtime framework.
- Not a replacement for project docs, source code, tests, review, CI, or user instruction.
- Not a rule that every task needs ceremony. Tiny safe edits can use a tiny inspect-edit-check loop.
- Not a promise that process creates correctness. Evidence still has to come from the repo and the checks that matter.

## Principles

- Evidence over impressions.
- Source and tests over stale summaries.
- One controlling workflow at a time.
- Smallest useful slice before broad rewrites.
- Reproduce bugs before fixing them.
- Preserve existing behavior during refactors unless asked to change it.
- Protect user work and unrelated changes.
- Verify before completion claims.
- Use subagents only when the work is bounded and the parent can review the result.

## What This Repo Contains

- `skills/`: reusable agent skills. Each skill has a `SKILL.md` with trigger, purpose, procedure, stop conditions, and handoffs.
- `AGENTS.md`: a copyable example agent guide for a programming repo.
- `scripts/validate-public-readiness.ps1`: a lightweight release check for this repo.
- `ACKNOWLEDGMENTS.md`: inspiration and no-affiliation notes.
- `LICENSE`: MIT license.

## Status

This is an experimental baseline, but it is not untested. These skills have been used across five programming projects and currently match the maintainer's preferred agent workflow.

Future revisions are expected as real work exposes weak wording, missing checks, unclear handoffs, or unnecessary process.

## Maintainer Check

Before publishing or cutting a release, run:

```powershell
pwsh -File scripts/validate-public-readiness.ps1
```

This checks skill metadata and basic public-repo hygiene.

## License

MIT. See [LICENSE](LICENSE).
