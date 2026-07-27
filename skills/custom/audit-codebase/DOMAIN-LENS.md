# Domain Fidelity Lens

Judge whether code expresses the repository's accepted model. Consume routed
domain records and ADRs; Audit does not create or mutate them.

## Concepts

- **Ubiquitous Language:** one canonical project-specific term and meaning used
  consistently by domain records, code, tests, interfaces, and conversation.
- **Language Collision:** overload, aliasing, implementation leakage, or
  conflicting meanings for one term.
- **Bounded Context:** a coherent model, language, responsibility, and change
  authority. Directory or deployment placement alone does not establish one.
- **Invariant:** a domain truth that every supported transition must preserve.
- **Context Relationship:** interaction direction, responsibilities, contract,
  language ownership, and change authority between Bounded Contexts.
- **Implementation Contradiction:** code or tests behave differently from the
  accepted intended model.
- **ADR Conflict:** a candidate contradicts a durable, surprising,
  hard-to-reverse trade-off already recorded.

## Audit

Trace `CONTEXT.md`, `CONTEXT-MAP.md`, routed context records, governing
specifications, ADRs, code, tests, schemas, and representative flows.

Ask:

- Do code and tests use the Ubiquitous Language, or invent aliases?
- Does one concept mean different things in different callers?
- Are Invariants enforced at their actual owner?
- Do Context Relationships preserve direction, responsibility, contract, and
  language ownership?
- Does implementation contradict accepted meaning?
- Does an opportunity reopen an ADR, and is current friction strong enough to
  justify that decision?

Example: if the glossary distinguishes **Customer** from **User**, code named
`account` may hide a Language Collision. The finding must show which behavior
or ownership is obscured; vocabulary preference alone is insufficient.

Example: if the model allows partial Order cancellation but code cancels the
entire Order, record an Implementation Contradiction against the authoritative
Invariant and supported scenario.

## Decision Boundary

Code and tests are evidence about present behavior, not authority over intended
meaning. When a candidate needs the user to settle a term, Invariant, Bounded
Context, Context Relationship, or ADR trade-off, write the exact collision and
consequences into the candidate's decision brief and recommend
`$grill-with-docs`.

Only `$domain-modeling`, directly or under `$grill-with-docs`, owns durable
domain changes and ADR handling. Audit later records the returned Domain Delta
without claiming its mutations.
