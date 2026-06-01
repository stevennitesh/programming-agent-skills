---
name: codebase-cleanup
description: Use when asked to clean up a repo, organize or comment code, refactor safely, reduce duplicated code paths, simplify module boundaries or caller interfaces, make behavior easier to test, or remove code made obsolete by a change.
---

# Codebase Cleanup

Find behavior-preserving refactors that make future code changes cheaper, safer, and easier to verify without starting a rewrite.

## Rule

Cleanup is justified by repo evidence of maintenance cost, not taste. Preserve caller-visible behavior unless the user approved a behavior change.

A caller interface is everything a caller must know to use code correctly: inputs, outputs, invariants, ordering, state changes, error modes, configuration, and performance expectations. Do not judge it only by a function signature or type.

## Readability And Comments Rule

When cleanup touches code, do a readability pass on the changed area. Prefer clearer names, ordering, grouping, and simpler control flow before adding comments.

Use comments and docstrings to preserve knowledge that clearer code cannot carry cheaply: non-obvious invariants, ordering constraints, domain rules, side effects, error semantics, performance tradeoffs, compatibility expectations, or caller contracts. Remove stale, misleading, duplicated, or commented-out code. Do not narrate obvious statements, repeat function names in prose, or use comments to justify confusing structure that should be simplified.

## Module Boundary Rule

Do not optimize for small files. Optimize for clear ownership and low caller/navigation cost.

Prefer an ownership module that is 150-300 cohesive lines over several tiny files that must be opened together to understand one behavior. Split a file only when the new boundary reduces coupling, hides a real implementation detail from callers, improves testability through a clearer public path, or separates distinct reasons to change.

Before creating a new file, ask:

- What caller or maintainer no longer needs to know this detail?
- What future change becomes easier or safer?
- Would the old and new files usually be opened together?
- Is this a real ownership boundary, or just a helper category?

If files would usually be edited, reviewed, or understood together, consolidate them. Use an ownership boundary, not a helper category.

## Depth And Locality Rule

Good cleanup makes modules deeper: callers learn less while the module does more useful work behind a clearer interface. Prefer changes that increase leverage for callers and locality for maintainers, so a future behavior change touches fewer files, callers, and tests.

Use the deletion test on wrappers, helpers, adapters, and ownership modules: if deleting it just removes indirection, it was likely pass-through cost; if deleting it would scatter rules, ordering, state, or error handling back across callers, it is earning its boundary.

## Look For

- One behavior requires edits across many files, modules, commands, or tests.
- The same rule, validation, calculation, or branch condition exists in multiple code paths.
- Callers must know internal steps, ordering, config, state transitions, or error details.
- The interface is nearly as complex as the implementation it hides.
- Domain logic is tangled with I/O, persistence, network calls, time, randomness, or state changes.
- Tests require excessive setup, private method access, or direct state/database inspection instead of a caller-facing entry point.
- Pure helpers exist only to make tests easy while real behavior, ordering, or state changes stay scattered.
- The same domain concept, interface contract, or state transition has several names.
- State/data updates are split across scattered conditionals.
- Related setup, validation, transformation, side effects, or output steps are interleaved in a way that hides the behavior.
- Important invariants, ordering constraints, domain rules, error semantics, or performance tradeoffs are only implicit in branch order, magic constants, fixtures, or call sites.
- Comments, docstrings, or commented-out code are stale, misleading, duplicated, noisy, or absent where they carry non-obvious caller or maintainer knowledge.
- Current work made code, imports, flags, config, docs, commands, or files obsolete.

## Process

1. Inspect repo instructions, the dirty tree, relevant source, tests, fixtures, recent diffs, and the caller-facing entry point or module under cleanup.
2. Use docs, ADRs, and `CONTEXT.md` as maps, then confirm the current behavior in source and tests.
3. Separate cleanup from behavior change. If target behavior is unclear, use `clarify-scope`; if a bug appears, use `diagnose-loop`.
4. List candidates:

```text
Opportunity:
Repo evidence of cost:
Caller-visible behavior to preserve:
Current caller interface or contract:
Interface depth:
Code organization/readability issue:
Comment/docstring need:
Likely files/modules:
Consolidation option:
Navigation cost:
Would these files usually be opened together:
Why a new file is justified, if any:
Deletion test outcome:
Locality/leverage gained:
Test surface impact:
Domain term or ADR constraint:
Baseline check:
Smallest behavior-preserving slice:
Diff risk:
Verification:
Engineering return: high|medium|low
```

