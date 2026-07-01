# Prompt 10: Validate Against Reality

Use this as Step 10 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to test audited candidate skill wording against real or
representative agent behavior and record concrete validation evidence.

````markdown
We are validating audited candidate skill wording against real or
representative agent behavior.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or behavior: `<facet-number-and-name, or behavior name>`
Compact draft: `<path or paste Prompt 08 output>`
Behavior audit: `<path or paste Prompt 09 output>`
Existing skill text: `<path or paste relevant SKILL.md section>`

Do not search for new sources.
Do not rewrite the skill yet.
Do not edit `SKILL.md` yet.
Do not final-prune yet.
Do not claim the skill improved without evidence.

Your job is to test whether the audited candidate wording would actually change
agent behavior in the intended direction.

Use the validation lane that best fits the evidence available:

- `real-task`: run or reason through a real repo task using the candidate
  wording
- `transcript-review`: compare old transcript behavior against the intended
  behavior
- `fixture`: create a small representative task scenario
- `eval-note`: define a repeatable eval or scoring rubric
- `before-after`: compare current skill wording versus candidate wording

Return:

## 1. Validation Scope

State:

- skill and facet or behavior under test;
- candidate wording being validated;
- behavior audit used;
- validation lane chosen;
- why this lane is appropriate;
- what validation will not decide.

## 2. Expected Behavior

Define what improvement should look like.

Use:

| Behavior | Current / Risky Agent Behavior | Expected Improved Behavior | Evidence Needed |
| --- | --- | --- | --- |

## 3. Validation Scenario

Describe the task, transcript, fixture, or eval scenario.

Use:

| Scenario | Why It Tests The Behavior | Inputs / Evidence Surface | Expected Observation |
| --- | --- | --- | --- |

If this is transcript validation, include transcript path or source.
If this is a real-task validation, include repo/path/task context.
If this is an eval note, include the scoring target.

## 4. Candidate Line Coverage

Map candidate lines to validation evidence.

Use:

| Candidate Line / Line ID | Behavior It Should Cause | Scenario That Tests It | Pass Signal | Fail Signal |
| --- | --- | --- | --- | --- |

Only validate lines that survived Prompt 09 or must be revised before
validation.

## 5. Run / Review Notes

Record what was actually done.

Use:

```markdown
Validation action:
- <command, transcript review, scenario walkthrough, or eval design>

Observed evidence:
- <concrete evidence>

Limitations:
- <what this validation cannot prove>
```

Prefer concrete observations: commands, diffs, transcript excerpts, task
outcomes, failure observations, or explicit scenario reasoning.

## 6. Results

Use:

| Behavior | Pass / Revise / Fail / Untested | Evidence | Notes |
| --- | --- | --- | --- |

Definitions:

- `Pass`: evidence supports the candidate wording.
- `Revise`: direction is right but wording/gate needs adjustment.
- `Fail`: candidate wording would not improve behavior or creates a regression.
- `Untested`: no adequate evidence yet.

## 7. Regression And Risk Check

Use:

| Existing Behavior / Risk | Protected? | Evidence | Follow-Up |
| --- | --- | --- | --- |

Check for:

- lost existing behavior;
- over-asking;
- under-asking;
- too-heavy gates;
- too-weak gates;
- context bloat;
- duplicated ownership;
- harder invocation;
- unclear completion criteria.

## 8. Validation Decision

Choose one:

- `ready-for-final-prune`
- `revise-before-prune`
- `needs-more-validation`
- `blocked`

Explain why.

## 9. Handoff To Final Prune

End with:

- lines validated as ready;
- lines requiring revision;
- lines to cut;
- support/context pointer decisions confirmed;
- residual risks;
- validation evidence path;
- what Prompt 11 should do first.

Write the validation note to the best matching path:

- skill validation:
  `docs/validation/skills/<skill-name>/<facet-or-behavior>.md`
- transcript validation:
  `docs/validation/transcripts/<skill-name>/<transcript-or-behavior>.md`
- eval note:
  `docs/validation/evals/<skill-name>/<behavior>.md`
````

## Quality Bar

This prompt is complete when validation records concrete evidence, skipped or
untested behavior is explicit, residual risk is named, and final pruning knows
which lines are ready, need revision, or should be cut.
