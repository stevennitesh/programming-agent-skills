# CONTEXT.md Format

`CONTEXT.md` is the project's glossary for resolved ubiquitous language.

## Structure

```md
# <Context name>

<One or two sentences describing the context and why it exists.>

## Language

### <Canonical term>

<Precise project meaning and boundary.>

_Avoid_: <ambiguous or rejected synonym>
```

## Writing Rules

- **Resolve:** Record only terms whose canonical name, definition, owning context, and material conflicts are settled.
- **Canonicalize:** Pick one term and list rejected synonyms under `_Avoid_`.
- **Define:** Use one or two sentences describing what the concept is, independent of implementation.
- **Scope:** Include only concepts specific to the domain context.
- **Cluster:** Add subheadings when natural groups emerge; keep one cohesive area flat.

## Single vs Multi-Context Repos

Single-context repos use one root `CONTEXT.md`.

Multi-context repos use a root `CONTEXT-MAP.md` that points to each context's `CONTEXT.md`:

```md
# Context Map

## Contexts

- [<Upstream context>](<path>/CONTEXT.md) - <owned language and responsibility>
- [<Downstream context>](<path>/CONTEXT.md) - <owned language and responsibility>

## Relationships

### <Upstream context> -> <Downstream context>

Relationship: <customer-supplier | conformist | shared kernel | translation>
Contract: <what crosses the boundary>
Owner: <who controls the contract>
```

Use `CONTEXT-MAP.md` to route terms and record resolved context relationships. Create or update it when a context boundary or relationship resolves. Update every relevant glossary when a term crosses contexts. Keep unclear ownership unresolved and surface it in the domain delta.
