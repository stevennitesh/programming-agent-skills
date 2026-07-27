# Simplification Lens

Understand the full supported flow first. Then stop at the first sufficient
reduction that preserves behavior and safety.

## Concepts

- **YAGNI:** remove behavior, configurability, compatibility, or abstraction
  that no supported need requires.
- **KISS:** prefer the simplest correct shape over clever or speculative
  machinery.
- **DRY:** concentrate one duplicated policy at its actual owner; do not create
  a generic abstraction merely because syntax repeats.
- **Readability First:** optimize for clear names, visible contracts, and
  unsurprising control flow, not code golf.
- **Repository Reuse:** use the helper, type, pattern, or owner already present
  in the codebase before creating another.
- **Standard Library:** use a language/runtime capability whose supported
  semantics fit.
- **Native Platform:** prefer a browser, framework, database, operating-system,
  or deployment capability when it already owns the behavior.
- **Installed Dependency:** reuse a dependency already justified by the
  repository before adding another or rebuilding it.
- **Collapse:** remove a pass-through boundary or concentrate one duplicated
  decision at its narrowest existing owner.
- **Known Ceiling:** a deliberate simple choice has an explicit limit and a
  **Revisit Trigger** that says when a more complex shape becomes justified.

## Reduction Ladder

1. delete behavior proved stale or unsupported;
2. Repository Reuse;
3. Standard Library;
4. Native Platform, framework, or database capability;
5. Installed Dependency;
6. collapse duplicate policy into its narrowest current owner;
7. deepen, merge, inline, or retain the current Module shape;
8. propose the smallest local reduction that holds.

Two rungs work: choose the earlier sufficient one. A shorter option that fails
edge cases, compatibility, or safety does not hold.

## Examples

- a third-party parser used only for supported ISO timestamps:
  Python's `datetime.datetime.fromisoformat()` may be the Standard Library
  replacement.
- a repository abstraction with one Implementation, no required substitution,
  and only pass-through forwarding: apply YAGNI and the Deletion Test, then
  inline the unearned boundary after proving behavior. One Implementation
  alone is insufficient evidence.
- a custom slug formatter beside the repository's canonical `slugify`:
  Repository Reuse preserves project-specific accent handling that a new regex
  may silently lose.
- an O(n²) scan accepted for tiny bounded input: retain it with a Known Ceiling
  and Revisit Trigger such as “profiled p95 exceeds the budget at 10k rows.”

## Stale And Dead Code

Use `delete` only with reachability and registration evidence. Use `reuse`,
`stdlib`, `native`, `yagni`, `collapse`, or `shrink` as strong candidate
concepts, but describe the supported behavior and proof rather than emitting a
tag alone.

Do not fabricate `net -N lines` or dependency savings. A per-repository number
requires a verified patch or mechanical count.

## Floors

Never trade away comprehension, Trust Boundary validation, data-loss
prevention, security, accessibility, durability, compatibility, physical
calibration, or the smallest meaningful Behavior Test.
