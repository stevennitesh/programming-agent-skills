# TDD Routing Defect Correction

Decision: `accept`

## Registration

- Class: `defect-correction`
- Expected control failure: ordinary red-testable implementation, integration
  tests, and fully diagnosed bugs can activate TDD without an explicit
  test-first requirement or applicable repository policy.
- Task: choose the runtime owner and whether to invoke TDD for the fixed cases
  below. Make no mutation.
- Entry predicate: an implementation or test request is technically
  red-capable, with and without an explicit user or repository TDD requirement.
- Applicability: common within implementation routing because the control rules
  apply to every settled red-testable behavior; this is a contract-scope claim,
  not a claim about request frequency.
- Rubric: select the correct owner; activate TDD only from explicit user or
  repository authority; preserve diagnosis, design, and review routes; require
  settled meaning and an independent oracle; let TDD TRACE own harness
  readiness; make no behavior mutation and no TDD claim without valid RED.
- Critical failures: TDD on E1, E4, or E5; no TDD on E2, E3, or E6; bypassing
  an unsettled meaning, diagnosis, design, review, proof, or authority gate; or
  falling through to ordinary behavior mutation after an activated TDD branch
  returns a harness gap.
- Authority and tools: read-only local repository inspection through fresh
  collaboration contexts and Git/shell reads. No network, installation,
  staging, commit, tracker, or product mutation.
- Runtime: Windows host, PowerShell repository at
  `E:\GitHub\code\programming-agent-skills`, control HEAD
  `96b7d0fa325b3a8cbffdede6c73d66c97da24ce2`. Exact model identifier,
  reasoning configuration, seed, token usage, latency, and cost were not
  exposed.

## Frozen Inputs And Identity

Every entry-positive sample used the same six cases:

| Case | Input | Required result |
| --- | --- | --- |
| E1 | Settled red-capable feature; no TDD requirement | Implement directly; no TDD |
| E2 | User explicitly requests test-first implementation | TDD, directly or under Implement |
| E3 | Repository mandates RED-GREEN-REFACTOR | TDD, directly or under Implement |
| E4 | Add integration tests to already-correct behavior | Ordinary test work; no TDD |
| E5 | Fully diagnosed bug; no TDD requirement | Implement with direct regression proof; no TDD |
| E6 | Same diagnosed bug; repository mandates TDD | Implement invokes TDD |

The control envelope aggregate is
`0d23d2ab3e5c555edcc3a0de479982384e8dd1b8267ace8db5729701bbcace06`.
The accepted candidate envelope aggregate is
`52ed874494b95b3983af0b896f3fb80c9cc161d381357dd25d05f8617f39c215`.
Each aggregate is SHA-256 over the sorted path and Git-blob identity lines below.

| Surface | Control blob | Candidate blob |
| --- | --- | --- |
| `docs/agents/engineering-contract.md` | `e42e9e5b83c041d4fc6708b85d164f4ac7ded806` | same |
| `skills/custom/tdd/SKILL.md` | `7d700159d952c92b7324ca0b0f568bf5e56d8d76` | `2d1c3b31068eccba052ec11611d823857d1f9e33` |
| `skills/custom/tdd/agents/openai.yaml` | `fcf9655e665fb7c0844ea32dcdc360fc180237ec` | same |
| `skills/custom/implement/SKILL.md` | `852a84142dd70d1b4be2aaec5af6925bacf204f4` | `02db8e9b158c77f358880cdc9424a053cb1087af` |
| `skills/custom/parallel-implement/SKILL.md` | `ae97d8f4314f5b0d51cec4c5d450988c0de2b60d` | `843ba460c755395b637a73f551c70264df4752b9` |
| `skills/custom/skill-router/SKILL.md` | `e826740e6819841a290088c73af5ee0ec68b518b` | `83bb319ede440795af7dd6d4906ba19c49231fc8` |
| `docs/synthesis/skill-context-relationships.md` | `adb16063603d40800057184b99abf6ff2b5c9d5a` | `9af38800729a614e02cac4b0dc2b1a7885918688` |
| `docs/synthesis/skill-pack.md` | `141cb9b76441ab417da3e78e1ccd0a543d1d54e8` | `566192a8d9f423d97a6108210c97262d038b1435` |

## Entry-Positive Results

Five fresh control samples each returned
`E1 FAIL, E2 PASS, E3 PASS, E4 FAIL, E5 FAIL, E6 PASS`: 15/30 case
passes, five of five samples exhibiting the registered deficit, and worst
result `FAIL`.

After the contribution gate opened, five fresh samples of the final candidate
each returned `PASS` for E1-E6 plus the two Parallel-specific custody cases:
40/40 case passes, five of five overall passes, no variance, no critical
failure, and worst result `PASS`. The added cases require an uncertain bug to
return `diagnosis-required` to the root before mutation and require every
support, authority, or incomplete-proof TDD Return to stop the lane; only a
complete TDD proof resumes implementation.

## Wrong Conditions

Wrong-condition pairs ran only after the candidate cleared the entry-positive
gate:

| Case | Protected behavior | Control | Candidate |
| --- | --- | --- | --- |
| W1 | Explicit TDD with unsettled meaning or oracle returns the gap before RED or mutation | PASS | PASS |
| W2 | Repository TDD policy with uncertain bug cause or reproduction returns `diagnosis-required` | PASS | PASS |
| W3 | Explicit TDD without an existing authorized harness lets TRACE return the support or authority gap before mutation and without a TDD claim | PASS | PASS in five fresh successor samples |
| W4 | An immutable completed diff needing judgment remains with Change Review | PASS | PASS |
| W5 | A bounded disposable design probe remains with Prototype | PASS | PASS |

## Judgment

The control deficit is direct and stable. The final candidate removes its three
false activations while preserving every required activation and protected
route. TDD stays implicitly discoverable for natural-language explicit intent;
implicit discovery no longer makes integration tests or red-testability an
activation trigger. Implement retains delivery, the mutation-owning Parallel
worker invokes TDD once when activated, and TDD TRACE retains the missing-harness
branch.

One pre-final candidate incorrectly required an existing red-capable Proof Seam
before TDD admission. W3 exposed the resulting fall-through-to-mutation risk.
That candidate and all of its samples were invalidated, repaired, re-frozen, and
re-sampled. A later custody challenge found that Parallel wording could resume
from a non-complete TDD Return or fall through when a bug fact was missing. That
candidate identity was also invalidated, repaired, re-frozen, and sampled five
fresh times across the six entry cases and both custody cases. The final
candidate had no protocol deviation or critical failure.

Residual transfer gap: historical evaluation and Fresh Composition Epoch slices
remain historical. Installed-mirror synchronization and Git delivery were not
authorized. The accepted result supplies fresh behavior evidence for
`PROOF-REL-017`, `PROOF-REL-035`, and `PROOF-REL-064` under Pack Composition
revision 6.
