# Example AGENTS.md For Programming Repos

This file is a reusable starting point for project-level agent instructions. Copy it into a repo, then adjust the source-of-truth files, commands, and project-specific constraints.

The goal is practical steering: help agents get grounded, choose a small useful path, protect existing work, and prove claims with evidence.

## Core Guidance

- Prefer workflows that make correct, verified work easier than rushed, unverified work.
- Optimize for working software, clear reasoning, and low process overhead.
- Prefer compact procedures, checklists, validators, and examples over broad frameworks.
- Delete, simplify, or merge before adding new abstractions, tools, or instructions.

## Grounding

- Current user instruction is the highest authority for the current task.
- Project docs, specs, issues, and plans describe intent. Use them to route work, then verify against the relevant source and checks.
- Current code and tests describe the existing baseline. For refactors, treat them as compatibility evidence, not necessarily the target design.
- Generated summaries, plans, and notes are maps, not authority. Do not let them override source evidence, tests, or explicit user direction.
- If a new term, boundary, or project-specific meaning becomes important, record it in the project’s durable context or glossary location.

## Operating Loop

Use the smallest loop that fits the risk:

1. Goal: what outcome must exist when done?
2. Assumptions: what are you relying on, and what could be wrong?
3. Approach: what is the smallest useful slice?
4. Output: what changed or what answer was produced?
5. Checks: what evidence supports the result?
6. Risks: what remains uncertain?
7. Next action: what should happen next, if anything?

For bugs or regressions:

1. Baseline: reproduce or observe the failure.
2. Hypothesis: identify the likely cause.
3. Change: make the smallest targeted fix.
4. Validation: rerun the failure path and relevant regression checks.
5. Decision: keep, retest, or discard the change.

## Scope Control

- Answer the real job, not only the literal wording.
- Ask only when missing information changes correctness, scope, reversibility, security, data integrity, cost, or user-visible behavior.
- If evidence in the repo can answer the question cheaply, inspect before asking.
- Prefer narrow, reversible slices over broad rewrites.
- Push back when the request is optimizing the wrong thing, skipping validation, or adding unnecessary process.

## Implementation

- Follow the repo’s existing patterns before inventing new ones.
- Keep edits close to the files and behavior implied by the task.
- Add abstractions only when they remove real complexity, reduce meaningful duplication, or match an established local pattern.
- For behavior changes, add or update a focused check when practical.
- For refactors, preserve behavior first; change behavior only when explicitly requested.
- Convert niche or project-local wording into clear programming language in public docs and reusable instructions.

## Verification

- Do not claim work is done, fixed, safe, passing, or ready without fresh evidence.
- Run the most relevant check that fits the risk and explain what it proves.
- If only a shallow check is practical, say what it does and does not prove.
- Inspect diffs before final reporting.
- Treat review comments, CI failures, and test failures as engineering signals, not paperwork.

## Workspace Safety

- Inspect `git status --short --branch` before risky edits, commits, branch changes, or cleanup.
- Preserve user changes and unrelated work. Do not revert changes you did not make unless explicitly asked.
- Keep scratch files, caches, logs, generated experiments, and local-only data out of tracked files.
- Do not run destructive Git or filesystem commands unless the user explicitly asks or approves.
- Stage intentionally. Commit only the files that belong to the requested checkpoint.

## Subagents And Tools

- Use subagents only for bounded work: independent exploration, one clear implementation slice, or independent review.
- Give subagents exact scope, allowed files, forbidden scope, expected output, and required evidence.
- Keep overlapping edits parent-owned or sequential.
- The parent agent owns integration, review triage, and final verification.
- Prefer deterministic tools and repo-native commands over manual reconstruction when they are available.

## Reporting

For nontrivial work, finish with:

- What changed.
- What evidence supports it.
- What remains uncertain.
- The next useful action.

Keep reports concise. Do not bury the result in process narration.
