# TDD Candidate, Evaluation, Promotion, And Install Evidence

Status: `complete`; Deploy Prompt 5 promotion and managed installation verified

Authority: Deploy Prompts 3 through 5. This record freezes the candidate,
records pruning equivalence, and closes canonical promotion and managed
installation. It contains no Git delivery.

## Identity And Provenance

| Role | Path | Tree SHA-256 | Provenance |
| --- | --- | --- | --- |
| Current canonical | `skills/custom/tdd/` | `2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae` | Repository fixed point `781f6b654feadf08bdfcd79ce33493a19025cf5e` |
| Behavior-complete pre-prune control | `docs/validation/evals/tdd-pruning-pre-prune/` | `2c54693e3c51ed5785430943786bfdd578a6fc4e99f0746de2f027ee16f286ae` | Exact byte-for-byte canonical freeze |
| B0 and C1 | `skills/experimental/tdd/` | `35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c` | Pre-prune control minus one delimited section |

There is one experimental package for both B0 and C1:

```text
B0 tree = C1 tree = 35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c
```

No duplicate C1 directory or file set exists.

## Package Inventories

| Relative path | Pre-prune SHA-256 | B0/C1 SHA-256 | Disposition |
| --- | --- | --- | --- |
| `SKILL.md` | `3c40b46601971434c5a0ab437e3172b02ad59880c06d3c50e6058f74251c3806` | `3c40b46601971434c5a0ab437e3172b02ad59880c06d3c50e6058f74251c3806` | Exact byte preservation |
| `tests.md` | `bc8d44d4966560e89d3a7d423a08c073b91f0e9c55a0b6ef315cb0d7e7e2f374` | `b3738122d3b3b72a66d9e40bd22ec252549ef7077b4d9914cb68f5b8dea67465` | Exact single-section deletion |
| `mocking.md` | `9523c1371ef4c711c69932a42214eef21159f5c20baf36cb1fdcf3e8fd2efa5e` | `9523c1371ef4c711c69932a42214eef21159f5c20baf36cb1fdcf3e8fd2efa5e` | Exact byte preservation |
| `refactoring.md` | `4d1ae71d594a02cdd09f0cef42224969d5deab39091149ab057edae5838097e4` | `4d1ae71d594a02cdd09f0cef42224969d5deab39091149ab057edae5838097e4` | Exact byte preservation |
| `agents/openai.yaml` | `d9ef3372e04c488b227009cd14ef0ed84fa4335056d48219bc6cbf8a80a970bd` | `d9ef3372e04c488b227009cd14ef0ed84fa4335056d48219bc6cbf8a80a970bd` | Exact byte preservation |

Both packages contain exactly these five files and no empty directory or
additional schema, script, template, asset, or helper.

## Baseline Adaptation Delta

The simplest credible upstream is Matt Pocock TDD at
`ed37663cc5fbef691ddfecd080dff42f7e7e350d`. B0 preserves the upstream core of
one behavior-first vertical red-green cycle, public or meaningful seams,
independent expectations, minimal GREEN, and disclosed test/double guidance.

Mandatory local adaptations already present in the preserved bytes are:

- implicit discovery with the four-fact bug gate;
- agent-owned technical seam choice and caller-owned commitment decisions;
- caller-owned delivery closeout;
- explicit invalid-RED and safe-quarantine boundaries;
- focused plus nearest relevant GREEN proof;
- GREEN-only in-slice REFACTOR;
- conditional engineering, domain, test-taste, mocking, and refactor pointers;
- original-caller and scoped follow-up relationships; and
- a compact proof Return and inner-loop completion boundary.

## Exact Pruning Delta

Delete from `tests.md` exactly the complete section beginning
`## Async Waiting` and ending immediately before `## Red Flags`, including its
two explanatory paragraphs and both Python examples. No other byte changes.

The removed guidance is deferred rather than behaviorally disproved. Prompt 4
must test pruning equivalence under asynchronous pressure before promotion.

