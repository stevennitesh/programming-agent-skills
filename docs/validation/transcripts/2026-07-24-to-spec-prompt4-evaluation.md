# To Spec Deploy Prompt 4 — M0/H1 Evaluation

Campaign epoch: `2026-07-24-to-spec`

Authorized operation: Deploy Prompt 4 only, using `writing-great-skills` in
Author mode.

Starting Git HEAD:
`f3be70c31dd8f2ae9f12a75248065ef313790bda`

## Input verification

The Prompt 3 manifest, exact packages, inventories, M0 checkpoint, research,
synthesis, semantic ledger, protected behavior, relationship owners, fixtures,
and existing evidence were read before behavioral dispatch.

| Input | Expected | Observed |
| --- | --- | --- |
| Prompt 3 campaign manifest | `64ba711a1a92aca615ad106810ac49894a4aa3e9ae3156b77616bca9ebf8cb5e` | match before authorized update |
| M0 tree | `548af7fd1dd0c581fd472f5652ee0c294381c082ecfc927604300edaf07ddaaa` | match |
| H1 tree | `ac02b5ad3892427cb4cda755c18c4fac381d011a333a85e7b7a6eea88bac94e9` | match |
| M0 bounded checkpoint | `b19edb0b03a176b0e4f903c001f1705587d04a4306bbd05be8c3d625d3f7a726` | match |
| Research packet | `2fecf286bdcdfa8a40269ee59a57e4d996736f447a88db5af15d54cb71215f37` | match |
| Prompt 3 synthesis | `0175b57caa3671a278b6e94d75d19902051e3e1da6f86d9422bc97e0b7d3f7bd` | match before Prompt 4 reconciliation |
| Root-only fixture | `4a4583c89cee71e4e8360a125f2dd7f8855e1ede93d72421d5494aa3e701b320` | unchanged |
| Git HEAD | fixed point above | match |

M0 used only settled C01-C16 obligations and M0-01 through M0-17 semantics.
No research/current-only behavior or H1 candidate language was present. The
minimum proof matrix was frozen before dispatch.

## M0 viability

V01-V22 all passed. The valid minimum suite covered GitHub, GitLab, and Local
Markdown success; caller packets; explicit invocation; setup/source/authority
failures; matching, divergent, and unknown state; commitment and lifecycle
coverage; publication failure and indeterminacy; verified cleanup; downstream
stop; and unrelated-state preservation.

Valid aggregate: 22/22, worst score 9/10, zero critical failures.

Invalid or under-specified attempts received zero credit. Source-completeness
repairs changed no task or rubric, were refrozen, and were rerun in fresh
contexts. The deviation ledger records V04, V14, V15, and V16 repairs and
contamination.

## Comparison controls

Before comparison, worker/root separation and the arm-only delta were
reverified. The final worker fixture contains tasks, source facts, authority,
state, operations, mutation boundary, and requested output. The unchanged
root-only fixture alone contains hypotheses, expected weaknesses, rubrics,
scoring, candidate terms, and conclusions. M0 and H1 share identical
`agents/openai.yaml`; their `SKILL.md` bytes are the sole arm delta.

For each of the 14 distinct fixture families, one M0 control was dispatched and
inspected before the remaining family wave. Every valid sample used
`gpt-5.6-sol`, Codex fresh-context subagent, `xhigh`, and the fixed
fixture-scoped tools.

| Cluster | Valid M0 | Root-held deficit result | Disposition | H1 run |
| --- | --- | --- | --- | --- |
| Q01 / H1-01 | 5 | absent; all reconstruction fields recovered | `rejected-no-control-deficit` | 0 |
| Q02 / H1-02 | 5 | absent; all defects repaired, no false block | `rejected-no-control-deficit` | 0 |
| Q03 / H1-03 | 5 | absent; triggered concerns covered without invention | `rejected-no-control-deficit` | 0 |
| Q04 / H1-04 | 5 | absent; every hop and the one gap branch correct | `rejected-no-control-deficit` | 0 |
| Q05 / H1-05 | 5 | absent; every proof portfolio adequate and low-coupling | `rejected-no-control-deficit` | 0 |
| Q06 / H1-06 | 5 | absent; all actors, benefits, and constraints retained | `rejected-no-control-deficit` | 0 |
| Q07 / H1-07 | 5 | absent; every deferral classification and field correct | `rejected-no-control-deficit` | 0 |

