# Improve Codebase Routing Evaluation

Date: 2026-07-18

## Claim

`$improve-codebase` should use one `$grill-with-docs` relationship for every selected user-owned decision while preserving its other resolver and terminal-route predicates. The composer should continue running `$grilling` with `$domain-modeling` active throughout, including when no durable domain change is expected.

## Runtime And Arms

Five fresh-context, read-only direct-agent samples ran per arm with inherited root model and settings, `fork_turns="none"`, and no model override. Both arms received the same five selected-candidate cases and output contract. Control samples loaded the still-unsynchronized installed package with separate `$grilling` and `$grill-with-docs` caller edges. Candidate samples loaded only the simplified working-tree package. No sample modified files or executed a downstream skill.

Control Git blob hashes:

- `improve-codebase/SKILL.md`: `c506eb43354d651486b62180e5f82db418664161`
- `improve-codebase/SELECTED-CANDIDATE.md`: `31fb640d7e12e0a049b111bf80c12e4704dc1416`
- `grill-with-docs/SKILL.md`: `4e7896334f7498f9597daf731bface64298bcfb6`

Candidate Git blob hashes:

- `improve-codebase/SKILL.md`: `24865f2d6f564686cf03b8f8fd40d41ccedec149`
- `improve-codebase/SELECTED-CANDIDATE.md`: `68a3f6eecb182e285797aa241e4eface563e4c26`
- `grill-with-docs/SKILL.md`: `4e7896334f7498f9597daf731bface64298bcfb6`

## Scenario

Each sample routed five hypothetical selected candidates:

1. one conversation-only user commitment or trade-off with no durable domain change expected;
2. one canonical domain term or ADR decision requiring durable capture;
3. one settled direction needing a durable parent specification before slicing;
4. multiple interdependent unresolved decisions or prerequisites requiring multi-session tracking;
5. one supported `Concentrate` candidate needing interface or seam design.

Every sample also had to distinguish the immediate `$improve-codebase Candidate N from <absolute-report-path>` pickup from the resolver or terminal route and name composed inner skills when applicable.

## Rubric And Results

| Behavior | Control | Candidate |
| --- | ---: | ---: |
| Preserve the immediate `$improve-codebase` pickup | 5 / 5 | 5 / 5 |
| Use one `$grill-with-docs` caller edge for both user-decision cases | 0 / 5 | 5 / 5 |
| Keep `$grilling` and `$domain-modeling` active for every user decision | 0 / 5 | 5 / 5 |
| Preserve durable domain and ADR handling | 5 / 5 | 5 / 5 |
| Route settled specification work to `$to-spec` | 5 / 5 | 5 / 5 |
| Route multi-decision fog to `$wayfinder` | 5 / 5 | 5 / 5 |
| Route interface or seam design to `$codebase-design` | 5 / 5 | 5 / 5 |
| Start no downstream skill | 5 / 5 | 5 / 5 |
| **Total** | **30 / 40** | **40 / 40** |

The executable relationship map fell from two improve-codebase user-decision edges to one. The composer edges remained unchanged.

## Observed Behavior

Every control sample sent the conversation-only case directly to `$grilling` and the durable-domain case to `$grill-with-docs`. Every candidate sample sent both cases to `$grill-with-docs`, named `$grilling` and `$domain-modeling` as its active composed skills, and allowed an empty domain delta without conditionally skipping domain-modeling.

Both arms preserved `$to-spec` for settled specification work, `$wayfinder` for interdependent decision fog, `$codebase-design` for interface design, report reconciliation ownership in `$improve-codebase`, and the terminal no-execution boundary.

## Variance And Residual Gap

Both arms had zero routing variance. The candidate deliberately spends domain-modeling legwork on conversation-only decisions in exchange for one caller relationship and one resolution category. Domain writes and ADR creation remain protected by `$domain-modeling`'s existing gates.

This evaluation covers selected-candidate relationship simplification. Survey classification, report rendering, stale-candidate handling, and downstream execution remain covered by structural tests and the earlier improvement-workflow evaluation.
