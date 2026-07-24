# Convergent PR Review Deploy Prompt 4: Behavior Audit

- Campaign epoch: `2026-07-24`
- Authorized unit: Deploy Prompt 4: Prove M0 And H1
- Authority: `writing-great-skills` Author
- Starting Git `HEAD`:
  `f3be70c31dd8f2ae9f12a75248065ef313790bda`
- Campaign shape: `hypothesis-candidate`
- Decision: `accepted`
- Pruning, promotion, installation, publication, and Git delivery: not
  performed

## Fixed Inputs And Telemetry

The exact Prompt 3 packages and fixtures were verified before sampling:

| Input | SHA-256 |
| --- | --- |
| M0 package tree | `6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280` |
| H1 package tree | `379474917dc540ef9704a74628af11e123db11fc9e800a94b797278c1ab05c82` |
| Worker-visible fixture | `466c53a4d1efbdb675df702189db5b0af77990603f1b98302bc49b162f9f6a62` |
| Root-only fixture | `697f22290d996128e4dda66eff229cda44deca131c146a38c8cffc2797104d22` |

Before the first sample, available telemetry was frozen in
[results.json](../evals/convergent-pr-review-2026-07-24/results.json). The host
reported Codex based on GPT-5 with inherited campaign model and reasoning
settings. Exact service model and reasoning-effort identifiers, temperature,
and seed were unavailable. Every evaluator used `fork_turns="none"` and
received one exact runtime arm plus one factual worker-visible case. Root-only
hypotheses, rubrics, candidate terms, conclusions, and peer outputs were not
dispatched.

## M0 Viability

All 25 viability cases ran and were inspected before any H1 sample. Every
valid case scored at least 9/10 with no critical failure.

The initial V09 dispatch omitted the frozen simulated-top-level-root authority.
The evaluator therefore applied its actual delegated-agent status and stopped
at the root guard. That output received zero credit. The unchanged V09 case
was rerun once in a fresh context with the exact fixed authority restored; the
task, facts, runtime, and rubric did not change. The rerun passed. This was a
Prompt 4 payload-assembly deviation, not a Prompt 3 fixture or runtime defect.

## Contribution Judgments

Each cluster's first M0 sample was inspected before its remaining four
controls.

| Cluster | M0 controls | Registered control result | H1 samples | Judgment |
| --- | ---: | --- | ---: | --- |
| `Q01-snapshot` | 5 | No defect. M0 used no forbidden operation, captured the required surfaces, detected same-status byte drift, bounded identity claims, and returned `incomplete` when atomicity was unavailable. | 0 | `reject-no-control-deficit` |
| `Q02-coverage-truth` | 5 | M0 remained viable and decision-correct. Q02-01 and Q02-05 omitted same-model or same-model/prompt common-mode limits. | 5 | H1-03 corrected 2/5, below the frozen 4/5 threshold. H1-02 and H1-04 had no control deficit. Cluster `reject-regression` for failed material contribution; no actual regression appeared. |
| `Q03-bounded-recovery` | 5 | M0 remained viable but refused to rehabilitate the origin's otherwise complete return after its sole omitted `blockers` field was supplied in Q03-03. | 5 | H1-05 corrected 1/5, below the frozen 4/5 threshold. Cluster `reject-regression` for failed material contribution; no actual regression appeared. |

All 50 valid behavioral samples and the one zero-credit output are preserved
under [raw](../evals/convergent-pr-review-2026-07-24/raw/). The results
manifest owns sample identities, scores, aggregate, variance, worst cases,
critical failures, deviations, unavailable telemetry, decisions, and transfer
limits.

## V1

No H1 unit met its frozen contribution bar:

- H1-01: rejected, no control deficit.
- H1-02: rejected, no control defect.
- H1-03: rejected, insufficient contribution at 2/5.
- H1-04: rejected, no control quality deficit.
- H1-05: rejected, insufficient contribution at 1/5.

V1 therefore equals exact M0:
`package-tree-sha256:6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280`.
The protected set is M0-01 through M0-20 plus the independently required
compatibility and relationship surfaces already registered in the campaign
manifest.

## Proof And Boundaries

Prompt 4 changed only authorized evaluation, synthesis, candidate, results,
raw-output, and transcript surfaces. Frozen M0/H1 arms and fixtures remained
byte-identical. No canonical runtime, installed mirror, caller, shared
contract, relationship map, setup, tracker, PR, external system, or Git
delivery surface changed.

Portable atomic dirty-tree capture, external-state completeness, authenticity,
statistical independence, a universal reviewer count, and multi-round truth
remain outside the claim.

```text
Authorized unit completed: Deploy Prompt 4: Prove M0 And H1
Decision: accepted
Campaign shape: hypothesis-candidate
Runtime identities: current=canonical=git-tree:d2210fc11b357f1e2f69408a8a21bd9d422c677a; installed=current-content-equivalent@sha256:42d2c56f8313fb35dbb4f5033f7ed48b81043466ca8becb8c4a38075acee44a9; M0=package-tree-sha256:6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280; H1=package-tree-sha256:379474917dc540ef9704a74628af11e123db11fc9e800a94b797278c1ab05c82; V1=package-tree-sha256:6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280; P1=pending
Artifacts changed: docs/validation/evals/convergent-pr-review-2026-07-24/campaign-manifest.json; candidate.md; results.json; raw/**; docs/synthesis/skills/convergent-pr-review.md; this transcript
Evidence used or reused: exact Prompt 1 M0 specification; exact Prompt 2 research/synthesis admission only; exact Prompt 3 runtime and fixture identities; 25 valid M0 viability samples; 15 M0 contribution controls; 10 gated H1 samples; one zero-credit V09 assembly-deviation output
Residual gaps: unavailable exact model/reasoning identifiers; bounded fixture transfer; portable atomic/external-state/authenticity/statistical-independence/universal-count/multi-round claims; P1, promotion, installation, and Git delivery
Recommended next unit: Deploy Pruning Pass
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: M0 is viable and every H1 unit was rejected under its frozen control or contribution gate, so V1 equals exact M0; stop before pruning
```
