# Design It Twice

Use this branch for a consequential interface choice. The first plausible interface is an anchor, not a conclusion.

Frame -> Diverge -> Compare -> Recommend.

Use [`SKILL.md`](SKILL.md) for vocabulary and [DIRECT-DESIGN.md](DIRECT-DESIGN.md) for the design packet. Read [DEEPENING.md](DEEPENING.md) only when dependency shape changes the seam, substitute, test migration, or validation strategy; it owns those mechanics, while this branch compares migration implications across alternatives.

## 1. Frame

Frame the problem from the Source Trace: candidate module or shallow cluster, spread behavior or decision, constraints, dependencies, painful callers and tests, public-contract commitments, and bounded-slice edge. Use a sketch only to make settled constraints concrete; label it illustrative, not a proposal or evidence.

## 2. Diverge

Produce at least three genuinely different candidate shapes. Each must make its caller-facing interface explicit; include the current or simplest no-new-seam shape when it is credible.

Use direct fresh-context scouts when independent judgment matters. Start each with `fork_turns="none"` when supported. Give every scout the same self-contained factual brief: objective, settled constraints, scope, source pointers, one distinct design pressure, mutation boundary, and output contract. Exclude parent hypotheses, preferred solutions, other candidates, and peer results.

Scouts inspect and propose only; they never edit files, mutate external state, or spawn. Keep alternatives private until every scout returns. The main agent owns comparison, recommendation, and completion.

When continuity matters more than independence, fork only the minimum necessary recent context and do not call the result independent. When delegation is unavailable, produce alternatives sequentially under different pressures.

Use pressures that force structural variety:

- **Minimal** — smallest useful surface;
- **Caller-first** — trivial common call;
- **Domain-owned** — decisions move to their domain owner;
- **Seam-first** — real adapters or substitutes shape the interface;
- **Migration-first** — first safe step fits the bounded slice.
- **No-new-seam** — merge, inline, retain, or simplify before introducing another abstraction.

For each alternative, show:

- candidate shape, caller-facing interface, and caller experience;
- behavior and decisions hidden or deliberately left with callers;
- any earned seam and relevant dependencies, adapters, or substitutes;
- caller-facing test surface and validation proof;
- first migration step, trade-offs, and risks.

## 3. Compare

Compare depth, locality, caller ergonomics, seam placement, dependency strategy, test surface, migration cost, and risk. Merge alternatives that differ only by names, parameter reshuffling, or cosmetic layering; replace fake variety with a genuinely different design.

## 4. Recommend

Recommend one design. Explain why it wins, why credible alternatives lose, any useful hybrid, the first bounded migration step, validation proof, risks, and follow-ups. Name behavior-preserving prerequisites as support slices.

## Completion

Complete when the frame is source-traced; at least three genuinely different candidate shapes exist; fake variety was removed; every alternative covers callers, hidden behavior, any earned seam, dependencies, tests, migration, trade-offs, and risk; one design was recommended; and the bounded first step and proof were returned.
