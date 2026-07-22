# Domain Modeling Prompt 3 Extraction And Pruning Evidence

Date: 2026-07-21

Status: experimental extraction complete; behavioral evaluation not run.

## Identity And Authority

- Operation: `$writing-great-skills` Author, Deploy Prompt 3.
- Normative source: `docs/synthesis/skills/domain-modeling.md` after confirmed Deploy Prompts 1 and 2.
- Simplest credible baseline: Matt Pocock `domain-modeling` at `ed37663cc5fbef691ddfecd080dff42f7e7e350d`.
- Baseline package tree hash: `ce2eb764d4d47a9bf39e54832a32ac11761cfb25cb523a5560f7474dd3dda430`.
- Active local package tree hash: `599a98910c7b392d54e595331d114ec4e101dffe251d277ed5067b308602e045`.
- Extracted candidate tree hash: `a52648ce0f314980e3ede15214c10800b3b89268f70138b40eee61ae62c1c272`.
- Mutation boundary: experimental package, its manifest entry, directly affected structural proof, and this evidence record only. Canonical and installed skills were not changed.

## Complete Package Inventory

| Surface | Classification | Runtime ownership |
| --- | --- | --- |
| `skills/experimental/domain-modeling/SKILL.md` | affected | invocation, universal authority, common runtime, conditional pointers, Return, completion |
| `skills/experimental/domain-modeling/CONTEXT-FORMAT.md` | affected disclosed reference | routed and fallback domain-record representation; Context Mapping patterns |
| `skills/experimental/domain-modeling/ADR-FORMAT.md` | affected disclosed reference | ADR worthiness, approval, routing fallback, representation, verification |
| `skills/experimental/domain-modeling/agents/openai.yaml` | preserve | implicit invocation policy |
| `skills/experimental/manifest.json` entry | affected machine schema | candidate origin, reason, candidate hash, active baseline hash |
| `tests/test_experimental_skill_contracts.py` Domain Modeling test | affected machine proof | package inventory, policy, required literals, rejected stale contracts |
| Scripts, templates, assets | not applicable | none exist in the package |
| Behavioral evaluation | deferred to Prompt 4 | invocation, judgment, action, context loading, Return, and completion claims |

## Baseline Delta And Classification

| Behavior | Classification | Destination | Admission evidence | Cheaper alternative |
| --- | --- | --- | --- | --- |
| Active modeling rather than vocabulary consumption | Baseline | description and opening | upstream core | none |
| Challenge conflicts and fuzzy language | Baseline | `Challenge` | upstream core | none |
| Concrete boundary scenarios | Baseline | `Challenge` | upstream core | none |
| Cross-check descriptive claims with code | Baseline | `Trace` and `Resolve` | upstream core | none |
| Lazy domain records | Baseline | `Trace`; both references | upstream core | none |
| Sparse ADR gate and record | Baseline | `ADR-FORMAT.md` | upstream core | none |
| Narrow implicit trigger and lookup exclusion | Add | description | passive lookup invocation collision | explicit-only reach |
| Source fact versus intended domain truth | Add | `Authority`, `Trace`, `Resolve` | semantic safety boundary | let implementation usage decide meaning |
| Context-scoped invariants and relationships | Add | `Resolve`, `CONTEXT-FORMAT.md` | glossary-only baseline omits load-bearing model boundaries | glossary-only record |
| Repository routing first; filename fallback | Add | `Trace`; both references | portability across existing repositories | mandate local filenames |
| Direct focused domain questions | Add | `Authority` | core DDD clarification cannot settle participant knowledge unaided | always invoke composer |
| Explicit persist versus render | Add | `Authority`, persistence branch | mutation authority safety | always persist resolved truth |
| Separate ADR approval | Add | `Authority`, `ADR-FORMAT.md` | ADR mutation safety | combine all write grants |
| Four common Domain Delta fields | Add | `Return` | caller needs semantic, persistence, blocker, and owner state | fixed forensic schema |
| Composed questioning owner and cumulative delta | Disclose | `Authority`, conditional Return paragraph | `$grill-with-docs` caller contract | duplicate composer procedure inline |
| Complete Context Mapping vocabulary | Disclose | `CONTEXT-FORMAT.md` | correct DDD representation branch | partial preferred list |
| Universal ADR recorder | Disclose | `ADR-FORMAT.md` | ADR-0006 caller contract | each workflow writes ADRs |
| Multi-target verification failure behavior | Disclose | persistence branch | non-intuitive safety boundary | rollback or best effort |
| Managed setup mutation | Caller-owned | returned setup requirement | `$repo-bootstrap` owns setup | Domain Modeling edits setup |
| Non-domain decision settlement and continuation | Caller-owned | originating workflow | authority boundary | Domain Modeling owns all decisions |
| Baseline hashes, rationale, admission and migration ledgers | Non-runtime | synthesis and this record | evidence only | inline them in runtime |
| Universal `Reconcile` stage | Rejected | none | confirmed simplification | keep seven-word spine |
| Five named Challenge lenses | Rejected | none | three plain checks preserve the behavior | keep invented labels |
| Domain Modeling to Skill Router edge | Rejected | none | adds no domain capability | automatic route suggestion |
| Fixed nine-field Domain Delta | Rejected | none | conditional detail preserves meaning | universal wrapper |
| Mandatory partial relationship taxonomy | Rejected | none | false labels damage the model | four labels plus custom |
| Ontology, automatic extraction or renaming, mandatory event storming | Deferred | none | no demonstrated baseline failure | speculative runtime machinery |

