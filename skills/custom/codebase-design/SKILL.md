---
name: codebase-design
description: "Design deep modules behind small interfaces. Use when the user wants to deepen a bounded module, shape or compare an interface, place a seam or adapter, improve testability through a caller-facing surface, or another skill needs the deep-module vocabulary."
---

# Codebase Design

Design **deep modules**: meaningful behavior behind a small interface, placed at a clean seam, and proved through that interface.

This skill is the **design bench** for one bounded candidate. `$improve-codebase-architecture` owns codebase-wide survey and candidate discovery.

When another skill needs only the vocabulary, apply it inside that caller's workflow. Keep the caller's output and completion criteria authoritative.

## Ownership

- **Codebase design:** Own architecture vocabulary, source-traced analysis, alternatives, recommendation, and the design packet.
- **User or caller:** Own public-contract commitments, design acceptance, implementation, and every tracker, spec, ADR, domain, staging, or commit mutation.
- **Write boundary:** Default to read-only design. Inside an authorized implementation workflow, keep the caller's write scope and gates authoritative.

## Vocabulary

Use repo and domain terms for business concepts and existing code. Use these terms for architecture claims; translate rather than rename established project language.

**Module** - anything with an interface and an implementation: a function, class, package, workflow, or tier-spanning slice.

**Interface** - everything callers must know to use the module correctly: operations, inputs, outputs, invariants, ordering, errors, configuration, performance, and behavior contract.

**Implementation** - behavior hidden behind the interface. Use **adapter** only when the role at a seam is the subject.

**Depth** - leverage at the interface: how much useful behavior callers and tests receive per unit of interface they must understand.

**Seam** - the place where behavior can vary without editing callers. The interface lives at the seam.

**Adapter** - a concrete implementation that satisfies an interface at a seam.

**Leverage** - more capability per unit of interface learned.

**Locality** - change, bugs, decisions, knowledge, and verification concentrated in one place.

## Deep And Shallow

A deep interface compresses caller knowledge:

```python
receipt = checkout.place_order(cart_id, payment_method)
```

A shallow interface makes callers reconstruct the implementation:

```python
cart = carts.get(cart_id)
reservation = inventory.reserve(cart.items)
payment = payments.authorize(payment_method, cart.total)
order = orders.create(cart, reservation, payment)
receipt = receipts.create(order)
```

That sequence may belong inside `checkout`; it is shallow when every caller must know it.

## Taste Gates

- **Caller compression:** A deeper module makes callers learn and coordinate less.
- **Deletion test:** Deleting a useful module redistributes its complexity across callers, tests, or workflows. Deleting a pass-through removes complexity.
- **Interface pressure:** Painful caller-facing tests signal a shallow, coupled, or misplaced interface. Return observable outcomes and inject dependencies only at real seams.
- **Interface is the test surface:** Callers and behavior tests cross the same seam. Test an internal module directly only when it owns behavior worth specifying independently.
- **Real seam:** Locality, dependency isolation, domain ownership, or real variation earns a seam. One adapter suggests a hypothetical seam; production plus a fake, substitute, emulator, or second integration can make it real.
- **Earned indirection:** Merge modules, inline pass-throughs, or keep code boring when another layer adds no leverage, locality, isolation, or testability.

## Direct Design Branch

When the user supplies one bounded module, shallow cluster, seam, or interface question, read [DIRECT-DESIGN.md](DIRECT-DESIGN.md) completely and run its pass.

## Completion Criteria

A reference-only use is complete when the caller's artifact applies the vocabulary consistently without changing the caller's workflow boundary.

A direct design pass is complete only through [DIRECT-DESIGN.md](DIRECT-DESIGN.md)'s completion criterion.
