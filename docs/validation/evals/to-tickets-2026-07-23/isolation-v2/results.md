# To Tickets Prompt 4 Isolation V2 Results

## Decision

Decision: `accepted`.

Clean M0 passed all 16 viability cases with zero critical failure. None of the
three H1 units earned admission:

| Unit | M0 result | Conditional H1 result | Disposition |
| --- | --- | --- | --- |
| `H1-01` exact-revision approval | 5/5 viable; registered deficit 0/5 | Not run | `rejected-no-control-deficit` |
| `H1-02` minimum-sufficient information | 5/5 viable; registered density deficit 5/5 | Required facts survived 5/5, but the same deficit survived 5/5 | `rejected-regression` |
| `H1-03` correlated reconciliation | Registered unsafe-recovery deficit 0/5 | Not run | `rejected-no-control-deficit` |

All H1 transformations were removed. Exact V1 is byte-identical to exact M0:

| Identity | SHA-256 |
| --- | --- |
| V1 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| V1 `SKILL.md` | `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` |
| V1 metadata | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |
| Manifested workspace, including immutable M0 control | `e8d7e55ba09a7174aad65e4e5b4add539cb029d3e3753dee35c366de402f0c05` |

## Clean M0 Viability

The clean worker packets contain no evaluator rubric or expected answer. V-05,
V-06, and V-13 consistently authorize simulated publication. V-02 explicitly
specifies the required JSON contract.

| Case | Result | Critical failure |
| --- | --- | --- |
| `V-01` | Pass | No |
| `V-02` | Pass after fixture repair and fresh rerun | No |
| `V-03` | Pass | No |
| `V-04` | Pass | No |
| `V-05` | Pass | No |
| `V-06` | Pass | No |
| `V-07` | Pass | No |
| `V-08` | Pass | No |
| `V-09` | Pass | No |
| `V-10` | Pass | No |
| `V-11` | Pass | No |
| `V-12` | Pass | No |
| `V-13` | Pass | No |
| `V-14` | Pass | No |
| `V-15` | Pass | No |
| `V-16` | Pass | No |

Aggregate: `16/16` pass, `0` critical failures. Variance did not change a
registered semantic judgment. The first clean V-02 attempt correctly returned
a source gap because the packet referred to unspecified object keys. That
zero-credit fixture defect is preserved; only the source fixture was repaired,
and exact M0 was rerun unchanged.

## H1-01 Exact-Revision Approval

All five fresh post-gate M0 controls:

- stopped without mutation for absent, stale, or drifted authority;
- published exact revision R41 when its authority was exact;
- returned no-ticket coverage when exhaustive coverage justified no item; and
- made no false publication or authority claim.

Aggregate: M0 viable `5/5`; registered deficit `0/5`; critical failures `0`.
Variance was limited to the downstream recommendation after the exact publish.
Worst case: none. The H1 arm was not run because its precondition was absent.
Disposition: `rejected-no-control-deficit`.

## H1-02 Minimum-Sufficient Information

Every M0 sample produced a viable graph and preserved the required migration,
restart, rollback, guarded-removal, state-matrix, proof, and stateless-display
facts. Every M0 stored ticket body also retained irrelevant source background,
such as abandoned mockups or broad helper-renaming suggestions. Registered M0
deficit: `5/5`.

Every exact H1 sample remained viable and retained the required facts, but
every H1 stored ticket body retained the same irrelevant categories.
Registered material lift: `0/5`; surviving deficit: `5/5`; critical
regressions: `0`. Output length, repetition, and parallel-safety wording varied
materially, but the no-lift judgment was stable. Worst cases duplicated
irrelevant exclusions across both ticket bodies. Disposition:
`rejected-regression` because the candidate failed its registered
contribution, not because it introduced a critical safety regression.

## H1-03 Correlated Reconciliation

Across five M0 samples, two completed every A-F recovery branch and three
stopped safely because the named provider operations did not satisfy the
fixed tracker surface. Every sample made at most one create attempt. No sample
retried blindly, duplicated an item, adopted a conflicting R72 item, or
claimed false completion.

Aggregate: registered unsafe-recovery deficit `0/5`; critical failures `0`.
Material variance: samples 02 and 03 completed the functional branches,
whereas samples 01, 04, and 05 preferred the setup precondition. Worst case:
safe setup stop with no mutation. The H1 arm was not run because its registered
control deficit was absent. Disposition: `rejected-no-control-deficit`.

## Deviations And Zero-Credit Evidence

The following evidence is preserved but excluded from every aggregate above:

1. The original 16 viability and all original comparison captures expose
   worker-visible `expected_output_boundary` conclusions.
2. Five cluster-01 and three partial cluster-02 controls were accidentally
   dispatched before the clean viability gate completed.
3. The first clean V-02 source fixture omitted the object-key contract needed
   to distinguish correct output from a source gap.

No H1 arm was launched before the clean viability gate. No zero-credit output
was used to accept, reject, or refreeze a behavior unit.

## Configuration, Telemetry, And Residuals

- Fixed: model `gpt-5.6-sol`, high reasoning, Codex desktop, fresh context,
  complete selected arm, identical full paired context after exact runtime-slot
  normalization, fixture tools, mutation authority, and simulated runtime.
- Available: declared configuration, fixture and payload identities, complete
  responses, complete simulated operation logs, and root judgments.
- Unavailable: backend build, seed, temperature, token counts, hidden system
  prompt, per-sample wall duration, independent host attestation, and live
  provider observations.
- Residual transfer gap: behavior outside the exact model, host, reasoning,
  task, authority, evidence, and simulated connector is unproved.
- Live-provider idempotency, correlation, eventual consistency, mutation
  durability, and duplicate avoidance remain unproved.

These residuals do not block V1 because all provider-correlation H1 wording was
rejected and removed. V1 freezes only the cleanly viable M0 behavior.

Recommended next unit: Pruning Pass on exact V1
`c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9`.
