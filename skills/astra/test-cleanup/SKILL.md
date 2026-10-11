---
name: test-cleanup
description: Clean up stale, redundant, or brittle tests in a selected scope. Explicit request only; excludes requests solely to run tests or add feature coverage.
---

# Test cleanup

Leave a maintainable suite that catches meaningful regressions in the current
supported workflow. Judge tests by the behavior and failures they protect, with
room to choose investigation, edits, and sufficient proof. Fewer tests, higher
coverage, or a green run alone do not establish improvement. A supported no-change
result is valid.

Use only when the user explicitly invokes or requests test cleanup. Validation
and replacement regression tests remain part of cleanup when needed; requests
solely to run tests or add feature coverage stay with their owning work.

Use the requested task, directory, or suite scope. If unspecified, review tests
added or modified during the current task and their associated fixtures and
helpers. Establish a scope before deleting when no task-local set is identifiable;
do not silently expand to the whole repository. A read-only audit returns findings.
A cleanup request authorizes supported test edits without approval for each one.
Ordinary implementation does not require this full audit. Before completing a
work section, briefly review tests added or modified in that section and remove
one-off edit-verification checks that have no continuing purpose. Keep that check
local. If it identifies substantive cleanup, suggest this workflow; expand into
it only when explicitly requested or already authorized.

## Establish what the tests protect

Inspect relevant implementation, accepted requirements, test configuration, and
nearby tests. Determine supported consumers and guarantees; an interface may have
external consumers even when a local caller search is empty. Use current owner
documentation and relevant history when intent is unclear. Tests and present
implementation are evidence, not sole authority for intended behavior.

Optimize for the project's established scope, correctness, simplicity, and fast
feedback. Do not invent compatibility, migrations, public deployment, or general
hardening requirements for a personal workflow. Equally, personal-project status
does not retire existing support or safeguards.

Establish a relevant baseline before editing where feasible, reusing recent
results when their code, inputs, dependencies, and environment remain applicable.
Distinguish failures of supported behavior from obsolete expectations and execution
limits. A failure itself is never evidence that a test should be deleted.

## Keep the protection; remove the burden

For each cleanup candidate, ask: **What plausible future regression would this
catch, and what supported behavior or concrete ongoing constraint would it affect?**
Use the answer to keep, rewrite, consolidate, or remove it. Investigate uncertainty;
retain and flag tests whose purpose remains unresolved while continuing independent
cleanup. No per-test ledger or deletion quota is needed.

- Remove one-off checks that only prove a completed rename, deletion, replacement,
  or migration happened, when the checked condition has no continuing requirement.
  Remove old-behavior tests only when that behavior is demonstrably unsupported.
- Prefer observable outputs, calculations, state transitions, errors, recovery,
  and side effects. Rewrite useful tests tied to incidental implementation where
  practical. Keep focused internal tests when they efficiently protect meaningful
  logic; converting everything to integration or end-to-end tests adds burden.
- Assess source-text checks, snapshots, mocks, and negative assertions by purpose,
  not syntax. An exact export name can protect a supported interface; absence of
  writes after cancellation can protect data. A test that only checks its own
  mock's configured return value offers no such protection unless it exercises
  meaningful product behavior. Narrow oversized snapshots to their real contract
  rather than accepting new snapshots merely to silence failures.
- Consolidate tests only when the remaining cases still catch their distinct
  failures. Shared code paths or covered lines do not prove redundancy: unit and
  integration checks may protect different wiring, ordering, or recovery behavior.
  Parameterization and shared helpers should clarify failures, not hide scenarios.
- Preserve proportional safeguards for actual consequences, including corruption,
  credential exposure, duplicate external actions, and incorrect calculations.
  Keep required platform, dependency, and compatibility cases. Slow, flaky, or
  skipped tests need investigation; those labels alone do not make them obsolete.

Remove orphaned test-only fixtures, helpers, imports, and assets within scope after
checking consumers, including implicit framework discovery, setup/teardown,
configuration, and CI references. Stay with the existing framework and avoid a
broad test abstraction or production refactor.

Do not weaken meaningful assertions, add skips or expected-failure markers, lower
thresholds, or change production behavior to make cleanup pass. Correct stale
expectations only against established supported behavior. A known failing test
can be removed when its requirement is demonstrably obsolete; report that reason
separately from repaired failures. Surface production bugs or support decisions
outside cleanup authority and continue work that does not depend on resolving them.

## Finish with proportionate evidence

Run affected tests and repository-required checks. Broaden validation when shared
fixtures, discovery, configuration, or remaining uncertainty can affect other
tests. Check that retained cases are still collected and actually exercise the
intended behavior; a passing run that collects nothing is not validation. Reuse
unchanged passing evidence and stop repeating checks once the relevant questions
are settled.

For a consequential rewrite whose ability to catch the intended fault is unclear,
use a safe temporary local fault or another discriminating check when practical.
No mutation-testing campaign is required. Isolate any fault experiment, restore
the exact prior state, and ensure it cannot trigger real external actions or
damage data. Disclose when fault sensitivity or other validation remains unproved.

Briefly report the reviewed scope, removals and reasons, rewrites or consolidations
and protection retained, exact checks and results, and unresolved decisions or
unrun checks. Group similar changes; do not imply full-suite success from a
targeted run. No permanent audit report or repository-guidance update is needed
unless requested.
