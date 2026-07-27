# Audit Pruning Equivalence Evaluation

Date: 2026-07-18

## Claim

The pruned `$audit-codebase` package should preserve the unpruned v2 behavior while removing duplicated runtime prose and strengthening its leading words.

## Runtime And Arms

Five fresh-context, read-only direct-agent samples ran per arm with inherited root model and settings. Both arms received the same comprehensive terminal-audit packet and output request. The control read the unpruned installed mirror; the candidate read the pruned canonical package. No sample modified files.

Control hashes:

- `SKILL.md`: `ce5c09b42db600dc73f4b1657498764f31fdcd2daf93cfad3e27b94395c868ea`
- `DEFECT-CONTRACT.md`: `94df2b38378c6e733e745b326da65c0c16acf9924ac3a7fc5f4c2cd04d3c106b`
- `PERFORMANCE-LENS.md`: `e8fbb6c24726fb564764688077438f802a34e516c362657f84938489b7e05e6e`
- `HTML-REPORT.md`: `d59017ff1a048a84b48803db8107d698e0a532dfe98668173279ef0b7d1cde62`

Candidate hashes:

- `SKILL.md`: `637a1462c6aa54b2e6f83b1cfce7b0e75809f402eb5a51b1b4f5b5558d052e64`
- `DEFECT-CONTRACT.md`: `a74e8f15e40259946169dd94fd8440dbea7ec7f5835c749e5ffab2b1cfd7f5b5`
- `PERFORMANCE-LENS.md`: `820133c2788ff1979a533b1b0ac1411a8a0e9333cd6416f8737bcd800b7759d6`
- `HTML-REPORT.md`: `4144131d6abc622892f2feb0bb33cbbce4002aba15f87fd09ceee46772edf185`

Runtime prose fell from 2,241 to 1,841 words, an 18 percent reduction. The candidate introduced `Terminal`, `Root-owned`, `Chain of custody`, `Burden Of Proof`, `Like-for-like`, and `Ledger, not leaderboard` as leading anchors.

## Scenario

The immutable, drift-free snapshot had full Charter coverage and a verified report. Its ledger contained a user-owned P0 domain decision, one ready P1 remediation, one measured ready P3 performance remediation, one nonblocking measured performance opportunity, one runnable performance gap, one settled multi-slice cluster, one foggy multi-decision cluster, one external-fact gap, and one unowned low-severity finding.

## Rubric And Results

| Behavior | Control | Candidate |
| --- | ---: | ---: |
| Return coverage status without a release decision | 4 / 5 | 5 / 5 |
| Preserve every defect, advisory, gap, and cluster classification | 5 / 5 | 5 / 5 |
| Preserve exact immediate owners and `none` | 5 / 5 | 5 / 5 |
| Preserve the complete HTML ledger, coverage matrix, and no-ranking boundary | 5 / 5 | 5 / 5 |
| Preserve terminal no-mutation and no-downstream boundaries | 5 / 5 | 5 / 5 |
| **Total** | **24 / 25** | **25 / 25** |

Every sample chose `$grill-with-docs`, `$implement`, `$prototype`, `$to-tickets`, `$wayfinder`, `$research`, and `none` under the intended predicates. Every sample retained cluster members, kept the performance opportunity severity-free, required caller selection, and started nothing.

## Variance And Residual Gap

One control marked the audit `incomplete` because it treated reportable evidence gaps as contradicting the prompt's explicit statement that every required gate closed. All candidate samples honored the stated Charter premise while preserving reduced confidence where appropriate. No candidate omitted a gate, schema, item, route, or terminal boundary.

The evaluation covers terminal synthesis and reporting, where most pruning occurred. Pin mechanics and delegated root-only refusal remain protected structurally and by the earlier v2 evaluations.