All synthesis behaviors were classified before candidate assembly. No `Deferred` or `Rejected` behavior entered the package.

## Pruning Ledger: `SKILL.md`

Each row covers one instruction-bearing paragraph, list item, schema field, or distinct clause in final semantic order.

| ID | Unit | Action | Behavior preserved or destination |
| --- | --- | --- | --- |
| S01 | Description: model and persist named domain surfaces | Keep | implicit positive trigger |
| S02 | Description: focused clarification, delegated capture, settled ADR assessment | Keep | three observable invocation branches |
| S03 | Description: exclude lookup and general design debate | Keep | nearest competing routes |
| S04 | Opening: coherent model plus complete Domain Delta | Keep | outcome and Return promise |
| S05 | `Model, don't catalog` | Keep | leading instruction |
| S06 | Capture meaning, behavior, invariants, responsibility, relationships | Keep | positive model scope |
| S07 | Omit technical vocabulary, indexes, layout-only boundaries | Keep | scope guard paired with positive target |
| S08 | Lock three independent authorities | Keep | authority separation |
| S09 | Meaning: evidence settles source facts | Keep | descriptive authority |
| S10 | Meaning: domain authority settles intent | Keep | normative authority |
| S11 | Direct use may ask focused domain questions | Keep | direct branch |
| S12 | Composition leaves questions to Grilling | Disclose | composer-only branch |
| S13 | Caller invocation returns unresolved choices | Keep | caller Return ownership |
| S14 | Context: explicit persist, otherwise render | Keep | mutation gate |
| S15 | ADR: offer unless identified settled candidate is approved | Keep | independent ADR gate |
| S16 | Originating workflow owns the decision | Keep | non-domain decision boundary |
| S17 | Mutate routed domain records and approved ADRs only | Keep | mutation scope |
| S18 | Return setup/code/spec/plan/tracker/implementation consequences | Collapse | one clause replaces separate exclusions |
| S19 | Invoke no Router, composer, or downstream work | Keep | leaf safety boundary |
| S20 | Five-stage runtime spine | Keep | common-path sequence |
| S21 | Trace bounded subject | Keep | admission bound |
| S22 | Trace repo instructions and domain routing | Keep | authority source |
| S23 | Trace records, ADRs, evidence, authorities, caller and owner | Collapse | one source-trace clause replaces a catalog |
| S24 | Follow configured repository route | Keep | portability |
| S25 | Existing root map selects multiple contexts | Keep | fallback branch |
| S26 | Root context file is final fallback | Keep | fallback branch |
| S27 | Create first record only for authorized settlement | Keep | lazy creation safety |
| S28 | Implementation artifacts are evidence, not semantic authority | Keep | source/meaning distinction |
| S29 | Contexts follow model/language/responsibility/consistency | Keep | DDD boundary criterion |
| S30 | Contexts do not follow layout or size alone | Keep | non-intuitive guardrail |
| S31 | Return topology and setup requirement when routing must change | Keep | setup owner boundary |
| S32 | Resume only after later setup read-back | Keep | ordering and verification |
| S33 | Challenge language collisions | Keep | first plain check |
| S34 | Challenge model boundaries | Keep | second plain check |
| S35 | Challenge contradictions | Keep | third plain check |
| S36 | Use scenario classes only when model-changing | Collapse | upstream scenario instruction plus economy gate |
| S37 | Resolve collision or return exact blocker and owner | Keep | Challenge completion |
| S38 | Resolve canonical term or decision | Keep | semantic core |
| S39 | Resolve implementation-independent meaning | Keep | DDD model boundary |
| S40 | Resolve context, sources, authority | Collapse | remaining semantic core fields |
| S41 | Add optional semantic details only when material | Keep | conditional load |
| S42 | Preserve intent and expose implementation contradiction | Keep | mismatch handling |
| S43 | Keep unresolved meaning out of records | Keep | persistence safety |
| S44 | Relationship interaction direction | Keep | relationship semantic field |
| S45 | Relationship responsibilities | Keep | relationship semantic field |
| S46 | Relationship contract | Keep | relationship semantic field |
| S47 | Relationship language ownership | Keep | relationship semantic field |
| S48 | Relationship change authority | Keep | relationship semantic field |
| S49 | Apply DDD pattern only when fitting | Keep | false-precision guard |
| S50 | Context-format pointer and condition | Disclose | representation branch |
| S51 | Context reference loads only for render or persistence | Keep | sharp context pointer |
| S52 | ADR reference loads only for plausible settled candidate | Keep | sharp ADR pointer |
| S53 | Persist refreshes routing and targets | Keep | stale-write protection |
| S54 | Persist preflights bounded set | Keep | partial-failure prevention |
| S55 | Persist writes accepted changes only | Keep | bounded mutation |
| S56 | Persist rereads attempted and changed records | Keep | verification |
| S57 | First failure preserves verified changes | Keep | partial-state safety |
| S58 | First failure stops mutation and returns exact state | Keep | safe failure Return |
| S59 | Render returns wording, target, placement, effects without write | Keep | no-write branch output |
| S60 | Return destination and stop | Keep | leaf Return |
| S61 | `Semantic outcome` field | Keep | common Domain Delta field |
| S62 | `Persistence outcome` field | Keep | common Domain Delta field |
| S63 | `Blockers and consequences` field | Keep | common Domain Delta field |
| S64 | `Return owner` field | Keep | common Domain Delta field |
| S65 | Conditional authority detail | Keep | present-only return field |
| S66 | Conditional resolved language | Keep | present-only return field |
| S67 | Conditional boundaries and invariants | Collapse | related present-only domain fields |
| S68 | Conditional relationships | Keep | present-only domain field |
| S69 | Conditional per-target state | Keep | persistence evidence |
| S70 | Conditional caller identifiers | Keep | caller integrity |
| S71 | Conditional ADR outcomes | Keep | branch outcome |
| S72 | Conditional continuation authority | Keep | caller contract |
| S73 | Blocker condition, owner, impact, re-entry | Keep | recoverable failure schema |
| S74 | Minimal no-change result | Keep | common-path economy |
| S75 | Composed pass accepts every settled material answer | Disclose | composer branch |
| S76 | No-durable-consequence answer remains accepted | Keep | no-change composition case |
| S77 | Return cumulative delta and collision before dependency advances | Keep | composition ordering |
| S78 | Domain Modeling does not choose interview materiality or branching | Keep | Grilling ownership |
| S79 | Completion: Trace current | Keep | source freshness |
| S80 | Completion: consequences accounted for | Keep | semantic completeness |
| S81 | Completion: target state exact | Keep | persistence completeness |
| S82 | Completion: ADR candidate outcome | Keep | ADR branch completeness |
| S83 | Completion: mutation boundary | Keep | scope safety |
| S84 | Completion: Domain Delta complete | Keep | output completeness |
| S85 | Completion: Return starts nothing | Keep | terminal boundary |
| S86 | Upstream file-tree diagrams and dialogue examples | Delete | reference exposition; behavior retained in routing and Challenge criteria |
| S87 | Old `Reconcile` step | Delete | behavior absorbed by Resolve, Verify, Return, and composed callback |
| S88 | Old five-lens names | Delete | behavior collapsed into three plain checks |
| S89 | Old Router residual paragraph | Delete | confirmed leaf Return |
| S90 | Old nine-field universal schema | Delete | four common fields plus conditional detail |

