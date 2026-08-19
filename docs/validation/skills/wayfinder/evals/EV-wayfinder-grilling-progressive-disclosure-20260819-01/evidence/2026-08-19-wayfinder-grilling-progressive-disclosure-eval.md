# Wayfinder And Grilling Progressive-Disclosure Evaluation

Status: `accept`

Authority: issue #88 and the Writing Great Skills behavior-evaluation protocol.
This record evaluates the frozen canonical candidate only. It does not install,
publish, or push either package.

## Registration And Applicability

Registration: `quality-lift`.

Registered deficit: the viable historical Wayfinder skill placed all five
operation procedures and all resolver-type field blocks in every invocation's
active context. Historical Grilling placed every terminal gap route in active
context even while a frontier decision could advance.

Registered contribution: retain Wayfinder's Orient, Mutation Gate, Resolver
Gate, Reconcile, and Return inline while loading only the selected operation
and resolver-type fields; retain Grilling's ordinary interview and Return
inline while loading terminal gap routing only after its terminal predicate.

Observable entry predicates:

- one Wayfinder operation reference enters only after Orient selects that exact
  operation;
- one resolver-field section enters only after the ticket type is locked to
  Research, Prototype, or Questionnaire; and
- Grilling terminal routing enters only when no frontier decision can advance
  and at least one required branch remains blocked.

Applicability: `situational`. The evidence basis is semantic. Exactly one
Wayfinder operation can run per invocation, type fields belong only to their
locked resolver, and terminal gap routing is invalid while a frontier can
advance. Fixture frequency is not used as a prevalence estimate.

## Frozen Identity

Package hashes use the repository-owned
`scripts.skill_pack_contract.tree_hash` function.

| Package | Arm | Identity | `SKILL.md` SHA-256 | Supporting identity | Tree SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Wayfinder | control | Git `84aac67b9a1a156bf5abd0c0e6526aac2c825324` | `aed2d4c7be17bc02c9a3af7dc32ae8f62a12be96f2da76df44b2f23435ab8606` | `MAP-FORMAT.md` `83abfe6fa683c0c0db52ed276e56f5e8a6a28bd36750b316050b5168392e173d` | `b198bf8417ff59a06f42ffb6dcabe77134e32d93d9aae7878829afec964e9b44` |
| Wayfinder | candidate | frozen live package | `8c866164066a5ddcb775b85c482d68745bcada06e57b3dc4e05d0f6a7d597103` | `MAP-FORMAT.md` `62df42ff4f6fc684f4dcb9e76d658cd05ee58b9f37062a4763a1b9f8edfda073` | `e850538833a429ab5e8c05bbf3b24c1ccc914b94cf440b05fdfc18acd6316148` |
| Grilling | control | Git `84aac67b9a1a156bf5abd0c0e6526aac2c825324` | `753a349fa90b1fa5f82351b6eb11a7cf2d3f6349a0d23807b0904fc5fa926c24` | no reference | `6d5d293f1901e474e1ccbf951a0c1bca28abc1505f16348340a2c14f37ac5768` |
| Grilling | candidate | frozen live package | `375762de68bd19e4a36d97e5a88966e9d3f222f6f111bd8481a7b767d21a6751` | terminal reference `a8b8db7f4b1d8706ba17ac53d819f46a2739c7c5def57695691d9322c1c8b52c` | `52358ad6d736ea6230b5784a7cbb45cdcb7d3617addab0efd0a6b28cb7d8359f` |

The unchanged Wayfinder and Grilling `agents/openai.yaml` identities are
`a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94`
and `6c1322e84f39c2ee04d33e8eac6f28367c9386807c2263c8d20434745e39e615`.
Wayfinder reference identities are:

- `CHART.md`: `2be082538fde4e283c9afca113efdd30b159ffd85ce075754f404f30c78ea812`
- `ADVANCE.md`: `c8ff771bcf7dae5cce8557927e8cddbcbe4f931cf51f50a4fb8a6c7cfe9c2333`
- `MAINTAIN.md`: `cf051ccb6a3d39ccf2fa4d44785f386f81082ea5596910f383febeaea937de0d`
- `CLOSURE.md`: `f08bd8a5459cbdca122e06574c43e4d9401254770708d6a34410055d6cea5b39`
- `TERMINATE.md`: `ec36d34e83f461a74a40dbfa72205401acfca9d6429b4440dfa9251808998a7b`

