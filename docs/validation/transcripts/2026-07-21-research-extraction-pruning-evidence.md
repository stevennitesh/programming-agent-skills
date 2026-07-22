# Research Experimental Extraction And Pruning Evidence

Date: 2026-07-21

## Scope And Authority

This record retrofits the complete-package coverage, unit-level pruning, and
pruning-equivalence evidence required by the revised Deploy Prompts 3 and 4.
It changes only the inactive experimental Research package and directly
affected proof surfaces. Canonical Research, installed Research, active callers,
and Git delivery remain unchanged.

## Complete Package Inventory

| Surface | Pre-prune state | Final state | Classification |
| --- | --- | --- | --- |
| `SKILL.md` | 244 lines, 1,615 words | 114 lines, 846 words | Runtime instructions; fully audited below |
| `agents/openai.yaml` | display name, short description, default prompt, implicit-invocation policy | byte-identical | Machine-consumed runtime metadata; Keep |
| References | none | none | No branch had evidence for a new pointer surface |
| Scripts | none | none | Non-runtime; Research owns no executable helper |
| Templates | none | none | Non-runtime; proportional note semantics stay inline |
| Assets | none | none | Non-runtime |
| Machine-consumed schemas | none | none | Non-runtime; the caller packet is semantic, not a parser schema |

The repaired behavior-complete pre-prune package is frozen at
[`docs/validation/evals/research-pruning-pre-prune/`](../evals/research-pruning-pre-prune/)
with tree hash
`f6c8ba9f63555e99a135dc3f38aa8f014692f8ac5779ffe896a2277a96fb0316`.
It reproduces the earlier 244-line audit-repaired candidate exactly, including
all-missing-predicate non-admission and the continuity-preserving scout branch.

The final candidate tree hash is
`1478a8ac6d50cae052802f8778a6addea9021366f3c36130385339f9fb54c099`.
Raw size fell 47.6 percent by words and 53.3 percent by lines. Those counts are
diagnostic; acceptance depends on the unit ledger and fresh equivalence proof.

## Synthesis Coverage Ledger

Every normative Research concern was reconciled before pruning.

| Synthesis concern | Prompt 3 classification | Pre-prune destination | Final disposition |
| --- | --- | --- | --- |
| Invocation reach and ordinary-lookup exclusion | Inline | description and YAML policy | Keep |
| One-question Admission and typed non-admission | Inline | Frame | Collapse into Admit |
| Caller and direct-user contract | Inline | Frame packet and inference rules | Collapse into Admit and Lock |
| Evidence, decision, and mutation authority | Inline | opening authority and Write/Verify | Collapse into Boundary, Write, Verify, Return |
| Legal route from current evidence | Non-runtime table; behavior Inline | ordered spine and status branches | Collapse into one spine and owning steps |
| Claim-specific source ownership | Inline | Trace taxonomy and source roles | Collapse to owning-source rule; detailed taxonomy remains synthesis reference |
| Assurance and proportionality | Inline | Appraise and Saturate | Collapse into Lock and Gate |
| Claim trace and result derivation | Inline | Appraise and Triangulate | Collapse into Classify |
| Freshness and applicability | Inline | Frame, Appraise, Triangulate | Collapse into Admit, Lock, Trace, Classify |
| Counterevidence, conflict, and inference | Inline | Appraise and Triangulate | Collapse into Classify and Gate |
| Scout admission, isolation, custody, and continuity | Inline | Inspect | Keep in Scout |
| Saturation and stopping evidence | Inline | Saturate | Collapse into Gate and Return |
| Artifact authority distinctions | Non-runtime explanatory table; boundary Inline | opening authority, Write, Verify | Collapse into Boundary, Write, Verify |
| One-note semantic contract | Inline | Write Or Inline | Collapse into Write |
| Citation, answer, and filesystem verification | Inline | Verify | Collapse into Verify |
| Context loading | Inline predicates; no pointer earned | branch predicates in Frame, Inspect, Write | Keep inline; no support file |
| Terminal Return forms | Inline | Return | Collapse status repetition into Classify, Admit, and generic Return |
| Completion | Inline | Completion | Collapse into one terminal criterion |
| Caller and recommendation relationships | Non-runtime registry; boundary Inline | Frame and Return | Keep generic direct/caller boundary; relationship catalog stays outside runtime |
| Rejected machinery and deferred hypotheses | Non-runtime | synthesis only | Delete from runtime; no helper, ledger, database, or support file |