The fixed gate prohibited every H1 dispatch. No candidate effect, candidate
variance, or protected-behavior regression was estimated.

## V1 and proof lanes

No H1 unit survives. V1 is an exact identity alias of M0:
`548af7fd1dd0c581fd472f5652ee0c294381c082ecfc927604300edaf07ddaaa`.
The package remains stored once under `runtime/m0`; `runtime/v1-identity.json`
records the alias and exact inventory.

- M0 intent fidelity and viability: passed.
- Method evidence: retained as admission only.
- H1 contribution: seven `rejected-no-control-deficit` decisions.
- Protected behavior: exact M0/V1 and required contracts passed.
- Invocation, context, machine, and relationships: explicit-only two-file
  package, no helper, F01-F08 absence, owner traces, and recommendation-and-stop
  boundaries passed.

Relationship changes: none. Relationship publication: not performed.

## Artifacts and identities

- Final worker fixture:
  `e16d50fce206dcd86fdf97a7dd355ed0bd580f5b363d29ad676e0195764df87c`.
- Dispatch template:
  `82fe5c4421969f547981bf4fb07ab9f6b274430012d678ffd0ef689faafb8029`.
- Results manifest:
  `90d3ea30f5ee5dc20e4507aedbb2ab7c56c17b2b78cda9694d230cae246fd42d`.
- Human decision:
  `880f8aeb80dacfa449a617265ba65b5302f2482b2266458b4cf170d3fbd18624`.
- Reconciled synthesis bounded fingerprint:
  `84eee89c376ee5e003428e06fa1a53315dd93241e4137b505e620d56435aed72`.
- Final campaign manifest:
  `3a312034b468fb212d229013953da1593d5c975a4504b7763d22e444d4242ec9`.

## Residuals

Live provider mutation/recovery, transfer beyond the fixed model/host/reasoning
and registered fixture families, P1, canonical promotion, installation,
relationship publication, and Git delivery remain unperformed. No unavailable
decision-bearing telemetry or unresolved current-removal risk remains.

## Shared Run Contract Return

Authorized unit completed: Deploy Prompt 4 — Prove M0 And H1 for `to-spec`

Decision: `accepted`

Campaign shape: `hypothesis-candidate`

Runtime identities: M0/V1 tree
`548af7fd1dd0c581fd472f5652ee0c294381c082ecfc927604300edaf07ddaaa`;
evaluated rejected H1 tree
`ac02b5ad3892427cb4cda755c18c4fac381d011a333a85e7b7a6eea88bac94e9`;
P1 unset

Artifacts changed: campaign-owned fixtures, dispatch/capture/results/decision
records, V1 identity alias, candidate and manifest reconciliation;
`docs/synthesis/skills/to-spec.md`; this Prompt 4 transcript

Evidence used or reused: exact M0 checkpoint and construction identities;
research for admission only; deterministic package, absence, invocation, and
relationship proof; 22 fresh valid M0 viability cases; 35 fresh valid M0
comparison controls; no H1 arm

Residual gaps: live provider recovery and transfer beyond fixed conditions;
P1, promotion, installation, publication of relationships, and Git delivery

Recommended next unit: Deploy Pruning Pass for `to-spec`

Git HEAD: `f3be70c31dd8f2ae9f12a75248065ef313790bda` ->
`f3be70c31dd8f2ae9f12a75248065ef313790bda`

Git delivery: pending

Exact stop reason: M0 is viable; every H1 unit was rejected because its
pre-registered M0 quality deficit was absent; exact V1 is frozen and no
Pruning Pass or successor work began.
