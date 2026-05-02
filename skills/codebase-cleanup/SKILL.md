---
name: codebase-cleanup
description: Use when asked to clean up a repo, improve architecture, refactor safely, reduce duplication, simplify module boundaries, make code easier to change, or make behavior easier to test.
---

# Codebase Cleanup

Find cleanup that makes future changes cheaper without changing behavior or starting a rewrite.

## Rule

Cleanup is justified by evidence of current cost, not taste. Preserve observable behavior unless the user approved a behavior change.

An interface is everything a caller must know to use code correctly: inputs, outputs, invariants, ordering, error modes, configuration, and performance expectations. Do not judge it only by a function signature or type.

## Look For

- One behavior requires edits in many places.
- The same rule, validation, or calculation exists in multiple places.
- Callers must know internal steps, ordering, config, or error details.
- Pure logic and I/O or state changes are tangled together.
- Tests require excessive setup or inspect internal details.
- The same concept has several names.
- State changes are split across scattered conditionals.
- Current work made code, imports, flags, or files obsolete.

## Process

1. Inspect repo instructions, the dirty tree, relevant tests, and the area of concern.
2. Use docs and `CONTEXT.md` as maps, then confirm the current source path.
3. Separate cleanup from behavior change. If target behavior is unclear, use `clarify-scope`; if a bug appears, use `diagnose-loop`.
4. List candidates:

```text
Opportunity:
Evidence of cost:
Behavior to preserve:
Caller interface:
Deletion test:
Smallest safe slice:
First check:
Risk:
Return: high|medium|low
```

5. Recommend the highest-return, lowest-risk slice. If it needs multiple slices, hand off to `thin-plan`.
6. Protect behavior first with existing tests or a small repeatable check that captures current behavior.
7. Refactor one narrow slice and keep the repo buildable or runnable after it lands.
8. Run focused and surrounding checks, then inspect the diff for behavior preservation and reduced future change cost.

## Good Cleanup

- Consolidates a duplicated rule into one home.
- Moves a side effect to an outer layer or explicit dependency.
- Gives callers a simpler function, object, command, or module to use.
- Makes behavior testable through the caller-facing interface instead of internal steps.
- Renames a concept to match shared domain language.
- Updates `CONTEXT.md` when cleanup resolves recurring vocabulary or boundary confusion.
- Deletes code made obsolete by the current change.
- Removes a wrapper, helper, or option that adds no useful behavior.

## Bad Cleanup

- Rewrites a subsystem because it looks untidy.
- Creates an abstraction, interface, adapter, hook, or option with one real use and no actual variation to hide.
- Moves files without reducing coupling.
- Changes behavior while calling it cleanup.
- Adds frameworks or metadata machinery.
- Mixes broad formatting churn with a functional or cleanup change.
- Deletes pre-existing dead code outside the requested area without approval.

## Stop Or Ask

- The cleanup requires a product, data, security, migration, or public interface decision.
- Current behavior is important but cannot be checked cheaply.
- The smallest safe slice is still a broad rewrite.

## Handoff

Use `thin-plan` for multi-slice cleanup. Use `tdd-slice` for behavior protection or approved behavior change. Use `diagnose-loop` when cleanup reveals a failing or unexplained symptom. Use `github-work-tracking` when cleanup should become durable issues. Use `workspace-safety` before broad file moves, deletes, branch/worktree changes, or dirty-tree edits. Use `verify-before-done` before claiming behavior was preserved or the cleanup is ready.
