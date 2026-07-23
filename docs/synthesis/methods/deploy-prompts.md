# Skill Synthesis And Deployment Prompts

Use these prompts to reconcile, create, or improve one skill at a time. Always
start with Deploy Prompt 1, even when a synthesis, experimental candidate, or
promotion record already exists. Prompt 1 verifies the durable state and
returns the earliest justified next unit.

Invoke one with, for example:

```text
Run Deploy Prompt 1 for diagnosing-bugs.
```

The ordinary sequence is:

```text
Deploy Prompt 1: establish the minimum-runtime decision
  -> when admitted: one Conditional Research Interlude, then Prompt 1 again
  -> Deploy Prompt 2: finalize decision-complete synthesis
  -> Deploy Prompt 3: build B0 and C1
  -> Deploy Prompt 4: audit, prune, and prove
  -> Deploy Prompt 5: promote and install
  -> optional Deploy Prompt 6: Git delivery
```

Prompt 1 may recommend a later prompt only when exact durable artifacts and
hashes prove that every earlier gate already passes. A missing or older
synthesis is reconciled in place by Prompt 2; do not rewrite every synthesis
document before its skill is selected.

## Shared Model

The workflow keeps four evidence roles distinct:

| Input | Role | Not Authority For |
| --- | --- | --- |
| Simplest credible upstream or current baseline | Smallest coherent design control for the core outcome | Local caller, platform, safety, or completion obligations it does not satisfy |
| Current canonical runtime | Source of local behavior, compatibility, callers, and prior evidence to classify | Preserving every existing mechanism or sentence |
| Credible research | Source meaning, professional counterpressure, conditions, and candidate techniques | Automatic local adoption or behavioral effectiveness |
| Candidate-owned proof | Contribution, preservation, pruning, invocation, and completion evidence for exact bytes | Broader wording, models, tasks, or hosts than it tested |

Use these shared artifacts:

- **Viability floor:** the outcome, invocation, authority, required caller and
  platform contracts, safe failure Return, completion, irreversible order, and
  safety boundaries the skill must preserve.
- **Protected behavior set:** current behavior that has a required owner,
  accepted evidence, caller contract, or non-intuitive safety value. Current
  prose is not protected merely because it exists.
- **`B0` executable minimum control:** the simplest credible baseline core,
  adapted only with mandatory local contracts and source-correct semantic
  substitutions that make no behavioral-improvement claim.
- **`C1` experimental candidate:** exact `B0` plus only admitted
  behavior-changing mechanisms. Source-correct substitutions and
  behavior-preserving cuts relative to the current or pre-prune package belong
  to baseline selection or the pruning lane, not the mechanism delta. A cut
  never receives mechanism-contribution credit.
- **Behavior-complete pre-prune package:** the immutable package compared with
  final `C1` when a material cut needs pruning-equivalence proof. Store it once
  even when it also serves another evidence role.
- **Semantic substitution:** a source-supported correction that replaces
  misleading language at equal or lower runtime load. Source fidelity can
  justify it; do not claim behavioral improvement without candidate proof.
- **Behavioral addition:** an action, branch, gate, pointer, Return, or
  completion demand beyond `B0`. It enters `C1` only when it cures an observed
  baseline failure, satisfies a required caller or platform contract, or
  protects a non-intuitive safety or authority boundary.

Minimum means the smallest behavior-complete runtime under the accepted
contract, not the shortest file or shortest upstream package.

Record the identity relationship among current canonical runtime, `B0`, and
`C1` before routing:

| Campaign Shape | Exact Identity | Meaning | Default Route |
| --- | --- | --- | --- |
| `runtime-no-change` | current = `B0` = `C1` | The canonical runtime already is the executable minimum and no candidate delta exists. Synthesis may still need reconciliation. | Stop after Prompt 2 unless exact later lifecycle work already exists. |
| `pruning-only` | current != `B0` = `C1` | The minimum differs only through a source-correct substitution or behavior-preserving cut; there is no mechanism-contribution claim. | Prompts 3, 4, and 5. |
| `behavioral-candidate` | `B0` != `C1` | At least one admitted mechanism needs exact B0-first contribution proof. | Prompts 3, 4, and 5. |

An exact existing artifact may justify a later prompt, but it does not change
the campaign shape.

Classify each prior evidence item or arm before reuse:

