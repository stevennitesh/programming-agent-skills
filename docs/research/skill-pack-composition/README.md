# Skill-Pack Composition Research

This lane owns reusable pack-composition evidence. Research Cards live under
`docs/research/skill-pack-composition/cards`; tracked public source packets
live under `docs/research/skill-pack-composition/sources`.

The ignored private source stack remains `sources/` at the repository root.
Public routers and indexes describe that boundary but never enumerate its
contents. Evidence recorded here cannot select the pack, admit H1, recommend
adoption, or record validation results.

## Research Card contract

Canonical Cards are Markdown files named `cards/RC-NNNN.md`. Their YAML
frontmatter carries schema version 1 and the complete evidence record; the
Markdown body may explain the record for people but is not a second machine
authority. `scripts.research_catalog` validates exact fingerprints, stable
claim/source links, lifecycle, labels, typed relations, applicability,
freshness inputs, retrieval dimensions, unknowns, and limits.

Preferred, alternative, and hidden labels are disjoint. Alias collision
returns explicit candidate IDs and scope notes; it never chooses equivalence.
Only `broader`, `narrower`, `related`, `exact-match`, `close-match`,
`conflicts-with`, `revision-of`, and `supersedes` are valid relations.

The thin derived index is
`docs/research/skill-pack-composition/catalog.json`. Regenerate it from Cards;
never hand-author entries:

```text
python -m scripts.research_catalog build --generated-at <ISO-8601>
python -m scripts.research_catalog validate
```

The index contains identities, paths, fingerprints, labels, dimensions,
method-evidence and freshness classes, relations, and integrity results. It
contains no claim narrative, citation copy, adoption, H1, recommendation,
validation result, popularity, confidence, or ranking.

## Admission and finite retrieval

The controller records a fingerprinted M0-derived independent packet before it
can open the catalog. Early or mismatched access returns
`catalog-not-admitted`; historical Card, synthesis, or incumbent fields return
`historical-seed-rejected`.

Each query supplies exactly one problem or recruited behavior, conditions and
exclusions, evidence/freshness filters, the exact fingerprint derived from its
conditions, exclusions, role, and lifecycle stage, current source fixed-point
observations, and an explicit positive maximum of canonical Card families. A
Card is fresh for that application only when both application and all source
identities match and no recorded refresh trigger fires; the application-free
index therefore records freshness as `unknown`. Problem dimensions are
matched before aliases or known methods. Exact, close, and related groups are
stable-ID ordered. An over-bound result returns `catalog-overflow`, the
eligible count, and narrowing dimensions with zero loaded Cards—never a ranked
or truncated subset.

Each session carries the complete validated independent packet and a chained
receipt for every legal transition, so constructed phase/counter dictionaries
fail closed. One session permits one reconciliation pass and at most one
named-gap pass for an unresolved gap already named in that packet and whose
resolution could materially change H1. A second pass or work after completion
fails closed. Query-session dispositions remain reconciliation
facts; per-skill synthesis alone decides applicability and H1.

The caller-facing pure sequence is
`record_independent_packet` → `open_catalog` → `query_catalog` →
`complete_session`. The caller retains each returned session value; the
controller writes no semantic state and performs no research-tree scan.
