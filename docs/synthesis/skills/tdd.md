# TDD Minimum-Runtime Synthesis

Status: Complete. Canonical and installed TDD are byte-identical at accepted
hash `35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c`.

This synthesis owns the completed pruning decision and its durable rationale.
Validation owns campaign chronology, raw evaluations, and installation proof.
Canonical runtime authority remains `skills/custom/tdd/`.

## Outcome And Decision

TDD owns one bounded inner loop for settled, red-testable production behavior:

```text
TRACE -> RED -> GREEN -> REFACTOR -> RETURN
```

It proves one observable behavior through an observed behavioral RED, the
smallest GREEN implementation, GREEN-only refactoring, and an inspectable
packet returned to the original caller.

The completed minimum-runtime decision is:

- the pre-prune package was behaviorally close to B0 but contained the
  unadmitted `## Async Waiting` mechanism;
- exact B0 removes only that complete section from `tests.md`;
- the accepted C1 was exactly B0, with no behavior-changing additions;
- typed result schemas, transition tables, and expanded packet machinery are
  rejected from runtime; and
- async-waiting mechanics remain deferred until an observed canonical failure
  supplies a new admission basis.

## Viability Floor

B0 must preserve all of the following:

1. implicit discovery for settled red-testable new behavior and for bugs only
   after expected behavior, exact symptom, cause, and a trusted red-capable
   reproduction are known;
2. caller ownership of scope, review, staging, commit, tracker or external
   mutation, publishing, deployment, and delivery closeout;
3. the five-operation spine and the invariant that after-the-fact proof cannot
   replace an observed behavioral RED;
4. one Source Trace naming behavior, source, meaningful seam, independent
   oracle, and focused command;
5. the smallest authorized repo-native red-capable harness or an honest support
   gap, with manual proof excluded from RED;
6. RED before production implementation, failing for the expected missing or
   wrong behavior rather than setup, import, fixture, typo, environment, or an
   unrelated baseline failure;
7. quarantine limited to current-cycle implementation authored for that
   behavior, preserving pre-existing and unrelated work;
8. the smallest GREEN production change, focused proof, nearest relevant test
   group, and preservation of a correct assertion;
9. REFACTOR only while GREEN, with behavior or interface change returning to a
   new RED cycle;
10. conditional test-taste, double-fidelity, and refactoring references;
11. repetition only for materially distinct acceptance behavior; and
12. a compact proof packet and completion criterion that return inner-loop
    evidence without claiming caller-owned closeout.

## Evidence Registry And Freshness

| Evidence | Identity or access depth | Role | Freshness limit |
| --- | --- | --- | --- |
| Canonical TDD package | `skills/custom/tdd/`; tree hash `35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c` | Current runtime authority and accepted B0/C1 | Recompute after any byte change |
| Pre-prune control | `docs/validation/evals/tdd-pruning-pre-prune/`; tree hash `2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae` | Behavior-complete control and exact deletion source | Immutable campaign evidence |
| Matt Pocock TDD | `.tmp/mattpocock-skills` at `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; complete package and named documentation read | Simplest credible baseline | Clean local `main`; not network-refreshed |
| Superpowers TDD | `.tmp/superpowers` at `d884ae04edebef577e82ff7c4e143debd0bbec99`; complete package read | Stricter comparison | Clean local `main`; not network-refreshed |
| Ponytail | `.tmp/ponytail` at `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; no TDD equivalent found | Absence check | Clean local `main`; not network-refreshed |
| Upper-bound engineering language | Applicable TDD, tracer-bullet, seam, proof, completion, and pruning rows read with their evidence pointers | Research pressure and semantic correction | Document states 2026-07-22 freshness |
| Runtime relationships | `docs/synthesis/skill-context-relationships.md` | Accepted caller and callee contracts | Unchanged by this pruning |
| Structural proof | `tests/test_experimental_skill_contracts.py::test_canonical_tdd_is_the_exact_single_cut_baseline` | Exact inventory and single-cut identity | Passed at promotion Lock |
| Pruning-equivalence decision | [`docs/validation/evals/tdd-pruning-results/decision.md`](../../validation/evals/tdd-pruning-results/decision.md) | Fixed-case non-regression result | Five fresh samples per arm; bounded to recorded runtime and cases |
| Campaign and installation record | [`docs/validation/transcripts/2026-07-22-tdd-candidate-evidence.md`](../../validation/transcripts/2026-07-22-tdd-candidate-evidence.md) | Package identities, promotion, installation, and parity | Historical proof record |

