# Parallel Implement Prompt 4 Results

Campaign epoch: `2026-07-24`

Decision: `blocked`.

Exact M0 did not clear the protected viability floor. H1 is byte-identical, so
there is no contribution arm and no alternative runtime that can become V1.

## Identities

```text
current: 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
M0: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
H1: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
relationship: current != M0 = H1
V1: not established
```

The compact per-sample authority is
[`results-manifest.json`](results-manifest.json). The five raw captures are in
[`raw/`](raw/).

## M0 Viability

| Family | Samples | Passing samples | Mean criteria | Range | Variance |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 3 | 3 | 8/8 | 8-8 | 0 |
| B | 2 | 0 | 6.5/8 | 6-7 | 0.25 |
| Total | 5 | 3 | 7.4/8 | 6-8 | 0.64 |

Aggregate: 37/40 criteria, 3/5 all-criteria sample passes, zero critical
failures, and zero protocol deviations. All captures were inspected and
root-scored. The first sample from each family passed the protocol gate before
the remaining wave ran.

Family A was stable. Every sample preserved admission and setup order,
serialized A/B, required claim and lane read-back, quarantined invalid or stale
packets, landed only in dependency order, preserved the C conflict, maintained
identity-bound overlays, and returned nonterminal state.

Family B exposed a systematic M0-14 failure. Both samples refused to admit the
eligible F1 `automatic-in-scope` repair while F2 remained
`decision-required`. The frozen rubric requires only F1 to enter Repair, with
F2 returned through its decision branch and F3 left advisory. The exact
`run_ledger.py` compatibility surface enforces the observed refusal: every
blocking finding must be automatic and `finding_ids` must equal the complete
blocking set. This is a frozen M0/K-02 construction contradiction, not
borderline model variance.

B-02 was the worst result at 6/8. It also deferred selection between `$review`
and `$convergent-pr-review` because the fixture did not explicitly label the
target type; B-01 selected the ordinary owner. This variance reinforces an
M0-13 clarity gap but is not needed for the blocking decision.

## Protected Set And Compatibility

M0-01 through M0-12 and M0-15 through M0-17 passed their registered behavior.
M0-13 varied in one B sample. M0-14 failed in both B samples. K-01 through
K-08 passed exact deterministic identity and helper checks, but unchanged
K-02 behavior cannot simultaneously satisfy the frozen M0-14 rule. All eight
relationship rows passed structural ownership traces; behavioral
formal-review routing varied as noted above.

There were no critical failures: no premature mutation, dispatch without
claim/lane read-back, concurrent landing, conflict discard, delegated
formal-review/closeout/publication authority, parent-first completion, or
completion with contradictory state.

## H1, Current-Only Behavior, And V1

No beyond-minimum hypothesis was admitted. H1 samples: `0`. No H1 contribution
claim is made.

The current-only runtime push action remains rejected as foreign Git-delivery
authority, and the arbitrary same-actor-once rule remains rejected in favor of
state-and-authority continuation. The samples exposed no regression from
either removal, but those dispositions cannot establish V1 while M0 itself is
nonviable.

V1 is therefore not `M0`, not `H1`, and not current. No V1 identity was
frozen. Pruning, promotion, relationship publication, installation, and Git
delivery remain closed.

## Limits

The protocol used simulated provider and Git observations. It did not run a
live tracker partial failure, remote publication, irreversible closeout, or
provider idempotency branch. Worktree containment does not prove process,
credential, network, cache, submodule, or scarce-resource isolation. Transfer
is limited to the exact runtime, fixtures, model, host, reasoning
configuration, tools, and sample count.

The safe next action is a bounded Prompt 3 reconstruction that resolves
M0-14 against K-02, refreezes exact runtime and protocol identities, and
returns to Prompt 4. This Prompt 4 run does not authorize that runtime change.