Nothing is `Disclosed`: the final package has no conditional reference whose
separate loading was behaviorally earned. Universal evidence judgment, note
authority, scout custody, Return, and completion remain inline.

## Unit-Level Pruning Ledger

Each row covers the named instruction-bearing paragraph, list block, schema
field set, or distinct clause in the frozen pre-prune package. `Collapse` names
the final owner; `Delete` names why no runtime behavior was earned.

| ID | Pre-prune instruction-bearing unit | Decision | Final owner or reason |
| --- | --- | --- | --- |
| M01 | Frontmatter `name` | Keep | Parser identity |
| M02 | Description: bounded source question and primary/governing triggers | Keep | Invocation metadata |
| M03 | Description: answer/conflict/blocker, note/no-write, ordinary-lookup exclusion | Keep | Invocation and mutation precision |
| M04 | YAML display name | Keep | Interface metadata |
| M05 | YAML short description | Keep | Interface metadata |
| M06 | YAML default prompt | Keep | Explicit invocation affordance |
| M07 | YAML `allow_implicit_invocation: true` | Keep | Invocation policy |
| O01 | Outcome paragraph | Collapse | Description, Boundary, and Completion already own it |
| O02 | Research/caller authority, read-only sources, dirty-work preservation | Collapse | Boundary, Scout, Verify |
| O03 | Nine-word branch spine | Collapse | One route-aware spine; duplicate branch sequences deleted |
| A01 | Admission: one source-answerable bounded question | Keep | Admit |
| A02 | Admission: one supported use fixes relevance | Keep | Admit |
| A03 | Admission: sufficient scope/exclusions | Keep | Admit and Lock |
| A04 | Admission: time/version/fixed point/jurisdiction | Collapse | Applicable freshness or fixed point in Admit/Lock/Trace |
| A05 | Admission: proportionate evidence feasible | Collapse | Gate exact evidence/access boundary |
| A06 | Admission: return owner | Keep | Admit and Lock |
| A07 | Admission: exact, delegated-convention, or none note authority | Collapse | Admit, Lock, Boundary, Write |
| A08 | Comparison remains one question only under one terminal scope | Keep | Admit |
| A09 | Split unrelated questions or uses | Collapse | Positive one-question predicate owns the safe action |
| A10 | Infer obvious direct-user fields and ask only for material omissions | Collapse | Admit |
| A11 | Caller packet fields: caller, question, supported use, scope, freshness, path, write authority | Collapse | Admit and Lock name every field; schema block deleted |
| A12 | Return all missing caller fields before research | Keep | Admit |
| A13 | Research infers assurance, source strategy, access, and budget | Collapse | Lock; budget detail deleted without control failure |
| A14 | Preserve stricter constraints and avoid predetermined conclusion | Keep | Lock |
| A15 | `not-admitted` with every failed/missing predicate and complete packet | Keep | Admit; current-canonical control failed this behavior |
| A16 | Direct deterministic recommendation; caller classification; no invocation | Keep | Admit and Return |
| T01 | Load-bearing claim definition and applicable owning-source map | Collapse | Trace and Classify |
| T02 | Six claim-kind/source-category list items | Delete | Current-canonical control passed source selection; detailed taxonomy remains synthesis reference |
| T03 | Five source-role labels | Collapse | Trace owning/discovery plus Classify counterevidence/access |
| T04 | Discovery artifacts cannot support; cite inspected source | Keep | Trace |
| T05 | Fixed source list versus summary-only rule | Delete | No observed control failure; retained outside runtime in synthesis |
| S01 | Serial default and substantial-disjoint-lane economic gate | Keep | Scout |
| S02 | Fresh context, one complete contract, one lane each | Keep | Scout |
| S03 | Scout return claims, citations, authority, applicability, conflicts, gaps | Keep | Scout |
| S04 | Scouts do not edit, dispatch, classify, or route | Keep | Scout protected custody |
| S05 | Exclude parent conclusions and peer returns | Keep | Scout independence |
| S06 | Root verifies citations and alone judges/writes | Keep | Scout custody |
| S07 | Continuity branch uses minimum recent context and is not independent | Keep | Scout truthfulness |
| C01 | Six-field working claim-trace schema | Collapse | Classify names proposition status, citation, applicability, counterevidence, impact |
| C02 | Conditional inference/method/corroboration/authority fields | Collapse | Classify labels inference; other detail stays proportional |
| C03 | Applicability precedes nominal recency | Collapse | Trace requires applicable state |
| C04 | Ordinary assurance definition and contradiction check | Keep | Lock and Gate |
| C05 | Heightened assurance triggers | Keep | Lock |
| C06 | Heightened disconfirmation and final pass | Keep | Gate |
| C07 | Independent corroboration/unique-authority explanation and no citation count | Delete | No current-control failure; Gate preserves disconfirmation without source-count machinery |
| C08 | Falsify/narrow search, intent/implementation/observation distinctions, scope reconciliation | Collapse | Classify counterevidence and Gate conflict/limits; detailed taxonomy deleted after passing controls |
| C09 | Label inference and cite premises | Keep | Classify |
| C10 | Definitions of supported, conflicted, and unknown | Collapse | Classify attaches evidence and derives the same three statuses |
| C11 | Result derivation for answered/conflicted/blocked | Keep | Classify |
| G01 | Every claim classified; best authority inspected or exact failure; conflict explicit | Keep | Gate |
| G02 | Ordinary contradiction check | Keep | Gate |
| G03 | Heightened active disconfirmation and final no-change pass | Keep | Gate |
| G04 | Exact evidence/access boundary closes blocked or conflicted work | Keep | Gate |
| G05 | Record saturation basis, not query log | Collapse | Return requires saturation basis |
| G06 | Budget cannot convert unknown to answered | Delete | Status derivation plus exact boundary already prevent the unsafe result |
| W01 | Create/update authority, exact or delegated convention, default path | Collapse | Boundary, Lock, Write; speculative default path deleted |
| W02 | Second tracked publication mutation returns blocker or no-write | Keep | Write |
| W03 | Note fields: question/status/use/scope/freshness/assurance/saturation | Keep | Write |
| W04 | Adjacent claim citations | Keep | Write |
| W05 | Conflicts, unknowns, applicability limits, and what is not proved | Keep | Write |
| W06 | Source identity, role, authority, applicability, and supported claim | Collapse | Write removes unused role label but retains semantic evidence fields |
| W07 | Caller-use boundary and return owner | Keep | Write |
| W08 | Omit empty sections and expand only for complexity | Keep | Write; current control failed rigid output shape |
| W09 | Bibliography is not support | Keep | Write guardrail paired with adjacent citations |
| W10 | Conflicted/blocked note is durable evidence, not settled answer | Keep | Write authority boundary |
| W11 | Inline branch uses proportional verified evidence and claims no durability | Collapse | Boundary, Verify, Return |
| V01 | Every claim appears in trace and answer | Collapse | Classify plus Verify returned claims |
| V02 | Direct citation resolves and entails within authority/applicability | Keep | Verify |
| V03 | Inference, counterevidence, conflicts, unknowns, freshness, limits visible | Collapse | Classify and Write |
| V04 | Status follows claims and answer stays in scope | Keep | Verify |
| V05 | Note reread/path/content or inline direct-citation/no-durability proof | Keep | Verify |
| V06 | Start/end state proves one-note or no-write containment | Keep | Verify |
| V07 | Disposable capture cleanup | Delete | Cross-cutting engineering Lock owns disposable cleanup; no Research-specific control failure |
| V08 | Citation existence without entailment fails | Collapse | Positive direct-citation verification owns the criterion |
| V09 | Preserve and report unrelated drift | Collapse | Verify preserves unrelated work; reporting detail remains engineering contract |
| R01 | Four status-specific Return field lists | Collapse | Admit and Classify own predicates; generic Return owns shared fields |
| R02 | Written absolute path/create-update and no-write mutation none | Keep | Return |
| R03 | Caller return without recommendation, decision, mutation, or route | Keep | Return |
| R04 | Direct answer `Next: none`; direct deterministic non-admission recommendation | Keep | Return |
| R05 | Stop without downstream work | Collapse | Caller authority sentence owns the stop boundary |
| X01 | Completion: admission, classification, assurance, saturation, citations, status, output, containment | Collapse | Completion points to Admit, Gate, and citation verification |
| X02 | Exactly one note or mutation none; preserve unrelated work | Keep | Completion |
| X03 | Complete Return without caller-authority crossing | Keep | Completion |

