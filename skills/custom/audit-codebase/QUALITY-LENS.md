# Quality Coverage And Triage

Use this compact owner on every subsystem Audit. It forces breadth before
specialist depth, classifies observations, admits opportunities, and records
retained complexity.

## Mandatory Lens Gate

Record every required class once:

```text
Lens:
Disposition: finding | retained complexity | gap | examined-no-finding | not applicable
Evidence:
Detailed owner loaded: yes | no
Reason:
```

`not applicable` requires source evidence. When applicability or a clean
disposition is not obvious, load the detailed owner and examine it. A missing
disposition keeps the subsystem `incomplete`.

| Class | Mandatory question | Load the detailed owner when |
| --- | --- | --- |
| Reliability | Can supported behavior be trusted across meaningful success, edge, state, failure, security, and environmental branches? | Always load [RELIABILITY-LENS.md](RELIABILITY-LENS.md). |
| [Domain](DOMAIN-LENS.md) | Does code express accepted language, Invariants, Bounded Context ownership, Context Relationships, and ADR decisions? | Domain records, project terms, policy meaning, Invariants, cross-context behavior, or a material decision is present or uncertain. |
| [Design](DESIGN-LENS.md) | Do Interfaces and Seams concentrate capability, decisions, change, and proof with useful Depth, Leverage, and Locality? | Boundaries, pass-through layers, caller spread, dependency direction, test seams, or ownership placement may matter. |
| [Simplification](SIMPLIFICATION-LENS.md) | Is behavior, configuration, compatibility, duplication, dependency, or abstraction unnecessary, or already owned by a smaller sufficient mechanism? | A stale path, duplicate policy, custom mechanism, shallow boundary, or cheaper behavior-preserving direction may exist. |
| [Coding practice](CODING-PRACTICES-LENS.md) | Do naming, types, errors, validation, control flow, comments, state, and tests make the contract clear and provable? | Implementation clarity, invalid states, error behavior, Trust Boundaries, test responsibility, or concurrency may affect cost or risk. |
| Performance | Is any speed or resource claim supported by like-for-like measurement against an applicable budget or comparison? | Performance or resources are declared, observed, suspected, or claimed; then load [PERFORMANCE-LENS.md](PERFORMANCE-LENS.md). |

## Class Ownership

A violated authoritative expectation is a defect under
[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md). A verified beneficial change without
a violated expectation is an opportunity. Missing required evidence is a gap.
Complexity that protects a real constraint is retained complexity.

Give each observation one primary class:

- **Reliability** owns Semantic Correctness, supported behavior, state, and
  failure safety.
- **Domain** owns accepted project meaning.
- **Design** owns Interface, Seam, and code-ownership placement.
- **Simplification** owns unnecessary behavior or a proved cheaper mechanism.
- **Coding practice** owns readability and provability when behavior, meaning,
  and ownership remain correct.
- **Performance** owns measured resource behavior; Reliability owns failure
  semantics under load.

When **Invariant** spans classes, use Reliability for behavioral enforcement
or failure safety and Domain for accepted meaning. A mixed candidate may group
observations later without erasing their primary owners.

## Triage

Before admitting an opportunity, test:

- **Necessary:** Does the behavior, compatibility path, flag, configuration,
  dependency, or abstraction serve a supported scenario?
- **Available:** Does Repository Reuse, Standard Library, Native Platform,
  framework, database, or an Installed Dependency already own it?
- **Owned:** Is policy duplicated, leaked across callers, or split between
  competing owners or Bounded Contexts?
- **Deep:** Does the Interface provide Leverage and Locality, or expose an
  implementation-sized surface?
- **Clear:** Do names, control flow, errors, state, comments, and configuration
  reveal the contract?
- **Provable:** Is the Interface the Test Surface, with each test owning a
  distinct behavior, branch, risk, or diagnostic responsibility?
- **Faithful:** Does code preserve Ubiquitous Language, Invariants, Context
  Relationships, and accepted decisions?

Function length, nesting depth, file size, test count, suite time, and
dependency count are discovery hints only.

## Opportunity Admission

Admit an opportunity only when all five gates close:

- **Reach:** the code participates in a supported subsystem scenario.
- **Evidence:** direct current-source evidence identifies the shape.
- **Cost:** concrete caller burden, duplicated decisions, change spread, proof
  friction, execution cost, dependency weight, misleading ownership, failure
  exposure, or comprehension cost exists.
- **Alternative:** a smaller, deeper, clearer, or more robust local shape
  plausibly removes the cost without weakening the contract.
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

Convert only a cohesive user-selectable opportunity, defect, or cluster
containing at least one of them under
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md). A related gap may join; a
gap-only hypothesis may not. Keep every member ID visible.

## Stale Code

Call code stale only after proportionately checking current reachability,
registration, configuration, callers, supported compatibility, generated
ownership, and relevant history. Missing text references do not prove
staleness for reflection, plugins, dynamic imports, serialization, command
registries, templates, or external entry points.

When obtainable proof is unfinished, keep the subsystem `incomplete`. When it
is unavailable within Audit authority, record a gap with its re-entry.

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