## Pruning Ledger: `CONTEXT-FORMAT.md`

| ID | Unit | Action | Behavior preserved or destination |
| --- | --- | --- | --- |
| C01 | Follow routed repository format first | Keep | portability |
| C02 | Use fallbacks only when no format exists | Keep | fallback scope |
| C03 | Records contain settled language, behavior, invariants, responsibilities, relationships | Keep | domain-record scope |
| C04 | Unresolved meaning stays in Domain Delta | Keep | persistence safety |
| C05 | Single-context fallback target | Keep | fallback routing |
| C06 | Context name field | Keep | record identity |
| C07 | Model/responsibility/boundary field | Collapse | three context facts in one preamble |
| C08 | Language heading | Keep | record section |
| C09 | Canonical term field | Keep | ubiquitous language |
| C10 | Meaning/behavior/boundary field | Collapse | one definition contract |
| C11 | Avoided synonym field | Keep | alias control |
| C12 | Invariants heading and rule field | Keep | load-bearing rules |
| C13 | Omit empty invariants section | Keep | lazy representation |
| C14 | Multi-context map target and routing purpose | Keep | fallback map |
| C15 | Context link field | Keep | route identity |
| C16 | Owned model/responsibility field | Keep | context ownership |
| C17 | Relationship heading | Keep | pair identity |
| C18 | Interaction direction field | Keep | directional semantics |
| C19 | Responsibilities field | Keep | ownership semantics |
| C20 | Contract field | Keep | boundary semantics |
| C21 | Language field | Keep | owner/reference/translation semantics |
| C22 | Authority field | Keep | controlling or joint change rule |
| C23 | Optional pattern field | Keep | accurate DDD label |
| C24 | Partnership item | Keep | recognized pattern meaning |
| C25 | Shared Kernel item | Keep | recognized pattern meaning and governance |
| C26 | Customer/Supplier Development item | Keep | recognized pattern meaning |
| C27 | Conformist item | Keep | recognized pattern meaning |
| C28 | Anticorruption Layer item | Keep | recognized pattern meaning |
| C29 | Open-host Service item | Keep | recognized pattern meaning |
| C30 | Published Language item | Keep | recognized pattern meaning |
| C31 | Separate Ways item | Keep | recognized pattern meaning |
| C32 | Big Ball of Mud item | Keep | recognized pattern meaning |
| C33 | Patterns may combine when each is true | Keep | representation accuracy |
| C34 | Translation is a language mapping, not pattern | Keep | corrected prior taxonomy |
| C35 | Omit false Pattern | Keep | false-precision guard |
| C36 | Settled meaning/ownership/conflict/authority only | Keep | representation admission |
| C37 | Implementation-independent model | Keep | DDD boundary |
| C38 | One canonical term and avoided synonyms | Keep | ubiquitous language consistency |
| C39 | Exclude generic language and code indexes | Keep | domain scope |
| C40 | One context owns meaning; consumers reference | Keep | duplication prevention |
| C41 | Translation defines local terms and mapping | Keep | context autonomy |
| C42 | Shared definitions require governed Shared Kernel | Keep | joint ownership safety |
| C43 | Natural subheadings only | Keep | non-ceremonial format |
| C44 | Render target, scope, wording, relationships, ordering | Collapse | complete directly applicable output |
| C45 | Unclear semantic state returns unresolved | Keep | safe failure |
| C46 | Upstream example entities and event lines | Delete | examples do not own behavior |
| C47 | Old four-label preferred taxonomy | Delete | incomplete and falsely privileged |

