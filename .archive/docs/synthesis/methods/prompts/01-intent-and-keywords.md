# Prompt 01: Intent And Keywords

Use this as Step 1 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to extract the skill's intent, behavior surface, rough facet
candidates, and preliminary search vocabulary before online research or
runtime edits.

```markdown
We are preparing to deepen a Codex skill before researching sources or editing
`SKILL.md`.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Related files or skills: `<paths, or "unknown">`
User goal for this skill: `<what we want the skill to do better>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not research online yet.
Do not rewrite the skill yet.
Do not propose final runtime wording yet.

Read the current skill and any directly related support files. Extract the
skill's intent, behavior surface, rough facet candidates, and preliminary
search vocabulary.

Use this lens:

A good skill makes Codex behave predictably. We are looking for the behaviors
that should become more reliable, the failure modes the skill should prevent,
and the strong words that may later steer Codex toward upper-bound engineering
behavior.

Return:

## 1. Skill Intent

- What job does this skill exist to do?
- When should it be invoked?
- What should it make Codex do more predictably?
- What should it explicitly not do?

## 2. Current Behavior Surface

Identify the parts of the skill that affect behavior:

- invocation / description
- first action
- main steps
- gates / completion criteria
- stop or ask rules
- context pointers / support files
- validation or proof requirements
- final report / handoff behavior

## 3. Owner Map

Map the current ownership boundaries before proposing research facets. This is
not the final facet map; Prompt 02 owns final merge/split and ordering
decisions.

Use:

| Behavior / Concept | Current Owner | Keep Here / Point Elsewhere / Unclear | Why |
| --- | --- | --- | --- |

Owners can include:

- this skill;
- another skill;
- engineering contract;
- repo-local docs;
- support/reference docs;
- unclear / needs Prompt 02 boundary.

## 4. Preserve Inventory

List current behaviors that must not regress during research, compaction, or
runtime editing.

Use:

| Current Behavior | Source File / Line Or Section | Why It Must Not Regress |
| --- | --- | --- |

Prefer concrete source references over paraphrase-only claims. If exact line
numbers are inconvenient, cite the file and heading.

## 5. Failure Modes To Prevent

List average-agent behaviors this skill should prevent, such as:

- premature completion
- scope creep
- shallow evidence
- wrong tool or skill routing
- weak handoff
- generic advice
- over-explaining instead of acting
- editing before enough context
- missing validation
- duplicating another skill's job

Use skill-specific failure modes, not generic ones only.

## 6. Rough Facet Candidates

Sketch possible research facets. Do not finalize facet boundaries here; Prompt
02 owns the final facet map, research order, and merge/split decisions.

For each candidate facet, provide:

- facet name
- behavior surface affected
- research question
- why this facet matters
- likely source lanes
- likely evidence gate
- stop / ask condition
- out-of-scope boundary
- preliminary keywords and phrases

Use this table:

| Facet | Behavior Surface | Research Question | Source Lanes | Evidence Gate | Stop/Ask Rule | Preliminary Keywords |
| --- | --- | --- | --- | --- | --- | --- |

## 7. Facet Collision Risks

Identify rough-facet overlap for Prompt 02 to resolve. Do not decide final
facet boundaries here.

Use:

| Candidate Facet | Likely Overlap | Risk If Researched Alone | Prompt 02 Boundary Question |
| --- | --- | --- | --- |

## 8. Preliminary Keyword Bank

Group keywords by type:

### Professional Software Engineering Terms

Terms likely to appear in books, professional practice, architecture, testing,
product, delivery, or operations.

### Agentic / LLM Execution Terms

Terms related to coding agents, tool use, context, evaluation, trajectories,
guardrails, or completion criteria.

### Skill-Writing Terms

Terms related to invocation, context pointers, leading words, completion
criteria, no-ops, sprawl, sediment, branches, and progressive disclosure.

### Weak Or Noisy Terms

Terms that are probably too generic, overloaded, or decorative unless paired
with a concrete gate.

## 9. Source Search Seeds

For each rough facet candidate, suggest 5-15 search queries.

Prefer queries that can find:

- respected books
- official manuals
- empirical papers
- professional engineering guides
- high-signal field practice

Do not include broad vague searches unless they are paired with a stronger
term.

For each facet, also name search lanes that are likely to produce noise or
ownership drift.

Use this shape for each facet:

- `<facet>`
- Search seeds:
  - `<query>`
- Avoid / demote:
  - `<term or lane>` because `<why it is likely noisy or owned elsewhere>`

## 10. Boundaries Before Research

State what research should not do.

Include:

- what should stay out of `SKILL.md`
- what another skill or engineering contract probably owns
- what would count as over-research
- what would make a source worth keeping

## 11. Questions For Prompt 02

List the facet-boundary, merge/split, ownership, and research-order questions
Prompt 02 must resolve.

Do not choose the final facet map here. Phrase each item as a question or
decision for Prompt 02.

## 12. Output Summary

End with:

- intent decision:
  - `ready-for-facet-map`: continue to Prompt 02;
  - `clarify-intent`: ask the user or inspect the missing local context before
    continuing;
  - `refresh-current-surface`: reread current skill/support/owner files before
    continuing;
- the top 3-5 rough facets or facet-map questions Prompt 02 should resolve
- the strongest preliminary search terms
- the highest-risk owner boundaries to preserve
- the biggest risk if this skill is rewritten without research
- the likely shape of the eventual compact skill change
```

## Quality Bar

This prompt is complete when the output makes the next facet-map prompt
obvious, including current owners, preserve inventory, and open boundary
questions, or names the clarification/current-surface gap that blocks Prompt
02, without deciding the final facet map or proposing final runtime wording.
