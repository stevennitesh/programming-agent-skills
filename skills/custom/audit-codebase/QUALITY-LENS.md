# Quality Coverage And Triage

Load this compact owner for every subsystem Audit. It owns coverage, detailed
lens routing, primary-class arbitration, opportunity admission, and retained
complexity.

## Six-Class Coverage

Record exactly one row per class:

```text
Class:
Applicability: applicable | not applicable
Coverage: complete | incomplete
Examined scenarios and evidence:
Admitted item IDs: <defects/opportunities/gaps/retained> | none
Detailed owner loaded: yes | no
Reason:
```

An admitted item does not close class coverage. `not applicable` requires
current-source evidence. Any unchecked obtainable evidence makes that class and
the subsystem `incomplete`.

| Class | Purpose | Load detailed owner when current evidence shows |
| --- | --- | --- |
| Reliability | Supported behavior, failure, lifecycle, security, state, and environmental correctness | Always load [RELIABILITY-LENS.md](RELIABILITY-LENS.md). |
| Domain | Accepted project meaning and durable decisions | A governing domain record, specification, schema, acceptance test, or declared code contract plus a possible language, Invariant, relationship, implementation, or ADR contradiction; then load [DOMAIN-LENS.md](DOMAIN-LENS.md). |
| Design | Interface, Seam, dependency direction, and ownership placement | Mapped caller spread, pass-through boundaries, a cycle or dependency-direction conflict, misplaced ownership, supported variation, or caller-facing tests bypassing an Interface; then load [DESIGN-LENS.md](DESIGN-LENS.md). |
| Simplification | Necessity and the lowest-burden sufficient behavior-preserving reduction | Reachable duplicate or stale behavior, unnecessary configuration/compatibility/dependency, a custom mechanism beside repository/standard/native capability, or an unearned boundary; then load [SIMPLIFICATION-LENS.md](SIMPLIFICATION-LENS.md). |
| Coding practice | Independently evidenced residual clarity and provability | An observed naming, control-flow, comment, error-expression, invalid-state, duplicated-expression, or test-portfolio burden; then load [CODING-PRACTICES-LENS.md](CODING-PRACTICES-LENS.md). |
| Performance | Measured resource behavior and comparability | A resource budget, requirement or claim, repository-owned measurement, current trace, deterministic count, or direct bottleneck evidence; then load [PERFORMANCE-LENS.md](PERFORMANCE-LENS.md). |

Generic project nouns, file size, function length, nesting, test count, suite
time, dependency count, or aesthetic preference do not trigger depth or prove a
finding.

## Primary Ownership

- **Reliability:** behavior, enforcement, failure safety, Trust Boundaries,
  lifecycle, concurrency, compatibility, and behavioral proof.
- **Domain:** accepted meaning and decision authority.
- **Design:** Interface, Seam, dependency direction, and code ownership.
- **Simplification:** necessity and the smallest sufficient reduction.
- **Coding practice:** residual clarity and provability.
- **Performance:** measured resource behavior; Reliability still owns failure
  semantics under load.

Design establishes whether a boundary is earned. Simplification chooses the
smallest safe removal, reuse, or collapse direction. Mixed and systemic
candidates may group items later without erasing each item's primary owner or
subsystem evidence.

## Classification

A violated authoritative expectation is a defect under
[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md). Missing required evidence unavailable
within Audit is a gap. Essential complexity protecting a verified constraint
is retained complexity; accidental complexity earns no retention merely
because it exists. A beneficial change without a violated expectation is an
opportunity only when all gates close:

- **Reach:** one supported scenario currently reaches the code.
- **Evidence:** direct current-source evidence identifies the shape.
- **Observed cost:** one affected scenario has concrete caller burden,
  duplicated decisions, change amplification, proof friction, execution cost,
  dependency weight, misleading ownership, failure exposure, cognitive load,
  or exposed unknown unknowns.
- **Existing direction:** a named current/local owner or sufficient mechanism
  plausibly removes that cost without weakening the contract.
- **Proof:** the observable seam and preservation checks are named.

```text
Opportunity ID:
Primary class:
Location and supported behavior:
Current evidence and observed cost:
Existing owner or smallest direction:
Behavior and safety floors:
Required proof:
Confidence:
```

Retain justified complexity:

```text
Retain ID:
Location and apparent cost:
Constraint or behavior protected:
Evidence:
Known Ceiling:
Revisit Trigger:
```

## Stale Code And False-Positive Controls

Call code stale only after proportionately checking current reachability,
registration, configuration, callers, supported compatibility, generated
ownership, and relevant history. Missing text references do not prove
staleness for reflection, plugins, dynamic imports, serialization, registries,
templates, or external entry points.

Do not estimate savings without a verified patch or mechanical count. Audit
records directions, not implementation. Retained complexity is not a candidate.
A gap-only or retained-only cluster is not a candidate. When an observation
suggests a repeated pattern, search sibling callers and repository-wide
variants before calling it systemic. Record the affected set and causal owner,
or keep the finding local.
