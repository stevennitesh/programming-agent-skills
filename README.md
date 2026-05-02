# Programming Agent Skills

Small, practical skills for steering coding agents toward grounded implementation, tight scope, and honest verification.

This repo is a small skill system, not a framework. It gives agents compact procedures for common programming work: clarifying scope, planning, test-first implementation, debugging, cleanup, workspace safety, GitHub tracking, subagent use, verification, and skill authoring.

## What This Repo Contains

- `skills/`: reusable agent skills. Each skill has a `SKILL.md` with trigger, purpose, procedure, stop conditions, and handoffs.
- `AGENTS.md`: a copyable example agent guide for a programming repo. Use it as a starting point for your own project-level agent instructions.
- `scripts/validate-public-readiness.ps1`: a lightweight release check for this repo.
- `ACKNOWLEDGMENTS.md`: inspiration and no-affiliation notes.
- `LICENSE`: MIT license.

## Status

This is an experimental baseline. The skills are meant to be revised as real work exposes weak wording, missing checks, unclear handoffs, or unnecessary process.

## How To Use

Copy the skill folders you want into your local skill system, or point an agent at the `skills/` directory if your tooling supports repo-local skills.

Use one controlling skill at a time:

1. Start with `coding-router` for nontrivial work.
2. Let it choose the smallest useful route.
3. Call gate skills only when the work reaches safety, delegation, tracking, or completion evidence.

For project-level instructions, copy `AGENTS.md` into your repo and adapt only the repo-specific parts. Keep it short. It should orient agents toward useful work, not become a second project spec.

## Skill Map

- `coding-router`: route nontrivial work to the smallest reliable skill path.
- `clarify-scope`: clarify fuzzy work without over-interviewing.
- `thin-plan`: create compact vertical-slice plans.
- `tdd-slice`: implement one behavior at a time with a failing check first.
- `diagnose-loop`: reproduce, minimize, hypothesize, fix, and regression-test bugs.
- `codebase-cleanup`: find high-value cleanup slices without broad rewrites.
- `github-work-tracking`: use GitHub issues, PRDs, slices, and PRs when durable tracking is useful.
- `manage-subagents`: control focused subagent use and review triage.
- `verify-before-done`: inspect diffs and run fresh checks before completion claims.
- `workspace-safety`: protect user changes, Git state, scratch space, branches, and commits.
- `author-skills`: create and revise skills from pressure-tested behavior.

## How The Skills Connect

- `coding-router` chooses the controlling skill for the next move.
- `clarify-scope` clarifies fuzzy targets, then hands to `thin-plan`, `tdd-slice`, `diagnose-loop`, or `github-work-tracking`.
- `thin-plan` slices approved work, then hands tasks to `tdd-slice`, `diagnose-loop`, `codebase-cleanup`, `github-work-tracking`, or `manage-subagents`.
- `workspace-safety`, `github-work-tracking`, `manage-subagents`, and `verify-before-done` are gates called when safety, durable tracking, delegation, or completion evidence is needed.

## Design Principles

- Prefer workflows that make correct, verified work easier than rushed, unverified work.
- Use only the context needed for the task.
- Treat docs, plans, summaries, and shared vocabulary as maps, not authority.
- Let source evidence and fresh verification decide whether work is correct.
- Prefer deletion, simplification, checklists, validators, and reusable procedures over new process.
- Use subagents only when bounded parallel work or independent review is worth the overhead.

## Public Readiness Check

Before publishing or cutting a release, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-public-readiness.ps1
```

The script checks skill metadata, stale source-corpus paths, obvious local identifiers, and Git history references to removed source material.

## License

MIT. See [LICENSE](LICENSE).
