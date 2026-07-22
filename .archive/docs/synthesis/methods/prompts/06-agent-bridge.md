# Prompt 06: Agent Bridge

Use this as Step 6 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to bridge triaged source language into an agent execution chain
without writing full behavior synthesis prose or final runtime skill wording.

````markdown
We are bridging triaged source material into agent behavior for one
Codex skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Source triage packet: `<path or paste Prompt 05 output>`
Triage decision: `<Prompt 05 triage decision>`
Runtime priority / budget: `<Prompt 05 must / should / could table>`
Bridge resolution plan: `<Prompt 05 bridge resolution plan>`
Duplicate-collapse notes: `<Prompt 05 duplicate / synonym collapse check>`
Owner-conflict severities: `<Prompt 05 owned-elsewhere severity table>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for sources.
Do not extract or triage new material except tiny gap notes.
Do not write final runtime `SKILL.md` wording yet.
Do not write full behavior synthesis prose yet.
Do not draft candidate runtime lines or convert the skill to plain language yet.

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

## 1. Agent Bridge Scope

State:

- facet being converted;
- triage packet used;
- surviving material in scope;
- material intentionally left for support/reference;
- what this agent bridge must not decide.

## 2. Prompt 05 Handoff Check

Confirm how triage shapes this agent bridge.

Use this table:

| Prompt 05 Input | Used / Revised / Deferred / Rejected | Bridge Consequence | Notes |
| --- | --- | --- | --- |

Cover at least:

- triage decision;
- runtime priority / budget;
- bridge resolution plan;
- duplicate / synonym collapse choices;
- owner-conflict severities;
- rejected temptations and watchpoints.

If triage did not provide enough priority, bridge translation, or ownership
clarity to build a flow, choose `return-to-triage`.

## 3. Priority Preservation Check

Show how Prompt 05's runtime priority survived into the bridge.

Use:

| Candidate | Must / Should / Could | Bridge Placement | Preserved / Demoted / Dropped | Why |
| --- | --- | --- | --- | --- |

The agent bridge should preserve `Must` behavior unless it violates the facet
boundary. `Should` and `Could` items may become branches, support cues, or
handoff notes.

## 4. Runtime Candidate Inventory

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

## 5. Duplicate-Term Resolution

Identify the primary term for each behavior role.

Use:

| Behavior Role | Primary Term | Support Terms | Demote / Avoid | Why |
| --- | --- | --- | --- | --- |

This keeps the agent bridge from carrying too many synonymous leading words
into Prompt 07. Do not decide final runtime wording.

## 6. Support / Reference Inventory

List support candidates that should inform behavior but probably not sit inline
in `SKILL.md`.

Use:

| Candidate | Why It Belongs In Support | Runtime Pointer Needed? |
| --- | --- | --- |

## 7. Behavior Sequence

Create the proposed execution chain.

Use numbered steps:

### Step <n>: <behavior name>

Trigger / situation:
- `<when this behavior runs>`

Agent action:
- `<what the agent does>`

Leading words:
- `<words that should anchor the behavior>`

Primary term:
- `<one primary leading word or phrase for this step>`

Supporting terms:
- `<secondary terms that inform the step, if any>`

Evidence gate:
- `<what proves the step is done>`

Gate type:
- `<hard gate / recheck / handoff / support cue>`

Stop / ask / continue rule:
- `<when to stop, ask, continue, or narrow>`

Failure prevented:
- `<what this step prevents>`

Source pressure:
- `<which triaged item supports it>`

Ownership severity:
- `<hard-boundary / later-facet-watchpoint / soft-reference / support-only / none>`

Next:
- `<next step, branch, or handoff>`

Use gate types as follows:

- `hard gate`: must pass before this facet can continue;
- `recheck`: inspect and either continue, narrow, or branch;
- `handoff`: pass to another facet, skill, or user-owned decision;
- `support cue`: keep as support/reference pressure rather than inline
  behavior.

## 8. Branches

Identify any branches in the agent bridge.

Use:

| Branch | Trigger | Behavior | Gate | Exit Type | Rejoin / Exit |
| --- | --- | --- | --- | --- | --- |

Only include branches that materially change agent behavior. Avoid branching
for stylistic variations.

`Exit Type` should be one of:

- `rejoin-flow`
- `handoff-facet`
- `handoff-skill`
- `ask-user`
- `record-follow-up`
- `blocked`

## 9. Completion Criteria

Define what "done" means for this facet's behavior.

Use:

| Criterion | Gate Type | What It Proves | How Agent Checks It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- |

Criteria should be checkable and tied to the facet, not generic.

## 10. Stop / Ask Rules

Consolidate stop and ask rules.

Use:

| Rule | Stop / Ask / Narrow / Continue | Why | Resume Condition |
| --- | --- | --- | --- |

Reject rules that would make the agent ask instead of doing ordinary
engineering work.

## 11. Ownership And Pointer Decisions

Decide where each behavior belongs later.

Use:

| Item | Runtime Skill | Support Doc | Research Only | Owned Elsewhere | Conflict Severity | Why |
| --- | --- | --- | --- | --- | --- | --- |

This is placement guidance only. Do not draft final wording.

## 12. Agent Bridge Risks

List risks in this agent bridge.

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

## 13. Handoff To Full Behavior Synthesis

End with:

- agent-bridge decision:
  - `ready-for-full-behavior-synthesis`: continue to Prompt 07;
  - `return-to-triage`: return to Prompt 05 because runtime/support ownership,
    rejection, or bridge translation is still unclear;
  - `revise-facet-map`: return to Prompt 02 because the agent bridge exposes
    overlapping facets or an owned-elsewhere facet;
  - `blocked`: stop until the named source, owner, or user decision is
    resolved;
- final behavior sequence;
- strongest leading words;
- strongest gates;
- support/reference pointers needed;
- unresolved design questions;
- ownership conflicts;
- what Prompt 07 should explain in prose.

The agent-bridge decision label must be explicit. Do not omit it.

Write the agent bridge to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/06-agent-bridge.md`
````

## Quality Bar

This prompt is complete when the facet has a clear agent execution skeleton with
ordered actions, typed gates, primary/supporting terms, branch exit types,
stop/ask rules, owner-severity-aware placement guidance, priority preservation,
and a handoff ready for full behavior synthesis, or when it names the triage/facet
loop needed before synthesis.
