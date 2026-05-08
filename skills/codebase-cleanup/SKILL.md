---
name: codebase-cleanup
description: Use when asked to clean up a repo, refactor safely, reduce duplicated code paths, simplify module boundaries or caller interfaces, make behavior easier to test, or remove code made obsolete by a change.
---

# Codebase Cleanup

Find behavior-preserving refactors that make future code changes cheaper, safer, and easier to verify without starting a rewrite.

## Rule

Cleanup is justified by repo evidence of maintenance cost, not taste. Preserve caller-visible behavior unless the user approved a behavior change.

A caller interface is everything a caller must know to use code correctly: inputs, outputs, invariants, ordering, state changes, error modes, configuration, and performance expectations. Do not judge it only by a function signature or type.

## Look For

- One behavior requires edits across many files, modules, commands, or tests.
- The same rule, validation, calculation, or branch condition exists in multiple code paths.
- Callers must know internal steps, ordering, config, state transitions, or error details.
- Domain logic is tangled with I/O, persistence, network calls, time, randomness, or state changes.
- Tests require excessive setup, private method access, or direct state/database inspection instead of a caller-facing entry point.
- The same domain concept, interface contract, or state transition has several names.
- State/data updates are split across scattered conditionals.
- Current work made code, imports, flags, config, docs, commands, or files obsolete.

## Process

1. Inspect repo instructions, the dirty tree, relevant source, tests, fixtures, recent diffs, and the caller path or module under cleanup.
2. Use docs, ADRs, and `CONTEXT.md` as maps, then confirm the current behavior in source and tests.
3. Separate cleanup from behavior change. If target behavior is unclear, use `clarify-scope`; if a bug appears, use `diagnose-loop`.
4. List candidates:

```text
Opportunity:
Repo evidence of cost:
Caller-visible behavior to preserve:
Current caller interface or contract:
Likely files/modules:
Baseline check:
Deletion test:
Smallest behavior-preserving slice:
Diff risk:
Verification:
Engineering return: high|medium|low
```

5. Recommend the highest-return, lowest-risk slice. If it needs multiple reviewable slices, hand off to `slice-plan`.
6. Establish a baseline with existing tests or a small repeatable check that captures current caller-visible behavior.
7. Refactor one narrow slice and keep the repo buildable or runnable after it lands.
8. Run focused and surrounding checks after the final edit, then inspect the diff for behavior preservation, scope control, user-change preservation, and reduced future change cost.

## Good Cleanup

- Consolidates a duplicated rule into one module, helper, or caller-facing path.
- Moves I/O, persistence, network calls, time, randomness, or other side effects to an outer layer or explicit dependency.
- Gives callers a simpler function, object, command, or module with clearer inputs, outputs, errors, and state changes.
- Makes behavior testable through the caller-facing interface instead of private methods or internal steps.
- Renames a concept to match shared domain or architecture language.
- Updates `CONTEXT.md` only when cleanup resolves recurring vocabulary, module-boundary, or public-contract confusion.
- Deletes code made obsolete by the current change.
- Removes a wrapper, helper, or option that adds no useful behavior.

## Bad Cleanup

- Rewrites a subsystem because it looks untidy.
- Creates an abstraction, interface, adapter, hook, or option with one real use and no actual caller variation to hide.
- Moves files without reducing coupling, simplifying a caller path, or improving a test surface.
- Changes behavior while calling it cleanup.
- Adds frameworks, dependencies, metadata machinery, or configuration systems.
- Mixes broad formatting churn with a functional or cleanup change.
- Deletes pre-existing dead code outside the requested area without approval.

## Stop Or Ask

- The cleanup requires a user/caller behavior, data, security, migration, dependency, or public contract decision.
- Current caller-visible behavior is important but cannot be checked cheaply.
- The smallest safe slice is still a broad rewrite.

## Handoff

- `slice-plan`: multi-slice cleanup.
- `tdd-slice`: behavior protection or approved behavior change.
- `diagnose-loop`: cleanup reveals a failing test, bug, regression, or unexplained symptom.
- `github-tracking`: cleanup should become issue or PR tracking.
- `workspace-safety`: before broad file moves, deletes, branch/worktree changes, dependency installs, generated output, or dirty-tree edits.
- `verify-before-done`: before claiming behavior was preserved or the cleanup is ready.
