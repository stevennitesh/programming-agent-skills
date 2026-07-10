# Design It Twice

Use this branch for a consequential interface choice.

The first plausible interface is an anchor, not a conclusion. Produce independent alternatives, expose fake variety, compare trade-offs, then recommend one.

Use [SKILL.md](SKILL.md) for vocabulary, [DIRECT-DESIGN.md](DIRECT-DESIGN.md) for the design packet, and [DEEPENING.md](DEEPENING.md) for dependency categories, seam discipline, adapter strategy, and test migration.

## Process

### 1. Frame The Problem Space

Before proposing designs, write a short user-facing frame:

- Source Trace: request or caller artifact, relevant implementation, callers, tests, domain terms, and ADR constraints;
- candidate module or shallow cluster;
- behavior or decision currently spread across callers;
- constraints the new interface must satisfy;
- dependencies and their categories from [DEEPENING.md](DEEPENING.md);
- existing callers and tests that reveal pain;
- bounded-slice constraint.

Include a rough code sketch only when it makes the constraints easier to see. Treat the sketch as evidence rather than a proposal.

### 2. Produce Alternatives

Produce at least three meaningfully different interfaces.

Use independent subagents when available. Give each worker the shared problem frame and one distinct design pressure without exposing the other alternatives. The main agent owns comparison and recommendation.

When delegation is unavailable, produce alternatives sequentially and reset the design pressure between them. Require three alternatives, not three workers; the main agent may contribute one independent design.

Use different design pressures to force real variety:

- **Minimal surface** - minimize the useful interface and maximize leverage per entry point.
- **Caller-optimized** - make the most common caller trivial.
- **Domain-owned** - move decisions to the module that owns the domain concept.
- **Seam-focused** - design around real adapters or local substitutes.
- **Migration-first** - fit the first safe step inside the bounded slice.

Each alternative includes:

- **Interface sketch** - usage plus useful type or function detail.
- **Caller experience** - what callers learn and stop knowing.
- **Behavior hidden** - what moves behind the interface.
- **Seam and adapters** - where variation lives and which adapters or substitutes are real.
- **Dependency category** - from [DEEPENING.md](DEEPENING.md).
- **Test surface** - how behavior is proved through the interface.
- **Migration path** - first safe step and any support slice.
- **Trade-offs** - gains and weaknesses in depth, leverage, locality, testability, and risk.

### 3. Compare

Present alternatives one at a time, then compare them by:

- **Depth**;
- **Locality**;
- **Caller ergonomics**;
- **Seam placement**;
- **Dependency strategy**;
- **Test surface**;
- **Migration cost**;
- **Risk**.

Merge alternatives that differ only by names, parameter reshuffling, or cosmetic layering; replace them with a genuinely different design.

### 4. Recommend

Choose one design.

Include:

- why it wins;
- why rejected alternatives lose;
- any useful hybrid;
- first migration step;
- validation proof;
- risks and follow-ups.

Name behavior-preserving prerequisites as support slices. When the design exceeds the bounded slice, recommend the smallest useful next slice.

## Completion Criteria

Complete only when the problem frame is source-traced; at least three genuinely different interfaces exist; fake variety was replaced; every alternative covers caller experience, hidden behavior, seam, dependencies, test surface, migration, and trade-offs; the alternatives were compared; one design was recommended; and the first bounded migration step, proof, risks, and follow-ups were returned.
