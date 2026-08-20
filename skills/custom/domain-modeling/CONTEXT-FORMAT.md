# Domain context format

Follow the repository's routed format. Use these fallbacks only when no format
exists and a non-obvious durable distinction would likely be misapplied without
a record.

A context record owns current semantic meaning, defining behavior, invariants,
responsibility, and material relationships. It does not own executable
procedure, algorithm specifications, commands, mutable work state,
implementation inventories, change history, or decision rationale.

## Single-context fallback

Use root `CONTEXT.md`:

```md
# <Context name>

<Model, responsibility, and boundary.>

## Language

### <Canonical term>

<Project-specific meaning, defining behavior, and boundary.>

_Avoid_: <ambiguous or rejected synonym>

## Invariants

- <Settled rule that remains true across implementation changes.>
```

Omit empty sections.

## Multi-context fallback

Use root `CONTEXT-MAP.md` to route each context record:

```md
# Context Map

## Contexts

- [<Context>](<path>/CONTEXT.md) - <owned model and responsibility>

## Relationships

### <Context A> <-> <Context B>

<Direction, responsibility, crossing contract, language translation, or change
authority needed to keep the boundary unambiguous.>
```

Name a recognized DDD Context Mapping pattern only when the repository already
uses one or the label clarifies ownership or translation. Never force a pattern.
Translation into a distinct local model is an Anticorruption Layer, not
Conformist. A versioned or published schema alone does not establish an
Open-host Service.

## Representation rules

- Reconcile with routed current records. Revise or remove covered or conflicting
  material rather than append a parallel definition.
- Record only settled project-specific meaning and implementation-stable domain
  behavior, invariants, ownership, boundaries, or relationships.
- Use one canonical term inside a context. Preserve independent meanings across
  contexts unless an explicit relationship or Shared Kernel joins them.
- Define the local term and translation when contexts use different language.
- Keep generic technical vocabulary, ordinary words, implementation layout,
  procedures, rationale, and code indexes out.
- Add subheadings only when natural groups emerge.

Rendered output includes only the target, replacement or insertion scope,
wording, and relationship or ordering effect needed to apply the material
delta. Unclear meaning or authority remains an unresolved question.
