# To Tickets Deploy Pruning Pass V2 Evidence

## Decision

Decision: `complete`.

Pruning disposition: `pruning-not-needed`.

The complete runtime-facing V1 package contains only `SKILL.md` and
`agents/openai.yaml`. The nested `controls/m0` package is immutable Prompt 4
evidence, not a runtime-facing P1 input. No material behavior-preserving cut
survived the audit, so exact P1 is byte-identical to exact V1. No candidate,
control, metadata, manifest, canonical, installed, relationship, or test byte
changed.

## Frozen Input And Output Identities

| Identity | SHA-256 |
| --- | --- |
| V1 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| V1 `SKILL.md` | `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` |
| V1 metadata | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |
| Prompt 4 manifested workspace, including immutable M0 | `e8d7e55ba09a7174aad65e4e5b4add539cb029d3e3753dee35c366de402f0c05` |
| P1 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| P1 `SKILL.md` | `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` |
| P1 metadata | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |

The V1/P1 runtime load is 6,874 bytes: `SKILL.md` is 6,831 bytes, 908
whitespace-delimited words, and 133 lines; metadata is 43 bytes, 3 words, and
2 lines. P1 load delta is exactly 0 bytes, 0 words, and 0 lines.

The start `HEAD` was
`dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6`. Protected concurrent files read
back as:

- `docs/synthesis/methods/deploy-prompts.md`:
  `7c50065bf...abe95b53e9`; and
- `tests/test_deploy_prompt_contracts.py`:
  `555b6b055...5cbc4c8b15b2`.

## Complete Runtime Passage Audit

Every instruction-bearing passage is classified below. `keep` means the
passage remains exact V1 bytes in P1.

| Runtime passage | Class | Protected unit or reason |
| --- | --- | --- |
| `SKILL.md` lines 1-4 | `keep` | M0-01 name and settled-source invocation outcome |
| lines 8-9 | `keep` | M0-01 outcome plus M0-03/M0-05/M0-06 exhaustive, ordered ticket result |
| lines 11-15 | `keep` | M0-01 admission, intent preservation, authority, exclusions, and owner stops |
| lines 17-21 | `keep` | M0-02/M0-05/M0-08/M0-10/M0-11 owner boundaries and local ownership |
| Shape lines 25-29 | `keep` | M0-02 setup gate, exact safe Return, unchanged state, and `$repo-bootstrap` relationship |
| lines 31-36 | `keep` | M0-03 complete Source Trace plus commitment-changing source-gap Return and delivery-owner fence |
| lines 38-40 | `keep` | M0-03 exhaustive commitment ledger and exact disposition set |
| lines 42-46 | `keep` | M0-04 vertical default, observable support/migration exception, and separate-completion criterion |
| lines 48-57 | `keep` | M0-05 complete ticket facts, proof, write scope, blockers, order, and parallel judgment |
| lines 59-61 | `keep` | M0-05 tracker Ready contract, unready state, and complete defect Return |
| lines 63-67 | `keep` | M0-06 true-blocker predicate, graph defects, non-blockers, and truthful ordered frontier |
| lines 69-74 | `keep` | M0-07 execution-profile fields and safety-driven serial constraints |
| lines 76-80 | `keep` | M0-08 applicable state-boundary matrix and explicit stateless disposition |
| lines 82-85 | `keep` | M0-04 compatibility safety, expand-migrate-contract order, delayed irreversible contraction, and proof |
| lines 87-88 | `keep` | M0-03/M0-13 no-ticket coverage Return, unchanged tracker, `none`, and stop |
| Publish lines 92-93 | `keep` | M0-05 readiness and settled category-role authority |
| lines 95-101 | `keep` | M0-09 complete pre-mutation freeze plus M0-10 design gate, irreversible mutation order, tracker ownership, and parent-intent safety |
| lines 103-107 | `keep` | M0-11 affected-dependent read-back, mismatch branch, partial-publication recovery, and no false completion |
| Return lines 111-114 | `keep` | M0-13 exhaustive typed Return set, evidence, observed state, gaps, and safe continuation |
| lines 116-125 | `keep` | M0-12/M0-13 published-graph contents and exact `$parallel-implement` / `$implement` / `none` relationship predicates |
| line 127 | `keep` | M0-12 recommend-and-stop boundary |
| lines 129-133 | `keep` | Checkable M0-01 through M0-13 successful-completion criteria and unstarted successor |
| `agents/openai.yaml` lines 1-2 | `keep` | M0-01 explicit-only invocation authority |

