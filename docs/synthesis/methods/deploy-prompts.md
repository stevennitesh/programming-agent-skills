# Skill Synthesis And Deployment Prompts

Use these prompts to reconcile, create, or improve one skill at a time. Invoke
Deploy Prompt 1 for a standalone unit or Deploy Campaign for verified
start-to-finish orchestration. A standalone unit may reuse later durable gates.
Every new Deploy Campaign starts a fresh campaign epoch and runs Prompts 1
through 5 in order, even when the named skill completed an earlier campaign.

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
Deploy Prompt 1: establish the minimum-runtime decision
  -> when admitted: one Conditional Research Interlude, then Prompt 1 again
  -> when admitted: one Conditional Prototype Interlude, then Prompt 1 again
  -> when admitted: one Conditional Behavior Decision Interlude, then Prompt 1 again
  -> Deploy Prompt 2: finalize decision-complete synthesis
  -> Deploy Prompt 3: build B0 and C1
  -> Deploy Prompt 4: audit, prune, and prove
  -> Deploy Prompt 5: promote and install
  -> optional Deploy Prompt 6: Git delivery
```

Outside a campaign, Prompt 1 may recommend a later prompt when exact durable
artifacts and hashes prove that every earlier gate passes. Inside a new
campaign, prior artifacts and proof are evidence, not lifecycle completion:
they may reduce repeated work but never skip Prompts 1 through 5. A missing or
older synthesis is reconciled in place by Prompt 2; do not rewrite every
synthesis document before its skill is selected.

## Shared Model

The workflow keeps four evidence roles distinct:

| Input | Role | Not Authority For |
| --- | --- | --- |
| Local intent authorities | The user, caller contracts, domain decisions, and relationship owners settle the skill's outcome, invocation, authority, Return, completion, exclusions, and relationships | Agent-owned technique or proof of behavioral effectiveness |
| Upstream packages and credible research | Source meaning, professional counterpressure, conditions, mechanics, and vocabulary for a new minimum rewrite | The local intended contract, wholesale copying, or behavioral effectiveness |
| Current canonical runtime | Inventory of local behavior, compatibility, callers, and prior evidence to challenge after B0 is defined | Baseline selection, protection by existence, or carrying inherited wording into B0 |
| Candidate-owned proof | Contribution, preservation, pruning, invocation, and completion evidence for exact bytes | Broader wording, models, tasks, or hosts than it tested |

For outside research, prefer relevant books, papers, standards, documentation,
practitioner material, and projects with documented high ratings, professional
acclaim, durable adoption, and explicit upper-bound engineering discipline.
Use acclaim, ratings, and popularity to order discovery, never as proof of
correctness, mechanism value, or local fit. Preserve primary meaning,
conditions, counterpressure, disagreements, and limitations.

Use these shared artifacts:

- **Viability floor:** the minimum local intended contract: outcome, invocation
  and exclusions, authority, caller and relationship obligations, safe failure
  Return, completion, irreversible order, and safety boundaries. Local intent
  authorities settle it; upstream and current runtime do not.
- **Semantic behavior unit:** the smallest independently owned observable
  trigger, action, branch, gate, Return, or completion condition with one proof
  obligation. Classify it once and map its runtime clauses to that ledger key;
  split only when meaning, owner, or proof differs.
- **Source-first checkpoint:** the frozen B0 semantic units plus exact upstream,
  research, and independent-owner identities produced before current runtime,
  synthesis conclusions, or historical evaluations are opened. Return it as
  one exact block with a content fingerprint. Re-entry verifies its identities
  and revisits only affected rows.
- **`B0` source-derived executable minimum:** a new minimum rewrite from the
  intersection of the viability floor and the strongest applicable source
  meaning, mechanics, conditions, and vocabulary, plus the cheapest required
  local compatibility. It is never current-minus-cuts and must pass its
  minimum-runtime controls before C1 testing.
- **`D0` no-guidance control:** the same fixed task, context, tools, authority,
  and evidence as B0, with invocation held constant and only the
  source-derived steering under test omitted. Invocation uses its own proof
  lane. Use D0 for source steering without exact behavioral evidence; skip
  independently required contracts unless efficacy is also claimed.
- **Protected behavior set:** behavior independently supported by an owning
  contract, exact accepted evidence, or a non-intuitive safety or authority
  boundary. Current presence is discovery only and never creates protection.
- **C1 behavior hypothesis:** behavior beyond B0 discovered from current
  canonical (`current-retention`), skill-pack use (`pack-composition`),
  credible sources (`source-mechanism`), or a bounded beyond-minimum
  counterexample (`intent-counterexample`). Origin invites inspection; it
  never proves adoption. A counterexample that disproves minimum viability
  reopens B0 instead.
- **`C1` experimental candidate:** exact `B0` plus only admitted
  behavior hypotheses. Each must name an owner, expected B0 failure, cheapest
  expression, wrong-condition case, and proof. Source-correct substitutions
  belong in B0; cuts receive no contribution credit.
- **Behavior-complete pre-prune package:** the immutable package compared with
  final `C1` when a material cut needs pruning-equivalence proof. Store it once
  even when it also serves another evidence role.
- **Semantic substitution:** a source-supported correction that replaces
  misleading language at equal or lower runtime load. Source fidelity can
  justify it; do not claim behavioral improvement without candidate proof.

Minimum means the smallest source-derived, behavior-complete rewrite under the
accepted local contract, not the shortest file, the shortest upstream package,
or the smallest edit to current.

Record the identity relationship among current canonical runtime, `B0`, and
`C1` before routing:

| Campaign Shape | Exact Identity | Meaning | Default Route |
| --- | --- | --- | --- |
| `runtime-no-change` | current = `B0` = `C1` | The canonical runtime already expresses the minimum and no candidate delta exists. Proof may still be missing. | A standalone run may stop after Prompt 2 when B0 proof is exact. A Deploy Campaign still runs Prompts 3, 4, and 5 as fresh construction, proof-review, and integration-parity units. |
| `pruning-only` | current != `B0` = `C1` | Retained lifecycle label for a source-derived rewrite with no C1 delta. Differences from current may include reconstruction, semantic substitution, and unsupported-behavior cuts; none receives mechanism-contribution credit. | Prompts 3, 4, and 5. |
| `behavioral-candidate` | `B0` != `C1` | At least one admitted mechanism needs exact B0-first contribution proof. | Prompts 3, 4, and 5. |

An exact existing artifact may justify a later standalone prompt, but it does
not change the campaign shape or skip a unit in a new Deploy Campaign.

Classify each prior evidence item or arm before reuse:

| Evidence Disposition | Meaning |
| --- | --- |
| `exact-reusable` | Bytes, task, protocol, configuration, tools, authority, evidence, runtime, rubric, and proof lane all match. |
| `lane-limited` | The evidence remains exact for one named lane, such as metadata invocation or current-contract preservation, but proves nothing outside it. |
| `historical-admission-only` | The result can justify inspecting or admitting a mechanism but is not a control or candidate result for the current exact packages. |
| `invalidated` | A behaviorally relevant identity changed. |
| `missing` | The required evidence has not been produced. |

## Shared Run Contract

A unit invocation performs exactly one numbered prompt or Conditional
Interlude. It never starts, simulates, or partially executes its successor.
Under an active Deploy Campaign, the coordinator alone may dispatch a verified
successor after the unit stops. Preserve unrelated work and every unit's
mutation boundary.

Prompts 1 through 5 and all three Conditional Interludes record Git `HEAD` before
work and read it back before Return. They never stage or commit. If `HEAD`
changed, return `blocked` with the observed transition; Deploy Prompt 6 is the
sole Git-delivery owner.

End every run with:

```text
Authorized unit completed:
Decision:
Campaign shape:
Runtime decision:
Artifacts changed:
Evidence used or reused:
Residual gaps:
Recommended next unit:
Git HEAD: <start> -> <end>
Git delivery: not-applicable | pending | committed | pushed
Exact stop reason:
```

Use `none` when no next unit is justified. A recommendation never permits its
unit owner to begin the successor; an active campaign coordinator or later
user invocation owns dispatch. `Git delivery: pending` records uncommitted
authorized artifacts. Prompt 6 requires the initial campaign delivery mode or
a later explicit user request.
`runtime-no-change` means no canonical runtime delta is justified even when a
synthesis document changed. Completed historical records may retain the older
decision label `no-change`.

## Proportionate Proof Budget

Run the cheapest proof that can establish the current unit:

**Affected Markdown gate:** whenever Deploy Prompt 2, 5, or 6 changes
Markdown, verify every affected file's local links, internal anchors, balanced
code fences, and consistent table columns.

| Unit | Default Proof |
| --- | --- |
| Deploy Prompt 1 | Read-back, identities, and existing evidence inspection. Read tests but do not execute them unless a current-state fact cannot be established more cheaply; never run the full suite by default. |
| Deploy Prompt 2 | Complete synthesis read-back, the affected Markdown gate, directly affected documentation checks, and both diff checks. Do not run the full suite unless a machine-consumed contract changed. |
| Deploy Prompt 3 | Candidate inventory, hashes, focused structural and relationship checks, skill validation, and both diff checks. Run the full suite only when a shared machine contract or test harness changed. |
| Deploy Prompt 4 | Exact behavioral or equivalence arms, affected focused checks, and one full suite only after final accepted bytes when repository test or pack contracts changed. Do not repeat the full suite after every repair. |
| Deploy Prompt 5 | Canonical and reconciled-synthesis read-back, the affected Markdown gate, affected focused proof, one full suite after final integration, install dry-run, synchronization, parity, and clean post-install dry-run. |
| Deploy Prompt 6 | Scoped final diff, the affected Markdown gate, required current mechanical checks, both diff checks, intentional staging, commit, and an explicitly authorized push. Do not rerun unchanged behavioral evidence. |

## Deploy Campaign: Orchestrate One Skill

Runs the bounded units under one continuing user authorization.

```text
Coordinate only one Deploy Campaign for the named skill. Invoking `Run Deploy
Campaign on <skill>` explicitly authorizes bounded fresh-context delegation,
one fresh campaign epoch containing Prompts 1 through 5, and any admitted
Conditional Interludes. This remains true when the skill completed an earlier
campaign. It includes canonical promotion and managed installation but not Git
delivery.