## Residual Unavoidable Runtime Surface

The remaining 846 words are not irreducible by word count; they are the smallest
surface currently supported by the cut audit. The longest retained units are
Scout custody and the proportional Write/Verify contracts. They stay inline
because every branch can encounter source-lane, citation, mutation, or caller
authority risk, and no pointer evaluation has shown reliable branch-only
disclosure. Further cuts require fresh evidence against a concrete unit rather
than another length target.

## Pruning-Equivalence Protocol

The frozen pre-prune package is the control and the 114-line candidate is the
candidate. Five independent fresh contexts per arm receive the same seven fixed
cases and local source bytes:

1. governing version versus superseded contract, implementation drift, and blog;
2. broad empirical claim versus a narrow trial, systematic review, and sponsor claim;
3. one authorized simple governing-standard note;
4. a user-owned preference that must return `not-admitted`;
5. two unreconciled applicable governing standards that must return `conflicted`;
6. an unavailable sole governing source that must return `blocked`; and
7. a publication convention requiring an unauthorized second tracked mutation.

The rubric requires correct source applicability and status; ordinary or
heightened closure as appropriate; direct citations; proportional note shape;
one-note/no-write containment; typed non-admission; complete mutation and return
fields; and no caller decision, downstream invocation, fabricated evidence, or
second mutation. The only authorized mutation in each context is its unique
case-3 note. Exact runtime model, reasoning tier, token use, and elapsed time are
unavailable; contexts use `fork_turns="none"` with no override.

