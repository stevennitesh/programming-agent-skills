# Writing Great Skills Deploy Prompt 3 Construction

<!-- BEGIN PROMPT3 DECISION -->

## Decision

`ready-for-prompt-4`

Authority was `Author`. Coverage was limited to construction of the exact
campaign M0 and H1 packages, their semantic and proof ledgers, frozen Prompt 4
fixtures and protocol, the candidate record, the campaign manifest, and this
transcript. No canonical skill, relationship publication, installation,
behavioral sample, Git index, commit, or remote state was changed.

Campaign shape is `hypothesis-candidate`; the exact identity relationship is
`current != M0 != H1`.

## Input integrity

- Git checkpoint: `55dd6818182caf75e85de713a13ed76996336a27`
- M0 checkpoint: `49d8890b655be04129baf67ad729e031fd926d9bd3d332c5bb4dc9cf271a2f03`
- Research file: `3aae141d4b10e4c0fb77b199edf0b002b105e3b7fe94b003fbf15322a6110c31`
- Prompt 2 synthesis file: `b4659bb8f19fe0957b90cfb99581e3c5bf629bc458b7e662be89a4d3063449c1`
- Prompt 2 bounded synthesis: `cef4e2302a9b77ee73ec3871d27e052fb0476709ba1233516947b87b693f26f4`
- Prompt 2 transcript: `0c578806d4126a99f15d93a08f3ad498c1cb09a2feb84fd033e81e60b6000974`
- Conditional Interludes: both closed

## Runtime identities

M0 is stored at
`.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/runtime/m0/writing-great-skills`
with `campaign-tree-v1` SHA-256
`559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032`.

H1 is stored separately at
`.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/runtime/h1/writing-great-skills`
with `campaign-tree-v1` SHA-256
`1021d8c5d9d20a81e4ab33a0b014cf71826b818a02153041b7845aac245cf553`.
Only `BEHAVIOR-EVALS.md` differs, and the complete delta is
`H1-UNCERTAINTY-01`.

Both packages contain exactly `SKILL.md`, `GLOSSARY.md`,
`BEHAVIOR-EVALS.md`, and `agents/openai.yaml`. Current canonical remains
separate comparison evidence at
`skills/custom/writing-great-skills`, tree
`2a83a9655d1f5f9ff8647d2c9d8fc8a74916b78727b11857bd9bf24e52f364d2`.

## Frozen fixture and protocol identities

- Worker fixture:
  `.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/fixtures/prompt4/worker-fixture.json`,
  SHA-256
  `c59c5afa04328c341c28eb721299e016dce84f3bde019ae6c82c2a42947fd518`
- Root evaluator and fixture-lint map:
  `.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/fixtures/prompt4/root-evaluator.json`,
  SHA-256
  `afbf11f0492db03135d39ed62031e03b3ddb61a3ccad0204f9c5ed6cc9e9f39b`
- Protocol:
  `.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/protocol/prompt4/protocol-manifest.json`,
  SHA-256
  `817580f9c860812673a794e3f9fd598cebd5849576b578ad5a8360c27569a8ba`
- Candidate record:
  `.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/candidate.json`,
  SHA-256
  `d9f14f8ec62781fc1d35c7758c0e289d8cb6c9c6c18269011a455a0edac0a811`
- Resolved `EP-CLEAR-01` arm pair shared-payload SHA-256:
  `c2c9320594c5c93dc6425185fb3899cfd8bd7fad9abc274bfdacaca2ab3a8b4c`

The worker fixture contains nine cases: six entry-positive cases across
clear-margin and borderline-variable families, plus deterministic-structural,
no-control-deficit, and nontriggering wrong-condition cases. Candidate terms,
the hypothesis, expected M0 weakness, rubric, scoring, prior outputs, and
conclusions remain root-only.

## Proof registration and construction evidence

M0 viability proof IDs are `V01` through `V10`. The H1 contribution control is
`H1-CTL-01`; its wrong-condition preservation obligation is `H1-WC-01`.
Protected behavior and focused proof use `INV-01`, `AUTH-01`, `COV-01`,
`CUT-01`, `RET-01`, `HEAD-01`, `REL-01` through `REL-04`, `CTX-01`,
`CTX-02`, `MACH-01`, `MACH-02`, `ISO-01`, `ABS-ALL`, and `MD-01`.

Construction verification passed with 41 mapped M0 instruction passages, two
classified H1 delta passages, all nine M0 semantic units, the one admitted H1
unit, all 15 executable full-package forbidden-semantic checks, nine fixture
cases, worker/root separation, fixture-lint referential and output coverage,
and payload equality outside `/runtime`.

`python -m scripts.campaign_artifacts lint-fixture` passed with nine cases.
`python -m scripts.campaign_artifacts compare-payloads` passed for the resolved
`EP-CLEAR-01` pair. The campaign verifier passed exact inventories, file
hashes, tree hashes, passage selectors, semantic ownership, one-file arm
delta, absence checks, pointer and policy compatibility, fixture isolation,
and Markdown gates. Repository skill validation and both diff checks are
recorded in the final read-back after this decision capsule freezes.

## Residual gaps

- M0 behavioral viability has not been sampled.
- H1 contribution, stop/extend calibration, and wrong-condition preservation
  have not been sampled.
- Live-host implicit discovery remains unproved.
- Exact model-build, sampler seed, token, and latency telemetry may remain
  unavailable.
- Any later behavioral conclusion is limited to the frozen runtime, fixture,
  task, model, host, reasoning, tools, authority, evidence, rubric, and sample
  identities.

## Shared Run Contract

Authorized unit completed: Deploy Prompt 3 for `writing-great-skills`

Decision: `ready-for-prompt-4`

Campaign shape: `hypothesis-candidate`

Runtime identities: current
`2a83a9655d1f5f9ff8647d2c9d8fc8a74916b78727b11857bd9bf24e52f364d2`;
M0 `559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032`;
H1 `1021d8c5d9d20a81e4ab33a0b014cf71826b818a02153041b7845aac245cf553`

Artifacts changed: campaign subtree
`.scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/**` and this
Prompt 3 transcript only

Evidence used or reused: exact Prompt 1 M0 checkpoint; exact research and
Prompt 2 identities; current canonical as comparison-only structural evidence;
fresh construction verifier, fixture lint, resolved payload comparison,
Markdown gates, skill validation, diff checks, scoped status, and HEAD
read-back

Residual gaps: candidate-owned behavioral viability and contribution evidence,
live-host implicit discovery, unavailable exact telemetry, and transfer beyond
the frozen execution identities

Recommended next unit: Prompt 4

Git HEAD: `55dd6818182caf75e85de713a13ed76996336a27` ->
`55dd6818182caf75e85de713a13ed76996336a27`

Git delivery: pending

Exact stop reason: Prompt 3 froze exact M0 and H1 packages plus uncontaminated
Prompt 4 fixtures and stopped before behavioral sampling.

<!-- END PROMPT3 DECISION -->
