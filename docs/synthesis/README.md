# Synthesis

Synthesis docs are the workshop bench between research and final skills.

They can be generous and exploratory. `SKILL.md` files should not be. The job
of synthesis is to turn source pressure into compact behavioral instructions.

Synthesis stays outside `docs/research/` because it is design judgment, not
source discovery. Research asks what sources and language might matter.
Synthesis decides what the skill should become before runtime wording changes.

The drafting loop inside synthesis is:

```text
source pressure
  -> generous synthesis
  -> controlled language pass
  -> behavior audit
  -> blunt gates
  -> validation draft
  -> validation on real tasks
  -> prune
```

## Files

| File Or Folder | Role |
| --- | --- |
| [`methods/`](methods/) | Reusable production flows, synthesis methods, and post-draft passes. |
| [`target-spine.md`](target-spine.md) | Accepted common target spine for future skill behavior. |
| [`language-direction.md`](language-direction.md) | Chosen language direction promoted from upstream vocabulary research. |
| [`skill-context-relationships.md`](skill-context-relationships.md) | Current context pointers, cross-skill relationships, and boundary owners. |
| [`facets/`](facets/) | Skill/facet synthesis timelines from behavior flow through final prune. |
| [`skills/`](skills/) | One synthesis note per high-leverage individual skill. |
| [`families/`](families/) | Synthesis notes for tightly coupled skill families. |

[`methods/source-to-skill-flow.md`](methods/source-to-skill-flow.md) owns the
production workflow from intent through final prune.

## Note Types

Use generous synthesis when source pressure is strong enough to make design
judgments, but the runtime wording is not ready to compress. It may explain,
compare, preserve rejected options, and expose the behavior.

Use compact synthesis when the behavior is chosen. It should identify the
chosen behavior, compressed candidate wording, audit notes, draft placement,
prune notes, and validation tasks.

Some older notes are source-map synthesis: they preserve source pressure and
concept maps for established skills or tightly coupled skill families. Keep
them in synthesis when they contain design judgment about what the skill should
become; move pure source lists or broad search targets back to
`docs/research/`.

## Output

A compact synthesis note should end with:

- the proposed runtime behavior;
- wording candidates small enough to edit into `SKILL.md`;
- what assembled validation draft would let the behavior be tested in context;
- what should stay in research;
- what validation would prove the skill improved.

## Rule

Research can be verbose. Generous and source-map synthesis can explain.
Compact synthesis and final skills should compress hard.
