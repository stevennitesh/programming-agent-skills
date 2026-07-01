# Implement Research Map

Use `../FACET-RESEARCH-PROMPT.md` for the reusable facet-research workflow, four-subagent review prompt, packet shape, and quality bar.

Use `SEARCH-VOCABULARY.md` only when a facet needs keyword help. The vocabulary file is research support, not the workflow.

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

Research one facet at a time. Each facet should end with candidate synthesis
wording, not a long essay.

| Order | Facet | Research Question | Skill Surface | Status |
| --- | --- | --- | --- | --- |
| 1 | Bounded slice | How do strong teams keep implementation work small, valuable, independently provable, and reviewable? | issue selection, scope boundary, stop rules | Researched in `FACET-1-BOUNDED-SLICE.md`; promoted to synthesis in `../../../synthesis/skills/implement.md`; runtime application pending explicit approval. |
| 2 | Baseline and fixed point | What must be known before editing so the diff stays reviewable and safe? | baseline capture, dirty work preservation, review fixed point | Pending |
| 3 | Exploration before choice | How much discovery is enough before committing to an approach? | orient/explore/choose gates | Pending |
| 4 | Commitment boundary | Which decisions belong to the user, and which belong to the agent? | ask/stop rules | Pending |
| 5 | Semantic proof | What counts as proof that behavior is correct, not merely present? | prove step, acceptance criteria, validation language | Pending |
| 6 | Seams and interfaces | How should implementation choose the test surface and avoid brittle internal checks? | seam choice, TDD handoff | Pending |
| 7 | Simplification while protected | How should cleanup and refactoring happen without widening the slice? | simplify step | Pending |
| 8 | Review and lock | What makes a change ready to hand to a maintainer or future agent? | review, commit, implementation note | Pending |

## Boundary

- This README owns the implement-specific map.
- `SEARCH-VOCABULARY.md` owns reusable implement search terms.
- `FACET-*.md` files own the actual research packets.
- Chosen wording belongs in `docs/synthesis/skills/implement.md` before any
  runtime edit. Runtime skill edits belong in `skills/current/implement/SKILL.md`
  only after synthesis compression and user approval.
