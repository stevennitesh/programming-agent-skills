---
name: codebase-cleanup
description: "Use when the user asks for cleanup beyond incidental touched-file polish: explicit human-reviewability cleanup for comments/docstrings/imports/code order, cleanup discovery, continued cleanup loops, behavior-preserving refactors with structure risk, duplicated logic, module-boundary or caller-interface simplification, testability blockers, or obsolete-code removal."
---

# Codebase Cleanup

Make requested code easier for humans to review, or find behavior-preserving refactors that make future changes cheaper, safer, and easier to verify without starting a rewrite.

## Rule

Cleanup is justified by explicit user-requested human-reviewability cleanup or by repo evidence of maintenance cost. Preserve caller-visible behavior unless the user approved a behavior change.

A caller interface is everything a caller must know to use code correctly: inputs, outputs, invariants, ordering, state changes, error modes, configuration, and performance expectations. Do not judge it only by a function signature or type.

First visible move:

```text
Scope:
Cleanup lane: human-reviewability | refactor | discovery | continued cleanup
Behavior to preserve:
Reason/evidence:
Route: fast cleanup | discovery path | detailed process
Check:
```

## Human Reviewability Rule

When the user asks for comment, docstring, import, ordering, or readability cleanup, make the requested script or code easier for a human to review without changing behavior. Keep it scoped to the requested files or already-touched code unless the user asks for a broader sweep.

Prefer the repo's existing ordering convention. If none is clear, organize by the reader's path:

- Imports grouped and consolidated by repo or language convention before module code.
- Module constants, types, and config before behavior that uses them.
- Caller-facing entry points before implementation details.
- Orchestration, setup, validation, core behavior, side effects, and output in workflow order.
- Closely related helpers near their only caller, or grouped below the public path when reused.
- Class methods in a stable human order: construction/lifecycle, public methods, internal helpers.
- Tests grouped by behavior or scenario, with shared fixtures/builders before tests that use them.

For import cleanup, remove unused imports introduced or made obsolete by the cleanup. Consolidate repeated imports from the same library, package, module, or helper when repo style and language semantics allow it. Do not merge imports that are intentionally separate for side effects, conditional loading, type-only/runtime separation, readability of large groups, or formatter/linter requirements.

Do not alphabetize, reshuffle, or split code mechanically. Reorder only when it reduces reader navigation cost, clarifies ownership, or makes a future change safer.

For comment or docstring cleanup, preserve knowledge that clearer code cannot carry cheaply: non-obvious invariants, ordering constraints, domain rules, side effects, error semantics, performance tradeoffs, compatibility expectations, or public or caller contracts.

Before adding a comment, first try clearer names, smaller local grouping, simpler control flow, or better ordering. Remove stale, misleading, duplicated, commented-out, or obvious comments. Do not repeat function names in prose or use comments to justify confusing structure that should be simplified. Do not use reviewability cleanup as permission to sweep unrelated files.

## Module Boundary Rule

Do not optimize for small files. Optimize for clear ownership and low caller/navigation cost.

As a heuristic, prefer one cohesive ownership module over several tiny files that must be opened together to understand one behavior. Do not split or merge files to hit a size target. Split a file only when the new boundary reduces coupling, hides a real implementation detail from callers, improves testability through a clearer public path, or separates distinct reasons to change.

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
- When import or reviewability cleanup is requested, multiple import lines pull from the same library, package, module, or helper without a repo-style or semantic reason to keep them separate.
- Important invariants, ordering constraints, domain rules, error semantics, or performance tradeoffs are only implicit in branch order, magic constants, fixtures, or call sites.
- When comment, docstring, or reviewability cleanup is requested, comments, docstrings, or commented-out code are stale, misleading, duplicated, noisy, or absent where they carry non-obvious caller or maintainer knowledge.
- Current work made code, imports, flags, config, docs, commands, or files obsolete.

## Fast Cleanup Path

Use for one narrow reviewability-cleanup or behavior-preserving refactor slice when this skill is already warranted.

Incidental tiny touched-file import, comment, ordering, or readability fixes stay in the default micro-loop. Use this skill when the user explicitly asks for that cleanup, asks for a cleanup workflow, the change is part of a behavior-preserving refactor, or the cleanup expands into structure, caller-interface, testability, duplication, or obsolete-code risk.

