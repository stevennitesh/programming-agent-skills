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

Use only when explicitly requested. Use the selected task, directory, or suite;
if unspecified, start with tests added or modified in the current task and their
fixtures/helpers. Establish scope before deletion when no task-local set exists.
A read-only audit returns findings; cleanup authorizes supported test edits
without approval for each one. Routine local completion checks do not invoke this
full workflow. Run-only requests and ordinary feature coverage stay with their work.

For a suite-wide purge or large deletion batch, read
[Bulk test pruning](references/bulk-pruning.md). Its shared rubric, deletion
review, exact edits, and measurements supplement this method only for that scope.

## Establish what the tests protect

Inspect implementation, accepted requirements, test configuration, and relevant
consumers/history. Local callers can miss supported external consumers. Tests
and current implementation are evidence, not sole authority for intended behavior.
Respect the established project scope: do not invent support or hardening
requirements, or retire existing protections because the project is personal.

Establish a relevant baseline where feasible; reuse results while code, inputs,
dependencies, and environment remain applicable. Distinguish supported-behavior
failures, stale expectations, and execution limits. Failure, slowness, flakiness,
or a skip alone is never a retirement reason.

## Keep the protection; remove the burden

For each candidate ask: **What plausible future regression would this catch, and
what supported behavior or ongoing constraint would it affect?** Investigate
uncertainty; retain unresolved tests while continuing independent cleanup.
No per-test ledger or deletion quota is needed for ordinary cleanup.

- Remove completed-edit checks with no continuing requirement. Retire old-behavior
  tests only when that behavior is demonstrably unsupported.
- Prefer observable results, calculations, state transitions, errors, recovery,
  and effects. Rewrite incidental implementation coupling where useful; focused
  internal tests can still efficiently protect meaningful logic.
- Judge source checks, snapshots, mocks, and negative assertions by their protected
  contract. An exact export name or absence of writes can be meaningful; asserting
  only a mock's configured result is not product coverage. Narrow oversized
  snapshots to their contract instead of updating them merely to silence failure.
- Consolidate only when retained cases still catch distinct failures. Shared lines
  or code paths do not prove redundancy across unit/integration boundaries. Use
  parameterization or small helpers where useful; keep scenarios identifiable,
  independently runnable, and diagnosable rather than combining unrelated cases.
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

Run affected tests and required checks; broaden for shared fixtures, discovery,
configuration, or unresolved impact. Confirm retained cases are collected and
exercise intended behavior. Reconcile scenarios after moves, renames, or
parameterization so changed identities do not conceal loss. Reuse still-valid
evidence rather than repeating settled checks.

For a consequential rewrite with unclear fault sensitivity, use a safe temporary
fault or another discriminating check when practical. Isolate it, restore the
exact prior state, and prevent real external effects or data damage. No mutation
campaign is required; disclose unproved sensitivity.

Report scope, removals and reasons, consolidation/organization, retained protection,
checks/results, and unresolved or unrun work. Runtime claims need comparable
measurements; maintainability can justify cleanup without a speedup. Group similar
changes and distinguish targeted from full-suite validation. No permanent report
or guidance update is required unless requested.
