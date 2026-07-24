# Review Deploy Prompt 3 — M0/H1 Construction

Campaign epoch: `2026-07-24-review-f3be70c`

Authorized unit: Deploy Prompt 3 only

Operation: `writing-great-skills` Author

Starting Git `HEAD`: `f3be70c31dd8f2ae9f12a75248065ef313790bda`

This is the authoritative human-readable construction record. The campaign
manifest owns shared semantic and identity state; the protocol manifest owns
Prompt 4 registration.

<!-- REVIEW-PROMPT3-DECISION:START -->

## Decision

Decision: `ready-for-prompt-4`.

Campaign shape: `minimum-candidate`.

```text
current != M0 = H1
```

The current canonical runtime remains comparison-only at tree SHA-256
`4bc1ce43eaa00a9ad7a7482a639793b286fde27c14ba0c5e41e1f73364eb9786`.
The exact M0/H1 runtime is stored once at tree SHA-256
`37a670dbe0748f5f89d7d8e0b61ff30b0241fffd81b1861da5f5838af6dd98c8`.
H1 has zero transformations and no contribution arm.

## Frozen Inputs

Before construction, the following identities were recomputed and matched:

| Input | SHA-256 |
| --- | --- |
| M0 checkpoint | `3fa19cd24076c25090adc1921dc1e5f1c21e74749e4179a6c59c17a523330366` |
| M0/H1 specification | `9adc5608bad387df9314df185d7de67b11eb6efb1f9a608e7f7a5c5409213268` |
| Research packet | `ba36096f6a7dc2862d721dac0f4931984de14a41ba1145152c0c89bbda49c754` |
| Prompt 2 bounded synthesis | `c0f6f293db5c7607128ff2fcaf462b0d4dd9928e5b8c071e1a96889dc67b2894` |
| Prompt 2 manifest decision | `e74c201541481ede0d5d193e0b7490056a69c966885a2dce2951c9e8190bf52a` |

The starting and ending checkpoint is
`f3be70c31dd8f2ae9f12a75248065ef313790bda`. Both conditional interludes were
closed before Prompt 3.

## Exact Runtime

The shared [M0/H1 corpus](../../../.scratch/deploy-campaigns/2026-07-24-review-f3be70c/runtime/m0-h1/review)
contains exactly:

| File | SHA-256 | Construction disposition |
| --- | --- | --- |
| `SKILL.md` | `a78aa310f340ffd4cdfa8e721b4bcf3ea99f89be01c834c01d4c1efee27d8153` | Materialized only from the frozen checkpoint and exact specification |
| `FINDING-CONTRACT.md` | `f99446f46d3f6f31b58d0dfecb31c3602742d1e7f8b14f43414f0575b7a6cc95` | Exact permitted compatibility bytes |
| `SMELL-BASELINE.md` | `966b35b7da2690a5df33d697b43b3c0bd41891b1a5e554c2f0b266610ac2259f` | Exact permitted compatibility bytes |
| `ADVISORY-CONTRACT.md` | `5edf5100cd8ff6d924d93866100f0c2c80f17751c999985105eb5bf0a6003972` | Exact foreign-consumer compatibility bytes; ordinary Review has no pointer |
| `agents/openai.yaml` | `5b344e7c178aeb37da631a640704dcc71d24c67442f7a9a5bc054586e9453ca4` | Exact implicit-invocation compatibility bytes |

The runtime keeps the required `Route -> Pin -> Trace -> Judge -> Admit ->
Return` order. It names the exact state-location snapshot tuple, records
producing commands and ref resolutions, judges captured bytes, recomputes each
applicable cell before Return, and makes any missing or changed cell
`incomplete` without recapture. Its in-context coverage ledger accounts for
changed units, necessary context, required proof, and explicit skips; a
material skipped or blocked entry prevents `complete`.

Every one of `M0-R01` through `M0-R14` has a runtime passage and registered
proof. The [campaign manifest](../../../.scratch/deploy-campaigns/2026-07-24-review-f3be70c/campaign.json)
owns the semantic trace. The
[protocol manifest](../../../.scratch/deploy-campaigns/2026-07-24-review-f3be70c/evals/prompt4/protocol-manifest.json)
owns the 46-entry instruction-passage map, selectors, origin classification,
proof IDs, and executable absence checks for all twelve forbidden semantic
IDs.

## Prompt 4 Registration

The candidate-specific
[proof protocol](../../../.scratch/deploy-campaigns/2026-07-24-review-f3be70c/evals/prompt4)
contains:

- one worker-visible fixture with task, source facts, authority, initial
  observations, tools, mutation boundary, requested output, and 32 exact
  cases;
- one root-only evaluator with expectations, scoring, critical failures,
  grounding trace, and conclusions withheld from workers;