Parse optional delivery wording once:

- bare invocation: run Prompts 1 through 5, then stop with Git delivery pending
  when bounded artifacts remain;
- `and commit`: also authorize Prompt 6 to commit, without push; or
- `and push`: also authorize Prompt 6 to commit and push.

The root owns transitions, user interaction, verification, and the terminal
decision. Track only skill, delivery mode, starting HEAD/worktree, campaign
epoch, current unit, checkpoint and identities, pending decision, and stop
reason. Do not create a controller ledger.

Dispatch one unit at a time. Start one direct child with `fork_turns="none"`
and a self-contained brief: repository, skill, delivery mode, method path and
unit, input and artifact pointers, allowed mutation paths, starting state,
proof budget, and Return contract. It loads the shared sections plus its unit,
executes only that unit, and stops. Serialize all writers; only the current
unit owner may mutate the shared workspace.

Nested delegation is evidence-only:

- Prompt 1 and Research owners may use bounded fresh-context grandchildren for
  independent source lanes.
- Prompt 4 may use fresh-context evaluation grandchildren in capacity-aware
  waves under `BEHAVIOR-EVALS.md`; the Prompt 4 owner fixes the packet and
  rubric, inspects every output, and makes the judgment.
- Other grandchildren require a concrete independent read-only check.

