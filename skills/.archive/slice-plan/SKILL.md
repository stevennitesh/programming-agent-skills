---
name: slice-plan
description: "Use when approved multi-step repo work truly needs a written execution plan or handoff with task boundaries, checks, execution mode, ownership scope, continuity, and final verification; skip tiny edits, one behavior, one bug, or issue-only/PR-only tracking."
---

# Slice Plan

Create a compact execution plan for coding agents. Plan enough to identify files, public or caller contracts, checks, and handoffs; not so much that the plan becomes a second implementation.

## Rule

Each task should be one reviewable source, test, or docs change with a pass/fail check, a clear file/module boundary, and a buildable or runnable repo after it lands.

Ownership scope means the files, modules, contracts, generated outputs, dependency/config state, or behavior a task, issue, or agent may change. It is task scope, not the same thing as GitHub assignee, repository owner, or long-term code ownership.

When approved multi-step repo work appears to need a written plan or handoff, first decide whether the plan is actually needed. Before writing tasks, account for the approved goal and non-goals, current repo evidence, public or caller contract, acceptance checks, execution mode, ownership scope, task continuity, verification commands, and the next handoff.

Do not turn a vague request into a broad task list. If target behavior, public or caller contract, ownership boundary, execution mode, or acceptance checks are unclear, resolve that with `clarify-scope`, `repo-onboarding`, or a focused source read before planning.

## Planning Depth

Scale the plan to the repo work:

- Tiny safe edit: no written plan; use the micro-loop from `coding-router`.
- One caller-visible behavior or one reproduced bug: skip the plan and use `tdd-slice` or `diagnose-loop`.
- Multi-step local repo work: write an inline plan with 2-5 tasks.
- Multi-session repo work, GitHub issues, subagent handoffs, or risky changes: use the full plan shape below.
- Unclear target: do not plan yet; use `clarify-scope`.
- If the only output needed is GitHub issues, PR tracking, or issue-by-issue execution with an explicit checkpoint policy, use `github-tracking` or `issue-driven-execution` after the source scope is clear.

## Fast Path

Use for 2-5 local steps.

- Write only Goal, Tasks/checks, Stop/ask, and Final verification.
- Keep each task tied to a source boundary and pass/fail check.
- Do not use the durable template unless work is multi-session, risky, GitHub-tracked, delegated, or likely to be resumed later.

## Inputs

Read only what is needed:

- Target evidence: approved request, design brief, issue, PRD, or review finding
- Repo evidence: instructions, source entry points/callers, tests/fixtures, logs, docs, diffs, working tree, and known commands
- `CONTEXT.md` only when shared terms, module boundaries, or public or caller contracts matter
- Related issue, PRD, PR, or acceptance criteria when present

Treat plans, summaries, memory, and prior issue comments as maps. Current behavior and source boundaries come from repo evidence: source, tests, fixtures, logs, commands, diffs, CI/check output, and live issue or PR state when relevant.

## Plan Shape

Inline plan:

```text
Goal:
Constraints/non-goals:
Evidence:
Tasks/checks:
Stop/ask:
Final verification:
```

Durable plan adds task continuity, risk/rollback, handoffs, and update policy:

