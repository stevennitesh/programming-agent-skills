# Prompt 07: Full Behavior Synthesis

Use this as Step 7 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to explain the chosen behavior fully enough that Prompt 08 can
draft candidate runtime lines without losing taste, gates, or intent.

````markdown
We are writing a full behavior synthesis for one Codex skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Agent bridge: `<path or paste Prompt 06 output>`
Agent-bridge decision: `<Prompt 06 agent-bridge decision>`
Typed gates and branch exits: `<Prompt 06 typed gates / branch exit tables>`
Priority preservation: `<Prompt 06 priority preservation table>`
Duplicate-term choices: `<Prompt 06 duplicate-term resolution>`
Owner-severity decisions: `<Prompt 06 ownership / pointer decisions>`
Relevant research packets:
- Source search: `<path>`
- Source extraction: `<path>`
- Source triage: `<path>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for new sources.
Do not extract or triage new material.
Do not write final runtime `SKILL.md` wording yet.
Do not draft candidate runtime lines or convert the skill to plain language yet.
Do not audit candidate runtime lines yet.

Your job is to explain the chosen behavior fully enough that the candidate
runtime draft can compress it without losing taste, gates, or intent.

Use the return sections below as the shape.

Return:

## 1. Purpose

State what behavior this facet should make predictable.

Include:

- when the behavior matters;
- what average-agent behavior it prevents;
- what upper-bound engineering taste it should recruit;
- what this facet does not own.

## 2. Prompt 06 Handoff Check

Confirm how the agent bridge shapes this synthesis.

Use this table:

| Prompt 06 Input | Used / Revised / Deferred / Rejected | Synthesis Consequence | Notes |
| --- | --- | --- | --- |

Cover at least:

- agent-bridge decision;
- final behavior sequence;
- typed gates;
- branch exits;
- priority preservation;
- duplicate-term choices;
- owner-severity decisions;
- support/reference pointers;
- unresolved design questions.

If the agent-bridge decision is not `ready-for-full-behavior-synthesis`, do not
continue. Return to Prompt 06 or the earlier owning prompt named by the
agent-bridge decision.

Do not rebuild the agent bridge here. If the sequence, gates, branch exits, or
ownership still change during synthesis, choose `revise-agent-bridge`.

## 3. Revision Feedback Disposition

If `Revision feedback` is not `none`, account for it before synthesizing.

Use:

| Feedback Item | Affected Sections | Step 7 Action | Remaining Risk |
| --- | --- | --- | --- |

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 4. Source Pressure

Summarize only the source pressure that survived triage.

Use:

| Source / Prior | Pressure It Adds | Behavior It Supports | Runtime Or Support? |
| --- | --- | --- | --- |

Do not summarize books, papers, or docs broadly. Preserve only pressure that
affects agent behavior.

## 5. Chosen Behavior

Explain the agent bridge in prose.

Include:

- what the agent does first;
- what the agent must notice;
- what the agent must prove;
- when the agent stops, asks, narrows, or continues;
- what handoff the behavior creates.

## 6. Bridge Traceability

Map the prose back to the agent-bridge skeleton so Prompt 08 can draft
without losing execution structure.

Use:

| Agent Bridge Step / Gate | Synthesis Explanation | Candidate Behavior Fragment Or Gate Consequence | Must Preserve? |
| --- | --- | --- | --- |

`Must Preserve?` should be `yes`, `optional`, or `support-only`.

## 7. Leading Words

List the leading words that should survive into the candidate runtime draft.

Use:

| Leading Word | Primary / Support / Avoid | Why It Recruits Useful Priors | Behavior It Anchors | Risk If Misused |
| --- | --- | --- | --- | --- |

Use Prompt 06's duplicate-term choices. If two words do the same job, make one
primary and demote the other to support or avoid.

## 8. Agent Execution Surface

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

## 9. Evidence Gates

Explain the gates that matter.

Use:

| Gate | Gate Type | Why It Matters | Too Weak If | Too Heavy If | Candidate Consequence Shape |
| --- | --- | --- | --- | --- | --- |

Candidate consequence shapes are rough notes only, not runtime wording.

Preserve Prompt 06's gate types: `hard gate`, `recheck`, `handoff`, or
`support cue`.

## 10. Stop / Ask / Continue Logic

Explain the control logic.

Use:

| Situation | Agent Should | Why | Resume / Continue When |
| --- | --- | --- | --- |

Avoid timid over-asking. Stop/ask only when the agent would otherwise cross a
real commitment boundary or lose correctness.

## 11. Runtime vs Support Placement

Explain placement decisions.

Use:

| Material | Runtime / Support / Research / Elsewhere | Pointer Shape | Why |
| --- | --- | --- | --- |

This section should make later context-pointer decisions easier.

`Pointer Shape` should be one of:

- inline runtime
- short runtime pointer
- support/reference section
- later facet
- other skill/contract
- research-only

Do not decide final file paths or support-doc structure here.

## 12. Rejected Or Deferred Options

Record what should not move forward.

Use:

| Option | Reject / Defer | Why | Revive Only If |
| --- | --- | --- | --- |

## 13. Design Questions

List unresolved choices before candidate runtime drafting.

Use:

| Question | Why It Matters | Disposition | Suggested Resolution |
| --- | --- | --- | --- |

If there are no meaningful questions, say so.

`Disposition` should be one of:

- `resolved-for-candidate-draft`
- `defer-to-Prompt-08`
- `revise-agent-bridge`
- `blocked`

If any question changes the behavior sequence, typed gates, branches, or
ownership, choose `revise-agent-bridge` instead of continuing.

## 14. Verbose Draft Notes

Write temporary explanatory prose that exposes the behavior.

This can be more verbose than runtime skill text. It should still be
directional.

Focus on:

- what the agent should think with;
- what it should do;
- what it should prove;
- what it should not do;
- where it should stop or ask.

## 15. Candidate Runtime Budget

Separate what Prompt 08 must carry from what it may demote.

Use:

| Candidate | Must Include / Optional / Support-Only / Avoid | Why | Drop Or Demote If |
| --- | --- | --- | --- |

Prefer a small `Must Include` set. If everything is mandatory, synthesis has
not prepared the candidate runtime draft.

## 16. Candidate Draft Contract

State the contract for Prompt 08.

Use:

| Preserve | May Compress | Must Not Carry Forward | Why |
| --- | --- | --- | --- |

This should name the behavior gates, leading words, support pointers,
research-only material, repeated meanings to collapse, and owner boundaries
that candidate runtime drafting must respect.

## 17. Candidate Runtime Draft Handoff

End with the smallest useful handoff into Prompt 08.

Include:

- synthesis decision:
  - `ready-for-candidate-runtime-draft`: continue to Prompt 08;
  - `revise-agent-bridge`: return to Prompt 06 because the chosen behavior,
    sequence, gates, or ownership still changes;
  - `revise-triage`: return to Prompt 05 because source material placement or
    rejection changed;
  - `blocked-design-question`: stop until the named design/ownership question
    is resolved;
- chosen behavior;
- strongest leading words;
- candidate behavior fragments;
- candidate runtime budget;
- traceability from fragments to agent-bridge steps or gates;
- gate consequences to preserve;
- support/reference pointers needed;
- support pointer shapes;
- what stays research-only;
- repeated meanings Prompt 08 should collapse;
- validation scenario seeds to remember;
- biggest candidate-drafting risk.

The synthesis decision label must be explicit. Do not omit it.

Write the full behavior synthesis to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/07-full-behavior-synthesis.md`
````

## Quality Bar

This prompt is complete when Prompt 08 can draft candidate runtime lines without
reopening research or losing the behavior's taste, typed gates, branch exits,
placement decisions, repeated-meaning collapse targets, candidate draft
contract, or synthesis risks, or when it names the agent-bridge, triage, or
design loop needed before drafting.

Completion requires:

- the Prompt 06 agent-bridge decision is `ready-for-full-behavior-synthesis`;
- revision feedback is dispositioned;
- every typed gate, branch exit, priority, duplicate-term choice, and
  owner-severity decision is preserved, demoted, deferred, or looped back;
- every meaningful design question is resolved, deferred to Prompt 08, or
  blocked;
- repeated meanings and collapse targets are named for Prompt 08;
- no candidate runtime draft, plain-language candidate, validation, final
  prune, or `SKILL.md` edit has happened.
