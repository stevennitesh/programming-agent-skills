# Skill Synthesis And Deployment Prompts

Use these prompts to reconcile, create, or improve one skill at a time. Invoke
Deploy Prompt 1 for a standalone unit or Deploy Campaign for verified
start-to-finish orchestration. Every new Deploy Campaign runs a fresh Prompt 1,
Research Pass, Prompts 2 through 4, Pruning Pass, and Prompt 5 epoch even when
the skill completed an earlier campaign.

Invoke with, for example:

```text
Run Deploy Prompt 1 for diagnosing-bugs.
Run Deploy Campaign on diagnosing-bugs.
```

For a standalone or delegated unit, load `Shared Model`, `Shared Run Contract`,
`Proportionate Proof Budget`, and that unit only. A campaign coordinator loads
those shared sections plus `Deploy Campaign`; it opens another unit only to
dispatch or verify it.

The ordinary sequence is:

```text
Deploy Prompt 1: freeze the intent-derived M0 specification
  -> when admitted: one Conditional Behavior Decision Interlude
  -> Deploy Research Pass: investigate the same intended behavior
  -> Deploy Prompt 2: reconcile evidence, current behavior, and H1 design
       |-> when admitted: one Conditional Prototype Interlude
       `-> when admitted: one Conditional Behavior Decision Interlude
  -> Deploy Prompt 3: materialize exact M0 and H1
  -> Deploy Prompt 4: prove M0 viability and H1 contribution; freeze V1
  -> Deploy Pruning Pass: prove a cheaper P1 without V1 regression
  -> Deploy Prompt 5: promote and install P1
  -> optional Deploy Prompt 6: Git delivery
