# Test collection audit

Audited the 17 top-level test modules and measured the collected suite before
and after pruning. The audit focused on executable regressions, duplicated
checks, prose assertions, and the slowest calls. It was not a mutation-coverage
analysis of every remaining assertion.

## Changes

| Area | Disposition and reason |
| --- | --- |
| Skill-pack contracts | Removed 76 tests dominated by exact prose, heading order, word choices, and static declarations of intended behavior. Retained executable setup validation, parsed routing, policy metadata, and artifact identity checks. |
| Tracker validation | Removed one duplicate lower-level case already exercised through the provider validator. |
| Deployment documents | Removed six prose/order tests. Kept the retired runtime path and reference checks, without banning historical phrase variants. |
| Experimental skills | Removed three prose tests. Kept actual per-file marker rejection and retired-package checks. |
| MLE workflow | Removed six prose tests. They checked declarations about scientific validity rather than running an evaluation or checking a computed result. |
| Value-stock instructions | Removed six wording tests, including tests named as evaluations that only searched for descriptions of those evaluations. Kept local link checks. |
| Worktree fixtures | Supply test Git identity through the subprocess environment, eliminating two configuration commands per fixture while retaining real repositories, commits, worktrees, and cleanup. |

Removed unused test helpers and constants. Retained mixed tests' executable
assertions while removing incidental prose assertions. Added a missing assertion
after restoring valid lane configuration in an existing reconciliation test.

The installer, worktree, migration, report-update, relationship helper,
composition, catalog, and validator tests exercise real effects or parsed
contracts. Their slower cases cover partial failures, drift, isolation,
concurrent writes, and recovery. These were retained rather than replaced by
mocks that would remove the behavior being tested. Frozen research fixtures
remain where they exercise catalog or composition mechanisms.

## Results and limits

| Run | Collected | Passed | Skipped | Elapsed |
| --- | ---: | ---: | ---: | ---: |
| Before | 401 | 396 | 5 | 14.74 s |
| Final candidate | 303 | 298 | 5 | 14.99 s |

Both measurements used the repository's default ten-worker configuration on the
same host. An intermediate candidate took 14.68 seconds. These single runs do
not establish a speed improvement. Real Git operations remain the dominant
cost; the longest final call took 3.50 seconds and verifies safe cleanup across
clean, dirty, and unintegrated lanes.

The benefit is 98 fewer tests that mostly froze wording, plus cheaper fixture
setup. Removing these assertions does remove automatic alarms for those exact
phrases. They were not evidence that an agent would follow the stated behavior.
Behavioral comparisons, when requested, need real tasks and observable results.

Repository validation and whitespace checks pass. No production implementation,
skill instructions, execution limits, or pytest concurrency settings changed
as part of this audit.
