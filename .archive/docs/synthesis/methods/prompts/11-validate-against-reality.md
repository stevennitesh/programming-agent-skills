# Prompt 11: Validate Against Reality

Use this as Step 11 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to test the plain-language candidate against real or representative
agent behavior and record concrete validation evidence.

````markdown
We are validating the plain-language skill candidate against real or
representative agent behavior.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or behavior: `<facet-number-and-name, or behavior name>`
Candidate runtime draft: `<path or paste Prompt 08 output>`
Detailed skill-context draft: `<path or paste Prompt 09 output>`
Plain-language candidate: `<path or paste Prompt 10 output>`
Plain-language candidate decision: `<Prompt 10 plain-language candidate decision>`
Traceability map and validation scenarios: `<Prompt 09/10 traceability map / scenarios>`
Existing skill text: `<path or paste relevant SKILL.md section>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for new sources.
Do not rewrite the skill yet.
Do not edit `SKILL.md` yet.
Do not final-prune yet.
Do not claim the skill improved without evidence.

Your job is to test whether the plain-language candidate would actually change
agent behavior in the intended direction. Validate the wording that might ship,
not the explanatory draft.

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
- plain-language candidate being tested;
- Prompt 10 plain-language candidate decision used;
- detailed skill-context draft and traceability used;
- validation lane chosen;
- why this lane is appropriate;
- what validation will not decide.

## 2. Handoff And Feedback Check

Confirm the draft is ready to validate before running or reviewing scenarios.

Use:

| Input | Used / Revised / Blocked | Validation Consequence | Notes |
| --- | --- | --- | --- |

Account for:

- Prompt 10 plain-language candidate decision;
- Prompt 09 detailed draft and traceability;
- traceability map;
- validation scenarios;
- support/context pointer placeholders;
- revision feedback.

If `Revision feedback` is not `none`, account for it before validating. If the
plain-language candidate decision is not `ready-for-reality-validation`, do not
validate anyway; return to the owning prompt named by the plain-language candidate
decision.

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 3. Expected Behavior

Define what improvement should look like.

Use:

| Behavior | Current / Risky Agent Behavior | Expected Improved Behavior | Evidence Needed |
| --- | --- | --- | --- |

## 4. Validation Scenario

Describe the task, transcript, fixture, or eval scenario.

Use:

| Scenario | Why It Tests The Behavior | Inputs / Evidence Surface | Expected Observation |
| --- | --- | --- | --- |

If this is transcript validation, include transcript path or source.
If this is a real-task validation, include repo/path/task context.
If this is an eval note, include the scoring target.

## 5. Draft Coverage

Map draft sections and candidate lines to validation evidence.

Use:

| Plain-Language Candidate Section / Line ID | Prompt 09/10 Validation ID | Behavior It Should Cause | Scenario That Tests It | Pass Signal | Fail Signal |
| --- | --- | --- | --- | --- | --- |

Validate the Step 10 plain-language candidate, not loose candidate lines or the
more explanatory Step 09 draft. Only validate plain-language sections assembled
from Prompt 08 candidate lines and Prompt 09 placement decisions.

## 6. Run / Review Notes

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

## 7. Results

Use:

| Behavior | Pass / Revise / Fail / Untested | Evidence | Notes |
| --- | --- | --- | --- |

Definitions:

- `Pass`: evidence supports the candidate wording.
- `Revise`: direction is right but wording/gate needs adjustment.
- `Fail`: candidate wording would not improve behavior or creates a regression.
- `Untested`: no adequate evidence yet.

## 8. Regression And Risk Check

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

## 9. Validation Decision

Choose one:

- `ready-for-final-prune`
- `revise-before-prune`
- `needs-more-validation`
- `blocked`

Explain why. If the decision is `revise-before-prune`, name the earliest
owning prompt to rerun: Prompt 10 for plain-language problems, Prompt 09
for draft assembly or placement, Prompt 08 for candidate wording or
validation-ID problems, or an earlier prompt for
behavior/source-boundary problems.

The validation decision label must be explicit. Do not omit it.

## 10. Handoff To Final Prune

End with:

- lines validated as ready;
- lines requiring revision;
- lines to cut;
- support/context pointer decisions confirmed;
- residual risks;
- validation evidence path;
- what Prompt 12 should do first.

Write the validation note to the best matching path:

- skill validation:
  `docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/11-validation.md`
- transcript validation:
  `docs/validation/transcripts/<skill-name>/<transcript-or-behavior>.md`
- eval note:
  `docs/validation/evals/<skill-name>/<behavior>.md`
````

## Quality Bar

This prompt is complete when validation records concrete evidence, skipped or
untested behavior is explicit, residual risk is named, and final pruning knows
which lines are ready, need revision, or should be cut.