Give grandchildren factual briefs without parent conclusions or peer outputs.
Source and check grandchildren are filesystem-read-only; evaluation
grandchildren may write only assigned isolated or disposable outputs. None
edits shared sources, decides adoption, interacts with the user, or spawns.
Respect the active-slot budget.

After every unit, verify its allowed status, complete Return, current HEAD and
worktree, changed artifacts, hashes, and claimed proof by read-back. A summary
alone is not evidence. Reject unauthorized scope, malformed packets, or
unexplained drift.

Prior campaign artifacts never satisfy the current epoch's numbered-unit
completion. They may be reused as inputs. Exact prior proof is reusable only
when bytes, behavior or wording, task, protocol, configuration, tools,
authority, evidence, runtime, rubric, and proof lane all match. Prompt 4 must
recheck that identity and judgment; it reruns only missing, drifted,
contaminated, newly claimed, or explicitly fresh evidence.

Advance only through these transitions:

- A campaign `ready-for-prompt-N` status is valid only when N is the immediate
  numbered successor.
- Start with Prompt 1. After a successful gate, dispatch Prompt 2 even if an
  earlier campaign left exact later artifacts.
- Successful Prompt 2 dispatches Prompt 3; successful Prompt 3 dispatches
  Prompt 4. A campaign-mode unit reports that immediate successor rather than
  skipping ahead.
- `research-gap` and `prototype-gap` dispatch their exact fresh-context
  Interlude; a closing result returns only to a fresh Prompt 1.
- `behavior-decision-gap` stays root-held: run the exact
  `$grill-with-docs` Interlude, ask one material question at a time, and retain
  the campaign across the user's answers. A confirmed result returns to a
  fresh Prompt 1. Surface an exact Prototype human-verdict question the same
  way.
- Prompt 4 `accepted` dispatches Prompt 5, including when C1 already equals
  canonical. Prompt 5 `complete` is the campaign's successful terminal.
- Before returning a successful terminal, dispatch Prompt 6 only when the
  initial delivery mode authorized it and bounded campaign artifacts remain
  pending. Prompt 6 is always terminal.
- `evidence-gap`, `blocked`, rejection, `needs-more-evidence`, or an Interlude
  with no re-entry recommendation is terminal. A `none` recommendation starts
  nothing; its owning decision determines success or failure.

Within one campaign epoch, never dispatch the same unit twice against
unchanged checkpoint, bytes, evidence, and user decision except the explicit
Prompt 1 re-entry after an Interlude. A later top-level `Run Deploy Campaign`
invocation creates a new epoch and runs every numbered unit again. Do not ask
the user to authorize ordinary unit transitions. Ask only for an admitted
intended-contract decision, an exact human verdict, or new external authority.

Give a concise update at each unit boundary. When awaiting the user, ask the
exact question and say the campaign remains active; do not emit a terminal
campaign result. At terminal Return, report:

Campaign:
Skill:
Terminal decision:
Units completed:
Canonical and installed identities:
Evidence:
Residual gaps:
Git HEAD: <campaign start> -> <campaign end>
Git delivery: pending | committed | pushed | not-applicable
Worktree:
Exact stop reason:

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 1: Establish The Minimum-Runtime Decision

Universal read-only entry point.

