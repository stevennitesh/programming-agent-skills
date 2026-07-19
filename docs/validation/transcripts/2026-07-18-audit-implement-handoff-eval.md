# Audit Implement Handoff Evaluation

Date: 2026-07-18

## Claim

When an audit has verified exactly one bounded ready remediation, it should suggest `$implement` as the complete delivery owner instead of exposing `$tdd` as a peer handoff. `$implement` owns any internal TDD choice.

## Runtime And Candidate

Five fresh-context, read-only direct-agent samples ran per arm with inherited root model and settings. The evidence packet and requested output were identical. Candidate samples read the canonical `$audit-codebase` skill and disclosed handoff contract.

- `SKILL.md`: `ce5c09b42db600dc73f4b1657498764f31fdcd2daf93cfad3e27b94395c868ea`
- `DEFECT-CONTRACT.md`: `94df2b38378c6e733e745b326da65c0c16acf9924ac3a7fc5f4c2cd04d3c106b`

## Scenario

The terminal audit contained one verified P1 defect. Expected behavior, exact symptom, cause, and a trusted red-capable reproduction were known; the remediation was exactly one bounded ready item. The user asked which single skill to invoke next to get it fixed completely.

## Rubric And Results

| Behavior | Control | Candidate |
| --- | ---: | ---: |
| Select `$implement` as the complete delivery owner | 0 / 5 | 5 / 5 |
| Keep `$tdd` internal rather than exposing it as the audit handoff | 0 / 5 | 5 / 5 |
| Return exactly one skill | 5 / 5 | 5 / 5 |
| **Total** | **5 / 15** | **15 / 15** |

Every control selected `$tdd`, focusing on the red-capable reproduction. Every candidate selected `$implement`, focusing on the bounded ready remediation. No candidate emitted a second route or workflow chain.

## Variance And Residual Gap

There was no within-arm variance. This evaluation covers the ready single-remediation boundary only. Uncertain diagnosis, unsettled intent, multi-slice work, and foggy programs retain their distinct owners in the audit handoff table.
