# Prompt 01: Scope The Source Question

Use this as Step 1 of
[`../source-distillation-flow.md`](../source-distillation-flow.md).

```markdown
We are bounding one source question before searching.

Question: `<the question the evidence must answer>`
Intended use: `<the synthesis, decision, or practice this will inform>`
Known source material: `<paths, URLs, titles, repositories, or "none">`
Requested source lanes: `<online, upstream skills, books, papers, standards, engineering practice, or "choose">`
Known exclusions: `<out-of-scope topics or sources>`
Freshness requirement: `<current as of date, durable sources acceptable, or mixed>`
Output path: `<authorized path or "choose by method default">`
Revision feedback: `<feedback or "none">`

Do not search yet. Define the smallest research boundary that can answer the
question without assuming a future runtime or document design.

Return:

## Source Question

- one precise question;
- intended use;
- what a useful answer must decide or clarify;
- explicit exclusions.

## Evidence Boundary

| Needed Evidence | Preferred Source Lane | Freshness / Access Need | Why |
| --- | --- | --- | --- |

Name any supplied source that must be inspected and any source type that would
be insufficient by itself.

## Search Vocabulary

- exact terms and named sources;
- broader synonyms;
- likely authoritative organizations, authors, repositories, or indexes;
- noise terms or misleading lanes to avoid.

## Facet Decision

Choose one:

- `search-directly`: one bounded question can proceed to Prompt 03;
- `map-facets`: independent subquestions justify Prompt 02;
- `blocked`: missing scope or access prevents responsible search.

Name the output path and the smallest missing input when blocked.
```

Complete when the question, intended use, exclusions, evidence lanes,
freshness, and next decision are explicit.