```

Prior artifacts and proof are evidence, not lifecycle completion. They may
reduce repeated legwork but never skip a numbered prompt, the Research Pass, or
the Pruning Pass in a fresh campaign. Historical B0/C1 records retain their
original meaning; current campaigns use M0/H1/V1/P1.

## Shared Model

Keep these authorities separate:

| Input | Authority | Not Authority For |
| --- | --- | --- |
| Local intent authorities | The user, caller contracts, domain decisions, relationship owners, required compatibility, and safety boundaries settle outcome, invocation, authority, Return, completion, exclusions, and relationships | Professional technique or behavioral effectiveness |
| Independent professional evidence | Applicable methods, vocabulary, conditions, alternatives, counterpressure, and limits | Local intent, exact runtime wording, or behavioral effectiveness |
| Upstream packages | What the inspected package instructs, names, tests, or implements at one revision | A professional claim the author did not make, professional correctness, local fit, or efficacy |
| Current canonical runtime | Existing behavior, compatibility, composition, and prior evidence inspected after M0 freezes | M0 by existence, automatic protection, or professional validity |
| Candidate-owned proof | Viability, contribution, preservation, pruning, invocation, and completion for exact bytes and fixed conditions | Untested models, hosts, tasks, configurations, or broader professional validity |

For independent research, prefer governing standards, primary sources,
respected books, original research, official documentation, and credible
practitioner evidence. Acclaim, ratings, popularity, and adoption order
discovery; they do not prove correctness or local fit. Preserve source meaning,
conditions, counterevidence, disagreement, applicability, and limitations.
Never simulate a practitioner conversation or attribute a professional claim
to an upstream author unless the inspected source makes it.

Use these artifacts:

- **Viability floor:** the minimum intended contract: outcome, invocation and
  exclusions, authority, caller and relationship obligations, safe failure
  Return, completion, irreversible order, required compatibility, and safety.
- **Semantic behavior unit:** the smallest independently owned observable
  trigger, action, judgment, branch, gate, Return, or completion condition with
  one proof obligation.
- **M0 checkpoint:** a pre-research, behavior-complete specification of the
  minimum viable runtime, its semantic units, neutral cheapest expressions,
  clause map, viability suite, local authorities, limitations, and fingerprint.
- **`M0` minimum viable runtime:** the exact runtime later materialized only
  from the M0 checkpoint. M0 is behavior-minimal: every behavior maps to the
  viability floor or a required local contract. It is not claimed to be
  wording-minimal.
- **Research packet:** the decision-ready evidence for the same intended
  behavior, produced after M0 freezes. It separates independent discovery,
  upstream and current observations, targeted verification, alternatives,
  conditions, counterpressure, and gaps.
- **Intent-adjacent steering hypothesis:** vocabulary or a method that preserves
  the intended contract while recruiting a stronger action, judgment, gate,
  sequence, or completion behavior for the same problem. Map it as
  `term -> recruited behavior -> expected M0 weakness -> observable gate ->
  comparative proof`.
- **`H1` hypothesis runtime:** exact M0 transformed only by admitted additions
  or substitutions from research, current behavior, pack composition, or an
  intent-adjacent opportunity. H1 remains provisional.
- **`V1` verified runtime:** exact Prompt 4 result containing M0 plus only H1
  behavior that demonstrated defect correction or a meaningful quality lift
  without protected-behavior regression.
- **`P1` pruned final runtime:** exact V1 or a cheaper expression proved
  non-regressing against V1. P1 is the only promotion candidate.
- **Protected behavior set:** M0 behavior plus accepted H1 behavior,
  independently required contracts, and non-intuitive safety or authority
  boundaries. Current presence alone creates no protection.

M0 is minimal by behavioral scope. P1 is minimal by proved wording and package
load. Research may admit a hypothesis but never proves that exact skill wording
changes behavior.

Classify independent method support separately from source claim labels:

| Method Evidence | Meaning |
| --- | --- |
| `independently-supported` | Applicable independent evidence supports the method under recorded conditions |
| `contested` | Applicable credible evidence materially disagrees |
| `pack-specific` | The behavior is observed in a pack but lacks broader independent support |
| `unverified` | Access, freshness, applicability, or evidence is insufficient |

Pack-specific or unverified behavior may be a clearly labeled local experiment
when no decisive contradiction exists. It cannot inherit professional or
upper-bound authority.

Record the pre-evaluation identity relationship:

| Campaign Shape | Exact Identity | Meaning |
| --- | --- | --- |
| `runtime-no-change` | current = M0 = H1 | Current already matches the proposed minimum and no hypothesis changes bytes; proof may still be missing |
| `minimum-candidate` | current != M0 = H1 | The intent-derived minimum differs from current but no beyond-minimum hypothesis is admitted |
| `hypothesis-candidate` | M0 != H1 | At least one admitted addition or substitution needs M0-first contribution proof |

Classify prior evidence before reuse:

| Evidence Disposition | Meaning |
| --- | --- |
| `exact-reusable` | Bytes, claim, task, protocol, model, host, configuration, tools, authority, evidence, runtime, rubric, and proof lane match |
| `lane-limited` | Exact for one named lane only |
| `historical-admission-only` | Useful for discovery or admission, not current control or candidate proof |
| `invalidated` | A behaviorally relevant identity changed |
| `missing` | Required evidence does not exist |

## Shared Run Contract

A unit invocation performs exactly one numbered prompt, the Research Pass, the
Pruning Pass, or one Conditional Interlude. It never starts or partially
executes its successor. Under an active Deploy Campaign, only the coordinator
dispatches a verified successor.

Prompts 1 through 5, the Research Pass, the Pruning Pass, and both Conditional
Interludes record Git `HEAD` before work and read it back before Return. They
never stage or commit. If `HEAD` changes, return `blocked` with the observed
transition. Prompt 6 is the sole Git-delivery owner. Preserve unrelated work
and every unit's mutation boundary.

End every run with:

```text
Authorized unit completed:
Decision:
Campaign shape:
Runtime identities:
Artifacts changed:
Evidence used or reused:
Residual gaps:
Recommended next unit:
Git HEAD: <start> -> <end>
Git delivery: not-applicable | pending | committed | pushed
Exact stop reason:
```

Use `none` when no successor is justified. A recommendation never authorizes a
leaf owner to start its successor. `Git delivery: pending` records uncommitted
authorized artifacts.

## Proportionate Proof Budget

Run the cheapest proof that establishes the current unit.

**Affected Markdown gate:** whenever Prompt 2, 5, or 6 changes Markdown, verify
every affected file's local links, internal anchors, balanced code fences, and
consistent table columns.

| Unit | Default Proof |
| --- | --- |
| Prompt 1 | Complete intent-source read-back, M0 checkpoint integrity, and existing local evidence inspection; no full suite |
| Research Pass | Citation and source-identity verification, independent-search and counterpressure coverage, packet read-back, and tracked-mutation boundary |
| Prompt 2 | Complete synthesis read-back, affected Markdown gate, directly affected documentation checks, and both diff checks |
| Prompt 3 | Exact M0/H1 inventories and hashes, focused structural and relationship checks, skill validation, and both diff checks |
| Prompt 4 | M0 viability first, then only registered H1 contribution arms; affected focused checks and one full suite only after final behavior-complete bytes when repository contracts changed |
| Pruning Pass | Complete cut audit; for material cuts reuse V1 controls and run only affected P1 equivalence, invocation, and context arms |
| Prompt 5 | Canonical and synthesis read-back, affected Markdown gate, affected focused proof, one full integration suite, install dry-run, synchronization, parity, and clean post-install dry-run |
| Prompt 6 | Scoped final diff, affected Markdown gate, required current checks, both diff checks, intentional staging, commit, and explicitly authorized push |

Behavioral claims follow `writing-great-skills/BEHAVIOR-EVALS.md`. Run at least
five fresh M0 samples for a causally coherent hypothesis cluster. Run H1 only
when the pre-registered defect or quality deficit appears. Extend sampling only
for material variance, borderline effect, or protocol deviation; stop early
for a critical regression. Structural and owner-matched claims do not require
behavioral samples.

## Deploy Campaign: Orchestrate One Skill

Runs one skill's bounded units under continuing user authorization.

```text
Coordinate only one Deploy Campaign for the named skill. `Run Deploy Campaign
on <skill>` authorizes bounded fresh-context delegation and one fresh epoch:
Prompt 1, Research Pass, Prompts 2 through 4, Pruning Pass, and Prompt 5,
including canonical promotion and managed installation but not Git delivery.