| Evidence Disposition | Meaning |
| --- | --- |
| `exact-reusable` | Bytes, task, protocol, configuration, tools, authority, evidence, runtime, rubric, and proof lane all match. |
| `lane-limited` | The evidence remains exact for one named lane, such as metadata invocation or current-contract preservation, but proves nothing outside it. |
| `historical-admission-only` | The result can justify inspecting or admitting a mechanism but is not a control or candidate result for the current exact packages. |
| `invalidated` | A behaviorally relevant identity changed. |
| `missing` | The required evidence has not been produced. |

## Shared Run Contract

Every invocation performs exactly one named prompt or one Conditional Research
Interlude. Never start, simulate, or partially execute the recommended
successor. Preserve unrelated work and stop at the prompt's mutation boundary.

Prompts 1 through 5 and the Conditional Research Interlude record Git `HEAD`
before work and read it back before Return. They never stage or commit. If
`HEAD` changed, return `blocked` with the observed transition; Deploy Prompt 6
is the sole Git-delivery owner.

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

Use `none` when no next unit is justified. A recommendation is not permission
to begin it. `Git delivery: pending` records uncommitted authorized artifacts;
it makes Deploy Prompt 6 available but does not recommend or authorize it.
`runtime-no-change` means no canonical runtime delta is justified even when a
synthesis document changed. Completed historical records may retain the older
decision label `no-change`.

## Proportionate Proof Budget

Run the cheapest proof that can establish the current unit:

| Unit | Default Proof |
| --- | --- |
| Deploy Prompt 1 | Read-back, identities, and existing evidence inspection. Read tests but do not execute them unless a current-state fact cannot be established more cheaply; never run the full suite by default. |
| Deploy Prompt 2 | Complete synthesis read-back, local links and table structure, directly affected documentation checks, and both diff checks. Do not run the full suite unless a machine-consumed contract changed. |
| Deploy Prompt 3 | Candidate inventory, hashes, focused structural and relationship checks, skill validation, and both diff checks. Run the full suite only when a shared machine contract or test harness changed. |
| Deploy Prompt 4 | Exact behavioral or equivalence arms, affected focused checks, and one full suite only after final accepted bytes when repository test or pack contracts changed. Do not repeat the full suite after every repair. |
| Deploy Prompt 5 | Canonical read-back, affected focused proof, one full suite after final integration, install dry-run, synchronization, parity, and clean post-install dry-run. |
| Deploy Prompt 6 | Scoped final diff, required current mechanical checks, both diff checks, intentional staging, commit, and an explicitly authorized push. Do not rerun unchanged behavioral evidence. |

## Deploy Prompt 1: Establish The Minimum-Runtime Decision

Universal read-only entry point.

