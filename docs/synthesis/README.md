# Synthesis

Synthesis docs are the decision-and-evidence bench between source discovery
and final skills. They preserve a decision-complete trace: decision-changing
source pressure, current-runtime evidence, ownership collisions, material
alternatives and rejection reasons, selected behavior, extraction placement,
and validation design.

`SKILL.md` files should not be exhaustive. Synthesis retains the evidence and
reasoning needed to produce compact behavioral instructions without forcing
later editors to rediscover why those instructions exist. Preserve provenance,
not every presentation: collapse duplicate prose and superseded
representations, then point to their owning evidence. See [ADR-0007](../adr/0007-synthesis-preserves-exhaustive-research-runtime-skills-compress.md).

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
| [`language-direction.md`](language-direction.md) | Historical upstream-language decision record; active owners are named inside. |
| [`skill-context-relationships.md`](skill-context-relationships.md) | Current context pointers, cross-skill relationships, and boundary owners. |
| [`facets/`](facets/) | Skill/facet synthesis timelines from behavior flow through final prune. |
| [`skills/`](skills/) | One whole-skill synthesis note per skill as coverage expands. |
| [`families/`](families/) | Synthesis notes for tightly coupled skill families. |

[`methods/source-to-skill-flow.md`](methods/source-to-skill-flow.md) owns the
production workflow from intent through final prune.

## Synthesis Ownership

`docs/synthesis/` is the central location for skill-design research and runtime extraction plans. Give every decision one synthesis owner:

| Decision | Owning synthesis |
| --- | --- |
| A skill's outcome, admission, authority, process, state transitions, outputs, completion, and use of another capability | `skills/<consumer-skill>.md` |
| Exact changes to a skill's `SKILL.md`, disclosed references, helpers, templates, validators, tests, evaluations, and installation surfaces | `skills/<file-owner>.md` |
| A provider or setup capability consumed by another skill | The consumer names the required outcome and links to the file owner's synthesis; the file owner specifies the concrete representation and verification |
| One cross-skill invocation or return edge | The participating skill syntheses own their respective boundaries; `skill-context-relationships.md` indexes the accepted edge without copying either process |
| Behavior genuinely shared by a tightly coupled family | `families/<family>.md`, with each member synthesis linking to the shared owner |
| The supported repo-setting schema, choice points, provider mappings, preservation rules, and reconciliation behavior | `skills/repo-bootstrap.md` |
| One target repository's selected literal settings, commands, provider ids, and preserved additions | That target repository's approved setup state; its reusable lessons return to Repo Bootstrap synthesis only when they change the global setup contract |

Use **consumer requirement, owner implementation**. A consumer synthesis may explain why and when it needs a capability, the observable result it requires, and how its own process reacts when that result is absent. It does not prescribe the foreign owner's file rewrite. The owner synthesis records the exact owned-file changes, provider or helper mechanics, compatibility work, validation, migration order, and deliberate non-changes, then links back to the consuming contract.

Cross-document references are contracts, not copies. When two synthesis notes need the same detail, keep the rule with its owner and replace the duplicate with a named requirement plus an anchor. If ownership changes, move the rule and update every pointer in the same revision.

Synthesis is design authority only until implemented. Canonical runtime files remain executable authority; target-repository settings remain instance authority. Repo Bootstrap synthesis owns how those settings are selected, represented, preserved, reconciled, and verified, but not any repository's literal values. Promote a repo-specific lesson only when it changes the reusable setup contract.

## Note Types

Use whole-skill synthesis when source pressure and current-runtime evidence are
strong enough to select a coordinated design. Preserve the orientation,
selected design contract, decision-to-evidence trace, material rejected and
deferred alternatives, runtime ownership map, extraction order, and validation
plan after the behavior is chosen. Collapse any duplicate representation that
adds no distinct decision, ownership, or proof value.

Facet timelines may remain narrower because their earlier and later prompt
artifacts preserve the rest of the trace. Candidate runtime drafts, detailed
skill-context drafts, plain-language candidates, and final-prune plans remain
compact at their owning steps; they do not redefine the whole-skill synthesis
record.

Some older notes are source-map synthesis: they preserve source pressure and
concept maps for established skills or tightly coupled skill families. Keep
them in synthesis when they contain design judgment about what the skill should
become; move pure source lists or broad search targets back to
`docs/research/`.

## Output

A whole-skill synthesis note should contain:

- an orientation and hard ownership boundary;
- one selected design contract for proposed behavior;
- a decision trace connecting evidence, rationale, runtime owner, and proof;
- explicit rejected, deferred, and deliberately unchanged behavior;
- an extraction and affected-surface map;
- a validation plan that distinguishes behavioral from deterministic proof;
- the remaining research and evidence gaps.

## Rule

Research may be exhaustive. Synthesis should be decision-complete, not
transcript-complete; candidate runtime wording and final skills should compress
hard. Prune a synthesis representation when removing it changes no selected
behavior, ownership boundary, material alternative, or proof obligation, and
preserve its provenance through source pointers or explicit historical notes.