Parse optional delivery wording once:

- bare invocation: complete Prompt 5 and stop with Git delivery pending when
  bounded artifacts remain;
- `and commit`: also authorize Prompt 6 to commit without push; or
- `and push`: also authorize Prompt 6 to commit and push.

The root owns transitions, user interaction, verification, and the terminal
decision. Track only skill, delivery mode, starting HEAD/worktree, campaign
epoch, current unit, M0 and research checkpoints, runtime identities, pending
decision, and stop reason. Do not create a controller ledger.

Dispatch one unit at a time. Start one direct child with `fork_turns="none"`
and a self-contained brief containing repository, skill, delivery mode, method
path and unit, input and artifact pointers, allowed mutation paths, starting
state, proof budget, and Return contract. It loads the shared sections plus its
unit, executes only that unit, and stops. Serialize all writers.

Nested delegation is evidence-only:

- Prompt 1 and Research owners may use bounded fresh-context grandchildren for
  independent read-only source lanes.
- Prompt 4 and the Pruning Pass may use fresh-context evaluation grandchildren
  in capacity-aware waves under `BEHAVIOR-EVALS.md`; the unit owner fixes the
  task, runtime, rubric, and identities, inspects every output, and judges.
- Other grandchildren require a concrete independent read-only check.

Give grandchildren factual briefs without parent conclusions or peer outputs.
Source and check grandchildren are filesystem-read-only; evaluation
grandchildren may write only assigned isolated or disposable outputs. None
edits shared sources, decides adoption, interacts with the user, or spawns.

After every unit, verify its allowed status, Return, current HEAD/worktree,
changed artifacts, hashes, and proof by read-back. A summary alone is not
evidence. Reject unauthorized scope, malformed packets, or unexplained drift.

Prior campaign artifacts never satisfy the current epoch's unit completion.
Reuse exact prior proof only when the complete identity tuple matches. Recheck
identity and judgment; rerun only missing, drifted, contaminated, newly
claimed, or explicitly fresh evidence.

Advance only through these transitions:

- Start with Prompt 1.
- Prompt 1 `ready-for-research` dispatches the Research Pass.
- Research `research-complete` dispatches Prompt 2.
- Research `intent-reopen` dispatches a fresh Prompt 1 with only the new
  authoritative evidence added to its blind input.
- Prompt 2 `ready-for-prompt-3` dispatches Prompt 3; Prompt 3
  `ready-for-prompt-4` dispatches Prompt 4.
- `prototype-gap` dispatches the exact Prototype Interlude; a closing verdict
  returns only to Prompt 2.
- `behavior-decision-gap` stays root-held. Run the exact `$grill-with-docs`
  Interlude one material question at a time. A minimum-contract decision
  returns to Prompt 1; an H1-only decision returns to Prompt 2.
- Prompt 4 `accepted` dispatches the Pruning Pass. The pass `complete`
  dispatches Prompt 5 with exact P1. Prompt 5 `complete` is successful.
- A missing M0 defect or quality deficit rejects only the affected H1 unit.
  A viable M0 keeps Prompt 4 running; if none survive, V1 = M0.