```text
Perform only Deploy Prompt 1 for the named skill. Never start its recommended successor.

Use $writing-great-skills in Audit mode. Read the complete current whole-skill synthesis when one exists, the complete canonical package, every disclosed runtime surface, directly affected callers and relationships, relevant current tests and evaluations, candidate or promotion records, and explicit evidence gaps. Headings, searches, summaries, and truncated excerpts are navigation aids, not complete coverage.

Inspect every checked-out upstream below as a mandatory baseline candidate:

- Matt Pocock under `.tmp/mattpocock-skills`;
- Superpowers under `.tmp/superpowers`; and
- Ponytail under `.tmp/ponytail`.

Search ignored paths explicitly, such as with `rg -uu`. For each upstream, locate and completely read the matching or equivalent package when one exists, plus any directly named exclusion or change record capable of changing its interpretation. Record the independent HEAD, worktree state, access depth, and freshness limit. Record an absent checkout or missing equivalent as a gap.

Read the applicable rows of `docs/research/language/upper-bound-engineering-language.md`, their exact evidence pointers when decision-relevant, and any skill-specific source packet already named by the synthesis. Preserve `direct`, `corroborated`, `synthesis`, `inference`, and `thin` boundaries. Research is pressure and source evidence, not local runtime authority.

First establish the viability floor: outcome, invocation, authority, required caller and platform contracts, safe failure Return, completion, irreversible order, and non-intuitive safety boundaries. Then compare every available upstream and the current canonical runtime. Select the simplest credible baseline that still achieves the core outcome. Use a minimal scratch outline only when no inspected package is credible. Name what the selected baseline omits and do not hide local obligations inside the word `adapt`.

Classify every distinct current-runtime behavior as `protect`, `replace`, `remove`, `disclose`, `owned elsewhere`, or `defer`. Protect only behavior supported by a required owner or caller contract, accepted evidence, or a non-intuitive safety boundary.

Classify every applicable research item as `semantic substitution`, `candidate mechanism`, `supporting rationale only`, `reject`, `defer`, or `evidence gap`. A semantic substitution may enter B0 only when it corrects meaning at equal or lower load without an efficacy claim. A candidate mechanism belongs beyond B0 and requires an admission basis.

Classify every prior evaluation, deterministic check, relationship trace, or promotion record as `exact-reusable`, `lane-limited`, `historical-admission-only`, `invalidated`, or `missing`. Name the exact bytes, task, protocol, configuration, authority, rubric, and proof lane behind any reuse. An aggregate result may admit a mechanism for inspection without serving as the current B0 or C1 arm.

Build one unified baseline-delta ledger:

| Mechanism | Baseline State | Current Disposition | Research Pressure And Claim Label | Admission Basis | Owner | Cheaper Expression | Runtime Destination | Required Proof | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Admission basis is exactly one or more of: `core outcome`, `required local contract`, `non-intuitive safety or authority boundary`, or `observed baseline failure`. Existing prose, a conceivable edge case, polished rationale, term frequency, a confirmed recommendation, or an existing structural test is not an admission basis by itself.

Specify B0 as an executable locally compatible minimum, not a conceptual slogan. Specify C1 only as B0 plus admitted behavioral additions. Classify substitutions and cuts relative to the current runtime separately from those additions. For each addition, name the exact failure or contract, cheapest operational expression, owner, positive or wrong-condition cases, and proof type. Translate retained steering research into `professional term + observable action + evidence or completion gate`; keep provenance and rationale in synthesis rather than runtime.

Record the expected campaign shape from the current/B0/C1 identity: `runtime-no-change`, `pruning-only`, or `behavioral-candidate`. Prompt 3 must later confirm any not-yet-materialized identity with exact hashes. Do not route a pruning-only campaign through mechanism-contribution claims.

Challenge the aggregate design through ambiguity, ownership trace, inversion, counterexample, cut test, common-path versus branch-only load, and comparison with B0. Individual admissions do not justify aggregate complexity.

If an unresolved semantic, professional-validity, or pack-intent question can change one exact ledger decision and stronger current evidence cannot decide it, return one Conditional Research Interlude admission containing the exact question, affected row or mechanism, evidence boundary, source lanes, finite stop, output path, and consequence of no answer. Do not browse, reopen remote repositories, contact people, run behavioral evaluations, or edit files in this prompt. Behavioral uncertainty without exact candidate bytes is not a source-research admission.

When evidence is sufficient but material user-owned design choices remain, use $grill-with-docs one question at a time. Recommend one answer and state the decisive tradeoff. Use domain context `render only` and ADR action `offer only`; do not edit. Acceptance of one answer confirms only that decision.

After the frontier closes, run an internal packet-integrity gate. Require every viability-floor behavior to have one exact B0 expression and owner; every C1 delta to be absent from B0 and have one admission basis and proof lane; every substitution or cut to be separated from mechanism contribution; every prior evidence item to have one reuse disposition; every affected relationship to have one owner; every gap to preserve its consequence; and the campaign shape to agree with the current/B0/C1 identity. When this gate passes and no material user-owned choice remains, mark the packet confirmed and return it without asking for ceremonial confirmation.

Inspect any existing synthesis, candidate, and evidence hashes against this model. Recommend the earliest unmet unit. A later prompt may be recommended only when its durable prerequisites are exact and uncontested.

Return the viability floor, source registry and freshness limits, selected baseline, current-runtime disposition ledger, research disposition ledger, prior-evidence disposition ledger, unified baseline-delta ledger, B0 specification, C1 delta set, protected behavior set, campaign shape, affected owners and relationships, claim-to-proof outline, rejected and deferred mechanisms, residual gaps, packet-integrity result, and one decision: `ready-for-prompt-2`, `ready-for-prompt-3`, `ready-for-prompt-4`, `ready-for-prompt-5`, `research-gap`, `runtime-no-change`, `evidence-gap`, or `blocked`.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Conditional Research Interlude

Run only when Prompt 1 returns `research-gap` with a complete admission packet.

```text
Perform only the Conditional Research Interlude for the named skill and the exact Prompt 1 admission packet. Never edit synthesis or runtime and never start Deploy Prompt 1 afterward.

