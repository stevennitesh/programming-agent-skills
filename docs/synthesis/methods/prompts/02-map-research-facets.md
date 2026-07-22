# Prompt 02: Map Research Facets

Use this optional Step 2 of
[`../source-distillation-flow.md`](../source-distillation-flow.md) only when
Prompt 01 decides `map-facets`.

```markdown
We are splitting one broad source question into independent research facets.

Scope packet: `<path or Prompt 01 output>`
Revision feedback: `<feedback or "none">`

Do not search yet. Do not create facets for future prose sections, agent steps,
or source types alone. Split only where subquestions require meaningfully
different evidence or can reach independent conclusions.

Return:

## Facet Map

| Order | Facet | Research Question | In Scope | Excluded | Source Lanes | Completion Evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Relationship Check

For each pair that may overlap, say whether to merge them, keep them separate,
or make one a shared source lane. Identify dependencies and contradictions that
must be compared during final distillation.

## Search Order

Name the first facet and why. Reuse shared searches without copying conclusions
between facets.

## Facet-Map Decision

Choose one:

- `ready-for-search`;
- `collapse-to-one-question` when the map adds no independent value;
- `revise-scope` when the original question or exclusions must change;
- `blocked`.
```

Complete when each retained facet has a distinct question and evidence need,
overlap is controlled, and unnecessary facets are removed.