- `evidence-gap`, `blocked`, or `needs-more-evidence` is terminal. Inconclusive
  removal risk preserves the current active runtime.
- Before successful terminal Return, dispatch Prompt 6 only when initial
  delivery wording authorized it and bounded artifacts remain pending.

Every fresh campaign runs every ordinary unit once. Repeat a unit only after an
explicit Interlude return or a changed identity that its transition contract
names. Do not ask the user to authorize ordinary transitions. Ask only for an
admitted intended-contract decision, an exact human verdict, or new external
authority.

At terminal Return, report:

Campaign:
Skill:
Terminal decision:
Units completed:
M0, H1, V1, P1, canonical, and installed identities:
Evidence:
Residual gaps:
Git HEAD: <campaign start> -> <campaign end>
Git delivery: pending | committed | pushed | not-applicable
Worktree:
Exact stop reason:

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 1: Freeze M0

Universal read-only intent entry.

```text
Perform only Deploy Prompt 1 for the named skill. Never inspect research,
upstream packages, or the target's current skill body, and never start a
successor.

Use $writing-great-skills in Audit mode.

Read local intent authorities: the user, domain decisions, relationship
owners, caller contracts, required compatibility, and safety contracts. Read a
complete caller package when it can alter the target contract. Do not open the
target synthesis conclusions, historical evaluations, experimental candidates,
promotion records, upstream skills, outside research, or current skill body.

Settle the viability floor: outcome, invocation and exclusions, authority,
caller and relationship obligations, safe failure Return, completion,
irreversible order, compatibility, and safety. If one axis is materially
fuzzy, return `behavior-decision-gap` with one Conditional Behavior Decision
Interlude admission. Ask no agent-owned technique question.

Specify M0 from that settled floor. Include one semantic behavior unit per
independently owned trigger, action, judgment, branch, gate, Return, or
completion condition. Every unit names its local authority, cheapest neutral
expression, entry and wrong-condition cases, failure Return, and proof. Use
locally owned vocabulary when required; do not import source-derived methods or
leading terms.

M0 is behavior-minimal, not word-count-minimal. Apply a clause-to-intent cut
audit: remove any behavior that maps to neither the viability floor nor a
required local contract. Define the complete M0 viability suite separately
from any later improvement claim.

Freeze one M0 checkpoint containing the intended contract, unit ledger,
runtime-clause specification, viability suite, local source identities and
hashes, limitations, research questions grouped by intended behavior, one
authorized research-note path, and a content fingerprint.

Re-entry verifies the checkpoint's HEAD, local authorities, identities, and
fingerprint. Revisit only the exact decision delta; unexpected drift requires
a fresh blind pass.

Under a Deploy Campaign, successful completion returns only
`ready-for-research`. A standalone run may also return `ready-for-research`;
later artifacts cannot waive this checkpoint. Return the intended contract,
M0 checkpoint, proof outline, research clusters, gaps, and exactly one of
`ready-for-research`, `behavior-decision-gap`, `evidence-gap`, or `blocked`.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Research Pass: Investigate The Intended Behavior

Mandatory read-only evidence and discovery unit after M0 freezes. It may write
only the Prompt 1-authorized research note.

```text
Perform only the Deploy Research Pass for the named skill and exact M0
checkpoint. Never alter M0, synthesis, runtime, relationships, evaluation,
installation, or Git state, and never start a successor.

Use $research for the bounded question: which methods, vocabulary, conditions,
and alternatives best support this skill's settled intended behavior? Apply
`docs/synthesis/methods/source-distillation-flow.md` when concept or technique
distillation is needed. Keep one authorized note; use facets or bounded
read-only source grandchildren for genuinely independent clusters.

First perform independent online discovery from the intended behavior without
opening upstream skill packages, the current target skill body, its synthesis,
or historical candidate conclusions. Search for the strongest applicable
method, credible alternatives, falsifying evidence, conditions, failure modes,
and professional counterpressure.

Only after recording that blind search, inspect:

- Matt Pocock under `.tmp/mattpocock-skills`;
- Superpowers under `.tmp/superpowers`;
- Ponytail under `.tmp/ponytail`;
- the complete current canonical target package; and
- applicable local language packets as historical source intake.

For every upstream, record revision, worktree state, access depth, files
inspected, and limits. Attribute only observed behavior to the pack. Then run
targeted independent online verification for any newly observed mechanic that
could affect H1. Search alternatives and counterevidence, not merely
corroboration. Upstream repetition proves shared pack usage only.

