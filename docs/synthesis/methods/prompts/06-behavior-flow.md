# Prompt 06: Behavior Flow

Use this as Step 6 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to turn triaged source material into an agent execution chain
without writing generous synthesis prose or final runtime skill wording.

````markdown
We are turning triaged source material into an agent behavior flow for one
Codex skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Source triage packet: `<path or paste Prompt 05 output>`

Do not search for sources.
Do not extract or triage new material except tiny gap notes.
Do not write final runtime `SKILL.md` wording yet.
Do not write generous synthesis prose yet.
Do not compact or plain-language the skill yet.

Your job is to turn the surviving source material into an execution chain: what
the agent should do, in what order, under what conditions, with what gates.

Use this shape:

```text
trigger / situation
  -> agent action
  -> evidence gate
  -> stop / ask / continue rule
  -> next action or handoff
```

Return:

## 1. Behavior Flow Scope

State:

- facet being converted;
- triage packet used;
- surviving material in scope;
- material intentionally left for support/reference;
- what this behavior flow must not decide.

## 2. Runtime Candidate Inventory

List the runtime candidates from triage.

Use:

| Candidate | Type | Why It Survived | Behavior Role |
| --- | --- | --- | --- |

Types may include:

- leading word
- behavior rule
- evidence gate
- stop/ask rule
- failure mode
- bridge translation

## 3. Support / Reference Inventory

List support candidates that should inform behavior but probably not sit inline
in `SKILL.md`.

Use:

| Candidate | Why It Belongs In Support | Runtime Pointer Needed? |
| --- | --- | --- |

## 4. Behavior Sequence

Create the proposed execution chain.

Use numbered steps:

### Step <n>: <behavior name>

Trigger / situation:
- `<when this behavior runs>`

Agent action:
- `<what the agent does>`

Leading words:
- `<words that should anchor the behavior>`

Evidence gate:
- `<what proves the step is done>`

Stop / ask / continue rule:
- `<when to stop, ask, continue, or narrow>`

Failure prevented:
- `<what this step prevents>`

Source pressure:
- `<which triaged item supports it>`

Next:
- `<next step, branch, or handoff>`

## 5. Branches

Identify any branches in the behavior flow.

Use:

| Branch | Trigger | Behavior | Gate | Rejoin / Exit |
| --- | --- | --- | --- | --- |

Only include branches that materially change agent behavior. Avoid branching
for stylistic variations.

## 6. Completion Criteria

Define what "done" means for this facet's behavior.

Use:

| Criterion | What It Proves | How Agent Checks It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- |

Criteria should be checkable and tied to the facet, not generic.

## 7. Stop / Ask Rules

Consolidate stop and ask rules.

Use:

| Rule | Stop / Ask / Narrow / Continue | Why | Resume Condition |
| --- | --- | --- | --- |

Reject rules that would make the agent ask instead of doing ordinary
engineering work.

## 8. Ownership And Pointer Decisions

Decide where each behavior belongs later.

Use:

| Item | Runtime Skill | Support Doc | Research Only | Owned Elsewhere | Why |
| --- | --- | --- | --- | --- | --- |

This is placement guidance only. Do not draft final wording.

## 9. Behavior Flow Risks

List risks in this behavior flow.

Use:

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |

Look for:

- sequence too long;
- branch too fuzzy;
- gate too vague;
- gate too heavy;
- leading word too weak;
- ownership conflict;
- accidental duplication with engineering contract or another skill.

## 10. Handoff To Generous Synthesis

End with:

- final behavior sequence;
- strongest leading words;
- strongest gates;
- support/reference pointers needed;
- unresolved design questions;
- ownership conflicts;
- what Prompt 07 should explain in prose.

Write the behavior flow to:

`docs/synthesis/verbose/skill-facets/<skill-name>/FACET-<n>-<name>-behavior-flow.md`
````

## Quality Bar

This prompt is complete when the facet has a clear execution skeleton with
ordered actions, gates, branches, stop/ask rules, placement guidance, and a
handoff ready for generous synthesis.
