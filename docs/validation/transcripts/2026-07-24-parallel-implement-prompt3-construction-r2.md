# Parallel Implement Deploy Prompt 3 — Corrected M0/H1 Construction

Campaign epoch: `2026-07-24-r2`
Skill: `parallel-implement`
Unit: `Deploy Prompt 3: Build M0 And H1`
Authority mode: `writing-great-skills / Author`
Starting Git HEAD: `94d68e78d8812e9a2ceffd093e729402cac1cff2`

This is the authoritative Prompt 3 candidate record for the correction epoch.
It references the authoritative intent and synthesis records and stores
candidate-specific identities and proof registration once.

<!-- DECISION-CONTENT-BEGIN -->

## Decision

Decision: `ready-for-prompt-4`.

Campaign shape: `minimum-candidate`.

Runtime identities:

```text
current = 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
failed r1 candidate = bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05
M0 = H1 = c347c36f782f401d770709bf0170dc9a5ac1a77a97038ea42f6d5b163b4c6a0d
relationship = current != M0 = H1
```

Exact M0 is executable and behavior-complete. H1 has no transformation unit,
so the exact M0 corpus is stored once as both M0 and H1. No no-guidance,
current-runtime, or empty H1 arm exists.

## Authoritative Inputs

- Corrected intended contract and M0 checkpoint:
  [Prompt 1 r2](2026-07-24-parallel-implement-prompt1-m0-r2.md), bounded
  fingerprint
  `ac7e81bdeb9ea05b929aa9c39af703521bd5b2b10979ad2c646132fec8f76715`.
- Corrected research packet:
  [research r2](../../research/parallel-implement-2026-07-24-r2.md), bounded
  fingerprint
  `0a4284ca7d4c06bb91b4d7aa47ff4362ffab4411ba5463862353355f9fe66b85`.
- Exact-carried unaffected research:
  [prior research](../../research/parallel-implement-2026-07-24.md), bounded
  fingerprint
  `3d8ad3acb1aedaf5a3c857d2a2ca573b67472072149ed7df71e8e07bc52b0d54`.
- Prompt 2 construction authority:
  [r2 synthesis](../../synthesis/skills/parallel-implement.md), bounded
  fingerprint
  `a9c50ed8c7f61a4adeb9f187360fb6c90294059da2146969986a87bbcfe6dbb6`.

All records retain fixed Git `HEAD`
`94d68e78d8812e9a2ceffd093e729402cac1cff2`. No Prototype or Behavior Decision
Interlude was admitted.

## Exact Candidate

The active experimental candidate is
[skills/experimental/parallel-implement](../../../skills/experimental/parallel-implement).
Its inventory is exactly eight files:

```text
SKILL.md
agents/openai.yaml
references/CODEX-WORKTREE-LAUNCH.md
references/INTEGRATOR-BRIEF.md
references/RUN-LEDGER.md
references/WORKER-BRIEF.md
scripts/lane_worktree.py
scripts/run_ledger.py
```

The compact
[protocol manifest](../evals/parallel-implement-prompt4-r2/protocol-manifest.json)
is the single machine authority for the inventory, every file SHA-256, tree
SHA-256, clause-to-runtime map, instruction-passage owners, K-01–K-08 map, H1
equality, helper identities, protected set, relationship plan, affected
surfaces, exact evaluation configuration, fixture identities, expected
captures, evidence dispositions, and limitations.

`scripts/run_ledger.py` remains exact SHA-256
`caa174522351d903985dbe94632bb54f6beb16e5eb3dcdcd31e64ee2bbae1f2d`;
`scripts/lane_worktree.py` remains exact SHA-256
`0884edd628114a9101c3e9d544ee03699fbbef93b3c3ff2a35dcb915e0897ce8`.
Both are byte-identical to the current canonical helpers. K-02 therefore
preserves its full machine schema and command compatibility.

The runtime keeps C01–C17 and M0-01–M0-17. The corrected Review owner:

- selects `$review` for an ordinary immutable candidate and
  `$convergent-pr-review` for a local PR or bounded high-risk diff from explicit
  target and risk facts;
- returns the complete mixed blocking report intact and creates no Repair plan,
  assignment, mutation, or successor snapshot before caller admission;
- after admission, requires admitted IDs to equal the complete blocking set,
  every blocker to be `automatic-in-scope`, each blocker to have
  Charter-preservation evidence, and both frozen Repair-generation and
  successor-review budgets to permit progression; and
- requires identity-matched proof and a fresh owner-matched formal review for
  every repaired successor.

The candidate retains no runtime push execution and no arbitrary
same-actor-once rule. Publication evidence may only be reconciled when supplied
under separate authority.

## Prompt 4 Registration

The new r2 protocol lives only at
[parallel-implement-prompt4-r2](../evals/parallel-implement-prompt4-r2).
The prior `parallel-implement-prompt4` directory remains historical and was not
modified by this unit.

The worker-visible fixture stores two exact templates plus reconstructing
parameters for exactly five affected samples:

```text
O-01, O-02, O-03: ordinary local branch diff
H-01, H-02: local PR with bounded high-risk authentication diff
```

