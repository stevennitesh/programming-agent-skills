# Evals

Use this folder for repeatable validation ideas: fixtures, scoring rubrics,
task sets, harness notes, and before/after comparisons.

An eval note should state:

- behavior being measured;
- task fixture or dataset;
- requested and resolved model, when available;
- reasoning effort, reasoning mode, and text verbosity, when configurable;
- expected evidence;
- scoring rubric;
- failure modes;
- how results should feed back into synthesis or skill wording.

Keep evals small enough to run and compare across skill revisions.
Change one instruction, example, tool group, or runtime setting at a time. Rerun
the same fixtures and preserve behavior-bearing context, hard constraints,
approval boundaries, evidence requirements, and completion criteria.

## Current Suite

- [`core-workflows.md`](core-workflows.md): pack-level routing, handoff, proof, mutation, and reconciliation fixtures.
- [`prototype-b0/`](prototype-b0/): immutable executable minimum control for
  Prototype's baseline-first candidate proof.
- [`prototype-description-pre-prune/`](prototype-description-pre-prune/):
  frozen full-package control that differs from the Prompt 4 Prototype
  candidate only in the longer pre-prune description.
- [`prototype-prompt4/`](prototype-prompt4/): fixed B0-first behavior,
  contribution, authority, and live-probe protocols for Prototype acceptance.
- [`research-pruning-pre-prune/`](research-pruning-pre-prune/): immutable
  behavior-complete Research package used as the pruning-equivalence control.
