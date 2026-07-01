# Implement Synthesis

## Purpose

`implement` should make one behavior change from one ready issue, then stop.
It should keep the work bounded, reviewable, proved, and honest about
follow-ups.

## Source Pressure

- [Facet 1: Bounded Slice](../../research/skill-facets/implement/FACET-1-BOUNDED-SLICE.md)
- `tracer bullet`
- `outside proof`
- `one self-contained reviewable change`
- `related proof travels with the diff`
- `stop, split, or ask`

## Proposed Runtime Behavior

Before editing, the agent should lock one visible activity/path, the outside
proof, likely in-scope areas, explicit non-goals, and the stop/split trigger.

For behavior work, the agent should prefer a tracer bullet: one narrow
real-system path proved through the best practical seam.

The diff should be one self-contained reviewable change. Related proof should
travel with the diff. Adjacent work should go into the note, not the patch.

## Controlled Language Draft

```markdown
Before editing, lock one user-, caller-, operator-, or maintainer-visible activity/path, the outside proof, the likely files or areas in scope, explicit non-goals, and the stop/split trigger.

For behavior work, prefer a tracer bullet: one narrow real-system path proved through the best practical seam. Slice by behavior, not by folder, layer, or component; use layer-only work only when the selected issue is an explicit support slice with observable validation.

Shape the diff as one self-contained reviewable change with related proof included. File spread is review size. If proof fails, iterate inside the locked slice; if the needed fix changes the slice, stop, split, or ask instead of broadening the diff. Follow-ups go in the note, not the diff.
```

Conditional walking-skeleton wording:

```markdown
For new or uncertain system shape, use a walking skeleton only when it is production-shaped and proves the smallest useful end-to-end behavior; do not count throwaway spike code as implementation.
```

Completion criterion wording:

```markdown
Done means one locked activity/path is usable for its promised purpose, verified through the best practical outside-facing seam, left in a repo-standard green state or documented substitute, and explainable as one self-contained change with one proof story. No proof, no done.
```

## Prune Notes

Do not import:

- detailed TDD mechanics from `tdd`;
- full review procedure from `review`;
- the whole convergence loop from `docs/agents/engineering-contract.md`;
- tracker publishing rules from `docs/agents/issue-tracker.md`;
- generic Agile glossary language;
- agent-framework taxonomy.

## Runtime Boundary

This synthesis note is not active behavior. Edit
`skills/current/implement/SKILL.md` only after explicit approval.