- Name the touched scope, cleanup lane, behavior to preserve, reason/evidence, and check.
- Inspect the relevant source, nearby tests or fixtures, and current diff if one exists.
- Establish the cheapest useful check before changing behavior-sensitive code; for pure human-reviewability cleanup, use the smallest syntax, lint, format, diff, or focused command that fits the files.
- Make one narrow reviewability cleanup or behavior-preserving refactor slice.
- Run the same focused check after the edit.
- Inspect the diff for behavior preservation, scope control, reduced future change cost, and requested human-reviewability cleanup.

Do not build a coverage note for ordinary narrow cleanup. If the cleanup expands into multiple ownership boundaries, repeated candidates, broad file movement, or "keep cleaning" scope, switch to the Discovery Path.

## Discovery Path

Use this path when the user asks to find cleanup opportunities, the cleanup has multiple candidate bundles, or the request says to continue searching, keep looping, keep cleaning, keep working until nothing useful remains, or similar. First define the requested scope, decide whether it can be inspected honestly in one pass, and run a bounded sweep across independent evidence signals before selecting a bundle.

For "keep looping" or "until nothing useful remains" requests, the accepted scope is part of the task. If the request is repo-wide and too large to inspect honestly in one pass, propose a smaller bounded scope before changing files.

The smallest useful loop controls edit size and verification size, not discovery depth. Use broad inspection to find ordered bundles, then use narrow verified edits to land them.

- Caller-facing entry points and ownership boundaries.
- Duplicated rules, validation, calculations, names, or state transitions.
- Tests and fixtures that show setup friction, private access, repeated doubles, or weak caller-facing checks.
- Docs, commands, config, scripts, and generated artifacts that may be stale, scattered, or obsolete.
- Recent diffs, TODOs, deprecations, wrappers, options, or compatibility paths that may no longer earn their cost.
- Additional cheap signals for exhaustive cleanup: duplicate-rule scans, dead private helper scans, repeated import/source scans, stale comment scans, test-friction scans, and ownership-boundary reads.

Use a coverage note only for continued cleanup, exhaustive search, "nothing useful remains" claims, or discovery broad enough that the inspected scope could be overclaimed:

```text
Requested scope:
Inspected areas/signals:
Candidate bundles found:
Deferred or low-return areas:
Uninspected areas:
Why the sweep is sufficient for this pass:
```

For continued or exhaustive cleanup, update the coverage note after each bundle, recheck the relevant signals, and continue to the next high- or medium-return candidate. For ordinary discovery, report the candidate bundles and recommended first slice without implying the cleanup scope is exhausted.

Do not claim that no cleanup remains unless the coverage note names the requested scope, inspected areas and signals, remaining low-return/risky/out-of-scope/intentional candidates, and uninspected areas. Stop only when remaining candidates are low-value, risky, outside the requested scope, already intentional by repo evidence, or require a behavior, API, data, security, dependency, migration, or user decision. Prefer: "I found no higher-return opportunities in the inspected scope; remaining uninspected or lower-return areas are ..."

## Detailed Process

Use this when the Fast Cleanup Path is not enough: discovery, continued cleanup, multi-bundle cleanup, or behavior-preserving refactors with structure, caller-interface, testability, duplication, or obsolete-code risk. For narrow human-reviewability cleanup, stay in the Fast Cleanup Path and stop after the lane-appropriate check and diff inspection.

1. Inspect repo instructions, relevant workspace state, relevant source, tests, fixtures, recent diffs, and the caller-facing entry point or module under cleanup.
2. Use docs, ADRs, and `CONTEXT.md` as maps, then confirm the current behavior in source and tests.
3. Separate cleanup from behavior change. If target behavior or the public or caller contract is unclear, use `clarify-scope`; if a bug appears, use `diagnose-loop`.
4. Group candidates into cleanup bundles by ownership boundary, public or caller contract, duplicated rule, test surface, or reason to change. Avoid unrelated grab bags:

```text
Bundle:
Why together:
Evidence of cost:
Behavior to preserve:
Likely files:
Change:
Baseline/check:
Risk:
Return: high|medium|low
```

5. For discovery or multi-bundle cleanup, recommend an ordered bundle plan. Order bundles by dependencies, behavior-preservation risk, validation confidence, and engineering return. Name the recommended first bundle and the next bundle to inspect or implement after it. For a narrow refactor, pick one scoped slice.
6. If the user asked to keep searching, keep looping, or clean until nothing useful remains, continue from the coverage note after each bundle: pick the next uninspected source area, deferred bucket, adjacent ownership boundary, or cleanup signal before concluding.
7. Choose the check by lane: behavior-sensitive refactors need an existing test or small repeatable behavior check; pure human-reviewability cleanup can use syntax, lint, format, diff inspection, or another focused check that fits the touched files.
8. Make one narrow reviewability cleanup or behavior-preserving refactor slice and keep the repo buildable or runnable after it lands.
9. When human-reviewability cleanup was requested, or a refactor leaves touched files harder to review, do a scoped pass on imports, method/function order, grouping, names, comments/docstrings, and stale comments. Keep the pass scoped to requested, touched, or directly related code.
10. Run focused and surrounding checks after the final edit, then inspect the diff for behavior preservation, scope control, user-change preservation, and reduced future change cost. For continued-cleanup requests, update the coverage note and either pick the next high- or medium-return bundle or state the concrete stop reason.