## Equivalence Result

The first pruned generation at hash
`7f791bd6cfeea0c6d6f24c85f6cfc59b33f39b731fb254f49fe741831621d4f6`
preserved every evidence, status, mutation, and caller boundary across the
seven cases. One of five samples omitted the explicit `Settled fields` slot in
its `not-admitted` packet; one written note expressed use and limits but did not
explicitly say which caller decision Research had not made. The frozen control
was 5/5 on both output details, so the unstable tail was admitted rather than
dismissed as cosmetic variance.

The repair replaced the existing non-admission prose with an ordered positive
packet contract and sharpened the existing caller-use field. It added no new
behavior or support file. Five new fresh contexts then reran the affected simple
note and capability-mismatch cases against final hash
`2edb00b756163ea7b58bac855598ec95922ac20e6f2347c5d5160ba8adc28e6c`.

| Behavior | Pre-prune control | Initial prune | Final repaired prune |
| --- | ---: | ---: | ---: |
| A: governing version, implementation drift, no write | 5 / 5 | 5 / 5 | unchanged by repair |
| B: aggregate empirical judgment and heightened limits | 5 / 5 | 5 / 5 | unchanged by repair |
| C: factual answer and exactly one authorized note | 5 / 5 | 5 / 5 | 5 / 5 |
| C: explicit caller-use boundary and complete Return | 5 / 5 | 4 / 5 | 5 / 5 |
| D: complete ordered `not-admitted` packet | 5 / 5 | 4 / 5 | 5 / 5 |
| E: unresolved governing conflict remains `conflicted` | 5 / 5 | 5 / 5 | unchanged by repair |
| F: unavailable sole owner remains `blocked` | 5 / 5 | 5 / 5 | unchanged by repair |
| G: unauthorized second publication mutation is not made | 5 / 5 | 5 / 5 | unchanged by repair |
| Critical failures | 0 / 5 | 0 / 5 | 0 / 5 |

