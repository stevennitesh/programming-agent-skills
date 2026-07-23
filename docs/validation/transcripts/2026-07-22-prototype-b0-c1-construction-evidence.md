# Prototype B0 And C1 Construction Evidence

Date: 2026-07-22

## Authority And Decision

This record executes Deploy Prompt 3 for Prototype under
`$writing-great-skills` Author authority. It owns the baseline-first
construction trace, exact package identities, deterministic structural proof,
and Prompt 4 handoff. It does not claim behavioral contribution, promote,
install, deliver through Git, or change an active relationship.

Decision: `ready-for-prompt-4`.

- Executable B0 is frozen independently at
  [`docs/validation/evals/prototype-b0/`](../evals/prototype-b0/) with tree hash
  `c1a79fa3a144e1cac39be80233e1a3a2756c2f5130af14d3bc20c53418c6d307`.
- Exact C1 remains the inactive package at
  [`skills/experimental/prototype/`](../../../skills/experimental/prototype/)
  with tree hash
  `4d9ca65a05d5b174b8eefbbc9396f00020ce267932b628415004575e03ff329d`.
  Its bytes already satisfy the revised C1, so no reconciliation or evidence
  invalidation was required.
- The behavior-complete longer-description C1 is frozen at
  [`docs/validation/evals/prototype-description-pre-prune/`](../evals/prototype-description-pre-prune/)
  with tree hash
  `efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.
  It differs from exact C1 only in the description line.
- The active canonical runtime, installed mirror, experimental manifest,
  callers, and relationship index are unchanged.

## Exact Package Inventories

### Selected canonical baseline

Tree hash:
`ecba1e84f0e0df9a0b32b2febdac4e1d7f096dcbf468f9c054c0d5bf7d95a3ef`.

| Relative path | SHA-256 |
| --- | --- |
| `SKILL.md` | `0d83e14ec61eeceacc410344d499de8743b2c86abd58997614d5b43e3a9f5959` |
| `LOGIC.md` | `cfc412fc28767309db7d36ae9651686653d12a9e500383d5b661c54b550f090a` |
| `UI.md` | `e785564cb4c7821e3ee875d225e10292ad44c03d481235ef45d62a9d5b4edb0b` |
| `agents/openai.yaml` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` |

### Frozen executable B0

Tree hash:
`c1a79fa3a144e1cac39be80233e1a3a2756c2f5130af14d3bc20c53418c6d307`.

| Relative path | SHA-256 |
| --- | --- |
| `SKILL.md` | `408b307aa8e63f30538322cd39fbf28403d11ca329191fcadc5e7188ddc40ba3` |
| `LOGIC.md` | `cfc412fc28767309db7d36ae9651686653d12a9e500383d5b661c54b550f090a` |
| `UI.md` | `e785564cb4c7821e3ee875d225e10292ad44c03d481235ef45d62a9d5b4edb0b` |
| `agents/openai.yaml` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` |

### Exact C1

Tree hash:
`4d9ca65a05d5b174b8eefbbc9396f00020ce267932b628415004575e03ff329d`.

| Relative path | SHA-256 |
| --- | --- |
| `SKILL.md` | `1fe5428af0134c6c5ead892ac45406ba97f6879677d220916e410eb261c1b983` |
| `LOGIC.md` | `561d27d37caeef82a4b8663186818a0dba5f4942c7ff45ebf31bf3fb176efd0a` |
| `UI.md` | `7a05360e662c2cc7c49e507d0e7024b80e0e1e1f4f2127cf6281671195c79f25` |
| `MEASURE.md` | `3fde86a4b2c8d2ccd730b1367fb11d0e166bc3de79ee78f12067b6fc7e10d5eb` |
| `RESUME.md` | `e9abad7540ab2bf4eae4d1c295978f19801cfaf446a99aeff2603519deb5ccc6` |
| `agents/openai.yaml` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` |

### Frozen description pre-prune C1

