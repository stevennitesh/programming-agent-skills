# Implement Research Map

Use `../../../synthesis/methods/source-distillation-flow.md` only when
`implement` needs optional source evidence or deliberate pruning of upstream
skills, books, papers, standards, or engineering practice.

Use `SEARCH-VOCABULARY.md` only when a facet needs keyword help. The vocabulary
file is research support, not the workflow. This README owns the active
implement facet map.

## Target Skill Shape

`implement` should make one behavior change from one ready issue, then stop.

The skill should steer the agent to:

- pick exactly one ready issue;
- establish the repo baseline before editing;
- understand product intent, acceptance criteria, and out-of-scope boundaries;
- choose a local approach inside the bounded slice;
- prove semantic correctness through the best available seam;
- use TDD when the behavior is clear enough for red-green-refactor;
- review from a fixed point against Standards and Spec;
- simplify only while behavior is protected;
- commit and leave an evidence-backed implementation note.

## Research Facets

Research one facet at a time. Each facet should end with a distilled source
packet, not candidate runtime wording or a long essay.

| Order | Facet | Research Question | Skill Surface | Status |
| --- | --- | --- | --- | --- |
| 1 | Ready issue selection | How should `implement` select exactly one ready issue or stop when no safe issue is available? | invocation, named issue precedence, PRD/spec handoff, ready-label selection, blocker/ambiguity/no-issue stop | Pending source distillation |
| 2 | Baseline and fixed point | What must the agent establish before editing so unrelated work is preserved and review/commit remain trustworthy? | baseline capture, dirty-work preservation, review starting point, commit isolation | Pending |
| 3 | Context intake | What must the agent understand before editing so implementation is not guesswork? | issue/spec reading, domain vocabulary, acceptance criteria, blockers, out-of-scope boundaries | Pending |
| 4 | Bounded slice control | How should one implementation run stay small, valuable, independently provable, and reviewable? | scope boundary, tracer-bullet/support distinction, adjacent work, failed proof, follow-ups | Pending source distillation |
| 5 | Commitment boundary | Which decisions can the agent make inside the slice, and which changes require stopping or asking? | ask/stop rules, autonomous technique, user-owned decisions, changed commitments | Pending |
| 6 | Semantic proof and seams | What proves the selected issue is correct, and how should `implement` choose a meaningful seam without duplicating `$tdd` or `codebase-design`? | semantic correctness, proof surface, `$tdd` handoff, seam choice, load-bearing internals, skipped checks | Pending |
| 7 | Protected simplification | How should the agent simplify after proof without widening the slice or changing behavior? | simplification, cleanup, refactor, scratch disposal | Pending |
| 8 | Review and lock | What makes the result ready to hand off after implementation: reviewed, committed, noted, and honest about residual risk? | fixed-point review, commit, implementation note, residual risk, issue-state restraint | Pending |

## Boundary

- This README owns the implement-specific map.
- `SEARCH-VOCABULARY.md` owns reusable implement search terms.
- `FACET-*.md` files own the actual research packets.
- Chosen evidence belongs in the owning whole-skill synthesis. Deploy Prompts
  own any later runtime extraction, evaluation, promotion, installation, or
  delivery.
