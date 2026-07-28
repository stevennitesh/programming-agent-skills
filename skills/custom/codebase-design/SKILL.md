---
name: codebase-design
description: "Design one bounded module behind a small caller-facing interface. Use when choosing one specific module's responsibilities, interface, state or failure policy, seam, adapter, migration, or caller-facing proof surface, or when another skill needs shared deep-module vocabulary."
---

# Codebase Design

Own one outcome: a terminal design packet for one bounded Module or Interface
question. Recommend a stronger shape, retain the current one, or name the exact
decision or evidence gap that prevents judgment.

Default to read-only design. The user or caller owns public-contract
commitments, design acceptance, implementation, and downstream mutations. When
another workflow loads this discipline, fold any vocabulary or Direct Design
result into its artifact and Return; create no separate workflow step.

Use Direct Design before planning or implementation only when one consequential
responsibility, Interface, Seam, migration, or caller-facing proof question
remains unresolved.

For codebase-wide mapping and improvement discovery, recommend `$audit-codebase`
and stop.

## Vocabulary

Use repo and domain terms for business concepts and existing code. Use these
terms for architecture claims:

- **Module** — an interface plus its hidden implementation; scale may be a
  function, class, package, workflow, or tier-spanning slice.
- **Interface** — everything callers must know: operations, inputs, outputs,
  invariants, ordering, errors, configuration, performance, and behavior.
- **Implementation** — behavior hidden behind the interface. Use **adapter**
  only when its role at a seam matters.
- **Depth** — caller and test leverage per unit of interface learned. Depth is a
  property of the interface, not implementation size.
- **Seam** — where behavior can vary without editing callers; the interface
  lives here.
- **Adapter** — a concrete implementation satisfying an interface at a seam.
- **Leverage** — capability gained per unit of interface learned.
- **Locality** — change, bugs, decisions, knowledge, and verification
  concentrated in one place.
- **Responsibility** — cohesive behavior, Invariants, decisions, and failure
  policy with one owner.
- **Proof Seam** — the caller-facing boundary where meaning is established;
  unlike a Seam, it does not imply variation or earn an Adapter.

## Taste

- **Compress.** Reduce what callers learn and coordinate.
- **Delete.** A useful module redistributes its complexity when removed; a
  pass-through removes it.
- **Earn.** Keep a seam or layer only for locality, dependency isolation,
  domain ownership, supported variation, a real external boundary, or
  caller-facing testability unavailable more directly. An Adapter count or
  test double alone does not earn one.
- **Prove.** Use the caller-facing Interface as the Proof Seam. Prefer
  observable outcomes; specify an internal Module directly only when it owns
  independently meaningful behavior.

## Direct Design

For one bounded module, shallow cluster, seam, or interface question, read
[DIRECT-DESIGN.md](DIRECT-DESIGN.md) completely and run its pass.

## Completion

A loaded use is complete when the caller's artifact incorporates the required
vocabulary or design result without transferring ownership. A direct pass is
complete only through [DIRECT-DESIGN.md](DIRECT-DESIGN.md)'s completion
criterion.