## Current-Runtime Disposition Ledger

| Current behavior group | Disposition in B0/C1 |
| --- | --- |
| Invocation policy and description | Preserve exact bytes |
| Caller boundary, Diagnosis and Prototype handoffs | Preserve exact bytes |
| Engineering/domain and three branch pointers | Preserve exact bytes |
| TRACE tuple, seam choice, harness gate | Preserve exact bytes |
| RED order, validity branches, quarantine, after-the-fact honesty | Preserve exact bytes |
| Minimal GREEN, nearby validation, assertion protection | Preserve exact bytes |
| GREEN-only refactor, coverage reconciliation, compact Return, completion | Preserve exact bytes |
| Tracer-bullet, public-behavior, independent-oracle examples and red flags | Preserve exact bytes |
| Async Waiting guidance | Delete from B0/C1; defer pending Prompt 4 result or a future admission |
| Double order, fake example, fidelity gate, contract proof, risk Return | Preserve exact bytes |
| Refactor moves, proof cadence, stop rules, and three scoped recommendations | Preserve exact bytes |

## Research Disposition Ledger

| Pressure | Disposition |
| --- | --- |
| RED-GREEN-REFACTOR and tracer bullet | Source-correct semantic foundation already present in B0 |
| Public interface/seam and independent oracle | Core outcome and supporting rationale; retain |
| Deep module, depth, leverage, locality | Supporting refactor rationale; no contribution claim |
| Context pointers and progressive disclosure | Required local information hierarchy; retain |
| Evidence before claims and completion criterion | Required local contract; retain |
| Classicist term | Defer term contribution; retain observable double rules |
| Async condition waiting | Defer and remove; no observed baseline failure admitted it |
| Source books and articles | Synthesis rationale only; no runtime load |
| Superpowers deletion, universal invocation, and no-exceptions rhetoric | Reject |
| Typed schemas, transition tables, helper, state ledger | Reject |

## Unified Mechanism Ledger

| Mechanism | Admission basis | Owner | Destination | Prompt 3 result |
| --- | --- | --- | --- | --- |
| Invocation and four-fact bug gate | Required local contract; safety boundary | TDD, Diagnosis, callers | `SKILL.md`, metadata | Preserved |
| Caller delivery boundary | Required local contract | Caller and TDD | `SKILL.md` | Preserved |
| TRACE and red-capable harness | Core outcome; local contract | TDD | `SKILL.md` | Preserved |
| Valid behavioral RED and safe quarantine | Core outcome; proof and safety boundary | TDD | `SKILL.md` | Preserved |
| Minimal GREEN and nearest proof | Core outcome; completion contract | TDD | `SKILL.md` | Preserved |
| GREEN-only refactor | Core local outcome; relationship contract | TDD | `SKILL.md`, `refactoring.md` | Preserved |
| Independent oracle and test taste | Core outcome | `tests.md` | Disclosed reference | Preserved |
| Double fidelity | Non-intuitive proof boundary | `mocking.md` | Disclosed reference | Preserved |
| Scoped refactor recommendations | Required local relationship contract | `refactoring.md` and callees | Disclosed reference | Preserved |
| Compact proof packet | Required caller contract | TDD | `SKILL.md` | Preserved |
| Typed schemas and transition tables | None | None | Non-runtime only | Rejected |
| Async waiting | None; no observed baseline failure | `tests.md` if later admitted | Deferred | Deleted from B0/C1 |
| Persistent helper, schema, or state ledger | None | None | None | Rejected |

C1 has no admitted additions, so every candidate instruction is either B0,
minimum context/pointer, or disclosed B0 reference. There is no
mechanism-contribution claim.

## Protected Behavior Set