```text
Perform only Deploy Prompt 1 for the named skill. Never start its recommended successor.

Use $writing-great-skills in Audit mode.

Re-entry: when an earlier source-first checkpoint is supplied, verify its Git HEAD, local intent authorities, upstream revisions and relevant file hashes, and research pointers before opening current runtime or synthesis. Reuse settled units when identities match except for the exact admitted interlude delta; apply only that delta and issue a successor checkpoint. Unexpected drift requires a new blind pass.

Blind intent and evidence pass: do not open the current canonical skill body, current synthesis conclusions, historical evaluations, experimental candidates, or promotion records until the source-first checkpoint is frozen.

Intent pass: establish the viability floor only from local intent authorities.
Read the applicable user, domain, relationship-owner, and caller-owned contract
surfaces; read a complete caller package when context can alter the contract.
Settle the outcome, invocation and exclusions, authority, caller and
relationship obligations, safe failure Return, completion, irreversible order,
and safety boundaries. Upstream packages, research, and the target's current
implementation cannot settle local intent.

When any minimum-viability axis is materially fuzzy, stop before source selection and return a Conditional Behavior Decision Interlude admission. Include the bounded intended-contract decision, unresolved axes, available authority and evidence, recommendation, decisive tradeoffs, and consequences. Do not ask about agent-owned mechanics.

Evidence pass: inspect all three checked-out upstreams as source candidates:

- Matt Pocock under `.tmp/mattpocock-skills`;
- Superpowers under `.tmp/superpowers`; and
- Ponytail under `.tmp/ponytail`.

Search ignored paths explicitly. For each upstream, record HEAD, worktree state, access depth, and freshness. Completely read each plausible equivalent package and any named exclusion or change record that can alter its meaning. A verified absence needs only the search evidence; unchanged exact source evidence may be reused through the checkpoint.

Read the applicable rows of `docs/research/language/upper-bound-engineering-language.md`, their decision-relevant evidence pointers, and any independently discoverable skill-specific source packet. Preserve `direct`, `corroborated`, `synthesis`, `inference`, and `thin`. Upstream usage proves what a pack instructs, not professional correctness, local intent, or efficacy.

Draft B0 from the intersection of the settled viability floor and credible source mechanics. Select only what is needed to realize the intended contract plus the cheapest required local compatibility. Merge equivalent language under one semantic owner. Retain a leading term only when it more precisely recruits an observable action, gate, Return, or completion condition; repetition across packs is not support.

Freeze one source-first checkpoint before opening current. It contains the viability floor; settled B0 semantic units; each unit's intent obligation, source mechanic, conditions, limitations, and cheapest expression; source identities and hashes; at most one admitted unresolved row; known gaps; and a content fingerprint. Every settled B0 unit has exactly one or more of these bases:

- settled intent realized through a source-supported mechanic;
- a source-correct semantic substitution; or
- independently required local compatibility.

If source authority, meaning, conditions, or professional validity can change
one unit, return a Conditional Research Interlude with the checkpoint, exact
question, affected row, evidence boundary, authorized note path, finite stop,
and consequence of no answer. If one agent-owned technical choice prevents
executable B0 or C1 and a disposable runnable probe can decide it, return a
Conditional Prototype Interlude with the checkpoint, frozen design question,
verdict basis, authorized disposable boundary, affected row, and consequence.
Behavioral wording or efficacy waits for exact D0/B0/C1 evaluation.

Current reconciliation: only now completely read the target's current
synthesis, canonical package, disclosed runtime surfaces, current caller
implementations beyond the contract surfaces already inspected, relevant tests
and evaluations, candidates, promotion records, and explicit gaps. Headings
and excerpts are navigation only.

Map current runtime clauses to semantic behavior units and classify each unit once as `B0`, `required compatibility`, `C1 hypothesis`, `replace`, `remove`, `disclose`, `owned elsewhere`, or `defer`. Split only when meaning, owner, or proof differs. Current presence creates neither intent, B0, nor protection.

If reconciliation exposes a previously missed intent authority or mandatory
compatibility, record its exact owner, invalidate the checkpoint, and return a
`blocked` result with fresh Prompt 1 as the only recommendation and that new
blind input. Never retrofit B0 after current or credit C1 for the omission.

Discover C1 hypotheses from four lanes:

- `current-retention`: current behavior absent from B0;
- `pack-composition`: a concrete caller/callee workflow exposes a missing owner, action, gate, Return, or completion condition;
- `source-mechanism`: credible evidence suggests a useful mechanic beyond minimum viability; or
- `intent-counterexample`: a normal, edge, failure, inclusion, or exclusion
  scenario exposes a useful beyond-minimum behavior under settled intent. If
  it disproves minimum viability, reopen B0 instead.

Symmetry, aesthetic completeness, frequency, and an interesting idea do not create a hypothesis. Classify prior proof as `exact-reusable`, `lane-limited`, `historical-admission-only`, `invalidated`, or `missing`, naming the exact identity and proof lane.

Build one ledger with one row per semantic behavior unit:

| Unit | Intent Or Source Support | Origin Or Current State | Prior Evidence | B0 Or C1 Basis | Owner | Cheapest Expression | Destination | Required Proof | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

B0 basis is `settled intent + source mechanic`, `semantic substitution`, or
`required local compatibility`. C1 origin is one of the four discovery lanes;
admission requires exact prior contribution evidence or a bounded trial with
intended value, owner, and an exact expected B0 failure. A required local
contract or minimum safety or authority boundary belongs in B0. Origin is not
admission.

Specify executable B0 and exact C1 = B0 plus admitted hypotheses. Every C1 unit records origin, intended value, owner, exposing evidence, expected B0 failure, cheapest expression, positive and wrong-condition cases, and proof. Mark every B0 steering unit without exact behavioral evidence `D0-required`; required contracts receive owner-matched proof unless efficacy is claimed.

Record `runtime-no-change`, `pruning-only`, or `behavioral-candidate`; Prompt 3 later confirms unmaterialized identities. Challenge ambiguity, ownership, counterexamples, branch load, and the cut test.

Apply the same bounded Research or Prototype admission to a C1 hypothesis when
its source validity or agent-owned mechanic remains decision-changing.
Preserve the checkpoint because minimum viability is unchanged.

When adopting a C1 hypothesis changes the intended outcome, invocation, authority, Return, completion, exclusion, or relationship, return a Conditional Behavior Decision Interlude. Include its origin, affected contract axis, alternatives, local authority, recommendation, tradeoff, expected B0 failure, and consequences. Grill intent and ownership only; agent-owned technique goes to Prototype or evaluation.

Gate the packet: local authorities settle intent; the checkpoint precedes current loading; every B0 unit joins an intent obligation to a source mechanic or required compatibility; every current unit and prior proof has one disposition; every C1 hypothesis has one origin, owner, expected failure, wrong-condition case, and proof; relationships have owners; gaps retain consequences; and campaign shape agrees with the identities.

For a standalone invocation, recommend the earliest unmet unit only when
earlier durable prerequisites are exact. Under a fresh Deploy Campaign,
successful completion always returns `ready-for-prompt-2`; prior campaign
artifacts remain classified evidence and cannot skip this epoch's synthesis
unit.

Return the intended contract, checkpoint, ledger, B0, C1, protected behavior, campaign shape, owners and relationships, proof outline including D0 decisions, rejected and deferred units, gaps, gate result, and one decision: `ready-for-prompt-2`, `ready-for-prompt-3`, `ready-for-prompt-4`, `ready-for-prompt-5`, `research-gap`, `prototype-gap`, `behavior-decision-gap`, `runtime-no-change`, `evidence-gap`, or `blocked`.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Conditional Research Interlude

Run only when Prompt 1 returns `research-gap` with a complete admission packet.

```text
Perform only the Conditional Research Interlude for the named skill and the exact Prompt 1 admission packet. Never edit synthesis or runtime and never start Deploy Prompt 1 afterward.

