# Synthesis Methods

Methods are reusable ways to distill sources or deploy selected synthesis.

Use this folder for process docs that apply across multiple skills or skill
families.

## Files

| File | Role |
| --- | --- |
| [`deploy-prompts.md`](deploy-prompts.md) | Universal one-skill entry and numbered workflow for selecting an executable minimum baseline, reconciling synthesis, building and evaluating an exact candidate, promoting it, and optionally delivering it through Git. |
| [`source-distillation-flow.md`](source-distillation-flow.md) | Optional flow for distilling primary and outside sources into important concepts and usable techniques. |
| [`prompts/`](prompts/) | Optional prompts supporting source distillation. |

## Routing

Start every selected skill with Deploy Prompt 1. It audits existing lifecycle
state, compares current and upstream minimum candidates, classifies applicable
research, defines executable `B0` and candidate `C1`, and returns the earliest
justified next unit. Its internal packet-integrity gate replaces ceremonial
human confirmation; user input is required only for a material user-owned
choice. Prompt 2 creates or reconciles that skill's synthesis in place; no
pack-wide synthesis migration is required first.

Route by exact campaign shape: current = B0 = C1 is
`runtime-no-change`; current != B0 = C1 is `pruning-only`; and B0 != C1 is a
`behavioral-candidate`. Classify prior evidence as exact-reusable,
lane-limited, historical-admission-only, invalidated, or missing. Pruning is a
non-regression lane and never receives mechanism-contribution credit.

Use the Conditional Research Interlude only when Prompt 1 admits one exact
decision-changing source gap. Source distillation returns one evidence packet
and stops before behavior design, runtime authoring, or deployment; rerun
Prompt 1 to apply it. Behavioral uncertainty waits for exact candidate bytes
and candidate-owned evaluation.

Every prompt performs one unit, recommends at most one successor, and stops
without beginning it. Use the proportionate proof budget in
[`deploy-prompts.md`](deploy-prompts.md): do not run a full suite at every
documentation or construction step. Prompts 1 through 5 preserve Git HEAD and
never stage or commit; optional Prompt 6 is the sole Git-delivery owner.

## Boundary

- Put reusable synthesis methods here.
- Put per-skill design judgment in `../skills/`.
- Put source research in `../../research/`.
- Put behavior evidence in `../../validation/`.
