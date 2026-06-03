---
name: codebase-cleanup
description: Use when asked to find cleanup opportunities, keep looping or cleaning until no useful cleanup remains, continue searching for cleanup work, organize code for human readability, clean up imports, add or remove comments, reorder methods or functions, refactor safely, reduce duplicated code paths, simplify module boundaries or caller interfaces, make behavior easier to test, or remove code made obsolete by a change.
---

# Codebase Cleanup

Find behavior-preserving refactors that make future code changes cheaper, safer, and easier to verify without starting a rewrite.

## Rule

Cleanup is justified by repo evidence of maintenance cost, not taste. Preserve caller-visible behavior unless the user approved a behavior change.

A caller interface is everything a caller must know to use code correctly: inputs, outputs, invariants, ordering, state changes, error modes, configuration, and performance expectations. Do not judge it only by a function signature or type.

## Human-Readable Organization Rule

Cleanup includes organizing the touched code so a maintainer can read the main behavior top-to-bottom without unnecessary jumping.

Prefer the repo's existing ordering convention. If none is clear, organize by reading path:

- Imports grouped and consolidated by repo or language convention before module code.
- Module constants, types, and config before behavior that uses them.
- Caller-facing entry points before implementation details.
- Orchestration, setup, validation, core behavior, side effects, and output in workflow order.
- Closely related helpers near their only caller, or grouped below the public path when reused.
- Class methods in a stable human order: construction/lifecycle, public methods, internal helpers.
- Tests grouped by behavior or scenario, with shared fixtures/builders before tests that use them.

Import cleanup is part of the organization pass. Remove unused imports introduced or made obsolete by the cleanup. Consolidate repeated imports from the same library, package, module, or helper when repo style and language semantics allow it. Do not merge imports that are intentionally separate for side effects, conditional loading, type-only/runtime separation, readability of large groups, or formatter/linter requirements.

Do not alphabetize, reshuffle, or split code mechanically. Reorder only when it reduces reader navigation cost, clarifies ownership, or makes a future change safer.

Use comments and docstrings to preserve knowledge that clearer code cannot carry cheaply: non-obvious invariants, ordering constraints, domain rules, side effects, error semantics, performance tradeoffs, compatibility expectations, or public or caller contracts.

Before adding a comment, first try clearer names, smaller local grouping, simpler control flow, or better ordering. Remove stale, misleading, duplicated, commented-out, or obvious comments. Do not repeat function names in prose or use comments to justify confusing structure that should be simplified.

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
- Multiple import lines pull from the same library, package, module, or helper without a repo-style or semantic reason to keep them separate.
- Important invariants, ordering constraints, domain rules, error semantics, or performance tradeoffs are only implicit in branch order, magic constants, fixtures, or call sites.
- Comments, docstrings, or commented-out code are stale, misleading, duplicated, noisy, or absent where they carry non-obvious caller or maintainer knowledge.
- Current work made code, imports, flags, config, docs, commands, or files obsolete.

## Opportunity Sweep

When the user asks to find cleanup opportunities, continue searching, keep looping, keep cleaning, keep working until nothing useful remains, or similar, the wording changes the done check: one good bundle is not completion, and endless churn is not success. First define the requested scope, decide whether it can be inspected honestly in one pass, and run a bounded sweep across independent evidence signals before selecting a bundle.

For "keep looping" or "until nothing useful remains" requests, the accepted scope is part of the task. If the request is repo-wide and too large to inspect honestly in one pass, propose a smaller bounded scope before changing files.

The smallest useful loop controls edit size and verification size, not discovery depth. Use broad inspection to find ordered bundles, then use narrow verified edits to land them.

- Caller-facing entry points and ownership boundaries.
- Duplicated rules, validation, calculations, names, or state transitions.
- Tests and fixtures that show setup friction, private access, repeated doubles, or weak caller-facing checks.
- Docs, commands, config, scripts, and generated artifacts that may be stale, scattered, or obsolete.
- Recent diffs, TODOs, deprecations, wrappers, options, or compatibility paths that may no longer earn their cost.
- Additional cheap signals for exhaustive cleanup: duplicate-rule scans, dead private helper scans, repeated import/source scans, stale comment scans, test-friction scans, and ownership-boundary reads.

Keep a short coverage ledger:

```text
Requested scope:
Inspected source areas:
Inspected tests/fixtures:
Searches or commands used:
Candidate bundles found:
Last cleanup signals checked:
Deferred or low-return areas:
Uninspected areas:
Why the sweep is sufficient for this pass:
```

After each cleanup bundle, update the coverage ledger, rerun relevant cleanup signals, and continue to the next high- or medium-return candidate. Passing tests for one bundle support behavior preservation; they do not prove the requested cleanup scope is exhausted.

Do not claim that no cleanup remains unless the coverage ledger shows the requested scope, inspected source and tests/fixtures, searches or commands used, last cleanup signals checked, remaining low-return/risky/out-of-scope/intentional candidates, and uninspected areas. Stop only when remaining candidates are low-value, risky, outside the requested scope, already intentional by repo evidence, or require a behavior, API, data, security, dependency, migration, or user decision. Prefer: "I found no higher-return opportunities in the inspected scope; remaining uninspected or lower-return areas are ..."

## Process