Use $research for exactly the admitted source question and authorized note path.
Apply the Shared Model source priority and favor original or primary evidence
for factual claims. When the result is a concept or technique packet, apply
`docs/synthesis/methods/source-distillation-flow.md` as its output standard.
Record why sources were selected and preserve source meaning before
application, claim labels, access depth, freshness, counterpressure,
limitations, contradictions, rejected lanes, and the finite stop.

Use the smallest source set that settles the row under credible counterpressure;
stop when another acclaimed or popular source cannot change its disposition.
Do not expand into adjacent research, skill design, candidate wording,
behavioral evaluation, synthesis edits, runtime edits, installation, or
delivery. Preserve the source-first checkpoint fingerprint and identify only
the affected ledger row. Return exactly `source-packet-complete`,
`evidence-gap`, or `blocked`.

Recommend Deploy Prompt 1 only when the returned packet can now change the admitted ledger decision. Otherwise recommend `none` and name the unresolved condition.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Research admission: CHANGE_ME
```

## Conditional Prototype Interlude

Run only when Prompt 1 returns `prototype-gap` with one complete admission
packet.

```text
Perform only the Conditional Prototype Interlude for the named skill and exact Prompt 1 admission packet. Never edit synthesis or runtime, evaluate skill wording, or start Deploy Prompt 1 afterward.

Use $prototype for the one frozen agent-owned design question. Prompt 1 remains the decision owner and result recipient. Keep the intended contract, source conditions, representative cases, verdict basis, and authorized disposable boundary fixed. Build only the smallest runnable probe needed to distinguish the candidate mechanics; production correctness and behavioral steering remain untested.

Preserve the source-first checkpoint fingerprint and identify only the affected ledger row. Return the intact Prototype result plus exactly one wrapper status: `prototype-complete`, `awaiting-human-verdict`, `evidence-gap`, or `blocked`.

Recommend Deploy Prompt 1 only when the verdict can close the admitted row. Otherwise recommend `none` and name the re-entry condition.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Prototype admission: CHANGE_ME
```

## Conditional Behavior Decision Interlude

Run only when Prompt 1 returns `behavior-decision-gap` with one complete
minimum-viability or C1 contract admission packet.

```text
Perform only the Conditional Behavior Decision Interlude for the named skill and exact Prompt 1 behavior packet. Never edit synthesis or runtime, run behavioral evaluation, or start Deploy Prompt 1 afterward.

