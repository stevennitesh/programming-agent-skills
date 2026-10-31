# Shared model routing

This reference owns child-model routing for controlled-delegation and
ultra-model-routing. It selects neither execution workflow. Preserve the selected
lead model, effort, and native mode; the calling workflow owns delegation,
custody, waiting, review arrangement, and delivery.

| Delegated assignment | Model | Effort |
| --- | --- | --- |
| Architecture, design advice, and candidate review | `gpt-6.1-sol` | `xhigh` |
| Substantive coding, debugging, investigation, and reasoning | `gpt-6.1-sol` | `high` |
| Routine execution, settled bulk work, and mechanical tasks | `gpt-6.1-terra` | `medium` |
| Computer use, including browser and desktop interaction | `gpt-6.1-terra` | `medium` |
| Visual extraction | `gpt-6.1-terra` | `medium` |
| Writing from supplied facts | `gpt-6.1-terra` | `medium` |
| Defined data analysis | `gpt-6.1-terra` | `medium` |
| Settled implementation work | `gpt-6.1-terra` | `medium` |

## Classify the assignment

Classify the delegated work, not its parent project's size. Bounded scope alone
does not make work routine.

- **Computer use:** route all browser and desktop interaction to
  `gpt-6.1-terra` at `medium`, including interaction supporting substantive work.
  Separate investigation, design advice, and candidate review retain their
  respective routes below.
- **Routine:** rules and inputs are settled, and observable acceptance can
  distinguish a correct result without substantial new judgment. Repetitive
  transformations and running a defined check can remain routine even at high volume.
- **Visual extraction:** extract specified facts or structured fields from
  screenshots, scanned tables, invoices, product images, or technical drawings.
- **Writing from supplied facts:** draft or revise documentation, summaries,
  proposals, and replies using supplied facts and established requirements.
- **Defined data analysis:** execute specified queries, summaries, charts, and
  data-quality checks with settled methods and clear acceptance criteria.
- **Settled implementation:** carry out repetitive edits, straightforward scripts,
  or mechanical transformations with settled behavior and design. Keep necessary
  implementation verification with the worker.
- **Substantive:** investigate causes, trace interacting behavior, make
  unsettled implementation or analytical choices, or resolve uncertain cases.
  Running a check may be routine while explaining its failure needs this route.
- **Architecture or review:** judge ownership, interfaces, migration, or candidate
  correctness. Collecting fixed evidence can be routine support; deciding what it
  establishes remains advisory or review work. The lead retains decisions and
  acceptance; ordinary coding choices need no separate architecture phase.

For other work, route a coherent assignment by the judgment it requires, including
substantive work mixed with routine steps. Keep mechanical steps and implementation
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