- implicit invocation and adjacent routing exclusions;
- the four-fact bug gate and non-bouncing original-caller return;
- caller-owned scope and delivery closeout;
- TRACE behavior, source, seam, oracle, and command;
- trustworthy automated RED or an honest support gap;
- pre-implementation behavioral RED and invalid-RED classification;
- current-cycle-only quarantine and unrelated-work preservation;
- minimal GREEN, nearby validation, and correct-assertion preservation;
- GREEN-only behavior-preserving refactoring;
- materially distinct behavior coverage without data-variation inflation;
- conditional test-taste, double, and refactor loading;
- real owned modules and fidelity-checked boundary doubles;
- scoped recommendations that stop; and
- compact proof Return and inner-loop completion.

## Instruction Classification And Pruning Ledger

| Candidate unit | Classification | Reason |
| --- | --- | --- |
| `SKILL.md` frontmatter and policy | B0 | Required invocation contract |
| Outcome, observed-RED invariant, caller boundary, handoffs | B0 | Core outcome, local contract, safety |
| Three reference pointers and repo pointers | Minimum context or pointer | Required conditional loading and platform ownership |
| TRACE section | B0 | Core outcome and admission evidence |
| RED section | B0 | Irreversible order, proof truth, safe failure |
| GREEN section | B0 | Smallest implementation and compatibility gate |
| REFACTOR section | B0 | Locally selected GREEN-only core outcome |
| RETURN section and completion sentence | B0 | Caller resumption and demanding completion |
| `tests.md` tracer-bullet example | Disclose | Branch-only test-shape reference |
| `tests.md` public-behavior contrast | Disclose | Branch-only seam reference |
| `tests.md` independent-oracle contrast | Disclose | Branch-only oracle reference |
| Pre-prune Async Waiting section | Delete | Deferred mechanism without admission basis |
| `tests.md` red flags | Disclose | Branch-only test-shape pressure |
| `mocking.md` substitute order and example | Disclose | Branch-only double selection |
| `mocking.md` fidelity gate and risk handling | B0 disclosed reference | Non-intuitive proof boundary |
| `refactoring.md` GREEN boundary, moves, proof, stop | B0 disclosed reference | Core refactor behavior |
| `refactoring.md` three recommendations | B0 disclosed reference | Accepted ownership edges |

No candidate clause is classified as an admitted C1 addition. No further cut
is authorized by Prompt 3.

## Affected Relationships

Relationship delta: none.

The candidate preserves exact `SKILL.md` and `refactoring.md` bytes, so the
accepted edges remain byte-identical: Implement and Parallel Implement invoke
TDD; TDD and Diagnosis exchange only across the four-fact gate while retaining
the original caller; TDD hands design evidence to Prototype; and GREEN
out-of-slice results recommend Simplify Code, Codebase Design, or Improve
Codebase and stop. `docs/synthesis/skill-context-relationships.md` was not
edited.

## Claim-To-Proof Matrix

| Lane | Claim | Current evidence | Prompt 4 obligation |
| --- | --- | --- | --- |
| Semantic fidelity | Retained words keep the selected TDD meaning | Exact byte preservation plus synthesis trace | Inspect only if a semantic claim is challenged |
| Mechanism contribution | None; B0 equals C1 | Identical package identity | Do not run contribution arms |
| Current-contract preservation | All protected behavior except deferred async prose remains discoverable | Exact hashes, structural test, relationship parity | Representative positive, failure, wrong-condition, and async-pressure cases |
| Pruning equivalence | Removing Async Waiting does not reduce admitted behavior | Exact pre-prune and candidate fixtures | Compare frozen packages under identical neutral tasks and rubric |
| Invocation/context loading | Metadata and remaining pointers are unchanged | Byte parity and pointer resolution | Should/should-not invoke and branch retrieval/application |
| Deterministic identity | Only `tests.md` changed by one section | Inventory, per-file hashes, tree hashes, exact-delta test | Recheck after any repair |

## Prompt 4 Pruning-Equivalence Result

The frozen pre-prune control and final C1 were compared on one neutral set of
nine fixed cases in five fresh contexts per arm. The cases included observable
asynchronous completion, exact trigger-relative timing, uncertain async bug
routing, invalid RED, unrelated baseline failure, assertion and owned-module
pressure, boundary-fake fidelity, refactor scope, and incomplete Return.

