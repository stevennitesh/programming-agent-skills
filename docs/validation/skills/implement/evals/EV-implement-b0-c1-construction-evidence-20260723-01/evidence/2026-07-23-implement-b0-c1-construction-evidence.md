# Implement B0/C1 Construction Evidence

Status: `promoted-and-installed` by Deploy Prompt 5 for exact accepted hash
`b918d2762505a69d1ba577533a2b9bd040133188b0e0c6dee4cb7e78351b4f7c`

Authority: Deploy Prompt 3 author mode only. This record constructs and
mechanically proves the inactive candidate. It does not behaviorally evaluate,
promote, install, deliver through Git, or begin a successor campaign.

## Campaign Identity

- campaign shape: `pruning-only`
- accepted relation: `current != B0 = C1`
- active fixed point:
  `a0879b1e1602928a705e4973e5a013bf3f2bb42c`
- one shared immutable B0/C1 corpus:
  `skills/experimental/implement`
- behavior-complete pre-prune corpus:
  `docs/validation/evals/implement-pruning-pre-prune`
- C1 behavioral delta from B0: empty
- proposed invocation, caller, ownership, and Return deltas from B0 to C1:
  none

One corpus serves as both B0 and C1. No duplicate candidate trees exist.

## Exact Inventories And Hashes

Package hashes use the repository's experimental `tree_hash` contract: sorted
relative POSIX path, NUL, file bytes, NUL, SHA-256.

| Identity | Package hash | Exact inventory |
| --- | --- | --- |
| Current canonical | `ef2a52520462266ad0af171869d516c709ba57e737dcf9658e0a3cbb643af8bc` | `SKILL.md`, `agents/openai.yaml` |
| Frozen pre-prune | `ef2a52520462266ad0af171869d516c709ba57e737dcf9658e0a3cbb643af8bc` | `SKILL.md`, `agents/openai.yaml` |
| Shared B0/C1 | `b918d2762505a69d1ba577533a2b9bd040133188b0e0c6dee4cb7e78351b4f7c` | `SKILL.md`, `agents/openai.yaml` |

| File | Current and pre-prune SHA-256 | Shared B0/C1 SHA-256 |
| --- | --- | --- |
| `SKILL.md` | `ba908bfb7276100ba203057c632bed3e03c615d65aa1fa359f926922c5a62ba5` | `7a8b391a92609e08e1b8f70526981381ddb9336c218aed8d3c28cc4fdb618b65` |
| `agents/openai.yaml` | `d1331038252c7012dceebe0627884e12bb2a9975263b974bf9a991168d6dc3b8` | `d1331038252c7012dceebe0627884e12bb2a9975263b974bf9a991168d6dc3b8` |

The frozen pre-prune files are byte-identical to current. The B0/C1 metadata is
byte-identical to current. The B0/C1 `SKILL.md` is 6,396 bytes and 915
whitespace-delimited words versus current's 6,924 bytes and 984 words: a
528-byte and 69-word reduction.

## Baseline Adaptation Delta

The selected Matt Pocock Implement source supplies only the small core:
implement one plan, inspect the repository, execute steps in order, validate,
and report. Executable local B0 necessarily adapts that core to this pack's
existing contract:

- one ready singleton rather than an arbitrary plan;
- explicit-only owner or named staged-worker authority;
- setup, selection, claim, fixed-point, dirty-state, and index isolation;
- immutable Charter, bounded slice, commitment boundary, and proof;
- caller routing to TDD or Diagnosis without copying their procedures;
- exactly one immutable review route;
- complete-report finding admission and finite Repair;
- review-tree to lock-tree identity, one commit, and tracker read-back; and
- typed Return outcomes and explicit external-action boundaries.

These are baseline compatibility requirements, not C1 mechanisms. C1 adds
nothing to this adapted B0.

## Evidence Dispositions

### Current Runtime

| Current evidence family | Disposition in B0/C1 |
| --- | --- |
| Frontmatter and provider metadata | Preserve exactly |
| Outcome, owner/staged spines, role authority | Preserve; collapse repeated explanation |
| Setup, singleton selection, readiness, claim, fixed point, isolation | Preserve |
| Charter, bounded proof story, commitment boundary | Preserve; express as one compact operation |
| TDD, Diagnosis, and RED-unsuitable routing | Preserve pointers; do not import foreign procedures |
| Staged-worker proof, staging, and owner handoff | Preserve |
| Immutable review route and acceptance | Preserve |
| Complete-report admission and bounded Repair generation | Preserve |
| Repo-local closeout, lock identity, one commit, connector read-back | Preserve |
| Typed Return and completion boundary | Preserve; collapse prose duplication |
| State, operation, artifact, proof-level, and other explanatory tables | Remove from runtime; their protected behaviors remain in the spine |
| Duplicated explanations and repeated selection-return language | Remove or consolidate |
| Broken relative Facet Consolidation Register link | Remove; no candidate link replaces it |

### Research And Prior Evidence