For practitioner evidence, prefer identifiable inspected material. Use an
actual practitioner conversation only when published evidence leaves one
material operational condition unresolved; record speaker authority, context,
date, and limits. Never fabricate or generalize a conversation.

Classify source claims with their original labels and each proposed method as
`independently-supported`, `contested`, `pack-specific`, or `unverified`.
Record applicability, freshness, alternative methods, rejected lanes, and the
consequence for H1. Pack-specific or unverified behavior may be proposed only
as a clearly labeled local experiment when no decisive contradiction exists.

Use decision saturation, not a source quota. Stop when every load-bearing
claim is classified, the strongest applicable owners and counterposition were
inspected or their access failure recorded, and another credible source is
unlikely to change the method, conditions, classification, or hypothesis.
Reuse an existing packet only when claim, conditions, source identity,
freshness, and intended application match; still verify applicability.

If evidence shows M0 omitted behavior essential to its settled intent, do not
repair it here. Return `intent-reopen` with the exact affected unit, evidence,
and consequence. Otherwise return one research packet containing independent
discovery, pack and current observations, targeted verification, method
classifications, intent-adjacent candidates, conflicts, gaps, and stopping
basis.

Return exactly `research-complete`, `intent-reopen`, `evidence-gap`, or
`blocked`. `research-complete` recommends Prompt 2; `intent-reopen` recommends
Prompt 1. An ordinary unverified idea is a disclosed disposition, not
automatically an evidence gap.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
M0 checkpoint: CHANGE_ME
```

## Conditional Prototype Interlude

Run only when Prompt 2 returns `prototype-gap`.

```text
Perform only the Conditional Prototype Interlude for the named skill and exact
Prompt 2 admission packet. Never alter M0, edit synthesis or runtime, evaluate
skill wording, or start a successor.

Use $prototype for one frozen agent-owned technical choice blocking executable
H1. Prompt 2 owns the decision and result. Keep intended contract, M0,
research conditions, representative cases, verdict basis, and disposable
boundary fixed. Build only the smallest runnable probe that distinguishes the
candidate mechanics. Production correctness and behavioral steering remain
untested.

Return the intact Prototype result plus exactly `prototype-complete`,
`awaiting-human-verdict`, `evidence-gap`, or `blocked`. Recommend Prompt 2 only
when the result can close the admitted choice.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Prototype admission: CHANGE_ME
```

## Conditional Behavior Decision Interlude

Run only for one admitted M0 or H1 contract decision.

```text
Perform only the Conditional Behavior Decision Interlude for the named skill
and exact admission packet. Never edit synthesis or runtime, run behavioral
evaluation, or start a successor.

Use $grill-with-docs for exactly one bounded intended-contract decision. Before
questioning, state context action `render only`, ADR action `offer only`, the
possibility that a domain collision may reopen or block the decision, and that
confirmation starts no downstream work. Ask one material question at a time
with one recommendation and decisive tradeoff. Relay every settled answer
through Domain Modeling.

Settle only outcome, invocation or exclusion, authority, Return, completion,
relationship, ownership, meaning, or boundary. Do not choose agent technique,
candidate wording, or efficacy. A minimum-viability answer returns to Prompt 1.
An H1-only contract answer preserves M0 and research identities and returns to
Prompt 2.

Return exactly `Confirmed`, `Evidence gap`, or `Blocked`, the intact Grilling
packet, current cumulative Domain Delta, and the owning resume target.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Behavior decision admission: CHANGE_ME
```

## Deploy Prompt 2: Finalize H1 Synthesis

Reconciles the selected skill's synthesis around exact M0 and research
decisions.

```text
Perform only Deploy Prompt 2 for the named skill. Never edit runtime skills,
create an experimental candidate, evaluate behavior, install, or start a
successor.

Use $writing-great-skills in Author mode. Require an intact M0 checkpoint and
`research-complete` packet with matching intended contract and identities.
Now completely read the target synthesis, canonical package, disclosed runtime
surfaces, callers, relationships, relevant tests and evaluations, candidates,
promotion records, and explicit gaps.

Map every current clause and research candidate to one semantic behavior unit.
Classify current behavior as `M0-equivalent`, `required compatibility`,
`H1 hypothesis`, `replace`, `remove`, `disclose`, `owned elsewhere`, `defer`,
or `unresolved removal risk`. Current presence creates neither intent nor
protection.

