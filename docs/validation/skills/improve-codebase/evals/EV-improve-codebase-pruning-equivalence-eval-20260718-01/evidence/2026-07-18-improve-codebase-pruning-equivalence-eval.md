# Improve Codebase Pruning Equivalence Evaluation

Date: 2026-07-18

## Claim

The pruned `$improve-codebase` package should preserve survey, report, selected-candidate, routing, and mutation behavior while replacing repeated prose with stronger leading words.

## Runtime And Arms

Five fresh-context, read-only direct-agent samples ran per arm with inherited root model and settings, `fork_turns="none"`, and no model override. Both arms received the same six-region survey, selected-candidate matrix, and output request. Control samples loaded the unsynchronized installed package; candidate samples loaded only the pruned canonical package. No sample modified files or executed a downstream skill.

Control Git blob hashes:

- `SKILL.md`: `24865f2d6f564686cf03b8f8fd40d41ccedec149`
- `SELECTED-CANDIDATE.md`: `68a3f6eecb182e285797aa241e4eface563e4c26`
- `HTML-REPORT.md`: `f8de11fe550e983132094b0966a6ab6693bc1990`

Candidate Git blob hashes:

- `SKILL.md`: `d87b8584b02f0bde8663e391971b333b98a3e691`
- `SELECTED-CANDIDATE.md`: `b9df2221db520b6140d6d9cccf68b0108fd6a554`
- `HTML-REPORT.md`: `20ac96e06ea2943eb7cd0f800d838075417f10f6`

Runtime prose fell from 2,065 to 1,702 words, an 18 percent reduction. The candidate strengthened `Caller bound wins`, `Ledger`, `Destination`, `Verify`, `Terminal`, `Stale`, `Resolve at most one blocker`, `Honor overlap`, `Offline`, and `Dark and accessible` as execution anchors.

## Scenario

The Survey contained an eliminable pass-through, a caller-spread responsibility to concentrate, an earning boundary, one exact external-source question preparatory for the concentration, work absorbed by that concentration, and residual work after it. Samples had to account for every region, choose cards and ranking, preserve the immediate candidate pickup, verify the HTML report, and hold the mutation boundary.

The selected-candidate matrix covered `none`, repository, source, runnable, user-decision, and design resolution needs; multi-decision fog; every final disposition and Concentrate work shape; overlap; stale evidence; reconciliation; return fields; and terminal no-execution behavior.

## Rubric And Results

| Behavior | Control | Candidate |
| --- | ---: | ---: |
| Account for every region and card only actionable dispositions | 5 / 5 | 5 / 5 |
| Preserve Preparatory, Absorbed, and Residual sequencing | 5 / 5 | 5 / 5 |
| Preserve ranking, Top recommendation, and exact survey pickup | 5 / 5 | 5 / 5 |
| Preserve HTML verification and mutation boundaries | 5 / 5 | 5 / 5 |
| Preserve zero-or-one resolver cardinality and resolver ownership | 5 / 5 | 5 / 5 |
| Preserve every terminal route, verdict, and no-execution boundary | 5 / 5 | 5 / 5 |
| Preserve reconciliation and return packet requirements | 5 / 5 | 5 / 5 |
| **Total** | **35 / 35** | **35 / 35** |

## Observed Repair

The first candidate wording used `Resolve one blocker`. Two of five samples interpreted that as requiring a resolver even for `resolution need: none`. The final wording, `Resolve at most one blocker`, restored the original cardinality; all five fresh final samples explicitly allowed zero or one resolver.

The initial pruning also replaced the literal CSS declaration with a general dark-theme instruction. The structural test exposed the lost browser-level accessibility contract, so `color-scheme: dark` was restored before the final samples.

## Variance And Residual Gap

Both final arms had zero rubric variance. Some samples in both arms invented concrete pickup syntax for delivery routes whose exact template is not fixed by the skill; this is pre-existing model variance, not a pruning regression. The contract fixes exact syntax only for the immediate survey pickup and `$simplify-code` route.

The evaluation covers instruction-level synthesis rather than rendering a real repository report. Static tests protect the HTML schema, anchors, explicit invocation policy, relationships, and required route literals.
