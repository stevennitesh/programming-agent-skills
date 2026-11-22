---
name: test-cleanup
description: Remove low-value tests and consolidate, organize, or streamline a selected suite. Explicit request only; excludes requests solely to run tests or add feature coverage.
---

# Test cleanup

Remove maintenance and execution burden while preserving meaningful regression
protection for supported behavior. Keep, rewrite, consolidate, reorganize, or
remove tests according to the failures they catch. Fewer tests, higher coverage,
or a green run alone do not establish improvement; a supported no-change result
is valid.

Use only when explicitly requested. A test purge covers the full collected suite
within the selected repository or narrower scope. For other cleanup with no stated
scope, start with tests added or modified in the current task and their fixtures
and helpers. Establish scope before deletion when no task-local set exists.
A read-only audit returns findings; cleanup authorizes supported test edits
without approval for each one. Routine local completion checks do not invoke this
full workflow. Run-only requests and ordinary feature coverage stay with their work.

For a small cleanup, start with the affected tests and the closest retained
coverage. Trace the behavior they protect, make the targeted edits, and run
the affected tests. Follow shared fixtures, runner configuration, or supported
consumers when they could change what should be kept or verified.

For a suite-wide purge or large deletion batch, read
[Bulk test pruning](references/bulk-pruning.md). Its shared rubric, deletion
review, exact edits, and measurements supplement this method only for that scope.

## Establish what the tests protect

Use the implementation and accepted requirements to identify the contract.
Consult configuration, consumers, or history when they could change the decision.
Account for supported external consumers. Preserve established requirements,
including existing protections in personal projects.

Use a baseline when it helps distinguish an existing failure, stale expectation,
or execution limit. Reuse results whose inputs and conditions still apply.
Failure, slowness, flakiness, or a skip alone is never a retirement reason.

## Keep the protection; remove the burden

For each candidate ask **what plausible regression in supported behavior it
could catch**. Call a case redundant only when a retained case would fail for
the same regression at the relevant boundary. Keep unresolved cases while
continuing independent cleanup. Group removals that share a reason.

- Remove completed-edit checks with no continuing requirement. Retire old-behavior
  tests only when that behavior is demonstrably unsupported.
- Prefer observable results, calculations, state transitions, errors, recovery,
  and effects. Rewrite incidental implementation coupling where useful; focused
  internal tests can still efficiently protect meaningful logic.
- Remove tautological assertions whose outcome is guaranteed by the test setup
  or whose expected result simply repeats the computation the test claims to
  verify. A check that only reads back a stub's configured value is one
  example. Remove the whole case when it exercises no other continuing
  obligation. Where the behavior still needs coverage, check an independently
  determined result, effect, or relationship, such as retry idempotence.
- Judge source checks, snapshots, mocks, and negative assertions by their protected
  contract. An exact export name or absence of writes can be meaningful. Narrow
  oversized snapshots to the relevant contract.
- Prune a matrix by the regressions its cases distinguish. Keep a representative
  case for each distinct failure, input boundary, or state transition. Where a
  shared parser rejects input before platform-specific logic, repeat a case per
  platform only if that adds coverage. Keep wiring, platform behavior, or
  interactions that can fail independently. Use parameterization or small
  helpers where useful, keeping each retained scenario identifiable and runnable.
- Use repository conventions for names, grouping, and fixture placement. Keep
  fixtures at the narrowest useful shared scope; impose no new taxonomy. Reconcile
  collection, imports, and CI selectors after moves or renames.
- Reduce costly setup or repeated work using relevant timings. Prefer small faithful
  fixtures and deterministic clocks; share expensive setup only with reliable
  reset and independence. Preserve the wiring boundary responsible for the fault.
- Retain required platform, dependency, and compatibility cases and proportional
  protection for corruption, credential exposure, duplicate external actions,
  incorrect calculations, and other supported consequences.

Remove orphaned test-only helpers, fixtures, imports, and assets after checking
implicit discovery, hooks, configuration, and CI consumers. Keep the framework;
do not expand cleanup into a production refactor. Do not weaken assertions, add
skips/xfails, lower thresholds, or change production behavior to obtain green.
Correct stale expectations only against established behavior; report obsolete
requirements separately from repaired failures. Surface out-of-scope production
bugs or support decisions and continue unaffected cleanup.

## Finish with proportionate evidence

Run affected tests and required checks. When removals, moves, renames, or
parameterization change test identities, verify that the runner still collects
the intended retained scenarios. Broaden checks when shared fixtures, discovery,
configuration, or unresolved impact could affect other tests. Reuse still-valid
evidence.

For a consequential rewrite with unclear fault sensitivity, use a safe temporary
fault or another discriminating check when practical. Isolate it, restore the
exact prior state, and prevent real external effects or data damage. No mutation
campaign is required; disclose unproved sensitivity.

For a small cleanup, report what changed, what protection remains, and the
checks and material limits. For a broader cleanup, group removals by reason and
state the scope verified. Runtime claims need comparable measurements.
