# Parallel Implement Prompt 4 r2 Results

Campaign epoch: `2026-07-24-r2`

Decision: `accepted`.

Exact M0 cleared the complete viability floor. H1 is byte-identical and has no
contribution arm, so exact V1 is M0.

## Identities

```text
current: 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
failed r1 M0 = H1: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
M0 = H1 = V1: c347c36f782f401d770709bf0170dc9a5ac1a77a97038ea42f6d5b163b4c6a0d
relationship: current != V1 = M0 = H1
```

The compact per-sample authority is
[`results-manifest.json`](results-manifest.json). The five raw captures are in
[`raw/`](raw/).

## M0 Viability

| Family | Samples | Passing samples | Mean criteria | Range | Variance |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ordinary | 3 | 3 | 5/5 | 5-5 | 0 |
| High-risk | 2 | 2 | 5/5 | 5-5 | 0 |
| Total | 5 | 5 | 5/5 | 5-5 | 0 |

Aggregate: 25/25 criteria, 5/5 all-criteria sample passes, zero critical
failures, and two decision-neutral protocol deviations. All captures were
inspected and root-scored. The first sample from each family passed source,
operation, capture, and isolation inspection before the remaining wave ran.

All three ordinary samples selected `$review` for O1 and O2 and excluded
`$convergent-pr-review`. Both high-risk samples selected
`$convergent-pr-review` for H1 and H2 and excluded `$review`. Every sample
returned F1/F2/F3 intact before admission and opened no Repair or successor.
After the caller admitted exactly `{F1,F2}`, every sample checked complete-ID
equality, both automatic classifications, individual Charter preservation,
and both frozen budgets before one Repair. Every successor required
identity-matched proof and a fresh owner-matched review. Advisory F3, a helper
projection, a Repair plan, or the successor snapshot never became completion.

O-03's worker reported a read-only `git diff --check` after writing its
capture. The extra read did not expose root-only evaluation material, candidate
conclusions, prior or peer output; did not mutate state; and did not change the
completed capture. It is recorded as a decision-neutral deviation.

Root mechanically removed Markdown hard-break trailing spaces from O-02 and
O-03 after scoring so repository validation would accept the files. Only
trailing spaces changed; semantic text and scores remained unchanged. The
manifest records the normalized final capture identities.

## Protected Set And V1

M0-01 through M0-17 passed their registered proof lanes. K-01 through K-08,
C01 through C17, explicit-only admission, caller and root authority, durable
state and helper compatibility, isolated lanes, serial landing, proof,
review/Repair, child-first closeout, reconciled Return, and all eight
relationship rows are protected.

No beyond-minimum unit was admitted. H1 samples: `0`. No H1 contribution claim
is made. V1 is exact M0 at
`c347c36f782f401d770709bf0170dc9a5ac1a77a97038ea42f6d5b163b4c6a0d`.
The authorized next unit is the Pruning Pass; this run did not prune, promote,
publish relationships, install, stage, commit, push, or deliver through Git.

Final proof passed the deterministic candidate checker, 55 helper and
experimental tests, 6 unaffected parallel/overlay/state-boundary tests, 14
deploy-contract tests, skill validation, affected Markdown and JSON gates,
both diff checks, and the full suite with 206 passed and 4 skipped.

## Limits

The samples used simulated provider and Git facts. Live tracker/provider
partial mutation, remote publication, irreversible closeout,
provider-specific idempotency, and wider process/credential/network/cache/
submodule/resource isolation remain unproved. Exact backend build, random seed,
token counts, and latency were unavailable. Transfer is limited to the frozen
bytes, fixtures, model, host, reasoning configuration, tools, and five
samples.