| Evidence | Disposition |
| --- | --- |
| Matt Pocock Implement core | Adapt into B0 as the small execution nucleus |
| Prior Implement facet synthesis | Use as provenance only; do not restore a competing runtime architecture |
| Current structural tests and provider fixtures | Reuse only where candidate-specific structural proof is needed |
| Prior behavior evidence | Preserve as prior evidence; do not claim it evaluates this hash |
| Installed-mirror evidence | Historical only; installation is outside Prompt 3 |
| Unexecuted dirty-index and connector-failure scenarios | Preserve as Prompt 4 evidence gaps |

### Unified Baseline-Delta Mechanism Ledger

| Candidate mechanism | B0 requirement | C1 contribution |
| --- | --- | --- |
| Singleton selection and authority | Yes | None |
| Charter and bounded proof story | Yes | None |
| TDD/Diagnosis caller routing | Yes | None |
| One immutable review route | Yes | None |
| Complete-report bounded Repair | Yes | None |
| Lock-tree identity and one commit | Yes | None |
| Tracker closeout read-back | Yes | None |
| Typed Return | Yes | None |
| Wording substitutions, ownership corrections, and cuts | Behavior-preserving baseline expression | None |

The unified ledger is exhaustive: there is no admitted C1 mechanism.

## Protected Viability Floor

B0/C1 must continue to:

1. deliver exactly one selected ready item;
2. keep named-target identity binding and reject unsliced source;
3. separate owner and staged-worker mutation authority;
4. preserve unrelated work and isolate the selected diff;
5. freeze Charter, commitment boundary, proof, route, and finite Budget;
6. route settled red-testable work to TDD and uncertain bugs to Diagnosis;
7. require focused semantic proof and a bounded staged handoff;
8. review exactly one immutable tree through exactly one route;
9. admit only a complete report and repair all eligible blockers as one
   generation without partial mixed-authority repair;
10. permit only verified closeout metadata after accepted review;
11. commit the exact lock tree once and verify `HEAD^{tree}`;
12. read back tracker mutations and report partial failure honestly; and
13. Return one typed result without claiming a staged handoff is complete.

## Clause Classification And Pruning Ledger

Every instruction-bearing candidate clause is classified below. `B0` denotes
locally necessary behavior, `minimum context` makes a B0 instruction routable,
and `collapse` is a behavior-preserving pruning operation. There are no
`admitted addition`, `disclose`, or C1-mechanism rows.

| Candidate lines | Classification | Construction disposition |
| --- | --- | --- |
| 1-4 | Minimum context / B0 | Preserve name and routing predicate exactly |
| 8 | B0 / collapse | One outcome replaces repeated north-star prose |
| 10-12 | B0 / collapse | Two executable spines replace explanatory flow |
| 14-21 | B0 / collapse | Retain role and mutation authority once |
| 25-27 | B0 | Retain setup and tracker-context gate |
| 29-38 | B0 / collapse | Retain binding selection, source boundary, policy order, and read-only selection |
| 40-45 | B0 | Retain readiness, claim read-back, fixed point, isolation, and preservation |
| 49-52 | B0 / collapse | One immutable Charter record |
| 54-58 | B0 / semantic substitution | Express existing scope/proof requirements as one bounded proof story |
| 60-67 | B0 / minimum pointer | Preserve TDD/Diagnosis routing, semantic evidence, and adjacent-work return |
| 69-72 | B0 / collapse | Preserve staged-worker proof and owner acceptance |
| 76-82 | B0 | Preserve canonical acceptance, selected tree, one route, and Spec packet |
| 84-91 | B0 / minimum pointer | Preserve acceptance and complete-report admission; point to the finding owner |
| 93-97 | B0 / collapse | Preserve one batched generation, successor review, and stop states |
| 101-113 | B0 / collapse | Preserve closeout order, lock comparison, one commit, and read-back failure |
| 117-127 | B0 / collapse | One seven-row Return schema replaces duplicated outcome prose |
| 129-133 | B0 / collapse | Preserve completion and external-action boundaries |
| `agents/openai.yaml` | Minimum context / B0 | Preserve explicit-only policy and provider interface byte-for-byte |

Removed runtime load:

- unsupported state-transition, operation-completion, artifact-authority, and
  proof-level tables;
- duplicated flow, role, selection, completion, and Return explanations;
- the broken Facet Consolidation Register link; and
- headings whose only function was to split one coherent operation.

No helper, schema, reference, extra candidate file, or foreign-owner procedure
was added.

## Relationships

The proposal changes no invocation, caller, ownership, or Return relationship.
Implement remains explicit-only; TDD and Diagnosis own their inner loops;
Review and Convergent PR Review own judgment; Review owns finding admission;
Repo Bootstrap and To Tickets own setup and shaping repairs; and staged-worker
Return still terminates at the accepting Implement owner. Therefore
`docs/synthesis/skill-context-relationships.md` requires no Prompt 3 edit.

## Claim-To-Proof Matrix