If current inspection or research exposes a missed minimum authority,
compatibility, safety, or relationship obligation, invalidate M0 and return
`blocked` with Prompt 1 as the only recommendation. H1 cannot make M0 viable.

Discover H1 hypotheses through these lanes:

- `professional-method`: independently supported method or vocabulary;
- `current-observed`: useful current behavior absent from M0;
- `pack-observed`: upstream-observed behavior considered under its explicit
  method-evidence classification;
- `pack-composition`: a concrete caller/callee scenario exposes useful
  beyond-minimum behavior; or
- `intent-adjacent`: a new action, judgment, gate, sequence, completion
  behavior, or leading term that may solve the same problem better.

Pack observation, frequency, aesthetics, and source prestige are discovery,
not admission. A pack-specific, unverified, current, composition, or novel
hypothesis may proceed as `locally-justified experimental` only when broader
research found no decisive contradiction.

For each H1 unit choose one contribution mode:

- `defect-correction`: M0 is expected to fail required behavior in a named
  representative condition; or
- `quality-lift`: M0 remains viable but is expected to score meaningfully
  lower on one pre-registered skill-specific dimension.

Every H1 unit records origin, method-evidence classification, intended value,
owner, expected M0 weakness, contribution mode, cheapest expression, positive
and wrong-condition cases, fixed rubric, proof, and residual professional or
transfer claim limits. A hypothesis may add or substitute behavior while
preserving the intended contract.

When a hypothesis changes outcome, invocation, authority, Return, completion,
exclusion, or relationship, return `behavior-decision-gap`. When one
agent-owned technical construction blocks executable H1, return
`prototype-gap`. Do not use either Interlude to prove efficacy.

Build one decision ledger:

| Unit | M0 Obligation Or H1 Origin | Method Evidence | Current State | Owner | Contribution Mode And Expected M0 Weakness | Cheapest Expression | Wrong Condition | Proof | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Make the synthesis decision-complete: intended contract, M0 checkpoint and
clause map, research registry and classifications, current dispositions, H1
transformations, protected behavior, relationships, affected surfaces, proof
matrix, rejected and deferred alternatives, lifecycle state, and residual
gaps. Preserve facts, synthesis, inference, and behavioral proof separately.

Dry-read the synthesis as Prompt 3 input. Block unless M0 is implementable
without research or current-only behavior; every current unit has a safe
disposition; every H1 unit has one origin, evidence classification, owner,
contribution mode, expected weakness, wrong-condition case, and proof; and
unresolved removal risk cannot reach promotion.

Under a Deploy Campaign, successful completion returns only
`ready-for-prompt-3`. A standalone `plan-only` request may stop here. Return
exactly `ready-for-prompt-3`, `prototype-gap`, `behavior-decision-gap`,
`evidence-gap`, or `blocked`, plus campaign shape, M0/H1 decision, prior
evidence dispositions, and residuals.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 3: Build M0 And H1

Builds the exact minimum control and hypothesis runtime.

```text
Perform only Deploy Prompt 3 for the named skill. Never run behavioral
evaluation, promote, install, deliver through Git, or start a successor.

Use $writing-great-skills in Author mode. Require Prompt 2-ready synthesis,
intact M0 and research fingerprints, and closed Interlude decisions. For a new
unscaffolded skill, use $skill-creator only for package structure and metadata.

Materialize exact M0 solely from the frozen M0 checkpoint. Do not import
research language, current-only behavior, H1 expected weaknesses, or evaluator
conclusions. Map every instruction-bearing passage to one M0 unit. Freeze
package inventory, bytes, hash, clause map, fingerprint, and limitations.
Block to Prompt 1 if the specification cannot produce one unambiguous runtime.

Construct exact H1 from M0 plus only admitted additions and substitutions.
Keep common behavior inline, disclose irreducible branches behind
trigger-bearing pointers, and point to foreign owners. Map each H1 passage to
its unit, origin, method-evidence classification, and contribution mode. A
Prototype verdict may select construction but is not behavioral evidence.

Store M0 once as the immutable control and H1 once as the candidate. When
M0 = H1, use one corpus and identity. Keep current canonical separate as
comparison evidence.

Pre-register:

- the complete M0 viability suite for outcome, invocation, authority,
  contracts, safe failure, completion, order, compatibility, and safety;
- each H1 defect-correction or quality-lift control with fixed task, model,
  host, reasoning configuration, tools, authority, evidence, runtime, rubric,
  wrong-condition case, and expected M0 weakness; and
- protected-behavior, relationship, invocation, context, and machine proof.

Cluster hypotheses only when one fixture and rubric isolate their joint
effect. Do not create a separate no-guidance control when M0 already supplies
the causal comparison.

Write one candidate record containing intended contract, M0 checkpoint,
research and Interlude dispositions, semantic ledger, runtime maps, exact
identities, proof plan, Pruning Pass boundary, affected relationships, and
residual load. Update candidate-specific structural proof only for
machine-consumed contracts; do not publish relationship changes before
promotion.

Return `ready-for-prompt-4`, `evidence-gap`, or `blocked`. M0 must be exact and
executable; H1 must be exact and fully classified.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 4: Prove M0 And H1

Establishes M0 viability, H1 contribution, and exact V1. Pruning is separate.

```text
Perform only Deploy Prompt 4 for the named skill. Never prune, promote,
install, deliver through Git, or start a successor.

