# Prompt 07: Generous Synthesis

Use this as Step 7 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to explain the chosen behavior generously enough that the compact
language pass can compress it without losing taste, gates, or intent.

````markdown
We are writing a generous synthesis for one Codex skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Behavior flow: `<path or paste Prompt 06 output>`
Relevant research packets:
- Source search: `<path>`
- Source extraction: `<path>`
- Source triage: `<path>`

Do not search for new sources.
Do not extract or triage new material.
Do not write final runtime `SKILL.md` wording yet.
Do not compact or plain-language the skill yet.
Do not audit candidate runtime lines yet.

Your job is to explain the chosen behavior generously enough that the
compact-language pass can compress it without losing taste, gates, or intent.

Use `docs/synthesis/GENEROUS-TEMPLATE.md` as the shape.

Return:

## 1. Purpose

State what behavior this facet should make predictable.

Include:

- when the behavior matters;
- what average-agent behavior it prevents;
- what upper-bound engineering taste it should recruit;
- what this facet does not own.

## 2. Source Pressure

Summarize only the source pressure that survived triage.

Use:

| Source / Prior | Pressure It Adds | Behavior It Supports | Runtime Or Support? |
| --- | --- | --- | --- |

Do not summarize books, papers, or docs broadly. Preserve only pressure that
affects agent behavior.

## 3. Chosen Behavior

Explain the behavior flow in prose.

Include:

- what the agent does first;
- what the agent must notice;
- what the agent must prove;
- when the agent stops, asks, narrows, or continues;
- what handoff the behavior creates.

## 4. Leading Words

List the leading words that should survive into compact language.

Use:

| Leading Word | Why It Recruits Useful Priors | Behavior It Anchors | Risk If Misused |
| --- | --- | --- | --- |

## 5. Agent Execution Surface

Explain how this facet becomes concrete agent action.

Use:

| Execution Surface | Agent Action | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- |

Execution surfaces may include:

- read
- inspect
- search
- compare
- test
- edit
- review
- stop
- ask
- delegate
- validate
- report

## 6. Evidence Gates

Explain the gates that matter.

Use:

| Gate | Why It Matters | Too Weak If | Too Heavy If | Candidate Blunt Form |
| --- | --- | --- | --- | --- |

Candidate blunt forms are rough notes only, not final runtime wording.

## 7. Stop / Ask / Continue Logic

Explain the control logic.

Use:

| Situation | Agent Should | Why | Resume / Continue When |
| --- | --- | --- | --- |

Avoid timid over-asking. Stop/ask only when the agent would otherwise cross a
real commitment boundary or lose correctness.

## 8. Runtime vs Support Placement

Explain placement decisions.

Use:

| Material | Runtime / Support / Research / Elsewhere | Why |
| --- | --- | --- |

This section should make later context-pointer decisions easier.

## 9. Rejected Or Deferred Options

Record what should not move forward.

Use:

| Option | Reject / Defer | Why | Revive Only If |
| --- | --- | --- | --- |

## 10. Design Questions

List unresolved choices before compacting.

Use:

| Question | Why It Matters | Suggested Resolution |
| --- | --- | --- |

If there are no meaningful questions, say so.

## 11. Verbose Draft Notes

Write temporary explanatory prose that exposes the behavior.

This can be more verbose than runtime skill text. It should still be
directional.

Focus on:

- what the agent should think with;
- what it should do;
- what it should prove;
- what it should not do;
- where it should stop or ask.

## 12. Compression Handoff

End with the smallest useful handoff into Prompt 08.

Include:

- chosen behavior;
- strongest leading words;
- candidate runtime wording fragments;
- blunt gates;
- support/reference pointers needed;
- what stays research-only;
- validation tasks to remember;
- biggest compression risk.

Write the generous synthesis to:

`docs/synthesis/verbose/skill-facets/<skill-name>/FACET-<n>-<name>-generous-synthesis.md`
````

## Quality Bar

This prompt is complete when the compact-language pass can draft candidate
runtime wording without reopening the research or losing the behavior's taste,
gates, placement decisions, or compression risks.
