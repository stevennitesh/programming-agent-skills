# Domain Context Format

Follow the repository's routed domain-document format. When no format exists, use the fallbacks below for settled, context-scoped language, behavior, invariants, responsibilities, and relationships. Keep unresolved meaning in the Domain Delta.

## Single-Context Fallback

Use root `CONTEXT.md`:

```md
# <Context name>

<Model, responsibility, and boundary.>

## Language

### <Canonical term>

<Precise project meaning, behavior, and boundary.>

_Avoid_: <ambiguous or rejected synonym>

## Invariants

- <Settled rule owned by this context.>
```

Omit `## Invariants` when no settled load-bearing rule needs durable capture.

## Multi-Context Fallback

Use root `CONTEXT-MAP.md` to route each context's record:

```md
# Context Map

## Contexts

- [<Context>](<path>/CONTEXT.md) - <owned model and responsibility>

## Relationships

### <Context A> <-> <Context B>

Interaction: <A -> B | B -> A | bidirectional | none>
Responsibilities: <what each context owns>
Contract: <what crosses the boundary>
Language: <owner, reference, or explicit translation>
Authority: <controlling owner, or joint owners and change rule>
Pattern: <recognized DDD pattern when one fits>
```

`Pattern` is optional. Recognized Context Mapping patterns are:

- **Partnership:** contexts coordinate evolution and share success or failure.
- **Shared Kernel:** contexts share an explicitly bounded model subset under joint change control.
- **Customer/Supplier Development:** downstream priorities influence the upstream provider's plan.
- **Conformist:** downstream adopts the upstream model without influence over it.
- **Anticorruption Layer:** a translation boundary protects one model from another.
- **Open-host Service:** an upstream context exposes a broadly usable integration protocol.
- **Published Language:** contexts share a documented interchange language.
- **Separate Ways:** contexts deliberately integrate nothing.
- **Big Ball of Mud:** a boundary contains an incoherent model instead of pretending it is well-structured.

Patterns may combine when each relationship is true. `Translation` belongs in the language mapping; it is not itself a Context Mapping pattern. Omit `Pattern` rather than force a false label.

Select patterns from model behavior, not organizational influence alone:

- Use **Conformist** only when downstream adopts the upstream model as its own. A boundary that translates into a distinct local model is an **Anticorruption Layer**, not Conformist for that interaction.
- Use **Open-host Service** only when upstream intentionally exposes a general protocol for multiple consumers. A versioned or published schema alone does not establish it.

## Representation Rules

- Record only settled canonical meaning, ownership, material conflicts, and decision authority.
- Define domain behavior and boundaries independently of implementation.
- Use one canonical term inside its context; list rejected synonyms under `_Avoid_`.
- Keep generic technical vocabulary, ordinary words without context-specific meaning, and code indexes out.
- Let one context own canonical meaning; consumers reference it through the relationship contract.
- Define each local term and mapping when contexts translate.
- Repeat definitions only for a genuine Shared Kernel with explicit joint control.
- Add language subheadings only when natural groups emerge.

Rendered output names the target, insertion or replacement scope, complete wording, affected relationships, and ordering dependency. Unclear meaning, ownership, relationship, or authority stays unresolved in the Domain Delta.