Tree hash:
`efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.

Every file hash equals exact C1 except `SKILL.md`, whose hash is
`e48ae8f59028170eb8d827d04ed316726c4e1618c2d6b8da862b493e4c5f06a3`.
A byte comparison confirms that replacing only line 3's longer description
with C1 line 3 produces exact C1. Description shortening is therefore an
independently testable pruning-equivalence transformation, not a C1 mechanism.

No package has scripts, templates, assets, or another machine-consumed schema.

## Baseline Provenance And B0 Adaptation Delta

The current canonical package is the selected baseline. B0 was constructed
from that baseline before candidate comparison. `LOGIC.md`, `UI.md`, and
`agents/openai.yaml` remain byte-identical to canonical. Only `SKILL.md`
changes, and only for mandatory local viability-floor adaptations:

| Canonical state | B0 adaptation | C1 mechanics excluded |
| --- | --- | --- |
| Assumed locked question | Mutation-free one-question Fit followed by one flat Freeze | Four-predicate Admit and fit/readiness split |
| Lock list omits receiver, recipe/bound, and limits | Add minimum decider, receiver, verdict basis, authority, recipe/bound, and limitation facts | Five named locks and role matrix |
| Logic/UI branch selection | Preserve both canonical disclosed surfaces | Measure and exactly-one-contract Load |
| Smoke and human/objective judgment | Preserve runnable-versus-answer distinction and truthful unavailable-human result | Three named proof levels and claim/mode matrix |
| File-oriented cleanup | Add Prototype-created live-resource stop, conflict-safe restoration, and verified minimum pending artifact | Exhaustive inventory and four named dispositions |
| Three named statuses plus common field list | Use semantic truthful outcomes with applicable facts only | Four exact statuses, shared envelope, status-owned deltas, identity read-back, and sole verdict |
| Recommends `$handoff` and `$domain-modeling` | Remove both outbound recommendations and return candidate context directly | No replacement route or downstream execution |
| Direct caller Return | Preserve and extend to every terminal result and direct-user work | No C1-only packet mechanics |

B0's known limitations are deliberate: no Measure branch, four-predicate
Admit, five-lock Freeze, role matrix, three-level proof taxonomy, exact packet
schema, exhaustive four-disposition accounting, or Resume procedure. Those
limitations are the exact contribution surface for Prompt 4.

## C1 Clause-By-Clause Derivation

The following ledger classifies every instruction-bearing C1 unit. `B0` means
the semantic clause is preserved from exact B0. `Admitted addition` means one
of the confirmed eight C1 mechanisms. `Minimum context or pointer` is required
to make an owner or disclosed branch reachable. `Collapse` is a
behavior-preserving compression. `Disclose` is an admitted branch-only
contract. No instruction-bearing C1 unit is unclassified.

### `SKILL.md`

| C1 lines or clause | Classification | Derivation from B0 |
| --- | --- | --- |
| 2 name | `Minimum context or pointer` | Package identity |
| 3 description | `Collapse` | Shortens the frozen pre-prune description; not a mechanism |
| 8 Outcome | `B0` | B0 outcome |
| 10 Prototype/caller ownership clauses | `B0` | B0 Ownership |
| 12 invocation root, scratch path, app-tree authority and isolation | `B0` | B0 Write boundary |
| 12 unique-sibling and disposition clauses | `Admitted addition` | Exhaustive artifact accounting |
| 14 continuous file/non-file inventory | `Admitted addition` | Exhaustive artifact accounting |
| 14 protected production and repository-state list | `Collapse` | B0 unrelated-state protection |
| 17 leading-word spine | `Minimum context or pointer` | Coordinates the derived C1 operations |
| 22-27 four admission predicates | `Admitted addition` | Replaces B0 simple Fit |
| 29 exact fit/readiness Return split | `Admitted addition` | Four-predicate Admit and exact packet statuses |
| 33 five-lock completeness rule | `Admitted addition` | Replaces B0 flat Freeze |
| 35 role identities, separation, custody, missing-owner block | `Admitted addition` | Claim/mode/role matrix |
| 36 B0 question, decision, surface, basis, and representatives | `B0` | B0 Freeze facts |
| 36 claim-level, mode, rule, and branch fields | `Admitted addition` | Role matrix and exactly-one Load |
| 37 B0 paths and effects | `B0` | B0 Freeze facts |
| 37 artifact dispositions | `Admitted addition` | Four dispositions |
| 38 entry point/recipe and finite bound | `B0` | B0 Freeze facts |
| 39 limitations | `B0` | B0 Freeze facts |
| 41 proportionality and material-question gate | `Collapse` | B0 proportional Freeze |
| 41 caller threshold and no-post-hoc-tuning clauses | `Admitted addition` | Claim/mode/role authority |
| 43 fresh Admit/Freeze trigger | `Admitted addition` | Five-lock identity |
| 47 exactly-one decision-bearing branch | `Admitted addition` | Replaces B0 one evidence surface |
| 51 Logic pointer | `B0` and `Minimum context or pointer` | B0 Logic surface |
| 52 UI pointer | `B0` and `Minimum context or pointer` | B0 UI surface |
| 53 Measure pointer | `Admitted addition` and `Disclose` | Measure mechanism |
| 55 tool and two-branch guards | `Admitted addition` | Exactly-one-contract Load |
| 59 Probe | `B0` | B0 Probe |
| 63 command, surface, state, assumptions | `B0` | B0 Smoke record |
| 65 Smoke/verdict/production separation | `Admitted addition` | Three proof levels |
| 69 representative discrimination | `B0` | B0 Judge |
| 73-76 claim/mode matrix | `Admitted addition` | Claim/mode/role matrix |
| 78 unavailable-human and nondiscrimination outcomes | `B0` | B0 truthful residual semantics |
| 78 exact statuses, evidence fields, and sole-verdict shapes | `Admitted addition` | Four status-owned packets |
| 80 production-proof ownership | `B0` and `Admitted addition` | B0 boundary sharpened as three proof levels |
| 84 exhaustive side-effect inventory and one disposition | `Admitted addition` | Exhaustive artifact accounting |
| 86 delete | `B0` and `Admitted addition` | B0 delete, made an exact disposition |
| 87 restore | `B0` and `Admitted addition` | B0 restore, made an exact disposition |
| 88 preserve-for-verdict | `B0` and `Admitted addition` | B0 pending minimum plus custody disposition |
| 89 authorized-durable-evidence | `B0` and `Admitted addition` | B0 durable path plus exact disposition |
| 91 resource stop, safe restoration, verified paths | `B0` | B0 Reconcile |
| 91 stale-pointer, answered-state, no-live-resource, blocked-conflict clauses | `Admitted addition` | Exhaustive accounting and packet truth |
| 95 current-invocation identity read-back | `Admitted addition` | Four packet mechanism |
| 97-105 shared envelope | `Admitted addition` | Four packet mechanism |
| 108 exactly-one status delta | `Admitted addition` | Four packet mechanism |
| 110-113 four status-owned deltas | `Admitted addition` | Four packet mechanism |
| 115 status predicates, sole result, no padding | `Admitted addition` | Four packet mechanism |
| 117 direct caller/user Return and stop | `B0` | B0 direct leaf exit |
| 117 no downstream selection/invocation | `B0` | B0 removal of outbound recommendations |
| 121 Resume pointer and root ownership | `Admitted addition` and `Disclose` | Awaiting-only Resume |
| 125 baseline completion semantics | `B0` | B0 Completion |
| 125 five-lock, branch, packet, and no-live-resource precision | `Admitted addition` | Derived C1 completion |

### Disclosed branches and metadata

| File and instruction unit | Classification | Derivation |
| --- | --- | --- |
| `LOGIC.md` opener and Return pointer | `Minimum context or pointer` | Names root and branch ownership |
| `LOGIC.md` Model | `B0` and `Collapse` | Canonical B0 model in compact form |
| `LOGIC.md` interactive and deterministic Driver | `B0` and `Collapse` | Canonical B0 surfaces |
| `LOGIC.md` representative-case and integration clauses | `Admitted addition` | Five-lock representatives and branch precision |
| `LOGIC.md` Smoke basics | `B0` | Canonical B0 branch Smoke |
| `LOGIC.md` explicit evidence boundary and Measure exclusion | `Admitted addition` | Three proof levels and exactly-one Load |
| `UI.md` opener and Return pointer | `Minimum context or pointer` | Names root and branch ownership |
| `UI.md` real-context Host and structural Bets | `B0` and `Collapse` | Canonical B0 UI core |
| `UI.md` exact-path and positive-isolation clauses | `B0` | B0 authorized app-tree boundary |
| `UI.md` stable keys, URLs, switch, browser inspection | `B0` and `Collapse` | Canonical B0 judgeability |
| `UI.md` explicit evidence boundary | `Admitted addition` | Three proof levels |
| `MEASURE.md` all Fit, contract, Observe, Smoke, evidence, and Return units | `Admitted addition` and `Disclose` | Measure and exactly-one Load |
| `RESUME.md` all admission, rejection, identity, custody, drift, restart, Smoke, and re-entry units | `Admitted addition` and `Disclose` | Awaiting-only Resume |
| `agents/openai.yaml` implicit policy | `B0` | Preserved platform contract |

The earlier complete per-line pruning ledger remains historical evidence for
the old Prompt 3/4 campaign. This ledger supersedes its B0/C1 interpretation;
the earlier raw evaluation corpus is not duplicated.

## Current-Runtime Disposition

| Current runtime behavior | Disposition in B0/C1 |
| --- | --- |
| One-question probe, implicit reach, caller ownership, paths, Logic/UI, smallest probe, Smoke, human/objective judgment | Protect in B0 and C1 |
| Current Lock presentation | Replace with flat B0 Freeze; replace again only through admitted five-lock C1 |
| Current status list and common verdict-field list | Replace with B0 semantic truth; formalize only in C1 packets |
| Current cleanup/preservation | Strengthen minimally in B0; make exhaustive only in C1 |
| Handoff recommendation | Remove in B0 and C1 |
| Domain Modeling recommendation | Remove in B0 and C1 |
| Direct caller Return | Protect and extend in B0 and C1 |
| Current completion | Replace with exact B0 completion; derive C1 precision from admitted mechanisms |

## Research Disposition

| Research pressure | Disposition |
| --- | --- |
| Matt Pocock one question, runnable surface, command, visible state, structural variants | Supporting rationale for B0 core |
| Prototype as default primary source | Reject; conflicts with local reconciliation |
| Question-driven prototype language | Supporting rationale only |
| No-op and pruning pressure | Prompt 4/pruning rationale only |
| Superpowers design ceremony | Reject as a broader workflow |
| Ponytail simplicity pressure | Supporting rationale only |
| Historical books and websites | Defer; not load-bearing |

No semantic uncertainty changes B0 or C1, so no research interlude is required.

## Unified C1 Mechanism Ledger

| Mechanism | B0 state | Exact C1 addition | Admission basis | Runtime owner | Prompt 4 proof |
| --- | --- | --- | --- | --- | --- |
| Admit | Simple one-question Fit | Four predicates and fit/readiness split | Observed baseline failure | `SKILL.md` | B0-first mismatch/readiness cases |
| Freeze | Flat facts | Five grouped locks and completeness | Observed failure; safety/authority | `SKILL.md` | B0 omission then C1 complete/partial cases |
| Load/Measure | Logic or UI surface | Measure plus exactly one decision-bearing contract | Observed failure; local contract | `SKILL.md`, `MEASURE.md` | B0 Measure failure; three positives and wrong-branch negatives |
| Claim/mode/roles | Generic decider, receiver, basis | Claim, mode, decision owner, judge, return owner, custody | Observed failure; safety/authority | `SKILL.md` | Role inference and wrong-pairing controls |
| Proof levels | Runnable versus answer and production non-claim | Explicit Smoke, verdict evidence, production proof | Local contract; safety | Root and branches | Green-Smoke false-answer and overclaim cases |
| Packets | Semantic truthful outcomes | Four statuses, envelope, one delta/predicate, identity read-back, sole verdict | Observed failure; safety/authority | `SKILL.md` | Padding, stale identity, duplicate result, false answer |
| Artifact accounting | Minimum safe cleanup | Continuous inventory and four exact dispositions | Observed failure; safety | `SKILL.md` | Process/path/dirty-work cases |
| Resume | Pending-human preservation | Awaiting-only fresh Resume with custody/drift/restart/Smoke | Observed failure; safety | `RESUME.md` | Awaiting, blocked, drift, custody cases |

The description shortening is absent from this ledger because it is
pruning-equivalence, not behavior-changing C1.

## Protected Behavior Set

C1 preserves: one question and decision; disposable probe and durable result;
narrow implicit invocation; caller-owned adoption, routing, implementation,
and production proof; Logic and UI judgeability; human-reserved judgment and
caller-locked objective criteria; Smoke before verdict; authorized paths and
unrelated work; cleanup before Return; truthful residuals; direct current
caller or user Return; and no Prototype recommendation or invocation of
Handoff, Domain Modeling, Router, or another downstream route.

## Relationship Record

No active relationship file changed. The proposed promotion-time delta is:

- remove Prototype's outbound recommendation edge to Handoff;
- remove Prototype's outbound recommendation edge to Domain Modeling;
- preserve every inbound caller edge and direct caller Return;
- add no replacement router or automatic successor edge.

Callers, Wayfinder packet fields, and the active relationship index remain
read-only until one atomic promotion.

## Evidence Scope And Claim-To-Proof Matrix

| Claim lane | Evidence valid now | Prompt 4 obligation |
| --- | --- | --- |
| Exact identity | Frozen tree and file hashes plus structural tests | Read back before evaluation |
| Semantic fidelity | Canonical provenance and no load-bearing research substitution | Preserve labels |
| Mechanism contribution | None for exact B0/C1 | Run B0 first per claimed mechanism; skip C1 when B0 does not fail |
| Historical admission | Canonical versus aggregate candidate `1/25` versus `25/25` | Use only as aggregate problem-family evidence |
| Current-contract preservation | Structural anchors and relationship trace | Prove protected behavior against exact packages |
| Body pruning | Prior pre-prune/final `35/35` for its exact historical bytes | Reuse only where bytes, task, rubric, and claim still match |
| Description pruning | Exact old/short packages and prior `45/45` protocol | Independently compare the two frozen variants |
| Invocation/context | Metadata simulation only | Prove host discovery and branch retrieval |
| Live behavior | Not proved | Exercise Logic, UI, Measure, cleanup, Resume, and callers |

The historical `1/25` versus `25/25` result is not an exact B0 contribution
control and cannot establish any individual mechanism's effect.

## Deterministic Structural Record

The candidate-specific test now fixes:

- all three tree hashes;
- exact B0 and pre-prune inventories;
- B0 minimum Freeze, truthful Return, reconciliation, and direct leaf exit;
- absence of C1-only Admit, five-lock, Measure, packet, four-disposition, and
  Resume anchors from B0;
- absence of `$handoff` and `$domain-modeling` recommendations from B0 and C1;
- byte identity of every pre-prune/C1 file except `SKILL.md`; and
- exact one-line description replacement equivalence.

Repository validation records are completed after this document's final
read-back. Their commands and results are appended below without converting
mechanical proof into behavioral proof.

## Residual Unavoidable Load And Prompt 4 Boundary

C1's remaining universal load is the admission gate, five-lock Freeze,
authority and side-effect boundary, selected-branch pointer table, proof-level
separation, claim/mode matrix, exhaustive reconciliation, status packets,
direct Return, and completion. Logic, UI, Measure, and Resume details remain
disclosed. Rationale, evaluation procedure, installer work, Git delivery, and
relationship mutation remain outside runtime.

Prompt 4 must independently prove mechanism contribution from exact B0,
current-contract preservation, pruning equivalence, invocation/context
loading, and live branch behavior. Prompt 3 stops here.

## Validation Results

- `python -m pytest tests/test_experimental_skill_contracts.py -q`:
  `10 passed`.
- `python -m scripts.validate_skills`: passed.
- `python -m scripts.pytest_focused`: `59 passed`.
- `python -m pytest`: `193 passed, 4 skipped`.
- `git diff --check`: passed before final record read-back.
- Final tree-hash, inventory, description-only diff, relationship non-change,
  and whitespace checks are recorded in the handoff read-back.