5. Recommend the highest-return, lowest-risk slice. Prefer consolidation, caller simplification, or an existing caller-facing test surface over new file boundaries unless the split has clear ownership value. If it needs multiple reviewable slices, hand off to `slice-plan`.
6. Establish a baseline with existing tests or a small repeatable check that captures current caller-visible behavior.
7. Refactor one narrow slice and keep the repo buildable or runnable after it lands.
8. Run focused and surrounding checks after the final edit, then inspect the diff for behavior preservation, scope control, user-change preservation, and reduced future change cost.

## Good Cleanup

- Consolidates a duplicated rule into one module, helper, or caller-facing path.
- Consolidates small helper modules into a clearer ownership module when separation creates navigation tax without reducing coupling.
- Keeps related types, adapters, and dispatch logic together when callers must understand them as one behavior.
- Uses file boundaries for ownership and reasons to change, not for every helper type or implementation step.
- Deepens a module by giving callers a smaller, clearer interface while hiding more useful implementation detail behind it.
- Improves locality so a future change to one behavior touches fewer files, callers, tests, and state paths.
- Moves I/O, persistence, network calls, time, randomness, or other side effects to an outer layer or explicit dependency.
- Gives callers a simpler function, object, command, or module with clearer inputs, outputs, errors, and state changes.
- Groups related code inside the right ownership boundary so setup, validation, core behavior, side effects, and output are easier to scan.
- Improves names, ordering, or local structure so fewer comments are needed to understand normal control flow.
- Adds or updates a short comment or docstring for a non-obvious invariant, ordering constraint, domain rule, side effect, error mode, performance tradeoff, compatibility expectation, or caller contract.
- Removes stale, misleading, duplicated, noisy, or commented-out code.
- Strengthens an existing caller-facing test surface instead of adding private hooks or new test-only entry points.
- Renames a concept to match shared domain or architecture language.
- Updates `CONTEXT.md` only when cleanup resolves recurring vocabulary, module-boundary, or public-contract confusion.
- Deletes code made obsolete by the current change.
- Removes a wrapper, helper, or option that adds no useful behavior.

## Bad Cleanup

- Rewrites a subsystem because it looks untidy.
- Creates one-file-per-helper, one-file-per-type, or one-file-per-step modules when the files are normally read or changed together.
- Adds a shallow pass-through wrapper whose interface is nearly as complex as the implementation.
- Creates an abstraction, interface, adapter, hook, or option with one real use and no actual caller variation to hide.
- Creates a protocol, registry, or adapter with one production adapter and no real variation.
- Splits a cohesive 150-300 line module into several tiny modules without simplifying caller behavior.
- Hides simple control flow behind extra modules, registries, protocols, or adapters that have only one production use.
- Extracts a pure helper only to simplify a private test while the real behavior remains scattered or hard to verify through a caller-facing entry point.
- Moves files without reducing coupling, simplifying a caller-facing entry point, or improving a test surface.
- Changes an interface shape but leaves callers needing the same implementation knowledge as before.
- Changes behavior while calling it cleanup.
- Adds frameworks, dependencies, metadata machinery, or configuration systems.
- Adds comments that restate obvious code, type names, function names, assignments, or simple control flow.
- Uses comments to explain confusing code that should instead be renamed, regrouped, simplified, or moved behind a clearer interface.
- Reorders, renames, or reformats broad areas for style without reducing caller knowledge, navigation cost, or maintenance risk.
- Mixes broad formatting churn with a functional or cleanup change.
- Deletes pre-existing dead code outside the requested area without approval.

## Stop Or Ask

- The cleanup requires a user or caller behavior, data, security, migration, dependency, or public contract decision.
- The cleanup has multiple plausible caller interfaces, test surfaces, or ownership boundaries and repo evidence does not clearly choose one.
- Current caller-visible behavior is important but cannot be checked cheaply.
- The smallest safe slice is still a broad rewrite.

## Handoff

- `slice-plan`: multi-slice cleanup.
- `tdd-slice`: behavior protection or approved behavior change.
- `diagnose-loop`: cleanup reveals a failing test, bug, regression, or unexplained symptom.
- `github-tracking`: cleanup should become issue or PR tracking.
- `workspace-safety`: before broad file moves, deletes, branch/worktree changes, dependency installs, generated output, or dirty-tree edits.
- `verify-before-done`: before claiming behavior was preserved or the cleanup is ready.