Use $grill-with-docs for exactly one bounded intended-contract decision. It may clarify minimum viability or judge a C1 hypothesis originating from current runtime, pack composition, credible sources, or an intent counterexample. Before questioning, state context action `render only`, ADR action `offer only`, the possibility that a domain collision may reopen or block the decision, and that confirmation starts no downstream work. Ask one material question at a time with one recommendation and decisive tradeoff. Relay every settled answer through Domain Modeling and return the intact Grilling packet plus current cumulative Domain Delta.

Settle only outcome, invocation or exclusion, authority, Return, completion, relationship, ownership, meaning, or boundary. Do not decide agent-owned technique, candidate wording, or efficacy. A confirmed minimum-viability answer becomes local intent for a new blind pass. A confirmed beyond-minimum behavior remains provisional C1 until Prompt 4 proof.

When a checkpoint exists, preserve it when the answer affects only C1 and
invalidate it when minimum viability changes. Return exactly `Confirmed`,
`Evidence gap`, or `Blocked`. Recommend Deploy Prompt 1 only when the result
can close the admitted decision; otherwise recommend `none` and name the
re-entry condition.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Behavior decision admission: CHANGE_ME
```

## Deploy Prompt 2: Finalize Decision-Complete Synthesis

Creates or reconciles the selected skill's synthesis in place.

```text
Perform only Deploy Prompt 2 for the named skill. Never edit runtime skills, create an experimental candidate, run behavioral evaluations, install, or start the recommended successor.

Use $writing-great-skills in Author mode. Require a gated Prompt 1 packet with
its intended contract, source-first checkpoint, ledger, and every admitted
interlude result. Match checkpoint fingerprints wherever one existed; a
minimum-viability decision requires the successor checkpoint created by
Prompt 1. Create or reconcile the whole-skill synthesis in place. Preserve
decision-changing provenance, material alternatives, rejection reasons,
ownership, and evidence limits; collapse duplicate or superseded
representations.

Make these decisions discoverable without requiring exact headings:

- status, outcome, and viability floor;
- checkpoint fingerprint, source identities, claim labels, and limits;
- one semantic-unit ledger joining each B0 unit to its intended-contract
  obligation and source mechanic or required compatibility, and recording
  current, research, Prototype, protected-behavior, and C1 dispositions;
- every C1 hypothesis's origin, owner, expected B0 failure, cheapest
  expression, wrong-condition case, proof, destination, and decision;
- executable B0, exact C1 delta, campaign identity, relationships, and affected
  runtime surfaces;
- proof matrix separating B0 viability, conditional D0 no-op comparison, C1
  contribution, invocation, protected contracts, pruning, and deterministic
  proof;
- candidate lifecycle state and residual gaps.

Keep facts, synthesis, and inference separate. Research can establish source
meaning, a grill can settle intent, and a Prototype can choose one runnable
technical design; none proves skill-steering effect. Keep evaluation,
installation, worker, and Git procedure with their owners.

Keep the synthesis decision-complete, not chronological. Raw outputs and run history belong in validation.

Dry-read it as Prompt 3 input. Block unless the checkpoint is intact; every B0
unit maps a settled intended-contract obligation to a credible source mechanic
or required compatibility; every semantic unit has one basis, owner,
disposition, destination, and proof; B0 is implementable without current-only
behavior; each C1 hypothesis has one origin and names an expected failure and
wrong-condition case; D0 decisions are explicit; foreign behavior points to
its owner; Prototype evidence is construction evidence only; and campaign
identity is coherent.

Preserve exact qualifying candidate and evidence hashes. Never manufacture historical B0 or proof.

Under a fresh Deploy Campaign, successful completion always returns
`ready-for-prompt-3`; exact prior artifacts remain inputs to the current
epoch's construction unit. For a standalone invocation, if current = B0 = C1
and all B0 proof is exact, return `runtime-no-change`. If those bytes match but
B0 viability or D0 evidence is missing, return `ready-for-prompt-3` for an
evidence-only route with no runtime delta. Other unmaterialized identities also
return `ready-for-prompt-3`. Skip forward only outside a campaign and only when
every earlier durable gate is exact.

Return `ready-for-prompt-3`, `ready-for-prompt-4`, `ready-for-prompt-5`, `runtime-no-change`, `evidence-gap`, or `blocked`, plus the campaign shape, final B0/C1 decision, prior-evidence dispositions, and every preserved residual.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 3: Build B0 And C1

Builds the executable minimum control and experimental candidate.