No passage qualifies for `collapse`, `disclose`, or `delete`. The package has
no disclosed runtime helper or unused runtime support.

## Rejected Cut Opportunities

These were audit probes, not constructed P1 variants. Their named load is the
maximum surface considered, not a claimed achievable reduction.

| Opportunity | Affected units | Expected unchanged behavior | Maximum surface | Decision |
| --- | --- | --- | --- | --- |
| R1: fold the body outcome into metadata | M0-01, M0-03, M0-05, M0-06 | Preserve explicit settled-source admission and exhaustive ordered output | lines 8-9: 122 bytes, 15 words | Reject: the description is an invocation pointer while the body statement is the runtime outcome; the saving is immaterial and equivalence is unproved |
| R2: replace the explicit owner allocation with a generic contract pointer | M0-02, M0-05, M0-08, M0-10, M0-11, M0-12 | Preserve every rule, transport, proof, state, Return, and relationship owner | lines 17-21: 362 bytes, 39 words | Reject: copied procedure is already absent; removing the local ownership slice risks authority and relationship drift |
| R3: compress execution-profile fields and serial tripwires | M0-07 | Preserve ownership, writes, proof-resource, ordering, safety, and independence judgments | lines 69-74: 402 bytes, 48 words | Reject: each field or tripwire maps to the required local contract and distinct viability cases; no neutral shorter expression is evidenced |
| R4: disclose the state-boundary matrix behind the engineering-contract pointer | M0-08 | Preserve stateful branch coverage and explicit stateless reasoning in every ticket | lines 76-80: 359 bytes, 47 words | Reject: applicability is a common-path per-ticket gate; the local inclusion rule and stateless branch cannot be delegated to foreign reference |
| R5: merge typed Return and completion | M0-13 plus all success gates | Preserve terminal result shape, safe failure, evidence, and successful-publication completion | Return lines 111-114: 277 bytes, 35 words; completion lines 129-133: 348 bytes, 47 words | Reject: Return specifies observable terminal packets; Completion independently proves when the successful branch is complete |

No cut has both a material named load reduction and a justified expectation of
unchanged protected behavior. Per the no-cut branch, no combinations,
micro-cuts, P1 fixture, or behavioral evaluation wave were created.

## Proof

Reused exact Prompt 4 evidence:

- clean M0 viability: `16/16`, zero critical failures;
- H1-01: rejected with M0 deficit `0/5`;
- H1-02: rejected after H1 retained the M0 deficit `5/5`;
- H1-03: rejected with M0 deficit `0/5`; and
- exact-V1 repository suite: `205 passed, 4 skipped`; and
- exact V1 refreeze and isolated worker/root-evaluator fixture separation in
  `../isolation-v2`.

Fresh pruning proof:

- complete runtime inventory and passage audit;
- exact V1/P1 byte and load read-back;
- isolation-v2 candidate verifier;
- focused repository checks: `59 passed`;
- skill-pack integrity validation;
- both diff checks; and
- final `HEAD` and protected-file hash read-back.

Because P1 equals V1 byte-for-byte, Prompt 4 V1 arms remain exact reusable
evidence and no new behavioral-equivalence claim or behavioral wave is needed.
The full suite was not rerun because no runtime, metadata, manifest, machine
contract, canonical package, relationship, or test byte changed.

## Residual Gaps

- live-provider publication, read-back, idempotency, eventual consistency,
  mutation durability, and duplicate avoidance;
- transfer beyond the exact Prompt 4 model, host, reasoning, tasks, authority,
  tools, and simulated tracker;
- unavailable backend build, seed, temperature, hidden system prompt, token
  count, independent host attestation, and live-provider timing; and
- support-work comparative economics when source facts do not settle them.

These are inherited Prompt 4 limits. They do not block exact V1 from serving
as exact P1.
