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

Start manually with Deploy Prompt 1, or use `Run Deploy Campaign on <skill>`
for one initiating prompt that runs a fresh Prompts 1-4, Pruning Pass, and
Prompt 5 campaign epoch, including no-op pruning, promotion, and
installation-parity verification when no changes are justified. Prior campaign
artifacts may supply exact reusable evidence but cannot skip a unit. Every path
begins with Prompt 1:

```text
Run Deploy Campaign on <skill> (optional controller)
  -> local intent authorities + upstream/research candidates
  -> Deploy Prompt 1 blind intent and evidence pass
       |-> fuzzy intended contract: one behavior-decision interlude
       |-> source gap: one Research interlude
       |-> agent-owned design gap: one Prototype interlude
       `-> current reconciliation and Prompt 2
  -> Deploy Prompt 2 in-place synthesis reconciliation
  -> Deploy Prompt 3 executable B0 control and exact C1 candidate
  -> Deploy Prompt 4 B0 viability, C1 contribution, and preservation proof
  -> Deploy Pruning Pass behavior-preserving runtime minimization
  -> Deploy Prompt 5 canonical promotion, proof, and separately owned install
  -> optional Deploy Prompt 6 Git delivery
```

The campaign root retains state transitions, verification, and user
interaction. It dispatches one fresh-context unit owner at a time and
serializes writers. Prompt 1 and Research may use read-only source
grandchildren; Prompt 4 and the Pruning Pass may use fresh evaluation
grandchildren. The unit owner keeps synthesis and judgment. Exact proof is
reused only when bytes, task, protocol, configuration, tools, authority,
evidence, runtime, rubric, and proof lane match. The Pruning Pass always audits
the accepted runtime, but creates an equivalence arm only for material cuts.
Bare campaign invocation excludes Git delivery; append `and commit` or
`and push` to authorize Prompt 6.

`B0` is a new runnable minimum rewrite: the intersection of the local intended
contract—outcome, invocation, authority, Return, completion, relationships,
exclusions, and safety boundaries—and the strongest applicable source meaning,
mechanics, conditions, and vocabulary. Add only the cheapest independently
required local compatibility. Never define B0 as current-minus-cuts or preserve
a clause because it is already canonical. Prompt 1 freezes B0 semantic behavior
units and source identities before opening current runtime or synthesis.
Unchanged re-entry verifies that checkpoint and revisits only affected units.

Outside research should prefer relevant sources with documented professional
acclaim, strong ratings or durable popularity, broad adoption, and explicit
upper-bound engineering discipline. Those signals order discovery; they do not
prove correctness, local fit, or behavioral effect. Source conditions,
counterpressure, disagreement, and limitations remain part of the evidence.

Before C1 comparison, B0 must pass its minimum-runtime controls. Compare every
source-derived steering unit without exact behavioral evidence against `D0`
no-guidance, reusing the B0 viability arm. Independently required contracts use
owner-matched proof unless efficacy is claimed. A nonviable B0 is a baseline
defect, not useful red evidence.

`C1` is exact `B0` plus admitted behavior hypotheses discovered from current
runtime (`current-retention`), a concrete caller/callee gap
(`pack-composition`), credible evidence beyond minimum viability
(`source-mechanism`), or a counterexample to the settled intent
(`intent-counterexample`). Origin invites inspection but does not prove
adoption. A counterexample that disproves minimum viability reopens B0; C1
receives no credit for repairing it. Every hypothesis needs an owner, expected
B0 failure, cheapest expression, wrong-condition case, and proof. Cuts relative
to current receive no mechanism-contribution credit.

A C1 no-control-failure or regression rejects only that hypothesis. Prompt 4
removes it, rederives C1 as B0 plus surviving units, and continues with viable
B0; if no C1 units survive, C1 = B0 before the Pruning Pass.

The current/B0/C1 identity determines the campaign:

| Shape | Identity | Route |
| --- | --- | --- |
| `runtime-no-change` | current = B0 = C1 | A standalone run may stop after Prompt 2 when B0 proof is exact. A Deploy Campaign still runs Prompts 3 and 4, the Pruning Pass, and Prompt 5 without claiming a runtime delta. |
| `pruning-only` | current != B0 = C1 | Prove B0 viability and protected behavior, then run the Pruning Pass before promotion. |
| `behavioral-candidate` | B0 != C1 | Prove each admitted hypothesis against B0, then run the Pruning Pass before promotion. |

Prompt 1 confirms its packet through an internal integrity gate. It asks the
user only when a material user-owned design choice remains, not to approve a
fully determined audit packet. Prior evidence is classified as
`exact-reusable`, `lane-limited`, `historical-admission-only`, `invalidated`,
or `missing` before it can affect a new campaign. Source and interlude re-entry
reuse exact checkpoint identities instead of repeating unchanged reads.

A Conditional Behavior Decision Interlude uses `$grill-with-docs` for one
bounded intended-contract decision: either a fuzzy minimum-viability axis or a
C1 hypothesis that would change outcome, invocation, authority, Return,
completion, exclusion, or relationships. It never chooses agent technique or
proves efficacy.

A Conditional Research Interlude resolves one admitted source question. A
Conditional Prototype Interlude resolves one agent-owned technical design
question with a disposable runnable probe. Research can establish meaning and
Prototype can select a construction; neither proves skill-steering effect.

`plan-only` work ends after Prompt 2 with decision-complete synthesis; it does
not mutate runtime files. A new unscaffolded skill uses the bundled
`skill-creator` only for structure and metadata when Prompt 3 requires it.
Writing Great Skills owns semantic quality and stops after canonical proof;
installation and delivery retain their separate owners. Every leaf prompt
executes exactly one unit, recommends at most one successor, and stops. Only
the active campaign coordinator may dispatch the verified successor.

Proof is proportional to the unit: early read-only and documentation prompts
use inspection and affected checks; exact behavior proof belongs to Prompt 4;
cut equivalence belongs to the Pruning Pass and runs only for material cuts;
one final integration suite, install dry-run, synchronization, and parity
belong to Prompt 5. Prompts 1 through 5 and the Pruning Pass never stage or
commit and must preserve their starting Git HEAD. Prompt 6 alone owns
intentional Git delivery.

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
- a verified source-derived minimum comparison and executable `B0` definition;
- one ledger row per semantic behavior unit, with source or owner provenance
  and a runtime-clause map;
- the current/B0/C1 campaign shape;
- dispositions for current behavior and applicable research, including the
  independently supported protected behavior set, all four C1 hypothesis
  origins, and original research claim labels;
- dispositions for prior evidence and the exact proof lane in which any result
  remains reusable;
- admitted `C1` deltas with basis, owner, cheapest expression, destination,
  entry condition, failure Return, and proof;
- a decision trace connecting evidence, rationale, runtime owner, and proof;
- explicit rejected, deferred, and deliberately unchanged behavior;
- an extraction and affected-surface map;
- a claim-to-proof matrix separating B0 fidelity, conditional D0 comparison,
  B0 viability, C1 contribution, invocation, protection, deterministic proof,
  and the separate pre-prune/final-C1 equivalence lane;
- the remaining research and evidence gaps.

## Rule

Research may be exhaustive. Synthesis should be decision-complete, not
transcript-complete; candidate runtime wording and final skills should compress
hard. Prune a synthesis representation when removing it changes no selected
behavior, ownership boundary, material alternative, or proof obligation, and
preserve its provenance through source pointers or explicit historical notes.
After promotion, reconcile the active synthesis to the canonical result and
remove superseded future-tense construction detail and raw campaign chronology.
Keep exact outputs, per-sample history, and run chronology in validation.