Use $writing-great-skills in Author mode. Verify complete M0/H1 packages,
hashes, inventories, checkpoints, synthesis, research classifications,
semantic ledger, protected behavior, relationships, fixed evaluation
configuration, and existing evidence.

Audit M0 first. Every M0 unit must realize one settled local obligation using
the cheapest neutral behavior consistent with that obligation. Reject current
or research leakage and any beyond-minimum behavior. Run the complete M0
viability suite before H1. A failing M0 is a baseline defect: rebuild only
within the frozen specification, refreeze affected identities, and rerun
affected M0 proof. If repair requires new intent, authority, or evidence,
return `blocked` to Prompt 1. H1 never receives credit for making M0 viable.

Only after M0 passes, resolve H1 by causally coherent cluster:

1. Run at least five fresh exact M0 samples under the pre-registered task and
   rubric.
2. For `defect-correction`, require the registered failure. For
   `quality-lift`, require a meaningful pre-registered deficit while M0 remains
   viable.
3. When neither appears, record `rejected-no-control-deficit`, do not run H1
   for that cluster, and remove its units.
4. When the deficit appears, run at least five fresh H1 samples. Accept only
   repeatable material improvement with acceptably bounded variance and no new
   critical or protected-behavior regression.
5. Record `rejected-regression` for failed contribution or regression.
   Borderline effect, material variance, or unavailable decision-bearing
   telemetry returns `needs-more-evidence`; do not presume adoption.
6. After rejection, rederive H1 from M0 plus surviving transformations,
   refreeze its identity, and rerun only affected integrated proof.

If no H1 units survive, set V1 = M0. Otherwise V1 is exact M0 transformed by
accepted H1 units. Unit rejection never terminates a campaign while viable M0
and safe current-behavior dispositions remain.

Use separate proof lanes:

1. **M0 intent fidelity and viability:** exact local obligation trace and
   complete minimum-runtime suite.
2. **Method evidence:** independent support, pack/current observation, limits,
   and professional claim boundary; admission only.
3. **H1 contribution:** defect correction or quality lift against exact M0.
4. **Protected behavior:** M0 plus accepted H1 and required contracts.
5. **Invocation, context, machine, and relationships:** behavioral proof when
   wording claims effect; deterministic checks and ownership traces otherwise.

Follow `BEHAVIOR-EVALS.md`. Keep candidate language and conclusions out of M0
contexts. Alternate or randomize arms when practical. Extend samples only for
material variance or borderline effect and stop early for a critical
regression. Reuse exact arms only when the complete identity tuple matches.
Inspect every output and record per-sample results, aggregate, variance, worst
case, critical failures, deviations, model, host, tools, configuration,
unavailable telemetry, and residual transfer gaps.

Current behavior has no protection by existence. If removing a current-only
unit carries unresolved material safety, authority, compatibility, or
relationship risk, return `needs-more-evidence` and preserve the active
runtime. If all H1 units are cleanly rejected and M0 is viable, V1 = M0 may
continue.

Refresh synthesis and validation with exact dispositions and V1 identity.
Record but do not publish relationship changes. Return `accepted`,
`needs-more-evidence`, or `blocked`. `accepted` names exact V1 and recommends
the Pruning Pass.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Pruning Pass: Derive P1

Tests whether V1 behavior survives a cheaper runtime expression.

