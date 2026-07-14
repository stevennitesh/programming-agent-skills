---
name: codebase-design
description: "Design one bounded module behind a small caller-facing interface. Use when choosing the interface, seam, adapter, or caller-facing test surface for one specific module, or when another skill needs shared deep-module vocabulary."
---

# Codebase Design

Own one outcome: a recommended shape for one bounded module or interface question. Prefer useful behavior behind a small interface at an earned seam, proved through that interface; merge, inline, or keep the current shape when that is stronger.

Default to read-only design. The user or caller owns public-contract commitments, design acceptance, implementation, and downstream mutations. When loaded only as vocabulary, retain the caller's artifact, mutation boundary, and completion criterion.

For codebase-wide candidate discovery, recommend `$improve-codebase-architecture` and stop.

## Vocabulary

Use repo and domain terms for business concepts and existing code. Use these terms for architecture claims:

- **Module** — an interface plus its hidden implementation; scale may be a function, class, package, workflow, or tier-spanning slice.
- **Interface** — everything callers must know: operations, inputs, outputs, invariants, ordering, errors, configuration, performance, and behavior.
- **Implementation** — behavior hidden behind the interface. Use **adapter** only when its role at a seam matters.
- **Depth** — caller and test leverage per unit of interface learned. Depth is a property of the interface, not implementation size.
- **Seam** — where behavior can vary without editing callers; the interface lives here.
- **Adapter** — a concrete implementation satisfying an interface at a seam.
- **Leverage** — capability gained per unit of interface learned.
- **Locality** — change, bugs, decisions, knowledge, and verification concentrated in one place.

## Taste

- **Compress.** Reduce what callers learn and coordinate.
- **Delete.** A useful module redistributes its complexity when removed; a pass-through removes it.
- **Earn.** Keep a seam or layer only for locality, dependency isolation, domain ownership, real variation, or testability. One adapter is hypothetical; production plus a fake, substitute, emulator, or second integration demonstrates variation.
- **Prove.** Use the caller-facing interface as the test surface. Prefer observable outcomes; specify an internal module directly only when it owns independently meaningful behavior.

## Direct Design

For one bounded module, shallow cluster, seam, or interface question, read [DIRECT-DESIGN.md](DIRECT-DESIGN.md) completely and run its pass.

## Completion

A vocabulary-only use is complete when the caller's artifact applies the terms without transferring ownership. A direct pass is complete only through [DIRECT-DESIGN.md](DIRECT-DESIGN.md)'s completion criterion.