1. Inspect repo instructions, the dirty tree, relevant source, tests, fixtures, recent diffs, and the caller-facing entry point or module under cleanup.
2. Use docs, ADRs, and `CONTEXT.md` as maps, then confirm the current behavior in source and tests.
3. Separate cleanup from behavior change. If target behavior or the public or caller contract is unclear, use `clarify-scope`; if a bug appears, use `diagnose-loop`.
4. Group candidates into cleanup bundles by ownership boundary, public or caller contract, duplicated rule, test surface, or reason to change. Avoid unrelated grab bags:

```text
Bundle:
Why these changes belong together:
Repo evidence of cost:
Caller-visible behavior to preserve:
Current public or caller contract:
Interface depth:
Current reading/navigation problem:
Human-readable organization plan:
Import cleanup plan:
Comment/docstring plan:
Comments to remove or avoid:
Likely files/modules:
Candidate changes:
Consolidation option:
Navigation cost:
Would these files usually be opened together:
Why a new file is justified, if any:
Deletion test outcome:
Locality/leverage gained:
Test surface impact:
Domain term or ADR constraint:
Dependencies or ordering constraints:
What should not be included:
Baseline check:
Diff risk:
Verification:
Engineering return: high|medium|low
```

5. Recommend an ordered bundle plan, not only the single best opportunity. Order bundles by dependencies, behavior-preservation risk, validation confidence, and engineering return. Name the recommended first bundle and the next bundle to inspect or implement after it. Prefer consolidation, caller simplification, or an existing caller-facing test surface over new file boundaries unless the split has clear ownership value. If it needs multiple reviewable slices, hand off to `slice-plan`.
6. If the user asked to keep searching, keep looping, or clean until nothing useful remains, continue from the coverage ledger after each bundle: pick the next uninspected source area, deferred bucket, adjacent ownership boundary, or cleanup signal before concluding.
7. Establish a baseline with existing tests or a small repeatable check that captures current caller-visible behavior.
8. Refactor one narrow slice and keep the repo buildable or runnable after it lands.
9. Before final checks, do a human-readability pass on touched files: imports, method/function order, grouping, names, comments/docstrings, and stale comments. Keep the pass scoped to touched or directly related code.
10. Run focused and surrounding checks after the final edit, then inspect the diff for behavior preservation, scope control, user-change preservation, and reduced future change cost. For continued-cleanup requests, update the coverage ledger and either pick the next high- or medium-return bundle or state the concrete stop reason.

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
- Removes unused imports and consolidates repeated same-source imports when the repo style and language semantics support it.
- Orders functions and methods around the reader's path through the behavior rather than mechanical sorting.
- Improves names, ordering, or local structure so fewer comments are needed to understand normal control flow.
- Adds or updates a short comment or docstring for a non-obvious invariant, ordering constraint, domain rule, side effect, error mode, performance tradeoff, compatibility expectation, or public or caller contract.
- Removes stale, misleading, duplicated, noisy, or commented-out code.
- Strengthens an existing caller-facing test surface instead of adding private hooks or new test-only entry points.
- Renames a concept to match shared domain or architecture language.
- Updates `CONTEXT.md` only when cleanup resolves recurring vocabulary, module-boundary, or public or caller contract confusion.
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
- Leaves unused imports or repeated same-source imports in touched files after cleanup when no repo-style or semantic reason requires them.
- Alphabetizes, reshuffles, or splits methods and helpers without making the behavior easier to read or change.
- Mixes broad formatting churn with a functional or cleanup change.
- Treats one cleanup bundle, one passing check, or one quick scan as proof that a continued-cleanup scope is exhausted.
- Keeps cleaning after only low-value, risky, out-of-scope, or decision-blocked candidates remain.
- Starts file moves, abstraction work, deletes, or broad formatting before the source evidence, caller-visible behavior to preserve, and baseline check are known.
- Deletes pre-existing dead code outside the requested area without approval.

## Stop Or Ask

- The cleanup requires a user or caller behavior, data, security, migration, dependency, or public or caller contract decision.
- The cleanup has multiple plausible caller interfaces, test surfaces, or ownership boundaries and repo evidence does not clearly choose one.
- Current caller-visible behavior is important but cannot be checked cheaply.
- The smallest safe slice is still a broad rewrite.
- The user wants exhaustive repo-wide cleanup but the repo is too large to inspect honestly in one pass; propose a bounded sweep scope before editing, then report uninspected areas instead of implying the whole repo is clean.
- Continued cleanup has reached only low-value, risky, outside-scope, already intentional, or decision-blocked findings; report the ledger and stop reason instead of continuing churn.

## Report

For cleanup discovery or continued-cleanup work, report the requested scope, changed files or recommended bundles, checks run, coverage ledger summary, remaining candidates or uninspected areas, and the next bundle or concrete stop reason. Do not claim behavior was preserved or a cleanup scope is exhausted without `verify-before-done` evidence.

## Handoff

- `slice-plan`: multi-slice cleanup.
- `tdd-slice`: behavior protection or approved behavior change.
- `diagnose-loop`: cleanup reveals a failing test, bug, regression, or unexplained symptom.
- `github-tracking`: cleanup should become issue or PR tracking.
- `workspace-safety`: before broad file moves, deletes, branch/worktree changes, dependency installs, generated output, or dirty-tree edits.
- `verify-before-done`: before claiming behavior was preserved or the cleanup is ready.
