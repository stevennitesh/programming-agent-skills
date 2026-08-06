# Prompt 03: Search And Verify Sources

Use this as Step 3 of
[`../source-distillation-flow.md`](../source-distillation-flow.md).

```markdown
We are finding the smallest strong source set for one bounded question or
facet.

Scope packet: `<path or Prompt 01 output>`
Facet map: `<path, relevant facet, or "not needed">`
Supplied sources: `<paths, URLs, titles, repositories, or "none">`
Revision feedback: `<feedback or "none">`

Search the requested lanes. Prefer sources closest to each claim and verify
changeable claims live. Use credible secondary sources only for comparison,
adoption evidence, or context they uniquely add.

When supplied sources include a skill pack, first search independently from
the intended behavior without using that pack's terminology. Then inspect the
pack and run targeted verification for each newly observed mechanic that could
affect the answer. Search for credible alternatives and counterevidence rather
than only corroboration. A pack establishes its own behavior, not professional
correctness or a professional claim its author did not make.

Apply these lane rules:

- Online: prefer official documentation, standards, original research, and
  canonical project material; record the verification date.
- Upstream skills: inspect the complete relevant package, revision, worktree
  state, referenced files, helpers, examples, tests, and explicit exclusions.
- Books: distinguish full text or inspected chapters/pages from excerpts,
  summaries, reviews, snippets, abstracts, or metadata.
- Engineering practice: prefer original definitions and empirical or
  authoritative operational guidance; use practitioner accounts as field
  context, not universal proof.

Return:

## Search Log

| Lane / Query | Result | Keep / Reject / Retry | Reason |
| --- | --- | --- | --- |

## Verified Source Registry

| Source | Type | Primary / Secondary | Access Depth | Revision / Date Checked | Authority For | Limitation |
| --- | --- | --- | --- | --- | --- | --- |

For upstream packages, add repository, commit or revision, worktree state, and
the package files inspected. For books, name exact chapters, pages, or excerpts
available.

## Rejected Or Thin Sources

| Source | Rejection / Weakness | Do Not Use For | Reconsider When |
| --- | --- | --- | --- |

## Extraction Queue

| Priority | Source And Exact Locator | Extract For | Compare Against | Avoid Inferring |
| --- | --- | --- | --- | --- |

Choose the smallest set that covers the question without over-weighting one
author, organization, era, or tool. Stop at decision saturation: another
credible source should be unlikely to change the mechanic, conditions,
classification, or answer.

## Source-Search Decision

Choose one:

- `ready-for-extraction`;
- `rerun-search` with the missing lane or query named;
- `revise-scope-or-facets`;
- `blocked` with the access or verification blocker named.
```

Complete when recommended sources are verified and extractable, weak searches
will not be repeated accidentally, and each source has an exact extraction
target.