No skill-specific source packet beyond the prior synthesis source list was
found. The book and article references below are rationale, not current local
runtime authority or behavioral proof.

## Simplest Credible Baseline

Matt's TDD package is the smallest inspected coherent control. It supplies:

- one vertical test-then-implementation cycle;
- behavior through public interfaces or meaningful seams;
- independently sourced expectations;
- minimal GREEN; and
- disclosed test and mocking examples.

It is not locally sufficient without explicit adaptation:

| Matt baseline difference | Local decision | Basis |
| --- | --- | --- |
| Broad feature and bug invocation | Narrow to settled red-testable behavior and the four-fact bug gate | Required local routing and safety contract |
| User must confirm every seam | Agent selects technical seams from repository evidence; ask only for unsettled user commitments | Caller authority and lower ceremony |
| No caller delivery boundary | Add the compact caller-owned boundary | Required local composition contract |
| Red-green only; refactoring moved to review | Retain GREEN-only in-slice REFACTOR | Core locally named outcome and accepted relationship contract |
| No explicit invalid-RED branches | Retain the current behavioral-failure gate | Non-intuitive proof boundary |
| No safe dirty-work quarantine rule | Retain current-cycle-only quarantine | Non-intuitive safety boundary |
| No nearest-group GREEN proof | Retain focused plus nearest relevant validation | Local completion contract |
| No proof Return | Retain the compact existing packet | Caller resumption contract |
| No engineering/domain pointers | Retain conditional local pointers | Required platform contract |

Superpowers is not selected. Its universal invocation, broad deletion command,
no-exceptions rhetoric, per-function checklist, and rationalization catalogue
add load and can violate unrelated-work preservation. Ponytail supplies no
matching baseline.

## Current-Runtime Disposition

This ledger classifies the complete current package by behavior-bearing unit.

| Surface and behavior | Disposition | Canonical treatment |
| --- | --- | --- |
| `agents/openai.yaml`: implicit invocation | Protect | Preserve exact bytes |
| `SKILL.md` description: new-behavior trigger, four bug facts, Diagnosis and Prototype exclusions | Protect | Preserve exact bytes |
| Outcome, five-operation spine, and observed-RED invariant | Protect | Preserve exact bytes |
| Caller-owned delivery and mutation boundary | Protect | Preserve exact bytes |
| Diagnosis and Prototype handoffs | Protect | Preserve exact bytes |
| Conditional `tests.md`, `mocking.md`, and `refactoring.md` pointers | Protect and disclose | Preserve exact bytes |
| Engineering-contract and domain routing pointers | Protect; foreign procedure owned elsewhere | Preserve exact bytes |
| TRACE Source Trace and one tracer-bullet tuple | Protect | Preserve exact bytes |
| Repository-evidence seam choice and user-decision boundary | Protect | Preserve exact bytes |
| Smallest repo-native harness and authority gate | Protect | Preserve exact bytes |
| Behavior-preserving GREEN prefactor or support-gap Return | Protect | Preserve exact bytes |
| RED-first mutation order and valid-failure classification | Protect | Preserve exact bytes |
| Immediate pass, error, and unrelated-failure responses | Protect | Preserve exact bytes |
| Current-cycle-only quarantine and honest after-the-fact classification | Protect | Preserve exact bytes |
| Minimal GREEN, focused plus nearby proof, and assertion preservation | Protect | Preserve exact bytes |
| GREEN-only REFACTOR and new-RED requirement for behavior/interface change | Protect | Preserve exact bytes |
| Distinct-behavior repetition and equivalent-data stop | Protect | Preserve exact bytes |
| Compact Return fields and completion criterion | Protect | Preserve exact bytes |
| `tests.md`: tracer-bullet example | Disclose | Preserve exact bytes |
| `tests.md`: public-behavior contrast and stable-module qualification | Disclose | Preserve exact bytes |
| `tests.md`: independent-oracle contrast | Disclose | Preserve exact bytes |
| Pre-prune `tests.md`: Async Waiting section | Defer | Removed canonically as one complete section |
| `tests.md`: test-shape red flags | Disclose | Preserve exact bytes |
| `mocking.md`: real-to-mock substitute order | Protect and disclose | Preserve exact bytes |
| `mocking.md`: boundary-fake example | Disclose | Preserve exact bytes |
| `mocking.md`: fidelity gate, shared contract test, risk Return, and no production test hook | Protect and disclose | Preserve exact bytes |
| `refactoring.md`: GREEN-only scope and proof cadence | Protect and disclose | Preserve exact bytes |
| `refactoring.md`: depth, leverage, and locality pressures | Supporting branch guidance | Preserve exact bytes; no contribution claim |
| `refactoring.md`: Simplify Code, Codebase Design, and Improve Codebase recommendations | Protect and disclose | Preserve exact bytes |

