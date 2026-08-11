---
name: codebase-design
description: "Design one bounded module behind a small caller-facing interface. Use when choosing one specific module's responsibilities, interface, state or failure policy, seam, adapter, migration, or caller-facing proof surface, or when another skill needs shared deep-module vocabulary."
---

# Codebase Design

Own one outcome: a terminal design packet for one bounded Module or Interface
question. Recommend a stronger shape, retain the current one, or name the exact
decision or evidence gap that prevents judgment.

Default to read-only design. The user or caller owns public-contract
commitments, design acceptance, implementation, and downstream mutations.

Use Direct Design before planning or implementation only when one consequential
responsibility, Interface, Seam, migration, or caller-facing proof question
remains unresolved.

A clear repository-native path earns no design pass. When another workflow
loads this skill, fold its vocabulary or supported Direct Design result into
the caller's artifact or Return and create no separate workflow step, design
packet, tracker item, or implementation edge.

For codebase-wide mapping and improvement discovery, recommend `$audit-codebase`
and stop.

## Vocabulary

Use repo and domain terms for business concepts and existing code. Use these
terms for architecture claims:

- **Module** — an interface plus its hidden implementation; scale may be a
  function, class, package, workflow, or tier-spanning slice.
- **Interface** — everything callers must know: operations, inputs, outputs,
  invariants, ordering, errors, configuration, performance, and behavior.
- **Implementation** — behavior and design decisions hidden behind the
  interface through **information hiding**. Use **adapter** only when its role
  at a seam matters.
- **Depth** — coherent functionality relative to interface burden. Depth
  is a property of the interface, not implementation size.
- **Seam** — where behavior can vary without editing callers; the interface
  lives here.
- **Adapter** — a concrete implementation satisfying an interface at a seam.
- **Change amplification**, **cognitive load**, and **unknown unknowns** — the
  three symptoms of complexity: how many places a supported change touches,
  how much information a developer must hold in mind, and whether needed
  information or dependencies are hard to discover.
- **Responsibility** — cohesive behavior, Invariants, decisions, and failure
  policy with one owner.
- **Proof Seam** — the caller-facing boundary where meaning is established;
  unlike a Seam, it does not imply variation or earn an Adapter.

## Taste

- **Deepen.** Prefer deep modules and somewhat general-purpose interfaces that
  reduce special cases without adding capabilities beyond current needs.
- **Delete.** Removing a useful Module exposes or redistributes essential
  complexity; removing a shallow module or pass-through method removes
  accidental complexity.
- **Earn.** Keep a seam or layer only for locality, dependency isolation,
  domain ownership, supported variation, a real external boundary, or
  caller-facing testability unavailable more directly. An Adapter count or
  test double alone does not earn one.
- **Prove.** Treat a test as the first user of the Interface. Use the
  caller-facing Interface as the Proof Seam, prefer state testing through
  observable outcomes, and use interaction testing only when the interaction
  is contractual or isolates a necessary failure.

## Direct Design

For one bounded module, shallow cluster, seam, or interface question, read
[DIRECT-DESIGN.md](DIRECT-DESIGN.md) completely and run its pass.

## Completion

A loaded use is complete when the caller's artifact incorporates the required
vocabulary or design result without transferring ownership. A direct pass is
complete only through [DIRECT-DESIGN.md](DIRECT-DESIGN.md)'s completion
criterion.