## Pruning Ledger: `ADR-FORMAT.md`

| ID | Unit | Action | Behavior preserved or destination |
| --- | --- | --- | --- |
| A01 | Domain Modeling records; originating workflow settles | Keep | recorder/decision boundary |
| A02 | Follow repository ADR route first | Keep | portability |
| A03 | Use fallback only without convention | Keep | fallback scope |
| A04 | Hard-to-reverse criterion | Baseline/Keep | worthiness gate |
| A05 | Surprising-without-context criterion | Baseline/Keep | worthiness gate |
| A06 | Real-trade-off criterion | Baseline/Keep | worthiness gate |
| A07 | Ordinary/reversible/unresolved/no-alternative exclusions | Collapse | negative controls in one clause |
| A08 | Explicit approval identifies settled candidate | Keep | ADR mutation gate |
| A09 | Context persistence does not grant ADR approval | Keep | independent authority |
| A10 | Offered/deferred/declined no-write outcomes | Keep | unapproved branch Return |
| A11 | System-wide fallback location | Keep | fallback route |
| A12 | Context-local fallback location | Keep | bounded-context route |
| A13 | Lazy directory creation | Baseline/Keep | non-ceremonial persistence |
| A14 | Highest-number scan and next slug | Baseline/Keep | fallback identity |
| A15 | Ambiguous/concurrent number returns blocker | Keep | overwrite safety |
| A16 | Decision title field | Keep | record identity |
| A17 | Context/pressure/constraints field | Collapse | concise rationale |
| A18 | Decision/choice/why field | Collapse | concise outcome |
| A19 | Optional accepted/deprecated/superseded status | Keep | lifecycle branch |
| A20 | Optional considered options | Keep | rejected-alternative branch |
| A21 | Optional consequences | Keep | downstream-effect branch |
| A22 | Reread each ADR | Keep | verification |
| A23 | Return candidate, authority, path, outcome, read-back | Collapse | complete ADR branch result |
| A24 | Upstream long qualifying-example catalog | Delete | gate already decides; examples add reference load |
| A25 | Upstream `proposed` status | Delete | candidates must already be settled and recording-approved |