No current canonical typed outcome schema, persistent state, helper, or
transition table exists. Their appearance in the superseded synthesis created
no protected runtime behavior.

## Research Intake

Original labels are retained where available.

| Research pressure | Original claim boundary | Local disposition | Runtime consequence |
| --- | --- | --- | --- |
| RED-GREEN-REFACTOR | `synthesis`; Superpowers corroborated; Matt corroborated but conflicted | Semantic substitution | State the chosen local GREEN-only refactor position; already present |
| Tracer bullet | `synthesis`; externally corrected only within the cited UBL scope; behavioral effect untested | Semantic substitution | Use as one narrow real feedback path, not task size or final architecture; already present |
| Public interface and seam | `synthesis`; Matt corroborated | Supporting rationale only | Keep repository-evidence seam selection; no new mechanism |
| Independent oracle | Upstream corroboration; no separate efficacy proof | Core outcome | Keep independent expectation requirement and examples |
| Deep module, depth, leverage, locality | `synthesis`; Matt corroborated; broader professional history unvalidated | Supporting rationale only | Retain compact refactor pressure without mandating abstraction |
| Classicist | Prior synthesis inference from Fowler and local design | Defer the term | Observable double mechanics already express the protected behavior |
| Async condition waiting | Prior synthesis proposal; no observed canonical failure or source packet | Defer | Remains absent from canonical runtime |
| Evidence before claims and completion criterion | `synthesis`; upstream corroborated | Required local contract | Existing Return and completion remain |
| Context pointer and progressive disclosure | Matt direct for authoring semantics | Required local information hierarchy | Existing three pointers remain |
| Source books and articles | Thin links and prior synthesis interpretation | Supporting rationale only | Keep here, never load at runtime |
| Superpowers Iron Law, deletion, and no-exceptions language | Direct upstream behavior with conflicting local safety requirements | Reject | Do not extract |

Decision-changing source references retained from the earlier synthesis:

- Kent Beck, *Test-Driven Development: By Example*;
- Martin Fowler, *Refactoring*, *Mocks Aren't Stubs*, and *Test Double*;
- Steve Freeman and Nat Pryce, *Growing Object-Oriented Software, Guided by Tests*;
- Gerard Meszaros, *xUnit Test Patterns*;
- Michael Feathers on seams and legacy code;
- Lasse Koskela, *Effective Unit Testing*; and
- John Ousterhout, *A Philosophy of Software Design*.

Their historical use was to pressure observed RED, behavior-first tests,
independent oracles, real owned collaborators, boundary doubles, and GREEN-only
refactoring. No source establishes that expanded schemas or async mechanics
improve this skill.

## Unified Baseline-Delta Ledger

