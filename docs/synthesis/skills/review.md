# Review Deployment Synthesis

Status: `promoted`; installation proof is recorded in
`docs/validation/transcripts/2026-07-23-review-prompt5-promotion.md`.

## Canonical Identity And Contract

The canonical package is `skills/custom/review` at tree SHA-256
`4bc1ce43eaa00a9ad7a7482a639793b286fde27c14ba0c5e41e1f73364eb9786`.
It contains exactly:

| Surface | SHA-256 | Runtime role |
| --- | --- | --- |
| `SKILL.md` | `03235a5bf4ade1f6d9c580e9210f2d0d7ee3ce8a7f773be0bd39b940ad625fdd` | Ordinary diff routing, immutable capture, Standards/Spec judgment, admission, drift, terminal Return |
| `FINDING-CONTRACT.md` | `f99446f46d3f6f31b58d0dfecb31c3602742d1e7f8b14f43414f0575b7a6cc95` | Five-gate finding admission, record, severity, remediation classification |
| `SMELL-BASELINE.md` | `966b35b7da2690a5df33d697b43b3c0bd41891b1a5e554c2f0b266610ac2259f` | Conditional fallback when repository Standards are thin |
| `ADVISORY-CONTRACT.md` | `5edf5100cd8ff6d924d93866100f0c2c80f17751c999985105eb5bf0a6003972` | Foreign Convergent/Audit compatibility; ordinary Review does not load it |
| `agents/openai.yaml` | `5b344e7c178aeb37da631a640704dcc71d24c67442f7a9a5bc054586e9453ca4` | Implicit invocation metadata |

Review judges one bounded ordinary branch, WIP, staged, or since-X diff from
one complete immutable snapshot. It runs:

```text
Route -> Pin -> Trace -> Judge -> Admit -> Return
```

Read-only constrains the entire sequence. Standards ("built right?") and
applicable Spec ("right thing?") are separate axes. The safe failure is
`incomplete`; `complete` means coverage closed, not release acceptance. The
caller retains the Charter, target inputs, proof and risk decisions, Repair,
Lock, successor snapshots, delivery, trackers, and every mutation.

## Relationships And Ownership

| Relationship | Observable trigger and Return |
| --- | --- |
| Implement / Parallel Implement -> Review | A complete ordinary fixed target with Charter, `Spec required`, Source Trace, fixed point, target, and required proof needs Standards/Spec judgment; one terminal report returns to the caller |
| Review -> Convergent PR Review | A local PR or high-risk local diff transfers once with the complete caller packet; Review stops |
| Review -> Audit Codebase | An immutable repository-baseline request receives one recommendation; Review stops and does not start Audit |
| Foreign consumers -> Review contracts | Convergent, Audit, Implement, and Parallel Implement use the finding, fallback, or advisory contracts under their recorded load conditions |

There is no reverse Convergent-to-Review handoff, duplicate ordinary pass,
automatic Audit run, or Review-owned Repair, Lock, or successor state. The
concurrent Parallel Implement promotion preserves the same caller packet,
one-route choice, idle-root Repair authority, and fresh successor review.
No relationship-index wording change was required by Review promotion.

## Decisions

Campaign shape was `pruning-only`: prior canonical
`ec62f904a12779de948dcfbbbc7c72c5b79470cc0edac8cfb1b1f017f9180080`
differed from source-derived `B0`, while accepted `C1 = B0`. No beyond-minimum
C1 mechanism was admitted.

Accepted steering claims:

- complete live-content and identity capture (`3/5` D0 to `5/5` B0);
- identity recomputation and drift-to-incomplete (`3/5` D0, including two
  stale-current critical failures, to `5/5` B0); and
- the exact authority footer plus one-report terminal stop (`0/5` D0 to `5/5`
  B0).

Rejected steering-efficacy claims:

- Route select-before-capture;
- the Standards-to-Spec lens reset;
- admission before severity; and
- the target-required/reviewer-required/optional proof-gap distinction.

Each rejected claim had `5/5` control and `5/5` B0 compliance. Its clause
remains only because an independent relationship, axis, finding, or truthful
coverage contract requires it.

The Pruning Pass retained every passage and made no material cut. Apparent
proof-gap overlap has separate owners: `SKILL.md` owns coverage and safe
failure, while `FINDING-CONTRACT.md` owns candidate admission for Review and
foreign consumers. No no-op, sediment, scattered meaning, inline branch-only
reference, copied foreign procedure, or unused runtime surface was found.

Rejected or deliberately absent behavior remains outside canonical Review:
ordinary advisory mode, a required finding title, same-axis deduplication,
artifact-authority tables, detailed snapshot-manifest vocabulary, helpers,
operations files, persistent ledgers, report renderers, automatic recapture,
cross-axis consensus, synthetic confidence scores, mutation, and delivery.

## Proof

- Construction and semantic-unit ledger:
  `docs/validation/transcripts/2026-07-23-review-prompt3-construction.md`
- Behavior audit and exact results:
  `docs/validation/transcripts/2026-07-23-review-prompt4-behavior-audit.md`
- Exact 95 raw outputs and per-sample SHA-256 pointers:
  `docs/validation/evals/review-prompt4/`
- Passage-level pruning decision:
  `docs/validation/transcripts/2026-07-23-review-pruning.md`
- Promotion, canonical integration, installation, parity, and final checks:
  `docs/validation/transcripts/2026-07-23-review-prompt5-promotion.md`

Behavior evidence is exact only for the promoted bytes, fixed tasks, supplied
context, inherited runtime, tools, authority, evidence, and recorded rubrics.
Unavailable telemetry remains exact model build ID, token counts, sampler seed,
and per-sample latency. The initial mixed Route packet and first remediation
fixture's disposition-vocabulary subcase remain superseded protocol
deviations; the valid Route and remediation reruns own those judgments.

Residual gaps are external generalization beyond the recorded packets and
unavailable telemetry. No new behavior wave was required or run for promotion.
Git delivery remains outside this synthesis.