Use `docs/synthesis/methods/source-distillation-flow.md` and its applicable prompts to answer exactly the admitted source question. Preserve source meaning before application, claim labels, access depth, freshness, counterpressure, limitations, contradictions, rejected lanes, and the finite stop. Use only the authorized output path.

Do not expand into adjacent research, skill design, candidate wording, behavioral evaluation, synthesis edits, runtime edits, installation, or delivery. Return exactly `source-packet-complete`, `evidence-gap`, or `blocked` for the bounded question.

Recommend Deploy Prompt 1 only when the returned packet can now change the admitted ledger decision. Otherwise recommend `none` and name the unresolved condition.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
Research admission: CHANGE_ME
```

## Deploy Prompt 2: Finalize Decision-Complete Synthesis

Creates or reconciles the selected skill's synthesis in place.

```text
Perform only Deploy Prompt 2 for the named skill. Never edit runtime skills, create an experimental candidate, run behavioral evaluations, install, or start the recommended successor.

Use $writing-great-skills in Author mode. Require a Prompt 1 packet whose internal packet-integrity gate passed and every admitted source packet. Do not require a separate user confirmation unless Prompt 1 preserved a material user-owned decision. Create the named whole-skill synthesis if none exists; otherwise reconcile it in place. Preserve decision-changing provenance, material alternatives, rejection reasons, ownership, and evidence limits. Collapse superseded or duplicate representations and do not rewrite historical evidence as current authority.

Make these decisions discoverable without requiring exact headings:

- status, outcome, and viability floor;
- campaign shape and current/B0/C1 identity;
- verified evidence registry and freshness limits;
- prior-evidence dispositions and their exact proof lanes;
- exact simplest-baseline comparison;
- current-runtime behavior dispositions and protected behavior set;
- research intake with original claim labels and local dispositions;
- executable B0 semantic surface;
- admitted C1 deltas, admission bases, owners, cheapest expressions, and destinations;
- common-path, disclosed, caller-owned, non-runtime, rejected, and deferred behavior;
- invocation, relationship, mutation, Return, and completion ownership;
- runtime and affected-surface extraction map;
- claim-to-proof matrix separating semantic fidelity, mechanism contribution, invocation and context loading, current-contract preservation, pruning equivalence, and deterministic proof;
- candidate lifecycle state and residual gaps.

Keep source facts separate from synthesis and inference. Research can correct language or propose a mechanism; it does not decide local adoption. Keep evaluation procedure, installer procedure, worker topology, and Git delivery in their shared owners rather than copying them into the synthesis.

Make the synthesis decision-complete, not campaign-transcript-complete. Keep raw outputs, per-sample chronology, repeated hash progressions, and operational run logs in validation. Retain only the provenance, alternatives, dispositions, identities, proof pointers, and gaps that can change a future decision. Reconcile one active design instead of appending a new architecture beside superseded proposals.

Dry-read the finished synthesis as Prompt 3 input. Block readiness unless every distinct current behavior and applicable research item has one disposition; every prior evidence item has one reuse disposition; every C1 addition has an admission basis, owner, cheapest expression, destination, entry condition, failure Return, and proof; substitutions and cuts remain outside mechanism contribution; B0 is implementable without invention; the protected behavior set is explicit; every foreign behavior points to its owner; competing prose is reconciled; the campaign shape agrees with the current/B0/C1 identity; and the aggregate design remains the minimum coherent runtime under the accepted contract.

If exact existing candidate and evidence artifacts already satisfy the revised synthesis, preserve their hashes and recommend the earliest applicable later prompt. Do not manufacture historical B0 or behavioral proof for a campaign that did not create it; record minimality or contribution as untested instead.

If current = B0 = C1, return `runtime-no-change` even when the synthesis changed. If current != B0 = C1, return `ready-for-prompt-3` for a pruning-only campaign. If B0 != C1, return `ready-for-prompt-3` for a behavioral-candidate campaign. An exact later artifact may justify the corresponding later prompt only when every earlier durable gate is already proved.

