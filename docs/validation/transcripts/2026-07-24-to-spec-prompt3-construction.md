# To Spec Deploy Prompt 3 — M0/H1 Construction

Campaign epoch: `2026-07-24-to-spec`

Authorized operation: Deploy Prompt 3 only, using `writing-great-skills` in
Author mode.

Starting Git HEAD:
`f3be70c31dd8f2ae9f12a75248065ef313790bda`

## Input identity verification

| Input | Expected identity | Observed identity | Result |
| --- | --- | --- | --- |
| M0 bounded decision content | `b19edb0b03a176b0e4f903c001f1705587d04a4306bbd05be8c3d625d3f7a726` | `b19edb0b03a176b0e4f903c001f1705587d04a4306bbd05be8c3d625d3f7a726` | match |
| Research packet bytes | `2fecf286bdcdfa8a40269ee59a57e4d996736f447a88db5af15d54cb71215f37` | `2fecf286bdcdfa8a40269ee59a57e4d996736f447a88db5af15d54cb71215f37` | match |
| Synthesis bounded decision content | `0175b57caa3671a278b6e94d75d19902051e3e1da6f86d9422bc97e0b7d3f7bd` | `0175b57caa3671a278b6e94d75d19902051e3e1da6f86d9422bc97e0b7d3f7bd` | match |
| Prompt 2 manifest bytes | `a2e39c48fd56edfe4057db00368973870e9aff264f04dfb13b285e84e1f4eb6b` | `a2e39c48fd56edfe4057db00368973870e9aff264f04dfb13b285e84e1f4eb6b` before authorized update | match |
| Git HEAD | fixed point above | fixed point above | match |

The marker-bounded algorithms declared by the M0 checkpoint and synthesis were
used. The M0 whole-file hash and synthesis whole-file hash are not their
semantic identities.

## Exact runtime construction

M0 was authored only from the frozen C01-C16 runtime-clause specification,
M0-01 through M0-17 ledger, order, Returns, compatibility boundaries, and
limitations. No research-only wording, current-only five-verb spine, H1
expected weakness, or evaluator conclusion was imported.

| Arm | Package tree SHA-256 | Inventory |
| --- | --- | --- |
| M0 immutable control | `548af7fd1dd0c581fd472f5652ee0c294381c082ecfc927604300edaf07ddaaa` | `SKILL.md`: 5,621 bytes, `00e26469482d657f6201ad33051f2d4c1d3554c91d6780e7402f41ca8158d7fd`; `agents/openai.yaml`: 43 bytes, `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |
| H1 candidate | `ac02b5ad3892427cb4cda755c18c4fac381d011a333a85e7b7a6eea88bac94e9` | `SKILL.md`: 7,571 bytes, `f38c0e39905958e8b4cb3218e4901d0d747504ce5e02d7a51b42501d32d0b4c8`; `agents/openai.yaml`: 43 bytes, `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |

The tree algorithm and sorted inventory lines are fixed in
[`campaign-manifest.json`](../evals/to-spec-2026-07-24/campaign-manifest.json).
The manifest maps all 17 M0 instruction-bearing passages plus invocation policy
to M0 units and clauses. Each required semantic has one named owner, one or
more exact runtime passages, and proof IDs.

H1 reuses common M0 behavior inline and adds or substitutes only the seven
Prompt 2 admissions. Its eight H1-bearing passages, including the completion
qualification, each record unit, origin, method-evidence classification, and
`quality-lift` mode. Both packages contain only `SKILL.md` and
`agents/openai.yaml`; no helper, schema, or disclosed runtime file was added.
Current canonical bytes remain separate and unchanged.

## Pre-registered proof

The worker-visible fixture is
[`worker-visible.json`](../evals/to-spec-2026-07-24/fixtures/worker-visible.json),
SHA-256
`abc1fccfebba51c0356c33073e38a97694e61f73dce3c841468806abfdb01e7d`.
It fixes task, source facts, authority, initial state and observations,
tools/operations, mutation boundary, requested output, model, host, reasoning,
runtime arms, sample counts, fresh-context rule, and arm order. It contains no
hypothesis, rubric, candidate terms, prior outputs, or conclusion.

The root-only fixture is
[`root-only-evaluation.json`](../evals/to-spec-2026-07-24/fixtures/root-only-evaluation.json),
SHA-256
`4a4583c89cee71e4e8360a125f2dd7f8855e1ede93d72421d5494aa3e701b320`.
It owns every expected branch, expected M0 weakness, candidate language,
scoring trace, contribution threshold, conclusion rule, and transfer limit.
Every expected branch is uniquely fixed by worker-visible facts.

The complete M0 viability family contains exact checkpoint cases V01-V22:
success across GitHub, GitLab, and Local Markdown; caller packets; invocation;
setup/source/authority failures; existing and unknown state; coverage and
lifecycle state; publication failure and indeterminacy; verified cleanup;
downstream stop; and unrelated-state preservation. The checkpoint contains no
V23; the construction manifest corrects the Prompt 2 manifest's unowned V23
entry back to the frozen V01-V22 suite.

Seven independent comparative clusters are fixed:

