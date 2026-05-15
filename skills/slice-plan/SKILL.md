---
name: slice-plan
description: Use when approved repo work needs multiple source, test, or docs steps; multiple files; end-to-end behavior slices; coding-agent handoff; issue/PR tracking; or durable plan notes without copying source code into the plan.
---

# Slice Plan

Create a compact execution plan for coding agents. Plan enough to identify files, caller contracts, checks, and handoffs; not so much that the plan becomes a second implementation.

## Rule

Each task should be one reviewable source, test, or docs change with a pass/fail check, a clear file/module boundary, and a buildable or runnable repo after it lands.

## Planning Depth

Scale the plan to the repo work:

- Tiny safe edit: no written plan; use the micro-loop from `coding-router`.
- One caller-visible behavior or one reproduced bug: skip the plan and use `tdd-slice` or `diagnose-loop`.
- Multi-step local repo work: write an inline plan with 2-5 tasks.
- Multi-session repo work, GitHub issues, subagent handoffs, or risky changes: use the full plan shape below.
- Unclear target: do not plan yet; use `clarify-scope`.

## Inputs

Read only what is needed:

- Target evidence: approved request, design brief, issue, PRD, or review finding
- Repo evidence: instructions, source entry points/callers, tests/fixtures, logs, docs, diffs, working tree, and known commands
- `CONTEXT.md` only when shared terms, module boundaries, or public contracts matter
- Related issue, PRD, PR, or acceptance criteria when present

## Plan Shape

Use this template inline for short work or in the repo planning location for multi-session work:

```markdown
# Plan: <title>

## Goal

## Non-goals

## Constraints

## Execution mode
Execution mode: sequential | parallel-disjoint | parallel-overlap
Default if omitted: sequential
Parallel groups:
- None | <group-name>: issues, expected ownership, worktree requirement, integration owner

## GitHub metadata
Use only when durable issue coordination needs it:
- Relationships: dependencies, parent/child work, duplicates, or blockers
- Milestone: release, migration, version, or scheduled checkpoint
- Assignee/labels: multi-agent ownership, readiness, blocking state, issue type, or execution mode when repo convention supports it
- Project: repo/team project board already tracks this work
- Development: branch/PR link when implementation starts

## Acceptance checks

## Baseline
- Working tree:
- Current behavior or failing symptom:
- Relevant source/tests/fixtures:
- Baseline commands/checks:

## Tasks

### Task 1: <caller-visible behavior or repo change>
- Outcome:
- Builds on or must preserve:
- Existing logic to reuse or extend:
- Public contract or state/data change:
- Depends on:
- Likely files/modules:
- First command/check:
- Change boundary:
- Verification command:
- Review focus:
- Risk/rollback:
- Stop/ask if:
- Status: pending

## Final verification

## Open questions
```

## Slicing Rules

- Every task must trace to the approved request, public contract, acceptance check, or named risk-reduction step.
- If the plan does not explicitly say `parallel-disjoint` or `parallel-overlap`, treat the work as `sequential`.
- Use `parallel-disjoint` only when planned issue or subagent scopes can run at the same time with distinct source ownership and separate worktrees/branches.
- Use `parallel-overlap` only when parallel implementation intentionally touches the same files, modules, public contracts, generated output, or dependency/config state; name the integration owner and comparison strategy.
- Plan GitHub metadata only when it helps coordination or documentation; sequential single-agent issue work can stay body/comment only.
- Map dependencies to Relationships and release/version targets to Milestones when those fields exist in the repo workflow.
- Map multi-agent ownership, parallel mode, and worktree need to assignees or labels only when repo convention supports it.
- Prefer end-to-end caller-visible slices over layer-only slices.
- A good task delivers one API/CLI/UI behavior, one state/data change, one public contract, one migration step, one bug reproduction plus fix, one focused fixture/check, or one behavior-preserving refactor.
- For every task after the first, state the earlier task output, source path, helper, test, contract, or issue result it builds on or must preserve. If the task is independent, say why.
- Later tasks must extend, reuse, or refactor the established implementation path instead of creating a parallel path for the same behavior. If source evidence shows the earlier path is wrong, reroute and update the plan before coding the new path.
- Each task needs a pass/fail command, test, fixture, or repeatable manual check.
- For validation or testing plans, each task must state the evidence type it will produce and what weaker evidence does not satisfy the intent.
- Merge tasks that cannot be reviewed independently.
- Split tasks that require unrelated files or decisions.
- Keep related tests or checks in the same task as the behavior they protect.
- Leave the repo buildable, runnable, or explicitly no worse after each task.
- Include exact commands when known.
- Use shared vocabulary from `CONTEXT.md`, but never let it override the approved request, source, tests, fixtures, or logs.
- If planning reveals a recurring term, boundary, contract, or state transition, hand back to `clarify-scope` or add a tiny `CONTEXT.md` note before slicing.

## Detail Level

- Include likely files/modules, commands, public contracts, state/data touched, and acceptance checks when known.
- State uncertainty instead of pretending the plan knows details only source inspection or implementation will reveal.
- Do not include source code unless the exact API shape, CLI contract, schema, fixture, or test case is the task.
- Do not add speculative tasks to look complete.
- Avoid placeholders such as "TBD", "handle edge cases", "add validation", or "write tests" without the specific input, behavior, expected output, and check.

## During Execution

Treat the plan as a route, not authority. Start each task from the current source, tests, diffs, and completed issue comments, not from the original plan snapshot alone. Before editing, name the prior implementation path the task will reuse, extend, or preserve. If repo evidence, user instruction, or verification contradicts the plan, reroute through the controlling skill and update the plan or issue only for durable contract, scope, or acceptance-check changes.

## Plan Review

Before handing off, scan the plan:

- Coverage: every acceptance check and public contract maps to at least one task.
- Evidence fit: each validation claim maps to a command, test, fixture, diff review, or manual check strong enough for the claim; simulated or review-only checks are not allowed to satisfy behavior-test intent.
- Execution fit: mode is explicit or safely defaults to `sequential`; parallel modes name dependencies, file/module ownership, worktree need, and integration risk.
- Continuity fit: each later task names the prior output, source path, helper, test, contract, or issue result it builds on or explains why it is independent.
- Placeholder scan: no vague work items such as "handle edge cases" without the exact input, behavior, expected output, and check.
- Name consistency: files, modules, types, functions, commands, events, statuses, and domain terms are named the same way across tasks.
- Scope fit: tasks do not mix unrelated files, behavior changes, refactors, dependency changes, or generated output.

## Handoff

- `tdd-slice`: behavior-changing tasks.
- `codebase-cleanup`: behavior-preserving refactor tasks.
- `diagnose-loop`: tasks that start from a failing test, bug, regression, log, or unexplained symptom.
- `issue-driven-execution`: the plan should become a plan doc, GitHub issues, and issue-by-issue execution.
- `github-tracking`: the plan should become issues, PR notes, CI/check evidence, or durable GitHub records.
- `subagent-workflow`: the user asked for subagents or independent coding/review work is genuinely useful.
- `workspace-safety`: before branch, worktree, commit, destructive, dependency install, generated-output, or dirty-tree operations.
- `verify-before-done`: before claiming the plan, branch, PR, or implementation is complete.
