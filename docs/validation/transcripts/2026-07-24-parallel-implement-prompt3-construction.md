# Parallel Implement — Deploy Prompt 3 Construction

Campaign epoch: `2026-07-24`
Skill: `parallel-implement`
Authorized unit: `Deploy Prompt 3: Build M0 And H1`
Authority: `writing-great-skills / Author`
Starting Git HEAD: `94d68e78d8812e9a2ceffd093e729402cac1cff2`

## Decision

Decision: `ready-for-prompt-4`.

Campaign shape: `minimum-candidate`.

Runtime identities:

```text
current: 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
M0: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
H1: bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
relationship: current != M0 = H1
```

M0 and H1 are one stored corpus at
`../../../skills/experimental/parallel-implement/`. No transformation file,
current-runtime arm, no-guidance arm, or behavioral result was created.

## Verified Inputs

| Input | Frozen identity | Result |
| --- | --- | --- |
| Prompt 1 M0 bounded content | `c91962879ff9bd03b48c34fa422974fff8a2aee8362c8a879627ebc66039271a` | exact |
| Research bounded content | `3d8ad3acb1aedaf5a3c857d2a2ca573b67472072149ed7df71e8e07bc52b0d54` | exact |
| Prompt 2 bounded content | `d231c314136f6795008bed1f9d9d860626978cfac829327cc35bbc385e9f3e62` | exact |
| Current canonical tree | `036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc` | exact |
| Starting Git HEAD | `94d68e78d8812e9a2ceffd093e729402cac1cff2` | exact |
| Prototype Interlude | not admitted | closed |
| Behavior Decision Interlude | not admitted | closed |

The authoritative intended contract remains the Prompt 1 record. The
authoritative construction decisions remain the Prompt 2 synthesis. This
record does not copy either contract into a second authority.

## Exact Candidate

The compact machine authority is
`../evals/parallel-implement-prompt4/protocol-manifest.json`. It freezes:

- the exact eight-file inventory, each file SHA-256, and tree SHA-256;
- the complete C01–C17 runtime-clause map and K-01–K-08 compatibility map;
- M0/H1 equality and current inequality;
- M0-01 through M0-17, the protected clauses and compatibility boundaries;
- all eight relationship triggers, owners, and Returns;
- excluded installation, publication, push, Git-delivery, and unrelated-cleanup
  authority;
- the exact model, host, reasoning effort, tools, fixed point, fixture
  identities, payload-isolation rule, expected captures, and limitations.

The package retains common admission, setup, packet, Charter, state,
frontier, claim, isolation, integration, proof, review, Repair, closeout, and
reconciliation gates inline. Ledger schema and commands, lane lifecycle,
worker packet mechanics, and optional integrator mechanics remain behind
trigger-bearing pointers.

The metadata remains explicit-only. The root no longer executes push or Git
delivery. It may reconcile applicable publication evidence supplied by a
separately authorized owner. The arbitrary “continue the same actor once”
rule is replaced by state- and authority-based continuation. Machine
push-event compatibility remains unchanged in `run_ledger.py`.

The fresh protocol replaces three 2026-07-23 raw capture files. Their
historical evidence remains recoverable at the campaign fixed point and is
classified `historical-admission-only`:

| Prior file | Git blob at fixed point |
| --- | --- |
| `concurrency-raw.md` | `c5ea87fdebebaa66622135387f05e92c7a500b3b` |
| `recovery-raw.md` | `66892b321a8577ce310f6d2dd62bc23e1b20868c` |
| `viability-raw.md` | `bfae66a1720bf53b90d26c8898b80dffcf29a850` |

Both helpers are byte-identical to current canonical:

| Helper | SHA-256 |
| --- | --- |
| `scripts/lane_worktree.py` | `0884edd628114a9101c3e9d544ee03699fbbef93b3c3ff2a35dcb915e0897ce8` |
| `scripts/run_ledger.py` | `caa174522351d903985dbe94632bb54f6beb16e5eb3dcdcd31e64ee2bbae1f2d` |

## Frozen Prompt 4 Protocol

Worker-visible facts and allowed simulated operations live only in
`../evals/parallel-implement-prompt4/worker-fixtures.json`, SHA-256
`e86f2b9ece2522c5ae2833b65696cb16c7cd5e36ab6fc6d74b8e25c1287069e3`.

The hypothesis, expected weakness, candidate terms, conclusions, rubrics,
scoring, and critical failures live only in the root-held
`../evals/parallel-implement-prompt4/evaluator-fixture.json`, SHA-256
`0961527e5409b14912808e5a1db02364b6799b5b6f7c4c41f945d59d98a0e89c`.
Every rubric criterion names its worker-visible fact or simulated observable
operation. No criterion depends on hidden candidate guidance.

The exact evaluation configuration is:

```text
model: gpt-5.6-sol
reasoning effort: high
host: Codex fresh-context subagents on Windows/PowerShell
tools: read exact candidate and worker fixture; write only one disposable capture
external operations: simulated only
runtime arm: exact M0 corpus
H1: identical corpus; zero separate samples
minimum samples: five total; A >= 2; B >= 2
expected captures: A-01, A-02, A-03, B-01, B-02
behavioral evaluation: not started
```

## Proof And Deliberate Non-Changes

Prompt 3 proof covers exact inventories and hashes, helper byte identity,
machine contracts, structural clauses, invocation metadata, disclosure
pointers, relationship ownership, focused helper behavior, Markdown gates,
skill-pack validation, mutation scope, both diff checks, and Git HEAD
read-back.

No behavioral sample ran. Canonical runtime, Prompt 2 synthesis, relationship
index, installation, installed mirrors, tests outside the target evaluation
folder, tracker state, remote state, Git staging, commits, and delivery remain
unchanged by this unit. Unrelated dirty `implement` campaign work was
preserved.

## Residual Gaps

- M0 behavioral viability remains unproved until Prompt 4.
- Live tracker/provider partial mutation, remote publication, and irreversible
  closeout remain outside the authorized protocol.
- Provider-specific mutation idempotency remains `unverified`.
- Worktree containment does not prove process, credential, network, cache,
  submodule, or scarce-resource isolation.
- Future evidence remains bounded to the frozen package, fixtures, model,
  host, reasoning configuration, tools, and sample count.
- Pruning, promotion, relationship publication, installation, and Git
  delivery remain with later owners.

## Return

```text
Authorized unit completed: Deploy Prompt 3: Build M0 And H1
Decision: ready-for-prompt-4
Campaign shape: minimum-candidate
Runtime identities: current 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc; M0 = H1 bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
Artifacts changed: experimental parallel-implement package and manifest entry; Prompt 4 protocol fixtures/manifest/checker; this construction record
Evidence used or reused: exact Prompt 1, research, and Prompt 2 fingerprints; current tree; lane-limited helper and relationship evidence; fresh deterministic Prompt 3 checks
Residual gaps: no behavioral viability; live external mutation and publication untested; provider idempotency unverified; isolation and transfer limits retained
Recommended next unit: Deploy Prompt 4: Prove M0 And H1
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: exact M0/H1 corpus and Prompt 4 protocol constructed; stopped before behavioral evaluation
```