Result: control 45/45 protected cases and C1 45/45; control 10/10 async cases
and C1 10/10; zero critical failures in either arm. One C1 sample contained a
noncritical contradictory sentence about an expected RED being observed, but
the same response rejected completion and required the full observed proof
packet. This was admitted as one bounded advisory, not a protected-behavior
failure.

The complete protocol, rubric, decision, and ten raw schema-valid responses
are in `docs/validation/evals/tdd-pruning-results/`.

Decision: `accepted`. Equal behavior supports the removal; no control failure
was required because this is a pruning-equivalence claim.

## Known Limits And Residual Load

- Pruning equivalence is supported only for the fixed Prompt 4 cases, runtime,
  and five-sample arms; it is not a universal equivalence claim.
- Prompt 4 observed exact parity on condition waiting, timeout diagnostics,
  and cases where elapsed time is itself the behavior.
- The pre-prune package is a local fixed-point control; upstream checkouts were
  not network-refreshed.
- Prompt 3 did not inspect installed parity; Prompt 5 later verified it at the
  accepted hash.
- The unavoidable runtime load is the five-operation common path, local
  authority and safety gates, three conditional references, and the compact
  Return/completion contract.
- Any candidate byte change invalidates the recorded B0/C1 tree identity and
  the affected later proof.

## Prompt 3 Completion

- Pre-prune control frozen once: complete.
- One shared B0/C1 package materialized: complete.
- Exact deletion and every other byte preserved: complete.
- Manifest and candidate record created: complete.
- Candidate structural proof added: complete.
- Canonical runtime and relationships unchanged: complete.
- Behavioral evaluation, promotion, installation, and delivery: not started.

Decision: `accepted`; ready for Prompt 5 promotion review.

## Prompt 5 Promotion And Installation

Decision: `complete`.

Prompt 5 promoted accepted C1 hash
`35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c`
byte-for-byte into `skills/custom/tdd/`. Read-back proved that the only
canonical delta from the frozen pre-prune control is deletion of the complete
Async Waiting section from `tests.md`; the other four package files remain
byte-identical. The Prompt 4 wording advisory was not applied, so no untested
candidate byte was introduced and the accepted behavioral evidence was reused
without another evaluation wave.

The relationship index remained unchanged at SHA-256
`c7884bb944715cfda8c295e75b90117137d0b76fb637b3c63a6a58065c46dc22`.
Only `skills/experimental/tdd/` and TDD's manifest entry were retired. Every
other experimental candidate and manifest entry was preserved. The pre-prune
control, Prompt 4 protocol, rubric, raw responses, and decision remain durable
validation evidence rather than active experimental runtime.

Canonical proof before lifecycle cleanup:

```text
canonical tree hash
35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c

accepted experimental tree hash
35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c

python -m scripts.validate_skills
Skill validation passed.

python -m pytest
192 passed, 4 skipped
```

After cleanup, the focused canonical single-cut proof passed 9 tests and skill
validation passed. The managed installation gate then reported exactly:

```text
Managed skills: 25 in C:\Users\steve\.agents\skills
Updated skills: tdd
Unchanged skills: 24
Global bootstrap: skipped
```

The supported installer synchronized the managed pack with the global
bootstrap deliberately skipped. Canonical and installed TDD now share exact
tree hash
`35bbe08d4f3ce1d137ae12bf3fd1e2a8bc1b75dd3f234d2266c020467e1e3e7c`.
Installed-root validation requiring all custom skills passed, and the
post-install dry-run reports all 25 managed skills unchanged.

Final current-state Lock also passed the full repository suite with 192 tests
passed and 4 skipped, the 9-test focused contract file, repository and
installed-root skill validation, and both worktree and staged whitespace
checks.

No relationship edit, behavioral rerun, advisory wording edit, unrelated
experimental cleanup, global bootstrap edit, staging, commit, or push was
performed. Deploy Prompt 5 stops before Git delivery.
