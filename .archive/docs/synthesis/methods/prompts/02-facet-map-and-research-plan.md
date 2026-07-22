# Prompt 02: Facet Map And Research Plan

Use this as Step 2 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to turn the intent-and-keywords output into a clean facet map and
research plan before any source search happens.

````markdown
We are preparing to research a Codex skill facet-by-facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Step 1 output: `<paste or link the intent-and-keywords output>`
User goal for this skill: `<what we want the skill to do better>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not research online yet.
Do not rewrite the skill yet.
Do not propose final runtime wording yet.

Your job is to turn the Step 1 output into a clean facet map and research
plan. Choose the structure for research before any source search happens.

Use this lens:

A facet is a distinct behavior surface of the skill. It should be narrow enough
to research well, but large enough to produce useful skill behavior. Avoid
facets that are merely document sections unless they correspond to a real agent
behavior.

Return:

## 1. Skill Research Objective

State the overall research objective in 2-4 sentences.

Include:

- what behavior should improve;
- what quality bar matters;
- what must not change;
- what would count as over-research.

## 2. Step 1 Carry-Forward Audit

Confirm how the Step 1 output shaped this map.

Use this table:

| Step 1 Input | Used / Revised / Deferred / Blocked | Where It Shows Up | Notes |
| --- | --- | --- | --- |

Cover at least:

- skill intent and current behavior surface;
- owner map;
- preserve inventory;
- rough facet candidates;
- facet collision risks;
- source search seeds and noisy lanes;
- questions for Prompt 02.

Do not redo Prompt 01. This section should account for the inputs that affect
the facet map, not repeat all of them.

## 3. Final Facet Map

Create the final facet list.

Use this table:

| Order | Facet | Behavior Surface | Research Question | Why It Matters | Output Artifact |
| --- | --- | --- | --- | --- | --- |

For each facet:

- make the name short and behavior-oriented;
- make the research question answerable;
- avoid overlapping ownership;
- include the expected artifact path, e.g.
  `docs/research/skill-facets/<skill-name>/FACET-1-<SHORT-NAME>.md`.

## 4. Facet Boundaries

For each facet, define:

```markdown
### Facet <n>: <name>

Owns:
- <what this facet is allowed to decide>

Does not own:
- <what belongs to another facet, another skill, or the engineering contract>

Research should answer:
- <question 1>
- <question 2>
- <question 3>

Research should not answer:
- <out-of-scope question 1>
- <out-of-scope question 2>
```

## 5. Research Order

Rank the facets in the order they should be researched.

For each facet, explain:

- why it comes now;
- what later facets depend on it for;
- whether it can be researched independently;
- what signal would make us skip or merge it.

Then state whether this is only the research order or whether it is also a safe
runtime integration order. If early facet integration would carry collision
risk with later facets, name that risk.

## 6. Source Lanes By Facet

For each facet, choose likely source lanes.

Use these lanes where relevant:

- professional software engineering books
- architecture/design books
- testing/TDD/proof sources
- product/requirements sources
- delivery/operations sources
- empirical software engineering papers
- agentic coding / LLM tooling sources
- prompt/skill-writing sources
- controlled language / procedure-writing sources

Use this table:

| Facet | Primary Source Lanes | Secondary Source Lanes | Avoided Source Lanes |
| --- | --- | --- | --- |

Use Step 1 source seeds as inputs, but revise them when the final facet map
changes ownership. Keep noisy or owner-drifting lanes visible in `Avoided
Source Lanes`.

## 7. Search Vocabulary By Facet

For each facet, provide:

### Facet <n>: <name>

Strong search terms:
- `<term>`

Exact phrase queries:
- `"<phrase>" <context>`

Book/source anchors:
- `"<term>" "<book or author>"`
- `"<term>" site:<trusted-site>`

Agentic bridge queries:
- `"<agent term>" "<software engineering term>"`

Noise filters:
- avoid `<kind of source>`
- avoid `<weak framing>`

## 8. Evidence Gates By Facet

For each facet, state what a good research packet must produce:

- high-signal leading words;
- concrete agent behaviors;
- evidence gates;
- stop/ask rules;
- weak/no-op language to avoid;
- source quality notes;
- what should stay research-only.

## 9. Merge / Split / Retire Ledger

Account for every rough facet candidate from Step 1.

Use:

| Step 1 Candidate | Decision | Final Facet(s) | Why | Risk To Watch |
| --- | --- | --- | --- | --- |

Only merge facets when they would use the same sources and produce the same
runtime behavior. Split facets when one facet hides multiple agent behaviors.
Retire a candidate only when it is fully owned elsewhere, is a duplicate, or
would not change skill behavior.

## 10. Cross-Facet Collision Map

Identify overlaps the later prompts must keep visible.

Use:

| Collision | Primary Owner | Secondary Facet / Owner | Risk If Ignored | Later Prompt Watchpoint |
| --- | --- | --- | --- | --- |

This section should not solve later-facet behavior or write runtime wording. It
only names ownership and integration risks so later prompts can avoid accidental
duplication or premature facet integration.

## 11. First Facet Recommendation

Recommend the first facet to research.

Include:

- why it is first;
- what source lanes to start with;
- the 5 strongest search queries;
- what output file to create;
- whether researching it first is also safe for early facet integration, or
  whether runtime integration should wait for named related facets;
- what would make the research good enough to proceed to the next facet.

## 12. Output Summary

End with:

- facet-map decision:
  - `ready-for-source-search`: continue to Prompt 03 for the recommended first
    facet;
  - `revise-intent`: return to Prompt 01 because the goal, current behavior
    surface, or owner context is wrong or incomplete;
  - `revise-facet-map`: rerun Prompt 02 because facets overlap, hide multiple
    behaviors, or have unclear boundaries;
  - `blocked`: stop until the named source, owner, or user decision is
    available;
- final facet count;
- first facet to research;
- next artifact path;
- strongest cross-facet terms;
- biggest risk in the research plan.

The facet-map decision label must be explicit. Do not omit it.
````

## Quality Bar

This prompt is complete when the output makes the first source-search pass
obvious, accounts for the Step 1 owner/boundary inputs, and names any
intent/facet-boundary blocker that must be resolved before search, without
having done the research yet.
