# Design It Twice

Use this when a chosen deepening candidate has a consequential interface choice.

The first plausible interface is rarely the best one.

Generate meaningfully different designs, compare their trade-offs, then recommend one. Do not leave the user with a menu.

Use this with [SKILL.md](SKILL.md) for vocabulary and [DEEPENING.md](DEEPENING.md) for dependency categories, seam discipline, adapter strategy, and test migration.

## Process

### 1. Frame The Problem Space

Before proposing designs, write a short user-facing frame:

- candidate module or shallow cluster
- behavior or decision currently spread across callers
- constraints the new interface must satisfy
- dependencies and their categories from [DEEPENING.md](DEEPENING.md)
- existing callers and tests that reveal pain
- relevant domain terms, glossary entries, or ADR constraints
- bounded-slice constraint: what must not widen in this design pass

Include a rough code sketch only when it makes the constraints easier to see. The sketch is not a proposal.

Then proceed to alternatives.

### 2. Produce Alternatives

Produce at least three meaningfully different interfaces for the deepened module.

Alternatives must differ in interface shape, seam placement, dependency strategy, caller model, or ownership of behavior. Renames, parameter reshuffles, and cosmetic layering are fake variety.

If the user explicitly requested subagents, delegation, or parallel agent work, spawn separate Codex subagents with independent technical briefs. Otherwise, produce the alternatives sequentially in the main Codex session.

Use different design constraints to force real variety:

- **Minimal surface** - aim for the smallest useful interface and maximum leverage per entry point.
- **Caller-optimized** - make the most common caller trivial, even if the implementation does more work.
- **Domain-owned** - move decisions to the module that owns the domain concept.
- **Seam-focused** - design around real adapters or local substitutes when dependencies cross a seam.
- **Migration-first** - choose the shape that can be reached safely inside the current bounded slice.

Each alternative must include:

- **Interface sketch** - Python-style usage and, when useful, type or function sketch.
- **Caller experience** - what callers learn and what they stop knowing.
- **Behavior hidden** - what moves behind the interface.
- **Seam and adapters** - where the seam lives and which adapters or substitutes are real.
- **Dependency category** - from [DEEPENING.md](DEEPENING.md).
- **Test surface** - how behavior is proved through the interface.
- **Migration path** - the first safe step, and whether it is a support slice.
- **Trade-offs** - where depth, leverage, locality, or testability improve, and where the design is weaker.

### 3. Compare

Present the alternatives one at a time, then compare them.

Compare by:

- **Depth** - how much behavior sits behind how small an interface.
- **Locality** - where change, bugs, decisions, and verification concentrate.
- **Caller ergonomics** - what the common caller must know and do.
- **Seam placement** - whether the seam is real and placed at the right point.
- **Dependency strategy** - whether adapters, fakes, local substitutes, or mocks are justified.
- **Test surface** - whether tests prove behavior through the same surface callers use.
- **Migration cost** - whether the first step fits the current bounded slice.
- **Risk** - coupling, over-abstraction, hidden behavior, compatibility, and operational risk.

Call out fake variety. If two alternatives are really the same design with different names, merge them and produce a genuinely different one.

### 4. Recommend

Give an opinionated recommendation.

Include:

- chosen design
- why it wins
- why the rejected alternatives lose
- any useful hybrid
- first migration step
- validation proof
- risks and follow-ups

If the best design needs behavior-preserving work before tracer bullets can continue, name that work as a support slice. If the design cannot fit the current bounded slice, say so and recommend the smallest useful next slice instead.
