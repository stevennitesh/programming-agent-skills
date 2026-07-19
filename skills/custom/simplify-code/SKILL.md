---
name: simplify-code
description: Apply one bounded, high-value, behavior-preserving simplification in existing code, or repeat proved cuts inside one named region when explicitly asked for until-clean. Use explicitly when code should become smaller or easier to reason about without feature work, bug fixing, or architectural redesign.
---

# Simplify Code

Own one outcome: one proved reduction in total codebase complexity by default, an explicitly requested bounded `until-clean` campaign, or a proved **No safe simplification** verdict.

**Trace -> Baseline -> Hunt -> Choose -> Cut -> Prove -> Lock.**

## Boundary

- This explicit invocation authorizes local edits for one simplification slice and its narrowly necessary proof support. `until-clean` authorizes serial slices only inside one named region. Leave the index, commits, trackers, external systems, and unrelated work unchanged.
- Target precedence is: an `Eliminate` candidate from a verified `$improve-codebase` report; a user-named file, symbol, module, or coherent diff; otherwise the current diff when it is one coherent region. Without a bounded target, recommend `$improve-codebase` and stop.
- Preserve the commitment boundary, public and data contracts, domain language, trust-boundary validation, data-loss prevention, security and privacy controls, accessibility, concurrency and durability guarantees, and required compatibility.
- Optimize concepts, branches, coordination, indirection, files, and dependencies before line count. Reject code golf, clever compression, and cuts that push complexity into callers.
- Never add a dependency. Remove one only when repository-wide reference and runtime-entry evidence proves that no use remains, then reconcile its manifest, lockfile, and validation fallout.

## Trace

Read repository instructions and routed engineering and domain context. Capture `git status --short`, the relevant diff, and the starting ref without disturbing pre-existing work. Snapshot `git ls-files --stage` and `git diff --cached --binary` so Lock can prove the index contents, not merely its status shape, stayed unchanged.

For `$simplify-code Candidate N from <absolute-report-path>`, read the named candidate from the verified `$improve-codebase` report: region, Source Trace, elimination target, behavior and commitment boundary, proof seam, risk, and sequence relationship. Return to `$improve-codebase` unchanged when the report is missing those fields, the candidate is no longer `Eliminate`, or it is `Absorbed` by another candidate.

Trace the selected behavior through its observable seam, direct callers and callees, tests, entry points, configuration, reflection or registration paths, and nearby equivalents. Search callers operationally; derive preserved behavior from authoritative contracts and caller-visible evidence, not from the implementation alone.

If the work requires a new interface or one ownership decision, recommend `$codebase-design` and stop. If it requires wide discovery, ranking, or multi-region sequencing, recommend `$improve-codebase` and stop. Return any other feature, bug, public-contract, or review ownership mismatch unchanged with the exact unresolved need.

## Baseline

Run the smallest trusted focused proof before production edits and record the result. A useful proof distinguishes the behavior being preserved rather than merely importing, parsing, or exiting successfully.

When focused proof is missing, add the smallest caller-facing characterization only if an independent observable oracle follows from an authoritative contract. Observe it pass against the starting implementation. If behavior is ambiguous or no meaningful seam can distinguish it, return **No safe simplification** with the exact proof gap; do not edit production code.

## Hunt

Inspect the bounded region in this order:

1. **Delete.** Remove unreachable code, expired compatibility, speculative branches, dead flags, or unused configuration only after reference and entry-point evidence proves the cut.
2. **Reuse.** Replace a local reimplementation with an existing project-owned helper, type, decision, or pattern whose semantics match.
3. **Standardize.** **Native-first.** Search in order: a standard-library, language, or runtime capability; a browser, database, framework, or platform capability; then an already-installed dependency. Use the first semantic match whose compatibility and edge behavior hold.
4. **Collapse.** Inline pass-through wrappers, single-product factories, one-implementation abstractions, or layers that add no earning boundary. Consolidate duplicated decisions at their narrowest existing owner.
5. **Shrink.** Reduce branching and data movement with ordinary, readable language constructs while preserving edge cases.

Earlier rungs outrank later ones. Within the first rung that holds, prefer the candidate that removes the most total complexity while remaining one coherent, provable slice. Record credible rejected candidates and why they fail behavior, scope, clarity, sequencing, or proof.

## Choose

Admit a candidate only when:

- its preserved behavior and proof seam are explicit;
- the cut is local enough to validate and review as one concept;
- total caller and maintainer burden decreases;
- no speculative abstraction or new commitment is required;
- its sequence relationship permits work now; and
- the expected simplification can be stated without a fabricated savings baseline.