```text
Perform only Deploy Prompt 3 for the named skill. Never run behavioral evaluation, promote, install, deliver through Git, or start the recommended successor.

Use $writing-great-skills in Author mode. Require a synthesis that passed Prompt 2 readiness. For a new unscaffolded skill, use the bundled $skill-creator only for package structure and metadata mechanics; semantic authoring remains here.

Verify the source-first checkpoint and source identities; reread a source only when its identity drifted or the synthesis does not preserve enough exact meaning to author its unit. Inventory the complete current package and every B0/C1-owned surface. Preserve unrelated work.

Under a fresh Deploy Campaign, reperform the construction audit and freeze
current-epoch B0/C1 identities even when an earlier candidate is byte-identical.
Reuse identical package bytes rather than rewriting them, but do not treat the
earlier Prompt 3 completion as this epoch's completion.

Construct B0 from the frozen intersection of the intended contract and credible
source mechanics, not by pruning canonical or experimental bytes. Keep the
viability floor complete and exclude current-only behavior, C1 language,
expected failures, and evaluator conclusions. Map every B0 unit to its local
intent obligation and source mechanic or required compatibility. Map each
instruction-bearing runtime passage to one unit key; many passages may share a
key, and text needs a separate classification only when its behavior, owner,
or proof differs. Freeze exact package bytes, inventory, hash, checkpoint
fingerprint, unit map, and limitations.

Construct exact C1 from B0 plus only admitted hypotheses from
`current-retention`, `pack-composition`, `source-mechanism`, and
`intent-counterexample`. Keep common behavior inline, disclose irreducible
branches behind trigger-bearing pointers, and point to foreign owners. Mark
trial units provisional with their expected B0 failure. A Prototype verdict
may select a technical expression; it is not behavioral-effect evidence.

When B0 = C1, store one corpus and one hash. Otherwise record the exact unit-level transformation. Keep current canonical separate as comparison evidence. Freeze a pre-prune package only when a material equivalence claim needs it.

Pre-register the B0 minimum-runtime suite for its outcome, invocation, authority, required contracts, safe failure, completion, order, and safety. Keep these controls separate from C1's expected B0 failures.

For `D0-required` units, freeze the smallest causally coherent no-guidance controls with task, context, tools, authority, evidence, and invocation held fixed. Cluster units only when one fixture and rubric isolate their joint effect. Reuse the matching B0 viability arm as the candidate arm. Do not create D0 for owner-required contracts unless efficacy is also claimed.

Write one candidate record containing the intended contract, checkpoint,
interlude dispositions, unit ledger and runtime map, exact package identities,
B0 suite, D0 controls, C1 proof plan, pruning control when needed, affected
relationships, and residual load. Store each corpus once.

Update candidate-specific structural proof only for machine-consumed contracts. Record proposed invocation, caller, ownership, and Return deltas in synthesis and candidate evidence; do not change the current relationship index before promotion. Read back every created or changed surface and run proportionate mechanical and candidate-relationship checks.

Return `ready-for-prompt-4`, `evidence-gap`, or `blocked`. B0 must be an executable control and C1 must be exact; a conceptual baseline or unclassified candidate cannot pass.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 4: Audit, Prune, And Prove

Establishes minimality, contribution, and preservation for exact candidate
bytes.

```text
Perform only Deploy Prompt 4 for the named skill. Never promote, install, deliver through Git, or start the recommended successor.

Use $writing-great-skills in Author mode. Verify the complete B0 and C1
packages, hashes, inventories, intended contract, B0 provenance, synthesis
decisions, protected behavior set, all four C1 hypothesis origins, semantic
ledger, interlude dispositions, and existing evidence. Refresh a source or
control only when its identity, contract, or configuration drifted.

Audit B0 first. Reject or rebuild a unit that does not realize one settled
intended-contract obligation through a credible source mechanic or required
compatibility, copies current, weakens a source condition, or uses a heavier
local expression than needed. Reputation and popularity never substitute for
unit-level support.

Run each required D0 control before its matching B0 arm, then complete the B0 minimum-runtime suite. D0 and B0 follow `BEHAVIOR-EVALS.md` when the claim is behavioral. If D0 matches B0 without a meaningful variance benefit, remove or demote the unproven steering unless an independent contract requires it, refreeze B0 and derived C1, and rerun only affected B0 proof. If B0 fails the viability floor, treat that as a baseline defect, not useful red evidence. Rebuild within settled units, rederive C1 and hashes, and invalidate affected proof; if repair requires new intent, source, or design authority, return `blocked` to Prompt 1. C1 never receives credit for making B0 viable.

Only after B0 passes, challenge each C1 unit against its origin, basis, owner,
cheaper expression, branch load, aggregate cost, and expected failure. Intent
confirmation and Prototype construction evidence never substitute for
behavioral contribution proof. If the challenge would reverse a material user
decision rather than enforce it, return `blocked` and recommend a fresh
Prompt 1 decision pass.

Repair only genuine omissions relative to B0, admitted C1 deltas, and the protected behavior set. Every repair creates new C1 bytes and invalidates only behaviorally affected candidate evidence.

Use separate proof lanes:

1. **B0 intent and source fidelity:** exact unit-to-intent and source-mechanic
   or compatibility trace, including conditions and limits.
2. **B0 effect and viability:** conditional D0 comparison plus the complete minimum-runtime suite.
3. **C1 contribution:** for current-retention, pack-composition,
   source-mechanism, and intent-counterexample hypotheses, run B0 first and run
   C1 only when the expected failure appears. Test pack composition against the
   exact caller/callee scenario.
4. **Protection and pruning:** prove only independently protected and admitted behavior; pre-prune extras gain no protection.
5. **Invocation and context:** test positive reach, adjacent negatives, false competition, body loading, and branch pointers only when affected.
6. **Machine and relationship contracts:** use deterministic checks and ownership traces.

