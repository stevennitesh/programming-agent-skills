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

## 3. Failure Modes To Prevent

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

## 4. Rough Facet Candidates

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

## 5. Preliminary Keyword Bank

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

## 6. Source Search Seeds

For each rough facet candidate, suggest 5-15 search queries.

Prefer queries that can find:

- respected books
- official manuals
- empirical papers
- professional engineering guides
- high-signal field practice

Do not include broad vague searches unless they are paired with a stronger
term.

## 7. Boundaries Before Research

State what research should not do.

Include:

- what should stay out of `SKILL.md`
- what another skill or engineering contract probably owns
- what would count as over-research
- what would make a source worth keeping

## 8. Output Summary

End with:

- the top 3-5 facets to research first
- the strongest preliminary search terms
- the biggest risk if this skill is rewritten without research
- the likely shape of the eventual compact skill change
```

## Quality Bar

This prompt is complete when the output makes the next source-search prompt
obvious, without proposing final runtime wording.