Return `ready-for-prompt-3`, `ready-for-prompt-4`, `ready-for-prompt-5`, `runtime-no-change`, `evidence-gap`, or `blocked`, plus the campaign shape, final B0/C1 decision, prior-evidence dispositions, and every preserved residual.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 3: Build B0 And C1

Builds the executable minimum control and experimental candidate.

```text
Perform only Deploy Prompt 3 for the named skill. Never run behavioral evaluation, promote, install, deliver through Git, or start the recommended successor.

Use $writing-great-skills in Author mode. Require a synthesis that passed Prompt 2 readiness. For a new unscaffolded skill, use the bundled $skill-creator only for package structure and metadata mechanics; semantic authoring remains here.

Inventory the complete current canonical package, the selected upstream baseline, and every owned or disclosed surface the synthesis assigns to B0 or C1, including `SKILL.md`, metadata, references, scripts, templates, assets, and machine-consumed schemas. Preserve unrelated work.

Construct B0 first. It must be runnable, locally compatible, and behavior-complete for the viability floor. Include only the selected baseline core, mandatory local caller/platform/safety contracts, and source-correct semantic substitutions that add no behavioral-improvement claim; reflect any explicitly classified cut relative to the current or pre-prune package. Do not leak C1 wording, mechanisms, expected failures, or evaluator conclusions into B0. Freeze its exact package bytes or an equivalent reproducible immutable fixture, hash, source provenance, local adaptation delta, and known limitations.

Construct C1 from the exact B0 plus only the synthesis-admitted behavioral additions. Preserve the protected behavior set. Keep common-path behavior inline; disclose irreducible branch-only reference behind a context pointer that names the trigger; point to caller-owned and foreign procedure instead of copying it. Do not add a mechanism and hope Prompt 4 later removes it.

When B0 = C1, store one immutable package corpus and let both roles reference its one hash; do not create duplicate B0 and C1 package trees. Keep the behavior-complete pre-prune package distinct only when a material cut requires an equivalence control. When B0 != C1, record the exact transformation from B0 to C1 and keep behavioral additions separate from substitutions and cuts.

Classify every instruction-bearing paragraph, list item, table row, schema field, and distinct clause in C1 as `B0`, `admitted addition`, `minimum context or pointer`, `collapse`, `disclose`, or `delete`. Apply the cut test only after behavior coverage is complete. When material pruning is claimed, freeze one behavior-complete pre-prune package for later pruning-equivalence proof.

Write one candidate-owned validation record containing the campaign shape, B0 and C1 hashes, package inventories, baseline adaptation delta, current-runtime disposition ledger, research disposition ledger, prior-evidence disposition ledger, unified mechanism ledger, protected behavior set, pruning ledger, affected relationships, claim-to-proof matrix, and residual unavoidable load. Store each raw corpus or immutable fixture once and reference it.

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

Use $writing-great-skills in Author mode. Verify the complete B0 and C1 packages, hashes, inventories, synthesis decisions, protected behavior set, baseline delta, mechanism ledger, and existing evidence. Refresh a source or control only when its identity, contract, or configuration drifted.

Audit scope minimality before repairing omissions. Challenge each C1 addition against its admission basis, owner, cheaper expression, destination, branch load, and aggregate cost. Remove unadmitted machinery and move caller-owned or branch-only behavior to its owner or disclosed surface. If this would reverse a confirmed material design decision rather than enforce its admission record, stop and return the exact Prompt 2 decision frontier.

Repair only genuine omissions relative to B0, admitted C1 deltas, and the protected behavior set. Every repair creates new C1 bytes and invalidates only behaviorally affected candidate evidence.

Build one claim-to-proof matrix with separate lanes:

1. **Semantic fidelity:** compare exact wording with its inspected research source and claim label. This can justify a semantic substitution but not an efficacy claim.
2. **Mechanism contribution:** compare B0 with C1 for each claimed behavioral improvement. Run and judge the B0 control first; do not run a C1 arm when B0 does not exhibit the claimed failure. Remove, demote, or reclassify rejected guidance.
3. **Current-contract preservation:** prove the protected behavior set through deterministic checks, relationship traces, and the smallest representative behavioral cases. Compare current canonical behavior directly only when preservation cannot be established more cheaply.
4. **Pruning equivalence:** compare the admitted behavior-complete pre-prune package with final C1 only for material pruning claims. Reject a cut that regresses admitted behavior.
5. **Term contribution, when decision-relevant:** compare plain `observable action + gate` with `term + identical action + gate`. Prefer plain mechanics when the term earns no demonstrated behavioral, invocation, context, or maintenance benefit.
6. **Invocation and context loading, when affected:** test should-invoke, should-not-invoke, explicit reach, false-positive competition, required body loading, and branch-pointer retrieval against the exact metadata and package state. Use a metadata-only comparison when only routing metadata can change behavior.

Use read-back and deterministic checks for exact bytes and machine contracts, relationship traces for ownership, and the current `BEHAVIOR-EVALS.md` contract for behavioral claims. Test positive, failure-revealing, and wrong-condition pressure only to the breadth claimed. A required caller contract or non-intuitive safety boundary may be admitted through contract-matched deterministic or relationship proof; do not invent a red behavioral claim merely to justify it.

Pruning equivalence is a non-regression lane, not mechanism contribution. Its pre-prune control need not fail, so `reject-no-control-failure` does not apply to that lane. Accept a cut only when the exact final package preserves the admitted behavior under the registered cases. Treat description shortening as pruning plus invocation/context-loading proof, not as a behavioral mechanism.

Before dispatch, minimize cost without weakening evidence. Deduplicate cases only when fixed inputs and one root-held rubric genuinely exercise multiple claims. Keep expected behavior, candidate wording, peer outputs, and conclusions out of neutral worker contexts. Apply the registered prior-evidence dispositions rather than treating all earlier results as reusable. Reuse an arm only when bytes, task, protocol, configuration, tools, authority, evidence, runtime, and proof lane remain identical and uncontaminated. After a repair, preserve unchanged controls and rerun only affected candidate arms.

Inspect every result. Record per-sample outcomes, variance, worst result, critical failures, deviations, unavailable telemetry, process cost when decision-relevant, raw-artifact pointers, and residual gaps. A screening result supports only its tested tasks, model, harness, and claim.

Reperform the complete cut test after accepted repairs. Every retained C1 unit must be B0-essential, locally required, source-correcting at equal or lower load, behaviorally demonstrated, safety-critical, or the minimum context/pointer needed to execute one. Word count is diagnostic, not proof.

Refresh the synthesis and candidate-owned validation surfaces with the exact learned decisions and final evidence dispositions. Record the accepted relationship delta without publishing it into the current relationship index before Prompt 5. Keep raw evaluation and campaign ledgers in validation; do not copy evaluation procedure into synthesis.

Return `accepted`, `reject-no-control-failure`, `reject-regression`, `needs-more-evidence`, or `blocked`. Only `accepted` recommends Deploy Prompt 5 and names the exact final C1 hash.

Use the Shared Run Contract and stop.

Skill name: CHANGE_ME
```

