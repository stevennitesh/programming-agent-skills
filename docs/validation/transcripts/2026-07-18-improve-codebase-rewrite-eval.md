# Improve-Codebase Rewrite Behavioral Evaluation

Date: 2026-07-18

Status: passed after one diagnosed contract repair.

Fixed repository point: `c2c096e0aa8d3f6ee8d8665058e8b9f532f5224b` plus the complete uncommitted rewrite diff. The evaluated current-source hashes were:

- `skills/custom/improve-codebase/SKILL.md`: `8a171bbf68900e8abafe1e4772aa08321bac8ae01a9a5b2bf1ad3986869786ce`
- `skills/custom/simplify-code/SKILL.md`: `d77e1449d704b54c0c37a0add5ad8ce3d705cf29eb85da5584acbd67238fe371`
- `skills/custom/codebase-design/SKILL.md`: `72223008c96ed87c498c2618c9dfe0d5fb3de8016282b0475779d858f8bb8357`

Runtime model, reasoning settings, token use, latency, and cost were unavailable.

## Method

A temporary four-region fixture presented the same bounded codebase evidence to fresh-context agents:

- Region A: a removable pass-through wrapper with no distinct policy.
- Region B: duplicated risk-tier rules with a known regression, requiring concentration.
- Region C: an `IdempotencyGuard` boundary earning its existence.
- Region D: vendor ordering behavior requiring external evidence before design.

Five negative-control samples loaded the prior `improve-codebase-architecture` instructions directly from the fixed-point Git object. Five post-repair candidate samples loaded the rewritten current skill. Every sample was instructed to survey read-only, write only its temporary HTML report, account for all four regions, and return the exact next pickup. A separate fresh-context run exercised the selected-candidate branch against one generated report.

## Results

| Behavior | Negative control | Rewritten candidate |
| --- | ---: | ---: |
| Accounted for all four regions with explicit dispositions | 0/5 | 5/5 |
| Identified the eliminable wrapper | 0/5 | 5/5 |
| Assigned every Eliminate candidate to `$simplify-code` | 0/5 | 5/5 |
| Preserved the earned boundary as Retain | 0/5 | 5/5 |
| Held the vendor question as Investigate | 0/5 | 5/5 |
| Left tracked and production files unchanged | 5/5 | 5/5 |
| Returned the exact report-backed pickup | 5/5 | 5/5 |

All five controls reported only the risk-tier deepening opportunity; none surfaced the cleanup opportunity. All five rewritten runs produced the four required outcomes: Concentrate and Eliminate candidate cards, a Retain ledger entry, and an Investigate evidence gap. Each ranked the recurring risk-tier regression above the smaller wrapper deletion, which was consistent with the stated evidence and ranking policy.

The selected-candidate run passed 1/1. It reopened Candidate 2, verified the cited evidence, retained Eliminate, updated the same report, made no production edit, and returned exactly `$simplify-code Candidate 2 from <absolute-report-path>`.

## Diagnosed Failure And Repair

The first candidate batch classified Region A correctly as Eliminate, but some reports named `$tdd` as its provisional next owner. The survey contract had not explicitly bound disposition to owner. The repair added a provisional-owner table to `improve-codebase`, specified that Eliminate always maps to `$simplify-code`, prohibited `$tdd` and `$implement` for Eliminate in the report contract, and added executable regressions. Five fresh post-repair samples then passed the ownership requirement.

## Until-Clean Convergence Follow-Up

A later review identified that `until-clean` had semantic stop reasons but no finite mechanical backstop. The repair added a named Campaign contract, an explicit finite positive cut limit or three successful cuts by default, strict net-reduction evidence, clean exhaustion, diminishing-return and oscillation gates, a one-failed-cut stop, budget accounting, and residual handoff.

Five fresh-context controls loaded the pre-repair installed skill at SHA-256 `74a1adbd1fa5124e8291f2a19b0bbc6b8f347392a595ec0799651a51c9d46725`. Five candidate samples loaded the repaired canonical skill at SHA-256 `3203c1246704f4e75835c1b0c8de04c3a9c0618618ead2d6c54823f440311bf7`. Each received the same bounded hypothetical campaign: three successful proved cuts, no user-stated numeric limit, and a fourth eligible net-reducing cut.

| Behavior | Pre-repair control | Finite-contract candidate |
| --- | ---: | ---: |
| Continued automatically into a fourth cut | 5/5 | 0/5 |
| Stopped at the default three-cut budget | 0/5 | 5/5 |
| Returned the fourth eligible cut as residual | 0/5 | 5/5 |
| Required a new explicit invocation and budget to continue | 0/5 | 5/5 |

The candidate removed the demonstrated endless-continuation path without suppressing the residual opportunity.

## Residual Evidence Gaps

- The source, runnable-prototype, and human-judgment resolver branches are covered by active contract tests and eval fixtures, but this run did not execute live network research, a throwaway prototype, or an interactive grilling session.
- The finite `until-clean` stop branch is forward-tested, structurally checked, and executable-test covered; no multi-cut production campaign was executed.
- Temporary fixtures and generated reports were deleted after this transcript was recorded. No evaluation artifact was retained as runtime state.