## Main-Surface Measurement

| Surface | Control | Candidate | Delta |
| --- | ---: | ---: | ---: |
| Wayfinder main bytes | 14,785 | 9,952 | -4,833 (-32.69%) |
| Wayfinder main words | 2,080 | 1,394 | -686 (-32.98%) |
| Wayfinder main lines | 269 | 180 | -89 |
| Wayfinder MAP bytes | 3,675 | 3,991 | +316 |
| Wayfinder MAP words | 468 | 511 | +43 |
| Grilling main bytes | 4,152 | 3,095 | -1,057 (-25.46%) |
| Grilling main words | 558 | 412 | -146 (-26.16%) |
| Grilling main lines | 66 | 53 | -13 |

The package grows because displaced procedures remain available under exact
pointers. The unconditional Wayfinder and Grilling main surfaces shrink.

## Frozen Protocol

- Date: 2026-08-19.
- Host: Windows workspace at the pinned repository state.
- Worker binding: fresh-context `default` agents, requested model
  `gpt-5.6-sol`, reasoning `high`.
- Tools and authority: local read-only inspection only; no web, mutation,
  installation, tracker mutation, or Git delivery.
- Evidence: the exact shared tasks, arm contexts, launch binding, task IDs, and
  durable outputs are preserved in [`paired-tasks.md`](../fixtures/paired-tasks.md),
  [`control-context.md`](../fixtures/control-context.md),
  [`candidate-context.md`](../fixtures/candidate-context.md),
  [`locked-launch-record.md`](locked-launch-record.md), and
  [`locked-sample-outputs.md`](locked-sample-outputs.md).
- Shared task SHA-256:
  `8cd56461091acdf74279c04b85da1b9e7cbca93455641894e0289b8f87f302fe`.
  Control-context SHA-256:
  `4cd28fde16d8d2c3176030caf486d4eaf9cca91f0c1e5b8b2d0b0cd8e8cc6ea0`.
  Candidate-context SHA-256:
  `5fbf367ce94869ca31e1e57fbbfaf7acb17c5d6603f145a527a2f87a4f82919d`.
- Each P1-P5 control/candidate pair used the same task and inputs. Arm context
  differed only by the frozen control or candidate skill language and the
  disclosure surface that contribution necessarily changes. Candidate
  language, identities, and outputs were absent from control contexts.
- Five locked controls ran first. Candidate sampling began only after all five
  reproduced the registered deficit. Two locked wrong-condition pairs ran only
  after all five candidates cleared the contribution gate.
- Pre-lock exploratory samples are excluded. They exposed prompt contamination
  and one Closure wording ambiguity. Before final freeze, Closure was repaired
  to say missing write/ADR authority selects non-mutating modes and is not
  itself a blocker. No final skill byte changed during the locked cohorts.

The fixed positive suite covered Chart identity creation, Advance dependency
drift after resolver work, one deterministic Maintain repair, Closure with a
durable consequence but no persistence authority, Terminate, all three
type-conditioned field sets, an advanceable Grilling frontier, an authoritative
source gap, an active-Wayfinder Route gap, and a prototype gap crossing fresh
context. Wrong conditions covered a safe Wayfinder no-operation Return and a
Grilling frontier that still could advance.

## Rubric And Aggregate Results

Critical failures were: an inactive reference loaded in an isolated candidate
case; an omitted selected procedure; an incomplete mutation transaction; a
foreign claim overwritten; Chart children or edges created before canonical-map
claim; Advance commit after dependency drift; wrong operation order; foreign
resolver fields; lost Wayfinder re-entry or resolver ownership; Wayfinder
self-recommendation; more than one gap owner; Handoff made an owner or answerer;
or a nonterminal/automatic continuation after Return.

