# Durable decisions

Use when producing a specification, domain update, or decision record. Capture
what future readers need to preserve the agreed result; choose the format and
level of detail for its consumers.

## Choose the owner

Follow repository conventions and reuse an existing useful owner. When no location
is established, choose a proportionate home within the authorized scope. Let the
content and its consumers determine the structure. If the intended destination is
unavailable, keep an accessible draft and report that limit.

For domain definitions or ADR rationale, use
[Domain meaning and decision records](domain-modeling.md). For conflicting or
displaced current sources, use [Document reconciliation](document-reconciliation.md).

## Make the specification useful

A requested specification is a deliverable, not merely an outline or interview
transcript. Capture the goal and relevant users or workflow, scope and exclusions,
agreed features and behavior, consequential constraints, acceptance, and material
uncertainty as applicable. Include concrete scenarios or rationale where their
omission would let an implementer satisfy the words but miss the intended result.

Distinguish accepted decisions, recommendations, assumptions, and unresolved
choices. Do not promote a suggested mechanism or unanswered proposal into a
requirement. Link maintained domain and decision owners rather than copying them.
A small example, schema, or state table can carry meaning more precisely than prose.

Read the result as a future implementer: the intended outcome and evidence should
be recoverable without guessing product policy. Mark readiness honestly when a
consequential decision remains open.

## Keep planning adaptable

Shaping may establish product priorities, stages, and dependencies that affect the
accepted outcome. A delivery outline can help explain feasibility or order of
work; distinguish accepted sequencing constraints from a suggested approach.

The execution lead owns implementation sequencing, assignments, checkpoints, and
run state, using cost-aware-coding when selected. Those decisions may adapt as
evidence changes. Ordinary planning does not require that workflow.

Keep speculative file lists, model settings, worker state, and orchestration
mechanics out of the durable product contract. A plan can live alongside the spec
or in the same document if their roles remain clear; separate files are optional.

## Persist within authority

Write the requested local artifact under repository rules. External tracker or
publication effects need authority for that target. Preserve divergently owned
content and unrelated work; inspect actual state before retrying an uncertain
write, and verify consequential persisted content at its intended destination.

A saved record does not itself establish acceptance, readiness, or permission for
implementation, ticketing, delegation, commit, push, or deployment.