## Prefer

- Consolidates a duplicated rule into one module, helper, or caller-facing path.
- Consolidates helper files or code paths into a clearer ownership module when separation creates navigation tax without reducing coupling.
- Deepens a module by giving callers a smaller interface, hiding useful implementation detail, and improving locality for future changes.
- Moves I/O, persistence, network calls, time, randomness, or other side effects to an outer layer or explicit dependency.
- Groups related code inside the right ownership boundary so setup, validation, core behavior, side effects, and output are easier to scan.
- Strengthens an existing caller-facing test surface instead of adding private hooks or new test-only entry points.
- Improves names, ordering, imports, comments, docstrings, or local structure inside the requested or touched scope when it reduces human review cost.
- Renames a concept to match shared domain or architecture language, and updates `CONTEXT.md` only for recurring vocabulary, module-boundary, or public or caller contract confusion.
- Deletes obsolete code, wrappers, helpers, options, stale comments, unused imports, or commented-out code that no longer earn their cost.

## Avoid

- Rewrites a subsystem because it looks untidy.
- Creates one-file-per-helper, one-file-per-type, one-file-per-step, or size-targeted modules when the files are normally read or changed together.
- Adds a shallow wrapper, abstraction, interface, adapter, hook, option, protocol, or registry with one real use and no actual caller variation to hide.
- Hides simple control flow behind extra modules, registries, protocols, or adapters with one production use.
- Extracts a pure helper only to simplify a private test while the real behavior remains scattered or hard to verify through a caller-facing entry point.
- Moves files without reducing coupling, simplifying a caller-facing entry point, or improving a test surface.
- Changes behavior or interface shape while calling it cleanup, or leaves callers needing the same implementation knowledge as before.
- Adds frameworks, dependencies, metadata machinery, or configuration systems.
- Adds comments that restate obvious code or explain confusing code that should be renamed, regrouped, simplified, or moved behind a clearer interface.
- Reorders, renames, reformats, or import-sorts broad areas for style without reducing caller knowledge, navigation cost, or maintenance risk.
- Mixes broad formatting churn with a functional or cleanup change.
- Treats one cleanup bundle, one passing check, or one quick scan as proof that a continued-cleanup scope is exhausted, or keeps cleaning after only low-value, risky, out-of-scope, or decision-blocked candidates remain.
- Starts file moves, abstraction work, deletes, or broad formatting before the source evidence, caller-visible behavior to preserve, and lane-appropriate check are known.
- Deletes pre-existing dead code outside the requested area without approval.

## Stop Or Ask

- The cleanup requires a user or caller behavior, data, security, migration, dependency, or public or caller contract decision.
- The cleanup has multiple plausible caller interfaces, test surfaces, or ownership boundaries and repo evidence does not clearly choose one.
- Current caller-visible behavior is important but cannot be checked cheaply.
- The smallest safe slice is still a broad rewrite.
- The user wants exhaustive repo-wide cleanup but the repo is too large to inspect honestly in one pass; propose a bounded sweep scope before editing, then report uninspected areas instead of implying the whole repo is clean.
- Continued cleanup has reached only low-value, risky, outside-scope, already intentional, or decision-blocked findings; report the coverage note and stop reason instead of continuing churn.

## Report

For cleanup discovery or continued-cleanup work, report the requested scope, changed files or recommended bundles, checks run, coverage note summary, remaining candidates or uninspected areas, and the next bundle or concrete stop reason. Do not claim behavior was preserved or a cleanup scope is exhausted without `verify-before-done` evidence.

## Handoff

- `slice-plan`: multi-slice cleanup.
- `tdd-slice`: behavior protection or approved behavior change.
- `diagnose-loop`: cleanup reveals a failing test, bug, regression, or unexplained symptom.
- `github-tracking`: cleanup should become issue or PR tracking.
- `workspace-safety`: before broad file moves, deletes, branch/worktree changes, dependency installs, generated output, or edits that overlap dirty paths.
- `verify-before-done`: before claiming behavior was preserved or the cleanup is ready.