| Mechanism | Baseline state | Current disposition | Research pressure and label | Admission basis | Owner | Cheaper expression | Runtime destination | Required proof | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Local invocation gate | Missing | Protect | Invocation economics; synthesis | Required local contract | TDD metadata | Current concise description | B0 `SKILL.md` and metadata | Invocation positives and adjacent negatives | Admit to B0 |
| Four-fact bug gate | Missing | Protect | Tight red-capable loop; synthesis | Required local contract; non-intuitive safety boundary | TDD and Diagnosis at independent entry points | One repeated predicate per entry | B0 `SKILL.md` | Four missing-fact cases plus fully known case | Admit to B0 |
| Caller delivery boundary | Missing | Protect | Ownership trace; local contract | Required local contract | Caller and TDD | Current compact paragraph | B0 `SKILL.md` | Relationship trace | Admit to B0 |
| TRACE tuple | Partial | Protect | Tracer bullet and seam; synthesis | Core outcome | TDD | Five named facts | B0 `SKILL.md` | Packet and action trace | Admit to B0 |
| Red-capable harness gate | Missing | Protect | Tight feedback loop; synthesis | Core outcome; required local contract | TDD | Current compact gate | B0 `SKILL.md` | Harness and support-gap cases | Admit to B0 |
| Valid behavioral RED | Partial | Protect | RED-GREEN-REFACTOR; synthesis | Core outcome; non-intuitive proof boundary | TDD | Expected behavioral failure plus three invalid branches | B0 `SKILL.md` | Immediate pass, setup, unrelated, wrong-failure cases | Admit to B0 |
| Safe quarantine | Missing | Protect | Local stewardship | Non-intuitive safety boundary | TDD | Current-cycle-authored implementation only | B0 `SKILL.md` | Dirty-work preservation case | Admit to B0 |
| Minimal GREEN and nearest proof | Partial | Protect | RED-GREEN-REFACTOR; synthesis | Core outcome; required local contract | TDD | Focused plus nearest group | B0 `SKILL.md` | Focused and nearby regression cases | Admit to B0 |
| GREEN-only refactor | Conflicted | Protect | Superpowers supports; Matt conflicts | Core locally named outcome; required relationship contract | TDD | One universal gate plus disclosed branch | B0 `SKILL.md` and `refactoring.md` | Behavior-changing and out-of-slice cases | Admit to B0 |
| Independent oracle and test taste | Partial | Disclose | Upstream corroboration | Core outcome | `tests.md` | Three compact contrasts | B0 `tests.md` | Circular-oracle and weak-seam cases | Admit to B0 |
| Double fidelity | Partial | Protect and disclose | Classicist pressure; synthesis | Non-intuitive proof boundary | `mocking.md` | Substitute order plus consumed-contract gate | B0 `mocking.md` | Owned-module and incomplete-fake cases | Admit to B0 |
| Scoped refactor recommendations | Missing | Protect and disclose | Local ownership trace | Required local contract | `refactoring.md` and callees | Three observed-scope routes | B0 `refactoring.md` | Relationship trace and stop behavior | Admit to B0 |
| Compact proof packet | Missing | Protect | Evidence before claims; synthesis | Required local contract | TDD | Existing six fields | B0 `SKILL.md` | Complete and incomplete Return cases | Admit to B0 |
| Typed outcome schemas | Missing | Remove from proposal | Prior local synthesis only | None | None | Existing compact packet | Non-runtime rationale only | Not applicable | Reject |
| Transition and operation tables | Missing | Remove from proposal | Prior local synthesis only | None | None | Five-operation spine and local gates | Non-runtime rationale only | Not applicable | Reject |
| Async waiting mechanics | Missing from Matt core; present pre-prune | Defer | Prior local synthesis only | None; no observed canonical failure | `tests.md` only if later admitted | No runtime expression now | Deferred | Observed canonical failure plus fresh claim-matched proof | Defer; absent canonically |
| Persistent ledger, helper, or schema | Missing | Reject | No supporting local evidence | None | None | Plain Markdown Return | None | Not applicable | Reject |

## Exact Canonical Pruning Identity

The accepted runtime is not a conceptual rewrite. It is the pre-prune TDD
package transformed by exactly one deletion:

> Remove from `skills/custom/tdd/tests.md` the complete section beginning with
> `## Async Waiting` and ending immediately before `## Red Flags`, including
> its two explanatory paragraphs and both Python examples. Make no other byte
> change in the five-file package.

The canonical package contains exactly these paths and hashes:

| Relative path | Canonical SHA-256 | Identity rule |
| --- | --- | --- |
| `SKILL.md` | `3c40b46601971434c5a0ab437e3172b02ad59880c06d3c50e6058f74251c3806` | Preserve current bytes |
| `tests.md` | `b3738122d3b3b72a66d9e40bd22ec252549ef7077b4d9914cb68f5b8dea67465` | Exact deletion above |
| `mocking.md` | `9523c1371ef4c711c69932a42214eef21159f5c20baf36cb1fdcf3e8fd2efa5e` | Preserve current bytes |
| `refactoring.md` | `4d1ae71d594a02cdd09f0cef42224969d5deab39091149ab057edae5838097e4` | Preserve current bytes |
| `agents/openai.yaml` | `d9ef3372e04c488b227009cd14ef0ed84fa4335056d48219bc6cbf8a80a970bd` | Preserve current bytes |

