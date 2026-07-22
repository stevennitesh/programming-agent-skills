# Synthesis Methods

Methods are reusable ways to distill sources or deploy selected synthesis.

Use this folder for process docs that apply across multiple skills or skill
families.

## Files

| File | Role |
| --- | --- |
| [`deploy-prompts.md`](deploy-prompts.md) | Default numbered workflow for finalizing one whole-skill synthesis, building and evaluating an experimental candidate, promoting it, and optionally delivering it through Git. |
| [`source-distillation-flow.md`](source-distillation-flow.md) | Optional flow for distilling primary and outside sources into important concepts and usable techniques. |
| [`prompts/`](prompts/) | Optional prompts supporting source distillation. |

## Routing

Use Deploy Prompts once a whole-skill synthesis exists. Use source distillation
when outside evidence or deliberate pruning would materially improve a
synthesis or engineering decision. Source distillation returns an evidence
packet and stops before behavior design, runtime authoring, or deployment.

## Boundary

- Put reusable synthesis methods here.
- Put per-skill design judgment in `../skills/`.
- Put source research in `../../research/`.
- Put behavior evidence in `../../validation/`.
