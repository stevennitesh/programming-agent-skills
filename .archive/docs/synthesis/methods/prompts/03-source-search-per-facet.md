# Prompt 03: Source Search Per Facet

Use this as Step 3 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to find and rank high-quality sources for one facet before any
detailed source extraction happens.

````markdown
We are researching one facet of a Codex skill so we can later compress the best
source pressure into strong runtime skill language.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Facet source lanes: `<primary / secondary / avoided lanes from facet map>`
Facet collision watchpoints: `<relevant collision-map rows, or "none">`
Prior artifacts:
- Intent and keywords: `<path or paste>`
- Facet map: `<path or paste>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not rewrite the skill yet.
Do not extract detailed lessons yet.
Do not summarize sources for their own sake.

Your job is to find and rank the best sources for this facet.

Search for sources that can raise the skill's engineering taste and agent
behavior. Prefer sources with strong professional consensus, practical
usefulness, or direct relevance to agentic coding behavior.

Verify sources through live search, official pages, publisher pages, library
metadata, paper indexes, or primary documentation when possible. Do not build
the source list from memory alone. Separate sources actually found from sources
expected to matter but not yet verified.

Use these source lanes where relevant:

- classic software engineering books
- architecture/design books
- testing/TDD/proof sources
- product/requirements sources
- delivery/operations sources
- empirical software engineering papers
- LLM / agentic coding papers
- AI tooling manuals and official docs
- prompt/skill-writing sources
- controlled language / procedure-writing sources
- high-signal professional field reports

Return:

## 1. Facet Search Objective

State what this source search is trying to find.

Include:

- the behavior we want to improve;
- what "upper-bound" source quality means for this facet;
- what kinds of sources would be noise.

## 2. Step 2 Handoff Check

Confirm how the facet map shapes this search.

Use this table:

| Facet Map Input | Search Impact | Source / Query Consequence | Notes |
| --- | --- | --- | --- |

Cover at least:

- facet boundary;
- primary and secondary source lanes;
- avoided source lanes;
- relevant cross-facet collision watchpoints;
- any first-facet integration-risk note.

Do not redo Prompt 02. This section should keep the source search inside the
facet's boundary and identify when the source landscape suggests the facet map
needs revision.

## 3. Search Queries

Provide the actual search queries to run.

Group them by lane:

### Books

- `<query>`

### Papers

- `<query>`

### Manuals / Official Docs

- `<query>`

### Agentic Coding / LLM Tooling

- `<query>`

### Field Practice

- `<query>`

For each query, include why it is worth running.

## 4. Verified Source List

List sources actually found or verified during the search.

Use this table:

| Rank | Source | Type | Link / Locator | Verification Basis | Access / Extractability | Why It Matters | Expected Contribution | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rank by usefulness for improving this skill facet, not by fame.
Access / extractability should say whether Prompt 04 can extract from the
source directly, needs a public excerpt or paper PDF, or should treat the
source as verified-but-not-extractable.

## 5. Expected But Unverified Sources

List sources that may matter but were not verified yet.

Use this table:

| Source | Why It Might Matter | How To Verify | Keep Searching? |
| --- | --- | --- | --- |

Do not promote unverified sources into the recommended extraction set unless
they are verified first.

## 6. Source Quality Notes

For each promising source, classify its value:

- `core`: likely essential for this facet
- `supporting`: useful but not central
- `bridge`: helps translate between SWE and agent behavior
- `contrast`: useful because it warns against a failure mode
- `reject`: not worth extraction

For rejected or weak sources, explain why briefly.

## 7. Searched / Rejected / Thin Lanes

Record the lanes that were tried, rejected, or weak.

Use:

| Lane Or Query Family | Result | Keep / Reject / Rerun Later | Reason |
| --- | --- | --- | --- |

This is a search log, not a bibliography. Include enough detail to prevent a
future rerun from repeating weak searches, and to make missing lanes explicit
rather than accidental.

## 8. Extraction Readiness Check

Before recommending sources for Prompt 04, answer:

- Are the recommended sources verified?
- Are they accessible enough for extraction?
- Does each recommended source have a clear extraction target?
- Which source is verified but too thin, indirect, or inaccessible for
  extraction?
- Which source would require user access, a library copy, or a substitute
  before extraction?

## 9. Expected Extraction Targets

For each core/supporting/bridge source, state what the next prompt should
extract.

Use:

| Source | Extract For | Watch For | Avoid Extracting |
| --- | --- | --- | --- |

Extraction targets may include:

- leading words;
- behavior gates;
- failure modes;
- stop/ask rules;
- evidence standards;
- sequencing discipline;
- weak/no-op language to avoid;
- agentic bridge vocabulary.

## 10. Boundary Stress Test

After seeing the source landscape, check whether the facet still fits.

Answer:

- Did any strong source actually belong to another facet or skill?
- Did any source reveal that this facet is too broad, too narrow, or wrongly
  named?
- Did the search surface a missing source lane that should change Prompt 02?
- Are the collision watchpoints still manageable for this facet?
- Should the next step continue to extraction, rerun search, or revise the
  facet map?

Do not solve the boundary problem here. If the boundary no longer fits, choose
`revise-facet-map` in the output decision.

## 11. Coverage Check

Answer:

- Do we have at least one strong professional SWE source?
- Do we have at least one source that connects to agentic coding or LLM
  behavior?
- Do we have at least one source that gives operational gates rather than taste
  words?
- Are we over-weighting one author, school, era, or tool?
- What source lane is missing?
- Which recommended sources still need stronger verification?

## 12. Recommended Source Set

Choose the smallest strong set to extract from next.

Use this table:

| Priority | Source | Why Extract Next |
| --- | --- | --- |

Keep this set focused. Prefer 5-10 excellent sources over a large bibliography.
Use only verified sources.

## 13. Output Artifact

Write the final source search packet to:

`docs/research/skill-facets/<skill-name>/FACET-<n>-<name>-sources.md`

End with:

- source-search decision:
  - `ready-for-extraction`: continue to Prompt 04;
  - `rerun-source-search`: search again because coverage, verification, or
    source quality is not good enough;
  - `revise-facet-map`: return to Prompt 02 because the facet boundary or
    research question no longer fits the source landscape;
  - `blocked`: stop until named source access, verification, or user scope is
    resolved;
- best source to start extraction from;
- strongest source lane;
- weakest source lane;
- biggest risk in the source set;
- whether this facet is ready for source extraction.

The source-search decision label must be explicit. Do not omit it.
````

## Quality Bar

This prompt is complete when it produces a ranked source set strong enough for
the next prompt to extract behavior-changing language without redoing search,
accounts for the Prompt 02 boundary/source-lane inputs, makes source access
clear, and either explicitly decides to continue, rerun search, revise the facet
map, or block.
