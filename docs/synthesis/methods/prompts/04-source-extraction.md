# Prompt 04: Source Extraction

Use this as Step 4 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to extract behavior-changing material from verified sources without
triaging, synthesizing, or drafting runtime skill wording.

````markdown
We are extracting behavior-changing material from verified sources for one Codex
skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Source search packet: `<path or paste Prompt 03 output>`
Verified sources to extract from:
- `<source 1 with link / locator>`
- `<source 2 with link / locator>`

Do not search for new sources unless a cited source cannot be verified or
opened.
Do not rewrite the skill yet.
Do not decide final runtime wording yet.
Do not summarize sources for their own sake.
Do not discard extracted material just because it feels redundant; triage
happens in the next step.

Your job is to extract only material that could change Codex behavior.

For every extracted item, connect source language to agent behavior:

```text
source term / claim
  -> possible agent behavior
  -> evidence gate
  -> risk if misused
```

Return:

## 1. Extraction Scope

State:

- which facet is being extracted for;
- which verified sources are in scope;
- which source lanes are represented;
- what is intentionally out of scope.

## 2. Source Coverage

Use this table:

| Source | Sections / Chapters / Pages / Docs Used | Why This Part Was Used | Extraction Confidence |
| --- | --- | --- | --- |

Only include parts actually inspected.

## 3. Leading Words

Extract terms that could steer model behavior because they recruit strong
professional or agentic priors.

Use:

| Term | Source | Meaning In Source | Possible Skill Use | Behavior It Should Trigger | Risk / Caveat |
| --- | --- | --- | --- | --- | --- |

A leading word is worth extracting only if it could make the agent choose a
better action, gate, or standard.

## 4. Behavior Rules

Extract operational rules.

Use:

| Rule | Source | Agent Behavior | When It Applies | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- | --- | --- |

Rules should be phrased as behavior, not as book summaries.

## 5. Failure Modes

Extract named or implied failure modes.

Use:

| Failure Mode | Source | What Goes Wrong | Agent Warning Sign | Countermeasure | Evidence Gate |
| --- | --- | --- | --- | --- | --- |

Focus on failures this skill can actually prevent.

## 6. Evidence Gates

Extract standards of proof, completion, validation, or review.

Use:

| Gate | Source | What It Proves | How An Agent Can Check It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- |

A useful gate should help Codex know when to continue, stop, ask, or call done.

## 7. Stop / Ask Conditions

Extract conditions where autonomous progress should stop or narrow.

Use:

| Condition | Source | Why It Matters | Agent Should | Resume When |
| --- | --- | --- | --- | --- |

## 8. Agentic Bridge Language

Translate source concepts into LLM / coding-agent execution language.

Use:

| Source Concept | SWE Meaning | Agentic Meaning | Skill Behavior It Could Steer | Bridge Confidence |
| --- | --- | --- | --- | --- |

Examples of bridge targets:

- context selection
- tool use
- scratch work
- tests and evidence
- completion criteria
- self-review
- handoff
- stopping rules

## 9. Weak Or No-Op Language

Capture language that should probably not survive into runtime skill text.

Use:

| Weak Phrase | Source / Context | Why It Is Weak | Stronger Replacement Direction |
| --- | --- | --- | --- |

Do not over-polish replacements here. Final language comes later.

## 10. Extraction Notes By Source

For each source, provide a short note:

```markdown
### <Source>

Most useful extraction:
- <item>

Strongest behavior pressure:
- <item>

Likely research-only material:
- <item>

Open question:
- <question>
```

## 11. Handoff To Triage

End with:

- strongest extracted leading words;
- strongest behavior rules;
- strongest evidence gates;
- extraction gaps;
- source material that seems promising but uncertain;
- what Prompt 05 should triage first.

Write the extraction packet to:

`docs/research/skill-facets/<skill-name>/FACET-<n>-<name>-extraction.md`
````

## Quality Bar

This prompt is complete when every useful extracted item is tied to a possible
agent behavior, evidence gate, and misuse risk, without deciding what survives
into synthesis or runtime skill text.
