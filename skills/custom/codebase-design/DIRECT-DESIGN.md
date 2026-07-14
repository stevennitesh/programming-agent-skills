# Direct Design Pass

Use this branch for one bounded module, shallow cluster, seam, or interface question. [`SKILL.md`](SKILL.md) owns vocabulary, taste, and the read-only boundary.

Orient -> Diagnose -> Shape -> Compare -> Recommend.

## 1. Orient

Reuse a supplied **Source Trace**. Otherwise trace the request or caller artifact, repo contracts, current interface and implementation, representative callers and tests, dependencies, and operational constraints.

## 2. Diagnose

Name the module, interface, implementation, spread behavior or decisions, caller friction, interface pressure, deletion-test result, and real or hypothetical seams. Explain the losses in depth, leverage, and locality.

## 3. Shape

Choose the strongest shape: deepen, merge, inline, retain, or introduce no new seam. Describe its caller-facing contract, hidden behavior and decisions, any earned seam, adapters or substitutes, caller and test surfaces, and first bounded migration step.

Read [DEEPENING.md](DEEPENING.md) when dependency shape changes the seam, substitute, test migration, or validation strategy.

## 4. Compare

Compare the candidate with the current shape and the simplest no-new-seam option. Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when the interface is consequential, several shapes are plausible, or migration and compatibility risk are meaningful.

## 5. Recommend

Choose one design. Explain why it wins, why credible alternatives lose, the first safe migration step, validation proof, risks, and follow-ups.

Evidence settles current behavior and constraints. The user or caller settles public-contract changes and accepted trade-offs.

## Design Packet

Return:

- Source Trace and current shallow shape;
- deletion-test result and caller friction;
- recommended shape, interface contract, and hidden behavior;
- any earned seam, dependencies, adapters, and substitutes;
- caller leverage, maintainer locality, and test surface;
- credible alternatives and recommendation;
- first bounded migration step and validation proof;
- risks, follow-ups, and any domain or ADR candidate.

## Completion

Complete when the Source Trace covers the candidate, callers, tests, dependencies, and constraints; current and recommended interfaces are explicit; any seam or adapter is earned; behavior is provable through the caller-facing surface; the current and no-new-seam shapes were compared; consequential alternatives were explored; one design and a bounded first migration step were recommended; the design packet was returned; and downstream mutations remain caller-owned.
