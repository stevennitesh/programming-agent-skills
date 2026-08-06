# Synthesis Methods

Methods are reusable ways to distill sources or deploy selected synthesis.

## Files

| File | Role |
| --- | --- |
| [`fresh-composition-epoch.md`](fresh-composition-epoch.md) | Parent controller for one Fresh Composition Epoch: schedule, integration, Lock, and cleanup handoff |
| [`deploy-prompts.md`](deploy-prompts.md) | Controllerless one-skill method: Contract Lock, Candidate Lock, conditional Behavioral Proof, and Release |
| [`source-distillation-flow.md`](source-distillation-flow.md) | Evidence-only flow for distilling primary and outside sources into important concepts and usable techniques |
| [`prompts/`](prompts/) | Optional prompts supporting source distillation |

The parent owner is `docs/synthesis/methods/fresh-composition-epoch.md`. The
one-skill owner is `docs/synthesis/methods/deploy-prompts.md`. Neither method
inherits the other's authority.

## Deploy Routing

Use `Run Deploy Campaign on <skill>` for one controllerless campaign organized
by four ordered proof obligations:

The lifecycle is:

```text
Contract Lock
  -> Candidate Lock
  -> conditional Behavioral Proof
  -> Release
```

The obligations are reasoning and proof, not persisted semantic lifecycle
state. Research runs only for a decision-relevant gap. Candidate-facing
deterministic and integration proof runs before behavioral dispatch or
promotion. Exact wording claims route to the existing conditional behavioral
protocol; real effects use disposable state. Release performs a cheap cut scan
and promotes only exact tested bytes. Installation and Git delivery retain
their existing authorities.

## Boundary

- Put reusable synthesis methods here.
- Put per-skill design judgment in `../skills/`.
- Put source research in `../../research/`.
- Put behavior evidence in `../../validation/`.