- exact M0 viability coverage for the seventeen checkpoint cases;
- committed, staged, WIP, mixed, untracked, and since-X target families;
- controlled drift for each applicable endpoint, `HEAD`, index, staged,
  unstaged, status, untracked inventory, path, mode, and content cell;
- coverage-ledger cases for changed units, context, required proof,
  nonmaterial skips, material skips, and false-complete pressure;
- invocation, relationship, conditional-context, machine-interface,
  before/after read-only, and successor-pressure proof; and
- no no-guidance, current-runtime, candidate-only, or H1 contribution arm.

The fixed future evaluation configuration is `gpt-5.6-sol`, `high` reasoning,
fresh-context Codex subagents on Windows/PowerShell, exact candidate and
assigned worker-visible facts, simulated read-only observations, and only an
assigned disposable capture write. Behavioral evaluation status remains
`not-started`.

Every scored criterion is traced to a worker-visible fact or observable
simulated operation. The facts make the expected route, gate, finding,
completion, or safe-failure branch unique; no adjacent outcome remains valid
without contradicting a supplied fact.

## Candidate Record, Pruning Boundary, And Relationships

The compact [candidate record](../../../.scratch/deploy-campaigns/2026-07-24-review-f3be70c/candidate.json)
references rather than copies the intended contract, checkpoint, research,
Prompt 2 decision, interlude dispositions, semantic ledger, and protocol. It
adds only the exact runtime identity, candidate-specific proof plan, future
Pruning Pass boundary, affected relationship set, publication boundary, and
residual load.

No relationship was published or changed. Prompt 4 must prove M0 first. A
future Pruning Pass may begin only after V1 exists and must preserve every
accepted M0 semantic, machine interface, relationship, context-loading
condition, and authority boundary.

## Preservation And Evidence Limits

Canonical `skills/custom/review`, installed mirrors, callers, relationship
maps, tests and scripts, research, synthesis, prior records, trackers, remotes,
and Git remained unchanged by this unit. Concurrent unrelated convergent-review
and to-spec artifacts were preserved.

Fresh Prompt 3 proof is structural and identity-matched. It does not establish
behavioral viability or tuple/coverage efficacy. Current behavior remains
`historical-admission-only`; current parsed contracts and unchanged helper
bytes remain `lane-limited`. Candidate-owned M0 behavior remains `missing`
until Prompt 4. Exact model build, token counts, sampler seed, per-sample
latency, and external generalization remain unavailable or unproved.

The deterministic candidate verifier passed frozen input fingerprints,
inventory and hashes, M0/H1 equality, passage and semantic maps, forbidden
absence checks, fixture isolation and grounding, invocation, relationships,
conditional context, machine interfaces, and Markdown/JSON gates. Six focused
Review, Router, Implement, and Parallel Implement contract tests passed.
`python -m scripts.validate_skills`, `git diff --check`, and
`git diff --cached --check` passed. Git `HEAD` read back unchanged.

<!-- REVIEW-PROMPT3-DECISION:END -->

Content fingerprint algorithm: SHA-256 over the exact UTF-8 content beginning
immediately after the `REVIEW-PROMPT3-DECISION:START` marker through the byte
immediately before the `REVIEW-PROMPT3-DECISION:END` marker, with line endings
normalized to LF.

Content fingerprint: `f1279dea97aec497017b9893d5475d0ca0cee65503de71e88d41a8480b1b7882`

## Shared Run Contract Return

```text
Authorized unit completed: Deploy Prompt 3: Build M0 And H1 for review, campaign 2026-07-24-review-f3be70c
Decision: ready-for-prompt-4
Campaign shape: minimum-candidate
Runtime identities: current 4bc1ce43eaa00a9ad7a7482a639793b286fde27c14ba0c5e41e1f73364eb9786; M0 = H1 37a670dbe0748f5f89d7d8e0b61ff30b0241fffd81b1861da5f5838af6dd98c8
Artifacts changed: campaign manifest; one shared immutable M0/H1 runtime corpus; Prompt 4 protocol, isolated fixtures, and verifier; candidate record; this construction transcript
Evidence used or reused: exact Prompt 1 checkpoint, research, Prompt 2 synthesis and manifest fingerprints; current runtime comparison identity; exact permitted compatibility bytes; fresh inventory, hash, passage, semantic, forbidden-absence, fixture-isolation, relationship, context, and machine proof
Residual gaps: no candidate-owned behavioral viability; tuple execution and coverage-ledger efficacy await Prompt 4; exact model build, token counts, sampler seed, and latency unavailable; external generalization unproved
Recommended next unit: Deploy Prompt 4: Prove M0 And H1
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: exact byte-identical M0/H1 runtime and complete isolated M0 proof registration constructed and structurally verified; stopped before behavioral evaluation, promotion, installation, Git delivery, or Prompt 4
```
