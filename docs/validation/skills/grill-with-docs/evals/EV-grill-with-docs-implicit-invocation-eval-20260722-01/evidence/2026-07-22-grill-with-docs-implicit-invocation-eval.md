# Grill With Docs Implicit Invocation Evaluation

Date: 2026-07-22

Decision: **accept** the narrow implicit-invocation candidate.

## Claim And Fixed Candidate

The candidate should make Grill With Docs discoverable when one direct-user request observably combines a repo-backed grilling interview with active domain capture, without taking conversation-only grilling, settled-domain-only updates, source research, or general design debate.

| Surface | Identity |
| --- | --- |
| Control revision | `de49269f5c3fb58d3c8d9d32eca868b808fcb53a` |
| Control `SKILL.md` blob | `1c095a21c9b797cd151d03bc1b4ab9279c8adc70` |
| Control metadata blob | `5b1f887a9138416870f64ba2fe21602e4a59cfa7` |
| Candidate `SKILL.md` SHA-256 | `4282dfc2c6efee78f38fe69fd208e4d126649ed982c1a2b7f9e10515fab0f01a` |
| Candidate metadata SHA-256 | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` |

The control catalog omitted Grill With Docs because its policy disabled implicit invocation. The candidate catalog added exactly this eligible description:

> Use when a request combines grilling one repo-backed decision with keeping its domain language, invariants, or relationships current; exclude conversation-only grilling and settled-domain-only work.

## Fixed Protocol

Five fresh control contexts and five fresh candidate contexts independently routed the same six requests to one eligible skill or `none`, without executing a skill, inspecting files, using tools, or mutating state. Both arms inherited the root model, reasoning settings, runtime, and authority. Exact backend build telemetry was unavailable.

The fixed cases were:

| Case | Request class | Required route |
| --- | --- | --- |
| A | Pressure-test a repository definition and keep its domain language current while settling it | `grill-with-docs` |
| B | Relentlessly question a repository term and capture accepted invariants and relationships while converging | `grill-with-docs` |
| C | Grill a presentation outline with no repository docs or durable capture | `grilling` |
| D | Update an already-settled domain term with no interview | `domain-modeling` |
| E | Research an official meaning and write a cited note | `none` in the bounded catalog |
| F | Debate a general architecture choice without updating project documentation | `none` |

Any missed combined case or any Grill With Docs selection for C-F was critical. Candidate language, expected routes, prior outputs, and conclusions were absent from control contexts. Root judgment used the fixed route rubric above.

## Per-Sample Results

`P` means the route matched the rubric; `F` means it did not.

| Arm / sample | A | B | C | D | E | F | Critical failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Control C1 | F | F | P | P | P | P | yes |
| Control C2 | F | F | P | P | P | P | yes |
| Control C3 | F | F | P | P | P | P | yes |
| Control C4 | F | F | P | P | P | P | yes |
| Control C5 | F | F | P | P | P | P | yes |
| Candidate N1 | P | P | P | P | P | P | no |
| Candidate N2 | P | P | P | P | P | P | no |
| Candidate N3 | P | P | P | P | P | P | no |
| Candidate N4 | P | P | P | P | P | P | no |
| Candidate N5 | P | P | P | P | P | P | no |

Control routing for A was `domain-modeling` in all five samples. Control routing for B was `domain-modeling` in four samples and `grilling` in one. Every control routed all four adjacent negatives correctly. Every candidate selected Grill With Docs for both combined cases and preserved all adjacent routes.

## Aggregate And Decision

| Claim family | Control | Candidate |
| --- | ---: | ---: |
| Combined-request discovery | 0/10 | 10/10 |
| Adjacent-negative exclusion | 20/20 | 20/20 |
| Fully passing samples | 0/5 | 5/5 |

Variance narrowed on the combined cases and remained zero on adjacent negatives. The worst candidate result passed all six cases. There were no protocol deviations or new critical failures.

**Accept.** Enable implicit invocation and retain the dual-condition description with its two nearest exclusions. Keep direct-user admission, component ownership, caller recommendation-only edges, Return, and completion unchanged.

## Residual Gap

This is a bounded catalog-routing evaluation, not telemetry from repeated live saved-prompt use. Revisit the predicate only if real use reveals a missed dual-component phrase or an adjacent false fire.

## Mechanical Verification And Install

```text
focused Grill With Docs and relationship contracts
2 passed

python -m scripts.validate_skills
Skill validation passed.

python -m pytest
191 passed, 4 skipped

managed install dry-run after synchronization
Unchanged skills: 25

canonical/installed SHA-256 parity
SKILL.md: match
agents/openai.yaml: match

git diff --check
passed

git diff --cached --check
passed
```
