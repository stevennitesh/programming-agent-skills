# Direct Design Pass

Use this branch for one bounded module, shallow cluster, seam, or interface question. [`SKILL.md`](SKILL.md) owns vocabulary, taste, and the read-only boundary.

Orient -> Diagnose -> Shape -> Compare -> Recommend.

## 1. Orient

Reuse a supplied **Source Trace**. Otherwise trace the request or caller artifact, repo contracts, current interface and implementation, representative callers and tests, dependencies, and operational constraints.

## 2. Diagnose

Name the module, interface, implementation, spread behavior or decisions, caller friction, interface pressure, deletion-test result, and real or hypothetical seams. Explain the losses in depth, leverage, and locality.

## 3. Shape

Choose the strongest shape: deepen, merge, inline, retain, replace, or introduce no new seam. Describe its caller-facing contract, hidden behavior and decisions, any earned seam, adapters or substitutes, caller and test surfaces, and first bounded migration step.

Admit **replace** only when current commitments and caller behavior are traceable, incremental evolution is riskier or more complicated, parity has a proof seam, and migration, cutover, rollback, and one bounded first slice are explicit.

For an enforceable boundary, require one **boundary proof**: a representative allowed caller, a forbidden caller, and a red-capable check that accepts the first and rejects the second.

Read [DEEPENING.md](DEEPENING.md) when dependency shape changes the seam, substitute, test migration, or validation strategy.

## 4. Compare

Compare the candidate with the current shape and the simplest no-new-seam option. When replacement is credible, compare it explicitly with incremental evolution. Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when the interface is consequential, several shapes are plausible, or migration and compatibility risk are meaningful.

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
- first bounded migration step and validation proof, including the boundary proof when applicable;
- for replacement, parity seam, migration, cutover, and rollback evidence;
- risks, follow-ups, and any domain or ADR candidate.

## Completion

Complete when the Source Trace covers the candidate, callers, tests, dependencies, and constraints; current and recommended interfaces are explicit; any seam or adapter is earned; behavior is provable through the caller-facing surface; every enforceable boundary has its boundary proof; the current and no-new-seam shapes were compared; replacement was compared with incremental evolution when credible and has parity, migration, cutover, and rollback evidence when chosen; consequential alternatives were explored; one design and a bounded first migration step were recommended; the design packet was returned; and downstream mutations remain caller-owned.
