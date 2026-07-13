# Direct Design Pass

Use this branch when the user supplies one bounded module, shallow cluster, seam, or interface question. [`SKILL.md`](SKILL.md) owns vocabulary, taste gates, and the read-only boundary.

## 1. Orient

Reuse the caller's **Source Trace** when supplied. Otherwise trace the request or caller artifact, repo instructions, applicable domain glossary and ADRs, current implementation and interface, callers, tests, dependencies, and operational constraints.

Complete when the bounded candidate, spread behavior or decision, current caller knowledge, and public-contract commitments are known.

## 2. Diagnose

Name the current module, interface, and implementation; behavior or decisions spread across callers; caller friction and interface pressure; real and hypothetical seams; deletion-test result; and losses in depth, leverage, and locality.

Recommend `$improve-codebase-architecture` and stop for a wide or candidate-finding scan.

## 3. Deepen

Propose the deeper module, caller-facing interface contract, behavior and decisions moving behind it, seam placement, real adapters or substitutes, caller and test surfaces, and bounded migration step.

Read [DEEPENING.md](DEEPENING.md) when dependency shape changes the seam, adapter, substitute, test migration, or validation strategy.

## 4. Design It Twice

Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when the interface is consequential, several shapes are plausible, or the first design carries meaningful migration or compatibility risk.

## 5. Recommend

Choose one design. Explain why it wins, why credible alternatives lose, the first safe migration step, validation proof, risks, and follow-ups.

Evidence settles current behavior and constraints. The user or caller settles public-contract changes and accepted trade-offs.

## Design Packet

Return:

- Source Trace;
- current shallow shape and deletion-test result;
- proposed deep module and caller-facing interface contract;
- behavior hidden behind the interface;
- seam, adapters, substitutes, and dependency categories;
- caller leverage and maintainer locality;
- test surface and validation proof;
- alternatives and why they lose;
- first bounded migration step;
- risks, follow-ups, and any domain or ADR candidate.

## Completion Criteria

Complete only when Source Trace covers the candidate, callers, tests, dependencies, and constraints; current and proposed interfaces are explicit; every seam and adapter is earned; behavior is provable through the caller-facing surface; consequential alternatives were compared; one design was recommended; the first migration step fits the bounded slice; downstream mutations remain caller-owned; and the design packet was returned.
