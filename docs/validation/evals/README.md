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

Track reusable fixtures, rubrics, protocols, compact result summaries, and
terminal decisions. Do not track raw model outputs, per-sample payloads,
generated worktrees, copied historical runtimes, or tests whose only purpose is
to preserve a past campaign identity. During active work, place locally useful
raw evidence under ignored `.tmp/campaign-evidence/`; later campaigns must rerun
behavioral proof instead of treating that local archive as authority.

## Current Suite

- [`core-workflows.md`](core-workflows.md): pack-level routing, handoff, proof, mutation, and reconciliation fixtures.
- [`prototype-prompt4/`](prototype-prompt4/): fixed B0-first behavior,
  contribution, authority, and live-probe protocols for Prototype acceptance.
