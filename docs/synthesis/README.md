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

The optional outside-source evidence loop is:

```text
source question
  -> optional facet map
  -> search and verify
  -> extract concepts and techniques
  -> distill source packet
```

## Files

| File Or Folder | Role |
| --- | --- |
| [`methods/`](methods/) | Reusable deployment and optional source-distillation methods. |
| [`skill-context-relationships.md`](skill-context-relationships.md) | Current context pointers, cross-skill relationships, and boundary owners. |
| [`skills/`](skills/) | One whole-skill synthesis note per skill as coverage expands. |

[`methods/deploy-prompts.md`](methods/deploy-prompts.md) owns the default
one-skill workflow from minimum-runtime comparison and research intake through
synthesis, candidate evaluation, promotion, installation, and optional Git
delivery. The source-distillation method is a conditional evidence lane for a
decision-changing source gap, not a required campaign before every skill.

## Synthesis Ownership

`docs/synthesis/` is the central location for skill-design research and runtime extraction plans. Give every decision one synthesis owner:

| Decision | Owning synthesis |
| --- | --- |
| A skill's outcome, admission, authority, process, state transitions, outputs, completion, and use of another capability | `skills/<consumer-skill>.md` |
| Exact changes to a skill's `SKILL.md`, disclosed references, helpers, templates, validators, tests, evaluations, and installation surfaces | `skills/<file-owner>.md` |
| A provider or setup capability consumed by another skill | The consumer names the required outcome and links to the file owner's synthesis; the file owner specifies the concrete representation and verification |
| One cross-skill invocation or return edge | The participating skill syntheses own their respective boundaries; `skill-context-relationships.md` indexes the accepted edge without copying either process |
| The supported repo-setting schema, choice points, provider mappings, preservation rules, and reconciliation behavior | `skills/repo-bootstrap.md` |
| One target repository's selected literal settings, commands, provider ids, and preserved additions | That target repository's approved setup state; its reusable lessons return to Repo Bootstrap synthesis only when they change the global setup contract |

Use **consumer requirement, owner implementation**. A consumer synthesis may explain why and when it needs a capability, the observable result it requires, and how its own process reacts when that result is absent. It does not prescribe the foreign owner's file rewrite. The owner synthesis records the exact owned-file changes, provider or helper mechanics, compatibility work, validation, migration order, and deliberate non-changes, then links back to the consuming contract.

Cross-document references are contracts, not copies. When two synthesis notes need the same detail, keep the rule with its owner and replace the duplicate with a named requirement plus an anchor. If ownership changes, move the rule and update every pointer in the same revision.

Synthesis is design authority only until implemented. Canonical runtime files remain executable authority; target-repository settings remain instance authority. Repo Bootstrap synthesis owns how those settings are selected, represented, preserved, reconciled, and verified, but not any repository's literal values. Promote a repo-specific lesson only when it changes the reusable setup contract.

## Canonical Extraction

Start every selected skill with Deploy Prompt 1. It compares current runtime,
matching upstreams, existing synthesis, and applicable research before routing
the earliest justified unit:

```text
current skill state + upstream minimum candidates + research intake
  -> Deploy Prompt 1 minimum-runtime decision
       |-> if admitted: one source-distillation interlude, then Prompt 1 again
       `-> no-change, evidence-gap, or the earliest justified later prompt
  -> Deploy Prompt 2 in-place synthesis reconciliation
  -> Deploy Prompt 3 executable B0 control and exact C1 candidate
  -> Deploy Prompt 4 minimality, contribution, preservation, and pruning proof
  -> Deploy Prompt 5 canonical promotion, proof, and separately owned install
  -> optional Deploy Prompt 6 Git delivery
```

`B0` is the runnable locally compatible minimum: the simplest credible
baseline core plus mandatory local contracts and source-correct semantic
substitutions that make no behavioral-improvement claim. `C1` is exact `B0`
plus admitted behavior-changing mechanisms. The current runtime supplies a
protected behavior set, not a presumption that every existing mechanism stays.

`plan-only` work ends after Prompt 2 with decision-complete synthesis; it does
not mutate runtime files. Conditional source distillation returns provenance,
limitations, and a bounded source decision to Prompt 1; it does not design or
evaluate behavior. A new unscaffolded skill uses the bundled `skill-creator`
only for structure and metadata when Prompt 3 requires it. Writing Great
Skills owns semantic quality and stops after canonical proof; installation and
delivery retain their separate owners. Every prompt executes exactly one unit,
recommends at most one successor, and stops without starting it.

The synthesis note supplies selected behavior, placement, preservation, and
proof obligations; it never becomes executable authority itself.

## Note Types

Use whole-skill synthesis when source pressure and current-runtime evidence are
strong enough to select a coordinated design. Preserve the orientation,
viability floor, baseline comparison, current-behavior and research
dispositions, selected `B0` and `C1` contract, decision-to-evidence trace,
material rejected and deferred alternatives, runtime ownership map, and
claim-to-proof design. Collapse any duplicate representation that adds no
distinct decision, ownership, or proof value.

Existing synthesis notes are reconciled in place only when their skill enters
the workflow. Do not mass-rewrite them or fabricate a historical baseline,
minimality comparison, or behavioral control for a campaign that did not
create one. Preserve that absence as an evidence gap.

Some older notes are source-map synthesis: they preserve source pressure and
concept maps for established skills or tightly coupled skill families. Keep
them in synthesis when they contain design judgment about what the skill should
become; move pure source lists or broad search targets back to
`docs/research/`.

## Output

A whole-skill synthesis note should contain:

- an orientation, viability floor, and hard ownership boundary;
- a verified simplest-baseline comparison and executable `B0` definition;
- dispositions for current behavior and applicable research, including the
  protected behavior set and original research claim labels;
- admitted `C1` deltas with basis, owner, cheapest expression, destination,
  entry condition, failure Return, and proof;
- a decision trace connecting evidence, rationale, runtime owner, and proof;
- explicit rejected, deferred, and deliberately unchanged behavior;
- an extraction and affected-surface map;
- a claim-to-proof matrix that separates semantic fidelity, mechanism
  contribution, invocation and context loading, current-contract preservation,
  pruning equivalence, and deterministic proof;
- the remaining research and evidence gaps.

## Rule

Research may be exhaustive. Synthesis should be decision-complete, not
transcript-complete; candidate runtime wording and final skills should compress
hard. Prune a synthesis representation when removing it changes no selected
behavior, ownership boundary, material alternative, or proof obligation, and
preserve its provenance through source pointers or explicit historical notes.
