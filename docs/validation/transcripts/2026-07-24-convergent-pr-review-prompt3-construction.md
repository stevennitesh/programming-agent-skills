# Convergent PR Review Deploy Prompt 3: Construction Record

- Campaign epoch: `2026-07-24`
- Authorized unit: Deploy Prompt 3: Build M0 And H1
- Authority: `writing-great-skills` Author
- Starting Git `HEAD`:
  `f3be70c31dd8f2ae9f12a75248065ef313790bda`
- Campaign shape: `hypothesis-candidate`
- Behavioral samples run: `0`
- Promotion, installation, and Git delivery performed: `no`

## Verified Inputs

The marker-bounded semantic fingerprints were recomputed from exact UTF-8
content after excluding each marker line and its adjacent single line feed:

| Input | Bounded SHA-256 | Result |
| --- | --- | --- |
| Prompt 1 M0 checkpoint | `469734af7b346c0f327d07fbd2a001d8b3f76cd985aa7c9468a53c6944326e4e` | exact |
| Research packet | `e1da6bc137e036d4dbb81174728eea0ed77cfa9d5bfcfcfa4e77af526747d9d7` | exact |
| Active synthesis | `605c0c52186b2f8fd288d068d4888756544cc9b68f6aaa6c73524a4bd5fd0f2b` | exact |

Git `HEAD` matched the fixed point before mutation. The campaign manifest was
Prompt 2-ready, the shape was `hypothesis-candidate`, H1-01 through H1-05 were
closed admissions, and F01 through F12 had complete absence obligations.

## Exact Runtime Construction

M0 was materialized solely from the bounded Prompt 1 checkpoint. It imports no
research wording, current-only behavior, expected H1 weakness, or evaluator
conclusion. The checkpoint's State-Location Ledger explicitly requires the
complete caller packet to be read and frozen before Pin, so the runtime places
that operation in the first route/root gate; Pin still precedes source tracing
and dispatch.

Each runtime-facing package has exactly this inventory:

```text
agents/openai.yaml
SKILL.md
```

| Arm | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| M0 | `agents/openai.yaml` | 413 | `fddd9784e700e2c38c4cab03e3b66b547a4ab4fca075c61b9d3adec785726c63` |
| M0 | `SKILL.md` | 11685 | `7b635dc4812472aed96a9b5661350835b7624e96db0142c8dcc311514c3f0d81` |
| H1 | `agents/openai.yaml` | 413 | `fddd9784e700e2c38c4cab03e3b66b547a4ab4fca075c61b9d3adec785726c63` |
| H1 | `SKILL.md` | 15138 | `a371e582b944a912b7d075116b5012996b22a79afbc6b961278e495c525b7d71` |

Package-tree identities use the manifest's declared case-folded,
package-relative path, byte-count, and file-hash algorithm:

- M0:
  `6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280`
- H1:
  `379474917dc540ef9704a74628af11e123db11fc9e800a94b797278c1ab05c82`

The YAML metadata is byte-identical between arms. A line-level exact diff has
only insert operations: H1 is M0 plus six semantic passages, mapped as two
passages for H1-01 and one each for H1-02, H1-03, H1-04, and H1-05. The
campaign manifest owns the complete M0 passage/unit/clause map, M0 unit owners
and proofs, and each H1 passage's origin, method-evidence classification,
evidence limit, and contribution mode.

## Frozen Prompt 4 Protocol

Prompt 4 input was frozen without generating an output:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `fixtures/worker-visible.json` | 36137 | `466c53a4d1efbdb675df702189db5b0af77990603f1b98302bc49b162f9f6a62` |
| `fixtures/root-only-evaluation.json` | 22731 | `697f22290d996128e4dda66eff229cda44deca131c146a38c8cffc2797104d22` |
| `candidate.md` | 4785 | `d944500da9542e43f6af20813c499734e44d8cf47a94cd923e0abcbda6f36c79` |

The protocol requires all 25 M0 viability cases first. Each contribution
cluster then runs five fresh M0 controls, beginning with a single first-sample
family gate, and releases five H1 samples only after its registered M0 defect
or meaningful quality deficit appears while M0 remains viable.
`Q01-snapshot` and `Q02-coverage-truth` each span two broad realistic
families. `Q03-bounded-recovery` spans two families but explicitly bounds
transfer to one unchanged snapshot and caller packet with one recovery action.