The frozen pre-prune package tree hash is
`2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae`.
Applying only the specified deletion yields the canonical B0/C1 tree hash
`35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c`
under the repository's format-1 tree-hash algorithm.

The canonical structural proof recomputes this identity from materialized
bytes and requires every non-`tests.md` file to remain byte-identical to the
pre-prune control.

## Pruning-Only Decision

C1 has no additions:

```text
C1 = exact B0
```

There is no mechanism-contribution claim and no C1-only entry condition,
failure Return, owner, destination, or proof arm. The accepted claim is only
that removing Async Waiting did not meaningfully regress the protected TDD
behavior on the fixed evaluation cases.

## Protected Behavior Set

The protected set is:

- implicit invocation and its positive and adjacent-negative routing boundary;
- the four-fact bug predicate at TDD, Diagnosis, Implement, Router, and lane
  entry surfaces;
- original-caller retention and caller-owned delivery closeout;
- engineering and domain context pointers;
- TRACE behavior, source, seam, oracle, and command;
- a trustworthy automated RED path or honest support gap;
- pre-implementation behavioral RED and invalid-RED classification;
- current-cycle-only quarantine and unrelated-work preservation;
- minimal GREEN, nearest relevant validation, and correct-assertion protection;
- GREEN-only behavior-preserving refactoring;
- materially distinct behavior coverage without equivalent-data inflation;
- conditional loading of test taste, mocking, and refactoring guidance;
- real owned modules and fidelity-checked boundary doubles;
- scoped out-of-slice recommendations that stop; and
- the compact proof packet and inner-loop completion boundary.

Exact current sentences and the Async Waiting section are not protected merely
because they exist.

## Current Placement And Ownership

| Concern | Owner and destination |
| --- | --- |
| Invocation, common path, gates, Return, completion | `skills/custom/tdd/SKILL.md` |
| Test shape, seams, and independent-oracle examples | `skills/custom/tdd/tests.md` |
| Double order and fidelity | `skills/custom/tdd/mocking.md` |
| GREEN refactor and scoped recommendations | `skills/custom/tdd/refactoring.md` |
| Invocation policy | `skills/custom/tdd/agents/openai.yaml` |
| Pre-prune control and raw equivalence evidence | `docs/validation/evals/tdd-pruning-pre-prune/` and `docs/validation/evals/tdd-pruning-results/` |
| Campaign, promotion, and installation record | `docs/validation/transcripts/2026-07-22-tdd-candidate-evidence.md` |
| Accepted relationship index | `docs/synthesis/skill-context-relationships.md`; unchanged by this decision |
| Canonical single-cut proof | `tests/test_experimental_skill_contracts.py::test_canonical_tdd_is_the_exact_single_cut_baseline` |

Foreign ownership remains unchanged:

- the caller owns bounded scope and delivery closeout;
- `$diagnosing-bugs` owns causal uncertainty and returns all four facts or a
  decision-needed packet without bounce;
- `$prototype` owns throwaway design evidence;
- `$simplify-code`, `$codebase-design`, and `$improve-codebase` own the three
  out-of-slice refactor outcomes;
- `docs/agents/engineering-contract.md` and `docs/agents/domain.md` own shared
  engineering and domain procedure;
- `docs/synthesis/skill-context-relationships.md` owns the accepted edge index;
  and
- evaluation, installation, and Git delivery remain with their shared owners.

## Information-Hierarchy Classification

| Class | Behavior |
| --- | --- |
| Common path | Outcome, admission, caller boundary, five operations, universal gates, Return, completion |
| Disclosed | Test taste and oracle examples; double fidelity; GREEN refactor guidance and scoped recommendations |
| Caller-owned | Scope, acceptance, review, staging, commit, trackers, external mutation, publishing, deployment, closeout |
| Owned elsewhere | Engineering/domain procedure; Diagnosis, Prototype, Simplify Code, Codebase Design, Improve Codebase procedures |
| Non-runtime | Source rationale, baseline comparison, decision ledgers, and validation-owned proof records |
| Rejected | Typed statuses, transition tables, helper/schema/ledger, universal deletion and no-exceptions rhetoric |
| Deferred | Async condition-waiting mechanics, Classicist term contribution, specialist test taxonomies |