Use read-back and deterministic checks for exact bytes and machine contracts, relationship traces for ownership, and the current `BEHAVIOR-EVALS.md` contract for behavioral claims. Test positive, failure-revealing, and wrong-condition pressure only to the breadth claimed. A required caller contract or non-intuitive safety boundary may be admitted through contract-matched deterministic or relationship proof; do not invent a red behavioral claim merely to justify it.

Pruning is non-regression, not contribution; its control need not fail. Description shortening also needs invocation proof.

Minimize cost without weakening attribution. Cluster units only when one fixed
fixture and rubric genuinely exercise them. Reuse exact unchanged arms when
bytes, behavior or wording, task, protocol, configuration, tools, authority,
evidence, runtime, rubric, and proof lane match. The current Prompt 4 must
recheck that identity and judgment, but it does not rerun identical samples.
Preserve controls after repairs and rerun only affected candidate arms. Keep
candidate language and conclusions out of neutral contexts.

Inspect every result. Record per-sample outcomes, variance, worst result, critical failures, deviations, unavailable telemetry, process cost when decision-relevant, raw-artifact pointers, and residual gaps. A screening result supports only its tested tasks, model, harness, and claim.

Reperform the cut test. Source provenance alone does not preserve runtime text. Retain a B0 unit only when the viable source-derived outcome or local contract requires it and any behavior-change claim passes D0. Retain C1 only with exact evidence, demonstrated contribution, contract-matched proof, a proved safety or authority role, or minimum execution context.

Refresh the synthesis and candidate-owned validation surfaces with the exact learned decisions and final evidence dispositions. Record the accepted relationship delta without publishing it into the current relationship index before Prompt 5. Keep raw evaluation and campaign ledgers in validation; do not copy evaluation procedure into synthesis.

Return `accepted`, `reject-no-control-failure`, `reject-regression`,
`needs-more-evidence`, or `blocked`. `accepted` names the exact final C1 hash.
Under a fresh Deploy Campaign it always recommends Prompt 5; standalone work
recommends Prompt 5 only when canonical integration, relationship publication,
or installation remains.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 5: Promote And Install

Promotes only the accepted exact candidate, then performs the separately owned
installation phase.

```text
Perform only Deploy Prompt 5 for the named skill. Never perform Git delivery or start another skill.

Require the accepted Prompt 4 record, exact final C1 hash, complete candidate package, and unchanged affected behavioral claims. If candidate bytes or a tested claim changed, stop and recommend Deploy Prompt 4 without promoting.

First use $writing-great-skills in Author mode to promote the accepted
candidate into the canonical skill and update only directly affected canonical
proof, relationship, and synthesis surfaces. When accepted C1 already equals
canonical, perform a no-op integration read-back instead of rewriting it.
Reuse accepted behavioral evidence when bytes, tasks, claims, and evidence
contracts are unchanged; do not rerun a wave solely because the lifecycle
stage changed. Read back the complete canonical package and run proportionate
canonical proof. Writing Great Skills stops after that proof.

Reconcile the active synthesis to the promoted state: record the canonical identity, final runtime and relationship surface, admitted and rejected mechanism or cut decisions, exact proof pointers, deliberate non-changes, and residual gaps. Remove duplicated future-tense construction instructions, superseded candidate representations, and raw campaign chronology from the active design. Preserve decision-changing history concisely; validation remains the owner of raw outputs and chronological run evidence.

Only after canonical proof passes, complete the separately owned experimental
and installation lifecycle authorized by this prompt: remove only the promoted
skill's entire experimental directory and manifest entry; preserve every other
candidate; run the managed installation dry-run; require the proposed changed
cohort to match the authorized scope; synchronize through the supported
installer when drift exists; and verify canonical-to-installed parity and a
clean post-install dry-run. When canonical and installed already match and the
dry-run is clean, record no-op installation parity without rewriting either.
Never edit the installed mirror as canonical source.

Append promotion and installation evidence to the candidate-owned record. Update research only when separately authorized: an exact downstream evidence pointer may narrow a stale universal gap, but it must not duplicate results or generalize beyond the tested candidate.

Return `complete`, `evidence-gap`, or `blocked`, with canonical and installed identities, validation, residual gaps, deliberate non-changes, and `Git delivery: pending` when authorized artifacts remain uncommitted. Recommend Deploy Prompt 6 only when Git delivery is wanted; otherwise recommend `none`.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 6: Git Delivery

Optional and separately invoked.

```text
Perform only Deploy Prompt 6 for the named skill. Never begin another skill or unrelated cleanup.

Deliver only the bounded synthesis, validation, baseline/candidate lifecycle, canonical, relationship, proof, and installation-record changes belonging to the completed skill campaign. Preserve unrelated work. Review the final scoped diff, run required current checks, stage intentionally, and commit the verified result. Push only when the user explicitly requests it.

Record the starting Git HEAD before delivery. Return `complete`, `evidence-gap`, or `blocked`, including the starting and ending HEAD, delivered commit identity when created, remote state when a push was authorized, residual gaps, and exact stop reason. Any HEAD transition must be wholly explained by this bounded delivery.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```
