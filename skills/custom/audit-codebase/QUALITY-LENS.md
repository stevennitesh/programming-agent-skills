# Quality Concept Triage

Use this index to classify observed friction before admitting an opportunity.
Load every required lens for the selected subsystem, but give each observation
one primary concept class and one owning contract.

## Concept Classes

| Class | Strong leading concepts | Reference | Primary question |
| --- | --- | --- | --- |
| Reliability | Semantic Correctness, Robustness, Invariant, Trust Boundary, Failure Atomicity, Recovery, Idempotency, Concurrency, State Lifecycle | [RELIABILITY-LENS.md](RELIABILITY-LENS.md) | Can supported behavior be trusted across its meaningful branches? |
| Domain | Ubiquitous Language, Bounded Context, Invariant, Context Relationship, Language Collision, ADR Conflict | [DOMAIN-LENS.md](DOMAIN-LENS.md) | Does code express the accepted model and ownership? |
| Design | Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality, Deletion Test | [DESIGN-LENS.md](DESIGN-LENS.md) | Does the shape concentrate capability, decisions, and proof? |
| Simplification | YAGNI, KISS, DRY, Readability First, Repository Reuse, Standard Library, Native Platform, Installed Dependency, Collapse, Surgical Change, Goal-Driven Execution, Known Ceiling, Revisit Trigger | [SIMPLIFICATION-LENS.md](SIMPLIFICATION-LENS.md) | What is the first smaller shape that preserves the contract? |
| Coding practice | Descriptive Naming, Type Safety, Immutability Default, Explicit Error Handling, Input Validation, Clear Control Flow, Why Comments, Behavior Tests, Focused Concurrency | [CODING-PRACTICES-LENS.md](CODING-PRACTICES-LENS.md) | Does implementation reveal and protect its contract? |
| Performance | Like-for-like workload, baseline, budget, measurement, variance | [PERFORMANCE-LENS.md](PERFORMANCE-LENS.md) | Is the resource claim measured under comparable conditions? |

A violated authoritative expectation is a defect under
[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md). A verified beneficial change without
a violated expectation is an opportunity. Missing required evidence is a gap.
Complexity that protects a real constraint is retained complexity.

When **Invariant** spans classes, use Reliability for behavioral enforcement
or failure safety and Domain for accepted meaning. Give every observation one
primary class even when a mixed candidate later groups several.

Use the violated contract to resolve other overlaps:

- Reliability owns observable behavior and failure safety.
- Domain owns accepted project meaning.
- Design owns Interface, Seam, and code-ownership placement.
- Simplification owns unnecessary behavior or a proved cheaper mechanism.
- Coding practice owns readability and provability when behavior, meaning,
  and ownership remain correct.
- Performance owns measured resource behavior; Reliability owns failure
  semantics under load.

## Triage Questions

- **Necessary:** Does the behavior, compatibility path, flag, configuration,
  dependency, or abstraction still serve a supported scenario?
- **Available:** Does the repository, Standard Library, Native Platform,
  framework, database, or an Installed Dependency already own the behavior?
- **Owned:** Is one policy duplicated, leaked across callers, or split between
  competing owners or Bounded Contexts?
- **Deep:** Does the Interface provide Leverage and Locality, or expose an
  implementation-sized surface?
- **Clear:** Do Descriptive Naming, Clear Control Flow, errors, state
  transitions, comments, and configuration reveal the contract?
- **Provable:** Is the Interface the Test Surface, including relevant failure
  and state branches?
- **Faithful:** Does code preserve Ubiquitous Language, Invariants, Context
  Relationships, and accepted decisions?

Generic thresholds such as function length, nesting depth, file size, test
count, or dependency count are discovery hints only.

## Opportunity Admission

Admit an opportunity only when all five gates close:

- **Reach:** the code participates in a supported subsystem scenario.
- **Evidence:** direct snapshot evidence identifies the current shape.
- **Cost:** the shape creates concrete caller burden, duplicated decisions,
  change spread, test friction, dependency weight, misleading ownership,
  failure exposure, or comprehension cost.
- **Alternative:** a smaller, deeper, clearer, or more robust local shape
  plausibly removes that cost without weakening the contract.
- **Proof:** the observable seam and checks needed to preserve behavior are
  named.

```text
Opportunity ID:
Primary class:
Concepts:
Location:
Supported behavior:
Current evidence:
Concrete cost:
Change direction:
Behavior and safety floors:
Required proof:
Confidence:
```

Convert a cohesive user-selectable opportunity, defect, or cluster containing
at least one of them under
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md). A related gap may join; a
gap-only hypothesis may not. Keep all member IDs visible.

## Stale Code

Call code stale only after checking current reachability, registration,
configuration, callers, supported compatibility, generated ownership, and
relevant history proportionately. Missing text references do not prove
staleness for reflection, plugins, dynamic imports, serialization, command
registries, templates, or external entry points.

When a proportionate check is available but unfinished, keep the subsystem
`incomplete`. When the check is unavailable within Audit authority, record an
evidence gap naming it.

## Retain

```text
Retain ID:
Location:
Apparent cost:
Constraint or behavior it protects:
Evidence:
Known Ceiling:
Revisit Trigger:
```

Retained complexity is not a candidate. It prevents the same unsafe reduction
from being re-proposed without new evidence.

## Bound

Do not estimate lines or dependencies saved without a verified patch or
mechanical count. Audit records change directions, not implementation. A
quality opportunity grants no mutation or downstream authority.
