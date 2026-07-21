# Domain Context Format

Use domain records for resolved, context-scoped ubiquitous language, behavior, invariants, responsibilities, and relationships. Keep unresolved meaning in the Domain Delta.

## Single Context

A single-context repository uses root `CONTEXT.md`:

```md
# <Context name>

<One or two sentences describing the model, responsibility, and boundary.>

## Language

### <Canonical term>

<Precise project meaning, behavior, and boundary.>

_Avoid_: <ambiguous or rejected synonym>

## Invariants

- <Settled rule owned by this context.>
```

Omit `## Invariants` when no settled load-bearing rule needs durable capture.

## Multi-Context Map

A multi-context repository uses root `CONTEXT-MAP.md` to route each context's `CONTEXT.md`:

```md
# Context Map

## Contexts

- [<Context>](<path>/CONTEXT.md) - <owned model and responsibility>

## Relationships

### <Upstream context> -> <Downstream context>

Relationship: <customer-supplier | conformist | shared kernel | translation | custom>
Contract: <what crosses the boundary>
Language: <owner | reference | translation | shared kernel>
Authority: <controlling owner | joint owners and change rule>
```

Use a custom relationship label only when the preferred labels are false; define its meaning, contract, and authority.

## Representation Rules

- **Resolve:** Record only settled canonical meaning, owning context, material conflicts, and decision authority.
- **Model:** Define domain behavior and boundaries independently of implementation. Record context-owned invariants only when they constrain valid behavior.
- **Canonicalize:** Use one canonical term inside its context and put rejected synonyms under `_Avoid_`.
- **Scope:** Keep generic technical vocabulary, ordinary words without context-specific meaning, and code indexes out.
- **Own:** One context defines canonical meaning; consumers reference it through the relationship contract instead of copying it.
- **Translate:** When contexts use different models, define each local term and the mapping between them.
- **Govern:** Repeat shared definitions only for a genuine shared kernel with explicit joint owners and a change rule.
- **Cluster:** Add language subheadings only when natural groups emerge; otherwise keep the context flat.

Rendered output names the target path, insertion or replacement scope, complete wording, affected relationships, and ordering dependency. Unclear meaning, ownership, relationship, or authority remains unresolved in the Domain Delta.