| Claim | Prompt 3 proof | Remaining owner |
| --- | --- | --- |
| One exact B0/C1 corpus | Manifest hash, exact inventory, candidate-specific test | Complete |
| Frozen behavior-complete pre-prune control | Byte equality and identical package hash | Complete |
| Empty B0-to-C1 behavioral delta | One shared corpus and unified ledger | Complete |
| Protected viability floor is present | Candidate-specific anchor assertions, relationship trace, and 45/45 fresh candidate cases | Complete |
| Candidate is pruning-only | Lower bytes/words, removed-table assertions, pruning ledger, and 45/45 pre-prune versus 45/45 candidate cases | Complete |
| Metadata and invocation are unchanged | Byte equality and explicit policy assertion | Complete |
| Current runtime remains untouched | Canonical hash assertion | Complete |
| Relationship surface is unchanged | Relationship read-back and no diff | Complete |
| Candidate is promotion-ready | Prompt 4 accepted exact hash; see `2026-07-23-implement-post-candidate-behavior-eval.md` | Prompt 5 |

## Residual Unavoidable Load And Evidence Gaps

The retained load is the minimum coherent local delivery owner: selection,
authority, Charter, proof routing, staged handoff, immutable review, bounded
Repair, Lock, tracker closeout, and typed Return. Removing any one would violate
the protected viability floor or transfer an unowned seam to the caller.

Prompt 4 established pruning equivalence on the registered fresh-context cases,
including dirty-index isolation, route selection, complete-report Repair,
review/lock tree identity, staged-worker limits, and partial tracker read-back.
Live Git and provider mutations remain residual limits rather than unrun
registered claims.

## Prompt 4 Acceptance

Five fresh pre-prune and five fresh candidate samples each passed all nine
registered behavior families: 45/45 per arm with no critical failure. No
candidate repair occurred, so the exact Prompt 3 hash remains accepted.

The complete protocol, rubric, per-sample ledger, variance, worst result,
deviations, unavailable telemetry, and residual gaps are recorded in
`2026-07-23-implement-post-candidate-behavior-eval.md`.

## Prompt 5 Promotion And Installation

Prompt 5 verified the accepted record, exact candidate hash, two-file
inventory, and unchanged behavioral claims before promotion. It then:

- copied the accepted package byte-for-byte into
  `skills/custom/implement`;
- preserved `agents/openai.yaml` byte-for-byte;
- converted candidate-only structural proof into canonical promotion proof;
- removed only `skills/experimental/implement` and its manifest entry;
- preserved the frozen pre-prune package and every unrelated candidate;
- reused Prompt 4 behavior evidence because bytes, tasks, claims, protocol,
  settings, and rubric were unchanged;
- previewed a managed cohort containing only `implement`;
- synchronized through
  `python -m scripts.install_skills --skip-global-agents`; and
- verified a clean post-install dry-run and canonical-to-installed hash
  parity.

Final identities:

| Surface | Tree hash | Inventory |
| --- | --- | --- |
| Canonical | `b918d2762505a69d1ba577533a2b9bd040133188b0e0c6dee4cb7e78351b4f7c` | `SKILL.md`, `agents/openai.yaml` |
| Installed | `b918d2762505a69d1ba577533a2b9bd040133188b0e0c6dee4cb7e78351b4f7c` | `SKILL.md`, `agents/openai.yaml` |
| Frozen pre-prune | `ef2a52520462266ad0af171869d516c709ba57e737dcf9658e0a3cbb643af8bc` | `SKILL.md`, `agents/openai.yaml` |

Canonical integration proof:

- affected pack contracts: `59 passed`;
- promoted lifecycle contracts: `11 passed`;
- full suite: `194 passed, 4 skipped`;
- `python -m scripts.validate_skills`: passed;
- install preview: `Updated skills: implement`, `Unchanged skills: 24`;
- clean post-install preview: `Unchanged skills: 25`;
- affected Markdown gate: passed for synthesis and both Implement validation
  transcripts;
- frozen-control link exception: the byte-exact pre-prune `SKILL.md` retains
  its original `../review/FINDING-CONTRACT.md` target; the corresponding
  canonical `skills/custom/review/FINDING-CONTRACT.md` exists, while rewriting
  the fixture would invalidate its accepted control hash;
- `git diff --check`: passed;
- `git diff --cached --check`: passed;
- Global bootstrap: deliberately skipped because no bootstrap change belongs
  to this promotion.

Relationship delta: none. Research update: none. This record enters the
separately authorized Deploy Prompt 6 commit; that unit returns the exact
commit identity.

## Mechanical Proof

- `python -m pytest tests/test_experimental_skill_contracts.py -q`:
  `11 passed`
- `python -m scripts.pytest_focused`: `59 passed`
- `python -m scripts.validate_skills`: passed
- `git diff --check`: passed
- `git diff --cached --check`: passed
- candidate-local Markdown links: none
- package inventories: exact
- current/pre-prune byte equality: passed
- relationship document diff: empty
