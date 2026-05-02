---
name: thin-plan
description: Use when approved coding work needs multiple steps, multiple files, end-to-end slices, handoff, issue tracking, or progress notes without copying implementation into the plan.
---

# Thin Plan

Create a compact executable plan. Plan enough for a fresh agent to start, not so much that the plan becomes a second implementation.

## Rule

Each task should be one reviewable change with a pass/fail check, a clear boundary, and a working repo after it lands.

## Planning Depth

Scale the plan to the work:

- Tiny safe edit: no written plan; use the micro-loop from `coding-router`.
- One behavior or one reproduced bug: skip the plan and use `tdd-slice` or `diagnose-loop`.
- Multi-step local work: write an inline plan with 2-5 tasks.
- Multi-session work, GitHub issues, subagents, or risky changes: use the full plan shape below.
- Unclear target: do not plan yet; use `clarify-scope`.

## Inputs

Read only what is needed:

- Approved request or design brief
- Repo instructions
- `CONTEXT.md` when it exists, for shared terms and boundaries
- Relevant source and tests
- Current working tree state
- Known verification commands
- Related issue, PRD, or acceptance criteria when present

## Plan Shape

Use this template inline for short work or in the repo planning location for multi-session work:

```markdown
# Plan: <title>

## Goal

## Non-goals

## Constraints

## Acceptance checks

## Baseline
- Working tree:
- Relevant tests/checks:
- Commands:

## Tasks

### Task 1: <observable behavior>
- Outcome:
- Depends on:
- Likely files:
- First check:
- Change boundary:
- Verification:
- Review focus:
- Risk/rollback:
- Stop/ask if:
- Status: pending

## Final verification

## Open questions
```

## Slicing Rules

- Every task must trace to the approved request, an acceptance check, or a named risk-reduction step.
- Prefer end-to-end behavior slices over layer-only slices.
- A good task delivers one visible behavior, one state change, one API contract, one migration step, one bug reproduction plus fix, or one safe refactor.
- Each task needs a pass/fail check.
- For validation or testing plans, each task must state the evidence level it will produce and what weaker evidence does not satisfy the intent.
- Merge tasks that cannot be reviewed independently.
- Split tasks that require unrelated files or decisions.
- Keep related tests or checks in the same task as the behavior they protect.
- Leave the repo buildable, runnable, or explicitly no worse after each task.
- Include exact commands when known.
- Use shared vocabulary from `CONTEXT.md`, but do not let it override the approved request, source, or tests.
- If planning reveals a new recurring term or boundary, hand back to `clarify-scope` or add a small `CONTEXT.md` note before slicing.

## Detail Level

- Include likely files, commands, interfaces, and acceptance checks when known.
- State uncertainty instead of pretending the plan knows details only implementation will reveal.
- Do not include private implementation code unless the exact contract is the task.
- Do not add speculative tasks to look complete.
- Avoid placeholders such as "TBD", "handle edge cases", "add validation", or "write tests" without the specific behavior and check.

## During Execution

Treat the plan as a route, not authority. If source evidence, user instruction, or verification contradicts it, reroute through the controlling skill and record only durable changes.

## Plan Review

Before handing off, scan the plan:

- Coverage: every acceptance check maps to at least one task.
- Evidence fit: each validation claim maps to evidence strong enough for the claim, and simulated or review-only checks are not allowed to satisfy behavior-test intent.
- Placeholder scan: no vague work items such as "handle edge cases" without the exact behavior and check.
- Name consistency: types, functions, commands, and terms are named the same way across tasks.

## Handoff

Use `tdd-slice` for behavior-changing tasks. Use `codebase-cleanup` for refactor-only tasks. Use `diagnose-loop` for tasks that start from a failing or unexplained symptom. Use `github-work-tracking` when the plan should become issues. Use `manage-subagents` only when the user asked for subagents or independent work/review is genuinely useful. Use `workspace-safety` before branch, worktree, commit, destructive, or dirty-tree operations. Use `verify-before-done` before claiming the plan, branch, PR, or implementation is complete.
