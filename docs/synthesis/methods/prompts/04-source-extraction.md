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
Recommended source set: `<sources Prompt 03 recommended for extraction>`
Expected extraction targets: `<Prompt 03 extraction-target table or summary>`
Source access notes: `<Prompt 03 access / extractability notes>`
Verified sources to extract from:
- `<source 1 with link / locator>`
- `<source 2 with link / locator>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

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

Label claim strength as:

- `direct`: directly backed by inspected source text;
- `cross-source`: synthesized from multiple inspected sources;
- `bridge`: an inference translating source material into coding-agent behavior;
- `thin`: plausible but weakly supported by accessible source material.

Return:

## 1. Extraction Scope

State:

- which facet is being extracted for;
- which verified sources are in scope;
- which source lanes are represented;
- what is intentionally out of scope.

## 2. Prompt 03 Handoff Check

Confirm how the source-search packet shaped this extraction.

Use this table:

| Prompt 03 Input | Used / Revised / Skipped | Extraction Consequence | Notes |
| --- | --- | --- | --- |

Cover at least:

- recommended source set;
- expected extraction targets;
- source access / extractability notes;
- rejected or thin lanes;
- source-search decision and any coverage warnings.

If you extract from sources beyond Prompt 03's recommended set, name why. If a
recommended source is skipped, name why. Do not use this section to triage what
survives; Prompt 05 owns survival decisions.

## 3. Source Coverage

Use this table:

| Source | Prompt 03 Status | Access / Claim Depth | Sections / Chapters / Pages / Docs Used | Why This Part Was Used | Extraction Confidence |
| --- | --- | --- | --- | --- | --- |

Only include parts actually inspected.

Use `Access / Claim Depth` to distinguish:

- full text inspected;
- chapter, excerpt, official page, or primary doc inspected;
- abstract, metadata, or summary only;
- source-search note only.

Do not give `High` extraction confidence to a claim that rests only on
metadata, abstracts, or source-search notes unless the claim is correspondingly
narrow.

## 4. Extraction Target Coverage

Account for the extraction targets from Prompt 03.

Use:

| Source | Prompt 03 Target | Extracted / Skipped / Thin | Where It Appears | Notes |
| --- | --- | --- | --- | --- |

This section keeps extraction tied to the source-search plan. It should not
discard extra useful material, but it should make unplanned extraction visible.

## 5. Leading Words

Extract terms that could steer model behavior because they recruit strong
professional or agentic priors.

Use:

| Term | Source | Claim Strength | Meaning In Source | Possible Skill Use | Behavior It Should Trigger | Risk / Caveat |
| --- | --- | --- | --- | --- | --- | --- |

A leading word is worth extracting only if it could make the agent choose a
better action, gate, or standard.

## 6. Behavior Rules

Extract operational rules.

Use:

| Rule | Source | Claim Strength | Agent Behavior | When It Applies | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- | --- | --- | --- |

Rules should be phrased as behavior, not as book summaries.

## 7. Failure Modes

Extract named or implied failure modes.

Use:

| Failure Mode | Source | Claim Strength | What Goes Wrong | Agent Warning Sign | Countermeasure | Evidence Gate |
| --- | --- | --- | --- | --- | --- | --- |

Focus on failures this skill can actually prevent.

## 8. Evidence Gates

Extract standards of proof, completion, validation, or review.

Use:

| Gate | Source | Claim Strength | What It Proves | How An Agent Can Check It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- | --- |

A useful gate should help Codex know when to continue, stop, ask, or call done.

## 9. Stop / Ask Conditions

Extract conditions where autonomous progress should stop or narrow.

Use:

| Condition | Source | Claim Strength | Why It Matters | Agent Should | Resume When |
| --- | --- | --- | --- | --- | --- |

## 10. Agentic Bridge Language

Translate source concepts into LLM / coding-agent execution language.

Use:

| Source Concept | SWE Meaning | Agentic Meaning | Claim Strength | Skill Behavior It Could Steer | Bridge Confidence |
| --- | --- | --- | --- | --- | --- |

Examples of bridge targets:

- context selection
- tool use
- scratch work
- tests and evidence
- completion criteria
- self-review
- handoff
- stopping rules

## 11. Weak Or No-Op Language

Capture language that should probably not survive into runtime skill text.

Use:

| Weak Phrase | Source / Context | Why It Is Weak | Stronger Replacement Direction |
| --- | --- | --- | --- |

Do not over-polish replacements here. Final language comes later.

## 12. Boundary Drift Notes

Flag extracted material that may belong outside this facet.

Use:

| Extracted Material | Possible Owner | Why It May Drift | Prompt 05 Triage Question |
| --- | --- | --- | --- |

Possible owners include another facet, another skill, the engineering contract,
support/reference docs, or research-only context. Do not decide final ownership
here; just make the drift visible for Prompt 05.

## 13. Extraction Notes By Source

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

## 14. Handoff To Triage

End with:

- extraction decision:
  - `ready-for-triage`: continue to Prompt 05;
  - `rerun-extraction`: inspect the verified sources again because important
    behavior, gates, or failure modes are missing;
  - `return-to-source-search`: return to Prompt 03 because source coverage or
    verification is insufficient;
  - `revise-facet-map`: return to Prompt 02 because extracted material does not
    fit the facet boundary;
- strongest extracted leading words;
- strongest behavior rules;
- strongest evidence gates;
- extraction gaps;
- source material that seems promising but uncertain;
- what Prompt 05 should triage first.

The extraction decision label must be explicit. Do not omit it.

Write the extraction packet to:

`docs/research/skill-facets/<skill-name>/FACET-<n>-<name>-extraction.md`
````

## Quality Bar

This prompt is complete when every useful extracted item is tied to a possible
agent behavior, evidence gate, misuse risk, and claim strength; the Prompt 03
source-search handoff is accounted for; boundary drift is flagged without
deciding ownership; and the output does not decide what survives into synthesis
or runtime skill text, or it names the search or facet-boundary loop needed
before triage.
