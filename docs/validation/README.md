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
| [`skills/`](skills/) | Per-skill validation plans, before/after notes, and behavior checks. |
| [`transcripts/`](transcripts/) | Transcript reviews that show how agents actually behaved. |
| [`evals/`](evals/) | Repeatable eval notes, fixtures, scoring rubrics, and harness ideas. |

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
