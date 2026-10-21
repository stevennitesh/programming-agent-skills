# Bulk test pruning

Use for a requested suite-wide purge or a deletion batch large enough that
inconsistent judgments or mechanical edits could hide lost protection. The
entrypoint's scope, authority, and preservation rules still apply. Aim to remove
low-signal maintenance cost; no deletion percentage is a success criterion.

## Establish one rubric and a comparable baseline

Collect the selected suite using its existing runner. Record source state,
commands, collected counts, failures, and relevant durations where feasible.
Distinguish individual file durations, suite wall time, and CI critical-path time;
their reductions are not interchangeable. Preserve enough of the starting state
and results to inspect or reverse each batch without overwriting unrelated work.
For a whole-suite request, account for every collected file and report any
unreviewed portion rather than claiming the purge covered it.

Apply the same keep, rewrite, consolidate, remove, or unresolved criteria across
files. Inspect assertions and the exercised implementation; names and framework
syntax are insufficient. These patterns identify candidates, not deletion rules:

| Candidate | Evidence for removal | Protection that can justify keeping or rewriting it |
| --- | --- | --- |
| Type, constant, or trivial getter checks | The check only restates a compile-time guarantee or the same literal, with no runtime obligation | Runtime validation of untrusted input, serialization, external formats, or an auth policy expressed as a mapping |
| Mock-call mirrors | Assertions restate the test's own setup or incidental private call sequence | Protocol translation, ordering, cancellation, retries, or preventing duplicate external actions |
| Basic DOM or smoke checks | They repeat framework behavior or another retained check without a distinct failure | Application wiring, accessibility behavior, packaging, compiler output, or an actual dependency regression |
| Timers and performance assertions | A sleep or machine-speed threshold has no continuing contract and adds no distinct protection | Deterministic expiry, debounce, race, cancellation, or a documented performance/dependency guard |
| Repeated table cases or snapshots | Retained cases catch the same fault without losing a boundary or outcome | Distinct invalid inputs, platforms, permissions, recovery paths, and state transitions |

Types do not validate runtime data. Fake clocks can make essential timing behavior
cheap and deterministic. Small assertions can enforce important boundaries. Keep
or improve protection for auth, credential isolation, persistence, migrations,
calculations, protocol handling, orchestration, and deterministic races according
to the actual supported workflow. Do not retire these obligations by classifying
their tests as trivial, timing, mock, or smoke tests.

## Review proposed deletions before applying them

Keep a temporary candidate list with exact test identities, a brief retirement
reason, and the retained protection when claiming redundancy. Group related
cases where that remains unambiguous; no permanent per-test audit ledger is
required. Record unresolved cases separately and keep them while other cleanup
proceeds.

When delegation is authorized and available, independent read-only passes can
apply the same rubric to the same source snapshot. Give reviewers the tests,
relevant implementation, accepted requirements, and scope without the other
pass's verdicts. Reviewers return candidates rather than competing edits; the
coordinator owns reconciliation and applies changes serially. Allocate extra
review to consequential boundaries and uncertain deletions rather than requiring
a particular model, swarm size, or pass count.

Agreement makes a candidate eligible for reconciliation, not automatically safe
to delete. Resolve disagreements from the protected behavior and evidence; an
additional reviewer can help but a majority vote cannot retire a requirement.
Without delegation, use a separate skeptical review of proposed deletions and
report that it was not independent. In either case, inspect the proposed batch
for lost safeguards, including deterministic-clock tests and small policy checks.

## Apply exact, reversible batches

For bulk automation, prefer the language's AST or an existing framework-aware
tool. Identify tests by file, enclosing suites, and runner/node identity or source
location tied to the inspected source state. Titles alone may collide, and a
parameterized declaration may generate both removable and essential cases.
Preview matched declarations and expected removals. On ambiguous matches, parse
failure, unexpected counts, or source drift, leave the affected file unchanged
and inspect it before retrying. Avoid broad regex deletion. Small contextual
patches remain suitable when automation adds no value.

Remove newly unused imports, test helpers, and fixtures only after checking all
consumers. Deleting the last test may leave suite hooks, resource setup, or
side-effect imports that still execute. Review those explicitly rather than
deleting an enclosing suite whose remaining children still need them. Parse or
typecheck edited files and run affected tests before extending a doubtful batch.

Reconcile references affected by retirement: setup files, fixture discovery,
explicit test lists, package scripts and test-only dependencies, coverage inputs,
CI shard weights, dead-code tool configuration, and maintained documentation.
Removing tests can expose implicit setup or dependency discovery that retained
tests relied on; repair necessary setup explicitly. Do not disable checks or
erase intentional coverage exclusions just to satisfy tooling.

A dead-code report is a lead, not proof that a production export or declaration
is unused. Check supported external consumers, dynamic loading, package entry
points, and generated uses. Retiring production interfaces or code is separate
from test-only cleanup unless that effect is already authorized; surface those
candidates without expanding scope.

## Verify protection and measure the result

Run the retained tests and repository-required checks for the affected surface,
including existing type, lint, and unused-code checks where relevant. Reconcile
collected test identities and counts with intended removals so missing discovery,
disabled scripts, or added skips cannot masquerade as success. Broad purges need
validation across the selected scope; staged checks need not rerun every suite
after each edit. Compare remaining failures with the applicable baseline before
attributing them to cleanup.

If claiming a speed improvement, repeat the same commands in comparable
environments and disclose cache state, concurrency, and timing noise that limit
the comparison. Report counts and measured durations with their meaning. A green
surviving suite does not prove that retired tests lacked value, and one clean run
does not establish a lower flake rate. Report the retained safeguards, unresolved
deletions, and checks or improvements that remain unproved.

## Source and caution

Adapted from [t3code PR #22557](https://github.com/pingdotgg/t3code/pull/22557):
shared judgments, syntax-aware removal, orphan cleanup, and before/after evidence.
Its [auth restoration commit](https://github.com/pingdotgg/t3code/commit/374959ebe9ec57ab4543ff1923ec68ef3065db39)
shows why category-based deletion needs semantic review: deterministic expiry,
scope, and credential-isolation tests were restored. The PR also repaired browser
dependency pre-bundling after pruning changed discovery. These are useful failure
cases, not evidence that this skill reproduces the PR's reported savings.
