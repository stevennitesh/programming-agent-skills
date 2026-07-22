# Skill Research Organization

This folder holds per-skill facet research. The research is not runtime
instruction by itself. Its job is to turn inspected sources into important
concepts, usable techniques, provenance, limitations, and evidence gaps that
can inform later synthesis.

## Structure

```text
docs/research/skill-facets/
  README.md

  <skill-name>/
    README.md
    SEARCH-VOCABULARY.md
    FACET-1-<NAME>.md
    FACET-2-<NAME>.md
```

## Boundaries

`README.md` in this folder owns the organization rules for all skill research.

`docs/synthesis/methods/source-distillation-flow.md` and its prompts provide an
optional lane when primary or outside sources and deliberate pruning are
needed. The prompts may produce scope, facet-map, search, extraction, and final
source-packet artifacts here.

`<skill-name>/README.md` owns one skill's research map: target skill shape, facet list, status, and links to facet docs.

`<skill-name>/SEARCH-VOCABULARY.md` is optional. Use it only when a skill has enough reusable keyword work to justify a separate file. Otherwise, put search terms in the facet doc.

`<skill-name>/FACET-*.md` owns the actual research packet for one facet:
verified sources, important concepts, usable techniques, provenance, source
limits and disagreements, prune decisions, and gaps.

## Creation Rule

For a new skill, start with:

```text
docs/research/skill-facets/<skill-name>/README.md
docs/research/skill-facets/<skill-name>/FACET-1-<NAME>.md
```

Add `SEARCH-VOCABULARY.md` only after search terms become too large or reusable across facets.

## Runtime Boundary

Research docs stop at evidence. They do not choose runtime behavior or draft
candidate skill wording. Later synthesis decides how, or whether, to use the
distilled concepts and techniques.

Before handing selected research to a whole-skill synthesis:

- carry forward only the concepts, techniques, provenance, limits, and gaps
  that affect the synthesis decision;
- check for duplication with the engineering contract and other skills;
- identify the decisions and evidence the synthesis must resolve.

Deploy Prompts own the later whole-skill deployment route. The durable research
rule is: one optional evidence lane, one skill map, one doc per research
artifact.