Worker dispatch assembly includes one exact runtime arm, the common fixed
execution fields, and one selected worker-visible case. Hypotheses, expected
weaknesses, rubrics, scores, candidate terms, prior outputs, and conclusions
remain root-only. Exact service model and reasoning identifiers were not
available to Prompt 3; Prompt 4 must record and freeze them before its first
sample.

An independent fresh-context read-only audit found that V18 originally lacked
the evidence needed to choose exact ledger dispositions, three Q03 cases fixed
an authorized recovery action without fixing its returned evidence, and
Q02-05 omitted terminal drift/residual facts. The worker facts and root traces
were tightened so each score and branch is now uniquely decided and adjacent
outcomes are invalid. The audit found no runtime purity, H1 classification,
inventory, passage-map, F01-F12, isolation, count, family, or gate defect.

## Prompt 3 Proof

The following current-state checks passed:

- exact package inventories, byte counts, file hashes, and package-tree hashes;
- YAML/frontmatter parsing and an insert-only M0-to-H1 line diff;
- complete M0 passage, semantic owner, clause, and proof coverage;
- complete H1-only origin, evidence, limit, and contribution classification;
- complete semantic absence of F01 through F12 across both packages;
- shared-contract, caller, audit recommendation-and-stop, no-reverse-handoff,
  root-only, mode, capacity, decision, drift, and Return relationships;
- command and mutation safety, including no review-owned fetch, Git-writing
  acquisition, helper, repository artifact, Repair, or successor work;
- 25/25 M0 viability fixtures and 5/5 samples in each of three contribution
  clusters, with fact-traced root branches and nonempty adjacent-invalid sets;
- worker/root payload isolation and zero generated outputs or samples;
- affected Markdown links, anchors, fences, tables, and trailing whitespace;
- campaign-manifest JSON parsing and all Prompt 3 invariants;
- `python -B -m scripts.validate_skills`;
- `git diff --check` and `git diff --cached --check`; and
- final Git `HEAD` and authorized-scope read-back.

No canonical runtime, installed mirror, caller, shared contract, relationship,
synthesis, research, test, setup, tracker, PR, external system, or Git
delivery surface changed. Concurrent unrelated work remained unmodified.

## Decision

Status: `ready-for-prompt-4`

M0 is exact and executable. H1 is exact, provisional, and fully classified.
The protocol is frozen and unrun. V1, P1, promotion, installation, and delivery
remain unset.

```text
Authorized unit completed: Deploy Prompt 3: Build M0 And H1
Decision: ready-for-prompt-4
Campaign shape: hypothesis-candidate
Runtime identities: current=canonical=git-tree:d2210fc11b357f1e2f69408a8a21bd9d422c677a; installed=current-content-equivalent@sha256:42d2c56f8313fb35dbb4f5033f7ed48b81043466ca8becb8c4a38075acee44a9; M0=package-tree-sha256:6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280; H1=package-tree-sha256:379474917dc540ef9704a74628af11e123db11fc9e800a94b797278c1ab05c82; V1=pending; P1=pending
Artifacts changed: docs/validation/evals/convergent-pr-review-2026-07-24/campaign-manifest.json; docs/validation/evals/convergent-pr-review-2026-07-24/runtime/m0/**; docs/validation/evals/convergent-pr-review-2026-07-24/runtime/h1/**; docs/validation/evals/convergent-pr-review-2026-07-24/candidate.md; docs/validation/evals/convergent-pr-review-2026-07-24/fixtures/worker-visible.json; docs/validation/evals/convergent-pr-review-2026-07-24/fixtures/root-only-evaluation.json; docs/validation/transcripts/2026-07-24-convergent-pr-review-prompt3-construction.md
Evidence used or reused: exact Prompt 1 M0 specification; exact research and synthesis for H1 admission/classification only; lane-limited current package and relationship evidence; fresh Prompt 3 structural, identity, absence, fixture-isolation, Markdown, repository-validation, diff, HEAD, scope, and independent read-only audit evidence; no behavioral evidence
Residual gaps: M0 viability behavior; control deficits; H1 comparative contribution and regression; exact Prompt 4 service model/reasoning telemetry; portable atomic dirty-tree and external-state guarantees; V1 and P1; promotion, installation, and Git delivery
Recommended next unit: Deploy Prompt 4
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: exact M0 and classified H1 plus an isolated frozen Prompt 4 protocol passed Prompt 3 proof; stop before Prompt 4
```