Every template exposes target type and risk evidence, the intact F1/F2/F3
report, absent pre-admission authority, the post-decision complete caller
admission, all-automatic classifications, per-blocker Charter evidence, both
frozen budgets, successor proof and review facts, mutation boundary, and
requested output. Root-only material separately holds the hypothesis, rubric,
critical failures, scoring, and conclusions. Each criterion traces to a named
worker-visible fact or observable simulation.

The frozen evaluation configuration is:

```text
model: gpt-5.6-sol
reasoning: high
host: Codex fresh-context subagents on Windows/PowerShell
tools: exact candidate and assigned fixture read; assigned disposable capture write only
external effects: tracker, Git, worktree, remote, publication, installation, and destructive operations simulated
```

Behavioral evaluation status is `not-started`. Prompt 3 ran no sample and
claims no behavioral viability.

## Proof And Preservation

Fresh Prompt 3 proof:

- `verify_candidate.py`: passed exact input fingerprints, runtime inventory,
  per-file hashes, tree hash, M0/H1 equality, helper identity, C/K/relationship
  maps, Repair authority, five-fixture isolation and grounding, manifest, and
  Markdown gates;
- JSON parsing for both fixtures, the protocol manifest, and the experimental
  manifest: passed;
- `pytest tests/test_parallel_implement_helpers.py
  tests/test_experimental_skill_contracts.py -q`: `55 passed`;
- focused `test_skill_pack_contracts.py` parallel, overlay, and state-boundary
  contracts: `6 passed`;
- `python -m scripts.validate_skills`: passed;
- `git diff --check` and `git diff --cached --check`: passed with no output;
  and
- mutation-boundary read-back retained the starting ambient cohort plus only
  the authorized r2 candidate, manifest-entry, evaluation, and transcript
  surfaces; Git `HEAD` remained unchanged.

No relationship index, canonical runtime, installation, research, synthesis,
checkpoint, prior transcript, prior evaluation/result/raw artifact, or test was
published or rewritten by this unit. Ambient unrelated `implement` work and
pre-existing historical r1 worktree state were preserved.

Evidence dispositions remain:

- prior research `exact-reusable`;
- exact K-02 helper mechanics `exact-reusable`, with corrected semantics
  `lane-limited` until affected proof;
- K-03/K-04, unaffected units, and unaffected relationships `lane-limited`
  after identity read-back;
- the failed r1 candidate and samples `invalidated` for affected proof and
  `historical-admission-only` otherwise;
- current canonical behavior `historical-admission-only`; and
- live provider mutation, remote publication, and irreversible closeout
  `missing`.

## Pruning Boundary And Gaps

The Pruning Pass may begin only after Prompt 4 establishes V1. It must protect
all accepted M0 behavior, K-01–K-08 compatibility, corrected review routing,
the complete-set caller-admission Repair gate, successor proof/review, and
every preserved relationship. No pruning or promotion has occurred.

Residual gaps:

- five fresh affected M0 samples for M0-13/M0-14/V21–V23 await Prompt 4;
- no current candidate-owned behavioral evidence exists;
- live tracker/provider partial mutation, remote publication, and irreversible
  closeout remain unauthorized;
- provider-specific mutation idempotency remains unverified;
- worktree containment does not prove process, credential, network, cache,
  submodule, or scarce-resource isolation; and
- future behavioral conclusions remain bounded to the frozen bytes, fixtures,
  model, host, reasoning, tools, and sample count.

Facts, professional synthesis, pack observations, inference, deterministic
proof, and future behavioral evidence remain separate.

<!-- DECISION-CONTENT-END -->

Content fingerprint algorithm: SHA-256 over the exact UTF-8 bytes after the
`DECISION-CONTENT-BEGIN` marker line through the byte immediately before the
`DECISION-CONTENT-END` marker line, including intervening line endings.

Content fingerprint: `9a0c828066152ff0afbca10717f55f51a0766cfddb551886eeeb8f6cd861e8d6`

## Shared Run Contract Return

```text
Authorized unit completed: Deploy Prompt 3: Build M0 And H1 for parallel-implement, correction epoch 2026-07-24-r2
Decision: ready-for-prompt-4
Campaign shape: minimum-candidate
Runtime identities: current 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc; failed r1 bbaf9558628dc5370d6b5f5770785746763eee63ca93f84113e18cb75307ed05; M0 = H1 c347c36f782f401d770709bf0170dc9a5ac1a77a97038ea42f6d5b163b4c6a0d
Artifacts changed: corrected experimental parallel-implement package; only its experimental manifest entry; new parallel-implement-prompt4-r2 protocol; this r2 construction record
Evidence used or reused: exact Prompt 1 r2, research r2, carried research, and Prompt 2 fingerprints; current and failed-candidate tree identities; exact K-02/K-04 helper bytes; lane-limited unaffected evidence; fresh deterministic Prompt 3 proof
Residual gaps: no behavioral viability; five affected M0 samples await Prompt 4; live provider mutation/publication/irreversible closeout untested; provider idempotency and wider isolation remain unverified
Recommended next unit: Deploy Prompt 4: Prove M0 And H1
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: corrected exact M0/H1 corpus and isolated r2 Prompt 4 protocol constructed and structurally proved; stopped before behavioral evaluation
```