## Claim-To-Proof Matrix

| Claim lane | Exact claim | Current evidence | Limit |
| --- | --- | --- | --- |
| Semantic fidelity | Canonical TDD retains observed RED, tracer bullet, independent oracle, GREEN-only refactor, and compact Return | Exact preservation of four files and the non-Async-Waiting bytes of `tests.md`; protected-behavior trace | Does not prove behavior outside the recorded contract |
| Mechanism contribution | None; accepted C1 equals B0 | Exact shared hash and no C1-only mechanism | No improvement claim exists |
| Current-contract preservation | Every protected behavior remains discoverable after the cut | Structural identity proof, relationship trace, and fixed behavioral cases | Structural checks alone are insufficient |
| Pruning equivalence | Removing Async Waiting caused no meaningful regression on the fixed cases | Control 45/45 and accepted package 45/45; async cases 10/10 per arm; zero critical failures | Supports only the recorded tasks, runtime, rubric, and sample size |
| Invocation and context loading | Metadata and the three remaining pointers retain their routing and conditional loading | Exact metadata and pointer-byte preservation plus fixed branch cases | No claim beyond tested invocation and branch pressure |
| Deterministic package identity | Canonical bytes equal the exact five-file manifest above | Tree hash, per-file hashes, and canonical single-cut test | Any byte change invalidates affected evidence |

## Rejected And Deferred Design

Rejected from canonical runtime unless a new evidence-backed admission reopens
them:

- typed `proved-tdd`, `after-the-fact`, `support-gap`, `handoff`, and
  `decision-needed` schemas;
- a universal state-transition or operation-completion table;
- a proof-packet helper, JSON schema, cycle ledger, or persisted state file;
- one file per operation;
- framework-specific universal commands;
- mandatory test counts, assertion counts, or coverage percentages;
- universal snapshot prohibition;
- mock-first implementation;
- public production hooks solely for tests;
- automatic tracker mutation, formal review, Git, or release procedure; and
- Superpowers' broad delete-and-restart and no-exceptions language.

Deferred pending an observed canonical failure and a new admission decision:

- async condition-waiting and elapsed-time mechanics;
- explicit property, metamorphic, mutation, contract, performance,
  concurrency, or nondeterminism references;
- `Classicist` as a term-contribution mechanism;
- a machine-readable proof packet; and
- any additional split of test-taste reference material.

## Completed Decision And Proof

The completed decision is pruning-only:

- pre-prune control hash:
  `2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae`;
- canonical and installed hash:
  `35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c`;
- canonical delta: delete only the complete Async Waiting section from
  `tests.md`;
- every other package byte and every relationship: unchanged; and
- behavioral claim: pruning equivalence on the fixed evaluation cases, not an
  improvement or universal async-testing claim.

The control and accepted package each passed 45/45 protected case judgments
and 10/10 async judgments, with zero critical failures. One accepted-package
sample contained a contradictory but noncritical wording advisory; it did not
change the protected decision, was not applied to runtime, and remains part of
the recorded evidence limit.

Proof is owned by validation:

- [pruning-equivalence decision](../../validation/evals/tdd-pruning-results/decision.md);
- [fixed protocol](../../validation/evals/tdd-pruning-results/protocol.md),
  [rubric](../../validation/evals/tdd-pruning-results/rubric.md), and adjacent
  raw responses;
- [promotion, installation, and parity record](../../validation/transcripts/2026-07-22-tdd-candidate-evidence.md); and
- frozen pre-prune package at
  `docs/validation/evals/tdd-pruning-pre-prune/`.

## Residual Limits

- Non-regression is bounded to the recorded tasks, runtime, rubric, and five
  fresh samples per arm; it is not universal equivalence.
- Removing Async Waiting does not establish that its mechanics are wrong. It
  establishes that they lacked an admission basis and caused no meaningful
  regression under the fixed pressure cases.
- The inspected upstream checkouts were local fixed points and were not
  network-refreshed for this campaign.
- Any canonical byte or affected behavioral-claim change invalidates the
  corresponding hash and behavioral evidence.
- Reintroducing async-specific mechanics requires an observed canonical
  failure, a new admission decision, and fresh claim-matched proof.