The publication case varied between `answered` inline with a publication
blocker and `blocked` publication in both arms. That variance is permitted by
the note/no-write contract: every sample supplied the same supported inline
answer, exposed the exact convention blocker, claimed no durability, and made
no second mutation.

Every written note in the repair wave named what Standards Review could use the
evidence for, what Research had not decided, and the return owner. Every
non-admission packet exposed the failed/missing predicates, settled fields,
actual need, available evidence, mutation `none`, and return owner. Variance was
zero on the repaired rubric and the worst final sample passed both cases.

## Invocation-Description Prune

The final metadata pass reduced the always-loaded description from 60 to 34
words. It deleted explicit `$research` reach, the complete-caller-packet phrase,
and note/no-write procedure because explicit naming does not need description
support and runtime owns those mechanics. It retained three observable triggers:
one bounded primary-or-governing-source investigation, an authorized repo-local
research note, and a caller-owned evidence gap. The ordinary-lookup exclusion
remains the adjacent-negative guardrail.

Five fresh metadata-only contexts per arm classified the same three positives
and six adjacent negatives from the description and invocation policy alone.
The frozen 60-word description and the 34-word candidate each scored 45/45:

| Request family | Control | Candidate |
| --- | ---: | ---: |
| Bounded governing-source investigation | 5 / 5 | 5 / 5 |
| Authorized repo-local research note | 5 / 5 | 5 / 5 |
| Caller-owned evidence gap | 5 / 5 | 5 / 5 |
| Ordinary lookup | 5 / 5 reject | 5 / 5 reject |
| Production diagnosis | 5 / 5 reject | 5 / 5 reject |
| Runnable prototype | 5 / 5 reject | 5 / 5 reject |
| User-owned preference | 5 / 5 reject | 5 / 5 reject |
| Multi-question literature survey | 5 / 5 reject | 5 / 5 reject |
| Ordinary explanation with incidental citations | 5 / 5 reject | 5 / 5 reject |

Variance was zero; the worst sample scored 9/9. This proves metadata-level
classification equivalence, not host-platform auto-discovery of an inactive
experimental package.

## Structural And Repository Proof

- Frozen pre-prune tree hash:
  `f6c8ba9f63555e99a135dc3f38aa8f014692f8ac5779ffe896a2277a96fb0316`.
- Final Research tree and manifest hash:
  `1478a8ac6d50cae052802f8778a6addea9021366f3c36130385339f9fb54c099`.
- Experimental structural contracts: 9 passed.
- Focused skill-pack contracts: 60 passed.
- Full repository suite: 192 passed, 4 skipped. An earlier parallel run had
  two temporary `parallel-implement` helper failures; both passed serially and
  the complete parallel rerun passed.
- `git diff --check` and `git diff --cached --check`: clean.
- Canonical Research: unchanged.
- `scripts.validate_skills`: blocked by unrelated concurrent
  `to-questionnaire` candidate drift. Its actual hash was
  `b00f8d515c00047be5897dc804cc436e537a97c483d2aed90f47e3e07fcb2036`
  while its pre-existing manifest entry remained
  `0005fbcd8d8ed333bc837d154fc0adbc4ae9de2b4271cc4b72501e0e312b0a3a`.
  Research itself matched exactly.
- The disposable `.tmp/research-pruning-eval` fixture and generated notes were
  removed after judgment; the frozen package and this record are durable proof.

**Decision: accept the final pruning-equivalent inactive candidate.** The
pruning materially reduces runtime load, the fresh control demonstrates no
semantic regression after repair, and no critical failure appeared. This is
not promotion; platform invocation, live network and scout execution, caller
migration, canonical replacement, installation, and mirror parity remain E4
obligations.