## Pruning Ledger: Metadata And Machine Surfaces

| ID | Unit | Action | Behavior preserved or destination |
| --- | --- | --- | --- |
| M01 | `policy.allow_implicit_invocation: true` | Keep | narrow description remains discoverable |
| M02 | Manifest origin | Replace | truthful upstream baseline identity |
| M03 | Manifest reason | Replace | Prompt 4 lifecycle state |
| M04 | Manifest candidate hash | Replace | exact extracted package identity |
| M05 | Manifest active baseline hash | Replace | exact current canonical identity |
| M06 | Structural positive contracts | Replace | new spine, authority, DDD representation, Return |
| M07 | Structural rejected contracts | Add | no Reconcile, five lenses, Router, nine-field schema |
| M08 | Exact package inventory assertion | Add | no undisclosed runtime surface |

## Residual Unavoidable Sprawl

The common `SKILL.md` remains 57 lines and 707 words because three universal authority gates, the safe persistence-failure branch, the caller-composition ordering contract, and exact completion boundaries are behavior-bearing. `CONTEXT-FORMAT.md` remains 77 lines and 426 words because the nine optional recognized Context Mapping patterns must be accurate at the branch that uses them. `ADR-FORMAT.md` is 41 lines and 258 words.

The complete candidate is 95 words larger than the upstream control across the three Markdown files while adding context-scoped invariants, full relationship semantics, repository-first routing, independent mutation authority, partial-state recovery, caller composition, and a typed Return. Word count is diagnostic only; Prompt 4 must still prove that admitted behavior survives pruning and that added wording changes behavior relative to a failing control.

## Mechanical Proof

Read-back covered all four candidate files after mutation. The first focused run exposed one stale structural literal (`already settled` versus `already-settled`); the candidate already held the intended contract, so only the assertion changed. The first full run then exposed stale composer-handshake literals from the replaced candidate; the updated assertions preserve the same cumulative-delta ordering contract without restoring rejected wording.

Final evidence:

```text
python -m pytest tests/test_experimental_skill_contracts.py -k domain_modeling
1 passed

python -m scripts.validate_skills
Skill validation passed.

manifest candidate_sha256
a52648ce0f314980e3ede15214c10800b3b89268f70138b40eee61ae62c1c272

actual candidate tree hash
a52648ce0f314980e3ede15214c10800b3b89268f70138b40eee61ae62c1c272

python -m pytest
191 passed, 4 skipped
```

The exact package-inventory assertion passed. Structural negatives confirm that the candidate omits the old `Reconcile` spine, five named lenses, `$skill-router`, and nine-field Domain Delta. `git diff --check` and `git diff --cached --check` are rerun after this evidence update as the final whitespace proof.

No fresh-context behavioral samples ran. The evidence above proves package shape, required structural contracts, manifest identity, and repository compatibility only; Prompt 4 owns behavioral claims and pruning equivalence.
