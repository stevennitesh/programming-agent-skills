# Skill Research Organization

This folder holds per-skill facet research. The research is not runtime
instruction by itself. Its job is to turn strong sources into compact
synthesis notes and candidate wording that can later steer Codex toward
upper-bound behavior.

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

`docs/synthesis/methods/source-to-skill-flow.md` and its prompts own the
reusable workflow. Prompts 01-05 produce research maps, source search,
extraction, and triage artifacts here.

`<skill-name>/README.md` owns one skill's research map: target skill shape, facet list, status, and links to facet docs.

`<skill-name>/SEARCH-VOCABULARY.md` is optional. Use it only when a skill has enough reusable keyword work to justify a separate file. Otherwise, put search terms in the facet doc.

`<skill-name>/FACET-*.md` owns the actual research packet for one facet:
sources, ratings, high-signal vocabulary, weak/no-op vocabulary, behavior
gates, good/bad contrast, synthesis promotion notes, prune notes, and gaps.

## Creation Rule

For a new skill, start with:

```text
docs/research/skill-facets/<skill-name>/README.md
docs/research/skill-facets/<skill-name>/FACET-1-<NAME>.md
```

Add `SEARCH-VOCABULARY.md` only after search terms become too large or reusable across facets.

## Runtime Boundary

Research docs can contain candidate wording, but they do not choose runtime
behavior. Promote selected wording into `docs/synthesis/` before editing the
runtime skill.

Before editing `skills/custom/<skill-name>/SKILL.md`:

- compress the facet packet into a synthesis note with the smallest
  behavior-changing wording;
- identify what stays research-only;
- check for duplication with the engineering contract and other skills;
- get explicit approval when the work so far has been research-only.

The durable rule is: one production workflow, one skill map, one doc per
research artifact.
