# Validation

Validation docs will hold evidence that the skill pack changes agent behavior.

Use this folder for:

- representative task fixtures;
- transcript reviews;
- before/after skill behavior notes;
- eval notes;
- skipped checks and residual risks from validation runs.

## Rule

Validation must be concrete. Prefer real tasks, transcript evidence, commands,
diffs, and failure observations over impressions.

## Lanes

| Lane | Role |
| --- | --- |
| [`shared/`](shared/) | Shared protocols, fixtures, schemas, and the mechanical Fresh Composition Epoch envelope. |
| [`skills/`](skills/) | Per-skill campaign and evaluation evidence under stable identities. |
| [`skill-pack/`](skill-pack/) | Pack-integration evidence for one composition epoch. |
| [`transcripts/`](transcripts/) | Compatibility pointer for unresolved historical pack evidence. |
| [`evals/`](evals/) | Compatibility pointer for unresolved historical pack evidence. |

Use this folder for cross-run evidence, transcript reviews, and repeatable eval
material that should remain durable across runs.

## Boundary

Research decides what might matter. Synthesis decides what should change.
Validation records whether the change worked.

Validation should name:

- the skill or behavior under test;
- the task or transcript used;
- the expected behavior;
- observed behavior;
- evidence;
- failure modes;
- follow-up changes.

Canonical Fresh Composition Epoch routes are
`docs/validation/shared/README.md`, `docs/validation/skills/README.md`, and
`docs/validation/skill-pack/README.md`. Validation owns evidence and tested
bounds; pack acceptance remains a synthesis decision.
