---
name: codebase-design
description: Design one bounded module or interface when architecture itself is unresolved. Use for an explicit architecture request or a consequential question about ownership, data shape, interface, state or failure policy, seam, or migration; exclude ordinary implementation with a clear repository-native design and codebase-wide discovery.
---

# Codebase Design

Design or retain one bounded module so callers get a small, clear interface
that hides the right behavior, data decisions, state, and failure policy.

Default to read-only design. The user or caller owns public-contract choices,
acceptance, implementation, and downstream mutation. A clear repository-native
shape needs no design pass. For codebase-wide discovery, recommend
`$audit-codebase` and stop.

## Deep modules

A **Module** is an interface plus its hidden implementation. It may be a
function, class, package, workflow, or tier-spanning slice.

- **Interface:** everything callers must know to use the module correctly,
  including operations, inputs, outputs, invariants, ordering, errors, effects,
  configuration, and consequential performance behavior.
- **Implementation:** behavior and decisions hidden from callers.
- **Depth:** useful behavior hidden relative to the interface callers must
  learn. A deep module gives callers leverage without exposing its machinery.
- **Seam:** a place where behavior can vary without editing callers.
- **Adapter:** an implementation that fills a role at a seam.
- **Leverage:** capability callers gain from learning one interface.
- **Locality:** decisions, change, bugs, and proof concentrated in one owner.

Use repository and domain language for real concepts. These terms sharpen an
architecture decision; they do not replace established names merely for
consistency.

## 1. Understand

Trace the requested behavior, current owner, real callers, data flow and access
patterns, state and failures, dependencies, accepted contracts, and existing
proof. Distinguish actual dependence from the intended public contract.

If a material behavior, ownership, or public-contract choice is unsettled,
return the exact decision and its owner without choosing for them.

## 2. Diagnose

Name one demonstrated architecture cost or retain the current shape. Look for:

- a broad interface that hides little;
- callers coordinating work or knowing internal rules;
- one representation, policy, or invariant repeated across owners;
- phase-shaped modules that split shared knowledge by execution order;
- pass-through layers, scattered state, invalid combinations, or synchronized
  copies;
- repeated same-shaped workarounds, branches, or type escape hatches.

Apply the deletion test. If removing the module removes no useful behavior or
policy, inline or delete it. If its complexity would spread across callers, it
may be earning its place. One awkward case does not prove a bad architecture.

## 3. Shape

Write the ordinary caller usage first. Derive the data representation, types,
operations, state transitions, effects, and failure behavior from that usage
and the dominant reads, writes, and transitions.

Choose the smallest coherent option: retain, delete, inline, merge, deepen,
replace, or add an earned seam. Keep cohesive rules and invariants with their
owner. Make invalid states difficult to express. Prefer local state, direct
control flow, and existing language, framework, and repository capabilities.

When stateful behavior or a trust or external boundary drives the decision,
resolve only the applicable lifecycle, ordering, concurrent or repeated-call,
partial-failure, recovery, trust, and compatibility behavior. If the boundary
must enforce access, include representative allowed and forbidden callers and
a check capable of failing.

Add a seam only when it hides meaningful policy or complexity, supports real
variation, isolates an actual external dependency, or separates distinct
ownership. A test double alone does not earn one. Keep transport, storage, and
framework representations behind the interface that owns their translation.

Read [DEEPENING.md](DEEPENING.md) only when dependency shape changes seam
placement, substitution, testing, or migration.

## 4. Compare

Compare the candidate with the current shape and the simplest credible
no-new-seam option under the same accepted behavior. Compare caller effort,
hidden decisions, data flow, interface burden, locality, reader load, change
cost, and proof.

Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) only when two or more materially
different shapes remain credible and the choice is consequential.

Replace an existing design only when actual dependents and intended behavior
are traceable, the new shape is simpler as a whole, callers can move in a
bounded change, and the real interface provides parity proof. Preserve an old
path only for a named compatibility or migration need.

## 5. Recommend

Return one opinionated design, retain the current shape, or name the exact
missing decision or evidence. A recommendation states the ownership, ordinary
caller usage, data and interface shape, hidden behavior, applicable state and
failure policy, displaced paths, first bounded implementation move, and nearest
useful proof. Explain briefly why each rejected credible alternative loses.

Fold a loaded result into the caller's artifact. Create no separate design
packet, tracker item, implementation step, or status taxonomy. Stop before
implementation.

## Completion

Complete when one bounded architecture question has an implementable
recommendation, a supported retain or no-change judgment, or an exact
user-owned decision or evidence gap. Start nothing downstream.