```markdown
# Plan: <title>

## Goal

## Non-goals

## Constraints

## Execution mode
Execution mode: sequential | parallel-disjoint | parallel-overlap
Default if omitted: sequential

## Acceptance checks

## Plan evidence
- Source/docs/tests/fixtures inspected:
- Assumptions:
- Decisions still needed:

## Baseline
- Working tree:
- Current behavior or failing symptom:
- Relevant source/tests/fixtures:
- Baseline commands/checks:

## Tasks

### Task 1: <caller-visible behavior or repo change>
- Outcome:
- Builds on or must preserve:
- Public contract or state/data change:
- Depends on:
- Likely files/modules:
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

- Every task must trace to the approved request, public or caller contract, acceptance check, or named risk-reduction step.
- If the plan does not explicitly say `parallel-disjoint` or `parallel-overlap`, treat the work as `sequential`.
- Use parallel modes only when ownership, dependencies, worktree need, overlap, and integration strategy are explicit.
- If the plan will become GitHub issues or PR tracking, route metadata and issue-body fields through `github-tracking`; keep this plan focused on source scope, task boundaries, checks, continuity, and execution mode.
- Prefer end-to-end caller-visible slices over layer-only slices.
- Make the first task prove the chosen source route, test surface, or integration path when the implementation path is uncertain.
- Do not make each helper extraction its own task unless it creates a reviewable ownership boundary; a helper category is not enough. Prefer tasks that leave fewer, clearer modules rather than more precise but tedious files.
- When a task proposes new files, name why each file deserves independent ownership and what existing files, if any, should be consolidated instead.
- A good task delivers one API/CLI/UI behavior, one state/data change, one public or caller contract, one migration step, one bug reproduction plus fix, one focused fixture/check, or one behavior-preserving refactor.
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
- Do not create tasks from headings, file layers, or implementation guesses when the behavior, check, owner, and dependency are not known.

## Detail Level

- Include likely files/modules, commands, public or caller contracts, state/data touched, and acceptance checks when known.
- State uncertainty instead of pretending the plan knows details only source inspection or implementation will reveal.
- Do not include source code unless the exact API shape, CLI contract, schema, fixture, or test case is the task.
- Do not add speculative tasks to look complete.
- Avoid placeholders such as "TBD", "handle edge cases", "add validation", or "write tests" without the specific input, behavior, expected output, and check.

## During Execution

Treat the plan as a route, not authority. Start each task from the current source, tests, diffs, and completed issue comments, not from the original plan snapshot alone. Before editing, name the prior implementation path the task will reuse, extend, or preserve. If repo evidence, user instruction, or verification contradicts the plan, reroute through the controlling skill and update the plan or issue only for durable contract, scope, or acceptance-check changes.

Do not implement from a task title alone. Use the task body, accepted scope, current source, prior task result, public or caller contract, and verification command as the baseline.

## Plan Review

Before handing off, scan the plan for:

- acceptance checks and public or caller contracts mapped to tasks
- each task having a pass/fail check strong enough for the intended claim
- continuity between dependent tasks, or a reason they are independent
- explicit execution mode, with parallel ownership and integration details only when needed
- no vague placeholders such as "handle edge cases" without the exact input, behavior, expected output, and check
- consistent names for files, modules, commands, statuses, and domain terms
- no unrelated behavior changes, refactors, dependency changes, or generated output bundled into one task

## Stop Or Ask

- The user has not approved planning or the work is small enough for a micro-loop.
- Target behavior, public or caller contract, acceptance checks, or ownership scope is materially unclear after cheap evidence review.
- Repo instructions, commands, branch/worktree rules, generated-output policy, or safety constraints are unknown and matter to the plan.
- A task lacks a pass/fail check, source/test entry point, continuity context, or concrete review boundary.
- Parallel work is desired but ownership, worktree requirement, dependencies, overlap, integration owner, or comparison strategy is not explicit.
- The plan would invent GitHub metadata, issue readiness, labels, milestones, assignees, projects, or tracker conventions not supported by repo evidence.
- The plan would copy source code, line-number maps, stale file lists, or implementation details instead of durable contracts, boundaries, checks, and handoffs.
- Existing source, tests, fixtures, logs, docs, or live issue/PR state contradict the approved request or prior plan.

## Report

```text
Plan:
Plan type: none | inline | durable
Evidence:
Tasks/checks:
Blocked on:
Next route:
```

## Handoff

- `tdd-slice`: behavior-changing tasks.
- `codebase-cleanup`: cleanup discovery, explicit reviewability cleanup, or behavior-preserving refactor tasks with structure, caller-interface, testability, duplication, or obsolete-code risk.
- `diagnose-loop`: tasks that start from a failing test, bug, regression, log, or unexplained symptom.
- `issue-driven-execution`: the plan should become a plan doc, GitHub issues, issue-by-issue execution, and an explicit checkpoint policy.
- `github-tracking`: the plan should become issues, PR record updates, readiness/blocker comments, or recorded CI/review evidence.
- `subagent-workflow`: the user asked for subagents or independent coding/review work is genuinely useful.
- `workspace-safety`: before branch, worktree, commit, destructive, dependency install, generated-output, or overlapping dirty-path operations.
- `verify-before-done`: before claiming the plan, branch, PR, or implementation is complete.
