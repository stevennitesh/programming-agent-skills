# Design It Twice

Use this branch for a consequential interface choice. The first plausible interface is an anchor, not a conclusion.

Frame -> Diverge -> Compare -> Commit.

Use [`SKILL.md`](SKILL.md) for vocabulary, [DIRECT-DESIGN.md](DIRECT-DESIGN.md) for the design packet, and [DEEPENING.md](DEEPENING.md) for dependency and migration strategy.

## 1. Frame

Frame the problem from the Source Trace: candidate module or shallow cluster, spread behavior or decision, constraints, dependencies, painful callers and tests, public-contract commitments, and bounded-slice edge. Use a sketch only when it clarifies constraints; it is evidence, not a proposal.

## 2. Diverge

Produce at least three genuinely different interfaces.

Use direct fresh-context scouts when independent judgment matters. Start each with `fork_turns="none"` when supported. Give every scout the same self-contained factual brief: objective, settled constraints, scope, source pointers, one distinct design pressure, mutation boundary, and output contract. Exclude parent hypotheses, preferred solutions, other candidates, and peer results.

Scouts inspect and propose only; they never edit files, mutate external state, or spawn. Keep alternatives private until every scout returns. The main agent owns comparison, recommendation, and completion.

When continuity matters more than independence, fork only the minimum necessary recent context and do not call the result independent. When delegation is unavailable, produce alternatives sequentially under different pressures.

Use pressures that force structural variety:

- **Minimal** — smallest useful surface;
- **Caller-first** — trivial common call;
- **Domain-owned** — decisions move to their domain owner;
- **Seam-first** — real adapters or substitutes shape the interface;
- **Migration-first** — first safe step fits the bounded slice.

For each alternative, show:

- interface sketch and caller experience;
- behavior hidden behind the interface;
- seam, dependencies, adapters, and substitutes;
- test surface and validation proof;
- first migration step, trade-offs, and risks.

## 3. Compare

Compare depth, locality, caller ergonomics, seam placement, dependency strategy, test surface, migration cost, and risk. Merge alternatives that differ only by names, parameter reshuffling, or cosmetic layering; replace fake variety with a genuinely different design.

## 4. Commit

Recommend one design. Explain why it wins, why credible alternatives lose, any useful hybrid, the first bounded migration step, validation proof, risks, and follow-ups. Name behavior-preserving prerequisites as support slices.

## Completion

Complete when the frame is source-traced; at least three genuinely different interfaces exist; fake variety was removed; every alternative covers callers, hidden behavior, seam, dependencies, tests, migration, trade-offs, and risk; one design was recommended; and the bounded first step and proof were returned.