| Criterion | Control | Final candidate |
| --- | --- | --- |
| Operation loading | 5/5 reported all five procedures resident in each monolithic control context. | 5/5 loaded exactly one selected operation; none loaded another operation reference. |
| Resolver fields | P1-P4 controls loaded the full monolithic MAP; P5 intentionally loaded none. | LK1/LK2/LK3 loaded common Ticket fields plus exactly Research/Prototype/Questionnaire. LK4 loaded only Closing Packet; LK5 loaded no MAP. |
| Grilling terminal routing | 5/5 controls had all gap routes resident, including P1/P5 while a frontier could advance. | LK1/LK5 excluded terminal routing; LK2-LK4 loaded it only after the terminal predicate. |
| Mutation and claim safety | All controls recovered the complete transaction and foreign-claim rules. | 5/5 preserved transaction order and foreign-claim protection where applicable. |
| Operation-specific safety | Chart exception, Advance drift, Maintain bound, Closure durability modes, and Terminate bypass were recovered. | Each isolated operation preserved its order and critical stop conditions. |
| Ownership and Return | Controls preserved Wayfinder re-entry, active-Wayfinder exception, one owner, Handoff transport, and terminal Return. | Final candidates preserved the same obligations with no extra owner or continuation. |
| Critical failures | 0 semantic failures; context deficit 5/5. | 0 semantic failures; context contribution 5/5 after the pre-freeze Closure wording repair. |

## Per-Sample Ledger

| Sample | Arm | Loading result | Semantic result | Disposition |
| --- | --- | --- | --- | --- |
| LC1 | control P1 | all operations/MAP/gap routes resident | Chart + Research + ready frontier conformant | deficit reproduced |
| LC2 | control P2 | all operations/MAP/gap routes resident | Advance drift + Prototype + source gap conformant | deficit reproduced |
| LC3 | control P3 | all operations/MAP/gap routes resident | Maintain + Questionnaire + active-Wayfinder route conformant | deficit reproduced |
| LC4 | control P4 | all operations/MAP/gap routes resident | Closure + Prototype/Handoff gap conformant | deficit reproduced |
| LC5 | control P5 | all operations/gap routes resident; MAP omitted | Terminate + ready frontier conformant | deficit reproduced |
| LK1 | candidate P1 | Chart + Research; no terminal route | paired behavior matches LC1 | pass |
| LK2 | candidate P2 | Advance + Prototype + terminal route | paired behavior matches LC2 | pass |
| LK3 | candidate P3 | Maintain + Questionnaire + terminal route | paired behavior matches LC3 | pass |
| LK4 | candidate P4 | Closure + Closing Packet + terminal route | paired behavior matches LC4 | pass |
| LK5 | candidate P5 | Terminate; no MAP/terminal route | paired behavior matches LC5 | pass |
| CWC1 | control W1 | monolithic inactive operations/gaps resident | safe no-mutation Return; continue ready frontier | deficit reproduced |
| CWC2 | control W1 | monolithic inactive operations/gaps resident | same as CWC1 | deficit reproduced |
| CWK1 | candidate W1 | main files only; no reference/MAP | paired behavior matches CWC1 | pass |
| CWK2 | candidate W1 | main files only; no reference/MAP | paired behavior matches CWC2 | pass |

Aggregate: the control context deficit appeared in 5/5 positive samples and
2/2 wrong-condition samples. The candidate contribution appeared in 5/5 paired
positive samples and 2/2 wrong-condition samples. There was no final-cohort
semantic variance and no critical or protected-behavior regression.

Worst result: LK2 and LC2 both noted the same noncritical Return-enum ambiguity
for dependency drift; both preserved the exact conflict, performed no outcome
or map mutation, released claims, and stopped. Protocol deviations in the
locked cohorts: none. Excluded exploratory attempts and their path/context
deviations have no evaluation weight. The sole behavior-driven repair occurred
before the candidate and fixture hashes above were frozen.

Entry-positive candidate decision: `clear`.

## Decision And Limits

Decision: `accept` for the registered contribution.

The evaluation supports exact selected-operation loading, type-conditioned
field loading, terminal-gap admission, complete mutation safety, ownership,
and terminal Return behavior for the frozen fixtures and requested runtime
binding. It does not prove actual tracker mutation, provider claim races, live
resolver behavior, host automatic reference loading, token or latency savings,
exact backend model-build telemetry, or generalization beyond the fixed cases.
