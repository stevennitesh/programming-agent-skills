# Shared model routing

This reference owns child-model routing for controlled-delegation and
ultra-model-routing. It selects neither execution workflow. Preserve the selected
lead model, effort, and native mode; the calling workflow owns delegation,
custody, waiting, review arrangement, and delivery.

| Delegated assignment | Model | Effort |
| --- | --- | --- |
| Architecture, design advice, and candidate review | `gpt-6.1-sol` | `xhigh` |
| Coding, debugging, investigation, and substantive reasoning | `gpt-6.1-sol` | `high` |
| Routine execution, settled bulk work, and mechanical tasks | `gpt-6.1-terra` | `medium` |

## Classify the assignment

Classify the delegated work, not its parent project's size. Bounded scope alone
does not make work routine.

- **Routine:** rules and inputs are settled, and observable acceptance can
  distinguish a correct result without substantial new judgment. Extraction,
  repetitive transformations, writing from supplied facts and patterns, and running
  a defined check can remain routine even at high volume.
- **Substantive:** investigate causes, trace interacting behavior, make
  implementation choices, or resolve uncertain cases. Running a check may be
  routine while explaining its failure needs this route.
- **Architecture or review:** judge ownership, interfaces, migration, or candidate
  correctness. Collecting fixed evidence can be routine support; deciding what it
  establishes remains advisory or review work. The lead retains decisions and
  acceptance; ordinary coding choices need no separate architecture phase.

Route a coherent assignment by the judgment it requires, including substantive
work mixed with routine steps. Keep mechanical steps and implementation
verification with that worker when splitting them would add unnecessary handoffs.
An author's testing and self-checking remain implementation work; they do not
count as independent candidate review.

When the assignment changes category, preserve useful evidence and re-scope it
under the appropriate route. Keep useful context for coherent corrections and
follow the execution owner's custody and support limits before reassignment.

## Overrides and unavailable routes

Pass model and effort together through [Native spawning](native-spawning.md).
Preserve exact versions and efforts. Explicit user overrides apply only to their
stated scope; do not silently substitute another family, alias, or effort, or turn
a temporary exception into a default.

If a required route is unavailable, report the affected assignment and capability
limit without claiming another route satisfied it. Resolve missing requirements,
access, data, dependencies, or functioning tools at their owner, continue useful
independent work, and report a consequential block. Stronger effort cannot replace
evidence or authorization.

These are operating defaults, not a quality ranking or savings result. Use
[Telemetry](telemetry.md) when measurement is requested or a budget materially
affects the work.