```text
Perform only the Deploy Pruning Pass for the named skill. Never add behavior,
promote, install, deliver through Git, or start a successor.

Use $writing-great-skills in Author mode. Require exact Prompt 4 acceptance,
V1 package and hash, protected behavior, and registered proof. Drift returns
`blocked` with Prompt 4 as the only recommendation.

Audit the complete runtime-facing package. Classify each instruction-bearing
passage as `keep`, `collapse`, `disclose`, or `delete`. Target duplication,
no-ops, sediment, scattered meaning, inline branch-only reference, negative
restatements, copied foreign procedure, and unused support. Protect M0,
accepted H1, safety and authority, irreversible order, proof, safe failure
Return, completion, invocation, and relationship triggers.

For every proposed cut, name the affected semantic units, expected unchanged
behavior, and reduced load. Word count is diagnostic, never the objective.

If no material cut exists, set P1 = V1 byte-for-byte, create no new behavioral
wave, record `pruning-not-needed`, and recommend Prompt 5.

For material cuts:

1. Freeze V1 once as the immutable behavior-complete control.
2. Build one P1 and group cuts by affected proof lane; do not search
   combinations.
3. Reuse exact Prompt 4 V1 arms and run only affected P1 behavior,
   M0-viability, invocation, context, machine, or relationship proof.
4. Treat pruning as non-regression: V1 need not fail.
5. Revert every regressing, ambiguous, or unproved cut group. Do not weaken
   the rubric or iterate micro-cuts. Prove surviving P1 once.

Accept a cut only when affected behavior has no critical or meaningful
regression and the named load is lower. Structural proof cannot establish
behavioral equivalence. If all cuts fail, set P1 = V1 and continue rather than
blocking promotion.

Update synthesis and candidate evidence with cut ledger, V1/P1 hashes, load
delta, reused and fresh proof, rejected cuts, and residual gaps. Return
`complete`, `evidence-gap`, or `blocked`, plus `pruned`,
`pruning-not-needed`, or `cuts-rejected` and exact P1. `complete` recommends
Prompt 5.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 5: Promote And Install P1

Promotes only exact P1, then performs the separately owned installation phase.

```text
Perform only Deploy Prompt 5 for the named skill. Never perform Git delivery
or start another skill.

Require Prompt 4 acceptance, completed Pruning Pass, exact V1 and P1 hashes,
complete P1 package, unchanged claims, and no unresolved current-removal risk.
Behavior-complete drift returns to Prompt 4; P1 drift returns to the Pruning
Pass.

First use $writing-great-skills in Author mode to promote P1 into the canonical
skill and update only directly affected canonical proof, relationships, and
synthesis. When P1 already equals canonical, perform no-op integration
read-back. Reuse exact accepted behavior evidence; do not rerun merely because
the lifecycle stage changed. Read back the complete canonical package and run
proportionate proof. Writing Great Skills stops after canonical proof.

Reconcile synthesis to active state: M0, research classifications, accepted and
rejected H1 units, V1, pruning decisions, P1, canonical identity,
relationships, proof pointers, deliberate non-changes, and residual
professional, behavioral, model, host, and transfer gaps. Remove superseded
future-tense construction and raw chronology; validation owns raw outputs.

After canonical proof, remove only this skill's experimental package and
manifest entry; preserve every other candidate. Run managed-install dry-run,
require the changed cohort to match scope, synchronize through the supported
installer when needed, and verify canonical/installed parity plus a clean
post-install dry-run. Never edit the installed mirror as canonical source.

Append promotion and installation evidence to the candidate record. Do not
rewrite research as behavioral proof or generalize beyond tested conditions.

Return `complete`, `evidence-gap`, or `blocked`, with P1, canonical, and
installed identities, validation, residual gaps, deliberate non-changes, and
`Git delivery: pending` when artifacts remain uncommitted. Recommend Prompt 6
only when delivery was authorized.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 6: Git Delivery

Optional and separately authorized.

```text
Perform only Deploy Prompt 6 for the named skill. Never begin another skill or
unrelated cleanup.

Deliver only bounded research, synthesis, validation, M0/H1/V1/P1 lifecycle,
canonical, relationship, proof, and installation-record changes belonging to
the completed campaign. Preserve unrelated work. Review the scoped diff, run
required current checks, stage intentionally, and commit. Push only when the
user explicitly requested it.

Record starting Git HEAD. Return `complete`, `evidence-gap`, or `blocked`,
including starting and ending HEAD, commit identity, remote state when pushed,
residual gaps, and exact stop reason. Every HEAD transition must be wholly
explained by this delivery.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```
