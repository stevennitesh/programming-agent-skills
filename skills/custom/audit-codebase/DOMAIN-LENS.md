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

Vocabulary preference alone is insufficient. A finding must identify the
accepted authority and the behavior, ownership, or decision it obscures or
contradicts.

Examples: `account` is problematic where accepted language distinguishes
Customer from User only when it obscures behavior or ownership. Code that
cancels a whole Order where the authoritative model permits partial cancellation
is an Implementation Contradiction.

## Decision Boundary

Code and tests are not authority merely because they describe current behavior;
honor acceptance tests, schemas, or code contracts that repository authority
explicitly designates. When a candidate needs a term, Invariant, Bounded Context, Context
Relationship, or ADR trade-off settled, record the exact collision and
consequences. Suggest the natural decision owner and stop. Audit never mutates
domain records and treats a returned Domain Delta only as evidence.
