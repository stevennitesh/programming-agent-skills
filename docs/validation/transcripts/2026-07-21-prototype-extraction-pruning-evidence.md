# Prototype Experimental Extraction And Pruning Evidence

Date: 2026-07-21

## Authority And Decision

This record executes Deploy Prompt 3 for Prototype and is the evidence owner for
the later Deploy Prompt 4 independent pruning audit. Prompt 3 completed its
provisional candidate at hash
`c82ea333f0f4cb01e57b3814155b51959702e5722ff2e0227040e3bbea2d94b5`.
Prompt 4 repaired that candidate and accepted final inactive hash
`efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.
Canonical, installed, promotion, and Git-delivery surfaces are unchanged.

The repaired pre-prune fixture at
`.tmp/prototype-prune-eval/pre-prune/` reproduces tree hash
`eb6d161906b02c0e8d8a63eabde589bf47d261d46471d52c912a48df281af171`.
It is the behavior-complete control for Deploy Prompt 4. The final candidate
fixture is refreshed only after the independent audit closes.

## Complete Inventory

| Surface | Classification | Prompt 3 disposition |
| --- | --- | --- |
| `skills/experimental/prototype/SKILL.md` | universal runtime owner | Reconcile every selected behavior; Shape and Prune after coverage |
| `skills/experimental/prototype/LOGIC.md` | disclosed Logic branch | Keep; no pruning change |
| `skills/experimental/prototype/UI.md` | disclosed UI branch | Keep; no pruning change |
| `skills/experimental/prototype/MEASURE.md` | disclosed Measure branch | Keep; no pruning change |
| `skills/experimental/prototype/RESUME.md` | disclosed Resume branch | Add as the destination for branch-only Resume procedure |
| `skills/experimental/prototype/agents/openai.yaml` | machine-consumed invocation policy | Keep implicit invocation field |
| Package scripts, templates, assets, additional schemas | absent | No surface to classify |
| `skills/custom/prototype/` | active canonical baseline and behavioral-gap control | Read-only; no promotion |
| installed Prototype mirror | active installed baseline | Read-only; no synchronization |
| `skills/experimental/manifest.json` | inactive candidate hash registry | Refresh candidate hash and truthful acceptance state |
| `tests/test_experimental_skill_contracts.py` | machine-contract proof | Register `RESUME.md` and its protected anchors |
| `docs/synthesis/skills/prototype.md` | exhaustive design and extraction map | Preserve rationale; update runtime ownership and evidence status |
| `docs/synthesis/skill-context-relationships.md` | relationship and context-owner registry | Add Resume ownership only; no edge change |
| `skills/experimental/wayfinder/MAP-FORMAT.md`, `OPERATIONS.md` | directly affected experimental caller fields | Keep; `claim level`, `judgment mode`, decision owner, and human judge already align |
| Grilling, Improve Codebase, TDD, Audit Codebase Prototype seams | canonical caller relationships | Read-only; no relationship or packet delta |
| `docs/validation/evals/core-workflows.md` | pack behavioral scenarios | Read-only; existing Prototype lifecycle rubric remains applicable |
| Prior Prototype evaluation transcripts | historical exact-snapshot evidence | Preserve; do not relabel as evidence for the pruned hash |

## Coverage Ledger

Every selected decision is classified before pruning.

| Decision | Classification | Runtime destination |
| --- | --- | --- |
| P01 one-question leaf and non-mutating admission | `Inline` | `SKILL.md` Outcome and Admit |
| P02 fit versus readiness | `Inline` | `SKILL.md` Admit and Freeze |
| P03 one Logic, UI, or Measure branch | `Inline` and `Disclosed` | `SKILL.md` Load; three branch files |
| P04 claim level and judgment mode | `Inline` | `SKILL.md` Freeze and Judge; Wayfinder fields |
| P05 caller-owned rule and adoption | `Inline` | `SKILL.md` Boundary, Freeze, Judge, and Return |
| P06 invocation root and authorized app-tree exception | `Inline` | `SKILL.md` Authority and Freeze |
| P07 positive production isolation | `Inline` and `Disclosed` | `SKILL.md` Authority; `UI.md` Host and Smoke |
| P08 four artifact dispositions | `Inline` | `SKILL.md` Reconcile |
| P09 four statuses, one delta, one predicate, one verdict | `Inline` | `SKILL.md` Return |
| P10 awaiting-only packet-backed Resume | `Disclosed` | `SKILL.md` pointer; `RESUME.md` procedure; Reconcile and Return stay in root |
| P11 Smoke, verdict evidence, and production proof separation | `Inline` and `Disclosed` | `SKILL.md` Smoke and Judge; branch Smoke sections |
| P12 narrow implicit invocation | `Inline` | frontmatter description and `agents/openai.yaml` |
| P13 behavior-family counterfactual evaluation | `Non-runtime` | this record and post-candidate evaluation |
| P14 staged construction and atomic promotion | `Non-runtime` | synthesis and deploy prompts |
| P15 historical source pressure | `Non-runtime` | synthesis rationale only |
| P16 every non-admission returns locally and stops | `Inline` | `SKILL.md` Return; relationship registry |

Prompt 3 reconciliation found two over-pruned clauses and restored them before
proof: valid `verdict` shapes including `none` and a threshold result, and the
status-specific `failed operation` field for `blocked`. No synthesis behavior,
confirmed decision, guardrail, authority boundary, Return field, or completion
condition remains unclassified.

## Instruction-Unit Pruning Ledger

Line references name the final candidate. `Collapse` means the pre-prune unit is
represented more compactly at the named destination; `Disclose` means it moved
behind a required pointer. Units not listed as `Delete` remain behavior-bearing.

### `SKILL.md`

| Unit | Decision | Behavior or destination |
| --- | --- | --- |
| frontmatter description positive and adjacent-negative clauses | `Keep` | Invocation recall and precision |
| 8 Outcome | `Keep` | One question; disposable probe; durable verdict |
| 10 Boundary clauses | `Collapse` | Prototype and caller ownership |
| 12 Authority root, unique sibling, durable path, and app-tree clauses | `Collapse` | Mutation authority and positive isolation |
| 14 inventory, confinement, and protected-state clauses | `Collapse` | Dirty-work and mutation guardrails |
| 17 eight-step spine | `Keep` | Ordered lifecycle leading words |
| 22 Admit-without-mutation gate | `Keep` | Admission authority |
| 24, 25, 26, 27 four fit predicates | `Keep` | One decision, one question, runnable discrimination, safe reconciliation |
| 29 failed-fit packet and readiness distinction | `Collapse` | Truthful `not-admitted` versus `blocked` |
| 33 five-lock pre-mutation gate | `Collapse` | Freeze completion |
| 35 ownership, role separation, missing-owner clauses | `Collapse` | Decision owner, human judge, custody, blocker |
| 36 question, decision, frame, branch, claim, mode, rule, representative clauses | `Keep` | Evidence lock |
| 37 mutation fields | `Collapse` | Paths, effects, dispositions |
| 38 execution fields | `Collapse` | Entry point or recipe and finite bound |
| 39 limits fields | `Collapse` | Evidence limits and extrapolations |
| 41 proportional defaults, ask gate, caller thresholds, no post-hoc tuning | `Collapse` | Caller authority and bounded legwork |
| 43 changed-Freeze trigger | `Keep` | Fresh invocation boundary |
| 47 selected-branch and exactly-one-reference clauses | `Keep` | Context-load gate |
| 51, 52, 53 Logic, UI, Measure rows | `Keep` | Observable branch routing |
| 55 authorized-tool and two-branch clauses | `Collapse` | Tools do not import contracts; split independent questions |
| 59 Probe clauses | `Collapse` | Smallest discriminating artifact and proportional structure |
| 63 Smoke execution and record clauses | `Collapse` | Runnable evidence record |
| 65 Smoke proof limit | `Keep` | Smoke is not verdict or production proof |
| 69 discriminating-evidence clause | `Keep` | Judge demand |
| 73, 74, 75, 76 judgment matrix rows | `Keep` | Four permitted or invalid claim/mode combinations |
| 78 unavailable-human, nondiscrimination, evidence, and verdict-shape clauses | `Collapse` | Awaiting, blocked, evidence fields, alternative/`none`/threshold result |
| 80 verdict scope and production owner | `Keep` | Production-proof refusal |
| 84 inventory and one-disposition clauses | `Collapse` | Complete side-effect accounting |
| 86, 87, 88, 89 four disposition items | `Collapse` | Delete, restore, preserve-for-verdict, durable evidence |
| 91 resource release, stale pointers, answered cleanup, no-live-resource, ambiguity clauses | `Collapse` | Safe reconciliation and failure action |
| 95 current-invocation identity clauses | `Keep` | No caller or subject leakage |
| 97 packet-format clause | `Keep` | One labeled Markdown packet |
| 100-105 six envelope fields | `Keep` | Shared packet schema |
| 108 exactly-one-delta clause | `Keep` | Status discrimination |
| 110, 111, 112, 113 four status rows and their distinct fields | `Collapse` | Status-owned packet and completion predicates |
| 115 predicate, answered-only, prohibited-universal-field clauses | `Keep` | Truthful completion and no conflicting result |
| 117 caller, direct-user, stop, and no-downstream clauses | `Collapse` | Leaf Return |
| 121 Resume pointer and ownership clauses | `Disclose` | `RESUME.md`; root retains Reconcile and Return |
| 125 admission, operation, judgment, artifact, packet, and return completion clauses | `Collapse` | Terminal completion gate |

### `LOGIC.md`

| Unit | Decision | Behavior |
| --- | --- | --- |
| 3 fit, root ownership, and branch ownership clauses | `Keep` | Logic branch boundary; duplicate return clause deleted |
| 7 model scope and decision-interface clauses | `Keep` | Small explicit model |
| 9 observability, disposable shell, public-surface clauses | `Keep` | Judgeable behavior |
| 13 interactive-driver, frame, invalid-action clauses | `Keep` | Human exploration |
| 15 deterministic report and per-case fields | `Keep` | Rule-based evidence |
| 17 happy/boundary/rejected and integration exclusions | `Keep` | Representative discrimination |
| 21 Smoke gate | `Keep` | Driver reaches model and cases |
| 23 interactive Smoke item | `Keep` | Frame, state change, safe invalid behavior, quit |
| 24 deterministic Smoke item | `Keep` | Cases, criteria, repeatability, no prompt |
| 26 evidence and Measure boundary clauses | `Keep` | Verdict meaning and branch precision |
| 28 return-to-Judge and no-Reconcile/Return clauses | `Keep` | Ownership handoff |

### `UI.md`

| Unit | Decision | Behavior |
| --- | --- | --- |
| 3 fit, root ownership, and branch ownership clauses | `Keep` | UI branch boundary; duplicate return clause deleted |
| 7 real-context and throwaway-route clauses | `Keep` | Representative host |
| 9 exact paths, positive isolation, no-link proxy, blocked fallback | `Keep` | Production-unreachable app-tree work |
| 13 structural-bet, variant-bound, decorative-negative clauses | `Keep` | Discriminating alternatives |
| 15 equal constraints, repo system, fake mutation, chrome clauses | `Keep` | Comparable safe variants |
| 19 keys, URLs, switching, reload, and whole-surface gate clauses | `Keep` | Stable inspection surface |
| 21 target-surface and source-inspection clauses | `Keep` | Real UI evidence |
| 25 Smoke clauses | `Keep` | Context, variants, switching, controls, isolation |
| 27 verdict and constraint clauses | `Keep` | Judgment evidence |
| 29 return-to-Judge and no-Reconcile/Return clauses | `Keep` | Ownership handoff |

### `MEASURE.md`

| Unit | Decision | Behavior |
| --- | --- | --- |
| 3 fit, root ownership, and branch ownership clauses | `Keep` | Measure branch boundary; duplicate return clause deleted |
| 7 comparison fit, diagnosis/baseline/SLO exclusions, owner return | `Keep` | Measurement precision |
| 13-19 seven measurement-contract items | `Keep` | Directions, metric, workload, environment, samples, rule, confounders |
| 21 repo tooling, isolation, identical conditions, deletable harness, no tuning | `Keep` | Comparable bounded probe |
| 25 samples/distributions, variance/worst, noise/cache/order clauses | `Keep` | Honest variable evidence |
| 29 harness Smoke and representativeness limit | `Keep` | Smoke boundary |
| 31 frozen-rule, limits, and changed-rule clauses | `Keep` | Verdict discipline |
| 33 return-to-Judge and no-Reconcile/Return clauses | `Keep` | Ownership handoff |

### `RESUME.md`

| Unit | Decision | Behavior |
| --- | --- | --- |
| 3 awaiting-only predicate | `Disclose` | Resume admission |
| 3 invalid-status, no-inspection, current-subject, failed-fit, fresh-freeze, no-mutation, no-fabrication clauses | `Disclose` | Truthful rejected Resume |
| 5 fresh invocation and question/decision/owner/claim/mode/rule/representative/boundary/bounds/path/custody/drift checks | `Disclose` | Resume identity and safety |
| 5 restart and rerun-Smoke clauses | `Disclose` | Judgeability refresh |
| 7 execution/reconciliation reassumption and return-to-Judge clauses | `Disclose` | Lifecycle re-entry |
| 7 changed-Freeze clause | `Disclose` | Fresh Admit and Freeze |

### Metadata

| Unit | Decision | Behavior |
| --- | --- | --- |
| description bounded-question and Logic/UI/Measure clauses | `Keep` | Positive implicit invocation |
| description production-proof, diagnosis, and multi-decision negatives | `Keep` | Adjacent-negative precision |
| `allow_implicit_invocation: true` | `Keep` | Host invocation policy |

## Prompt 3 Pruning Result

- `Keep`: all non-intuitive mechanics, authority, proof, safe-failure, packet,
  branch, and completion contracts above.
- `Collapse`: repeated meaning inside the universal root, with one runtime owner
  retained for every selected behavior.
- `Disclose`: Resume procedure behind one mandatory request predicate; Logic,
  UI, and Measure remain their existing selected-branch disclosures.
- `Delete`: only no-op qualifiers and repeated explanatory wording whose
  behavior remains at the cited owner. No distinct selected behavior is deleted.

The pre-prune root has 1,497 words. The final pruned root has 1,237 words;
`RESUME.md` has 112 branch-only words. The remaining root length is unavoidable
universal contract surface under current evidence, not a raw word target.

## Deploy Prompt 4

An independent complete-package audit initially rejected equivalence because
the provisional prune omitted arbitrary frozen-rule answers and softened
partial `Freeze fields reached` into a completed Freeze. Both P09 contracts were
restored and structurally anchored. The audit also admitted deletion of the
duplicated return-to-Judge phrase in each branch opener; each terminal handoff
remains.

Five fresh pre-prune and five fresh final-pruned contexts each passed 35/35
fixed cases with zero variance and no critical failure. Decision: `accept` for
pruning equivalence at
`efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.
See
[`2026-07-21-prototype-post-prune-behavior-eval.md`](2026-07-21-prototype-post-prune-behavior-eval.md).
