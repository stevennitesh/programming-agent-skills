# Prompt 04: Extract Concepts And Techniques

Use this as Step 4 of
[`../source-distillation-flow.md`](../source-distillation-flow.md).

```markdown
We are extracting source meaning before deciding what survives.

Source-search packet: `<path or Prompt 03 output>`
Question or facet: `<bounded research question>`
Revision feedback: `<feedback or "none">`

Inspect the exact queued source sections. Do not rely on search snippets or
uninspected summaries for stronger claims. Do not force every useful concept
into agent behavior or runtime wording.

Use claim labels exactly:

- `direct`;
- `corroborated`;
- `synthesis`;
- `inference`;
- `thin`.

Return:

## Coverage

| Queued Source / Target | Inspected / Skipped / Thin | Exact Sections Used | Consequence |
| --- | --- | --- | --- |

## Concepts

| Concept | Source And Locator | Claim Label | Meaning In Context | Importance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- |

## Techniques

| Technique | Source And Locator | Claim Label | Purpose | How It Works | When It Fits | Failure / Misuse Risk |
| --- | --- | --- | --- | --- | --- | --- |

## Tradeoffs, Failure Modes, And Evidence Standards

| Item | Source And Locator | Claim Label | Consequence | Counterpoint Or Limit |
| --- | --- | --- | --- | --- |

## Agreements And Disagreements

| Topic | Sources | Agreement / Conflict | Context Explaining Difference | Distillation Question |
| --- | --- | --- | --- | --- |

## Proposed Applications

Record applications only when useful. Label every application `inference` and
keep the source claim separate from the proposed adaptation.

| Source Concept / Technique | Proposed Use | Why It May Transfer | Assumption To Validate |
| --- | --- | --- | --- |

## Extraction Decision

Choose one:

- `ready-for-distillation`;
- `rerun-extraction` with the skipped section or missing context named;
- `return-to-search` with the evidence gap named;
- `revise-scope-or-facets`;
- `blocked`.
```

Complete when every extracted item has exact provenance, honest claim strength,
context, limitations, and enough meaning for independent triage.