## Deploy Prompt 5: Promote And Install

Promotes only the accepted exact candidate, then performs the separately owned
installation phase.

```text
Perform only Deploy Prompt 5 for the named skill. Never perform Git delivery or start another skill.

Require the accepted Prompt 4 record, exact final C1 hash, complete candidate package, and unchanged affected behavioral claims. If candidate bytes or a tested claim changed, stop and recommend Deploy Prompt 4 without promoting.

First use $writing-great-skills in Author mode to promote the accepted candidate into the canonical skill and update only directly affected canonical proof, relationship, and synthesis surfaces. Reuse accepted behavioral evidence when bytes, tasks, claims, and evidence contracts are unchanged; do not rerun a wave solely because the lifecycle stage changed. Read back the complete canonical package and run proportionate canonical proof. Writing Great Skills stops after that proof.

Reconcile the active synthesis to the promoted state: record the canonical identity, final runtime and relationship surface, admitted and rejected mechanism or cut decisions, exact proof pointers, deliberate non-changes, and residual gaps. Remove duplicated future-tense construction instructions, superseded candidate representations, and raw campaign chronology from the active design. Preserve decision-changing history concisely; validation remains the owner of raw outputs and chronological run evidence.

Only after canonical proof passes, complete the separately owned experimental and installation lifecycle authorized by this prompt: remove only the promoted skill's entire experimental directory and manifest entry; preserve every other candidate; run the managed installation dry-run; require the proposed changed cohort to match the authorized scope; synchronize through the supported installer; and verify canonical-to-installed parity and a clean post-install dry-run. Never edit the installed mirror as canonical source.

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
