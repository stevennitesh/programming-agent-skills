# Evals

This is a compatibility owner for historical validation whose exact pack
identity remains unresolved. Canonical one-skill evaluations live under
[`../skills/<skill>/evals/<EV-id>/`](../skills/).

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

## Preserved owner gaps

- [`core-workflows.md`](core-workflows.md): historical pack-level routing,
  handoff, proof, mutation, and reconciliation evidence. It remains here
  without a fabricated composition epoch.
- [`2026-08-12-source-vocabulary-quality-lift.md`](2026-08-12-source-vocabulary-quality-lift.md):
  frozen cross-skill quality-lift evidence for source-vocabulary choices across
  design, testing, diagnosis, and simplification. It remains here without a
  fabricated per-skill evaluation identity or composition epoch.