If every candidate fails, return **No safe simplification** with the accounted region and proof.

## Cut

Make one meaningful move at a time. After each move, remove only change-created fallout: unused imports, helpers, files, configuration, dependencies, and implementation-detail tests superseded by stronger caller-facing proof. Preserve correct behavior tests and pre-existing dead work outside the slice.

Keep the code boring and readable. Retain one concise comment when the cut depends on a non-obvious constraint; name its ceiling and concrete revisit trigger. Omit commentary that only narrates the code.

## Prove

Rerun the focused proof after every meaningful move. Then run the nearest relevant test group and proportionate repository checks. For dependency removal, also prove install or lockfile integrity through the repository-owned lane.

Compare final behavior, diff, and work state with the baseline. Treat exact lines, files, branches, or dependencies removed as descriptive facts, never as correctness proof or universal productivity gains.

## Lock

Run repository diff and whitespace checks. After the last proof command, refresh worktree status and remove only caches, temporary files, and generated artifacts created by this invocation. Review the patch separately for preserved commitments and maintainability. Confirm that only the selected slice and proof support changed, no correct assertion was weakened, change-created fallout is gone, and unrelated work survived. Compare final staged entries and cached binary diff exactly with their Trace snapshots; status text alone is not index proof.

## Until Clean

Enter this branch only when the invocation explicitly says `until-clean` and names one bounded region. Before the first edit, establish a **Campaign contract**:

- **Region:** one file, symbol, module, or coherent subsystem boundary, plus the behavior and proof seam that must remain invariant.
- **Budget:** the user's explicit finite positive cut limit, or `3` successful cuts by default. Never infer, extend, or reset the budget during the run.
- **Progress unit:** one named maintenance obligation removedâ€”a concept, branch family, duplicated decision, coordination step, indirection layer, file responsibility, or dependencyâ€”without introducing an obligation of equal or greater scope.
- **Clean criterion:** one complete Hunt accounts for all five rungs and finds no remaining candidate that passes every Choose gate and removes a progress unit. Renaming, formatting, expression shortening, subjective style preference, or line-count reduction alone never keeps a campaign open.

After each successful Lock, append the cut and its removed and introduced obligations to a progress ledger, decrement the budget, treat the proved result as the next starting state, and rerun the complete Trace, Baseline, Hunt, Choose, Cut, Prove, Lock cycle serially. Admit the next cut only when the ledger shows a strict net reduction. A later cut may revisit a path for a different recorded obligation, but must not recreate or undo an earlier removal.

Stop at the first condition that holds:

1. **Clean:** a complete Hunt satisfies the Clean criterion.
2. **Budget exhausted:** the finite cut limit is reached. Return any still-eligible candidates as residuals; continuation requires a new explicit invocation and budget.
3. **Diminishing return:** the strongest remaining move lacks a progress unit or only changes presentation.
4. **Oscillation:** a move recreates, undoes, or trades an earlier obligation for an equivalent one.
5. **Failed cut:** one Cut or Prove attempt cannot restore the focused and nearby proof. Restore only that attempt to the last locked state and end the campaign.
6. **Boundary stop:** the next move changes behavior or a commitment; needs design or multi-region sequencing; lacks adequate proof; leaves the named region; is absorbed by another candidate; or encounters repository drift outside the campaign.

Return the completed cuts, budget used and remaining, progress ledger, residual eligible candidates, and the precise stop condition. Do not reinterpret `until-clean` as permission for a whole-tree rewrite or automatic budget renewal.

## Return

Return:

```text
Mode: <single-cut | until-clean>
Campaign: <region; cut budget, used, and remaining | n/a>
Simplification: <target and cut(s) | No safe simplification>
Why simpler: <concepts, branches, coordination, indirection, files, or dependencies removed>
Progress ledger: <cut -> removed obligation -> introduced obligation | n/a>
Preserved behavior: <contract and observable seam>
Proof: <before and after commands with results for each cut>
Changed paths: <paths | none>
Rejected or deferred: <candidate and reason | none>
Stop reason: <campaign stop | single cut complete | no safe cut>
Residual risk: <risk or skipped proof | none>
```

## Completion

Complete only when the bounded region, callers, contracts, and proof seam are traced; trusted focused proof passed before and after every cut; each changed path belongs to the authorized region and one proved simplification at a time; nearby checks passed or their skips are named; change-created fallout and invocation-created artifacts are reconciled; and worktree, index, tracker, external, and unrelated state respect the boundary. An `until-clean` result additionally requires the finite Campaign contract, strict progress ledger, budget accounting, one terminal stop condition, and explicit residuals. A fully accounted **No safe simplification** verdict with no production edit is also complete.
