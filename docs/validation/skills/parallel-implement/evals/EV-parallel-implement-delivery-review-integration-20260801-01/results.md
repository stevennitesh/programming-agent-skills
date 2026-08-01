# Delivery and review integration behavior results

Evaluation ID: `EV-parallel-implement-delivery-review-integration-20260801-01`

Decision: **accept**

The control deficit appeared before candidate sampling. The candidate then
removed every observed critical failure and preserved every wrong-condition
guard.

## Frozen identity read-back

| Arm | Packet SHA-256 before sampling | Packet SHA-256 after sampling |
|---|---|---|
| Control | `10702aab369af72938149112fe0ceae11dcb84df8e07f5841d7ec7be32281304` | `10702aab369af72938149112fe0ceae11dcb84df8e07f5841d7ec7be32281304` |
| Candidate | `b9cc098085287d73d0b0d7c449542f445bec34e80556838cf9b30b67a443f82a` | `b9cc098085287d73d0b0d7c449542f445bec34e80556838cf9b30b67a443f82a` |

## Entry-positive results

| Sample | Arm | Score | Critical failures | Material omissions |
|---|---|---:|---|---|
| `behavior_control_1` | control | 7/14 | P1, P2 | P3, P4, P7 |
| `behavior_control_2` | control | 3/14 | P1, P2, P5, P6 | P3, P4, P7 |
| `behavior_control_3` | control | 3/14 | P1, P2, P5, P6 | P3, P4, P7 |
| `behavior_control_4` | control | 3/14 | P1, P2, P5, P6 | P3, P4, P7 |
| `behavior_control_5` | control | 3/14 | P1, P2, P5, P6 | P3, P4, P7 |
| `behavior_candidate_1` | candidate | 14/14 | none | none |
| `behavior_candidate_2` | candidate | 14/14 | none | none |
| `behavior_candidate_3` | candidate | 14/14 | none | none |
| `behavior_candidate_4` | candidate | 14/14 | none | none |
| `behavior_candidate_5` | candidate | 14/14 | none | none |

The control failures were practical topology failures:

- P1: 5/5 routed Implement directly to Parallel Implement instead of returning
  the parent campaign to the caller.
- P2: 5/5 routed Parallel Implement directly to Implement instead of returning
  the standalone item to the caller.
- P5: 4/5 allowed a separated-root Standards fallback after the bounded lane
  replacement was exhausted.
- P6: 4/5 made High-Assurance Review hand the ordinary packet directly to
  Change Review instead of returning `scope-mismatch` to the delivery caller.

All control samples also omitted at least one explicit delivery-owned freshness
or semantic task-identity requirement in P3, P4, or P7. Those omissions scored
`1`, not as critical failures, because the returned endpoint was otherwise
correct and the sample did not explicitly prescribe identity reuse.

The candidate produced the required behavior in every sample:

- wrong-scope inputs return intact to the caller without delivery cross-routing;
- ordinary formal review uses one fresh `ordinary-reviewer` task and Change
  Review remains the direct read-only leaf;
- high-risk review begins in a fresh `assurance-coordinator` task and requires
  fresh `har-spec-reviewer` and `har-standards-reviewer` core tasks;
- an exhausted invalid core lane returns `incomplete` without coordinator
  substitution or recursive rounds;
- review route mismatches return intact to the delivery caller, which may
  reselect once in a new task; and
- repaired candidates receive a new generation identity and new review actor
  and task identities.

## Entry-positive aggregate

| Metric | Control | Candidate |
|---|---:|---:|
| Samples | 5 | 5 |
| Total score | 19/70 | 70/70 |
| Mean | 3.8/14 | 14/14 |
| Range | 3-7 | 14-14 |
| Population variance | 2.56 | 0 |
| Critical failures | 18 | 0 |
| Critical-failure reduction | — | 100% |
| Worst sample | 3/14 | 14/14 |

The preregistered control gate opened because every control sample had critical
failures and the mean was below `12/14`. The candidate cleared every
contribution threshold.

## Wrong-condition results

| Sample | Arm | Score | Critical regressions |
|---|---|---:|---|
| `behavior_guard_control_1` | control | 10/10 | none |
| `behavior_guard_control_2` | control | 10/10 | none |
| `behavior_guard_control_3` | control | 10/10 | none |
| `behavior_guard_control_4` | control | 10/10 | none |
| `behavior_guard_control_5` | control | 10/10 | none |
| `behavior_guard_candidate_1` | candidate | 10/10 | none |
| `behavior_guard_candidate_2` | candidate | 10/10 | none |
| `behavior_guard_candidate_3` | candidate | 10/10 | none |
| `behavior_guard_candidate_4` | candidate | 10/10 | none |
| `behavior_guard_candidate_5` | candidate | 10/10 | none |

Both arms had mean `10/10`, range `10-10`, population variance `0`, and no
critical regression. The candidate preserved:

- valid standalone ordinary Change Review;
- ordinary routing for a large diff without a supported high-risk trigger;
- exactly two core High-Assurance lanes when no specialist gap exists;
- residual-risk treatment for unavailable optional verification; and
- the distinction between worker-commit landing inspection and formal candidate
  review.

## Runtime and deviations

- Twenty fresh-context samples completed: five entry-positive and five
  wrong-condition samples per arm.
- All samples obeyed the read-only and evidence-isolation packet. No sample read
  the opposite arm or mutated the repository.
- Raw outputs remain in their named task records.
- Host telemetry exposed completion state and task identity but not per-sample
  token use, cost, or stable latency; those metrics are unavailable rather than
  estimated.
- No protocol deviation occurred. Control variation in P5 and P6 is recorded in
  the per-sample results and did not affect the contribution decision.

## Decision

**Accept.** The observed control deficit was large, the candidate contribution
was complete across five independent entry-positive executions, and five
independent wrong-condition executions found no regression.