| Cluster | Unit | Families | M0 controls | Conditional H1 samples |
| --- | --- | --- | --- | --- |
| Q01 | H1-01 | product vocabulary; integration premises | 5 | 5 |
| Q02 | H1-02 | defective drafts; nondefects | 5 | 5 |
| Q03 | H1-03 | service concerns; local-tool concerns | 5 | 5 |
| Q04 | H1-04 | credential integration; migration/configuration | 5 | 5 |
| Q05 | H1-05 | API proof; stateful-flow proof | 5 | 5 |
| Q06 | H1-06 | multi-actor product; internal platform | 5 | 5 |
| Q07 | H1-07 | product deferrals; operations deferrals | 5 | 5 |

M0 is the control. There is no third no-guidance arm. H1 dispatch is
conditional on a pre-registered meaningful M0 quality deficit while M0 remains
viable. Broad claims use two realistic families. No hypotheses were clustered
because no single fixture and rubric isolated a joint effect more cheaply.

The candidate-specific owner record is
[`candidate.md`](../evals/to-spec-2026-07-24/candidate.md), SHA-256
`ce0cf4b288ea9915f0571dabaa31dbf6dc802ae3248dbe9ad3d49e578cde62aa`.
It points to the authoritative contract, checkpoint, research, synthesis,
manifest, and fixtures and adds only the proof plan, Pruning Pass boundary,
affected relationships, and residual load.

## Structural, relationship, and absence proof

- Manifest JSON parse, enums, semantic cross-references, M0/H1 proof
  cardinalities, V01-V22 count, seven five-sample comparisons, two-family
  breadth, package-wide F01-F08 checks, and worker/root visibility invariants:
  passed.
- Exact package inventories, byte counts, file hashes, sorted tree hashes, and
  identity-slot read-back: passed.
- Fixture ambiguity audit: all 35 comparative variants have one root-owned
  expected branch determined by nonempty worker-visible source facts; passed.
- Candidate-term leakage scan against the worker-visible fixture: passed.
- Relationship read-back: explicit-only invocation; Skill Router, Wayfinder,
  and Improve Codebase callers; vocabulary-only `codebase-design` Load;
  `$repo-bootstrap` recommendation-and-stop; and `$to-tickets`
  recommendation-and-stop remain owner-matched. No relationship change was
  published.
- Complete-package absence proof for F01-F08: registered and structurally
  passed; behavior-dependent preservation remains for Prompt 4.
- Focused target contract tests:
  `.\.venv\Scripts\python.exe -m pytest tests/test_skill_pack_contracts.py -q
  -k 'to_spec or runtime_composition_edges or
  mutating_workflows_require_readback'`: `3 passed`.
- `.\.venv\Scripts\python.exe -m scripts.validate_skills`: passed.
- Affected Markdown local links, anchors, balanced fences, and tables: passed.
- `git diff --check` and `git diff --cached --check`: passed.
- Authorized-path and unrelated-state inspection: passed; concurrent unrelated
  files were neither read nor altered.
- Git HEAD read-back: unchanged.

Final campaign manifest SHA-256:
`64ba711a1a92aca615ad106810ac49894a4aa3e9ae3156b77616bca9ebf8cb5e`.

## Residuals

No behavioral sample or Prompt 4 result exists. M0 viability, every H1
contribution, live provider mutation/recovery, V1/P1, promotion, installation,
relationship publication, and Git delivery remain unperformed. The fixed
claims do not transfer beyond the registered model, host, reasoning, tools,
fixtures, and family bounds.

## Shared Run Contract Return

Authorized unit completed: Deploy Prompt 3 — Build M0 And H1 for `to-spec`

Decision: `ready-for-prompt-4`

Campaign shape: `hypothesis-candidate`

Runtime identities: M0 tree
`548af7fd1dd0c581fd472f5652ee0c294381c082ecfc927604300edaf07ddaaa`;
H1 tree
`ac02b5ad3892427cb4cda755c18c4fac381d011a333a85e7b7a6eea88bac94e9`;
V1/P1 not materialized; current canonical remains separate

Artifacts changed:
`docs/validation/evals/to-spec-2026-07-24/runtime/m0/SKILL.md`;
`docs/validation/evals/to-spec-2026-07-24/runtime/m0/agents/openai.yaml`;
`docs/validation/evals/to-spec-2026-07-24/runtime/h1/SKILL.md`;
`docs/validation/evals/to-spec-2026-07-24/runtime/h1/agents/openai.yaml`;
`docs/validation/evals/to-spec-2026-07-24/fixtures/worker-visible.json`;
`docs/validation/evals/to-spec-2026-07-24/fixtures/root-only-evaluation.json`;
`docs/validation/evals/to-spec-2026-07-24/candidate.md`;
`docs/validation/evals/to-spec-2026-07-24/campaign-manifest.json`;
`docs/validation/transcripts/2026-07-24-to-spec-prompt3-construction.md`

Evidence used or reused: exact M0 checkpoint for M0 construction; exact
research and synthesis only for admitted H1 construction and classification;
Prompt 2 current observations as historical admission only; relationship and
structural owners for deterministic construction proof; no behavioral evidence
reused

Residual gaps: M0 viability, H1 comparative contribution, live provider
recovery, V1/P1, promotion, installation, and transfer beyond fixed conditions

Recommended next unit: Deploy Prompt 4 for `to-spec`

Git HEAD: `f3be70c31dd8f2ae9f12a75248065ef313790bda` ->
`f3be70c31dd8f2ae9f12a75248065ef313790bda`

Git delivery: pending

Exact stop reason: exact M0/H1 construction and Prompt 4 pre-registration are
complete; no behavioral evaluation or successor began.
